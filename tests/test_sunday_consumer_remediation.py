"""Evidence-derived consumer regressions; no generated export prefiltering."""
import copy
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

os.environ['LECTIONARY_DISABLE_VAULT_PUBLISH'] = '1'
import build_lectionary_crosswalk as crosswalk
import build_design_deliverables as design
import build_lectionary_reference as reference
import calendar_resolution as calendar

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'sources/coptic-reader/sunday-qualified-2026-10-07'
PIN = 'b673677c0493634366a8c3fb454e61dfdb34fc340212cafe77d1b33417cd5f2c'


def serialize(rows, fields):
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return list(csv.DictReader(io.StringIO(out.getvalue())))


def sunday_rows():
    with (ROOT / 'out/data/copticchurch_date_readings_2020_2035.csv').open() as f:
        raw = [r for r in csv.DictReader(f) if r['gregorian_date'] == '2027-02-21']
    resolved = calendar.resolve_current_date_rows(raw, [])
    return [dict(r, matched_ref=r['normalized_ref']) for r in resolved]


class SundayConsumers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert hashlib.sha256((FIXTURE / 'accepted-oracle.json').read_bytes()).hexdigest() == PIN
        cls.oracle = json.loads((FIXTURE / 'accepted-oracle.json').read_bytes())
        cls.books = reference.load_books()
        cls.cycle = reference.export_cycle_tables(cls.books)
        cls.temp = tempfile.TemporaryDirectory()
        cls.data = Path(cls.temp.name)
        for name, rows in [('katameros_cycle_readings', cls.cycle),
                           ('katameros_cycle_passage_index', reference.build_passage_index(cls.cycle, cls.books))]:
            with (cls.data / (name + '.csv')).open('w', newline='') as f:
                fields = list(dict.fromkeys(k for r in rows for k in r))
                w = csv.DictWriter(f, fields); w.writeheader(); w.writerows(rows)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def cli(self, passage, historical=False):
        cmd = [sys.executable, str(ROOT / 'query_lectionary.py'), '--data-dir', str(self.data),
               '--cycle-passage', passage, '--limit', '10000']
        if historical:
            cmd.append('--historical')
        p = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def test_corrected_numeric_and_textual_acts_are_equivalent(self):
        for p in ('Acts 24:1-9', '44.24:1-9'):
            result = self.cli(p)
            for key in ('Bashans 5', 'Baunah 5', 'Abib 5'):
                self.assertIn('SundayReadings | ' + key + ' |', result)
                self.assertEqual(sum('SundayReadings | ' + key + ' |' in l for l in result.splitlines()), 1)

    def test_current_old_coordinates_do_not_expose_superseded_appointments(self):
        for p in ('44.14:1-9', 'Acts 14:1-9'):
            result = self.cli(p)
            for key in ('Bashans 5', 'Baunah 5', 'Abib 5'):
                self.assertNotIn('SundayReadings | ' + key + ' |', result)
        result = self.cli('44.18:13-21')
        self.assertIn('SundayReadings | Tut 5 |', result)
        self.assertIn('Acts 18:9-21', result)
        self.assertNotIn('Acts 18:9-12 |', '\n'.join(l for l in self.cli('44.18:9-12').splitlines() if '| Tut 5 |' in l))

    def test_numeric_query_excludes_each_explicit_removed_state_without_prefilter(self):
        anchor = next(r for r in self.cycle if r.get('day_key') == 'Bashans 5' and r.get('normalized_ref') == 'Acts 24:1-9')
        markers = [{'active': False}, {'include_in_current_index': 'false'}, {'state': 'removed'},
                   {'status': 'inactive'}, {'removed_from_standard_lectionary': 'true'},
                   {'removal_reason': 'removed'}, {'removed_reason': 'removed'},
                   {'removal_effective_version': '0.9'}, {'superseded_reason': 'superseded'},
                   {'removed_marker': 'removed'}, {'superseded_by_ref': 'Acts 24:1-9'}]
        original = (self.data / 'katameros_cycle_readings.csv').read_bytes()
        try:
            probes = [dict(anchor, day_key='removed-probe-' + str(i), **marker) for i, marker in enumerate(markers)]
            values = self.cycle + probes
            fields = list(dict.fromkeys(k for r in values for k in r))
            with (self.data / 'katameros_cycle_readings.csv').open('w', newline='') as f:
                w = csv.DictWriter(f, fields); w.writeheader(); w.writerows(values)
            self.assertNotIn('removed-probe-', self.cli('44.24:1-9'))
            self.assertIn('removed-probe-', self.cli('44.24:1-9', historical=True))
        finally:
            (self.data / 'katameros_cycle_readings.csv').write_bytes(original)

    def test_historical_lane_is_explicitly_labeled_and_retains_raw(self):
        result = self.cli('44.14:1-9', historical=True)
        self.assertIn('HISTORICAL', result)
        self.assertIn('state=superseded', result)
        self.assertIn('raw=44.14:1-9', result)
        self.assertIn('SundayReadings | Bashans 5 |', result)

    def test_sunday_held_psalm_survives_real_csv_design_daily_reverse_disclosure(self):
        row = sunday_rows()[0]
        projected = serialize(crosswalk.project_date_rows([row]), crosswalk.FIELDS)
        self.assertEqual(projected[0]['source_family'], 'coptic_reader_verified_sunday_policy')
        self.assertIn('HELD', projected[0]['provenance'])
        presentation, identities = design.build_reverse_presentation(projected)
        p = presentation[0]
        self.assertNotEqual(p['source_convention'], 'mt_nkjv')
        self.assertEqual(p['canonical_mt_ref'], '')
        self.assertEqual(p['canonical_lxx_ref'], '')
        self.assertEqual(p['canonicalization_confidence'], 'held')
        self.assertEqual(p['source_label'], projected[0]['passage'])
        table = self.oracle['tables'][0]
        block = table['documents'][0]['assigned_blocks'][0]
        # Observe the actual reverse payload at its unchanged fail-closed ledger
        # boundary; never substitute candidate mode or bypass this validator.
        from unittest.mock import patch
        reverse = []
        verifier = design.verify_reverse_index_contract
        def observe(rows):
            reverse.extend(rows)
            return verifier(rows)
        with patch.object(design, 'verify_reverse_index_contract', observe), self.assertRaises(AssertionError):
            design.build_reverse_lectionary_index(presentation, transport_mode='presentation')
        self.assertEqual(len(reverse), 1)
        for output in (projected, presentation, reverse,
                       design.build_daily_year_files(presentation, transport_mode='presentation')[2027]['2027-02-21'],
                       design.build_collapsed_source_disclosure(presentation)[0],
                       design.build_passage_source_disclosure(presentation, transport_mode='presentation')):
            text = json.dumps(output, ensure_ascii=False)
            self.assertIn(block['printed_ref'], text)
            self.assertIn(block['literal_block_sha256'], text)
            self.assertIn('HELD', text)
        self.assertEqual(json.loads(projected[0]['provenance'])['consumer_source_transport']['source_block']['literal_block'], block['literal_block'])

    def test_each_removal_marker_survives_csv_and_never_restores_daily(self):
        base = sunday_rows()[0]
        markers = [{'active': False}, {'active': 'false'}, {'include_in_current_index': False},
                   {'state': 'removed'}, {'status': 'removed'}, {'state': 'superseded'},
                   {'removed_from_standard_lectionary': True}, {'removal_reason': 'source removed'},
                   {'removed_reason': 'source removed'}, {'removal_effective_version': '0.9'},
                   {'superseded_reason': 'source superseded'}, {'removed_marker': 'removed'},
                   {'superseded_by_ref': 'Ps 17:1-15'}]
        for marker in markers:
            with self.subTest(marker=marker):
                projected = serialize(crosswalk.project_date_rows([dict(base, **marker)]), crosswalk.FIELDS)
                presentation, _ = design.build_reverse_presentation(projected)
                self.assertFalse(design.is_current_presentation(presentation[0]))
                self.assertEqual(design.build_daily_year_files(presentation, transport_mode='presentation'), {})
                transport = json.loads(projected[0]['provenance'])['consumer_source_transport']
                for k, v in marker.items():
                    self.assertEqual(transport['state'][k], v)

    def test_held_psalm_missing_or_downgraded_transport_is_rejected(self):
        projected = serialize(crosswalk.project_date_rows([sunday_rows()[0]]), crosswalk.FIELDS)[0]
        for change in ('missing', 'downgrade', 'truncated_body'):
            bad = copy.deepcopy(projected)
            data = json.loads(bad['provenance'])
            if change == 'missing':
                data.pop('consumer_source_transport')
            elif change == 'downgrade':
                data['consumer_source_transport']['normalization_state'] = 'source_qualified'
            else:
                data['consumer_source_transport']['source_block']['literal_block'] = 'truncated'
            bad['provenance'] = json.dumps(data)
            with self.subTest(change=change), self.assertRaises(ValueError):
                design.build_reverse_presentation([bad])

    def test_direct_daily_reverse_disclosure_reject_truncated_source_body(self):
        projected = serialize(crosswalk.project_date_rows([sunday_rows()[0]]), crosswalk.FIELDS)
        presentation, _ = design.build_reverse_presentation(projected)
        data = json.loads(presentation[0]['provenance'])
        data['consumer_source_transport']['source_block']['literal_block'] = 'truncated'
        presentation[0]['provenance'] = json.dumps(data)
        for consumer in (design.build_daily_year_files, design.build_reverse_lectionary_index,
                         design.build_passage_source_disclosure):
            with self.subTest(consumer=consumer.__name__), self.assertRaises(ValueError):
                consumer(presentation)

    def test_direct_consumers_cannot_promote_held_psalm_to_exact_mt(self):
        projected = serialize(crosswalk.project_date_rows([sunday_rows()[0]]), crosswalk.FIELDS)
        presentation, _ = design.build_reverse_presentation(projected)
        presentation[0]['canonical_mt_ref'] = 'Ps 17:3,17:15'
        for consumer in (design.build_daily_year_files, design.build_reverse_lectionary_index,
                         design.build_passage_source_disclosure):
            with self.subTest(consumer=consumer.__name__), self.assertRaises(ValueError):
                consumer(presentation)

    def test_wrong_context_has_no_reader_source_body(self):
        row = sunday_rows()[0]
        row['source'] = 'other'
        projected = crosswalk.project_date_rows([row])
        self.assertEqual(projected[0]['source_family'], 'ordinary_date_resolved')
        self.assertNotIn('source_block', projected[0]['provenance'])

    def test_legacy_identity_unchanged_and_candidate_still_opt_in(self):
        self.assertEqual(design.identity_for('Ps 17:3,17:15')['identity_key'], 'rid_03817397d9b1b7d01295')
        self.assertEqual(design.identity_for('Ps 17:3,17:15')['source_convention'], 'mt_nkjv')
        with self.assertRaises(ValueError):
            design.identity_for('Sir 8:1-22', 'edition_fragment_candidate')


if __name__ == '__main__':
    unittest.main()
