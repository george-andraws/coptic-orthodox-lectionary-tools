"""Disclose three bounded ordinary corrections, without upgrading authority."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from convertdate import coptic
import ordinary_appointment_repairs as ordinary
from reading_context_overlays import is_current_source_row

ROOT = Path(__file__).resolve().parent
BABA = 'sources/user-corrections/babah-third-sunday-pauline.json'
CONTRACTS = {ordinary.CONTRACT_RELATIVE, BABA}
BABA_KEY = ('The third Sunday of Baba', 'Liturgy', 'Pauline Epistle', '1Cor 16:12-23')


def _key(row):
    return tuple(row.get(k, '') for k in ('day_title', 'service_section', 'reading_type', 'raw_ref'))


def transport_for_index(row):
    """Authenticate source/index context afresh; preserve source edition labels."""
    relative = row.get('correction_source')
    if relative not in CONTRACTS:
        return {}
    date = dt.date.fromisoformat(row['gregorian_date'])
    if (not 2020 <= date.year <= 2035 or row.get('weekday') != date.strftime('%A')
            or row.get('source') != 'copticchurch.net daily scrape'
            or row.get('url') != f'https://copticchurch.net/readings?g_year={date.year}&g_month={date.month:02d}&g_day={date.day:02d}'
            or not is_current_source_row(row) or row.get('removed_marker')
            or row.get('candidate_only') or row.get('superseded_reason')
            or row.get('source_occasion') or row.get('source_slot')
            or row.get('source_ref_status') != 'source_corrected'):
        raise ValueError('Unqualified ordinary correction source/index context')
    if relative == ordinary.CONTRACT_RELATIVE:
        contract = ordinary.load_ordinary_appointment_contract()
        repair = next((r for r in contract['repairs'] if tuple(r[k] for k in
                       ('day_title','service_section','reading_type','raw_ref')) == _key(row)), None)
        if repair is None or not ordinary._qualified_date(row):
            raise ValueError('Ordinary correction occasion/date does not qualify')
        corrected = repair['normalized_ref']
        warning = 'ordinary_appointment_source_qualified; ' + repair['note']
        evidence = repair['reader']['text']
        digest = contract['fingerprints'][evidence]
        printed = repair['reader_printed_ref']
        selected = repair['reader']['source_date']
        note = repair['note']
    else:
        if _key(row) != BABA_KEY:
            raise ValueError('Baba correction context does not qualify')
        _, month, day = coptic.from_gregorian(date.year, date.month, date.day)
        if month != 2 or date.weekday() != 6 or not 15 <= day <= 21:
            raise ValueError('Baba correction date does not qualify')
        policy = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())
        contract = json.loads(ordinary._read_authenticated(BABA, policy['source_fingerprints'][BABA]))
        ctx = contract['context']
        if tuple(ctx[k] for k in ('day_title','service_section','reading_type','expected_raw_ref')) != BABA_KEY:
            raise ValueError('Baba correction contract context drift')
        corrected = ctx['corrected_ref']
        warning = 'source_corrected_from_george_user-supplied_correction; evidence=' + BABA
        evidence, digest = next(iter(contract['source_fingerprints'].items()))
        ordinary._read_authenticated(evidence, digest)
        printed = contract['reader_corroboration']['printed_ref']
        selected = contract['reader_corroboration']['selected_date']
        note = contract['scope']
    if row.get('matched_ref') != corrected or row.get('normalization_warning') != warning:
        raise ValueError('Ordinary correction coordinates/warning drift')
    q = dict(gregorian_date=row['gregorian_date'], day_title=row['day_title'],
             service_section=row['service_section'], reading_type=row['reading_type'],
             source_url=row['url'], original_raw_ref=row['raw_ref'], corrected_ref=corrected,
             reader_printed_ref=printed, correction_source=relative,
             normalization_warning=warning, source_file=evidence, source_sha256=digest,
             source_selected_date=selected, qualification_note=note,
             fresh_app_verification=False, independent_recurring_year_confirmation=False)
    return {'ordinary_source_correction': q,
            'evidenceLocator': evidence + '; sha256=' + digest + '; correction=' + relative}


def qualify_projected_row(row):
    """Copied disclosures cannot qualify a different source/occasion/reference."""
    try:
        provenance = json.loads(row.get('provenance') or '{}')
    except json.JSONDecodeError:
        provenance = {}
    transport = provenance.get('consumer_source_transport', {}) if isinstance(provenance, dict) else {}
    if not isinstance(transport, dict):
        raise ValueError('Ordinary correction transport must be an object')
    q = transport.get('ordinary_source_correction')
    target = row.get('source_family') == 'ordinary_date_resolved' and _key(row) in {*ordinary.TARGETS, BABA_KEY}
    if q is None:
        if target:
            raise ValueError('Ordinary source correction disclosure missing')
        return None
    if (not isinstance(q, dict) or q.get('fresh_app_verification') is not False
            or q.get('independent_recurring_year_confirmation') is not False):
        raise ValueError('Ordinary correction disclosure type/authority drift')
    try:
        date = dt.date.fromisoformat(q['gregorian_date'])
        indexed = dict(source='copticchurch.net daily scrape', gregorian_date=q['gregorian_date'],
                       weekday=date.strftime('%A'), day_title=q['day_title'],
                       service_section=q['service_section'], reading_type=q['reading_type'],
                       raw_ref=q['original_raw_ref'], matched_ref=q['corrected_ref'],
                       source_ref_status='source_corrected', normalization_warning=q['normalization_warning'],
                       url=q['source_url'], correction_source=q['correction_source'])
        expected = transport_for_index(indexed)
        if expected.get('ordinary_source_correction') != q or expected.get('evidenceLocator') != transport.get('evidenceLocator'):
            raise ValueError('Ordinary source correction disclosure drift')
        fields = dict(source_kind='copticchurch_date', source_family='ordinary_date_resolved',
                      source_table='copticchurch_date_readings_2020_2035', source_file='cache/copticchurch_html',
                      gregorian_date=q['gregorian_date'], day_title=q['day_title'],
                      service_day=q['day_title'], calendar_key=q['day_title'],
                      service_section=q['service_section'], service_hour='', reading_type=q['reading_type'],
                      raw_ref=q['original_raw_ref'], source_ref=q['corrected_ref'],
                      passage=q['corrected_ref'], normalized_ref=q['corrected_ref'], url=q['source_url'])
        if (any(row.get(k, '') != v for k, v in fields.items()) or not is_current_source_row(row)
                or row.get('candidate_only') or row.get('removed_marker') or row.get('superseded_reason')):
            raise ValueError('Ordinary projected correction context drift')
        return q
    except (KeyError, TypeError, OSError) as exc:
        raise ValueError('Ordinary correction disclosure malformed') from exc
