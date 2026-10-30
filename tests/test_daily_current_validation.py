"""Bounded real package-validator regressions; no builders or publication."""
import copy
import datetime as dt
import json
import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

import holy_week_review_repairs as holy
import kiahk23_review_repairs as r2
from scripts import review_release_contract as contract
from scripts import verify_package_integrity as v

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.write_text(json.dumps(value), encoding='utf-8')


@pytest.fixture(scope='module')
def bounded_package(tmp_path_factory):
    """Keep real authenticated rows/runtime, shrink only the corpus inventory.

    This is a daily-boundary integration fixture, not release-corpus acceptance.
    No validation gates are mocked and no producer is invoked.
    """
    source = ROOT / 'packages/lectionary-data'
    reverse_path = Path(os.environ.get('LECTIONARY_REVIEW_REVERSE',
                                      source / 'data/reverse_lectionary_index.jsonl'))
    reverse = v.parse_jsonl(reverse_path)
    owned = [row for row in reverse if row.get('source_family') == r2.FAMILY]
    retired = next(row for row in reverse if row.get('kiahk23_retirement'))
    held = next(row for row in reverse if row.get('current_status') == holy.HOLD)
    assert len(owned) == 9
    assert contract.review_inactive_qualified(retired)
    assert contract.review_inactive_qualified(held)

    daily_source = json.loads((source / 'data/daily/lectionary-2026.json').read_text())
    current = [copy.deepcopy(row) for row in daily_source['2026-01-01']
               if row.get('source_family') == r2.FAMILY]
    assert len(current) == 9
    for index, row in enumerate(current, 1):
        row['reading_order'] = index
    # Use an exact reverse occurrence, not a differently spelled daily label,
    # so the legacy transport without spans has a genuine exact-join control.
    ordinary_reverse = next(row for row in reverse
                            if row.get('identity_key') == daily_source['2026-01-02'][0]['identity_key']
                            and row.get('coptic_date_key') == 'kiahk-24'
                            and v.is_current_reference_row(row))
    ordinary = dict(copy.deepcopy(ordinary_reverse), reading_order=1, service_order=1)
    selected = owned + [retired, held, ordinary_reverse]

    package = tmp_path_factory.mktemp('daily-current-package').resolve()
    generated = {'meta.json', 'data/reverse_lectionary_index.jsonl'}
    for relative in sorted(v.REQUIRED_PACKAGE_FILES):
        target = package / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative not in generated and not relative.startswith('data/daily/'):
            shutil.copyfile(source / relative, target)
    (package / 'data/reverse_lectionary_index.jsonl').write_text(
        ''.join(json.dumps(row) + '\n' for row in selected), encoding='utf-8')
    meta = json.loads((source / 'meta.json').read_text())
    meta['occasion_index_rows'] = len(selected)
    removed = sum(v.is_removed_projection_row(row) for row in selected)
    meta['projection_rules'] = {'active_rows': len(selected) - removed,
                                'removed_rows_included': removed}
    meta['daily_files'] = []
    for year in meta['shipped_years']:
        start, end = dt.date(year, 1, 1), dt.date(year + 1, 1, 1)
        daily = {(start + dt.timedelta(days=offset)).isoformat(): []
                 for offset in range((end - start).days)}
        if year == 2026:
            daily['2026-01-01'] = current
            daily['2026-01-02'] = [ordinary]
        write_json(package / f'data/daily/lectionary-{year}.json', daily)
        meta['daily_files'].append(dict(year=year, rows=len(daily),
                                       date_count=len(daily),
                                       reading_count=sum(map(len, daily.values()))))
    write_json(package / 'meta.json', meta)
    return package, retired, held


@pytest.fixture
def package(bounded_package, tmp_path):
    target = tmp_path / 'package'
    shutil.copytree(bounded_package[0], target)
    return target


def validate(package):
    with patch('sqlite3.connect', side_effect=AssertionError('SQLite forbidden')):
        return v.validate_package_integrity(package, strict_file_set=True)


def replace_ordinary(package, updates, *, embedded_spans=True):
    path = package / 'data/daily/lectionary-2026.json'
    daily = json.loads(path.read_text())
    row = daily['2026-01-02'][0]
    row.update(updates)
    if not embedded_spans:
        row.pop('spans_json')
    write_json(path, daily)
    return row


@pytest.mark.parametrize('embedded_spans', [True, False], ids=['embedded', 'reverse-joined'])
def test_current_only_control_accepts_source_only_psalms_and_reverse_history(package, embedded_spans):
    replace_ordinary(package, {}, embedded_spans=embedded_spans)
    result = validate(package)
    assert result['failures'] == []
    assert result['status'] == 'pass'
    current = json.loads((package / 'data/daily/lectionary-2026.json').read_text())['2026-01-01']
    psalms = [row for row in current if not row['canonical_mt_ref']]
    assert len(psalms) == 3
    assert all(v.is_current_reference_row(row) for row in current)
    assert all(contract.source_owned_empty_coordinates(row, '2026-01-01') for row in psalms)
    assert result['removed_projection_rows'] == 2


@pytest.mark.parametrize('embedded_spans', [True, False], ids=['embedded', 'reverse-joined'])
@pytest.mark.parametrize('updates, reason', [
    ({'active': False}, 'noncurrent_daily_reading'),
    ({'status': 'removed'}, 'noncurrent_daily_reading'),
    ({'current_status': 'historical_witness'}, 'noncurrent_daily_reading'),
    ({'current_status': 'historical_candidate_removed'}, 'noncurrent_daily_reading'),
    ({'current_status': 'superseded_by_source'}, 'noncurrent_daily_reading'),
    ({'removed_marker': 'removed_by_source'}, 'noncurrent_daily_reading'),
    ({'current_status': 'current_unreviewed_forgery'}, 'unknown_daily_reading_status'),
    ({'current_status': '', 'status': 'unknown_archive_state'}, 'unknown_daily_reading_status'),
])
def test_daily_lifecycle_is_checked_before_both_reference_paths(package, updates, reason, embedded_spans):
    row = replace_ordinary(package, updates, embedded_spans=embedded_spans)
    result = validate(package)
    assert result['status'] == 'fail'
    assert len(result['failures']) == 1, result['failures']
    failure = result['failures'][0]
    assert failure['reason'] == reason
    assert failure['date'] == '2026-01-02'
    assert failure['reading_index'] == 1
    assert failure['identity_key'] == row['identity_key']
    assert failure['current_status'] == row['current_status']
    if reason == 'unknown_daily_reading_status':
        assert 'Unknown explicit reading status:' in failure['detail']


@pytest.mark.parametrize('archive_index', [1, 2], ids=['authenticated-kiahk-retirement', 'authenticated-holy-hold'])
def test_authenticated_reverse_history_is_still_forbidden_in_daily(package, bounded_package, archive_index):
    archive = copy.deepcopy(bounded_package[archive_index])
    assert contract.review_inactive_qualified(archive)
    reverse_path = package / 'data/reverse_lectionary_index.jsonl'
    before = reverse_path.read_bytes()
    path = package / 'data/daily/lectionary-2026.json'
    daily = json.loads(path.read_text())
    archive.update(reading_order=10, service_order=1)
    daily['2026-01-01'].append(archive)
    write_json(path, daily)
    meta = json.loads((package / 'meta.json').read_text())
    meta['daily_files'][0]['reading_count'] += 1
    write_json(package / 'meta.json', meta)
    result = validate(package)
    assert result['status'] == 'fail'
    assert len(result['failures']) == 1, result['failures']
    failure = result['failures'][0]
    assert failure['reason'] == 'noncurrent_daily_reading'
    assert failure['date'] == '2026-01-01'
    assert failure['reading_index'] == 10
    assert failure['identity_key'] == archive['identity_key']
    assert reverse_path.read_bytes() == before
    assert contract.review_inactive_qualified(bounded_package[archive_index])
