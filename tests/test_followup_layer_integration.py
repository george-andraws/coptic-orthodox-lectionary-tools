"""Real source-bound composition, including hostile serialized follow-up input."""
import copy
import pytest
import metadata_followup_repairs as metadata
import mark_followup_repairs as mark
from scripts import apply_review_repairs as builder
from scripts import review_release_contract as contract


@pytest.fixture(scope='module')
def successor():
    frozen = metadata.baseline()
    daily = {}
    for year, days in frozen['daily'].items():
        daily[year] = builder.finish_daily(mark.repair_daily(copy.deepcopy(days)))
    rows = builder.project('occurrence', {'rows': mark.repair_rows(copy.deepcopy(frozen['reverse_rows'])),
                                         'daily_by_year': daily})['rows']
    return frozen, rows, daily


def test_real_followup_composition_recovers_exact_historical_views(successor):
    frozen, rows, daily = successor
    restored = contract.followup_reverse_view(rows)
    # Mark's independent layer adds four new inactive candidates.
    assert len(restored) == len(frozen['reverse_rows']) + 4
    assert len(rows) == 12282
    for year, days in daily.items():
        old = contract.followup_daily_view(days)
        old = mark.restore_predecessor_for_comparison(old, int(year))
        assert old == frozen['daily'][year]


@pytest.mark.parametrize('field,value', [('display_label', 'forged'), ('normalized_season', 'forged'),
                                         ('source_locator', 'forged')])
def test_serialized_metadata_forgery_rejected_by_real_boundary(successor, field, value):
    _, rows, _ = successor
    bad = copy.deepcopy(rows)
    target = next(r for r in bad if r.get('normalized_season'))
    target[field] = value
    with pytest.raises(ValueError):
        contract.followup_reverse_view(bad)


def test_decoder_is_not_evidence_authority(successor):
    _, rows, _ = successor
    bad = copy.deepcopy(rows)
    target = next(r for r in bad if r.get('evidence_json'))
    target['evidence_json'] = target['evidence_json'].replace('1.3.7', 'forged')
    with pytest.raises(ValueError, match='evidence'):
        contract.followup_reverse_view(bad)


def test_psalm_annotation_inverse_rejects_fabricated_coordinates(successor):
    _, _, daily = successor
    bad = copy.deepcopy(daily['2026'])
    target = next(r for r in bad['2026-05-23'] if r.get('psalm_annotation_review_json'))
    target['canonical_lxx_ref'] = 'Ps 50:99'
    with pytest.raises(ValueError, match='annotation'):
        contract.followup_daily_view(bad)
