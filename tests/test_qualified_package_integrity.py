"""Source-qualified package bounds and public lifecycle regression controls."""
import copy
import json
from pathlib import Path

import pytest

from scripts import verify_package_integrity as v
import bright_saturday_composite_supplements as bright
import covenant_thursday_source_supplements as covenant
import build_design_deliverables as design

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def qualified_rows():
    # Source-derived fixtures, never refreshed from candidate output. No global gate
    # bypass: only this bounded fixture's final whole-corpus membership gate is isolated.
    presentation, _ = design.build_reverse_presentation(
        bright.load_bright_composite_rows() + [r for r in covenant.load_covenant_thursday_rows()
                                               if not r['normalized_ref']])
    from unittest.mock import patch
    with patch.object(design, 'verify_reverse_index_contract'):
        rows, _ = design.build_reverse_lectionary_index(presentation)
    assert len(rows) == 6
    return rows


@pytest.mark.parametrize('index', range(6))
def test_source_authenticated_empty_coordinates_are_accepted(qualified_rows, index):
    assert v.validate_row_reference_bounds(qualified_rows[index])['failures'] == []


def mutate(row, field):
    row = copy.deepcopy(row)
    if field in {'source_disclosure', 'provenance'}:
        row[field] = '[]' if field == 'source_disclosure' else '{}'
    elif field in {'canonical_mt_ref', 'canonical_lxx_ref'}:
        row[field] = 'Ps 1:1'
    elif field == 'spans_json':
        row[field] = json.dumps([dict(book='Jn', chapter_start=1, chapter_end=1, verse_start=1, verse_end=2)])
    elif field == 'top_approval':
        row['runtime_activation_approved'] = True
    elif field == 'approval':
        disclosure = json.loads(row['source_disclosure'])
        key = 'bright_composite_source' if row['source_kind'] == bright.SOURCE_KIND else 'covenant_thursday_source'
        disclosure[0][key][0]['runtime_activation_approved'] = True
        row['source_disclosure'] = json.dumps(disclosure)
    elif field in {'body', 'sha', 'source_context'}:
        disclosure = json.loads(row['source_disclosure'])
        key = 'bright_composite_source' if row['source_kind'] == bright.SOURCE_KIND else 'covenant_thursday_source'
        target = disclosure[0][key][0]
        target[{'body': 'body_literal', 'sha': 'contract_sha256', 'source_context': 'service_section'}[field]] = 'forged'
        row['source_disclosure'] = json.dumps(disclosure)
    else:
        row[field] = {'current_status': 'current_confirmed_coptic_reader', 'removed_marker': 'removed_by_fake',
                      'active': False, 'source_kind': 'forged', 'source_family': 'forged',
                      'service_section': 'Vespers', 'service_hour': 'Vespers', 'occasion': 'Monday',
                      'slot': 'Gospel', 'identity_key': 'forged', 'source_locator': 'forged',
                      'display_ref': 'Jn 1:1-2'}[field]
    return row


@pytest.mark.parametrize('index', range(6))
@pytest.mark.parametrize('field', ['source_disclosure', 'provenance', 'canonical_mt_ref', 'canonical_lxx_ref',
                                  'spans_json', 'approval', 'top_approval', 'body', 'sha', 'source_context', 'current_status',
                                  'removed_marker', 'active', 'source_kind', 'source_family', 'service_section',
                                  'service_hour', 'occasion', 'slot', 'identity_key', 'source_locator', 'display_ref'])
def test_qualified_exception_rejects_mutations(qualified_rows, index, field):
    assert v.validate_row_reference_bounds(mutate(qualified_rows[index], field))['failures']


@pytest.mark.parametrize('index', range(6))
def test_source_derived_daily_transport(qualified_rows, index):
    row = copy.deepcopy(qualified_rows[index])
    row.update(reading_order=1, source_order=int(row['source_order']), source_token_order=int(row['source_token_order']))
    disclosure = json.loads(row['source_disclosure'])
    row['source_disclosure'] = json.dumps([dict(disclosure[0], attested_year_min='2026', attested_year_max='2026'), disclosure[0]])
    row['source_disclosure_count'] = '2'
    date = '2026-04-11' if row['source_kind'] == bright.SOURCE_KIND else '2026-04-09'
    if row['source_kind'] != bright.SOURCE_KIND:
        row.pop('provenance')  # Actual npm Covenant daily shape; body stays in witnesses.
    assert not v.validate_row_reference_bounds(row, date_key=date)['failures']
    for field in ['approval', 'body', 'sha', 'source_context', 'source_disclosure', 'spans_json', 'canonical_mt_ref']:
        assert v.validate_row_reference_bounds(mutate(row, field), date_key=date)['failures'], field


def test_daily_date_is_bounded_to_authenticated_structural_recurrence(qualified_rows):
    for row in qualified_rows:
        assert v.validate_row_reference_bounds(row, date_key='2026-01-01')['failures']
        date = '2026-04-11' if row['source_kind'] == bright.SOURCE_KIND else '2026-04-09'
        assert not v.validate_row_reference_bounds(row, date_key=date)['failures']


@pytest.mark.parametrize('family', ['bright', 'covenant'])
def test_evidence_authentication_failure_is_closed_at_verifier(qualified_rows, monkeypatch, family):
    def refuse(*args, **kwargs):
        raise ValueError('injected source authentication failure')
    if family == 'bright':
        monkeypatch.setattr(bright, 'authenticate_bright_composite_evidence', refuse)
        row = next(r for r in qualified_rows if r['source_kind'] == bright.SOURCE_KIND)
    else:
        monkeypatch.setattr(covenant, 'load_covenant_thursday_contract', refuse)
        row = next(r for r in qualified_rows if r['source_kind'] == covenant.SOURCE_KIND)
    assert v.validate_row_reference_bounds(row)['failures']


def test_package_entrypoint_rejects_inactive_qualified_lifecycle(monkeypatch):
    original = v.parse_jsonl
    rows = original(v.PACKAGE_DIR / 'data/reverse_lectionary_index.jsonl')
    row = next(row for row in rows if row['source_kind'] == bright.SOURCE_KIND)
    row['current_status'] = 'historical_witness'
    monkeypatch.setattr(v, 'parse_jsonl', lambda path: rows if path.name == 'reverse_lectionary_index.jsonl' else original(path))
    result = v.validate_package_integrity(v.PACKAGE_DIR)
    assert any(f['reason'] == 'invalid_current_reverse_span' and f['display_ref'] == row['display_ref']
               for f in result['failures'])


def test_ordinary_empty_scripture_still_fails():
    assert v.validate_row_reference_bounds(dict(reading_type='scripture', display_ref='Ps 1:1', spans_json='[]'))['failures']


def competitors():
    base = dict(occasion='Good Friday', service_section='Sixth Hour', service_hour='Sixth Hour',
                slot='Psalm', slot_type='psalm', current_status='current_public_or_local_reference', removed_marker='')
    return [dict(base, source_family='holy_pascha', display_ref='Ps 1:1-3', spans_json=json.dumps([
        dict(book='Ps', chapter_start=1, chapter_end=1, verse_start=1, verse_end=3)])),
            dict(base, source_family='holy_pascha_curated_day_hour', display_ref='Ps 1:1-2', spans_json=json.dumps([
                dict(book='Ps', chapter_start=1, chapter_end=1, verse_start=1, verse_end=2)]))]


@pytest.mark.parametrize('inactive', [dict(current_status='historical_witness'), dict(current_status='historical_candidate_removed'),
                                     dict(active=False), dict(status='removed'), dict(current_status='superseded_by_source'),
                                     dict(removed_marker='removed_by_source')])
def test_historical_competitor_is_not_eligible_and_is_retained(inactive):
    rows = competitors()
    rows[0].update(inactive)
    before = copy.deepcopy(rows)
    assert v.detect_context_passage_conflicts(rows) == []
    assert rows == before


def test_active_conflict_positive_control():
    assert len(v.detect_context_passage_conflicts(competitors())) == 1


def test_unknown_explicit_status_refused():
    rows = competitors()
    rows[0]['current_status'] = 'current_unreviewed_forgery'
    with pytest.raises(ValueError, match='Unknown explicit reading status'):
        v.detect_context_passage_conflicts(rows)
