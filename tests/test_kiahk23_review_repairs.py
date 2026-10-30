"""R2 source-qualified published-overlay regressions (no shared builder writes)."""
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from convertdate import coptic
import kiahk23_review_repairs as repair

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/coptic-reader/kiahk-23-qualified-2026-10-29'
EXPECTED = [('Vespers', 'Psalm', 'Psalms 131:7,8'),
            ('Vespers', 'Gospel', 'Jn 7:40-53'),
            ('Matins', 'Psalm', 'Psalms 88:13-15'),
            ('Matins', 'Gospel', 'Matt 12:1-8'),
            ('Liturgy', 'Pauline Epistle', 'Heb 11:32-40'),
            ('Liturgy', 'Catholic Epistle', 'James 5:7-13'),
            ('Liturgy', 'Acts of the Apostles', 'Acts 2:22-36'),
            ('Liturgy', 'Psalm', 'Psalms 77:61-63'),
            ('Liturgy', 'Gospel', 'Matt 22:35-46')]


def legacy():
    return json.loads((SOURCE / 'repair-approval/legacy-published-1.3.6.json').read_text())['reverse_rows']


def daily_fixture(date):
    # Complete ordinary table from the authenticated published reverse witness.
    rows = [copy.deepcopy(r) for r in legacy() if r['source_family'] == 'ordinary_date_resolved']
    for i, row in enumerate(rows, 1):
        row.update(occasion='Kiahk 23', reading_order=i)
        for key in ('calendar_keys', 'day_titles', 'attestation_years'):
            row.pop(key, None)
    return rows


def visible(rows):
    return [(r['service_section'], r['slot'], r['canonical_mt_ref'] or r['source_ref'])
            for r in rows if repair.is_current_reading(r)]


class Kiahk23ReviewRepairs(unittest.TestCase):
    def test_complete_reverse_replaces_moses_table_not_just_matins(self):
        output = repair.repair_reverse_rows(legacy())
        self.assertEqual(visible(output), EXPECTED)
        self.assertEqual(len(output), 29)

    def test_daily_is_exactly_nine_current_rows_with_history_only_in_reverse(self):
        source = {'2026-01-01': daily_fixture('2026-01-01'),
                  '2027-01-01': daily_fixture('2027-01-01')}
        before = copy.deepcopy(source)
        raw = legacy()
        raw_before = copy.deepcopy(raw)
        reverse = repair.repair_reverse_rows(raw)
        reverse_before = copy.deepcopy(reverse)
        output = repair.repair_daily(source, reverse)
        self.assertEqual(source, before)
        self.assertEqual(raw, raw_before)
        self.assertEqual(reverse, reverse_before)
        self.assertEqual(len(reverse), 29)
        self.assertTrue(all(not repair.is_current_reading(r) for r in reverse[:20]))
        self.assertEqual(visible(reverse), EXPECTED)
        lifecycle = {'active', 'status', 'current_status', 'removed_marker', 'kiahk23_retirement'}
        for original, retired in zip(raw, reverse[:20]):
            self.assertEqual({k:v for k,v in original.items() if k not in lifecycle},
                             {k:v for k,v in retired.items() if k not in lifecycle})
        for date, rows in output.items():
            self.assertEqual(len(rows), 9, date)
            self.assertTrue(all(repair.is_current_reading(r) for r in rows), date)
            self.assertEqual(visible(rows), EXPECTED, date)
            self.assertEqual([r['reading_order'] for r in rows], list(range(1, 10)))
            self.assertEqual([r['source_row_id'] for r in rows], ['R2:' + str(i) for i in range(1, 10)])
            self.assertTrue(all(r['gregorian_date'] == date for r in rows))
            self.assertTrue(all(r['weekday'] == dt.date.fromisoformat(date).strftime('%A') for r in rows))
            psalms = [r for r in rows if r['slot'] == 'Psalm']
            self.assertEqual(len(psalms), 3)
            for row in psalms:
                self.assertEqual(row['canonical_mt_ref'], '')
                self.assertEqual(row['canonical_lxx_ref'], '')
                self.assertEqual(json.loads(row['spans_json']), [])
        self.assertEqual(repair.repair_daily(output, reverse), output)
        self.assertEqual(repair.repair_daily(source, reverse), output)
        self.assertEqual(source, before)
        self.assertEqual(reverse, reverse_before)

    def test_daily_does_not_drop_or_retire_unrelated_inactive_rows(self):
        reverse = repair.repair_reverse_rows(legacy())
        for changes in ({'active': False}, {'current_status': 'historical_witness'},
                        {'removed_marker': 'source omitted'}, {'source_family': 'unrelated'}):
            data = {'2026-01-01': daily_fixture('2026-01-01')}
            data['2026-01-01'].append(dict(data['2026-01-01'][0], **changes))
            before = copy.deepcopy(data)
            with self.subTest(changes=changes):
                self.assertEqual(repair.repair_daily(data, reverse), before)
                self.assertEqual(data, before)

    def test_daily_mixed_replays_refuse_to_silently_remove_unqualified_extras(self):
        reverse = repair.repair_reverse_rows(legacy())
        good = repair.repair_daily({'2026-01-01': daily_fixture('2026-01-01')}, reverse)
        # A mixed old projection must be regenerated from raw, not cleaned by
        # trusting an inactivity flag, a retirement marker, or a copied receipt.
        historical = repair._retire(daily_fixture('2026-01-01')[0])
        for extra in (historical, dict(historical, kiahk23_retirement='{}'),
                      dict(historical, canonical_mt_ref='Matt 1:1-2'),
                      dict(historical, occasion='Nativity Paramoun'),
                      dict(historical, active=True, status='current', current_status='current')):
            data = copy.deepcopy(good)
            data['2026-01-01'].insert(0, extra)
            before = copy.deepcopy(data)
            with self.subTest(extra=extra), self.assertRaisesRegex(ValueError, 'Kiahk23 daily current-only'):
                repair.repair_daily(data, reverse)
            self.assertEqual(data, before)

    def test_daily_unknown_status_is_not_silently_discarded(self):
        data = {'2026-01-01': daily_fixture('2026-01-01')}
        data['2026-01-01'][0]['current_status'] = 'unsupported'
        with self.assertRaisesRegex(ValueError, 'Unknown explicit reading status'):
            repair.repair_daily(data, repair.repair_reverse_rows(legacy()))

    def test_daily_replay_refuses_order_drift(self):
        reverse = repair.repair_reverse_rows(legacy())
        good = repair.repair_daily({'2026-01-01': daily_fixture('2026-01-01')}, reverse)
        reordered = copy.deepcopy(good)
        reordered['2026-01-01'][0], reordered['2026-01-01'][1] = reordered['2026-01-01'][1], reordered['2026-01-01'][0]
        renumbered = copy.deepcopy(good)
        renumbered['2026-01-01'][0]['reading_order'] = 20
        for data in (reordered, renumbered):
            with self.assertRaisesRegex(ValueError, 'Kiahk23 daily reading order'):
                repair.repair_daily(data, reverse)

    def test_daily_replay_rejects_transplanted_dates_before_selection(self):
        reverse = repair.repair_reverse_rows(legacy())
        good = repair.repair_daily({'2026-01-01': daily_fixture('2026-01-01')}, reverse)['2026-01-01']
        for date in ('2027-01-01', '2026-01-02', '2028-01-02', '2034-01-01', '2019-01-01', '2036-01-02'):
            with self.subTest(date=date), self.assertRaisesRegex(ValueError, 'Kiahk23 projected'):
                repair.repair_daily({date: good}, reverse)

    def test_sunday_and_overriding_occasion_are_never_replaced(self):
        sunday = daily_fixture('2028-01-02')
        sunday[0]['occasion'] = 'Fourth Sunday of Kiahk'
        sunday[1]['canonical_mt_ref'] = 'Mark 3:28-35'
        sunday[-1]['canonical_mt_ref'] = 'Lk 1:57-80'
        feast = daily_fixture('2027-01-01')
        feast[-1]['occasion'] = 'Nativity Paramoun'
        data = {'2028-01-02': sunday, '2034-01-01': daily_fixture('2034-01-01'),
                '2027-01-01': feast, '2026-01-02': daily_fixture('2026-01-02')}
        self.assertEqual(repair.repair_daily(data, repair.repair_reverse_rows(legacy())), data)

    def test_bounded_2020_2035_all_supported_weekday_dates(self):
        dates = []
        for year in range(2019, 2037):
            cy = coptic.from_gregorian(year, 1, 5)[0]
            date = dt.date(*coptic.to_gregorian(cy, 4, 23))
            dates.append(date)
        source = {d.isoformat(): daily_fixture(d.isoformat()) for d in dates}
        output = repair.repair_daily(source, repair.repair_reverse_rows(legacy()))
        for date in dates:
            rows = output[date.isoformat()]
            if 2020 <= date.year <= 2035 and date.weekday() != 6:
                self.assertEqual(visible(rows), EXPECTED, date)
            else:
                self.assertEqual(rows, source[date.isoformat()], date)

    def test_actual_published_sunday_and_fresh_reader_matins_agree_and_survive(self):
        sunday = json.loads((SOURCE / 'repair-approval/published-sunday-2028-01-02.json').read_text())
        data = {'2028-01-02': sunday}
        self.assertEqual(repair.repair_daily(data, repair.repair_reverse_rows(legacy())), data)
        self.assertEqual([(r['service_section'], r['canonical_mt_ref']) for r in sunday if r['slot']=='Gospel'],
                         [('Vespers', 'Lk 8:1-3'), ('Matins', 'Mark 3:28-35'), ('Liturgy', 'Lk 1:57-80')])
        capture = SOURCE / 'repair-approval/sunday-2028-01-02'
        receipt = json.loads((capture / 'capture-receipt.json').read_text())
        self.assertEqual(receipt['occasion'], '4th Sunday of Koiahk')
        self.assertEqual(receipt['coptic_date'], 'Koiahk 23, 1744')
        self.assertEqual(receipt['printed_references'], ['Psalms 95:10,11,12', 'Mark 3:28-35'])
        self.assertEqual([int(line.split(' ', 1)[0]) for line in receipt['numbered_English_verse_lines']], list(range(28,36)))
        for relative, metadata in receipt['fingerprints'].items():
            self.assertEqual(hashlib.sha256((capture / relative).read_bytes()).hexdigest(), metadata['sha256'])

    def test_daily_present_calendar_weekday_and_outer_date_fields_are_mandatory(self):
        reverse = repair.repair_reverse_rows(legacy())
        for changes in ({'weekday':'Friday'}, {'gregorian_date':'2027-01-01'},
                        {'calendar_key':'Kiahk 24'}, {'coptic_date_key':'kiahk-24'},
                        {'coptic_date':'Koiahk 24, 1742'}):
            data = {'2026-01-01':daily_fixture('2026-01-01')}
            data['2026-01-01'][0].update(changes)
            self.assertEqual(repair.repair_daily(data, reverse), data, changes)

    def test_inactive_witnesses_and_cycle_raw_fields_remain_exact(self):
        rows = legacy()
        inactive = dict(rows[0], active=False, current_status='historical_witness')
        rows.append(inactive)
        before = copy.deepcopy(rows)
        output = repair.repair_reverse_rows(rows)
        self.assertEqual(rows, before)
        self.assertEqual(output[20], inactive)
        lifecycle = {'active', 'status', 'current_status', 'removed_marker', 'kiahk23_retirement'}
        for original, retained in zip(rows[:20], output[:20]):
            self.assertFalse(repair.is_current_reading(retained))
            self.assertEqual({k:v for k,v in retained.items() if k not in lifecycle},
                             {k:v for k,v in original.items() if k not in lifecycle})

    def test_public_current_predicate_agrees_with_actual_frozen_npm(self):
        cases = [dict(), {'active': False}, {'status': 'removed'},
                 {'removed_marker': 'superseded source'}, {'current_status': 'historical_witness'},
                 {'current_status': 'current_public_or_local_reference'},
                 {'current_status': 'current_working_source_not_coptic_reader_checked'},
                 {'current_status': 'pending_psalm_equivalence_unresolved'},
                 {'current_status': 'unsupported'}]
        # Extract the actual committed public predicate, not a duplicate oracle.
        code = (ROOT / 'scripts/build_npm_package.mjs').read_text()
        start = code.index('function isCurrentReading(row) {')
        end = code.index('\n}\n', start) + 2
        script = code[start:end] + '\nconsole.log(JSON.stringify(' + json.dumps(cases) + ".map(r=>{try{return isCurrentReading(r)}catch(e){return 'unknown'}})));"
        expected = json.loads(subprocess.check_output(['node', '-e', script], text=True))
        actual = []
        for row in cases:
            try:
                actual.append(repair.is_current_reading(row))
            except ValueError:
                actual.append('unknown')
        self.assertEqual(actual, expected)

    def test_inactive_and_wrong_family_kind_context_do_not_select(self):
        for changes in ({'active':False}, {'current_status':'historical_witness'},
                        {'source_kind':'other'}, {'source_family':'other'},
                        {'occasion':'Kiyahk 24'}, {'calendar_keys':'Kiyahk 24'}):
            rows = legacy()
            rows = [dict(r, **changes) for r in rows]
            self.assertEqual(repair.repair_reverse_rows(rows), rows, changes)
        rows = legacy()
        rows[0]['current_status'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'Unknown explicit reading status'):
            repair.repair_reverse_rows(rows)

    def test_psalms_are_source_only_with_no_inferred_numeric_spans(self):
        output = repair.repair_reverse_rows(legacy())
        psalms = [r for r in output if r.get('source_family') == repair.FAMILY and r['slot'] == 'Psalm']
        self.assertEqual(len(psalms), 3)
        for row in psalms:
            self.assertEqual(json.loads(row['spans_json']), [])
            self.assertEqual(row['canonical_mt_ref'], '')
            self.assertEqual(row['canonical_lxx_ref'], '')
            self.assertEqual(row['current_status'], 'pending_psalm_equivalence_unresolved')
            self.assertIn('source-only', row['canonicalization_note'])

    def test_qualified_rows_reject_context_coordinate_and_disclosure_mutations(self):
        rows = repair.repair_reverse_rows(legacy())
        good = next(r for r in rows if r.get('source_family') == repair.FAMILY)
        repair.qualify_row(good)
        for changes in ({'source_family':'other'}, {'source_kind':'other'},
                        {'occasion':'Fourth Sunday of Kiahk'}, {'source_ref':'Psalms 132:7,8'},
                        {'canonical_mt_ref':'Ps 132:10-11'}, {'spans_json':'[{"book":"Ps"}]'},
                        {'source_locator':'https://example.com/'}, {'active':False},
                        {'kiahk23_review_evidence':'{}'}, {'source_disclosure':'[]'},
                        {'coptic_date_key':'kiahk-24'}, {'calendar_key':'Kiahk 24'}):
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, 'Kiahk23 projected'):
                repair.qualify_row(dict(good, **changes))
            corrupted = [dict(r, **changes) if r is good else r for r in rows]
            with self.assertRaisesRegex(ValueError, 'Kiahk23 projected'):
                repair.repair_reverse_rows(corrupted)
            with self.assertRaisesRegex(ValueError, 'Kiahk23 projected'):
                repair.repair_daily({'2026-01-01':daily_fixture('2026-01-01')}, corrupted)
        with self.assertRaisesRegex(ValueError, 'Kiahk23.*date'):
            repair.qualify_row(good, civil_date='2028-01-02')

    def test_real_reverse_and_daily_callers_fail_closed_on_any_source_drift(self):
        rows = repair.repair_reverse_rows(legacy())
        real = repair._read
        targets = list(repair.authenticate_plan()['fingerprints']) + ['repair-approval/repair-plan.json']
        for target in targets:
            def drift(relative, target=target):
                raw = real(relative)
                return raw + b'corrupt' if relative.endswith(target) else raw
            with self.subTest(target=target), patch.object(repair, '_read', side_effect=drift):
                with self.assertRaisesRegex(ValueError, 'Kiahk23.*authentication'):
                    repair.repair_reverse_rows(legacy())
                with self.assertRaisesRegex(ValueError, 'Kiahk23.*authentication'):
                    repair.repair_daily({'2026-01-01':daily_fixture('2026-01-01')}, rows)

    def test_idempotency_and_daily_reverse_whole_table_agreement(self):
        reverse = repair.repair_reverse_rows(legacy())
        self.assertEqual(repair.repair_reverse_rows(reverse), reverse)
        data = {'2026-01-01': daily_fixture('2026-01-01')}
        daily = repair.repair_daily(data, reverse)
        self.assertEqual(repair.repair_daily(daily, reverse), daily)
        self.assertEqual(visible(daily['2026-01-01']), visible(reverse))
        # A corrupted or partial corrected reverse input cannot qualify a daily table.
        corrupt = copy.deepcopy(reverse)
        corrupt[-1]['source_locator'] = 'bad'
        with self.assertRaisesRegex(ValueError, 'Kiahk23 projected'):
            repair.repair_daily(data, corrupt)
        with self.assertRaisesRegex(ValueError, 'Kiahk23.*complete'):
            repair.repair_daily(data, reverse[:-1])

    def test_exact_type_complete_table_control_and_legacy_projection(self):
        from scripts import review_release_contract as contract
        from scripts import verify_package_integrity as validator

        plan = repair.authenticate_plan()
        rows = [repair._new_row(reading, plan) for reading in plan['appointments']]
        self.assertEqual(len(rows), 9)
        before = repair._json(rows)
        self.assertEqual(repair.repair_reverse_rows(rows), rows)
        daily = {'2026-01-01': [dict(row, reading_order=i, gregorian_date='2026-01-01',
                                      weekday='Thursday') for i, row in enumerate(rows, 1)]}
        daily_before = repair._json(daily)
        self.assertEqual(repair.repair_daily(daily, rows), daily)
        for row in rows:
            self.assertIs(row['active'], True)
            for field in ('source_order', 'source_token_order', 'slot_order'):
                self.assertIs(type(row[field]), int)
            self.assertIs(contract.source_owned_empty_coordinates(row), row['slot'] == 'Psalm')
        for row in daily['2026-01-01']:
            self.assertEqual(validator.validate_row_reference_bounds(row, date_key='2026-01-01'),
                             {'failures': [], 'unverified': []})
        original = legacy()
        original_before = repair._json(original)
        projected = repair.repair_reverse_rows(original)
        self.assertEqual(visible(projected), EXPECTED)
        self.assertEqual([r for r in projected if r.get('source_family') == repair.FAMILY], rows)
        self.assertEqual(sum(r['spans_json'] == '[]' for r in rows), 3)
        self.assertEqual(repair._json(original), original_before)
        self.assertEqual(repair._json(rows), before)
        self.assertEqual(repair._json(daily), daily_before)

    def test_exact_type_mutations_fail_at_real_projection_and_validation_boundaries(self):
        from scripts import review_release_contract as contract
        from scripts import verify_package_integrity as validator

        plan = repair.authenticate_plan()
        good = [repair._new_row(reading, plan) for reading in plan['appointments']]
        mutations = [{'source_order': True}, {'source_order': 1.0},
                     {'source_token_order': True}, {'source_token_order': 1.0},
                     {'slot_order': True}, {'slot_order': 1.0}, {'active': 1},
                     {'source_order': True, 'source_token_order': True, 'active': 1}]
        detail = 'Kiahk23 projected source/context/coordinate/disclosure drift'
        for index in (0, 1):  # Source-only Psalm and numeric Gospel must both qualify.
            for changes in mutations:
                rows = copy.deepcopy(good)
                # Keep the Gospel ordinal equal in value, changing only its type.
                changes = dict(changes)
                if index and 'source_order' in changes:
                    if type(changes['source_order']) is bool:
                        continue  # No bool is equal to ordinal 2.
                    changes['source_order'] = float(rows[index]['source_order'])
                rows[index].update(changes)
                daily = {'2026-01-01': [dict(row, reading_order=i, gregorian_date='2026-01-01',
                                              weekday='Thursday') for i, row in enumerate(rows, 1)]}
                good_daily = {'2026-01-01': [dict(row, reading_order=i, gregorian_date='2026-01-01',
                                                   weekday='Thursday') for i, row in enumerate(good, 1)]}
                snapshots = [repair._json(value) for value in (rows, daily, good, good_daily)]
                calls = [('reverse', lambda: repair.repair_reverse_rows(rows)),
                         ('daily-both-forged', lambda: repair.repair_daily(daily, rows)),
                         ('daily-owned-only', lambda: repair.repair_daily(daily, good)),
                         ('daily-reverse-only', lambda: repair.repair_daily(good_daily, rows)),
                         ('source-owned', lambda: contract.source_owned_empty_coordinates(rows[index])),
                         ('dated-source-owned', lambda: contract.source_owned_empty_coordinates(
                             daily['2026-01-01'][index], '2026-01-01'))]
                for boundary, call in calls:
                    with self.subTest(index=index, changes=changes, boundary=boundary):
                        with self.assertRaisesRegex(ValueError, '^' + detail + '$'):
                            call()
                        self.assertEqual([repair._json(value) for value in (rows, daily, good, good_daily)],
                                         snapshots)
                with self.subTest(index=index, changes=changes, boundary='reference-validation'):
                    self.assertEqual(validator.validate_row_reference_bounds(
                        daily['2026-01-01'][index], date_key='2026-01-01'),
                        {'failures': [{'reason': 'unqualified_empty_coordinate_appointment',
                                       'detail': detail}], 'unverified': []})
                    self.assertEqual([repair._json(value) for value in (rows, daily, good, good_daily)],
                                     snapshots)

    def test_original_receipt_still_denies_recurrence(self):
        auth = json.loads((SOURCE / 'retained-authentication.json').read_text())
        self.assertIs(auth['genericTemplateQualification'], False)
        self.assertEqual(auth['original_review_status'], 'qualified_exact_observed_date_table')
        plan = repair.authenticate_plan()
        self.assertIs(plan['retained_receipt_grants_recurrence'], False)
        self.assertIs(plan['canonical_psalm_alignment_approved'], False)


if __name__ == '__main__':
    unittest.main()
