"""Bounded ordinary appointment regressions; no builders, network, or publication."""
import copy
import datetime as dt
import importlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_reference as core
from passage_normalization import extract_text_ref_tokens, parse_passage, passage_matches

ROOT = Path(__file__).resolve().parents[1]


def source_row(date='2026-09-01', **changes) -> dict:
    day = dt.date.fromisoformat(date)
    row = dict(source='copticchurch.net daily scrape', gregorian_date=date,
               weekday=day.strftime('%A'), day_title='Mesra 26',
               service_section='Matins', reading_type='Gospel', raw_ref='12:20-26',
               normalized_ref='12:20-26', parse_status='ok', normalization_warning='',
               url=f'https://copticchurch.net/readings?g_year={day.year}&g_month={day.month:02d}&g_day={day.day:02d}')
    row.update(changes)
    return row


def psalm_row(date='2026-11-01', **changes):
    return source_row(date, **dict(day_title='The fourth Sunday of Baba',
                      service_section='Liturgy', reading_type='Psalm',
                      raw_ref='Psalm 79:13:00', normalized_ref='Psalm 79:13:00', **changes))



class OrdinaryTokenRepairs(unittest.TestCase):
    def test_php_open_end_is_one_cross_chapter_appointment(self):
        self.assertEqual(extract_text_ref_tokens('Php 1:27—  &  Php 2:1-11'), ['Phil 1:27-2:11'])
        self.assertEqual(getattr(parse_passage('Php 2:1-11'), 'canonical', None), 'Phil 2:1-11')

    def test_jude_explicit_verse_range_stays_in_single_chapter(self):
        for raw in ['Jude 14-25', 'Jude 14–25', 'Jude 14—25']:
            with self.subTest(raw=raw):
                self.assertEqual(extract_text_ref_tokens(raw), ['Jude 1:14-25'])
                self.assertEqual(getattr(parse_passage(raw), 'canonical', None), 'Jude 1:14-25')
        self.assertEqual(getattr(parse_passage('Jude 1'), 'canonical', None), 'Jude 1')

    def test_ambiguous_books_and_malformed_sources_are_not_generically_salvaged(self):
        for raw in ['Prayer of Manasseh 1-15', 'PrMan 1-15', 'John 14-25',
                    'Jude 0-25', 'Jude 14-26', 'Jude 25-14',
                    'Jude 14-25:1', 'Jude 14-25,30', 'Jude 14-25-30',
                    '12:20-26', 'Psalm 79:13:00', '120:130, 141']:
            with self.subTest(raw=raw):
                self.assertIsNone(parse_passage(raw))
                self.assertEqual(extract_text_ref_tokens(raw), [])
        self.assertEqual(getattr(parse_passage('John 14'), 'canonical', None), 'Jn 14')
        self.assertEqual(extract_text_ref_tokens('Prayer of Manasseh 1:1-15'), ['PrMan 1:1-15'])


class OrdinarySourceRepairs(unittest.TestCase):
    def setUp(self):
        self.adapter = importlib.import_module('ordinary_appointment_repairs')

    def test_exact_source_repairs_preserve_raw_and_other_receipts(self):
        for row, expected in [(source_row(), 'Jn 12:20-26'), (psalm_row(), 'Ps 79:13')]:
            row.update(original_review={'runtime_activation_approved': False},
                       independent_review_approved=False, unrelated_field=['retained'])
            before = copy.deepcopy(row)
            result = self.adapter.apply_ordinary_appointment_repair(row)
            self.assertEqual(row, before)
            self.assertEqual(result['normalized_ref'], expected)
            self.assertEqual(result['raw_ref'], before['raw_ref'])
            self.assertEqual(result['original_review'], before['original_review'])
            self.assertIs(result['independent_review_approved'], False)
            self.assertEqual(result['unrelated_field'], ['retained'])
            self.assertEqual(self.adapter.apply_ordinary_appointment_repair(result), result)
        self.assertEqual(result['ordinary_appointment_reader_printed_ref'], 'Psalms 78:14')
        self.assertIn('NKJV', result['normalization_warning'])

    def test_wrong_source_family_kind_service_type_date_and_raw_are_noops(self):
        for original in [source_row(), psalm_row()]:
            mutations = [('source', 'katameros-api sqlite'), ('source_family', 'pascha'),
                         ('source_kind', 'special_service'), ('service_section', 'Vespers'),
                         ('reading_type', 'Prophecy'), ('day_title', 'neighbor'),
                         ('url', original['url'] + '&untrusted=1'), ('weekday', 'Monday'),
                         ('gregorian_date', '2026-09-02'),
                         ('raw_ref', original['raw_ref'] + ' '),
                         ('normalized_ref', 'existing source-qualified correction')]
            for field, value in mutations:
                row = dict(original, **{field: value})
                with self.subTest(original=original['day_title'], field=field):
                    self.assertEqual(self.adapter.apply_ordinary_appointment_repair(row), row)

    def test_inactive_candidates_and_held_psalm_coordinates_are_unchanged(self):
        for key, value in [('active', False), ('include_in_current_index', False),
                           ('status', 'removed'), ('state', 'superseded'),
                           ('current_status', 'historical_witness'),
                           ('current_status', 'pending_psalm_equivalence_unresolved'),
                           ('removed_marker', 'retained witness'), ('candidate_only', True),
                           ('source_convention', 'coptic_reader_psalm_alignment_hold'),
                           ('superseded_reason', 'old decision')]:
            row = dict(psalm_row(), **{key: value})
            with self.subTest(key=key):
                self.assertEqual(self.adapter.apply_ordinary_appointment_repair(row), row)

    def test_amshir_conflict_is_explicitly_held_not_replaced_from_another_table(self):
        row = source_row('2028-02-15', day_title='Amshir 7', service_section='Matins',
                         reading_type='Psalm', raw_ref='120:130, 141', normalized_ref='120:130, 141')
        self.assertEqual(self.adapter.apply_ordinary_appointment_repair(row), row)
        self.assertEqual(core.build_date_passage_index([row]), [])
        contract = self.adapter.load_ordinary_appointment_contract()
        self.assertEqual(contract['held'][0]['decision'], 'hold_no_activation')
        self.assertEqual(contract['held'][0]['current_cycle_ref'], 'Ps 73:23,24,28; Ps 9:14')

    def test_source_and_authorization_hash_drift_fail_closed_without_cache(self):
        contract = self.adapter.load_ordinary_appointment_contract()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative in [self.adapter.CONTRACT_RELATIVE, *contract['fingerprints']]:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / relative).read_bytes())
            with patch.object(self.adapter, 'ROOT', root):
                self.assertEqual(self.adapter.apply_ordinary_appointment_repair(source_row())['normalized_ref'], 'Jn 12:20-26')
                for relative in [self.adapter.CONTRACT_RELATIVE, *contract['fingerprints']]:
                    path = root / relative
                    original = path.read_bytes()
                    path.write_bytes(original + b' ')
                    with self.subTest(relative=relative), self.assertRaisesRegex(ValueError, 'drift'):
                        self.adapter.apply_ordinary_appointment_repair(source_row())
                    path.write_bytes(original)
                evidence = root / next(iter(contract['fingerprints']))
                original = evidence.read_bytes()
                evidence.unlink()
                with tempfile.TemporaryDirectory() as outside:
                    external = Path(outside) / 'evidence'
                    external.write_bytes(original)
                    evidence.symlink_to(external)
                    with self.assertRaises(ValueError):
                        self.adapter.apply_ordinary_appointment_repair(source_row())


class OrdinaryCoreIntegration(unittest.TestCase):
    def test_parser_index_and_reverse_matcher_through_real_correction_hook(self):
        cases = [(source_row(), 'Jn 12:20-26', 'John 12:26', 'John 12:27'),
                 (psalm_row(), 'Ps 79:13', 'Psalm 79:13', 'Psalm 79:12'),
                 (source_row('2026-07-19', day_title='The second Sunday of Abib', service_section='Liturgy',
                             reading_type='Catholic Epistle', raw_ref='Jude 14-25'),
                  'Jude 1:14-25', 'Jude 1:25', 'Jude 1:13'),
                 (source_row('2026-08-02', day_title='The fourth Sunday of Abib', service_section='Liturgy',
                             reading_type='Pauline Epistle', raw_ref='Php 1:27—  &  Php 2:1-11'),
                  'Phil 1:27-2:11', 'Philippians 2:11', 'Philippians 2:12')]
        for row, expected, hit, miss in cases:
            with self.subTest(ref=expected):
                evidence = ROOT / 'sources/coptic-reader/ordinary-appointment-qualified-2026-10-25/copticchurch' / (row['gregorian_date'] + '.html')
                _, rows = core.parse_copticchurch_html(evidence.read_text(), dt.date.fromisoformat(row['gregorian_date']))
                rows = [r for r in rows if r['service_section'] == row['service_section'] and r['reading_type'] == row['reading_type']]
                index = core.build_date_passage_index(rows)
                self.assertEqual([r['matched_ref'] for r in index], [expected])
                self.assertEqual(index[0]['raw_ref'], row['raw_ref'])
                self.assertTrue(passage_matches(hit, index[0]['matched_ref']))
                self.assertFalse(passage_matches(miss, index[0]['matched_ref']))

    def test_all_2020_through_2035_recurrences_and_neighbor_controls(self):
        from convertdate import coptic
        for year in range(2020, 2036):
            cy = coptic.from_gregorian(year, 9, 1)[0]
            mesra = dt.date(*coptic.to_gregorian(cy, 12, 26))
            baba_start = dt.date(*coptic.to_gregorian(cy + 1, 2, 1))
            fourth = baba_start + dt.timedelta(days=(6 - baba_start.weekday()) % 7 + 21)
            for row, expected in [(source_row(mesra.isoformat()), 'Jn 12:20-26'),
                                  (psalm_row(fourth.isoformat()), 'Ps 79:13')]:
                with self.subTest(date=row['gregorian_date']):
                    self.assertEqual(core.apply_copticchurch_source_correction(row)['normalized_ref'], expected)
                    for offset in [-1, 1]:
                        day = dt.date.fromisoformat(row['gregorian_date']) + dt.timedelta(days=offset)
                        neighbor = source_row(day.isoformat())
                        neighbor.update({k: v for k, v in row.items() if k not in ['gregorian_date', 'weekday', 'url']})
                        self.assertEqual(core.apply_copticchurch_source_correction(neighbor), neighbor)
        for date in ['2019-09-01', '2036-09-01']:
            row = source_row(date)
            self.assertEqual(core.apply_copticchurch_source_correction(row), row)


if __name__ == '__main__':
    unittest.main()
