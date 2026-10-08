"""Bounded Reader policies through real date/cycle helpers, never generated JSON."""
import copy
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import calendar_resolution as calendar
import build_lectionary_reference as reference
from passage_normalization import canonicalize_text_ref, passage_matches
from reading_context_overlays import is_current_source_row

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'sources/coptic-reader/sunday-qualified-2026-10-07'
ORACLE = json.loads((FIXTURE / 'accepted-oracle.json').read_text())
PRIMARY = ['2027-02-21', '2027-02-28', '2028-01-09', '2027-09-05']


def raw_rows():
    with (ROOT / 'out/data/copticchurch_date_readings_2020_2035.csv').open() as f:
        return list(csv.DictReader(f))


def nonpsalm(rows):
    return [(r['service_section'], canonicalize_text_ref(r['normalized_ref']))
            for r in rows if r['reading_type'] != 'Psalm']


def expected(date):
    table = next(t for t in ORACLE['tables'] if t['date'] == date)
    result = []
    for d in table['documents']:
        service = d['label'].split('-')[0]
        for ref in d['printedReferences']:
            if not ref.startswith('Psalms '):
                result.append((service, canonicalize_text_ref(ref)))
    return result


class SundayReaderCalendarRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = raw_rows()
        cls.by_date = {}
        for row in cls.raw:
            cls.by_date.setdefault(row['gregorian_date'], []).append(row)

    def test_four_primary_dates_select_complete_correct_nonpsalm_tables(self):
        for date in PRIMARY:
            with self.subTest(date=date):
                rows = self.by_date[date]
                before = copy.deepcopy(rows)
                result = calendar.resolve_current_date_rows(rows, [])
                self.assertEqual(nonpsalm(result), expected(date))
                self.assertEqual(len(result), 9)
                self.assertEqual([r['service_section'] for r in result],
                                 ['Vespers'] * 2 + ['Matins'] * 2 + ['Liturgy'] * 5)
                self.assertEqual([r['reading_type'] for r in result],
                                 ['Psalm', 'Gospel', 'Psalm', 'Gospel', 'Pauline Epistle',
                                  'Catholic Epistle', 'Acts of the Apostles', 'Psalm', 'Gospel'])
                self.assertEqual({r['gregorian_date'] for r in result}, {date})
                self.assertEqual(rows, before)
                self.assertEqual(calendar.resolve_current_date_rows(result, []), result)
                with tempfile.TemporaryDirectory() as temp, patch.object(reference, 'DATA', Path(temp)):
                    index = reference.build_date_passage_index(result)
                for _, ref in expected(date):
                    self.assertTrue(any(passage_matches(ref, r['matched_ref']) for r in index), ref)

    def test_documented_month_context_seams_do_not_change_numeric_coptic_date(self):
        cases = {'2027-02-07': ('SundayReadings', 6, 1),
                 '2027-02-14': ('SundayReadings', 6, 2),
                 '2027-02-21': ('SundayReadings', 6, 3),
                 '2027-02-28': ('SundayReadings', 6, 4),
                 '2027-09-05': ('SundayReadings', 13, 1),
                 '2028-01-09': ('AnnualReadings', 4, 30)}
        for date, key in cases.items():
            self.assertEqual(calendar.sunday_policy_selection(dt.date.fromisoformat(date)), key)
        self.assertEqual(calendar.numeric_coptic_date(dt.date(2027, 2, 7)), (1743, 5, 30))
        self.assertEqual(calendar.numeric_coptic_date(dt.date(2027, 9, 5)), (1743, 12, 30))
        self.assertIsNone(calendar.sunday_policy_selection(dt.date(2027, 3, 7)))
        for date in ('2026-06-14', '2026-06-21', '2026-06-28', '2026-07-05'):
            self.assertIsNone(calendar.sunday_policy_selection(dt.date.fromisoformat(date)))

    def test_fifth_thoout_excludes_new_year_sunday(self):
        # 2022 Thoout 1 is Sunday; day 8/15/22/29 are only first..fourth.
        self.assertIsNone(calendar.sunday_policy_selection(dt.date(2022, 9, 11)))
        for i in range(1, 5):
            date = dt.date(2022, 9, 11) + dt.timedelta(days=7*i)
            if i == 4:  # Joyful 29th has higher precedence.
                self.assertIsNone(calendar.sunday_policy_selection(date))
            else:
                self.assertEqual(calendar.sunday_policy_selection(date), ('SundayReadings', 1, i))

    def test_cycle_acts_corrections_keep_raw_and_filter_superseded_history(self):
        books = reference.load_books()
        rows = reference.export_cycle_tables(books)
        current = reference.build_passage_index(rows, books)
        history = reference.build_passage_index(rows, books, include_inactive=True)
        for key, old, new in [('Bashans 5', '44.14:1-9', 'Acts 24:1-9'),
                              ('Baunah 5', '44.14:1-9', 'Acts 24:1-9'),
                              ('Abib 5', '44.14:1-9', 'Acts 24:1-9'),
                              ('Tut 5', '44.18:9-12', 'Acts 18:9-21')]:
            target = [r for r in rows if r['source_table'] == 'SundayReadings'
                      and r['day_key'] == key and r['reading_slot'] == 'liturgy_acts']
            self.assertEqual(len(target), 2)
            active = [r for r in target if is_current_source_row(r)]
            inactive = [r for r in target if not is_current_source_row(r)]
            self.assertEqual(len(active), 1)
            self.assertEqual(active[0]['normalized_ref'], new)
            self.assertEqual(active[0]['raw_ref'], old)
            self.assertEqual(len(inactive), 1)
            self.assertEqual(inactive[0]['raw_ref'], old)
            matches = [r for r in current if r['source_table'] == 'SundayReadings'
                       and r['day_key'] == key and r['reading_slot'] == 'liturgy_acts']
            self.assertEqual([r['normalized_segment'] for r in matches], [new])
            self.assertEqual(len([r for r in history if r['source_table'] == 'SundayReadings'
                                 and r['day_key'] == key and r['reading_slot'] == 'liturgy_acts']), 2)

    def test_removed_cycle_inputs_are_not_restored_and_wrong_context_does_not_leak(self):
        row = dict(source='katameros-api sqlite', source_table='SundayReadings', day_key='Bashans 5',
                   month_number=9, day=5, reading_slot='liturgy_acts', raw_ref='44.14:1-9',
                   normalized_ref='Acts 14:1-9', active=False, state='removed')
        self.assertEqual(calendar.apply_sunday_cycle_overlays([row]), [row])
        for change in ({'source_table': 'AnnualReadings'}, {'day': 4}, {'reading_slot': 'liturgy_gospel'},
                       {'month_number': 8}, {'day_key': 'Bashans 4'}, {'source': 'other'}):
            probe = dict(row, active=True, state='current', **change)
            self.assertEqual(calendar.apply_sunday_cycle_overlays([probe]), [probe])

    def test_no_feast_season_wrong_day_or_inactive_restoration(self):
        rows = self.by_date['2027-02-21']
        for title in ('Annunciation', 'Sunday before the Great Lent', 'Sunday of the first week of Great Lent',
                      'First Sunday of the Holy Fifty Days'):
            changed = [dict(r, day_title=title) for r in rows]
            result = calendar.resolve_current_date_rows(changed, [])
            self.assertCountEqual(result, changed)
        for date in ('2027-02-20', '2026-02-21', '2027-03-07'):
            changed = [dict(r, gregorian_date=date) for r in rows]
            self.assertCountEqual(calendar.resolve_current_date_rows(changed, []), changed)
        changed = [dict(r, active=False, state='removed') for r in rows]
        self.assertCountEqual(calendar.resolve_current_date_rows(changed, []), changed)

    def test_corruption_missing_extra_duplicate_slot_and_mixed_context_fail_closed(self):
        rows = self.by_date['2027-02-21']
        for bad in (rows[:-1], rows + rows[:1], [dict(r, day_title='Fourth Sunday of Amshir') if i == 0 else r for i, r in enumerate(rows)],
                    [dict(r, reading_type='Gospel') if r['reading_type'] == 'Psalm' else r for r in rows]):
            with self.assertRaises(RuntimeError):
                calendar.resolve_current_date_rows(bad, [])

    def test_replayed_overlay_corruption_and_wrong_year_fail_closed(self):
        result = calendar.resolve_current_date_rows(self.by_date['2027-02-21'], [])
        for change in ({'normalized_ref': 'Jn 6:27-45'}, {'source_order': 'bogus'},
                       {'correction_source': 'unbound'}, {'day_title': 'Fourth Sunday of Meshir'},
                       {'gregorian_date': '2026-02-21'}, {'weekday': 'Saturday'}):
            bad = copy.deepcopy(result)
            if 'gregorian_date' in change:
                bad = [dict(r, **change) for r in bad]
            else:
                bad[0].update(change)
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                calendar.resolve_current_date_rows(bad, [])
        with self.assertRaises(RuntimeError):
            calendar.resolve_current_date_rows(list(reversed(result)), [])

    def test_cycle_replay_is_exact_once_and_corrupt_numeric_provenance_is_rejected(self):
        books = reference.load_books()
        rows = reference.export_cycle_tables(books)
        self.assertEqual(calendar.apply_sunday_cycle_overlays(rows), rows)
        target = next(r for r in rows if r.get('source_table') == 'SundayReadings'
                      and r.get('day_key') == 'Bashans 5'
                      and r.get('reading_slot') == 'liturgy_acts' and is_current_source_row(r))
        for change in ({'numeric_ref': '44.14:1-9'}, {'normalized_ref': 'Acts 24:1-8'},
                       {'correction_source': 'unbound'}):
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                reference.build_passage_index([dict(target, **change)], books)
        with self.assertRaises(RuntimeError):
            calendar.apply_sunday_cycle_overlays([target, target])

    def test_evidence_byte_drift_rejected(self):
        original = Path.read_bytes
        target = FIXTURE / 'accepted-oracle.json'
        def corrupt(path):
            value = original(path)
            return value + b' ' if path == target else value
        with patch.object(Path, 'read_bytes', corrupt), self.assertRaises(RuntimeError):
            calendar.load_sunday_evidence()


if __name__ == '__main__':
    unittest.main()
