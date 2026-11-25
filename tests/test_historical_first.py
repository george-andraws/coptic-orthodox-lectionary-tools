"""Collection-only scheduling controls, independent of lectionary assertions."""
from collections import Counter
from types import SimpleNamespace
import pytest

from conftest import HISTORICAL_FIRST, pytest_collection_modifyitems


def configuration(enabled=False, workers=0):
    options = dict(historical_first=enabled, numprocesses=workers)
    return SimpleNamespace(getoption=lambda name, default=None: options.get(name, default))


def test_default_collection_order_is_unchanged():
    items = [SimpleNamespace(nodeid=name) for name in reversed(HISTORICAL_FIRST)]
    original = list(items)
    pytest_collection_modifyitems(configuration(), items)
    assert items == original


def test_historical_lane_is_stable_and_never_drops_or_repeats_items():
    names = ['ordinary-a', HISTORICAL_FIRST[3], 'ordinary-b',
             *reversed(HISTORICAL_FIRST[:3]), 'ordinary-a', HISTORICAL_FIRST[4]]
    items = [SimpleNamespace(nodeid=name) for name in names]
    original_ids = Counter(map(id, items))
    pytest_collection_modifyitems(configuration(enabled=True), items)
    assert [item.nodeid for item in items] == [*HISTORICAL_FIRST, 'ordinary-a', 'ordinary-b', 'ordinary-a']
    assert Counter(map(id, items)) == original_ids
    assert Counter(item.nodeid for item in items) == Counter(names)


def test_partial_selection_cannot_silently_claim_the_full_historical_lane():
    items = [SimpleNamespace(nodeid=HISTORICAL_FIRST[0])]
    with pytest.raises(pytest.UsageError, match='requires the full compatibility inventory'):
        pytest_collection_modifyitems(configuration(enabled=True), items)


@pytest.mark.parametrize('workers', [1, 2, 'auto'])
def test_parallel_scheduler_cannot_silently_claim_serial_preflight(workers):
    items = [SimpleNamespace(nodeid=name) for name in HISTORICAL_FIRST]
    with pytest.raises(pytest.UsageError, match='requires a serial release run'):
        pytest_collection_modifyitems(configuration(enabled=True, workers=workers), items)
