"""New source review overlay: assignment is not coordinate/completeness approval."""
import copy
import json
import unittest
import hashlib
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch
import build_special_service_reference as s

FIXTURE = Path(s.__file__).parent / 'sources/coptic-reader/special-classification-integration-2026-10-07'
CLASSIFICATIONS = json.loads((FIXTURE / 'source-classification-verdicts.json').read_text())
STAGES = json.loads((FIXTURE / 'stage-join-verdicts.json').read_text())


def meta(row):
    value = s.projection_metadata(row)
    assert value is not None
    return value


def source(rows, proof):
    return next(r for r in rows[178:] if (meta(r)['capture_id'], meta(r)['ordinal']) ==
                (proof['capture_id'], proof['ordinal']))


class SpecialClassificationIntegration(unittest.TestCase):
    def test_all_37_assigned_blocks_have_exact_source_classification(self):
        rows = s.project_special_contexts()
        self.assertEqual(len(CLASSIFICATIONS), 37)
        for proof in CLASSIFICATIONS:
            with self.subTest(ref=proof['printed_ref'], capture=proof['capture_id']):
                row = source(rows, proof)
                self.assertEqual(row['reading_type'], proof['proposed_reading_type'])
                self.assertEqual(meta(row)['assignment_proof']['evidence'], proof['evidence'])
                self.assertNotIn('source_rubric_unclassified', meta(row)['reasons'])
                if row['raw_ref'].startswith('Sirach '):
                    self.assertFalse(meta(row)['is_active'])
                    self.assertEqual(s.build_passage_index([row]), [])
                else:
                    self.assertTrue(meta(row)['is_active'])
                    self.assertTrue(s.build_passage_index([row]))

    def test_35_proven_stage_joins_have_exact_inactive_history_and_single_attestation(self):
        rows = s.project_special_contexts()
        proven = [p for p in STAGES if p['verdict'] == 'proven_stage_assigned_reading']
        self.assertEqual(len(proven), 35)
        for p in proven:
            with self.subTest(row=p['legacy_row']):
                old = rows[p['legacy_row']]
                self.assertIn(meta(old)['projection_status'], ['coalesced_attestation', 'superseded'])
                self.assertEqual(s.build_passage_index([old]), [])
                target = source(rows, p['reader_evidence'][0])
                witnesses = meta(target)['legacy_attestations']
                self.assertEqual(witnesses.count(s.LEGACY_ROWS[p['legacy_row']]), 1)
                self.assertEqual(meta(old)['stage_join_proof']['legacy_row'], p['legacy_row'])

    def test_row144_is_explicit_reader_authority_book_conflict_not_rename(self):
        rows = s.project_special_contexts()
        old = rows[144]
        self.assertEqual(old['raw_ref'], 'Titus 2:11-15; Titus 3:1-7')
        self.assertEqual(meta(old)['projection_status'], 'superseded')
        self.assertEqual(meta(old)['conflict_type'], 'source_book_conflict')
        self.assertEqual(meta(old)['authoritative_printed_ref'], '1 Timothy 2:11-3:7')
        target = source(rows, next(p for p in STAGES if p['legacy_row'] == 144)['reader_evidence'][0])
        self.assertEqual([x['matched_ref'] for x in s.build_passage_index([target])], ['1Tim 2:11-3:7'])
        self.assertTrue(meta(target)['source_conflicts'])
        self.assertEqual(s.build_passage_index([old]), [])

    def test_prayer176_inactive_and126_unresolved_not_wrong_myron_join(self):
        rows = s.project_special_contexts()
        self.assertEqual(meta(rows[176])['kind'], 'prescribed_psalm_prayer')
        self.assertEqual(meta(rows[176])['projection_status'], 'prescribed_prayer')
        self.assertEqual(meta(rows[126])['projection_status'], 'held')
        self.assertIn('unresolved_reader_join', meta(rows[126])['reasons'])
        self.assertEqual(s.build_passage_index([rows[126], rows[176]]), [])
        self.assertFalse(any(s.LEGACY_ROWS[126] in meta(r).get('legacy_attestations', []) for r in rows[178:]))

    def test_cornerstone_aliases_and_altar_opening_and_late_gospels_remain_distinct(self):
        rows = s.project_special_contexts()
        cornerstone = [r for r in rows[178:] if meta(r)['navigation'] == ['Special', 'Consecrations', 'Cornerstone']]
        pauline = next(r for r in cornerstone if r['reading_type'] == 'pauline')
        self.assertEqual(len(meta(pauline)['legacy_attestations']), 2)
        self.assertEqual(sum(x['matched_ref'] == 'Heb 9:1-11' and x['service_family'] == 'cornerstone_prayer'
                             for x in s.build_passage_index(rows)), 1)
        altar = [r for r in rows[178:] if meta(r)['navigation'] == ['Special', 'Consecrations', 'Altar'] and r['reading_type'] == 'gospel']
        self.assertEqual([r['raw_ref'] for r in altar], ['Matthew 16:13-19', 'Luke 19:1-10'])
        self.assertFalse(meta(altar[0])['legacy_attestations'])
        self.assertIn(s.LEGACY_ROWS[177], meta(altar[1])['legacy_attestations'])

    def test_literal_preservation_and_psalm_holds_and_partial_contract(self):
        rows = s.project_special_contexts()
        self.assertEqual(len(rows), 178 + 478)
        for old, row in zip(s.LEGACY_ROWS, rows):
            self.assertEqual({k: row[k].split(s.PROJECTION_MARKER)[0] if k == 'notes' else row[k] for k in old}, old)
        reader = rows[178:]
        self.assertEqual(sum(meta(r)['reasons'] == ['canonical_psalm_coordinates_held'] for r in reader), 54)
        self.assertEqual(sum(meta(r)['reasons'] == ['legacy_psalm_coordinates_unqualified'] for r in rows[:178]), 17)
        self.assertFalse(s.load_classification_overlay()['manifest']['completeness_claimed'])
        self.assertFalse(s.load_classification_overlay()['manifest']['normalization_changes'])

    def test_parent_removal_and_metadata_allowlist_cannot_reactivate(self):
        records = s.load_projection_fixture()
        proof = CLASSIFICATIONS[0]
        i = next(i for i,r in enumerate(records) if (r['capture_id'], r['ordinal']) == (proof['capture_id'], proof['ordinal']))
        for state in [{'active': False}, {'status': 'removed'}, {'include_in_current_index': False}, {'state': 'superseded'}]:
            mutated = copy.deepcopy(records)
            mutated[i].update(state, injected_metadata='must_not_copy')
            with patch.object(s, 'load_projection_fixture', return_value=mutated):
                row = source(s.project_special_contexts(), proof)
            self.assertFalse(meta(row)['is_active'])
            self.assertEqual(s.build_passage_index([row]), [])
            self.assertNotIn('injected_metadata', meta(row))

    def test_count_contract_is_independent_evidence_preservation_not_generator_length(self):
        old = json.loads((s.FIXTURE_DIR / 'assigned-scripture-oracle.json').read_text())
        records = json.loads((s.PROJECTION_DIR / 'records.json').read_text())
        original = {(b['provenance']['captureId'], b['ordinalWithinDocument']) for b in old}
        new = {(r['capture_id'], r['ordinal']) for r in records}
        self.assertEqual(len(old), 403)
        self.assertEqual(len(original), 403)
        self.assertEqual(len(new), len(records))
        self.assertTrue(original.issubset(new))
        self.assertEqual(len(new - original), 75)
        self.assertEqual(178 + len(records), 656)
        for record in records:
            raw = (s.PROJECTION_DIR / 'raw' / (record['capture_id'] + '.txt')).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), record['raw_text_sha256'])
            text = raw.decode()
            self.assertEqual(text.splitlines()[record['line'] - 1], record['raw_heading'])
            self.assertTrue(text[record['offset']:].startswith(record['raw_heading']))

    def test_overlay_proof_file_corruption_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / 'fixture'
            shutil.copytree(FIXTURE, fixture)
            for name in ['manifest.json', 'source-classification-verdicts.json', 'stage-join-verdicts.json', 'independent-timothy-proof.json']:
                target = fixture / name
                original = target.read_bytes()
                target.write_bytes(original + b' ')
                with self.subTest(name=name), self.assertRaisesRegex(RuntimeError, 'source drift'):
                    s.load_classification_overlay(fixture)
                target.write_bytes(original)

    def test_all_projection_metadata_and_ordering_corruptions_rejected(self):
        original = s.project_special_contexts()
        for mutation in ['omit', 'reverse', 'double_join', 'wrong_rite', 'wrong_stage', 'kind', 'proof', 'removal', 'canonical']:
            rows = copy.deepcopy(original)
            target = source(rows, CLASSIFICATIONS[0])
            if mutation == 'omit': rows.remove(target)
            elif mutation == 'reverse': rows.reverse()
            else:
                m = meta(target)
                if mutation == 'double_join': m['legacy_attestations'].append(s.LEGACY_ROWS[143])
                elif mutation == 'wrong_rite': m['navigation'] = ['Special', 'Consecrations', 'Cornerstone']
                elif mutation == 'wrong_stage': target['section'] = 'third_liturgy_liturgy_of_the_word'
                elif mutation == 'kind': m['kind'] = 'prescribed_psalm_prayer'
                elif mutation == 'proof': m['assignment_proof']['evidence'][0]['text'] += 'drift'
                elif mutation == 'removal': m['is_active'] = False
                else: m['canonical_ref'] = 'Jn 3:16'
                target['notes'] = target['notes'].split(s.PROJECTION_MARKER)[0] + s.PROJECTION_MARKER + json.dumps(m)
            with self.subTest(mutation=mutation), self.assertRaises(RuntimeError):
                s.validate_projection_rows(rows)


if __name__ == '__main__':
    unittest.main()
