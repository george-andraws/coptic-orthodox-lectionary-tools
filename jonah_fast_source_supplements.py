"""Narrow user-authorized Jonah Fast repair; no I/O except source reads.

Call apply_jonah_fast_supplements(date, day_title, rows) after existing ordinary
source corrections/supplements, BEFORE generic candidate Matins opt-in. Returns
current rows followed by explicit inactive history. Never enables held candidates.

Canonical Jonah coordinates are verified *covering parallel loci*, not a claim
that Reader English/Arabic is verbatim NKJV or Brenton. In particular Tuesday
contains edition variants and combined/redistributed units. Printed references,
full bilingual body envelopes and old source-only approval flags remain separate.
The original independent reviews did NOT approve this new activation contract.
"""
from __future__ import annotations

from copy import deepcopy
import datetime as dt
import hashlib
import json
from pathlib import Path

from calendar_resolution import julian_pascha_gregorian
from reading_context_overlays import is_current_source_row

ROOT = Path(__file__).resolve().parent
SOURCE_RELATIVE = Path('sources/coptic-reader/jonah-qualified-2026-10-25')
SOURCE_ROOT = ROOT / SOURCE_RELATIVE
CONTRACT_SHA256 = 'e0175a66f98ab0c8dc3c5bda2917e82e5a490fe97cf00c59b732af7475225726'
APPROVAL_SHA256 = '7ed7fcf10eae622af4633add3c55f0b497426f13757c7e17256c4aed08cc493e'
APPROVAL_PATH = ROOT / 'sources/user-corrections/jonah-fast-2026-10-25.json'
SOURCE = 'Coptic Reader source-qualified Jonah Fast supplement'
FAMILY = 'jonah_fast_source_qualified'
KIND = 'jonah_fast_date_supplement'
ALIASES = {-69: 'Fast of Nineveh', -68: "Tuesday of Ninevah's Fast", -67: "Wednesday of Ninevah's Fast"}
COLLISIONS = {'2022-02-15', '2033-02-15'}
CORE = ('source', 'gregorian_date', 'weekday', 'day_title', 'service_section',
        'reading_type', 'raw_ref', 'normalized_ref', 'parse_status',
        'normalization_warning', 'url')


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def load_jonah_contract(root=None):
    """Authenticate every portable witness on each call; no mutable cache trust."""
    root = Path(SOURCE_ROOT if root is None else root).resolve()
    try:
        data = (root / 'source-contract.json').read_bytes()
        if _sha(data) != CONTRACT_SHA256:
            raise ValueError('Jonah source contract drift')
        contract = json.loads(data)
        if (_sha(APPROVAL_PATH.read_bytes()) != APPROVAL_SHA256
                or contract['approval_sha256'] != APPROVAL_SHA256):
            raise ValueError('Jonah new user authorization drift')
        for relative, expected in contract['fingerprints'].items():
            path = root / relative
            if (Path(relative).is_absolute() or '..' in Path(relative).parts
                    or path.is_symlink() or not path.resolve().is_relative_to(root)
                    or _sha(path.read_bytes()) != expected):
                raise ValueError('Jonah portable evidence drift: ' + relative)
        if contract['old_receipts_grant_activation'] is not False:
            raise ValueError('Jonah old receipts are source-only')
        for day in contract['days']:
            date = dt.date.fromisoformat(day['date'])
            if ((date - julian_pascha_gregorian(date.year)).days != day['offset']
                    or date.weekday() != day['offset'] + 69
                    or day['day_title'] != ALIASES[day['offset']]
                    or len(day['appointments']) != 8):
                raise ValueError('Jonah source date/context drift')
            for order, appointment in enumerate(day['appointments'], 1):
                raw = (root / appointment['evidence']).read_bytes()
                lines = raw.decode().splitlines()
                literal = appointment['body_envelope_literal']
                if (appointment['order'] != order or _sha(raw) != appointment['document_sha256']
                        or lines[appointment['heading_line']-1] != '\t' + appointment['printed_ref']
                        or _sha(literal.encode()) != appointment['body_envelope_sha256']
                        or literal not in '\n'.join(lines)):
                    raise ValueError('Jonah heading/body/order drift')
        return contract
    except (OSError, KeyError, TypeError, IndexError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('Jonah source contract missing or malformed') from exc


def _contexts(root):
    return json.loads((Path(root) / 'input-contexts.json').read_text())


def _history(row):
    return {**deepcopy(row), 'active': False, 'include_in_current_index': False,
            'state': 'superseded', 'status': 'removed', 'current_status': 'historical_witness',
            'superseded_reason': 'jonah_fast_source_qualified_repair',
            'jonah_contract_sha256': CONTRACT_SHA256}


def _metadata(appointment, day):
    evidence = str(SOURCE_RELATIVE / appointment['evidence'])
    return {'printed_ref': appointment['printed_ref'], 'source_order': appointment['order'],
            'source_edition': 'Coptic Reader retained rendered bilingual source',
            'source_verified_date': day['date'], 'source_captured_at': next(
                x['retrieved_at'] for x in day['documents'] if x['file'] == appointment['evidence']),
            'source_selected_context': day['selected_context'],
            'source_heading_line': appointment['heading_line'],
            'jonah_source_body_sha256': appointment['body_envelope_sha256'],
            'jonah_source_body_literal': appointment['body_envelope_literal'],
            'source_full_document_sha256': appointment['document_sha256'],
            'source_evidence': evidence, 'correction_source': evidence,
            'source_family': FAMILY, 'source_kind': KIND,
            'jonah_contract_sha256': CONTRACT_SHA256,
            'runtime_activation_approved': True,
            'canonicalization_confidence': 'bounded_parallel_locus_not_exact_edition_equivalence',
            'canonicalization_note': appointment['coordinate_note']}


def _project(date, day_title, rows, contract, context):
    """Input identities must match the frozen parser lane, even for partial dates."""
    allowed = context['rows']
    seen = set()
    for row in rows:
        signature = _json({k: row.get(k) for k in CORE})
        if signature in seen:
            raise ValueError('Jonah duplicate upstream appointment')
        seen.add(signature)
        matches = [expected for expected in allowed if all(row.get(k) == expected.get(k) for k in CORE)]
        if (len(matches) != 1 or (
                    not is_current_source_row(row) and not (
                        row['service_section'] == 'Vespers'
                        and row == matches[0]
                        and row.get('superseded_reason') == 'coptic_reader_no_service'))
                or row.get('removed_marker') or row.get('candidate_only')
                or row.get('source_family') not in (None, '', 'ordinary_date_resolved')
                or row.get('source_kind') not in (None, '', 'copticchurch_date')
                or any(row.get(k) not in (None, '') for k in ('source_slot', 'source_order'))):
            raise ValueError('Jonah unqualified upstream source/context/state/slot')
        # No arbitrary payload/lifecycle metadata may be inherited by new rows.
        if (set(row) - set(matches[0]) - {'source_family', 'source_kind'}
                or any(row.get(k) != value for k, value in matches[0].items())):
            raise ValueError('Jonah unexpected upstream fields or frozen provenance/lifecycle drift')
    offset = context['offset']
    day = next(d for d in contract['days'] if d['offset'] == offset)
    historical = []
    for row in rows:
        psalm_repair = (date.isoformat() not in COLLISIONS and any(
            a['canonical_repair_required'] and a['service_section'] == row['service_section']
            and a['reading_type'] == row['reading_type'] for a in day['appointments']))
        if offset == -69 or row['service_section'] == 'Vespers' or psalm_repair:
            historical.append(_history(row) if is_current_source_row(row) else deepcopy(row))
    if date.isoformat() in COLLISIONS:
        # Only this seasonal child is authorized in the separately witnessed feast.
        appointments = day['appointments'][:1]
    else:
        appointments = day['appointments']
    result = []
    for appointment in appointments:
        kind, service = appointment['reading_type'], appointment['service_section']
        original = next((r for r in rows if r['reading_type'] == kind and r['service_section'] == service), None)
        baseline = next((r for r in allowed if r['reading_type'] == kind and r['service_section'] == service), None)
        if kind != 'Prophecy' and offset != -69:
            base = original if original is not None else baseline
            if base is None:
                raise ValueError('Jonah missing nonprophecy source identity')
            row = deepcopy(base)
            if appointment['canonical_repair_required']:
                row.update(normalized_ref=appointment['normalized_ref'],
                           parse_status='jonah_fast_source_supplement',
                           normalization_warning=appointment['coordinate_note'])
        else:
            row = {'source': SOURCE, 'gregorian_date': date.isoformat(), 'weekday': date.strftime('%A'),
                   'day_title': day_title, 'service_section': service, 'reading_type': kind,
                   'raw_ref': appointment['printed_ref'], 'normalized_ref': appointment['normalized_ref'],
                   'parse_status': 'jonah_fast_source_supplement',
                   'normalization_warning': appointment['coordinate_note'], 'url': 'https://copticreader.org/app/'}
        row.update(_metadata(appointment, day))
        if kind == 'Prophecy':
            row.update(source_slot='OT1', source_order=1, slot_type='prophecy',
                       source_convention='coptic_reader_jonah_covering_modern_locus',
                       jonah_input_rows_json=_json(rows))
            if date.isoformat() in COLLISIONS:
                witnesses = json.loads((Path(SOURCE_ROOT) / 'collision-witnesses.json').read_text())
                row['jonah_collision_witness_json'] = _json([
                    w for w in witnesses if w['date'] == date.isoformat()])
        result.append(row)
    if date.isoformat() in COLLISIONS:
        # Keep exact feast companion bytes and their order; no synthetic Jonah companions.
        result.extend(deepcopy([r for r in rows if r['service_section'] != 'Vespers']))
    return result + historical


def apply_jonah_fast_supplements(date, day_title, rows):
    """Repair only authenticated 2020..2035 offsets/aliases; all other contexts no-op.

    Wrong title/date is outside policy, not a fuzzy match. Within policy, malformed,
    inactive, overlapping or forged inputs raise. Partial input is supported only
    for known source identities. Replayed outputs are exact typed JSON-verified.
    Returned history must be retained but excluded from default current indexes.
    """
    if not isinstance(date, dt.date) or isinstance(date, dt.datetime):
        raise ValueError('Jonah date requires a civil date')
    marked = [r for r in rows if any(k in r for k in ('jonah_contract_sha256', 'jonah_input_rows_json'))
              or r.get('source') == SOURCE or r.get('parse_status') == 'jonah_fast_source_supplement']
    offset = (date - julian_pascha_gregorian(date.year)).days
    collision = date.isoformat() in COLLISIONS and day_title == 'Entrance into the Temple'
    outside = (not 2020 <= date.year <= 2035 or offset not in ALIASES
               or date.weekday() != offset + 69
               or not (day_title == ALIASES[offset] or collision)
               or date.isoformat() in COLLISIONS and not collision)
    if outside:
        if marked:
            raise ValueError('Jonah repaired payload replayed under wrong outer context')
        return rows
    contract = load_jonah_contract()
    context = next(c for c in _contexts(SOURCE_ROOT) if c['date'] == date.isoformat())
    if context['day_title'] != day_title:
        raise ValueError('Jonah frozen context disagrees')
    if marked:
        prophecy = [r for r in rows if r.get('reading_type') == 'Prophecy' and 'jonah_input_rows_json' in r]
        if len(prophecy) != 1:
            raise ValueError('Jonah replay missing unique source prophecy')
        try:
            original = json.loads(prophecy[0]['jonah_input_rows_json'])
            expected = _project(date, day_title, original, contract, context)
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError('Jonah replay input drift') from exc
        if _json(rows) != _json(expected):
            raise ValueError('Jonah replay evidence/context/state/body drift')
        return deepcopy(rows)
    return _project(date, day_title, rows, contract, context)


def source_transport(row):
    """Small lossless qualification envelope; body bytes stay in frozen evidence."""
    result = {k: v for k, v in row.items() if k not in {
        'jonah_source_body_literal', 'jonah_input_rows_json'} and v not in ('', None)}
    # The source builder's union-schema CSV adds empty unrelated columns and
    # stringifies typed ordinals/approval. Canonicalize only these declared types;
    # do not accept booleans as ordinals or truthy strings as authorization.
    for key in ('source_order', 'source_heading_line'):
        value = result.get(key)
        if type(value) is str and value.isascii() and value.isdecimal() and str(int(value)) == value:
            value = int(value)
        if type(value) is not int or value < 1:
            raise ValueError('Jonah source ordinal type/value drift')
        result[key] = value
    value = result.get('runtime_activation_approved')
    if type(value) is str and value in ('True', 'False'):
        value = value == 'True'
    if type(value) is not bool:
        raise ValueError('Jonah source authorization type drift')
    result['runtime_activation_approved'] = value
    return result


def expected_source(selector):
    contract = load_jonah_contract()  # Reauthenticate captures, never trust CSV hashes.
    context = next((c for c in _contexts(SOURCE_ROOT)
                    if c['date'] == selector.get('gregorian_date')), None)
    if context is None:
        raise ValueError('Jonah selected date outside authenticated contract')
    expected = _project(dt.date.fromisoformat(context['date']), context['day_title'],
                        context['rows'], contract, context)
    matches = [r for r in expected if is_current_source_row(r)
               and r.get('source_kind') == KIND
               and r['service_section'] == selector.get('service_section')
               and r['reading_type'] == selector.get('reading_type')]
    if len(matches) != 1 or source_transport(matches[0]) != selector:
        raise ValueError('Jonah source metadata/context/lifecycle drift')
    return matches[0]


def transport_for(row):
    try:
        value = json.loads(row.get('provenance') or '{}')
        return value.get('consumer_source_transport', value)
    except (TypeError, ValueError, AttributeError):
        return {}


def is_jonah_projection(row):
    return (row.get('source_kind') == KIND or row.get('source_family') == FAMILY
            or 'jonah_source' in transport_for(row)
            or str(SOURCE_RELATIVE) in str(row.get('source_file', '')))


def qualify_projected_row(row):
    """Compare the actual selected crosswalk row, not merely its embedded witness."""
    import build_lectionary_reference as reference
    import build_lectionary_crosswalk as crosswalk
    transport = transport_for(row)
    source = expected_source(transport.get('jonah_source', {}))
    indexed = reference.build_date_passage_index([source])
    expected = crosswalk.project_date_rows(indexed)
    # CSV preserves strings, while in-memory builders retain integer ordinals.
    def normalized(value):
        return {k: str(v) for k, v in value.items() if v not in ('', None)}
    if not any(normalized(row) == normalized(item) for item in expected):
        raise ValueError('Jonah projected date/source/kind/family/service/slot/token drift')
    return source
