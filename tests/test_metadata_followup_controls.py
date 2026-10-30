import copy
import json
import pytest
import metadata_followup_repairs as m


@pytest.fixture(scope='module')
def frozen():
    return copy.deepcopy(m.baseline())


@pytest.mark.parametrize('field,value', [('normalized_season', 'holy_fifty'),
    ('display_commemoration_titles', ['The Twenty-Four Priests']),
    ('metadata_review_flags', []), ('synthetic_overlay_years', '1900')])
def test_whole_inventory_checks_source_derived_metadata(frozen, field, value):
    rows = m.repair_rows(frozen['reverse_rows'])
    if field == 'normalized_season':
        row = next(r for r in rows if r.get('normalized_season') == 'great_lent')
        row[field] = value
        row['normalized_calendar_keys'] = ['holy_fifty:' + key for key in m.bare_cycle_keys(row)]
        row['display_label'] = ' / '.join(m._cycle_label('holy_fifty', key)[0] for key in m.bare_cycle_keys(row))
    else:
        row = next(r for r in rows if field in r)
        row[field] = value
    with pytest.raises(ValueError, match='metadata follow-up'):
        m.validate_rows(rows)


def test_source_authentication_failure_reaches_real_projection(frozen, monkeypatch):
    authenticated = m._authenticated
    def reject(relative, digest):
        if relative == m.FIXTURE:
            raise ValueError('metadata follow-up source authentication failed: injected corruption')
        return authenticated(relative, digest)
    monkeypatch.setattr(m, '_authenticated', reject)
    with pytest.raises(ValueError, match='source authentication failed'):
        m.repair_rows(frozen['reverse_rows'])


def test_endpoint_inventory_uses_canonical_not_raw_source_frame():
    source = dict(source_family='other', source_kind='source', canonical_mt_ref='Ps 51:7',
                  spans_json=json.dumps([dict(book='Ps', chapter_start=50, verse_start=9, chapter_end=50, verse_end=9)]),
                  occasion='source appointment', service_section='Matins', slot_type='psalm', current_status='current')
    second = dict(source, source_family='another', canonical_mt_ref='Ps 51:7-8')
    inventory = m.endpoint_conflicts([source, second])
    assert len(inventory) == 1
    assert inventory[0]['start'] == 'Ps 51:7'
    assert inventory[0]['references'] == ['Ps 51:7', 'Ps 51:7-8']


def test_unknown_current_status_is_not_silently_eligible():
    with pytest.raises(ValueError, match='unknown explicit reading status'):
        m.endpoint_conflicts([dict(current_status='pending_unreviewed_appointment')])
