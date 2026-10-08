import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

import build_lectionary_reference as reference


class DateIndexSideEffectTests(unittest.TestCase):
    def row(self):
        return {'source':'test','gregorian_date':'2026-03-04','weekday':'Wednesday',
                'day_title':'source test','service_section':'Matins','reading_type':'Gospel',
                'raw_ref':'Mk 14:-39','normalized_ref':'Mark 14:39','parse_status':'repaired',
                'normalization_warning':'repaired marker','url':'primary'}

    def test_helper_cannot_overwrite_a_complete_build_report(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(reference,'DATA',Path(folder)):
            report=Path(folder)/'source_ref_repair_report.csv';report.write_text('complete retained evidence\n')
            self.assertTrue(reference.build_date_passage_index([self.row()]))
            self.assertEqual(report.read_text(),'complete retained evidence\n')
            self.assertFalse((Path(folder)/'source_ref_repair_report.jsonl').exists())

    def test_explicit_build_report_target_is_written(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)
            reference.build_date_passage_index([self.row()],repair_report_root=target)
            self.assertIn('Mk 14:-39',(target/'source_ref_repair_report.csv').read_text())


if __name__=='__main__':unittest.main()
