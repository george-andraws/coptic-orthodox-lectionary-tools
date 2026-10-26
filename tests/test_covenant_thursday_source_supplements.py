"""Exact retained-source oracle; no builder imports or generated writes."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class CovenantThursdayTests(unittest.TestCase):
    def module(self):
        path = ROOT / 'covenant_thursday_source_supplements.py'
        self.assertTrue(path.exists(), 'bounded Covenant Thursday helper is missing')
        spec = importlib.util.spec_from_file_location('covenant_thursday_source_supplements', path)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_exact_complete_appointment_table(self):
        m = self.module()
        rows = m.load_covenant_thursday_rows()
        expected = {
            'Liturgy': [
                ('Pauline', '1 Corinthians 11:23-34', ['1Cor 11:23-34']),
                ('Psalm', 'Psalms 22:5;40:9', ['Ps 23:5', 'Ps 41:9']),
                ('Gospel', 'Matthew 26:20-29', ['Matt 26:20-29'])],
            'Liturgy of Blessing of the Water': [
                ('OT1', 'Genesis 18:1-23', ['Gen 18:1-23']),
                ('OT2', 'Proverbs 9:1-11', ['Prov 9:1-11']),
                ('OT3', 'Exodus from 14, 15', ['Exodus from 14, 15']),
                ('OT4', 'Joshua from 1, 3', ['Joshua from 1, 3']),
                ('OT5', 'Isaiah 4:2-4', ['Isa 4:2-4']),
                ('OT6', 'Isaiah 55:1-56:1', ['Isa 55:1-56:1']),
                ('OT7', 'Ezekiel 36:25-29', ['Ezek 36:25-29']),
                ('OT8', 'Ezekiel 47:1-9', ['Ezek 47:1-9']),
                ('Pauline', '1 Timothy 4:9-5:10', ['1Tim 4:9-5:10']),
                ('Psalm', 'Psalms 51:7, 10', ['Ps 51:7', 'Ps 51:10']),
                ('Gospel', 'John 13:1-17', ['Jn 13:1-17'])]}
        self.assertEqual(len(rows), 16)
        for section, appointments in expected.items():
            actual = [r for r in rows if r['service_section'] == section]
            self.assertEqual(len({r['source_row_id'] for r in actual}), len(appointments))
            for order, (slot, raw, passages) in enumerate(appointments, 1):
                fragments = [r for r in actual if int(r['source_order']) == order]
                self.assertEqual([r['passage'] for r in fragments], passages)
                self.assertEqual([r['source_token_order'] for r in fragments], [str(i) for i in range(1, len(passages)+1)])
                for r in fragments:
                    self.assertEqual((r['reading_slot'], r['raw_ref'], r['source_ref']), (slot, raw, raw))
                    self.assertEqual((r['day_title'], r['service_day'], r['service_hour']), ('Great Thursday', 'Great Thursday', section))
                    self.assertEqual(r['source_family'], 'coptic_reader_qualified_pascha_hour')
                    self.assertEqual(r['source_kind'], r['source_family'])
                    self.assertFalse(Path(r['source_file']).is_absolute())
                    self.assertEqual(m.qualify_covenant_thursday_row(r)['current_status'], 'source_qualified_retained_within_bounded_scope')
        self.assertFalse(any(r['reading_slot'] in ('Catholic', 'Praxis') for r in rows))
        self.assertFalse(any(r['raw_ref'] in ('Psalm 50', 'Psalm 150') for r in rows))

    def test_unaddressable_excerpts_never_claim_chapter_completeness(self):
        m = self.module()
        for r in m.load_covenant_thursday_rows():
            if ' from ' not in r['raw_ref']:
                continue
            self.assertEqual(r['normalized_ref'], '')
            for key in ('chapter_start', 'chapter_end', 'verse_start', 'verse_end', 'normalized_segment'):
                self.assertEqual(r[key], '')
            q = m.qualify_covenant_thursday_row(r)
            self.assertFalse(q['chapter_complete'])
            self.assertEqual(q['coordinate_status'], 'verse_unaddressable_named_excerpt')
            self.assertIn('not whole chapters', q['coordinate_note'])
            self.assertTrue(q['chapter_hints'])

    def test_exact_raw_rows_reject_every_field_or_metadata_forgery(self):
        m = self.module()
        row = m.load_covenant_thursday_rows()[0]
        for key in row:
            bad = {**row, key: row[key] + ' forged'}
            with self.subTest(field=key), self.assertRaises(ValueError):
                m.qualify_covenant_thursday_row(bad)
        for key, value in [('active', False), ('include_in_current_index', False), ('candidate_only', True), ('current_status', 'inactive'), ('runtime_activation_approved', True), ('source_family', 'forged'), ('full_capture_sha256', '0'*64)]:
            bad = copy.deepcopy(row)
            q = json.loads(bad['provenance'])
            q[key] = value
            bad['provenance'] = json.dumps(q)
            with self.subTest(metadata=key), self.assertRaises(ValueError):
                m.qualify_covenant_thursday_row(bad)
        for key in ('active', 'removed_marker', 'candidate_only'):
            with self.assertRaises(ValueError):
                m.qualify_covenant_thursday_row({**row, key: 'false'})

    def test_portable_pack_reauthenticates_every_evidence_file_each_call(self):
        m = self.module()
        expected = m.load_covenant_thursday_rows()
        with tempfile.TemporaryDirectory() as td:
            portable = Path(td) / 'pack'
            shutil.copytree(m.SOURCE_ROOT, portable)
            with patch.object(m, 'SOURCE_ROOT', portable):
                self.assertEqual(m.load_covenant_thursday_rows(), expected)
                manifest = json.loads((portable/'source-contract.json').read_text())
                for relative in manifest['fingerprints']:
                    target = portable / relative
                    original = target.read_bytes()
                    target.write_bytes(original+b'\nforged')
                    with self.subTest(file=relative), self.assertRaises(ValueError):
                        m.qualify_covenant_thursday_row(expected[0])
                    target.write_bytes(original)
                self.assertEqual(m.load_covenant_thursday_rows(), expected)

    def test_body_and_context_qualification_preserves_old_nonapproval(self):
        m = self.module()
        contract = m.load_covenant_thursday_contract()
        self.assertFalse(contract['old_receipts_grant_activation'])
        self.assertEqual(contract['selected_civil_date'], '2026-04-09')
        self.assertEqual(len(contract['appointments']), 14)
        for r in m.load_covenant_thursday_rows():
            q = m.qualify_covenant_thursday_row(r)
            self.assertTrue(q['active'])
            self.assertFalse(q['fresh_app_verification'])
            self.assertFalse(q['runtime_activation_approved'])
            self.assertTrue(q['body_envelope_literal'])
            self.assertEqual(q['contract_sha256'], m.CONTRACT_SHA256)
        receipt = json.loads((m.SOURCE_ROOT/'old-review-receipt.json').read_text())
        self.assertFalse(receipt['consumer_eligible'])
        self.assertFalse(receipt['release_approval'])
        self.assertEqual(receipt['runtime_contract_acceptance'], 'pending')


if __name__ == '__main__':
    unittest.main()
