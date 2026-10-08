"""Actual consumer boundary regressions for independent R1/R2/R3 findings."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import build_design_deliverables as d
import source_reading_contracts as c
import verify_design_deliverables as v


class EditionFragmentRemediation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables, _ = c.load_reviewed_tables()
        cls.rows, _ = d.build_reverse_presentation(c.project_table(cls.tables[0]), candidate_projection=True)
        cls.daily = d.build_daily_year_files(cls.rows, candidate_projection=True, transport_mode="presentation")[2026]['2026-03-06']
        cls.reverse, _ = d.build_reverse_lectionary_index(cls.rows, candidate_projection=True, transport_mode="presentation")

    def test_serialized_disclosure_corruptions_rejected_by_real_verifier(self):
        for lane, original in [('daily', self.daily), ('reverse', self.reverse)]:
            for corruption in ['missing', 'empty', 'duplicate', 'body', 'promotion', 'fragments', 'kind']:
                rows = copy.deepcopy(original)
                if corruption == 'missing':
                    rows[0].pop('source_disclosure')
                else:
                    disclosure = json.loads(rows[0]['source_disclosure'])
                    if corruption == 'empty': disclosure = []
                    elif corruption == 'duplicate': disclosure += copy.deepcopy(disclosure)
                    elif corruption == 'kind': disclosure[0]['source_kind'] = 'forged'
                    elif corruption == 'promotion': disclosure[0][c.CONTRACT_KEY]['runtime_activation'] = True
                    elif corruption == 'body': disclosure[0][c.CONTRACT_KEY]['metadata']['raw_source_block'] = 'FORGED BODY'
                    else: disclosure[0][c.CONTRACT_KEY]['metadata']['fragment_inventory'].append({'source_literal': 'FORGED FRAGMENT'})
                    rows[0]['source_disclosure'] = json.dumps(disclosure)
                with self.subTest(lane=lane, corruption=corruption), self.assertRaises(ValueError):
                    v.verify_source_contract_rows(rows, candidate_projection=True, transport_mode=lane)

    def test_inactive_current_status_rejected_at_all_actual_boundaries(self):
        consumers = [lambda rs: d.build_daily_year_files(rs, candidate_projection=True, transport_mode="presentation"),
                     lambda rs: d.build_reverse_lectionary_index(rs, candidate_projection=True, transport_mode="presentation"),
                     d.build_passage_source_disclosure,
                     lambda rs: v.verify_source_contract_rows(rs, candidate_projection=True)]
        for status in ['removed', 'inactive', 'superseded', 'Removed', 'INACTIVE']:
            for consumer in consumers:
                rows = copy.deepcopy(self.rows); rows[0]['current_status'] = status
                with self.subTest(status=status, consumer=consumer), self.assertRaises(ValueError): consumer(rows)
            for lane, original in [("daily", self.daily), ("reverse", self.reverse)]:
                rows = copy.deepcopy(original); rows[0]['current_status'] = status
                with self.subTest(status=status, serialized=True), self.assertRaises(ValueError):
                    v.verify_source_contract_rows(rows, candidate_projection=True, transport_mode=lane)

    def test_serialized_disclosure_duplicate_json_keys_are_rejected(self):
        for lane, original in [("daily", self.daily), ("reverse", self.reverse)]:
            rows = copy.deepcopy(original)
            rows[0]['source_disclosure'] = rows[0]['source_disclosure'].replace(
                '"runtime_activation":false', '"runtime_activation":true,"runtime_activation":false', 1)
            with self.subTest(lane=original), self.assertRaises(ValueError):
                v.verify_source_contract_rows(rows, candidate_projection=True, transport_mode=lane)

    def test_nonboolean_runtime_flags_rejected_at_actual_boundaries(self):
        for lane, original in [("presentation", self.rows), ("daily", self.daily), ("reverse", self.reverse)]:
            for value in ['true', 1, 'false', 0, None]:
                rows = copy.deepcopy(original); rows[0]['runtime_activation'] = value
                with self.subTest(value=value), self.assertRaises(ValueError):
                    v.verify_source_contract_rows(rows, candidate_projection=True, transport_mode=lane)

    def test_post_projection_lent_witness_corruption_rejected_at_all_boundaries(self):
        manifest = json.loads((c.FIXTURES / 'bindings.json').read_text())
        witness = next(value for label, value in manifest.items() if label.endswith('.html') and 'lent' in label)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'fixtures'; shutil.copytree(c.FIXTURES, root)
            (root / witness['file']).write_bytes(b'changed witness edition')
            with patch.object(c, 'FIXTURES', root):
                for consumer in [lambda: d.build_daily_year_files(self.rows, candidate_projection=True, transport_mode="presentation"),
                                 lambda: d.build_reverse_lectionary_index(self.rows, candidate_projection=True, transport_mode="presentation"),
                                 lambda: d.build_passage_source_disclosure(self.rows, transport_mode="presentation"),
                                 lambda: v.verify_source_contract_rows(self.daily, candidate_projection=True, transport_mode="daily"),
                                 lambda: v.verify_source_contract_rows(self.reverse, candidate_projection=True)]:
                    with self.subTest(consumer=consumer), self.assertRaisesRegex(ValueError, 'hash mismatch'): consumer()


if __name__ == '__main__':
    unittest.main()
