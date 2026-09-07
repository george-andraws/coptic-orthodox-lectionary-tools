import unittest
import build_design_deliverables as design

class DailyForwardContract(unittest.TestCase):
    def test_preserves_machine_reference_and_source_slot_metadata(self):
        row = dict(gregorian_date='2026-04-10', occasion='Good Friday', service_hour='First Hour', slot='OT10', slot_type='prophecy', slot_order=10, service_order=1, identity_key='mic7', display_ref='Mic 7:1-8', spans_json='[{"book":"Mic","chapter_start":7,"verse_start":1,"chapter_end":7,"verse_end":8}]', current_status='current_working_source_not_coptic_reader_checked', source_kind='pascha_day_hour', source_row_id='source10')
        result = design.build_daily_year_files([row])[2026]['2026-04-10'][0]
        for field in ['spans_json','slot_type','slot_order','service_order','current_status','source_row_id']:
            self.assertEqual(result[field], row[field])
        self.assertTrue(result['source_group_key'])

    def test_only_current_rows_enter_default_daily_artifact(self):
        base = dict(gregorian_date='2026-04-06', occasion='Monday', display_ref='Gen 1:1-2:3')
        rows = [dict(base,current_status=s) for s in ['current_public_or_local_reference','historical_witness','historical_candidate_removed','superseded_by_composite']]
        self.assertEqual(len(design.build_daily_year_files(rows)[2026]['2026-04-06']), 1)
        with self.assertRaises(ValueError):
            design.build_daily_year_files([dict(base,current_status='current_invented')])

if __name__=='__main__': unittest.main()
