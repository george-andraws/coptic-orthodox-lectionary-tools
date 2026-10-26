"""Real no-service crosswalk witnesses must never mint chapter appointments."""
import contextlib
import copy
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_bible_chapter_lectionary_index as builder
import build_lectionary_crosswalk as crosswalk
import covenant_thursday_source_supplements as covenant
import no_service_history as history
import verify_lectionary_queries as verifier

ROOT = Path(__file__).resolve().parents[1]


def write_rows(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class NoServiceArchiveChapterExclusion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archives = crosswalk.project_no_service_history(history.authenticated_raw_rows())
        with (ROOT / 'out/data/reverse_lookup_crosswalk.csv').open(newline='', encoding='utf-8') as handle:
            produced = [r for r in csv.DictReader(handle) if history.is_archive(r)]
        assert len(cls.archives) == len(produced) == 32
        assert sorted(cls.archives, key=lambda r: r['source_row_id']) == sorted(produced, key=lambda r: r['source_row_id'])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)

    def sources(self, rows):
        fields = list(dict.fromkeys(k for row in rows for k in row))
        write_rows(self.data / 'reverse_lookup_crosswalk.csv', rows, fields)

    def build(self, rows):
        self.sources(rows)
        with patch.object(builder, 'DATA', self.data), patch.object(builder, 'DISABLE_VAULT_PUBLISH', True), contextlib.redirect_stdout(io.StringIO()):
            builder.main()
        with (self.data / 'bible_chapter_lectionary_occurrences.csv').open(newline='', encoding='utf-8') as handle:
            return list(csv.DictReader(handle))

    def check_chapters(self):
        with patch.object(verifier, 'DATA', self.data):
            return verifier.assert_chapter_occurrence_row_count()

    def check_spans(self):
        with patch.object(verifier, 'DATA', self.data):
            return verifier.assert_reverse_crosswalk_spans_valid()

    @staticmethod
    def controls():
        base = dict(passage='Exod 4:19-6:13', source_kind='copticchurch_date',
                    source_family='ordinary_date_resolved', source_ref='Exodus 4:19-6:13',
                    service_section='Matins', reading_type='Prophecy', url='ordinary-control')
        return [dict(base, provenance=json.dumps({'consumer_source_transport': {'state': {'current_status': 'current_public_or_local_reference'}}})),
                dict(base, provenance=json.dumps({'consumer_source_transport': {'state': {'current_status': 'historical_candidate_removed'}}}), url='approved-historical-control')]

    def test_all_32_real_archives_produce_zero_numeric_occurrences(self):
        before = copy.deepcopy(self.archives)
        raw = json.dumps(before, sort_keys=True)
        self.assertTrue(any(builder.chapter_keys_for_passage(r['passage']) for r in before))
        self.assertIn('Lk 10:38-52', [r['passage'] for r in before])
        self.assertIn('Psalm 32:11  &  33:1  &  32:6', [r['source_ref'] for r in before])
        self.assertEqual(self.build(before), [])
        self.assertEqual(self.check_chapters()['chapter_occurrence_rows'], 0)
        self.assertEqual(json.dumps(before, sort_keys=True), raw)
        with (self.data / 'reverse_lookup_crosswalk.csv').open(newline='', encoding='utf-8') as handle:
            self.assertEqual(list(csv.DictReader(handle)), before)

    def test_independent_counter_accepts_all_32_without_parsing_composite(self):
        self.sources(self.archives)
        write_rows(self.data / 'bible_chapter_lectionary_occurrences.csv', [], builder.DETAIL_FIELDS)
        self.assertEqual(self.check_chapters()['chapter_occurrence_rows'], 0)

    def test_span_validator_counts_archives_separately_from_named_covenant(self):
        named = [r for r in covenant.load_covenant_thursday_rows() if not r['normalized_ref']]
        self.sources(self.archives + named + self.controls())
        result = self.check_spans()
        self.assertEqual(result['qualified_archive_source_only_rows'], 32)
        self.assertEqual(result['qualified_unaddressable_rows'], 2)
        self.assertEqual(result['parsed_rows'], 2)
        self.assertEqual(result['reverse_crosswalk_rows'], 36)

    def test_current_and_other_historical_numeric_controls_unchanged(self):
        rows = self.build(self.archives + self.controls())
        self.assertEqual(len(rows), 6)
        self.assertEqual({r['chapter'] for r in rows}, {'4', '5', '6'})
        self.assertEqual({r['url'] for r in rows}, {'ordinary-control', 'approved-historical-control'})
        self.assertEqual(self.check_chapters()['chapter_occurrence_rows'], 6)

    def test_independent_counter_rejects_injected_archive_even_at_same_total(self):
        self.build(self.archives + self.controls())
        self.check_chapters()  # Successful control precedes each mutation.
        with (self.data / 'bible_chapter_lectionary_occurrences.csv').open(newline='', encoding='utf-8') as handle:
            valid = list(csv.DictReader(handle))
        for archive in self.archives:
            book, chapter = (builder.chapter_keys_for_passage(archive['passage']) or [('Ps', 32)])[0]
            injected = {field: archive.get(field, '') for field in builder.DETAIL_FIELDS}
            injected.update(book_abbrev=book, chapter=str(chapter), chapter_ref=f'{book} {chapter}')
            for rows in (valid + [injected], valid[:-1] + [injected]):
                with self.subTest(witness=archive['source_row_id'], count=len(rows)):
                    write_rows(self.data / 'bible_chapter_lectionary_occurrences.csv', rows, builder.DETAIL_FIELDS)
                    with self.assertRaises(AssertionError) as caught:
                        self.check_chapters()
                    self.assertIn('extra', str(caught.exception))
                    self.assertIn(archive['passage'], str(caught.exception))

    def test_all_boundaries_reject_projected_forgeries_before_parse(self):
        mutations = [('source_family', 'ordinary_date_resolved'), ('source_kind', 'katameros_cycle'),
                     ('chapter_start', '10'), ('normalized_ref', 'Lk 10:38-42'),
                     ('service_section', 'Matins'), ('gregorian_date', '2020-02-11'),
                     ('source_ref', 'Lk 10:38-42'), ('passage', 'Lk 10:38-42'),
                     ('significance_note', ''), ('provenance', '{}'), ('active', 'True')]
        for field, value in mutations:
            rows = copy.deepcopy(self.archives)
            rows[0][field] = value
            for caller in ('builder', 'chapter', 'span'):
                with self.subTest(field=field, caller=caller), self.assertRaisesRegex(ValueError, 'No-service archive'):
                    if caller == 'builder':
                        self.build(rows)
                    else:
                        self.sources(rows)
                        write_rows(self.data / 'bible_chapter_lectionary_occurrences.csv', [], builder.DETAIL_FIELDS)
                        (self.check_chapters if caller == 'chapter' else self.check_spans)()

    def test_compound_marker_stripping_all_32_rejected_before_parse(self):
        for archive in self.archives:
            mutant = dict(archive, source_family='ordinary_date_resolved', source_row_id='',
                          provenance='{}', superseded_reason='')
            for caller in ('builder', 'chapter', 'span'):
                with self.subTest(witness=archive['source_row_id'], caller=caller):
                    self.sources([mutant])
                    write_rows(self.data / 'bible_chapter_lectionary_occurrences.csv', [], builder.DETAIL_FIELDS)
                    with self.assertRaisesRegex(ValueError, 'No-service archive'):
                        if caller == 'builder':
                            self.build([mutant])
                        else:
                            (self.check_chapters if caller == 'chapter' else self.check_spans)()

    def test_compound_forgeries_retain_any_existing_ref_and_slot(self):
        archive = next(r for r in self.archives if r['passage'] == 'Lk 10:38-52')
        ref_fields = ('source_ref', 'raw_ref', 'passage', 'normalized_ref', 'normalized_segment')
        for retained in ref_fields:
            mutant = dict(archive, source_family='ordinary_date_resolved', source_row_id='',
                          provenance='{}', superseded_reason='', source_kind='katameros_cycle',
                          day_title='Great Lent', calendar_key='forged', active='True', chapter_start='10')
            for field in ref_fields:
                mutant[field] = 'Lk 10:38-42'
            mutant[retained] = archive[retained]
            mutant['reading_type'] = 'forged'  # The retained reading_slot still identifies the source.
            for caller in ('builder', 'chapter', 'span'):
                with self.subTest(retained=retained, caller=caller):
                    self.sources([mutant])
                    write_rows(self.data / 'bible_chapter_lectionary_occurrences.csv', [], builder.DETAIL_FIELDS)
                    with self.assertRaisesRegex(ValueError, 'No-service archive'):
                        if caller == 'builder':
                            self.build([mutant])
                        else:
                            (self.check_chapters if caller == 'chapter' else self.check_spans)()

    def test_typed_proof_forgeries_rejected_at_all_boundaries(self):
        for field, value in [('source_order', 1), ('source_token_order', True), ('active', False)]:
            mutant = dict(self.archives[0], **{field: value})
            # Direct boundary input preserves Python types instead of CSV coercion.
            for caller in ('builder', 'chapter', 'span'):
                with self.subTest(field=field, caller=caller):
                    self.build(self.archives)
                    with patch.object(builder, 'read_csv', return_value=[mutant]), patch.object(verifier.csv, 'DictReader', side_effect=[iter([]), iter([mutant])] if caller == 'chapter' else [iter([mutant])]), self.assertRaisesRegex(ValueError, 'No-service archive'):
                        if caller == 'builder':
                            with patch.object(builder, 'DATA', self.data):
                                builder.main()
                        else:
                            (self.check_chapters if caller == 'chapter' else self.check_spans)()

    def test_complete_real_crosswalk_has_exactly_32_recognized_tuples(self):
        with (ROOT / 'out/data/reverse_lookup_crosswalk.csv').open(newline='', encoding='utf-8') as handle:
            rows = list(csv.DictReader(handle))
        keys = builder.no_service_source_tuples()
        selected = [r for r in rows if builder.is_no_service_chapter_source(r, keys)]
        self.assertEqual(sorted(r['source_row_id'] for r in selected), sorted(r['source_row_id'] for r in self.archives))
        self.assertEqual(len(selected), 32)

    def test_real_cli_rejects_luke_leak_and_query_remains_unread(self):
        import os
        import subprocess
        import sys
        self.build(self.archives)  # Valid zero-occurrence control.
        env = dict(os.environ, LECTIONARY_DATA_DIR=str(self.data), LECTIONARY_DISABLE_VAULT_PUBLISH='1')
        query = [sys.executable, str(ROOT / 'query_lectionary.py'), '--data-dir', str(self.data), '--chapter', 'Lk 10']
        control = subprocess.run(query, capture_output=True, text=True, env=env, cwd=ROOT)
        self.assertEqual(control.returncode, 0, control.stderr)
        self.assertIn('read=no', control.stdout)
        archive = next(r for r in self.archives if r['passage'] == 'Lk 10:38-52')
        self.sources([dict(archive, source_family='ordinary_date_resolved', source_row_id='', provenance='{}', superseded_reason='')])
        result = subprocess.run([sys.executable, str(ROOT / 'build_bible_chapter_lectionary_index.py')], capture_output=True, text=True, env=env, cwd=ROOT)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No-service archive', result.stderr)
        # Exercise the real verifier functions in a fresh interpreter against disposable DATA.
        for function in ('assert_chapter_occurrence_row_count', 'assert_reverse_crosswalk_spans_valid'):
            result = subprocess.run([sys.executable, '-c', f'import pathlib; import verify_lectionary_queries as v; v.DATA=pathlib.Path({str(self.data)!r}); v.{function}()'], capture_output=True, text=True, env=env, cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('No-service archive', result.stderr)
        result = subprocess.run(query, capture_output=True, text=True, env=env, cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('read=no', result.stdout)

    def test_all_boundaries_reauthenticate_retained_capture_and_context(self):
        self.build(self.archives)
        for digest in ('CAPTURE_SHA256', 'CONTEXT_SHA256'):
            for caller in (lambda: self.build(self.archives), self.check_chapters, self.check_spans):
                with self.subTest(digest=digest, caller=caller), patch.object(history, digest, '0' * 64), self.assertRaisesRegex(ValueError, 'source hash/context drift'):
                    caller()

    def test_ordinary_unparseable_reference_still_rejected(self):
        rows = [dict(self.controls()[0], passage='unparsed nonsense')]
        self.sources(rows)
        write_rows(self.data / 'bible_chapter_lectionary_occurrences.csv', [], builder.DETAIL_FIELDS)
        with self.assertRaisesRegex(AssertionError, 'Unparsed chapter source'):
            self.check_chapters()
        with self.assertRaisesRegex(AssertionError, 'unparsed'):
            self.check_spans()


if __name__ == '__main__':
    unittest.main()
