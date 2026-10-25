"""Reader-backed Bright Saturday references must tokenize without false book hits."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_lectionary_crosswalk import public_special_day_title
from passage_normalization import extract_text_ref_tokens, parse_passage


class BrightSaturdayGapRefs(unittest.TestCase):
    def test_added_reader_refs_keep_verse_boundaries(self):
        cases = {
            'Susanna 1:1-64': ('Sus 1:1-64', 'Sus', (1, 1, 1, 64)),
            'Prayer of Manasseh 1:1-15': ('PrMan 1:1-15', 'PrMan', (1, 1, 1, 15)),
            'Pr Man 1:1-15': ('PrMan 1:1-15', 'PrMan', (1, 1, 1, 15)),
            'Daniel 3:91-97': ('Dan 3:91-97', 'Dan', (3, 91, 3, 97)),
            'Isaiah 55:2-13': ('Isa 55:2-13', 'Isa', (55, 2, 55, 13)),
            'Ephesians 4:1-5': ('Eph 4:1-5', 'Eph', (4, 1, 4, 5)),
        }
        for raw, (canonical, book, span) in cases.items():
            with self.subTest(raw=raw):
                tokens = extract_text_ref_tokens(raw)
                self.assertEqual(tokens, [canonical])
                parsed = parse_passage(tokens[0])
                if parsed is None:
                    self.fail(raw)
                self.assertEqual(parsed.book_abbrev, book)
                part = parsed.parts[0]
                self.assertEqual((part.chapter_start, part.verse_start, part.chapter_end, part.verse_end), span)

    def test_short_sus_alias_does_not_eat_jesus(self):
        self.assertEqual(extract_text_ref_tokens('Jesus 3:16'), [])
        self.assertEqual(extract_text_ref_tokens('Prayer of Manasseh 1-15'), [])

    def test_laqan_day_title_names_the_feast_and_keeps_other_families(self):
        self.assertEqual(
            public_special_day_title({'service_variant': 'epiphany_laqan', 'service_family': 'liturgy_of_the_waters'}),
            'Theophany Liturgy of the Waters',
        )
        self.assertNotIn('Epiphany', public_special_day_title({'service_variant': 'epiphany_laqan'}))
        self.assertEqual(
            public_special_day_title({'service_variant': 'lakkan_covenant_thursday', 'service_family': 'liturgy_of_the_waters'}),
            'Covenant Thursday Liturgy of the Waters',
        )
        self.assertEqual(
            public_special_day_title({'service_variant': 'apostles_feast_laqan', 'service_family': 'liturgy_of_the_waters'}),
            'Apostles Feast Liturgy of the Waters',
        )
        self.assertEqual(
            public_special_day_title({'service_variant': 'holy_matrimony_main', 'service_family': 'holy_matrimony'}),
            'holy_matrimony',
        )


if __name__ == '__main__':
    unittest.main()
