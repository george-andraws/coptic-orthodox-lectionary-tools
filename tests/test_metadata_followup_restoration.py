"""Real Mark complete-table guard remains in charge after metadata restoration."""
import copy
import pytest
import metadata_followup_repairs as m
import mark_followup_repairs as mark


@pytest.mark.parametrize('year', [2026, 2027, 2028])
def test_authenticated_metadata_inverse_preserves_complete_mark_guard(year):
    before = copy.deepcopy(m.baseline()['daily'][str(year)])
    mark_rows = mark.repair_daily(before)
    metadata_rows = m.repair_daily(mark_rows)
    restored = m.restore_daily_for_comparison(metadata_rows)
    assert restored == mark_rows
    assert mark.restore_predecessor_for_comparison(restored, year) == before
    for date, rows in restored.items():
        for row in rows:
            mark.qualify_emitted(row, date=date)


@pytest.mark.parametrize('field,value', [('display_label', 'forged label'),
    ('source_locator', 'forged locator'), ('metadata_review_flags', ['forged flag']),
    ('normalized_season', 'holy_fifty')])
def test_metadata_inverse_rejects_unauthenticated_delta(field, value):
    source = next(r for r in m.baseline()['reverse_rows'] if r['display_ref'] == '1Tim 2:1-3:4' and m.bare_cycle_keys(r))
    valid = m.repair_rows([dict(source, display_label=mark.display_label(source))])[0]
    valid[field] = value
    with pytest.raises(ValueError, match='metadata follow-up'):
        m.restore_rows_for_comparison([valid])


@pytest.mark.parametrize('mutation', ['delete', 'add', 'order', 'reference', 'lifecycle'])
def test_metadata_inverse_never_masks_complete_mark_corruption(mutation):
    date = '2026-04-07'
    before = copy.deepcopy(m.baseline()['daily']['2026'])
    mark_rows = mark.repair_daily({date: before[date]})
    projected = m.repair_daily(mark_rows)
    if mutation == 'delete':
        projected[date].pop()
    elif mutation == 'add':
        projected[date].append(copy.deepcopy(projected[date][0]))
    elif mutation == 'order':
        projected[date][0], projected[date][1] = projected[date][1], projected[date][0]
    elif mutation == 'reference':
        projected[date][0]['display_ref'] = 'Jn 11:12-24'
    else:
        projected[date][0]['active'] = False
    restored = m.restore_daily_for_comparison(projected)
    with pytest.raises(ValueError, match='complete-table mismatch'):
        mark.restore_predecessor_for_comparison(restored, 2026)


def test_calendar_view_restores_exact_predecessor_labels_not_source_titles():
    original = next(r for r in m.baseline()['reverse_rows'] if r.get('annual_sunday') == 'amshir-4')
    projected = m.repair_rows([dict(original, display_label=mark.display_label(original))])
    calendar_view = m.restore_rows_for_comparison(projected, previous_layer='calendar')[0]
    assert calendar_view['display_label'] == original['display_label']
    assert calendar_view['source_title'] == original['source_title']
    assert calendar_view['calendar_keys'] == original['calendar_keys']
