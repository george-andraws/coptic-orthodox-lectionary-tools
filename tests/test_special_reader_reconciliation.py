"""Primary-source regressions; no network, vault or shared build output."""
import collections
import contextlib
import copy
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import build_special_service_reference as special

FIXTURE = Path(__file__).resolve().parents[1] / 'sources/coptic-reader/special-reconciled-2026-10-07'
ORACLE = json.loads((FIXTURE / 'assigned-scripture-oracle.json').read_text())
ASSIGNED = [b for b in ORACLE if b['kind'] == 'assigned_scripture_reading']


def reader_rows():
    return [r for r in special.ROWS if r['service_variant'].startswith('coptic_reader__')]


def evidence(row):
    return json.loads(row['notes'].split('evidence=', 1)[1])


class SpecialReaderReconciliation(unittest.TestCase):
    def test_baptism_water_catholic_boundary(self):
        row = next(r for r in special.ROWS if r['service_family'] == 'baptism'
                   and r['service_variant'] == 'sanctification_of_baptismal_water'
                   and r['reading_type'] == 'catholic')
        self.assertEqual(special.canonicalize_row_refs(row)['canonical_ref'], '1Jn 5:5-14')
        self.assertEqual([r['matched_ref'] for r in special.build_passage_index([row])], ['1Jn 5:5-14'])
        self.assertEqual(row['raw_ref'], '1 John 5:5-20')

    def test_cornerstone_boundaries(self):
        expected = {'old_testament': 'Gen 28:10-22', 'pauline': 'Heb 9:1-11', 'gospel': 'Lk 9:28-36'}
        for kind, reference in expected.items():
            with self.subTest(kind=kind):
                row = next(r for r in special.ROWS if r['service_family'] == 'cornerstone_prayer'
                           and r['service_variant'] == 'main' and r['reading_type'] == kind)
                self.assertEqual(special.canonicalize_row_refs(row)['canonical_ref'], reference)
                self.assertEqual([r['matched_ref'] for r in special.build_passage_index([row])], [reference])

    def test_all_73_documents_and_333_assigned_blocks_are_hash_bound(self):
        manifest, _ = special.load_reader_fixture()
        self.assertEqual(manifest['document_count'], 73)
        self.assertEqual(manifest['assigned_reading_count'], 333)
        self.assertEqual(manifest['assigned_context_count'], 48)
        self.assertFalse(manifest['completeness_claimed'])
        for block in ORACLE:
            with self.subTest(capture=block['provenance']['captureId'], line=block['lineNumber']):
                raw = FIXTURE / 'raw' / (block['provenance']['captureId'] + '.txt')
                self.assertEqual(hashlib.sha256(raw.read_bytes()).hexdigest(), block['provenance']['rawTextSha256'])
                self.assertEqual(raw.read_text().splitlines()[block['lineNumber'] - 1], block['rawHeading'])

    def test_independent_oracle_exact_once_order_context_and_provenance(self):
        # Expected headings/order come directly from the independently captured oracle,
        # never from the implementation's row-construction helper.
        grouped = collections.defaultdict(list)
        for row in reader_rows():
            meta = evidence(row)
            grouped[tuple(meta['navigation'])].append((row, meta))
        expected_contexts = {tuple(b['provenance']['navigation']) for b in ASSIGNED}
        self.assertEqual(set(grouped), expected_contexts)
        self.assertEqual(sum(map(len, grouped.values())), 333)
        for navigation in expected_contexts:
            expected = [b for b in ASSIGNED if tuple(b['provenance']['navigation']) == navigation]
            actual = grouped[navigation]
            with self.subTest(context=navigation):
                self.assertEqual([r['raw_ref'] for r, m in actual], [b['printedRef'] for b in expected])
                self.assertEqual([m['ordinal'] for r, m in actual], [b['ordinalWithinDocument'] for b in expected])
                self.assertEqual([m['line'] for r, m in actual], [b['lineNumber'] for b in expected])
                self.assertEqual([m['raw_heading'] for r, m in actual], [b['rawHeading'] for b in expected])
                self.assertEqual([m['capture_id'] for r, m in actual], [b['provenance']['captureId'] for b in expected])
                self.assertEqual([m['raw_text_sha256'] for r, m in actual], [b['provenance']['rawTextSha256'] for b in expected])
                self.assertTrue(all(m['status'] == 'source_confirmed_assigned' for r, m in actual))
        keys = [(evidence(r)['capture_id'], evidence(r)['ordinal']) for r in reader_rows()]
        self.assertEqual(len(set(keys)), len(keys))

    def test_prescribed_prayers_interpretation_and_incidental_refs_not_promoted(self):
        actual = {(evidence(r)['capture_id'], evidence(r)['ordinal']) for r in reader_rows()}
        excluded = [b for b in ORACLE if b['kind'] != 'assigned_scripture_reading']
        self.assertEqual(len(excluded), 70)
        self.assertFalse(actual.intersection((b['provenance']['captureId'], b['ordinalWithinDocument']) for b in excluded))
        documents = json.loads((FIXTURE / 'document-dispositions.json').read_text())
        negatives = [d for d in documents if d['assignedReadingBlocks'] == 0]
        self.assertEqual(len(negatives), 25)
        self.assertFalse({evidence(r)['capture_id'] for r in reader_rows()}.intersection(d['provenance']['captureId'] for d in negatives))

    def test_all_178_legacy_raw_rows_and_provenance_retained(self):
        frozen = json.loads((FIXTURE / 'legacy-generator-rows.json').read_text())
        self.assertEqual(len(frozen), 178)
        self.assertEqual(special.LEGACY_ROWS, frozen)
        self.assertEqual(special.ROWS[:178], frozen)
        indexed = special.build_passage_index(special.LEGACY_ROWS)
        with patch.object(special, 'BOUNDARY_CORRECTIONS', {}):
            baseline = special.build_passage_index(special.LEGACY_ROWS)
        self.assertEqual(len(indexed), len(baseline))
        identity = lambda r: (r['service_family'], r['service_variant'], r['section'], r['reading_type'], r['raw_ref'], r['matched_ref'])
        before = collections.Counter(map(identity, baseline))
        after = collections.Counter(map(identity, indexed))
        self.assertEqual(sum((before - after).values()), 4)
        self.assertEqual(sum((after - before).values()), 4)
        for correction in special.READER_MANIFEST['boundary_corrections']:
            row = next(r for r in frozen if (r['service_family'], r['service_variant'], r['reading_type'], r['raw_ref']) ==
                       (correction['service_family'], correction['service_variant'], correction['reading_type'], correction['expected_raw_ref']))
            normalized = special.canonicalize_row_refs(row)
            self.assertEqual(normalized['raw_ref'], correction['expected_raw_ref'])
            self.assertIn('superseded_boundary_preserved_as_raw', normalized['notes'])
            self.assertEqual(normalized['source_url'], row['source_url'])
            wrong_variant = dict(row, service_variant='other_variant')
            self.assertNotEqual(special.canonicalize_row_refs(wrong_variant)['canonical_ref'], normalized['canonical_ref'])

    def test_psalm_book_continuations_do_not_disappear_or_renumber(self):
        cases = {'Psalms 127:1; 122:1-2': ['Ps 127:1', 'Ps 122:1-2'],
                 'Psalms 114:3-8;115:1-2': ['Ps 114:3-8', 'Ps 115:1-2'],
                 'Psalm 64:1; 149:1': ['Ps 64:1', 'Ps 149:1']}
        for printed, expected in cases.items():
            row = next(r for r in reader_rows() if r['raw_ref'] == printed)
            with self.subTest(printed=printed):
                self.assertEqual([r['matched_ref'] for r in special.build_passage_index([row])], expected)
                self.assertEqual(row['raw_ref'], printed)
        girl = next(r for r in reader_rows() if evidence(r)['navigation'][-1] == 'Absolution of the Woman (Girl)' and r['reading_type'] == 'psalm')
        self.assertEqual(girl['raw_ref'], 'Psalms 45:13')
        self.assertEqual(special.canonicalize_row_refs(girl)['canonical_ref'], 'Ps 45:13')
        self.assertTrue(any(r['raw_ref'] == 'Psalm 45:9; Psalm 45:13' for r in special.LEGACY_ROWS))

    def test_myron_source_variants_and_first_second_third_liturgies_never_collapse(self):
        rows = reader_rows()
        third = next(r for r in rows if evidence(r)['navigation'][-1] == 'Pre-sanctified Chrism' and r['raw_ref'] == '1 John 5:5-13')
        consecration_day = next(r for r in rows if evidence(r)['navigation'][-1] == 'Oil of Gladness' and r['raw_ref'] == '1 John 4:7-5:21')
        self.assertEqual(third['section'], 'third_liturgy_liturgy_of_the_word')
        self.assertNotEqual(third['service_variant'], consecration_day['service_variant'])
        sections = {r['section'] for r in rows if evidence(r)['navigation'][-1] == 'Pre-sanctified Chrism'}
        self.assertEqual(sections, {f'{n}_liturgy_{s}' for n in ['first', 'second', 'third']
                                   for s in ['offering_of_morning_incense', 'liturgy_of_the_word']})
        self.assertTrue(any(r['raw_ref'] == '1 Timothy 2:11-3:7' and r['service_variant'] == third['service_variant'] for r in rows))
        stages = {evidence(r)['navigation'][-1] for r in rows if 'Myron' in evidence(r)['navigation']}
        self.assertEqual(stages, {'Preparation', 'Consecration'})

    def test_church_consecration_all_subservices_and_theophany_pauline_once_per_source_context(self):
        rows = reader_rows()
        church = [r for r in rows if evidence(r)['navigation'][1:3] == ['Consecrations', 'Church']]
        self.assertEqual(len(church), 45)
        self.assertEqual(collections.Counter(evidence(r)['navigation'][-1] for r in church),
                         {'Liturgy of the Word': 5, 'Part 1': 8, 'Part 2': 12, 'Part 3': 5, 'Part 4': 13, 'Vespers': 2})
        theophany = [r for r in rows if evidence(r)['navigation'] == ['Special', 'Lakkan', 'Theophany']]
        self.assertEqual(len(theophany), 10)
        self.assertEqual(sum(r['raw_ref'] == '1 Corinthians 10:1-13' for r in theophany), 1)
        self.assertEqual(sum(r['raw_ref'] == '1 Corinthians 10:1-13' and r['service_variant'] == 'epiphany_laqan'
                             for r in special.LEGACY_ROWS), 1)

    def test_omitted_reordered_truncated_wrong_variant_removed_duplicate_and_incidental_fail_closed(self):
        for mutation in ['omitted', 'reordered', 'truncated', 'wrong_variant', 'removed', 'duplicate', 'incidental']:
            rows = copy.deepcopy(special.ROWS)
            first = 178
            if mutation == 'omitted':
                del rows[first]
            elif mutation == 'reordered':
                rows[first], rows[first + 1] = rows[first + 1], rows[first]
            elif mutation == 'truncated':
                rows[first]['raw_ref'] = 'Hebrews 1:8-11'
            elif mutation == 'wrong_variant':
                rows[first]['service_variant'] += '_other'
            elif mutation == 'removed':
                rows[first]['notes'] = rows[first]['notes'].replace('source_confirmed_assigned', 'removed')
            elif mutation == 'duplicate':
                rows.insert(first, copy.deepcopy(rows[first]))
            else:
                rows[first]['raw_ref'] = 'John 3:16'
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(RuntimeError, 'omitted/reordered/truncated/wrong context or status'):
                    special.validate_reader_rows(rows)
                with tempfile.TemporaryDirectory() as temporary:
                    output = Path(temporary) / 'not_created'
                    with patch.object(special, 'ROWS', rows), patch.object(special, 'OUT', output), patch.object(special, 'DISABLE_VAULT_PUBLISH', True):
                        with self.assertRaises(RuntimeError):
                            special.main()
                    self.assertFalse(output.exists())

    def test_raw_or_oracle_or_manifest_hash_corruption_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / 'fixture'
            shutil.copytree(FIXTURE, directory)
            for relative in ['manifest.json', 'assigned-scripture-oracle.json', next(n for n in special.READER_MANIFEST['files'] if n.startswith('raw/'))]:
                target = directory / relative
                original = target.read_bytes()
                with self.subTest(file=relative):
                    target.write_bytes(original + b' ')
                    with self.assertRaisesRegex(RuntimeError, 'source drift'):
                        special.load_reader_fixture(directory)
                    target.write_bytes(original)

    def test_cli_isolated_env_and_nonexistent_home_do_not_publish(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / 'missing_home'
            output = root / 'cli_output'
            env = dict(os.environ, HOME=str(home), LECTIONARY_DISABLE_VAULT_PUBLISH='1',
                       LECTIONARY_SPECIAL_OUTPUT_DIR=str(output))
            result = subprocess.run([sys.executable, str(Path(special.__file__).resolve())],
                                    cwd=root, env=env, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['curated_rows'],
                             len(json.loads((FIXTURE / 'legacy-generator-rows.json').read_text())) +
                             len(json.loads((special.PROJECTION_DIR / 'records.json').read_text())))
            self.assertFalse(home.exists())
            self.assertEqual(set(p.name for p in output.iterdir()),
                             {'special_service_readings_curated.csv', 'special_service_readings_curated.jsonl',
                              'special_service_passage_index.csv', 'special_service_passage_index.jsonl'})

    def test_isolated_real_generator_csv_jsonl_round_trip_without_vault(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'data'
            vault = Path(temporary) / 'forbidden_vault'
            with patch.object(special, 'OUT', output), patch.object(special, 'VAULT', vault), patch.object(special, 'DISABLE_VAULT_PUBLISH', True), contextlib.redirect_stdout(io.StringIO()) as log:
                special.main()
            self.assertFalse(vault.exists())
            self.assertEqual(json.loads(log.getvalue())['curated_rows'],
                             len(json.loads((FIXTURE / 'legacy-generator-rows.json').read_text())) +
                             len(json.loads((special.PROJECTION_DIR / 'records.json').read_text())))
            with (output / 'special_service_readings_curated.csv').open() as handle:
                csv_rows = list(csv.DictReader(handle))
            json_rows = [json.loads(line) for line in (output / 'special_service_readings_curated.jsonl').read_text().splitlines()]
            self.assertEqual(csv_rows, json_rows)
            # Original 511 ROWS / 333 assigned blocks remain a separate valid lane.
            self.assertEqual(len(special.ROWS), 511)
            self.assertEqual(len(reader_rows()), 333)
            special.validate_reader_rows(special.ROWS)
            projected = special.project_special_contexts()
            special.validate_projection_rows(projected)
            # API parity is supplemental, not the source of behavioral expectations.
            self.assertEqual(json_rows, [special.canonicalize_row_refs(r) for r in projected])
            records = json.loads((special.PROJECTION_DIR / 'records.json').read_text())
            frozen = json.loads((FIXTURE / 'legacy-generator-rows.json').read_text())
            def meta(row):
                value = special.projection_metadata(row)
                assert value is not None
                return value
            original_keys = {(b['provenance']['captureId'], b['ordinalWithinDocument']) for b in ORACLE}
            source_keys = {(x['capture_id'], x['ordinal']) for x in records}
            self.assertEqual(len(ORACLE), 403)
            self.assertEqual(len(ASSIGNED), 333)
            self.assertEqual(len(original_keys), 403)
            self.assertTrue(original_keys.issubset(source_keys))
            self.assertEqual(len(source_keys - original_keys), 75)
            self.assertEqual(len(records), len(source_keys))
            self.assertEqual(len(frozen), 178)
            self.assertEqual(len(json_rows), 656)
            self.assertEqual([(meta(r)['capture_id'], meta(r)['ordinal'], r['raw_ref'])
                              for r in json_rows[178:]],
                             [(x['capture_id'], x['ordinal'], x['printed_ref']) for x in records])
            for old, row in zip(frozen, json_rows):
                self.assertEqual({k: row[k].split(special.PROJECTION_MARKER)[0] if k == 'notes' else row[k]
                                  for k in old}, old)
            for row, record in zip(json_rows[178:], records):
                with self.subTest(capture=record['capture_id'], ordinal=record['ordinal']):
                    raw = (special.PROJECTION_DIR / 'raw' / (record['capture_id'] + '.txt')).read_bytes()
                    self.assertEqual(hashlib.sha256(raw).hexdigest(), record['raw_text_sha256'])
                    text = raw.decode()
                    self.assertEqual(text.splitlines()[record['line'] - 1], record['raw_heading'])
                    self.assertTrue(text[record['offset']:].startswith(record['raw_heading']))
                    for key in ['capture_id', 'ordinal', 'navigation', 'raw_text_sha256', 'line',
                                'offset', 'raw_heading', 'context', 'kind', 'selected', 'section']:
                        self.assertEqual(meta(row)[key], record[key])
            pidx = [json.loads(line) for line in (output / 'special_service_passage_index.jsonl').read_text().splitlines()]
            with (output / 'special_service_passage_index.csv').open() as handle:
                self.assertEqual(list(csv.DictReader(handle)), pidx)
            self.assertEqual(pidx, special.build_passage_index(projected))
            self.assertEqual(len(pidx), 364)
            self.assertEqual(sum(meta(r)['is_active'] for r in json_rows), 331)
            self.assertFalse(any(r['service_variant'].startswith('coptic_reader__') for r in json_rows))
            self.assertFalse(any(r['service_variant'].startswith('coptic_reader__') for r in pidx))
            indexed_keys = {(meta(r).get('capture_id'), meta(r).get('ordinal')) for r in pidx}
            for row in json_rows:
                if not meta(row)['is_active']:
                    self.assertEqual(special.build_passage_index([row]), [])
                    self.assertEqual(row['canonical_ref'], '')
                    if meta(row).get('capture_id'):
                        self.assertNotIn((meta(row)['capture_id'], meta(row)['ordinal']), indexed_keys)
            for row in pidx:
                self.assertTrue(meta(row)['is_active'])


if __name__ == '__main__':
    unittest.main()
