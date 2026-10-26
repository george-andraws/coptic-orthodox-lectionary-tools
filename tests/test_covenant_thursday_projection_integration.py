"""Bounded real raw/CSV/design pipeline; no production ledger bypass."""
import copy
import csv
import datetime as dt
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_crosswalk as crosswalk
import build_design_deliverables as design
import covenant_thursday_source_supplements as covenant

# Literal appointment/fragment oracle, independent of the loader and projection.
TABLE = {
    'Liturgy': [
        ('Pauline', '1 Corinthians 11:23-34', '1Cor 11:23-34', '1Cor 11:23-34'),
        ('Psalm', 'Psalms 22:5;40:9', 'Ps 23:5', 'Ps 22:5'),
        ('Psalm', 'Psalms 22:5;40:9', 'Ps 41:9', 'Ps 40:10'),
        ('Gospel', 'Matthew 26:20-29', 'Matt 26:20-29', 'Matt 26:20-29')],
    'Liturgy of Blessing of the Water': [
        ('OT1', 'Genesis 18:1-23', 'Gen 18:1-23', 'Gen 18:1-23'),
        ('OT2', 'Proverbs 9:1-11', 'Prov 9:1-11', 'Prov 9:1-11'),
        ('OT3', 'Exodus from 14, 15', '', ''),
        ('OT4', 'Joshua from 1, 3', '', ''),
        ('OT5', 'Isaiah 4:2-4', 'Isa 4:2-4', 'Isa 4:2-4'),
        ('OT6', 'Isaiah 55:1-56:1', 'Isa 55:1-56:1', 'Isa 55:1-56:1'),
        ('OT7', 'Ezekiel 36:25-29', 'Ezek 36:25-29', 'Ezek 36:25-29'),
        ('OT8', 'Ezekiel 47:1-9', 'Ezek 47:1-9', 'Ezek 47:1-9'),
        ('Pauline', '1 Timothy 4:9-5:10', '1Tim 4:9-5:10', '1Tim 4:9-5:10'),
        ('Psalm', 'Psalms 51:7, 10', 'Ps 51:7', 'Ps 50:9'),
        ('Psalm', 'Psalms 51:7, 10', 'Ps 51:10', 'Ps 50:12'),
        ('Gospel', 'John 13:1-17', 'Jn 13:1-17', 'Jn 13:1-17')],
}


def raw_csv():
    rows = crosswalk.load_covenant_thursday_source_rows()
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, crosswalk.FIELDS)
    writer.writeheader(); writer.writerows(rows)
    buffer.seek(0)
    transported = list(csv.DictReader(buffer))
    if transported != rows:
        raise AssertionError('raw CSV transport changed exact source rows')
    return transported


class CovenantThursdayProjection(unittest.TestCase):
    def test_real_crosswalk_loader_csv_and_design_exact_subset(self):
        raw = raw_csv()
        self.assertEqual(raw, covenant.load_covenant_thursday_rows())
        self.assertEqual(len(raw), 16)
        presentation, _ = design.build_reverse_presentation(raw)
        for section, expected in TABLE.items():
            actual = [r for r in presentation if r['service_section'] == section]
            self.assertEqual([(r['slot'], r['source_label'], r['canonical_mt_ref'], r['canonical_lxx_ref']) for r in actual], expected)
        for source, row in zip(raw, presentation):
            q = covenant.qualify_covenant_thursday_row(source)
            self.assertEqual(row['source_key'], 'coptic_reader_qualified_covenant_thursday')
            self.assertEqual(row['current_status'], 'current_public_or_local_reference')
            self.assertIn('source-qualified', row['source_title'])
            self.assertIn(q['full_capture_sha256'], row['source_locator'])
            self.assertIn(q['body_envelope_sha256'], row['source_locator'])
            self.assertIn('lines ', row['source_locator'])
            self.assertEqual(json.loads(row['provenance']), q)
            self.assertFalse(q['runtime_activation_approved'])
            self.assertFalse(q['fresh_app_verification'])
            self.assertFalse(q['old_receipts_grant_activation'])
            if not row['canonical_mt_ref']:
                self.assertEqual(json.loads(row['spans_json']), [])
                self.assertEqual(row['reading_type'], 'scripture')
            else:
                self.assertEqual(row['canonicalization_note'], q['coordinate_note'])
        # Only the whole-corpus guard is substituted, with literal exact members.
        expected_keys = set()
        for section, appointments in TABLE.items():
            for slot, printed, mt, lxx in appointments:
                material = 'scripture|' + mt + '|' + lxx if mt else 'scripture_named_excerpt|' + printed
                import hashlib
                identity = 'rid_' + hashlib.sha256(material.encode()).hexdigest()[:20]
                expected_keys.add(('the Covenant Thursday' if section == 'Liturgy' else 'Great Thursday', section, section, slot, identity))
        def exact_subset(rows):
            self.assertEqual(len(rows), 16)
            self.assertEqual({design.occasion_index_key(r) for r in rows}, expected_keys)
        with patch.object(design, 'verify_reverse_index_contract', side_effect=exact_subset):
            reverse, disagreements = design.build_reverse_lectionary_index(presentation, transport_mode='presentation')
        self.assertEqual(disagreements, [])
        self.assertEqual(len(reverse), 16)
        for row in reverse:
            disclosure, = json.loads(row['source_disclosure'])
            self.assertIn('sha256=', disclosure['source_locator'])
            self.assertIn('not fresh app verification', disclosure['source_edition'])
            self.assertTrue(json.loads(row['provenance'])['body_envelope_literal'])

    def test_crosswalk_main_reaches_real_loader_without_generated_writes(self):
        captured = {}
        def collect(path, rows, fields):
            captured[path.name] = copy.deepcopy(rows)
        with tempfile.TemporaryDirectory() as td, \
                patch.object(crosswalk, 'OUT', Path(td)), \
                patch.object(crosswalk, 'WORK_OUT_DATA', Path(td)), \
                patch.object(crosswalk, 'DISABLE_VAULT_PUBLISH', True), \
                patch.object(crosswalk, 'read_csv', return_value=[]), \
                patch.object(crosswalk, 'project_bright_rows', return_value=[]), \
                patch.object(crosswalk, 'write_csv', side_effect=collect), \
                patch.object(crosswalk, 'write_jsonl'), \
                patch.object(crosswalk.shutil, 'copy2'), patch('builtins.print'):
            crosswalk.main()
        typed = [r for r in captured['reverse_lookup_crosswalk.csv'] if r['source_kind'] == covenant.SOURCE_KIND]
        self.assertEqual(sorted(typed, key=lambda r: (r['service_section'], int(r['source_order']), int(r['source_token_order']))),
                         sorted(covenant.load_covenant_thursday_rows(), key=lambda r: (r['service_section'], int(r['source_order']), int(r['source_token_order']))))
        self.assertEqual(sum(r['total_occurrences'] for r in captured['reverse_lookup_summary.csv']), 28)

    def test_default_design_loader_uses_csv_rows_without_relabeling(self):
        with patch.object(design, 'read_csv', return_value=raw_csv()), \
                patch.object(design, 'load_removed_pascha_source_text_supplement', return_value=[]), \
                patch.object(design, 'load_fixture_rows', return_value=[]), \
                patch.object(design, 'hosanna_sunday_reader_prophecy_rows', return_value=[]):
            presentation, _ = design.build_reverse_presentation()
        self.assertEqual(len(presentation), 16)
        self.assertTrue(all(r['source_key'] == 'coptic_reader_qualified_covenant_thursday' for r in presentation))
        # The independent production global ledger is intentionally not relaxed.
        with self.assertRaisesRegex(AssertionError, 'intended source ledger'):
            design.verify_reverse_index_contract(presentation)

    def test_named_excerpt_confidence_is_declared_by_schema(self):
        with tempfile.TemporaryDirectory() as td, patch.object(design, 'OUT', Path(td)):
            schema = design.write_schema()
        self.assertIn('source_qualified_named_excerpt', schema['controlled_vocabularies']['canonicalization_confidence'])

    def test_generic_kind_does_not_promote_another_held_appointment(self):
        row = dict(covenant.load_covenant_thursday_rows()[0],
                   source_file='held-other.txt', source_table='held-other', provenance='',
                   day_title='Unreviewed service', calendar_key='Unreviewed service',
                   liturgical_place='Unreviewed service')
        presentation, _ = design.build_reverse_presentation([row])
        self.assertEqual(presentation[0]['current_status'], 'unknown')
        self.assertNotEqual(presentation[0]['source_key'], 'coptic_reader_qualified_covenant_thursday')

    def test_daily_recurrence_exact_dates_and_separate_existing_hour(self):
        presentation, _ = design.build_reverse_presentation(raw_csv())
        hour = dict(design.identity_for('Matt 26:17-19', 'pascha_day_hour'),
                    occasion='Great Thursday', day_title='Great Thursday',
                    service_section='First Hour', service_hour='First Hour', slot='Gospel',
                    gregorian_date='2026-04-09', source_kind='pascha_day_hour',
                    source_family='holy_pascha_curated_day_hour', current_status='current_working_source_not_coptic_reader_checked')
        daily = design.build_daily_year_files(presentation + [hour], transport_mode='presentation')
        for year, date in [(2026, '2026-04-09'), (2027, '2027-04-29'), (2028, '2028-04-13')]:
            rows = daily[year][date]
            qualified = [r for r in rows if r['source_kind'] == covenant.SOURCE_KIND]
            self.assertEqual(len(qualified), 16)
            for section, expected in TABLE.items():
                actual = [r for r in qualified if r['service_section'] == section]
                self.assertEqual([(r['slot'], r['canonical_mt_ref'], r['canonical_lxx_ref']) for r in actual], [(s, mt, lxx) for s, _, mt, lxx in expected])
            for row in qualified:
                disclosure, = json.loads(row['source_disclosure'])
                self.assertIn('sha256=', disclosure['source_locator'])
                self.assertEqual(row['slot_type'], 'prophecy' if row['slot'].startswith('OT') else row['slot'].lower())
                self.assertGreater(row['slot_order'], 0)
            if year == 2026:
                self.assertEqual(len([r for r in rows if r['service_hour'] == 'First Hour']), 1)
        self.assertEqual(set(daily), {2026, 2027, 2028})

    def test_design_rejects_raw_context_and_metadata_tampering(self):
        original = covenant.load_covenant_thursday_rows()[0]
        for field, value in [('source_kind', 'pascha_day_hour'), ('source_family', 'holy_pascha_curated_day_hour'), ('day_title', 'Great Friday'), ('service_hour', 'Sixth Hour'), ('service_section', 'Sixth Hour'), ('source_row_id', '2'), ('source_order', '2'), ('source_token_order', '2'), ('source_file', 'forged.txt'), ('raw_ref', '1 Corinthians 11'), ('normalized_ref', '1Cor 11'), ('gregorian_date', '2027-04-29')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                design.build_reverse_presentation([dict(original, **{field: value})])
        for field, value in [('runtime_activation_approved', True), ('fresh_app_verification', True), ('full_capture_sha256', '0'*64), ('active', False)]:
            bad = copy.deepcopy(original)
            q = json.loads(bad['provenance']); q[field] = value
            bad['provenance'] = json.dumps(q)
            with self.subTest(metadata=field), self.assertRaises(ValueError):
                design.build_reverse_presentation([bad])
        with self.assertRaises(ValueError):
            design.build_reverse_presentation([dict(original, active='false')])

    def test_design_freshly_authenticates_source_files_after_success(self):
        row = covenant.load_covenant_thursday_rows()[0]
        design.build_reverse_presentation([row])
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'pack'
            shutil.copytree(covenant.SOURCE_ROOT, root)
            manifest = json.loads((root / 'source-contract.json').read_text())
            targets = [manifest['documents'][0]['file'], 'thursday--context.json', 'old-review-receipt.json']
            with patch.object(covenant, 'SOURCE_ROOT', root):
                for relative in targets:
                    target = root / relative
                    original = target.read_bytes(); target.write_bytes(original + b'\nTAMPER')
                    with self.subTest(file=relative), self.assertRaises(ValueError):
                        design.build_reverse_presentation([row])
                    target.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
