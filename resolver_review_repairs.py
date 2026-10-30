"""Isolated, source-qualified R1/R3/R4/R6 repairs.

No I/O writes, publication, implicit activation, or corpus-membership bypasses.
Callers retain raw witnesses and apply appointment grouping only after their
unchanged whole-corpus membership gate. R3 is descriptive, never a selector.
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parent
DATABASE = 'sources/katameros-api/Core/KatamerosDatabase.db'
DATABASE_SHA256 = 'b6a1bbfa96543b7028bba77ad33df5cb018d21ec7bde1335247c2bd86ff43784'
LAST_FRIDAY = 'Friday of the seventh week of Great Lent'
BOUNDARY_SOURCE = 'Coptic Reader verified calendar boundary'
LAST_FRIDAY_CAPTURE = ('sources/coptic-reader/matins-source-accepted-2026-10-07/evidence/'
                       'lent-source-completion-04/attempts/2026-04-03-ready02')
BEL_CAPTURE = 'sources/coptic-reader/lent-qualified-2026-10-07/2026-03-13'
MONTHS = ('tout', 'baba', 'hatour', 'kiahk', 'toba', 'amshir', 'baramhat',
          'baramouda', 'bashans', 'paona', 'abib', 'mesra', 'nasie')
COMPOSITES = {
    '40.4:23-25*@+40.5:1-16': ('Matt 4:23-25', 'Matt 5:1-16'),
    '41.8:34-38*@+41.9:1': ('Mark 8:34-38', 'Mark 9:1'),
    '42.11:53-54*@+42.12:1-12': ('Lk 11:53-54', 'Lk 12:1-12'),
    '44.25:23-27*@+44.26:1-6': ('Acts 25:23-27', 'Acts 26:1-6'),
    'Acts 25:23-27  &  Acts 26:1-6': ('Acts 25:23-27', 'Acts 26:1-6'),
}
SLOT_COLUMNS = {'vespers_gospel': 'V_Gospel_Ref', 'matins_gospel': 'M_Gospel_Ref',
                'liturgy_gospel': 'L_Gospel_Ref', 'liturgy_acts': 'X_Gospel_Ref'}


def _authenticated_bytes(relative, digest):
    payload = (ROOT / relative).read_bytes()
    if hashlib.sha256(payload).hexdigest() != digest:
        raise ValueError(f'Resolver repair source drift: {relative}')
    return payload


def _read_authenticated(relative, digest):
    return _authenticated_bytes(relative, digest).decode('utf-8')


def _authenticate_last_friday():
    base = LAST_FRIDAY_CAPTURE + '/'
    pins = {
        'capture.json': 'fdcc57fefe7571c407707d4e05fa07c1e99e2aff0b54f65f21cba0eb7eac8457',
        'Psalm_and_Gospel.txt': '8a1764eb45b2e251e6401c2d5ea5a4b0c0d8c98eb258056877197f94a9983c89',
        '2026-04-03/context.txt': 'c6bfa43f7466fc9d8f5317f7f36ec223f4b5844cd62d729939b83ad6a762b9f0',
        '2026-04-03/picker.json': 'a5f082d5f086faaf9de8497cebce79c61bd365352b9b30b2ce9d299441da796f',
    }
    docs = {name: _read_authenticated(base + name, pin) for name, pin in pins.items()}
    metadata = json.loads(docs['capture.json'])
    document, = metadata['documents']
    for image in document['reference_screenshots']:
        _authenticated_bytes(base + Path(image['path']).name, image['sha256'])
    _authenticated_bytes(base + '2026-04-03/context.png',
        'd109041e159e43160fd592567a4809c5cc102fb2980474f84d281a1f33ad353a')
    _authenticated_bytes(base + '2026-04-03/picker.png',
        '00f0c6b84ad7b8f8a292478e984a6df2b21ebb6c6dcb2955e8f7567f8146978f')
    if (metadata['civil_date'] != '2026-04-03'
            or document['navigation'] != ['Readings', 'Matins', 'Psalm and Gospel']
            or document['raw_reference_lines'] != ['\tPsalms 31:11-12', '\tLuke 16:19-31']
            or not docs['2026-04-03/context.txt'].startswith('Selected Season Last Friday of Great Fast Paremhotep 25, 1742 Friday, April 3, 2026')
            or '\tLuke 16:19-31\n' not in docs['Psalm_and_Gospel.txt']):
        raise ValueError('Last Friday retained Matins source/context mismatch')
    return base + 'Psalm_and_Gospel.txt'


def _active(row):
    from reading_context_overlays import is_current_source_row
    if not is_current_source_row(row):
        return False
    if row.get('removed_marker') or row.get('superseded_reason'):
        return False
    if row.get('active') is False or row.get('include_in_current_index') is False:
        return False
    if row.get('state') in {'removed', 'superseded', 'inactive'}:
        return False
    return row.get('current_status', row.get('status', '')) in {
        '', 'current', 'current_confirmed_coptic_reader',
        'current_confirmed_by_fixture_equivalence', 'current_public_or_local_reference',
        'current_working_source_not_coptic_reader_checked'}


def pascha(year):
    """Julian computus, Gregorian civil result, including Gregorian centuries."""
    a, b, c = year % 4, year % 7, year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    return dt.date(year, 3, 22) + dt.timedelta(days=d + e + year // 100 - year // 400 - 2)


def repair_last_friday_matins(rows):
    """Correct this captured ordinary Matins Gospel only, not collision tables.

    Preserve the literal conflicting raw reference. The complete retained Matins
    Psalm/Gospel source is authenticated, but its Psalm coordinates are not
    silently projected or renumbered by a Gospel correction.
    """
    result = copy.deepcopy(rows)
    targets = []
    for row in result:
        date = row.get('gregorian_date')
        if (not date or row.get('day_title') != LAST_FRIDAY
                or row.get('service_section') != 'Matins'
                or row.get('reading_type') != 'Gospel'
                or row.get('source') == BOUNDARY_SOURCE or not _active(row)):
            continue
        date = dt.date.fromisoformat(date)
        if (date - pascha(date.year)).days != -9:
            continue
        if (row.get('source') not in {'copticchurch.net', 'copticchurch.net daily scrape',
                                      'Coptic Reader verified Last Friday Matins repair'}
                or row.get('normalized_ref') not in {'Lk 17:20-37', 'Luke 17:20-37', 'Lk 16:19-31'}):
            continue
        targets.append(row)
    if len({r['gregorian_date'] for r in targets}) != len(targets):
        raise ValueError('Last Friday duplicate Matins Gospel')
    if targets:
        locator = _authenticate_last_friday()
        for row in targets:
            row.update(normalized_ref='Lk 16:19-31',
                       source='Coptic Reader verified Last Friday Matins repair',
                       current_status='current_confirmed_coptic_reader',
                       correction_source=locator,
                       normalization_warning=('R1 retained Reader Matins Gospel; '
                           f'evidence={locator}; verified_date=2026-04-03; '
                           'recurs only at Last Friday offset -9; raw_ref retained'))
    return result


def _coptic_date(year, month, day):
    jdn = 1825030 + 365 * (year - 1) + year // 4 + (month - 1) * 30 + day - 1
    return dt.date.fromordinal(jdn - 1721425)


def coptic_key(date):
    jdn = date.toordinal() + 1721425
    year = (4 * (jdn - 1825030) + 1463) // 1461
    offset = jdn - (1825030 + 365 * (year - 1) + year // 4)
    return f'{MONTHS[offset // 30]}-{offset % 30 + 1}'


def _calendar_key(row):
    fixed, sunday = row.get('coptic_date_key'), row.get('annual_sunday')
    if fixed and sunday:
        raise ValueError('Fixed date and annual Sunday are mutually exclusive')
    key = fixed or sunday
    if not key:
        return None
    if sunday == 'any-month-5':
        return 0, 5, True
    match = re.fullmatch(r'([a-z]+)-([1-9]|[12][0-9]|30)', key)
    if not match or match[1] not in MONTHS:
        raise ValueError(f'Invalid normalized Coptic key: {key}')
    month, number = MONTHS.index(match[1]) + 1, int(match[2])
    if (sunday and number > 5) or (not sunday and month == 13 and number > 6):
        raise ValueError(f'Invalid Coptic day/ordinal: {key}')
    return month, number, bool(sunday)


def _candidate_dates(civil_year, month, number, sunday):
    if month == 0 and sunday and number == 5:
        for actual_month in range(1, 13):
            yield from _candidate_dates(civil_year, actual_month, number, sunday)
        return
    for year in (civil_year - 284, civil_year - 283):
        if not sunday and month == 13 and number == 6 and year % 4 != 3:
            continue
        date = _coptic_date(year, month, 1 if sunday else number)
        if sunday:
            date += dt.timedelta(days=(6 - date.weekday()) % 7 + 7 * (number - 1))
            if date >= _coptic_date(year, month, 1) + dt.timedelta(days=30 if month < 13 else (6 if year % 4 == 3 else 5)):
                continue
        if date.year == civil_year:
            yield date


def _season(date):
    offset = (date - pascha(date.year)).days
    if -56 <= offset <= -8:
        return 'great_lent'
    if -7 <= offset <= -1:
        return 'holy_week'
    if 0 <= offset <= 49:
        return 'holy_fifty'
    return ''


@lru_cache(maxsize=400)
def _cycle_profile(month, number, sunday):
    # Julian/Coptic leap and weekdays repeat in 28 years, computus in 19.
    # Their joint cycle is exactly 532 years, not a sample of scraped years.
    dates = [date for year in range(2000, 2532)
             for date in _candidate_dates(year, month, number, sunday)]
    seasons = {_season(date) for date in dates}
    return ('' in seasons, tuple(s for s in ('great_lent', 'holy_week', 'holy_fifty') if s in seasons))


def _service(row):
    section = row.get('service_section', '')
    slot = row.get('slot') or row.get('reading_slot') or row.get('reading_type', '')
    if '_' in section and section.split('_')[0] in {'vespers', 'matins', 'liturgy'}:
        section, slot = section.split('_', 1)
    aliases = {'pauline epistle': 'pauline', 'catholic epistle': 'catholicon',
               'acts of the apostles': 'praxis', 'acts': 'praxis', 'liturgy_acts': 'praxis'}
    slot = slot.lower().split('_')[-1]
    return section.lower(), aliases.get(slot, slot)


def annotate_calendar_occurrence(row, daily_by_year):
    """Add descriptive R3 metadata without altering eligibility or membership.

    occurs_in_shipped_years checks actual daily output. displaced_by lists the
    Paschal seasons overlapping the occasion across the complete computus cycle;
    it is potential seasonal displacement, not a claim that a Lord's feast yields
    to every season. Consumers MUST NOT use these fields as a selection policy.
    """
    from kiahk23_review_repairs import is_current_reading
    result = copy.deepcopy(row)
    key = _calendar_key(row)
    if key is None:
        return result
    month, number, sunday = key
    occurs = False
    for year, days in daily_by_year.items():
        for date in _candidate_dates(int(year), *key):
            def same_occasion(reading):
                normalized = reading.get('annual_sunday' if sunday else 'coptic_date_key')
                if normalized:
                    return normalized == row.get('annual_sunday' if sunday else 'coptic_date_key')
                title = (reading.get('occasion') or reading.get('day_title') or '').lower()
                return not any(season in title for season in (
                    'great lent', 'holy fifty', 'holy week', 'pascha', 'fast of nineveh'))
            # Presence is the public current-reading contract, not permission
            # to interpret a held source Psalm as certified canonical spans.
            if any(is_current_reading(reading) and same_occasion(reading)
                   and _service(reading) == _service(row)
                   and reading.get('display_ref') == row.get('display_ref')
                   for reading in days.get(date.isoformat(), [])):
                occurs = True
    outside, seasons = _cycle_profile(*key)
    result.update(occurs_in_shipped_years=occurs, displaced_by=list(seasons),
                  occurs_outside_paschal_seasons=outside,
                  occurrence_scope={'shipped_years': sorted(int(y) for y in daily_by_year),
                      'computus_cycle_years': 532, 'computus_cycle_start': 2000,
                      'displaced_by_semantics': 'potential seasonal displacement; not a feast-precedence rule'})
    return result


def _db_records(table):
    if table not in {'AnnualReadings', 'SundayReadings', 'GreatLentReadings', 'PentecostReadings'}:
        return []
    # Authenticate the unchanged source file, not mutable row claims.
    if hashlib.sha256((ROOT / DATABASE).read_bytes()).hexdigest() != DATABASE_SHA256:
        raise ValueError('Composite SQLite source drift')
    with sqlite3.connect(f'file:{ROOT / DATABASE}?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        return [dict(row) for row in db.execute('SELECT * FROM ' + table)]


def _same_database_cell(row, raw):
    if row.get('source_family') == 'ordinary_date_resolved':
        import html
        date = row.get('gregorian_date', '')
        path = f'cache/copticchurch_html/{date}.html'
        pins = json.loads(_read_authenticated('sources/resolver-review-2026-10-29/composite-source-pins.json',
            '76c6c04ef95ef8a16271a76666c764416d587a0a8a2426bd9b24960b7b768ece'))
        if path not in pins:
            return False
        text = html.unescape(_read_authenticated(path, pins[path]))
        return (row.get('calendar_key') == 'Thursday of the seventh week of Great Lent'
                and row.get('service_section') == 'Liturgy'
                and (row.get('slot') or row.get('reading_type')) == 'Acts of the Apostles'
                and '<h5>' + raw + '</h5>' in text
                and 'Thursday of the seventh week of Great Lent' in text)
    slot = row.get('slot', row.get('reading_slot', ''))
    column = SLOT_COLUMNS.get(slot)
    table = row.get('source_table')
    if not column:
        return False
    for record in _db_records(table):
        if record.get(column) != raw:
            continue
        if table in {'GreatLentReadings', 'PentecostReadings'}:
            key = f"week {record['Week']} day_of_week {record['DayOfWeek']}"
        else:
            key = f"{record.get('Month_Name', '')} {record['Day']}"
        if row.get('calendar_key') == key:
            return True
    return False


def merge_proven_composites(rows):
    """Group only the four reviewed split patterns from one actual SQLite cell.

    Raw canonical witnesses are not modified. Returned appointment rows retain
    every complete fragment in composite_fragments_json and provenance, including
    literal source locators. This is a separate presentation contract: run the
    ordinary all-witness membership guard BEFORE this projection, not instead of it.
    """
    result = copy.deepcopy(rows)
    groups = defaultdict(list)
    for index, row in enumerate(result):
        raw = row.get('raw_ref')
        database_source = (row.get('source_family'), row.get('source_kind'), row.get('source_file')) == ('katameros_cycle', 'katameros_cycle', DATABASE)
        ordinary_source = (row.get('source_family'), row.get('source_kind'), row.get('source_file')) == ('ordinary_date_resolved', 'copticchurch_date', 'cache/copticchurch_html')
        if raw not in COMPOSITES or not _active(row) or not (database_source or ordinary_source):
            continue
        key = tuple(str(row.get(field, '')) for field in (
            'source_table', 'calendar_key', 'gregorian_date', 'service_section', 'slot', 'raw_ref'))
        groups[key].append((index, row))
    events, replacements, removed = [], {}, set()
    for items in groups.values():
        if len(items) < 2:
            continue
        raw = items[0][1]['raw_ref']
        if not _same_database_cell(items[0][1], raw):
            continue
        expected = COMPOSITES[raw]
        by_ref = {row.get('display_ref'): (index, row) for index, row in items}
        if len(by_ref) != len(items) or set(by_ref) != set(expected):
            raise ValueError('Proven composite has incomplete/duplicate/changed fragment set')
        fragments = [by_ref[ref][1] for ref in expected]
        spans = [span for row in fragments for span in json.loads(row['spans_json'])]
        from passage_normalization import parse_passage
        for ref, row in zip(expected, fragments):
            parsed = parse_passage(ref)
            if parsed is None:
                raise ValueError('Unsupported reviewed composite reference')
            actual = json.loads(row['spans_json'])
            coordinates = [(s.get('book'), s.get('chapter_start'), s.get('verse_start'),
                            s.get('chapter_end'), s.get('verse_end')) for s in actual]
            expected_coordinates = [(parsed.book_abbrev, p.chapter_start, p.verse_start,
                                     p.chapter_end, p.verse_end) for p in parsed.parts]
            if coordinates != expected_coordinates:
                raise ValueError('Composite fragment coordinates differ from source cell')
        joined = '; '.join(expected)
        merged = dict(fragments[0], display_ref=joined, canonical_mt_ref=joined,
                      canonical_lxx_ref=joined, spans_json=json.dumps(spans, sort_keys=True),
                      identity_key='rid_' + hashlib.sha256(('scripture|' + joined + '|' + joined).encode()).hexdigest()[:20],
                      composite_fragments_json=json.dumps(fragments, sort_keys=True))
        merged['provenance'] = (str(merged.get('provenance', '')) + '; R4 composite_fragments=' + merged['composite_fragments_json']).lstrip('; ')
        position = min(index for index, _ in items)
        replacements[position] = merged
        removed.update(index for index, _ in items if index != position)
        events.append({'calendar_key': merged.get('calendar_key', ''),
                       'source_table': merged['source_table'], 'display_ref': joined,
                       'fragment_identity_keys': [row['identity_key'] for row in fragments],
                       'source_locators': [row.get('source_locator', '') for row in fragments]})
    return [replacements.get(i, row) for i, row in enumerate(result) if i not in removed], events


def _authenticate_bel():
    oracle_text = _read_authenticated(BEL_CAPTURE + '/qualified-oracle.json',
        'be41ab28f5f01f9e0ce9341b9013a26e08bec9cb5c3d979c47f99b482b7ab9a5')
    oracle = json.loads(oracle_text)
    text = _read_authenticated(BEL_CAPTURE + '/Prophecies.txt', oracle['text_sha256'])
    for witness in oracle['context_files'] + oracle['reference_screenshots']:
        _authenticated_bytes(witness['path'], witness['sha256'])
    if (oracle['civil_date'] != '2026-03-13' or oracle['service'] != 'Matins'
            or oracle['raw_reference_lines'][-1] != '\tDaniel 14:1-42'
            or '\tDaniel 14:1-42\n' not in text
            or '1 And so Daniel was living with the king' not in text
            or '42 Then the king said' not in text):
        raise ValueError('Bel retained source/context mismatch')
    return BEL_CAPTURE + '/Prophecies.txt'


def bel_identity_for(row):
    """Correct the exact legacy Bel token, preserving its raw source externally.

    Reader's Daniel 14 body is CPDV-like, not Brenton's verse-for-verse Bel.
    Bel 1 is the standalone book coordinate, with the Reader edition explicit;
    canonical MT/LXX equivalence remains blank rather than fabricated.
    """
    if (row.get('source_kind'), row.get('source_family'), row.get('source_file'),
            row.get('source_table'), row.get('calendar_key'),
            row.get('reading_slot', row.get('slot'))) != (
            'katameros_cycle', 'katameros_cycle', DATABASE, 'GreatLentReadings',
            'week 4 day_of_week 5', 'prophecy'):
        return None
    if row.get('source_ref') != 'Dan 1:1-42' or row.get('passage', row.get('display_ref')) != 'Dan 1:1-42' or not _active(row):
        return None
    if row.get('raw_ref') != '5.10:12-22*@+5.11:1-28@23.29:12-23@18.21:1-34@27.1:1-42':
        raise ValueError('Bel legacy raw source token drift')
    locator = _authenticate_bel()
    note = ('Reader Daniel 14:1-42 retained in standalone Bel coordinates; '
            'Brenton verse-for-verse equivalence not certified. Original erroneous '
            f'Dan 1:1-42 and raw locator retained; evidence={locator}; verified_date=2026-03-13')
    span = {'book': 'Bel', 'chapter_start': 1, 'verse_start': 1,
            'chapter_end': 1, 'verse_end': 42, 'source_ref': 'Daniel 14:1-42',
            'source_convention': 'reader_daniel_14_standalone_bel',
            'canonical_mt_ref': '', 'canonical_lxx_ref': '', 'confidence': 'source_coordinates',
            'validation_basis': note}
    return {'identity_key': 'rid_' + hashlib.sha256(b'scripture|Bel|reader_daniel_14:1-42').hexdigest()[:20],
            'reading_type': 'scripture', 'reading_name': '', 'source_label': 'Dan 1:1-42',
            'display_ref': 'Bel 1:1-42 (Reader Daniel 14:1-42)',
            'canonical_mt_ref': '', 'canonical_lxx_ref': '',
            'source_convention': span['source_convention'],
            'canonicalization_confidence': 'source_coordinates',
            'canonicalization_note': note, 'spans_json': json.dumps([span], sort_keys=True)}


# Published-like runtime overlay APIs. These do not change the design inventory.
RAW_CONTRACT = 'sources/resolver-review-2026-10-29/raw-fragment-contract.json'
RAW_CONTRACT_SHA256 = 'fa2a7f2ae2a09bbb90a15cbcc5a24b3b07031f6a5d60726ab044ac497b45f61e'


def _bounded_last_friday_policy():
    locator = _authenticate_last_friday()
    records = [r for r in _db_records('GreatLentReadings')
               if r['Week'] == 7 and r['DayOfWeek'] == 5]
    if len(records) != 1 or records[0]['M_Gospel_Ref'] != '42.16:19-31':
        raise ValueError('Last Friday recurrence source table disagrees')
    return {'id': 'R1_last_friday_matins_gospel_bounded',
            'day_title': LAST_FRIDAY, 'pascha_offset': -9, 'service': 'Matins',
            'slot': 'Gospel', 'normalized_ref': 'Lk 16:19-31',
            'verified_date': '2026-04-03', 'reader_evidence': locator,
            'recurrence_evidence': DATABASE + ':GreatLentReadings Week=7 DayOfWeek=5 M_Gospel_Ref',
            'scope': 'Reviewed runtime projection of this appointment only; not fresh Reader verification of every generated year'}


def _runtime_luke_identity():
    ref = 'Lk 16:19-31'
    return {'identity_key': 'rid_' + hashlib.sha256(f'scripture|{ref}|{ref}'.encode()).hexdigest()[:20],
            'display_ref': ref, 'canonical_mt_ref': ref, 'canonical_lxx_ref': ref,
            'spans_json': json.dumps([{'book': 'Lk', 'chapter_start': 16, 'verse_start': 19,
                'chapter_end': 16, 'verse_end': 31, 'source_ref': 'Luke 16:19-31',
                'source_convention': 'modern_english_reference', 'canonical_mt_ref': ref,
                'canonical_lxx_ref': ref, 'confidence': 'high',
                'validation_basis': 'R1 bounded Reader and recurring SQLite table policy'}], sort_keys=True)}


def _is_last_friday_gospel(row, ref):
    return (_active(row) and row.get('occasion', row.get('day_title')) == LAST_FRIDAY
            and _service(row) == ('matins', 'gospel') and row.get('display_ref') == ref)


def _runtime_contract():
    rows = json.loads(_read_authenticated(RAW_CONTRACT, RAW_CONTRACT_SHA256))
    return {(r['source_family'], r['source_kind'], r['source_row_id']): r for r in rows}


def _raw_for_runtime(row, contract, date=None):
    row_id = str(row.get('source_row_id') or '')
    if not row_id:
        found = re.search(r':row (\d+); source_ref=', row.get('source_locator', ''))
        row_id = found[1] if found else ''
    raw = contract.get((row.get('source_family'), row.get('source_kind'), row_id))
    if raw is None or row.get('composite_fragments_json'):
        return None
    if row.get('display_ref') != raw['passage']:
        return None
    expected_locator = ((raw['url'] + '; ') if raw['url'] else '') + raw['source_file'] + ':row ' + raw['source_row_id'] + '; source_ref=' + raw['source_ref']
    if row.get('source_locator') != expected_locator:
        raise ValueError('Runtime fragment source locator mismatch')
    context = row.get('calendar_key') or row.get('calendar_keys') or row.get('occasion')
    if (context != raw['calendar_key'] or _service(row) != _service(raw)
            or (date and raw['gregorian_date'] and date != raw['gregorian_date'])):
        raise ValueError('Runtime fragment source/date/service context mismatch')
    return raw


def _runtime_composites(rows, contract, date=None):
    hydrated = []
    for row in rows:
        raw = _raw_for_runtime(row, contract, date)
        if raw is None or raw['raw_ref'] not in COMPOSITES:
            hydrated.append(copy.deepcopy(row))
            continue
        projection = dict(row)
        for field in ('source_table', 'source_file', 'raw_ref', 'calendar_key', 'gregorian_date'):
            projection[field] = raw[field]
        # Source database aliases are needed for exact source-cell authentication.
        projection['slot'] = raw['reading_slot'] or raw['reading_type']
        projection['service_section'] = raw['service_section']
        projection['_review_original_row'] = copy.deepcopy(row)
        hydrated.append(projection)
    merged, events = merge_proven_composites(hydrated)
    output = []
    for row in merged:
        original = row.pop('_review_original_row', None)
        if original is None:
            output.append(row)
        elif not row.get('composite_fragments_json'):
            output.append(original)
        else:
            result = dict(original)
            for field in ('identity_key', 'display_ref', 'canonical_mt_ref', 'canonical_lxx_ref',
                          'spans_json', 'provenance', 'composite_fragments_json'):
                result[field] = row[field]
            output.append(result)
    return output, events


def _runtime_bel(row, contract, date=None):
    raw = _raw_for_runtime(row, contract, date)
    if raw is None or raw['passage'] != 'Dan 1:1-42':
        return row
    ident = bel_identity_for(raw)
    if ident is None:
        raise ValueError('Bel runtime source qualification failed')
    original = copy.deepcopy(row)
    result = dict(row, **ident)
    result['resolver_review_disclosure'] = json.dumps({'id': 'R6', 'original': original,
        'source': BEL_CAPTURE + '/qualified-oracle.json',
        'coordinate_qualification': 'Reader standalone Bel coordinates; no certified Brenton/MT equivalence'}, sort_keys=True)
    return result


def repair_daily_rows(date, rows):
    """Return (published-like daily rows, events), preserving original sources.

    Call AFTER the package's canonicalization/structural fill. The trusted outer
    civil date is required and is never derived from a mutable row field.
    """
    date_value = dt.date.fromisoformat(date)
    contract = _runtime_contract()
    result, events = copy.deepcopy(rows), []
    targets = [r for r in result if _is_last_friday_gospel(r, 'Lk 17:20-37')
               and r.get('source_family') == 'ordinary_date_resolved'
               and r.get('source_kind') == 'copticchurch_date']
    if targets and (date_value - pascha(date_value.year)).days == -9:
        if len(targets) != 1:
            raise ValueError('R1 duplicate runtime Matins Gospel')
        if _raw_for_runtime(targets[0], contract, date) is None:
            raise ValueError('R1 runtime source witness missing')
        policy = _bounded_last_friday_policy()
        original = copy.deepcopy(targets[0])
        targets[0].update(_runtime_luke_identity(), current_status='current_confirmed_coptic_reader',
            resolver_review_disclosure=json.dumps({'policy': policy, 'original': original}, sort_keys=True))
        events.append({'id': 'R1', 'date': date, 'before': 'Lk 17:20-37', 'after': 'Lk 16:19-31'})
    bel_result = [_runtime_bel(row, contract, date) if _active(row) else row for row in result]
    events.extend({'id': 'R6', 'date': date, 'after': after['display_ref']}
                  for before, after in zip(result, bel_result) if before != after)
    result = bel_result
    result, merges = _runtime_composites(result, contract, date)
    events.extend(dict(event, id='R4', date=date) for event in merges)
    for order, row in enumerate(result, 1):
        row['reading_order'] = order
    return result, events


def repair_reverse_rows(rows, daily_by_year=None):
    """Return (published-like reverse rows, events), after canonicalization.

    Retain superseded R1 source witnesses as historical rows. The already present
    Reader Luke16 appointment receives the bounded runtime recurrence disclosure.
    R3 annotations require the FINAL daily output supplied by the owning caller.
    """
    result, events = copy.deepcopy(rows), []
    contract = _runtime_contract()
    old = [r for r in result if _is_last_friday_gospel(r, 'Lk 17:20-37')
           and (r.get('source_family'), r.get('source_kind')) == ('ordinary_date_resolved', 'copticchurch_date')]
    if old:
        current = [r for r in result if _is_last_friday_gospel(r, 'Lk 16:19-31')
                   and r.get('source_family') == 'coptic_reader_verified_calendar_boundary']
        if len(old) != 1 or len(current) != 1:
            raise ValueError('R1 expected one legacy and one Reader reverse appointment')
        if _raw_for_runtime(old[0], contract) is None:
            raise ValueError('R1 runtime source witness missing')
        policy = _bounded_last_friday_policy()
        original = copy.deepcopy(old[0])
        disclosure = json.dumps({'policy': policy, 'superseded_source': original}, sort_keys=True)
        old[0].update(current_status='historical_witness',
                      removed_marker='R1 superseded by bounded Reader Last Friday Matins policy',
                      resolver_review_disclosure=disclosure)
        current[0]['resolver_review_disclosure'] = disclosure
        events.append({'id': 'R1', 'before': 'Lk 17:20-37', 'after': 'Lk 16:19-31', 'raw_witness_retained': True})
    bel_result = [_runtime_bel(row, contract) if _active(row) else row for row in result]
    events.extend({'id': 'R6', 'after': after['display_ref']}
                  for before, after in zip(result, bel_result) if before != after)
    result = bel_result
    result, merges = _runtime_composites(result, contract)
    events.extend(dict(event, id='R4') for event in merges)
    if daily_by_year is not None:
        result = [annotate_calendar_occurrence(row, daily_by_year) for row in result]
    return result, events
