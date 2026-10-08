"""Ordered source components are fragments of one SPECIAL appointment."""
import copy
import unittest

import build_special_service_reference as special


class OrderedReaderComponentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = next(r for r in special.ROWS if r['raw_ref'] == 'Psalms 127:1; 122:1-2')

    def row(self, reference):
        row = copy.deepcopy(self.base)
        row['raw_ref'] = reference
        return row

    def test_source_order_and_complete_reference_on_each_fragment(self):
        row = self.row('Psalms 127:1; 122:1-2')
        indexed = special.build_passage_index([row])
        self.assertEqual([x['matched_ref'] for x in indexed], ['Ps 127:1', 'Ps 122:1-2'])
        self.assertEqual([x['canonical_ref'] for x in indexed], ['Ps 127:1; Ps 122:1-2'] * 2)
        self.assertTrue(all(x['raw_ref'] == row['raw_ref'] for x in indexed))
        self.assertEqual(row, self.row('Psalms 127:1; 122:1-2'))

    def test_repeated_component_retains_first_order_without_duplicate_fragment(self):
        indexed = special.build_passage_index([self.row('Psalms 127:1; 122:1-2; 127:1')])
        self.assertEqual([x['matched_ref'] for x in indexed], ['Ps 127:1', 'Ps 122:1-2'])

    def test_distinct_overlapping_components_and_gaps_are_not_collapsed(self):
        indexed = special.build_passage_index([self.row('Psalms 127:1-2; 127:2-3; 127:5')])
        self.assertEqual([x['matched_ref'] for x in indexed], ['Ps 127:1-2', 'Ps 127:2-3', 'Ps 127:5'])

    def test_malformed_same_book_expression_rejects_entire_appointment(self):
        for ref in ['Psalms 127:1; 122:', 'Psalms 127:1; 122:1:2',
                    'Psalms 127:1; 122:2-1', 'Psalms 127:1;; 122:1',
                    'Psalms 127:1; 122:1,']:
            with self.subTest(reference=ref), self.assertRaises(ValueError):
                special.build_passage_index([self.row(ref)])

    def test_existing_cross_book_tokenizer_path_stays_separate(self):
        indexed = special.build_passage_index([self.row('Psalms 127:1; John 1:1')])
        self.assertEqual([x['matched_ref'] for x in indexed], ['Ps 127:1', 'Jn 1:1'])

    def test_removed_appointment_never_reappears(self):
        row = self.row('Psalms 127:1; 122:1-2')
        row['current_status'] = 'removed'
        self.assertEqual(special.build_passage_index([row]), [])


if __name__ == '__main__':
    unittest.main()
