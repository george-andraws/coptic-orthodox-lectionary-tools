"""Bounded L1-L10 overlay on the authenticated published 1.3.7 projection.

No appointment promotion or coordinate correction is authorized by this lane.
The historical design ledger and prior H/K/R fixture policies stay unchanged.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURE = 'sources/mark-followup-1.3.8/published-1.3.7.json.gz'
FIXTURE_SHA256 = 'c67a9d2699a368f028850e52ebdc3568dccdc327a5ab8afafebe794b47d7d1e5'
ORACLE = 'sources/mark-followup-1.3.8/independent-acceptance-oracle.json'
ORACLE_SHA256 = '2d0dcb7c2072de7965ff0ab75af3deab0fd313143afe44b894ead7dcc0ada153'
HOLD = 'pending_coptic_reader_review'
LEGACY = ('holy_pascha_curated_day_hour', 'pascha_day_hour')
HOURS = ('First Hour', 'Third Hour', 'Sixth Hour', 'Ninth Hour', 'Eleventh Hour')
# Missing hours are coverage holds, not fabricated Scripture appointments.
EVE_GAPS = {
    'eve_of_monday': ('First Hour', 'Sixth Hour', 'Ninth Hour'),
    'eve_of_tuesday': (),
    'eve_of_wednesday': ('Third Hour', 'Ninth Hour', 'Eleventh Hour'),
    'eve_of_thursday': (),
    'eve_of_friday': (),
}
TUESDAY_HOLDS = {
    ('First Hour', 'Gospel', 'Jn 11:12-24'),
    ('Third Hour', 'Gospel', 'Mark 11:11-19'),
    ('Third Hour', 'OT1', 'Isa 5:20-30'),
    ('Third Hour', 'OT2', 'Jer 9:12-19'),
    ('Ninth Hour', 'Gospel', 'Matt 21:23-27'),
    ('Eleventh Hour', 'Gospel', 'Jn 8:51-59'),
}
PRINTED_CANDIDATES = {
    ('Third Hour', 'Matt 24:36-51'), ('Third Hour', 'Amos 5:18-27'),
    ('Ninth Hour', 'Matt 23:29-36'), ('Ninth Hour', 'Hos 9:14-10:2'),
}
SERVICE_LABELS = {
    'palm_sunday': 'Palm Sunday', 'eve_of_monday': 'Eve of Monday',
    'monday': 'Monday', 'eve_of_tuesday': 'Eve of Tuesday',
    'tuesday': 'Tuesday', 'eve_of_wednesday': 'Eve of Wednesday',
    'wednesday': 'Wednesday', 'eve_of_thursday': 'Eve of Thursday',
    'great_thursday': 'Great Thursday', 'eve_of_friday': 'Eve of Good Friday',
    'good_friday': 'Good Friday', 'bright_saturday': 'Bright Saturday',
}


def _authenticated(relative, digest):
    path = ROOT / relative
    if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != ROOT.parent):
        raise ValueError('Mark follow-up source symlink rejected')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError('Mark follow-up source authentication failed: ' + relative)
    return data


@lru_cache(maxsize=1)
def _decode(data):
    return json.loads(gzip.decompress(data))


def baseline():
    return _decode(_authenticated(FIXTURE, FIXTURE_SHA256))


@lru_cache(maxsize=1)
def _json_decode(data):
    return json.loads(data)


def source_oracle():
    return _json_decode(_authenticated(ORACLE, ORACLE_SHA256))


def validate_pending_reading(row, date):
    """Check the dated pending allowance, not the complete source-row schema.

    Compose with the source-family/disclosure validators at serialized output;
    daily rows do not all contain reverse-only source_title/calendar_keys cells.
    """
    status = row.get('current_status', '')
    if not isinstance(status, str) or not status.startswith('pending_'):
        return
    matches = [entry for entry in source_oracle()['L9']['pending_occurrence_oracle']
               if entry['date'] == date and entry['selector']['identity_key'] == row.get('identity_key')
               and entry['lane'].startswith('preserve_')]
    for entry in matches:
        expected = {k: v for k, v in entry['selector'].items() if k != 'calendar_keys'}
        expected.update({k: entry[k] for k in ('current_status', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json', 'source_locator')})
        if (all(type(row.get(k)) is type(v) and row.get(k) == v for k, v in expected.items())
                and hashlib.sha256(str(row.get('source_disclosure', '')).encode()).hexdigest() == entry['source_disclosure_sha256']):
            return
    raise ValueError('Pending daily reading outside authenticated allowance: ' + date + ' ' + str(row.get('identity_key')))


def display_label(row):
    import holy_week_review_repairs as holy
    label = row.get('display_label') or row.get('display_occasion') or row.get('occasion', '')
    context = holy.pascha_context(row)
    service = row.get('pascha_service') or context.get('pascha_service')
    if service in SERVICE_LABELS:
        label = SERVICE_LABELS[service]
    elif row.get('occasion') in {'Palm Sunday', 'Hosanna Sunday', 'Bright Saturday'}:
        label = 'Bright Saturday' if row['occasion'] == 'Bright Saturday' else 'Palm Sunday'
    elif (row.get('source_family'), row.get('source_kind')) == ('coptic_reader', 'coptic_reader_fixture') and row.get('occasion') == 'Wednesday of Holy Pascha':
        label = 'Wednesday'
    elif row.get('source_family') == 'coptic_reader_qualified_pascha_hour':
        label = {'the Covenant Thursday': 'Great Thursday'}.get(row.get('occasion'), label)
    return label.replace('Kiyank', 'Kiahk').replace('Ninevah', 'Nineveh')


def rule(row):
    pair = (row.get('source_family'), row.get('source_kind'))
    ref = row.get('canonical_mt_ref', '')
    if (pair == ('ordinary_date_resolved', 'copticchurch_date')
            and row.get('occasion') == 'Mesra 7' and row.get('service_section') == 'Vespers'
            and row.get('slot') == 'Gospel' and row.get('identity_key') == 'rid_24a3269b0d1a1fb0412d'):
        return 'L1'
    if pair == LEGACY and row.get('occasion') == 'Tuesday' and (
            row.get('service_hour'), row.get('slot'), ref) in TUESDAY_HOLDS:
        return 'L2'
    if (pair == ('holy_pascha', 'pascha_source_text') and row.get('occasion') == 'Wednesday Eve'
            and (row.get('service_hour'), ref) in PRINTED_CANDIDATES):
        return 'L3'
    if (pair in {('ordinary_date_resolved', 'copticchurch_date'), ('katameros_cycle', 'katameros_cycle')}
            and row.get('occasion') in {'Hatur 11', 'Hator 11'}
            and row.get('service_section') in {'Vespers', 'vespers_gospel'}
            and row.get('slot') in {'Gospel', 'vespers_gospel'}
            and ref in {'Mark 14:3-9', 'Matt 10:24-33'}):
        return 'L6'
    if pair[1] == 'special_service' and (
            pair[0] == 'myron_consecration' and (row.get('service_section'), ref) in {
                ('main_readings', 'Mark 14:3-9'),
                ('second_liturgy_liturgy_of_the_word', 'Mark 14:3-9'),
                ('offering_of_morning_incense', 'Mark 16:1-20')}
            or pair[0] == 'consecration' and row.get('calendar_keys') == 'consecrations_monk' and ref == 'Mark 8:34-9:1'
            or pair[0] == 'wedding_crowning' and row.get('service_section') == 'main_readings' and ref in {'Matt 19:1-6', 'Eph 5:22-6:3'}):
        return 'L7'
    if pair == LEGACY and row.get('current_status') == 'pending_psalm_equivalence_unresolved' and not row.get('removed_marker'):
        return 'L9'
    return ''


NOTES = {
    'L1': 'L1: malformed Mk 14:-39 heading and whole-chapter body do not establish Mark 14:3-9. Hold for Reader; retain the literal source.',
    'L2': 'L2: copied Tuesday day-hour working appointment held pending Reader confirmation. No replacement inferred.',
    'L3': 'L3: printed Third/Ninth Hour candidate only; no Reader activation. Eleventh Hour remains an explicit coverage gap.',
    'L6': 'L6: Hator 11 Vespers sources disagree: Matthew 10:24-33 versus Mark 14:3-9. Preserve both; Q-L1 remains open.',
    'L7': 'L7: requested unverified_service_book annotation retained alongside the existing saved Reader evidence. No source information, appointment status or prior qualification is downgraded.',
    'L9': 'L9: unresolved legacy Pascha Psalm excluded from daily output. Status and numeric witness retained; accepted source-only alignment holds are separate.',
}


def _project(original):
    row = copy.deepcopy(original)
    row['display_label'] = display_label(row)
    item = rule(row)
    if not item:
        return row
    if item == 'L1':
        _authenticated('cache/copticchurch_html/2024-08-13.html',
                       '42e0457d3939781d9c08c9af6da0a8ebd6d78b74e7c1a458880afcf577ee0868')
    elif item == 'L3':
        _authenticated('out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt',
                       'd37ef1df5ff9e5caadfe77a2b45a6e21b66bf69005715c93ed11e7004f1c872d')
    row['mark_followup_note'] = NOTES[item]
    row['mark_followup_evidence'] = json.dumps(dict(
        issue=item, predecessor=FIXTURE, predecessor_sha256=FIXTURE_SHA256,
        original_status=original.get('current_status'), reader_activation=False), sort_keys=True, separators=(',', ':'))
    if item in {'L1', 'L2', 'L3'}:
        row['current_status'] = HOLD
        row['active'] = False
    elif item == 'L9':
        row['active'] = False
    elif item == 'L6':
        row['evidence_status'] = 'conflicting_vespers_sources'
    elif item == 'L7':
        row['evidence_status'] = 'unverified_service_book'
    return row


KEY = ('identity_key', 'source_family', 'source_kind', 'occasion', 'service_section', 'service_hour', 'slot', 'source_locator')


def key(row):
    return tuple(row.get(f, '') for f in KEY)


def originals(date=None):
    frozen = baseline()
    if date is None:
        return frozen['reverse_rows']
    return frozen['daily'].get(date[:4], {}).get(date, [])


def _qualify(row, original, *, projected):
    expected = _project(original) if projected else original
    # These two positions are assigned after suppression and may legitimately
    # differ. All coordinates, source cells, raw keys and lifecycle stay exact.
    ignore = {'reading_order', 'service_order', 'displaced_by', 'occurrence_scope',
              'occurs_in_shipped_years', 'occurs_outside_paschal_seasons'}
    a = {k: v for k, v in row.items() if k not in ignore}
    b = {k: v for k, v in expected.items() if k not in ignore}
    if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
        changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k) or (k in a) != (k in b))
        raise ValueError('Mark follow-up source/context/lifecycle drift: ' + str(key(row)) + '; fields=' + str(changed))


def repair_rows(rows, *, date=None):
    index = {key(r): r for r in originals(date)}
    output = []
    candidates_seen = set()
    for row in rows:
        item = rule(row)
        if item or row.get('mark_followup_evidence'):
            original = index.get(key(row))
            if original is None or not rule(original):
                raise ValueError('Mark follow-up unqualified source/context')
            _qualify(row, original, projected=bool(row.get('mark_followup_evidence')))
            if item == 'L3' and not row.get('mark_followup_evidence'):
                # Keep the historical witness independently, and add a review
                # candidate with the same literal source coordinates and keys.
                output.append(dict(copy.deepcopy(original), display_label=display_label(original)))
            if item != 'L3' or key(row) not in candidates_seen:
                output.append(_project(original))
                candidates_seen.add(key(row))
        else:
            output.append(dict(copy.deepcopy(row), display_label=display_label(row)))
    return output


@lru_cache(maxsize=1)
def _owned_anchors():
    frozen = baseline()
    rows = frozen['reverse_rows'] + [r for days in frozen['daily'].values() for readings in days.values() for r in readings]
    rows = [r for r in rows if rule(r)]
    fields = ('identity_key', 'occasion', 'service_section', 'service_hour', 'slot')
    return ({r.get('source_locator') for r in rows}, {tuple(r.get(f, '') for f in fields) for r in rows})


def qualify_emitted(row, *, date=None):
    """Recognize owned tuples independently of mutable family/lifecycle markers."""
    candidates = [r for r in originals(date) if rule(r)]
    matches = [r for r in candidates if row.get('source_locator') == r.get('source_locator') or (
        row.get('identity_key') == r.get('identity_key') and all(row.get(f, '') == r.get(f, '')
        for f in ('occasion', 'service_section', 'service_hour', 'slot')))]
    if not matches:
        locators, contexts = _owned_anchors()
        context = tuple(row.get(f, '') for f in ('identity_key', 'occasion', 'service_section', 'service_hour', 'slot'))
        if (row.get('mark_followup_evidence') or row.get('mark_followup_note')
                or row.get('source_locator') in locators or context in contexts):
            raise ValueError('Mark follow-up unowned emitted evidence or outer date')
        return False
    exact = [r for r in matches if key(row) == key(r)]
    if not exact:
        # A raw source cell may legitimately own both a retired legacy Psalm
        # and a reviewed fragment. Shared locator text is not identical identity.
        neighbors = [r for r in originals(date) if key(row) == key(r) and not rule(r)]
        if len(neighbors) == 1:
            _qualify(row, neighbors[0], projected=True)
            return False
    if len(exact) != 1:
        raise ValueError('Mark follow-up emitted source/context rebound')
    _qualify(row, exact[0], projected=not (rule(exact[0]) == 'L3' and not row.get('mark_followup_evidence')))
    return True


def inactive_qualified(row):
    # Recognize exact predecessor identity even if friendly markers are stripped.
    matches = [r for r in originals() if rule(r) in {'L1', 'L2', 'L3', 'L9'} and key(row) == key(r)]
    if not matches and not row.get('mark_followup_evidence'):
        return False
    if not matches:
        if row.get('mark_followup_note', '').startswith(('L6:', 'L7:')):
            return False
        raise ValueError('Mark follow-up inactive source/context rebound')
    _qualify(row, matches[0], projected=True)
    return True


def repair_daily(days):
    output = {}
    for date, rows in days.items():
        projected = repair_rows(rows, date=date)
        output[date] = [r for r in projected if r.get('active') is not False]
        # Suppression can change the structural-fill positions seen by older
        # hooks. Preserve the independently frozen complete service sequence,
        # sorting actual rows only; never reconstruct content from the candidate.
        source_order = {key(r): i for i, r in enumerate(originals(date))}
        if source_order:
            if any(key(r) not in source_order for r in output[date]):
                raise ValueError('Mark follow-up unexpected daily appointment: ' + date)
            output[date].sort(key=lambda r: source_order[key(r)])
        for i, row in enumerate(output[date], 1):
            validate_pending_reading(row, date)
            row['reading_order'] = i
    return output


def validate_eve_coverage(days, year):
    """Five-hour accountability, with explicit missing-hour holds, not invention."""
    from calendar_resolution import julian_pascha_gregorian
    import datetime as dt
    import holy_week_review_repairs as holy
    from reading_context_overlays import is_current_source_row
    result = []
    for service, held in EVE_GAPS.items():
        date = (julian_pascha_gregorian(year) + dt.timedelta(days=holy.OFFSET[service])).isoformat()
        rows = [r for r in days.get(date, []) if r.get('pascha_service') == service
                and not r.get('removed_marker') and is_current_source_row(r)]
        present = {r.get('service_hour') for r in rows}
        if present & set(held) or present | set(held) != set(HOURS):
            raise ValueError('Pascha eve five-hour coverage drift: ' + service)
        result.extend(dict(service=service, hour=h, coverage='held_missing_reader' if h in held else 'current', civil_date=date) for h in HOURS)
    return result


def validate_day_hour_sets(days):
    """Reject complete non-Psalm day-hour copies across distinct Pascha days.

    Partial hours lacking a Gospel or prophecy do not assert completeness. Eve
    services and the same-day H5 question are not different-day duplicates.
    """
    groups = {}
    for readings in days.values():
        for row in readings:
            service = row.get('pascha_service')
            if service not in {'palm_sunday', 'monday', 'tuesday', 'wednesday', 'great_thursday', 'good_friday'}:
                continue
            if row.get('active') is False or row.get('removed_marker'):
                continue
            if row.get('slot_type') in {'gospel', 'prophecy'}:
                groups.setdefault((service, row.get('service_hour')), []).append(row)
    seen = {}
    for (service, hour), rows in groups.items():
        if {r.get('slot_type') for r in rows} != {'gospel', 'prophecy'}:
            continue
        signature = tuple(sorted((r.get('slot_type'), r.get('canonical_mt_ref')) for r in rows))
        if signature in seen and seen[signature][0] != service:
            raise ValueError('Pascha day-hour set repeats another day: ' + str(seen[signature]) + ' / ' + str((service, hour)))
        seen[signature] = (service, hour)


def restore_predecessor_for_comparison(daily, year):
    """Authenticate complete successor groups, then replay historical comparator.

    Only pinned predecessor arrays enter the repair. Candidate rows never create
    an expected table, and omitted, reordered or extra rows are rejected first.
    """
    output = copy.deepcopy(daily)
    for date, before in baseline()['daily'].get(str(year), {}).items():
        expected = repair_daily({date: before})[date]
        if daily.get(date) != expected:
            raise ValueError('Mark follow-up daily complete-table mismatch: ' + date)
        output[date] = copy.deepcopy(before)
    return output
