"""Bounded archive lane: real raw -> crosswalk -> presentation -> npm predicate."""
import base64
import hashlib
import tempfile
import zlib
import copy
import csv
import json
import io
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import build_lectionary_reference as reference
import build_lectionary_crosswalk as crosswalk
import build_design_deliverables as design

ROOT = Path(__file__).resolve().parents[1]


def retained():
    with (ROOT / 'out/data/copticchurch_date_readings_2020_2035.csv').open() as stream:
        return [r for r in csv.DictReader(stream)
                if r.get('superseded_reason') == 'coptic_reader_no_service']


class NoServiceHistory(unittest.TestCase):
    def test_raw_archive_pipeline_and_current_exclusion(self):
        raw = retained()
        self.assertEqual(len(raw), 32)
        self.assertEqual(reference.build_date_passage_index(raw), [])
        projected = crosswalk.project_no_service_history(raw)
        self.assertEqual(len(projected), 32)
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=crosswalk.FIELDS)
        writer.writeheader(); writer.writerows(projected); buffer.seek(0)
        projected = list(csv.DictReader(buffer))
        presentation, _ = design.build_reverse_presentation(projected)
        self.assertTrue(all(not design.is_current_presentation(r) for r in presentation))
        # The authenticated archive must be declared, without implying alignment.
        self.assertEqual({r['source_convention'] for r in presentation},
                         {'unapproved_original_source_literal'})
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(design, 'OUT', Path(directory)):
                schema = design.write_schema()
        self.assertIn('unapproved_original_source_literal',
                      schema['controlled_vocabularies']['source_convention'])
        daily = design.build_daily_year_files(presentation, transport_mode='presentation')
        self.assertFalse(any(rows for year in daily.values() for rows in year.values()))
        expected = json.loads((Path(__file__).with_name('fixtures') / 'no-service-history-keys.json').read_text())['added_keys']
        def subset(rows):
            self.assertEqual(sorted([list(design.occasion_index_key(r)) for r in rows]), expected)
        with patch.object(design, 'verify_reverse_index_contract', side_effect=subset):
            reverse, disagreements = design.build_reverse_lectionary_index(presentation, transport_mode='presentation')
        self.assertEqual(len(reverse), 18)
        self.assertEqual(disagreements, [])
        self.assertEqual(sum(int(r['collapsed_row_count']) for r in reverse), 32)
        luke, = [r for r in reverse if r['display_ref'] == 'Lk 10:38-52']
        self.assertEqual(luke['removed_marker'], 'removed_by_coptic_reader_no_service')
        for row in reverse:
            self.assertEqual((row['canonical_mt_ref'], row['canonical_lxx_ref'], row['spans_json']), ('', '', '[]'))
            self.assertIn('84aa373f8bad6f8420d63792103752195818e316c6823d81e7575889e6e8fc4f', row['source_locator'])
        script = "const a=require('./packages/lectionary-data');let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{const r=JSON.parse(s);if(r.some(a.isCurrentReading))process.exit(1);console.log(r.length)})"
        result = subprocess.run(['node', '-e', script], cwd=ROOT, input=json.dumps(reverse), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), '18')
        design.verify_source_plan_qualifications(reverse, {})
        for field, value in [('current_status', 'current_public_or_local_reference'),
                             ('removed_marker', ''), ('canonical_mt_ref', 'Lk 10:38-42'),
                             ('spans_json', '[{"book":"Lk","chapter_start":10}]'),
                             ('occasion', 'Great Lent'), ('source_disclosure', '[]'),
                             ('provenance', '{}'), ('source_locator', 'forged')]:
            forged = copy.deepcopy(reverse)
            forged[0][field] = value
            with self.subTest(reverse_field=field), self.assertRaises((ValueError, AssertionError)):
                design.verify_source_plan_qualifications(forged, {})
        forged = copy.deepcopy(reverse)
        for key in ('source_family', 'source_kind', 'source_locator', 'provenance', 'source_disclosure', 'removed_marker'):
            forged[0][key] = ''
        forged[0]['current_status'] = 'current_public_or_local_reference'
        with self.assertRaises(ValueError):
            design.verify_source_plan_qualifications(forged, {})
        # Exercise the real current release gate, without an 18-row-only shortcut.
        # Its domain may later be amended; the historical refusal remains pinned
        # in test_authenticated_predecessor_complete_domain_expected_block.
        existing = [json.loads(line) for line in (ROOT / 'out/design/reverse_lectionary_index.jsonl').read_text().splitlines()]
        fixture = json.loads((Path(__file__).with_name('fixtures') / 'no-service-history-keys.json').read_text())
        old = json.loads(zlib.decompress(base64.b85decode(fixture['predecessor_contract_zlib_base85'])))
        old_keys = set(map(tuple, old['intended_keys']))
        joined = [r for r in existing if design.occasion_index_key(r) in old_keys] + reverse
        policy = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())
        live = json.loads((ROOT / policy['seasonal_reverse_index_contract']).read_text())
        if set(map(tuple, live['intended_keys'])) == old_keys:
            with self.assertRaisesRegex(AssertionError, 'expected=12168 actual=12186 missing=0 extra=18'):
                design.verify_reverse_index_contract(joined)
        else:
            self.assertEqual(set(map(tuple, live['intended_keys'])), old_keys | set(map(tuple, expected)))
            design.verify_reverse_index_contract(joined)

    def archive_rows(self):
        presentation, _ = design.build_reverse_presentation(crosswalk.project_no_service_history(retained()))
        expected = json.loads((Path(__file__).with_name('fixtures') / 'no-service-history-keys.json').read_text())['added_keys']
        def subset(rows):
            self.assertEqual(sorted(list(design.occasion_index_key(r)) for r in rows), expected)
        # Only corpus membership is isolated; real qualification is called below.
        with patch.object(design, 'verify_reverse_index_contract', side_effect=subset):
            reverse, _ = design.build_reverse_lectionary_index(presentation, transport_mode='presentation')
        design.verify_source_plan_qualifications(reverse, {})
        return presentation, reverse

    def test_same_identity_marker_stripping_is_refused_at_real_boundaries(self):
        presentation, reverse = self.archive_rows()
        # Reviewer's EXACT all-32 mutant, then stronger compound marker/state mutant.
        for compound in (False, True):
            forged = copy.deepcopy(presentation)
            for row in forged:
                for key in ('source_family', 'source_row_id', 'provenance', 'superseded_reason', 'removed_marker'):
                    row[key] = ''
                row['current_status'] = 'current_public_or_local_reference'
                if compound:
                    row.update(source_kind='', active=True, status='current', runtime_activation_approved=True)
            self.assertEqual({r['identity_key'] for r in forged}, {r['identity_key'] for r in presentation})
            for caller in (design.build_daily_year_files, design.build_reverse_lectionary_index, design.build_reverse_presentation):
                with self.subTest(compound=compound, caller=caller.__name__), self.assertRaises(ValueError):
                    if caller == design.build_reverse_presentation:
                        caller(forged)
                    else:
                        caller(forged, transport_mode='presentation')
            self.assertFalse(any(design.is_current_presentation(row) for row in forged))
        forged = copy.deepcopy(reverse)
        for row in forged:
            row.update(source_family='', source_kind='', removed_marker='', provenance='', source_disclosure='',
                       active=True, status='current', runtime_activation_approved=True,
                       current_status='current_public_or_local_reference')
        with self.assertRaises(ValueError):
            design.verify_source_plan_qualifications(forged, {})

    def test_reverse_context_nonapproval_and_transport_types_fail_closed(self):
        presentation, reverse = self.archive_rows()
        mutations = [('calendar_keys', 'Great Lent'), ('day_titles', 'Great Lent'),
                     ('active', True), ('status', 'current'), ('runtime_activation_approved', True),
                     ('active', 0), ('active', 'false'), ('runtime_activation_approved', 0),
                     ('runtime_activation_approved', 'False'), ('source_disclosure_count', 1),
                     ('collapsed_row_count', True), ('spans_json', []), ('canonical_mt_ref', None)]
        for field, value in mutations:
            forged = copy.deepcopy(reverse); forged[0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                design.verify_source_plan_qualifications(forged, {})
        for field, value in [('source_order', True), ('source_token_order', 1), ('active', 0),
                             ('runtime_activation_approved', 'False'), ('source_disclosure', {})]:
            forged = copy.deepcopy(presentation); forged[0][field] = value
            for caller in (design.build_daily_year_files, design.build_reverse_lectionary_index):
                with self.subTest(field=field, caller=caller.__name__), self.assertRaises(ValueError):
                    caller(forged, transport_mode='presentation')

    def test_authenticated_predecessor_complete_domain_expected_block(self):
        fixture = json.loads((Path(__file__).with_name('fixtures') / 'no-service-history-keys.json').read_text())
        contract_bytes = zlib.decompress(base64.b85decode(fixture['predecessor_contract_zlib_base85']))
        self.assertEqual(hashlib.sha256(contract_bytes).hexdigest(),
                         '739d6374050db17be77b9afc73ff243a3bcc2b27d0fcfeaeed6e976935f0d28d')
        policy_bytes = zlib.decompress(base64.b85decode(fixture['predecessor_policy_zlib_base85']))
        self.assertEqual(hashlib.sha256(policy_bytes).hexdigest(), fixture['predecessor_policy_sha256'])
        old = json.loads(contract_bytes); old_keys = set(map(tuple, old['intended_keys']))
        self.assertEqual(len(old_keys), 12168)
        _, reverse = self.archive_rows()
        added = set(map(tuple, fixture['added_keys']))
        existing = [json.loads(line) for line in (ROOT / 'out/design/reverse_lectionary_index.jsonl').read_text().splitlines()]
        predecessor = [r for r in existing if design.occasion_index_key(r) in old_keys]
        before = copy.deepcopy(predecessor)
        self.assertEqual(len(predecessor), 12168)
        self.assertEqual({design.occasion_index_key(r) for r in predecessor}, old_keys)
        joined = predecessor + reverse
        actual = {design.occasion_index_key(r) for r in joined}
        self.assertEqual(old_keys - actual, set())
        self.assertEqual(actual - old_keys, added)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy_path = root / 'sources/lectionary_corrections.json'
            policy_path.parent.mkdir(parents=True); policy_path.write_bytes(policy_bytes)
            contract_path = root / json.loads(policy_bytes)['seasonal_reverse_index_contract']
            contract_path.parent.mkdir(parents=True, exist_ok=True); contract_path.write_bytes(contract_bytes)
            with patch.object(design, 'ROOT', root):
                with self.assertRaisesRegex(AssertionError, 'expected=12168 actual=12186 missing=0 extra=18'):
                    design.verify_reverse_index_contract(joined)
        self.assertEqual(predecessor, before)

    def test_wrong_raw_context_or_lifecycle_fails_closed(self):
        import no_service_history as history
        original = retained()[0]
        for field, value in [('gregorian_date','2020-02-11'), ('day_title','Great Lent'),
                             ('service_section','Matins'), ('source_family','jonah_fast_source_qualified'),
                             ('source_kind','jonah_fast_date_supplement'), ('raw_ref','Lk 22:24-31'),
                             ('current_status','current_public_or_local_reference'), ('active','True')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                crosswalk.project_no_service_history([dict(original, **{field:value})])
        with patch.object(history, 'CAPTURE_SHA256', '0'*64), self.assertRaises(ValueError):
            crosswalk.project_no_service_history([original])

    def test_projected_and_presentation_activation_replays_fail(self):
        projected = crosswalk.project_no_service_history(retained()[:1])
        for field, value in [('gregorian_date','2020-02-11'), ('source_family','ordinary_date_resolved'),
                             ('source_kind','katameros_cycle'), ('service_section','Matins'),
                             ('passage','Lk 22:24-31'), ('superseded_reason',''), ('active',True)]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                design.build_reverse_presentation([dict(projected[0], **{field:value})])
        presentation, _ = design.build_reverse_presentation(projected)
        corrupted = copy.deepcopy(projected[0])
        proof = json.loads(corrupted['provenance'])
        proof['consumer_source_transport']['no_service_archive']['capture_sha256'] = '0'*64
        corrupted['provenance'] = json.dumps(proof)
        with self.assertRaises(ValueError):
            design.build_reverse_presentation([corrupted])
        for field, value in [('current_status','current_public_or_local_reference'), ('removed_marker',''),
                             ('canonical_mt_ref','Lk 22:24-30'), ('source_family','other')]:
            forged = [dict(presentation[0], **{field:value})]
            for caller in [design.build_reverse_lectionary_index, design.build_daily_year_files]:
                with self.subTest(field=field, caller=caller.__name__), self.assertRaises(ValueError):
                    caller(forged, transport_mode='presentation')


if __name__ == '__main__':
    unittest.main()
