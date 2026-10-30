"""R2 full Kiahk23 table, source-owned npm overlay after canonicalization.

Parent hooks: repair_reverse_rows(published_rows); then
repair_daily(daily_dict, corrected_reverse_rows) after structural daily fill.
No raw/design mutation or corpus-key guard change. Original receipts remain
exact-date-only. A separately pinned current repair plan grants only bounded
2020-2035 annual weekday recurrence, never a Sunday/overriding-occasion table.
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import re

from convertdate import coptic

ROOT = Path(__file__).resolve().parent
SOURCE = 'sources/coptic-reader/kiahk-23-qualified-2026-10-29'
PLAN = SOURCE + '/repair-approval/repair-plan.json'
PLAN_SHA256 = '2b9e41828da41d2e9519783d5e626304d4ee176071df59e6ee033484b24b0d13'
FAMILY = 'coptic_reader_qualified_kiahk23_review'
LABELS = {'Kiahk 23', 'Kiyahk 23'}
EVIDENCE_FIELDS = ['kiahk23_review_evidence', 'kiahk23_retirement']


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _read(relative):
    """Reject symlinks and nonliteral case at every evidence path component."""
    current = ROOT
    for part in Path(relative).parts:
        if part in {'..', '/', ''} or part not in {p.name for p in current.iterdir()}:
            raise ValueError('Kiahk23 evidence authentication path rejected')
        current /= part
        if current.is_symlink():
            raise ValueError('Kiahk23 evidence authentication symlink rejected')
    if not current.is_file() or not current.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Kiahk23 evidence authentication path rejected')
    return current.read_bytes()


def authenticate_plan():
    """Authenticate full seven-document table at each real projection boundary."""
    try:
        raw = _read(PLAN)
        if _sha(raw) != PLAN_SHA256:
            raise ValueError('Kiahk23 plan authentication failed')
        plan = json.loads(raw)
        payloads = {}
        for relative, digest in plan['fingerprints'].items():
            raw = _read(SOURCE + '/' + relative)
            if _sha(raw) != digest:
                raise ValueError('Kiahk23 evidence authentication failed: ' + relative)
            payloads[relative] = raw
        auth = json.loads(payloads['retained-authentication.json'])
        if (auth['genericTemplateQualification'] is not False
                or auth['original_review_status'] != 'qualified_exact_observed_date_table'
                or plan['retained_receipt_grants_recurrence'] is not False
                or plan['canonical_psalm_alignment_approved'] is not False):
            raise ValueError('Kiahk23 retained qualification authentication failed')
        composite = '\n'.join(d['label'] + '\n' + payloads[d['local_path']].decode()
                              for d in auth['documents'])
        if _sha(composite.encode()) != plan['retained_table_sha256']:
            raise ValueError('Kiahk23 complete table authentication failed')
        for reading in plan['appointments']:
            lines = payloads[reading['document']].decode().splitlines()
            if lines[reading['heading_line'] - 1] != reading['heading_exact']:
                raise ValueError('Kiahk23 heading authentication failed')
        if 'No prophecies are read on this day.' not in payloads['retained-2026-01-01/Matins-Prophecies.txt'].decode():
            raise ValueError('Kiahk23 no-prophecies authentication failed')
        return plan
    except (OSError, KeyError, IndexError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('Kiahk23 source authentication missing or malformed') from exc


def is_current_reading(row):
    """Exact Python counterpart of the package's public isCurrentReading.

    Contract-tested against the actual JS function, including unknown refusal.
    Do not replace with marker-only or status-only filtering before selection.
    """
    if not isinstance(row, dict) or row.get('active') is False or row.get('status') == 'removed':
        return False
    marker = str(row.get('removed_marker') or '').strip()
    if re.search(r'^(superseded\b|removed\b|removed_|omitted\b)|\bremoved in\b|\bsource omitted\b', marker, re.I):
        return False
    status = str(row.get('current_status') or row.get('status') or '').strip().lower()
    if not status:
        return True
    if status == 'removed' or status.startswith('superseded') or status in {'historical_candidate_removed', 'historical_witness'}:
        return False
    if status in {'current', 'current_public_or_local_reference', 'current_working_source_not_coptic_reader_checked',
                  'current_confirmed_coptic_reader', 'current_confirmed_by_fixture_equivalence',
                  'pending_psalm_equivalence_unresolved'}:
        return True
    raise ValueError('Unknown explicit reading status: ' + status)


def _date_eligible(civil_date):
    try:
        date = dt.date.fromisoformat(civil_date)
        return (2020 <= date.year <= 2035 and date.weekday() != 6
                and coptic.from_gregorian(date.year, date.month, date.day)[1:] == (4, 23))
    except (ValueError, TypeError):
        return False


def _context(row, civil_date=None):
    if row.get('occasion') not in LABELS or row.get('service_hour', ''):
        return False
    for field in ('calendar_key', 'calendar_keys', 'day_title', 'day_titles'):
        if row.get(field) and row[field] not in LABELS:
            return False
    if row.get('coptic_date_key') not in (None, '', 'kiahk-23'):
        return False
    date_text = civil_date or row.get('gregorian_date')
    if date_text:
        if not _date_eligible(date_text):
            return False
        date = dt.date.fromisoformat(date_text)
        if row.get('gregorian_date') and row['gregorian_date'] != date_text:
            return False
        if row.get('weekday') and row['weekday'] != date.strftime('%A'):
            return False
        if row.get('coptic_date'):
            year = coptic.from_gregorian(date.year, date.month, date.day)[0]
            if row['coptic_date'] not in {f'{month} 23, {year}' for month in ('Kiahk', 'Kiyahk', 'Koiahk')}:
                return False
    return True


def _selector(row):
    return tuple(row.get(k, '') for k in ('source_family', 'source_kind', 'service_section', 'slot', 'canonical_mt_ref'))


def _legacy_selectors():
    witness = json.loads(_read(SOURCE + '/repair-approval/legacy-published-1.3.6.json'))
    return {_selector(r) for r in witness['reverse_rows']}


def _is_target(row, selectors, civil_date=None):
    return _context(row, civil_date) and _selector(row) in selectors


def _recognized(row):
    return (row.get('source_family') == FAMILY or row.get('source_kind') == FAMILY
            or str(row.get('source_row_id', '')).startswith('R2:')
            or str(row.get('source_locator', '')).startswith(SOURCE + '/')
            or any(token in str(row.get(field, '')) for field in
                   ('source_disclosure', 'provenance', 'source_file', 'kiahk23_review_evidence')
                   for token in (FAMILY, PLAN)))


def _new_row(reading, plan):
    ref = reading['canonical_mt_ref']
    printed = reading['printed_ref']
    psalm = not ref
    if psalm:
        spans = []
        identity = 'reader_source_only|' + FAMILY + '|' + reading['service_section'] + '|' + printed
    else:
        match = re.fullmatch(r'(\w+) (\d+):(\d+)-(\d+)', ref)
        if match is None:
            raise ValueError('Kiahk23 unsupported canonical selection')
        book, chapter, first, last = match.groups()
        spans = [dict(book=book, chapter_start=int(chapter), chapter_end=int(chapter),
                      verse_start=int(first), verse_end=int(last), source_ref=printed,
                      canonical_mt_ref=ref, canonical_lxx_ref=ref, confidence='high',
                      source_convention='modern_english_reference', validation_basis='retained_full_numbered_Reader_body')]
        identity = 'scripture|' + ref + '|' + ref
    locator = SOURCE + '/' + reading['document'] + ':line ' + str(reading['heading_line']) + '; sha256=' + reading['document_sha256']
    evidence = dict(repair_id=plan['repair_id'], source_family=FAMILY, source_kind=FAMILY,
                    plan=PLAN, plan_sha256=PLAN_SHA256, table_sha256=plan['retained_table_sha256'],
                    source_document=SOURCE + '/' + reading['document'],
                    document_sha256=reading['document_sha256'], heading_line=reading['heading_line'],
                    ordinal=reading['ordinal'], printed_ref=printed, canonical_mt_ref=ref,
                    service_section=reading['service_section'], slot=reading['slot'],
                    retained_exact_date='2026-01-01', retained_clock='10:00 AM',
                    fresh_app_verification=False, recurrence_policy=plan['recurrence_policy'],
                    old_receipt_grants_recurrence=False, canonical_psalm_alignment_approved=False)
    note = ('Reader printed/body edition retained as source-only; exact canonical Psalm alignment held; no numeric spans.'
            if psalm else 'Full retained Reader service body; bounded weekday fixed-day repair, not fresh per-year verification.')
    slot_type = {'Psalm':'psalm', 'Gospel':'gospel', 'Pauline Epistle':'pauline',
                 'Catholic Epistle':'catholicon', 'Acts of the Apostles':'praxis'}[reading['slot']]
    return dict(identity_key='rid_' + _sha(identity.encode())[:20], reading_type='scripture', reading_name='',
                occasion='Kiahk 23', occasion_kind='specific', coptic_date_key='kiahk-23',
                calendar_keys='Kiahk 23', day_titles='Kiahk 23', service_section=reading['service_section'],
                service_hour='', slot=reading['slot'], slot_type=slot_type, slot_order=1,
                hour_theme='', attestation_year_min='2026', attestation_year_max='2026',
                source_family=FAMILY, source_kind=FAMILY, source_title='Coptic Reader retained Kiahk 23 full table',
                source_edition='Reader printed reference and rendered body, retained 2026-01-01 at 10:00 AM',
                source_file=SOURCE + '/' + reading['document'], source_row_id='R2:' + str(reading['ordinal']),
                source_order=reading['ordinal'], source_token_order=1, source_ref=printed, raw_ref=printed,
                source_url='https://copticreader.org/app/', source_locator=locator,
                authority_tier='primary_reader_source', display_ref=printed if psalm else ref,
                canonical_mt_ref=ref, canonical_lxx_ref=ref, spans_json=_json(spans),
                current_status='pending_psalm_equivalence_unresolved' if psalm else 'current_confirmed_coptic_reader',
                active=True, status='current', removed_marker='', source_convention='reader_printed_edition_source_only' if psalm else 'modern_english_reference',
                canonicalization_confidence='held' if psalm else 'high', canonicalization_note=note,
                provenance=FAMILY + '; ' + PLAN + '; ' + locator,
                source_disclosure=_json([evidence]), source_disclosure_count='1',
                kiahk23_review_evidence=_json(evidence))


def _qualify(row, plan, civil_date=None):
    if civil_date is not None and not _date_eligible(civil_date):
        raise ValueError('Kiahk23 projected date not eligible (Sunday/override/outside policy)')
    candidates = [_new_row(r, plan) for r in plan['appointments']]
    expected = next((r for r in candidates if r['source_row_id'] == row.get('source_row_id')), None)
    if (expected is None or any(type(row.get(k)) is not type(v) or row.get(k) != v for k, v in expected.items())
            or not _context(row, civil_date)):
        raise ValueError('Kiahk23 projected source/context/coordinate/disclosure drift')
    if row.get('gregorian_date') and (civil_date is None or row['gregorian_date'] != civil_date):
        raise ValueError('Kiahk23 projected outer date mismatch')
    if 'weekday' in row and (civil_date is None or row['weekday'] != dt.date.fromisoformat(civil_date).strftime('%A')):
        raise ValueError('Kiahk23 projected weekday mismatch')
    return row


def qualify_row(row, *, civil_date=None):
    """Fail closed when an owned disclosure has been transplanted or corrupted."""
    return _qualify(row, authenticate_plan(), civil_date)


def _retire(row):
    retained = copy.deepcopy(row)
    retained.update(active=False, status='removed', current_status='historical_witness',
                    removed_marker='removed_by_kiahk23_review',
                    kiahk23_retirement=_json(dict(plan=PLAN, plan_sha256=PLAN_SHA256,
                        reason='Source edition retained inactive; authenticated full fixed-day Reader table supersedes current projection only.')))
    return retained


def repair_reverse_rows(rows):
    """After existing canonicalizeOccurrences; keep all old rows and labels."""
    plan = authenticate_plan()
    selectors = _legacy_selectors()
    out = []
    owned = []
    selected = False
    for row in rows:
        if _recognized(row):
            _qualify(row, plan)
            owned.append(row)
            out.append(copy.deepcopy(row))
            continue
        # The public predicate is evaluated BEFORE a competitor is selected.
        if is_current_reading(row) and _is_target(row, selectors):
            selected = True
            out.append(_retire(row))
        else:
            out.append(copy.deepcopy(row))
    if owned:
        if len(owned) != 9 or {r['source_row_id'] for r in owned} != {'R2:' + str(i) for i in range(1, 10)}:
            raise ValueError('Kiahk23 complete reverse table required')
    elif selected:
        out.extend(_new_row(r, plan) for r in plan['appointments'])
    return out


def repair_daily(daily, corrected_reverse):
    """After structural fill; require exact annual weekday context at outer date.

    Daily output is current-only; retired witnesses belong in raw/reverse only.
    Refuse mixed legacy replays rather than deleting unauthenticated extras.
    Sunday/feast tables are never replaced merely because their numeric Coptic
    date is 4/23. Held Psalms deliberately contribute zero numeric hits.
    """
    plan = authenticate_plan()
    selectors = _legacy_selectors()
    source = [r for r in corrected_reverse if _recognized(r)]
    for row in source:
        _qualify(row, plan)
    if source and (len(source) != 9 or {r['source_row_id'] for r in source} != {'R2:' + str(i) for i in range(1, 10)}):
        raise ValueError('Kiahk23 complete corrected reverse table required')
    source.sort(key=lambda r: r['source_order'])
    output = copy.deepcopy(daily)
    for civil_date, rows in output.items():
        owned = [r for r in rows if _recognized(r)]
        for row in owned:
            _qualify(row, plan, civil_date)
        if owned:
            if len(owned) != 9 or {r['source_row_id'] for r in owned} != {'R2:' + str(i) for i in range(1, 10)}:
                raise ValueError('Kiahk23 complete daily table required')
            if len(rows) != 9:
                raise ValueError('Kiahk23 daily current-only table required; regenerate mixed projection from raw')
            if any(row.get('reading_order') != ordinal or row['source_row_id'] != 'R2:' + str(ordinal)
                   for ordinal, row in enumerate(rows, 1)):
                raise ValueError('Kiahk23 daily reading order drift')
            continue
        if not _date_eligible(civil_date):
            continue
        live = [r for r in rows if is_current_reading(r)]
        if not live or len(live) != len(rows) or not all(_is_target(r, selectors, civil_date) for r in live):
            continue
        if not source:
            raise ValueError('Kiahk23 complete corrected reverse table required')
        output[civil_date] = []
        for ordinal, original in enumerate(source, 1):
            row = copy.deepcopy(original)
            row['reading_order'] = ordinal
            row['gregorian_date'] = civil_date
            row['weekday'] = dt.date.fromisoformat(civil_date).strftime('%A')
            _qualify(row, plan, civil_date)
            output[civil_date].append(row)
    return output
