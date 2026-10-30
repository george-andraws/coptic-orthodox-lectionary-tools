"""Independent review-lane controls: pinned old witnesses and literal selections."""
import copy
import datetime as dt
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts import compare_external_sources as compare

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads(compare.CORRECTIONS.read_text())


@pytest.fixture(scope='module')
def corpus():
    source = compare.load_csv(compare.SOURCE_INDEX)
    daily = {year: json.loads((compare.PACKAGE_DIR / 'data/daily' / f'lectionary-{year}.json').read_text())
             for year in (2026, 2027, 2028)}
    # These literal H/K/R count, sequence and corruption oracles belong to the
    # authenticated 1.3.7 contract, not a successor with new holds/display labels.
    # Keep every historical assertion and test L1-L10 in its own successor suite.
    import mark_followup_repairs as followup
    for year, days in followup.baseline()['daily'].items():
        daily[int(year)].update(copy.deepcopy(days))
    return source, daily


def probe(source, daily, year=2026):
    src, pkg, skipped, dispositions, issues = compare.contextual_counters(source, daily, year, POLICY)
    return compare.counter_delta_rows(year, src, pkg) + issues, dispositions


def subset(corpus, date):
    source, years = corpus
    return copy.deepcopy([r for r in source if r['gregorian_date'] == date]), {date: copy.deepcopy(years[int(date[:4])][date])}


@pytest.mark.parametrize('date', ['2026-02-02', '2026-04-05', '2026-04-07', '2026-04-08'])
def test_current_review_controls_pass(corpus, date):
    source, daily = subset(corpus, date)
    assert probe(source, daily)[0] == []


def test_reviewed_overlay_has_exact_retirements_and_new_selections(corpus):
    source, daily = subset(corpus, '2026-04-07')
    issues, dispositions = probe(source, daily)
    assert issues == []
    assert len(source) == 38
    assert len(daily['2026-04-07']) == 28
    assert sum(r['slot'].startswith('OT') for r in daily['2026-04-07']) == 16
    retired = [r for r in dispositions if r['disposition'] == 'authenticated_holy_week_cached_retirement']
    added = [r for r in dispositions if r['disposition'] == 'source_qualified_holy_week_review_selection']
    assert len(retired) == 15
    assert len(added) == 5
    assert {r['normalized_ref'] for r in added} == {'Ezek 22:17-22', 'Ezek 22:23-29', 'Matt 22:1-14', 'Jer 16:9-13', 'Matt 25:1-13'}
    assert all(r['evidence_sha256'] for r in retired + added)


@pytest.mark.parametrize('year', [2026, 2027, 2028])
def test_all_holy_week_review_dates_have_eleven_exact_additions(corpus, year):
    from calendar_resolution import julian_pascha_gregorian
    source, years = corpus
    dates = [(julian_pascha_gregorian(year) + dt.timedelta(days=offset)).isoformat() for offset in range(-7, -1)]
    daily = {date: copy.deepcopy(years[year][date]) for date in dates}
    selected = [r for rows in daily.values() for r in rows if r['source_family'] == 'coptic_reader_qualified_holy_week_review']
    assert len(selected) == 11
    assert {r['canonical_mt_ref'] for r in selected} == {
        'Zeph 1:14-2:2', 'Lk 9:18-22', 'Mic 3:1-4', 'Matt 17:19-23',
        'Ezek 22:17-22', 'Ezek 22:23-29', 'Matt 22:1-14', 'Jer 16:9-13',
        'Matt 25:1-13', 'Ezek 43:5-11', 'Jn 19:13-27'}
    issues, dispositions = probe([r for r in source if r['gregorian_date'] in dates], daily, year)
    assert issues == []
    assert sum(r['disposition'] == 'source_qualified_holy_week_review_selection' for r in dispositions) == 11


def test_review_epoch_cannot_fall_back_to_complete_predecessor(corpus):
    from scripts import review_comparison_contract as contract
    before = json.loads(contract._pinned(contract.HOLY_FIXTURE, contract.HOLY_SHA256))['daily']['2026']
    source = [r for r in corpus[0] if r['gregorian_date'] == '2026-04-07']
    current = {'2026-04-07': corpus[1][2026]['2026-04-07']}
    src, pkg, _, _, issues = compare.contextual_counters(source, current, 2026, POLICY, review_release=True)
    assert src == pkg and issues == []
    src, pkg, _, _, issues = compare.contextual_counters(
        source, {'2026-04-07': before['2026-04-07']}, 2026, POLICY, review_release=True)
    assert 'invalid_qualified_holy_week_review_complete_sequence' in {r['status'] for r in issues}


def test_review_service_reordering_is_rejected_even_after_renumbering(corpus):
    source, daily = subset(corpus, '2026-04-07')
    assert probe(source, daily)[0] == []
    rows = daily['2026-04-07']
    rows[:] = rows[-5:] + rows[:-5]
    for i, row in enumerate(rows, 1): row['reading_order'] = i
    issues, _ = probe(source, daily)
    assert 'invalid_qualified_holy_week_review_service_sequence' in {r['status'] for r in issues}


@pytest.mark.parametrize('field,value', [('pascha_service', 'good_friday'),
                                        ('pascha_civil_date', '2026-04-10'),
                                        ('pascha_offset_days', -2),
                                        ('display_occasion', 'Good Friday')])
def test_bright_saturday_context_metadata_does_not_create_a_reading_bypass(corpus, field, value):
    source, daily = subset(corpus, '2026-04-11')
    assert probe(source, daily)[0] == []
    row = next(r for r in daily['2026-04-11'] if r.get('pascha_service'))
    row[field] = value
    issues, _ = probe(source, daily)
    assert 'invalid_qualified_holy_week_review_context' in {r['status'] for r in issues}


@pytest.mark.parametrize('mutation', ['omit', 'duplicate', 'swap', 'family', 'hour', 'status', 'extra', 'spans', 'evidence'])
def test_holy_week_new_lane_rejects_for_its_own_diagnostic(corpus, mutation):
    source, daily = subset(corpus, '2026-04-07')
    assert probe(source, daily)[0] == []
    rows = daily['2026-04-07']
    positions = [i for i, r in enumerate(rows) if r['source_family'] == 'coptic_reader_qualified_holy_week_review']
    row = rows[positions[0]]
    if mutation == 'omit': rows.pop(positions[0])
    elif mutation == 'duplicate': rows.append(copy.deepcopy(row))
    elif mutation == 'swap': rows[positions[0]], rows[positions[1]] = rows[positions[1]], rows[positions[0]]
    else:
        field, value = {'family': ('source_family', 'holy_pascha_curated_day_hour'),
                        'hour': ('service_hour', 'Ninth Hour'), 'status': ('current_status', 'unreviewed_future_status'),
                        'extra': ('runtime_activation_approved', True), 'spans': ('spans_json', '[]'),
                        'evidence': ('holy_week_review_evidence', '{}')}[mutation]
        row[field] = value
    for i, r in enumerate(rows, 1): r['reading_order'] = i
    issues, _ = probe(source, daily)
    assert 'invalid_qualified_holy_week_review_complete_sequence' in {r['status'] for r in issues}


@pytest.mark.parametrize('mutation', ['reference', 'context', 'omit', 'duplicate', 'extra'])
def test_retired_cache_witness_cannot_be_changed_or_hidden(corpus, mutation):
    source, daily = subset(corpus, '2026-04-07')
    assert probe(source, daily)[0] == []
    i = next(i for i, r in enumerate(source) if r['day_title'] == 'Tuesday Eve')
    if mutation == 'omit': source.pop(i)
    elif mutation == 'duplicate': source.append(copy.deepcopy(source[i]))
    elif mutation == 'reference': source[i]['matched_ref'] = 'Jn 1:1-2'
    elif mutation == 'context': source[i]['source_occasion'] = 'Monday Eve'
    else: source[i]['unknown_approval'] = 'yes'
    issues, _ = probe(source, daily)
    assert 'invalid_holy_week_review_cached_source_table' in {r['status'] for r in issues}


@pytest.mark.parametrize('date', ['2026-02-02', '2026-04-05'])
@pytest.mark.parametrize('field', ['coptic_date_key', 'annual_sunday', 'calendar_review_status', 'display_label', 'unapproved_extra'])
def test_calendar_metadata_is_authenticated_not_arbitrarily_discarded(corpus, date, field):
    source, daily = subset(corpus, date)
    assert probe(source, daily)[0] == []
    row = next(r for r in daily[date] if r.get('source_kind') == ('jonah_fast_date_supplement' if date.endswith('02-02') else 'coptic_reader_qualified_pascha_hour'))
    row[field] = 'forged'
    issues, _ = probe(source, daily)
    assert any(r['status'].startswith('invalid_qualified_') for r in issues)


def r2_fixture(date='2026-01-01'):
    # Reconstruct from the approved full source, never from candidate daily rows
    # (the pre-rebuild candidate still contains the rejected inactive daily rows).
    import kiahk23_review_repairs as r2
    plan = r2.authenticate_plan()
    rows = [dict(r2._new_row(a, plan), gregorian_date=date,
                 weekday=dt.date.fromisoformat(date).strftime('%A'),
                 reading_order=i, display_label='Kiahk 23',
                 service_order={'Vespers': 1, 'Matins': 2, 'Liturgy': 99}[a['service_section']])
            for i, a in enumerate(plan['appointments'], 1)]
    source = [r for r in compare.load_csv(compare.SOURCE_INDEX) if r['gregorian_date'] == date]
    return source, {date: rows}


@pytest.mark.parametrize('date', ['2026-01-01', '2027-01-01'])
def test_kiahk_full_weekday_source_replacement_has_nine_current_only_and_no_numeric_psalms(date):
    source, daily = r2_fixture(date)
    issues, dispositions = probe(source, daily, int(date[:4]))
    assert issues == []
    assert len(daily[date]) == 9
    psalms = [r for r in daily[date] if r['slot'] == 'Psalm']
    assert len(psalms) == 3
    assert all(r['canonical_mt_ref'] == r['canonical_lxx_ref'] == '' and r['spans_json'] == '[]' for r in psalms)
    assert len([r for r in dispositions if r['disposition'] == 'authenticated_kiahk23_cached_retirement']) == 11


@pytest.mark.parametrize('mutation', ['omit', 'duplicate', 'swap', 'psalm_coordinates', 'inactive', 'extra', 'old_daily', 'source_context', 'source_missing'])
def test_kiahk_full_table_failure_categories(mutation):
    source, daily = r2_fixture()
    assert probe(source, daily)[0] == []
    rows = daily['2026-01-01']
    if mutation == 'omit': rows.pop()
    elif mutation == 'duplicate': rows.append(copy.deepcopy(rows[0]))
    elif mutation == 'swap': rows[0], rows[1] = rows[1], rows[0]
    elif mutation == 'psalm_coordinates': rows[0]['canonical_mt_ref'] = 'Ps 1:1'
    elif mutation == 'inactive': rows[0].update(active=False, status='removed')
    elif mutation == 'extra': rows[0]['runtime_activation_approved'] = True
    elif mutation == 'old_daily':
        import kiahk23_review_repairs as r2
        r2.authenticate_plan()
        old = json.loads(r2._read(r2.SOURCE + '/repair-approval/legacy-published-1.3.6.json'))['reverse_rows'][0]
        rows.insert(0, dict(r2._retire(old), reading_order=1))
    elif mutation == 'source_context': source[0]['service_section'] = 'Wrong service'
    else: source.pop()
    issues, _ = probe(source, daily)
    expected = ('invalid_kiahk23_review_cached_source_table' if mutation.startswith('source_')
                else 'invalid_qualified_kiahk23_review_complete_sequence')
    assert expected in {r['status'] for r in issues}
    if mutation == 'old_daily': assert 'removed_state_in_daily' in {r['status'] for r in issues}


@pytest.mark.parametrize('date', ['2026-01-02', '2028-01-02'])
def test_kiahk_wrong_day_or_sunday_cannot_claim_source_disposition(date):
    source, daily = r2_fixture(date)
    issues, dispositions = probe(source, daily, int(date[:4]))
    assert 'invalid_qualified_kiahk23_review_context' in {r['status'] for r in issues}
    assert not any(r['disposition'] == 'authenticated_kiahk23_cached_retirement' for r in dispositions)


@pytest.mark.parametrize('module,method', [('holy_week_review_repairs', 'authenticate_document'), ('kiahk23_review_repairs', 'authenticate_plan')])
def test_review_source_failure_is_not_hidden_by_cached_expected_tables(corpus, module, method):
    source, daily = subset(corpus, '2026-04-07') if module.startswith('holy') else r2_fixture()
    assert probe(source, daily)[0] == []
    with patch(module + '.' + method, side_effect=ValueError('review source authentication failed')):
        with pytest.raises(ValueError, match='review source authentication failed'):
            probe(source, daily)
