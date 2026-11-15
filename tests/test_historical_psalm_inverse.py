"""Offline historical inverses: independently authenticated 1.3.8 AND 1.3.9 bytes.

The bounded fixture retains 18 reverse rows (all six PK loci plus four LK9
annotations) and five complete 2026 days from EACH archive. Their Psalm slices
are identical, but the complete member/archive hashes are not. Historical output
oracles were obtained with the base-commit implementation, not the candidate.
No npm cache, registry request, scratch path or generated baseline is required.
"""
import copy
import gzip
import hashlib
import json
from pathlib import Path

import pytest

import evidence_followup_repairs as evidence
from scripts import review_release_contract as contract

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'sources/revelation-review-1.3.10/published-historical-psalm-inverse.json.gz'
FIXTURE_SHA256 = 'ea3cc21cacf296178ed99870666b7b15eab92d4a7e95dabab8670ce80dd6271f'
ARCHIVES = {
    '1.3.8': '99473ce26796bd8510022d97f53a4e38b08e096c206fbf59a148da1fdbe0133d',
    '1.3.9': 'e1636d4c33ed409bad910130eca6c56c27b45ea5b350522c7effa1146a4f7c80',
}
SLICE_SHA256 = '299e20ca7b19862951e9153b3d0bfcf7ee594d2f4e6f6815c189e2b1f5f797cc'


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


@pytest.fixture(scope='module')
def historical():
    raw = FIXTURE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256
    versions = json.loads(gzip.decompress(raw))['versions']
    assert set(versions) == set(ARCHIVES)
    for version, data in versions.items():
        assert data['archive_sha256'] == ARCHIVES[version]
        assert data['archive_url'].endswith('/lectionary-data-' + version + '.tgz')
        assert len(data['reverse_rows']) == 18
        assert len(data['daily']) == 5
        assert sum(map(len, data['daily'].values())) == 48
        assert len(data['daily']['2026-02-01']) == 10
        assert digest({k: data[k] for k in ('reverse_rows', 'daily')}) == data['slice_sha256'] == SLICE_SHA256
        assert evidence.REVELATION_PSALM_REFS <= {r['canonical_mt_ref'] for r in data['reverse_rows']}
        assert sum(bool(r.get('psalm_annotation_review_json')) for r in data['reverse_rows']) == 4
    assert versions['1.3.8']['members_sha256'] != versions['1.3.9']['members_sha256']
    return versions


@pytest.mark.parametrize('version', ARCHIVES)
def test_authenticated_historical_daily_inverse_recovers_base_output(historical, version):
    data = historical[version]
    result = contract.followup_daily_view(data['daily'], version=version)
    assert len(result['2026-02-01']) == 10
    assert digest(result) == data['expected_views_sha256']['daily']


@pytest.mark.parametrize('version', ARCHIVES)
def test_authenticated_historical_reverse_inverse_recovers_base_output(historical, version):
    data = historical[version]
    result = contract.followup_reverse_view(data['reverse_rows'], version=version, require_all_targets=False)
    assert len(result) == 18
    assert digest(result) == data['expected_views_sha256']['reverse']


@pytest.mark.parametrize('version', ARCHIVES)
def test_direct_historical_evidence_inverse_uses_same_explicit_version(historical, version):
    data = historical[version]
    assert digest(evidence.restore_rows_for_comparison(data['reverse_rows'], version=version)) == data['expected_views_sha256']['evidence_reverse']
    for date, rows in data['daily'].items():
        assert digest(evidence.restore_rows_for_comparison(rows, date=date, version=version)) == data['expected_views_sha256']['evidence_daily'][date]


@pytest.mark.parametrize('version', ARCHIVES)
@pytest.mark.parametrize('route', ['reverse', 'daily'])
@pytest.mark.parametrize('field,value', [('canonical_lxx_ref', 'Ps 50:99'),
                                       ('display_ref', 'forged'), ('spans_json', '[]'),
                                       ('psalm_annotation_review_json', None)])
def test_historical_lk9_annotations_still_require_exact_delta_and_disclosure(historical, version, route, field, value):
    data = historical[version]
    rows = copy.deepcopy(data['reverse_rows'] if route == 'reverse' else data['daily']['2026-05-23'])
    target = next(r for r in rows if r.get('psalm_annotation_review_json'))
    if value is None:
        target.pop(field)
    else:
        target[field] = value
    with pytest.raises(ValueError, match='^Psalm annotation authenticated delta drift: ' + field + '$'):
        if route == 'reverse':
            contract.followup_reverse_view(rows, version=version, require_all_targets=False)
        else:
            contract.followup_daily_view({'2026-05-23': rows}, version=version)


def test_default_evidence_helpers_keep_current_exact_inverse(historical):
    before = [r for r in historical['1.3.9']['reverse_rows'] if r['canonical_mt_ref'] in evidence.REVELATION_PSALM_REFS]
    after, counts = evidence.repair_psalm_annotations(before)
    assert counts['annotations_changed'] == 11
    assert evidence.repair_psalm_annotations(before, version='1.3.10') == (after, counts)
    assert evidence.restore_rows_for_comparison(after) == before
    assert evidence.restore_rows_for_comparison(after, version='1.3.10') == before
    for version in ARCHIVES:
        assert evidence.repair_psalm_annotations(before, version=version)[0] == before
        assert evidence.frame_qualified_lxx('Ps 116:15-16', version=version) == ('Ps 115:15-16', 'chapter_mapped_verse_offset_not_guessed', 'medium')
    assert evidence.frame_qualified_lxx('Ps 116:15-16')[0] == 'Ps 115:6-7'


@pytest.mark.parametrize('version', ARCHIVES)
@pytest.mark.parametrize('route', ['reverse', 'daily'])
def test_current_pk_annotations_cannot_be_authenticated_as_historical(historical, version, route):
    data = historical[version]
    before = data['reverse_rows'] if route == 'reverse' else data['daily']['2026-02-01']
    after, counts = evidence.repair_psalm_annotations(before)
    assert counts['annotations_changed'] > 0
    with pytest.raises(ValueError, match='^Psalm annotation unqualified source context$'):
        if route == 'reverse':
            contract.followup_reverse_view(after, version=version, require_all_targets=False)
        else:
            contract.followup_daily_view({'2026-02-01': after}, version=version)


@pytest.fixture(scope='module')
def current():
    package = ROOT / 'packages/lectionary-data'
    reverse = [json.loads(line) for line in (package / 'data/reverse_lectionary_index.jsonl').read_bytes().splitlines()]
    days = json.loads((package / 'data/daily/lectionary-2026.json').read_bytes())
    daily = {date: days[date] for date in ('2026-02-01', '2026-05-23')}
    import final_site_review_repairs as final
    import site_review_repairs as site
    predecessor_reverse = site.restore_rows(final.restore_rows(reverse))
    predecessor_daily = {date: site.restore_rows(final.restore_rows(rows, date=date), date=date)
                         for date, rows in daily.items()}
    assert len(reverse) == 12299 and len(predecessor_reverse) == 12291
    # Exact outputs pinned before the fix; the new historical branch must not alter them.
    assert digest(contract.followup_reverse_view(predecessor_reverse, version='1.3.10')) == '44c836aca2a268034458554d1408bdbb5e4c50b943fab363718b4bb4654f9a98'
    assert digest(contract.followup_daily_view(predecessor_daily, version='1.3.10')) == 'bc48244c4bd06aed1e8afc0ae8d62c13eadb1ee3f0dcd0a55e6308abee5d031b'
    return predecessor_reverse, predecessor_daily


def test_current_complete_reverse_and_daily_outputs_unchanged(current):
    reverse, daily = current
    assert len(reverse) == 12291 and len(daily['2026-02-01']) == 10


@pytest.mark.parametrize('route', ['reverse', 'daily'])
@pytest.mark.parametrize('field,value', [('canonical_lxx_ref', 'Ps 115:99'),
                                       ('display_ref', 'forged'), ('spans_json', '[]'),
                                       ('psalm_annotation_review_json', None)])
def test_current_annotations_still_require_exact_delta_and_disclosure(current, route, field, value):
    reverse, daily = current
    rows = copy.deepcopy(reverse if route == 'reverse' else daily['2026-02-01'])
    target = next(r for r in rows if r.get('psalm_annotation_review_json') and r['canonical_mt_ref'] in evidence.REVELATION_PSALM_REFS)
    if value is None:
        target.pop(field)
    else:
        target[field] = value
    with pytest.raises(ValueError, match='^Psalm annotation authenticated delta drift: ' + field + '$'):
        if route == 'reverse':
            contract.followup_reverse_view(rows, version='1.3.10')
        else:
            contract.followup_daily_view({'2026-02-01': rows}, version='1.3.10')
