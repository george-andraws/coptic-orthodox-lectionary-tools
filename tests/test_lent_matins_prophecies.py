"""Locked official Coptic Reader context; not an all-Lent enrichment."""
import datetime as dt
import copy
import contextlib
import io
import sys
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_reference as reference
import build_design_deliverables as design
from calendar_resolution import julian_pascha_gregorian, resolve_current_date_rows

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'Wednesday of the third week of Great Lent'
PRINTED = ['Exodus 4:19-6:13', 'Joel 2:21-27', 'Isaiah 9:9-10:4', 'Job 12:1-14:22']
NORMALIZED = ['Exod 4:19-6:13', 'Joel 2:21-27', 'Isa 9:9-10:4', 'Job 12:1-14:22']
RAW = '2.4:19-31*@+2.5:1-23*@+2.6:1-13@29.2:21-26@23.9:9-21*@+23.10:1-4@18.12:1-25*@+18.13:1-28*@+18.14:1-22'


# Independently captured own tables, not expectations derived from the policy
# or parser. Diagnosis 09 authenticated all four before retiring the old blanket
# absence assertion. Source hashes and printed coordinates remain literal.
SUPPLEMENT_SOURCE = 'Coptic Reader verified recurring supplement'
WEDNESDAY_EVIDENCE = 'sources/coptic-reader/lent-week3-wednesday-2026-10-07/coptic-reader-2026-03-04-matins-prophecies.txt'
NEIGHBORS = {
    '2026-03-03': {
        'title': 'Tuesday of the third week of Great Lent', 'offset': -40,
        'captured_at': '2026-10-07T17:17:34.270Z',
        'printed': ['Proverbs 2:1-15', 'Isaiah 10:12-20'],
        'normalized': ['Prov 2:1-15', 'Isa 10:12-20'],
        'text_sha256': '020687341f1e233c466c0272872d5b87f60f28d0191b6a61a3807feb3be892c3',
        'context_sha256': 'af2d20b974275314107770ed5ac3958ba2b3383e3c95a2ab93ff96d4ee63f25f',
        'oracle_sha256': 'd196a0c74204a1ff9b2a91b8c3790992a52a313b584c8933bbb002e8375be7d8',
    },
    '2026-03-05': {
        'title': 'Thursday of the third week of Great Lent', 'offset': -38,
        'captured_at': '2026-10-07T17:17:49.562Z',
        'printed': ['Genesis 18:17-19:29', 'Proverbs 2:16-3:4', 'Isaiah 11:10-12:2'],
        'normalized': ['Gen 18:17-19:29', 'Prov 2:16-3:4', 'Isa 11:10-12:2'],
        'text_sha256': 'b59249bddf65bb45749dd7dae9d12fcc716b91601809b85c67cda25e781f043a',
        'context_sha256': '354def8274f6ed899e63b280107e2a344809e7b77c26833ebe05b4c399454c2d',
        'oracle_sha256': 'f75ed9414a73e29ee325449f3af232692ee93a8a2d5ac34f206447a93afa92b2',
    },
    '2026-02-25': {
        'title': 'Wednesday of the second week of Great Lent', 'offset': -46,
        'captured_at': '2026-10-07T17:15:58.396Z',
        'printed': ['Exodus 2:11-20', 'Isaiah 5:17-25'],
        'normalized': ['Exod 2:11-20', 'Isa 5:17-25'],
        'text_sha256': '96187816698536e91647d160f1a1f929dc3946469c5fc50c24a21ab35b555561',
        'context_sha256': '3bf0aae8ecee4ece42fc007c9db80891c6f38d505c9170e0e5ae186727e23547',
        'oracle_sha256': 'd35e2cf5ecf9c896688f62fede1c02873eb1cfb59b27f867d3aaded067a95e78',
    },
    '2026-03-11': {
        'title': 'Wednesday of the fourth week of Great Lent', 'offset': -32,
        'captured_at': '2026-10-07T17:25:31.767Z',
        'printed': ['Exodus 7:14-8:19', 'Joel 2:28-32', 'Job 1:1-22', 'Isaiah 26:21-27:9'],
        'normalized': ['Exod 7:14-8:19', 'Joel 2:28-32', 'Job 1:1-22', 'Isa 26:21-27:9'],
        'text_sha256': '28bd2e9ed09af67ae770a6fb92c87a2314fb8a28ba6e37a1b7ffb7793e4660b5',
        'context_sha256': '3000f7eae106cad78d3a60a47746f8be987197163f093b18b6ad448a96dd5b22',
        'oracle_sha256': '5b2a43a30fe3fdcfa9aa666eda8bf535f0820bf6b48505d913df3ec3df2f5157',
    },
}


def parse(date):
    html = (ROOT / 'cache/copticchurch_html' / f'{date.isoformat()}.html').read_text()
    return reference.parse_copticchurch_html(html, date)


class LentMatinsProphecies(unittest.TestCase):
    def test_locked_primary_text_and_printed_order(self):
        text = ROOT / 'sources/coptic-reader/lent-week3-wednesday-2026-10-07/coptic-reader-2026-03-04-matins-prophecies.txt'
        self.assertEqual(hashlib.sha256(text.read_bytes()).hexdigest(), 'd3f082fb383f8bd3518a7f53bc94b6c5252e1a026e8ce6bf0cc6ed55a8ab0f43')
        self.assertEqual([line.strip() for line in text.read_text().splitlines() if line.startswith('\t')], PRINTED)

    def test_recurs_in_supported_years_at_only_verified_movable_context(self):
        for year in range(2020, 2036):
            date = julian_pascha_gregorian(year) - dt.timedelta(days=39)
            with self.subTest(year=year):
                meta, rows = parse(date)
                self.assertEqual(meta['day_title'], TITLE)
                prophecies = [r for r in rows if r['reading_type'] == 'Prophecy']
                self.assertEqual([r['raw_ref'] for r in prophecies], PRINTED)
                self.assertEqual([r['normalized_ref'] for r in prophecies], NORMALIZED)
                self.assertEqual([int(r['source_order']) for r in prophecies], [1, 2, 3, 4])
                self.assertTrue(all(r['service_section'] == 'Matins' for r in prophecies))
                self.assertTrue(all(r['source'] == 'Coptic Reader verified recurring supplement' for r in prophecies))
                self.assertEqual(meta['reading_count'], len(rows))
                _, repeated = parse(date)
                self.assertEqual(repeated, rows)
                self.assertEqual([r['matched_ref'] for r in reference.build_date_passage_index(prophecies)], NORMALIZED)

    def test_source_boundary_and_current_date_helper_order(self):
        _, rows = parse(dt.date(2026, 3, 4))
        for stage in [rows, resolve_current_date_rows(rows, [])]:
            matins = [row for row in stage if row['service_section'] == 'Matins']
            self.assertEqual([row['raw_ref'] for row in matins[:4]], PRINTED)
            self.assertEqual(len(matins), 6)

    def test_primary_fingerprint_and_printed_reference_drift_fail_closed(self):
        html = (ROOT / 'cache/copticchurch_html/2026-03-04.html').read_text()
        for case in ['fingerprint', 'printed_reference']:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                overlay = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())
                supplement = overlay['recurring_date_supplements'][0]
                if case == 'fingerprint':
                    overlay['source_fingerprints'][supplement['evidence']] = '0' * 64
                else:
                    supplement['readings'][1]['printed_ref'] = 'Joel 2:21-26'
                Path(directory, 'lectionary_corrections.json').write_text(json.dumps(overlay))
                with patch.object(reference, 'SRC', Path(directory)):
                    with self.assertRaisesRegex(RuntimeError, 'source drift|printed references/order'):
                        reference.parse_copticchurch_html(html, dt.date(2026, 3, 4))

    def assert_neighbor_source_context(self, day, rows, *, resolved=False):
        expected = NEIGHBORS[day]
        evidence = f'sources/coptic-reader/lent-qualified-2026-10-07/{day}/Prophecies.txt'
        warning = (f'verified recurring context; evidence={evidence}; verified_date={day}; '
                   f"captured_at={expected['captured_at']}")
        # Compare every prophecy, not just rows still bearing a convenient label.
        props = [r for r in rows if r['reading_type'] == 'Prophecy']
        fields = ('gregorian_date', 'weekday', 'day_title', 'service_section',
                  'reading_type', 'raw_ref', 'normalized_ref', 'source_order',
                  'source_slot', 'source', 'parse_status', 'correction_source',
                  'normalization_warning', 'url')
        self.assertEqual([tuple(r.get(k) for k in fields) for r in props], [
            (day, dt.date.fromisoformat(day).strftime('%A'), expected['title'],
             'Matins', 'Prophecy', printed, normalized, order, f'OT{order}',
             SUPPLEMENT_SOURCE, 'source_supplement', evidence, warning,
             'https://copticreader.org/app/')
            for order, (printed, normalized) in enumerate(
                zip(expected['printed'], expected['normalized']), 1)
        ])
        self.assertEqual([r for r in rows if r['source'] == SUPPLEMENT_SOURCE], props)
        matins = [r for r in rows if r['service_section'] == 'Matins']
        self.assertEqual(matins[:len(props)], props)
        # The date resolver's established tie-breaker sorts the two unnumbered
        # HTML anchors by type; it must not disturb numbered prophecy order.
        self.assertEqual([r['reading_type'] for r in matins[len(props):]],
                         ['Gospel', 'Psalm'] if resolved else ['Psalm', 'Gospel'])
        for row in rows:
            self.assertNotIn(row['raw_ref'], PRINTED)
            self.assertNotIn(row.get('normalized_ref'), NORMALIZED)
            self.assertNotEqual(row.get('correction_source'), WEDNESDAY_EVIDENCE)
            self.assertNotIn(WEDNESDAY_EVIDENCE, row.get('normalization_warning', ''))

    def test_qualified_neighbors_have_only_their_exact_own_source_tables(self):
        # The old universal absence premise is false; these are four different
        # authenticated tables. This does not activate any new/expanded fixture.
        for day, expected in NEIGHBORS.items():
            with self.subTest(day=day):
                date = dt.date.fromisoformat(day)
                self.assertEqual((date - julian_pascha_gregorian(2026)).days, expected['offset'])
                folder = ROOT / f'sources/coptic-reader/lent-qualified-2026-10-07/{day}'
                for filename, key in [('Prophecies.txt', 'text_sha256'),
                                      ('context.txt', 'context_sha256'),
                                      ('qualified-oracle.json', 'oracle_sha256')]:
                    self.assertEqual(hashlib.sha256((folder / filename).read_bytes()).hexdigest(), expected[key])
                self.assertEqual([line.strip() for line in (folder / 'Prophecies.txt').read_text().splitlines()
                                  if line.startswith('\t')], expected['printed'])
                oracle = json.loads((folder / 'qualified-oracle.json').read_text())
                self.assertIs(oracle['source_qualified'], True)
                self.assertEqual((oracle['civil_date'], oracle['service']), (day, 'Matins'))
                self.assertEqual(oracle['context'], (folder / 'context.txt').read_text())
                self.assertEqual(oracle['raw_reference_lines'], ['\t' + p for p in expected['printed']])
                meta, rows = parse(date)
                self.assertEqual((meta['date'], meta['day_title'], meta['reading_count']),
                                 (day, expected['title'], len(rows)))
                self.assert_neighbor_source_context(day, rows)
                self.assert_neighbor_source_context(day, resolve_current_date_rows(rows, []), resolved=True)
                props = [r for r in rows if r['reading_type'] == 'Prophecy']
                index = reference.build_date_passage_index(props)
                self.assertEqual([(r['matched_ref'], r['raw_ref'], r['source_order'],
                                   r['source_slot'], r['correction_source'], r['normalization_warning']) for r in index],
                                 [(r['normalized_ref'], r['raw_ref'], r['source_order'],
                                   r['source_slot'], r['correction_source'], r['normalization_warning']) for r in props])
                # Exercise the actual CSV date-query consumer on freshly parsed
                # rows, not the known stale generated integration snapshot.
                import query_lectionary as query
                with tempfile.TemporaryDirectory() as directory:
                    reference.write_csv(Path(directory) / 'copticchurch_date_readings_current_2020_2035.csv',
                                        resolve_current_date_rows(rows, []))
                    stream = io.StringIO()
                    with patch.object(sys, 'argv', ['query_lectionary', '--data-dir', directory,
                                                   '--date', day]), patch.object(query, 'DATA', query.DATA), contextlib.redirect_stdout(stream):
                        query.main()
                    self.assertEqual([line for line in stream.getvalue().splitlines() if ' | Prophecy | ' in line],
                                     [f"{day} | {expected['title']} | Matins | Prophecy | {p}" for p in expected['printed']])

    def test_exact_title_and_pascha_offset_required_for_each_table(self):
        contexts = {**{day: e['title'] for day, e in NEIGHBORS.items()}, '2026-03-04': TITLE}
        for day, title in contexts.items():
            html = (ROOT / 'cache/copticchurch_html' / f'{day}.html').read_text()
            date = dt.date.fromisoformat(day)
            for delta in [-7, -1, 1, 7]:
                with self.subTest(day=day, offset_delta=delta):
                    _, rows = reference.parse_copticchurch_html(html, date + dt.timedelta(days=delta))
                    self.assertFalse(any(r['source'] == SUPPLEMENT_SOURCE for r in rows))
            with self.subTest(day=day, wrong_title=True):
                _, rows = reference.parse_copticchurch_html(html.replace(title, 'Other occasion'), date)
                self.assertFalse(any(r['source'] == SUPPLEMENT_SOURCE for r in rows))

    def test_authentic_unqualified_matins_contexts_stay_held_and_unindexed(self):
        import matins_source_projection as matins
        fixture = matins.load_dated_matins_fixture()
        for day in ['2026-03-06', '2026-03-10']:
            with self.subTest(day=day):
                record = next(r['source_record'] for r in fixture['corpus']['records']
                              if r['source_record']['civil_date'] == day)
                context = {key: record[key] for key in matins.CONTEXT_KEYS}
                date = dt.date.fromisoformat(day)
                _, ordinary = parse(date)
                self.assertFalse(any(r['source'] == SUPPLEMENT_SOURCE for r in ordinary))
                html = (ROOT / 'cache/copticchurch_html' / f'{day}.html').read_text()
                _, projected = reference.parse_copticchurch_html(html, date, candidate_matins_context=context)
                candidates = [r for r in projected if matins.is_dated_matins_candidate(r)]
                self.assertTrue(candidates)
                for row in candidates:
                    for flag in ['runtime_activation_approved', 'recurrence_approved',
                                 'canonical_equivalence_approved', 'include_in_current_index']:
                        self.assertIs(row[flag], False)
                    # Active identifies the current candidate, NOT activation.
                    self.assertIs(row['active'], True)
                    self.assertIs(row['candidate_only'], True)
                self.assertEqual(reference.build_date_passage_index(candidates), [])
                optin = reference.build_date_passage_index(candidates, include_candidate_matins=True)
                self.assertEqual(len(optin), len(candidates))
                self.assertTrue(all(r['matched_ref'] == '' and r['canonical_ref'] == '' for r in optin))

    def test_neighbor_oracle_rejects_corrupted_real_parse_results(self):
        _, wednesday = parse(dt.date(2026, 3, 4))
        wednesday_props = [r for r in wednesday if r['reading_type'] == 'Prophecy']
        for day in NEIGHBORS:
            _, original = parse(dt.date.fromisoformat(day))
            self.assert_neighbor_source_context(day, original)
            for mutation in ['moved_wednesday', 'wrong_date', 'wrong_title', 'wrong_order',
                             'truncated_boundary', 'wrong_evidence', 'wrong_service', 'missing']:
                with self.subTest(day=day, mutation=mutation):
                    damaged = copy.deepcopy(original)
                    props = [r for r in damaged if r['reading_type'] == 'Prophecy']
                    if mutation == 'moved_wednesday':
                        moved = copy.deepcopy(wednesday_props)
                        for row in moved:
                            row.update(gregorian_date=day, weekday=dt.date.fromisoformat(day).strftime('%A'),
                                       day_title=NEIGHBORS[day]['title'])
                        damaged = moved + [r for r in damaged if r['reading_type'] != 'Prophecy']
                    elif mutation == 'wrong_date': props[0]['gregorian_date'] = '2026-03-04'
                    elif mutation == 'wrong_title': props[0]['day_title'] = TITLE
                    elif mutation == 'wrong_order':
                        a, b = damaged.index(props[0]), damaged.index(props[1])
                        damaged[a], damaged[b] = damaged[b], damaged[a]
                    elif mutation == 'truncated_boundary':
                        props[0]['raw_ref'] = props[0]['raw_ref'][:-1]
                        props[0]['normalized_ref'] = props[0]['normalized_ref'][:-1]
                    elif mutation == 'wrong_evidence': props[0]['correction_source'] = WEDNESDAY_EVIDENCE
                    elif mutation == 'wrong_service': props[0]['service_section'] = 'Liturgy'
                    else: damaged.remove(props[0])
                    with self.assertRaises(AssertionError):
                        self.assert_neighbor_source_context(day, damaged)

    def test_context_qualified_cycle_correction_retains_raw_api(self):
        rows = reference.export_cycle_tables(reference.load_books())
        row = next(r for r in rows if r['source_table'] == 'GreatLentReadings' and r['day_key'] == 'week 3 day_of_week 3' and r['reading_slot'] == 'prophecy')
        self.assertEqual(row['raw_ref'], RAW)
        self.assertIn('Joel 2:21-27', row['normalized_ref'])
        self.assertIn('evidence=', row['normalization_warning'])
        segments = reference.build_passage_index([row], reference.load_books())
        self.assertTrue(any(r['book_abbrev'] == 'Joel' and r['verse_end'] == 27 for r in segments))
        self.assertTrue(any(r['book_abbrev'] == 'Exod' and r['chapter'] == 5 for r in segments))
        self.assertNotIn(('GreatLentReadings', 'week 3 day_of_week 4', 'prophecy', RAW), reference.KATAMEROS_CYCLE_CORRECTIONS)

    def test_daily_preserves_source_prophecy_order_before_psalm_gospel(self):
        props = [dict(gregorian_date='2026-03-04', occasion=TITLE, service_section='Matins', slot=f'OT{i}', source_order=i, reading_type='scripture', source_family='coptic_reader_verified_supplement', source_kind='copticchurch_date', display_ref=ref, spans_json='[]') for i, ref in enumerate(NORMALIZED, 1)]
        psalm = dict(gregorian_date='2026-03-04', occasion=TITLE, service_section='Matins', slot='Psalm', display_ref='Ps 26:4')
        gospel = dict(gregorian_date='2026-03-04', occasion=TITLE, service_section='Matins', slot='Gospel', display_ref='Lk 13:18-22')
        daily = design.build_daily_year_files([psalm] + list(reversed(props)) + [gospel])[2026]['2026-03-04']
        self.assertEqual([r['display_ref'] for r in daily[:4]], NORMALIZED)
        self.assertEqual([r['slot_type'] for r in daily[:4]], ['prophecy'] * 4)
        self.assertEqual([r['slot_order'] for r in daily[:4]], [1, 2, 3, 4])
        self.assertEqual([r['slot'] for r in daily[4:]], ['Psalm', 'Gospel'])

    def test_design_validator_accepts_source_verified_daily_artifacts(self):
        import verify_design_deliverables as validator
        validator.verify_rows()

    def test_design_validator_rejects_missing_reordered_and_truncated_prophecies(self):
        import verify_design_deliverables as validator
        path = ROOT / 'out/design/daily/lectionary-2026.json'
        original_text = Path.read_text
        content = json.loads(path.read_text())
        for mutation in ['missing', 'reordered', 'truncated']:
            with self.subTest(mutation=mutation):
                damaged = json.loads(json.dumps(content))
                day = damaged['2026-03-04']
                if mutation == 'missing':
                    del day[0]
                elif mutation == 'reordered':
                    day[0], day[1] = day[1], day[0]
                else:
                    day[1]['display_ref'] = 'Joel 2:21-26'
                def read_text(target, *args, **kwargs):
                    if target == path:
                        return json.dumps(damaged)
                    return original_text(target, *args, **kwargs)
                with patch.object(Path, 'read_text', read_text):
                    with self.assertRaisesRegex(AssertionError, 'lectionary-2026.json does not exactly match'):
                        validator.verify_rows()


if __name__ == '__main__':
    unittest.main()
