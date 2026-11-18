"""The daily producer must authenticate the actual reverse input groups."""
import copy
import json
from pathlib import Path
import pytest
import site_review_repairs as repair


def complete_slice():
    b=repair.baseline()
    return [d['original'] for d in b['reverse_annotations']] + [r for group in b['waters_groups'].values() for r in group]

@pytest.mark.parametrize('mutation',[
    {'source_family':'forged'},{'source_kind':'forged'},{'calendar_keys':'forged'},
    {'service_section':'Liturgy'},{'slot':'Gospel'},{'canonical_mt_ref':'Ezek 36:25-29'},
    {'current_status':'historical_witness'},{'active':False},{'source_disclosure':'[]'}])
def test_actual_reverse_input_waters_group_must_qualify_before_daily_materialization(mutation):
    before=complete_slice()
    assert repair.restore_rows(repair.project_rows(before))==before
    bad=copy.deepcopy(before)
    next(r for r in bad if r['source_family']=='liturgy_of_the_waters').update(mutation)
    with pytest.raises(ValueError,match='site review waters'):
        repair.project_rows(bad)


def test_actual_reverse_input_waters_missing_or_duplicate_refused():
    before=complete_slice()
    assert repair.restore_rows(repair.project_rows(before))==before
    for bad in (before[:-1],before+[copy.deepcopy(before[-1])]):
        with pytest.raises(ValueError,match='site review waters'):
            repair.project_rows(bad)


def test_real_complete_composed_reverse_caller_refuses_same_total_waters_substitution():
    from scripts.review_release_contract import followup_reverse_view
    package=Path(__file__).resolve().parents[1]/'packages/lectionary-data'
    rows=[json.loads(l)for l in (package/'data/reverse_lectionary_index.jsonl').read_text().splitlines()]
    from holy_week_successor_fixture import reverse_1_3_11
    rows = reverse_1_3_11(rows)
    assert len(followup_reverse_view(rows,version='1.3.11'))>12000
    bad=copy.deepcopy(rows)
    next(r for r in bad if r['source_family']=='liturgy_of_the_waters' and r['canonical_mt_ref']=='Ezek 36:24-29')['canonical_mt_ref']='Ezek 36:25-29'
    with pytest.raises(ValueError,match='site review waters'):
        followup_reverse_view(bad,version='1.3.11')
