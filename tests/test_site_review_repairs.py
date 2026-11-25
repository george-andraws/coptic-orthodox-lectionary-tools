"""Independent literal service/edition expectations for the 1.3.11 candidate."""
import copy
import gzip
import json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'packages/lectionary-data'
SOURCE=ROOT/'sources/site-review-1.3.11'

def frozen():
    return json.loads(gzip.decompress((SOURCE/'published-1.3.10-targets.json.gz').read_bytes()))

def reverse_slice(b):
    return [x['original'] for x in b['reverse_annotations']] + [r for group in b['waters_groups'].values() for r in group]


def test_serialized_psalm_title_seam_and_partial_clause_repairs():
    rows=[json.loads(line) for line in (PACKAGE/'data/reverse_lectionary_index.jsonl').read_text().splitlines()]
    from holy_week_successor_fixture import reverse_1_3_11
    # Authenticate/undo the successor before applying this 160-row historical
    # oracle; the new Bright Saturday annotation is tested in its own domain.
    rows = reverse_1_3_11(rows)
    # These are distinct exact-context witnesses, not a blanket verse offset.
    expected={'Ps 60:4-5':'Ps 59:6-7','Ps 60:7':'Ps 59:9-10',
              'Ps 19:4':'Ps 18:5-6','Ps 19:5':'Ps 18:6','Ps 80:1-3':'Ps 79:2-4'}
    selected=[r for r in rows if r.get('edition_psalm_covering_json')]
    assert selected, 'Missing edition-qualified covering annotations'
    for mt,lxx in expected.items():
        found=[r for r in selected if r['canonical_mt_ref']==mt]
        assert found, mt
        assert all(r['canonical_lxx_ref']==lxx for r in found)
        assert all(json.loads(r['edition_psalm_covering_json'])['whole_verse_equivalence'] is False for r in found)
    assert len(selected)==160

@pytest.mark.parametrize('date,expected',[
    ('2026-01-19',['Hab 3:2-19','Isa 35:1-2','Isa 40:1-5','Isa 9:1-2','Bar 3:36-4:4','Ezek 36:24-29','Ezek 47:1-9','1Cor 10:1-13','Ps 114:3','Ps 114:5','Matt 3:1-17']),
    ('2027-01-19',['Hab 3:2-19','Isa 35:1-2','Isa 40:1-5','Isa 9:1-2','Bar 3:36-4:4','Ezek 36:24-29','Ezek 47:1-9','1Cor 10:1-13','Ps 114:3','Ps 114:5','Matt 3:1-17']),
    ('2028-01-20',['Hab 3:2-19','Isa 35:1-2','Isa 40:1-5','Isa 9:1-2','Bar 3:36-4:4','Ezek 36:24-29','Ezek 47:1-9','1Cor 10:1-13','Ps 114:3','Ps 114:5','Matt 3:1-17']),
    ('2026-07-12',['Exod 15:22-16:1','Exod 30:17-30','Isa 1:16-26','Isa 35:1-10','Isa 43:16-44:6','Zech 8:7-19','Zech 14:8-11','Heb 10:22-38','Ps 51:7','Ps 51:10','Jn 5:1-18']),
    ('2027-07-12',['Exod 15:22-16:1','Exod 30:17-30','Isa 1:16-26','Isa 35:1-10','Isa 43:16-44:6','Zech 8:7-19','Zech 14:8-11','Heb 10:22-38','Ps 51:7','Ps 51:10','Jn 5:1-18']),
    ('2028-07-12',['Exod 15:22-16:1','Exod 30:17-30','Isa 1:16-26','Isa 35:1-10','Isa 43:16-44:6','Zech 8:7-19','Zech 14:8-11','Heb 10:22-38','Ps 51:7','Ps 51:10','Jn 5:1-18']),
])
def test_serialized_complete_waters_group_preserves_ordinary_services(date,expected):
    days=json.loads((PACKAGE/f'data/daily/lectionary-{date[:4]}.json').read_text())
    rows=days[date]
    waters=[r for r in rows if r['source_family']=='liturgy_of_the_waters']
    assert [r['canonical_mt_ref']for r in waters]==expected
    ordinary=[{k:v for k,v in r.items()if k!='reading_order'} for r in rows if r not in waters]
    before=[{k:v for k,v in r.items()if k!='reading_order'} for r in frozen()['waters_daily_predecessors'][date]]
    # Annotation-only changes on ordinary Psalms are tested separately.
    assert [r['identity_key']for r in ordinary]==[r['identity_key']for r in before]
    assert [r['reading_order']for r in rows]==list(range(1,len(rows)+1))
    assert all(r['current_status']=='current_public_or_local_reference' for r in waters)


def test_exact_context_projection_and_inverse_roundtrip():
    import site_review_repairs as repair
    b=frozen(); reverse=reverse_slice(b)
    assert repair.restore_rows(repair.project_rows(reverse))==reverse
    for date,rows in b['daily_annotations'].items():
        if date not in b['waters_dates']:
            assert repair.restore_rows(repair.project_rows(rows,date=date),date=date)==rows
    for date,rows in b['waters_daily_predecessors'].items():
        after=repair.project_rows(rows,date=date)
        assert repair.restore_rows(after,date=date)==rows
        assert repair.project_rows(after,date=date)==after

@pytest.mark.parametrize('field,value',[
    ('source_family','forged'),('source_kind','forged'),('occasion','forged'),
    ('calendar_keys','forged'),('source_locator','forged'),('source_disclosure','[]'),
    ('canonical_mt_ref','Ps 1:1'),('spans_json','[]'),('active',True),('status',True),
    ('current_status','current_confirmed_coptic_reader'),('edition_psalm_covering_json','{}')])
def test_complete_reverse_control_then_real_inverse_rejects_mutations(field,value):
    import site_review_repairs as repair
    b=frozen(); before=reverse_slice(b)
    rows=repair.project_rows(before)
    assert repair.restore_rows(rows)==before
    bad=copy.deepcopy(rows); bad[0][field]=value
    with pytest.raises(ValueError,match='site review'):
        repair.restore_rows(bad)

@pytest.mark.parametrize('field,value',[
    ('source_family','forged'),('source_kind','forged'),('service_section','Liturgy'),
    ('service_hour','First Hour'),('slot','Gospel'),('source_locator','forged'),
    ('source_disclosure','[]'),('current_status','historical_witness'),('active',False),
    ('canonical_mt_ref','Ezek 36:25-29'),('service_order',True),('reading_order',1.0)])
def test_complete_daily_control_then_real_inverse_rejects_waters_mutations(field,value):
    import site_review_repairs as repair
    date='2026-01-19'; before=frozen()['waters_daily_predecessors'][date]
    rows=repair.project_rows(before,date=date)
    assert repair.restore_rows(rows,date=date)==before
    next(r for r in rows if r['source_family']=='liturgy_of_the_waters')[field]=value
    with pytest.raises(ValueError,match='site review'):
        repair.restore_rows(rows,date=date)


def test_compound_marker_stripping_and_wrong_date_refused():
    import site_review_repairs as repair
    date='2026-07-12'; before=frozen()['waters_daily_predecessors'][date]
    rows=repair.project_rows(before,date=date)
    with pytest.raises(ValueError,match='site review'):
        repair.restore_rows(rows,date='2026-07-13')
    target=next(r for r in rows if r['source_family']=='liturgy_of_the_waters')
    for field in ('source_family','source_kind','source_locator','source_disclosure','waters_materialization_json'):
        target.pop(field,None)
    with pytest.raises(ValueError,match='site review'):
        repair.restore_rows(rows,date=date)


def test_held_and_historical_coordinates_remain_byte_exact():
    import site_review_repairs as repair
    rows=[json.loads(line)for line in (PACKAGE/'data/reverse_lectionary_index.jsonl').read_text().splitlines()]
    for row in rows:
        if row.get('current_status')=='pending_psalm_equivalence_unresolved' or row.get('active') is False or row.get('removed_marker'):
            assert 'edition_psalm_covering_json' not in row
    # Unspecified Ps8, Psalm147 edition seam, and wrong-heading Toba30 remain held.
    assert not any(r.get('edition_psalm_covering_json') for r in rows if r['canonical_mt_ref'] in ('Ps 147:12','Ps 147:18','Ps 69:25-26'))
