"""Opt-in serial release ordering; existing controls execute exactly once."""
import pytest

# Completed release timings order the five previously stale compatibility
# controls from cheap to expensive. These are existing tests, not new oracles.
HISTORICAL_FIRST = (
    'tests/test_reading_semantics.py::ReadingSemanticsTests::test_lectionary_corrections_are_idempotent_and_reject_drift',
    'tests/test_site_review_repairs.py::test_serialized_psalm_title_seam_and_partial_clause_repairs',
    'tests/test_qualified_package_integrity.py::test_package_entrypoint_rejects_inactive_qualified_lifecycle',
    'tests/test_finalization_supplement.py::test_actual_composed_release_control_and_source_auth_failure',
    'tests/test_revelation_version_routes.py::test_integrity_counts_public_daily_rows_not_authenticated_inverse_history',
)


def pytest_addoption(parser):
    parser.addoption('--historical-first', action='store_true',
                     help='Run five existing historical compatibility controls first in the serial full suite; combine with -x.')


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    if not config.getoption('historical_first'):
        return
    if config.getoption('numprocesses', default=0) not in (None, 0):
        raise pytest.UsageError('--historical-first requires a serial release run (-n 0); parallel schedulers can reorder files')
    selected = {item.nodeid for item in items}
    missing = set(HISTORICAL_FIRST) - selected
    if missing:
        raise pytest.UsageError('--historical-first requires the full compatibility inventory; missing: ' + ', '.join(sorted(missing)))
    rank = {nodeid: index for index, nodeid in enumerate(HISTORICAL_FIRST)}
    # Stable sorting preserves every selected item and the remaining order.
    # No preliminary pytest run, deselection, verdict cache or duplicate work.
    items.sort(key=lambda item: rank.get(item.nodeid, len(rank)))
