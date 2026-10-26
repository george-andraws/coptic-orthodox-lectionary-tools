"""Real verifier/comparator callers must qualify Lent fallback per civil date."""
import copy
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_design_deliverables as design
import build_lectionary_crosswalk as crosswalk
import build_lectionary_reference as reference
import verify_design_deliverables as validator
from scripts import compare_external_sources as comparator
from test_lent_reader_precedence import fixture, prophecies, POLICY, ROOT, DATE, TITLE

LEGACY_DATE = '2025-02-26'


class LentMixedDateQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source, qualified = fixture()
        legacy_source = reference.build_date_passage_index(reference.parse_copticchurch_html(
            (ROOT / 'cache/copticchurch_html' / f'{LEGACY_DATE}.html').read_text(),
            dt.date.fromisoformat(LEGACY_DATE))[1])
        cls.legacy_source = [r for r in legacy_source if r.get('source') != 'Coptic Reader verified recurring supplement']
        legacy, _ = design.build_reverse_presentation(crosswalk.project_date_rows(cls.legacy_source))
        cls.presentation = qualified + legacy
        cls.daily = design.build_daily_year_files(cls.presentation)

    def test_literal_two_year_control_and_unchanged_raw_witness(self):
        self.assertEqual([r['canonical_mt_ref'] for r in prophecies(self.daily[2026][DATE])],
                         ['Isa 2:3-11', 'Joel 2:12-26'])
        self.assertEqual([r['canonical_mt_ref'] for r in prophecies(self.daily[2025][LEGACY_DATE])],
                         ['Joel 2:12-27'])
        self.assertEqual(len([r for r in self.presentation if not r.get('gregorian_date')
                              and r.get('canonical_mt_ref') == 'Joel 2:12-27']), 1)

    def verify_fixture(self, presentation=None, daily=None):
        presentation = self.presentation if presentation is None else presentation
        daily = self.daily if daily is None else daily
        source = self.source + self.legacy_source
        original_read = validator.read_csv
        original_seasonal = validator.verify_seasonal_daily

        def read(path):
            if str(path).endswith('out/data/copticchurch_passage_index_current_2020_2035.csv'):
                return source
            if str(path).endswith('out/data/pascha_day_hour_index.csv'):
                return []  # This bounded fixture has no Pascha source contexts.
            return original_read(path)

        def seasonal(rows, days, policy, *, complete_year=False):
            # Replace only the whole-corpus date-inventory guard for this exact
            # two-date fixture; preserve the real seasonal authentication oracle.
            if complete_year:
                year = next(iter(days))[:4]
                self.assertEqual(set(days), {DATE if year == '2026' else LEGACY_DATE})
            return original_seasonal(rows, days, policy)

        counts = {str(year): sum(map(len, days.values())) for year, days in daily.items()}
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            (out / 'daily').mkdir()
            for year, days in daily.items():
                (out / 'daily' / f'lectionary-{year}.json').write_text(json.dumps(days))
            with patch.object(validator, 'OUT', out), patch.object(validator, 'read_csv', side_effect=read), \
                    patch.object(validator, 'verify_seasonal_daily', side_effect=seasonal):
                validator.verify_daily_rows(presentation, {'tables': {'daily_lectionary_year': design.DAILY_READING_FIELDS}},
                                            {'daily_lectionary_years': counts, 'daily_lectionary_total_rows': sum(counts.values())})

    def counters(self, year, daily=None):
        original_read = validator.read_csv

        def read(path):
            if str(path).endswith('out/design/reverse_lectionary_presentation.csv'):
                return copy.deepcopy(self.presentation)
            return original_read(path)

        source = self.source if year == 2026 else self.legacy_source
        rows = copy.deepcopy(self.daily[year] if daily is None else daily)
        # npm's existing public service-stage contract for the cycle supplement.
        for readings in rows.values():
            for row in readings:
                if row.get('source_kind') == 'katameros_cycle':
                    row['service_order'] = 2
        with patch.object(validator, 'read_csv', side_effect=read):
            return comparator.contextual_counters(source, rows, year, POLICY)

    def test_production_verifier_accepts_mixed_inventory(self):
        self.verify_fixture()

    def test_actual_contextual_counters_accept_both_years_independently(self):
        for year in (2026, 2025):
            with self.subTest(year=year):
                source, package, _, dispositions, issues = self.counters(year)
                self.assertEqual(issues, [])
                self.assertEqual(source, package)
                supplements = [r for r in dispositions if r['disposition'] == 'source_qualified_cycle_supplement']
                self.assertEqual([r['gregorian_date'] for r in supplements], [LEGACY_DATE] if year == 2025 else [])

    def test_verifier_keeps_exact_reader_and_fallback_negative_guards(self):
        for mutation in ('missing_reader', 'duplicate_reader', 'extra_legacy', 'missing_fallback', 'missing_date'):
            daily = copy.deepcopy(self.daily)
            if mutation == 'missing_reader':
                daily[2026][DATE].remove(prophecies(daily[2026][DATE])[0])
            elif mutation == 'duplicate_reader':
                daily[2026][DATE].append(copy.deepcopy(prophecies(daily[2026][DATE])[0]))
            elif mutation == 'extra_legacy':
                daily[2026][DATE].append(copy.deepcopy(prophecies(daily[2025][LEGACY_DATE])[0]))
            elif mutation == 'missing_fallback':
                daily[2025][LEGACY_DATE].remove(prophecies(daily[2025][LEGACY_DATE])[0])
            else:
                del daily[2026][DATE]
            with self.subTest(mutation=mutation), self.assertRaises((AssertionError, RuntimeError)):
                self.verify_fixture(daily=daily)

    def test_comparator_rejects_cross_date_fallback_leak_and_omission(self):
        daily = copy.deepcopy(self.daily[2026])
        daily[DATE].append(copy.deepcopy(prophecies(self.daily[2025][LEGACY_DATE])[0]))
        result = self.counters(2026, daily)
        self.assertIn('invalid_source_qualified_cycle_supplement', [r['status'] for r in result[4]])
        legacy = copy.deepcopy(self.daily[2025])
        legacy[LEGACY_DATE].remove(prophecies(legacy[LEGACY_DATE])[0])
        source, package, _, _, _ = self.counters(2025, legacy)
        self.assertNotEqual(source, package)


if __name__ == '__main__':
    unittest.main()
