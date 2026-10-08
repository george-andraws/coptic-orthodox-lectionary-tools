"""The captured Jm abbreviation must survive the actual date parser/index path."""
import datetime as dt
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build_lectionary_reference as core
from passage_normalization import extract_text_ref_tokens, normalize_text_query, parse_passage

FIXTURE = ROOT / 'sources/coptic-reader/annual-reconciled-2026-10-07'
# Independent primary-source coordinates, not values derived from tokenization.
CASES = {26: ('Jm 1:1-18', 'James 1:1-18'),
         54: ('Jm 5:9 - 20', 'James 5:9-20'),
         57: ('Jm 1:12-21', 'James 1:12-21'),
         59: ('Jm 1:1-12', 'James 1:1-12')}


class JamesSourceToken(unittest.TestCase):
    def test_four_captured_abbreviations_extract_without_losing_boundaries(self):
        for raw, expected in CASES.values():
            with self.subTest(raw=raw):
                self.assertEqual(extract_text_ref_tokens(raw), [expected])

    def test_query_alias_round_trip_and_existing_spelling_preservation(self):
        for prefix in ('Jm', 'jm', 'JM', 'Jm.', 'James', 'Jas'):
            with self.subTest(prefix=prefix):
                self.assertEqual(normalize_text_query(prefix + ' 1:1-18'), 'James 1:1-18')
                parsed = parse_passage(prefix + ' 1:1-18')
                assert parsed is not None, prefix
                self.assertEqual(parsed.canonical, 'James 1:1-18')

    def test_actual_html_catholic_rows_are_indexed_once_and_raw_is_preserved(self):
        oracle = json.loads((FIXTURE / 'oracle.json').read_text())
        for ident, (raw, expected) in CASES.items():
            with self.subTest(context=ident):
                capture = next(r for r in oracle if r['key']['Id'] == ident)
                evidence = next(r for r in capture['source_approved_nonPsalm'] if r['slot'] == 'liturgy_catholic')
                self.assertEqual(evidence['source_ref'], expected)
                _, rows = core.parse_copticchurch_html(
                    (FIXTURE / 'date-source' / (capture['date'] + '.html')).read_text(),
                    dt.date.fromisoformat(capture['date']))
                catholic = [r for r in rows if r['service_section'] == 'Liturgy' and r['reading_type'] == 'Catholic Epistle']
                self.assertEqual(len(catholic), 1)
                self.assertEqual(catholic[0]['raw_ref'], raw)
                indexed = core.build_date_passage_index(catholic)
                self.assertEqual([r['matched_ref'] for r in indexed], [expected])
                self.assertEqual(catholic[0]['raw_ref'], raw)
                self.assertEqual(indexed[0]['service_section'], 'Liturgy')
                self.assertEqual(indexed[0]['reading_type'], 'Catholic Epistle')

    def test_other_catholic_books_and_empty_input_are_unchanged(self):
        for ref in ('1Pet 1:25-2:10', '2Pet 2:1-10', '1Jn 5:5-14', 'Jude 1:1-10'):
            with self.subTest(ref=ref):
                self.assertEqual(extract_text_ref_tokens(ref), [ref])
        self.assertEqual(extract_text_ref_tokens(''), [])
        self.assertEqual(extract_text_ref_tokens(None), [])


if __name__ == '__main__':
    unittest.main()
