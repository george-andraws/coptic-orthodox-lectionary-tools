"""Candidate order must cross the real historical-comparison boundary intact."""
import copy
import gzip
import hashlib
import json
from pathlib import Path

import pytest
from scripts.review_release_contract import followup_daily_view

ROOT = Path(__file__).resolve().parents[1]


def frozen():
    payload = (ROOT / 'tests/fixtures/good-friday-published-1.3.11.json.gz').read_bytes()
    assert hashlib.sha256(payload).hexdigest() == '54f264bdb981bbc7e8fbbaad9c2554b7bdc28c6a62599c9e3a8025ae7e73f4d3'
    return json.loads(gzip.decompress(payload))['daily']


def successor(rows):
    output = copy.deepcopy(rows)
    for hour, refs in (
        ('Sixth Hour', ['Matt 27:27-45', 'Mark 15:26-33', 'Lk 23:26-44', 'Jn 19:13-27']),
        ('Twelfth Hour', ['Matt 27:57-61', 'Mark 15:42-16:1', 'Lk 23:50-56', 'Jn 19:38-42']),
    ):
        positions = [i for i, r in enumerate(rows) if r['service_section'] == hour and r['slot'] == 'Gospel']
        assert len(positions) == 4
        for i, ref in zip(positions, refs):
            output[i] = copy.deepcopy(next(r for r in rows if r['service_section'] == hour and r['canonical_mt_ref'] == ref))
    for i, r in enumerate(output):
        r['reading_order'] = i + 1
    return output


@pytest.mark.parametrize('date', ['2026-04-10', '2027-04-30', '2028-04-14'])
def test_real_followup_view_accepts_only_the_source_order_delta(date):
    baseline = frozen()[date]
    expected = followup_daily_view({date: baseline}, version='1.3.11')
    changed = successor(baseline)
    assert changed != baseline
    assert followup_daily_view({date: changed}, version='1.3.11') == expected
    assert baseline == frozen()[date]


@pytest.mark.parametrize('field,value', [
    ('canonical_mt_ref', 'Jn 19:1-12'), ('source_family', 'other'),
    ('source_kind', 'other'), ('source_disclosure', '[]'), ('active', False),
    ('slot_order', True), ('service_hour', 'Third Hour'), ('unexpected', 'injected'),
])
def test_real_followup_view_does_not_launder_foreign_changes(field, value):
    date = '2026-04-10'
    rows = successor(frozen()[date])
    rows[38][field] = value
    with pytest.raises((ValueError, TypeError, KeyError)):
        followup_daily_view({date: rows}, version='1.3.11')


def test_real_followup_view_rejects_missing_or_duplicated_current_member():
    date = '2026-04-10'
    rows = successor(frozen()[date])
    for altered in (rows[:-1], rows + [rows[-1]]):
        with pytest.raises((ValueError, TypeError, KeyError)):
            followup_daily_view({date: altered}, version='1.3.11')


def test_real_followup_view_reauthenticates_sources_and_predecessor(monkeypatch, tmp_path):
    import good_friday_order_review as ordering
    for relative, _ in (*ordering.SOURCES, (ordering.FIXTURE, ordering.FIXTURE_SHA256)):
        dest = tmp_path / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((ROOT / relative).read_bytes())
    monkeypatch.setattr(ordering, 'ROOT', tmp_path)
    date = '2026-04-10'
    rows = successor(frozen()[date])
    expected = followup_daily_view({date: rows}, version='1.3.11')
    assert expected
    for relative, _ in (*ordering.SOURCES, (ordering.FIXTURE, ordering.FIXTURE_SHA256)):
        target = tmp_path / relative
        original = target.read_bytes()
        target.write_bytes(original + b'corrupt')
        with pytest.raises(ValueError, match='Good Friday ordering source authentication failed'):
            followup_daily_view({date: rows}, version='1.3.11')
        target.write_bytes(original)
    assert followup_daily_view({date: rows}, version='1.3.11') == expected


def test_inverse_leaves_historical_version_and_wrong_date_guards_intact():
    import good_friday_order_review as ordering
    date = '2026-04-10'
    baseline = frozen()[date]
    rows = successor(baseline)
    assert ordering.restore_daily_order(rows, date) == baseline
    assert ordering.restore_daily_order(ordering.restore_daily_order(rows, date), date) == baseline
    assert ordering.restore_daily_order(rows, '2026-04-09') == rows
    with pytest.raises(ValueError):
        followup_daily_view({date: rows}, version='1.3.10')
