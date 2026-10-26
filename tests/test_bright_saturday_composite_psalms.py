"""Bright Saturday shorthand keeps all explicit Psalm coordinates, unchanged."""
import unittest

import build_lectionary_crosswalk as crosswalk
from passage_normalization import extract_text_ref_tokens


class BrightSaturdayCompositePsalms(unittest.TestCase):
    def expand(self, reference):
        fn = getattr(crosswalk, 'expand_bright_psalm_shorthand', None)
        self.assertIsNotNone(fn, 'Omitted-book Psalm shorthand is not expanded')
        return fn(reference)

    def test_complete_matins_composite_preserves_all_three_psalms_and_gospel(self):
        raw = 'Ps. 88:4-5; 44:23-26; 126:2-3 + Matt. 27:62-66'
        self.assertEqual(extract_text_ref_tokens(self.expand(raw)),
                         ['Ps 88:4-5', 'Ps 44:23-26', 'Ps 126:2-3', 'Matt 27:62-66'])

    def test_sixth_hour_composite_keeps_second_psalm(self):
        raw = 'Ps. 130:1; 142:7 + Matt. 5:3-12'
        self.assertEqual(extract_text_ref_tokens(self.expand(raw)),
                         ['Ps 130:1', 'Ps 142:7', 'Matt 5:3-12'])

    def test_only_psalm_prefix_before_plus_is_in_scope(self):
        for raw in ['Matt. 5:3-12; 6:1-4', 'Isaiah 50:10; 51:1-8', 'Ps 151',
                    'Psalm 3:1 + Matt 5:1; 6:1']:
            self.assertEqual(self.expand(raw), raw)


if __name__ == '__main__':
    unittest.main()
