"""Sunday boundaries use caller origin, never mutated output markers."""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import source_reading_contracts as contracts
import sunday_consumer_contracts as sunday
import build_design_deliverables as design
from test_sunday_consumer_remediation import sunday_rows, serialize
import build_lectionary_crosswalk as cross


class SundayForwarding(unittest.TestCase):
    def test_shared_boundary_forwards_each_trusted_mode(self):
        for mode in ('raw', 'presentation', 'daily', 'reverse', 'output'):
            with patch.object(sunday, 'validate_rows', wraps=sunday.validate_rows) as boundary:
                contracts.validate_consumer_rows([], serialized=mode != 'raw', transport_mode=mode)
            self.assertEqual(boundary.call_args.kwargs.get('transport_mode'), mode)


class SundayTrustedTransport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.presentation = design.build_reverse_presentation(serialize(cross.project_date_rows([sunday_rows()[0]]), cross.FIELDS))[0]

    def outputs(self):
        p = self.presentation
        day = design.build_daily_year_files(p, transport_mode='presentation')[2027]['2027-02-21'][0]
        observed = []
        with patch.object(design, 'verify_reverse_index_contract', lambda rows: observed.extend(rows)):
            design.build_reverse_lectionary_index(p, transport_mode='presentation')
        return {'daily': day, 'reverse': observed[0]}

    def test_trusted_origin_survives_marker_deletion(self):
        for lane, row in self.outputs().items():
            bad = dict(row, source_ref=self.presentation[0]['source_ref'], provenance=self.presentation[0]['provenance'], source_disclosure='[]')
            for key in ('source_group_key', 'source_disclosure_count', 'collapsed_row_count'):
                bad.pop(key, None)
            with self.subTest(lane=lane), self.assertRaises(ValueError):
                contracts.validate_consumer_rows([bad], transport_mode=lane)

    def test_redundant_locator_and_edition_dispatch(self):
        for field in ('source_locator', 'source_edition'):
            bad = {field: self.presentation[0][field]}
            self.assertTrue(sunday.is_sunday(bad))
            with self.assertRaises(ValueError):
                contracts.validate_consumer_rows([bad], transport_mode='presentation')

    def test_raw_reference_is_bound_to_primary_source(self):
        bad = copy.deepcopy(self.presentation[0])
        p = json.loads(bad['provenance'])
        bad['raw_ref'] = p['consumer_source_transport']['consumer_context']['raw_ref'] = 'forged raw'
        bad['provenance'] = json.dumps(p)
        with self.assertRaises(ValueError):
            contracts.validate_consumer_rows([bad], transport_mode='presentation')

    def test_required_fields_and_counts_not_truthiness(self):
        for lane, row in self.outputs().items():
            required = tuple(row)  # Every real emitted public field is required.
            for field in required:
                bad = dict(row); bad.pop(field)
                with self.subTest(lane=lane, missing=field), self.assertRaises(ValueError):
                    contracts.validate_consumer_rows([bad], transport_mode=lane)
            for value in ('', None, False):
                with self.subTest(lane=lane, identity=value), self.assertRaises(ValueError):
                    contracts.validate_consumer_rows([dict(row, identity_key=value)], transport_mode=lane)
            if lane == 'reverse':
                with self.assertRaises(ValueError):
                    contracts.validate_consumer_rows([dict(row, collapsed_row_count='999')], transport_mode=lane)

    def test_nonactivation_extras_are_literal_boolean_false(self):
        bases = dict(self.outputs(), presentation=self.presentation[0])
        for lane, row in bases.items():
            for flag in ('runtime_activation', 'consumer_eligible'):
                contracts.validate_consumer_rows([dict(row, **{flag: False})], transport_mode=lane)
                for value in (0, 0.0, 'false', None, [], {}, True):
                    with self.subTest(lane=lane, flag=flag, value=value), self.assertRaises(ValueError):
                        contracts.validate_consumer_rows([dict(row, **{flag: value})], transport_mode=lane)

    def test_witness_drift_is_value_error_but_io_is_not_hidden(self):
        import calendar_resolution as calendar
        target = calendar.WORK / calendar.SUNDAY_FIXTURE / 'accepted-oracle.json'
        read = Path.read_bytes
        def corrupt(path):
            return read(path) + (b'fault' if path == target else b'')
        with patch.object(Path, 'read_bytes', corrupt), self.assertRaises(ValueError):
            contracts.validate_consumer_rows(self.presentation, transport_mode='presentation')
        with patch.object(calendar, 'load_sunday_evidence', side_effect=OSError('infrastructure')), self.assertRaises(OSError):
            contracts.validate_consumer_rows(self.presentation, transport_mode='presentation')


if __name__ == '__main__':
    unittest.main()
