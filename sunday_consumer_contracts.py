"""Sunday consumer proof/state boundary; no calendar or activation decisions."""
import json
import re
import sqlite3
import datetime as dt
from contextlib import closing
from pathlib import Path
from typing import Literal
from passage_normalization import canonicalize_text_ref, normalize_numeric_ref, iter_numeric_ref_segments
from query_lectionary import current_source_row

STATE_FIELDS = ('active', 'is_active', 'include_in_current_index', 'state', 'status',
    'current_status', 'projection_status', 'removed_from_standard_lectionary',
    'removal_reason', 'removed_reason', 'removal_effective_version',
    'superseded_reason', 'superseded_by_ref', 'removed_marker')
SOURCE = 'Coptic Reader source-qualified Sunday policy'
FAMILY = 'coptic_reader_verified_sunday_policy'
KEY = 'coptic_reader_sunday_policy'
FILE = 'sources/coptic-reader/sunday-qualified-2026-10-07/accepted-oracle.json'
EDITION = 'Saved accepted whole tables; Psalm alignment HELD'
TransportMode = Literal['raw', 'presentation', 'daily', 'reverse', 'output']
CONTEXT_FIELDS = ('source_ref', 'raw_ref', 'passage', 'gregorian_date', 'service_section',
    'reading_slot', 'liturgical_place', 'source_row_id', 'source_order')


def strict_json(value):
    def unique(pairs):
        result = {}
        for key, item in pairs:
            if key in result:
                raise ValueError('Sunday duplicate JSON member: ' + key)
            result[key] = item
        return result
    return json.loads(value, object_pairs_hook=unique) if isinstance(value, str) else value


def provenance(row):
    raw = row.get('provenance', '')
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.lstrip().startswith('{'):
        return strict_json(raw)
    # Passage-disclosure CSV keeps the original provenance in its citation cell.
    citation = row.get('citation', '')
    if 'provenance={' in citation:
        start = citation.index('provenance=') + len('provenance=')
        # Decode only the JSON value; the following URL is not JSON.
        _, end = json.JSONDecoder().raw_decode(citation[start:])
        return strict_json(citation[start:start + end])
    return {}


def transport(row):
    result = provenance(row).get('consumer_source_transport', {})
    if not isinstance(result, dict) or not isinstance(result.get('state', {}), dict):
        raise ValueError('Sunday malformed consumer source transport/state')
    return result


def is_sunday(row):
    if (row.get('source_family') == FAMILY or row.get('source_key') == KEY
            or row.get('source_file') == FILE or row.get('correction_source') == FILE
            or row.get('source') == SOURCE or row.get('source_title') == SOURCE
            or row.get('source_edition') == EDITION
            or str(row.get('source_locator', '')).startswith('sources/coptic-reader/sunday-qualified-2026-10-07/')):
        return True
    if row.get('source_convention') == 'existing_numeric_source_coordinates_alignment_held':
        return True
    return any(token in str(row.get(field, '')) for field in ('provenance', 'source_disclosure', 'citation', 'canonicalization_note')
               for token in (SOURCE, FILE, FAMILY, 'Sunday selection '))


def is_current(row):
    return current_source_row(row) and current_source_row(transport(row).get('state', {}))


def bind_context(projected, source_transport):
    source_transport['consumer_context'] = {k: projected.get(k, '') for k in CONTEXT_FIELDS}


def _proof(row, t, oracle):
    for container in (t, t.get('state', {})):
        if any(flag in container and container[flag] is not False for flag in ('runtime_activation', 'consumer_eligible')):
            raise ValueError('Sunday malformed envelope nonactivation flag')
    if t.get('source') != SOURCE or t.get('correction_source') != FILE:
        raise ValueError('Sunday missing/counterfeit source transport')
    ctx = t.get('consumer_context')
    if not isinstance(ctx, dict) or set(ctx) != set(CONTEXT_FIELDS):
        raise ValueError('Sunday missing consumer context envelope')
    match = re.search(r'Sunday selection (SundayReadings|AnnualReadings):(\d+);', t.get('normalization_warning', ''))
    if not match or t.get('table_id') != match[1] + '-' + match[2]:
        raise ValueError('Sunday selection/table mismatch')
    import calendar_resolution as calendar
    slot = ctx['reading_slot']
    position = next((p for p in calendar.SUNDAY_POSITIONS if p[:2] == (ctx['service_section'], slot)), None)
    if not position:
        raise ValueError('Sunday source section/slot mismatch')
    with closing(sqlite3.connect(f'file:{calendar.WORK / "sources/katameros-api/Core/KatamerosDatabase.db"}?mode=ro', uri=True)) as con:
        con.row_factory = sqlite3.Row
        seed = con.execute(f'SELECT * FROM {match[1]} WHERE Id=?', (int(match[2]),)).fetchone()
        books = {r['Id']: r['Name'] for r in con.execute('SELECT Id, Name FROM Books')}
    if seed is None or t.get('existing_numeric_source_ref') != seed[position[2]]:
        raise ValueError('Sunday numeric source witness mismatch')
    table = next((item for item in oracle['tables'] if item['id'] == t['table_id']), None)
    date = dt.date.fromisoformat(ctx['gregorian_date'])
    selection = calendar.sunday_policy_selection(date)
    if selection != (match[1], seed['Month_Number'], seed['Day']):
        raise ValueError('Sunday date/context selection mismatch')
    expected_title = ('Second Day of Nativity' if match[1] == 'AnnualReadings' else
                      calendar.SUNDAY_ORDINALS[seed['Day'] - 1].capitalize() + ' Sunday of ' +
                      {1: 'Tout', 6: 'Meshir', 13: 'Nesi'}[seed['Month_Number']])
    if ctx['liturgical_place'] != expected_title or str(ctx['source_order']) != str(calendar.SUNDAY_POSITIONS.index(position) + 1):
        raise ValueError('Sunday occasion/assigned order mismatch')
    psalm = slot == 'Psalm'
    if psalm and (t.get('normalization_state') != 'HELD' or 'HELD' not in t['normalization_warning']):
        raise ValueError('Sunday Psalm alignment hold lost')
    if not psalm and t.get('normalization_state') != 'source_qualified':
        raise ValueError('Sunday normalization state changed')
    if table:
        matches = [(doc, block) for doc in table['documents'] if doc['label'].split('-')[0] == ctx['service_section']
                   for block in doc['assigned_blocks'] if block == t.get('source_block')]
        if len(matches) != 1:
            raise ValueError('Sunday literal source body/context mismatch')
        doc, block = matches[0]
        path = str(calendar.SUNDAY_FIXTURE / doc['textPath'])
        locator = f"{path}:lines {block['line_start']}-{block['line_end']}"
        if (t.get('source_document_path') != path or t.get('source_document_sha256') != doc['textSha256']
                or t.get('source_capture_date') != table['date'] or t.get('evidenceLocator') != locator):
            raise ValueError('Sunday document/path/locator/capture mismatch')
        expected_ref = normalize_numeric_ref(seed[position[2]], books) if psalm else block['printed_ref']
    else:
        if any(t.get(k) for k in ('source_block', 'source_capture_date', 'source_document_path', 'source_document_sha256')):
            raise ValueError('Uncaptured Sunday cannot claim source body')
        locator = FILE
        if t.get('evidenceLocator') != locator:
            raise ValueError('Sunday uncaptured source locator mismatch')
        expected_ref = normalize_numeric_ref(seed[position[2]], books)
        # The accepted post-Nativity canary supplies non-Psalm headings for
        # AnnualReadings 4/30, but this old adapter claims no attached body.
        # Authenticate its reference without inventing a captured-body envelope.
        if not psalm and match[1] == 'AnnualReadings' and (seed['Month_Number'], seed['Day']) == (4, 30):
            canary = next(item for item in oracle['tables'] if item['id'] == 'canary-postNativity')
            headings = [b['printed_ref'] for d in canary['documents'] for b in d['assigned_blocks']]
            expected_ref = headings[calendar.SUNDAY_POSITIONS.index(position)]
    primary = next((item for item in oracle['tables'] if
                    (item['family'] == match[1] and item['key'] == {'Month_Number': seed['Month_Number'], 'Day': seed['Day']})
                    or (match[1] == 'AnnualReadings' and item['id'] == 'canary-postNativity')), None)
    headings = [ref for doc in primary['documents'] for ref in doc['printedReferences']] if primary else []
    expected_raw = headings[calendar.SUNDAY_POSITIONS.index(position)] if headings and not psalm else seed[position[2]]
    if ctx['raw_ref'] != expected_raw:
        raise ValueError('Sunday raw_ref primary source mismatch')
    if (type(ctx['source_row_id']) is bool or not str(ctx['source_row_id']).isdigit()
            or (int(ctx['source_row_id']) == 0 and current_source_row(t.get('state', {})))):
        raise ValueError('Sunday missing/invalid source row identity')
    allowed = {canonicalize_text_ref(expected_ref)}
    if not table or psalm:
        allowed.update(canonicalize_text_ref(p['normalized_segment']) for p in iter_numeric_ref_segments(seed[position[2]], books))
    if canonicalize_text_ref(ctx['source_ref']) not in allowed or canonicalize_text_ref(ctx['passage']) not in allowed:
        raise ValueError('Sunday source_ref/fragment counterfeit')
    aliases = {'passage': 'source_label', 'reading_slot': 'slot', 'liturgical_place': 'occasion'}
    for field in CONTEXT_FIELDS:
        name = field if field in row else aliases.get(field, field)
        if name in row and str(row[name]) != str(ctx[field]):
            raise ValueError('Sunday consumer context/source disagreement: ' + name)
    for field, value in (('source_family', FAMILY), ('source_kind', 'copticchurch_date'), ('source_key', KEY), ('source_file', FILE), ('source_locator', locator)):
        if field in row and row[field] != value:
            raise ValueError('Sunday public attribution mismatch: ' + field)
    import build_design_deliverables as design
    registry = design.source_registry_for_key(KEY)
    for field, key in (('source_title', 'title'), ('source_edition', 'edition')):
        if field in row and row[field] != registry[key]:
            raise ValueError('Sunday public attribution mismatch: ' + field)
    if 'identity_key' in row:
        expected = design.identity_for(ctx['passage'], row.get('source_kind', 'copticchurch_date'), source_transport=t)
        for field in ('identity_key', 'reading_type', 'reading_name', 'display_ref', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json',
                      'source_convention', 'canonicalization_confidence', 'canonicalization_note'):
            if field in row and row[field] != expected[field]:
                raise ValueError('Sunday identity/hold promotion: ' + field)
    if row.get('identity_key') and 'current_status' in row and current_source_row(row) != current_source_row(t.get('state', {})):
        raise ValueError('Sunday contradictory consumer/source state')
    if 'current_status' in row:
        expected_status = ('historical_candidate_removed' if not current_source_row(t.get('state', {}))
                           else 'pending_psalm_equivalence_unresolved' if psalm else 'current_public_or_local_reference')
        if row['current_status'] != expected_status:
            raise ValueError('Sunday consumer state restoration/promotion')
    return ctx, locator


def validate_citation_output(row, t, p, oracle):
    required = {'identity_key', 'display_ref', 'canonical_mt_ref', 'canonical_lxx_ref',
                'source_key', 'source_title', 'source_edition', 'source_locator', 'source_url',
                'source_ref', 'occasion', 'calendar_key', 'day_title', 'service_hour', 'slot',
                'current_status', 'removed_marker', 'citation'}
    if not required.issubset(row) or set(row) - required - {'runtime_activation', 'consumer_eligible'}:
        raise ValueError('Sunday incomplete/ambiguous standalone serialized output')
    ctx, _ = _proof(row, t, oracle)
    import build_design_deliverables as design
    virtual = dict(ctx, source_key=KEY, source_title=SOURCE,
                   source_edition=design.source_registry_for_key(KEY)['edition'],
                   source_locator=t['evidenceLocator'], source_file=FILE,
                   provenance=json.dumps(p, ensure_ascii=False, sort_keys=True), url='https://copticreader.org/app/')
    if row['citation'] != design._row_citation_unchecked(virtual):
        raise ValueError('Sunday serialized citation attribution mismatch')


def validate_rows(rows, *, serialized=True, transport_mode: TransportMode | None = None):
    mode = transport_mode if transport_mode is not None else ('output' if serialized else 'raw')
    if mode not in ('raw', 'presentation', 'daily', 'reverse', 'output') or (not serialized and mode != 'raw'):
        raise ValueError('Sunday contradictory/unknown trusted transport mode')
    qualified = [r for r in rows if is_sunday(r)]
    if not qualified:
        return
    from calendar_resolution import load_sunday_evidence
    try:
        oracle = load_sunday_evidence()  # Reauthenticate standalone consumer witness bytes.
    except RuntimeError as exc:
        # Translate only the loader's explicit witness-drift errors, not IO.
        if str(exc) not in ('Sunday evidence manifest drift', 'Sunday SQLite source drift') and not str(exc).startswith('Sunday evidence source drift: '):
            raise
        raise ValueError(str(exc)) from exc
    for row in qualified:
        if any(flag in row and row[flag] is not False for flag in ('runtime_activation', 'consumer_eligible')):
            raise ValueError('Sunday malformed nonactivation flag')
        p = provenance(row)
        t = transport(row)
        if mode == 'output':
            # Compatibility union of complete serialized schemas. Never route
            # to raw/presentation from output key presence or failed guards.
            for lane in ('daily', 'reverse'):
                try:
                    validate_rows([row], transport_mode=lane)
                    break
                except ValueError:
                    pass
            else:
                validate_citation_output(row, t, p, oracle)
            continue
        if mode in ('daily', 'reverse'):
            required = {'identity_key', 'display_ref', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json', 'current_status',
                        'source_family', 'source_kind', 'source_locator'}
            required |= {'source_disclosure', 'occasion', 'service_section', 'service_hour', 'slot', 'reading_type', 'reading_name', 'removed_marker'}
            required |= ({'source_file', 'source_row_id', 'source_group_key', 'slot_type', 'slot_order', 'service_order', 'superseded_by_ref'} if mode == 'daily' else
                         {'source_title', 'source_edition', 'source_disclosure_count', 'collapsed_row_count', 'provenance', 'calendar_keys', 'day_titles', 'slot_type', 'slot_order', 'occasion_kind', 'hour_theme', 'authority_tier', 'attestation_year_min', 'attestation_year_max', 'attestation_years'})
            if not required.issubset(row):
                raise ValueError('Sunday serialized identity/attribution omitted')
            disclosure = strict_json(row.get('source_disclosure'))
            if not isinstance(disclosure, list) or len(disclosure) != 1 or not isinstance(disclosure[0], dict):
                raise ValueError('Sunday missing/duplicate serialized disclosure')
            item = disclosure[0]
            ts = item.get('consumer_source_transport')
            if not isinstance(ts, list) or not ts or any(not isinstance(x, dict) for x in ts):
                raise ValueError('Sunday missing serialized source envelopes')
            if mode == 'reverse' and 'consumer_source_envelopes' not in p:
                raise ValueError('Sunday reverse authoritative envelope omitted')
            bound = p.get('consumer_source_envelopes', [t] if t else ts)
            if ts != bound or (mode == 'daily' and len(ts) != 1):
                raise ValueError('Sunday serialized disclosure omission/forgery/state disagreement')
            for index, value in enumerate(ts):
                # Reverse groups can span several years. Their public spans are
                # the first representative's exact identity; later witnesses
                # retain their own dated validation notes in the envelope.
                if any(flag in value and value[flag] is not False for flag in ('runtime_activation', 'consumer_eligible')):
                    raise ValueError('Sunday malformed envelope nonactivation flag')
                omitted = {'gregorian_date', 'source_row_id', 'source_order'} if mode == 'reverse' else set()
                if index:
                    omitted.update({'spans_json', 'canonicalization_note'})
                _proof({k: v for k, v in row.items() if k not in omitted}, value, oracle)
            if mode == 'daily' and not current_source_row(ts[0].get('state', {})):
                raise ValueError('Sunday removed source cannot enter daily serialization')
            if 'source_disclosure_count' in row and row['source_disclosure_count'] != '1':
                raise ValueError('Sunday disclosure count mismatch')
            if mode == 'reverse' and row['collapsed_row_count'] != str(len(ts)):
                raise ValueError('Sunday collapsed row count mismatch')
            if mode == 'daily':
                ctx = ts[0]['consumer_context']
                group = '|'.join(str(value or '') for value in ('copticchurch_date', ctx['source_row_id'], ctx['liturgical_place'], row['service_hour'], ctx['reading_slot']))
                if row['source_group_key'] != group:
                    raise ValueError('Sunday daily source group mismatch')
            import build_design_deliverables as design
            registry = design.source_registry_for_key(KEY)
            expected = {'source_family': FAMILY, 'source_kind': row.get('source_kind'),
                        'source_edition': registry['edition'], 'source_title': registry['title'],
                        'consumer_source_transport': ts, 'source_locator': ts[0]['evidenceLocator']}
            years = sorted({x['consumer_context']['gregorian_date'][:4] for x in ts})
            if years:
                expected.update(attested_year_min=years[0], attested_year_max=years[-1])
                if not design.years_are_contiguous(map(int, years)):
                    expected['attested_years'] = '; '.join(years)
            if item != expected:
                raise ValueError('Sunday serialized source attribution/years/cell mismatch')
        else:
            required = set(CONTEXT_FIELDS) if mode == 'raw' else {'identity_key', 'display_ref', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json', 'current_status', 'source_label', 'source_ref', 'raw_ref', 'gregorian_date', 'service_section', 'slot', 'occasion', 'source_row_id', 'source_order', 'source_key', 'source_file', 'source_family', 'source_kind', 'source_locator', 'source_title', 'source_edition', 'provenance'}
            if mode == 'presentation':
                required |= {'reading_type', 'reading_name', 'source_convention', 'canonicalization_confidence', 'canonicalization_note', 'service_hour'}
            if not required.issubset(row):
                raise ValueError('Sunday required input schema omitted')
            if any(flag in t and t[flag] is not False for flag in ('runtime_activation', 'consumer_eligible')):
                raise ValueError('Sunday malformed envelope nonactivation flag')
            ctx, _ = _proof(row, t, oracle)
            if 'citation' in row:
                import build_design_deliverables as design
                virtual = dict(ctx, source_key=KEY, source_title=SOURCE,
                               source_edition=design.source_registry_for_key(KEY)['edition'],
                               source_locator=t['evidenceLocator'], source_file=FILE,
                               provenance=json.dumps(p, ensure_ascii=False, sort_keys=True), url='https://copticreader.org/app/')
                if row['citation'] != design._row_citation_unchecked(virtual):
                    raise ValueError('Sunday serialized citation attribution mismatch')
