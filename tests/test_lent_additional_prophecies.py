"""Bounded recovery of the first/fifth Lent Wednesday Matins tables.

Expected tables come from retained primary documents, not policy-derived oracles.
No network, package build, generated-output refresh, or global oracle rewrite.
"""
import copy
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_reference as ref
from calendar_resolution import julian_pascha_gregorian, resolve_current_date_rows

ROOT = Path(__file__).resolve().parents[1]
BASE = 'sources/coptic-reader/lent-additional-qualified-2026-10-25'
SOURCE = 'Coptic Reader verified recurring supplement'
CASES = {
    '2026-02-18': (-53, 'Wednesday of the first week of Great Lent',
                   ['Isaiah 2:3-11', 'Joel 2:12-26'], ['Isa 2:3-11', 'Joel 2:12-26']),
    '2026-03-18': (-25, 'Wednesday of the fifth week of Great Lent',
                   ['Exodus 8:20-9:35', 'Isaiah 41:4-14', 'Joel 3:9-21', 'Job 28:12-28', 'Proverbs 4:10-19'],
                   ['Exod 8:20-9:35', 'Isa 41:4-14', 'Joel 3:9-21', 'Job 28:12-28', 'Prov 4:10-19']),
}


def policy():
    return json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())


def parse(date, html=None):
    if html is None:
        html = (ROOT / 'cache/copticchurch_html' / f'{date}.html').read_text()
    return ref.parse_copticchurch_html(html, date)[1]


class AdditionalLentProphecies(unittest.TestCase):
    def rules(self):
        rules = [r for r in policy()['recurring_date_supplements'] if r['evidence'].startswith(BASE + '/')]
        self.assertEqual([r['verified_date'] for r in rules], list(CASES))
        return rules

    def test_complete_ordered_tables_recur_from_real_cached_html_2020_2035(self):
        for day, (offset, title, printed, normalized) in CASES.items():
            for year in range(2020, 2036):
                date = julian_pascha_gregorian(year) + dt.timedelta(days=offset)
                with self.subTest(day=day, year=year):
                    rows = parse(date)
                    props = [r for r in rows if r['reading_type'] == 'Prophecy']
                    collisions = {
                        '2034-02-15': 'Entrance into the Temple',
                        '2021-04-07': 'Annunciation', '2027-04-07': 'Annunciation',
                        '2032-04-07': 'Annunciation',
                        '2031-03-19': 'Wednesday of the fifth week of Great Lent <br>(Feast of the Cross - Readings of 10th Baramhat)',
                    }
                    if str(date) in collisions:
                        self.assertFalse(props)
                        self.assertFalse(any(r['source'] == SOURCE for r in rows))
                        self.assertTrue(all(r['day_title'] == collisions[str(date)] for r in rows))
                        continue
                    self.assertEqual([r['raw_ref'] for r in props], printed)
                    self.assertEqual([r['normalized_ref'] for r in props], normalized)
                    self.assertEqual([r['source_slot'] for r in props], [f'OT{i}' for i in range(1, len(printed) + 1)])
                    self.assertEqual([r['source_order'] for r in props], list(range(1, len(printed) + 1)))
                    self.assertTrue(all(r['source'] == SOURCE and r['service_section'] == 'Matins'
                                        and r['day_title'] == title and r['gregorian_date'] == str(date)
                                        and r['parse_status'] == 'source_supplement' for r in props))
                    self.assertEqual([r for r in rows if r['source'] == SOURCE], props)
                    for materialized in (rows, resolve_current_date_rows(rows, [])):
                        matins = [r for r in materialized if r['service_section'] == 'Matins']
                        self.assertEqual(matins[:len(props)], props)
                        self.assertEqual(len(matins), len(props) + 2)
                    self.assertEqual([r['matched_ref'] for r in ref.build_date_passage_index(props)], normalized)
                    self.assertEqual(parse(date), rows)

    def test_primary_hash_context_picker_and_literal_reference_contract(self):
        current = policy()
        for rule in self.rules():
            with self.subTest(day=rule['verified_date']):
                ref.authenticate_recurring_supplement(rule, current)
                folder = ROOT / BASE / rule['verified_date']
                oracle = json.loads((folder / 'qualified-oracle.json').read_text())
                self.assertIs(oracle['source_qualified'], True)
                self.assertEqual(oracle['service'], 'Matins')
                self.assertEqual(oracle['slot'], 'Prophecies')
                self.assertEqual(oracle['context'], (folder / 'context.txt').read_text())
                self.assertEqual(rule['source_verified_context'], oracle['context'])
                self.assertEqual(oracle['raw_reference_lines'], ['\t' + p for p in CASES[rule['verified_date']][2]])
                self.assertEqual(len([r for r in json.loads((folder / 'picker.json').read_text())
                                      if r.get('current') == 'true']), 1)
                for path, digest in rule['evidence_fingerprints'].items():
                    self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest)
                    self.assertEqual(current['source_fingerprints'][path], digest)

    def test_authentication_rejects_source_ordinal_hash_and_table_drift(self):
        for original in self.rules():
            for mutation in ('missing', 'duplicate', 'reorder', 'endpoint', 'ordinal', 'slot', 'date', 'offset', 'hash'):
                rule = copy.deepcopy(original)
                current = policy()
                if mutation == 'missing': rule['readings'].pop()
                elif mutation == 'duplicate': rule['readings'].append(copy.deepcopy(rule['readings'][0]))
                elif mutation == 'reorder': rule['readings'].reverse()
                elif mutation == 'endpoint': rule['readings'][0]['normalized_ref'] += '0'
                elif mutation == 'ordinal': rule['readings'][0]['source_order'] = 99
                elif mutation == 'slot': rule['readings'][0]['source_slot'] = 'Psalm'
                elif mutation == 'date': rule['verified_date'] = '2026-02-19'
                elif mutation == 'offset': rule['pascha_offset_days'] += 1
                else: current['source_fingerprints'][rule['evidence']] = '0' * 64
                with self.subTest(day=original['verified_date'], mutation=mutation), self.assertRaises(RuntimeError):
                    ref.authenticate_recurring_supplement(rule, current)

    def test_qualified_oracle_state_and_context_drift_fail_closed(self):
        for original in self.rules():
            for mutation in ('state', 'service', 'date', 'context'):
                current = policy()
                rule = copy.deepcopy(original)
                with self.subTest(day=rule['verified_date'], mutation=mutation), tempfile.TemporaryDirectory() as directory:
                    work = Path(directory)
                    for relative in rule['evidence_fingerprints']:
                        target = work / relative
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes((ROOT / relative).read_bytes())
                    path = work / rule['oracle_evidence']
                    oracle = json.loads(path.read_text())
                    if mutation == 'state': oracle['source_qualified'] = False
                    elif mutation == 'service': oracle['service'] = 'Liturgy'
                    elif mutation == 'date': oracle['civil_date'] = '2026-02-19'
                    else: oracle['context'] = 'Different selected context'
                    path.write_text(json.dumps(oracle))
                    digest = hashlib.sha256(path.read_bytes()).hexdigest()
                    current['source_fingerprints'][rule['oracle_evidence']] = digest
                    rule['evidence_fingerprints'][rule['oracle_evidence']] = digest
                    with patch.object(ref, 'WORK', work), self.assertRaises(RuntimeError):
                        ref.authenticate_recurring_supplement(rule, current)

    def test_neighbor_wrong_title_and_upstream_overlap_controls(self):
        for day, (offset, title, _, _) in CASES.items():
            date = dt.date.fromisoformat(day)
            html = (ROOT / 'cache/copticchurch_html' / f'{day}.html').read_text()
            for delta in (-7, -1, 1, 7):
                with self.subTest(day=day, delta=delta):
                    self.assertFalse(any(r['source'] == SOURCE for r in parse(date + dt.timedelta(days=delta), html)))
            self.assertFalse(any(r['source'] == SOURCE for r in parse(date, html.replace(title, 'Other occasion'))))
            injected = html.replace('<h2>Matins</h2>', '<h2>Matins</h2><h4>Prophecy</h4><h5>Isaiah 2:3-11</h5>')
            self.assertNotEqual(injected, html)
            with self.assertRaisesRegex(RuntimeError, 'overlaps upstream'):
                parse(date, injected)

    def test_full_numbered_bodies_and_source_line_boundaries(self):
        expected = {
            '2026-02-18': [list(range(3, 12)), list(range(12, 27))],
            '2026-03-18': [list(range(20, 33)) + list(range(1, 36)),
                           list(range(4, 15)), list(range(9, 22)),
                           list(range(12, 29)), list(range(10, 20))],
        }
        for rule in self.rules():
            day = rule['verified_date']
            folder = ROOT / BASE / day
            lines = (folder / 'Prophecies.txt').read_text().splitlines()
            oracle = json.loads((folder / 'qualified-oracle.json').read_text())
            for reading, body, numbers in zip(rule['readings'], oracle['body_constraints'], expected[day]):
                with self.subTest(day=day, ref=reading['printed_ref']):
                    self.assertEqual(lines[reading['source_line'] - 1], '\t' + reading['printed_ref'])
                    segment = lines[body['source_line_start']:body['source_line_end']]
                    english = [line for line in segment if re.match(r'^\d+ [“‘\"]?[A-Za-z]', line)]
                    self.assertEqual([int(line.split(' ', 1)[0]) for line in english], numbers)
                    self.assertEqual((english[0], english[-1]), (body['english_opening'], body['english_closing']))
                    self.assertEqual(hashlib.sha256('\n'.join(segment).encode()).hexdigest(), body['body_sha256'])
            self.assertIs(oracle['canonical_equivalence_approved'], False)

    def test_crosswalk_source_identity_registry_and_active_status(self):
        import build_lectionary_crosswalk as crosswalk
        import build_design_deliverables as design
        for rule in self.rules():
            rows = parse(dt.date.fromisoformat(rule['verified_date']))
            props = [r for r in rows if r['source'] == SOURCE]
            projected = crosswalk.project_date_rows(ref.build_date_passage_index(props))
            self.assertEqual([r['source_row_id'] for r in projected],
                             [f"{rule['source_id']}:{rule['verified_date']}:OT{i}" for i in range(1, len(props) + 1)])
            for row in projected:
                self.assertEqual(design.source_key_for(row), rule['source_key'])
                self.assertEqual(design.source_registry_for_key(rule['source_key'])['default_locator'], rule['evidence'])
                identity = design.identity_for(row['passage'], row['source_kind'])
                self.assertEqual(design.status_for(row, identity, set())[0], 'current_confirmed_coptic_reader')
                self.assertFalse(design.removed_marker_for(row, identity))

    def test_package_first_gate_is_exactly_five_missing_appointments_two_partials(self):
        gate = json.loads((ROOT / BASE / 'package-first-gap.json').read_text())
        self.assertEqual(gate['version'], '1.3.5')
        self.assertEqual(gate['tar_sha256'], '2bce78f092c318bdf5dc67a0b0bc1e300b668418ca98b0ff7e3742b1f31ae509')
        self.assertEqual(gate['missing_book_appointment_count'], 5)
        self.assertEqual({day: r['missing_book_appointments'] for day, r in gate['dates'].items()},
                         {'2026-02-18': ['Isa'], '2026-03-18': ['Exod', 'Isa', 'Job', 'Prov']})
        self.assertEqual([r['classification'] for r in gate['dates'].values()], ['Partial', 'Partial'])

    def test_joel_body_is_literal_26_not_an_invented_27(self):
        text = (ROOT / BASE / '2026-02-18/Prophecies.txt').read_text()
        joel = text.split('\tJoel 2:12-26', 1)[1]
        self.assertIn('26 You shall eat in plenty and be satisfied', joel)
        self.assertNotIn('\n27 ', joel)
        self.assertNotIn('Then you shall know that I am in the midst of Israel', joel)
        rule = self.rules()[0]
        self.assertEqual(rule['readings'][1]['normalized_ref'], 'Joel 2:12-26')
        self.assertIn('27', rule['readings'][1]['normalization_note'])


if __name__ == '__main__':
    unittest.main()
