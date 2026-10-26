"""Portable retained-source authentication; never read the original audit archive."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path('sources/coptic-reader/pascha-resolution-qualified-2026-10-25')
EXPECTED = {
    'good_friday_twelfth': ('friday--12th-hour.txt', '9a6bd0b11b67fa6d3cfbe10a99b84a085796b8b3e886ddec4d191ef02dbe2e0e'),
    'hosanna_sunday_day_ninth': ('Sunday--Sunday_Day--9th_Hour.txt', 'ea7e186ff09fe3ab46ee4dc16aa7ba6e4a740060d714bec78aaf30ea49bebd74'),
    'bright_saturday_matins': ('saturday--matins.txt', 'eb373a8c80ae9fcb658c1726c38a1815281a078217a5d61e1bb305b08cedbb7f'),
}


class PaschaResolutionEvidence(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT / 'pascha_resolution_evidence.py').is_file(),
                        'Portable authenticated Pascha evidence helper is missing')
        self.tmp = tempfile.TemporaryDirectory(prefix='pascha-evidence-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'portable-repo'
        self.root.mkdir()
        shutil.copy2(ROOT / 'pascha_resolution_evidence.py', self.root)
        shutil.copytree(ROOT / RELATIVE, self.root / RELATIVE)
        spec = importlib.util.spec_from_file_location('portable_pascha', self.root / 'pascha_resolution_evidence.py')
        assert spec is not None and spec.loader is not None
        self.helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.helper)
        self.manifest_path = self.root / RELATIVE / 'source-manifest.json'
        self.manifest = json.loads(self.manifest_path.read_bytes())

    def document(self, key):
        return self.manifest['documents'][key]

    def capture(self, key):
        return self.root / RELATIVE / self.document(key)['file']

    def rewrite_manifest(self):
        self.manifest_path.write_text(json.dumps(self.manifest), encoding='utf-8')

    def test_exact_three_captures_context_and_qualifications(self):
        self.assertEqual(set(self.manifest['documents']), set(EXPECTED))
        for key, (filename, sha) in EXPECTED.items():
            with self.subTest(key=key):
                result = self.helper.authenticate_pascha_evidence(key)
                self.assertEqual(result['key'], key)
                self.assertEqual(Path(result['path']).name, filename)
                self.assertFalse(Path(result['path']).is_absolute())
                self.assertEqual(result['sha256'], sha)
                self.assertIn(result['path'], result['locator'])
                self.assertIn(sha, result['locator'])
                self.assertEqual(hashlib.sha256((self.root / result['path']).read_bytes()).hexdigest(), sha)
                self.assertTrue(result['qualification_notes'])
                self.assertFalse(result['fresh_app_verification'])
                self.assertFalse(result['new_appointment_approval'])
                self.assertIsNone(result['app_version'])
                self.assertIsNone(result['capture_time'])
                self.assertTrue(result['companions'])
        friday = self.helper.authenticate_pascha_evidence('good_friday_twelfth')
        self.assertEqual(friday['readings'][0]['heading_exact'], '\tLamentations 3:1-66')
        self.assertIn('no Jonah', friday['qualification_notes'])
        hosanna = self.helper.authenticate_pascha_evidence('hosanna_sunday_day_ninth')
        self.assertEqual(hosanna['readings'][0]['heading_exact'], '\tLamentations 1:1-4')
        self.assertIn('not 1:1-5', hosanna['qualification_notes'])
        self.assertEqual(hosanna['service_day'], 'Hosanna Sunday')
        self.assertEqual(hosanna['service_hour'], 'Ninth Hour')
        bright = self.helper.authenticate_pascha_evidence('bright_saturday_matins')
        self.assertEqual(bright['document_title'], 'Offering of Morning Incense')
        self.assertIn('\t1 Corinthians 5:7-13', [r['heading_exact'] for r in bright['readings']])
        self.assertIn('not 1 Corinthians 1:1-19', bright['qualification_notes'])

    def test_keys_are_exact_strings_not_paths_aliases_or_coercible_objects(self):
        class StringSubclass(str):
            pass
        for key in [None, True, 0, [], {}, Path('good_friday_twelfth'),
                    StringSubclass('good_friday_twelfth'), '../good_friday_twelfth',
                    'good_friday_twelfth ', 'GOOD_FRIDAY_TWELFTH', 'monday_eve_ninth', '']:
            with self.subTest(key=repr(key)), self.assertRaises(ValueError):
                self.helper.authenticate_pascha_evidence(key)

    def test_full_document_drift_missing_and_context_truncation_fail_closed(self):
        for key in EXPECTED:
            path = self.capture(key)
            original = path.read_bytes()
            for changed in [original + b'\n', original.split(b'\n', 1)[1], original[:1000], b'X' + original[1:]]:
                with self.subTest(key=key, size=len(changed)):
                    path.write_bytes(changed)
                    with self.assertRaises(ValueError):
                        self.helper.authenticate_pascha_evidence(key)
                    path.write_bytes(original)
            path.unlink()
            with self.assertRaises(ValueError):
                self.helper.authenticate_pascha_evidence(key)
            path.write_bytes(original)

    def test_all_retained_companions_are_authenticated_on_every_call(self):
        for key in EXPECTED:
            self.helper.authenticate_pascha_evidence(key)
            for companion in self.document(key)['companions']:
                path = self.root / RELATIVE / companion['file']
                original = path.read_bytes()
                path.write_bytes(original + b'altered')
                with self.subTest(key=key, file=companion['file']), self.assertRaises(ValueError):
                    self.helper.authenticate_pascha_evidence(key)
                path.write_bytes(original)

    def test_self_consistent_rehash_cannot_rebind_title_hour_or_literal_readings(self):
        original_manifest = self.manifest_path.read_bytes()
        key = 'hosanna_sunday_day_ninth'
        original_capture = self.capture(key).read_bytes()
        for old, new in [(b'Hosanna Sunday', b'Monday Eve'), (b'Ninth Hour', b'Eleventh Hour'),
                         (b'Lamentations 1:1-4', b'Lamentations 1:1-5')]:
            self.manifest = json.loads(original_manifest)
            changed = original_capture.replace(old, new)
            self.capture(key).write_bytes(changed)
            self.document(key)['sha256'] = hashlib.sha256(changed).hexdigest()
            self.document(key)['bytes'] = len(changed)
            self.rewrite_manifest()
            with self.subTest(new=new), self.assertRaises(ValueError):
                self.helper.authenticate_pascha_evidence(key)
        self.capture(key).write_bytes(original_capture)

    def test_manifest_rebinding_paths_qualifications_and_unknown_keys_rejected(self):
        original = self.manifest_path.read_bytes()
        mutations = [lambda d: d.update(file='../outside.txt'),
                     lambda d: d.update(file='/outside.txt'),
                     lambda d: d.update(service_hour='First Hour'),
                     lambda d: d.update(qualification_notes='fresh app approval'),
                     lambda d: d['readings'][0].update(heading_exact='\tLamentations 1:1-5')]
        for mutate in mutations:
            self.manifest = json.loads(original)
            mutate(self.document('hosanna_sunday_day_ninth'))
            self.rewrite_manifest()
            with self.assertRaises(ValueError):
                self.helper.authenticate_pascha_evidence('hosanna_sunday_day_ninth')
        self.manifest = json.loads(original)
        self.manifest['documents']['invented_appointment'] = self.document('good_friday_twelfth')
        self.rewrite_manifest()
        with self.assertRaises(ValueError):
            self.helper.authenticate_pascha_evidence('good_friday_twelfth')

    def test_symlink_escape_is_rejected_even_for_identical_bytes(self):
        path = self.capture('good_friday_twelfth')
        outside = Path(self.tmp.name) / 'outside.txt'
        shutil.copy2(path, outside)
        path.unlink()
        path.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.helper.authenticate_pascha_evidence('good_friday_twelfth')

    def test_symlink_parent_and_manifest_are_rejected(self):
        directory = self.capture('good_friday_twelfth').parent
        moved = Path(self.tmp.name) / 'moved-captures'
        directory.rename(moved)
        directory.symlink_to(moved, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.helper.authenticate_pascha_evidence('good_friday_twelfth')
        directory.unlink()
        moved.rename(directory)
        outside = Path(self.tmp.name) / 'manifest.json'
        shutil.copy2(self.manifest_path, outside)
        self.manifest_path.unlink()
        self.manifest_path.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.helper.authenticate_pascha_evidence('good_friday_twelfth')

    def test_returned_metadata_cannot_poison_later_authentication(self):
        result = self.helper.authenticate_pascha_evidence('good_friday_twelfth')
        result['readings'][0]['heading_exact'] = 'Jonah 1:10-2:8'
        result['sha256'] = 'forged'
        again = self.helper.authenticate_pascha_evidence('good_friday_twelfth')
        self.assertEqual(again['sha256'], EXPECTED['good_friday_twelfth'][1])
        self.assertEqual(again['readings'][0]['heading_exact'], '\tLamentations 3:1-66')

    def test_copied_repository_runs_offline_with_unrelated_cwd_and_absent_home(self):
        env = dict(os.environ, HOME=str(Path(self.tmp.name) / 'nonexistent-home'),
                   PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(self.root))
        code = ('from pascha_resolution_evidence import authenticate_pascha_evidence as a; '
                'print([a(k)["sha256"] for k in ' + repr(list(EXPECTED)) + '])')
        run = subprocess.run([sys.executable, '-c', code], env=env, cwd=self.tmp.name,
                             text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        for _, sha in EXPECTED.values():
            self.assertIn(sha, run.stdout)
        self.assertFalse(Path(env['HOME']).exists())


if __name__ == '__main__':
    unittest.main()
