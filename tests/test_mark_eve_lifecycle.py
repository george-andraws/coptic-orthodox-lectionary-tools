"""Current-hour coverage must not count archived or explicitly inactive rows."""
import copy
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mark_followup_repairs as followup


def valid_days():
    return followup.repair_daily(copy.deepcopy(followup.baseline()['daily']['2026']))


def test_eve_coverage_valid_current_and_explicit_held_hours():
    coverage = followup.validate_eve_coverage(valid_days(), 2026)
    assert len(coverage) == 25
    assert sum(row['coverage'] == 'current' for row in coverage) == 19
    assert sum(row['coverage'] == 'held_missing_reader' for row in coverage) == 6


@pytest.mark.parametrize('lifecycle', [
    {'active': False},
    {'status': 'removed'},
    {'current_status': 'historical_witness'},
    {'removed_marker': 'superseded_by_canonical_occurrence_projection'},
])
def test_inactive_sixth_hour_does_not_satisfy_current_coverage(lifecycle):
    days = valid_days()
    selected = [row for row in days['2026-04-07']
                if row.get('pascha_service') == 'eve_of_wednesday'
                and row.get('service_hour') == 'Sixth Hour']
    assert selected
    for row in selected:
        row.update(lifecycle)
    with pytest.raises(ValueError, match='five-hour coverage drift'):
        followup.validate_eve_coverage(days, 2026)
