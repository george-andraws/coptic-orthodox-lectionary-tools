"""Daily verifier regression: captured order, exact rows and serialized transport."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from reading_context_overlays import load_fixture
import verify_design_deliverables as validator

ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / 'out/design/reverse_lectionary_presentation.csv'
DAILY = ROOT / 'out/design/daily/lectionary-2026.json'
LABELS = {'Psalm': 'psalm', 'Gospel': 'gospel', 'Pauline Epistle': 'pauline',
          'Catholic Epistle': 'catholicon', 'Acts of the Apostles': 'praxis'}
SOURCE_SLOTS = {('Vespers', 'gospel'): 'vespers_gospel',
                ('Matins', 'gospel'): 'matins_gospel',
                ('Liturgy', 'pauline'): 'liturgy_pauline',
                ('Liturgy', 'catholicon'): 'liturgy_catholic',
                ('Liturgy', 'praxis'): 'liturgy_acts',
                ('Liturgy', 'gospel'): 'liturgy_gospel'}
SOURCE_BOOKS = {'1 Corinthians': '1Cor', '1 John': '1Jn', '1 Peter': '1Pet',
                '2 Corinthians': '2Cor', '2 Peter': '2Pet', '2 Timothy': '2Tim',
                'Acts': 'Acts', 'Colossians': 'Col', 'Ephesians': 'Eph',
                'Galatians': 'Gal', 'Hebrews': 'Heb', 'James': 'James',
                'John': 'Jn', 'Luke': 'Lk', 'Mark': 'Mark', 'Matthew': 'Matt',
                'Philippians': 'Phil', 'Romans': 'Rom', 'Titus': 'Titus'}


class DailyValidatorProjection(unittest.TestCase):
    def verify_daily(self):
        # Run the real daily gate separately from later schema-vocabulary gates;
        # verify_rows still calls it and retains every surrounding assertion.
        presentation = validator.read_csv(PRESENTATION)
        validator.verify_source_contract_rows(presentation, transport_mode='presentation')
        validator.verify_daily_rows(presentation,
            json.loads((validator.OUT / 'lectionary_schema.json').read_text()),
            json.loads((validator.OUT / 'BUILD_DESIGN_SUMMARY.json').read_text()))

    def test_captured_service_slot_order_and_fragments_pass_exact_validator(self):
        # Authenticate primary evidence; neither expected labels nor order come
        # from the producer or observed daily output. Psalm coordinates stay held.
        fixture = load_fixture(ROOT / 'sources/coptic-reader/annual-reconciled-2026-10-07')
        for ident in (16, 17, 19, 26, 54, 57, 59):
            capture = next(r for r in fixture['oracle'] if r['id'] == f'AnnualReadings-{ident}')
            with self.subTest(context=ident):
                daily = json.loads((ROOT / f"out/design/daily/lectionary-{capture['date'][:4]}.json").read_text())
                rows = daily[capture['date']]
                self.assertTrue(all(r['slot_type'] == LABELS[r['slot']] and r['slot_order'] == 1 for r in rows))
                actual = [(SOURCE_SLOTS[(r['service_section'], r['slot_type'])], r['canonical_mt_ref'])
                          for r in rows if r['slot_type'] != 'psalm']
                expected = []
                for source in capture['source_approved_nonPsalm']:
                    book, coordinates = source['source_ref'].rsplit(' ', 1)
                    expected.append((source['slot'], SOURCE_BOOKS[book] + ' ' + coordinates))
                self.assertEqual(actual, expected)
                for service in ('Vespers', 'Matins', 'Liturgy'):
                    stages = [r['slot_type'] for r in rows if r['service_section'] == service]
                    self.assertLess(stages.index('psalm'), stages.index('gospel'))
        self.verify_daily()

    def test_valid_baseline_then_ordinary_corruptions_are_rejected(self):
        self.verify_daily()
        original_read = Path.read_text
        original = json.loads(DAILY.read_text())
        for mutation in ('omit', 'duplicate', 'truncate', 'reorder', 'fragment_order', 'service', 'type', 'order', 'missing_order'):
            damaged = copy.deepcopy(original)
            rows = damaged['2026-09-26']
            if mutation == 'omit': rows.pop(0)
            elif mutation == 'duplicate': rows.insert(0, copy.deepcopy(rows[0]))
            elif mutation == 'truncate': rows[1]['display_ref'] = 'Lk 7:1-9'
            elif mutation == 'reorder': rows[0], rows[1] = rows[1], rows[0]
            elif mutation == 'fragment_order':
                fragments = [i for i, r in enumerate(rows) if r['service_section'] == 'Matins' and r['slot'] == 'Psalm']
                self.assertEqual(len(fragments), 2)
                a, b = fragments
                rows[a], rows[b] = rows[b], rows[a]
            elif mutation == 'service': rows[0]['service_section'] = 'Matins'
            elif mutation == 'type': rows[0]['slot_type'] = 'gospel'
            elif mutation == 'order': rows[0]['slot_order'] = 99
            else: rows[0]['slot_order'] = ''
            def read_text(target, *args, **kwargs):
                return json.dumps(damaged) if target == DAILY else original_read(target, *args, **kwargs)
            with self.subTest(mutation=mutation), patch.object(Path, 'read_text', read_text):
                with self.assertRaisesRegex(AssertionError, 'does not exactly match'):
                    self.verify_daily()

    def test_serialized_authenticated_transport_is_not_dropped_or_forged(self):
        self.verify_daily()
        original_read = Path.read_text
        transport_path = ROOT / 'out/design/daily/lectionary-2021.json'
        original = json.loads(transport_path.read_text())
        date, position = next((date, i) for date, rows in original.items() for i, row in enumerate(rows)
                              if 'consumer_source_transport' in row['source_disclosure'])
        for mutation in ('omit', 'forge', 'nonboolean_state'):
            damaged = copy.deepcopy(original)
            row = damaged[date][position]
            disclosure = json.loads(row['source_disclosure'])
            if mutation == 'omit': disclosure[0].pop('consumer_source_transport')
            elif mutation == 'forge': disclosure[0]['consumer_source_transport'][0]['source_ref'] = 'forged'
            else: disclosure[0]['consumer_source_transport'][0]['state'] = False
            row['source_disclosure'] = json.dumps(disclosure, ensure_ascii=False, separators=(',', ':'))
            def read_text(target, *args, **kwargs):
                return json.dumps(damaged) if target == transport_path else original_read(target, *args, **kwargs)
            with self.subTest(mutation=mutation), patch.object(Path, 'read_text', read_text):
                with self.assertRaisesRegex(AssertionError, 'does not exactly match'):
                    self.verify_daily()

    def test_explicit_ordinary_type_disagreement_in_presentation_fails_closed(self):
        self.verify_daily()
        original = validator.read_csv
        rows = original(PRESENTATION)
        position = next(i for i, r in enumerate(rows) if r['gregorian_date'] == '2020-01-01'
                        and r['service_section'] == 'Vespers' and r['slot'] == 'Psalm')
        for value in ('gospel', 'unknown', 1, False):
            damaged = copy.deepcopy(rows)
            damaged[position]['slot_type'] = value
            with self.subTest(value=value), patch.object(validator, 'read_csv',
                    side_effect=lambda path: damaged if path == PRESENTATION else original(path)):
                with self.assertRaisesRegex(AssertionError, 'Ordinary source slot type'):
                    self.verify_daily()


if __name__ == '__main__':
    unittest.main()
