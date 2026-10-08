"""Current indexes must not resurrect retained annual source history."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_reference as core
from reading_context_overlays import load_fixture, repair_table
from test_annual_source_contexts import captured_table, FIXTURE


class AnnualStateContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load_fixture(FIXTURE)

    def test_superseded_history_has_explicit_inactive_state_and_preserves_raw(self):
        capture, table = captured_table(self.fixture, 16)
        result = repair_table(capture['context'], table, self.fixture, 'date_source')
        history = result['history'][0]
        self.assertEqual(history['raw_ref'], '2Pet 2:1-10')
        self.assertIs(history.get('active'), False)
        self.assertEqual(history.get('state'), 'superseded')
        self.assertEqual(history.get('status'), 'removed')
        self.assertIs(history.get('include_in_current_index'), False)

    def test_real_current_helper_excludes_history_and_explicit_historical_lane_retains_it(self):
        capture, table = captured_table(self.fixture, 16)
        result = repair_table(capture['context'], table, self.fixture, 'date_source')
        with tempfile.TemporaryDirectory() as tmp, patch.object(core, 'DATA', Path(tmp)):
            current = core.build_date_passage_index(result['history'])
            self.assertEqual(current, [])
            historic = core.build_date_passage_index(result['history'], include_inactive=True)
        self.assertEqual([r['matched_ref'] for r in historic], ['2Pet 2:1-10'])
        self.assertEqual(historic[0]['state'], 'superseded')
        self.assertIs(historic[0]['active'], False)
        self.assertEqual(result['history'][0]['raw_ref'], '2Pet 2:1-10')

    def test_removed_target_is_rejected_not_implicitly_restored(self):
        capture, table = captured_table(self.fixture, 57)
        target = next(r for r in table if r['slot']=='liturgy_catholic')
        target.update(active=False, state='removed', removal_effective_version='1.3.0')
        frozen = copy.deepcopy(table)
        with self.assertRaises(ValueError):
            repair_table(capture['context'], table, self.fixture, 'date_source')
        self.assertEqual(table, frozen)

    def test_removed_order_anchor_cannot_authorize_new_active_supplement(self):
        capture, table = captured_table(self.fixture, 57)
        table = [r for r in table if r['slot']!='liturgy_catholic']
        next(r for r in table if r['slot']=='liturgy_pauline').update(active=False, state='removed')
        with self.assertRaises(ValueError):
            repair_table(capture['context'], table, self.fixture, 'date_source')

    def test_supplement_copies_only_allowlisted_context_not_arbitrary_anchor_metadata(self):
        capture, table = captured_table(self.fixture, 57)
        table = [r for r in table if r['slot']!='liturgy_catholic']
        next(r for r in table if r['slot']=='liturgy_pauline')['unrelated_anchor_payload'] = 'must not leak'
        result = repair_table(capture['context'], table, self.fixture, 'date_source')
        new = next(r for r in result['active'] if r['slot']=='liturgy_catholic')
        self.assertNotIn('unrelated_anchor_payload', new)
        self.assertEqual(new['gregorian_date'], capture['date'])
        self.assertEqual(new['reading_type'], 'Catholic Epistle')

    def test_csv_state_and_removal_metadata_never_enter_current_indexes(self):
        capture, table = captured_table(self.fixture, 57)
        base = next(r for r in table if r['slot']=='liturgy_catholic')
        states = [dict(active='false'), dict(state='removed'), dict(status='removed'),
                  dict(include_in_current_index='false'), dict(removed_from_standard_lectionary='true'),
                  dict(removal_effective_version='1.3.0', removal_reason='prior suppression')]
        with tempfile.TemporaryDirectory() as tmp, patch.object(core, 'DATA', Path(tmp)):
            for state in states:
                with self.subTest(state=state):
                    self.assertEqual(core.build_date_passage_index([dict(base, **state)]), [])

    def test_blank_csv_state_cells_are_unmarked_not_inactive(self):
        capture, table = captured_table(self.fixture, 57)
        base = next(r for r in table if r['slot']=='liturgy_catholic')
        with tempfile.TemporaryDirectory() as tmp, patch.object(core, 'DATA', Path(tmp)):
            rows = core.build_date_passage_index([dict(base, active='', state='', status='', include_in_current_index='')])
        self.assertEqual([r['matched_ref'] for r in rows], ['James 1:12-21'])

    def test_removed_cycle_row_has_no_current_passage_occurrence(self):
        row = dict(source='katameros-api sqlite', source_table='AnnualReadings',
                   day_key='Tout 16', reading_slot='liturgy_catholic', raw_ref='60.2:1-10',
                   normalized_ref='1Pet 2:1-10', active=False, state='removed')
        self.assertEqual(core.build_passage_index([row], {60:'1 Peter'}), [])


if __name__ == '__main__':
    unittest.main()
