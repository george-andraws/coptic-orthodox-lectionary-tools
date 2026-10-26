"""Bounded real pipeline; only the whole-corpus ledger has a subset oracle."""
import copy
import csv
import datetime as dt
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_lectionary_reference as reference
import build_lectionary_crosswalk as crosswalk
import build_design_deliverables as design
import jonah_fast_source_supplements as jonah
from calendar_resolution import julian_pascha_gregorian
from reading_context_overlays import is_current_source_row

ROOT = Path(__file__).resolve().parents[1]


def pipeline(date):
    date = dt.date.fromisoformat(date)
    meta, raw = reference.parse_copticchurch_html(
        (ROOT / 'cache/copticchurch_html' / f'{date}.html').read_text(), date)
    indexed = reference.build_date_passage_index(raw)
    # Exercise the real CSV serialization boundary.
    buf = io.StringIO()
    fields = list(dict.fromkeys(k for row in indexed for k in row))
    writer = csv.DictWriter(buf, fields); writer.writeheader(); writer.writerows(indexed)
    buf.seek(0)
    return raw, crosswalk.project_date_rows(list(csv.DictReader(buf)))


class JonahProjection(unittest.TestCase):
    def test_full_raw_csv_union_boundary_preserves_authenticated_jonah_rows(self):
        raw = []
        for date in ['2026-02-02', '2026-02-03', '2026-02-04', '2026-11-01']:
            _, rows = reference.parse_copticchurch_html(
                (ROOT / 'cache/copticchurch_html' / (date + '.html')).read_text(), dt.date.fromisoformat(date))
            raw.extend(rows)
        fields = list(dict.fromkeys(k for row in raw for k in row))
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fields)
        writer.writeheader(); writer.writerows(raw)
        buffer.seek(0)
        restored = list(csv.DictReader(buffer))
        native = reference.build_date_passage_index([r for r in raw if r.get('source_kind') == jonah.KIND])
        from_csv = reference.build_date_passage_index([r for r in restored if r.get('source_kind') == jonah.KIND])
        expected_appointments = {(date, service, kind)
            for date in ('2026-02-02', '2026-02-03', '2026-02-04')
            for service, kind in [('Matins', 'Prophecy'), ('Matins', 'Psalm'), ('Matins', 'Gospel'),
                ('Liturgy', 'Pauline Epistle'), ('Liturgy', 'Catholic Epistle'),
                ('Liturgy', 'Acts of the Apostles'), ('Liturgy', 'Psalm'), ('Liturgy', 'Gospel')]}
        self.assertEqual({(r['gregorian_date'], r['service_section'], r['reading_type']) for r in from_csv}, expected_appointments)
        self.assertEqual([(r['matched_ref'], r['provenance']) for r in from_csv],
                         [(r['matched_ref'], r['provenance']) for r in native])
        for bad in [True, 0, 1.0, '01']:
            row = copy.deepcopy(next(r for r in restored if r.get('source_kind') == jonah.KIND))
            row['source_order'] = bad
            with self.subTest(ordinal=bad), self.assertRaises(ValueError):
                reference.build_date_passage_index([row])

    def test_real_pipeline_daily_and_bounded_reverse_all_source_dates(self):
        contexts = json.loads((jonah.SOURCE_ROOT / 'input-contexts.json').read_text())
        projected = []
        for context in contexts:
            raw, rows = pipeline(context['date'])
            typed = [r for r in rows if r['source_kind'] == jonah.KIND]
            self.assertEqual(len([r for r in typed if r['reading_type'] == 'Prophecy']), 1)
            self.assertTrue(all(r['source_family'] == jonah.FAMILY for r in typed))
            self.assertFalse(any(r['service_section'] == 'Vespers' for r in rows))
            if context['date'] in jonah.COLLISIONS:
                companions = [r for r in raw if is_current_source_row(r) and r['reading_type'] != 'Prophecy']
                self.assertEqual(list(dict.fromkeys((r['service_section'], r['reading_type'], r['raw_ref']) for r in rows if r['source_kind'] != jonah.KIND)),
                                 [(r['service_section'], r['reading_type'], r['raw_ref']) for r in companions])
            projected.extend(rows)
        presentation, _ = design.build_reverse_presentation(projected)
        typed = [r for r in presentation if r['source_kind'] == jonah.KIND]
        self.assertTrue(all(r['current_status'] == 'current_public_or_local_reference' for r in typed))
        self.assertTrue(all(r['source_key'] == 'coptic_reader_qualified_jonah_fast' for r in typed))
        self.assertTrue(all('sha256=' in r['source_locator'] for r in typed))
        self.assertFalse(any('body_literal' in r['provenance'] for r in typed))
        daily = design.build_daily_year_files(presentation, transport_mode='presentation')
        for year in (2026, 2027, 2028):
            for offset, ref in [(-69, 'Jonah 1:1-17'), (-68, 'Jonah 2:1-10'), (-67, 'Jonah 3:1-4:11')]:
                date = (julian_pascha_gregorian(year) + dt.timedelta(days=offset)).isoformat()
                rows = daily[year][date]
                prophecy, = [r for r in rows if r['slot'] == 'OT1']
                self.assertEqual((prophecy['canonical_mt_ref'], prophecy['slot_type'], prophecy['slot_order']), (ref, 'prophecy', 1))
                self.assertEqual(rows[0], prophecy)
                if offset == -69:
                    self.assertEqual(len(rows), 8)
        # Independent literal membership oracle: no keys derived from output.
        expected = set()
        tables = {
            'Fast of Nineveh': [('Matins','OT1','Jonah 1:1-17'),('Matins','Psalm','Ps 103:1,8'),('Matins','Gospel','Matt 7:6-12'),('Liturgy','Pauline Epistle','Rom 6:17-23'),('Liturgy','Catholic Epistle','Jude 1:1-13'),('Liturgy','Acts of the Apostles','Acts 2:38-47'),('Liturgy','Psalm','Ps 130:2,4'),('Liturgy','Gospel','Matt 12:35-45')],
        }
        monday = [r for r in presentation if r['occasion'] == 'Fast of Nineveh']
        for occasion, appointments in tables.items():
            for service, slot, ref in appointments:
                expected.add((occasion, service, '', slot, design.identity_for(ref, jonah.KIND)['identity_key']))
        def subset_ledger(rows):
            self.assertEqual({design.occasion_index_key(r) for r in rows}, expected)
            self.assertEqual(len(rows), len(expected))
        with patch.object(design, 'verify_reverse_index_contract', side_effect=subset_ledger):
            reverse, disagreements = design.build_reverse_lectionary_index(monday, transport_mode='presentation')
        self.assertEqual(disagreements, [])
        self.assertEqual(next(r for r in reverse if r['slot'] == 'OT1')['slot_order'], 1)
        prophecies = [r for r in presentation if r['slot'] == 'OT1']
        prophecy_expected = {
            (occasion, 'Matins', '', 'OT1', design.identity_for(ref, jonah.KIND)['identity_key'])
            for occasion, ref in [('Fast of Nineveh', 'Jonah 1:1-17'),
                                  ("Tuesday of Ninevah's Fast", 'Jonah 2:1-10'),
                                  ("Wednesday of Ninevah's Fast", 'Jonah 3:1-4:11'),
                                  ('Entrance into the Temple', 'Jonah 2:1-10')]}
        def prophecy_ledger(rows):
            self.assertEqual({design.occasion_index_key(r) for r in rows}, prophecy_expected)
            self.assertEqual(len(rows), 4)
        with patch.object(design, 'verify_reverse_index_contract', side_effect=prophecy_ledger):
            reverse_prophecies, disagreements = design.build_reverse_lectionary_index(prophecies, transport_mode='presentation')
        self.assertEqual(disagreements, [])
        self.assertTrue(all(r['slot_type'] == 'prophecy' and r['slot_order'] == 1 for r in reverse_prophecies))
        monday_prophecy = next(r for r in reverse_prophecies if r['occasion'] == 'Fast of Nineveh')
        self.assertEqual(monday_prophecy['attestation_years'], '; '.join(map(str, range(2020, 2036))))
        with tempfile.TemporaryDirectory() as temporary, patch.object(design, 'OUT', Path(temporary)):
            schema = design.write_schema()
        self.assertIn('bounded_parallel_locus_not_exact_edition_equivalence', schema['controlled_vocabularies']['canonicalization_confidence'])

    def test_projected_row_cannot_inherit_source_privilege(self):
        _, rows = pipeline('2026-02-02')
        original = next(r for r in rows if r['reading_slot'] == 'OT1')
        for field, value in [('source_family','ordinary_date_resolved'), ('source_kind','copticchurch_date'),
                             ('source_order',2), ('source_token_order',2), ('gregorian_date','2027-02-22'),
                             ('reading_slot','OT2'), ('service_section','Vespers'), ('passage','Jonah 2:1-10'),
                             ('active',False), ('current_status','historical_witness')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                design.build_reverse_presentation([dict(original, **{field:value})])
        forged = copy.deepcopy(original)
        payload = json.loads(forged['provenance'])
        payload['consumer_source_transport']['jonah_source']['source_full_document_sha256'] = '0'*64
        forged['provenance'] = json.dumps(payload)
        with self.assertRaises(ValueError):
            design.build_reverse_presentation([forged])

    def test_design_reauthenticates_capture_after_success(self):
        _, rows = pipeline('2026-02-02')
        source = next(r for r in rows if r['reading_slot'] == 'OT1')
        design.build_reverse_presentation([source])
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'captures'
            shutil.copytree(jonah.SOURCE_ROOT, root)
            target = root / '2026-02-02/Matins/Prophecies.txt'
            target.write_bytes(target.read_bytes() + b'\nTAMPER')
            with patch.object(jonah, 'SOURCE_ROOT', root), self.assertRaises(ValueError):
                design.build_reverse_presentation([source])


if __name__ == '__main__':
    unittest.main()
