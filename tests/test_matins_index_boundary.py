"""Actual API boundary regressions; source-only coordinates are not MT authority."""
import copy
import itertools
import unittest
import matins_source_projection as m
import build_lectionary_reference as b
from passage_normalization import passage_matches, parse_passage

FLAGS = ('runtime_activation_approved', 'recurrence_approved',
         'canonical_equivalence_approved', 'include_in_current_index',
         'candidate_only', 'source_coordinate_hold', 'normalization_hold', 'active')

class MatinsIndexBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = m.load_dated_matins_fixture()
        record = next(x['source_record'] for x in cls.fixture['corpus']['records']
                      if x['source_record']['civil_date'] == '2026-03-04')
        cls.base = m._source_rows({k: record[k] for k in m.CONTEXT_KEYS}, cls.fixture)[0]

    def apis(self, rows):
        return (lambda: b.build_date_passage_index(rows, include_candidate_matins=True),
                lambda: m.candidate_matins_index(rows, self.fixture),
                lambda: b.build_date_passage_index(rows))

    def test_all_flags_require_literal_booleans_before_equality(self):
        for key, val in itertools.product(FLAGS, [0, 1, '', [], None, 'false']):
            rows = copy.deepcopy(self.base); rows[0][key] = val
            for i, api in enumerate(self.apis(rows)):
                with self.subTest(key=key, value=val, api=i), self.assertRaises(ValueError):
                    api()

    def test_combined_erasure_never_falls_through_or_authenticates_empty(self):
        for status, widen in itertools.product(['current', 'active', 'removed', 'unknown'], [False, True]):
            rows = copy.deepcopy(self.base)
            for row in rows:
                row.update(source='copticchurch.net daily scrape', parse_status='ok',
                           include_in_current_index=True, current_status=status)
                row.pop('source_context')
                if widen: row['normalized_ref'] = 'Exodus 4:1-6:30'
            for i, api in enumerate(self.apis(rows)):
                with self.subTest(status=status, widen=widen, api=i), self.assertRaises(ValueError):
                    api()

    def test_each_preserved_marker_routes_erased_candidates_to_guard(self):
        markers = ('candidate_only', 'source_coordinate_hold', 'normalization_hold',
                   'source_document_body', 'source_document_sha256', 'source_captured_context',
                   'source_navigation', 'source_body', 'source_body_sha256', 'source_evidence',
                   'source_body_qualification')
        for marker in markers:
            rows = copy.deepcopy(self.base)
            for row in rows:
                retained = {marker: row[marker]}
                for key in markers: row.pop(key, None)
                row.update(retained)
                row.update(source='copticchurch.net daily scrape', parse_status='ok',
                           service_section='Liturgy', include_in_current_index=True)
                row.pop('source_context')
            for i, api in enumerate(self.apis(rows)):
                with self.subTest(marker=marker, api=i), self.assertRaises(ValueError): api()

    def test_trusted_api_controls_and_empty_fixture_authentication(self):
        for key in ('include_candidate_matins', 'include_inactive'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                b.build_date_passage_index([], **{key: 1})
        fixture = copy.deepcopy(self.fixture)
        fixture['corpus']['records'][0]['runtime_activation'] = 0
        with self.assertRaises(ValueError): m.candidate_matins_index([], fixture)

    def test_valid_candidates_remain_optin_held_source_only(self):
        self.assertEqual(b.build_date_passage_index(self.base), [])
        index = b.build_date_passage_index(self.base, include_candidate_matins=True)
        self.assertEqual(index, m.candidate_matins_index(self.base, self.fixture))
        self.assertEqual(len(index), 6)
        for row in index:
            self.assertEqual(row['matched_ref'], '')
            self.assertEqual(row['canonical_ref'], '')
            self.assertEqual(row['search_coordinate_kind'], 'held_source_only')
            self.assertFalse(row['runtime_activation_approved'])

    def test_authenticated_held_source_query_lane_and_partial_disclosures(self):
        record = next(x['source_record'] for x in self.fixture['corpus']['records']
                      if 'Isaiah 1:19-2:2-3' in [s.strip() for s in x['source_record']['raw_reference_lines']])
        rows = m._source_rows({k: record[k] for k in m.CONTEXT_KEYS}, self.fixture)[0]
        matcher = getattr(m, 'query_candidate_matins_source', None)
        self.assertTrue(callable(matcher), 'explicit authenticated held-source query API required')
        matches = matcher('Isaiah 2:2', rows, self.fixture)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matcher('Isaiah 2:1', rows, self.fixture), [])
        self.assertTrue(matches[0]['source_body_qualification']['partial_boundary_notes'])
        self.assertEqual(matches[0]['source_convention'], 'literal_reader_edition_unmapped')
        forged = copy.deepcopy(rows); forged[0]['runtime_activation_approved'] = 0
        with self.assertRaises(ValueError): matcher('no match', forged, self.fixture)

    def test_explicit_book_semicolons_match_only_observed_components(self):
        cases = [('Isaiah 1:19-31; Isaiah 2:2-3', 'Isaiah 2:2', True),
                 ('Isaiah 1:19-31; Isaiah 2:2-3', 'Isaiah 2:1', False),
                 ('Mark 9:43; Mark 9:45; Mark 9:47-50', 'Mark 9:45', True),
                 ('Mark 9:43; Mark 9:45; Mark 9:47-50', 'Mark 9:44', False),
                 ('Mark 9:43; Mark 9:45; Mark 9:47-50', 'Mark 9:46', False),
                 ('Jonah 1:1-16; Jonah 2:1', 'Jonah 2:1', True),
                 ('Jonah 1:1-16; Jonah 2:1', 'Jonah 1:17', False)]
        for candidate, query, expected in cases:
            with self.subTest(candidate=candidate, query=query):
                self.assertIs(passage_matches(query, candidate), expected)
                self.assertIsNotNone(parse_passage(candidate))
        self.assertIsNone(parse_passage('Isaiah 1:19; Mark 9:45'))
        self.assertIsNone(parse_passage('Isaiah 1:19; invalid'))

if __name__ == '__main__': unittest.main()
