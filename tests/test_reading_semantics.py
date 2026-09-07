import datetime as dt
import hashlib
import json
import os
import sys
import tempfile
import unittest
import csv
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ['LECTIONARY_DISABLE_VAULT_PUBLISH'] = '1'
import build_lectionary_reference as reference
import build_lectionary_crosswalk as crosswalk
import build_design_deliverables as design
import passage_normalization as passages


class ReadingSemanticsTests(unittest.TestCase):
    def test_lectionary_corrections_are_idempotent_and_reject_drift(self):
        overlay = {
            'source_fingerprints': {},
            'pascha_day_hour': [{
                'day': 'Monday Eve', 'hour': 'Sixth Hour', 'slot': 'Psalm+Gospel',
                'expected_raw_ref': 'raw', 'corrected_ref': 'corrected',
                'source_path': 'source.txt', 'source_line': 7,
            }],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / 'data'
            data.mkdir()
            (root / 'sources').mkdir()
            (root / 'sources/lectionary_corrections.json').write_text(json.dumps(overlay))
            csv_path = data / 'pascha_day_hour_index.csv'
            csv_path.write_text('day,hour,slot,refs\nMonday Eve,Sixth Hour,Psalm+Gospel,raw\n')
            with patch.object(reference, 'WORK', root), patch.object(reference, 'DATA', data):
                reference.apply_lectionary_corrections()
                reference.apply_lectionary_corrections()
                rows = list(csv.DictReader(csv_path.open()))
                self.assertEqual(rows[0]['refs'], 'corrected')
                self.assertEqual(rows[0]['raw_refs'], 'raw')
                self.assertEqual(rows[0]['correction_source'], 'source.txt:7')
                rows[0]['correction_source'] = 'wrong:9'
                reference.write_csv(csv_path, rows, list(rows[0]))
                with self.assertRaisesRegex(RuntimeError, 'drift'):
                    reference.apply_lectionary_corrections()

    def test_pascha_correction_fixture_matches_sources_and_contexts(self):
        fixture = json.loads((ROOT / 'tests/fixtures/lectionary_corrections.json').read_text())
        for source in fixture['sources'].values():
            digest = hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest()
            self.assertEqual(digest, source['sha256'])
        corrections = fixture['pascha_reference_corrections']
        self.assertEqual(
            [(row['day'], row['normalized_citation']) for row in corrections],
            [('Monday Eve', 'Mark 10:32-34'), ('Tuesday Eve', 'Lk 21:34-38')],
        )
        raw = (ROOT / 'out/data/pascha_day_hour_index.jsonl').read_text()
        for row in corrections:
            self.assertIn(row['expected_raw_ref'], raw)
            self.assertIn(row['corrected_ref'], raw)

    def test_tout_catholic_source_error_is_corrected_without_changing_raw_evidence(self):
        for day in (21, 23):
            html = f'<title>Readings</title><div class="col-lg-9"><h1>Readings</h1><h2>Tout {day}</h2><h2>Liturgy</h2><h4>Catholic Epistle</h4><h5>Jn 2:7-11</h5></div>'
            _, rows = reference.parse_copticchurch_html(html, dt.date(2026, 10, day - 20))
            self.assertEqual(rows[0]['normalized_ref'], '1Jn 2:7-11')
            self.assertEqual(rows[0]['raw_ref'], 'Jn 2:7-11')
            self.assertEqual(rows[0]['reading_type'], 'Catholic Epistle')

    def test_coptic_reader_date_corrections_are_context_scoped_and_preserve_raw(self):
        cases = [
            ('The first Sunday of Tout', 'Pauline Epistle', '1Tim 1:12-27', '1Tim 1:12-19'),
            ('Abib 7', 'Gospel', 'Matt 9:33 - 41', 'Mark 9:33-41'),
            ('Amshir 2', 'Gospel', 'Matt 9:33 - 41', 'Mark 9:33-41'),
            ('Fast of Nineveh', 'Gospel', 'Matt 9:33 - 41', 'Matt 12:35-45'),
        ]
        for title, reading_type, raw_ref, expected in cases:
            row = reference.apply_copticchurch_source_correction({
                'day_title': title,
                'service_section': 'Liturgy',
                'reading_type': reading_type,
                'raw_ref': raw_ref,
                'normalized_ref': raw_ref,
            })
            self.assertEqual(row['raw_ref'], raw_ref)
            self.assertEqual(row['normalized_ref'], expected)
            self.assertEqual(row['parse_status'], 'source_corrected')
            self.assertIn('coptic_reader', row['normalization_warning'])

        unaffected = reference.apply_copticchurch_source_correction({
            'day_title': 'Amshir 3', 'service_section': 'Liturgy',
            'reading_type': 'Gospel', 'raw_ref': 'Matt 9:33-41',
            'normalized_ref': 'Matt 9:33-41',
        })
        self.assertEqual(unaffected['normalized_ref'], 'Matt 9:33-41')

    def test_jonah_fast_no_vespers_is_exact_date_context_only(self):
        base = {'day_title': 'Fast of Nineveh', 'service_section': 'Vespers', 'reading_type': 'Gospel', 'raw_ref': 'Lk 10:38-52', 'normalized_ref': 'Lk 10:38-52'}
        removed = reference.apply_copticchurch_source_correction({**base, 'gregorian_date': '2029-01-29'})
        self.assertEqual(removed['raw_ref'], 'Lk 10:38-52')
        self.assertEqual(removed['superseded_reason'], 'coptic_reader_no_service')
        same_fast = reference.apply_copticchurch_source_correction({**base, 'gregorian_date': '2028-01-29'})
        self.assertEqual(same_fast['superseded_reason'], 'coptic_reader_no_service')
        control = reference.apply_copticchurch_source_correction({**base, 'day_title': 'Toba 21', 'gregorian_date': '2028-01-29'})
        self.assertNotIn('superseded_reason', control)

    def test_malformed_double_numeric_book_code_cannot_be_salvaged(self):
        books = {3: 'Leviticus', 43: 'John', 62: '1 John'}
        for raw in ('62.43.4:15-21*@+62.5:1-4', '1.43.2:7-11'):
            with self.assertRaises(ValueError):
                passages.normalize_numeric_ref(raw, books)
            with self.assertRaises(ValueError):
                list(passages.iter_numeric_ref_segments(raw, books))

    def test_numeric_source_cross_chapter_boundaries_are_not_truncated(self):
        books = {23: 'Isaiah', 43: 'John', 45: 'Romans', 47: '2 Corinthians', 62: '1 John'}
        fixtures = {
            '45.1:26-2:7': 'Rom 1:26-2:7',
            '47.6:14-7:16': '2Cor 6:14-7:16',
            '23.8:13-9:7': 'Isa 8:13-9:7',
            '62.2:20-3:1': '1Jn 2:20-3:1',
            '43.15:26-16:15': 'Jn 15:26-16:15',
            '43.14:26-15:4': 'Jn 14:26-15:4',
        }
        for raw, expected in fixtures.items():
            with self.subTest(raw=raw):
                rows = list(passages.iter_numeric_ref_segments(raw, books))
                self.assertEqual(rows[0]['canonical_segment'], expected)

    def test_bashans_sunday_source_mapping_preserves_numbered_john(self):
        rows = reference.export_cycle_tables(reference.load_books())
        row = next(r for r in rows if r['source_table'] == 'SundayReadings' and r['day_key'] == 'Bashans 3' and r['reading_slot'] == 'liturgy_catholic')
        self.assertEqual(row['raw_ref'], '62.43.4:15-21*@+62.5:1-4')
        self.assertEqual(row['normalized_ref'], '1Jn 4:15-21; 1Jn 5:1-4')
        self.assertEqual({r['book_abbrev'] for r in reference.build_passage_index([row], reference.load_books())}, {'1Jn'})

    def test_psalm_embedded_under_gospel_heading_is_typed_per_passage(self):
        row = dict(source='fixture', gregorian_date='2026-04-05', weekday='Sunday', day_title='Palm Sunday', service_section='Liturgy', reading_type='Gospel', raw_ref='Psalm 64:1-2', normalized_ref='Psalm 64:1-2', url='fixture')
        with tempfile.TemporaryDirectory() as tmp, patch.object(reference, 'DATA', Path(tmp)):
            result = reference.build_date_passage_index([row])
        self.assertEqual(result[0]['reading_type'], 'Psalm')
        self.assertIn('Gospel', result[0]['normalization_warning'])

    def test_crosswalk_retains_gospel_group_but_types_its_psalm_correctly(self):
        from collections import defaultdict, Counter
        rows = []
        crosswalk.add_row(rows, defaultdict(Counter), 'Ps 81:3', 'special_service', reading_slot='first_gospel', reading_type='psalm', service_section='first_gospel')
        self.assertEqual(rows[0]['reading_slot'], 'first_psalm')
        self.assertEqual(rows[0]['service_section'], 'first_gospel')
        self.assertEqual(design.slot_type_for({'slot': 'first_psalm', 'spans_json': json.dumps([{'book': 'Ps'}])}), 'psalm')

    def test_chapter_labels_use_passage_slot_not_enclosing_service(self):
        import build_bible_chapter_lectionary_index as chapters
        labels = chapters.occurrence_labels(dict(source_kind='katameros_cycle', service_section='liturgy_gospel', reading_slot='liturgy_psalm', reading_type='GreatLentReadings'))
        self.assertEqual(labels['reading_label'], 'Psalm')
        self.assertEqual(labels['service_label'], 'Liturgy')

    def test_unknown_bad_daily_assignment_stops_index_build(self):
        row = dict(source='fixture', gregorian_date='2026-01-01', weekday='Thursday', day_title='Unrecognized day', service_section='Liturgy', reading_type='Catholic Epistle', raw_ref='Jn 3:16', normalized_ref='Jn 3:16', url='fixture')
        with self.assertRaises(ValueError):
            reference.build_date_passage_index([row])

    def test_unknown_bad_cycle_assignment_stops_index_build(self):
        row = dict(source_table='fixture', day_key='fixture', reading_slot='liturgy_catholic', raw_ref='43.3:16', normalized_ref='Jn 3:16')
        with self.assertRaises(ValueError):
            reference.build_passage_index([row], {43: 'John'})

    def test_design_rejects_impossible_book_slot_pairs_instead_of_relabeling(self):
        for slot, book in [('Catholic Epistle', 'Jn'), ('Gospel', '1Jn'), ('Pauline Epistle', 'Acts'), ('Praxis', 'Rom'), ('Psalm', 'Lk')]:
            with self.subTest(slot=slot, book=book), self.assertRaises(ValueError):
                design.slot_type_for({'slot': slot, 'spans_json': json.dumps([{'book': book}])})
        for slot, book, expected in [('Catholic Epistle', '1Jn', 'catholicon'), ('Gospel', 'Jn', 'gospel'), ('Pauline Epistle', 'Heb', 'pauline')]:
            self.assertEqual(design.slot_type_for({'slot': slot, 'spans_json': json.dumps([{'book': book}])}), expected)


if __name__ == '__main__':
    unittest.main()
