"""Real consumer compatibility after explicit LK6 evidence decoding."""
import copy
import json

import pytest
import composite_followup_repairs as repairs
import source_reading_contracts as contracts
import build_design_deliverables as design
import verify_design_deliverables as verify
from test_luke_provenance_transport import complete_candidate


def test_candidate_all_exported_output_consumers_keep_primary_authentication():
    public = repairs.compact_public_rows(complete_candidate())
    # Direct contract entry accepts the new transport and retains its exact gate.
    verify.verify_source_contract_rows(public, candidate_projection=True, transport_mode='reverse')
    restored = repairs.restore_public_rows(public)
    reverse, _ = design.build_reverse_lectionary_index(restored, candidate_projection=True, transport_mode='reverse')
    verify.verify_source_contract_rows(reverse, candidate_projection=True, transport_mode='reverse')
    daily = design.build_daily_year_files(restored, candidate_projection=True, transport_mode='reverse')
    for days in daily.values():
        for date, readings in days.items():
            contracts.validate_consumer_rows([dict(r, gregorian_date=date) for r in readings], candidate_projection=True, transport_mode='daily')
    disclosure = design.build_passage_source_disclosure(restored, transport_mode='reverse')
    assert disclosure and len(disclosure) == len(restored)
    for consumer in (
        lambda rows: design.build_reverse_lectionary_index(rows, candidate_projection=True, transport_mode='reverse'),
        lambda rows: design.build_daily_year_files(rows, candidate_projection=True, transport_mode='reverse'),
        lambda rows: design.build_passage_source_disclosure(rows, transport_mode='reverse'),
        lambda rows: verify.verify_source_contract_rows(rows, candidate_projection=True, transport_mode='reverse'),
    ):
        bad = copy.deepcopy(public)
        bad[0]['source_disclosure'] = '[]'
        with pytest.raises(ValueError, match='source contract.*disclosure'):
            consumer(repairs.restore_public_rows(bad))


@pytest.mark.parametrize('family', ['psalmody', 'bright', 'covenant'])
def test_real_source_owned_raw_qualifiers_keep_body_and_lifecycle_guards(family):
    if family == 'psalmody':
        import psalmody_source_supplements as source
        rows, qualify = source.load_psalmody_source_rows(), source.qualify_psalmody_row
    elif family == 'bright':
        import bright_saturday_composite_supplements as source
        rows, qualify = source.load_bright_composite_rows(), source.qualify_bright_composite_row
    else:
        import covenant_thursday_source_supplements as source
        rows, qualify = source.load_covenant_thursday_rows(), source.qualify_covenant_thursday_row
    public = repairs.compact_public_rows(rows)
    decoded = repairs.restore_public_rows(public)
    assert decoded == rows
    assert all(qualify(row) is not None for row in decoded)
    # Exact primary-source equality, not a copied hash or family name.
    for mutation in ['body', 'missing', 'lifecycle', 'context']:
        bad = copy.deepcopy(public[0])
        if mutation == 'body':
            q = json.loads(bad['provenance_evidence_json'])
            body = json.loads(q['legacy_provenance'])
            body['forged_body'] = 'forged'
            q['legacy_provenance'] = json.dumps(body)
            bad['provenance_evidence_json'] = json.dumps(q)
        elif mutation == 'missing':
            del bad['provenance_evidence_json']
        elif mutation == 'lifecycle':
            bad['active'] = False
        else:
            bad['service_section'] = 'Foreign service'
        with pytest.raises(ValueError, match='(LK6|Unqualified)'):
            qualify(repairs.restore_public_row(bad))
