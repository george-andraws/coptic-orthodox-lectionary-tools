"""Adversarial cached-source preservation tests; fixtures are independent source rows."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import compare_external_sources as comparator
from historical_review_fixture import published_1_3_7, historical_policy

CURRENT = ROOT / 'out/data/copticchurch_passage_index_current_2020_2035.csv'
CORRECTIONS = ROOT / 'sources/lectionary_corrections.json'


class ContextComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CURRENT.open(newline='', encoding='utf-8') as handle:
            cls.source = list(csv.DictReader(handle))
        # Historical preservation/mutation contract, not successor materialization.
        cls.daily = published_1_3_7()['daily']['2026']
        historical_policy()  # Bind the retained source rows to their pinned policy.

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.package = self.root / 'package'
        (self.package / 'data/daily').mkdir(parents=True)
        (self.package / 'meta.json').write_text(json.dumps({'version': '1.3.7', 'shipped_years': [2026]}))

    def fixtures(self, date):
        return [copy.deepcopy(r) for r in self.source if r['gregorian_date'] == date], {date: copy.deepcopy(self.daily[date])}

    def suppression_fixture(self):
        # Current materialization has already applied the no-Vespers rule. Test
        # preservation of the conflicting earlier witness explicitly, without
        # making supported consumers fall back to that historical snapshot.
        source, daily = self.fixtures('2026-02-02')
        historical = ROOT / 'out/data/copticchurch_passage_index_2020_2035.csv'
        with historical.open(newline='', encoding='utf-8') as handle:
            vespers = [row for row in csv.DictReader(handle)
                       if row['gregorian_date'] == '2026-02-02' and row['service_section'] == 'Vespers']
        self.assertEqual(len(vespers), 2)
        self.assertFalse(any(row['service_section'] == 'Vespers' for row in source))
        source.extend({field: row.get(field, '') for field in self.source[0]} for row in vespers)
        return source, daily

    def compare(self, source, daily, *, version='1.3.7', **kwargs):
        index = self.root / 'current.csv'
        with index.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=self.source[0].keys())
            writer.writeheader()
            writer.writerows(source)
        (self.package / 'data/daily/lectionary-2026.json').write_text(json.dumps(daily))
        (self.package / 'meta.json').write_text(json.dumps({'version': version, 'shipped_years': [2026]}))
        return comparator.compare_copticchurch_cache(self.package, index, [2026], **kwargs)

    def rejected(self, source, daily, **kwargs):
        # Only the intended prerequisite categories may short-circuit parity;
        # an unrelated assertion must not turn a broken valid control green.
        try:
            result = self.compare(source, daily, **kwargs)
        except AssertionError as error:
            self.assertRegex(str(error), r'Evidence SHA-256 mismatch:|Calendar overlay lacks the exact documented correction context|Unqualified recurring supplement:')
            return
        self.assertEqual(result['status'], 'fail', result)

    def test_supported_default_is_current_not_legacy(self):
        self.assertEqual(comparator.SOURCE_INDEX, CURRENT)

    def test_verified_prophecy_labels_compare_without_losses(self):
        source, daily = self.fixtures('2026-03-04')
        self.assertEqual(self.compare(source, daily)['status'], 'pass')

    def test_prophecy_omitted_duplicate_truncated_reordered_and_extra(self):
        source, original = self.fixtures('2026-03-04')
        for mutation in ('omitted', 'duplicate', 'truncated', 'reordered', 'extra', 'slot_order', 'removed'):
            with self.subTest(mutation=mutation):
                daily = copy.deepcopy(original)
                rows = daily['2026-03-04']
                if mutation == 'omitted': rows.pop(0)
                elif mutation == 'duplicate': rows.append(copy.deepcopy(rows[0]))
                elif mutation == 'truncated': rows[1]['display_ref'] = 'Joel 2:21-26'
                elif mutation == 'reordered': rows[0], rows[1] = rows[1], rows[0]
                elif mutation == 'extra': rows.append(dict(rows[0], display_ref='Exod 4:19-31'))
                elif mutation == 'slot_order': rows[0]['slot_order'] = 2
                elif mutation == 'removed': rows.append(dict(rows[0], active=False, status='removed'))
                self.rejected(source, daily)

    def test_prophecy_wrong_context_and_provenance(self):
        source, original = self.fixtures('2026-03-04')
        for field, value in [('occasion', 'Wednesday of the fourth week of Great Lent'), ('service_hour', 'Third Hour'), ('source_family', 'ordinary_date_resolved'), ('source_file', 'wrong-source.txt'), ('slot', 'OT10')]:
            with self.subTest(field=field):
                daily = copy.deepcopy(original)
                daily['2026-03-04'][0][field] = value
                self.rejected(source, daily)
        for field, value in [('source', 'copticchurch.net daily scrape'), ('day_title', 'Wrong title'), ('gregorian_date', '2026-03-05'), ('service_section', 'Liturgy'), ('source_order', '2'), ('source_slot', 'OT10'), ('correction_source', 'wrong-source.txt')]:
            with self.subTest(source_field=field):
                rows = copy.deepcopy(source)
                next(r for r in rows if r['source_slot'] == 'OT1')[field] = value
                self.rejected(rows, original)

    def overlay_fixture(self):
        # Exercise authenticated published 1.3.7 bytes; no slot metadata repair.
        return self.fixtures('2026-04-07')

    def test_pinned_pre_review_overlay_source_order_and_unknown99_corruption(self):
        # Historical facts belong to their authenticated predecessor package,
        # not the 1.3.7 table with 15 retired Eve rows and five new selections.
        fixture = (ROOT / 'tests/fixtures/holy_week_review_1_3_6.json').read_bytes()
        self.assertEqual(hashlib.sha256(fixture).hexdigest(), '8aa845a557e06b3b58a900335a8d5b695727ea934b76065bb2cf6d822762fc02')
        self.assertEqual(hashlib.sha256(CURRENT.read_bytes()).hexdigest(), 'd373b55d42f78209a74ee1533884c81c357995333e58e884b76b2d0c14e2b2dd')
        source, _ = self.fixtures('2026-04-07')
        daily = {'2026-04-07': json.loads(fixture)['daily']['2026']['2026-04-07']}
        self.assertEqual(self.compare(source, daily, version='1.3.6')['status'], 'pass')
        self.assertEqual(self.compare(source, daily, version='1.3.6')['years']['2026']['comparable_package_rows'], 38)
        prophecies = [row for row in daily['2026-04-07'] if row['slot'].startswith('OT')]
        self.assertEqual(len(prophecies), 18)
        for row in prophecies:
            row['slot_order'] = 99
        result = self.compare(source, daily, version='1.3.6')
        self.assertEqual(result['status'], 'fail')
        self.assertEqual(result['years']['2026']['mismatch_rows'], 36)
        self.assertEqual({r['slot_order'] for r in result['comparison_rows'] if r['status'] == 'package_only_extra_vs_source'}, {'99'})

    def test_overlay_compared_symmetrically_in_full_day_eve_hour_context(self):
        source, daily = self.overlay_fixture()
        result = self.compare(source, daily)
        self.assertEqual(result['status'], 'pass', result)
        self.assertEqual(result['years']['2026']['comparable_package_rows'], 28)
        self.assertEqual(sum(r['slot'].startswith('OT') for r in daily['2026-04-07']), 16)

    def test_overlay_omitted_duplicate_reordered_truncated_wrong_context_removed(self):
        source, original = self.overlay_fixture()
        for field, value in [('occasion', 'Tuesday Eve'), ('service_hour', 'Third Hour'), ('source_family', 'ordinary_date_resolved'), ('display_ref', 'Ps 120:2'), ('active', False)]:
            with self.subTest(field=field):
                daily = copy.deepcopy(original)
                daily['2026-04-07'][0][field] = value
                self.rejected(source, daily)
        for operation in ('omit', 'duplicate', 'reorder'):
            with self.subTest(operation=operation):
                daily = copy.deepcopy(original)
                rows = daily['2026-04-07']
                if operation == 'omit': rows.pop(0)
                elif operation == 'duplicate': rows.append(copy.deepcopy(rows[0]))
                else: rows[0], rows[1] = rows[1], rows[0]
                self.rejected(source, daily)
        for field, value in [('source', 'wrong source'), ('source_occasion', 'Monday'), ('day_title', 'Monday'), ('service_section', 'Wrong Hour'), ('source_ref_status', 'ok')]:
            with self.subTest(source_field=field):
                rows = copy.deepcopy(source)
                rows[0][field] = value
                self.rejected(rows, original)

    def test_matching_wrong_overlay_date_cannot_hide_behind_structural_exclusion(self):
        source, daily = self.overlay_fixture()
        for row in source: row['gregorian_date'] = '2026-04-08'
        daily['2026-04-08'] = daily.pop('2026-04-07')
        self.rejected(source, daily)

    def test_matching_wrong_overlay_hour_is_not_accepted(self):
        source, daily = self.overlay_fixture()
        for row in source:
            if row['service_section'] == 'First Hour': row['service_section'] = 'Wrong Hour'
        for row in daily['2026-04-07']:
            if row['service_section'] == 'First Hour':
                row['service_section'] = row['service_hour'] = 'Wrong Hour'
        self.rejected(source, daily)

    def test_renumbered_physical_prophecy_reordering_still_fails(self):
        for date in ('2026-03-04', '2026-04-07'):
            with self.subTest(date=date):
                source, daily = self.overlay_fixture() if date == '2026-04-07' else self.fixtures(date)
                rows = daily[date]
                positions = [i for i, r in enumerate(rows) if r['slot'].startswith('OT') and (date != '2026-04-07' or r['occasion'] == 'Tuesday')]
                rows[positions[0]], rows[positions[1]] = rows[positions[1]], rows[positions[0]]
                for i, row in enumerate(rows, 1): row['reading_order'] = i
                self.rejected(source, daily)

    def test_restored_wednesday_and_hosanna_rows_have_qualified_structural_dispositions(self):
        for date in ('2026-04-08', '2026-04-05'):
            with self.subTest(date=date):
                source, daily = self.fixtures(date)
                self.assertEqual(self.compare(source, daily)['status'], 'pass')

    def test_source_qualified_joel_appointments_preserve_exact_context(self):
        for date in ('2026-02-18', '2026-03-18'):
            source, original = self.fixtures(date)
            with self.subTest(date=date):
                result = self.compare(source, original)
                self.assertEqual(result['status'], 'pass', result['comparison_rows'])
                # Complete authenticated Reader tables take precedence in these
                # dated services. The separate legacy-only fallback is exercised
                # in test_lent_reader_precedence.py, not added beside this table.
                expected_joel = {'2026-02-18': 'Joel 2:12-26',
                                 '2026-03-18': 'Joel 3:9-21'}[date]
                selected = next(i for i, r in enumerate(original[date])
                                if r['source_family'] == 'coptic_reader_verified_supplement'
                                and r['canonical_mt_ref'] == expected_joel)
                for field, value in [('occasion', 'Other Wednesday'), ('source_family', 'ordinary_date_resolved'),
                                     ('source_kind', 'pascha_day_hour'), ('source_locator', 'forged.txt'),
                                     ('display_ref', 'Joel 1:1-2'), ('spans_json', '[]'),
                                     ('current_status', 'historical_witness'), ('slot', 'OT1')]:
                    with self.subTest(field=field):
                        daily = copy.deepcopy(original)
                        daily[date][selected][field] = value
                        self.rejected(source, daily)
                self.rejected(source, {date: [r for i, r in enumerate(original[date]) if i != selected]})

    def test_qualified_hosanna_day_ninth_hour_has_exact_source_disposition(self):
        source, original = self.fixtures('2026-04-05')
        result = self.compare(source, original)
        self.assertEqual(result['status'], 'pass', result['comparison_rows'])
        dispositions = [r for r in result['audit_dispositions']
                        if r['occasion'] == 'Hosanna Sunday' and r['service_section'] == 'Ninth Hour']
        self.assertEqual(sum(r['count'] for r in dispositions), 3)  # Psalm, prophecy, Gospel.
        selected = next(i for i, r in enumerate(original['2026-04-05'])
                        if r['source_kind'] == 'coptic_reader_qualified_pascha_hour')
        for field, value in [('occasion', 'Monday Eve'), ('service_hour', 'Eleventh Hour'),
                             ('service_section', 'Eleventh Hour'), ('source_family', 'holy_pascha_curated_day_hour'),
                             ('source_kind', 'pascha_day_hour'), ('source_locator', 'forged.txt'),
                             ('source_disclosure', '[]'), ('spans_json', '[]'),
                             ('display_ref', 'Lam 1:1-3'), ('canonical_mt_ref', 'Lam 1:1-3'),
                             ('slot', 'OT2'), ('slot_order', 2), ('identity_key', 'forged'),
                             ('current_status', 'historical_witness')]:
            with self.subTest(field=field):
                daily = copy.deepcopy(original)
                daily['2026-04-05'][selected][field] = value
                self.rejected(source, daily)
        for date in ('2026-04-04', '2026-04-06'):
            self.rejected([], {date: [copy.deepcopy(original['2026-04-05'][selected])]})

    def test_restored_structural_rows_do_not_bypass_context_or_reading_validation(self):
        for date, family in [('2026-04-08', 'coptic_reader'), ('2026-04-05', 'holy_pascha_curated_day_hour')]:
            source, original = self.fixtures(date)
            selected = next(i for i, row in enumerate(original[date])
                            if row.get('structural_day') and row.get('source_family') == family)
            for field, value in [('source_kind', 'ordinary_date'), ('source_locator', 'forged.txt'),
                                 ('source_disclosure', '[]'), ('display_ref', 'Jn 1:1-2'),
                                 ('spans_json', '[]'), ('slot', 'wrong-slot'),
                                 ('identity_key', 'forged'), ('active', False)]:
                with self.subTest(date=date, field=field):
                    daily = copy.deepcopy(original)
                    daily[date][selected][field] = value
                    self.rejected(source, daily)
            daily = {'2026-04-09': copy.deepcopy(original[date])}
            self.rejected([], daily)

    def test_structural_exclusions_require_independent_date_occasion_hour_context(self):
        source, original = self.fixtures('2026-04-06')
        self.assertEqual(source, [])
        self.assertEqual(self.compare(source, original)['status'], 'pass')
        for field, value in [('occasion', 'Tuesday'), ('service_hour', 'Wrong Hour'), ('source_family', 'ordinary_date_resolved'), ('active', False), ('structural_day', 'Tuesday')]:
            with self.subTest(field=field):
                daily = copy.deepcopy(original)
                daily['2026-04-06'][0][field] = value
                self.rejected(source, daily)
        daily = copy.deepcopy(original)
        extra = copy.deepcopy(daily['2026-04-06'][0])
        extra['reading_order'] = len(daily['2026-04-06']) + 1
        daily['2026-04-06'].append(extra)
        self.rejected(source, daily)

    def test_authenticated_suppression_has_explicit_audit_dispositions(self):
        source, daily = self.suppression_fixture()
        self.assertTrue(any(r['service_section'] == 'Vespers' for r in source))
        result = self.compare(source, daily)
        self.assertEqual(result['status'], 'pass', result)
        suppressed = [r for r in result['audit_dispositions'] if r['disposition'] == 'authenticated_no_service_suppression']
        self.assertEqual(sum(r['count'] for r in suppressed), 2)
        self.assertTrue(all(r['evidence_sha256'] for r in suppressed))

    def test_suppression_wrong_source_title_service_date_and_removed_extra_fail(self):
        source, original = self.suppression_fixture()
        for field, value in [('source', 'wrong source'), ('day_title', 'Great Lent'), ('service_section', 'Matins'), ('source_occasion', 'Wrong occasion')]:
            with self.subTest(field=field):
                rows = copy.deepcopy(source)
                next(r for r in rows if r['service_section'] == 'Vespers')[field] = value
                self.rejected(rows, original)
        rows = copy.deepcopy(source)
        for row in rows: row['gregorian_date'] = '2026-02-03'
        daily = {'2026-02-03': copy.deepcopy(original['2026-02-02'])}
        self.rejected(rows, daily)
        for removed in (False, True):
            daily = copy.deepcopy(original)
            row = dict(daily['2026-02-02'][0], service_section='Vespers', slot='Gospel', display_ref='Jn 1:1-17')
            if removed: row.update(active=False, status='removed')
            daily['2026-02-02'].append(row)
            self.rejected(source, daily)

    def test_vespers_evidence_cannot_authorize_matins_policy_suppression(self):
        source, daily = self.suppression_fixture()
        baseline = self.compare(source, daily)
        self.assertEqual(baseline['status'], 'pass')
        policy = json.loads(CORRECTIONS.read_text())
        vespers_rule = next(r for r in policy['suppressed_date_contexts']
                            if r['day_title'] == 'Fast of Nineveh')
        policy['suppressed_date_contexts'].append(dict(vespers_rule, service_section='Matins'))
        policy_path = self.root / 'wrong-service-policy.json'
        policy_path.write_text(json.dumps(policy))
        daily['2026-02-02'] = [r for r in daily['2026-02-02'] if r['service_section'] != 'Matins']
        result = self.compare(source, daily, corrections_path=policy_path)
        self.assertEqual(result['status'], 'fail')
        self.assertTrue(any(r['service_section'] == 'Matins' for r in result['comparison_rows']))
        self.assertFalse(any(r['service_section'] == 'Matins' for r in result['audit_dispositions']))
        self.assertEqual(sum(r['count'] for r in result['audit_dispositions']
                             if r['disposition'] == 'authenticated_no_service_suppression'), 2)

    def test_evidence_wrong_hash_and_wrong_suppression_reason_fail_closed(self):
        for date, alteration in [('2026-02-02', 'manifest'), ('2026-03-04', 'supplement'), ('2026-02-02', 'reason')]:
            with self.subTest(alteration=alteration):
                policy = json.loads(CORRECTIONS.read_text())
                if alteration == 'manifest':
                    key = 'sources/coptic-reader/remaining-2026-09-07/SHA256SUMS'
                    policy['source_fingerprints'][key] = '0' * 64
                elif alteration == 'supplement':
                    key = policy['recurring_date_supplements'][0]['evidence']
                    policy['source_fingerprints'][key] = '0' * 64
                else: policy['suppressed_date_contexts'][0]['reason'] = 'unreviewed_suppression'
                path = self.root / 'corrections.json'
                path.write_text(json.dumps(policy))
                source, daily = self.suppression_fixture() if date == '2026-02-02' else self.fixtures(date)
                self.rejected(source, daily, corrections_path=path)

    def test_wrong_calendar_correction_metadata_fails_closed(self):
        source, daily = self.overlay_fixture()
        policy = json.loads(CORRECTIONS.read_text())
        policy['calendar_overlays'][0]['replacement_source'] = 'wrong-source.csv'
        path = self.root / 'calendar-corrections.json'
        path.write_text(json.dumps(policy))
        self.rejected(source, daily, corrections_path=path)

    def test_ordinary_wrong_context_removed_and_structural_masquerade_fail(self):
        # Jan 1 is the reviewed complete Kiahk 23 replacement. Jan 2 remains
        # an ordinary cache appointment; full Kiahk controls live separately.
        source, original = self.fixtures('2026-01-02')
        self.assertEqual(self.compare(source, original)['status'], 'pass')
        for field, value in [('occasion', 'Wrong title'), ('service_hour', 'Third Hour'), ('source_family', 'bright_saturday'), ('status', 'removed'), ('current_status', 'historical_witness'), ('current_status', 'historical_candidate_removed'), ('current_status', 'superseded_by_fixture'), ('removed_marker', 'removed in current practice'), ('structural_day', 'Good Friday')]:
            with self.subTest(field=field):
                daily = copy.deepcopy(original)
                daily['2026-01-02'][0][field] = value
                self.rejected(source, daily)


if __name__ == '__main__':
    unittest.main()
