import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.verify_package_integrity import validate_synaxarium_integrity
ROOT = Path(__file__).resolve().parents[1]

class SynaxariumValidationTests(unittest.TestCase):
    def test_source_catalog_passes(self):
        self.assertEqual(validate_synaxarium_integrity(ROOT / 'packages/lectionary-data')['status'], 'pass')

    def test_seeded_corruption_fails(self):
        data = json.loads((ROOT / 'packages/lectionary-data/data/synaxarium/synaxarium.json').read_text())
        def move_day(d): d['tout-31'] = d.pop('tout-30')
        def move_record(d): d['tout-2']['commemorations'].append(d['tout-1']['commemorations'].pop())
        def private_record(d): d['tout-1']['commemorations'][0]['sources'] = []
        def private_day(d): d['tout-1']['raw'] = 'capture'
        def duplicate_id(d): d['tout-1']['commemorations'][1]['id'] = d['tout-1']['commemorations'][0]['id']
        def bad_type(d): d['tout-1']['commemorations'][0]['type'] = 'invalid'
        def wrong_title(d): d['tout-1']['commemorations'][0]['title'] = 'different'
        def bad_leap(d): d['nasie-6']['validInCommonYear'] = True
        def missing(d): del d['nasie-6']
        def bad_slug(d): d['hator-1'] = d.pop('hatour-1')
        def malformed(d): d['tout-1']['commemorations'][0] = None
        for mutate in [move_day, move_record, private_record, private_day, duplicate_id, bad_type, wrong_title, bad_leap, missing, bad_slug, malformed]:
            with self.subTest(mutation=mutate.__name__), tempfile.TemporaryDirectory() as tmp:
                value = copy.deepcopy(data)
                mutate(value)
                target = Path(tmp) / 'data/synaxarium/synaxarium.json'
                target.parent.mkdir(parents=True)
                target.write_text(json.dumps(value))
                self.assertEqual(validate_synaxarium_integrity(Path(tmp))['status'], 'fail')
