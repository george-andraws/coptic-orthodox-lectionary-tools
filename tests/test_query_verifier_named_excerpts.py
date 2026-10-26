"""Named Covenant excerpts are disclosed, never fabricated chapter occurrences."""
import copy
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import covenant_thursday_source_supplements as covenant
import verify_lectionary_queries as verifier


class NamedExcerptVerification(unittest.TestCase):
    def sources(self):
        return [r for r in covenant.load_covenant_thursday_rows() if not r['normalized_ref']]

    def check(self, sources, chapters=()):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (root / 'reverse_lookup_crosswalk.csv').open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(sources[0]))
                writer.writeheader(); writer.writerows(sources)
            with (root / 'bible_chapter_lectionary_occurrences.csv').open('w', newline='') as handle:
                fields = list(dict.fromkeys([*sources[0], 'chapter', 'chapter_ref']))
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader(); writer.writerows(chapters)
            with patch.object(verifier, 'DATA', root):
                chapter = verifier.assert_chapter_occurrence_row_count()
                spans = verifier.assert_reverse_crosswalk_spans_valid()
            return chapter, spans

    def test_exact_qualified_excerpts_pass_without_numeric_occurrences(self):
        chapter, spans = self.check(self.sources())
        self.assertEqual(chapter['chapter_occurrence_rows'], 0)
        self.assertEqual(spans['qualified_unaddressable_rows'], 2)
        self.assertEqual(spans['parsed_rows'], 0)

    def test_named_excerpt_cannot_gain_a_whole_chapter_occurrence(self):
        rows = self.sources()
        false_chapter = dict(rows[0], book_abbrev='Exod', chapter='14', chapter_ref='Exod 14')
        with self.assertRaises(AssertionError):
            self.check(rows, [false_chapter])

    def test_source_or_context_forgery_does_not_receive_the_exception(self):
        for field, value in [('source_kind','copticchurch_date'), ('source_family','unqualified'),
                             ('service_section','Matins'), ('source_file','unqualified.txt'),
                             ('passage','Exodus from 14, 16')]:
            rows = copy.deepcopy(self.sources()); rows[0][field] = value
            with self.subTest(field=field), self.assertRaises((AssertionError, ValueError)):
                self.check(rows)

    def test_unrelated_unparsed_rows_still_fail(self):
        rows = self.sources()
        rows.append(dict(rows[0], source_kind='copticchurch_date', source_family='ordinary_date_resolved',
                         source_file='unqualified.txt', passage='unparsed nonsense'))
        with self.assertRaises(AssertionError):
            self.check(rows)


if __name__ == '__main__':
    unittest.main()
