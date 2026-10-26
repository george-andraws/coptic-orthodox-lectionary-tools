"""Four exact Bright Saturday selections; canonical numeric counterparts HELD.

load_bright_composite_rows / qualify_bright_composite_row authenticate fresh bytes
and exact string-valued raw CSV fields. bright_composite_identity_for is the ONLY
identity hook: it deliberately returns empty MT/LXX and spans, never the generic
Psalm normalizer. authenticate_bright_composite_identity revalidates passage-CSV
transport. A retained local capture is not a fresh app or independent confirmation.
Design daily/reverse callers must invoke these hooks before projecting these rows.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_RELATIVE = 'sources/coptic-reader/bright-composites-qualified-2026-10-25'
SOURCE_ROOT = ROOT / SOURCE_RELATIVE
CONTRACT_RELATIVE = 'sources/user-corrections/bright-saturday-composites-2026-10-25.json'
CONTRACT_SHA256 = '6365f62b235fcf3b0b41a7d96d11096de01a7cf93107c87943155a5aea5bc5a0'
SOURCE_KIND = 'bright_saturday_qualified_composite'
HOLD = 'bright_composite_edition_context_hold'
CONVENTION = 'coptic_reader_bright_composite_printed_selection_only'
RAW_FIELDS = ('passage source_kind source_family source_table source_file source_row_id '
              'source_order source_token_order superseded_by_ref superseded_reason '
              'liturgical_place calendar_key gregorian_date coptic_date day_title '
              'service_day service_hour service_section reading_slot reading_type '
              'source_ref raw_ref normalized_ref normalized_segment book book_abbrev '
              'chapter_start verse_start chapter_end verse_end significance_note '
              'synaxarium_note url provenance').split()


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _read(root, name):
    if type(name) is not str or Path(name).name != name or name in {'.', '..'}:
        raise ValueError('Bright evidence literal filename required')
    if root.is_symlink() or name not in {p.name for p in root.iterdir()}:
        raise ValueError('Bright evidence literal path missing')
    target = root / name
    if target.is_symlink() or not target.is_file():
        raise ValueError('Bright evidence symlink/non-file rejected')
    return target.read_bytes()


def authenticate_bright_composite_evidence(root=None):
    """Return fresh pinned contract; alternate evidence root is for portable tests."""
    root = SOURCE_ROOT if root is None else Path(root)
    try:
        path = ROOT / CONTRACT_RELATIVE
        if path.is_symlink():
            raise ValueError('Bright contract symlink rejected')
        data = path.read_bytes()
        if _sha(data) != CONTRACT_SHA256:
            raise ValueError('Bright contract authentication failed')
        contract = json.loads(data)
        for asset in contract['assets']:
            raw = _read(root, asset['file'])
            if len(raw) != asset['bytes'] or _sha(raw) != asset['sha256']:
                raise ValueError('Bright retained capture authentication failed')
        for doc in contract['documents'].values():
            lines = _read(root, doc['file']).decode().splitlines()
            body = '\n'.join(lines[doc['body_first_line']-1:doc['body_last_line']])
            if (len(lines) != doc['line_count'] or lines[0] != doc['document_title']
                    or lines[doc['heading_line']-1] != doc['heading_exact']
                    or _sha(body.encode()) != doc['body_sha256']):
                raise ValueError('Bright bounded heading/body/context drift')
        for record in contract['records']:
            doc = contract['documents'][record['document']]
            line = _read(root, doc['file']).decode().splitlines()[record['body_line']-1]
            if record['body_literal'] not in line or _sha(record['body_literal'].encode()) != record['body_literal_sha256']:
                raise ValueError('Bright selected clause drift')
        return contract
    except (OSError, KeyError, TypeError, IndexError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('Bright source evidence missing or malformed') from exc


def _row(record, contract):
    doc = contract['documents'][record['document']]
    q = {**record, 'document': doc, 'source_edition': contract['source_edition'],
         'source_path': SOURCE_RELATIVE + '/' + doc['file'],
         'contract_path': CONTRACT_RELATIVE, 'contract_sha256': CONTRACT_SHA256}
    row = dict.fromkeys(RAW_FIELDS, '')
    row.update(passage=record['source_selection_ref'], source_kind=SOURCE_KIND,
               source_family='bright_saturday', source_table='bright_composite_qualified_source',
               source_file=q['source_path'], source_row_id=record['handle'],
               source_order=record['source_order'], source_token_order=record['source_token_order'],
               liturgical_place='Bright Saturday', calendar_key='Bright Saturday',
               day_title='Bright Saturday', service_day='Bright Saturday',
               service_section=record['service_section'], reading_slot='Psalm', reading_type='Psalm',
               source_ref=record['printed_ref'], raw_ref=record['legacy_source_row']['reference'],
               normalized_ref=record['source_selection_ref'], normalized_segment=record['source_selection_ref'],
               significance_note=record['qualification_note'] + ' Canonical MT/LXX coordinates held.',
               url=contract['source_url'], provenance=_json(q))
    # No generic book/chapter envelope: it would falsely include disjoint gaps.
    return row


def load_bright_composite_rows(root=None):
    contract = authenticate_bright_composite_evidence(root)
    return [_row(r, contract) for r in contract['records']]


def qualify_bright_composite_row(row):
    """None only for unrelated rows; a copied/altered disclosure always fails."""
    related = (row.get('source_kind') == SOURCE_KIND
               or row.get('source_table') == 'bright_composite_qualified_source'
               or SOURCE_RELATIVE in str(row.get('source_file', ''))
               or CONTRACT_RELATIVE in str(row.get('provenance', '')))
    if not related:
        return None
    for expected in load_bright_composite_rows():
        if row == expected and all(type(v) is str for v in row.values()):
            return json.loads(expected['provenance'])
    raise ValueError('Unqualified Bright composite raw occurrence/context/scalar')


def bright_composite_identity_for(row):
    q = qualify_bright_composite_row(row)
    if q is None:
        raise ValueError('Not a qualified Bright composite')
    label = q['source_selection_ref']
    return dict(identity_key='rid_' + _sha(('scripture|' + CONVENTION + '|' + label).encode())[:20],
                reading_type='scripture', reading_name='', source_label=q['printed_ref'],
                display_ref=label + ' (Reader selection; canonical coordinates held)',
                canonical_mt_ref='', canonical_lxx_ref='', source_convention=CONVENTION,
                canonicalization_confidence='source_selection_only_canonical_hold',
                canonicalization_note=q['qualification_note'] + ' No exact cross-edition counterpart certified.',
                spans_json='[]')


def authenticate_bright_composite_identity(raw, identity):
    expected = bright_composite_identity_for(raw)
    if identity != expected or any(type(v) is not str for v in identity.values()):
        raise ValueError('Bright composite passage transport drift')
    return expected


def reconcile_bright_composite_rows(rows, source_rows):
    """Hold four legacy numeric projections; append exact source-only selections.

    Full legacy printed references and receipt files remain untouched. The hold
    is on generic coordinate activation, not on the authentic Reader selection.
    """
    qualified = load_bright_composite_rows()
    contract = authenticate_bright_composite_evidence()
    expected = {r['source_order']: r['legacy_source_row'] for r in contract['records']}
    for order, source in expected.items():
        if source_rows[int(order)-1] != source:
            raise ValueError('Bright source/service/slot/composite reference drift')
    result = []
    seen = set()
    for row in rows:
        match = next((r for r in contract['records']
                      if str(row['source_order']) == r['source_order']
                      and str(row['source_token_order']) == r['source_token_order']
                      and row['passage'] == r['legacy_ref']), None)
        if match:
            seen.add(match['handle'])
            row = dict(row, superseded_reason=HOLD, superseded_by_ref=match['source_selection_ref'])
        result.append(row)
    if seen != {r['handle'] for r in contract['records']}:
        raise ValueError('Bright exact four-case legacy projection incomplete')
    result.extend(qualified)
    return result
