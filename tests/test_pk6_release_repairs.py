"""PK6 complete accepted controls and explicit no-third-current-Reader rule."""
import copy
import json
import pytest
import pk6_release_repairs as pk6


@pytest.fixture(scope='module')
def frozen(): return pk6.baseline()


def test_error_is_retired_and_joel_remains_historical_with_source_note(frozen):
    after=pk6.project_reverse(frozen['reverse_rows'])
    assert len(after)==2
    for old,new in zip(frozen['reverse_rows'],after):
        assert new['current_status']=='historical_witness'
        for f in ('identity_key','display_ref','canonical_mt_ref','canonical_lxx_ref','spans_json','source_locator','authority_tier'):
            assert new[f]==old[f]
        note=json.loads(new['source_disclosure'])[0]['historical_reference_review']
        assert note['reader_note'].startswith('Historical printed witness:')
        assert note['reader_omission']['fresh_app_verification'] is False
        assert note['reader_omission']['user_reports_current_reader_absence'] is True
        assert note['date_or_reason_of_liturgical_removal'] is None
        assert note['current_reader_activation_approved'] is False
        if new['identity_key']==pk6.ERROR_ID:
            assert new['active'] is False and new['status']=='removed'
            assert new['removal_effective_version']=='1.3.10'
            assert note['disposition']=='local_transcription_error_inactive_audit_witness'
        else:
            assert note['disposition']=='historical_printed_joel_not_current_reader_appointment'
    assert pk6.restore_reverse(after)==frozen['reverse_rows']
    assert pk6.project_reverse(after)==after


def test_complete_good_friday_tables_lose_only_erroneous_appointment(frozen):
    for date,before in frozen['daily'].items():
        after=pk6.project_daily(before,date)
        assert len(before)==66 and len(after)==65
        assert not any(r['identity_key'] in (pk6.ERROR_ID,pk6.JOEL_ID) for r in after)
        assert [r['reading_order'] for r in after]==list(range(1,66))
        assert pk6.restore_daily(after,date)==before
        assert pk6.project_daily(after,date)==after
        for new,old in zip(after,[r for r in before if r['identity_key']!=pk6.ERROR_ID]):
            assert {k:v for k,v in new.items() if k!='reading_order'}=={k:v for k,v in old.items() if k!='reading_order'}


@pytest.mark.parametrize('mutation',[{'active':True},{'current_status':'current_confirmed_coptic_reader'},
    {'canonical_mt_ref':'Joel 2:1-3,2:10-11'},{'source_disclosure':'[]'},{'removal_effective_version':'1.3.9'}])
def test_complete_valid_retirement_then_forgery_refused(frozen,mutation):
    after=pk6.project_reverse(frozen['reverse_rows'])
    assert pk6.restore_reverse(after)==frozen['reverse_rows']
    next(r for r in after if r['identity_key']==pk6.ERROR_ID).update(mutation)
    with pytest.raises(ValueError,match='PK'):
        pk6.restore_reverse(after)


def test_joel_is_not_activated_or_given_fresh_reader_authority(frozen):
    after=pk6.project_reverse(frozen['reverse_rows'])
    assert pk6.restore_reverse(after)==frozen['reverse_rows']
    row=next(r for r in after if r['identity_key']==pk6.JOEL_ID)
    row['current_status']='current_confirmed_coptic_reader'
    with pytest.raises(ValueError,match='PK'):
        pk6.restore_reverse(after)


def test_complete_daily_injection_reorder_or_missing_companion_rejected(frozen):
    date='2026-04-10';before=frozen['daily'][date]
    good=pk6.project_daily(before,date)
    assert pk6.restore_daily(good,date)==before
    erroneous=next(r for r in before if r['identity_key']==pk6.ERROR_ID)
    for bad in (good+[erroneous],good[:-1],list(reversed(good))):
        with pytest.raises(ValueError,match='PK'):
            pk6.restore_daily(bad,date)


def test_source_context_rebound_and_foreign_metadata_preserved(frozen):
    after=pk6.project_reverse(frozen['reverse_rows'])
    assert pk6.restore_reverse(after)==frozen['reverse_rows']
    after[0]['unexpected_approval']='forged'
    assert pk6.restore_reverse(after)[0]['unexpected_approval']=='forged'
    after[0].update(source_family='',source_kind='',source_locator='',source_disclosure='[]',removed_marker='')
    with pytest.raises(ValueError,match='PK'):
        pk6.restore_reverse(after)
