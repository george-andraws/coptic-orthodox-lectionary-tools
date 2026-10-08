"""The approved eight dated rules must reach actual current sidecars."""
import copy
import csv
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_reference as core
import reading_context_overlays as overlays

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'sources/coptic-reader/annual-reconciled-2026-10-07'
EXPECTED = {
    '2026-09-26': ('Catholic Epistle','1Pet 1:25-2:10'),
    '2027-09-28': ('Catholic Epistle','1Pet 2:11-25'),
    '2026-09-29': ('Gospel','Lk 14:25-35'),
    '2026-11-06': ('Gospel','Matt 4:23-5:16'),
}

class AnnualDatedMaterialization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = overlays.load_fixture(FIXTURE)

    def raw(self,date):
        return core.parse_copticchurch_html((FIXTURE/'date-source'/f'{date}.html').read_text(),dt.date.fromisoformat(date))[1]

    def apply(self,rows):
        implementation = getattr(overlays,'apply_annual_dated_hardening',None)
        self.assertIsNotNone(implementation,'Approved dated annual adapter is not wired for production')
        assert implementation is not None
        return implementation(rows,self.fixture)

    def test_four_missing_source_assignments_are_corrected_with_history(self):
        for date,(kind,ref) in EXPECTED.items():
            with self.subTest(date=date):
                raw=self.raw(date);before=copy.deepcopy(raw);result=self.apply(raw)
                target=next(r for r in result['active'] if r['service_section']=='Liturgy' and r['reading_type']==kind)
                self.assertEqual(target['normalized_ref'],ref)
                self.assertEqual(raw,before)
                self.assertTrue(any(r['superseded_by_ref']==ref for r in result['history']))
                self.assertTrue(all(r['active'] is False for r in result['history']))
                self.assertEqual([r['raw_ref'] for r in result['active']],[r['raw_ref'] for r in raw])

    def test_actual_sidecar_pipeline_uses_the_source_adapter(self):
        raw=[r for date in EXPECTED for r in self.raw(date)]
        with tempfile.TemporaryDirectory() as folder,patch.object(core,'DATA',Path(folder)):
            core.write_csv(Path(folder)/'copticchurch_date_readings_2020_2035.csv',raw)
            core.write_csv(Path(folder)/'pascha_day_hour_index.csv',[],fieldnames=['day','hour','slot','refs'])
            active,index=core.build_current_date_sidecars()
            for date,(kind,ref) in EXPECTED.items():
                match=[r for r in index if r['gregorian_date']==date and r['service_section']=='Liturgy' and r['reading_type']==kind]
                self.assertEqual([r['matched_ref'] for r in match],[ref])
            with (Path(folder)/'annual_dated_readings_history.csv').open(newline='') as handle:
                historical=list(csv.DictReader(handle))
            self.assertTrue(historical)
            self.assertTrue(all(r['active']=='False' for r in historical))

    def test_unmatched_dates_preserved_and_selected_drift_rejected(self):
        raw=self.raw('2026-09-26')
        shifted=[dict(r,gregorian_date='2026-09-27',weekday='Sunday') for r in raw]
        self.assertEqual(self.apply(shifted),{'active':shifted,'history':[],'events':[]})
        for mutate in [lambda r:r.pop(),lambda r:r.append(copy.deepcopy(r[0])),
                       lambda r:r[0].update(raw_ref='Psalms 1:1'),
                       lambda r:r[0].update(current_status='removed')]:
            bad=copy.deepcopy(raw);mutate(bad)
            with self.assertRaises(ValueError):self.apply(bad)

    def test_replay_is_idempotent_without_duplicate_history(self):
        once=self.apply(self.raw('2026-09-26'));twice=self.apply(once['active'])
        self.assertEqual(once['active'],twice['active'])
        self.assertEqual(twice['history'],[])


if __name__=='__main__':unittest.main()
