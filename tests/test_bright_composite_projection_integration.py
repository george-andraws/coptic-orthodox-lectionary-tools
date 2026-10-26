"""Bounded real Bright raw/CSV/design projections; production ledger stays enforced."""
import copy
import csv
import io
import json
from unittest.mock import patch

import pytest
import build_design_deliverables as design
import build_lectionary_crosswalk as crosswalk
import bright_saturday_composite_supplements as bright

# Independent literal identity and historical membership oracles.
CASES = [
    ('Matins', 'Ps 44:23,44:26', 'rid_d58dc513121900158fc9'),
    ('Matins', 'Ps 126:2-3', 'rid_16e3ff8ccefe525d98e0'),
    ('6th Hour', 'Ps 142:7', 'rid_969f73205a3c4d8ceef6'),
    ('Liturgy', 'Ps 82:8', 'rid_5be18395526b0ff8b009'),
]
HISTORICAL_KEYS = {
    ('6TH HOUR', '6th Hour', '', 'Psalm', 'rid_f8f64afe999bed4ad0e1'),
    ('MATINS / RAISING OF INCENSE', 'Matins', '', 'Psalm', 'rid_01f32bd787164f059e93'),
    ('MATINS / RAISING OF INCENSE', 'Matins', '', 'Psalm', 'rid_cf1a402c8a2d11ef55de'),
    ('ST. BASIL LITURGY – LITURGY OF THE WORD', 'Liturgy', '', 'Psalm', 'rid_c6e5abb3b44d8783f05f'),
}
HELD_KEYS = {('Bright Saturday', service, '', 'Psalm', identity) for service, _, identity in CASES}


def csv_transport(rows, fields=None):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fields or list(rows[0]))
    writer.writeheader(); writer.writerows(rows); stream.seek(0)
    return list(csv.DictReader(stream))


def raw_rows():
    # Actual creator and union-schema serialization, not standalone helper rows.
    rows = crosswalk.project_bright_rows(crosswalk.read_csv(crosswalk.BRIGHT_CSV), crosswalk.BRIGHT_CSV)
    return csv_transport(rows, crosswalk.FIELDS)


def selected_presentation():
    raw = [r for r in raw_rows() if r['source_kind'] == bright.SOURCE_KIND]
    rows, _ = design.build_reverse_presentation(raw)
    return csv_transport(rows)


def exact_subset(rows):
    assert len(rows) == 4
    assert {design.occasion_index_key(r) for r in rows} == HELD_KEYS


def reverse(rows):
    with patch.object(design, 'verify_reverse_index_contract', side_effect=exact_subset):
        return design.build_reverse_lectionary_index(rows, transport_mode='presentation')[0]


def test_literal_identities_csv_and_disclosures():
    rows = selected_presentation()
    assert [(r['service_section'], r['identity_key']) for r in rows] == [(s, i) for s, _, i in CASES]
    for row, (_, label, _) in zip(rows, CASES):
        assert row['canonical_mt_ref'] == row['canonical_lxx_ref'] == ''
        assert row['spans_json'] == '[]'
        assert row['current_status'] == 'pending_psalm_equivalence_unresolved'
        assert row['source_key'] == 'coptic_reader_qualified_bright_composite'
        assert row['source_convention'] == bright.CONVENTION
        assert label in row['display_ref']
    outputs = reverse(rows)
    for row in outputs:
        q = json.loads(row['provenance'])
        disclosure, = json.loads(row['source_disclosure'])
        assert q['document']['sha256'] in disclosure['source_locator']
        assert q['document']['body_sha256'] in disclosure['source_locator']
        assert q['printed_ref'] in disclosure['source_locator']
        assert 'not fresh app verification' in disclosure['source_edition']
        assert 'canonical' in disclosure['source_edition']
        assert disclosure['bright_composite_source'][0] == q
        assert row['source_order'] == q['source_order']
        assert row['source_token_order'] == q['source_token_order']


def test_daily_exact_dates_services_fragments_and_no_numeric_activation():
    rows = selected_presentation()
    daily = design.build_daily_year_files(rows, transport_mode='presentation')
    assert set(daily) == {2026, 2027, 2028}
    for year, date in [(2026, '2026-04-11'), (2027, '2027-05-01'), (2028, '2028-04-15')]:
        assert set(daily[year]) == {date}
        actual = daily[year][date]
        assert [(r['service_section'], r['identity_key']) for r in actual] == [(s, i) for s, _, i in CASES]
        for row in actual:
            assert row['slot'] == 'Psalm' and row['slot_type'] == 'psalm'
            assert row['canonical_mt_ref'] == row['canonical_lxx_ref'] == ''
            assert row['spans_json'] == '[]'
            assert row['current_status'] == 'pending_psalm_equivalence_unresolved'
            q = json.loads(row['provenance'])
            assert row['source_order'] == int(q['source_order'])
            assert row['source_token_order'] == int(q['source_token_order'])
            disclosure, = json.loads(row['source_disclosure'])
            assert disclosure['bright_composite_source'] == [q]
    from passage_normalization import parse_passage
    assert [(p.verse_start, p.verse_end) for p in parse_passage(CASES[0][1]).parts] == [(23, 23), (26, 26)]


def test_all_four_generic_numeric_keys_remain_inactive_historical_members():
    raw = raw_rows()
    held = [r for r in raw if r.get('superseded_reason') == bright.HOLD]
    assert len(held) == 4
    rows, _ = design.build_reverse_presentation(held)
    assert {design.occasion_index_key(r) for r in rows} == HISTORICAL_KEYS
    assert all(r['current_status'] == 'historical_candidate_removed' and bright.HOLD in r['status_note'] for r in rows)
    assert all(bright.HOLD in r['removed_marker'] for r in rows)
    assert all(not design.is_current_presentation(r) for r in rows)
    assert design.build_daily_year_files(csv_transport(rows), transport_mode='presentation') == {}
    # Whole-corpus membership includes history, not only active rows.
    def oracle(result):
        assert len(result) == 8
        assert {design.occasion_index_key(r) for r in result} == HISTORICAL_KEYS | HELD_KEYS
    with patch.object(design, 'verify_reverse_index_contract', side_effect=oracle):
        result, disagreements = design.build_reverse_lectionary_index(csv_transport(rows) + selected_presentation(), transport_mode='presentation')
    assert len(result) == 8 and not disagreements


@pytest.mark.parametrize('field,value', [
    ('source_family','ordinary_date_resolved'), ('source_kind','pascha_day_hour'),
    ('service_section','3rd Hour'), ('gregorian_date','2026-04-12'),
    ('source_order',True), ('source_token_order',2), ('passage','Ps 44:23-26'),
    ('provenance','{}'), ('book','Ps')])
def test_real_creation_rejects_raw_drift(field, value):
    row = bright.load_bright_composite_rows()[0]
    with pytest.raises(ValueError):
        design.build_reverse_presentation([dict(row, **{field:value})])


@pytest.mark.parametrize('boundary', ['daily','reverse'])
@pytest.mark.parametrize('field,value', [
    ('source_family','ordinary_date_resolved'), ('source_kind','pascha_day_hour'),
    ('service_section','3rd Hour'), ('service_hour','Sixth Hour'),
    ('gregorian_date','2026-04-11'), ('occasion','Good Friday'), ('slot','Gospel'),
    ('source_order',True), ('source_token_order',1), ('current_status',True),
    ('current_status','current_confirmed_coptic_reader'), ('canonical_mt_ref','Ps 44:23-26'),
    ('canonical_lxx_ref','Ps 43:23-26'), ('spans_json','[{"book":"Ps"}]'),
    ('spans_json',[]), ('source_locator','forged'), ('provenance','{}'),
    ('identity_key','rid_fake'), ('source_ref','Psalm 44:23-26')])
def test_actual_csv_projection_boundaries_reject_drift(boundary, field, value):
    rows = selected_presentation()
    rows[0][field] = value
    caller = design.build_daily_year_files if boundary == 'daily' else design.build_reverse_lectionary_index
    with pytest.raises(ValueError):
        caller(rows, transport_mode='presentation')


@pytest.mark.parametrize('boundary', ['creator','daily','reverse'])
def test_actual_callers_freshly_authenticate_and_fail_closed(boundary):
    rows = selected_presentation()
    raw = bright.load_bright_composite_rows()
    with patch.object(bright, 'authenticate_bright_composite_evidence', side_effect=ValueError('retained evidence unavailable')):
        with pytest.raises(ValueError, match='retained evidence unavailable'):
            if boundary == 'creator':
                design.build_reverse_presentation(raw)
            elif boundary == 'daily':
                design.build_daily_year_files(rows, transport_mode='presentation')
            else:
                design.build_reverse_lectionary_index(rows, transport_mode='presentation')


@pytest.mark.parametrize('boundary', ['daily','reverse'])
def test_boundary_uses_identity_authenticator_not_only_rebuild(boundary):
    rows = selected_presentation()
    caller = design.build_daily_year_files if boundary == 'daily' else design.build_reverse_lectionary_index
    with patch.object(bright, 'authenticate_bright_composite_identity', side_effect=ValueError('identity authentication failed')):
        with pytest.raises(ValueError, match='identity authentication failed'):
            caller(rows, transport_mode='presentation')


def test_schema_declares_source_only_confidence(tmp_path):
    with patch.object(design, 'OUT', tmp_path):
        schema = design.write_schema()
    assert 'source_selection_only_canonical_hold' in schema['controlled_vocabularies']['canonicalization_confidence']
    assert bright.CONVENTION in schema['controlled_vocabularies']['source_convention']
    assert 'source_selection_only_canonical_hold' in schema['controlled_vocabularies']['source_authority_tier']


@pytest.mark.parametrize('boundary', ['daily', 'reverse'])
@pytest.mark.parametrize('field,value', [('document_hash', '0'*64), ('body_hash', '0'*64),
    ('printed_ref', 'Psalm 44:23-26'), ('fresh_app_verification', True),
    ('canonical_numeric_activation_approved', 'false')])
def test_provenance_hash_printed_selection_and_approval_types(boundary, field, value):
    rows = selected_presentation()
    q = json.loads(rows[0]['provenance'])
    if field == 'document_hash':
        q['document']['sha256'] = value
    elif field == 'body_hash':
        q['document']['body_sha256'] = value
    else:
        q[field] = value
    rows[0]['provenance'] = json.dumps(q)
    caller = design.build_daily_year_files if boundary == 'daily' else design.build_reverse_lectionary_index
    with pytest.raises(ValueError):
        caller(rows, transport_mode='presentation')


def test_global_corpus_gate_is_not_disabled():
    with pytest.raises(AssertionError, match='intended source ledger'):
        design.build_reverse_lectionary_index(selected_presentation(), transport_mode='presentation')
