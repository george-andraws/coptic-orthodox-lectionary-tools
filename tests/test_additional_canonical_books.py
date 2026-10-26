"""Chapter lookup must not silently lose source-backed standalone additions."""
import unittest

import build_bible_chapter_lectionary_index as chapters


class AdditionalCanonicalBooks(unittest.TestCase):
    def test_bright_saturday_standalone_additions_have_one_chapter(self):
        for reference, abbreviation in [('PrMan 1:1-15', 'PrMan'), ('Sus 1:1-64', 'Sus')]:
            with self.subTest(reference=reference):
                self.assertIn(abbreviation, chapters.BOOK_BY_ABBREV)
                self.assertEqual(chapters.chapter_keys_for_passage(reference), [(abbreviation, 1)])
                self.assertEqual(chapters.chapter_keys_for_passage(f'{abbreviation} 2:1'), [])

    def test_psalm151_is_searchable_without_adding_a_fictitious_psalm152(self):
        self.assertEqual(chapters.chapter_keys_for_passage('Ps 151:1-7'), [('Ps', 151)])
        self.assertEqual(chapters.chapter_keys_for_passage('Ps 152:1'), [])
        self.assertEqual(chapters.chapter_keys_for_passage('Ps 150:1-6'), [('Ps', 150)])


if __name__ == '__main__':
    unittest.main()
