"""Complete real serialized candidate controls, not incomplete fixture refusals."""
import copy
import json
from pathlib import Path
import pytest
from scripts import review_release_contract as contract
import revelation_release_repairs as repair

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def candidate():
    package = ROOT / 'packages/lectionary-data'
    version=json.loads((package/'package.json').read_text())['version']
    assert version in ('1.3.10','1.3.11','1.3.12')
    reverse = [json.loads(line) for line in (package/'data/reverse_lectionary_index.jsonl').read_text().splitlines()]
    daily = json.loads((package/'data/daily/lectionary-2026.json').read_text())
    if version == '1.3.12':
        from holy_week_successor_fixture import reverse_1_3_11, daily_1_3_11
        reverse = reverse_1_3_11(reverse)
        daily = {d: daily_1_3_11(rows, d) for d, rows in daily.items()}
        version = '1.3.11'
    if version=='1.3.11':
        # Authenticate the complete real outer successor before preserving all
        # historical1.3.10 counts, mutation assertions and contract expectations.
        import final_site_review_repairs as final
        import site_review_repairs as site
        reverse=site.restore_rows(final.restore_rows(reverse))
        daily={d:site.restore_rows(final.restore_rows(rows,date=d),date=d)for d,rows in daily.items()}
    assert len(reverse) == 12291 and sum(map(len,daily.values())) == 4078
    # These are genuine complete-valid controls through every prior inverse.
    assert len(contract.followup_reverse_view(reverse,version='1.3.10')) > 12000
    assert len(contract.followup_daily_view(daily,version='1.3.10')) == 365
    return reverse,daily


@pytest.mark.parametrize('field,value', [('canonical_mt_ref','Ps 17:15'),('spans_json','[]'),
    ('source_family','forged'),('current_status','historical_witness')])
def test_complete_reverse_source_only_and_source_coordinate_holds_fail_closed(candidate,field,value):
    reverse,_ = candidate
    for source_only in (True,False):
        bad = copy.deepcopy(reverse)
        row = next(r for r in bad if r['current_status'] == 'pending_psalm_equivalence_unresolved'
                   and (r['spans_json'] == '[]') is source_only)
        # Keep this mutation distinct from the valid source-only empty span shape.
        row[field] = '[{"book":"Ps","chapter_start":17}]' if field == 'spans_json' else value
        with pytest.raises(ValueError,match='PK source/context/coordinate drift'):
            contract.followup_reverse_view(bad,version='1.3.10')


def test_complete_daily_fabricated_coordinates_rejected_and_older_numeric_hold_retained(candidate):
    _,daily = candidate
    bad = copy.deepcopy(daily)
    target = next(r for r in bad['2026-04-11'] if r['current_status'] == 'pending_psalm_equivalence_unresolved')
    assert target['spans_json'] == '[]'
    target['canonical_mt_ref'] = 'Ps 17:15'
    with pytest.raises(ValueError,match='PK source/context/coordinate drift: canonical_mt_ref'):
        contract.followup_daily_view(bad,version='1.3.10')


def test_complete_reverse_foreign_lifecycle_drift_is_not_hidden_by_inverse(candidate):
    reverse,_ = candidate
    bad = copy.deepcopy(reverse)
    # Unrelated earlier-layer source qualification must still see its mutation.
    row = next(r for r in bad if r.get('evidence_json'))
    row['active'] = False
    with pytest.raises(ValueError,match='evidence'):
        contract.followup_reverse_view(bad,version='1.3.10')


def test_public_default_daily_and_reverse_archive_use_real_current_predicate(candidate):
    import subprocess
    result = subprocess.run(['node','-e', "const p=require('./packages/lectionary-data');const fs=require('fs');const r=fs.readFileSync(p.occasionIndexPath,'utf8').trim().split('\\n').map(JSON.parse);const old=r.filter(x=>x.identity_key==='rid_8ae616e6b96572e37bd9');if(old.length!==1||p.isCurrentReading(old[0]))process.exit(1);for(const y of p.shippedYears){const d=JSON.parse(fs.readFileSync(p.dailyYearPath(y)));if(!Object.values(d).flat().every(p.isCurrentReading))process.exit(2);}console.log('current-only daily; one inactive PK2 predecessor');"],cwd=ROOT,text=True,capture_output=True)
    assert result.returncode == 0,result.stderr


def test_pk6_notes_and_inactive_error_through_actual_serialized_package(candidate):
    import pk6_release_repairs as pk6
    reverse,daily = candidate
    error, = [r for r in reverse if r['identity_key'] == pk6.ERROR_ID]
    joel, = [r for r in reverse if r['identity_key'] == pk6.JOEL_ID]
    assert error['current_status'] == joel['current_status'] == 'historical_witness'
    assert error['active'] is False and error['removal_effective_version'] == '1.3.10'
    assert error['canonical_mt_ref'] == 'Hos 2:1-3,2:10-11'
    assert joel['canonical_mt_ref'] == 'Joel 2:1-3,2:10-11'
    for row in (error,joel):
        note = json.loads(row['source_disclosure'])[0]['historical_reference_review']
        assert note['printed_source']['pages'] == [610,611]
        assert note['current_reader_activation_approved'] is False
        assert note['date_or_reason_of_liturgical_removal'] is None
    assert len(daily['2026-04-10']) == 65
    assert not any(r['identity_key'] in (pk6.ERROR_ID,pk6.JOEL_ID) for r in daily['2026-04-10'])


def test_pk6_source_failure_is_closed_at_composed_reverse_and_daily_callers(candidate,monkeypatch):
    import pk6_release_repairs as pk6
    reverse,daily = candidate
    def refuse():
        raise ValueError('PK6 injected source authentication failure')
    monkeypatch.setattr(pk6,'authenticate',refuse)
    with pytest.raises(ValueError,match='PK6 injected source'):
        contract.followup_reverse_view(reverse,version='1.3.10')
    with pytest.raises(ValueError,match='PK6 injected source'):
        contract.followup_daily_view(daily,version='1.3.10')
