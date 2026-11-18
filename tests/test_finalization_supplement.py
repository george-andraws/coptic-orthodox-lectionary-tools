"""Bounded independent source supplement and IR-02 provenance regressions."""
import copy
import json
from collections import Counter
from pathlib import Path
import pytest
import final_site_review_repairs as repair

ROOT=Path(__file__).resolve().parents[1]
BRIGHT=('2026-04-11','2027-05-01','2028-04-15')


def _bare_sources(row):
    return Counter(json.dumps({k:v for k,v in s.items()if k!='final_site_review'},sort_keys=True)
                   for s in json.loads(row['source_disclosure']))


@pytest.mark.parametrize('date',BRIGHT)
def test_ir02_complete_disclosure_cardinality_and_envelope_multiset(date):
    before=repair.predecessor()['daily'][date]
    after=repair.project_rows(before,date=date)
    held=next(r for r in after if r['identity_key']=='rid_5be18395526b0ff8b009')
    originals=[r for r in before if r['identity_key']in('rid_5be18395526b0ff8b009','rid_c6e5abb3b44d8783f05f')]
    assert len(originals)==2
    expected=sum((_bare_sources(r)for r in originals),Counter())
    assert _bare_sources(held)==expected
    assert held['source_disclosure_count']=='3'
    assert held['source_disclosure_count']==str(len(json.loads(held['source_disclosure'])))
    assert held['canonical_mt_ref']==held['canonical_lxx_ref']=='' and held['spans_json']=='[]'
    assert repair.restore_rows(after,date=date)==before


@pytest.mark.parametrize('date',BRIGHT)
def test_ir02_serialized_count_all_three_dates(date):
    rows=json.loads((ROOT/f'packages/lectionary-data/data/daily/lectionary-{date[:4]}.json').read_text())[date]
    held=next(r for r in rows if r['identity_key']=='rid_5be18395526b0ff8b009')
    assert held['source_disclosure_count']=='3'
    assert held['source_disclosure_count']==str(len(json.loads(held['source_disclosure'])))


def test_supplement_six_new_reverse_keys_and_literal_revelation_span():
    rows=repair.project_rows([])
    assert len(rows)==8
    rev=next(r for r in rows if r['identity_key']=='rid_5ec1f5c5b847553e2bfb')
    assert rev['canonical_mt_ref']==rev['canonical_lxx_ref']=='Rev 1-22'
    spans=json.loads(rev['spans_json'])
    assert len(spans)==1
    assert {k:spans[0][k]for k in('book','chapter_start','chapter_end','verse_start','verse_end')}==dict(book='Rev',chapter_start=1,chapter_end=22,verse_start=None,verse_end=None)


@pytest.mark.parametrize('date,count',[('2027-08-02',9),('2028-02-15',17)])
def test_supplement_serialized_bounded_ordinary_appointment_counts(date,count):
    rows=json.loads((ROOT/f'packages/lectionary-data/data/daily/lectionary-{date[:4]}.json').read_text())[date]
    assert len(rows)==count


@pytest.mark.parametrize('date',BRIGHT)
def test_bright_revelation_between_sixth_and_ninth_source_stages(date):
    menu=repair.supplement_plan()['bright_saturday']['source_menu_order']
    assert menu.index('Third and Sixth Hours')<menu.index('Revelation')<menu.index('Ninth Hour')
    original=repair.predecessor()['daily'][date]
    before=repair.project_base_rows(original,date=date)
    actual=repair.project_rows(original,date=date)
    sixth=[i for i,r in enumerate(actual)if r['service_section']=='6th Hour']
    ninth=[i for i,r in enumerate(actual)if r['service_section']=='9th Hour']
    revelation=[i for i,r in enumerate(actual)if r['service_section']=='Revelation']
    assert sixth and ninth and len(revelation)==1
    pos=revelation[0]
    assert max(sixth)<pos<min(ninth), 'Revelation must precede the complete Ninth Hour'
    assert max(actual[i]['service_order']for i in sixth)<actual[pos]['service_order']<min(actual[i]['service_order']for i in ninth)
    assert [r['reading_order']for r in actual]==list(range(1,len(actual)+1))
    added={'rid_5ec1f5c5b847553e2bfb','rid_34a83ab69dcba0a6fd3b','rid_ca4b57d664d6ae9fe6fc'}
    strip_order=lambda row:{k:v for k,v in row.items()if k!='reading_order'}
    assert [strip_order(r)for r in actual if r['identity_key']not in added]==[strip_order(r)for r in before]
    assert repair.restore_rows(actual,date=date)==original


@pytest.fixture(scope='module')
def serialized():
    reverse=[json.loads(l)for l in(ROOT/'packages/lectionary-data/data/reverse_lectionary_index.jsonl').read_text().splitlines()]
    daily={str(y):json.loads((ROOT/f'packages/lectionary-data/data/daily/lectionary-{y}.json').read_text())for y in(2026,2027,2028)}
    from holy_week_successor_fixture import reverse_1_3_11, daily_1_3_11
    reverse = reverse_1_3_11(reverse)
    daily = {y: {d: daily_1_3_11(rows, d) for d, rows in days.items()} for y, days in daily.items()}
    return reverse,daily


def test_cumulative_independent_multiset_and_no_predecessor_loss(serialized):
    reverse,_=serialized
    assert repair.verify_successor_membership(reverse)=={'row_count':12299,'distinct_keys':12174}
    original=repair.restore_rows(reverse)
    assert len(original)==12291
    assert repair.project_rows(original)==reverse
    with pytest.raises(ValueError,match='membership/multiplicity'):
        repair.verify_successor_membership(reverse[:-1]+[reverse[0]])


@pytest.mark.parametrize('date',sorted(repair.SUPPLEMENT_DATES))
def test_complete_daily_first_projection_inverse_and_literal_order(serialized,date):
    _,daily=serialized;actual=daily[date[:4]][date]
    before=repair.restore_rows(actual,date=date)
    assert repair.project_rows(before,date=date)==actual
    assert repair.project_rows(actual,date=date)==actual
    if date in BRIGHT:
        assert [r['display_ref']for r in actual if r['service_section']=='Distribution']==['Psalm 68: 1','Lk 24:1-12']
        assert len([r for r in actual if r['service_section']=='Revelation'])==1
        sixth=[i for i,r in enumerate(actual)if r['service_section']=='6th Hour']
        ninth=[i for i,r in enumerate(actual)if r['service_section']=='9th Hour']
        revelation=next(i for i,r in enumerate(actual)if r['service_section']=='Revelation')
        assert sixth and ninth and max(sixth)<revelation<min(ninth)
        assert actual[max(sixth)]['service_order']<actual[revelation]['service_order']<actual[min(ninth)]['service_order']
    else:
        p=repair.supplement_plan();s=repair._supplement_json(repair.supplement_inputs()['selectors'])
        group=p['joseph_2027'if date=='2027-08-02'else'amshir7_2028']
        assert [r['identity_key']for r in actual]==[d['tuple'][0]for d in group['complete_expected_order']]
        assert len(before)==(11 if date=='2027-08-02'else 8)
        if date=='2027-08-02':
            holds=[r for r in actual if r['identity_key']in repair.SUPPLEMENT_IDS]
            assert len(holds)==3
            assert [r['source_selected_english']for r in holds]==[a['selected_english']for a in group['additional_source_only_psalm_witnesses']]
        else:
            assert all(r['source_family']=='katameros_cycle'for r in actual)
            proof=json.loads(actual[0][repair.SUPPLEMENT_MARKER])
            assert proof['retained_context']['clock']=='2:00 PM'
            assert proof['exact_2028_reader_confirmation']is False
            assert all(d['sourceProbe']is True and d['reusedImmutableEvidence']is True for d in proof['source_documents'])


@pytest.mark.parametrize('field,value',[
 ('source_family','FORGED'),('source_kind','FORGED'),('calendar_keys','FORGED'),
 ('source_disclosure','[]'),('current_status','historical_witness'),('active',False),
 ('slot_order',True),('slot_order',1.0),('spans_json','[{"book":"Ps","chapter_start":68}]'),
 ('canonical_mt_ref','Ps 68:1'),('source_only_selection_json','{}')])
def test_real_composed_reverse_hold_mutations_refused(serialized,field,value):
    from scripts.review_release_contract import followup_reverse_view
    rows=copy.deepcopy(serialized[0])
    target=next(r for r in rows if r['identity_key']=='rid_34a83ab69dcba0a6fd3b')
    target[field]=value
    with pytest.raises(ValueError,match='final site review'):
        followup_reverse_view(rows,version='1.3.11')


@pytest.mark.parametrize('ident',['rid_34a83ab69dcba0a6fd3b','rid_753be171aee9fe41026f','rid_8685f027ac3abc3243e1','rid_7b2fb603c3595c6509f6'])
def test_each_hold_marker_stripping_still_refused_by_identity(serialized,ident):
    from scripts.review_release_contract import followup_reverse_view
    rows=copy.deepcopy(serialized[0]);target=next(r for r in rows if r['identity_key']==ident)
    target.pop(repair.SUPPLEMENT_MARKER);target.pop('source_only_selection_json')
    target['source_disclosure']='[]'
    with pytest.raises(ValueError,match='final site review'):
        followup_reverse_view(rows,version='1.3.11')


@pytest.mark.parametrize('date',['2026-04-11','2027-08-02','2028-02-15'])
def test_real_composed_daily_wrong_type_lifecycle_and_date_refused(serialized,date):
    from scripts.review_release_contract import followup_daily_view
    rows=serialized[1][date[:4]][date]
    for field,value in [('reading_order',True),('reading_order',1.0),('active',False),('source_kind','FORGED')]:
        bad=copy.deepcopy(rows);bad[-1][field]=value
        with pytest.raises(ValueError,match='final site review'):
            followup_daily_view({date:bad},version='1.3.11')
    with pytest.raises(ValueError,match='wrong daily date'):
        followup_daily_view({'2029-01-01':rows},version='1.3.11')


def test_revelation_wrong_reference_and_endpoints_refused(serialized):
    from scripts.review_release_contract import followup_reverse_view
    for mutation in ('reference','endpoints','split'):
        rows=copy.deepcopy(serialized[0]);r=next(r for r in rows if r['identity_key']=='rid_5ec1f5c5b847553e2bfb')
        if mutation=='reference':r['canonical_mt_ref']='Rev 1:1-22:21'
        else:
            spans=json.loads(r['spans_json'])
            if mutation=='endpoints':spans[0].update(verse_start=1,verse_end=21)
            else:spans=[dict(spans[0],chapter_start=i,chapter_end=i)for i in range(1,23)]
            r['spans_json']=json.dumps(spans)
        with pytest.raises(ValueError,match='final site review'):
            followup_reverse_view(rows,version='1.3.11')


def test_actual_composed_release_control_and_source_auth_failure(serialized,monkeypatch):
    from scripts.apply_review_repairs import project
    import site_review_repairs as site
    reverse,daily=serialized
    original_reverse=site.restore_rows(repair.restore_rows(reverse))
    original_daily={y:{d:site.restore_rows(repair.restore_rows(rows,date=d),date=d)for d,rows in days.items()}for y,days in daily.items()}
    payload={'rows':original_reverse,'daily_by_year':original_daily}
    output=project('release',payload)
    from holy_week_successor_fixture import reverse_1_3_11, daily_1_3_11
    output['rows'] = reverse_1_3_11(output['rows'])
    output['daily_by_year'] = {y: {d: daily_1_3_11(rows, d) for d, rows in days.items()} for y, days in output['daily_by_year'].items()}
    assert output['rows']==reverse and output['daily_by_year']==daily
    def refuse():raise ValueError('supplement injected source authentication failure')
    monkeypatch.setattr(repair,'authenticate_supplement_sources',refuse)
    with pytest.raises(ValueError,match='supplement injected source'):
        project('release',payload)
    from scripts.review_release_contract import followup_reverse_view,followup_daily_view
    with pytest.raises(ValueError,match='supplement injected source'):
        followup_reverse_view(reverse,version='1.3.11')
    with pytest.raises(ValueError,match='supplement injected source'):
        followup_daily_view({'2026-04-11':daily['2026']['2026-04-11']},version='1.3.11')



def test_joseph_new_psalm_witnesses_keep_their_own_commemoration_not_bright_template():
    p=repair.supplement_plan()
    rows=[r for r in repair.project_rows([])if r['source_kind']=='retained_reader_dated_psalm_selection']
    assert len(rows)==3
    assert all(r['day_titles']==p['joseph_2027']['context']['commemoration']for r in rows)
