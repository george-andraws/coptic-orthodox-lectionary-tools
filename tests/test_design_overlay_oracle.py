"""Independent source-oracle contract and exact daily corruption guards."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import verify_design_deliverables as validator

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / 'out/data/copticchurch_passage_index_current_2020_2035.csv'
DIRECT = ROOT / 'out/data/pascha_day_hour_index.csv'


def sources():
    current = dict(gregorian_date='2026-04-07', source_occasion='Tuesday',
                   service_section='First Hour', source_slot='OT2',
                   matched_ref='Job 23:2-24:25', source_order='2',
                   source_ref_status='calendar_overlay',
                   source_raw_refs='Job 23:2-17; Job 24:1-25')
    direct = dict(day='Tuesday', hour='First Hour', slot='OT2', order='2',
                  refs='Job 23:2-17; Job 24:1-25')
    return current, direct


class DesignOverlayOracle(unittest.TestCase):
    def test_locked_source_context_and_order_without_daily_or_builder(self):
        current, direct = sources()
        self.assertEqual(validator.calendar_overlay_source_orders([current], [direct]), {
            ('2026-04-07', 'Tuesday', 'First Hour', 'First Hour', 'OT2', 'Job 23:2-24:25'): 2})

    def test_missing_wrong_duplicate_direct_context_rejected(self):
        current, direct = sources()
        for changes in ({'day': 'Tuesday Eve'}, {'hour': 'Third Hour'},
                        {'slot': 'OT1'}, {'refs': 'Job 23:2-24:24'},
                        {'order': ''}, {'order': '99'}, {'order': '1'}):
            with self.subTest(changes=changes), self.assertRaises(AssertionError):
                validator.calendar_overlay_source_orders([current], [dict(direct, **changes)])
        for rows in ([], [direct, direct]):
            with self.subTest(rows=rows), self.assertRaises(AssertionError):
                validator.calendar_overlay_source_orders([current], rows)

    def test_duplicate_current_context_and_invalid_order_rejected(self):
        current, direct = sources()
        with self.assertRaises(AssertionError):
            validator.calendar_overlay_source_orders([current, current], [direct])
        for order in ('', 'bogus', '0', '-1', '99', '1'):
            with self.subTest(order=order), self.assertRaises(AssertionError):
                validator.calendar_overlay_source_orders([dict(current, source_order=order)], [direct])

    def test_real_oracle_covers_all_65_source_qualified_appointments(self):
        orders = validator.calendar_overlay_source_orders(validator.read_csv(CURRENT), validator.read_csv(DIRECT))
        self.assertEqual(len(orders), 65)
        self.assertEqual({date: sum(key[0] == date for key in orders) for date in {key[0] for key in orders}},
                         {'2026-04-07': 18, '2031-04-07': 19, '2034-04-07': 28})
        self.assertEqual(orders[('2026-04-07', 'Tuesday', 'First Hour', 'First Hour', 'OT2', 'Job 23:2-24:25')], 2)

    def test_validator_accepts_baseline_then_rejects_missing_or_wrong_source_context(self):
        validator.verify_rows()
        original = validator.read_csv
        rows = original(CURRENT)
        position = next(i for i, r in enumerate(rows) if r['gregorian_date'] == '2026-04-07' and r['source_slot'] == 'OT2' and r['service_section'] == 'First Hour')
        for field, value in (('source_occasion', 'Tuesday Eve'), ('service_section', 'Third Hour'),
                             ('matched_ref', 'Job 23:2-24:24'), ('source_order', '99'),
                             ('gregorian_date', '2026-04-08'), ('source_slot', 'OT1'),
                             ('omit', None), ('duplicate', None), ('extra', None)):
            damaged = copy.deepcopy(rows)
            if field == 'omit': damaged.pop(position)
            elif field == 'duplicate': damaged.append(copy.deepcopy(damaged[position]))
            elif field == 'extra': damaged.append(dict(damaged[position], gregorian_date='2026-04-08'))
            else: damaged[position][field] = value
            with self.subTest(field=field), patch.object(validator, 'read_csv', side_effect=lambda path: damaged if path == CURRENT else original(path)):
                with self.assertRaises(AssertionError):
                    validator.verify_rows()

    def test_exact_equality_rejects_duplicate_wrong_hour_and_order_on_all_overlay_dates(self):
        validator.verify_rows()
        original_read = Path.read_text
        for date in ('2026-04-07', '2031-04-07', '2034-04-07'):
            path = ROOT / f'out/design/daily/lectionary-{date[:4]}.json'
            original = json.loads(path.read_text())
            for mutation in ('duplicate', 'hour', 'order99', 'missing_order'):
                damaged = copy.deepcopy(original)
                rows = damaged[date]
                position = next(i for i, r in enumerate(rows) if r['slot'] == 'OT2')
                if mutation == 'duplicate': rows.insert(position, copy.deepcopy(rows[position]))
                elif mutation == 'hour': rows[position]['service_hour'] = 'Wrong Hour'
                elif mutation == 'order99': rows[position]['slot_order'] = 99
                else: rows[position]['slot_order'] = ''
                def read_text(target, *args, **kwargs):
                    return json.dumps(damaged) if target == path else original_read(target, *args, **kwargs)
                with self.subTest(date=date, mutation=mutation), patch.object(Path, 'read_text', read_text):
                    with self.assertRaisesRegex(AssertionError, 'does not exactly match'):
                        validator.verify_rows()


if __name__ == '__main__':
    unittest.main()
