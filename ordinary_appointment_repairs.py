"""Two exact-source ordinary repairs; Amshir 7 remains held.

Parent hook: apply_ordinary_appointment_repair(row) inside
apply_copticchurch_source_correction. No writes, source retrieval or activation
of retained history. Original review receipts do not authorize these repairs.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

from convertdate import coptic
from reading_context_overlays import is_current_source_row

ROOT = Path(__file__).resolve().parent
CONTRACT_RELATIVE = 'sources/user-corrections/ordinary-appointment-repairs-2026-10-25.json'
CONTRACT_SHA256 = 'd86c2973f020a707d9eafa855e01c5226c81e046e0c9e87ec4322aba2d6bdbe6'
EVIDENCE_PREFIX = 'sources/coptic-reader/ordinary-appointment-qualified-2026-10-25/'
TARGETS: dict = {
    ('Mesra 26', 'Matins', 'Gospel', '12:20-26'): 'Jn 12:20-26',
    ('The fourth Sunday of Baba', 'Liturgy', 'Psalm', 'Psalm 79:13:00'): 'Ps 79:13',
}


def _read_authenticated(relative, expected):
    path = ROOT / relative
    if (Path(relative).is_absolute() or '..' in Path(relative).parts
            or path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve())):
        raise ValueError('Ordinary appointment evidence path drift')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('Ordinary appointment evidence hash drift: ' + relative)
    return data


def load_ordinary_appointment_contract():
    """Reauthenticate portable authority and witness bytes, without mutable caches."""
    try:
        contract = json.loads(_read_authenticated(CONTRACT_RELATIVE, CONTRACT_SHA256))
        for relative, expected in contract['fingerprints'].items():
            if not relative.startswith(EVIDENCE_PREFIX):
                raise ValueError('Ordinary appointment evidence namespace drift')
            _read_authenticated(relative, expected)
        if contract['old_receipts_grant_activation'] is not False:
            raise ValueError('Ordinary appointment old source receipt authority drift')
        return contract
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError('Ordinary appointment source contract missing or drifted') from exc


def _qualified_date(row):
    try:
        date = dt.date.fromisoformat(row.get('gregorian_date', ''))
    except (ValueError, TypeError):
        return False
    if (not 2020 <= date.year <= 2035 or row.get('weekday') != date.strftime('%A')
            or row.get('url') != f'https://copticchurch.net/readings?g_year={date.year}&g_month={date.month:02d}&g_day={date.day:02d}'):
        return False
    _, month, day = coptic.from_gregorian(date.year, date.month, date.day)
    if row['day_title'] == 'Mesra 26':
        return (month, day) == (12, 26)
    return month == 2 and date.weekday() == 6 and 22 <= day <= 28


def apply_ordinary_appointment_repair(row: dict) -> dict:
    """Copy qualified current rows; unrelated, held and historical rows are no-ops.

    Exact raw labels, source URL/date, ordinary family/kind and current lifecycle
    are mandatory. Existing different corrections are not replaced. Recurrence
    is bounded policy, not a claim of fresh Reader confirmation in every year.
    """
    key = (row.get('day_title'), row.get('service_section'), row.get('reading_type'), row.get('raw_ref'))
    corrected = TARGETS.get(key)
    if (not corrected or row.get('source') != 'copticchurch.net daily scrape'
            or row.get('source_family') not in (None, '', 'ordinary_date_resolved')
            or row.get('source_kind') not in (None, '', 'copticchurch_date')
            or not is_current_source_row(row) or row.get('removed_marker')
            or row.get('candidate_only')
            or row.get('current_status') in {'pending_psalm_equivalence_unresolved', 'unknown'}
            or row.get('source_convention') not in (None, '', 'mt_nkjv')
            or row.get('normalized_ref') not in (row['raw_ref'], corrected)
            or row.get('correction_source') not in (None, '', CONTRACT_RELATIVE)
            or not _qualified_date(row)):
        return row
    contract = load_ordinary_appointment_contract()
    repair = next(r for r in contract['repairs'] if tuple(r[field] for field in
                  ('day_title', 'service_section', 'reading_type', 'raw_ref')) == key)
    note = 'ordinary_appointment_source_qualified; ' + repair['note']
    warnings = row.get('normalization_warning') or ''
    if note not in warnings:
        warnings = '; '.join(filter(None, [warnings, note]))
    return {**row, 'normalized_ref': corrected, 'parse_status': 'source_corrected',
            'normalization_warning': warnings, 'correction_source': CONTRACT_RELATIVE,
            'ordinary_appointment_reader_printed_ref': repair['reader_printed_ref']}
