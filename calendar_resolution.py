"""Pure, source-boundary calendar collision resolution for generated artifacts."""
from __future__ import annotations

import copy
from contextlib import closing
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Iterable

from passage_normalization import canonicalize_text_ref, normalize_numeric_ref
from reading_context_overlays import is_current_source_row

WORK = Path(__file__).resolve().parent
LAST_FRIDAY_TITLE = "Friday of the seventh week of Great Lent"
BOUNDARY_SOURCE = "Coptic Reader verified calendar boundary"


ANNUNCIATION_EXCEPTION = (
    "UK Midlands Katameros Days p.22 rule 13: Annunciation yields during the "
    "non-repeatable Lord-events window"
)


def julian_pascha_gregorian(year: int) -> dt.date:
    """Return Orthodox Pascha using the Julian computus, expressed Gregorian."""
    a, b, c = year % 4, year % 7, year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    julian = dt.date(year, 3, 22) + dt.timedelta(days=d + e)
    return julian + dt.timedelta(days=13)


def holy_week_day(date_value: dt.date) -> str | None:
    offset = (date_value - julian_pascha_gregorian(date_value.year)).days
    return {-6: "Monday", -5: "Tuesday", -4: "Wednesday", -3: "Great Thursday", -2: "Good Friday"}.get(offset)


def _reading_type(slot: str, ref: str) -> str:
    if slot == "Psalm+Gospel":
        return "Psalm" if re.match(r"^Ps(?:alm)?\s", ref) else "Gospel"
    if slot.startswith("OT"):
        return "Prophecy"
    return slot


def load_last_friday_boundary() -> tuple[dict, dict]:
    """Authenticate the complete primary table, not a guessed extended season.

    The prophecy supplement is part of this feast-collision table only. Generic
    recurring_date_supplements remain independent and are not expanded here.
    """
    overlay = json.loads((WORK / 'sources/lectionary_corrections.json').read_text())
    rules = overlay.get('calendar_boundary_tables', [])
    if len(rules) != 1:
        raise RuntimeError('Last Friday boundary requires exactly one source-qualified table')
    rule = rules[0]
    if (rule.get('day_title'), rule.get('pascha_offset_days'), rule.get('feast_collision'), rule.get('verified_date')) != (LAST_FRIDAY_TITLE, -9, 'Annunciation', '2028-04-07'):
        raise RuntimeError('Unsupported Last Friday boundary context/offset')
    path = WORK / rule['evidence']
    if hashlib.sha256(path.read_bytes()).hexdigest() != overlay['source_fingerprints'].get(rule['evidence']):
        raise RuntimeError('Last Friday boundary fixture source drift')
    table = json.loads(path.read_text())
    if (table.get('verified_date'), table.get('coptic_date'), table.get('occasion'), table.get('day_title'), table.get('pascha_offset_days'), table.get('feast_collision'), table.get('suppressed_service')) != ('2028-04-07', 'Paremhotep 29, 1744', 'Last Friday of Great Fast', LAST_FRIDAY_TITLE, -9, 'Annunciation', 'Vespers'):
        raise RuntimeError('Last Friday primary date/occasion/service qualification disagrees')
    if table.get('recurring_prophecy_context') != {'day_title': LAST_FRIDAY_TITLE, 'pascha_offset_days': -9, 'requires_feast_collision': 'Annunciation', 'source_document': 'Matins-Prophecies.txt'}:
        raise RuntimeError('Last Friday prophecy supplement context disagrees')
    fingerprints = table['source_fingerprints']
    if set(fingerprints) != {p.name for p in path.parent.iterdir() if p.is_file() and p != path}:
        raise RuntimeError('Last Friday primary evidence inventory disagrees')
    for name, expected_hash in fingerprints.items():
        if Path(name).name != name or hashlib.sha256((path.parent / name).read_bytes()).hexdigest() != expected_hash:
            raise RuntimeError(f'Last Friday primary source drift: {name}')
    home = (path.parent / 'home-selected.txt').read_text()
    if not home.startswith('Selected Season Last Friday of Great Fast Paremhotep 29, 1744 Friday, April 7, 2028'):
        raise RuntimeError('Last Friday selected primary date/occasion disagrees')
    capture = json.loads((path.parent / 'capture-manifest.json').read_text())
    if any(d['date'] != table['verified_date'] or d['context'] != 'exception-2028-04-07' for d in capture):
        raise RuntimeError('Last Friday capture date/occasion disagrees')
    rubric = (path.parent / 'Vespers.txt').read_text()
    if 'Vespers and Vesper Praises are not prayed' not in rubric or 'weekdays of the Great Fast' not in rubric:
        raise RuntimeError('Last Friday no-Vespers rubric absent')
    # Derive exact order and service/type from actual documents, not fixture rows.
    documents = [
        ('Matins-Prophecies.txt', 'Matins', ['Prophecy'] * 4),
        ('Matins-Psalm_and_Gospel.txt', 'Matins', ['Psalm', 'Gospel']),
        ('Liturgy-Pauline_Epistle.txt', 'Liturgy', ['Pauline Epistle']),
        ('Liturgy-Catholic_Epistle.txt', 'Liturgy', ['Catholic Epistle']),
        ('Liturgy-Praxis.txt', 'Liturgy', ['Acts']),
        ('Liturgy-Psalm_and_Gospel.txt', 'Liturgy', ['Psalm', 'Gospel']),
    ]
    expected = []
    for name, service, types in documents:
        text = (path.parent / name).read_text()
        printed = [line.strip() for line in text.splitlines() if re.fullmatch(r'\t(?:[1-3] )?[A-Za-z ]+ \d+:.*', line)]
        if len(printed) != len(types):
            raise RuntimeError(f'Last Friday incomplete primary document: {name}')
        expected.extend((name, service, kind, ref, heading) for heading, (kind, ref) in enumerate(zip(types, printed), 1))
    readings = table['readings']
    actual = [(r['evidence'], r['service_section'], r['reading_type'], r['printed_ref'], r['heading_order']) for r in readings]
    if actual != expected or [r['source_order'] for r in readings] != list(range(1, 12)):
        raise RuntimeError('Last Friday complete table missing/reordered/duplicate or wrong service')
    for reading in readings:
        kind = reading['reading_type']
        if kind != 'Psalm':
            canonical = canonicalize_text_ref(reading['printed_ref'])
        else:
            matins = reading['service_section'] == 'Matins'
            canonical = 'Ps 32:10-11' if matins else 'Ps 98:8-9'
            witness = 'nkjv-psalm-32.txt' if matins else 'nkjv-psalm-98.txt'
            text = (path.parent / witness).read_text()
            aligned = ('mercy shall surround him' in text and 'upright in heart' in text) if matins else bool(re.search(r'8 Let the rivers clap their hands; Let the hills be joyful together 9 before the Lord', text))
            if not aligned or reading.get('normalization_evidence') != witness or reading.get('canonicalization_confidence') != 'confirmed_text_aligned':
                raise RuntimeError('Last Friday Psalm verse normalization unresolved')
        if reading['normalized_ref'] != canonical:
            raise RuntimeError('Last Friday normalized reference truncated or disagrees with primary')
        if reading['source_slot'] != (f"OT{reading['source_order']}" if kind == 'Prophecy' else kind):
            raise RuntimeError('Last Friday source slot/order disagrees')
    return rule, table


def last_friday_collision_rows(date_value: dt.date, date_rows: list[dict]) -> list[dict]:
    rule, table = load_last_friday_boundary()
    if any(row.get('day_title') != rule['feast_collision'] for row in date_rows):
        raise RuntimeError('Last Friday boundary mixed/overlapping upstream contexts')
    return [{
        'source': BOUNDARY_SOURCE, 'gregorian_date': date_value.isoformat(),
        'weekday': date_value.strftime('%A'), 'day_title': rule['day_title'],
        'service_section': reading['service_section'], 'reading_type': reading['reading_type'],
        'raw_ref': reading['printed_ref'], 'normalized_ref': reading['normalized_ref'],
        'parse_status': 'source_boundary_overlay',
        'normalization_warning': (f"{ANNUNCIATION_EXCEPTION}; evidence={rule['evidence']}; verified_date={table['verified_date']}; " + reading.get('canonicalization_note', '')).rstrip(),
        'url': 'https://copticreader.org/app/#/document',
        'source_order': reading['source_order'], 'source_slot': reading['source_slot'],
        'source_raw_refs': reading['printed_ref'], 'correction_source': rule['evidence'],
        'source_convention': reading.get('source_convention', ''),
        'canonicalization_confidence': reading.get('canonicalization_confidence', ''),
        'canonicalization_note': reading.get('canonicalization_note', ''),
    } for reading in table['readings']]


def resolve_current_date_rows(raw_rows: Iterable[dict], pascha_rows: Iterable[dict]) -> list[dict]:
    """Overlay documented Holy Week and verified Last Friday feast collisions.

    Raw source rows are copied and never relabelled. Unsupported collision shapes
    fail closed instead of guessing a broader movable-season endpoint.
    """
    rows = [copy.deepcopy(row) for row in raw_rows]
    pascha = [copy.deepcopy(row) for row in pascha_rows]
    by_date: dict[str, list[dict]] = {}
    for row in rows:
        by_date.setdefault(row.get("gregorian_date", ""), []).append(row)
    sunday_oracle = load_sunday_evidence() if any(
        date_text and (any(r.get('source') == SUNDAY_SOURCE for r in date_rows)
        or (sunday_policy_selection(dt.date.fromisoformat(date_text))
        and any(_ordinary_sunday_context(r.get("day_title", "")) for r in date_rows)))
        for date_text, date_rows in by_date.items()) else {}
    resolved: list[dict] = []
    for date_text, date_rows in by_date.items():
        if sunday_oracle and date_text:
            date_rows = sunday_policy_rows(dt.date.fromisoformat(date_text), date_rows, sunday_oracle)
        is_annunciation = any("annunciation" in row.get("day_title", "").casefold() for row in date_rows)
        if not is_annunciation:
            resolved.extend(date_rows)
            continue
        date_value = dt.date.fromisoformat(date_text)
        if (date_value - julian_pascha_gregorian(date_value.year)).days == -9:
            resolved.extend(last_friday_collision_rows(date_value, date_rows))
            continue
        day = holy_week_day(date_value)
        if day is None:
            resolved.extend(date_rows)
            continue
        occasions = {day, f"{day} Eve"}
        replacements = [row for row in pascha if row.get("day") in occasions]
        if not replacements:
            raise RuntimeError(f"Unsupported Annunciation collision on {date_text}: no source-backed {day} rows")
        seen: set[tuple[str, str, str, str]] = set()
        for source_row in replacements:
            for ref in (part.strip() for part in source_row.get("refs", "").split(";") if part.strip()):
                key = (source_row["day"], source_row.get("hour", ""), source_row.get("slot", ""), ref)
                if key in seen:
                    continue
                seen.add(key)
                resolved.append({
                    "source": "generated current-date overlay from local Holy Week source",
                    "gregorian_date": date_text,
                    "weekday": date_value.strftime("%A"),
                    "day_title": source_row["day"],
                    "service_section": source_row.get("hour", ""),
                    "reading_type": _reading_type(source_row.get("slot", ""), ref),
                    "raw_ref": ref,
                    "normalized_ref": ref,
                    "parse_status": "calendar_overlay",
                    "normalization_warning": ANNUNCIATION_EXCEPTION,
                    "url": "",
                    "source_occasion": source_row["day"],
                    "source_order": source_row.get("order", ""),
                    "source_slot": source_row.get("slot", ""),
                    "source_raw_refs": source_row.get("raw_refs", "") or source_row.get("refs", ""),
                    "correction_source": source_row.get("correction_source", ""),
                })
    return sorted(resolved, key=lambda row: (
        row.get("gregorian_date", ""), row.get("source_occasion", row.get("day_title", "")),
        (int(row["source_order"]) if row.get("source") == SUNDAY_SOURCE else 0),
        ({'Matins': '0', 'Liturgy': '1'}[row['service_section']] if row.get('source') == BOUNDARY_SOURCE else row.get("service_section", "")),
        0 if row.get('source') == 'Coptic Reader verified recurring supplement' else 1,
        (f"{int(row['source_order']):02d}" if row.get('source') == BOUNDARY_SOURCE else str(row.get("source_order", ""))), row.get("reading_type", ""), row.get("raw_ref", "")
    ))


SUNDAY_SOURCE = 'Coptic Reader source-qualified Sunday policy'
SUNDAY_FIXTURE = Path('sources/coptic-reader/sunday-qualified-2026-10-07')
SUNDAY_MANIFEST_SHA256 = '4cfa7be9ad90a77b714a68ad40b57c0bd884afb4ba36f425f299d4058d9ddfbd'
SUNDAY_POSITIONS = [
    ('Vespers', 'Psalm', 'V_Psalm_Ref'), ('Vespers', 'Gospel', 'V_Gospel_Ref'),
    ('Matins', 'Psalm', 'M_Psalm_Ref'), ('Matins', 'Gospel', 'M_Gospel_Ref'),
    ('Liturgy', 'Pauline Epistle', 'P_Gospel_Ref'),
    ('Liturgy', 'Catholic Epistle', 'C_Gospel_Ref'),
    ('Liturgy', 'Acts of the Apostles', 'X_Gospel_Ref'),
    ('Liturgy', 'Psalm', 'L_Psalm_Ref'), ('Liturgy', 'Gospel', 'L_Gospel_Ref'),
]
SUNDAY_MONTHS = {'tout': 1, 'toba': 5, 'amshir': 6, 'kiak': 4, 'mesra': 12,
                 'meshir': 6, 'nesi': 13}
SUNDAY_ORDINALS = ['first', 'second', 'third', 'fourth', 'fifth']
SUNDAY_CYCLE_CONTEXTS = {
    'Bashans 5': (9, '44.14:1-9', '44.24:1-9', 'SundayReadings-65'),
    'Baunah 5': (10, '44.14:1-9', '44.24:1-9', 'SundayReadings-66'),
    'Abib 5': (11, '44.14:1-9', '44.24:1-9', 'SundayReadings-62'),
    'Tut 5': (1, '44.18:9-12', '44.18:9-21', 'SundayReadings-56'),
}


def load_sunday_evidence() -> dict:
    """Authenticate reviewed literal tables; never silently bless edited fixtures."""
    folder = WORK / SUNDAY_FIXTURE
    payload = (folder / 'manifest.json').read_bytes()
    if hashlib.sha256(payload).hexdigest() != SUNDAY_MANIFEST_SHA256:
        raise RuntimeError('Sunday evidence manifest drift')
    manifest = json.loads(payload)
    for relative, expected in manifest['files'].items():
        if hashlib.sha256((folder / relative).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f'Sunday evidence source drift: {relative}')
    db = WORK / 'sources/katameros-api/Core/KatamerosDatabase.db'
    if hashlib.sha256(db.read_bytes()).hexdigest() != manifest['db_sha256']:
        raise RuntimeError('Sunday SQLite source drift')
    return json.loads((folder / 'accepted-oracle.json').read_bytes())


def numeric_coptic_date(date_value: dt.date) -> tuple[int, int, int]:
    """Numeric date, independent of liturgical Sunday month (1900–2099)."""
    if not 1900 <= date_value.year <= 2099:
        raise ValueError('Sunday numeric calendar supports Gregorian 1900–2099 only')
    year = date_value.year
    start = dt.date(year, 9, 12 if (year + 1) % 4 == 0 else 11)
    if date_value < start:
        year -= 1
        start = dt.date(year, 9, 12 if (year + 1) % 4 == 0 else 11)
    offset = (date_value - start).days
    return year - 283, offset // 30 + 1, offset % 30 + 1


def sunday_policy_selection(date_value: dt.date) -> tuple[str, int, int] | None:
    """Only documented changed selections, not an invented complete calendar.

    Existing higher feast/season contexts are retained at the row boundary.
    Ordinary unmodified Sundays and uncaptured fifth-Meshir edges return None.
    Month 14 is a SQLite pseudo-month, never a numeric Coptic month here.
    """
    if date_value.weekday() != 6:
        return None
    _, month, day = numeric_coptic_date(date_value)
    offset = (date_value - julian_pascha_gregorian(date_value.year)).days
    if -56 <= offset <= 49:
        return None
    if (month, day) in ((1, 17), (6, 8)):
        return None  # Cross / Presentation precede the ordinary month sequence.
    if day == 29 and month not in (5, 6):
        return None  # Joyful 29th precedes ordinary Sunday selection.
    start = date_value - dt.timedelta(days=day - 1)
    first_sunday = (6 - start.weekday()) % 7 + 1
    ordinal = (day - first_sunday) // 7 + 1
    if month == 4 and day == 30:
        return 'AnnualReadings', 4, 30
    if month == 1 and first_sunday == 1 and day > 1:
        return 'SundayReadings', 1, ordinal - 1
    tobe_start = start if month == 5 else start - dt.timedelta(days=30)
    tobe_first = (6 - tobe_start.weekday()) % 7 + 1
    if month in (5, 6) and tobe_first <= 2:
        if month == 5 and ordinal == 5:
            return 'SundayReadings', 6, 1
        if month == 6 and ordinal < 4:
            return 'SundayReadings', 6, ordinal + 1
    if month == 12 and ordinal == 5:
        nesi_start = start + dt.timedelta(days=30)
        year, _, _ = numeric_coptic_date(date_value)
        nesi_length = 6 if year % 4 == 3 else 5
        if (6 - nesi_start.weekday()) % 7 >= nesi_length:
            return 'SundayReadings', 13, 1
    return None


def _ordinary_sunday_context(title: str) -> tuple[int, int] | None:
    match = re.fullmatch(r'(?:the )?(first|second|third|fourth|fifth) Sunday of ([A-Za-z]+)', title, re.I)
    if not match or match[2].casefold() not in SUNDAY_MONTHS:
        return None
    return SUNDAY_MONTHS[match[2].casefold()], SUNDAY_ORDINALS.index(match[1].casefold()) + 1


def sunday_policy_rows(date_value: dt.date, rows: list[dict], oracle: dict) -> list[dict]:
    selection = sunday_policy_selection(date_value)
    if not rows or any(not is_current_source_row(r) for r in rows):
        return rows  # Never restore an inactive/removed appointment.
    is_overlay = any(r.get('source') == SUNDAY_SOURCE for r in rows)
    if selection is None:
        if is_overlay:
            raise RuntimeError('Sunday policy overlay wrong date/season')
        return rows
    contexts = [_ordinary_sunday_context(r.get('day_title', '')) for r in rows]
    if is_overlay:
        if not all(r.get('source') == SUNDAY_SOURCE for r in rows):
            raise RuntimeError('Sunday policy mixed overlay sources')
    else:
        if not any(contexts):
            return rows  # A feast / special / movable context already won upstream.
        if len(set(r.get('day_title', '') for r in rows)) != 1 or not all(contexts):
            raise RuntimeError('Sunday policy mixed upstream contexts')
    _, month, day = numeric_coptic_date(date_value)
    if not is_overlay and contexts[0] is not None and contexts[0][0] != month:
        return rows  # Wrong-date / month payload is not an authenticated context.
    table, target_month, target_day = selection
    if not is_overlay and table == 'SundayReadings' and contexts[0] == (target_month, target_day):
        return rows
    positions = [(r.get('service_section'), r.get('reading_type')) for r in rows]
    expected = [(service, kind) for service, kind, _ in SUNDAY_POSITIONS]
    if len(rows) != 9 or sorted(positions) != sorted(expected):
        raise RuntimeError('Sunday policy incomplete/extra/duplicate upstream slots')
    db = WORK / 'sources/katameros-api/Core/KatamerosDatabase.db'
    with closing(sqlite3.connect(f'file:{db}?mode=ro', uri=True)) as con:
        con.row_factory = sqlite3.Row
        seeds = list(con.execute(f'SELECT * FROM {table} WHERE Month_Number=? AND Day=?', (target_month, target_day)))
        if len(seeds) != 1:
            raise RuntimeError('Sunday policy ambiguous/missing SQLite table')
        seed = dict(seeds[0])
        books = {r['Id']: r['Name'] for r in con.execute('SELECT Id, Name FROM Books')}
    # A dated canary is not promoted to a generic template. Match the proper
    # source key, not its retained fifth-Sunday queue key.
    key_tables = [t for t in oracle['tables'] if
                  (t['family'] == table and t['key'] == {'Month_Number': target_month, 'Day': target_day})
                  or (table == 'AnnualReadings' and t['id'] == 'canary-postNativity')]
    captured = key_tables[0] if key_tables else None
    printed = [ref for d in captured['documents'] for ref in d['printedReferences']] if captured else []
    title = ('Second Day of Nativity' if table == 'AnnualReadings' else
             f"{SUNDAY_ORDINALS[target_day - 1].capitalize()} Sunday of " +
             {1: 'Tout', 6: 'Meshir', 13: 'Nesi'}[target_month])
    result = []
    for order, (service, kind, column) in enumerate(SUNDAY_POSITIONS, 1):
        raw = seed[column]
        normalized = normalize_numeric_ref(raw, books)
        primary = printed[order - 1] if printed else ''
        if kind != 'Psalm' and primary:
            normalized = canonicalize_text_ref(primary)
        result.append({
            'source': SUNDAY_SOURCE, 'gregorian_date': date_value.isoformat(),
            'weekday': date_value.strftime('%A'), 'day_title': title,
            'service_section': service, 'reading_type': kind,
            'raw_ref': primary if primary and kind != 'Psalm' else raw,
            'normalized_ref': normalized, 'parse_status': 'sunday_policy_overlay',
            'source_order': order, 'source_slot': kind, 'source_raw_refs': raw,
            'correction_source': str(SUNDAY_FIXTURE / 'accepted-oracle.json'),
            'normalization_warning': f'Source-qualified Sunday selection {table}:{seed["Id"]}; '
                f'numeric_coptic={month}/{day}; verified_date={captured["date"] if captured else "context-only/publisher-policy"}; '
                + ('Psalm MT/LXX verse alignment HELD; existing numeric source coordinates retained' if kind == 'Psalm' else ''),
            'url': 'https://copticreader.org/app/',
        })
    if is_overlay:
        comparable = [{key: value for key, value in row.items()
                       if key in result[0] or value not in ('', None)} for row in rows]
        try:
            for row in comparable:
                row['source_order'] = int(row['source_order'])
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError('Sunday policy overlay source order drift') from exc
        if comparable != result:
            raise RuntimeError('Sunday policy overlay reference/order/provenance drift')
    return result


def apply_sunday_cycle_overlays(rows: Iterable[dict]) -> list[dict]:
    """Retain original inactive rows plus exactly one context-qualified correction."""
    rows = [copy.deepcopy(r) for r in rows]
    candidates = []
    for row in rows:
        rule = SUNDAY_CYCLE_CONTEXTS.get(row.get('day_key', ''))
        if (rule and is_current_source_row(row) and row.get('source') == 'katameros-api sqlite'
                and row.get('source_table') == 'SundayReadings'
                and str(row.get('month_number')) == str(rule[0]) and str(row.get('day')) == '5'
                and row.get('reading_slot') == 'liturgy_acts' and row.get('raw_ref') == rule[1]):
            candidates.append((row, rule))
    if not candidates:
        return rows
    oracle = load_sunday_evidence()
    seen = set()
    for row, (_, old, numeric, source_id) in candidates:
        if source_id in seen:
            raise RuntimeError('Sunday cycle duplicate correction context')
        seen.add(source_id)
        source = next(t for t in oracle['tables'] if t['id'] == source_id)
        doc = next(d for d in source['documents'] if d['label'] == 'Liturgy-Praxis')
        normalized = canonicalize_text_ref(doc['printedReferences'][0])
        evidence = str(SUNDAY_FIXTURE / doc['textPath'])
        if row.get('numeric_ref'):
            if (row['numeric_ref'], row.get('normalized_ref'), row.get('correction_source')) != (numeric, normalized, evidence):
                raise RuntimeError('Sunday cycle corrected source/provenance drift')
            continue
        if row.get('normalized_ref') != ('Acts 18:9-12' if old == '44.18:9-12' else 'Acts 14:1-9'):
            raise RuntimeError('Sunday cycle original source drift')
        current = dict(row, numeric_ref=numeric, normalized_ref=normalized,
                       correction_source=evidence,
                       normalization_warning=f'Reader verified {source["date"]}; superseded numeric source retained')
        row.update(active=False, state='superseded', include_in_current_index=False,
                   superseded_reason=f'Reader Praxis endpoint/body: {source_id}')
        rows.append(current)
    return rows
