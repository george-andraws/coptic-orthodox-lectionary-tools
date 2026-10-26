"""Ordinary daily Psalms follow retained source ordinals, not reverse-index order."""
import copy

import datetime as dt
import unittest
from pathlib import Path

import build_design_deliverables as design
import build_lectionary_crosswalk as crosswalk
import build_lectionary_reference as reference

ROOT = Path(__file__).resolve().parents[1]


class OrdinaryPsalmCompanionOrder(unittest.TestCase):
    def test_tokens_sharing_source_identity_keep_order_and_occasion_boundaries(self):
        base = dict(gregorian_date='2026-02-18', service_section='Liturgy', service_hour='',
                    slot='Psalm', source_kind='copticchurch_date', source_family='ordinary_date_resolved',
                    source_file='cache/copticchurch_html', source_row_id='same-row', source_order=1,
                    current_status='current_public_or_local_reference')
        rows = [dict(base, occasion=occasion, source_token_order=token, canonical_mt_ref=ref)
                for occasion in ['ordinary day', 'ordinary day Eve']
                for token, ref in [(2, 'Ps 25:16'), (1, 'Ps 25:20')]]
        original = copy.deepcopy(rows)
        daily = design.build_daily_year_files(rows)[2026]['2026-02-18']
        self.assertEqual([(r['occasion'], r['canonical_mt_ref']) for r in daily],
                         [(occasion, ref) for occasion in ['ordinary day', 'ordinary day Eve']
                          for ref in ['Ps 25:20', 'Ps 25:16']])
        self.assertEqual(rows, original)

    def test_real_corrected_source_survives_passage_sorted_crosswalk(self):
        date = dt.date(2026, 2, 18)
        _, source = reference.parse_copticchurch_html(
            (ROOT / 'cache/copticchurch_html/2026-02-18.html').read_text(), date)
        source = [r for r in source if r['service_section'] == 'Liturgy' and r['reading_type'] == 'Psalm']
        self.assertEqual(source[0]['normalized_ref'], 'Ps 25:20; Ps 25:16')
        indexed = reference.build_date_passage_index(source)
        self.assertEqual([r['matched_ref'] for r in indexed], ['Ps 25:20', 'Ps 25:16'])
        projected = crosswalk.project_date_rows(indexed)
        # Reverse storage is legitimately passage sorted; daily must recover the
        # retained source ordinals, without changing reverse membership or bytes.
        projected.sort(key=lambda r: r['passage'])
        original = copy.deepcopy(projected)
        # Load the complete production context (including the Katameros prophecy
        # dependency); partial Lent tables are intentionally rejected.
        presentation, _ = design.build_reverse_presentation()
        daily = design.build_daily_year_files(presentation, transport_mode='presentation')[2026][date.isoformat()]
        self.assertEqual([r['canonical_mt_ref'] for r in daily
                          if r['service_section'] == 'Liturgy' and r['slot'] == 'Psalm'],
                         ['Ps 25:20', 'Ps 25:16'])
        self.assertEqual(projected, original)

    def test_other_sources_and_unordered_companions_keep_supplied_order(self):
        base = dict(gregorian_date='2026-02-18', occasion='ordinary fixture',
                    service_section='Liturgy', service_hour='', slot='Psalm',
                    source_kind='copticchurch_date', source_family='ordinary_date_resolved',
                    source_file='cache/copticchurch_html', current_status='current_public_or_local_reference')
        for change in ({'source_kind': 'other'}, {'source_family': 'other'},
                       {'source_file': 'other'}, {'source_order': ''}):
            rows = [dict(base, source_order=n, source_token_order=1,
                         source_row_id=str(n), canonical_mt_ref=ref, **change)
                    for n, ref in [(2, 'Ps 25:16'), (1, 'Ps 25:20')]] if 'source_order' not in change else [
                        dict(base, source_row_id=str(n), canonical_mt_ref=ref, **change)
                        for n, ref in [(2, 'Ps 25:16'), (1, 'Ps 25:20')]]
            daily = design.build_daily_year_files(rows)[2026]['2026-02-18']
            self.assertEqual([r['canonical_mt_ref'] for r in daily], ['Ps 25:16', 'Ps 25:20'])


if __name__ == '__main__':
    unittest.main()
