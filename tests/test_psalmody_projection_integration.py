"""Source-qualified Psalmody must survive the actual design projection."""
import copy
import json
import unittest
from unittest.mock import patch

import build_design_deliverables as design
import psalmody_source_supplements as psalmody


class PsalmodyProjectionIntegration(unittest.TestCase):
    def test_projection_preserves_twelve_scoped_source_chapters(self):
        raw = psalmody.load_psalmody_source_rows()
        projected, identities = design.build_reverse_presentation(raw)
        self.assertEqual(len(projected), 12)
        self.assertEqual(len(identities), 4)
        for source, row in zip(raw, projected):
            q = psalmody.qualify_psalmody_row(source)
            self.assertEqual(row['canonical_mt_ref'], '')
            self.assertEqual(row['canonical_lxx_ref'], 'Ps ' + str(q['chapter']))
            self.assertEqual(row['current_status'], 'current_confirmed_coptic_reader')
            self.assertEqual(row['source_key'], 'coptic_reader_qualified_psalmody')
            self.assertIn('lines ', row['source_locator'])
            self.assertIn(q['full_capture_sha256'], row['source_locator'])
            self.assertEqual(json.loads(row['provenance'])['handle'], q['handle'])
        # This deliberately tests a bounded source subset. Full-build acceptance
        # still requires the independent complete reverse-membership ledger.
        expected_keys = {(r['liturgical_place'], r['service_section'], '', r['reading_slot'],
                          psalmody.psalmody_identity_for(r)['identity_key']) for r in raw}
        def bounded_ledger(rows):
            self.assertEqual({design.occasion_index_key(r) for r in rows}, expected_keys)
            self.assertEqual(len(rows), len(expected_keys))
        with patch.object(design, 'verify_reverse_index_contract', side_effect=bounded_ledger):
            reverse, disagreements = design.build_reverse_lectionary_index(
                projected, transport_mode='presentation')
        self.assertEqual(len(reverse), 12)
        self.assertEqual(disagreements, [])
        for row in reverse:
            self.assertEqual(row['canonical_mt_ref'], '')
            disclosure, = json.loads(row['source_disclosure'])
            self.assertTrue(disclosure['source_locator'])
            self.assertTrue(json.loads(row['provenance'])['body_literal'])
        for occasion in ('Church Consecration (Part 1)', 'Preparation of the Holy Myron', 'Pentecost Prostration Praises'):
            hoos = sorted((r for r in reverse if r['occasion'] == occasion and r['slot'] == 'FourthHoos'), key=lambda r: r['slot_order'])
            self.assertEqual([r['canonical_lxx_ref'] for r in hoos], ['Ps 148', 'Ps 149', 'Ps 150'])
        bright, = [r for r in reverse if r['source_family'] == 'bright_saturday']
        self.assertEqual((bright['occasion'], bright['service_section'], bright['canonical_lxx_ref']),
                         ('Bright Saturday', 'Midnight Praises', 'Ps 151'))
        self.assertNotIn('FourthHoos', bright['slot'])
        self.assertGreater(bright['slot_order'], 0)

    def test_raw_qualification_is_not_a_family_name_bypass(self):
        original = psalmody.load_psalmody_source_rows()[0]
        for field, value in [('source_family', 'special_service'), ('passage', 'Ps 152'),
                             ('service_section', 'Distribution'), ('source_order', '1')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                design.build_reverse_presentation([dict(original, **{field: value})])
        source = copy.deepcopy(original)
        source['active'] = False
        with self.assertRaises(ValueError):
            design.build_reverse_presentation([source])


if __name__ == '__main__':
    unittest.main()
