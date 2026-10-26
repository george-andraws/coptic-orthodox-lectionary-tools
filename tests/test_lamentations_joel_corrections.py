"""Reader resolution and Joel chapter-seam corrections. Not a full Lent enrichment."""
import datetime as dt
import unittest

import build_design_deliverables as design
from calendar_resolution import julian_pascha_gregorian


class LamentationsJoelCorrections(unittest.TestCase):
    def test_joel_lxx_keeps_printed_english_and_names_hebrew_chapters(self):
        first = design.identity_for('Joel 2:28-32')
        self.assertEqual(first['canonical_mt_ref'], 'Joel 2:28-32')
        self.assertEqual(first['canonical_lxx_ref'], 'Joel 3:1-5')
        self.assertEqual(first['display_ref'], 'Joel 2:28-32 (LXX Joel 3:1-5)')
        self.assertIn('four chapters', first['canonicalization_note'])
        second = design.identity_for('Joel 3:9-21')
        self.assertEqual(second['canonical_mt_ref'], 'Joel 3:9-21')
        self.assertEqual(second['canonical_lxx_ref'], 'Joel 4:9-21')
        self.assertEqual(second['display_ref'], 'Joel 3:9-21 (LXX Joel 4:9-21)')
        unchanged = design.identity_for('Joel 2:12-27')
        self.assertEqual(unchanged['canonical_lxx_ref'], 'Joel 2:12-27')

    def test_good_friday_reader_confirms_lamentations_and_retires_jonah(self):
        lam = {'day_title': 'Good Friday', 'service_hour': 'Twelfth Hour', 'source_kind': 'pascha_day_hour',
               'source_family': 'holy_pascha_curated_day_hour'}
        resolved = design.qualified_reader_pascha_resolution(lam, 'Lam 3:1-66')
        self.assertIsNotNone(resolved)
        status, note = resolved
        self.assertEqual(status, 'current_confirmed_coptic_reader')
        self.assertIn('no Jonah', note)
        jonah = design.qualified_reader_pascha_resolution(lam, 'Jonah 1:10-2:8')
        self.assertIsNotNone(jonah)
        self.assertEqual(jonah[0], 'historical_candidate_removed')
        self.assertIn('1:10-2:7', jonah[1])
        self.assertIn('2:8', jonah[1])
        marker = design.removed_marker_for(
            lam, {'canonical_mt_ref': 'Jonah 1:10-2:8', 'source_label': 'Jonah 1:10-2:8'})
        self.assertEqual(marker, 'edition_specific_not_current_reader_practice')

    def test_hosanna_row_is_sunday_day_and_does_not_relabel_ottawa(self):
        template = {
            'day_title': 'Hosanna Sunday', 'service_hour': 'Ninth Hour', 'service_section': 'Ninth Hour',
            'source_kind': 'pascha_day_hour', 'reading_slot': 'Gospel', 'gregorian_date': '',
            'source_family': 'holy_pascha_curated_day_hour',
            'liturgical_place': 'Hosanna Sunday', 'passage': 'Matt 21:10-17',
        }
        monday = dict(template, day_title='Monday Eve', liturgical_place='Monday Eve', service_hour='Ninth Hour')
        rows = design.hosanna_sunday_reader_prophecy_rows([template, monday])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['day_title'], 'Hosanna Sunday')
        self.assertEqual(rows[0]['reading_slot'], 'OT1')
        self.assertNotIn('Monday Eve', rows[0]['calendar_key'])
        self.assertNotEqual(rows[0]['source_kind'], 'pascha_source_text')

    def test_lent_prophecy_projection_skips_annunciation(self):
        cycle = {
            'calendar_key': 'week 5 day_of_week 3', 'canonical_mt_ref': 'Joel 3:9-21',
            'source_kind': 'katameros_cycle', 'source_family': 'katameros_cycle',
            'source_file': 'sources/katameros-api/Core/KatamerosDatabase.db', 'source_row_id': '5408',
            'source_locator': 'row 5408',
        }
        ordinary = [{'occasion': 'Wednesday of the fifth week of Great Lent', 'service_section': 'Matins', 'display_ref': 'Ps 1:1'}]
        feast = [{'occasion': 'Annunciation', 'service_section': 'Matins', 'display_ref': 'Lk 1:26-38'}]
        by_year = {2026: {'2026-03-18': ordinary}, 2027: {'2027-04-07': feast}}
        design.project_katameros_lent_prophecies(by_year, [cycle])
        self.assertEqual(ordinary[0]['display_ref'], 'Joel 3:9-21 (LXX Joel 4:9-21)')
        self.assertEqual(ordinary[0]['current_status'], 'current_public_or_local_reference')
        self.assertEqual([row['display_ref'] for row in feast], ['Lk 1:26-38'])
        pascha = julian_pascha_gregorian(2026)
        self.assertEqual(pascha - dt.timedelta(days=25), dt.date(2026, 3, 18))


if __name__ == '__main__':
    unittest.main()
