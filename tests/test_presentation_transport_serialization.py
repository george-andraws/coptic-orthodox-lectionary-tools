"""Round-trip authenticated source transport through actual declared CSV fields."""
import ast
import csv
import json
from pathlib import Path
import tempfile
import unittest

import build_design_deliverables as design
import verify_design_deliverables as verify

ROOT=Path(__file__).resolve().parents[1]

class PresentationTransportSerialization(unittest.TestCase):
    def fields(self):
        tree=ast.parse((ROOT/'build_design_deliverables.py').read_text())
        return next(ast.literal_eval(node.value) for node in ast.walk(tree)
                    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='presentation_fields' for t in node.targets))

    def test_independent_disclosure_oracle_preserves_source_and_lifecycle_transport(self):
        rows=verify.read_csv(ROOT/'out/design/reverse_lectionary_presentation.csv')
        sunday=next(row for row in rows if row['source_key']=='coptic_reader_sunday_policy')
        history=next(row for row in rows if row['occasion']=='Annunciation (superseded date 2023-04-07)')
        for row in [sunday,history]:
            with self.subTest(source=row['source_key']):
                expected=json.loads(row['provenance'])['consumer_source_transport']
                actual,_=verify.expected_source_disclosure([row])
                self.assertEqual(actual[0].get('consumer_source_transport'),[expected])

    def test_real_sunday_transport_survives_csv_roundtrip(self):
        actual,_=design.build_reverse_presentation()
        presentation=[next(row for row in actual if row['source_key']=='coptic_reader_sunday_policy')]
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/'roundtrip.csv'
            design.write_csv(file,presentation,self.fields())
            reread=verify.read_csv(file)
        verify.verify_source_contract_rows(reread,transport_mode='presentation')
        for field in ['source_label','source_order']:
            corrupted=dict(reread[0]);corrupted.pop(field)
            with self.assertRaises(ValueError):verify.verify_source_contract_rows([corrupted],transport_mode='presentation')

if __name__=='__main__':unittest.main()
