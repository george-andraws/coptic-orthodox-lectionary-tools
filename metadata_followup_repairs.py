"""Source-qualified T-L/LK metadata at the final package projection boundary.

No lifecycle, reading endpoint, source title, raw key or source disclosure is
changed. Run after the Mark overlay. The predecessor fixture is source evidence,
not a replacement for the unchanged whole-corpus release membership guard.
"""
from __future__ import annotations

import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
FIXTURE = 'sources/metadata-followup-1.3.8/published-1.3.7.json.gz'
FIXTURE_SHA256 = '6b08ce872a07b2849a8ddc05c8db759648ee50e3b5f6a693df392f81da02c5ba'
SOURCE_HASHES = {
    'out/data/katameros_cycle_passage_index.csv': '56756b063813c36c81439d178ac605eac490c79316b2a749d231d281dc08e184',
    'sources/katameros-api/Core/Repositories/ReadingsRepository.cs': '3638b061903f1ed94d2f711fcc815a6bfe142dfc479d582c55708a90dc36937d',
}
KATAMEROS = ('katameros_cycle', 'katameros_cycle')
ORDINARY = ('ordinary_date_resolved', 'copticchurch_date')
GENERIC_CYCLES = {'Great Lent/Jonah/Nineveh cycle': 'great_lent',
                  'Holy Fifty Days/Pentecost cycle': 'holy_fifty'}
GENERATED_OVERLAY = 'generated current-date overlay from local Holy Week source'
WEEKDAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
ORDINALS = ('first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh')
MONTHS = ('Tout', 'Baba', 'Hatour', 'Kiahk', 'Toba', 'Amshir', 'Baramhat',
          'Baramouda', 'Bashans', 'Paona', 'Abib', 'Mesra', 'Nasie')
MONTH_SLUGS = tuple(s.lower() for s in MONTHS)
MONTH_ALIASES = {
    'tut': 'Tout', 'thoout': 'Tout', 'babah': 'Baba', 'hatur': 'Hatour',
    'hator': 'Hatour', 'hatoor': 'Hatour', 'kiyahk': 'Kiahk', 'kiyank': 'Kiahk',
    'kiak': 'Kiahk', 'tubah': 'Toba', 'tobe': 'Toba', 'meshir': 'Amshir',
    'barmuda': 'Baramouda', 'baramoudah': 'Baramouda', 'baramudah': 'Baramouda',
    'bashons': 'Bashans', 'baunah': 'Paona', 'misra': 'Mesra',
    'al-nasi': 'Nasie', 'nesi': 'Nasie',
    **{name.lower(): name for name in MONTHS},
}
MONTH_PATTERN = re.compile(r'\b(' + '|'.join(sorted(MONTH_ALIASES, key=len, reverse=True)) + r')\b', re.I)
BARE = re.compile(r'week (\d+) day_of_week (\d+)')
LK1_FLAG = 'LK1_abib_26_conflicting_gospel_sets'
CHANGED_FIELDS = frozenset({
    'display_label', 'occurs_in_shipped_years', 'normalized_season',
    'normalized_calendar_keys', 'cycle_label_status', 'display_commemoration_titles',
    'commemoration_join_basis', 'metadata_review_flags', 'attestation_years',
    'attestation_year_min', 'attestation_year_max', 'attestation_years_basis',
    'synthetic_overlay_years',
})
# These fields identify the retained appointment, never merely its shared rid.
SOURCE_FIELDS = ('source_family', 'source_kind', 'source_locator', 'source_title',
                 'source_edition', 'calendar_keys', 'service_section', 'service_hour',
                 'slot', 'identity_key', 'canonical_mt_ref')


def _authenticated(relative, digest):
    path = ROOT / relative
    if path.is_symlink():
        raise ValueError('metadata follow-up source symlink rejected')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError('metadata follow-up source authentication failed: ' + relative)
    return data


@lru_cache(maxsize=1)
def _decode_fixture(data):
    return json.loads(gzip.decompress(data))


def baseline():
    """Return hash-authenticated predecessor source observations, read-only."""
    return _decode_fixture(_authenticated(FIXTURE, FIXTURE_SHA256))


def _signature(row):
    # Calendar splitting can retain one locator/rid in several fixed-day rows.
    # Never collapse those distinct predecessor witnesses during inverse lookup.
    return tuple(row.get(k, '') for k in SOURCE_FIELDS + ('coptic_date_key', 'annual_sunday'))


@lru_cache(maxsize=1)
def _source_index(fixture_bytes):
    frozen = _decode_fixture(fixture_bytes)
    rows = list(frozen['reverse_rows'])
    for days in frozen['daily'].values():
        rows.extend(r for readings in days.values() for r in readings)
    by_signature = {}
    by_anchor = defaultdict(list)
    for row in rows:
        by_signature[_signature(row)] = row
        by_anchor[(row.get('identity_key'), row.get('source_locator'))].append(row)
    return by_signature, by_anchor


@lru_cache(maxsize=1)
def _cycle_source(data, implementation):
    # The C# caller uses System.DateTime.DayOfWeek cast to int, not Python's
    # Monday-zero weekday. Retained Palm Sunday and Ascension names corroborate
    # Sunday=0 and Thursday=4 independently in the actual source table.
    text = implementation.decode()
    if 'int dayNumber = (int)date.DayOfWeek;' not in text:
        raise ValueError('metadata follow-up source weekday protocol changed')
    rows = list(csv.DictReader(io.StringIO(data.decode())))
    assert any(r['day_key'] == 'week 7 day_of_week 0' and r['day_name'] == 'Readings for Palm Sunday' for r in rows)
    assert any(r['day_key'] == 'week 6 day_of_week 4' and 'Ascension' in r['day_name'] for r in rows)
    return rows


def _sources():
    fixture = _authenticated(FIXTURE, FIXTURE_SHA256)
    by_signature, by_anchor = _source_index(fixture)
    cycle_data, implementation = [_authenticated(p, h) for p, h in SOURCE_HASHES.items()]
    return by_signature, by_anchor, _cycle_source(cycle_data, implementation)


def bare_cycle_keys(row):
    return [k for k in str(row.get('calendar_keys', '')).split(' || ') if BARE.fullmatch(k)]


def normalize_month_words(label):
    return MONTH_PATTERN.sub(lambda match: MONTH_ALIASES[match[0].lower()], label)


def is_current(row):
    """The package's supported current states, for report scope only."""
    if row.get('active') is False or row.get('status') == 'removed' or row.get('removed_marker'):
        return False
    status = str(row.get('current_status') or row.get('status') or '').lower().strip()
    if not status:
        return True
    if status == 'removed' or status.startswith('superseded') or status in {'historical_candidate_removed', 'historical_witness'}:
        return False
    if status in {'current', 'current_public_or_local_reference', 'current_working_source_not_coptic_reader_checked',
                  'current_confirmed_coptic_reader', 'current_confirmed_by_fixture_equivalence', 'pending_psalm_equivalence_unresolved'}:
        return True
    raise ValueError('metadata follow-up unknown explicit reading status: ' + status)


def _cycle_label(season, key):
    week, day = map(int, BARE.fullmatch(key).groups())
    if not 0 <= day <= 6:
        raise ValueError('metadata follow-up source weekday outside protocol')
    special = {
        ('great_lent', 99, 0): 'Preparation Sunday',
        ('great_lent', 99, 6): 'Preparation Saturday',
        ('great_lent', 7, 6): 'Lazarus Saturday',
        ('great_lent', 7, 0): 'Palm Sunday',
        ('holy_fifty', 0, 0): 'Feast of the Resurrection',
        ('holy_fifty', 1, 0): 'Thomas Sunday',
        ('holy_fifty', 6, 4): 'Feast of the Ascension',
        ('holy_fifty', 7, 0): 'Feast of Pentecost',
    }.get((season, week, day))
    if special:
        return special, 'source_mapped'
    if week == 49 and season == 'great_lent':
        return 'Wednesday of Great Lent (source week 49 unresolved)', 'unresolved_source_week_49'
    if not 1 <= week <= 7:
        raise ValueError('metadata follow-up source cycle week unmapped: ' + key)
    suffix = 'Great Lent' if season == 'great_lent' else 'the holy fifty days'
    return f'{WEEKDAYS[day]} of the {ORDINALS[week - 1]} week of {suffix}', 'source_mapped'


def _lk1(row):
    return row.get('coptic_date_key') == 'abib-26' and row.get('slot_type') == 'gospel' and (
        row.get('source_family'), row.get('source_kind')) in {KATAMEROS, ORDINARY}


def _lk4(row):
    return ((row.get('annual_sunday') == 'mesra-4' and _service(row) == 'Vespers'
             and row.get('canonical_mt_ref') in {'Lk 17:20-36', 'Lk 17:20-37'})
            or (row.get('coptic_date_key') == 'tout-8' and _service(row) == 'Liturgy'
                and row.get('canonical_mt_ref') in {'Matt 23:13-26', 'Matt 23:13-36'}))


def repair_rows(rows):
    """One-to-one additive metadata transform; never drops or promotes rows."""
    exact, anchors, cycles = _sources()
    synaxarium = baseline()['synaxarium']
    output = []
    for row in rows:
        out = dict(row)
        source = exact.get(_signature(row))
        cycle_keys = bare_cycle_keys(row)
        known = anchors.get((row.get('identity_key'), row.get('source_locator')), [])
        scoped = cycle_keys or row.get('normalized_season') or _lk1(row) or row.get('provenance') == GENERATED_OVERLAY
        # Recognize stripped/rebound targeted contexts without a mutable family.
        if not source and (scoped or any(bare_cycle_keys(r) or _lk1(r) for r in known)):
            raise ValueError('metadata follow-up source context mismatch: ' + str(row.get('source_locator')))
        label = normalize_month_words(row.get('display_label') or row.get('occasion', ''))
        label = re.sub(r'^(?:the\s+)?(first|second|third|fourth|fifth) Sunday of ',
                       lambda match: match[1].capitalize() + ' Sunday of ', label, flags=re.I)
        if source:
            annual = source.get('annual_sunday', '')
            if annual:
                month, ordinal = annual.rsplit('-', 1)
                if month in MONTH_SLUGS and 1 <= int(ordinal) <= 5:
                    label = f'{ORDINALS[int(ordinal)-1].capitalize()} Sunday of {MONTHS[MONTH_SLUGS.index(month)]}'
            if cycle_keys:
                if (source['source_family'], source['source_kind']) != KATAMEROS:
                    raise ValueError('metadata follow-up source cycle family/kind mismatch')
                season = GENERIC_CYCLES.get(source['occasion'])
                if not season:
                    raise ValueError('metadata follow-up source cycle season missing')
                match = re.search(r':row (\d+);', source['source_locator'])
                if not match:
                    raise ValueError('metadata follow-up source cycle locator missing')
                # Published locators can retain an earlier materialization's
                # row ordinal. Authenticate their literal bytes in the fixture,
                # then join the source by complete table/key/slot context instead
                # of reinterpreting an old ordinal against a different CSV.
                table = 'GreatLentReadings' if season == 'great_lent' else 'PentecostReadings'
                if any(not any(c['source_table'] == table and c['day_key'] == key
                               and c['reading_slot'] == source['slot'] for c in cycles)
                       for key in cycle_keys):
                    raise ValueError('metadata follow-up source cycle table/key mismatch')
                mapped = [_cycle_label(season, key) for key in cycle_keys]
                label = ' / '.join(value for value, status in mapped)
                out.update(normalized_season=season,
                           normalized_calendar_keys=[f'{season}:{key}' for key in cycle_keys],
                           cycle_label_status='unresolved_source_week_49' if any(s != 'source_mapped' for _, s in mapped) else 'source_mapped')
            if source.get('coptic_date_key') == 'hatour-24':
                titles = [entry['title'] for entry in synaxarium['hatour-24']['commemorations']]
                out.update(display_commemoration_titles=titles, commemoration_join_basis='coptic_date_only')
                label = 'Hatour 24 (' + titles[0] + ')'
            if _lk1(source):
                out['metadata_review_flags'] = sorted(set(row.get('metadata_review_flags', [])) | {LK1_FLAG})
            if _lk4(source):
                out['metadata_review_flags'] = sorted(set(row.get('metadata_review_flags', [])) | {'LK4_range_variant_no_endpoint_change'})
            if source.get('provenance') == GENERATED_OVERLAY:
                out.update(attestation_years='', attestation_year_min='', attestation_year_max='',
                           attestation_years_basis='synthetic_movable_overlay_not_dated_source_observations',
                           synthetic_overlay_years=source.get('attestation_years', ''))
        if row.get('removed_marker'):
            out['occurs_in_shipped_years'] = False
        out['display_label'] = label
        output.append(out)
    return output


def restore_rows_for_comparison(rows, *, date=None, previous_layer='mark', annotated=False):
    """Authenticate this layer's full metadata delta, then undo only that delta.

    The trusted caller selects ``mark`` for Mark's exact complete-table guard,
    or ``calendar`` for the old calendar metadata qualifier. Other worker layers
    must undo their own changes first, in reverse projection order. Membership,
    order, endpoints, lifecycle and all foreign fields remain untouched so the
    existing guards still detect additions, deletions and source corruption.
    """
    if previous_layer not in {'mark', 'calendar'}:
        raise ValueError('metadata follow-up unsupported prior projection')
    frozen = baseline()
    originals = frozen['reverse_rows'] if date is None else frozen['daily'].get(date[:4], {}).get(date, [])
    index = {_signature(r): r for r in originals}
    if date is None:
        # LK5 precedes metadata. Its 52 new inactive identities are independently
        # reconstructed from authenticated published witnesses and source cells.
        import composite_followup_repairs as composite
        for group in composite._witness_groups():
            original = composite._merged(group)
            index[_signature(original)] = original
    known_ids = {r.get('identity_key') for r in originals}
    known_locators = {r.get('source_locator') for r in originals}
    output = []
    recognized = []
    import mark_followup_repairs as mark
    for position, row in enumerate(rows):
        source = index.get(_signature(row))
        if annotated and date is None and source is not None and mark.rule(source) == 'L1':
            # Trusted final-occurrence lane: L1 has no surviving daily reading.
            # Historical, pre-occurrence callers retain their original bit.
            source = dict(source, occurs_in_shipped_years=False)
        if source is None:
            # Out-of-scope rows must not carry this layer's positive claims.
            owned = CHANGED_FIELDS - {'display_label', 'occurs_in_shipped_years',
                                      'attestation_years', 'attestation_year_min', 'attestation_year_max'}
            if (owned.intersection(row) or row.get('identity_key') in known_ids
                    or row.get('source_locator') in known_locators):
                raise ValueError('metadata follow-up source restoration context mismatch')
            output.append(dict(row))
            continue
        prior = dict(row)
        for field in CHANGED_FIELDS:
            if field in source:
                prior[field] = source[field]
            else:
                prior.pop(field, None)
        # Reconstruct Mark's preceding label from immutable predecessor bytes.
        prior['display_label'] = mark.display_label(source)
        output.append(prior)
        recognized.append((position, source))
    expected_rows = repair_rows([output[position] for position, source in recognized])
    for (position, source), expected in zip(recognized, expected_rows):
        row = rows[position]
        for field in CHANGED_FIELDS:
            if ((field in row) != (field in expected) or
                    (field in row and (type(row[field]) is not type(expected[field]) or row[field] != expected[field]))):
                raise ValueError('metadata follow-up authenticated restoration delta mismatch: ' + field)
        if previous_layer == 'calendar':
            if 'display_label' in source:
                output[position]['display_label'] = source['display_label']
            else:
                output[position].pop('display_label', None)
    return output


def restore_daily_for_comparison(days, *, previous_layer='mark'):
    return {date: restore_rows_for_comparison(rows, date=date, previous_layer=previous_layer)
            for date, rows in days.items()}


def repair_daily(days):
    """Preserve each trusted outer date, every appointment and physical order."""
    return {date: repair_rows(rows) for date, rows in days.items()}


def validate_rows(rows):
    """Whole inventory metadata invariants; no membership-policy replacement."""
    contexts = defaultdict(set)
    expected_rows = repair_rows(rows)
    for row, expected_row in zip(rows, expected_rows):
        for field in CHANGED_FIELDS:
            if field in expected_row and (type(row.get(field)) is not type(expected_row[field]) or row.get(field) != expected_row[field]):
                raise ValueError('metadata follow-up projected field mismatch: ' + field)
        if row.get('removed_marker') and row.get('occurs_in_shipped_years') is not False:
            raise ValueError('metadata follow-up removed witness reports occurrence')
        label = row.get('display_label', '')
        if normalize_month_words(label) != label or re.match(r'^the (first|second|third|fourth|fifth) Sunday', label, re.I):
            raise ValueError('metadata follow-up noncanonical display month or Sunday label')
        keys = bare_cycle_keys(row)
        if keys:
            season = row.get('normalized_season')
            if season not in set(GENERIC_CYCLES.values()) or row.get('normalized_calendar_keys') != [f'{season}:{k}' for k in keys]:
                raise ValueError('metadata follow-up ambiguous bare cycle context')
            expected = [_cycle_label(season, key) for key in keys]
            if label != ' / '.join(value for value, _ in expected):
                raise ValueError('metadata follow-up unusable cycle display label')
            if is_current(row):
                for raw, normalized in zip(keys, row['normalized_calendar_keys']):
                    contexts[normalized].add(season)
        if row.get('provenance') == GENERATED_OVERLAY and any(row.get(f) for f in ('attestation_years', 'attestation_year_min', 'attestation_year_max')):
            raise ValueError('metadata follow-up synthetic overlay reports source attestation')
    if any(len(seasons) > 1 for seasons in contexts.values()):
        raise ValueError('metadata follow-up active normalized week key crosses seasons')
    return True


def _service(row):
    service = row.get('service_section', '')
    if (row.get('source_family'), row.get('source_kind')) == KATAMEROS:
        return service.split('_', 1)[0].capitalize()
    return service


def _contexts(row):
    if row.get('annual_sunday'):
        return ['annual_sunday:' + row['annual_sunday']]
    if row.get('coptic_date_key'):
        return ['coptic_date:' + row['coptic_date_key']]
    if row.get('normalized_calendar_keys'):
        return row['normalized_calendar_keys']
    return ['occasion:' + row.get('occasion', '')]


def _locator_dates(row):
    dates = set()
    for locator in [row.get('source_locator', ''), *row.get('calendar_review_source_locators', [])]:
        parsed = urlparse(locator.split(';', 1)[0])
        if parsed.netloc != 'copticchurch.net' or parsed.path != '/readings':
            continue
        query = parse_qs(parsed.query)
        if all(len(query.get(k, [])) == 1 for k in ('g_year', 'g_month', 'g_day')):
            dates.add(dt.date(*(int(query[k][0]) for k in ('g_year', 'g_month', 'g_day'))).isoformat())
    return dates


def endpoint_conflicts(rows):
    """Report-only same-start/different-end source variants, exact date/slots.

    Counts are appointment context/service/slot/book/start groups, not pairwise
    combinations. Dates come only from retained dated locators, never invented
    recurrence. Split multi-span readings are not mistaken for endpoint variants.
    """
    groups = defaultdict(list)
    for row in repair_rows(rows):
        if not is_current(row) or not row.get('canonical_mt_ref'):
            continue
        spans = json.loads(row.get('spans_json') or '[]')
        if len(spans) != 1:
            continue
        span = spans[0]
        # Compare approved MT coordinates, not source-frame numeric fields.
        match = re.fullmatch(r'(.+?) (\d+):(\d+)(?:-(?:(\d+):)?(\d+))?', row['canonical_mt_ref'])
        if not match:
            continue
        book, chapter, verse = match[1], int(match[2]), int(match[3])
        end = (int(match[4] or chapter), int(match[5] or verse))
        for context in _contexts(row):
            key = (context, _service(row), row.get('service_hour', ''), row.get('slot_type') or row.get('slot'),
                   book, chapter, verse)
            groups[key].append((row, end))
    output = []
    for key, group in sorted(groups.items(), key=lambda item: str(item[0])):
        if len({end for _, end in group}) < 2 or len({(r['source_family'], r['source_kind']) for r, _ in group}) < 2:
            continue
        context, service, hour, slot, book, chapter, verse = key
        output.append(dict(context=context, service=service, hour=hour, slot=slot,
                           start=f'{book} {chapter}:{verse}',
                           references=sorted({r['canonical_mt_ref'] for r, _ in group}),
                           dates=sorted(set().union(*(_locator_dates(r) for r, _ in group))),
                           witnesses=[{k: r.get(k, '') for k in ('identity_key', 'source_family', 'source_kind',
                                      'source_locator', 'calendar_keys', 'display_ref', 'current_status')} for r, _ in group]))
    return output


def timothy_confirmations():
    """Exactly seven dated appointments, low priority without status promotion."""
    wanted = {'1Tim 1:12-19': 'First Sunday of Tut',
              '1Tim 2:1-3:4': 'Thursday of the sixth week of Great Lent',
              '1Tim 3:13-16': 'The Feast of the Ascension',
              '1Tim 4:9-5:10': 'Great Thursday', '1Tim 5:17-6:2': 'Hatur 24',
              '1Tim 6:3-16': 'Third Sunday of Abib', '1Tim 6:3-21': 'Fourth Sunday of Babah'}
    rows = baseline()['reverse_rows']
    output = []
    for reference, occasion in wanted.items():
        selected = [r for r in rows if r.get('canonical_mt_ref') == reference and r.get('occasion') == occasion
                    and (r.get('source_family'), r.get('source_kind')) == ORDINARY]
        # Published 1.3.7 already replaced the Great Thursday water appointment
        # with retained Reader evidence. No copticchurch locator is present for
        # that service in its reverse or daily arrays; do not fabricate one.
        if not selected and reference == '1Tim 4:9-5:10':
            selected = [r for r in rows if r.get('canonical_mt_ref') == reference
                        and r.get('source_family') == 'coptic_reader_qualified_pascha_hour'
                        and r.get('service_section') == 'Liturgy of Blessing of the Water']
        if not selected:
            raise ValueError('metadata follow-up source missing Timothy confirmation: ' + reference)
        selected.sort(key=lambda r: r['source_locator'])
        row = selected[0]
        output.append({**{k: row.get(k, '') for k in ('identity_key', 'occasion', 'service_section', 'display_ref',
                       'source_locator', 'current_status', 'source_family', 'source_kind')},
                       'priority': 'low', 'action': 'confirm, no change expected'})
    return output
