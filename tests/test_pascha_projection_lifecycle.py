"""Lifecycle and context notes must remain truthful through real projection."""
import copy
import json
import unittest

import build_design_deliverables as design


class PaschaProjectionLifecycle(unittest.TestCase):
    def test_good_friday_jonah_note_is_not_a_wednesday_fixture_explanation(self):
        row = dict(day_title='Good Friday', service_hour='Twelfth Hour',
                   source_kind='pascha_day_hour', source_family='holy_pascha_curated_day_hour', passage='Jonah 1:10-2:8')
        status, note = design.status_for(row, design.identity_for(row['passage']), set())
        self.assertEqual(status, 'historical_candidate_removed')
        self.assertIn('Twelfth', note.replace('12th', 'Twelfth'))
        self.assertIn('Ottawa', note)
        self.assertNotIn('Wednesday Day', note)

    @staticmethod
    def source():
        return dict(calendar_key='week 5 day_of_week 3', canonical_mt_ref='Joel 3:9-21',
                    source_kind='katameros_cycle', source_family='katameros_cycle',
                    current_status='current_public_or_local_reference',
                    source_file='sources/katameros-api/Core/KatamerosDatabase.db',
                    source_row_id='5408', source_locator='row 5408',
                    source_title='Katameros API retained database', source_edition='Retained source')

    @staticmethod
    def days():
        return {2026: {'2026-03-18': [dict(occasion='Wednesday of the fifth week of Great Lent',
                                        service_section='Matins', display_ref='Ps 1:1')]}}

    def test_historical_or_wrong_family_joel_cannot_be_reactivated(self):
        for mutation in [dict(current_status='historical_witness'), dict(active=False),
                         dict(removed_marker='superseded source'), dict(source_family='annual_fixed')]:
            with self.subTest(mutation=mutation):
                days = self.days()
                before = copy.deepcopy(days)
                with self.assertRaisesRegex(AssertionError, 'Missing.*prophecy'):
                    design.project_katameros_lent_prophecies(days, [dict(self.source(), **mutation)])
                self.assertEqual(days, before)

    def test_added_joel_keeps_source_disclosure_status_and_is_idempotent(self):
        days = self.days()
        design.project_katameros_lent_prophecies(days, [self.source()])
        rows = days[2026]['2026-03-18']
        added = rows[0]
        disclosure = json.loads(added['source_disclosure'])
        self.assertTrue(disclosure)
        self.assertEqual(disclosure[0]['source_family'], 'katameros_cycle')
        self.assertIn('row 5408', disclosure[0]['source_locator'])
        self.assertEqual(added['current_status'], self.source()['current_status'])
        before = copy.deepcopy(days)
        design.project_katameros_lent_prophecies(days, [self.source()])
        self.assertEqual(days, before)


if __name__ == '__main__':
    unittest.main()
