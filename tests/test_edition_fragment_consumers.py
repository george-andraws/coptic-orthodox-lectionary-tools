"""Bounded real design consumers; candidates never authorize current activation."""
import copy
import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from unittest import mock
from pathlib import Path

import build_design_deliverables as design


class EditionFragmentConsumers(unittest.TestCase):
    def test_unbound_edition_kind_cannot_manufacture_exact_mt_identity(self):
        with self.assertRaisesRegex(ValueError, 'contract'):
            design.identity_for('Dan 14:1-42', 'edition_fragment_candidate')

    def test_actual_daily_consumer_rejects_unbound_contract_metadata(self):
        row = dict(design.identity_for('Prov 9:1-11'), gregorian_date='2026-03-26',
                   occasion='Thursday of the sixth week of Great Lent',
                   source_kind='edition_fragment_candidate', slot='OT3',
                   service_section='Matins', source_contract={'lane': 'lent', 'table_id': 'fake'})
        with self.assertRaisesRegex(ValueError, 'contract'):
            design.build_daily_year_files([row], transport_mode="presentation")

    def test_actual_disclosure_consumer_rejects_unbound_contract_metadata(self):
        row = dict(design.identity_for('Sir 2:1-3:4'), source_kind='edition_fragment_candidate')
        with self.assertRaisesRegex(ValueError, 'contract'):
            design.build_passage_source_disclosure([row], transport_mode="presentation")


class BoundProductionContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import source_reading_contracts as contracts
        cls.contracts = contracts
        cls.tables, cls.psalms = contracts.load_reviewed_tables()
        cls.raw = contracts.project_table(cls.tables[0])
        cls.rows, cls.ids = design.build_reverse_presentation(cls.raw, candidate_projection=True)

    def consumers(self, rows):
        return [lambda: design.build_daily_year_files(rows, candidate_projection=True, transport_mode="presentation"),
                lambda: design.build_reverse_lectionary_index(rows, candidate_projection=True, transport_mode="presentation"),
                lambda: design.build_passage_source_disclosure(rows, transport_mode="presentation")]

    def test_all_ten_tables_pass_actual_production_pipeline_without_activation(self):
        total = 0
        for table in self.tables:
            raw = self.contracts.project_table(table)
            if table['staged']:
                self.assertEqual(raw, [])
                self.assertEqual(len(table['readings']), 11)
                continue
            rows, identities = design.build_reverse_presentation(raw, candidate_projection=True)
            daily = design.build_daily_year_files(rows, candidate_projection=True, transport_mode="presentation")
            reverse, disagreements = design.build_reverse_lectionary_index(rows, candidate_projection=True, transport_mode="presentation")
            disclosure = design.build_passage_source_disclosure(rows, transport_mode="presentation")
            serialized = daily[int(table['civil_date'][:4])][table['civil_date']]
            self.assertEqual([r['slot_order'] for r in serialized], list(range(1, len(rows) + 1)))
            self.assertEqual(len(reverse), len(rows))
            self.assertEqual(len(disclosure), len(rows))
            self.assertEqual(disagreements, [])
            self.assertEqual(design.build_daily_year_files(rows, transport_mode="presentation"), {})
            with self.assertRaisesRegex(ValueError, 'current reverse'):
                design.build_reverse_lectionary_index(rows, transport_mode="presentation")
            for source, presented, shipped in zip(raw, rows, serialized):
                self.assertEqual(presented['source_ref'], source['source_ref'])
                self.assertEqual(shipped['spans_json'], presented['spans_json'])
                self.assertEqual(list(shipped), design.DAILY_READING_FIELDS)
                self.assertFalse(design.is_current_presentation(presented))
                self.assertEqual(presented['canonical_mt_ref'], '')
                self.assertEqual(presented['canonical_lxx_ref'], '')
                self.assertEqual(identities[presented['identity_key']]['source_label'], source['source_ref'])
            total += len(rows)
        self.assertEqual(total, 40)

    def test_disclosure_transports_complete_fragment_contract_not_only_covering_ref(self):
        reverse, _ = design.build_reverse_lectionary_index(self.rows, candidate_projection=True, transport_mode="presentation")
        daily = design.build_daily_year_files(self.rows, candidate_projection=True, transport_mode="presentation")[2026]['2026-03-06']
        for output in [reverse, daily]:
            for row in output:
                disclosure = json.loads(row['source_disclosure'])
                self.assertIn(self.contracts.CONTRACT_KEY, disclosure[0])
                self.assertFalse(disclosure[0][self.contracts.CONTRACT_KEY]['consumer_eligible'])

    def test_whole_table_corruptions_rejected_by_all_actual_consumers(self):
        cases = {'omitted': self.rows[:-1], 'reordered': list(reversed(self.rows)),
                 'duplicate': self.rows + [self.rows[-1]]}
        for field, value in [('identity_key', self.rows[1]['identity_key']),
                             ('canonical_mt_ref', 'Sir 2:1-3:4'),
                             ('source_ref', 'Sir 2:1-3:4'),
                             ('service_section', 'Liturgy'),
                             ('occasion', 'Feast of the Cross'),
                             ('source_kind', 'invented_edition'),
                             ('source_convention', 'invented_edition'),
                             ('source_order', 99),
                             ('source_file', 'unbound-document.txt'),
                             ('consumer_eligible', True),
                             ('source_family', 'ordinary_date_resolved'),
                             ('state', 'removed'),
                             ('is_active', False),
                             ('current_status', 'current_confirmed_coptic_reader'),
                             ('active', False), ('removed_marker', 'superseded')]:
            altered = copy.deepcopy(self.rows)
            altered[0][field] = value
            cases[field] = altered
        for name, rows in cases.items():
            for consumer in self.consumers(rows):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    consumer()

    def test_bound_metadata_corruptions_rejected_before_real_presentation(self):
        for field, value in [('text_sha256', '0' * 64), ('context', 'Feast of the Cross'),
                             ('navigation', ['Special']), ('runtime_activation', True)]:
            table = copy.deepcopy(self.tables[0]); table[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.contracts.project_table(table)
        for field, value in [('edition_id', 'MT'), ('spans', []), ('source_order', 99),
                             ('printed_ref', 'Sirach 2:1-3:4'), ('source_slot', 'OT9')]:
            raw = copy.deepcopy(self.raw)
            raw[-1]['source_contract']['metadata'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                design.build_reverse_presentation(raw, candidate_projection=True)

    def test_cpdv_boundaries_are_edition_specific_and_raw_grammar_survives(self):
        for table in self.tables:
            raw = self.contracts.project_table(table)
            if not raw: continue
            rows, _ = design.build_reverse_presentation(raw, candidate_projection=True)
            for row in rows:
                spans = json.loads(row['spans_json'])
                e = spans[0][self.contracts.CONTRACT_KEY]
                m = e['metadata']
                if m['edition_id'] != 'cpdv_2009_original': continue
                self.assertNotEqual(row['identity_key'], design.identity_for(m['normalized_literal_ref'])['identity_key'])
                self.assertEqual([(s['chapter_start'], s['verse_start'], s['verse_end']) for s in spans],
                                 [(r['chapter'], r['verse_start'], r['verse_end']) for r in m['edition_bounds_qualification']['ordered_observed_chapter_runs']])
                if m['book'] == 'Sir' and spans[0]['chapter_start'] == 8:
                    self.assertIn('8, 9, 10:1', row['source_ref'])
                    self.assertEqual(spans[0]['canonical_edition_ref'], 'Sir 8:1-10:1')
                    self.assertEqual([(s['chapter_start'], s['verse_end']) for s in spans], [(8, 22), (9, 25), (10, 1)])
                if m['book'] == 'Dan':
                    self.assertEqual(spans[0]['verse_end'], 42)
                    self.assertEqual(spans[0]['chapter_start'], 14)

    def test_actual_occasion_guard_allows_gabriel_commemoration_not_cross(self):
        thursday = next(t for t in self.tables if t['civil_date'] == '2027-04-08')
        self.assertIn('Archangel Gabriel', thursday['context'])
        self.assertEqual(len(self.contracts.project_table(thursday)), 3)
        with self.assertRaisesRegex(ValueError, 'occasion/offset'):
            self.contracts.project_table(thursday, '2026-03-19', 'Feast of the Cross')
        with self.assertRaisesRegex(ValueError, 'occasion/offset'):
            self.contracts.project_table(thursday, '2026-03-19', 'Thursday of the fifth week of Great Lent')

    def test_psalm_literal_null_partial_apparatus_contract_survives_reverse_disclosure(self):
        total = 0
        for psalm in self.psalms:
            raw = self.contracts.project_psalm(psalm)
            rows, _ = design.build_reverse_presentation(raw, candidate_projection=True)
            reverse, _ = design.build_reverse_lectionary_index(rows, candidate_projection=True, transport_mode="presentation")
            self.assertEqual(reverse[0]['spans_json'], rows[0]['spans_json'])
            spans = json.loads(reverse[0]['spans_json'])
            self.assertIsNone(spans[0]['chapter_start'])
            fragments = spans[0]['source_fragments']
            self.assertEqual(''.join(f['source_literal'] for f in fragments), psalm['body_english'])
            for fragment in fragments:
                if fragment['source_literal'] in ['to Jacob', "For Your name’s sake", 'Alleluia.']:
                    self.assertIsNone(fragment['mt'])
            self.assertEqual(design.build_daily_year_files(rows, transport_mode="presentation"), {})
            self.assertEqual(design.build_passage_source_disclosure(rows, transport_mode="presentation")[0]['source_ref'], psalm['heading_exact'])
            total += len(fragments)
        self.assertEqual(total, 13)

    def test_fragment_inflation_extra_mt_and_truncation_fail_all_consumers(self):
        table = next(t for t in self.tables if t['civil_date'] == '2026-03-26')
        rows, _ = design.build_reverse_presentation(self.contracts.project_table(table), candidate_projection=True)
        target = next(i for i, r in enumerate(rows) if r['source_ref'] == '\tProverbs 9:1-11')
        for mutate in ['lettered_inflation', 'extra_MT', 'omission', 'eligibility']:
            altered = copy.deepcopy(rows)
            spans = json.loads(altered[target]['spans_json'])
            if mutate == 'lettered_inflation': spans[0]['verse_end'] = 12
            if mutate == 'extra_MT': spans[0]['canonical_mt_ref'] = 'Prov 9:1-12'
            if mutate == 'omission': spans[0]['source_fragments'].pop()
            if mutate == 'eligibility': spans[0][self.contracts.CONTRACT_KEY]['consumer_eligible'] = True
            altered[target]['spans_json'] = json.dumps(spans, ensure_ascii=False, sort_keys=True)
            for consumer in self.consumers(altered):
                with self.subTest(mutate=mutate), self.assertRaises(ValueError): consumer()

    def test_verifier_strictly_accepts_only_bound_edition_vocab(self):
        import verify_design_deliverables as verifier
        verifier.verify_source_contract_rows(self.rows, candidate_projection=True, transport_mode="presentation")
        for field in ['source_kind', 'source_convention', 'source_key']:
            altered = copy.deepcopy(self.rows); altered[0][field] = 'invented_edition'
            with self.subTest(field=field), self.assertRaises(ValueError):
                verifier.verify_source_contract_rows(altered, candidate_projection=True, transport_mode="presentation")

    def test_daily_serialization_round_trip_keeps_contract_without_new_header(self):
        daily = design.build_daily_year_files(self.rows, candidate_projection=True, transport_mode="presentation")[2026]['2026-03-06']
        rehydrated = [dict(r, gregorian_date='2026-03-06') for r in json.loads(json.dumps(daily))]
        self.contracts.validate_consumer_rows(rehydrated, candidate_projection=True, transport_mode="daily")

    def test_query_facing_reverse_spans_round_trip_in_real_verifier(self):
        import verify_design_deliverables as verifier
        for rows in [self.rows] + [design.build_reverse_presentation(self.contracts.project_psalm(p), candidate_projection=True)[0] for p in self.psalms]:
            reverse, _ = design.build_reverse_lectionary_index(rows, candidate_projection=True, transport_mode="presentation")
            verifier.verify_source_contract_rows(json.loads(json.dumps(reverse)), candidate_projection=True)

    def test_psalm_corruptions_rejected_by_actual_reverse_and_disclosure(self):
        for psalm in self.psalms:
            rows, _ = design.build_reverse_presentation(self.contracts.project_psalm(psalm), candidate_projection=True)
            for corruption in ['jacob_mt', 'apparatus_main', 'literal_order', 'literal_truncation']:
                bad = copy.deepcopy(rows)
                spans = json.loads(bad[0]['spans_json'])
                fragments = spans[0]['source_fragments']
                if corruption == 'jacob_mt':
                    target = next(f for f in fragments if f['mt'] is None)
                    target['mt'] = [98, 3]
                elif corruption == 'apparatus_main':
                    fragments[-1]['lxx'] = [97, 8]
                elif corruption == 'literal_order':
                    fragments.reverse()
                else:
                    fragments[-1]['source_literal'] = fragments[-1]['source_literal'][:-1]
                bad[0]['spans_json'] = json.dumps(spans, ensure_ascii=False, sort_keys=True)
                for consumer in self.consumers(bad):
                    with self.subTest(corruption=corruption), self.assertRaises(ValueError): consumer()

    def test_corrected_psalm_fragments_survive_actual_candidate_daily_serializer(self):
        for psalm in self.psalms:
            date = psalm['capture_context_metadata']['captureTime'][:10]
            raw = self.contracts.project_psalm(psalm, candidate_date=date)
            rows, _ = design.build_reverse_presentation(raw, candidate_projection=True)
            daily = design.build_daily_year_files(rows, candidate_projection=True, transport_mode="presentation")[int(date[:4])][date]
            self.assertEqual(len(daily), 1)
            self.assertEqual(daily[0]['spans_json'], rows[0]['spans_json'])
            self.assertEqual(design.build_daily_year_files(rows, transport_mode="presentation"), {})
            with self.assertRaises(ValueError):
                self.contracts.project_psalm(psalm, candidate_date='2026-03-19')

    def test_lent_projection_authenticates_public_witness_document_bytes(self):
        manifest = json.loads((self.contracts.FIXTURES / 'bindings.json').read_text())
        witness = next(value for label, value in manifest.items() if label.endswith('.html') and 'lent' in label)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'fixtures'
            shutil.copytree(self.contracts.FIXTURES, root)
            (root / witness['file']).write_bytes(b'changed witness edition')
            with mock.patch.object(self.contracts, 'FIXTURES', root):
                with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                    self.contracts.project_table(self.tables[0])

    def test_all_2591_legacy_identity_canaries_preserved_byte_for_byte(self):
        path = self.contracts.FIXTURES / 'legacy-identities.json'
        raw = path.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), 'fe93a4fde3f10abd229ea6897c35fae7094a68cae65e0e4ac40948e3620a88f1')
        expected = json.loads(raw)
        self.assertEqual(len(expected), 2591)
        for label, identity in expected.items():
            if label.endswith('|fixture'):
                actual = design.identity_for(label[:-8], 'coptic_reader_fixture')
            else:
                actual = design.identity_for(label)
            self.assertEqual(actual, identity, label)

    def test_existing_wednesday_fixture_remains_26_rows_and_named_job(self):
        raw = design.load_fixture_rows()
        rows, identities = design.build_reverse_presentation(raw)
        self.assertEqual(len(rows), 26)
        self.assertEqual(sum(r['reading_name'] == 'Memoirs of Job' for r in rows), 1)
        self.assertTrue(all(r['current_status'] == 'current_confirmed_coptic_reader' for r in rows))
        self.assertTrue(all(r['source_key'] == 'coptic_reader_fixture_wednesday_day' for r in rows))

    def test_existing_crosswalk_csv_headers_transport_contract_via_provenance(self):
        with (design.DATA / 'reverse_lookup_crosswalk.csv').open(newline='') as f:
            fields = next(csv.reader(f))
        self.assertNotIn('source_contract', fields)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'candidate-crosswalk.csv'
            design.write_csv(path, self.raw, fields)
            reread = design.read_csv(path)
            rows, identities = design.build_reverse_presentation(reread, candidate_projection=True)
        self.assertEqual([r['spans_json'] for r in rows], [r['spans_json'] for r in self.rows])
        self.assertEqual(identities, self.ids)


if __name__ == '__main__':
    unittest.main()
