"""Literal source-plan controls; never derive expectations from candidate output."""
import copy
import json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('date', ['2026-02-16','2027-03-08','2028-02-21'])
def test_printed_first_monday_complete_service_and_inverse(date):
    import final_site_review_repairs as repair
    before=repair.predecessor()['daily'][date]
    after=repair.project_base_rows(before,date=date)
    liturgy=[r['canonical_mt_ref'] for r in after if r['service_section']=='Liturgy']
    assert liturgy==['Rom 1:26-2:7','James 2:1-13','Acts 14:19-28','Ps 22:26','Mark 9:33-50']
    assert [r['canonical_mt_ref'] for r in after if r['service_section']=='Matins' and r['slot_type']=='gospel']==['Matt 12:24-34']
    if date!='2026-02-16':
        assert [r['canonical_mt_ref'] for r in after if r['service_section']=='Matins'][:3]==['Exod 2:23-25','Exod 3:1-5','Isa 1:2-18']
        assert all(r['source_family']=='katameros_cycle' for r in after if r['service_section']=='Matins')
    assert [r for r in before if r['service_section']=='Vespers']==[dict(r,reading_order=before[i]['reading_order']) for i,r in enumerate(after[:2])]
    assert repair.restore_base_rows(after,date=date)==before
    assert repair.project_base_rows(after,date=date)==after

@pytest.mark.parametrize('date', ['2026-04-11','2027-05-01','2028-04-15'])
def test_bright_missing_appointments_and_complete_matins_order(date):
    import final_site_review_repairs as repair
    before=repair.predecessor()['daily'][date]
    after=repair.project_base_rows(before,date=date)
    assert [r['canonical_mt_ref'] for r in after if r['service_section']=='Matins']==['Eph 4:1-5','Isa 55:2-13','1Cor 5:7-13','Ps 88:4-5','','','Matt 27:62-66']
    midnight=[r for r in after if r['service_section']=='Midnight Praises']
    assert midnight[1]['canonical_mt_ref']=='Exod 15'
    assert json.loads(midnight[1]['spans_json'])[0]['verse_end'] is None
    assert len(after)==len(before)+1
    psalms=[r for r in after if r['service_section']=='Liturgy' and r['slot_type']=='psalm']
    assert len(psalms)==2
    assert json.loads(psalms[0]['source_selection_order_json'])['selected_verse_order']==[5,3]
    assert psalms[1]['identity_key']=='rid_5be18395526b0ff8b009'
    assert psalms[1]['canonical_mt_ref']==psalms[1]['canonical_lxx_ref']==''
    assert psalms[1]['spans_json']=='[]'
    assert any(s['source_family']=='holy_pascha_curated_day_hour' for s in json.loads(psalms[1]['source_disclosure']))
    assert repair.restore_base_rows(after,date=date)==before
    assert repair.project_base_rows(after,date=date)==after

@pytest.mark.parametrize('field,value', [('source_family','forged'),('source_kind','forged'),('calendar_keys','forged'),('service_section','Liturgy'),('source_disclosure','[]'),('canonical_mt_ref','1Cor 5:1-13'),('active',False),('slot_order',True)])
def test_real_inverse_qualifies_complete_control_then_rejects_mutations(field,value):
    import final_site_review_repairs as repair
    date='2026-04-11'; before=repair.predecessor()['daily'][date]
    after=repair.project_base_rows(before,date=date)
    assert repair.restore_base_rows(after,date=date)==before
    next(r for r in after if r['canonical_mt_ref']=='1Cor 5:7-13')[field]=value
    with pytest.raises(ValueError,match='final site review'):
        repair.restore_base_rows(after,date=date)


def test_reverse_added_tuple_membership_and_inverse():
    import final_site_review_repairs as repair
    after=repair.project_base_rows([])
    assert [r['canonical_mt_ref'] for r in after]==['1Cor 5:7-13','Exod 15']
    assert after[1]['slot_type']=='source_label_preserved'
    assert repair.restore_base_rows(after)==[]
    assert repair.project_base_rows(after)==after
    bad=copy.deepcopy(after)
    for key in ('source_family','source_kind','source_disclosure','source_locator','final_site_review_json'):
        bad[0].pop(key,None)
    with pytest.raises(ValueError,match='final site review'):
        repair.restore_base_rows(bad)


def test_source_authentication_failure_reaches_actual_projection(monkeypatch):
    import final_site_review_repairs as repair
    def fail(): raise ValueError('final site review source authentication failure')
    monkeypatch.setattr(repair,'authenticate_sources',fail)
    with pytest.raises(ValueError,match='authentication'):
        repair.project_base_rows([])
    with pytest.raises(ValueError,match='authentication'):
        repair.project_base_rows(repair.predecessor()['daily']['2026-02-16'],date='2026-02-16')


def test_wrong_date_and_daily_ordinal_mutations_refused():
    import final_site_review_repairs as repair
    rows=repair.project_base_rows(repair.predecessor()['daily']['2026-04-11'],date='2026-04-11')
    with pytest.raises(ValueError,match='final site review'):
        repair.restore_base_rows(rows,date='2026-04-12')
    rows[0]['reading_order']=True
    with pytest.raises(ValueError,match='final site review'):
        repair.restore_base_rows(rows,date='2026-04-11')


def test_seven_daily_presentation_alias_joins_are_independently_qualified():
    import final_site_review_repairs as repair
    p=repair.plan()
    assert len(p['additional_daily_annotation_joins'])==7
    for item in p['additional_daily_annotation_joins']:
        date=item['date']
        after=repair.project_base_rows(repair.predecessor()['daily'][date],date=date)
        row=next(r for r in after if r['identity_key']==item['original']['identity_key'] and r['source_locator']==item['original']['source_locator'])
        assert row['canonical_lxx_ref']==item['proof']['brenton_covering_ref']
        assert row['canonical_mt_ref']==item['original']['canonical_mt_ref']
        assert repair.restore_base_rows(after,date=date)==repair.predecessor()['daily'][date]


def test_complete_serialized_successor_matches_independent_multiset():
    import gzip
    from collections import Counter
    source=ROOT/'sources/site-review-1.3.11'
    data=json.loads(gzip.decompress((source/'approved-successor-context-keyset.json.gz').read_bytes()))
    rows=[json.loads(l) for l in (ROOT/'packages/lectionary-data/data/reverse_lectionary_index.jsonl').read_text().splitlines()]
    import final_site_review_repairs as repair
    rows=repair._supplement_restore(rows)
    actual=Counter(tuple(r.get(f,'')for f in data['fields'])for r in rows)
    # Stored independent keyset retains multiplicity; inspect declared schema.
    expected=Counter({tuple(x['key']):x['multiplicity'] for x in data['multiset']})
    assert actual==expected
    assert sum(actual.values())==12293
    import final_site_review_repairs as repair
    assert repair.verify_successor_membership(rows,stage='base')=={'row_count':12293,'distinct_keys':12168}
    with pytest.raises(ValueError,match='membership/multiplicity'):
        repair.verify_successor_membership(rows+[rows[0]],stage='base')
    with pytest.raises(ValueError,match='membership/multiplicity'):
        repair.verify_successor_membership(rows[1:]+[rows[2]],stage='base')
