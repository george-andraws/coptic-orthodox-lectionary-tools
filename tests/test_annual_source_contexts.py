"""Bounded regressions exercise the real HTML/helper path; no builders run."""
import copy
import datetime as dt
import json
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build_lectionary_reference as core
from passage_normalization import extract_text_ref_tokens
from reading_context_overlays import load_fixture, repair_table, authenticate_fixture

FIXTURE = ROOT / 'sources/coptic-reader/annual-reconciled-2026-10-07'
# Independent spelling table only: never derive expected boundaries from the
# implementation's parser or repaired rows. Printed Reader boundaries control.
SOURCE_BOOKS = {'1 Corinthians':'1Cor', '1 John':'1Jn', '1 Peter':'1Pet',
                '2 Corinthians':'2Cor', '2 Peter':'2Pet', '2 Timothy':'2Tim',
                'Acts':'Acts', 'Colossians':'Col', 'Ephesians':'Eph',
                'Galatians':'Gal', 'Hebrews':'Heb', 'James':'James',
                'John':'Jn', 'Luke':'Lk', 'Mark':'Mark', 'Matthew':'Matt',
                'Philippians':'Phil', 'Romans':'Rom', 'Titus':'Titus'}


def source_expected(reference):
    book, coordinates = reference.rsplit(' ', 1)
    return SOURCE_BOOKS[book] + ' ' + coordinates


TARGETS = [(16, 'liturgy_catholic'), (17, 'liturgy_catholic'),
           (19, 'liturgy_gospel'), (26, 'liturgy_catholic'),
           (54, 'liturgy_catholic'), (57, 'liturgy_catholic'),
           (57, 'liturgy_gospel'), (59, 'liturgy_catholic')]


def captured_table(fixture, ident):
    capture = next(r for r in fixture['oracle'] if r['id'] == f'AnnualReadings-{ident}')
    _, raw = core.parse_copticchurch_html(
        (FIXTURE / 'date-source' / (capture['date'] + '.html')).read_text(),
        dt.date.fromisoformat(capture['date']))
    # Explicit service/label adapter, never a book-inferred service.
    mapping = {('Vespers', 'Gospel'): 'vespers_gospel',
               ('Matins', 'Gospel'): 'matins_gospel',
               ('Liturgy', 'Pauline Epistle'): 'liturgy_pauline',
               ('Liturgy', 'Catholic Epistle'): 'liturgy_catholic',
               ('Liturgy', 'Acts of the Apostles'): 'liturgy_acts',
               ('Liturgy', 'Gospel'): 'liturgy_gospel'}
    for row in raw:
        row['slot'] = mapping.get((row['service_section'], row['reading_type']), 'uncompared_psalm')
    return capture, raw


class AnnualContexts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load_fixture(FIXTURE)

    def test_eight_source_defects_through_actual_helper(self):
        for ident, slot in TARGETS:
            with self.subTest(ident=ident, slot=slot):
                capture, table = captured_table(self.fixture, ident)
                original = copy.deepcopy(table)
                if os.environ.get('ANNUAL_COUNTERPROBE'):
                    active = table
                else:
                    result = repair_table(capture['context'], table, self.fixture, 'date_source')
                    active = result['active']
                    self.assertEqual(table, original)
                    self.assertEqual([r['raw_ref'] for r in active], [r['raw_ref'] for r in original])
                target = next(r for r in active if r['slot'] == slot)
                expected = source_expected(next(r['source_ref'] for r in capture['source_approved_nonPsalm'] if r['slot'] == slot))
                actual = [row['matched_ref'] for row in core.build_date_passage_index([target])]
                self.assertEqual(actual, [expected])

    def test_full_24_context_counter_and_17_canaries(self):
        snapshots = json.loads((FIXTURE / 'snapshots.json').read_text())
        matches = whole = 0
        for capture in self.fixture['oracle']:
            snapshot = next(s for s in snapshots if s['id']==capture['id'] and s['layer']=='current_date_source')
            table = [dict(slot['actual_rows'][0], slot=slot['slot']) for slot in snapshot['nonPsalm_slots']]
            result = repair_table(capture['context'], table, self.fixture, 'date_source')
            actual = [[extract_text_ref_tokens(row['normalized_ref']), row['slot']] for row in result['active']]
            expected = [[[source_expected(row['source_ref'])], row['slot']] for row in capture['source_approved_nonPsalm']]
            self.assertEqual(actual, expected, capture['id'])
            matches += len(actual)
            whole += actual == expected
            if capture['key']['Id'] not in {16,17,19,26,54,57,59}:
                self.assertEqual(result['active'], table)
                self.assertEqual(result['events'], [])
        self.assertEqual((matches, whole), (144, 24))

    def test_neighbor_wrong_occasion_weekday_variant_and_date_noop(self):
        capture, table = captured_table(self.fixture, 59)
        for key, value in [('id', 'AnnualReadings-58'), ('date', '2027-11-10'),
                           ('coptic_day', 28), ('coptic_month', 1),
                           ('occasion', 'Standard'), ('season', 'Standard'),
                           ('weekday', 'Wednesday'), ('variant', 'generic_annual')]:
            with self.subTest(key=key):
                context = dict(capture['context'], **{key: value})
                result = repair_table(context, table, self.fixture, 'date_source')
                self.assertEqual(result['active'], table)
                self.assertEqual(result['history'], [])
                self.assertEqual(result['events'], [])

    def test_wrong_service_and_drift_duplicate_order_guards(self):
        capture, table = captured_table(self.fixture, 57)
        for mutation in ['service', 'raw', 'duplicate', 'order', 'date', 'type', 'source']:
            bad = copy.deepcopy(table)
            index = next(i for i, row in enumerate(bad) if row['slot'] == 'liturgy_catholic')
            if mutation == 'service': bad[index]['service_section'] = 'Matins'
            if mutation == 'raw': bad[index]['raw_ref'] = 'Jm 1:1-99'
            if mutation == 'duplicate': bad.insert(index, copy.deepcopy(bad[index]))
            if mutation == 'order': bad.reverse()
            if mutation == 'date': bad[index]['gregorian_date'] = '2026-11-07'
            if mutation == 'type': bad[index]['reading_type'] = 'Gospel'
            if mutation == 'source': bad[index]['source'] = 'unverified generic template'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                repair_table(capture['context'], bad, self.fixture, 'date_source')

    def test_idempotency_and_superseded_raw_history(self):
        capture, table = captured_table(self.fixture, 16)
        once = repair_table(capture['context'], table, self.fixture, 'date_source')
        twice = repair_table(capture['context'], once['active'], self.fixture, 'date_source')
        self.assertEqual(once['active'], twice['active'])
        self.assertEqual(twice['events'], [])
        self.assertEqual(once['history'][0]['raw_ref'], '2Pet 2:1-10')
        self.assertEqual(once['history'][0]['superseded_by_ref'], '1Pet 1:25-2:10')
        self.assertEqual([r for r in table if r['slot']=='uncompared_psalm'],
                         [r for r in once['active'] if r['slot']=='uncompared_psalm'])

    def test_authenticated_source_headings_order_and_bytes(self):
        authenticate_fixture(self.fixture)
        for mutation in ['order', 'heading', 'duplicate']:
            bad = copy.deepcopy(self.fixture)
            doc = bad['oracle'][0]['documents'][0]
            if mutation == 'order': doc['sourceReferenceHeadings'].reverse()
            if mutation == 'heading': doc['sourceReferenceHeadings'][0]['raw_line'] = '\tLuke 1:1\n'
            if mutation == 'duplicate': doc['sourceReferenceHeadings'].append(copy.deepcopy(doc['sourceReferenceHeadings'][0]))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): authenticate_fixture(bad)

    def test_cross_variants_and_joyful_are_exact_captured_contexts(self):
        byid = {r['key']['Id']: r for r in self.fixture['oracle']}
        for ident in [17,18,19]:
            self.assertEqual(byid[ident]['context']['occasion'], 'Feast of the Cross')
            self.assertEqual(byid[ident]['context']['coptic_day'], ident)
        self.assertEqual(byid[59]['context']['occasion'], 'Joyful 29th of the Month')
        self.assertEqual((byid[59]['context']['coptic_month'], byid[59]['context']['coptic_day']), (2,29))
        self.assertEqual(len(self.fixture['oracle']), 24)
        self.assertEqual(len(self.fixture['repairs']), 8)

    def test_supplements_insert_in_source_order_and_refuse_nonJames_missing(self):
        capture, table = captured_table(self.fixture, 57)
        missing = [r for r in table if r['slot'] != 'liturgy_catholic']
        result = repair_table(capture['context'], missing, self.fixture, 'date_source')
        slots = [r['slot'] for r in result['active'] if r['slot']!='uncompared_psalm']
        self.assertEqual(slots, [r['slot'] for r in capture['source_approved_nonPsalm']])
        self.assertEqual(result['events'][0]['action'], 'supplement')
        capture, table = captured_table(self.fixture, 16)
        with self.assertRaises(ValueError):
            repair_table(capture['context'], [r for r in table if r['slot']!='liturgy_catholic'], self.fixture, 'date_source')

    def test_cycle_16_is_bounded_and_raw_preserved(self):
        capture = next(r for r in self.fixture['oracle'] if r['key']['Id']==16)
        rows = [{'slot':'liturgy_catholic','service_section':'Liturgy',
                 'raw_ref':'60.2:1-10','normalized_ref':'1Pet 2:1-10'}]
        result = repair_table(capture['context'], rows, self.fixture, 'cycle')
        self.assertEqual(result['active'][0]['normalized_ref'],'1Pet 1:25-2:10')
        self.assertEqual(result['active'][0]['raw_ref'],'60.2:1-10')
        # B5 intentionally rejects an explicitly selected unsupported source kind.
        with self.assertRaises(ValueError):
            repair_table(capture['context'],rows,self.fixture,'unknown')

if __name__ == '__main__': unittest.main()
