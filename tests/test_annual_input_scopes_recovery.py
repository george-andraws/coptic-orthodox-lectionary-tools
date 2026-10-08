"""Compatibility scopes are complete authenticated projections, never count bypasses."""
import copy
import json
import unittest
from reading_context_overlays import repair_table, load_fixture
from test_annual_source_contexts import captured_table, FIXTURE

class AnnualInputScopes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load_fixture(FIXTURE)
        cls.snapshots = json.loads((FIXTURE / 'snapshots.json').read_text())

    def compared(self, ident):
        capture = next(c for c in self.fixture['oracle'] if c['id'] == f'AnnualReadings-{ident}')
        snap = next(s for s in self.snapshots if s['id'] == capture['id'] and s['layer'] == 'current_date_source')
        return capture, [dict(s['actual_rows'][0], slot=s['slot']) for s in snap['nonPsalm_slots']]

    def test_six_compared_and_nine_whole_tables_match_all_seven_contexts(self):
        for ident in (16,17,19,26,54,57,59):
            c,six = self.compared(ident)
            _,nine = captured_table(self.fixture,ident)
            a = repair_table(c['context'],six,self.fixture,'date_source')
            b = repair_table(c['context'],nine,self.fixture,'date_source')
            self.assertEqual(len(a['active']),6)
            self.assertEqual(len(b['active']),9)
            self.assertEqual([(r['slot'],r['normalized_ref']) for r in a['active']],
                             [(r['slot'],r['normalized_ref']) for r in b['active'] if r['reading_type'] != 'Psalm'])

    def test_each_scope_rejects_missing_duplicate_reordered_nonrepair_wrongbook(self):
        for ident in (16,17,19,26,54,57,59):
            for c,table in (self.compared(ident),captured_table(self.fixture,ident)):
                for mutation in ('missing','duplicate','order','wrongbook','unknown'):
                    bad=copy.deepcopy(table)
                    if mutation=='missing': bad.pop(next(i for i,r in enumerate(bad) if r['slot']=='liturgy_acts'))
                    if mutation=='duplicate': bad.append(copy.deepcopy(bad[-1]))
                    if mutation=='order': bad.reverse()
                    if mutation=='wrongbook': next(r for r in bad if r['slot']=='vespers_gospel').update(raw_ref='Jn 1:1',normalized_ref='Jn 1:1')
                    if mutation=='unknown': bad[-1]['slot']='unknown'
                    with self.subTest(id=ident,scope=len(table),mutation=mutation),self.assertRaises(ValueError):
                        repair_table(c['context'],bad,self.fixture,'date_source')

    def test_all_four_james_supplements_in_both_scopes_bound_provenance_allowlist_idempotent(self):
        for ident in (26,54,57,59):
            for c,table in (self.compared(ident),captured_table(self.fixture,ident)):
                missing=[r for r in table if r['slot']!='liturgy_catholic']
                missing[0]['anchor_payload']='do not inherit'
                once=repair_table(c['context'],missing,self.fixture,'date_source')
                added=next(r for r in once['active'] if r['slot']=='liturgy_catholic')
                rule=next(r for r in self.fixture['repairs'] if r['id']==c['id'] and r['slot']=='liturgy_catholic')
                doc=next(d for d in c['documents'] if rule['printed_ref'] in d['printedReferences'])
                self.assertEqual(added['raw_ref'],rule['printed_ref'])
                self.assertEqual(added['source_context'],c['context'])
                self.assertEqual((added['source_evidence'],added['source_sha256']),(doc['textPath'],doc['textSha256']))
                self.assertNotIn('anchor_payload',added)
                self.assertEqual(repair_table(c['context'],once['active'],self.fixture,'date_source'),dict(active=once['active'],history=[],events=[]))

    def test_replayed_supplement_cannot_forge_raw_provenance(self):
        c,table=self.compared(26)
        once=repair_table(c['context'],[r for r in table if r['slot']!='liturgy_catholic'],self.fixture,'date_source')
        for key,value in (('source_context',{}),('source_evidence','unbound.txt'),('source_sha256','0'*64),('source_printed_ref','James 1:1'),('source_order',999),('source_kind','unverified')):
            bad=copy.deepcopy(once['active'])
            next(r for r in bad if r['slot']=='liturgy_catholic')[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError): repair_table(c['context'],bad,self.fixture,'date_source')

    def test_short_cycle_vector_is_exactly_bound_not_optional_full_schema(self):
        c=next(c for c in self.fixture['oracle'] if c['id']=='AnnualReadings-16')
        vector=[dict(slot='liturgy_catholic',service_section='Liturgy',raw_ref='60.2:1-10',normalized_ref='1Pet 2:1-10')]
        once=repair_table(c['context'],vector,self.fixture,'cycle')
        self.assertEqual(once['active'][0]['numeric_ref'],'60.1:25-2:10')
        self.assertEqual(once['history'][0]['raw_ref'],'60.2:1-10')
        self.assertEqual(repair_table(c['context'],once['active'],self.fixture,'cycle')['events'],[])
        for key,value in (('source_table','AnnualReadings'),('raw_ref','61.2:1-10'),('normalized_ref','2Pet 2:1-10'),('numeric_ref','60.1:24-2:10'),('current_status','removed')):
            bad=copy.deepcopy(vector);bad[0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError): repair_table(c['context'],bad,self.fixture,'cycle')

    def test_supported_current_statuses_remain_current_and_unknown_kind_rejects_even_neighbor(self):
        c,t=self.compared(16)
        for status in ('current','active','current_confirmed_coptic_reader','current_confirmed_by_fixture_equivalence','current_public_or_local_reference','current_working_source_not_coptic_reader_checked','pending_psalm_equivalence_unresolved','unknown'):
            rows=[dict(r,current_status=status) for r in t]
            self.assertEqual(len(repair_table(c['context'],rows,self.fixture,'date_source')['active']),6)
        with self.assertRaises(ValueError): repair_table(dict(c['context'],date='2099-01-01'),t,self.fixture,'unknown')

if __name__ == '__main__': unittest.main()
