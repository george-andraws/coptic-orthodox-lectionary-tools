"""R1/R4 comparison must authenticate predecessors, not repair the candidate."""
import copy
import json
from unittest.mock import patch

import pytest

from scripts import compare_external_sources as compare
from historical_review_fixture import published_1_3_7, historical_policy

POLICY = historical_policy()


@pytest.fixture(scope='module')
def corpus():
    # R4 deliberately mutates the legacy embedded _review_original_row and
    # provenance together. LK6 public transport is a different API boundary.
    frozen = published_1_3_7()
    return (compare.load_csv(compare.SOURCE_INDEX),
            {y: frozen['daily'][str(y)] for y in (2026, 2027, 2028)})


def subset(corpus, date):
    source, daily = corpus
    return (copy.deepcopy([r for r in source if r['gregorian_date'] == date]),
            {date: copy.deepcopy(daily[int(date[:4])][date])})


def probe(source, daily):
    year = int(next(iter(daily))[:4])
    src, pkg, _, audits, issues = compare.contextual_counters(
        source, daily, year, POLICY, review_release=True)
    return compare.counter_delta_rows(year, src, pkg) + issues, audits, src, pkg


@pytest.mark.parametrize('date,kind,count', [
    ('2026-04-03', 'r1', 1), ('2027-04-23', 'r1', 1),
    ('2026-04-02', 'r4', 2), ('2027-04-22', 'r4', 2), ('2028-04-06', 'r4', 2)])
def test_reviewed_resolver_appointments_compare_in_common_domain(corpus, date, kind, count):
    source, daily = subset(corpus, date)
    original = copy.deepcopy((source, daily))
    issues, audits, src, pkg = probe(source, daily)
    assert issues == []
    assert src == pkg
    retired = [a for a in audits if a['disposition'] == f'authenticated_{kind}_cached_retirement']
    selected = [a for a in audits if a['disposition'] == f'source_qualified_{kind}_review_selection']
    assert len(retired) == count and len(selected) == 1
    assert all(a['evidence_sha256'] for a in retired + selected)
    assert (source, daily) == original


def test_reader_collision_boundary_has_no_r1_disposition(corpus):
    source, daily = subset(corpus, '2028-04-07')
    issues, audits, _, _ = probe(source, daily)
    assert issues == []
    assert not any('_r1_' in a['disposition'] for a in audits)


@pytest.mark.parametrize('mutation', ['source', 'context', 'disclosure'])
def test_r1_tampering_is_rejected_for_its_own_reason(corpus, mutation):
    source, daily = subset(corpus, '2026-04-03')
    assert probe(source, daily)[0] == []
    row = next(r for r in daily['2026-04-03'] if r['service_section'] == 'Matins' and r['slot'] == 'Gospel')
    if mutation == 'source':
        next(r for r in source if r['service_section'] == 'Matins' and r['reading_type'] == 'Gospel')['source_occasion'] = 'forged'
    elif mutation == 'context':
        row['service_hour'] = 'First Hour'
    else:
        disclosure = json.loads(row['resolver_review_disclosure'])
        disclosure['original']['source_locator'] = 'forged'
        row['resolver_review_disclosure'] = json.dumps(disclosure, sort_keys=True)
    issues, audits, _, _ = probe(source, daily)
    expected = 'invalid_r1_review_cached_source_table' if mutation == 'source' else 'invalid_qualified_r1_review_appointment'
    assert expected in {r['status'] for r in issues}
    assert not any(a['disposition'] == 'authenticated_r1_cached_retirement' for a in audits)


@pytest.mark.parametrize('mutation', ['missing', 'duplicate', 'reordered', 'rebound', 'coordinates'])
def test_r4_complete_ordered_original_fragments_are_authenticated(corpus, mutation):
    source, daily = subset(corpus, '2026-04-02')
    assert probe(source, daily)[0] == []
    row = next(r for r in daily['2026-04-02'] if r['slot'] == 'Acts of the Apostles')
    fragments = json.loads(row['composite_fragments_json'])
    if mutation == 'missing': fragments.pop()
    elif mutation == 'duplicate': fragments.append(copy.deepcopy(fragments[0]))
    elif mutation == 'reordered': fragments.reverse()
    elif mutation == 'rebound': fragments[1]['_review_original_row']['source_row_id'] = fragments[0]['source_row_id']
    else:
        spans = json.loads(fragments[1]['spans_json'])
        spans[0]['verse_end'] = 5
        fragments[1]['spans_json'] = json.dumps(spans, sort_keys=True)
    # Rebind the companion disclosure too: agreement is not authentication.
    row['composite_fragments_json'] = json.dumps(fragments, sort_keys=True)
    row['provenance'] = 'R4 composite_fragments=' + row['composite_fragments_json']
    issues, audits, _, _ = probe(source, daily)
    assert 'invalid_qualified_r4_review_appointment' in {r['status'] for r in issues}
    assert not any(a['disposition'] == 'authenticated_r4_cached_retirement' for a in audits)


@pytest.mark.parametrize('mutation', ['missing', 'duplicate', 'reordered', 'rebound', 'coordinates'])
def test_r4_cached_fragments_must_be_complete_literal_and_ordered(corpus, mutation):
    source, daily = subset(corpus, '2027-04-22')
    assert probe(source, daily)[0] == []
    positions = [i for i, r in enumerate(source) if r['reading_type'] == 'Acts of the Apostles']
    first, second = positions
    if mutation == 'missing': source.pop(second)
    elif mutation == 'duplicate': source.insert(second, copy.deepcopy(source[first]))
    elif mutation == 'reordered': source[first], source[second] = source[second], source[first]
    elif mutation == 'rebound': source[second]['url'] = source[first]['url'] + '&forged=1'
    else: source[second]['matched_ref'] = 'Acts 26:1-5'
    issues, audits, _, _ = probe(source, daily)
    assert 'invalid_r4_review_cached_source_table' in {r['status'] for r in issues}
    assert not any(a['disposition'] == 'authenticated_r4_cached_retirement' for a in audits)


@pytest.mark.parametrize('date,kind', [('2026-04-03', 'r1'), ('2026-04-02', 'r4')])
def test_review_epoch_cannot_hide_behind_unmarked_published_predecessor(corpus, date, kind):
    from scripts import review_comparison_contract as contract
    source, _ = subset(corpus, date)
    old = json.loads(contract._pinned(contract.RESOLVER_FIXTURE, contract.RESOLVER_SHA256))['daily'][date]
    issues, audits, _, _ = probe(source, {date: old})
    assert 'invalid_qualified_' + kind + '_review_appointment' in {r['status'] for r in issues}
    assert not any(a['disposition'] == 'authenticated_' + kind + '_cached_retirement' for a in audits)
    # The historical contract is still usable when explicitly not upgraded.
    src, pkg, _, _, historical_issues = compare.contextual_counters(source, {date: old}, 2026, POLICY)
    assert src == pkg and historical_issues == []


def test_resolver_retained_source_failure_reaches_comparison(corpus):
    source, daily = subset(corpus, '2026-04-03')
    assert probe(source, daily)[0] == []
    with patch('resolver_review_repairs._authenticate_last_friday', side_effect=ValueError('retained source drift')):
        with pytest.raises(ValueError, match='retained source drift'):
            probe(source, daily)
