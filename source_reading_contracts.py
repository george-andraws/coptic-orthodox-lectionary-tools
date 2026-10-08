"""Hash-bound edition/fragment contracts. Research acceptance is not activation.

All projections are explicitly candidate-only. Existing MT parsing/bounds and
legacy identity are intentionally untouched. The immutable object namespace is
portable; original evidence paths remain provenance labels, never read targets.
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / 'tests/fixtures/edition_fragment_contract_v1'
MANIFEST_SHA256 = '707c408c1ab6dcd6650ae5fff391e9c6aec67171dac6cd9f44311d3ab45938b4'
AUDIT_LABEL = '/Users/ga/workspace/lectionary-comprehensive-audit-2026-10-07/'
PINS = {
    'lent-normalization-corrections-02/IMMUTABLE-HASH-RECEIPT.json': '3ffca22069b75ee7ef9ce09102c86f86d916be198aad14ed280a6977609a69b3',
    'lent-corrections-independent-review-02/FINAL-RECEIPT.json': '266c7611e5911cfef28bba80b48373d409c14e7a06e3bce38a558c63b367800b',
    'psalm-normalization-special-corrections-03/FINAL-RECEIPT.json': '27d40d077d38adf59c96d06c120933a26ce117f0a80cae355be57b9bbaed4e52',
    'psalm-special-corrections-independent-review-03/FINAL-RECEIPT.json': '2216675596486c3730ade8f992383225a869b550adf2252830de8314fd5b1c64',
}
EDITION_IDS = frozenset({
    'cpdv_2009_original', 'nkjv_coordinates_boundary_witness',
    'coptic_reader_isaiah_mixed_nkjv_brenton',
    'coptic_reader_proverbs_nkjv_plus_lxx',
    'coptic_reader_genesis_nkjv_clause_boundaries',
    'coptic_reader_tobit_mixed_unresolved', 'reader_psalm_selected_fragments',
})
CONVENTIONS = frozenset({'edition_qualified', 'reader_source_fragment_qualified',
                         'mt_nkjv_coordinate_witness_not_exact_translation_claim'})
CONTRACT_KIND = 'edition_fragment_candidate'
CONTRACT_KEY = 'edition_fragment_contract_v1'


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def bound_bytes(label: str, expected: str | None = None) -> bytes:
    raw = (FIXTURES / 'bindings.json').read_bytes()
    if digest(raw) != MANIFEST_SHA256:
        raise ValueError('source contract fixture manifest hash mismatch')
    binding = json.loads(raw).get(label)
    if not binding or (expected and binding['sha256'] != expected):
        raise ValueError('source contract unbound document: ' + label)
    relative = Path(binding['file'])
    path = FIXTURES / relative
    if relative.is_absolute() or '..' in relative.parts or path.is_symlink():
        raise ValueError('source contract document path escape')
    data = path.read_bytes()
    if digest(data) != binding['sha256']:
        raise ValueError('source contract document hash mismatch: ' + label)
    return data


def load_reviewed_tables() -> tuple[list[dict], list[dict]]:
    receipts = {name: json.loads(bound_bytes(AUDIT_LABEL + name, pin))
                for name, pin in PINS.items()}
    lent_receipt = receipts['lent-normalization-corrections-02/IMMUTABLE-HASH-RECEIPT.json']
    review = receipts['lent-corrections-independent-review-02/FINAL-RECEIPT.json']
    if (review['research_metadata_approved'] is not True
            or review['runtime_activation_approved'] is not False
            or review['corrected_packet_receipt_sha256'] != PINS['lent-normalization-corrections-02/IMMUTABLE-HASH-RECEIPT.json']):
        raise ValueError('source contract independent Lent acceptance mismatch')
    outputs = {r['path']: r['sha256'] for r in lent_receipt['output_manifest']}
    candidate = json.loads(bound_bytes(AUDIT_LABEL + 'lent-normalization-corrections-02/normalization-candidate.json', outputs['normalization-candidate.json']))
    # The proposed overlay is independently pinned as well; it cannot enable
    # activation by changing eligibility flags in a new local fixture.
    overlay = json.loads(bound_bytes(AUDIT_LABEL + 'lent-normalization-corrections-02/proposed-overlay.json', outputs['proposed-overlay.json']))
    if (candidate['contract_implemented'] is not False or candidate['counts']['runtime_activated_readings'] != 0
            or overlay['not_applied'] is not True or overlay['runtime_activation'] is not False):
        raise ValueError('source contract premature promotion')
    psalm_receipt = receipts['psalm-normalization-special-corrections-03/FINAL-RECEIPT.json']
    psalm_review = receipts['psalm-special-corrections-independent-review-03/FINAL-RECEIPT.json']
    if (psalm_review['consumer_eligible'] is not False or psalm_review['release_approval'] is not False
            or psalm_review['packet_receipt_sha256'] != PINS['psalm-normalization-special-corrections-03/FINAL-RECEIPT.json']):
        raise ValueError('source contract premature Psalm promotion')
    psalms = [json.loads(line) for line in bound_bytes(AUDIT_LABEL + 'psalm-normalization-special-corrections-03/corrections.jsonl', psalm_receipt['artifact_hashes']['corrections.jsonl']).decode().splitlines()]
    if {r['id'] for r in psalms} != set(psalm_review['corrected_ids']):
        raise ValueError('source contract corrected Psalm scope mismatch')
    return candidate['tables'], psalms


def authenticate_source_namespace() -> None:
    """Check every copied source/witness object before a local projection."""
    raw = (FIXTURES / 'bindings.json').read_bytes()
    if digest(raw) != MANIFEST_SHA256:
        raise ValueError('source contract fixture manifest hash mismatch')
    checked = set()
    for label, binding in json.loads(raw).items():
        if binding['sha256'] not in checked:
            bound_bytes(label, binding['sha256'])
            checked.add(binding['sha256'])


def ordinary_occasion(table: dict) -> str:
    week = re.search(r'(\d+)(?:st|nd|rd|th) Week of Great Fast', table['context'])
    if not week:
        raise ValueError('source contract unknown Lent occasion')
    names = {3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth'}
    return dt.date.fromisoformat(table['civil_date']).strftime('%A') + ' of the ' + names[int(week[1])] + ' week of Great Lent'


def validate_applicability(table: dict, date: str, occasion: str) -> None:
    from calendar_resolution import julian_pascha_gregorian
    day = dt.date.fromisoformat(date)
    # A supplied label is not proof of the actually resolved occasion. This
    # candidate lane admits only the authenticated capture date/context. Future
    # recurrence needs an independently bound resolved-date context adapter.
    if (date != table['civil_date']
            or (day - julian_pascha_gregorian(day.year)).days != table['pascha_offset_days']
            or occasion != ordinary_occasion(table)):
        raise ValueError('source contract actual occasion/offset mismatch')


def authenticate_table(table: dict) -> dict:
    tables, _ = load_reviewed_tables()
    expected = next((t for t in tables if t['civil_date'] == table.get('civil_date')), None)
    if expected is None or table != expected:
        raise ValueError('source contract whole table metadata/order/bounds mismatch')
    source = bound_bytes(table['text_path'], table['text_sha256']).decode()
    context_label = str(Path(table['text_path']).with_name('context.txt'))
    if bound_bytes(context_label).decode().strip() != table['context'].strip():
        raise ValueError('source contract capture context mismatch')
    lines = source.splitlines()
    for i, reading in enumerate(table['readings'], 1):
        if (reading['source_order'] != i or reading['source_slot'] != 'OT' + str(i)
                or lines[reading['source_line'] - 1] != reading['printed_ref']
                or reading['raw_source_block'] not in source
                or reading['edition_id'] not in EDITION_IDS):
            raise ValueError('source contract literal heading/slot/block/edition mismatch')
        if reading['edition_id'] == 'cpdv_2009_original':
            maxima = {'Sir': {2: 23, 3: 4, 8: 22, 9: 25, 10: 1}, 'Dan': {14: 42}}
            for run in reading['edition_bounds_qualification']['ordered_observed_chapter_runs']:
                if run['verse_end'] > maxima[reading['book']].get(run['chapter'], 0):
                    raise ValueError('source contract controlled CPDV bounds exceeded')
    return expected


def authenticate_psalm(row: dict) -> dict:
    _, psalms = load_reviewed_tables()
    expected = next((r for r in psalms if r['id'] == row.get('id')), None)
    if expected is None or row != expected or row['consumer_eligible'] is not False:
        raise ValueError('source contract Psalm metadata/eligibility mismatch')
    capture = row['capture_context_metadata']
    source = bound_bytes(capture['rawTextPath'], capture['rawTextSha256']).decode()
    if (source.splitlines()[row['line_start'] - 1] != row['heading_exact']
            or row['block_raw'] not in source or digest(row['block_raw'].encode()) != row['block_sha256']
            or digest(row['body_english'].encode()) != row['body_sha256']):
        raise ValueError('source contract Psalm whole document/heading/body mismatch')
    end = 0
    for order, fragment in enumerate(row['source_fragments'], 1):
        if (fragment['source_order'] != order or fragment['start'] != end
                or row['body_english'][fragment['start']:fragment['end']] != fragment['source_literal']):
            raise ValueError('source contract ordered literal fragment coverage mismatch')
        end = fragment['end']
        for witness in fragment['witness_bindings'].values():
            bound_bytes(witness['raw_path'], witness['raw_sha256'])
    if end != len(row['body_english']):
        raise ValueError('source contract fragment truncation')
    return expected


def envelope(lane: str, table_id: str, ordinal: int, metadata: dict, date: str, occasion: str) -> dict:
    return {'lane': lane, 'table_id': table_id, 'ordinal': ordinal,
            'metadata': copy.deepcopy(metadata), 'actual_date': date,
            'actual_occasion': occasion, 'consumer_eligible': False,
            'runtime_activation': False}


def project_table(table: dict, actual_date: str | None = None, actual_occasion: str | None = None) -> list[dict]:
    authenticate_source_namespace()
    authenticate_table(table)
    date = actual_date or table['civil_date']
    occasion = actual_occasion or ordinary_occasion(table)
    validate_applicability(table, date, occasion)
    if table['staged']:
        return []  # Whole March 27, never five apparently safe companions.
    rows = []
    for i, reading in enumerate(table['readings'], 1):
        rows.append(_raw_row(envelope('lent', table['civil_date'], i, reading, date, occasion),
                             reading['printed_ref'], reading.get('canonical_edition_ref') or reading['normalized_literal_ref'], table['text_path'], i, occasion, date, 'Matins', reading['source_slot']))
    return rows


def project_psalm(row: dict, *, candidate_date: str = '') -> list[dict]:
    """Optional capture-date serializer probe, NOT a civil-date appointment."""
    authenticate_source_namespace()
    authenticate_psalm(row)
    if candidate_date not in ('', row['capture_context_metadata']['captureTime'][:10]):
        raise ValueError('source contract candidate Psalm date must be capture date')
    occasion = ' / '.join(row['navigation'])
    e = envelope('psalm', row['id'], row['source_assigned_order'], row, candidate_date, occasion)
    return [_raw_row(e, row['heading_exact'], row['printed_ref'], row['capture_context_metadata']['rawTextPath'],
                     row['source_assigned_order'], occasion, candidate_date, 'Special Service', 'Psalm')]


def _raw_row(e: dict, literal: str, parser_input: str, source_file: str, order: int,
             occasion: str, date: str, section: str, slot: str) -> dict:
    return {'source_contract': e, 'source_kind': CONTRACT_KIND,
            'source_family': 'reviewed_metadata_candidate_only',
            'source_file': source_file, 'source_row_id': order, 'source_order': order,
            'source_token_order': 1, 'source_ref': literal, 'raw_ref': literal,
            'passage': parser_input, 'normalized_ref': parser_input, 'normalized_segment': parser_input,
            'liturgical_place': occasion, 'day_title': occasion, 'calendar_key': occasion,
            'gregorian_date': date, 'service_section': section, 'service_hour': '',
            'reading_slot': slot, 'reading_type': slot,
            'provenance': canonical_json(e), 'url': 'https://copticreader.org/app/#/document'}


def validate_envelope(e: dict) -> dict:
    # Standalone consumers must reauthenticate the immutable witness namespace,
    # even when these rows were projected before a local object changed.
    authenticate_source_namespace()
    if not isinstance(e, dict):
        raise ValueError('source contract malformed envelope')
    if set(e) != {'lane', 'table_id', 'ordinal', 'metadata', 'actual_date', 'actual_occasion', 'consumer_eligible', 'runtime_activation'} or e['consumer_eligible'] is not False or e['runtime_activation'] is not False:
        raise ValueError('source contract malformed envelope/premature promotion')
    if e['lane'] == 'lent':
        tables, _ = load_reviewed_tables()
        table = next((t for t in tables if t['civil_date'] == e['table_id']), None)
        if table is None or table['staged']:
            raise ValueError('source contract unknown/staged whole table')
        authenticate_table(table)
        validate_applicability(table, e['actual_date'], e['actual_occasion'])
        if type(e['ordinal']) is not int or not 1 <= e['ordinal'] <= len(table['readings']):
            raise ValueError('source contract ordinal outside table')
        r = table['readings'][e['ordinal'] - 1]
        if r != e['metadata']:
            raise ValueError('source contract reading metadata/edition/bounds/fragment mismatch')
    elif e['lane'] == 'psalm':
        r = authenticate_psalm(e['metadata'])
        if (e['table_id'] != r['id'] or e['ordinal'] != r['source_assigned_order']
                or e['actual_date'] not in ('', r['capture_context_metadata']['captureTime'][:10])
                or e['actual_occasion'] != ' / '.join(r['navigation'])):
            raise ValueError('source contract Psalm context/slot mismatch')
    else:
        raise ValueError('source contract unknown lane')
    return r


def identity(e: dict) -> dict:
    r = validate_envelope(e)
    psalm = e['lane'] == 'psalm'
    edition = 'reader_psalm_selected_fragments' if psalm else r['edition_id']
    literal = r['heading_exact'] if psalm else r['printed_ref']
    ref = r['printed_ref'] if psalm else r.get('canonical_edition_ref') or r['normalized_literal_ref']
    convention = 'reader_source_fragment_qualified' if psalm else r['source_convention']
    # These are SOURCE coordinates. Exact full-body canonical counterparts are
    # deliberately empty even for boundary-only NKJV witnesses.
    base_spans = [] if psalm else r['spans']
    spans = []
    for run in base_spans or [None]:
        span = {'source_ref': literal, 'source_convention': convention,
                'canonical_mt_ref': '', 'canonical_lxx_ref': '',
                'confidence': 'medium', 'validation_basis': 'hash-bound independently reviewed metadata; candidate only',
                'book': 'Ps' if psalm else r['book'],
                'chapter_start': None if psalm else run['chapter_start'],
                'verse_start': None if psalm else run['verse_start'],
                'chapter_end': None if psalm else run['chapter_end'],
                'verse_end': None if psalm else run['verse_end'],
                'edition_id': edition, 'canonical_edition_ref': ref,
                'coordinate_scope': 'source_only_not_exact_MT_or_universal_LXX'}
        spans.append(span)
    spans[0][CONTRACT_KEY] = copy.deepcopy(e)
    spans[0]['source_fragments'] = copy.deepcopy(r['source_fragments'] if psalm else r['fragment_inventory'])
    spans[0]['source_body'] = r['body_english'] if psalm else copy.deepcopy(r['source_body_verses'])
    spans[0]['raw_source_block'] = r['block_raw'] if psalm else r['raw_source_block']
    material = {'edition': edition, 'source_coordinates': ref,
                'body': spans[0]['source_body'], 'fragments': spans[0]['source_fragments'],
                'raw_source_block': spans[0]['raw_source_block']}
    # Capture line/date never supplies full-body equivalence. Keep the exact
    # fragment sequence and source-coordinate edition separate from legacy IDs.
    key = 'rid_' + digest(('edition-fragment-v1|' + canonical_json(material)).encode())[:20]
    return {'identity_key': key, 'reading_type': 'scripture', 'reading_name': '',
            'source_label': literal, 'display_ref': ref + ' [' + edition + '; candidate only]',
            'canonical_mt_ref': '', 'canonical_lxx_ref': '', 'source_convention': convention,
            'canonicalization_confidence': 'medium',
            'canonicalization_note': 'Exact source body/edition/fragments preserved. Covering counterparts are metadata only; no current activation approved.',
            'spans_json': json.dumps(spans, ensure_ascii=False, sort_keys=True)}


def strict_transport_json(raw: str):
    """Never let duplicate JSON members mask a contradictory public claim."""
    def unique_members(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('source contract duplicate serialized member: ' + key)
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique_members)


def row_envelope(row: dict) -> dict | None:
    e = row.get('source_contract')
    raw_spans = row.get('spans_json') or '[]'
    controlled = e is not None or row.get('source_kind') == CONTRACT_KIND or CONTRACT_KEY in raw_spans
    spans = strict_transport_json(raw_spans) if controlled else json.loads(raw_spans)
    embedded = next((s[CONTRACT_KEY] for s in spans if CONTRACT_KEY in s), None)
    if e is not None and embedded is not None and e != embedded:
        raise ValueError('source contract envelope disagreement')
    provenance = row.get('provenance')
    transported = None
    if row.get('source_kind') == CONTRACT_KIND and provenance:
        try:
            transported = strict_transport_json(provenance) if isinstance(provenance, str) else provenance
        except (ValueError, TypeError) as exc:
            raise ValueError('source contract malformed provenance transport') from exc
        if not isinstance(transported, dict):
            raise ValueError('source contract malformed provenance envelope')
    e = e or embedded or transported
    if transported is not None and transported != e:
        raise ValueError('source contract provenance disagreement')
    if row.get('source_kind') == CONTRACT_KIND and not e:
        raise ValueError('source contract missing for edition kind')
    return e


# Transport context is selected by the caller, never inferred as a permission
# from source_ref/count/group keys. The standalone 'output' default is the
# complete reverse schema; daily containers explicitly supply their trusted lane.
COMMON_OUTPUT_FIELDS = frozenset('occasion service_section service_hour slot display_ref identity_key reading_type reading_name removed_marker current_status source_kind source_family source_disclosure spans_json canonical_mt_ref canonical_lxx_ref slot_type slot_order source_locator'.split())
DAILY_FIELDS = COMMON_OUTPUT_FIELDS | frozenset('source_file source_row_id source_group_key service_order superseded_by_ref'.split())
REVERSE_FIELDS = COMMON_OUTPUT_FIELDS | frozenset('calendar_keys day_titles occasion_kind hour_theme authority_tier provenance source_edition source_title source_disclosure_count attestation_year_min attestation_year_max attestation_years collapsed_row_count'.split())
PRESENTATION_FIELDS = frozenset('identity_key reading_type reading_name source_label display_ref canonical_mt_ref canonical_lxx_ref source_convention canonicalization_confidence canonicalization_note spans_json current_status removed_marker source_key source_title source_edition source_locator source_kind source_family source_file source_row_id source_order source_token_order occasion gregorian_date service_section service_hour slot reading_slot source_ref raw_ref provenance'.split())
RAW_FIELDS = frozenset('source_kind source_family source_file source_row_id source_order source_token_order source_ref raw_ref passage normalized_ref normalized_segment liturgical_place gregorian_date service_section service_hour reading_slot reading_type provenance'.split())


def validate_transport_schema(row: dict, mode: str) -> None:
    schemas = {'raw': RAW_FIELDS, 'presentation': PRESENTATION_FIELDS,
               'daily': DAILY_FIELDS, 'reverse': REVERSE_FIELDS}
    if mode == 'output':
        mode = 'reverse'
    if mode in schemas:
        if not schemas[mode] <= row.keys():
            raise ValueError('source contract missing required ' + mode + ' fields: ' + ', '.join(sorted(schemas[mode] - row.keys())))
        if mode in ('daily', 'reverse'):
            other = REVERSE_FIELDS if mode == 'daily' else DAILY_FIELDS
            if (other - COMMON_OUTPUT_FIELDS) & row.keys():
                raise ValueError('source contract contradictory output schemas')
    else:
        raise ValueError('source contract unknown trusted transport mode')
    if mode != 'raw' and row['current_status'] != 'unknown':
        raise ValueError('source contract candidate current_status must be unknown')


def expected_source_disclosure(e: dict, r: dict) -> dict:
    literal = r['heading_exact'] if e['lane'] == 'psalm' else r['printed_ref']
    source_file = r['capture_context_metadata']['rawTextPath'] if e['lane'] == 'psalm' else r['text_path']
    expected = {
        'source_family': 'reviewed_metadata_candidate_only',
        'source_kind': CONTRACT_KIND,
        'source_edition': 'Hash-bound captured source body; candidate projection only, no activation approval',
        'source_title': 'Coptic Reader independently reviewed edition/fragment research metadata',
        'source_locator': 'https://copticreader.org/app/#/document; ' + source_file + ':row ' + str(e['ordinal']) + '; source_ref=' + literal,
        CONTRACT_KEY: e,
    }
    if e['actual_date']:
        expected['attested_year_min'] = expected['attested_year_max'] = e['actual_date'][:4]
    return expected


def validate_serialized_disclosure(row: dict, e: dict, r: dict, *, transport_mode: str = 'output') -> None:
    """Authenticate public disclosure; only an explicit input lane rebuilds it."""
    if transport_mode in ('raw', 'presentation'):
        return
    try:
        raw = row.get('source_disclosure')
        disclosure = strict_transport_json(raw) if isinstance(raw, str) else raw
    except (ValueError, TypeError) as exc:
        raise ValueError('source contract malformed serialized disclosure') from exc
    if not isinstance(disclosure, list) or len(disclosure) != 1 or not isinstance(disclosure[0], dict):
        raise ValueError('source contract missing/duplicate serialized disclosure')
    item = disclosure[0]
    if item.get(CONTRACT_KEY) != e:
        raise ValueError('source contract serialized disclosure envelope/body/fragments disagreement')
    validate_envelope(item[CONTRACT_KEY])
    expected = expected_source_disclosure(e, r)
    if item != expected:
        raise ValueError('source contract serialized disclosure source/context/state mismatch')
    for field in ['source_family', 'source_kind', 'source_edition', 'source_title', 'source_locator']:
        if field in row and row[field] != expected[field]:
            raise ValueError('source contract serialized disclosure scalar disagreement: ' + field)
    for field in ['source_disclosure_count', 'collapsed_row_count']:
        if field in row and row[field] != '1':
            raise ValueError('source contract serialized disclosure count mismatch: ' + field)


def validate_consumer_rows(rows: list[dict], *, candidate_projection: bool = False,
                           serialized: bool = True, transport_mode: str | None = None) -> None:
    mode = transport_mode if transport_mode is not None else ('output' if serialized else 'raw')
    if mode not in ('raw', 'presentation', 'daily', 'reverse', 'output') or (not serialized and mode != 'raw'):
        raise ValueError('source contract contradictory/unknown trusted transport mode')
    import sunday_consumer_contracts
    sunday_consumer_contracts.validate_rows(rows, serialized=serialized, transport_mode=mode)
    groups = {}
    for row in rows:
        e = row_envelope(row)
        if e is None:
            if candidate_projection:
                raise ValueError('source contract candidate projection requires bound rows only')
            continue
        if any(flag in row and row[flag] is not False for flag in ['consumer_eligible', 'runtime_activation']):
            raise ValueError('source contract malformed runtime flag/premature promotion forbidden')
        if (any(row.get(flag) is False for flag in ['active', 'is_active', 'include_in_current_index'])
                or any(str(row.get(field, '')).strip().lower().startswith(('removed', 'inactive', 'superseded', 'historical', 'omitted')) for field in ['status', 'state', 'projection_status', 'current_status'])
                or row.get('removed_marker') or row.get('superseded_by_ref')
                or row.get('consumer_eligible') is True or row.get('runtime_activation') is True
                or str(row.get('current_status', '')).startswith(('historical', 'current_confirmed'))):
            raise ValueError('source contract historical restoration/premature promotion forbidden')
        r = validate_envelope(e)
        validate_transport_schema(row, mode)
        if mode == 'presentation':
            source = expected_source_disclosure(e, r)
            for field in ['source_locator', 'source_title', 'source_edition']:
                if row[field] != source[field]:
                    raise ValueError('source contract presentation source scalar mismatch: ' + field)
        if row.get('source_kind') != CONTRACT_KIND:
            raise ValueError('source contract source kind mismatch')
        if row.get('source_family') != 'reviewed_metadata_candidate_only':
            raise ValueError('source contract source family mismatch')
        expected_file = r['capture_context_metadata']['rawTextPath'] if e['lane'] == 'psalm' else r['text_path']
        if 'source_file' in row and row['source_file'] != expected_file:
            raise ValueError('source contract source document mismatch')
        for order_field in ['source_order', 'source_row_id', 'slot_order']:
            # Reverse Psalm slot_order is the typed Psalm slot, not its ordinal
            # among every assigned reading in the captured rite document.
            if order_field == 'slot_order' and e['lane'] == 'psalm' and 'source_row_id' not in row:
                continue
            if order_field in row and (type(row[order_field]) is bool or str(row[order_field]) != str(e['ordinal'])):
                raise ValueError('source contract consumer order mismatch')
        if 'source_key' in row and row['source_key'] != 'coptic_reader_edition_fragment_candidate':
            raise ValueError('source contract source registry mismatch')
        if serialized:
            validate_serialized_disclosure(row, e, r, transport_mode=mode)
            expected = identity(e)
            fields = ['identity_key', 'reading_type', 'reading_name', 'display_ref', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json']
            if 'source_convention' in row:
                fields.append('source_convention')
            for field in fields:
                if row.get(field) != expected[field]:
                    raise ValueError('source contract serialized identity/fragments mismatch: ' + field)
        literal = r['heading_exact'] if e['lane'] == 'psalm' else r['printed_ref']
        if 'source_ref' in row and row['source_ref'] != literal:
            raise ValueError('source contract raw source_ref changed')
        expected_section = 'Special Service' if e['lane'] == 'psalm' else 'Matins'
        slot = 'Psalm' if e['lane'] == 'psalm' else r['source_slot']
        if (row.get('service_section') != expected_section or row.get('service_hour', '')
                or row.get('slot', row.get('reading_slot')) != slot
                or row.get('occasion', row.get('liturgical_place')) != e['actual_occasion']
                or row.get('gregorian_date', e['actual_date']) != e['actual_date']):
            raise ValueError('source contract actual consumer context/slot mismatch')
        group = (e['lane'], e['table_id'], e['actual_date'], e['actual_occasion'])
        groups.setdefault(group, []).append(e['ordinal'])
    tables, _ = load_reviewed_tables() if groups else ([], [])
    for (lane, table_id, _, _), orders in groups.items():
        expected = list(range(1, len(next(t for t in tables if t['civil_date'] == table_id)['readings']) + 1)) if lane == 'lent' else [orders[0]]
        if orders != expected:
            raise ValueError('source contract whole-table order/omission/duplicate mismatch')


def rehydrate_output_rows(rows: list[dict], *, transport_mode: str = 'output') -> list[dict]:
    """Restore builder inputs only AFTER authenticating the entire public output.

    Reconstruct from bound envelopes, not attacker extras or absent exporter
    fields. This retains previously supported output-to-builder round trips.
    """
    if transport_mode not in ('output', 'daily', 'reverse'):
        raise ValueError('source contract rehydration requires trusted output mode')
    validate_consumer_rows(rows, candidate_projection=True, transport_mode=transport_mode)
    raw = []
    for row in rows:
        e = row_envelope(row)
        if e is None:
            raise ValueError("source contract rehydration requires bound output")
        r = validate_envelope(e)
        psalm = e['lane'] == 'psalm'
        literal = r['heading_exact'] if psalm else r['printed_ref']
        ref = r['printed_ref'] if psalm else r.get('canonical_edition_ref') or r['normalized_literal_ref']
        file = r['capture_context_metadata']['rawTextPath'] if psalm else r['text_path']
        raw.append(_raw_row(e, literal, ref, file, e['ordinal'], e['actual_occasion'],
                            e['actual_date'], 'Special Service' if psalm else 'Matins',
                            'Psalm' if psalm else r['source_slot']))
    return raw


PASSAGE_DISCLOSURE_FIELDS = frozenset('identity_key display_ref canonical_mt_ref canonical_lxx_ref source_key source_title source_edition source_locator source_url source_ref occasion calendar_key day_title service_hour slot current_status removed_marker citation'.split())


def validate_passage_disclosure_output(rows: list[dict], context_rows: list[dict]) -> None:
    """Validate the unchanged flat disclosure schema against trusted context.

    This legacy table has no envelope cell; it cannot authenticate itself as a
    daily/reverse row. The builder supplies its already-authenticated input.
    """
    validate_consumer_rows(context_rows, transport_mode='presentation')
    if len(rows) != len(context_rows):
        raise ValueError('source contract disclosure output count mismatch')
    for output, context in zip(rows, context_rows):
        if row_envelope(context) is None:
            continue
        if set(output) != PASSAGE_DISCLOSURE_FIELDS:
            raise ValueError('source contract disclosure output required schema mismatch')
        for field in PASSAGE_DISCLOSURE_FIELDS - {'citation'}:
            expected = context.get(field, '')
            if field == 'source_ref':
                expected = context.get('source_ref', '') or context.get('raw_ref', '')
            if output[field] != expected:
                raise ValueError('source contract disclosure output scalar/identity/state mismatch: ' + field)
        parts = [f'{field}={context.get(field, "")}' for field in
                 ['source_key', 'source_title', 'source_edition', 'source_locator', 'source_file', 'source_row_id', 'source_ref']]
        parts.append('provenance=' + context['provenance'])
        if context.get('url'):
            parts.append('url=' + context['url'])
        if output['citation'] != ' | '.join(part for part in parts if not part.endswith('=')):
            raise ValueError('source contract disclosure output citation mismatch')


def is_candidate(row: dict) -> bool:
    return row_envelope(row) is not None
