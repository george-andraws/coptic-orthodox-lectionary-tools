"""LK5 inactive appointment projection and LK6 lossless public evidence transport.

Run the unchanged raw all-witness ledger FIRST. This module does not authorize
membership, activate a source, or replace any primary-source authentication.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import resolver_review_repairs as resolver

ROOT = Path(__file__).resolve().parent
WITNESSES = 'docs/reviews/luke-composites-1.3.8/published-1.3.7-composite-witnesses.json'
WITNESSES_SHA256 = '3b9b50fe425f4ec881180da6d927a5f93a0c5b793152b7d716028a4042067279'
SCHEMA = 'lectionary_provenance_v1'
EVIDENCE = 'provenance_evidence_json'
FORMAT = 'provenance_format'
OLD_KEY = '_review_original_row'
PUBLIC_KEY = 'original_source_row'


def _strict_json(value):
    def unique(pairs):
        result = {}
        for key, item in pairs:
            if key in result:
                raise ValueError('LK6 duplicate evidence member: ' + key)
            result[key] = item
        return result
    return json.loads(value, object_pairs_hook=unique)


def _key(row):
    return tuple(row.get(k, '') for k in ('source_family', 'source_kind', 'source_locator',
                 'identity_key', 'occasion', 'service_section', 'service_hour', 'slot'))


def _witness_groups():
    data = (ROOT / WITNESSES).read_bytes()
    if hashlib.sha256(data).hexdigest() != WITNESSES_SHA256:
        raise ValueError('LK5 published witness authentication failed')
    return json.loads(data)['groups']


def _check_witness(row, expected):
    # LK2 may normalize display prose, never raw keys, titles or locators.
    month, day = expected['coptic_date_key'].rsplit('-', 1)
    label = month.capitalize() + ' ' + day
    allowed = dict(expected)
    if row.get('display_label') == label:
        allowed['display_label'] = label
    if json.dumps(row, sort_keys=True) != json.dumps(allowed, sort_keys=True):
        raise ValueError('LK5 archived witness lifecycle/coordinates/disclosure drift')


def _is_archived_composite(row, groups):
    if row.get('composite_review') == 'LK5_archived_source_cell_v1':
        return True
    return any(row.get('source_locator') in {r['source_locator'] for r in group}
               and (row.get('composite_fragments_json') or ';' in row.get('display_ref', ''))
               for group in groups)


def _source_order(group):
    """Authenticate full source table and literal approved composite cell."""
    contract = resolver._runtime_contract()
    hydrated = []
    for row in group:
        raw = resolver._raw_for_runtime(row, contract)
        if raw is None or raw['raw_ref'] not in resolver.COMPOSITES:
            raise ValueError('LK5 archived witness missing raw source contract')
        projected = dict(row, **{k: raw[k] for k in ('source_table', 'source_file',
                         'raw_ref', 'calendar_key', 'gregorian_date')})
        projected.update(slot=raw['reading_slot'] or raw['reading_type'],
                         service_section=raw['service_section'])
        if not resolver._same_database_cell(projected, raw['raw_ref']):
            raise ValueError('LK5 archived witness differs from SQLite cell')
        hydrated.append((raw, row))
    first = hydrated[0][0]
    context = lambda raw: tuple(raw[k] for k in ('source_table', 'calendar_key', 'gregorian_date',
                            'service_section', 'reading_slot', 'raw_ref'))
    if any(context(raw) != context(first) for raw, _ in hydrated):
        raise ValueError('LK5 archived witnesses have different source contexts')
    expected = resolver.COMPOSITES[first['raw_ref']]
    by_ref = {row['display_ref']: row for _, row in hydrated}
    if len(by_ref) != len(hydrated) or set(by_ref) != set(expected):
        raise ValueError('LK5 incomplete or duplicate archived witness pair')
    return [by_ref[ref] for ref in expected]


def _merged(group):
    fragments = _source_order(group)
    joined = '; '.join(r['display_ref'] for r in fragments)
    result = dict(fragments[0], display_ref=joined, canonical_mt_ref=joined,
                  canonical_lxx_ref=joined,
                  identity_key='rid_' + hashlib.sha256(('scripture|' + joined + '|' + joined).encode()).hexdigest()[:20],
                  spans_json=json.dumps([s for r in fragments for s in json.loads(r['spans_json'])], sort_keys=True),
                  composite_fragments_json=json.dumps(fragments, sort_keys=True),
                  composite_review='LK5_archived_source_cell_v1')
    # Source locator/title/calendar keys and retirement fields remain literal.
    # Both complete disclosures survive, not just the first fragment's locator.
    disclosures = [d for r in fragments for d in json.loads(r['source_disclosure'])]
    result.update(source_disclosure=json.dumps(disclosures, separators=(',', ':')),
                  source_disclosure_count=str(len(disclosures)), collapsed_row_count=str(len(fragments)))
    result['calendar_review_source_locators'] = [r['source_locator'] for r in fragments]
    return result


def merge_remaining_composites(rows):
    """Project only the 52 pinned, inactive 1.3.7 pairs. Never activate history.

    Source transforms such as display-label normalization belong AFTER this
    projection. Raw source rows and the all-witness ledger remain unchanged.
    """
    groups = _witness_groups()
    index = {_key(row): i for i, group in enumerate(groups) for row in group}
    # Secondary identity recognizes a single-field mutation instead of allowing
    # a changed known witness to fall through as an unrelated row.
    locators = {row['source_locator'] for group in groups for row in group}
    contexts = {(row['occasion'], row['service_section'], row['slot'], row['identity_key'])
                for group in groups for row in group}
    found = defaultdict(list)
    for position, row in enumerate(rows):
        if _is_archived_composite(row, groups):
            qualify_archived_composite(row)
            continue
        match = index.get(_key(row))
        related = (row.get('source_locator') in locators or
            (row.get('source_family') == 'katameros_cycle' and
             (row.get('occasion'), row.get('service_section'), row.get('slot'), row.get('identity_key')) in contexts))
        if match is None:
            if related:
                raise ValueError('LK5 archived witness source/context drift')
            continue
        expected = next(r for r in groups[match] if _key(r) == _key(row))
        _check_witness(row, expected)
        found[match].append((position, row))
    replacements, removed, events = {}, set(), []
    for number, items in found.items():
        if len(items) != 2 or len({_key(r) for _, r in items}) != 2:
            raise ValueError('LK5 incomplete or duplicate archived witness pair')
        result = _merged([row for _, row in items])
        position = min(p for p, _ in items)
        replacements[position] = result
        removed.update(p for p, _ in items if p != position)
        events.append(dict(id='LK5', calendar_key=result['calendar_keys'],
                           service_section=result['service_section'], slot=result['slot'],
                           display_ref=result['display_ref'], active=False,
                           source_locators=[r['source_locator'] for _, r in items]))
    return [copy.deepcopy(replacements.get(i, row)) for i, row in enumerate(rows) if i not in removed], events


def qualify_archived_composite(row):
    """Authenticate the complete retained predecessor pair and exact projection."""
    row = restore_public_row(row)
    for group in _witness_groups():
        if row.get('source_locator') not in {r['source_locator'] for r in group}:
            continue
        try:
            fragments = _strict_json(row.get('composite_fragments_json') or '[]')
            if not isinstance(fragments, list) or len(fragments) != 2:
                raise ValueError('LK5 missing archived composite witnesses')
            originals = {_key(r): r for r in group}
            for fragment in fragments:
                if _key(fragment) not in originals:
                    raise ValueError('LK5 archived composite witness source drift')
                _check_witness(fragment, originals[_key(fragment)])
            expected = _merged(fragments)
            month, day = group[0]['coptic_date_key'].rsplit('-', 1)
            if row.get('display_label') == month.capitalize() + ' ' + day:
                expected['display_label'] = row['display_label']
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError('LK5 malformed archived composite evidence') from exc
        if row.get('source_locator') == expected['source_locator']:
            if json.dumps(row, sort_keys=True) != json.dumps(expected, sort_keys=True):
                raise ValueError('LK5 archived composite lifecycle/source/evidence drift')
            return copy.deepcopy(json.loads(expected['composite_fragments_json']))
    raise ValueError('LK5 unknown archived composite source')


def _source_name(row, legacy):
    if legacy.lstrip().startswith(('{', '[')):
        candidates = (row.get('source_title'), row.get('source_family'), row.get('source_kind'))
    else:
        candidates = (legacy.split(';', 1)[0], row.get('source_title'), row.get('source_family'))
    for candidate in candidates:
        if isinstance(candidate, str):
            value = ' '.join(candidate.split())
            if value and len(value) <= 300 and not any(c in value for c in '{}[]'):
                return value
    return 'Retained source evidence'


def compact_public_row(row):
    """Serialize full evidence separately; this operation is NOT authentication.

    original_source_row is the public spelling of the former internal temporary
    key. The reserved spelling is reversible, including nested JSON strings.
    """
    if FORMAT in row or EVIDENCE in row:
        restore_public_row(row)  # Reject malformed or inconsistent replay.
        return copy.deepcopy(row)
    result = copy.deepcopy(row)
    legacy = result.get('provenance', '')
    if not isinstance(legacy, str):
        raise ValueError('LK6 provenance must be a string')
    private = OLD_KEY in json.dumps(result, ensure_ascii=False)
    needs = (private or len(legacy) > 300 or legacy.lstrip().startswith(('{', '['))
             or 'R4 composite_fragments=' in legacy)
    if not needs:
        return result
    serialized = json.dumps(result, ensure_ascii=False)
    if PUBLIC_KEY in serialized:
        raise ValueError('LK6 reserved public evidence key collision')
    # Substitute only the reserved private-key spelling. No evidence is dropped,
    # and exact original JSON bytes are recovered on the internal validation lane.
    result = json.loads(serialized.replace(OLD_KEY, PUBLIC_KEY))
    result['provenance'] = _source_name(row, legacy)
    result[FORMAT] = SCHEMA
    marker = 'R4 composite_fragments='
    if marker in legacy:
        prefix, fragments = legacy.split(marker, 1)
        if fragments != row.get('composite_fragments_json'):
            raise ValueError('LK6 composite provenance/fragment evidence disagreement')
        envelope = {'schema': SCHEMA, 'composite_provenance_prefix': prefix + marker}
    else:
        envelope = {'schema': SCHEMA, 'legacy_provenance': legacy.replace(OLD_KEY, PUBLIC_KEY)}
    result[EVIDENCE] = json.dumps(envelope, ensure_ascii=False, sort_keys=True)
    return result


def restore_public_row(row):
    """Decode a public transport, then let existing consumers authenticate it.

    Never treat this as primary evidence validation. Callers must run their real
    source/disclosure/lifecycle/membership gates on the returned legacy view.
    """
    if FORMAT not in row and EVIDENCE not in row:
        return copy.deepcopy(row)
    if row.get(FORMAT) != SCHEMA or EVIDENCE not in row:
        raise ValueError('LK6 missing or unknown provenance evidence transport')
    try:
        envelope = _strict_json(row[EVIDENCE])
    except (TypeError, ValueError) as exc:
        raise ValueError('LK6 malformed provenance evidence JSON') from exc
    if (not isinstance(envelope, dict) or envelope.get('schema') != SCHEMA
            or set(envelope) not in ({'schema', 'legacy_provenance'}, {'schema', 'composite_provenance_prefix'})):
        raise ValueError('LK6 malformed provenance evidence schema')
    result = copy.deepcopy(row)
    del result[FORMAT]
    del result[EVIDENCE]
    if 'legacy_provenance' in envelope:
        legacy = envelope['legacy_provenance']
    else:
        prefix = envelope['composite_provenance_prefix']
        fragments = result.get('composite_fragments_json')
        if (type(prefix) is not str or not prefix.endswith('R4 composite_fragments=')
                or type(fragments) is not str):
            raise ValueError('LK6 missing composite provenance/fragment evidence')
        legacy = prefix + fragments
    if type(legacy) is not str:
        raise ValueError('LK6 malformed legacy provenance evidence scalar')
    legacy = legacy.replace(PUBLIC_KEY, OLD_KEY)
    if row.get('provenance') != _source_name(result, legacy):
        raise ValueError('LK6 public provenance label/evidence mismatch')
    result['provenance'] = legacy
    return json.loads(json.dumps(result, ensure_ascii=False).replace(PUBLIC_KEY, OLD_KEY))


def compact_public_rows(rows):
    return [compact_public_row(row) for row in rows]


def restore_public_rows(rows):
    return [restore_public_row(row) for row in rows]


def legacy_validation_rows(rows):
    """Restore authenticated LK5 witnesses for existing corpus/security gates.

    This is a validator view only. Never expose these split historical rows as
    current daily appointments or use them to derive a successor membership set.
    """
    result = []
    groups = _witness_groups()
    for row in restore_public_rows(rows):
        if _is_archived_composite(row, groups):
            result.extend(qualify_archived_composite(row))
        else:
            result.append(row)
    return result
