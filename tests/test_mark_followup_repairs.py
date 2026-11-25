"""L1-L10 source-owned controls and corruption probes, not corpus substitutions."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

import pytest

import mark_followup_repairs as m
import revelation_release_repairs as revelation
import pk6_release_repairs as pk6
from scripts.review_release_contract import followup_daily_view, review_inactive_qualified

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_VERSION = '1.3.13'


@pytest.fixture(scope='module')
def candidate():
    package = ROOT / 'packages/lectionary-data'
    assert json.loads((package / 'package.json').read_text())['version'] == CANDIDATE_VERSION
    assert json.loads((package / 'meta.json').read_text())['version'] == CANDIDATE_VERSION
    return {year: json.loads((package / 'data/daily' / f'lectionary-{year}.json').read_text())
            for year in (2026, 2027, 2028)}


@pytest.fixture(scope='module')
def frozen():
    return copy.deepcopy(m.baseline())


def test_complete_predecessor_projection_preserves_sources_and_is_idempotent(frozen):
    before = frozen['reverse_rows']
    after = m.repair_rows(before)
    assert len(after) == len(before) + 4
    assert m.repair_rows(after) == after
    representatives = [r for r in after if not (m.rule(r) == 'L3' and r.get('mark_followup_evidence'))]
    assert len(representatives) == len(before)
    allowed = {'display_label', 'current_status', 'active', 'mark_followup_note', 'mark_followup_evidence', 'evidence_status'}
    counts = {}
    for old, new in zip(before, representatives):
        for field in set(old) | set(new):
            if old.get(field) != new.get(field):
                assert field in allowed, field
        if m.rule(old):
            counts[m.rule(old)] = counts.get(m.rule(old), 0) + 1
            assert m.qualify_emitted(new)
        assert new.get('source_title') == old.get('source_title')
        assert new.get('source_locator') == old.get('source_locator')
        assert new.get('calendar_keys') == old.get('calendar_keys')
        assert new.get('spans_json') == old.get('spans_json')
    assert counts == {'L1': 1, 'L2': 6, 'L3': 4, 'L6': 2, 'L7': 6, 'L9': 3}


@pytest.mark.parametrize('issue', ['L1', 'L2', 'L3', 'L9'])
@pytest.mark.parametrize('field,value', [
    ('active', True), ('active', 0), ('current_status', 'current_confirmed_coptic_reader'),
    ('canonical_mt_ref', 'Mark 14:3-9'), ('spans_json', '[]'),
    ('source_locator', 'forged'), ('source_family', 'unrelated'),
    ('source_kind', 'unrelated'), ('calendar_keys', 'neighbor'),
    ('service_hour', 'Twelfth Hour'), ('identity_key', 'rid_forged'),
    ('mark_followup_evidence', '{}'), ('source_disclosure', '[]'),
])
def test_emitted_hold_rejects_mutations_and_unauthorized_promotion(frozen, issue, field, value):
    original = next(r for r in frozen['reverse_rows'] if m.rule(r) == issue)
    valid = m.repair_rows([original])[-1]
    assert m.qualify_emitted(valid)
    assert review_inactive_qualified(valid)
    corrupt = dict(valid, **{field: value})
    with pytest.raises(ValueError, match='Mark follow-up'):
        m.qualify_emitted(corrupt)


def test_compound_family_evidence_lifecycle_stripping_is_not_ordinary_reading(frozen):
    original = next(r for r in frozen['reverse_rows'] if m.rule(r) == 'L2')
    corrupt = m.repair_rows([original])[0]
    for field in ['source_family', 'source_kind', 'mark_followup_evidence', 'mark_followup_note', 'active']:
        corrupt.pop(field, None)
    corrupt['current_status'] = 'current'
    with pytest.raises(ValueError, match='source/context rebound'):
        m.qualify_emitted(corrupt)


@pytest.mark.parametrize('year', [2026, 2027, 2028])
def test_complete_daily_tables_and_comparator_positive_control(frozen, candidate, year):
    before = frozen['daily'][str(year)]
    after = m.repair_daily(before)
    assert m.repair_daily(after) == after
    from scripts.apply_review_repairs import finish_daily
    actual_scope = {date: candidate[year][date] for date in after}
    # Start with the hash-authenticated Mark predecessor, then compose ALL public
    # layers in release order. Replay alone would not prove the first projection.
    finished = finish_daily(after)
    import site_review_repairs as site
    import final_site_review_repairs as final
    expected = {}
    pk_layer = {}
    for date, rows in finished.items():
        projected = pk6.project_daily(revelation.project_rows(rows, date=date), date)
        pk_layer[date] = projected
        import holy_week_continuation as continuation
        expected[date] = continuation.project_daily(final.project_rows(site.project_rows(projected, date=date), date=date), date)
    import jeremiah_followup as jeremiah
    historical_scope = {date: jeremiah.restore_daily(rows, date) for date, rows in actual_scope.items()}
    assert historical_scope == expected, 'complete authenticated predecessor arrays, not helper-only agreement'
    assert followup_daily_view(actual_scope, version=CANDIDATE_VERSION) == after
    assert m.restore_predecessor_for_comparison(after, year) == before
    for version in (None, '1.3.9'):
        with pytest.raises(ValueError, match='Mark follow-up daily complete-table mismatch'):
            m.restore_predecessor_for_comparison(followup_daily_view(historical_scope, version=version), year)
    bad = copy.deepcopy(historical_scope)
    owned = [(date, row) for date, rows in bad.items() for row in rows
             if 'display_reference_review' in row.get('source_disclosure', '')]
    assert owned and all(date in final.SUPPLEMENT_DATES for date, _ in owned)
    for _, row in owned:
        row['source_disclosure'] = '[]'
    # Retain the original final-site mutation at its authenticated 1.3.12 boundary;
    # new 1.3.13 corruption rejection has separate complete-array regressions.
    with pytest.raises(ValueError, match='final site review complete source/context/coordinate/order mismatch'):
        followup_daily_view(bad, version='1.3.12')
    # The older PK field diagnostic remains on the pre-supplement table. The
    # 1.3.11 view above must not be the only proof, because that layer returns first.
    pk_date, pk_rows = next((date, rows) for date, rows in pk_layer.items()
                            if any('display_reference_review' in r.get('source_disclosure', '') for r in rows))
    pk_bad = copy.deepcopy(pk_rows)
    next(r for r in pk_bad if 'display_reference_review' in r.get('source_disclosure', ''))['source_disclosure'] = '[]'
    with pytest.raises(ValueError, match='PK source/context/coordinate drift: source_disclosure'):
        revelation.restore_rows(pk6.restore_daily(pk_bad, pk_date), date=pk_date)
    assert len(m.validate_eve_coverage(after, year)) == 25
    m.validate_day_hour_sets(after)
    for date, rows in after.items():
        assert [r['reading_order'] for r in rows] == list(range(1, len(rows) + 1))
        for r in rows:
            m.qualify_emitted(r, date=date)
    old_counts = sum(len(a) for a in before.values())
    new_counts = sum(len(a) for a in after.values())
    assert old_counts - new_counts == (9 if year == 2028 else 10)


@pytest.mark.parametrize('mutation', ['delete', 'add', 'order', 'reference', 'source', 'activate'])
def test_complete_comparison_oracle_rejects_corruption(frozen, mutation):
    year = 2026
    valid = m.repair_daily(frozen['daily'][str(year)])
    assert m.restore_predecessor_for_comparison(valid, year)
    bad = copy.deepcopy(valid)
    date = '2026-04-07'
    if mutation == 'delete': bad[date].pop()
    elif mutation == 'add': bad[date].append(copy.deepcopy(bad[date][0]))
    elif mutation == 'order': bad[date][0], bad[date][1] = bad[date][1], bad[date][0]
    elif mutation == 'reference': bad[date][0]['display_ref'] = 'Jn 11:12-24'
    elif mutation == 'source': bad[date][0]['source_disclosure'] = '[]'
    else:
        bad[date].append(next(copy.deepcopy(r) for r in frozen['daily']['2026'][date] if m.rule(r) == 'L2'))
    with pytest.raises(ValueError, match='complete-table mismatch'):
        m.restore_predecessor_for_comparison(bad, year)


def test_five_hour_check_requires_explicit_gaps_and_rejects_lost_current_hour(frozen):
    valid = m.repair_daily(frozen['daily']['2026'])
    coverage = m.validate_eve_coverage(valid, 2026)
    assert [(r['service'], r['hour']) for r in coverage if r['coverage'] == 'held_missing_reader'] == [
        ('eve_of_monday', 'First Hour'), ('eve_of_monday', 'Sixth Hour'), ('eve_of_monday', 'Ninth Hour'),
        ('eve_of_wednesday', 'Third Hour'), ('eve_of_wednesday', 'Ninth Hour'), ('eve_of_wednesday', 'Eleventh Hour')]
    invalid = copy.deepcopy(valid)
    invalid['2026-04-07'] = [r for r in invalid['2026-04-07'] if r.get('pascha_service') != 'eve_of_wednesday' or r.get('service_hour') != 'Sixth Hour']
    with pytest.raises(ValueError, match='five-hour coverage drift'):
        m.validate_eve_coverage(invalid, 2026)
    with patch.dict(m.EVE_GAPS, {'eve_of_wednesday': ('Third Hour', 'Ninth Hour')}, clear=False):
        with pytest.raises(ValueError, match='five-hour coverage drift'):
            m.validate_eve_coverage(valid, 2026)


def test_cross_day_complete_set_repetition_is_red_before_overlay(frozen):
    before = frozen['daily']['2026']
    with pytest.raises(ValueError, match='repeats another day'):
        m.validate_day_hour_sets(before)
    m.validate_day_hour_sets(m.repair_daily(before))


def test_l8_readings_remain_unchanged_and_wrong_family_cannot_gain_hold(frozen):
    for row in frozen['reverse_rows']:
        if row.get('coptic_date_key') == 'tout-23':
            assert m.repair_rows([row])[0] == row
    original = next(r for r in frozen['reverse_rows'] if m.rule(r) == 'L2')
    unrelated = dict(original, source_family='unrelated')
    assert m.repair_rows([unrelated]) == [unrelated]


def test_owned_row_moved_to_another_outer_date_is_rejected(frozen):
    original = next(r for r in frozen['daily']['2026']['2026-11-20'] if m.rule(r) == 'L6')
    valid = m.repair_rows([original], date='2026-11-20')[0]
    assert m.qualify_emitted(valid, date='2026-11-20')
    with pytest.raises(ValueError, match='outer date'):
        m.qualify_emitted(valid, date='2026-11-19')


def test_source_authentication_failure_reaches_actual_projection_caller(frozen):
    import scripts.apply_review_repairs as bridge
    with patch.object(m, '_authenticated', side_effect=ValueError('Mark follow-up source authentication failed')):
        with pytest.raises(ValueError, match='source authentication failed'):
            bridge.project('reverse', {'rows': []})


def test_pending_allowances_preserve_both_empty_and_numeric_source_coordinates(candidate):
    oracle = m.source_oracle()['L9']['pending_occurrence_oracle']
    # Authenticate the complete public release inverse before invoking the older
    # disclosure-hash allowance. Never refresh that historical hash from output.
    restored = {year: followup_daily_view(days, version=CANDIDATE_VERSION)
                for year, days in candidate.items()}
    counts = {}
    numeric = 0
    cleaned = 0
    for entry in oracle:
        row = {k: v for k, v in entry['selector'].items() if k != 'calendar_keys'}
        row.update({k: entry[k] for k in ('current_status', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json', 'source_locator')})
        actual = next((r for r in candidate[entry['year']][entry['date']] if r['identity_key'] == row['identity_key']), None)
        if entry['lane'].startswith('preserve_'):
            assert actual is not None
            historical = next(r for r in restored[entry['year']][entry['date']]
                              if r['identity_key'] == row['identity_key'])
            m.validate_pending_reading(historical, entry['date'])
            if actual['source_disclosure'] != historical['source_disclosure']:
                cleaned += 1
                with pytest.raises(ValueError, match='outside authenticated allowance'):
                    m.validate_pending_reading(actual, entry['date'])
            counts[entry['year']] = counts.get(entry['year'], 0) + 1
            numeric += bool(json.loads(historical['spans_json']))
            bad = dict(historical, canonical_mt_ref='Ps 1:1')
            with pytest.raises(ValueError, match='outside authenticated allowance'):
                m.validate_pending_reading(bad, entry['date'])
        else:
            assert actual is None
            with pytest.raises(ValueError, match='outside authenticated allowance'):
                m.validate_pending_reading(row, entry['date'])
    assert counts == {2026: 7, 2027: 22, 2028: 7}
    assert numeric == 18
    assert cleaned > 0
    with pytest.raises(ValueError, match='outside authenticated allowance'):
        m.validate_pending_reading({'current_status': 'pending_arbitrary'}, '2026-01-01')
