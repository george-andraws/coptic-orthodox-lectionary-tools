"""Retained evidence must be authenticated at the actual projection boundary."""
import unittest
from unittest.mock import patch

import build_design_deliverables as design
import pascha_resolution_evidence as evidence


def friday():
    return {'day_title': 'Good Friday', 'liturgical_place': 'Good Friday',
            'service_hour': 'Twelfth Hour', 'service_section': 'Twelfth Hour',
            'source_kind': 'pascha_day_hour', 'source_family': 'holy_pascha_curated_day_hour',
            'source_file': 'out/data/pascha_day_hour_index.csv', 'reading_slot': 'OT1',
            'passage': 'Lam 3:1-66'}


def hosanna():
    return {'day_title': 'Hosanna Sunday', 'liturgical_place': 'Hosanna Sunday',
            'service_hour': 'Ninth Hour', 'service_section': 'Ninth Hour',
            'calendar_key': 'Hosanna Sunday | Ninth Hour',
            'source_kind': 'pascha_day_hour', 'source_family': 'holy_pascha_curated_day_hour',
            'reading_slot': 'Gospel', 'gregorian_date': '', 'passage': 'Matt 21:1-17'}


class PaschaEvidenceProjectionIntegration(unittest.TestCase):
    def test_good_friday_status_fails_closed_on_retained_evidence_drift(self):
        with patch.object(evidence, 'authenticate_pascha_evidence', side_effect=ValueError('retained evidence drift')):
            for ref in ['Lam 3:1-66', 'Jonah 1:10-2:8']:
                with self.subTest(ref=ref), self.assertRaisesRegex(ValueError, 'retained evidence drift'):
                    design.qualified_reader_pascha_resolution(friday(), ref)

    def test_hosanna_appointment_creation_fails_closed_on_retained_evidence_drift(self):
        with patch.object(evidence, 'authenticate_pascha_evidence', side_effect=ValueError('retained evidence drift')):
            with self.assertRaisesRegex(ValueError, 'retained evidence drift'):
                design.hosanna_sunday_reader_prophecy_rows([hosanna()])

    def test_good_friday_reader_citation_retains_portable_authenticated_locator(self):
        row = friday()
        locator = design.source_locator_for(row, {})
        expected = evidence.authenticate_pascha_evidence('good_friday_twelfth')
        self.assertIn(expected['path'], locator)
        self.assertIn(expected['sha256'], locator)

    def test_unrelated_or_inactive_context_cannot_inherit_reader_resolution(self):
        for changes in [{'source_family': 'ordinary_date_resolved'}, {'source_kind': 'special_service'},
                        {'day_title': 'Good Friday Eve'}, {'service_hour': 'Eleventh Hour'},
                        {'active': False}, {'state': 'superseded'}]:
            with self.subTest(changes=changes), patch.object(evidence, 'authenticate_pascha_evidence') as authenticate:
                self.assertIsNone(design.qualified_reader_pascha_resolution(dict(friday(), **changes), 'Lam 3:1-66'))
                authenticate.assert_not_called()

    def test_hosanna_row_retains_authenticated_capture_instead_of_external_archive(self):
        rows = design.hosanna_sunday_reader_prophecy_rows([hosanna()])
        self.assertEqual(len(rows), 1)
        expected = evidence.authenticate_pascha_evidence('hosanna_sunday_day_ninth')
        self.assertEqual(rows[0]['source_file'], expected['path'])
        self.assertIn(expected['sha256'], rows[0]['provenance'])
        self.assertEqual(rows[0]['normalized_ref'], 'Lam 1:1-4')


if __name__ == '__main__':
    unittest.main()
