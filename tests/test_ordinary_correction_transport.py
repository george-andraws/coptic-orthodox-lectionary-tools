"""Retain the three bounded correction disclosures through real CSV transport."""
import copy
import csv
import datetime as dt
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import build_lectionary_reference as reference
import build_lectionary_crosswalk as crosswalk
import build_design_deliverables as design

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ('2026-09-01', '12:20-26', 'Jn 12:20-26', 'John 12:20-26',
     'sources/user-corrections/ordinary-appointment-repairs-2026-10-25.json'),
    ('2026-11-01', 'Psalm 79:13:00', 'Ps 79:13', 'Psalms 78:14',
     'sources/user-corrections/ordinary-appointment-repairs-2026-10-25.json'),
    ('2026-10-25', '1Cor 16:12-23', '1Cor 16:12-24', '1 Corinthians 16:12-24',
     'sources/user-corrections/babah-third-sunday-pauline.json'),
]


def indexed(case):
    date, raw, *_ = case
    _, rows = reference.parse_copticchurch_html(
        (ROOT / 'cache/copticchurch_html' / (date + '.html')).read_text(), dt.date.fromisoformat(date))
    selected = [r for r in rows if r['raw_ref'] == raw]
    assert len(selected) == 1
    rows = reference.build_date_passage_index(selected)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)
    buffer.seek(0)
    return list(csv.DictReader(buffer))


class OrdinaryCorrectionTransport(unittest.TestCase):
    def test_index_retains_the_exact_correction_locator(self):
        for case in CASES:
            with self.subTest(date=case[0]):
                self.assertEqual(indexed(case)[0]['correction_source'], case[4])

    def test_index_disclosure_reauthenticates_the_three_retained_contracts(self):
        import ordinary_correction_transport as disclosure
        for case in CASES:
            with self.subTest(date=case[0]):
                row, = indexed(case)
                q = disclosure.transport_for_index(row)['ordinary_source_correction']
                self.assertEqual((q['original_raw_ref'], q['corrected_ref'], q['reader_printed_ref']), case[1:4])
                for field, value in [('matched_ref','Ps 79:14'), ('normalization_warning','forged'),
                                     ('weekday','Friday'), ('active',False)]:
                    with self.subTest(field=field), self.assertRaises(ValueError):
                        disclosure.transport_for_index(dict(row, **{field:value}))

    def test_disclosure_qualifier_accepts_only_its_real_projected_context(self):
        import ordinary_correction_transport as disclosure
        for case in CASES:
            source, = indexed(case)
            projected, = crosswalk.project_date_rows([source])
            # Unit boundary: install the authenticated transport, not fake source evidence.
            projected['provenance'] = json.dumps({'consumer_source_transport': disclosure.transport_for_index(source)})
            qualified = disclosure.qualify_projected_row(projected)
            self.assertIsNotNone(qualified)
            assert qualified is not None
            self.assertEqual(qualified['corrected_ref'], case[2])
            for field, value in [('source_kind','pascha_day_hour'), ('source_family','coptic_reader'),
                                 ('gregorian_date','2026-01-01'), ('active',False), ('source_ref','Ps 79:14')]:
                with self.subTest(date=case[0], field=field), self.assertRaises(ValueError):
                    disclosure.qualify_projected_row(dict(projected, **{field:value}))
            for bad in [True, 0, 'false']:
                forged = copy.deepcopy(projected)
                payload = json.loads(forged['provenance'])
                payload['consumer_source_transport']['ordinary_source_correction']['fresh_app_verification'] = bad
                forged['provenance'] = json.dumps(payload)
                with self.assertRaises(ValueError):
                    disclosure.qualify_projected_row(forged)

    def test_real_daily_and_reverse_disclosures_keep_both_printed_coordinates(self):
        for case in CASES:
            with self.subTest(date=case[0]):
                source, = indexed(case)
                projected, = crosswalk.project_date_rows([source])
                transport = design.consumer_source_transport(projected)
                q = transport['ordinary_source_correction']
                self.assertEqual((q['original_raw_ref'], q['corrected_ref'], q['reader_printed_ref']), case[1:4])
                self.assertEqual(q['correction_source'], case[4])
                self.assertFalse(q['fresh_app_verification'])
                self.assertFalse(q['independent_recurring_year_confirmation'])
                self.assertEqual(len(q['source_sha256']), 64)
                presentation, _ = design.build_reverse_presentation([projected])
                self.assertIn(q['source_sha256'], presentation[0]['source_locator'])
                daily = design.build_daily_year_files(presentation, transport_mode='presentation')[2026][case[0]]
                self.assertEqual(daily[0]['canonical_mt_ref'], case[2])
                self.assertIn('ordinary_source_correction', daily[0]['source_disclosure'])
                self.assertIn(case[1], daily[0]['source_disclosure'])
                self.assertIn(case[3], daily[0]['source_disclosure'])
                expected = {design.occasion_index_key(presentation[0])}
                def exact_subset(rows):
                    self.assertEqual(len(rows), 1)
                    self.assertEqual({design.occasion_index_key(r) for r in rows}, expected)
                with patch.object(design, 'verify_reverse_index_contract', side_effect=exact_subset):
                    reverse, disagreements = design.build_reverse_lectionary_index(presentation, transport_mode='presentation')
                self.assertEqual(disagreements, [])
                self.assertIn('ordinary_source_correction', reverse[0]['source_disclosure'])
                self.assertIn(case[3], reverse[0]['source_disclosure'])

    def test_a_copied_disclosure_does_not_qualify_a_changed_projected_row(self):
        source, = indexed(CASES[1])
        projected, = crosswalk.project_date_rows([source])
        self.assertIn('ordinary_source_correction', design.consumer_source_transport(projected))
        changes = [('gregorian_date','2026-11-02'), ('source_family','coptic_reader'),
                   ('source_kind','pascha_day_hour'), ('service_section','Matins'),
                   ('day_title','The third Sunday of Baba'), ('passage','Ps 79:14'),
                   ('source_ref','Ps 79:14'), ('raw_ref','Psalm 79:14:00'), ('active',False)]
        for field, value in changes:
            with self.subTest(field=field), self.assertRaises(ValueError):
                design.build_reverse_presentation([dict(projected, **{field:value})])
        forged = copy.deepcopy(projected)
        payload = json.loads(forged['provenance'])
        payload['consumer_source_transport']['ordinary_source_correction']['source_sha256'] = '0' * 64
        forged['provenance'] = json.dumps(payload)
        with self.assertRaises(ValueError):
            design.build_reverse_presentation([forged])


if __name__ == '__main__':
    unittest.main()
