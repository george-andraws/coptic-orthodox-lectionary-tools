"""Exercise both real release callers: successor must not skip prior guards."""
import pytest
from scripts import review_release_contract as contract
from scripts import verify_package_integrity as integrity
from scripts import compare_external_sources as compare


@pytest.mark.parametrize('version',['1.3.8','1.3.9','1.3.10'])
def test_integrity_version_routes_reverse_and_daily_through_authenticated_lane(version,monkeypatch):
    original_load = integrity.load_json
    calls = []
    def load(path):
        result = original_load(path)
        if path.name in ('meta.json','package.json'):
            result['version'] = version
        return result
    def reverse(rows,**kwargs):
        assert len(rows) > 12000
        calls.append(('reverse',kwargs.get('version')))
        raise ValueError('route sentinel reverse')
    def daily(days,**kwargs):
        assert sum(map(len,days.values())) > 4000
        calls.append(('daily',kwargs.get('version')))
        raise ValueError('route sentinel daily')
    monkeypatch.setattr(integrity,'load_json',load)
    monkeypatch.setattr(contract,'followup_reverse_view',reverse)
    monkeypatch.setattr(contract,'followup_daily_view',daily)
    report = integrity.validate_package_integrity(integrity.PACKAGE_DIR)
    failures = report['failures']
    assert any(f['reason'] == 'unqualified_followup_reverse' and 'route sentinel' in f['detail'] for f in failures)
    assert sum(f['reason'] == 'unqualified_followup_daily' and 'route sentinel' in f['detail'] for f in failures) == 3
    assert calls == [('reverse',version)] + [('daily',version)]*3


@pytest.mark.parametrize('version',['1.3.8','1.3.9','1.3.10'])
def test_comparator_version_routes_actual_complete_daily_through_authenticated_lane(version,monkeypatch):
    original_load = compare.load_json
    def load(path):
        result = original_load(path)
        if path.name == 'meta.json':
            result['version'] = version
        return result
    def daily(days,**kwargs):
        assert sum(map(len,days.values())) > 4000
        assert kwargs['version'] == version
        raise ValueError('route sentinel comparator')
    monkeypatch.setattr(compare,'load_json',load)
    monkeypatch.setattr(contract,'followup_daily_view',daily)
    with pytest.raises(ValueError,match='route sentinel comparator'):
        compare.compare_copticchurch_cache(years=[2026])


def test_integrity_counts_public_daily_rows_not_authenticated_inverse_history(monkeypatch):
    report = integrity.validate_package_integrity(integrity.PACKAGE_DIR)
    assert report['status'] == 'pass', report['failures']
    assert {year: row['reading_count'] for year,row in report['daily_summary'].items()} == {
        '2026':4078,'2027':4068,'2028':4086}
    original_load = integrity.load_json
    def forged_metadata(path):
        result = original_load(path)
        if path.name == 'meta.json':
            for item in result['daily_files']:
                item['reading_count'] += 1
        return result
    monkeypatch.setattr(integrity,'load_json',forged_metadata)
    bad = integrity.validate_package_integrity(integrity.PACKAGE_DIR)
    assert sum(f['reason'] == 'daily_meta_reading_count_mismatch' for f in bad['failures']) == 3
