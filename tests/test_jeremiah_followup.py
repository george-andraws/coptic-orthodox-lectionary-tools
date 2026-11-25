"""Literal Reader-priority successor expectations, not generated from repair rules."""
import copy
import json
from pathlib import Path
import pytest
from scripts.apply_review_repairs import project
from tests.test_holy_week_continuation import before_release
import holy_week_continuation as hw

ROOT = Path(__file__).resolve().parents[1]
THURSDAYS = ('2026-04-09', '2027-04-29', '2028-04-13')
FRIDAYS = ('2026-04-10', '2027-04-30', '2028-04-14')


def published():
    import gzip
    return json.loads(gzip.decompress((ROOT / 'tests/fixtures/jeremiah-published-1.3.12.json.gz').read_bytes()))


@pytest.fixture(scope='module')
def successor():
    package = ROOT / 'packages/lectionary-data/data'
    return {'rows': [json.loads(line) for line in (package / 'reverse_lectionary_index.jsonl').read_text().splitlines()],
            'daily_by_year': {str(year): json.loads((package / 'daily' / f'lectionary-{year}.json').read_text())
                              for year in (2026, 2027, 2028)}}


def current(row):
    return row.get('active') is not False and not row.get('removed_marker') and row.get('current_status') != 'historical_witness'


def group(rows, occasion, hour):
    return [r for r in rows if current(r) and r.get('occasion') == occasion and r.get('service_hour') == hour and r.get('slot_type') == 'prophecy']


def test_pk2_reader_exodus_not_invented_leviticus(successor):
    refs = [r['canonical_mt_ref'] for r in group(successor['rows'], 'Good Friday', 'Eleventh Hour')]
    assert refs == ['Exod 12:1-14']
    ninth = group(successor['rows'], 'Good Friday', 'Ninth Hour')
    assert any(r['canonical_mt_ref'] == 'Jer 11:18-12:13' for r in ninth)


def test_pk6_reader_start_and_sirach(successor):
    assert [r['canonical_mt_ref'] for r in group(successor['rows'], 'Great Thursday', 'Sixth Hour')] == ['Jer 7:1-15', 'Ezek 20:39-44', 'Sir 12:13-13:1']


def test_pk3_reader_and_specific_historical_service(successor):
    rows = successor['rows']
    selected = group(rows, 'Great Thursday Eve', 'Ninth Hour')
    assert [(r['canonical_mt_ref'], r['canonical_lxx_ref']) for r in selected] == [('Jer 9:7-11', 'Jer 9:6-10'), ('Ezek 21:33-37', 'Ezek 21:33-37')]
    ottawa = next(r for r in rows if r['identity_key'] == 'rid_000333f2b55f4f89b928')
    assert ottawa['pascha_service'] == 'eve_of_friday'
    assert ottawa['current_status'] == 'historical_witness'


def test_pk7_named_brenton_not_generic_offset(successor):
    row = next(r for r in successor['rows'] if r['identity_key'] == 'rid_fa44089aa2993cc17312')
    assert row['canonical_mt_ref'] == 'Ps 41:5,41:10'
    assert row['canonical_lxx_ref'] == 'Ps 40:6; Ps 40:11'
    assert 'Brenton covering locus' in row['display_ref']


def test_complete_daily_arrays_current_only_and_same_order(successor):
    for year, days in successor['daily_by_year'].items():
        for date, rows in days.items():
            assert all(current(r) for r in rows)
            assert [r['reading_order'] for r in rows] == list(range(1, len(rows)+1))
    for date in THURSDAYS:
        rows = successor['daily_by_year'][date[:4]][date]
        assert [r['canonical_mt_ref'] for r in group(rows, 'Great Thursday', 'Sixth Hour')] == ['Jer 7:1-15', 'Ezek 20:39-44', 'Sir 12:13-13:1']
    for date in FRIDAYS:
        rows = successor['daily_by_year'][date[:4]][date]
        assert [r['canonical_mt_ref'] for r in group(rows, 'Good Friday', 'Eleventh Hour')] == ['Exod 12:1-14']
