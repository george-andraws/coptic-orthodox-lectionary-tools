"""Source-backed Last Friday boundary; no generated/package oracle or full builds."""
import copy
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import calendar_resolution as calendar
import build_lectionary_reference as reference

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = Path('sources/coptic-reader/last-friday-2028-04-07-2026-10-07')
DATE = dt.date(2028, 4, 7)
TITLE = 'Friday of the seventh week of Great Lent'
# Independent complete primary-source oracle, NOT extracted from the fixture.
EXPECTED = [
    ('Matins', 'Prophecy', 'Genesis 49:33-50:26', 'Gen 49:33-50:26'),
    ('Matins', 'Prophecy', 'Proverbs 11:27-12:22', 'Prov 11:27-12:22'),
    ('Matins', 'Prophecy', 'Isaiah 66:10-24', 'Isa 66:10-24'),
    ('Matins', 'Prophecy', 'Job 42:7-17', 'Job 42:7-17'),
    ('Matins', 'Psalm', 'Psalms 31:11-12', 'Ps 32:10-11'),
    ('Matins', 'Gospel', 'Luke 16:19-31', 'Lk 16:19-31'),
    ('Liturgy', 'Pauline Epistle', '2 Timothy 3:1-4:5', '2Tim 3:1-4:5'),
    ('Liturgy', 'Catholic Epistle', 'James 5:7-16', 'James 5:7-16'),
    ('Liturgy', 'Acts', 'Acts 15:1-18', 'Acts 15:1-18'),
    ('Liturgy', 'Psalm', 'Psalms 97:8', 'Ps 98:8-9'),
    ('Liturgy', 'Gospel', 'Luke 13:31-35', 'Lk 13:31-35'),
]


def raw(date=DATE):
    html = (ROOT / 'cache/copticchurch_html' / f'{date.isoformat()}.html').read_text()
    return reference.parse_copticchurch_html(html, date)[1]


def signature(rows):
    return [(r['service_section'], r['reading_type'], r['raw_ref'], r['normalized_ref']) for r in rows]


class LastFridayAnnunciationBoundary(unittest.TestCase):
    def test_april_7_2028_complete_source_table_replaces_wrong_annunciation(self):
        original = raw()
        saved = copy.deepcopy(original)
        current = calendar.resolve_current_date_rows(original, [])
        self.assertEqual(signature(current), EXPECTED)
        self.assertEqual({r['day_title'] for r in current}, {TITLE})
        self.assertFalse(any(r['service_section'] == 'Vespers' for r in current))
        self.assertEqual(original, saved)
        self.assertEqual(signature(calendar.resolve_current_date_rows(original, [])), EXPECTED)
        self.assertEqual(calendar.resolve_current_date_rows(current, []), current)
        # The same recurring boundary collision occurs in 2023; provenance must
        # continue to identify the verified 2028 capture, not a fictitious 2023 one.
        recurring = calendar.resolve_current_date_rows(raw(dt.date(2023, 4, 7)), [])
        self.assertEqual(signature(recurring), EXPECTED)
        self.assertTrue(all('verified_date=2028-04-07' in r['normalization_warning'] for r in recurring))
        self.assertTrue(all(r['normalization_warning'] == r['normalization_warning'].rstrip() for r in current + recurring))

    def test_exact_offset_and_feast_collision_required(self):
        for date, title in [(dt.date(2027, 4, 7), 'Annunciation'),
                            (dt.date(2028, 4, 6), 'Annunciation'),
                            (dt.date(2028, 4, 7), TITLE),
                            (dt.date(2028, 4, 7), 'Other occasion')]:
            with self.subTest(date=date, title=title):
                rows = [dict(raw()[0], gregorian_date=date.isoformat(), day_title=title)]
                self.assertEqual(calendar.resolve_current_date_rows(rows, []), rows)

    def test_2026_pascha_and_2027_annunciation_preserved(self):
        with (ROOT / 'out/data/pascha_day_hour_index.csv').open() as handle:
            pascha = list(csv.DictReader(handle))
        from build_lectionary_crosswalk import apply_pascha_curated_ref_correction
        pascha = [apply_pascha_curated_ref_correction(row) for row in pascha]
        day = calendar.resolve_current_date_rows(raw(dt.date(2026, 4, 7)), pascha)
        self.assertEqual({r['day_title'] for r in day}, {'Tuesday', 'Tuesday Eve'})
        self.assertEqual(len(day), 38)
        ordinary = raw(dt.date(2027, 4, 7))
        self.assertEqual(calendar.resolve_current_date_rows(ordinary, pascha), sorted(ordinary, key=lambda r: (r['gregorian_date'], r['day_title'], r['service_section'], r['reading_type'], r['raw_ref'])))

    def test_passage_helper_uses_exact_normalized_boundaries_and_preserves_printed(self):
        current = calendar.resolve_current_date_rows(raw(), [])
        with tempfile.TemporaryDirectory() as directory, patch.object(reference, 'DATA', Path(directory)):
            index = reference.build_date_passage_index(current)
        self.assertEqual([r['matched_ref'] for r in index], [r[3] for r in EXPECTED])
        self.assertEqual([r['raw_ref'] for r in index], [r[2] for r in EXPECTED])
        self.assertEqual([r['source_slot'] for r in index[:4]], ['OT1', 'OT2', 'OT3', 'OT4'])

    def test_fixture_corruptions_fail_closed_even_with_updated_outer_hash(self):
        for mutation in ('missing', 'reordered', 'truncated', 'wrong_date', 'wrong_occasion', 'duplicate', 'wrong_service', 'wrong_offset', 'wrong_suppression', 'bad_hash'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copytree(ROOT / FIXTURE, root / FIXTURE)
                overlay = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())
                rule = overlay['calendar_boundary_tables'][0]
                path = root / rule['evidence']
                fixture = json.loads(path.read_text())
                if mutation == 'missing': fixture['readings'].pop(0)
                elif mutation == 'reordered': fixture['readings'][0:2] = reversed(fixture['readings'][0:2])
                elif mutation == 'truncated': fixture['readings'][0]['normalized_ref'] = 'Gen 49:33-50:25'
                elif mutation == 'wrong_date': fixture['verified_date'] = '2028-04-06'
                elif mutation == 'wrong_occasion': fixture['occasion'] = 'Annunciation'
                elif mutation == 'duplicate': fixture['readings'].append(copy.deepcopy(fixture['readings'][0]))
                elif mutation == 'wrong_service': fixture['readings'][0]['service_section'] = 'Liturgy'
                elif mutation == 'wrong_offset': rule['pascha_offset_days'] = -8
                elif mutation == 'wrong_suppression': fixture['suppressed_service'] = 'Matins'
                path.write_text(json.dumps(fixture))
                overlay['source_fingerprints'][rule['evidence']] = hashlib.sha256(path.read_bytes()).hexdigest()
                if mutation == 'bad_hash':
                    (root / FIXTURE / 'Vespers.txt').write_text('Missing reading is not a rubric')
                (root / 'sources/lectionary_corrections.json').write_text(json.dumps(overlay))
                with patch.object(calendar, 'WORK', root):
                    with self.assertRaises(RuntimeError):
                        calendar.resolve_current_date_rows(raw(), [])

    def test_raw_overlap_with_seasonal_table_is_rejected_not_duplicated(self):
        duplicate = dict(raw()[0], day_title=TITLE, service_section='Matins', reading_type='Prophecy', raw_ref='Genesis 49:33-50:26')
        with self.assertRaisesRegex(RuntimeError, 'overlap|mixed'):
            calendar.resolve_current_date_rows(raw() + [duplicate], [])


if __name__ == '__main__':
    unittest.main()
