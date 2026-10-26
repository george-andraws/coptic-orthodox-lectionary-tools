"""Third Sunday of Babah: retain verse 24, without correcting other contexts."""
import datetime as dt
import hashlib
import unittest
from pathlib import Path

import build_lectionary_reference as core

ROOT = Path(__file__).resolve().parents[1]


class BabahThirdSundayPauline(unittest.TestCase):
    def test_reader_witness_includes_heading_and_actual_verse24(self):
        evidence = ROOT / 'sources/coptic-reader/babah-third-sunday-2026-10-25/Pauline.txt'
        raw = evidence.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), '880697daa4c3ad6d3681fdb54857791f051c2483d673b2fd2a09a1bf880c9e8a')
        self.assertIn('1 Corinthians 16:12-24', raw.decode())
        self.assertIn('24 My love be with you all in Christ Jesus. Amen.', raw.decode())

    def test_cached_today_pauline_keeps_raw_but_projects_complete_reader_range(self):
        _, readings = core.parse_copticchurch_html(
            (ROOT / 'cache/copticchurch_html/2026-10-25.html').read_text(), dt.date(2026, 10, 25))
        pauline = [r for r in readings if r['service_section'] == 'Liturgy' and r['reading_type'] == 'Pauline Epistle']
        self.assertEqual(len(pauline), 1)
        self.assertEqual(pauline[0]['raw_ref'], '1Cor 16:12-23')
        self.assertEqual(pauline[0]['normalized_ref'], '1Cor 16:12-24')
        index = core.build_date_passage_index(pauline)
        self.assertEqual([r['matched_ref'] for r in index], ['1Cor 16:12-24'])

    def test_recurring_third_sunday_all_supported_years(self):
        from convertdate import coptic
        for year in range(2020, 2036):
            cy, _, _ = coptic.from_gregorian(year, 10, 20)
            first = dt.date(*coptic.to_gregorian(cy, 2, 1))
            date = first + dt.timedelta(days=(6 - first.weekday()) % 7 + 14)
            with self.subTest(date=date.isoformat()):
                _, rows = core.parse_copticchurch_html(
                    (ROOT / 'cache/copticchurch_html' / (date.isoformat() + '.html')).read_text(), date)
                self.assertTrue(rows)
                self.assertEqual(rows[0]['day_title'], 'The third Sunday of Baba')
                pauline, = [r for r in rows if r['service_section'] == 'Liturgy' and r['reading_type'] == 'Pauline Epistle']
                self.assertEqual(pauline['normalized_ref'], '1Cor 16:12-24')
                self.assertIn(pauline['raw_ref'], {'1Cor 16:12-23', '1Cor 16:12-24'})

    def test_correction_is_not_a_blanket_reference_replacement(self):
        row = dict(day_title='The third Sunday of Baba', service_section='Liturgy',
                   reading_type='Pauline Epistle', raw_ref='1Cor 16:12-23',
                   normalized_ref='1Cor 16:12-23', source='copticchurch.net daily scrape',
                   url='https://copticchurch.net/readings?g_year=2026&g_month=10&g_day=25')
        self.assertEqual(core.apply_copticchurch_source_correction(row)['normalized_ref'], '1Cor 16:12-24')
        for field, value in [('day_title', 'The fourth Sunday of Babah'), ('service_section', 'Vespers'),
                             ('reading_type', 'Catholic Epistle'), ('source', 'unqualified witness'),
                             ('url', 'https://unqualified.example/readings'), ('raw_ref', '1Cor 16:12-22')]:
            with self.subTest(field=field):
                changed = dict(row, **{field: value})
                self.assertEqual(core.apply_copticchurch_source_correction(changed), changed)
        inactive = dict(row, active=False)
        self.assertEqual(core.apply_copticchurch_source_correction(inactive), inactive)


if __name__ == '__main__':
    unittest.main()
