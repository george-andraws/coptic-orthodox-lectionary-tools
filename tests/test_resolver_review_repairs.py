"""Bounded resolver/model repairs, with retained Reader and SQLite oracles."""
import copy
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import resolver_review_repairs as repairs

ROOT = Path(__file__).resolve().parents[1]


def gospel(date='2026-04-03'):
    return {'gregorian_date': date, 'day_title': repairs.LAST_FRIDAY,
            'service_section': 'Matins', 'reading_type': 'Gospel',
            'raw_ref': 'Lk 17:20-37', 'normalized_ref': 'Lk 17:20-37',
            'url': 'https://copticchurch.net/readings', 'source': 'copticchurch.net'}


def fragment(ref, order):
    span = {'book': 'Acts', 'chapter_start': 25 if order == 1 else 26,
            'chapter_end': 25 if order == 1 else 26,
            'verse_start': 23 if order == 1 else 1, 'verse_end': 27 if order == 1 else 6}
    return {'display_ref': ref, 'source_ref': ref, 'raw_ref': '44.25:23-27*@+44.26:1-6',
            'source_kind': 'katameros_cycle', 'source_family': 'katameros_cycle',
            'source_file': 'sources/katameros-api/Core/KatamerosDatabase.db',
            'source_table': 'GreatLentReadings', 'calendar_key': 'week 7 day_of_week 4',
            'service_section': 'liturgy_acts', 'slot': 'liturgy_acts',
            'source_row_id': str(5598 + order), 'source_locator': 'literal locator ' + str(order),
            'current_status': 'current_public_or_local_reference', 'removed_marker': '',
            'identity_key': 'fragment-' + str(order), 'spans_json': json.dumps([span])}


class LastFridayRepair(unittest.TestCase):
    def test_every_shipped_last_friday_uses_authenticated_noncollision_gospel(self):
        for date in ['2026-04-03', '2027-04-23']:
            original = [gospel(date)]
            saved = copy.deepcopy(original)
            actual = repairs.repair_last_friday_matins(original)
            self.assertEqual(actual[0]['normalized_ref'], 'Lk 16:19-31')
            self.assertEqual(actual[0]['raw_ref'], 'Lk 17:20-37')
            self.assertEqual(actual[0]['current_status'], 'current_confirmed_coptic_reader')
            self.assertIn('verified_date=2026-04-03', actual[0]['normalization_warning'])
            self.assertEqual(original, saved)
            self.assertEqual(repairs.repair_last_friday_matins(actual), actual)

    def test_boundary_and_unrelated_services_unchanged(self):
        for row in [gospel('2026-04-02'), dict(gospel(), day_title='Other'),
                    dict(gospel(), service_section='Liturgy'),
                    dict(gospel('2028-04-07'), source=repairs.BOUNDARY_SOURCE,
                         raw_ref='Luke 16:19-31', normalized_ref='Lk 16:19-31')]:
            self.assertEqual(repairs.repair_last_friday_matins([row]), [row])

    def test_removed_unknown_duplicate_or_foreign_payload_cannot_be_promoted(self):
        for fields in [{'removed_marker': 'removed'}, {'current_status': 'historical_witness'},
                       {'normalized_ref': 'Lk 1:1-4'}, {'current_status': 'unknown'}]:
            row = dict(gospel(), **fields)
            self.assertEqual(repairs.repair_last_friday_matins([row]), [row])
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            repairs.repair_last_friday_matins([gospel(), gospel()])

    def test_primary_authentication_failure_reaches_real_repair_caller(self):
        with patch.object(repairs, '_authenticate_last_friday', side_effect=ValueError('source drift')):
            with self.assertRaisesRegex(ValueError, 'source drift'):
                repairs.repair_last_friday_matins([gospel()])


class OccurrenceMetadata(unittest.TestCase):
    def test_full_computus_cycle_distinguished_from_shipped_occurrence(self):
        row = {'coptic_date_key': 'baramouda-30', 'display_ref': 'Mark 1:1-11',
               'service_section': 'Liturgy', 'slot': 'Gospel'}
        meta = repairs.annotate_calendar_occurrence(row, {2026: {}, 2027: {}, 2028: {}})
        self.assertFalse(meta['occurs_in_shipped_years'])
        self.assertFalse(meta['occurs_outside_paschal_seasons'])
        self.assertEqual(meta['displaced_by'], ['holy_fifty'])
        self.assertEqual(meta['occurrence_scope']['computus_cycle_years'], 532)
        self.assertEqual(row.get('occurs_in_shipped_years'), None)

    def test_just_outside_always_displaced_band_has_real_cycle_counterexample(self):
        # Baramhat 3 is March 12 in 2078, 57 days before Pascha May 8.
        # Baramhat 6 (March 15) is always in Lent, not a valid counterexample.
        row = {'coptic_date_key': 'baramhat-3', 'display_ref': 'Gal 1:1-19',
               'service_section': 'Liturgy', 'slot': 'Pauline Epistle'}
        result = repairs.annotate_calendar_occurrence(row, {2026: {}})
        self.assertTrue(result['occurs_outside_paschal_seasons'])
        self.assertIn('great_lent', result['displaced_by'])

    def test_shipped_occurrence_matches_actual_date_service_and_complete_reference(self):
        row = {'coptic_date_key': 'tout-2', 'display_ref': 'Mark 1:1-11',
               'service_section': 'liturgy_gospel', 'slot': 'liturgy_gospel'}
        daily = {2026: {'2026-09-12': [{'display_ref': 'Mark 1:1-11',
                                      'service_section': 'Liturgy', 'slot': 'Gospel'}]}}
        self.assertTrue(repairs.annotate_calendar_occurrence(row, daily)['occurs_in_shipped_years'])
        daily[2026]['2026-09-12'][0]['display_ref'] = 'Mark 1:1-10'
        self.assertFalse(repairs.annotate_calendar_occurrence(row, daily)['occurs_in_shipped_years'])

    def test_annual_sunday_is_not_bare_fixed_day_and_no_seasonal_rows_annotated(self):
        row = {'annual_sunday': 'bashans-3', 'display_ref': 'Lk 10:25-37',
               'service_section': 'Liturgy', 'slot': 'Gospel'}
        result = repairs.annotate_calendar_occurrence(row, {2026: {}})
        self.assertFalse(result['occurs_outside_paschal_seasons'])
        self.assertEqual(result['displaced_by'], ['holy_fifty'])
        with self.assertRaisesRegex(ValueError, 'mutually exclusive'):
            repairs.annotate_calendar_occurrence(dict(row, coptic_date_key='bashans-3'), {})
        self.assertEqual(repairs.annotate_calendar_occurrence({'calendar_keys': 'Great Lent'}, {}), {'calendar_keys': 'Great Lent'})

    def test_generic_fifth_sunday_metadata_accepts_calendar_sentinel(self):
        row = {'annual_sunday': 'any-month-5', 'display_ref': 'Lk 9:10-17',
               'service_section': 'Liturgy', 'slot': 'Gospel'}
        daily = {2026: {'2026-03-08': [dict(row)]}}
        result = repairs.annotate_calendar_occurrence(row, daily)
        self.assertTrue(result['occurs_in_shipped_years'])
        self.assertTrue(result['occurs_outside_paschal_seasons'])
        with self.assertRaisesRegex(ValueError, 'Invalid'):
            repairs.annotate_calendar_occurrence(dict(row, annual_sunday='any-month-4'), daily)

    def test_source_only_current_psalm_counts_as_present_without_numeric_claim(self):
        row = {'coptic_date_key': 'kiahk-23', 'display_ref': 'Psalms 88:13-15',
               'service_section': 'Matins', 'slot': 'Psalm', 'active': True,
               'current_status': 'pending_psalm_equivalence_unresolved', 'spans_json': '[]'}
        daily = {2026: {'2026-01-01': [dict(row)]}}
        self.assertTrue(repairs.annotate_calendar_occurrence(row, daily)['occurs_in_shipped_years'])
        daily[2026]['2026-01-01'][0]['active'] = False
        self.assertFalse(repairs.annotate_calendar_occurrence(row, daily)['occurs_in_shipped_years'])

    def test_easter_matches_independent_known_dates_and_century_shift(self):
        for year, date in [(2026, '2026-04-12'), (2027, '2027-05-02'),
                           (2028, '2028-04-16'), (2100, '2100-05-02')]:
            self.assertEqual(repairs.pascha(year).isoformat(), date)


class CompositeModel(unittest.TestCase):
    def test_one_proven_database_cell_becomes_one_ordered_appointment_without_loss(self):
        original = [fragment('Acts 26:1-6', 2), fragment('Acts 25:23-27', 1)]
        actual, report = repairs.merge_proven_composites(original)
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0]['display_ref'], 'Acts 25:23-27; Acts 26:1-6')
        self.assertEqual([s['chapter_start'] for s in json.loads(actual[0]['spans_json'])], [25, 26])
        evidence = json.loads(actual[0]['composite_fragments_json'])
        self.assertEqual(evidence, original[::-1])
        self.assertEqual(len(report), 1)
        self.assertEqual(repairs.merge_proven_composites(actual), (actual, []))

    def test_different_context_or_inactive_fragment_is_not_silently_merged(self):
        original = [fragment('Acts 25:23-27', 1), fragment('Acts 26:1-6', 2)]
        for mutation in [{'calendar_key': 'week 6 day_of_week 4'},
                         {'source_family': 'other'}, {'removed_marker': 'removed'},
                         {'current_status': 'historical_witness'}, {'slot': 'other'}]:
            rows = [original[0], dict(original[1], **mutation)]
            actual, events = repairs.merge_proven_composites(rows)
            self.assertEqual(actual, rows)
            self.assertEqual(events, [])

    def test_not_just_same_slot_or_coordinate_adjacency(self):
        original = [fragment('Acts 25:23-27', 1), fragment('Acts 26:1-6', 2)]
        rows = [dict(r, raw_ref='unproven') for r in original]
        self.assertEqual(repairs.merge_proven_composites(rows), (rows, []))
        rows = [original[0], dict(original[1], display_ref='Acts 26:1-5')]
        with self.assertRaisesRegex(ValueError, 'incomplete|fragment'):
            repairs.merge_proven_composites(rows)


class BelCorrection(unittest.TestCase):
    def row(self):
        return {'source_kind': 'katameros_cycle', 'source_family': 'katameros_cycle',
                'source_table': 'GreatLentReadings', 'source_file': repairs.DATABASE,
                'calendar_key': 'week 4 day_of_week 5', 'service_section': 'prophecy',
                'reading_slot': 'prophecy', 'raw_ref': '5.10:12-22*@+5.11:1-28@23.29:12-23@18.21:1-34@27.1:1-42',
                'source_ref': 'Dan 1:1-42', 'passage': 'Dan 1:1-42'}

    def test_correct_source_coordinates_not_fabricated_brenton_equivalence(self):
        row = self.row()
        actual = repairs.bel_identity_for(row)
        self.assertEqual(actual['display_ref'], 'Bel 1:1-42 (Reader Daniel 14:1-42)')
        span, = json.loads(actual['spans_json'])
        self.assertEqual(span['book'], 'Bel')
        self.assertEqual((span['chapter_start'], span['verse_end']), (1, 42))
        self.assertEqual(span['source_ref'], 'Daniel 14:1-42')
        self.assertEqual(actual['canonical_mt_ref'], '')
        self.assertIn('not certified', actual['canonicalization_note'])
        self.assertEqual(row['source_ref'], 'Dan 1:1-42')

    def test_context_and_source_drift_fail_closed(self):
        self.assertIsNone(repairs.bel_identity_for(dict(self.row(), calendar_key='week 5 day_of_week 5')))
        self.assertIsNone(repairs.bel_identity_for(dict(self.row(), source_ref='Dan 1:1-21', passage='Dan 1:1-21')))
        with patch.object(repairs, '_authenticate_bel', side_effect=ValueError('Bel source drift')):
            with self.assertRaisesRegex(ValueError, 'Bel source drift'):
                repairs.bel_identity_for(self.row())


class RetainedSourceIntegration(unittest.TestCase):
    def test_real_date_csv_changes_only_fourteen_noncollision_matins_gospels(self):
        fixture = json.loads((ROOT / 'tests/fixtures/resolver_review_published_1_3_6.json').read_text())
        rows = fixture['last_friday_matins']
        actual = repairs.repair_last_friday_matins(rows)
        changed = [(a, b) for a, b in zip(rows, actual) if a != b]
        self.assertEqual(len(changed), 14)
        self.assertIn('2026-04-03', {a['gregorian_date'] for a, _ in changed})
        self.assertIn('2027-04-23', {a['gregorian_date'] for a, _ in changed})
        self.assertNotIn('2028-04-07', {a['gregorian_date'] for a, _ in changed})
        for before, after in changed:
            self.assertEqual(before['normalized_ref'], 'Luke 17:20-37')
            self.assertEqual(after['normalized_ref'], 'Lk 16:19-31')
            self.assertEqual(after['raw_ref'], before['raw_ref'])
            self.assertEqual(after['url'], before['url'])
        self.assertEqual(repairs.repair_last_friday_matins(actual), actual)

    def test_real_retained_body_drift_fails_at_repair_not_only_helper(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            capture = root / repairs.LAST_FRIDAY_CAPTURE
            shutil.copytree(ROOT / repairs.LAST_FRIDAY_CAPTURE, capture)
            (capture / 'Psalm_and_Gospel.txt').write_text('Luke 17:20-37')
            with patch.object(repairs, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'source drift'):
                    repairs.repair_last_friday_matins([gospel()])

    def test_real_crosswalk_sixtynine_proven_composites_retain_every_fragment(self):
        from passage_normalization import parse_passage
        fixture = json.loads((ROOT / 'tests/fixtures/resolver_review_published_1_3_6.json').read_text())
        rows = fixture['composite_fragments']
        for row in rows:
            parsed = parse_passage(row['passage'])
            row['display_ref'] = row['passage']
            row['identity_key'] = 'raw-' + row['source_row_id']
            row['source_locator'] = row['source_file'] + ':row ' + row['source_row_id']
            row['spans_json'] = json.dumps([{'book': parsed.book_abbrev,
                'chapter_start': part.chapter_start, 'verse_start': part.verse_start,
                'chapter_end': part.chapter_end, 'verse_end': part.verse_end} for part in parsed.parts])
        actual, report = repairs.merge_proven_composites(rows)
        self.assertEqual((len(rows), len(actual), len(report)), (138, 69, 69))
        recovered = [fragment for row in actual for fragment in json.loads(row['composite_fragments_json'])]
        key = lambda row: row['source_row_id']
        self.assertEqual(sorted(recovered, key=key), sorted(rows, key=key))
        corrupted = [fragment('Acts 25:23-27', 1), fragment('Acts 26:1-6', 2)]
        corrupted[1]['spans_json'] = corrupted[0]['spans_json']
        with self.assertRaisesRegex(ValueError, 'coordinates'):
            repairs.merge_proven_composites(corrupted)

    def test_existing_parser_book_code_compatibility_is_explicit_not_global_alias(self):
        from passage_normalization import parse_passage
        self.assertEqual(parse_passage('Bel 1:1-42').book_abbrev, 'Bel')
        self.assertEqual(parse_passage('Dan 14:1-42').book_abbrev, 'Dan')
        self.assertEqual(parse_passage('Dan 1:1-42').book_abbrev, 'Dan')
        self.assertIsNone(parse_passage('Bel and the Dragon 1:1-42'))

    def test_seasonal_coincidence_is_not_an_annual_appointment_occurrence(self):
        row = {'coptic_date_key': 'baramhat-6', 'display_ref': 'Gal 1:1-19',
               'service_section': 'Liturgy', 'slot': 'Pauline Epistle'}
        date = next(repairs._candidate_dates(2026, 7, 6, False)).isoformat()
        seasonal = dict(row, occasion='Great Lent', coptic_date_key='')
        daily = {2026: {date: [seasonal]}}
        self.assertFalse(repairs.annotate_calendar_occurrence(row, daily)['occurs_in_shipped_years'])


class PublishedLikeRuntimeAPI(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / 'tests/fixtures/resolver_review_runtime_1_3_6.json').read_text())

    def test_complete_daily_arrays_correct_only_qualified_slots_and_keep_source_fields(self):
        fixture = self.fixture()
        for date, original in fixture['daily'].items():
            actual, events = repairs.repair_daily_rows(date, original)
            self.assertEqual(repairs.repair_daily_rows(date, actual), (actual, []))
            self.assertEqual([r['reading_order'] for r in actual], list(range(1, len(actual) + 1)))
            if date == '2028-04-07':
                self.assertEqual(actual, original)
                self.assertEqual(events, [])
                continue
            if date == '2026-04-02':
                self.assertEqual(len(actual), len(original) - 1)
                merged, = [r for r in actual if r['display_ref'] == 'Acts 25:23-27; Acts 26:1-6']
                fragments = json.loads(merged['composite_fragments_json'])
                originals = [r['_review_original_row'] for r in fragments]
                self.assertEqual(originals, [r for r in original if r['display_ref'] in {'Acts 25:23-27', 'Acts 26:1-6'}])
            else:
                changed = [(a, b) for a, b in zip(original, actual) if a != b]
                self.assertEqual(len(changed), 1)
                before, after = changed[0]
                self.assertEqual(after['display_ref'], 'Lk 16:19-31')
                for field in ('source_family', 'source_kind', 'source_locator', 'source_row_id'):
                    self.assertEqual(before[field], after[field])
                disclosure = json.loads(after['resolver_review_disclosure'])
                self.assertEqual(disclosure['original'], before)
                self.assertEqual(disclosure['policy']['verified_date'], '2026-04-03')
                self.assertEqual(disclosure['policy']['pascha_offset'], -9)

    def test_reverse_keeps_old_witness_and_joins_only_proven_source_appointment(self):
        original = self.fixture()['reverse']
        actual, events = repairs.repair_reverse_rows(original)
        self.assertEqual(len(actual), len(original) - 1)
        old, = [r for r in actual if r['display_ref'] == 'Lk 17:20-37']
        self.assertEqual(old['current_status'], 'historical_witness')
        self.assertTrue(old['removed_marker'])
        self.assertEqual({e['id'] for e in events}, {'R1', 'R4', 'R6'})
        bel, = [r for r in actual if r['display_ref'].startswith('Bel ')]
        self.assertEqual(bel['source_locator'], next(r['source_locator'] for r in original if r['display_ref'] == 'Dan 1:1-42'))
        self.assertEqual(repairs.repair_reverse_rows(actual), (actual, []))

    def test_real_daily_caller_rejects_forged_source_locator_and_outer_date(self):
        rows = self.fixture()['daily']['2026-04-03']
        wrong = copy.deepcopy(rows)
        next(r for r in wrong if r['display_ref'] == 'Lk 17:20-37')['source_locator'] = 'forged'
        with self.assertRaisesRegex(ValueError, 'source locator'):
            repairs.repair_daily_rows('2026-04-03', wrong)
        with self.assertRaisesRegex(ValueError, 'source/date/service'):
            repairs.repair_daily_rows('2027-04-23', rows)
        with patch.object(repairs, '_authenticate_last_friday', side_effect=ValueError('source drift')):
            with self.assertRaisesRegex(ValueError, 'source drift'):
                repairs.repair_daily_rows('2026-04-03', rows)

    def test_full_pascha_range_has_all_thirtyfive_coptic_dates_and_repeats(self):
        keys = {repairs.coptic_key(repairs.pascha(y)) for y in range(2000, 2532)}
        self.assertEqual(len(keys), 35)
        for month, day in [(7, 3), (7, 6), (8, 30)]:
            a = {(d - repairs.pascha(d.year)).days for y in range(2000, 2532)
                 for d in repairs._candidate_dates(y, month, day, False)}
            b = {(d - repairs.pascha(d.year)).days for y in range(2532, 3064)
                 for d in repairs._candidate_dates(y, month, day, False)}
            self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
