"""LK6 round trips use complete valid controls and real exported validators."""
import copy
import json
from pathlib import Path

import pytest
import composite_followup_repairs as repairs
import resolver_review_repairs as resolver
import source_reading_contracts as contracts

ROOT = Path(__file__).resolve().parents[1]


def test_real_runtime_composite_has_short_source_and_no_private_token_after_public_projection():
    frozen = json.loads((ROOT / 'tests/fixtures/resolver_review_runtime_1_3_6.json').read_text())
    rows, _ = resolver.repair_daily_rows('2026-04-02', frozen['daily']['2026-04-02'])
    projected = repairs.compact_public_rows(rows)
    assert '_review_original_row' not in json.dumps(projected)
    assert all(len(r.get('provenance', '')) <= 300 for r in projected)
    restored = repairs.restore_public_rows(projected)
    assert restored == rows
    assert repairs.compact_public_rows(projected) == projected


def complete_candidate():
    import build_design_deliverables as design
    tables, _ = contracts.load_reviewed_tables()
    raw = contracts.project_table(next(t for t in tables if not t['staged']))
    presentation, _ = design.build_reverse_presentation(raw, candidate_projection=True)
    reverse, _ = design.build_reverse_lectionary_index(presentation, candidate_projection=True, transport_mode='presentation')
    return reverse


def test_complete_valid_candidate_through_real_exported_consumer():
    rows = complete_candidate()
    contracts.validate_consumer_rows(rows, candidate_projection=True)
    public = repairs.compact_public_rows(rows)
    assert all(not r['provenance'].lstrip().startswith(('{', '[')) for r in public)
    # Authentication is performed by the real consumer, not the transport adapter.
    contracts.validate_consumer_rows(public, candidate_projection=True)
    contracts.validate_consumer_rows(repairs.restore_public_rows(public), candidate_projection=True)
    assert repairs.restore_public_rows(public) == rows


@pytest.mark.parametrize('mutation', ['body', 'missing', 'disclosure', 'context', 'label'])
def test_compacted_evidence_cannot_forge_or_hide_candidate_disclosures(mutation):
    public = repairs.compact_public_rows(complete_candidate())
    contracts.validate_consumer_rows(repairs.restore_public_rows(public), candidate_projection=True)
    row = public[0]
    if mutation == 'body':
        q = json.loads(row['provenance_evidence_json'])
        p = json.loads(q['legacy_provenance'])
        p['metadata']['edition_id'] = 'forged'
        q['legacy_provenance'] = json.dumps(p)
        row['provenance_evidence_json'] = json.dumps(q)
    elif mutation == 'missing':
        del row['provenance_evidence_json']
    elif mutation == 'disclosure':
        row['source_disclosure'] = '[]'
    elif mutation == 'context':
        row['service_section'] = 'Vespers'
    else:
        row['provenance'] = 'fresh Reader verification'
    with pytest.raises(ValueError, match='(LK6|source contract)'):
        contracts.validate_consumer_rows(repairs.restore_public_rows(public), candidate_projection=True)


def test_transport_rejects_duplicate_and_unexpected_members():
    row = repairs.compact_public_rows(complete_candidate())[0]
    for payload in ['{"schema":"lectionary_provenance_v1","schema":"forged","legacy_provenance":"{}"}',
                    '{"schema":"lectionary_provenance_v1","legacy_provenance":"{}","extra":true}']:
        with pytest.raises(ValueError, match='LK6'):
            repairs.restore_public_rows([dict(row, provenance_evidence_json=payload)])
