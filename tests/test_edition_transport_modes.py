"""Trusted transport context must not be supplied by mutable row keys."""
import copy
import json
import unittest
import build_design_deliverables as d
import source_reading_contracts as c
import verify_design_deliverables as v

class TransportModes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, psalms = c.load_reviewed_tables()
        p = psalms[0]
        cls.presentation, _ = d.build_reverse_presentation(c.project_psalm(p, candidate_date=p['capture_context_metadata']['captureTime'][:10]), candidate_projection=True)
        cls.reverse, _ = d.build_reverse_lectionary_index(cls.presentation, candidate_projection=True, transport_mode="presentation")
        ds = d.build_daily_year_files(cls.presentation, candidate_projection=True, transport_mode="presentation")
        cls.daily = [dict(r, gregorian_date=date) for days in ds.values() for date, rs in days.items() for r in rs]

    def consumers(self, mode="output"):
        return [lambda rs: d.build_daily_year_files(rs, candidate_projection=True, transport_mode=mode),
                lambda rs: d.build_reverse_lectionary_index(rs, candidate_projection=True, transport_mode=mode),
                lambda rs: d.build_passage_source_disclosure(rs, transport_mode=mode),
                lambda rs: v.verify_source_contract_rows(rs, candidate_projection=True, transport_mode=mode)]

    def test_laundered_real_output_rejects_at_every_supported_consumer(self):
        for lane, original in [('daily', self.daily), ('reverse', self.reverse)]:
            for fault in ['empty', 'body', 'promotion']:
                bad = copy.deepcopy(original)
                cell = json.loads(bad[0]['source_disclosure'])
                if fault == 'empty': cell = []
                elif fault == 'body': cell[0][c.CONTRACT_KEY]['metadata']['body_english'] = 'FORGED'
                else: cell[0][c.CONTRACT_KEY]['runtime_activation'] = True
                bad[0]['source_disclosure'] = json.dumps(cell)
                bad[0]['source_ref'] = self.presentation[0]['source_ref']
                bad[0].pop('source_group_key', None)
                bad[0].pop('source_disclosure_count', None)
                for i, consumer in enumerate(self.consumers(lane)):
                    with self.subTest(lane=lane, fault=fault, consumer=i), self.assertRaises(ValueError): consumer(bad)

    def test_required_output_fields_cannot_be_deleted(self):
        for lane, original, fields in [('daily', self.daily, ['source_locator','source_file','source_row_id','source_group_key','current_status']),
                                      ('reverse', self.reverse, ['source_locator','source_title','source_edition','source_disclosure_count','current_status'])]:
            for field in fields:
                bad = copy.deepcopy(original); bad[0].pop(field)
                for i, consumer in enumerate(self.consumers(lane)):
                    with self.subTest(lane=lane, field=field, consumer=i), self.assertRaises(ValueError): consumer(bad)

    def test_arbitrary_output_state_is_not_candidate_state(self):
        for lane, original in [("daily", self.daily), ("reverse", self.reverse)]:
            bad = copy.deepcopy(original); bad[0]['current_status'] = 'nonce forged'
            for i, consumer in enumerate(self.consumers(lane)):
                with self.subTest(consumer=i), self.assertRaises(ValueError): consumer(bad)

    def test_verifier_default_requires_output_disclosure(self):
        with self.assertRaises(ValueError): v.verify_source_contract_rows(self.presentation, candidate_projection=True)

    def test_explicit_presentation_extras_are_rebuilt_not_authenticated(self):
        bad = copy.deepcopy(self.presentation); bad[0]['source_disclosure'] = '[]'; bad[0]['source_disclosure_count'] = 'forged'
        v.verify_source_contract_rows(bad, candidate_projection=True, transport_mode='presentation')
        reverse, _ = d.build_reverse_lectionary_index(bad, candidate_projection=True, transport_mode='presentation')
        v.verify_source_contract_rows(reverse, candidate_projection=True, transport_mode='reverse')

    def test_explicit_output_lane_rejects_other_lane(self):
        for lane, rows in [('daily', self.reverse), ('reverse', self.daily)]:
            with self.subTest(lane=lane), self.assertRaises(ValueError):
                v.verify_source_contract_rows(rows, candidate_projection=True, transport_mode=lane)

    def test_supported_output_round_trips_remain_authenticated(self):
        for lane, original in [("daily", self.daily), ("reverse", self.reverse)]:
            v.verify_source_contract_rows(original, candidate_projection=True, transport_mode=lane)
            reverse, _ = d.build_reverse_lectionary_index(original, candidate_projection=True, transport_mode=lane)
            v.verify_source_contract_rows(reverse, candidate_projection=True, transport_mode='reverse')
            self.assertEqual(json.loads(reverse[0]['source_disclosure']), json.loads(self.reverse[0]['source_disclosure']))
            daily = d.build_daily_year_files(original, candidate_projection=True, transport_mode=lane)
            for days in daily.values():
                for date, readings in days.items():
                    v.verify_source_contract_rows([dict(row, gregorian_date=date) for row in readings], candidate_projection=True, transport_mode='daily')
            disclosure = d.build_passage_source_disclosure(original, transport_mode=lane)
            c.validate_passage_disclosure_output(disclosure, self.presentation)

    def test_empty_source_row_id_is_not_an_authenticated_ordinal(self):
        bad = copy.deepcopy(self.daily); bad[0]['source_row_id'] = ''
        with self.assertRaises(ValueError): v.verify_source_contract_rows(bad, candidate_projection=True, transport_mode='daily')

    def test_reverse_required_count_cannot_be_replaced_by_daily_shape(self):
        bad = copy.deepcopy(self.reverse)
        for field in c.REVERSE_FIELDS - c.COMMON_OUTPUT_FIELDS: bad[0].pop(field, None)
        for field in c.DAILY_FIELDS - c.COMMON_OUTPUT_FIELDS: bad[0][field] = self.daily[0][field]
        bad[0]['source_ref'] = self.presentation[0]['source_ref']
        with self.assertRaises(ValueError): v.verify_source_contract_rows(bad, candidate_projection=True)

    def test_each_output_required_field_rejects_omission_in_trusted_lane(self):
        for lane, original, fields in [('daily', self.daily, c.DAILY_FIELDS), ('reverse', self.reverse, c.REVERSE_FIELDS)]:
            for field in fields:
                bad = copy.deepcopy(original); bad[0].pop(field)
                with self.subTest(lane=lane, field=field), self.assertRaises(ValueError):
                    v.verify_source_contract_rows(bad, candidate_projection=True, transport_mode=lane)

    def test_presentation_core_source_scalars_cannot_be_forged(self):
        for field in ['source_locator', 'source_title', 'source_edition']:
            bad = copy.deepcopy(self.presentation); bad[0][field] = 'forged'
            with self.subTest(field=field), self.assertRaises(ValueError):
                v.verify_source_contract_rows(bad, candidate_projection=True, transport_mode='presentation')

    def test_disclosure_output_requires_authenticated_context_and_complete_schema(self):
        output = d.build_passage_source_disclosure(self.presentation, transport_mode='presentation')
        c.validate_passage_disclosure_output(output, self.presentation)
        for field in output[0]:
            bad = copy.deepcopy(output); bad[0].pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                c.validate_passage_disclosure_output(bad, self.presentation)
        bad = copy.deepcopy(output); bad[0]['citation'] = 'forged'
        with self.assertRaises(ValueError): c.validate_passage_disclosure_output(bad, self.presentation)

    def test_output_identity_name_and_collapse_count_are_authenticated(self):
        for lane, original, fields in [('daily', self.daily, ['reading_name']), ('reverse', self.reverse, ['reading_name', 'collapsed_row_count'])]:
            for field in fields:
                bad = copy.deepcopy(original); bad[0][field] = 'forged'
                with self.subTest(lane=lane, field=field), self.assertRaises(ValueError):
                    v.verify_source_contract_rows(bad, candidate_projection=True, transport_mode=lane)

    def test_each_input_required_field_rejects_omission_in_trusted_lane(self):
        _, psalms = c.load_reviewed_tables()
        raw = c.project_psalm(psalms[0], candidate_date=psalms[0]['capture_context_metadata']['captureTime'][:10])
        for lane, original, fields in [('raw', raw, c.RAW_FIELDS), ('presentation', self.presentation, c.PRESENTATION_FIELDS)]:
            for field in fields:
                bad = copy.deepcopy(original); bad[0].pop(field)
                with self.subTest(lane=lane, field=field), self.assertRaises(ValueError):
                    if lane == 'raw': d.build_reverse_presentation(bad, candidate_projection=True)
                    else: v.verify_source_contract_rows(bad, candidate_projection=True, transport_mode=lane)

    def test_unknown_mode_rejected(self):
        with self.assertRaises(ValueError): v.verify_source_contract_rows(self.reverse, candidate_projection=True, transport_mode='guess')
