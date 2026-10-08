"""Preserve verse boundaries on literal Reader pre-colon whitespace."""
import unittest

from passage_normalization import extract_text_ref_tokens, parse_passage


class PreColonReferenceSpacing(unittest.TestCase):
    def test_reader_psalm_ranges_do_not_widen_to_whole_chapters(self):
        for raw, expected in [
            ('Psalms 29 :10-11', 'Ps 29:10-11'),
            ('Psalms 16 :1-2', 'Ps 16:1-2'),
            ('Psalms 29\u00a0:10\u201311', 'Ps 29:10-11'),
        ]:
            with self.subTest(raw=raw):
                self.assertEqual(extract_text_ref_tokens(raw), [expected])
                parsed = parse_passage(extract_text_ref_tokens(raw)[0])
                source_parsed = parse_passage(raw)
                assert parsed is not None and source_parsed is not None
                self.assertIsNotNone(parsed.parts[0].verse_start)
                self.assertEqual(parsed.canonical, source_parsed.canonical)

    def test_numbered_and_cross_chapter_books_keep_boundaries(self):
        for raw, expected in [
            ('1 Timothy 2 :11-3:7', '1Tim 2:11-3:7'),
            ('Matthew 23 :13-36', 'Matt 23:13-36'),
            ('Exodus 4 :19-6:13', 'Exod 4:19-6:13'),
        ]:
            with self.subTest(raw=raw):
                self.assertEqual(extract_text_ref_tokens(raw), [expected])

    def test_multiple_references_and_chapter_only_legacy_behavior(self):
        self.assertEqual(
            extract_text_ref_tokens('Psalms 29 :10-11; Matthew 23 :13-36'),
            ['Ps 29:10-11', 'Matt 23:13-36'],
        )
        for raw, expected in [('Psalms 29', 'Ps 29'),
                              ('Psalms 29:10-11', 'Ps 29:10-11'),
                              ('John 3:16', 'Jn 3:16')]:
            with self.subTest(raw=raw):
                self.assertEqual(extract_text_ref_tokens(raw), [expected])


if __name__ == '__main__':
    unittest.main()
