"""Candidate boundary regressions independent of generated fixtures."""
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('integrity', ROOT / 'scripts/verify_package_integrity.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class CandidateValidation(unittest.TestCase):
    def span(self, book='Jn', cs=21, vs=34, ce=21, ve=38):
        return dict(book=book, chapter_start=cs, verse_start=vs, chapter_end=ce, verse_end=ve)

    def test_impossible_john_verses_rejected(self):
        self.assertEqual(v.validate_reference_span(self.span())['status'], 'fail')

    def test_cross_chapter_bounds_and_order(self):
        self.assertEqual(v.validate_reference_span(self.span('Jn', 3, 16, 4, 10))['status'], 'pass')
        self.assertEqual(v.validate_reference_span(self.span('Jn', 4, 10, 3, 16))['status'], 'fail')
        self.assertEqual(v.validate_reference_span(self.span('Jn', 3, 16, 22, 1))['status'], 'fail')
        self.assertEqual(v.validate_reference_span(self.span('Jn', 3, 0, 3, 16))['status'], 'fail')

    def test_canonical_system_not_silently_guessed(self):
        for book, chapter in [('Ps', 151), ('Dan', 13), ('Sir', 51)]:
            self.assertEqual(v.validate_reference_span(self.span(book, chapter, 1, chapter, 2))['status'], 'unverified')

    def test_numbering_difference_is_not_an_impossible_reference(self):
        span = self.span("3Jn", 1, 10, 1, 15)
        span["source_convention"] = "modern_english_reference"
        self.assertEqual(v.validate_reference_span(span)["status"], "unverified")
        span["source_convention"] = "kjv"
        self.assertEqual(v.validate_reference_span(span)["status"], "fail")

    def test_named_readings_do_not_require_scripture_spans(self):
        self.assertEqual(v.validate_row_reference_bounds({"reading_type": "named-reading", "reading_name": "Memoirs of Job", "spans_json": "[]"})["failures"], [])

    def test_numeric_types_are_not_coerced(self):
        for value in [True, 1.5, 'three', None]:
            self.assertEqual(v.validate_reference_span(self.span(cs=value))['status'], 'fail')

    def test_real_gregorian_dates(self):
        for text in ['2026-02-29', '2026-04-31', '2026-13-01', '0000-01-01', '2026-1-01']:
            self.assertFalse(v.is_real_iso_date(text), text)
        self.assertTrue(v.is_real_iso_date('2028-02-29'))

    def test_explicit_mt_old_testament_bounds_without_lxx_coercion(self):
        span = self.span('Ps', 42, 5, 42, 5)
        span['source_convention'] = 'mt_nkjv'
        self.assertEqual(v.validate_reference_span(span)['status'], 'pass')
        span['verse_end'] = 500
        self.assertEqual(v.validate_reference_span(span)['status'], 'fail')
        span['source_convention'] = 'lxx_liturgical'
        self.assertEqual(v.validate_reference_span(span)['status'], 'unverified')

    def test_daily_join_rejects_tampered_reference_and_other_occasion(self):
        reverse = {'identity_key':'x', 'display_ref':'Jn 1:1-17', 'occasion':'Monday', 'service_section':'Sixth Hour', 'slot':'Gospel'}
        self.assertEqual(v.reverse_matches_for_daily(reverse, [reverse]), [reverse])
        for changed in ({'display_ref':'Jn 21:34-38'}, {'occasion':'Monday Eve'}, {'service_section':'Ninth Hour'}, {'slot':'Psalm'}):
            with self.subTest(changed=changed):
                self.assertEqual(v.reverse_matches_for_daily(dict(reverse, **changed), [reverse]), [])

    def test_missing_node_cannot_pass_release_gate(self):
        from unittest.mock import patch
        with patch.object(v.subprocess, 'run', side_effect=FileNotFoundError):
            self.assertEqual(v.validate_commonjs_exports(ROOT)['status'], 'fail')

    def test_tarball_matching_names_different_bytes_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            package = root / 'candidate'
            package.mkdir()
            (package / 'index.js').write_text('approved')
            tgz = root / 'candidate.tgz'
            with tarfile.open(tgz, 'w:gz') as arc:
                data = b'unreviewed'
                info = tarfile.TarInfo('package/index.js')
                info.size = len(data)
                arc.addfile(info, io.BytesIO(data))
            result = v.compare_tarball_bytes(package, tgz)
            self.assertEqual(result['status'], 'fail')
            self.assertEqual(result['mismatched'], ['index.js'])


if __name__ == '__main__':
    unittest.main()
