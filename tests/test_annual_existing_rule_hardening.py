"""Source-derived B1–B5 regression probes; no full builders or generated writes."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_reference as core
from reading_context_overlays import load_fixture, repair_table, is_current_source_row
from test_annual_source_contexts import captured_table, FIXTURE

IDS=(16,17,19,26,54,57,59)

class AnnualExistingHardening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=load_fixture(FIXTURE)

    def test_seven_removed_current_status_tables_reject_without_restoration(self):
        for ident in IDS:
            capture,table=captured_table(self.fixture,ident)
            table[0]['current_status']='removed'
            before=copy.deepcopy(table)
            with self.subTest(id=ident),self.assertRaises(ValueError):
                repair_table(capture['context'],table,self.fixture,'date_source')
            self.assertEqual(table,before)

    def test_seven_nonrepair_wrongbook_samecount_tables_reject(self):
        for ident in IDS:
            capture,table=captured_table(self.fixture,ident)
            r=next(r for r in table if r['slot']=='vespers_gospel')
            r.update(raw_ref='Jn 1:1-5',normalized_ref='Jn 1:1-5')
            with self.subTest(id=ident),self.assertRaises(ValueError):
                repair_table(capture['context'],table,self.fixture,'date_source')

    def test_seven_explicit_unknown_sourcekinds_reject(self):
        for ident in IDS:
            capture,table=captured_table(self.fixture,ident)
            with self.subTest(id=ident),self.assertRaises(ValueError):
                repair_table(capture['context'],table,self.fixture,'unknown')

    def test_benign_unknown_context_is_unchanged(self):
        capture,table=captured_table(self.fixture,16)
        result=repair_table(dict(capture['context'],date='2099-01-01'),table,self.fixture,'date_source')
        self.assertEqual(result,dict(active=table,history=[],events=[]))

    def test_current_status_countercases_reach_real_date_index(self):
        capture,table=captured_table(self.fixture,16)
        target=next(r for r in table if r['slot']=='liturgy_catholic')
        for value in ('removed','superseded','historical','false'):
            with self.subTest(value=value):
                self.assertFalse(is_current_source_row(dict(target,current_status=value)))
                with tempfile.TemporaryDirectory() as tmp,patch.object(core,'DATA',Path(tmp)):
                    self.assertEqual(core.build_date_passage_index([dict(target,current_status=value)]),[])
        self.assertTrue(is_current_source_row(dict(target,current_status='')))
        self.assertTrue(is_current_source_row(dict(target,current_status='current')))
        self.assertFalse(is_current_source_row(dict(target,current_status='current',active=False)))

    def test_cycle_export_numeric_and_actual_index_carry_chapter1_verse25(self):
        rows=core.export_cycle_tables(core.load_books())
        target=[r for r in rows if r['source_table']=='AnnualReadings' and r['day_key']=='Tut 16' and r['reading_slot']=='liturgy_catholic']
        current=[r for r in target if is_current_source_row(r)]
        self.assertEqual(len(current),1)
        self.assertEqual(current[0].get('numeric_ref'),'60.1:25-2:10')
        self.assertEqual(current[0]['raw_ref'],'60.2:1-10')
        self.assertEqual(current[0]['normalized_ref'],'1Pet 1:25-2:10')
        history=[r for r in target if not is_current_source_row(r)]
        self.assertEqual(len(history),1)
        self.assertEqual(history[0]['raw_ref'],'60.2:1-10')
        index=core.build_passage_index(rows,core.load_books())
        indexed=[r for r in index if r['source_table']=='AnnualReadings' and r['day_key']=='Tut 16' and r['service_section']=='liturgy_catholic']
        self.assertEqual([(r['book_abbrev'],r['chapter'],r['verse_start'],r['chapter_end'],r['verse_end']) for r in indexed],[('1Pet',1,25,2,10)])

    def test_cycle_nonrepair_numeric_spoof_and_partial_table_reject(self):
        baseline=json.loads((FIXTURE/'snapshots.json').read_text())
        rows=next(x['actual_context_rows'] for x in baseline if x['id']=='AnnualReadings-16' and x['layer']=='current_cycle')
        bad=copy.deepcopy(rows)
        bad[0]['numeric_ref']='60.1:25-2:10'
        with self.assertRaises(ValueError): core.build_passage_index(bad,core.load_books())
        with self.assertRaises(ValueError): core.build_passage_index(rows[1:],core.load_books())

    def test_all_four_supplements_are_idempotent_with_no_anchor_leak(self):
        for ident in (26,54,57,59):
            capture,table=captured_table(self.fixture,ident)
            table=[r for r in table if r['slot']!='liturgy_catholic']
            for r in table: r['untrusted_anchor']='not a source field'
            once=repair_table(capture['context'],table,self.fixture,'date_source')
            added=next(r for r in once['active'] if r['slot']=='liturgy_catholic')
            self.assertNotIn('untrusted_anchor',added)
            twice=repair_table(capture['context'],once['active'],self.fixture,'date_source')
            self.assertEqual(twice['active'],once['active'])
            self.assertEqual(twice['history'],[])
            self.assertEqual(twice['events'],[])

    def test_psalm_wrongbook_omission_and_context_extra_reject(self):
        capture,table=captured_table(self.fixture,16)
        for mutation in ('psalm','omit','extra','reorder'):
            bad=copy.deepcopy(table)
            if mutation=='psalm': next(r for r in bad if r['reading_type']=='Psalm').update(raw_ref='Jn 1:1',normalized_ref='Jn 1:1')
            if mutation=='omit': bad.pop(0)
            if mutation=='extra': bad.append(copy.deepcopy(bad[0]))
            if mutation=='reorder': bad.reverse()
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                repair_table(capture['context'],bad,self.fixture,'date_source')

if __name__=='__main__': unittest.main()
