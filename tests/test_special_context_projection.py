"""Consumer projection counterprobes, independent captured source expectations."""
import copy
import json
from pathlib import Path
import unittest
import collections
import os
import subprocess
import sys
import tempfile
import shutil
import csv
import hashlib
import build_special_service_reference as s


# Frozen from the independent review's independent-count-contract.json
# (sha256 b5ee147091ec9c2557f352f4b1b1b47049078f2e60f26cc27790ad22de117cfe).
# Labels only: endpoints stay exactly as printed in authenticated rubric evidence.
# Never compute these expectations with the implementation's parser/canonicalizer.
APPROVED_SOURCE_SPANS = {
    '1 Chronicles 15:2-16:43': ['1Chr 15:2-16:43'],
    '1 Chronicles 28:2-29:22': ['1Chr 28:2-29:22'],
    '2 Chronicles 3:1-6:11': ['2Chr 3:1-6:11'],
    '1 Kings 8:22-61': ['1Kgs 8:22-61'],
    '2 Chronicles 7:1-6': ['2Chr 7:1-6'],
    '2 Chronicles 7:7-18': ['2Chr 7:7-18'],
    'Revelation 21': ['Rev 21'],
    'Song of Solomon 2:1-17': ['Song 2:1-17'],
    'Song of Solomon 3:1-11': ['Song 3:1-11'],
    'Song of Solomon 4:1-16': ['Song 4:1-16'],
    'Song of Solomon 5:1-16': ['Song 5:1-16'],
    'Song of Solomon 6:1-13': ['Song 6:1-13'],
    'Song of Solomon 7:1-13': ['Song 7:1-13'],
    'Song of Solomon 8:1-14': ['Song 8:1-14'],
    '1 Kings 19:9-18': ['1Kgs 19:9-18'],
    '1 Chronicles 11:1-5': ['1Chr 11:1-5'],
    '1 Chronicles 29:20-25': ['1Chr 29:20-25'],
    'Proverbs 8:22-31': ['Prov 8:22-31'],
    'Isaiah 61:1-11': ['Isa 61:1-11'],
    'Daniel 9:20-27': ['Dan 9:20-27'],
    'Acts 2:1-42': ['Acts 2:1-42'],
    'Acts 8:14-17': ['Acts 8:14-17'],
    'Acts 10:34-48': ['Acts 10:34-48'],
    'Acts 13:1-4': ['Acts 13:1-4'],
    'Acts 19:1-8': ['Acts 19:1-8'],
    '1 John 2:20-29': ['1Jn 2:20-29'],
    'Luke 23:50-24:12': ['Lk 23:50-24:12'],
    'Mark 16:1-20': ['Mark 16:1-20'],
    'John 19:38-20:18': ['Jn 19:38-20:18'],
    'John 1:18-42': ['Jn 1:18-42'],
    'Matthew 26:6-13': ['Matt 26:6-13'],
    'John 3:22-4:2': ['Jn 3:22-4:2'],
    'Mark 14:3-9': ['Mark 14:3-9'],
    'John 3:1-21': ['Jn 3:1-21'],
    'Matthew 28:16-20': ['Matt 28:16-20'],
    'Sirach 2:1-9': [],  # Two assigned lessons; edition coordinates still held.
}


def projection():
    return s.project_special_contexts() if hasattr(s, 'project_special_contexts') else s.ROWS


def metadata(row):
    value = s.projection_metadata(row)
    assert value is not None
    return value


class SpecialContextProjection(unittest.TestCase):
    def test_same_baptism_appointment_has_one_current_witness_not_two(self):
        rows = projection()
        matches = [r for r in s.build_passage_index(rows) if r['service_family'] == 'baptism'
                   and r['matched_ref'] == 'Heb 1:8-12']
        self.assertEqual(len(matches), 1)

    def test_superseded_legacy_boundary_is_inactive_history(self):
        row = next(r for r in projection() if r['service_variant'] == 'sanctification_of_baptismal_water'
                   and r['raw_ref'] == '1 John 5:5-20')
        self.assertIn('"is_active": false', row['notes'])
        self.assertEqual(s.build_passage_index([row]), [])

    def test_unproven_printed_psalm_never_emits_mt_coordinate(self):
        row = next(r for r in projection() if r['raw_ref'] == 'Psalm 72:17,18,21')
        self.assertEqual(s.canonicalize_row_refs(row)['canonical_ref'], 'Ps 73:23-24; Ps 73:28')
        held = next(r for r in projection() if metadata(r).get('reasons') == ['canonical_psalm_coordinates_held'])
        self.assertEqual(s.canonicalize_row_refs(held)['canonical_ref'], '')
        self.assertEqual(s.build_passage_index([held]), [])


    def test_all_source_records_exact_once_order_and_real_context(self):
        oracle = json.loads((s.PROJECTION_DIR / 'records.json').read_text())
        actual = projection()[len(s.LEGACY_ROWS):]
        self.assertEqual(len(actual), len(oracle))
        self.assertEqual([(metadata(r)['capture_id'], metadata(r)['ordinal'], r['raw_ref']) for r in actual],
                         [(x['capture_id'], x['ordinal'], x['printed_ref']) for x in oracle])
        self.assertFalse(any(r['service_variant'].startswith('coptic_reader__') for r in actual))
        proof_path = s.CLASSIFICATION_DIR / 'source-classification-verdicts.json'
        self.assertEqual(hashlib.sha256(proof_path.read_bytes()).hexdigest(),
                         'de56efa0c2009b32359dbd2e1901a2848f04a3dc35dee10d2ad3302799f0bf19')
        proofs = json.loads(proof_path.read_text())
        approved = {(p['capture_id'], p['ordinal']): p for p in proofs}
        self.assertEqual(len(proofs), 37)
        self.assertEqual(len(approved), 37)
        self.assertEqual({p['printed_ref'] for p in proofs}, set(APPROVED_SOURCE_SPANS))
        self.assertEqual(sum(bool(APPROVED_SOURCE_SPANS[p['printed_ref']]) for p in proofs), 35)
        self.assertEqual(set(approved), {(x['capture_id'], x['ordinal']) for x in oracle
                         if x['reading_type'] == 'unclassified'
                         and (x['capture_id'], x['ordinal']) in approved})
        for r, x in zip(actual, oracle):
            self.assertEqual(metadata(r)['navigation'], x['navigation'])
            self.assertEqual(metadata(r)['raw_text_sha256'], x['raw_text_sha256'])
            proof = approved.get((x['capture_id'], x['ordinal']))
            if not x['selected'] or x['kind'] != 'assigned_scripture_reading':
                self.assertEqual(s.build_passage_index([r]), [])
            elif x['reading_type'] == 'unclassified':
                if proof is None:
                    self.assertEqual(s.build_passage_index([r]), [])
                else:
                    with self.subTest(capture=x['capture_id'], ordinal=x['ordinal']):
                        raw = s.PROJECTION_DIR / 'raw' / (x['capture_id'] + '.txt')
                        self.assertEqual(hashlib.sha256(raw.read_bytes()).hexdigest(), proof['sha256'])
                        for line in proof['evidence'] + proof['governing_rubric']:
                            self.assertEqual(raw.read_text().splitlines()[line['line'] - 1], line['text'])
                        self.assertEqual(x['printed_ref'], proof['printed_ref'])
                        self.assertEqual(x['navigation'], proof['navigation'])
                        self.assertEqual(x['section'], proof['section'])
                        self.assertEqual(r['reading_type'], proof['proposed_reading_type'])
                        self.assertEqual(metadata(r)['assignment_proof']['evidence'], proof['evidence'])
                        self.assertEqual(metadata(r)['assignment_proof']['governing_rubric'], proof['governing_rubric'])
                        expected = APPROVED_SOURCE_SPANS[proof['printed_ref']]
                        self.assertEqual(metadata(r)['is_active'], bool(expected))
                        self.assertEqual([v['matched_ref'] for v in s.build_passage_index([r])], expected)

    def test_legacy_literals_preserved_without_active_conflicts(self):
        frozen = json.loads((s.FIXTURE_DIR / 'legacy-generator-rows.json').read_text())
        actual = projection()[:len(frozen)]
        self.assertEqual(len(frozen), 178)
        for old, row in zip(frozen, actual):
            for key in old:
                self.assertEqual(row[key].split(s.PROJECTION_MARKER)[0] if key == 'notes' else row[key], old[key])
            if metadata(row)['projection_status'] in {'superseded', 'coalesced_attestation', 'held'}:
                self.assertEqual(s.build_passage_index([row]), [])

    def test_crowning_prostration_and_three_liturgies_keep_source_order(self):
        rows = projection()
        for variant, refs in {
            'holy_matrimony_main': ['Ephesians 5:22-6:3', 'Psalms 19:5-6;128:3-4', 'Matthew 19:1-6'],
            'first_prostration': ['Deuteronomy 5:22-6:3', '1 Corinthians 12:28-13:12', 'Psalms 97:7, 8, 1', 'John 17:1-26'],
            'second_prostration': ['Deuteronomy 6:17-25', '1 Corinthians 13:13-14:17', 'Psalms 115:12-13', 'Luke 24:36-53'],
            'third_prostration': ['Deuteronomy 16:1-18', '1 Corinthians 14:18-40', 'Psalms 66:4;72:11', 'John 4:1-24'],
        }.items():
            source = [r for r in rows if r['service_variant'] == variant and metadata(r).get('selected')
                      and metadata(r).get('kind') == 'assigned_scripture_reading']
            self.assertEqual([r['raw_ref'] for r in source], refs)
            if 'prostration' in variant:
                self.assertTrue(all('June 20, 2027' in metadata(r)['context']['text'] for r in source))
        chrism = [r for r in rows if r['service_variant'] == 'consecrations_oil_pre_sanctified_chrism']
        self.assertEqual({r['section'].split('_liturgy_')[0] for r in chrism}, {'first', 'second', 'third'})
        timothy = next(r for r in chrism if r['raw_ref'] == '1 Timothy 2:11-3:7')
        self.assertEqual(timothy['section'], 'third_liturgy_liturgy_of_the_word')
        self.assertEqual(timothy['reading_type'], 'pauline')
        self.assertIn('1Tim 2:11-3:7', [r['matched_ref'] for r in s.build_passage_index([timothy])])

    def test_theophany_full_january_19_capture_replaces_old_attestation(self):
        source = [r for r in projection() if metadata(r).get('navigation') == ['Special', 'Lakkan', 'Theophany']
                  and metadata(r).get('selected')]
        self.assertEqual(sum(r['raw_ref'] == '1 Corinthians 10:1-13' for r in source), 1)
        self.assertTrue(all('Tuesday, January 19, 2027' in metadata(r)['context']['text'] for r in source))
        self.assertEqual(len({metadata(r)['capture_id'] for r in source}), 1)
        self.assertEqual(sum(r['matched_ref'] == '1Cor 10:1-13' and r['service_variant'] == 'epiphany_laqan'
                             for r in s.build_passage_index(projection())), 1)

    def test_all_52_confirmations_are_context_attestations_not_extra_occurrences(self):
        ledger = json.loads((s.PROJECTION_DIR / 'legacy-exact-attestations.json').read_text())
        self.assertEqual(len(ledger), 52)
        rows = projection()
        for evidence in ledger:
            with self.subTest(navigation=evidence['navigation'], reference=evidence['printed_ref']):
                history = [r for r in rows[:len(s.LEGACY_ROWS)]
                           if [r['service_family'], r['service_variant']] == evidence['legacy_target_context']
                           and r['raw_ref'] in evidence['legacy_exact_raw_refs']]
                self.assertEqual(len(history), 1)
                self.assertEqual(metadata(history[0])['projection_status'], 'coalesced_attestation')
                self.assertEqual(s.build_passage_index(history), [])
                source = [r for r in rows[len(s.LEGACY_ROWS):]
                          if metadata(r)['navigation'] == evidence['navigation']
                          and metadata(r)['selected'] and r['raw_ref'] == evidence['printed_ref']]
                self.assertEqual(len(source), 1)
                self.assertEqual(metadata(source[0])['legacy_attestations'], [history[0] | {'notes': history[0]['notes'].split(s.PROJECTION_MARKER)[0]}])

    def test_parent_removal_state_never_reactivates_raw_or_projected_input(self):
        current = next(r for r in projection() if metadata(r)['is_active'])
        for field, value in [('active', False), ('state', 'superseded'), ('status', 'removed'),
                             ('include_in_current_index', False), ('removal_effective_version', 'v1')]:
            for projected in (False, True):
                row = copy.deepcopy(current if projected else s.LEGACY_ROWS[0])
                row[field] = value
                with self.subTest(field=field, projected=projected):
                    self.assertEqual(s.build_passage_index([row]), [])
                    self.assertEqual(s.canonicalize_row_refs(row)['canonical_ref'], '')
                    self.assertEqual(s.canonicalize_row_refs(row)['raw_ref'], row['raw_ref'])
                    self.assertEqual(s.canonicalize_row_refs(row)[field], value)
        for row in projection():
            meta = metadata(row)
            self.assertEqual(s.is_current_source_row(meta), meta['is_active'])
            if not meta['is_active']:
                self.assertEqual(meta['status'], 'removed')
                self.assertFalse(meta['active'])
                self.assertFalse(meta['include_in_current_index'])

    def test_projection_mutations_fail_closed(self):
        original = projection()
        for mutation in ['omit', 'reorder', 'duplicate', 'context', 'active', 'canonical', 'raw']:
            rows = copy.deepcopy(original)
            i = len(s.LEGACY_ROWS)
            if mutation == 'omit': rows.pop(i)
            elif mutation == 'reorder': rows[i], rows[i+1] = rows[i+1], rows[i]
            elif mutation == 'duplicate': rows.append(copy.deepcopy(rows[i]))
            elif mutation == 'raw': rows[i]['raw_ref'] = 'John 3:16'
            else:
                m = metadata(rows[i])
                if mutation == 'context': m['navigation'] = ['Special', 'Other']
                elif mutation == 'active': m['is_active'] = not m['is_active']
                else: m['canonical_ref'] = 'Ps 26:1'
                rows[i]['notes'] = rows[i]['notes'].split(s.PROJECTION_MARKER)[0] + s.PROJECTION_MARKER + json.dumps(m)
            with self.subTest(mutation=mutation), self.assertRaises(RuntimeError):
                s.validate_projection_rows(rows)

    def test_projection_source_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / 'fixture'
            shutil.copytree(s.PROJECTION_DIR, fixture)
            target = fixture / 'records.json'
            target.write_bytes(target.read_bytes() + b' ')
            with self.assertRaisesRegex(RuntimeError, 'source drift'):
                s.load_projection_fixture(fixture)

    def test_real_cli_fresh_home_only_owned_outputs_and_round_trip(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / 'nonexistent_home'
            out = root / 'data'
            result = subprocess.run([sys.executable, s.__file__], cwd=root, env=dict(os.environ,
                HOME=str(home), LECTIONARY_DISABLE_VAULT_PUBLISH='1', LECTIONARY_SPECIAL_OUTPUT_DIR=str(out)),
                capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(home.exists())
            curated = [json.loads(l) for l in (out / 'special_service_readings_curated.jsonl').read_text().splitlines()]
            index = [json.loads(l) for l in (out / 'special_service_passage_index.jsonl').read_text().splitlines()]
            self.assertEqual(curated, [s.canonicalize_row_refs(r) for r in projection()])
            self.assertEqual(index, s.build_passage_index(projection()))
            with (out / 'special_service_readings_curated.csv').open() as handle:
                self.assertEqual(list(csv.DictReader(handle)), curated)
            self.assertEqual(json.loads(result.stdout), {'curated_rows': len(curated), 'passage_rows': len(index)})


if __name__ == '__main__':
    unittest.main()
