"""Timothy/Luke metadata controls against the authenticated published predecessor."""
import copy
import json
from collections import Counter

import pytest

import gzip
from pathlib import Path
import metadata_followup_repairs as m


@pytest.fixture(scope='module')
def frozen():
    source = Path(__file__).resolve().parents[1] / 'sources/metadata-followup-1.3.8/published-1.3.7.json.gz'
    return json.loads(gzip.decompress(source.read_bytes()))


def test_removed_rows_never_claim_occurrence(frozen):
    after = m.repair_rows(frozen['reverse_rows'])
    assert sum(bool(r.get('removed_marker')) for r in after) == 4509
    assert all(r.get('occurs_in_shipped_years') is False for r in after if r.get('removed_marker'))


def test_bare_cycle_keys_get_source_qualified_seasons_and_labels(frozen):
    after = m.repair_rows(frozen['reverse_rows'])
    rows = [r for r in after if m.bare_cycle_keys(r)]
    assert len(rows) == 1090
    single = [r for r in rows if len(m.bare_cycle_keys(r)) == 1]
    assert Counter(r['normalized_season'] for r in single if m.is_current(r)) == {'great_lent': 156, 'holy_fifty': 64}
    assert Counter(r['normalized_season'] for r in rows if m.is_current(r)) == {'great_lent': 156, 'holy_fifty': 65}
    assert all(r['normalized_calendar_keys'] for r in rows)
    assert all(r['display_label'] not in m.GENERIC_CYCLES for r in rows)
    for reference, expected in [('1Tim 2:1-3:4', 'Thursday of the sixth week of Great Lent'),
                                ('1Tim 3:13-16', 'Feast of the Ascension')]:
        row = next(r for r in rows if r['calendar_keys'] == 'week 6 day_of_week 4' and r['display_ref'] == reference)
        assert row['display_label'] == expected


def test_month_labels_and_hatour_date_only_commemorations(frozen):
    after = m.repair_rows(frozen['reverse_rows'])
    assert all(m.normalize_month_words(r['display_label']) == r['display_label'] for r in after)
    for row in after:
        if row.get('annual_sunday') == 'amshir-4':
            assert row['display_label'] == 'Fourth Sunday of Amshir'
        if row.get('coptic_date_key') == 'hatour-24':
            assert row['display_commemoration_titles'][0] == 'The Commemoration of the Twenty-Four Presbyters'
            assert row['commemoration_join_basis'] == 'coptic_date_only'


def test_generated_attestations_are_empty_not_fabricated(frozen):
    after = m.repair_rows(frozen['reverse_rows'])
    selected = [r for r in after if r.get('provenance') == m.GENERATED_OVERLAY]
    assert len(selected) == 145
    assert all(r['attestation_years'] == r['attestation_year_min'] == r['attestation_year_max'] == '' for r in selected)
    for old, new in zip(frozen['reverse_rows'], after):
        assert new.get('source_disclosure') == old.get('source_disclosure')
        assert new.get('current_status') == old.get('current_status')


def test_lk1_flags_exactly_both_three_gospel_sets_without_choice(frozen):
    before = frozen['reverse_rows']
    after = m.repair_rows(before)
    flagged = [r for r in after if r.get('metadata_review_flags') == ['LK1_abib_26_conflicting_gospel_sets']]
    assert len(flagged) == 6
    assert Counter(r['source_family'] for r in flagged) == {'ordinary_date_resolved': 3, 'katameros_cycle': 3}
    for old, new in zip(before, after):
        assert new.get('active') == old.get('active')
        assert new.get('current_status') == old.get('current_status')


def test_complete_projection_idempotency_and_protected_fields(frozen):
    before = frozen['reverse_rows']
    after = m.repair_rows(before)
    assert len(after) == len(before) == 12330
    assert m.repair_rows(after) == after
    m.validate_rows(after)
    allowed = m.CHANGED_FIELDS
    for old, new in zip(before, after):
        assert {k: v for k, v in old.items() if k not in allowed} == {k: v for k, v in new.items() if k not in allowed}


@pytest.mark.parametrize('year', [2026, 2027, 2028])
def test_daily_metadata_does_not_change_membership_or_order(frozen, year):
    before = frozen['daily'][str(year)]
    after = m.repair_daily(before)
    assert m.repair_daily(after) == after
    assert list(after) == list(before)
    for date, rows in before.items():
        assert len(after[date]) == len(rows)
        for old, new in zip(rows, after[date]):
            assert {k: v for k, v in old.items() if k not in m.CHANGED_FIELDS} == {k: v for k, v in new.items() if k not in m.CHANGED_FIELDS}
    if year == 2027:
        assert len([r for r in after['2027-08-02'] if r.get('metadata_review_flags')]) == 3


@pytest.mark.parametrize('field,value', [('source_family', 'forged'), ('source_kind', 'forged'),
    ('calendar_keys', 'week 5 day_of_week 4'), ('source_locator', 'forged'),
    ('source_title', 'forged'), ('canonical_mt_ref', '1Tim 3:13-15')])
def test_targeted_context_mutations_fail_closed(frozen, field, value):
    original = next(r for r in frozen['reverse_rows'] if r['display_ref'] == '1Tim 3:13-16' and r['source_family'] == 'katameros_cycle')
    with pytest.raises(ValueError, match='metadata follow-up source'):
        m.repair_rows([dict(original, **{field: value})])


@pytest.mark.parametrize('mutator', [
    lambda rows: rows[0].update(occurs_in_shipped_years=True, removed_marker='superseded'),
    lambda rows: next(r for r in rows if m.bare_cycle_keys(r)).pop('normalized_season'),
    lambda rows: next(r for r in rows if m.bare_cycle_keys(r)).update(normalized_calendar_keys=['unqualified']),
    lambda rows: rows[0].update(display_label='Fourth Sunday of Meshir'),
])
def test_whole_row_guards_reject_targeted_metadata_corruption(frozen, mutator):
    after = m.repair_rows(frozen['reverse_rows'])
    mutator(after)
    with pytest.raises(ValueError, match='metadata follow-up'):
        m.validate_rows(after)


def test_lk4_report_only_finds_known_pairs_and_preserves_all_coordinates(frozen):
    before = copy.deepcopy(frozen['reverse_rows'])
    inventory = m.endpoint_conflicts(before)
    assert before == frozen['reverse_rows']
    known = {(x['context'], x['service'], tuple(x['references'])): x for x in inventory}
    key = ('annual_sunday:mesra-4', 'Vespers', ('Lk 17:20-36', 'Lk 17:20-37'))
    assert key in known
    assert len(known[key]['dates']) == 16
    # Tout 8's Katameros endpoint is already inactive in the published
    # predecessor, so it is flagged but not counted as a two-current-row group.
    assert ('coptic_date:tout-8', 'Liturgy', ('Matt 23:13-26', 'Matt 23:13-36')) not in known
    flags = [r for r in m.repair_rows(before) if 'LK4_range_variant_no_endpoint_change' in r.get('metadata_review_flags', [])]
    assert len(flags) == 4
    assert sum(not m.is_current(r) for r in flags) == 1


def test_checksheet_has_exact_seven_timothy_appointments(frozen):
    entries = m.timothy_confirmations()
    assert len(entries) == 7
    assert len({(r['identity_key'], r['occasion'], r['service_section']) for r in entries}) == 7
    assert all(r['priority'] == 'low' and r['action'] == 'confirm, no change expected' for r in entries)
    assert sum('https://copticchurch.net/readings?' in r['source_locator'] for r in entries) == 6
    water = next(r for r in entries if r['display_ref'] == '1Tim 4:9-5:10')
    assert water['source_family'] == 'coptic_reader_qualified_pascha_hour'
    assert 'selected=2026-04-09' in water['source_locator']


def test_sentinels_and_feasts_are_not_naive_week_numbers(frozen):
    after = m.repair_rows(frozen['reverse_rows'])
    expected = {('great_lent', 'week 7 day_of_week 0'): 'Palm Sunday',
                ('great_lent', 'week 99 day_of_week 6'): 'Preparation Saturday',
                ('great_lent', 'week 99 day_of_week 0'): 'Preparation Sunday',
                ('holy_fifty', 'week 0 day_of_week 0'): 'Feast of the Resurrection',
                ('holy_fifty', 'week 7 day_of_week 0'): 'Feast of Pentecost'}
    for (season, key), label in expected.items():
        rows = [r for r in after if r.get('normalized_season') == season and r['calendar_keys'] == key]
        if rows:
            assert all(r['display_label'] == label for r in rows)
    unresolved = [r for r in after if r.get('cycle_label_status') == 'unresolved_source_week_49']
    assert len(unresolved) == 2
    assert all(not m.is_current(r) for r in unresolved)
