"""Membership alone must not activate reviewed Bright holds or erase witnesses."""
import copy
import json
from unittest.mock import patch

import pytest
import build_design_deliverables as design
import bright_saturday_composite_supplements as bright
from test_bright_composite_projection_integration import raw_rows, HELD_KEYS, HISTORICAL_KEYS
from test_covenant_thursday_coexistence import baseline, literal_keys, projected


@pytest.fixture(scope='module')
def qualified_subset():
    covenant = projected()
    old = [r for r in baseline() if design.occasion_index_key(r) in literal_keys()]
    selected = [r for r in raw_rows() if r['source_kind'] == bright.SOURCE_KIND or r.get('superseded_reason') == bright.HOLD]
    bright_rows, _ = design.build_reverse_presentation(selected)
    keys = literal_keys() | HELD_KEYS | HISTORICAL_KEYS
    def subset(rows):
        assert len(rows) == len(keys) == 24
        assert {design.occasion_index_key(r) for r in rows} == keys
    with patch.object(design, 'verify_reverse_index_contract', side_effect=subset):
        result, _ = design.build_reverse_lectionary_index(covenant + old + bright_rows, transport_mode='presentation')
    contract = {'mandatory_qualifications': {
        'bright_legacy_inactive_keys': [list(k) for k in sorted(HISTORICAL_KEYS)],
        'bright_source_only_keys': [list(k) for k in sorted(HELD_KEYS)],
        'covenant_source_keys': [list(k) for k in sorted(literal_keys())],
        'covenant_old_witnesses': [{'key': list(design.occasion_index_key(r)), 'current_status': r['current_status']} for r in old],
    }}
    return result, contract


def gate(rows, contract):
    fn = getattr(design, 'verify_source_plan_qualifications', None)
    assert fn is not None, 'Source-plan qualification gate is not implemented'
    fn(rows, contract)


def test_qualified_current_history_and_source_only_states_are_accepted(qualified_subset):
    gate(*qualified_subset)


@pytest.mark.parametrize('kind,field,value', [
    ('legacy', 'current_status', 'current_public_or_local_reference'),
    ('legacy', 'removed_marker', ''),
    ('legacy', 'superseded_by_ref', ''),
    ('held', 'current_status', 'current_confirmed_coptic_reader'),
    ('held', 'canonical_mt_ref', 'Ps 44:23-26'),
    ('held', 'canonical_lxx_ref', 'Ps 43:23-26'),
    ('held', 'spans_json', '[{"book":"Ps"}]'),
    ('held', 'source_kind', 'bright_saturday_service_order'),
    ('held', 'provenance', '{}'),
    ('held', 'source_disclosure', '[]'),
    ('covenant', 'current_status', 'current_confirmed_coptic_reader'),
    ('covenant', 'source_disclosure', '[]'),
])
def test_same_membership_cannot_bypass_source_qualifications(qualified_subset, kind, field, value):
    original, contract = qualified_subset
    rows = copy.deepcopy(original)
    keys = {'legacy': HISTORICAL_KEYS, 'held': HELD_KEYS, 'covenant': literal_keys()}[kind]
    target = next(r for r in rows if design.occasion_index_key(r) in keys)
    target[field] = value
    assert {design.occasion_index_key(r) for r in rows} == {design.occasion_index_key(r) for r in original}
    with pytest.raises(AssertionError, match='Source-plan qualification'):
        gate(rows, contract)


def test_declared_main_csv_header_preserves_supersession_transport(qualified_subset, tmp_path):
    import ast
    import inspect
    tree = ast.parse(inspect.getsource(design.main))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == 'presentation_fields' for target in node.targets))
    fields = ast.literal_eval(assignment.value)
    with patch.object(design, 'OUT', tmp_path):
        schema = design.write_schema()
    assert fields == schema['tables']['reverse_lectionary_presentation']
    raw = next(r for r in raw_rows() if r.get('superseded_reason') == bright.HOLD)
    presentation, _ = design.build_reverse_presentation([raw])
    path = tmp_path / 'reverse_lectionary_presentation.csv'
    design.write_csv(path, presentation, fields)
    transported, = design.read_csv(path)
    assert transported.get('superseded_by_ref') == raw['superseded_by_ref']
    assert transported.get('superseded_reason') == bright.HOLD
    import verify_design_deliverables as independent
    assert independent.is_authenticated_bright_hold(transported)


def test_legacy_supersession_targets_survive_reverse_output(qualified_subset):
    rows, _ = qualified_subset
    by_key = {design.occasion_index_key(row): row for row in rows}
    for raw in raw_rows():
        if raw.get('superseded_reason') != bright.HOLD:
            continue
        p, _ = design.build_reverse_presentation([raw])
        row = by_key[design.occasion_index_key(p[0])]
        assert p[0].get('superseded_by_ref') == raw['superseded_by_ref']
        assert row.get('superseded_by_ref') == raw['superseded_by_ref']
        assert row.get('superseded_reason') == bright.HOLD


def test_covenant_old_witness_cannot_be_relabelled_current(qualified_subset):
    original, contract = qualified_subset
    rows = copy.deepcopy(original)
    expected = next(w for w in contract['mandatory_qualifications']['covenant_old_witnesses'] if w['current_status'] == 'historical_witness')
    target = next(r for r in rows if design.occasion_index_key(r) == tuple(expected['key']))
    disclosures = json.loads(target['source_disclosure'])
    changed = 0
    for source in disclosures:
        for witness in source.get('source_witnesses', []):
            if witness['current_status'] == 'historical_witness':
                witness['current_status'] = 'current_public_or_local_reference'
                changed += 1
    assert changed
    target['source_disclosure'] = json.dumps(disclosures)
    with pytest.raises(AssertionError, match='Source-plan qualification'):
        gate(rows, contract)


def test_old_runtime_nonapproval_cannot_be_flipped(qualified_subset):
    original, contract = qualified_subset
    rows = copy.deepcopy(original)
    target = next(r for r in rows if design.occasion_index_key(r) in literal_keys())
    disclosures = json.loads(target['source_disclosure'])
    item = next(s for s in disclosures if s.get('covenant_thursday_source'))
    item['covenant_thursday_source'][0]['runtime_activation_approved'] = True
    target['source_disclosure'] = json.dumps(disclosures)
    with pytest.raises(AssertionError, match='Source-plan qualification'):
        gate(rows, contract)
