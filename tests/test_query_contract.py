import csv
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build_bible_chapter_lectionary_index as index
from calendar_resolution import resolve_current_date_rows
from passage_normalization import parse_passage


class QueryContract(unittest.TestCase):
    def test_annunciation_holy_week_overlay_uses_real_source_shape(self):
        raw_path = ROOT / 'out/data/copticchurch_date_readings_2020_2035.csv'
        pascha_path = ROOT / 'out/data/pascha_day_hour_index.csv'
        with raw_path.open(newline='', encoding='utf-8') as handle:
            raw_rows = list(csv.DictReader(handle))
        with pascha_path.open(newline='', encoding='utf-8') as handle:
            pascha_rows = list(csv.DictReader(handle))
        resolved = resolve_current_date_rows(raw_rows, pascha_rows)
        april7 = [row for row in resolved if row['gregorian_date'] == '2026-04-07']
        self.assertTrue(april7)
        self.assertFalse(any(row['day_title'] == 'Annunciation' for row in april7))
        self.assertEqual({'Tuesday', 'Tuesday Eve'}, {row['day_title'] for row in april7})
        chapter_occurrences = ROOT / 'out/data/bible_chapter_lectionary_occurrences.csv'
        with chapter_occurrences.open(newline='', encoding='utf-8') as handle:
            nahum = [row for row in csv.DictReader(handle) if row.get('chapter_ref') == 'Nah 1']
        self.assertEqual(1, len(nahum))

    def test_regenerated_current_sidecars_drive_root_cli(self):
        sidecar = ROOT / 'out/data/copticchurch_date_readings_current_2020_2035.csv'
        self.assertTrue(sidecar.exists(), 'run the local current-date sidecar build')
        result = subprocess.run(
            [sys.executable, str(ROOT / 'query_lectionary.py'), '--date', '2026-04-07', '--limit', '200'],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('Tuesday', result.stdout)
        self.assertIn('Tuesday Eve', result.stdout)
        self.assertNotIn('Annunciation', result.stdout)

    def test_registry_matches_parser_canonical_books(self):
        for _, name, abbrev, _ in index.BOOKS:
            with self.subTest(book=name):
                parsed = parse_passage(name + ' 1')
                self.assertTrue(parsed)
                self.assertEqual(parsed.book_abbrev, abbrev)

    def test_cli_explicit_data_dir_and_generated_copy(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            scripts = root / 'out/scripts'
            data = root / 'chosen-data'
            scripts.mkdir(parents=True)
            data.mkdir()
            for filename in ['query_lectionary.py', 'passage_normalization.py']:
                shutil.copyfile(ROOT / filename, scripts / filename)
            with (data / 'copticchurch_date_readings_2020_2035.csv').open('w') as f:
                f.write('gregorian_date,day_title,service_section,reading_type,raw_ref\n2026-01-01,Test Day,Vespers,Gospel,Jn 1:1-5\n')
            for script in [ROOT / 'query_lectionary.py', scripts / 'query_lectionary.py']:
                result = subprocess.run([sys.executable, str(script), '--data-dir', str(data), '--date', '2026-01-01'], cwd=td, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('Test Day', result.stdout)

    def test_nahum_occurrence_survives_chapter_generation(self):
        import os
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            # Source-backed occurrence: Ottawa Pascha text, Hosanna Sunday,
            # Eleventh Hour, Nahum 1:2-8 (source row 1633).
            (data / 'reverse_lookup_crosswalk.csv').write_text('passage,source_kind,liturgical_place,service_section,reading_type\nNah 1:2-8,pascha_source_text,Hosanna Sunday,Eleventh Hour,Prophecy\n')
            env = {**os.environ, 'LECTIONARY_DATA_DIR': td, 'LECTIONARY_DISABLE_VAULT_PUBLISH': '1'}
            built = subprocess.run([sys.executable, str(ROOT / 'build_bible_chapter_lectionary_index.py')], env=env, capture_output=True, text=True)
            self.assertEqual(built.returncode, 0, built.stderr)
            outputs = []
            for query in ['Nahum 1', 'Nah 1']:
                result = subprocess.run([sys.executable, str(ROOT / 'query_lectionary.py'), '--data-dir', td, '--chapter', query], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('Hosanna Sunday', result.stdout)
                outputs.append(result.stdout)
            self.assertEqual(outputs[0], outputs[1])

    def test_missing_explicit_data_dir_is_actionable(self):
        with tempfile.TemporaryDirectory() as td:
            result = subprocess.run([sys.executable, str(ROOT / 'query_lectionary.py'), '--data-dir', str(Path(td) / 'missing'), '--date', '2026-01-01'], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Data directory not found', result.stderr)
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
