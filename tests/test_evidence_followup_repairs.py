"""Source-owned evidence follow-up controls; no generators or network calls."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import evidence_followup_repairs as e

ROOT = Path(__file__).resolve().parents[1]
LEDGER = json.loads((ROOT / 'docs/reviews/timothy-luke-evidence-1.3.8/baseline-targets.json').read_text())


class EvidenceFollowupTests(unittest.TestCase):
    def targets(self):
        return copy.deepcopy([t['baseline'] for t in LEDGER['targets']])

    def test_exact_45_targets_keep_lifecycle_raw_coordinates_and_sources(self):
        rows = self.targets()
        before = copy.deepcopy(rows)
        result, counts = e.repair_evidence_rows(rows)
        self.assertEqual(rows, before)
        self.assertEqual(counts, {'targets': 45, 'captured': 34, 'unverified_service_book': 11,
                                  'authority_tier_changed': 34, 'same_service_marked': 1})
        self.assertEqual(len(result), 45)
        for old, new in zip(before, result):
            for field in ('current_status', 'removed_marker', 'source_title', 'source_locator',
                          'source_edition', 'calendar_keys', 'spans_json', 'identity_key'):
                self.assertEqual(new[field], old[field], field)
            self.assertEqual(new['authority_tier'], 'current_authority' if new['evidence_status'] == 'retained_reader_capture' else old['authority_tier'])
            self.assertEqual(json.loads(new['source_disclosure'])[0]['source_locator'],
                             json.loads(old['source_disclosure'])[0]['source_locator'])
        e.validate_evidence_rows(result)

    def test_complete_membership_rejects_missing_and_same_total_substitution(self):
        rows, _ = e.repair_evidence_rows(self.targets())
        e.validate_evidence_rows(rows, require_all_targets=True)
        for malformed in (rows[:-1], rows[:-1] + [rows[0]]):
            with self.assertRaisesRegex(ValueError, 'evidence target membership'):
                e.validate_evidence_rows(malformed, require_all_targets=True)

    def test_idempotent_without_collapsing_combined_contexts(self):
        first, _ = e.repair_evidence_rows(self.targets())
        second, counts = e.repair_evidence_rows(first)
        self.assertEqual(first, second)
        self.assertEqual(counts['authority_tier_changed'], 0)
        monk = next(r for r in second if r['calendar_keys'] == 'funeral_monk_priests || funeral_monks')
        self.assertEqual(len(json.loads(monk['evidence_json'])['captures']), 2)

    def test_inactive_witnesses_are_not_promoted_or_activated(self):
        original = self.targets()[0]
        for field, value in [('active', False), ('include_in_current_index', False),
                             ('removed_marker', 'held'), ('current_status', 'historical_witness'),
                             ('active', 1), ('include_in_current_index', 'true')]:
            with self.subTest(field=field, value=value):
                row = {**original, field: value}
                result, counts = e.repair_evidence_rows([row])
                self.assertEqual(result[0]['authority_tier'], row['authority_tier'])
                self.assertEqual(result[0][field], value)
                self.assertEqual(counts['authority_tier_changed'], 0)

    def test_wrong_context_cannot_borrow_capture(self):
        rows, _ = e.repair_evidence_rows([self.targets()[0]])
        for field, value in [('source_family', 'home_blessing'), ('source_kind', 'agpeya'),
                             ('calendar_keys', 'different_rite'), ('service_section', 'vespers'),
                             ('slot', 'different_slot'), ('canonical_mt_ref', 'Lk 19:1-9'),
                             ('current_status', 'historical_witness'), ('active', False)]:
            altered = copy.deepcopy(rows)
            altered[0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'evidence'):
                e.validate_evidence_rows(altered)

    def test_same_reference_in_uncaptured_context_stays_untouched(self):
        row = self.targets()[0]
        row['calendar_keys'] = 'unknown_service'
        result, counts = e.repair_evidence_rows([row])
        self.assertEqual(result, [row])
        self.assertEqual(counts['captured'], 0)

    def test_real_caller_fails_closed_on_document_hash_tamper(self):
        target = self.targets()[0]
        entry = LEDGER['targets'][0]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = [e.LEDGER_RELATIVE, e.SPECIAL_RELATIVE / 'manifest.json',
                     e.SPECIAL_RELATIVE / 'records.json']
            paths += [e.SPECIAL_RELATIVE / 'raw' / (r['capture_id'] + '.txt') for r in entry['records']]
            for relative in paths:
                dest = root / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, dest)
            valid, _ = e.repair_evidence_rows([target], root=root)
            self.assertEqual(valid[0]['authority_tier'], 'current_authority')
            doc = root / paths[-1]
            doc.write_bytes(doc.read_bytes() + b'changed')
            with self.assertRaisesRegex(ValueError, 'evidence.*hash'):
                e.repair_evidence_rows([target], root=root)

    def test_disclosure_and_evidence_tamper_rejected_at_validator(self):
        rows, _ = e.repair_evidence_rows([self.targets()[0]])
        for field in ('evidence_json', 'source_disclosure'):
            altered = copy.deepcopy(rows)
            data = json.loads(altered[0][field])
            if field == 'evidence_json':
                data['captures'][0]['navigation'] = ['Special', 'Wrong']
            else:
                data[0]['evidence_followup']['captures'][0]['sha256'] = '0' * 64
            altered[0][field] = json.dumps(data)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'evidence'):
                e.validate_evidence_rows(altered)

    def test_preserve_other_disclosure_additions_and_require_original_source(self):
        row = self.targets()[0]
        disclosures = json.loads(row['source_disclosure'])
        disclosures[0]['independent_metadata'] = 'retained sibling addition'
        row['source_disclosure'] = json.dumps(disclosures)
        fixed, _ = e.repair_evidence_rows([row])
        self.assertEqual(json.loads(fixed[0]['source_disclosure'])[0]['independent_metadata'], 'retained sibling addition')
        disclosures[0]['source_locator'] = 'another service'
        row['source_disclosure'] = json.dumps(disclosures)
        with self.assertRaisesRegex(ValueError, 'evidence original source disclosure'):
            e.repair_evidence_rows([row])

    def test_missing_evidence_rejected_in_serialized_readback(self):
        with self.assertRaisesRegex(ValueError, 'evidence metadata missing'):
            e.validate_evidence_rows(self.targets())

    def test_lakkan_same_service_is_documented_not_deleted(self):
        row = next(r for r in self.targets() if r['calendar_keys'] == 'lakkan_covenant_thursday')
        rows, _ = e.repair_evidence_rows([row])
        proof = json.loads(rows[0]['evidence_json'])['same_service']
        self.assertEqual(proof['service_section'], 'Liturgy of Blessing of the Water')
        self.assertEqual(proof['matching_ref'], '1Tim 4:9-5:10')
        self.assertFalse(proof['entire_tables_equivalent'])
        self.assertEqual(rows[0]['current_status'], row['current_status'])


class PsalmFollowupTests(unittest.TestCase):
    def mt(self, ref='Ps 51:7', lxx='Ps 50:7'):
        # Explicit MT source coordinates, not coordinates inferred from display text.
        ch, verse = map(int, ref.split()[1].split(':'))
        return {'identity_key': 'retained_id', 'canonical_mt_ref': ref, 'canonical_lxx_ref': lxx,
                'display_ref': f'{ref} (LXX {lxx})', 'source_kind': 'special_service',
                'current_status': 'current_public_or_local_reference',
                'spans_json': json.dumps([{'book': 'Ps', 'source_ref': ref,
                    'source_convention': 'mt_nkjv', 'canonical_mt_ref': ref,
                    'canonical_lxx_ref': lxx, 'chapter_start': ch, 'chapter_end': ch,
                    'verse_start': verse, 'verse_end': verse, 'confidence': 'medium',
                    'validation_basis': 'chapter_mapped_verse_offset_not_guessed'}])}

    def test_qualified_superscription_repair_and_coordinate_preservation(self):
        rows = [self.mt(), self.mt('Ps 51:10', 'Ps 50:10')]
        old = copy.deepcopy(rows)
        result, counts = e.repair_psalm_annotations(rows)
        self.assertEqual(counts['annotations_changed'], 2)
        self.assertEqual([r['canonical_lxx_ref'] for r in result], ['Ps 50:9', 'Ps 50:12'])
        self.assertEqual(rows, old)
        for before, after in zip(old, result):
            a, b = json.loads(before['spans_json'])[0], json.loads(after['spans_json'])[0]
            for key in ('chapter_start', 'chapter_end', 'verse_start', 'verse_end', 'source_ref', 'source_convention'):
                self.assertEqual(a[key], b[key])
            self.assertEqual(before['identity_key'], after['identity_key'])
        again, stats = e.repair_psalm_annotations(result)
        self.assertEqual(result, again)
        self.assertEqual(stats['annotations_changed'], 0)
        e.validate_psalm_annotations(result)

    def test_source_frame_and_held_alignment_are_not_treated_as_mt(self):
        for convention in ('lxx_liturgical_or_fixture_label', 'existing_numeric_source_coordinates_alignment_held', 'source_coordinates'):
            row = self.mt()
            spans = json.loads(row['spans_json'])
            spans[0]['source_convention'] = convention
            row['spans_json'] = json.dumps(spans)
            result, counts = e.repair_psalm_annotations([row])
            self.assertEqual(result, [row])
            self.assertEqual(counts['annotations_changed'], 0)
        held = self.mt()
        held.update(canonical_mt_ref='', canonical_lxx_ref='', spans_json='[]', current_status='pending_psalm_equivalence_unresolved')
        self.assertEqual(e.repair_psalm_annotations([held])[0], [held])

    def test_disagreement_without_content_qualification_holds_not_guesses(self):
        row = self.mt('Ps 52:7', 'Ps 51:99')
        result, stats = e.repair_psalm_annotations([row])
        self.assertEqual(result, [row])
        self.assertEqual(stats['unresolved_disagreements'], 1)
        self.assertEqual(stats['annotations_changed'], 0)

    def test_numeric_source_coordinates_cannot_override_claimed_mt_frame(self):
        row = self.mt()
        span = json.loads(row['spans_json'])[0]
        span['chapter_start'] = span['chapter_end'] = 50
        row['spans_json'] = json.dumps([span])
        self.assertEqual(e.repair_psalm_annotations([row])[0], [row])
        self.assertEqual(e.repair_psalm_annotations([row])[1]['frame_mismatch'], 1)

    def test_validator_detects_stale_annotation_without_global_one_to_one_rule(self):
        with self.assertRaisesRegex(ValueError, 'Psalm annotation'):
            e.validate_psalm_annotations([self.mt()])
        source = self.mt()
        span = json.loads(source['spans_json'])[0]
        span['source_convention'] = 'lxx_liturgical_or_fixture_label'
        source['spans_json'] = json.dumps([span])
        e.validate_psalm_annotations([source])


if __name__ == '__main__':
    unittest.main()
