"""Remaining independently reproduced Sunday consumer boundaries."""
import copy
import json
import unittest
from unittest.mock import patch
import build_design_deliverables as design
import build_lectionary_crosswalk as cross
import source_reading_contracts as contracts
from test_sunday_consumer_remediation import sunday_rows, serialize


class RemainingSundayConsumers(unittest.TestCase):
    def setUp(self):
        self.presentation = design.build_reverse_presentation(serialize(cross.project_date_rows([sunday_rows()[0]]), cross.FIELDS))[0]

    def emitted(self):
        daily = design.build_daily_year_files(self.presentation, transport_mode='presentation')[2027]['2027-02-21'][0]
        reverse = []
        validator = design.verify_reverse_index_contract
        def observe(rows):
            reverse.extend(rows)
            return validator(rows)
        with patch.object(design, 'verify_reverse_index_contract', observe), self.assertRaises(AssertionError):
            design.build_reverse_lectionary_index(self.presentation, transport_mode='presentation')
        return [daily, reverse[0]]

    def test_actual_serialized_disclosure_and_count_are_authenticated(self):
        for row in self.emitted():
            contracts.validate_consumer_rows([row])
            for attack in ('omit', 'body', 'hold', 'remove', 'locator', 'count', 'identity', 'spans', 'canonical-omit'):
                bad = copy.deepcopy(row)
                disclosure = json.loads(bad['source_disclosure'])
                if attack == 'omit':
                    bad.pop('source_disclosure')
                elif attack == 'count':
                    bad['source_disclosure_count'] = '2'
                elif attack in ('identity', 'spans', 'canonical-omit'):
                    bad.pop({'identity': 'identity_key', 'spans': 'spans_json', 'canonical-omit': 'canonical_mt_ref'}[attack])
                else:
                    transport = disclosure[0]['consumer_source_transport'][0]
                    if attack == 'body':
                        transport['source_block']['literal_block'] = 'forged'
                    elif attack == 'hold':
                        transport['normalization_state'] = 'source_qualified'
                    elif attack == 'remove':
                        transport['state'] = {'current_status': 'removed'}
                    else:
                        disclosure[0]['source_locator'] = 'forged'
                    bad['source_disclosure'] = json.dumps(disclosure)
                with self.subTest(surface='reverse' if 'collapsed_row_count' in row else 'daily', attack=attack), self.assertRaises(ValueError):
                    contracts.validate_consumer_rows([bad])

    def test_direct_citation_and_collapsed_disclosure_reject_counterfeit(self):
        for attack in ('body', 'source_ref', 'locator', 'canonical', 'family'):
            bad = copy.deepcopy(self.presentation[0])
            prov = json.loads(bad['provenance'])
            if attack == 'body':
                prov['consumer_source_transport']['source_block']['literal_block'] = 'forged'
            elif attack == 'source_ref':
                bad['source_ref'] = 'Ps 150:1'
            elif attack == 'locator':
                bad['source_locator'] = 'forged'
            elif attack == 'canonical':
                bad['canonical_mt_ref'] = 'Ps 17:3,17:15'
            else:
                bad['source_family'] = 'ordinary_date_resolved'
                prov.pop('consumer_source_transport')
                bad.update(design.identity_for('Ps 17:3,17:15'))
            bad['provenance'] = json.dumps(prov)
            for consumer in (lambda r: design.row_citation(r[0]), design.build_collapsed_source_disclosure):
                with self.subTest(attack=attack), self.assertRaises(ValueError):
                    consumer([bad])

    def test_current_status_and_is_active_retained_not_restored(self):
        for marker in ({'current_status': 'removed'}, {'current_status': 'inactive'},
                       {'current_status': 'superseded'}, {'current_status': 'historical_witness'},
                       {'is_active': False}, {'is_active': '0'}):
            with self.subTest(marker=marker):
                rows = serialize(cross.project_date_rows([dict(sunday_rows()[0], **marker)]), cross.FIELDS)
                transport = json.loads(rows[0]['provenance'])['consumer_source_transport']
                for k, v in marker.items():
                    self.assertEqual(transport.get('state', {}).get(k), v)
                p = design.build_reverse_presentation(rows)[0]
                self.assertEqual(p[0]['current_status'], 'historical_candidate_removed')
                self.assertEqual(design.build_daily_year_files(p, transport_mode='presentation'), {})
                self.assertTrue(design.build_collapsed_source_disclosure(p)[0])

    def test_supported_current_states_remain_current(self):
        for status in ('current', 'active', 'current_public_or_local_reference',
                       'current_confirmed_coptic_reader', 'pending_psalm_equivalence_unresolved'):
            rows = cross.project_date_rows([dict(sunday_rows()[0], current_status=status)])
            p = design.build_reverse_presentation(rows)[0]
            self.assertTrue(design.build_daily_year_files(p, transport_mode='presentation'))

    def test_actual_citation_is_authenticated(self):
        row = design.build_passage_source_disclosure(self.presentation, transport_mode='presentation')[0]
        contracts.validate_consumer_rows([row])
        row['citation'] = 'forged source attribution'
        with self.assertRaises(ValueError):
            contracts.validate_consumer_rows([row])


if __name__ == '__main__':
    unittest.main()
