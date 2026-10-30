"""LK5 fixed historical witnesses, not candidate-derived membership."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

import pytest
import composite_followup_repairs as repairs
import resolver_review_repairs as resolver

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'docs/reviews/luke-composites-1.3.8/published-1.3.7-composite-witnesses.json'


def witnesses():
    return [r for g in json.loads(FIXTURE.read_text())['groups'] for r in g]


def test_published_52_inactive_pairs_become_ordered_inactive_appointments_without_loss():
    original = witnesses()
    saved = copy.deepcopy(original)
    actual, events = repairs.merge_remaining_composites(original)
    assert (len(actual), len(events)) == (52, 52)
    assert original == saved
    assert all(r['active'] is False and r['status'] == 'removed' for r in actual)
    assert all(r['removed_marker'] for r in actual)
    recovered = [f for r in actual for f in json.loads(r['composite_fragments_json'])]
    signature = lambda r: json.dumps(r, sort_keys=True)
    assert sorted(map(signature, recovered)) == sorted(map(signature, saved))
    for row in actual:
        fragments = json.loads(row['composite_fragments_json'])
        assert row['spans_json'] == json.dumps([s for f in fragments for s in json.loads(f['spans_json'])], sort_keys=True)
        assert repairs.qualify_archived_composite(row) == fragments
        assert row['provenance'] == 'katameros-api sqlite'
    assert repairs.merge_remaining_composites(actual) == (actual, [])


@pytest.mark.parametrize('field,value', [
    ('source_locator', 'forged'), ('calendar_keys', 'Abib 13'),
    ('source_family', 'other'), ('source_kind', 'other'),
    ('service_section', 'Vespers'), ('slot', 'Gospel'),
    ('active', True), ('removed_marker', ''), ('current_status', 'current_confirmed_coptic_reader'),
    ('spans_json', '[]'), ('source_disclosure', '[]'),
])
def test_recognized_fragment_mutations_fail_closed(field, value):
    rows = witnesses()
    rows[0][field] = value
    with pytest.raises(ValueError, match='LK5.*witness'):
        repairs.merge_remaining_composites(rows)


def test_incomplete_and_duplicate_pair_are_rejected_not_silently_partial():
    rows = witnesses()
    for changed in [rows[1:], rows + [rows[0]]]:
        with pytest.raises(ValueError, match='LK5.*(incomplete|duplicate)'):
            repairs.merge_remaining_composites(changed)


def test_source_authentication_failure_reaches_real_merge():
    with patch.object(resolver, '_db_records', side_effect=ValueError('SQLite source drift')):
        with pytest.raises(ValueError, match='source drift'):
            repairs.merge_remaining_composites(witnesses())


def test_merged_evidence_lifecycle_and_disclosure_mutations_are_rejected():
    rows, _ = repairs.merge_remaining_composites(witnesses())
    for field, value in [('active', True), ('source_disclosure', '[]'),
                         ('spans_json', '[]'), ('composite_fragments_json', '[]')]:
        with pytest.raises(ValueError, match='LK5'):
            repairs.qualify_archived_composite(dict(rows[0], **{field: value}))


def test_unrelated_history_is_unchanged_and_no_whole_corpus_guard_is_replaced():
    row = dict(witnesses()[0], source_locator='unrelated', identity_key='other', occasion='Other', calendar_keys='Other')
    assert repairs.merge_remaining_composites([row]) == ([row], [])


def test_known_lk2_label_projection_does_not_change_oracle_or_raw_source_fields():
    rows = witnesses()
    for row in rows:
        month, day = row['coptic_date_key'].rsplit('-', 1)
        row['display_label'] = month.capitalize() + ' ' + day
    actual, events = repairs.merge_remaining_composites(rows)
    assert len(events) == 52
    recovered = repairs.legacy_validation_rows(actual)
    signature = lambda row: json.dumps(row, sort_keys=True)
    assert sorted(map(signature, recovered)) == sorted(map(signature, rows))
    for row in actual:
        repairs.qualify_archived_composite(row)


def test_stripping_composite_marker_does_not_evade_exact_authentication():
    rows, _ = repairs.merge_remaining_composites(witnesses())
    del rows[0]['composite_review']
    with pytest.raises(ValueError, match='LK5'):
        repairs.legacy_validation_rows(rows)
