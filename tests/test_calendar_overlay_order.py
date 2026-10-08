"""Source-first prophecy-order regression; no downstream package-derived oracle."""
import copy
import csv
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import build_design_deliverables as design

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-04-07'
# Locked direct Pascha source appointments, including continuous-span normalization.
EXPECTED = [
    ('Tuesday', 'First Hour', 'OT1', 1, 'Exod 19:1-9'),
    ('Tuesday', 'First Hour', 'OT2', 2, 'Job 23:2-24:25'),
    ('Tuesday', 'First Hour', 'OT3', 3, 'Hos 4:1-8'),
    ('Tuesday', 'Third Hour', 'OT1', 1, 'Isa 5:20-30'),
    ('Tuesday', 'Third Hour', 'OT2', 2, 'Jer 9:12-19'),
    ('Tuesday', 'Sixth Hour', 'OT1', 1, 'Ezek 21:3-13'),
    ('Tuesday', 'Sixth Hour', 'OT2', 2, 'Sir 4:20-5:2'),
    ('Tuesday', 'Sixth Hour', 'OT3', 3, 'Isa 1:1-9'),
    ('Tuesday', 'Ninth Hour', 'OT1', 1, 'Gen 6:5-9:7'),
    ('Tuesday', 'Ninth Hour', 'OT2', 2, 'Isa 40:1-5'),
    ('Tuesday', 'Ninth Hour', 'OT3', 3, 'Prov 1:1-9'),
    ('Tuesday', 'Eleventh Hour', 'OT1', 1, 'Isa 50:1-3'),
    ('Tuesday', 'Eleventh Hour', 'OT2', 2, 'Wis 2:20-30'),
    ('Tuesday Eve', 'First Hour', 'OT1', 1, 'Zech 1:1-6'),
    ('Tuesday Eve', 'Third Hour', 'OT1', 1, 'Mal 1:1-9'),
    ('Tuesday Eve', 'Sixth Hour', 'OT1', 1, 'Hos 4:15-5:7'),
    ('Tuesday Eve', 'Ninth Hour', 'OT1', 1, 'Hos 10:12-11:2'),
    ('Tuesday Eve', 'Eleventh Hour', 'OT1', 1, 'Amos 5:6-14'),
]


def fixture():
    return [dict(gregorian_date=DATE, occasion=day, service_section=hour,
                 service_hour=hour, slot=slot, source_order=str(order),
                 display_ref=ref, source_kind='pascha_day_hour',
                 source_family='holy_pascha_curated_day_hour',
                 source_file='out/data/pascha_day_hour_index.csv',
                 current_status='current_working_source_not_coptic_reader_checked')
            for day, hour, slot, order, ref in EXPECTED]


def projected_tuples(rows):
    return [(r['occasion'], r['service_hour'], r['slot'], r['slot_order'], r['display_ref']) for r in rows if r['slot'].startswith('OT')]


class CalendarOverlayOrder(unittest.TestCase):
    def test_independent_direct_source_fixture_preserves_order_and_context(self):
        rows = fixture()
        original = copy.deepcopy(rows)
        daily = design.build_daily_year_files(rows)[2026][DATE]
        self.assertEqual(projected_tuples(daily), EXPECTED)
        self.assertEqual([r['slot_type'] for r in daily], ['prophecy'] * 18)
        self.assertEqual([r['service_section'] for r in daily], [r['service_section'] for r in rows])
        self.assertEqual(rows, original)

    def test_current_source_and_live_presentation_agree_with_direct_fixture(self):
        with (ROOT / 'out/data/copticchurch_passage_index_current_2020_2035.csv').open() as handle:
            source = [r for r in csv.DictReader(handle) if r['gregorian_date'] == DATE and r['source_slot'].startswith('OT')]
        self.assertCountEqual([(r['source_occasion'], r['service_section'], r['source_slot'], int(r['source_order']), r['matched_ref']) for r in source], EXPECTED)
        with (ROOT / 'out/data/pascha_day_hour_index.csv').open() as handle:
            direct = [r for r in csv.DictReader(handle) if r['day'] in ('Tuesday', 'Tuesday Eve') and r['slot'].startswith('OT')]
        self.assertCountEqual([(r['day'], r['hour'], r['slot'], int(r['order'])) for r in direct], [r[:4] for r in EXPECTED])
        presentation, _ = design.build_reverse_presentation()
        daily = design.build_daily_year_files(presentation, transport_mode='presentation')[2026][DATE]
        self.assertCountEqual(projected_tuples(daily), EXPECTED)
        self.assertEqual(len(daily), 38)

    def test_all_current_date_pascha_overlays_preserve_exact_source_context_order(self):
        with (ROOT / 'out/data/copticchurch_passage_index_current_2020_2035.csv').open() as handle:
            source = [r for r in csv.DictReader(handle) if r['source_ref_status'] == 'calendar_overlay' and r['source_slot'].startswith('OT')]
        self.assertEqual(len(source), 65)
        self.assertEqual({r['gregorian_date'] for r in source}, {'2026-04-07', '2031-04-07', '2034-04-07'})
        presentation, _ = design.build_reverse_presentation()
        daily = design.build_daily_year_files(presentation, transport_mode='presentation')
        for date in sorted({r['gregorian_date'] for r in source}):
            with self.subTest(date=date):
                expected = [(r['source_occasion'], r['service_section'], r['source_slot'], int(r['source_order']), r['matched_ref']) for r in source if r['gregorian_date'] == date]
                actual = [(r['occasion'], r['service_hour'], r['slot'], r['slot_order'], r['canonical_mt_ref']) for r in daily[int(date[:4])][date] if r['slot'].startswith('OT')]
                # Daily Psalm display includes the existing labeled LXX equivalent;
                # current-source matched_ref uses its preserved MT convention.
                self.assertCountEqual(actual, expected)

    def test_missing_invalid_and_conflicting_source_order_fail_closed(self):
        for order in ('', None, 'bogus', '0', '-1', '99', '2'):
            with self.subTest(order=order):
                row = dict(fixture()[0], source_order=order)
                with self.assertRaisesRegex(AssertionError, 'source.*order'):
                    design.build_daily_year_files([row])

    def test_non_target_and_unsupported_labels_do_not_inherit_prophecy_order(self):
        base = fixture()[0]
        for changes in ({'source_kind': 'copticchurch_date'}, {'source_family': 'ordinary_date_resolved'}, {'slot': 'Unknown label'}, {'slot': 'Psalm'}, {'slot': 'Gospel'}):
            with self.subTest(changes=changes):
                row = dict(base, **changes, slot_order='', slot_type='')
                daily = design.build_daily_year_files([row])[2026][DATE][0]
                self.assertEqual(daily['slot_order'], '')
                self.assertEqual(daily['slot_type'], '')
                self.assertEqual(daily['slot'], row['slot'])
        undated = dict(base, gregorian_date='')
        self.assertEqual(design.build_daily_year_files([undated]), {})

    def test_input_relative_order_is_not_inferred_from_package_or_renumbered(self):
        rows = list(reversed(fixture()))
        daily = design.build_daily_year_files(rows)[2026][DATE]
        self.assertEqual(projected_tuples(daily), list(reversed(EXPECTED)))
        # This projection only transports metadata: the strict comparator rejects
        # physical reorderings. It must not silently sort away upstream corruption.

    def test_design_validator_rejects_omission_truncation_reorder_and_wrong_context(self):
        import verify_design_deliverables as validator
        path = ROOT / 'out/design/daily/lectionary-2026.json'
        original_read = Path.read_text
        original = json.loads(path.read_text())
        # Establish a valid baseline before claiming any corruption was caught.
        validator.verify_rows()
        for mutation in ('omit', 'truncate', 'reorder', 'eve', 'section', 'order99'):
            with self.subTest(mutation=mutation):
                damaged = copy.deepcopy(original)
                rows = damaged[DATE]
                position = next(i for i, r in enumerate(rows) if r['slot'] == 'OT2' and r['occasion'] == 'Tuesday')
                if mutation == 'omit': rows.pop(position)
                elif mutation == 'truncate': rows[position]['display_ref'] = 'Job 23:2-24:24'
                elif mutation == 'reorder': rows[position], rows[position + 1] = rows[position + 1], rows[position]
                elif mutation == 'eve': rows[position]['occasion'] = 'Tuesday Eve'
                elif mutation == 'section': rows[position]['service_section'] = 'Third Hour'
                else: rows[position]['slot_order'] = 99
                def read_text(target, *args, **kwargs):
                    return json.dumps(damaged) if target == path else original_read(target, *args, **kwargs)
                with patch.object(Path, 'read_text', read_text):
                    with self.assertRaisesRegex(AssertionError, 'lectionary-2026.json does not exactly match'):
                        validator.verify_rows()


if __name__ == '__main__':
    unittest.main()
