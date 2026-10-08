import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_design_deliverables as design


class HeldSundaySchema(unittest.TestCase):
    def test_schema_declares_held_coordinates_without_claiming_canonical_alignment(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(design, 'OUT', Path(directory)):
                schema = design.write_schema()
        vocabulary = schema['controlled_vocabularies']
        self.assertEqual(set(vocabulary['source_convention']), {
            'modern_english_reference', 'mt_nkjv', 'lxx_liturgical_or_fixture_label',
            'existing_numeric_source_coordinates_alignment_held',
        })
        self.assertIn('held', vocabulary['canonicalization_confidence'])
        self.assertNotIn('unverified_reader_coordinates_are_canonical', vocabulary['source_convention'])


if __name__ == '__main__':
    unittest.main()
