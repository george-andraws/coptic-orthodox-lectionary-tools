"""George's Mesra 19 override is source-qualified, not Reader verification."""
import copy
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build_lectionary_reference as core
import build_design_deliverables as design
from passage_normalization import passage_matches


class Mesra19UserCorrection(unittest.TestCase):
    def table(self):
        _, rows = core.parse_copticchurch_html(
            (ROOT / 'cache/copticchurch_html/2023-08-25.html').read_text(), dt.date(2023, 8, 25))
        self.assertEqual(len(rows), 9)
        self.assertEqual({r['day_title'] for r in rows}, {'Mesra 19'})
        return rows

    def test_actual_html_date_index_corrects_james_and_preserves_raw_source(self):
        rows = self.table()
        catholic = next(r for r in rows if r['reading_type'] == 'Catholic Epistle')
        self.assertEqual(catholic['raw_ref'], 'Jm 1:1-12')
        self.assertEqual(catholic['normalized_ref'], 'James 1:12-21')
        self.assertEqual(catholic['parse_status'], 'source_corrected')
        self.assertIn('george_user-supplied_correction', catholic['normalization_warning'])
        self.assertNotIn('verified_date=', catholic['normalization_warning'])
        indexed = core.build_date_passage_index(rows)
        hit = [r for r in indexed if r['reading_type'] == 'Catholic Epistle']
        self.assertEqual([r['matched_ref'] for r in hit], ['James 1:12-21'])
        self.assertTrue(passage_matches('James 1:20', hit[0]['matched_ref']))
        self.assertFalse(passage_matches('James 1:1', hit[0]['matched_ref']))

    def test_exact_context_source_and_lifecycle_negatives(self):
        row = next(r for r in self.table() if r['reading_type'] == 'Catholic Epistle')
        row.update(normalized_ref='Jm 1:1-12', parse_status='ok', normalization_warning='')
        for changes in ({'day_title':'Mesra 18'}, {'day_title':'Mesra 20'},
                        {'service_section':'Matins'}, {'reading_type':'Pauline Epistle'},
                        {'raw_ref':'Jm 1:1-18'}, {'raw_ref':'James 1:1-12'},
                        {'source':'unverified source'}, {'url':'https://example.com/readings'},
                        {'active':False}, {'status':'removed'}, {'state':'inactive'},
                        {'include_in_current_index':False}, {'superseded_reason':'retained history'}):
            with self.subTest(changes=changes):
                negative = dict(row, **changes)
                self.assertEqual(core.apply_copticchurch_source_correction(negative), negative)
        corrected = core.apply_copticchurch_source_correction(row)
        self.assertEqual(corrected['normalized_ref'], 'James 1:12-21')
        self.assertEqual(core.apply_copticchurch_source_correction(corrected), corrected)
        self.assertEqual(row['normalized_ref'], 'Jm 1:1-12')

    def test_all_cached_mesra_dates_and_other_eight_slots_preserved(self):
        dates = []
        with (ROOT / 'out/data/copticchurch_date_readings_current_2020_2035.csv').open() as f:
            dates = sorted({r['gregorian_date'] for r in csv.DictReader(f) if r['day_title']=='Mesra 19'})
        self.assertEqual(len(dates), 14)
        key = core.correction_key('Mesra 19', 'Liturgy', 'Catholic Epistle', 'Jm 1:1-12')
        for date in dates:
            with self.subTest(date=date):
                html = (ROOT / 'cache/copticchurch_html' / (date + '.html')).read_text()
                _, actual = core.parse_copticchurch_html(html, dt.date.fromisoformat(date))
                rules = dict(core.COPTICCHURCH_SOURCE_CORRECTIONS)
                rules.pop(key, None)
                with patch.object(core, 'COPTICCHURCH_SOURCE_CORRECTIONS', rules):
                    _, baseline = core.parse_copticchurch_html(html, dt.date.fromisoformat(date))
                self.assertEqual(len(actual), 9)
                self.assertEqual([r for r in actual if r['reading_type']!='Catholic Epistle'],
                                 [r for r in baseline if r['reading_type']!='Catholic Epistle'])
                hit = [r for r in core.build_date_passage_index(actual) if r['reading_type']=='Catholic Epistle']
                self.assertEqual([r['matched_ref'] for r in hit], ['James 1:12-21'])

    def test_fixture_and_versioned_ledger_are_authenticated_without_rewriting_history(self):
        policy = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())
        relative = 'sources/user-corrections/mesra-19-james.json'
        fixture = json.loads((ROOT / relative).read_text())
        self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), policy['source_fingerprints'][relative])
        self.assertEqual(fixture['literal_user_instruction'], 'correction: Mesra 19 reading needs to be James 1:12-21')
        self.assertEqual(fixture['authority'], 'George user-supplied correction')
        for name, expected in fixture['source_fingerprints'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected)
        witness = fixture['existing_cycle_witness']
        self.assertEqual(hashlib.sha256((ROOT / witness['path']).read_bytes()).hexdigest(), witness['sha256'])
        self.assertEqual(witness['row']['C_Gospel_Ref'], '59.1:12-21')
        new = json.loads((ROOT / policy['seasonal_reverse_index_contract']).read_text())
        lineage = new['lineage']
        oldpath = ROOT / lineage['previous_contract']
        self.assertEqual(hashlib.sha256(oldpath.read_bytes()).hexdigest(), lineage['previous_contract_sha256'])
        old = json.loads(oldpath.read_text())
        before = {tuple(k) for k in old['intended_keys']}
        after = {tuple(k) for k in new['intended_keys']}
        expected_old = ('Mesra 19', 'Liturgy', '', 'Catholic Epistle', 'rid_6d8a99da1f1ae35aa028')
        expected_new = expected_old[:4] + ('rid_663541d046c596982394',)
        self.assertEqual(before - after, {expected_old})
        self.assertEqual(after - before, {expected_new})
        self.assertEqual(len(after), len(before))
        # Real whole-key contract guard, without reading or regenerating output counts.
        rows = [dict(occasion=k[0], service_section=k[1], service_hour=k[2], slot=k[3], identity_key=k[4]) for k in after]
        design.verify_reverse_index_contract(rows)
        with self.assertRaises(AssertionError):
            design.verify_reverse_index_contract(rows[:-1])

    def test_loader_rejects_unbound_user_instruction_endpoint_and_evidence(self):
        import tempfile
        policy = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())
        original = next(r for r in policy['copticchurch_date'] if r['authority']=='George user-supplied correction')
        for changes in ({'corrected_ref':'James 1:12-20'}, {'user_instruction':'invented verification'},
                        {'evidence':'../outside.json'}):
            with self.subTest(changes=changes), tempfile.TemporaryDirectory() as directory:
                source = Path(directory)
                payload = dict(policy, copticchurch_date=[dict(original, **changes)])
                (source / 'lectionary_corrections.json').write_text(json.dumps(payload))
                with patch.object(core, 'SRC', source), self.assertRaises(RuntimeError):
                    core.load_coptic_reader_corrections()
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            payload = dict(policy, copticchurch_date=[original], source_fingerprints=dict(policy['source_fingerprints']))
            payload['source_fingerprints'][original['evidence']] = '0' * 64
            (source / 'lectionary_corrections.json').write_text(json.dumps(payload))
            with patch.object(core, 'SRC', source), self.assertRaises(RuntimeError):
                core.load_coptic_reader_corrections()

    def test_complete_existing_date_corpus_has_only_fourteen_surgical_mutations(self):
        key = core.correction_key('Mesra 19', 'Liturgy', 'Catholic Epistle', 'Jm 1:1-12')
        with (ROOT / 'out/data/copticchurch_date_readings_current_2020_2035.csv').open() as stream:
            corpus = list(csv.DictReader(stream))
        changes = []
        # Reset only the explicit conflicting source value so this remains a
        # regression after the parent regenerates the current CSV.
        for row in corpus:
            if (row['day_title'], row['service_section'], row['reading_type'], row['raw_ref']) == ('Mesra 19', 'Liturgy', 'Catholic Epistle', 'Jm 1:1-12'):
                row.update(normalized_ref='Jm 1:1-12', parse_status='ok', normalization_warning='')
        with patch.object(core, 'COPTICCHURCH_SOURCE_CORRECTIONS', {key:core.COPTICCHURCH_SOURCE_CORRECTIONS[key]}), patch.object(core, 'SUPPRESSED_DATE_CONTEXTS', {}):
            for row in corpus:
                result = core.apply_copticchurch_source_correction(row)
                if result != row:
                    changes.append((row, result))
        self.assertEqual(len(changes), 14)
        for before, after in changes:
            self.assertEqual(before['day_title'], 'Mesra 19')
            self.assertEqual(before['raw_ref'], 'Jm 1:1-12')
            self.assertEqual(after['normalized_ref'], 'James 1:12-21')
            self.assertEqual({k:v for k,v in before.items() if k not in ('normalized_ref','parse_status','normalization_warning')},
                             {k:v for k,v in after.items() if k not in ('normalized_ref','parse_status','normalization_warning')})

    def test_real_daily_and_reverse_helpers_emit_current_corrected_membership(self):
        inputs = []
        for i, r in enumerate(core.build_date_passage_index(self.table())):
            identity = design.identity_for(r['matched_ref'], 'copticchurch_date')
            inputs.append(dict(r, **identity, occasion=r['day_title'], slot=r['reading_type'],
                               source_kind='copticchurch_date', source_family='ordinary_date_resolved',
                               source_row_id=str(i), current_status='current_working_source_not_coptic_reader_checked'))
        frozen = copy.deepcopy(inputs)
        daily = design.build_daily_year_files(inputs)[2023]['2023-08-25']
        self.assertEqual([r['display_ref'] for r in daily if r['slot_type']=='catholicon'], ['James 1:12-21'])
        # Whole-corpus contract is separately authenticated; this helper probe is nine slots only.
        with patch.object(design, 'verify_reverse_index_contract'):
            reverse, _ = design.build_reverse_lectionary_index(inputs)
        hits = [r for r in reverse if r['slot']=='Catholic Epistle']
        self.assertEqual([r['display_ref'] for r in hits], ['James 1:12-21'])
        self.assertTrue(all(design.is_current_presentation(r) for r in hits))
        self.assertEqual(inputs, frozen)


if __name__ == '__main__':
    unittest.main()
