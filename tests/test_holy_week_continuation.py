"""Source-plan oracle: exact recurring proper, no guessed companion coordinates."""
import copy
import gzip
import hashlib
import json
from pathlib import Path

import pytest
from scripts.apply_review_repairs import project
import final_site_review_repairs as final
import site_review_repairs as site
import pk6_release_repairs as pk6
import revelation_release_repairs as revelation

ROOT = Path(__file__).resolve().parents[1]
DATES = ('2026-04-08', '2027-04-28', '2028-04-12')
FRIDAYS = ('2026-04-10', '2027-04-30', '2028-04-14')


def frozen():
    raw = (ROOT / 'tests/fixtures/holy-week-continuation-published-1.3.11.json.gz').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '8f0f938699ea7073beaee0ac70708e04fbbc9bb9ad875e1f66c42b85a31e8b25'
    return json.loads(gzip.decompress(raw))


def before_release(rows, date=None):
    return revelation.restore_rows(pk6.restore_reverse(site.restore_rows(final.restore_rows(rows)))) if date is None else revelation.restore_rows(pk6.restore_daily(site.restore_rows(final.restore_rows(rows, date=date), date=date), date), date=date)


def release_payload():
    # Existing membership guard requires the real complete predecessor corpus.
    # This authenticated immutable file is not overwritten by candidate builds.
    import holy_week_continuation as hw
    rows = hw.published_reverse()
    days = frozen()['daily']
    return {'rows': before_release(rows), 'daily_by_year': {
        str(y): {d: before_release(r, d) for d, r in days.items() if d.startswith(str(y))}
        for y in (2026, 2027, 2028)}}


def test_real_release_boundary_replaces_wrong_night_and_holds_companions():
    import holy_week_continuation as hw
    rows = hw.published_reverse()
    days = frozen()['daily']
    payload = {'rows': before_release(rows), 'daily_by_year': {
        str(y): {d: before_release(r, d) for d, r in days.items() if d.startswith(str(y))}
        for y in (2026, 2027, 2028)}}
    out = project('release', payload)
    for date in DATES:
        group = [r for r in out['daily_by_year'][date[:4]][date] if r.get('pascha_service') == 'eve_of_thursday' and r['service_hour'] == 'Eleventh Hour']
        assert [r['canonical_mt_ref'] for r in group] == ['Jn 12:44-50']
    old = [r for r in out['rows'] if r.get('identity_key') in {'rid_86a14760f5eee2200c69', 'rid_911892923f645ebfa5fb', 'rid_6dcf6122d785e98450f1'} and r.get('occasion') == 'Wednesday Eve' and r.get('service_hour') == 'Eleventh Hour']
    assert len(old) == 3
    assert all(r['removed_marker'] == 'held_wrong_context_holy_week_1.3.12' for r in old)


def test_real_release_boundary_qualifies_four_existing_burial_gospels():
    import holy_week_continuation as hw
    rows = hw.published_reverse()
    out = project('release', {'rows': before_release(rows), 'daily_by_year': {}})
    group = [r for r in out['rows'] if r.get('occasion') == 'Good Friday' and r.get('service_hour') == 'Twelfth Hour' and r.get('slot') == 'Gospel']
    assert len(group) == 4
    assert all(r['current_status'] == 'current_confirmed_coptic_reader' for r in group)
    assert all(json.loads(r['holy_week_continuation_json'])['capture_selected_year'] == 2026 for r in group)


@pytest.fixture(scope='module')
def successor():
    return project('release', release_payload())


def test_inverse_preserves_complete_predecessor_and_membership(successor):
    import holy_week_continuation as hw
    from scripts.review_release_contract import followup_daily_view, followup_reverse_view
    baseline = hw.published_reverse()
    assert hw.restore_reverse(successor['rows']) == baseline
    assert hw.project_reverse(successor['rows']) == successor['rows']
    assert hw.verify_membership(successor['rows']) == {'row_count': 12300, 'predecessor_rows': 12299, 'additions': 1, 'removals': 0}
    assert followup_reverse_view(successor['rows'], version='1.3.12') == followup_reverse_view(baseline, version='1.3.11')
    for year, days in successor['daily_by_year'].items():
        old = {d: frozen()['daily'][d] for d in days}
        assert followup_daily_view(days, version='1.3.12') == followup_daily_view(old, version='1.3.11')
        for date, rows in days.items():
            assert hw.project_daily(rows, date) == rows
            assert hw.project_daily(hw.restore_daily(rows, date), date) == rows
            assert len(rows) == (34 if date in DATES else 65)


@pytest.mark.parametrize('field,value', [
    ('source_family', 'other'), ('source_kind', 'other'), ('occasion', 'Thursday Eve'),
    ('service_hour', 'Sixth Hour'), ('service_section', 'Third Hour'),
    ('canonical_mt_ref', 'Jn 12:43-50'), ('spans_json', '[]'),
    ('current_status', 'current'), ('active', True), ('source_disclosure', '[]'),
    ('source_disclosure_count', 1), ('unexpected', 'injected'),
])
def test_owned_cells_cannot_be_laundered_by_inverse(successor, field, value):
    import holy_week_continuation as hw
    from scripts.review_release_contract import followup_daily_view
    rows = copy.deepcopy(successor['daily_by_year']['2026']['2026-04-08'])
    next(r for r in rows if r.get(hw.MARKER))[field] = value
    with pytest.raises(ValueError, match='Holy Week continuation'):
        followup_daily_view({'2026-04-08': rows}, version='1.3.12')
    reverse = copy.deepcopy(successor['rows'])
    next(r for r in reverse if r.get(hw.MARKER))[field] = value
    with pytest.raises(ValueError, match='Holy Week continuation'):
        hw.restore_reverse(reverse)


def test_wrong_dates_missing_duplicate_and_stripped_hold_rejected(successor):
    import holy_week_continuation as hw
    rows = successor['daily_by_year']['2026']['2026-04-08']
    for date in ('2026-04-09', '2027-04-08', '2029-04-08'):
        with pytest.raises(ValueError, match='wrong daily date'):
            hw.project_daily(rows, date)
    for bad in (rows[:-1], rows+[rows[-1]]):
        with pytest.raises(ValueError, match='Holy Week continuation'):
            hw.restore_daily(bad, '2026-04-08')
    for bad in (successor['rows'][:-1], successor['rows']+[successor['rows'][-1]]):
        with pytest.raises(ValueError, match='Holy Week continuation'):
            hw.verify_membership(bad)
    bad = copy.deepcopy(successor['rows'])
    hold = next(r for r in bad if r.get('removed_marker') == hw.HOLD)
    for key in (hw.MARKER, 'source_family', 'source_kind', 'removed_marker', 'active'):
        hold.pop(key, None)
    hold['current_status'] = 'current'
    with pytest.raises(ValueError, match='Holy Week continuation'):
        hw.verify_membership(bad)


def test_no_canonical_companion_invention_or_inactive_history_loss(successor):
    import holy_week_continuation as hw
    before = hw.published_reverse()
    owned = {_key(r) for r in frozen()['reverse']}
    assert [r for r in before if _key(r) not in owned] == [r for r in successor['rows'] if _key(r) not in owned and not r.get(hw.MARKER)]
    for date in DATES:
        old = frozen()['daily'][date]
        new = successor['daily_by_year'][date[:4]][date]
        unaffected = [r for r in old if not (r.get('pascha_service') == 'eve_of_thursday' and r['service_hour'] == 'Eleventh Hour')]
        actual = [r for r in new if not r.get(hw.MARKER)]
        strip_order = lambda rows: [{k:v for k,v in r.items() if k != 'reading_order'} for r in rows]
        assert strip_order(actual) == strip_order(unaffected)


def _key(row):
    return tuple(row.get(f, '') for f in ('identity_key', 'source_family', 'source_kind', 'occasion', 'service_section', 'service_hour', 'slot'))


def test_source_authentication_fails_closed_through_real_projection_and_inverse(monkeypatch, tmp_path, successor):
    import holy_week_continuation as hw
    for path in hw.PINS:
        dest = tmp_path / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((ROOT/path).read_bytes())
    monkeypatch.setattr(hw, 'ROOT', tmp_path)
    rows = frozen()['daily']['2026-04-08']
    assert hw.project_daily(rows, '2026-04-08')
    for path in hw.PINS:
        target = tmp_path/path
        raw = target.read_bytes()
        target.write_bytes(raw+b'corrupt')
        with pytest.raises(ValueError, match='source authentication failed'):
            hw.project_daily(rows, '2026-04-08')
        with pytest.raises(ValueError, match='source authentication failed'):
            hw.restore_reverse(successor['rows'])
        target.write_bytes(raw)


def test_historical_version_does_not_select_successor_policy(successor):
    from scripts.review_release_contract import followup_reverse_view, followup_daily_view
    with pytest.raises(ValueError):
        followup_reverse_view(successor['rows'], version='1.3.11')
    with pytest.raises(ValueError):
        followup_daily_view(successor['daily_by_year']['2026'], version='1.3.11')


def test_authentication_failure_reaches_real_release_and_both_comparison_callers(successor, monkeypatch):
    import holy_week_continuation as hw
    from scripts.review_release_contract import followup_reverse_view, followup_daily_view
    payload = release_payload()
    def refuse():
        raise ValueError('continuation injected source authentication failure')
    monkeypatch.setattr(hw, 'authenticate', refuse)
    with pytest.raises(ValueError, match='continuation injected source'):
        project('release', payload)
    with pytest.raises(ValueError, match='continuation injected source'):
        followup_reverse_view(successor['rows'], version='1.3.12')
    with pytest.raises(ValueError, match='continuation injected source'):
        followup_daily_view(successor['daily_by_year']['2026'], version='1.3.12')
