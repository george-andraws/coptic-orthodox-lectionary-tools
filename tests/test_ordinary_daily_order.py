"""Ordinary daily service ordering comes from captured Reader slots, not file order."""
import copy
import unittest

import build_design_deliverables as design
from test_annual_source_contexts import captured_table, FIXTURE
from reading_context_overlays import load_fixture

TYPE_SLOTS = {('Vespers','gospel'):'vespers_gospel', ('Matins','gospel'):'matins_gospel',
              ('Liturgy','pauline'):'liturgy_pauline', ('Liturgy','catholicon'):'liturgy_catholic',
              ('Liturgy','praxis'):'liturgy_acts', ('Liturgy','gospel'):'liturgy_gospel'}


def presentation(table):
    return [dict(gregorian_date=r['gregorian_date'], occasion=r['day_title'],
                 service_section=r['service_section'], service_hour='', slot=r['reading_type'],
                 display_ref=r['normalized_ref'], source_kind='copticchurch_date',
                 source_family='ordinary_date_resolved', source_row_id=str(i),
                 current_status='current_working_source_not_coptic_reader_checked',
                 slot_type='', slot_order='') for i,r in enumerate(table)]


class OrdinaryDailyOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load_fixture(FIXTURE)

    def test_captured_annual_slots_order_correctly_when_presentation_is_scrambled(self):
        # Expected slots derive from the independently authenticated Reader oracle.
        for ident in (16,17,19,26,54,57,59):
            with self.subTest(context=ident):
                capture, table = captured_table(self.fixture, ident)
                inputs = list(reversed(presentation(table)))
                frozen = copy.deepcopy(inputs)
                daily = design.build_daily_year_files(inputs)[int(capture['date'][:4])][capture['date']]
                actual = [TYPE_SLOTS.get((r['service_section'], r['slot_type']), 'missing_or_invalid_slot_metadata')
                          for r in daily if r['slot_type']!='psalm']
                expected = [r['slot'] for r in capture['source_approved_nonPsalm']]
                self.assertEqual(actual, expected)
                self.assertTrue(all(r['slot_order']==1 for r in daily))
                self.assertEqual(inputs, frozen)
                self.assertCountEqual([r['display_ref'] for r in daily], [r['display_ref'] for r in inputs])

    def test_psalm_precedes_gospel_in_each_ordinary_service(self):
        capture, table = captured_table(self.fixture, 16)
        daily = design.build_daily_year_files(list(reversed(presentation(table))))[2026][capture['date']]
        for section in ('Vespers','Matins','Liturgy'):
            kinds=[r['slot_type'] for r in daily if r['service_section']==section]
            self.assertIn('psalm', kinds)
            self.assertIn('gospel', kinds)
            self.assertLess(kinds.index('psalm'), kinds.index('gospel'))

    def test_split_psalm_fragments_keep_relative_order_without_verse_sorting(self):
        capture, table = captured_table(self.fixture, 16)
        rows = presentation(table)
        ps = next(r for r in rows if r['service_section']=='Matins' and r['slot']=='Psalm')
        rows = [r for r in rows if r is not ps]
        rows += [dict(ps, display_ref='Ps 33:11', source_row_id='fragment-first'),
                 dict(ps, display_ref='Ps 33:10', source_row_id='fragment-second')]
        daily = design.build_daily_year_files(rows)[2026][capture['date']]
        fragments = [r['display_ref'] for r in daily if r['service_section']=='Matins' and r['slot']=='Psalm']
        self.assertEqual(fragments, ['Ps 33:11','Ps 33:10'])

    def test_unqualified_family_and_hour_contexts_are_not_reordered_or_typed(self):
        capture, table = captured_table(self.fixture, 16)
        for changes in ({'source_family':'unverified_variant'}, {'source_kind':'pascha_day_hour'},
                        {'service_hour':'First Hour'}, {'service_section':'First Hour'}):
            inputs=[dict(r, **changes) for r in reversed(presentation(table))]
            daily=design.build_daily_year_files(inputs)[2026][capture['date']]
            self.assertEqual([r['display_ref'] for r in daily], [r['display_ref'] for r in inputs])
            self.assertEqual([r['slot_type'] for r in daily], ['']*len(inputs))


if __name__=='__main__': unittest.main()
