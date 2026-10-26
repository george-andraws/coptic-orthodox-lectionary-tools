"""Narrow source-coordinate Psalmody lane; never a general special-service gate."""
import ast
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class PsalmodySourceSupplements(unittest.TestCase):
    def module(self):
        try:
            import psalmody_source_supplements
        except ModuleNotFoundError:
            self.fail('Authenticated Psalmody supplement lane is not implemented')
        return psalmody_source_supplements

    def test_twelve_exact_occurrences_and_csv_contract(self):
        m = self.module()
        rows = m.load_psalmody_source_rows()
        tree = ast.parse((ROOT / 'build_lectionary_crosswalk.py').read_text())
        fields = next(ast.literal_eval(n.value) for n in tree.body
                      if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'FIELDS' for t in n.targets))
        self.assertEqual(len(rows), 12)
        expected = {'bright_saturday': [151], 'church_consecration_part1': [151, 148, 149, 150],
                    'myron_preparation': [151, 148, 149, 150], 'pentecost_prostration_praises': [148, 149, 150]}
        observed = {}
        for row in rows:
            self.assertEqual(set(row), set(fields))
            self.assertTrue(all(type(v) is str for v in row.values()))
            q = m.qualify_psalmody_row(row)
            observed.setdefault(q['rite'], []).append(q['chapter'])
            self.assertIs(q['active'], True)
            self.assertEqual(q['qualification'], 'authenticated_prescribed_psalmody_chapter_only')
            path = ROOT / row['source_file']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), q['full_capture_sha256'])
            self.assertEqual(row['raw_ref'], 'Psalm ' + str(q['chapter']))
            self.assertEqual(row['gregorian_date'], '')
            self.assertEqual(row['verse_start'], '')
            self.assertEqual(row['verse_end'], '')
        self.assertEqual(observed, expected)
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        reread = list(csv.DictReader(io.StringIO(out.getvalue())))
        self.assertEqual(rows, reread)
        for row in reread:
            m.qualify_psalmody_row(row)
        self.assertEqual(rows, m.load_psalmody_source_rows())

    def test_bright_first_slot_pascha_rule_other_rites_nondated(self):
        m = self.module()
        rows = m.load_psalmody_source_rows()
        bright = rows[0]
        q = m.qualify_psalmody_row(bright)
        self.assertEqual((bright['source_family'], bright['calendar_key'], bright['service_section'], bright['service_hour']),
                         ('bright_saturday', 'Bright Saturday', 'Midnight Praises', ''))
        self.assertEqual((bright['source_order'], bright['source_row_id']), ('0', '0'))
        self.assertEqual(q['recurrence'], {'kind': 'pascha_offset', 'offset_days': -1})
        for row in rows[1:]:
            self.assertEqual(m.qualify_psalmody_row(row)['recurrence'], {'kind': 'none'})
            self.assertNotIn('2026-10-07', row['calendar_key'])
        for rite in ('church_consecration_part1', 'myron_preparation', 'pentecost_prostration_praises'):
            fourth = [m.qualify_psalmody_row(r) for r in rows if m.qualify_psalmody_row(r)['rite'] == rite and r['reading_slot'] == 'FourthHoos']
            self.assertEqual([r['chapter'] for r in fourth], [148, 149, 150])
            self.assertEqual(len({r['source_group_key'] for r in fourth}), 1)
            self.assertEqual([r['group_order'] for r in fourth], [1, 2, 3])
        self.assertNotIn('Distribution', str(rows))

    def test_identity_is_searchable_chapter_only_not_mt_or_named_fallback(self):
        m = self.module()
        identities = {}
        for row in m.load_psalmody_source_rows():
            q = m.qualify_psalmody_row(row)
            ident = m.psalmody_identity_for(row)
            chapter = q['chapter']
            self.assertEqual(ident['reading_type'], 'scripture')
            self.assertEqual(ident['canonical_mt_ref'], '')
            self.assertEqual(ident['canonical_lxx_ref'], f'Ps {chapter}')
            self.assertNotIn('pending', ident['display_ref'].lower())
            span, = json.loads(ident['spans_json'])
            self.assertEqual((span['book'], span['chapter_start'], span['chapter_end']), ('Ps', chapter, chapter))
            self.assertIsNone(span['verse_start'])
            self.assertIsNone(span['verse_end'])
            self.assertEqual(span['canonical_mt_ref'], '')
            self.assertEqual(span['source_convention'], 'coptic_reader_psalmody_lxx_chapter_only')
            self.assertIn('not exact MT', ident['canonicalization_note'])
            if chapter == 151:
                self.assertIn('NO_MT_COUNTERPART_PSALM151', ident['canonicalization_note'])
            if chapter in identities:
                self.assertEqual(ident['identity_key'], identities[chapter])
            identities[chapter] = ident['identity_key']
        self.assertEqual(len(set(identities.values())), 4)

    def test_bounded_bodies_preserve_reader_wording_and_exclude_doxology(self):
        m = self.module()
        for row in m.load_psalmody_source_rows():
            q = m.qualify_psalmody_row(row)
            lines = (ROOT / row['source_file']).read_text().splitlines()
            self.assertEqual(lines[q['heading_line'] - 1], q['heading_exact'])
            body = '\n'.join(lines[q['body_first_line'] - 1:q['body_last_line']])
            self.assertEqual(body, q['body_literal'])
            self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), q['body_sha256'])
            if q['chapter'] == 150:
                self.assertIn('Praise God, in all His saints', body)
                self.assertNotIn('Glory to the Father', body)
            if q['chapter'] == 148:
                self.assertIn('He has ordered and they were created', body)
            if q['chapter'] == 151:
                self.assertIn('I am small among my brothers', body)
                self.assertNotIn('This Psalm is a genuine one', body)

    def test_row_counterprobes_cannot_bypass_qualification(self):
        m = self.module()
        original = m.load_psalmody_source_rows()[2]
        substitutions = {'source_family': 'bright_saturday', 'source_kind': 'special_service',
                         'service_section': 'Distribution', 'calendar_key': '2026-10-07',
                         'source_order': '1', 'source_file': '../wrong.txt',
                         'passage': 'Ps 148:1-14', 'verse_end': '14', 'raw_ref': 'Psalm 151'}
        for field, value in substitutions.items():
            row = dict(original, **{field: value})
            with self.subTest(field=field), self.assertRaises(ValueError):
                m.qualify_psalmody_row(row)
        for field, value in [('heading_line', 1148), ('body_literal', 'substituted'),
                             ('stage', 'Part 2'), ('active', False), ('active', 1),
                             ('chapter', 147), ('full_capture_sha256', '0' * 64)]:
            row = copy.deepcopy(original)
            envelope = json.loads(row['provenance'])
            envelope[field] = value
            row['provenance'] = json.dumps(envelope, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            with self.subTest(envelope_field=field), self.assertRaises(ValueError):
                m.psalmody_identity_for(row)
        for field, value in [('active', False), ('state', 'superseded'), ('include_in_current_index', False)]:
            with self.subTest(lifecycle_field=field), self.assertRaises(ValueError):
                m.qualify_psalmody_row(dict(original, **{field: value}))
        with self.assertRaises(ValueError):
            m.qualify_psalmody_row({'passage': 'Ps 151', 'source_kind': m.SOURCE_KIND})

    def test_full_capture_and_manifest_drift_fail_closed(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'fixture'
            shutil.copytree(m.SOURCE_ROOT, root)
            self.assertEqual(len(m.load_psalmody_source_rows(root)), 12)
            doc = root / 'bright-saturday-midnight-praises.full.txt'
            original = doc.read_bytes()
            doc.write_bytes(original + b'\nsubstitution beyond selected block')
            with self.assertRaises(ValueError):
                m.load_psalmody_source_rows(root)
            doc.write_bytes(original)
            doc.unlink()
            with self.assertRaises(ValueError):
                m.load_psalmody_source_rows(root)
        for mutation in ('duplicate', 'missing', 'inactive', 'shifted', 'wrongstage'):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / 'fixture'
                shutil.copytree(m.SOURCE_ROOT, root)
                path = root / 'source-manifest.json'
                manifest = json.loads(path.read_bytes())
                if mutation == 'duplicate':
                    manifest['records'].append(copy.deepcopy(manifest['records'][0]))
                elif mutation == 'missing':
                    manifest['records'].pop()
                elif mutation == 'inactive':
                    manifest['records'][0]['active'] = False
                elif mutation == 'shifted':
                    manifest['records'][0]['heading_line'] += 1
                else:
                    manifest['documents'][0]['stage'] = 'Matins'
                path.write_text(json.dumps(manifest))
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    m.load_psalmody_source_rows(root)
                # Independent of the outer trust pin, semantic guards must also
                # reject broken bounds/lifecycle/occurrence shape. Rebinding is
                # test-only; production never accepts a caller-provided pin.
                with patch.object(m, 'MANIFEST_SHA256', hashlib.sha256(path.read_bytes()).hexdigest()):
                    with self.subTest(semantic_guard=mutation), self.assertRaises(ValueError):
                        m.load_psalmody_source_rows(root)

    def test_previously_loaded_row_is_reauthenticated_after_disk_drift(self):
        m = self.module()
        rows = m.load_psalmody_source_rows()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'fixture'
            shutil.copytree(m.SOURCE_ROOT, root)
            with patch.object(m, 'SOURCE_ROOT', root):
                m.qualify_psalmody_row(rows[0])
                doc = root / 'myron-preparation.full.txt'
                doc.write_bytes(doc.read_bytes() + b'changed')
                with self.assertRaises(ValueError):
                    m.qualify_psalmody_row(rows[0])


if __name__ == '__main__':
    unittest.main()
