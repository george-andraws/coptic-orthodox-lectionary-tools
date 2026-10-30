"""Narrow release-validator contracts; no builders, SQLite, or shared writes."""
import os
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import kiahk23_review_repairs as r2
import holy_week_review_repairs as holy
from scripts import review_release_contract as contract

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


class ReviewReleaseContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidate = rows(Path(os.environ.get('LECTIONARY_REVIEW_REVERSE',
            ROOT / 'packages/lectionary-data/data/reverse_lectionary_index.jsonl')))
        cls.owned = [r for r in cls.candidate if r.get('source_family') == r2.FAMILY]
        cls.inactive = [r for r in cls.candidate if r.get('kiahk23_retirement')
                        or r.get('current_status') == holy.HOLD]

    def test_candidate_all_nine_owned_rows_and_exact_three_empty_psalms(self):
        self.assertEqual(len(self.owned), 9)
        self.assertEqual(sum(contract.source_owned_empty_coordinates(r) for r in self.owned), 3)
        self.assertFalse(contract.source_owned_empty_coordinates({'spans_json': '[]'}))

    def test_owned_mutations_fail_even_when_markers_and_coordinates_are_stripped(self):
        for original in self.owned:
            for field, value in [('source_family', 'forged'), ('source_kind', 'forged'),
                                 ('identity_key', 'rid_forged'), ('occasion', 'Tubah 23'),
                                 ('slot', 'Forged'), ('canonical_mt_ref', 'Ps 1:1-2'),
                                 ('spans_json', '[]' if original['canonical_mt_ref'] else '[{}]'),
                                 ('coptic_date_key', 'toba-23'), ('active', False),
                                 ('current_status', 'historical_witness'),
                                 ('source_disclosure', '[]')]:
                with self.subTest(row=original['source_row_id'], field=field):
                    row = dict(original, **{field: value})
                    with self.assertRaisesRegex(ValueError, 'Kiahk23'):
                        contract.source_owned_empty_coordinates(row)
        row = dict(next(r for r in self.owned if not r['canonical_mt_ref']))
        for key in list(row):
            if key.startswith(('source_', 'kiahk23_')) or key == 'provenance':
                row.pop(key)
        row['spans_json'] = '[{}]'
        with self.assertRaisesRegex(ValueError, 'Kiahk23'):
            contract.source_owned_empty_coordinates(row)

    def test_daily_qualifier_uses_actual_outer_date(self):
        row = dict(self.owned[0], gregorian_date='2026-01-01', weekday='Thursday')
        self.assertTrue(contract.source_owned_empty_coordinates(row, '2026-01-01'))
        for date in ('2026-01-02', '2034-01-01', None):
            with self.subTest(date=date), self.assertRaisesRegex(ValueError, 'Kiahk23'):
                contract.source_owned_empty_coordinates(row, date)

    def test_all_37_inactive_candidate_witnesses_are_authenticated(self):
        self.assertEqual(len(self.inactive), 37)
        self.assertTrue(all(contract.review_inactive_qualified(r) for r in self.inactive))
        self.assertFalse(contract.review_inactive_qualified({'active': False}))

    def test_inactive_source_identity_context_lifecycle_and_disclosure_rebinds_fail(self):
        for original in self.inactive:
            for field, value in [('source_family', 'forged'), ('source_kind', 'forged'),
                                 ('source_locator', 'forged'), ('identity_key', 'forged'),
                                 ('occasion', 'Tubah 23'), ('slot', 'forged'),
                                 ('canonical_mt_ref', 'Ps 1:1-2'), ('spans_json', '[]'),
                                 ('coptic_date_key', 'toba-23'), ('active', True),
                                 ('status', 'current'), ('current_status', 'current'),
                                 ('source_disclosure', '[]')]:
                with self.subTest(row=original['identity_key'], field=field):
                    row = dict(original, **{field: value})
                    with self.assertRaisesRegex(ValueError, 'review|calendar'):
                        contract.review_inactive_qualified(row)
        row = dict(next(r for r in self.inactive if r.get('kiahk23_retirement')),
                   kiahk23_retirement='{}')
        with self.assertRaisesRegex(ValueError, 'review'):
            contract.review_inactive_qualified(row)

    def test_frozen_design_anchor_rejects_source_drift_in_private_fixture(self):
        original = ROOT / contract.DESIGN_SOURCE
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), contract.DESIGN_SHA256)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / contract.DESIGN_SOURCE
            target.parent.mkdir(parents=True)
            target.write_bytes(original.read_bytes())
            held = next(r for r in self.inactive if r.get('current_status') == holy.HOLD)
            with patch.object(contract, 'ROOT', root):
                self.assertTrue(contract.review_inactive_qualified(held))
                target.write_bytes(original.read_bytes() + b'\n')
                with self.assertRaisesRegex(ValueError, 'authentication'):
                    contract.review_inactive_qualified(held)

    def test_calendar_accepts_complete_candidate_including_r1_r4_r6(self):
        with patch('sqlite3.connect', side_effect=AssertionError('SQLite forbidden')):
            contexts = [contract.qualified_calendar_context(r) for r in self.candidate]
        self.assertEqual(len(contexts), len(self.candidate))
        self.assertIn(('kiahk-23', ''), contexts)
        self.assertIn(('', 'bashans-3'), contexts)
        self.assertEqual(contract.qualified_calendar_context({'occasion': 'unscoped'}), ('', ''))

    def test_calendar_rejects_normalized_metadata_and_evidence_mutations(self):
        original = next(r for r in self.candidate if r.get('calendar_review_source_locators')
                        and not r.get('composite_fragments_json'))
        for field, value in [('coptic_date_key', 'toba-23'), ('annual_sunday', 'toba-3'),
                             ('display_label', 'forged'), ('calendar_review_status', 'forged'),
                             ('calendar_review_source_locators', ['forged']),
                             ('calendar_review_calendar_keys', ['forged']),
                             ('source_family', 'forged'), ('source_kind', 'forged')]:
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'calendar'):
                contract.qualified_calendar_context(dict(original, **{field: value}))
        with self.assertRaisesRegex(ValueError, 'calendar'):
            contract.qualified_calendar_context({'occasion': 'unscoped', 'coptic_date_key': 'toba-23'})

    def test_calendar_transformed_rows_cannot_transplant_context(self):
        transformed = [r for r in self.candidate if r.get('composite_fragments_json')
                       or r.get('resolver_review_disclosure')]
        self.assertTrue(transformed)
        for original in transformed:
            for field, value in [('coptic_date_key', 'toba-23'), ('source_kind', 'forged'),
                                 ('occasion', 'forged'), ('slot', 'forged')]:
                with self.subTest(row=original['identity_key'], field=field):
                    with self.assertRaisesRegex(ValueError, 'calendar'):
                        contract.qualified_calendar_context(dict(original, **{field: value}))

    def test_source_authentication_failure_propagates(self):
        with patch.object(r2, 'authenticate_plan', side_effect=ValueError('Kiahk23 authentication')):
            with self.assertRaisesRegex(ValueError, 'authentication'):
                contract.source_owned_empty_coordinates(self.owned[0])
            with self.assertRaisesRegex(ValueError, 'authentication'):
                contract.review_inactive_qualified(next(r for r in self.inactive if r.get('kiahk23_retirement')))


if __name__ == '__main__':
    unittest.main()
