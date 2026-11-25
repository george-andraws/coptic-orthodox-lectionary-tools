"""Mutation and complete-array checks at real producer/inverse boundaries."""
import ast
import copy
import csv
import hashlib
import json
from pathlib import Path
import tempfile
import pytest
import jeremiah_followup as repair
from scripts.apply_review_repairs import project

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def output():
    b = repair.predecessor()
    return project('jeremiah', {'rows': b['reverse'], 'daily_by_year': b['daily']})


def test_real_boundary_exact_corpus_inverse_and_replay(output):
    b = repair.predecessor()
    assert repair.restore_reverse(output['rows']) == b['reverse']
    assert repair.verify_membership(output['rows']) == dict(row_count=12308, predecessor_rows=12300, additions=8, removals=0)
    assert project('jeremiah', output) == output
    # A Reader Wednesday Sirach row shares Ottawa's reading identity; it is not
    # the historical Great-Thursday source and must remain byte-for-byte intact.
    original_wednesday = next(r for r in b['reverse'] if r['identity_key'] == repair.OTTAWA_SIR and r['source_family'] == 'coptic_reader')
    assert original_wednesday in output['rows']
    assert repair.project_daily([original_wednesday], '2026-04-08') == [original_wednesday]
    for year, days in output['daily_by_year'].items():
        for date, rows in days.items():
            assert repair.restore_daily(rows, date) == b['daily'][year][date]
    inactive = [r for r in output['rows'] if r.get('source_family') == 'katameros_api_jeremiah_variant']
    assert [(r['canonical_mt_ref'], r['active'], r['current_status']) for r in inactive] == [
        ('Exod 12:1-14', False, 'historical_witness'), ('Lev 23:5-12', False, 'historical_witness'),
        ('Jer 7:2-15', False, 'historical_witness'), ('Sir 12:13-13:1', False, 'historical_witness')]


@pytest.mark.parametrize('value', [True, 1.0])
@pytest.mark.parametrize('representation', ['reverse', 'daily'])
def test_predecessor_scalar_type_is_authenticated_before_projection(value, representation):
    before = repair.predecessor()
    rows = copy.deepcopy(before['reverse'] if representation == 'reverse' else before['daily']['2026']['2026-04-09'])
    target = next(r for r in rows if type(r.get('slot_order')) is int and r['slot_order'] == 1)
    target['slot_order'] = value
    with pytest.raises(ValueError, match='Jeremiah follow-up'):
        if representation == 'reverse':
            project('jeremiah', {'rows': rows, 'daily_by_year': {}})
        else:
            repair.project_daily(rows, '2026-04-09')


def test_successor_dispatch_restores_original_historical_contract(output):
    from scripts.review_release_contract import followup_reverse_view, followup_daily_view
    before = repair.predecessor()
    assert followup_reverse_view(output['rows'], version='1.3.13') == followup_reverse_view(before['reverse'], version='1.3.12')
    for year, days in output['daily_by_year'].items():
        assert followup_daily_view(days, version='1.3.13') == followup_daily_view(before['daily'][year], version='1.3.12')
    with pytest.raises(ValueError):
        followup_reverse_view(output['rows'], version='1.3.12')


@pytest.mark.parametrize('field,value', [
    ('source_family', 'wrong'), ('source_kind', 'wrong'), ('occasion', 'Monday'),
    ('service_hour', 'Third Hour'), ('slot', 'OT2'), ('canonical_mt_ref', 'Jer 7:2-15'),
    ('canonical_lxx_ref', 'Jer 7:2-15'), ('spans_json', '[]'),
    ('source_disclosure', '[]'), ('source_disclosure_count', 1),
    ('active', 1), ('active', 'true'), ('current_status', 'historical_witness'),
    ('reading_order', True), ('jeremiah_followup_json', '{}'),
])
def test_complete_day_mutation_refused_at_both_boundaries(output, field, value):
    rows = copy.deepcopy(output['daily_by_year']['2026']['2026-04-09'])
    target = next(r for r in rows if r.get('source_family') == 'coptic_reader_jeremiah_followup')
    target[field] = value
    for fn in (repair.restore_daily, repair.project_daily):
        with pytest.raises(ValueError, match='Jeremiah follow-up'):
            fn(rows, '2026-04-09')


def test_source_auth_failure_through_actual_producer_and_inverse(output, monkeypatch):
    def fail():
        raise ValueError('injected evidence authentication failure')
    monkeypatch.setattr(repair, 'authenticate', fail)
    with pytest.raises(ValueError, match='evidence authentication'):
        project('jeremiah', {'rows': repair.predecessor()['reverse'], 'daily_by_year': {}})
    with pytest.raises(ValueError, match='evidence authentication'):
        repair.restore_daily(output['daily_by_year']['2026']['2026-04-09'], '2026-04-09')


def test_stripped_inactive_original_and_same_total_membership_forgery(output):
    bad = copy.deepcopy(output['rows'])
    row = next(r for r in bad if r['identity_key'] == 'rid_0946df3427160b8ebe38')
    for key in (repair.MARKER, 'removed_marker', 'source_family', 'source_kind', 'active'):
        row.pop(key, None)
    row.update(current_status='current', source_disclosure='[]')
    with pytest.raises(ValueError, match='Jeremiah follow-up'):
        repair.verify_membership(bad)
    bad = output['rows'][:-1]+[output['rows'][0]]
    with pytest.raises(ValueError, match='Jeremiah follow-up'):
        repair.verify_membership(bad)


def test_wrong_date_and_stripped_identity_still_refused(output):
    rows = copy.deepcopy(output['daily_by_year']['2026']['2026-04-09'])
    for row in rows:
        if row.get(repair.MARKER):
            for key in (repair.MARKER, 'source_family', 'source_kind', 'source_disclosure'):
                row.pop(key, None)
    with pytest.raises(ValueError, match='wrong daily date'):
        repair.project_daily(rows, '2026-04-08')
    assert repair.project_daily([], '2026-02-01') == []


def test_jeremiah8_hold_and_other_historical_context_untouched(output):
    old = repair.predecessor()['reverse']
    by_id = {r['identity_key']: r for r in output['rows']}
    for row in old:
        if row['identity_key'] == 'rid_16337d9b7cbd88ba893e':
            assert by_id[row['identity_key']] == row
    sir = next(r for r in output['rows'] if r['identity_key'] == repair.OTTAWA_SIR)
    assert sir['canonical_mt_ref'] == 'Sir 23:7-14'
    assert sir['current_status'] == 'historical_witness'
    assert sir['pascha_service'] == 'great_thursday'
    assert json.loads(sir[repair.MARKER])['body_counterpart'] == 'Sir 12:13-13:1'


def _source_fixture(tmp_path):
    data = tmp_path / 'out/data'
    data.mkdir(parents=True)
    rows = list(csv.DictReader((ROOT / 'out/data/pascha_day_hour_index.csv').open()))
    policy = json.loads((ROOT/'sources/lectionary_corrections.json').read_text())
    policy['pascha_day_hour'] = [r for r in policy['pascha_day_hour'] if r.get('expected_source') == 'api']
    paths = {r['source_path'] for r in policy['pascha_day_hour']}
    policy['source_fingerprints'] = {p: policy['source_fingerprints'][p] for p in paths}
    for path in paths:
        dest = tmp_path / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((ROOT/path).read_bytes())
    (tmp_path/'sources/lectionary_corrections.json').write_text(json.dumps(policy))
    def write_csv(path, items, fields):
        with path.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(items)
    def write_jsonl(path, items):
        path.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in items))
    write_csv(data/'pascha_day_hour_index.csv', rows, list(rows[0]))
    fn = next(n for n in ast.parse((ROOT/'build_lectionary_reference.py').read_text()).body
              if isinstance(n, ast.FunctionDef) and n.name == 'apply_lectionary_corrections')
    namespace = dict(WORK=tmp_path, DATA=data, csv=csv, json=json, write_csv=write_csv,
                     write_jsonl=write_jsonl, sha256=lambda p: hashlib.sha256(p.read_bytes()).hexdigest())
    exec(compile(ast.Module(body=[fn], type_ignores=[]), 'build_lectionary_reference.py', 'exec'), namespace)
    return data, rows, write_csv, namespace['apply_lectionary_corrections']


def test_real_source_function_four_literal_deltas_and_both_exports(tmp_path):
    data, before, write_csv, run = _source_fixture(tmp_path)
    run()
    after = list(csv.DictReader((data/'pascha_day_hour_index.csv').open()))
    assert after == [json.loads(line) for line in (data/'pascha_day_hour_index.jsonl').read_text().splitlines()]
    changes = [(a['day'], a['hour'], a['slot'], a['refs'], b['refs']) for a,b in zip(before, after) if a != b]
    assert changes == [('Great Thursday', 'Sixth Hour', 'OT1', 'Exod 7:2-15', 'Jer 7:2-15'),
                       ('Great Thursday', 'Sixth Hour', 'OT3', 'Wis 12:13-13:1', 'Sir 12:13-13:1'),
                       ('Good Friday', 'Eleventh Hour', 'OT1', 'Jer 12:1-14', 'Exod 12:1-14'),
                       ('Good Friday', 'Eleventh Hour', 'OT2', 'Isa 3:5-12', 'Lev 23:5-12')]
    assert len(after) == len(before) == 172
    raw = (data/'pascha_day_hour_index.csv').read_bytes()
    run()
    assert (data/'pascha_day_hour_index.csv').read_bytes() == raw


@pytest.mark.parametrize('field,value', [('source', 'printed'), ('day', 'Monday'), ('hour', 'Ninth Hour'), ('slot', 'OT2'), ('refs', 'Exod 7:2-14')])
def test_real_source_selector_rejects_context_and_source_before_writes(tmp_path, field, value):
    data, rows, write_csv, run = _source_fixture(tmp_path)
    target = next(r for r in rows if r['day'] == 'Great Thursday' and r['hour'] == 'Sixth Hour' and r['slot'] == 'OT1')
    target[field] = value
    write_csv(data/'pascha_day_hour_index.csv', rows, list(rows[0]))
    raw = (data/'pascha_day_hour_index.csv').read_bytes()
    with pytest.raises(RuntimeError, match='drift or ambiguous'):
        run()
    assert (data/'pascha_day_hour_index.csv').read_bytes() == raw
    assert not (data/'pascha_day_hour_index.jsonl').exists()
