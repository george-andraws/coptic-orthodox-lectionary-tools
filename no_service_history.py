"""Bounded inactive archive of 32 retained Nineveh Vespers source rows.

This is NOT an appointment/coordinate repair. The no-service capture disqualifies
worship activation; the frozen input contexts authenticate the old literal refs.
Even well-formed archive references receive no numeric consumer coordinates.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from functools import lru_cache
from pathlib import Path

from calendar_resolution import julian_pascha_gregorian
from passage_normalization import canonicalize_text_ref

ROOT = Path(__file__).resolve().parent
CONTEXT_PATH = ROOT / 'sources/coptic-reader/jonah-qualified-2026-10-25/input-contexts.json'
CONTEXT_SHA256 = 'a6399e7f24b0da3f4520b4dff9977a8daddf96ab4d6fbe6daca365a3e505a638'
CAPTURE_RELATIVE = 'sources/coptic-reader/remaining-2026-09-07/2029-01-29-vespers-.txt'
CAPTURE_SHA256 = '84aa373f8bad6f8420d63792103752195818e316c6823d81e7575889e6e8fc4f'
REASON = 'coptic_reader_no_service'
MARKER = 'removed_by_coptic_reader_no_service'
FAMILY = 'ordinary_date_resolved_no_service_archive'
PREFIX = 'no-service-archive:'
NOTE = ('Inactive original-source archive only: Vespers are not prayed during Jonah\'s Fast. '
        'Original references are not approved numeric appointments; Lk 10:38-52 is a retained malformed source error, not Lk 10:38-42. '
        'Repeated years attest old source rows, not independent Reader confirmations.')
STATE = {'active': False, 'include_in_current_index': False,
         'current_status': 'historical_candidate_removed', 'status': 'removed'}


def authenticated_raw_rows():
    data = CONTEXT_PATH.read_bytes()
    capture = (ROOT / CAPTURE_RELATIVE).read_bytes()
    if (hashlib.sha256(data).hexdigest() != CONTEXT_SHA256
            or hashlib.sha256(capture).hexdigest() != CAPTURE_SHA256
            or not capture.decode().startswith("Vespers and Vesper Praises are not prayed during Jonah's Fast,")):
        raise ValueError('No-service archive source hash/context drift')
    result = []
    for context in json.loads(data):
        for row in context['rows']:
            if row.get('superseded_reason') != REASON:
                continue
            date = dt.date.fromisoformat(row['gregorian_date'])
            if (context['date'] != date.isoformat() or context['offset'] != -69
                    or (date - julian_pascha_gregorian(date.year)).days != -69
                    or date.weekday() != 0 or not 2020 <= date.year <= 2035
                    or row['day_title'] != 'Fast of Nineveh' or row['service_section'] != 'Vespers'
                    or row['reading_type'] not in {'Psalm', 'Gospel'}
                    or row['correction_source'] != CAPTURE_RELATIVE):
                raise ValueError('No-service archive seasonal context drift')
            result.append(row)
    if len(result) != 32 or len({r['gregorian_date'] for r in result}) != 16:
        raise ValueError('No-service archive source count drift')
    return result


def qualify_raw(row, allowed):
    # Union-schema empty CSV cells are absence, never authorization.
    clean = {k: v for k, v in row.items() if v not in ('', None)}
    matches = [r for r in allowed if clean == {k: v for k, v in r.items() if v not in ('', None)}]
    if len(matches) != 1:
        raise ValueError('Unqualified no-service raw source/context/lifecycle')
    return matches[0]


def locator(row):
    return (f"{CAPTURE_RELATIVE}:line 1; sha256={CAPTURE_SHA256}; "
            f"retained_context={CONTEXT_PATH.relative_to(ROOT)}; context_sha256={CONTEXT_SHA256}; "
            f"date={row['gregorian_date']}; raw_ref={row['raw_ref']}; no current appointment")


def project_rows(raw_rows, fields, coptic_date_for):
    allowed = authenticated_raw_rows()
    result = []
    seen = set()
    for raw in raw_rows:
        r = qualify_raw(raw, allowed)
        row_id = PREFIX + r['gregorian_date'] + ':' + r['reading_type']
        if row_id in seen:
            raise ValueError('Duplicate no-service archive witness')
        seen.add(row_id)
        ref = canonicalize_text_ref(r['raw_ref'])
        row = dict.fromkeys(fields, '')
        row.update(passage=ref, source_kind='copticchurch_date', source_family=FAMILY,
                   source_table='copticchurch_date_readings_2020_2035',
                   source_file='out/data/copticchurch_date_readings_2020_2035.csv',
                   source_row_id=row_id, source_order='1' if r['reading_type']=='Psalm' else '2', source_token_order='1',
                   superseded_reason=REASON, liturgical_place='Fast of Nineveh', calendar_key='Fast of Nineveh',
                   gregorian_date=r['gregorian_date'], coptic_date=coptic_date_for(r['gregorian_date']),
                   day_title='Fast of Nineveh', service_day='Fast of Nineveh', service_section='Vespers',
                   reading_slot=r['reading_type'], reading_type=r['reading_type'],
                   source_ref=r['raw_ref'], raw_ref=r['raw_ref'], normalized_ref=ref, normalized_segment=ref,
                   significance_note=NOTE, url=r['url'],
                   provenance=json.dumps({'consumer_source_transport': {'state': STATE,
                       'no_service_archive': {'context_sha256': CONTEXT_SHA256, 'capture_sha256': CAPTURE_SHA256,
                           'raw_row': r, 'runtime_activation_approved': False}}, 'legacy_provenance': r['source']},
                       ensure_ascii=False, sort_keys=True))
        result.append(row)
    return result


@lru_cache(maxsize=1)
def archive_identity_keys():
    # Cache recognition only, never qualification: each real boundary below
    # reauthenticates the retained bytes, even after this set is populated.
    return frozenset('rid_' + hashlib.sha256(('no_service_archive|' + canonicalize_text_ref(r['raw_ref'])).encode()).hexdigest()[:20]
                     for r in authenticated_raw_rows())


def is_archive(row):
    return (row.get('source_family') == FAMILY or str(row.get('source_row_id','')).startswith(PREFIX)
            or 'no_service_archive' in str(row.get('provenance',''))
            or row.get('superseded_reason') == REASON
            or row.get('identity_key', '') in archive_identity_keys())


def exact_row(actual, expected):
    # Python otherwise treats False == 0 and True == 1 as authentic transport.
    return (actual.keys() == expected.keys()
            and all(type(actual[k]) is type(v) and actual[k] == v for k, v in expected.items()))


def qualify_projected(row):
    # Late import avoids a producer/helper cycle, while reusing its exact schema.
    import build_lectionary_crosswalk as crosswalk
    allowed = authenticated_raw_rows()
    raw = next((r for r in allowed if PREFIX + r['gregorian_date'] + ':' + r['reading_type'] == row.get('source_row_id')), None)
    if raw is None:
        raise ValueError('No-service archive missing retained witness identity')
    expected, = project_rows([raw], crosswalk.FIELDS, crosswalk.coptic_date_for)
    if not exact_row(row, expected):
        raise ValueError('No-service archive projected context/ref/status/proof drift')
    return raw


def identity_for(row):
    qualify_projected(row)
    ref = row['passage']
    return {'identity_key': 'rid_' + hashlib.sha256(('no_service_archive|' + ref).encode()).hexdigest()[:20],
            'reading_type': 'source-archive', 'reading_name': '', 'source_label': row['raw_ref'],
            'display_ref': ref, 'canonical_mt_ref': '', 'canonical_lxx_ref': '',
            'source_convention': 'unapproved_original_source_literal',
            'canonicalization_confidence': 'n/a', 'canonicalization_note': NOTE, 'spans_json': '[]'}


def validate_presentation(rows, build_presentation):
    selected = [r for r in rows if is_archive(r)]
    if not selected:
        return
    import build_lectionary_crosswalk as crosswalk
    raw = authenticated_raw_rows()
    expected, _ = build_presentation(project_rows(raw, crosswalk.FIELDS, crosswalk.coptic_date_for))
    if any(not any(exact_row(r, witness) for witness in expected) for r in selected):
        raise ValueError('No-service archive presentation context/status/ref/proof drift')


def validate_reverse(rows):
    """Key membership cannot authorize activation or replacement disclosure.

    Reconstruct qualifications from retained source, never candidate inventory.
    Recognize literal archive identity keys even if all friendly markers vanish.
    """
    import build_design_deliverables as design
    import build_lectionary_crosswalk as crosswalk
    raw = authenticated_raw_rows()
    keys = {'rid_' + hashlib.sha256(('no_service_archive|' + canonicalize_text_ref(r['raw_ref'])).encode()).hexdigest()[:20]
            for r in raw}
    selected = [r for r in rows if is_archive(r) or r.get('identity_key') in keys]
    if not selected:
        return
    presentation, _ = design.build_reverse_presentation(project_rows(raw, crosswalk.FIELDS, crosswalk.coptic_date_for))
    groups = {}
    for row in presentation:
        groups.setdefault(design.occasion_index_key(row), []).append(row)
    expected_rows = []
    for key, witnesses in sorted(groups.items()):
        first = witnesses[0]
        fields = ('display_ref', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json',
                  'current_status', 'removed_marker', 'reading_type', 'reading_name',
                  'source_family', 'source_kind', 'source_edition', 'source_title')
        disclosure, _ = design.build_collapsed_source_disclosure(witnesses)
        source, winner = design.choose_collapsed_scalar_source(disclosure, witnesses)
        years = sorted({r['gregorian_date'][:4] for r in witnesses})
        expected = {'source_disclosure': json.dumps(disclosure, ensure_ascii=False, separators=(',', ':')),
                    'source_disclosure_count': str(len(disclosure)),
                    'provenance': winner['provenance'], 'source_locator': source['source_locator'],
                    'attestation_years': '; '.join(years), 'attestation_year_min': years[0],
                    'attestation_year_max': years[-1], 'collapsed_row_count': str(len(witnesses)),
                    'occasion': first['occasion'], 'calendar_keys': design.join_unique(r['calendar_key'] for r in witnesses),
                    'day_titles': design.join_unique(r['day_title'] for r in witnesses),
                    'service_section': first['service_section'], 'service_hour': first['service_hour'],
                    'slot': first['slot'], 'slot_type': design.slot_type_for(first),
                    'slot_order': None, 'occasion_kind': design.occasion_kind_for(first),
                    'identity_key': first['identity_key'],
                    'hour_theme': design.join_unique(r['hour_theme'] for r in witnesses),
                    'authority_tier': design.join_unique(r['authority_tier'] for r in witnesses),
                    '_slot_explicit_order': design.explicit_slot_order(first),
                    '_slot_source_order': min(int(r['source_order']) for r in witnesses),
                    '_slot_source_token_order': min(int(r['source_token_order']) for r in witnesses)}
        expected.update({k: first[k] for k in fields})
        # Ordering is part of the public row contract too. Reconstruct the full
        # archive group so a same-slot neighboring identity cannot change it.
        expected_rows.append(expected)
    design.assign_slot_orders(expected_rows)
    by_key = {design.occasion_index_key(r): r for r in expected_rows}
    if any(design.occasion_index_key(row) not in by_key
           or not exact_row(row, by_key[design.occasion_index_key(row)]) for row in selected):
        raise ValueError('No-service archive reverse context/disclosure/attestation/state/type drift')

