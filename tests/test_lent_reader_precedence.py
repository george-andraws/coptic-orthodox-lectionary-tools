"""Complete retained Reader tables outrank legacy cycle fallback, never erase it."""
import copy
import csv
import datetime as dt
import json
import tempfile
from pathlib import Path
import unittest
from scripts import compare_external_sources as comparator

import build_design_deliverables as design
import build_lectionary_crosswalk as crosswalk
import build_lectionary_reference as ref
import verify_design_deliverables as validator

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())
DATE = '2026-02-18'
TITLE = 'Wednesday of the first week of Great Lent'


def fixture():
    source = ref.build_date_passage_index(ref.parse_copticchurch_html(
        (ROOT / 'cache/copticchurch_html' / f'{DATE}.html').read_text(), dt.date.fromisoformat(DATE))[1])
    with (ROOT / 'out/data/reverse_lookup_crosswalk.csv').open() as stream:
        cycle = [r for r in csv.DictReader(stream) if r.get('source_kind') == 'katameros_cycle'
                 and (r.get('calendar_key'), r.get('passage')) in {
                     ('week 1 day_of_week 3', 'Joel 2:12-27'), ('week 5 day_of_week 3', 'Joel 3:9-21')}]
    assert len(cycle) == 2
    presentation, _ = design.build_reverse_presentation(crosswalk.project_date_rows(source) + cycle)
    return source, presentation


def prophecies(rows):
    return [r for r in rows if r.get('service_section') == 'Matins' and r.get('slot_type') == 'prophecy']


class LentReaderPrecedence(unittest.TestCase):
    def test_complete_reader_group_wins_without_deleting_raw_cycle_witness(self):
        source, presentation = fixture()
        before = copy.deepcopy(presentation)
        daily = design.build_daily_year_files(presentation)[2026]
        self.assertEqual([r['canonical_mt_ref'] for r in prophecies(daily[DATE])], ['Isa 2:3-11', 'Joel 2:12-26'])
        self.assertEqual(presentation, before)
        self.assertTrue(any(r.get('canonical_mt_ref') == 'Joel 2:12-27' and not r.get('gregorian_date') for r in presentation))
        validator.verify_seasonal_daily(source, daily, POLICY)

    def test_validator_rejects_legacy_extra_even_with_intact_reader_rows(self):
        source, presentation = fixture()
        daily = design.build_daily_year_files(presentation)[2026]
        clean = [r for r in daily[DATE] if r.get('source_kind') != 'katameros_cycle']
        legacy = design.build_daily_year_files([r for r in presentation if r.get('source_family') != 'coptic_reader_verified_supplement'])[2026][DATE]
        legacy = next(r for r in legacy if r.get('source_kind') == 'katameros_cycle')
        for extra in (legacy, copy.deepcopy(prophecies(clean)[0])):
            with self.subTest(ref=extra['display_ref']), self.assertRaises(AssertionError):
                validator.verify_seasonal_daily(source, {DATE: [extra] + clean}, POLICY)

    def test_fake_incomplete_moved_or_forged_reader_does_not_suppress_fallback(self):
        _, presentation = fixture()
        for mutation in ('missing', 'duplicate', 'kind', 'family', 'file', 'rowid', 'slot', 'date', 'title', 'body', 'approval'):
            damaged = copy.deepcopy(presentation)
            target = next(r for r in damaged if r.get('source_family') == 'coptic_reader_verified_supplement')
            if mutation == 'missing': damaged.remove(target)
            elif mutation == 'duplicate': damaged.append(copy.deepcopy(target))
            elif mutation == 'kind': target['source_kind'] = 'coptic_reader_fixture'
            elif mutation == 'family': target['source_family'] = 'ordinary_date_resolved'
            elif mutation == 'file': target['source_file'] = 'wrong.txt'
            elif mutation == 'rowid': target['source_row_id'] += ':forged'
            elif mutation == 'slot': target['slot'] = 'OT99'
            elif mutation == 'date': target['gregorian_date'] = '2026-02-19'
            elif mutation == 'title': target['occasion'] = 'Other occasion'
            elif mutation == 'body': target['provenance'] = 'forged body authentication'
            else: target['canonical_equivalence_approved'] = True
            with self.subTest(mutation=mutation), self.assertRaises((AssertionError, RuntimeError, ValueError)):
                design.build_daily_year_files(damaged)

    def test_unqualified_context_still_projects_legacy_literal_endpoint(self):
        _, presentation = fixture()
        presentation = [r for r in presentation if r.get('source_family') != 'coptic_reader_verified_supplement']
        daily = design.build_daily_year_files(presentation)[2026][DATE]
        self.assertEqual([r['canonical_mt_ref'] for r in prophecies(daily)], ['Joel 2:12-27'])

    def test_validator_rejects_copied_disclosure_and_false_approval(self):
        source, presentation = fixture()
        daily = design.build_daily_year_files(presentation)[2026]
        daily[DATE] = [r for r in daily[DATE] if r.get('source_kind') != 'katameros_cycle']
        for mutation in ('disclosure', 'kind', 'approval', 'endpoint'):
            damaged = copy.deepcopy(daily)
            row = prophecies(damaged[DATE])[0]
            if mutation == 'disclosure': row['source_disclosure'] = '[]'
            elif mutation == 'kind': row['source_kind'] = 'coptic_reader_fixture'
            elif mutation == 'approval': row['canonical_equivalence_approved'] = True
            else: row['canonical_mt_ref'] = 'Joel 2:12-27'
            with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                validator.verify_seasonal_daily(source, damaged, POLICY)
    def test_independent_cycle_qualifier_keeps_unqualified_literal_fallback(self):
        _, presentation = fixture()
        templates = validator.qualified_lent_cycle_daily_rows(presentation, design.DAILY_READING_FIELDS)
        self.assertNotIn(TITLE, templates)
        legacy = [r for r in presentation if r.get('source_family') != 'coptic_reader_verified_supplement']
        templates = validator.qualified_lent_cycle_daily_rows(legacy, design.DAILY_READING_FIELDS)
        self.assertEqual(templates[TITLE]['canonical_mt_ref'], 'Joel 2:12-27')
        for mutation in ('missing', 'body', 'kind', 'locator', 'approval'):
            damaged = copy.deepcopy(presentation)
            row = next(r for r in damaged if r.get('source_family') == 'coptic_reader_verified_supplement')
            if mutation == 'missing': damaged.remove(row)
            elif mutation == 'body': row['provenance'] = 'forged'
            elif mutation == 'kind': row['source_kind'] = 'pascha_day_hour'
            elif mutation == 'locator': row['source_locator'] = 'forged.txt'
            else: row['canonical_equivalence_approved'] = True
            with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                validator.qualified_lent_cycle_daily_rows(damaged, design.DAILY_READING_FIELDS)

    def test_existing_supplement_kind_locator_guard_through_both_comparator_callers(self):
        date = '2026-03-18'
        source = ref.build_date_passage_index(ref.parse_copticchurch_html(
            (ROOT / 'cache/copticchurch_html' / f'{date}.html').read_text(), dt.date.fromisoformat(date))[1])
        presentation, _ = design.build_reverse_presentation(crosswalk.project_date_rows(source))
        daily = design.build_daily_year_files(presentation)[2026]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data/daily').mkdir(parents=True)
            (root / 'meta.json').write_text(json.dumps({'shipped_years': [2026]}))
            index = root / 'source.csv'
            with index.open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(source[0]))
                writer.writeheader()
                writer.writerows(source)
            for field, value in ((None, None), ('source_kind', 'pascha_day_hour'), ('source_locator', 'forged.txt')):
                damaged = copy.deepcopy(daily)
                if field:
                    target = next(r for r in damaged[date] if r.get('source_family') == 'coptic_reader_verified_supplement')
                    target[field] = value
                counters = comparator.contextual_counters(source, damaged, 2026, POLICY)
                with self.subTest(field=field, entry='counter'):
                    self.assertEqual(bool(counters[4]), field is not None)
                    if field is None:
                        self.assertEqual(counters[0], counters[1])
                (root / 'data/daily/lectionary-2026.json').write_text(json.dumps(damaged))
                result = comparator.compare_copticchurch_cache(root, index, [2026])
                with self.subTest(field=field, entry='full'):
                    self.assertEqual(result['status'], 'fail' if field else 'pass')


if __name__ == '__main__':
    unittest.main()
