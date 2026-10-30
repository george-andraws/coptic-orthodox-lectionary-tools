"""Bounded H1-H8 regressions; no corpus membership gate is replaced."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import holy_week_review_repairs as review

ROOT = Path(__file__).resolve().parents[1]


def legacy(day, hour, ref, slot='Gospel', **extra):
    from build_design_deliverables import identity_for
    return dict(identity_for(ref, 'pascha_day_hour'),
                source_kind='pascha_day_hour', source_family=review.LEGACY,
                occasion=day, day_title=day, calendar_key=day + ' | ' + hour,
                service_hour=hour, service_section=hour, slot=slot,
                reading_slot=slot, source_locator='original locator',
                source_title='original title', source_file='out/data/pascha_day_hour_index.csv',
                current_status='current_working_source_not_coptic_reader_checked',
                removed_marker='', gregorian_date='', **extra)


class HolyWeekReviewTests(unittest.TestCase):
    def test_h1_holds_all_live_wrong_night_but_preserves_inactive(self):
        source = [legacy('Tuesday Eve', 'First Hour', 'Lk 13:23-30'),
                  legacy('Tuesday Eve', 'Sixth Hour', 'Hos 4:15-5:7', 'OT1')]
        source[1].update(current_status='historical_candidate_removed', removed_marker='superseded by original')
        before = copy.deepcopy(source)
        out = review.repair_presentation_rows(source, add_reader=False)
        self.assertEqual(review.HOLD, out[0]['current_status'])
        self.assertEqual(before[1]['current_status'], out[1]['current_status'])
        self.assertEqual(before, source)
        for old, new in zip(before, out):
            for field in ['source_locator', 'source_title', 'calendar_key', 'identity_key']:
                self.assertEqual(old[field], new[field])

    def test_h4_only_sixth_is_held_and_new_reading_is_source_authenticated(self):
        source = [legacy('Good Friday', h, 'Jn 19:1-12') for h in ['Third Hour', 'Sixth Hour']]
        out = review.repair_presentation_rows(source)
        self.assertEqual(source[0]['current_status'], out[0]['current_status'])
        self.assertEqual(review.HOLD, out[1]['current_status'])
        new = [r for r in out if r.get('source_family') == review.FAMILY and r['canonical_mt_ref'] == 'Jn 19:13-27']
        self.assertEqual(1, len(new))
        self.assertEqual('current_confirmed_coptic_reader', new[0]['current_status'])
        review.validate_review_projection(out)

    def test_h5_both_gospels_preserved_without_global_duplicate_rule(self):
        source = [legacy('Great Thursday', h, 'Matt 26:17-19') for h in ['Third Hour', 'Ninth Hour']]
        out = review.repair_presentation_rows(source, add_reader=False)
        self.assertEqual([r['current_status'] for r in source], [r['current_status'] for r in out])
        self.assertTrue(all('H5' in r['holy_week_review_note'] for r in out))

    def test_h6_book_error_held_reader_ezekiel_added(self):
        out = review.repair_presentation_rows([legacy('Wednesday Eve', 'First Hour', 'Jer 43:5-11', 'OT1')])
        self.assertEqual(review.HOLD, out[0]['current_status'])
        self.assertTrue(any(r['canonical_mt_ref'] == 'Ezek 43:5-11' and r['current_status'] == 'current_confirmed_coptic_reader' for r in out))

    def test_eve_names_are_source_specific_and_dates_use_civil_evening(self):
        curated = legacy('Monday Eve', 'First Hour', 'Zech 1:1-6', 'OT1')
        printed = dict(curated, source_kind='pascha_source_text', source_family='holy_pascha')
        self.assertEqual('eve_of_tuesday', review.pascha_context(curated)['pascha_service'])
        self.assertEqual('eve_of_monday', review.pascha_context(printed)['pascha_service'])
        self.assertEqual('2026-04-06', review.pascha_context(curated, '2026-04-06')['pascha_civil_date'])
        with self.assertRaisesRegex(ValueError, 'civil date'):
            review.pascha_context(curated, '2026-04-05')
        self.assertEqual('eve_of_friday', review.pascha_context(legacy('Great Thursday Eve', 'First Hour', 'Jn 13:33-14:25'))['pascha_service'])

    def test_h2_only_source_backed_hours_activate_printed_candidates_do_not(self):
        out = review.repair_presentation_rows([])
        eve = [r for r in out if r.get('pascha_service') == 'eve_of_monday']
        self.assertEqual({'Third Hour', 'Eleventh Hour'}, {r['service_hour'] for r in eve})
        self.assertEqual({'Zeph 1:14-2:2', 'Lk 9:18-22', 'Mic 3:1-4', 'Matt 17:19-23'}, {r['canonical_mt_ref'] for r in eve})
        dates = review.project_review_dates(out, (2026, 2027, 2028))
        self.assertEqual({'2026-04-05', '2027-04-25', '2028-04-09'}, {r['gregorian_date'] for r in dates if r.get('pascha_service') == 'eve_of_monday'})

    def test_h7_galatians_eleventh_stays_historical_and_sixth_is_confirmed(self):
        historical = legacy('Good Friday', 'Eleventh Hour', 'Gal 3:1-6', 'Pauline')
        historical.update(source_family='holy_pascha', source_kind='pascha_source_text', current_status='historical_witness')
        out = review.repair_presentation_rows([historical])
        self.assertEqual('historical_witness', out[0]['current_status'])
        self.assertFalse(any(r['canonical_mt_ref'] == 'Gal 3:1-6' and r['current_status'].startswith('current') for r in out))
        self.assertTrue(any(r['canonical_mt_ref'] == 'Gal 6:14-18' and r['current_status'] == 'current_confirmed_coptic_reader' for r in out))
        self.assertEqual([], review.authenticate_document('friday--11th-hour')['pauline_readings'])

    def test_evidence_failure_reaches_repair_creation_and_downstream_validator(self):
        valid = review.repair_presentation_rows([])
        with patch.object(review, 'authenticate_document', side_effect=ValueError('capture authentication failed')):
            with self.assertRaisesRegex(ValueError, 'capture authentication failed'):
                review.repair_presentation_rows([])
            with self.assertRaisesRegex(ValueError, 'capture authentication failed'):
                review.validate_review_projection(valid)

    def test_reader_projection_rejects_context_reference_status_and_disclosure_forgery(self):
        valid = review.repair_presentation_rows([])[0]
        review.validate_review_projection([valid])
        for changes in [dict(occasion='Tuesday'), dict(service_hour='Ninth Hour'),
                        dict(canonical_mt_ref='Jn 1:1-12'), dict(current_status='historical_witness'),
                        dict(source_family='forged'), dict(source_locator='forged'),
                        dict(provenance='forged'), dict(source_order=True)]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                review.validate_review_projection([dict(valid, **changes)])

    def test_idempotent_no_duplicate_appointments_or_mutated_legacy_locators(self):
        first = review.repair_presentation_rows([legacy('Tuesday Eve', 'First Hour', 'Lk 13:23-30')])
        self.assertEqual(first, review.repair_presentation_rows(first))

    def test_wrong_family_neighbor_and_inactive_never_promoted(self):
        good = legacy('Wednesday Eve', 'Third Hour', 'Amos 4:4-13', 'OT1')
        wrong = dict(good, source_family='unrelated')
        neighbor = dict(good, service_hour='Ninth Hour', service_section='Ninth Hour')
        inactive = dict(good, current_status='historical_candidate_removed', removed_marker='superseded original')
        out = review.repair_presentation_rows([good, wrong, neighbor, inactive], add_reader=False)
        self.assertEqual('current_confirmed_coptic_reader', out[0]['current_status'])
        for actual, original in zip(out[1:], [wrong, neighbor, inactive]):
            self.assertEqual(original['current_status'], actual['current_status'])


class PublishedHolyWeekReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import hashlib
        path = ROOT / 'tests/fixtures/holy_week_review_1_3_6.json'
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == '8aa845a557e06b3b58a900335a8d5b695727ea934b76065bb2cf6d822762fc02'
        cls.fixture = json.loads(raw)

    def test_published_reverse_counts_exact_holds_confirmations_and_no_witness_loss(self):
        before = self.fixture['reverse_rows']
        self.assertEqual(414, len(before))
        self.assertEqual(247, sum(r['current_status'] == 'current_working_source_not_coptic_reader_checked' for r in before))
        after = review.repair_reverse_rows(before)
        self.assertEqual(len(before) + 11, len(after))
        self.assertEqual(17, sum(r['current_status'] == review.HOLD for r in after))
        self.assertEqual(53, sum(b['current_status'] != a['current_status'] and a['current_status'] == 'current_confirmed_coptic_reader' for b, a in zip(before, after)))
        for old, new in zip(before, after):
            for field in ['source_title', 'source_locator', 'calendar_keys', 'identity_key', 'spans_json']:
                self.assertEqual(old[field], new[field])
            if old['current_status'].startswith('historical') or old['removed_marker']:
                self.assertEqual(old['current_status'], new['current_status'])
                self.assertEqual(old['removed_marker'], new['removed_marker'])
        self.assertEqual(after, review.repair_reverse_rows(after))

    def test_published_daily_all_three_years_remove_holds_keep_h5_and_order_repair(self):
        reverse = review.repair_reverse_rows(self.fixture['reverse_rows'])
        for year, days in self.fixture['daily'].items():
            out = review.repair_daily_year(int(year), days, reverse)
            with self.subTest(year=year):
                self.assertEqual(sum(map(len, days.values())) - 6, sum(map(len, out.values())))
                self.assertFalse(any(r.get('current_status') == review.HOLD for rs in out.values() for r in rs))
                self.assertEqual(11, sum(r['source_family'] == review.FAMILY for rs in out.values() for r in rs))
                self.assertEqual(out, review.repair_daily_year(int(year), out, reverse))
                all_rows = [r for rs in out.values() for r in rs]
                self.assertFalse(any(r['occasion'] == 'Good Friday' and r['service_hour'] == 'Sixth Hour' and r.get('canonical_mt_ref') == 'Jn 19:1-12' for r in all_rows))
                self.assertEqual(2, sum(r['occasion'] == 'Great Thursday' and r.get('canonical_mt_ref') == 'Matt 26:17-19' for r in all_rows))
                self.assertFalse(any('saint' in key.lower() for r in all_rows for key in r))
                for date, rs in out.items():
                    self.assertEqual(list(range(1, len(rs) + 1)), [r['reading_order'] for r in rs])
                    for r in rs:
                        if r.get('pascha_service'):
                            self.assertEqual(date, r['pascha_civil_date'])
                friday = next(rs for rs in out.values() if any(r.get('pascha_service') == 'good_friday' for r in rs))
                sixth_gospels = [r['canonical_mt_ref'] for r in friday if r.get('service_hour') == 'Sixth Hour' and r.get('slot_type') == 'gospel']
                self.assertEqual(['Matt 27:27-45', 'Mark 15:26-33', 'Lk 23:26-44', 'Jn 19:13-27'], sixth_gospels)

    def test_complete_capture_byte_drift_fails_real_creation_and_validation(self):
        read = review._read
        def corrupt(path):
            data = read(path)
            return data + b'changed' if path.endswith('friday--6th-hour.txt') else data
        valid = review.repair_reverse_rows(self.fixture['reverse_rows'])
        with patch.object(review, '_read', side_effect=corrupt):
            with self.assertRaisesRegex(ValueError, 'capture authentication failed'):
                review.repair_reverse_rows(self.fixture['reverse_rows'])
            with self.assertRaisesRegex(ValueError, 'capture authentication failed'):
                review.validate_review_projection(valid)

    def test_reverse_order_shuffle_preserves_new_source_selection_order(self):
        reverse = review.repair_reverse_rows(self.fixture['reverse_rows'])
        days = self.fixture['daily']['2026']
        control = review.repair_daily_year(2026, days, reverse)
        shuffled = review.repair_daily_year(2026, days, list(reversed(reverse)))
        self.assertEqual(control, shuffled)

    def test_public_javascript_predicate_rejects_holds_and_structural_daily_never_restores_them(self):
        import subprocess
        reverse = review.repair_reverse_rows(self.fixture['reverse_rows'])
        held = [r for r in reverse if r['current_status'] == review.HOLD]
        days = review.repair_daily_year(2026, self.fixture['daily']['2026'], reverse)
        script = """
const fs = require('node:fs');
const api = require('./packages/lectionary-data');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const holdsCurrent = input.held.map(row => api.isCurrentReading(row));
const dailyCurrent = input.daily.every(row => api.isCurrentReading(row));
let unknownRefused = false;
try { api.isCurrentReading({current_status:'pending_coptic_reader_review'}); }
catch (error) { unknownRefused = error instanceof RangeError; }
process.stdout.write(JSON.stringify({holdsCurrent,dailyCurrent,unknownRefused}));
"""
        result = subprocess.run(['node', '-e', script], cwd=ROOT, text=True,
                                input=json.dumps(dict(held=held, daily=[r for rs in days.values() for r in rs])),
                                capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        actual = json.loads(result.stdout)
        self.assertEqual([False] * 17, actual['holdsCurrent'])
        self.assertTrue(actual['dailyCurrent'])
        self.assertTrue(actual['unknownRefused'])
        self.assertTrue(all(r.get('active') is False for r in held))

    def test_json_bridge_runs_in_fresh_process(self):
        import subprocess
        import sys
        result = subprocess.run([sys.executable, '-m', 'holy_week_review_repairs'],
                                input=json.dumps({'mode': 'reverse', 'rows': []}),
                                text=True, cwd=ROOT, capture_output=True, check=True)
        rows = json.loads(result.stdout)
        self.assertEqual(12, len(rows))
        review.validate_review_projection(rows)


if __name__ == '__main__':
    unittest.main()
