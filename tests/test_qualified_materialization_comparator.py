"""Current source-derived comparator regressions; never refresh a package oracle."""
import copy
import csv
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from scripts import compare_external_sources as compare
from historical_review_fixture import published_1_3_7, historical_policy

ROOT = Path(__file__).resolve().parents[1]
DATES = ('2026-02-02', '2026-02-03', '2026-04-05', '2026-04-09', '2026-04-11')


@pytest.fixture(scope='module')
def corpus():
    with (ROOT / 'out/data/copticchurch_passage_index_current_2020_2035.csv').open() as f:
        source = list(csv.DictReader(f))
    # These exact group/order oracles precede the 1.3.8 hold/metadata layers.
    daily = published_1_3_7()['daily']['2026']
    return source, daily, historical_policy()


def fixture(corpus, date):
    source, daily, policy = corpus
    return copy.deepcopy([r for r in source if r['gregorian_date'] == date]), {date: copy.deepcopy(daily[date])}, policy


def valid(source, daily, policy):
    try:
        src, pkg, _, _, issues = compare.contextual_counters(source, daily, 2026, policy)
    except (AssertionError, ValueError, RuntimeError):
        return False
    return src == pkg and not issues


def selected(row, date):
    if date.startswith('2026-02'):
        return row.get('source_family') == 'jonah_fast_source_qualified'
    if date == '2026-04-11':
        return row.get('source_kind') == 'bright_saturday_qualified_composite'
    return row.get('source_kind') == 'coptic_reader_qualified_pascha_hour'


@pytest.mark.parametrize('date', DATES)
def test_complete_actual_source_and_emitted_groups_pass(corpus, date):
    source, daily, policy = fixture(corpus, date)
    src, pkg, _, dispositions, issues = compare.contextual_counters(source, daily, 2026, policy)
    assert issues == []
    assert src == pkg  # Complete keys + multiplicities, not totals.
    expected = {'2026-02-02': 8, '2026-02-03': 9, '2026-04-05': 1, '2026-04-09': 16, '2026-04-11': 4}
    assert sum(selected(r, date) for r in daily[date]) == expected[date]
    if date == '2026-04-11':
        assert all(not r['canonical_mt_ref'] and not r['canonical_lxx_ref'] and r['spans_json'] == '[]'
                   for r in daily[date] if selected(r, date))
    if date == '2026-04-09':
        rows = [r for r in daily[date] if selected(r, date)]
        assert {r['service_section'] for r in rows} == {'Liturgy', 'Liturgy of Blessing of the Water'}
        assert len({(r['service_section'], r['source_row_id']) for r in rows}) == 14


@pytest.mark.parametrize('date', DATES)
@pytest.mark.parametrize('mutation', ['omit', 'duplicate', 'renumbered_swap', 'family', 'kind', 'occasion',
                                     'service_section', 'service_hour', 'slot', 'endpoint', 'disclosure',
                                     'body_hash', 'activation', 'lifecycle', 'coordinates'])
def test_qualified_materialization_mutations_fail_closed(corpus, date, mutation):
    source, daily, policy = fixture(corpus, date)
    rows = daily[date]
    positions = [i for i, r in enumerate(rows) if selected(r, date)]
    row = rows[positions[0]]
    if mutation == 'omit': rows.pop(positions[0])
    elif mutation == 'duplicate': rows.insert(positions[0], copy.deepcopy(row))
    elif mutation == 'renumbered_swap':
        other = positions[1] if len(positions) > 1 else positions[0] + 1
        rows[positions[0]], rows[other] = rows[other], rows[positions[0]]
    elif mutation in ('family', 'kind'): row['source_' + mutation] = 'ordinary_date_resolved'
    elif mutation in ('occasion', 'service_section', 'service_hour', 'slot'): row[mutation] = 'Wrong context'
    elif mutation == 'endpoint': row['display_ref'] = 'Jonah 1:1-16'
    elif mutation == 'disclosure': row['source_disclosure'] = '[]'
    elif mutation == 'body_hash': row['source_disclosure'] = row['source_disclosure'].replace('sha256', 'sha255')
    elif mutation == 'activation': row['runtime_activation_approved'] = True
    elif mutation == 'lifecycle': row['current_status'] = 'historical_witness'
    elif mutation == 'coordinates': row['canonical_mt_ref'] = 'Ps 44:23-26'
    for i, r in enumerate(rows, 1): r['reading_order'] = i
    assert not valid(source, daily, policy), (date, mutation)


@pytest.mark.parametrize('date', DATES)
def test_matching_wrong_outer_date_cannot_authorize_disposition(corpus, date):
    source, daily, policy = fixture(corpus, date)
    wrong = '2026-06-01'
    for row in source: row['gregorian_date'] = wrong
    assert not valid(source, {wrong: daily[date]}, policy)


@pytest.mark.parametrize('mutation', ['omit_both', 'source_family', 'source_kind', 'source_order', 'matched_ref', 'provenance'])
def test_jonah_source_authentication_not_just_package_parity(corpus, mutation):
    source, daily, policy = fixture(corpus, '2026-02-02')
    if mutation == 'omit_both':
        source.pop(0); daily['2026-02-02'].pop(0)
    else:
        source[0][mutation] = 'forged'
    assert not valid(source, daily, policy)


@pytest.mark.parametrize('module,method', [('jonah_fast_source_supplements', 'load_jonah_contract'),
                                         ('covenant_thursday_source_supplements', 'load_covenant_thursday_contract'),
                                         ('bright_saturday_composite_supplements', 'authenticate_bright_composite_evidence'),
                                         ('pascha_resolution_evidence', 'authenticate_pascha_evidence')])
def test_retained_evidence_failure_reaches_comparison(corpus, module, method):
    date = {'jonah_fast_source_supplements': '2026-02-02', 'covenant_thursday_source_supplements': '2026-04-09',
            'bright_saturday_composite_supplements': '2026-04-11', 'pascha_resolution_evidence': '2026-04-05'}[module]
    source, daily, policy = fixture(corpus, date)
    with patch(module + '.' + method, side_effect=ValueError('retained body/hash drift')):
        assert not valid(source, daily, policy)
