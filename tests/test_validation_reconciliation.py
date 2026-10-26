"""Reconcile retained source witnesses without relaxing current-output equality.

Oracle: 1.3.5 retains Good Friday Jonah as inactive; the qualified Reader
Sunday Day Ninth Hour adds Lam 1:1-4. Seasonal coverage comes from the pinned
qualified-date oracle, not optional fields in a reverse-identity contract.
"""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import verify_design_deliverables as validator

ROOT = Path(__file__).resolve().parents[1]


class ValidationReconciliation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.presentation = validator.read_csv(ROOT / 'out/design/reverse_lectionary_presentation.csv')
        cls.schema = json.loads((ROOT / 'out/design/lectionary_schema.json').read_text())
        cls.summary = json.loads((ROOT / 'out/design/BUILD_DESIGN_SUMMARY.json').read_text())

    def verify(self, rows=None):
        validator.verify_daily_rows(self.presentation if rows is None else rows, self.schema, self.summary)

    def test_retained_good_friday_jonah_does_not_require_current_daily_appointment(self):
        retained = [r for r in self.presentation if r['gregorian_date'] == '2034-04-07'
                    and r['occasion'] == 'Good Friday' and r['service_hour'] == 'Twelfth Hour'
                    and r['canonical_mt_ref'] == 'Jonah 1:10-2:8']
        self.assertEqual(len(retained), 1)
        self.assertEqual(retained[0]['current_status'], 'historical_candidate_removed')
        self.verify()

    def test_inactive_overlay_cannot_be_reactivated_in_presentation(self):
        self.verify()
        rows = copy.deepcopy(self.presentation)
        target = next(r for r in rows if r['gregorian_date'] == '2034-04-07'
                      and r['occasion'] == 'Good Friday' and r['service_hour'] == 'Twelfth Hour'
                      and r['canonical_mt_ref'] == 'Jonah 1:10-2:8')
        target.update(current_status='current_confirmed_coptic_reader', removed_marker='')
        with self.assertRaisesRegex(AssertionError, 'calendar overlay'):
            self.verify(rows)

    def test_current_overlay_omission_cannot_shrink_source_oracle(self):
        self.verify()
        rows = [r for r in self.presentation if not (r['gregorian_date'] == '2034-04-07'
                and r['occasion'] == 'Good Friday' and r['service_hour'] == 'Twelfth Hour'
                and r['canonical_mt_ref'] == 'Lam 3:1-66')]
        with self.assertRaisesRegex(AssertionError, 'calendar overlay source contexts'):
            self.verify(rows)

    def test_full_validator_accepts_only_qualified_inactive_edition_witness(self):
        retained = [r for r in self.presentation if r['removed_marker'] == 'edition_specific_not_current_reader_practice']
        self.assertEqual(len(retained), 2)
        self.assertEqual({(r['source_family'], r['source_kind'], r['occasion'], r['service_hour'],
                          r['slot'], r['canonical_mt_ref'], r['current_status']) for r in retained},
                         {('holy_pascha_curated_day_hour', 'pascha_day_hour', 'Good Friday',
                           'Twelfth Hour', 'OT2', 'Jonah 1:10-2:8', 'historical_candidate_removed')})
        validator.verify_rows()

    def test_joel_lxx_display_seam_preserves_mt_supplement_oracle(self):
        row = next(r for r in self.presentation if r['gregorian_date'] == '2023-03-15'
                   and r['source_family'] == 'coptic_reader_verified_supplement' and r['slot'] == 'OT2')
        self.assertEqual(row['display_ref'], 'Joel 2:28-32 (LXX Joel 3:1-5)')
        self.assertEqual(row['canonical_mt_ref'], 'Joel 2:28-32')
        self.assertEqual(row['canonical_lxx_ref'], 'Joel 3:1-5')
        self.verify()

    def test_seasonal_complete_year_coverage_includes_rule_recurrences_and_boundary(self):
        source = validator.read_csv(ROOT / 'out/data/copticchurch_passage_index_current_2020_2035.csv')
        policy = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())
        for year in (2026, 2027, 2028, 2031):
            with self.subTest(year=year):
                primary = [r for r in source if r['gregorian_date'].startswith(str(year))]
                daily = json.loads((ROOT / f'out/design/daily/lectionary-{year}.json').read_text())
                validator.verify_seasonal_daily(primary, daily, policy, complete_year=True)
                date = '2028-04-07' if year == 2028 else next(r['gregorian_date'] for r in primary
                    if r.get('source') == 'Coptic Reader verified recurring supplement')
                primary = [r for r in primary if r['gregorian_date'] != date]
                del daily[date]
                with self.assertRaisesRegex(AssertionError, 'qualified date inventory changed'):
                    validator.verify_seasonal_daily(primary, daily, policy, complete_year=True)


if __name__ == '__main__':
    unittest.main()
