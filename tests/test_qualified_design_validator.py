"""Independent validator regressions: retained evidence is not activation."""
import copy
import json
from collections import defaultdict

import pytest
import verify_design_deliverables as v


@pytest.fixture(scope='module')
def groups():
    result = defaultdict(list)
    for row in v.read_csv(v.OUT / 'reverse_lectionary_presentation.csv'):
        result[v.occasion_index_key(row)].append(row)
    return result


@pytest.mark.parametrize('kind,field', [
    ('bright_saturday_qualified_composite', 'bright_composite_source'),
    ('coptic_reader_qualified_pascha_hour', 'covenant_thursday_source'),
])
def test_disclosure_derived_from_authenticated_source(groups, kind, field):
    rows = next(rs for rs in groups.values() if any(r['source_kind'] == kind for r in rs))
    disclosure, _ = v.expected_source_disclosure(rows)
    item = next(d for d in disclosure if d['source_kind'] == kind)
    assert item[field]
    if 'covenant' in field:
        assert item[field][0]['runtime_activation_approved'] is False
        assert all('source_witnesses' in d for d in disclosure)


@pytest.mark.parametrize('kind', ['bright_saturday_qualified_composite', 'coptic_reader_qualified_pascha_hour'])
@pytest.mark.parametrize('mutation', ['family', 'context', 'missing', 'tampered', 'approval'])
def test_forged_qualification_fails_closed(groups, kind, mutation):
    row = copy.deepcopy(next(r for rs in groups.values() for r in rs if r['source_kind'] == kind))
    if mutation == 'family':
        row['source_family'] = 'forged'
    elif mutation == 'context':
        row['service_section'] = 'Vespers'
    elif mutation == 'missing':
        row['provenance'] = ''
    else:
        q = json.loads(row['provenance'])
        q['runtime_activation_approved' if mutation == 'approval' else 'printed_ref'] = True if mutation == 'approval' else 'forged'
        row['provenance'] = json.dumps(q)
    with pytest.raises((ValueError, AssertionError)):
        v.expected_source_disclosure([row])


def test_exact_contract_status_groups(groups):
    known = v.qualified_status_disagreement_keys(groups, 5)
    assert len(known) == len(v.source_plan_qualifications()['covenant_old_witnesses'])
    for count in (0, 4, 6):
        with pytest.raises(AssertionError):
            v.qualified_status_disagreement_keys(groups, count)


@pytest.mark.parametrize('mutation', ['old_status', 'new_status', 'marker', 'extra', 'missing'])
def test_status_compatibility_is_not_a_five_group_allowance(groups, mutation):
    altered = copy.deepcopy(groups)
    key = tuple(v.source_plan_qualifications()['covenant_old_witnesses'][0]['key'])
    rows = altered[key]
    old = next(r for r in rows if r['source_kind'] == 'pascha_source_text')
    new = next(r for r in rows if r['source_kind'] == 'coptic_reader_qualified_pascha_hour')
    if mutation == 'old_status':
        old['current_status'] = new['current_status']
    elif mutation == 'new_status':
        new['current_status'] = 'historical_witness'
    elif mutation == 'marker':
        old['removed_marker'] = 'removed'
    elif mutation == 'missing':
        rows.remove(old)
    else:
        extra = copy.deepcopy(rows)
        for r in extra:
            r['occasion'] = 'unrelated'
        altered[v.occasion_index_key(extra[0])] = extra
    with pytest.raises((ValueError, AssertionError)):
        v.qualified_status_disagreement_keys(altered, 5)


def test_bright_hold_requires_exact_authenticated_context(groups):
    rows = [r for rs in groups.values() for r in rs if r['removed_marker'] == 'superseded_bright_composite_edition_context_hold']
    assert len(rows) == 4
    import bright_saturday_composite_supplements as bright
    contract = bright.authenticate_bright_composite_evidence()
    for original in rows:
        record = next(r for r in contract['records'] if r['source_order'] == original['source_order']
                      and r['source_token_order'] == original['source_token_order'])
        # Build the reviewed transport fixture from source, not candidate index.
        # The full verifier separately rejects an older generated CSV lacking it.
        row = dict(original, superseded_by_ref=record['source_selection_ref'], superseded_reason=bright.HOLD)
        assert v.is_authenticated_bright_hold(row)
        for field, value in [('current_status', 'current_public_or_local_reference'), ('source_family', 'forged'), ('service_section', 'Vespers'), ('provenance', 'forged'), ('superseded_by_ref', 'forged'), ('superseded_reason', '')]:
            altered = dict(row, **{field: value})
            with pytest.raises((ValueError, AssertionError)):
                v.is_authenticated_bright_hold(altered)


def test_actual_daily_transport_matches_fresh_presentation():
    v.verify_daily_rows(v.read_csv(v.OUT / 'reverse_lectionary_presentation.csv'),
                        json.loads((v.OUT / 'lectionary_schema.json').read_text()),
                        json.loads((v.OUT / 'BUILD_DESIGN_SUMMARY.json').read_text()))


def test_source_label_order_requires_authenticated_psalmody(groups):
    rows = [r for rs in groups.values() for r in rs if r['source_kind'] == 'psalmody_source_supplement']
    assert len(rows) == 12
    for row in rows:
        assert v.authenticated_psalmody_order(row) >= 1
        with pytest.raises((ValueError, AssertionError)):
            v.authenticated_psalmody_order(dict(row, service_section='forged'))


def test_old_covenant_provenance_must_not_be_rewritten(groups):
    altered = copy.deepcopy(groups)
    key = tuple(v.source_plan_qualifications()['covenant_old_witnesses'][0]['key'])
    next(r for r in altered[key] if r['source_kind'] == 'pascha_source_text')['provenance'] = 'fresh Reader confirmation'
    with pytest.raises((ValueError, AssertionError)):
        v.qualified_status_disagreement_keys(altered, 5)
