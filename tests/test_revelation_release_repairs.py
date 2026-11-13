"""Literal source-backed successor and display-only hold regressions."""
import copy
import json
import re
import pytest
import revelation_release_repairs as repair


@pytest.fixture(scope='module')
def frozen():
    return repair.baseline()


def test_endpoint_successor_and_exact_historical_witness(frozen):
    before = frozen['reverse_rows']
    after = repair.project_rows(before)
    assert len(after) == len(before) + 1
    old, = [r for r in after if r['identity_key'] == repair.OLD_ID]
    new, = [r for r in after if r['identity_key'] == repair.NEW_ID]
    assert new['canonical_mt_ref'] == new['canonical_lxx_ref'] == 'Deut 32:1-43'
    assert json.loads(new['spans_json'])[0]['verse_end'] == 43
    assert new['current_status'] == 'current_confirmed_coptic_reader'
    assert old['removal_effective_version'] == '1.3.10'
    assert old['active'] is False and old['status'] == 'removed'
    original, = [r for r in before if r['identity_key'] == repair.OLD_ID]
    for field in ('display_ref','spans_json','source_locator','source_disclosure','canonical_mt_ref','canonical_lxx_ref'):
        assert old[field] == original[field]
    assert repair.restore_rows(after) == before
    assert repair.project_rows(after) == after


def test_display_cleanup_preserves_every_coordinate_hold_and_raw_month(frozen):
    before = frozen['reverse_rows']
    after = repair.project_rows(before)
    held = [r for r in before if r['identity_key'] != repair.OLD_ID]
    assert len(held) == 22
    for original in held:
        new, = [r for r in after if (r['identity_key'],r['source_locator'],r['occasion'],r['service_section']) ==
                (original['identity_key'],original['source_locator'],original['occasion'],original['service_section'])]
        assert new['display_ref'] == original['display_ref'].split(' (Reader')[0]
        assert not re.search('held|Reader selection',new['display_ref'],re.I)
        for field in ('canonical_mt_ref','canonical_lxx_ref','spans_json','current_status','occasion','calendar_keys','display_label'):
            assert new[field] == original[field]
        disclosures = json.loads(new['source_disclosure'])
        for source in disclosures:
            assert source['display_reference_review']['raw_display_ref'] == original['display_ref']
    assert repair.restore_rows(after) == before


def test_all_three_daily_endpoints_and_thirty_hold_labels(frozen):
    held_count = endpoint_count = 0
    for date, before in frozen['daily'].items():
        after = repair.project_rows(before,date=date)
        assert len(after) == len(before)
        assert repair.restore_rows(after,date=date) == before
        assert repair.project_rows(after,date=date) == after
        for old, new in zip(before,after):
            if old['identity_key'] == repair.OLD_ID:
                endpoint_count += 1
                assert new['identity_key'] == repair.NEW_ID
                assert new['display_ref'] == 'Deut 32:1-43'
            else:
                held_count += 1
                assert new['display_ref'] == old['display_ref'].split(' (Reader')[0]
                assert new['spans_json'] == old['spans_json']
    assert (endpoint_count,held_count) == (3,30)


@pytest.mark.parametrize('field,value', [('canonical_mt_ref','Ps 17:15'),('canonical_lxx_ref','Ps 16:15'),
    ('spans_json','[{"book":"Ps","chapter_start":17}]'),('current_status','current_confirmed_coptic_reader'),
    ('source_family','forged'),('source_kind','forged'),('source_locator','forged'),('occasion','forged'),
    ('source_disclosure','[]'),('active',True)])
def test_complete_valid_reverse_then_mutation_rejected(frozen,field,value):
    after = repair.project_rows(frozen['reverse_rows'])
    assert repair.restore_rows(after) == frozen['reverse_rows']
    bad = copy.deepcopy(after)
    target = next(r for r in bad if r['current_status'] == 'pending_psalm_equivalence_unresolved')
    target[field] = value
    with pytest.raises(ValueError,match='PK'):
        repair.restore_rows(bad)


def test_daily_context_rebinding_and_compound_stripping_rejected(frozen):
    date = '2026-04-11'
    after = repair.project_rows(frozen['daily'][date],date=date)
    assert repair.restore_rows(after,date=date) == frozen['daily'][date]
    with pytest.raises(ValueError,match='PK'):
        repair.restore_rows(after,date='2026-04-12')
    bad = copy.deepcopy(after)
    row = next(r for r in bad if r['identity_key'] == repair.NEW_ID)
    row.update(source_family='',source_kind='',source_locator='',source_disclosure='[]',removed_marker='')
    with pytest.raises(ValueError,match='PK'):
        repair.restore_rows(bad,date=date)


@pytest.mark.parametrize('mutation', [{'active':True}, {'removal_effective_version':'1.3.9'},
    {'canonical_mt_ref':'Deut 32:1-43'},{'source_disclosure':'[]'}, {'status':False}])
def test_retired_witness_cannot_be_reactivated_or_rewritten(frozen,mutation):
    after = repair.project_rows(frozen['reverse_rows'])
    assert repair.restore_rows(after) == frozen['reverse_rows']
    old = next(r for r in after if r['identity_key'] == repair.OLD_ID)
    old.update(mutation)
    with pytest.raises(ValueError,match='PK'):
        repair.restore_rows(after)


def test_missing_duplicate_successor_and_missing_history_refused(frozen):
    after = repair.project_rows(frozen['reverse_rows'])
    assert repair.restore_rows(after) == frozen['reverse_rows']
    for id_to_remove in (repair.OLD_ID,repair.NEW_ID):
        with pytest.raises(ValueError,match='PK'):
            repair.restore_rows([r for r in after if r['identity_key'] != id_to_remove])
    with pytest.raises(ValueError,match='PK'):
        repair.restore_rows(after + [copy.deepcopy(next(r for r in after if r['identity_key'] == repair.NEW_ID))])


def test_foreign_fields_survive_inverse_for_downstream_rejection(frozen):
    after = repair.project_rows(frozen['reverse_rows'])
    next(r for r in after if r['identity_key'] == repair.OLD_ID)['unexpected_approval'] = 'forged'
    restored = repair.restore_rows(after)
    assert next(r for r in restored if r['identity_key'] == repair.OLD_ID)['unexpected_approval'] == 'forged'


def test_source_authentication_failure_is_not_cached(frozen,monkeypatch):
    assert repair.restore_rows(repair.project_rows(frozen['reverse_rows'])) == frozen['reverse_rows']
    def refuse():
        raise ValueError('PK retained source authentication failed')
    monkeypatch.setattr(repair,'authenticate_endpoint',refuse)
    with pytest.raises(ValueError,match='PK retained source'):
        repair.project_rows(frozen['reverse_rows'])
