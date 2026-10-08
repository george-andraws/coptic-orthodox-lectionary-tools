"""Primary-source oracle, generic seasonal plumbing, no full builder or package writes."""
import copy
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_reference as ref
import build_lectionary_crosswalk as crosswalk
import build_design_deliverables as design
import verify_design_deliverables as validator
from scripts import compare_external_sources as compare
from calendar_resolution import resolve_current_date_rows, julian_pascha_gregorian
from passage_normalization import canonicalize_text_ref, parse_passage

ROOT=Path(__file__).resolve().parents[1]
POLICY=json.loads((ROOT/'sources/lectionary_corrections.json').read_text())
RULES=POLICY['recurring_date_supplements']

def parse(date):
    date=dt.date.fromisoformat(date)
    return ref.parse_copticchurch_html((ROOT/'cache/copticchurch_html'/f'{date}.html').read_text(),date)[1]

class SeasonalIntegration(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.patcher=patch.object(ref,'DATA',Path(self.directory.name))
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_qualified_source_table_exactly_once_and_full_span(self):
        for rule in RULES:
            with self.subTest(date=rule['verified_date']):
                ref.authenticate_recurring_supplement(rule,POLICY)
                primary=[line.strip() for line in (ROOT/rule['evidence']).read_text().splitlines() if line.startswith('\t')]
                rows=parse(rule['verified_date'])
                actual=[r for r in rows if r['source']=='Coptic Reader verified recurring supplement']
                self.assertEqual([r['raw_ref'] for r in actual],primary)
                self.assertEqual([r['normalized_ref'] for r in actual],[canonicalize_text_ref(p) for p in primary])
                self.assertEqual([r['source_slot'] for r in actual],[f'OT{i}' for i in range(1,len(primary)+1)])
                index=ref.build_date_passage_index(actual)
                self.assertEqual(len(index),len(primary))
                for item,printed in zip(index,primary):
                    self.assertEqual(parse_passage(item['matched_ref']),parse_passage(printed))
                projected=crosswalk.project_date_rows(index)
                self.assertEqual(len(projected),len(primary))
                for item in projected:
                    key=design.source_key_for(item)
                    self.assertTrue(design.source_registry_for_key(key))
                    self.assertEqual(design.source_registry_for_key(key)['default_locator'],rule['evidence'])

    def test_missing_duplicate_reordered_endpoint_wrong_capture_rejected(self):
        original=RULES[1]
        for mutation in ['missing','duplicate','reorder','endpoint','capture','offset','slot','sourcehash','contexthash']:
            rule=copy.deepcopy(original)
            if mutation=='missing': rule['readings'].pop()
            elif mutation=='duplicate': rule['readings'].append(copy.deepcopy(rule['readings'][0]))
            elif mutation=='reorder': rule['readings'].reverse()
            elif mutation=='endpoint': rule['readings'][0]['normalized_ref']='Exod 3:6-13'
            elif mutation=='capture': rule['verified_date']='2026-02-24'
            elif mutation=='offset': rule['pascha_offset_days']+=1
            elif mutation=='slot': rule['readings'][0]['source_slot']='OT99'
            elif mutation=='sourcehash': rule['evidence']='../outside.txt'
            else: rule['evidence_fingerprints'][next(k for k in rule['evidence_fingerprints'] if k.endswith('context.txt'))]='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(RuntimeError):
                ref.authenticate_recurring_supplement(rule,POLICY)

    def test_generic_crosswalk_boundary_is_authority_and_history_inactive(self):
        current=resolve_current_date_rows(parse('2028-04-07'),[])
        index=ref.build_date_passage_index(current)
        projected=crosswalk.project_date_rows(index)
        self.assertEqual(len(projected),11)
        self.assertTrue(all(r['source_family']=='coptic_reader_verified_calendar_boundary' for r in projected))
        self.assertTrue(all(r['source_file'].endswith('verified-table.json') for r in projected))
        history=crosswalk.displaced_date_history(ref.build_date_passage_index(parse('2028-04-07')),index)
        self.assertTrue(history)
        for row in crosswalk.project_date_rows(history):
            ident=design.identity_for(row['passage'],row['source_kind'])
            self.assertEqual(design.status_for(row,ident,set())[0],'historical_candidate_removed')
            self.assertTrue(design.removed_marker_for(row,ident))
        self.assertFalse(crosswalk.displaced_date_history(ref.build_date_passage_index(parse('2027-04-07')),ref.build_date_passage_index(parse('2027-04-07'))))

    def test_independent_daily_oracle_rejects_corruption(self):
        for date in ['2026-02-23','2028-04-07']:
            source=ref.build_date_passage_index(resolve_current_date_rows(parse(date),[]))
            projected=crosswalk.project_date_rows(source)
            presentation=[]
            for row in projected:
                ident=design.identity_for(row['passage'],row['source_kind'])
                presentation.append({**row,**ident,'occasion':row['liturgical_place'],'slot':row['reading_slot'] or row['reading_type'],'display_ref':ident['display_ref'],'current_status':design.status_for(row,ident,set())[0],'removed_marker':''})
            daily=design.build_daily_year_files(presentation)[int(date[:4])][date]
            validator.verify_seasonal_daily(source,{date:daily},POLICY)
            counters=compare.contextual_counters(source,{date:daily},int(date[:4]),POLICY)
            self.assertEqual(counters[0],counters[1]); self.assertFalse(counters[4])
            for mutation in ['missing','duplicate','reorder','endpoint','wrongdate','removed','span','slotorder','provenance']:
                damaged=copy.deepcopy(daily); target=date
                pos=next(i for i,r in enumerate(damaged) if r.get('source_family') in {'coptic_reader_verified_supplement','coptic_reader_verified_calendar_boundary'})
                if mutation=='missing': damaged.pop(pos)
                elif mutation=='duplicate': damaged.insert(pos,copy.deepcopy(damaged[pos]))
                elif mutation=='reorder': damaged[pos],damaged[pos+1]=damaged[pos+1],damaged[pos]
                elif mutation=='endpoint': damaged[pos]['display_ref']='Exod 3:6-13'
                elif mutation=='wrongdate': target=date[:8]+'08'
                elif mutation=='span': damaged[pos]['spans_json']='[]'
                elif mutation=='slotorder': damaged[pos]['slot_order']=99
                elif mutation=='provenance': damaged[pos]['source_file']='wrong-source.txt'
                else: damaged[pos]['current_status']='historical_candidate_removed'
                with self.subTest(date=date,mutation=mutation),self.assertRaises(AssertionError):
                    validator.verify_seasonal_daily(source,{target:damaged},POLICY)

    def test_upstream_overlap_wrong_date_title_and_policy_duplicate_fail_closed(self):
        rule=RULES[1]
        date=dt.date.fromisoformat(rule['verified_date'])
        html=(ROOT/'cache/copticchurch_html'/f'{date}.html').read_text()
        injected=html.replace('<h2>Matins</h2>', '<h2>Matins</h2><h4>Prophecy</h4><h5>Exodus 3:6-14</h5>')
        self.assertNotEqual(injected,html)
        with self.assertRaisesRegex(RuntimeError,'overlaps upstream'):
            ref.parse_copticchurch_html(injected,date)
        for altered,target in [(html,date+dt.timedelta(days=1)),(html.replace(rule['day_title'],'Other occasion'),date)]:
            rows=ref.parse_copticchurch_html(altered,target)[1]
            self.assertFalse(any(r['source']=='Coptic Reader verified recurring supplement' for r in rows))
        policy=copy.deepcopy(POLICY)
        policy['recurring_date_supplements'].append(copy.deepcopy(rule))
        path=Path(self.directory.name)/'lectionary_corrections.json'; path.write_text(json.dumps(policy))
        with patch.object(ref,'SRC',path.parent),self.assertRaisesRegex(RuntimeError,'overlaps upstream'):
            ref.parse_copticchurch_html(html,date)

    def test_complete_year_rejects_simultaneously_missing_source_and_daily_date(self):
        dates={r['verified_date'] for r in RULES}
        source=[]
        for date in dates:
            source.extend(ref.build_date_passage_index(parse(date)))
        presentation=[]
        for row in crosswalk.project_date_rows(source):
            ident=design.identity_for(row['passage'],row['source_kind'])
            presentation.append({**row,**ident,'occasion':row['liturgical_place'],'slot':row['reading_slot'] or row['reading_type'],'current_status':design.status_for(row,ident,set())[0],'removed_marker':''})
        daily=design.build_daily_year_files(presentation)[2026]
        validator.verify_seasonal_daily(source,daily,POLICY,complete_year=True)
        omitted=RULES[1]['verified_date']
        del daily[omitted]
        source=[r for r in source if r['gregorian_date']!=omitted]
        with self.assertRaisesRegex(AssertionError,'qualified date inventory changed'):
            validator.verify_seasonal_daily(source,daily,POLICY,complete_year=True)

    def test_enumerated_count_contract_rejects_same_count_substitution_and_duplicates(self):
        contract=json.loads((ROOT/POLICY['seasonal_reverse_index_contract']).read_text())
        rows=[dict(zip(['occasion','service_section','service_hour','slot','identity_key'],key)) for key in contract['intended_keys']]
        design.verify_reverse_index_contract(rows)
        for mutation in ['missing','duplicate','same_count_wrong_identity']:
            damaged=copy.deepcopy(rows)
            if mutation=='missing': damaged.pop()
            elif mutation=='duplicate': damaged[0]=copy.deepcopy(damaged[1])
            else: damaged[0]['identity_key']='rid_'+'0'*20
            with self.subTest(mutation=mutation),self.assertRaises(AssertionError):
                design.verify_reverse_index_contract(damaged)

    def test_cycle_numeric_changes_are_context_bound_and_raw_sqlite_preserved(self):
        cycles=ref.export_cycle_tables(ref.load_books())
        corrections=[r for r in POLICY['katameros_cycle'] if r['verified_date'] in {'2026-02-24','2026-02-25','2026-02-26','2026-02-27','2026-03-03'}]
        self.assertEqual(len(corrections),5)
        for rule in corrections:
            row=next(r for r in cycles if (r['source_table'],r['day_key'],r['reading_slot'])==(rule['source_table'],rule['day_key'],rule['reading_slot']))
            self.assertEqual(row['raw_ref'],rule['expected_raw_ref'])
            self.assertEqual(row['normalized_ref'],rule['corrected_ref'])
            self.assertNotIn((rule['source_table'],rule['day_key']+' wrong','prophecy',rule['expected_raw_ref']),ref.KATAMEROS_CYCLE_CORRECTIONS)
        original=RULES[0]
        index=ref.build_date_passage_index([r for r in parse(original['verified_date']) if r['source']=='Coptic Reader verified recurring supplement'])
        self.assertEqual([r['source_row_id'] for r in crosswalk.project_date_rows(index)], [f'lent-week3-wednesday:2026-03-04:OT{i}' for i in range(1,5)])

    def test_blocked_contexts_remain_unpublished(self):
        staged=POLICY['staged_date_supplements']
        self.assertEqual([s['verified_date'] for s in staged],['2026-03-06','2026-03-10','2026-03-13'])
        for rule in staged:
            self.assertFalse(any(r['source']=='Coptic Reader verified recurring supplement' for r in parse(rule['verified_date'])))
            self.assertTrue(rule['normalization_blockers'])
            self.assertTrue(any(not r['normalized_ref'] for r in rule['readings']))

if __name__=='__main__': unittest.main()
