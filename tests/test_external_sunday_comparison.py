"""Sunday cache gate: authenticated witnesses, real serialized consumers, isolated writes."""
import copy
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import compare_external_sources as comparator
import sunday_consumer_contracts as contracts

ROOT = Path(__file__).resolve().parents[1]


class SundayComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = comparator.load_csv(comparator.SOURCE_INDEX)
        cls.daily = {year: comparator.load_json(comparator.PACKAGE_DIR / 'data/daily' / f'lectionary-{year}.json')
                     for year in (2027, 2028)}

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.package = self.root / 'package'
        (self.package / 'data/daily').mkdir(parents=True)

    def fixture(self, date='2027-02-07'):
        return ([copy.deepcopy(r) for r in self.source if r['gregorian_date'] == date],
                {date: copy.deepcopy(self.daily[int(date[:4])][date])})

    def compare(self, source, daily, policy=None):
        year = int(next(iter(daily))[:4])
        (self.package / 'meta.json').write_text(json.dumps({'shipped_years': [year]}))
        (self.package / 'data/daily' / f'lectionary-{year}.json').write_text(json.dumps(daily))
        index = self.root / 'index.csv'
        fields = list(dict.fromkeys(k for r in source for k in r)) or list(self.source[0])
        with index.open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader(); writer.writerows(source)
        kwargs = {}
        if policy is not None:
            path = self.root / 'policy.json'
            path.write_text(json.dumps(policy))
            kwargs['corrections_path'] = path
        return comparator.compare_copticchurch_cache(self.package, index, [year], **kwargs)

    def rejected(self, source, daily, policy=None):
        try:
            result = self.compare(source, daily, policy)
        except (AssertionError, ValueError, RuntimeError):
            return
        self.assertEqual(result['status'], 'fail', result)

    def test_all_shipped_selected_sunday_tables_preserve_full_multiplicity(self):
        dates = sorted({r['gregorian_date'] for r in self.source if r['source'] == contracts.SOURCE
                        and r['gregorian_date'][:4] in ('2027', '2028')})
        self.assertTrue(dates)
        for date in dates:
            with self.subTest(date=date):
                source, daily = self.fixture(date)
                result = self.compare(source, daily)
                self.assertEqual(result['status'], 'pass', result)
                self.assertEqual(result['years'][date[:4]]['source_rows'], len(source))
                self.assertEqual(result['years'][date[:4]]['comparable_package_rows'], len(source))

    def test_source_context_reference_order_rule_and_hold_corruptions_fail(self):
        source, daily = self.fixture()
        for field, value in [('source', 'copticchurch.net daily scrape'), ('day_title', 'First Sunday of Toba'),
                             ('service_section', 'Matins'), ('source_slot', 'Gospel'), ('source_order', '2'),
                             ('matched_ref', 'Ps 82:7'), ('raw_ref', '19.83:8,6'),
                             ('source_raw_refs', '19.83:8,6'), ('source_ref_status', 'ok'),
                             ('correction_source', 'wrong.json'), ('service_hour', 'Third Hour'),
                             ('normalization_warning', source[0]['normalization_warning'].replace('5/30', '6/30')),
                             ('normalization_warning', source[0]['normalization_warning'].replace('HELD', 'resolved')),
                             ('normalization_warning', source[0]['normalization_warning'].replace(':21;', ':22;'))]:
            with self.subTest(field=field, value=value):
                rows = copy.deepcopy(source); rows[0][field] = value
                self.rejected(rows, daily)

    def test_symmetric_wrong_date_and_matching_source_package_reference_fail(self):
        source, daily = self.fixture()
        for row in source: row['gregorian_date'] = '2027-02-08'
        daily['2027-02-08'] = daily.pop('2027-02-07')
        self.rejected(source, daily)
        source, daily = self.fixture()
        source[0]['matched_ref'] = 'Ps 82:7'
        daily['2027-02-07'][0]['display_ref'] = 'Ps 82:7 (Reader Psalm alignment HELD)'
        self.rejected(source, daily)

    def test_package_schema_disclosure_flags_hold_and_order_corruptions_fail(self):
        source, original = self.fixture('2027-02-21')
        for field, value in [('source_family', 'ordinary_date_resolved'), ('source_file', 'wrong.json'),
                             ('occasion', 'Third Sunday of Toba'), ('service_hour', 'Third Hour'),
                             ('slot', 'Gospel'), ('slot_type', 'gospel'), ('slot_order', 2), ('slot_order', True),
                             ('service_order', 3), ('reading_order', True),
                             ('canonical_mt_ref', 'Ps 82:6'), ('canonical_lxx_ref', 'Ps 81:6'),
                             ('display_ref', 'Ps 82:6'), ('source_disclosure', '[]'),
                             ('runtime_activation', 0), ('consumer_eligible', 'false')]:
            with self.subTest(field=field):
                daily = copy.deepcopy(original); daily['2027-02-21'][0][field] = value
                self.rejected(source, daily)
        for field in ('source_disclosure', 'spans_json', 'canonical_mt_ref', 'removed_marker', 'reading_order'):
            daily = copy.deepcopy(original); del daily['2027-02-21'][0][field]
            self.rejected(source, daily)
        for flag in (0, 'false', True):
            daily = copy.deepcopy(original)
            row = daily['2027-02-21'][0]
            disclosure = json.loads(row['source_disclosure'])
            disclosure[0]['consumer_source_transport'][0]['runtime_activation'] = flag
            row['source_disclosure'] = json.dumps(disclosure)
            self.rejected(source, daily)
        for mutation in ('omit', 'duplicate', 'reorder', 'forge-body', 'hold', 'month', 'hash'):
            with self.subTest(mutation=mutation):
                daily = copy.deepcopy(original); rows = daily['2027-02-21']
                if mutation == 'omit': rows.pop(0)
                elif mutation == 'duplicate': rows.append(copy.deepcopy(rows[0]))
                elif mutation == 'reorder':
                    rows[0], rows[1] = rows[1], rows[0]
                    for i, row in enumerate(rows, 1): row['reading_order'] = i
                else:
                    disclosure = json.loads(rows[0]['source_disclosure'])
                    envelope = disclosure[0]['consumer_source_transport'][0]
                    if mutation == 'forge-body': envelope['source_block']['literal_block'] += ' forged'
                    elif mutation == 'hold': envelope['normalization_state'] = 'source_qualified'
                    elif mutation == 'month': envelope['normalization_warning'] = envelope['normalization_warning'].replace('6/', '5/')
                    elif mutation == 'hash': envelope['source_document_sha256'] = '0' * 64
                    rows[0]['source_disclosure'] = json.dumps(disclosure)
                self.rejected(source, daily)

    def test_oracle_policy_hash_drift_fails_closed(self):
        source, daily = self.fixture()
        policy = comparator.load_json(comparator.CORRECTIONS)
        policy['source_fingerprints'][contracts.FILE] = '0' * 64
        self.rejected(source, daily, policy)

    def test_immutable_witness_drift_rejected_in_isolated_snapshot(self):
        import calendar_resolution as calendar
        from unittest.mock import patch
        snapshot = self.root / 'snapshot'
        shutil.copytree(ROOT / calendar.SUNDAY_FIXTURE, snapshot / calendar.SUNDAY_FIXTURE)
        db_relative = Path('sources/katameros-api/Core/KatamerosDatabase.db')
        (snapshot / db_relative).parent.mkdir(parents=True)
        shutil.copyfile(ROOT / db_relative, snapshot / db_relative)
        source, daily = self.fixture('2027-02-21')
        manifest = json.loads((snapshot / calendar.SUNDAY_FIXTURE / 'manifest.json').read_text())
        body = next(path for path in manifest['files'] if path.endswith('.txt'))
        with patch.object(calendar, 'WORK', snapshot):
            self.assertEqual(self.compare(source, daily)['status'], 'pass')
            for relative in (calendar.SUNDAY_FIXTURE / 'manifest.json',
                             calendar.SUNDAY_FIXTURE / 'accepted-oracle.json',
                             calendar.SUNDAY_FIXTURE / body, db_relative):
                with self.subTest(witness=str(relative)):
                    path = snapshot / relative
                    original = path.read_bytes()
                    try:
                        path.write_bytes(original + b'corrupted')
                        self.rejected(source, daily)
                    finally:
                        path.write_bytes(original)

    def test_literal_false_flags_allowed_but_source_lifecycle_and_multiplicity_fail(self):
        source, daily = self.fixture()
        for row in daily['2027-02-07']:
            row['runtime_activation'] = row['consumer_eligible'] = False
        self.assertEqual(self.compare(source, daily)['status'], 'pass')
        for field, value in (('active', 'false'), ('state', 'removed'), ('include_in_current_index', 'false'),
                             ('runtime_activation', 'false'), ('consumer_eligible', 0)):
            with self.subTest(field=field):
                rows = copy.deepcopy(source); rows[0][field] = value
                self.rejected(rows, daily)
        for operation in ('omit', 'duplicate', 'blanket-reader'):
            rows = copy.deepcopy(source)
            if operation == 'omit': rows.pop(0)
            elif operation == 'duplicate': rows.append(copy.deepcopy(rows[0]))
            else: rows[0]['source'] = 'Coptic Reader unverified Sunday'
            self.rejected(rows, daily)

    def test_boundary_regression_remains_a_strict_failure_not_a_sunday_exclusion(self):
        source, daily = self.fixture('2028-04-07')
        self.assertEqual(self.compare(source, daily)['status'], 'pass')
        rows = daily['2028-04-07']
        # Reintroduce R1's OT1/Psalm/Gospel/OT2 projection, even with apparently
        # valid per-date reading_order. This is not a Sunday-policy appointment.
        rows[1], rows[4] = rows[4], rows[1]
        for i, row in enumerate(rows, 1): row['reading_order'] = i
        result = self.compare(source, daily)
        self.assertEqual(result['status'], 'fail')
        self.assertTrue(any(r['status'].startswith('invalid_seasonal_primary_table:')
                            for r in result['comparison_rows']))

    def test_cli_returns_nonzero_for_dictionary_failure(self):
        source, daily = self.fixture()
        daily['2027-02-07'].pop()
        self.assertEqual(self.compare(source, daily)['status'], 'fail')
        proc = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/compare_external_sources.py'),
                               '--package-dir', str(self.package), '--source-index', str(self.root / 'index.csv'),
                               '--years', '2027'], capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == '__main__':
    unittest.main()
