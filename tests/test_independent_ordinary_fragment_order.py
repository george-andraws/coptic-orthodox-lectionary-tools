"""Primary-cache order and complete-row rejection through the real daily oracle."""
import copy
import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup
import verify_design_deliverables as validator

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    '2020-01-30': ('e6f841880eeb6add0b9c966ba6592af608cc907ab3593dfdf15f24e435463707',
                   'Psalm 48:8  &  Psalm 48:1', 'Matins', ['Ps 48:8', 'Ps 48:1']),
    '2020-02-01': ('650f5af1d1b7c62804ac7f30507ad6c663d7325e27f2b6e13d6ef3db964686ec',
                   'Psalm 132:9  &  Psalm 132:10  &  Psalm 132:17  &  Psalm 132:18',
                   'Matins', ['Ps 132:9', 'Ps 132:10', 'Ps 132:17', 'Ps 132:18']),
    '2020-02-02': ('456605f4943a8fc8181e4cd2e9bdaba27707543215b2145902704edfc05630b0',
                   'Psalm 80:7  &  Psalm 80:18', 'Matins', ['Ps 80:7', 'Ps 80:18']),
    # This source's printed chapter is corrected independently by retained policy.
    '2026-02-18': ('560c843ef1d9c553e3c17b5377e9e5bf5ab19348addaa05e80d29e7ff6ffca86',
                   'Psalm 24:20  &  Psalm 24:16', 'Liturgy', ['Ps 25:20', 'Ps 25:16']),
}


class IndependentOrdinaryFragmentOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / 'out/design/reverse_lectionary_presentation.csv').open() as stream:
            cls.presentation = [r for r in csv.DictReader(stream) if r.get('gregorian_date') in CASES
                                or (not r.get('gregorian_date') and r.get('source_kind') == 'katameros_cycle'
                                    and r.get('canonical_mt_ref') in {'Joel 2:12-27', 'Joel 3:9-21'})]
        with (ROOT / 'out/data/copticchurch_passage_index_current_2020_2035.csv').open() as stream:
            cls.source = [r for r in csv.DictReader(stream) if r.get('gregorian_date') in CASES]
        cls.schema = json.loads((ROOT / 'out/design/lectionary_schema.json').read_text())
        cls.daily = {}
        for date in CASES:
            year = date[:4]
            if year not in cls.daily:
                cls.daily[year] = {}
            cls.daily[year][date] = json.loads((ROOT / f'out/design/daily/lectionary-{year}.json').read_text())[date]

    def verify(self, daily=None, presentation=None):
        daily = self.daily if daily is None else daily
        presentation = self.presentation if presentation is None else presentation
        original_read = validator.read_csv
        original_seasonal = validator.verify_seasonal_daily

        def read(path):
            if str(path).endswith('out/data/copticchurch_passage_index_current_2020_2035.csv'):
                return self.source
            if str(path).endswith('out/data/pascha_day_hour_index.csv'):
                return []
            return original_read(path)

        def seasonal(source, days, policy, *, complete_year=False):
            if complete_year:
                self.assertEqual(set(days), {d for d in CASES if d[:4] == next(iter(days))[:4]})
            return original_seasonal(source, days, policy)

        counts = {y: sum(map(len, days.values())) for y, days in daily.items()}
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            (out / 'daily').mkdir()
            for year, days in daily.items():
                (out / 'daily' / f'lectionary-{year}.json').write_text(json.dumps(days))
            with patch.object(validator, 'OUT', out), patch.object(validator, 'read_csv', side_effect=read), \
                    patch.object(validator, 'verify_seasonal_daily', side_effect=seasonal):
                validator.verify_daily_rows(presentation, self.schema, {
                    'daily_lectionary_years': counts, 'daily_lectionary_total_rows': sum(counts.values())})

    def test_literal_cache_and_source_ordinals_independent_of_producer(self):
        for date, (digest, literal, section, refs) in CASES.items():
            with self.subTest(date=date):
                raw = (ROOT / 'cache/copticchurch_html' / f'{date}.html').read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
                headings = [node.get_text() for node in BeautifulSoup(raw, 'html.parser').find_all('h5')]
                self.assertIn(literal, headings)
                rows = [r for r in self.presentation if r['gregorian_date'] == date
                        and r['service_section'] == section and r['slot'] == 'Psalm']
                rows.sort(key=lambda r: (int(r['source_order']), int(r['source_token_order'])))
                self.assertEqual([r['canonical_mt_ref'] for r in rows], refs)
                actual = [r for r in self.daily[date[:4]][date]
                          if r['service_section'] == section and r['slot'] == 'Psalm']
                self.assertEqual([r['canonical_mt_ref'] for r in actual], refs)

    def test_real_verifier_accepts_complete_source_ordered_dates(self):
        self.verify()

    def test_storage_shuffle_does_not_change_source_companions(self):
        self.verify(presentation=list(reversed(self.presentation)))

    def test_same_count_consumer_corruptions_fail_exact_comparison(self):
        self.verify()  # Every negative starts from a successful complete control.
        for mutation in ('order', 'identity_key', 'canonical_mt_ref', 'source_disclosure', 'service_section', 'date'):
            daily = copy.deepcopy(self.daily)
            rows = daily['2020']['2020-01-30']
            positions = [i for i, r in enumerate(rows) if r['service_section'] == 'Matins' and r['slot'] == 'Psalm']
            if mutation == 'order':
                a, b = positions
                rows[a], rows[b] = rows[b], rows[a]
            elif mutation == 'date':
                daily['2020']['2020-01-31'] = daily['2020'].pop('2020-01-30')
            else:
                rows[positions[0]][mutation] = 'corrupted'
            with self.subTest(mutation=mutation), self.assertRaisesRegex(AssertionError, 'does not exactly match'):
                self.verify(daily=daily)

    def test_token_ordinals_not_identity_or_reference_tiebreakers(self):
        presentation = copy.deepcopy(self.presentation)
        for row in presentation:
            if row['gregorian_date'] == '2020-01-30' and row['service_section'] == 'Matins' and row['slot'] == 'Psalm':
                row['source_order'] = '314'
                row['source_token_order'] = '1' if row['canonical_mt_ref'] == 'Ps 48:8' else '2'
        self.verify(presentation=presentation)

    def test_nonordinary_family_and_hour_do_not_acquire_companion_sort(self):
        for change in ({'source_family': 'nonordinary_control'}, {'service_hour': 'First Hour'},
                       {'source_file': 'noncache-control'}):
            presentation = copy.deepcopy(self.presentation)
            daily = copy.deepcopy(self.daily)
            for rows in (presentation, daily['2020']['2020-01-30']):
                for row in rows:
                    if (row.get('gregorian_date', '2020-01-30') == '2020-01-30'
                            and row['service_section'] == 'Matins' and row['slot'] == 'Psalm'):
                        row.update(change)
            # Keep the pre-existing supplied order for the excluded group.
            rows = daily['2020']['2020-01-30']
            positions = [i for i, r in enumerate(rows) if r['service_section'] == 'Matins' and r['slot'] == 'Psalm']
            a, b = positions
            rows[a], rows[b] = rows[b], rows[a]
            # Context changes must still update the exact source disclosure.
            for row in rows:
                if row['service_section'] == 'Matins' and row['slot'] == 'Psalm':
                    disclosure = json.loads(row['source_disclosure'])
                    for key in ('source_family', 'source_file'):
                        if key in change:
                            disclosure[0][key] = change[key]
                    row['source_disclosure'] = json.dumps(disclosure, ensure_ascii=False, separators=(',', ':'))
                    if 'source_family' in change or 'service_hour' in change:
                        row['slot_type'] = ''
                        row['slot_order'] = ''
                    if 'service_hour' in change:
                        row['source_group_key'] = '|'.join(row.get(f, '') for f in
                            ('source_kind', 'source_row_id', 'occasion', 'service_hour', 'slot'))
            # Mixed-family/hour dates retain their whole supplied sequence.
            if 'source_file' not in change:
                order = {r['identity_key']: i for i, r in enumerate(presentation) if r['gregorian_date'] == '2020-01-30'}
                rows.sort(key=lambda r: order[r['identity_key']])
            with self.subTest(change=change):
                self.verify(presentation=presentation, daily=daily)


if __name__ == '__main__':
    unittest.main()
