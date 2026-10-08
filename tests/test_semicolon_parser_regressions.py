"""Whole-expression semicolon validation without altering legacy single refs."""
import unittest

from passage_normalization import normalize_numeric_ref, parse_passage, passage_matches
import build_lectionary_reference as reference


class SemicolonParserRegressions(unittest.TestCase):
    def test_malformed_component_rejects_in_every_position(self):
        invalid = ['Isaiah 2:', 'Isaiah 2:,', 'Isaiah 2:2,',
                   'Isaiah 2:2,,3', 'Isaiah 2:,2', 'Isaiah 2:2-1',
                   'Isaiah 2:2-1:3', 'Isaiah 2:3-2:2', '', 'nonsense']
        for bad in invalid:
            for text in [f'Isaiah 1:19; {bad}', f'{bad}; Isaiah 1:19',
                         f'Isaiah 1:19; {bad}; Isaiah 3:1']:
                with self.subTest(text=text):
                    self.assertIsNone(parse_passage(text))
                    self.assertFalse(passage_matches('Isaiah 1:19', text))
                    self.assertFalse(reference.passage_matches('Isaiah 1:19', text))

    def test_numeric_continuations_reject_malformed_components(self):
        for bad in ['2:', '2:,', '2:2,', '2:2,,3', '2:,2',
                    '2:2-1', '2:2-1:3', '2:3-2:2', '0:2', '2:0']:
            with self.subTest(component=bad):
                text = f'Isaiah 1:19; {bad}'
                self.assertIsNone(parse_passage(text))
                self.assertFalse(reference.passage_matches('Isaiah 1:19', text))

    def test_same_book_order_and_gaps_survive(self):
        for text in ['Isaiah 2:3; 1:19; Isaiah 2:2',
                     'Isa 2:3; 1:19; Isaiah 2:2',
                     'Isaiah 2 : 3 ; 1 : 19 ; Isa 2 : 2']:
            with self.subTest(text=text):
                parsed = parse_passage(text)
                self.assertIsNotNone(parsed)
                assert parsed is not None
                self.assertEqual([(p.chapter_start, p.verse_start) for p in parsed.parts],
                                 [(2, 3), (1, 19), (2, 2)])
                for query, expected in [('Isaiah 2:1', False), ('Isaiah 2:2', True),
                                        ('Isaiah 2:3', True), ('Isaiah 1:19', True)]:
                    self.assertIs(reference.passage_matches(query, text), expected)

    def test_unicode_chained_and_numbered_book_controls(self):
        controls = [('Mark 9:47–50; Mk 9:43; 9:45', 'Mark 9:49'),
                    ('Mark 9:47—50; Mark 9:43; 9:45', 'Mark 9:45'),
                    ('Genesis 1:1-2:1-3; Gen 3:1', 'Genesis 2:3'),
                    ('Isaiah 55:1-13-56:1; 57:2', 'Isaiah 56:1'),
                    ('1 Timothy 1:1; 1 TimOTHY 2:1', '1 Timothy 2:1'),
                    ('Psalms 54:1; 26:11', 'Psalm 26:11')]
        for text, query in controls:
            with self.subTest(text=text):
                self.assertIsNotNone(parse_passage(text))
                self.assertTrue(reference.passage_matches(query, text))
        self.assertFalse(reference.passage_matches('Mark 9:44', controls[0][0]))
        self.assertFalse(reference.passage_matches('Mark 9:46', controls[0][0]))

    def test_numeric_normalization_keeps_same_book_semicolons(self):
        text = normalize_numeric_ref('23.1:19@23.2:2', {23: 'Isaiah'})
        self.assertEqual(text, 'Isa 1:19; Isa 2:2')
        self.assertTrue(reference.passage_matches('Isaiah 2:2', text))
        self.assertFalse(reference.passage_matches('Isaiah 2:1', text))

    def test_cross_book_expressions_reject(self):
        for text in ['Isaiah 1:19; Mark 9:45', 'Isaiah 1:19; John 2:1',
                     '1 Timothy 1:1; 2 Timothy 1:1']:
            with self.subTest(text=text):
                self.assertIsNone(parse_passage(text))
                self.assertFalse(reference.passage_matches('Isaiah 1:19', text))

    def test_duplicate_colon_first_rejects_whole_expression(self):
        self.assertIsNone(parse_passage('Isaiah 2:2:3; Isaiah 1:19'))

    def test_duplicate_colon_middle_rejects_whole_expression(self):
        self.assertIsNone(parse_passage('Isaiah 1:19; Isaiah 2:2:3; Isaiah 3:1'))

    def test_duplicate_colon_last_rejects_whole_expression(self):
        self.assertFalse(passage_matches('Isaiah 1:19', 'Isaiah 1:19; Isaiah 2:2:3'))

    def test_generated_component_grammar_and_lexical_noise(self):
        # Independent construction, not a regex copied from the production gate.
        import random
        rng = random.Random(10910)
        for _ in range(40):
            c, v = rng.randint(2, 20), rng.randint(2, 20)
            forms = [(f'{c}:{v}', [(c, v, c, v)]),
                     (f'{c}:{v}-{v+2}', [(c, v, c, v+2)]),
                     (f'{c}:{v}-{c+1}:3', [(c, v, c+1, 3)]),
                     (f'{c}:{v}-{c+1}:1-3', [(c, v, c+1, 3)]),
                     (f'{c}:{v}-{v+2}-{c+1}:3', [(c, v, c+1, 3)]),
                     (f'{c}:{v},{c+1}:2-4,7', [(c,v,c,v),(c+1,2,c+1,4),(c+1,7,c+1,7)]),
                     (str(c), [(c,None,c,None)])]
            for body, expected in forms:
                for label in ['Isaiah ', 'Isa.', 'ISA\u00a0']:
                    text = f'{label}{body}; Isaiah 1:19'
                    with self.subTest(text=text):
                        parsed = parse_passage(text)
                        self.assertIsNotNone(parsed)
                        assert parsed is not None
                        self.assertEqual([(p.chapter_start,p.verse_start,p.chapter_end,p.verse_end)
                                          for p in parsed.parts], expected+[(1,19,1,19)])
            for noise in ['x', ':3', '/', '+', '.', '@', '\u200b']:
                # Noise after a complete chapter/verse atom must not be consumed.
                bad = f'Isaiah {c}:{v}{noise}'
                for text in [f'{bad}; Isaiah 1:19', f'Isaiah 1:19; {bad}',
                             f'Isaiah 1:19; {bad}; Isaiah 3:1']:
                    with self.subTest(text=text):
                        self.assertIsNone(parse_passage(text))
                        self.assertFalse(passage_matches('Isaiah 1:19', text))
                        self.assertFalse(passage_matches(text, 'Isaiah 1:19'))

    def test_generated_invalid_numeric_productions(self):
        for body in ['2:2:3', '2:2:3-4', '2:2:3-4:5', '2:2:3,4',
                     '2:2-3:0-4', '2:2-3:5-4', '2:2-0-3:4',
                     '2:5-4-3:2', '2:2-3:1-4-5', '2:2-3:1:4',
                     '2:2,3:4:5', '2:2,3:4:5-6', '2:2,-3', '2:2,3:']:
            for text in [f'Isaiah {body}; Isaiah 1:19', f'Isaiah 1:19; {body}',
                         f'Isaiah 1:19; Isaiah {body}; Isaiah 3:1']:
                with self.subTest(text=text):
                    self.assertIsNone(parse_passage(text))
                    self.assertFalse(passage_matches('Isaiah 1:19', text))
                    self.assertFalse(passage_matches(text, 'Isaiah 1:19'))

    def test_single_component_legacy_behavior_is_unchanged(self):
        for text in ['Isaiah 2:', 'Isaiah 2:,', 'Isaiah 2:2,',
                     'Isaiah 2:2,,3', 'Isaiah 2:2-1', 'Isaiah 2:2-1:3']:
            with self.subTest(text=text):
                self.assertIsNotNone(parse_passage(text))
        self.assertIsNotNone(parse_passage('Isaiah 999:999'))


if __name__ == '__main__':
    unittest.main()
