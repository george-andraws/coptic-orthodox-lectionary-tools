"""Dated Jonah attestations are not duplicate undated service appointments."""
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import verify_lectionary_queries as verifier


class DatedDuplicateGuard(unittest.TestCase):
    def check(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            with (data / 'reverse_lookup_crosswalk.csv').open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(dict.fromkeys(k for r in rows for k in r)))
                writer.writeheader(); writer.writerows(rows)
            (data / 'katameros_cycle_passage_index.csv').write_text('source_table,season,day_key,reading_slot,canonical_segment\n')
            with patch.object(verifier, 'DATA', data):
                return verifier.assert_no_duplicate_reading_tuples()

    def rows(self):
        # Explicit duplicate-key contract fixtures, not primary source captures.
        base = dict(source_kind='jonah_fast_date_supplement', source_family='jonah_fast_source_qualified',
                    gregorian_date='2026-02-02', service_section='Matins', reading_type='Prophecy',
                    reading_slot='OT1', passage='Jonah 1:1-17', significance_note='Matins',
                    calendar_key='Fast of Nineveh', source_row_id='first')
        return [base, dict(base, gregorian_date='2027-02-22', source_row_id='second')]

    def test_distinct_annual_jonah_attestations_are_not_duplicates(self):
        self.assertEqual(self.check(self.rows())['reverse_lookup_rows_checked'], 2)

    def test_same_date_duplicate_is_rejected_even_with_different_source_id(self):
        rows = self.rows(); rows[1]['gregorian_date'] = rows[0]['gregorian_date']
        with self.assertRaises(AssertionError):
            self.check(rows)

    def test_unknown_family_does_not_gain_the_jonah_dated_exception(self):
        rows = [dict(r, source_family='unqualified') for r in self.rows()]
        with self.assertRaises(AssertionError):
            self.check(rows)

    def test_undated_legacy_layers_keep_their_natural_duplicate_key(self):
        rows = [dict(r, source_kind='pascha_day_hour', source_family='holy_pascha_curated_day_hour') for r in self.rows()]
        with self.assertRaises(AssertionError):
            self.check(rows)


if __name__ == '__main__':
    unittest.main()
