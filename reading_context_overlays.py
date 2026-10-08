"""Source-qualified annual repairs. No I/O in repair_table; no recurrence inferred.

Rows use explicit source slot and service labels. Parent adapters must supply the
selected context, never infer it from books or a generic annual-cycle collision.
The active table retains every preexisting raw_ref; superseded copies are returned
separately. This is an upstream API, not a generated-artifact editor.
"""
from __future__ import annotations

import base64
from copy import deepcopy
import hashlib
import json
from pathlib import Path

CONTEXT_KEYS = ('id', 'date', 'coptic_month', 'coptic_day', 'weekday',
                'occasion', 'variant', 'season')


def is_current_source_row(row: dict) -> bool:
    """Unmarked legacy rows are current; explicit removal never implies restoration.

    Empty CSV cells are unmarked, not False. Source history remains separately
    retained; this predicate only controls current materialization eligibility.
    """
    for key in ('active', 'include_in_current_index'):
        value = row.get(key)
        if value not in (None, '') and str(value).strip().lower() not in {'true', '1', 'yes'}:
            return False
    for key in ('state', 'status'):
        value = str(row.get(key) or '').strip().lower()
        if value and value not in {'current', 'active'}:
            return False
    value = str(row.get('current_status') or '').strip().lower()
    if value and value not in {'current', 'active', 'current_confirmed_coptic_reader',
            'current_confirmed_by_fixture_equivalence', 'current_public_or_local_reference',
            'current_working_source_not_coptic_reader_checked', 'pending_psalm_equivalence_unresolved', 'unknown'}:
        return False
    if str(row.get('removed_from_standard_lectionary', '')).strip().lower() in {'true', '1', 'yes'}:
        return False
    return not any(row.get(key) for key in ('superseded_reason', 'removal_reason',
                                           'removed_reason', 'removal_effective_version'))


def load_fixture(root: Path) -> dict:
    root = Path(root).resolve()
    fixture = {'root': root, 'fingerprints': json.loads((root / 'fingerprints.json').read_text()),
               'oracle': json.loads((root / 'oracle.json').read_text()),
               'repairs': json.loads((root / 'repairs.json').read_text())}
    authenticate_fixture(fixture)
    return fixture


def authenticate_fixture(fixture: dict) -> None:
    """Authenticate captured bytes, literal headings, selected context and order.

    Fingerprints are a local integrity trust root, not a publisher signature.
    Original independent audit/readiness qualifications are retained verbatim.
    """
    root = Path(fixture['root']).resolve()
    for relative, expected in fixture['fingerprints'].items():
        path = (root / relative).resolve()
        if Path(relative).is_absolute() or not path.is_relative_to(root):
            raise ValueError('Evidence path escapes fixture')
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Source fingerprint drift: {relative}')
    for key, file in [('oracle', 'oracle.json'), ('repairs', 'repairs.json')]:
        if fixture[key] != json.loads((root / file).read_text()):
            raise ValueError(f'In-memory {key} drift')
    seen = set()
    for capture in fixture['oracle']:
        if capture['id'] in seen:
            raise ValueError('Duplicate captured context')
        seen.add(capture['id'])
        if not capture['table_bytes_hash_verified'] or capture['review_status'] != 'qualified_captured_Readings_whole_context':
            raise ValueError('Unqualified source context')
        if len(capture['context_evidence']) != 4:
            raise ValueError('Missing selected context evidence')
        for relative in capture['context_evidence']:
            if relative not in fixture['fingerprints']:
                raise ValueError('Unbound selected context')
            if Path(relative).name == 'home-selected.txt':
                if (root / relative).read_text().strip() != capture['homeContext'].strip():
                    raise ValueError('Selected home context disagrees')
        ordered = []
        for doc in capture['documents']:
            data = (root / doc['textPath']).read_bytes()
            if fixture['fingerprints'].get(doc['textPath']) != doc['textSha256']:
                raise ValueError('Unbound source document')
            references = []
            last_offset = -1
            for order, heading in enumerate(doc['sourceReferenceHeadings'], 1):
                offset, length = heading['byte_offset'], heading['byte_length']
                raw = data[offset:offset + length]
                if (offset <= last_offset or heading['ordinal'] != order or
                        raw != heading['raw_line'].encode('utf-8') or
                        raw != base64.b64decode(heading['raw_line_utf8_base64']) or
                        raw.decode('utf-8').strip() != heading['printed_reference']):
                    raise ValueError('Source heading bytes/order disagree')
                last_offset = offset
                references.append(heading['printed_reference'])
            if references != doc['printedReferences']:
                raise ValueError('Printed reference ordering disagrees')
            ordered.append({'slot': doc['label'], 'refs': references})
        if ordered != capture['orderedPrintedReferences']:
            raise ValueError('Whole source table order disagrees')
    for rule in fixture['repairs']:
        capture = next(c for c in fixture['oracle'] if c['id'] == rule['id'])
        matches = [r for r in capture['source_approved_nonPsalm'] if r['slot'] == rule['slot']]
        if len(matches) != 1 or matches[0]['source_ref'] != rule['printed_ref']:
            raise ValueError('Repair is not qualified by the independent source oracle')


HARDENING_PATH = Path(__file__).resolve().parent / 'tests/fixtures/annual_existing_rule_hardening_v1/overlay.json'
HARDENING_SHA256 = '91fe5fc1c72322c1af95faf2a660d6bbfeff0e7b24bb0db2d4ecd5b2d44d157b'


def load_hardening(fixture: dict) -> dict:
    """Separate preconditions; original independently reviewed bytes stay untouched."""
    data = HARDENING_PATH.read_bytes()
    if hashlib.sha256(data).hexdigest() != HARDENING_SHA256:
        raise ValueError('Annual hardening precondition drift')
    hardening = json.loads(data)
    for name, expected in hardening['original_fixture_hashes'].items():
        if hashlib.sha256((fixture['root'] / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Original annual source/legacy-input fingerprint drift')
    authenticate_fixture(fixture)
    return hardening


def authenticate_table_input(capture: dict, rows: list[dict], fixture: dict,
                             source_kind: str, rules: list[dict]) -> None:
    hardening = load_hardening(fixture)
    bound = next(c for c in hardening['contexts'] if c['id'] == capture['id'])
    if bound['context'] != capture['context'] or bound['table_sha256'] != capture['tableTextSha256']:
        raise ValueError('Annual hardening source context drift')
    baseline = bound['date_source_rows' if source_kind == 'date_source' else 'cycle_rows']
    rulemap = {r['slot']: r for r in rules}
    def slot(row):
        if source_kind == 'cycle':
            return row.get('reading_slot') or row.get('slot')
        service, kind = row.get('service_section'), row.get('reading_type')
        labels = {'Psalm': 'psalm', 'Gospel': 'gospel', 'Pauline Epistle': 'pauline',
                  'Catholic Epistle': 'catholic', 'Acts of the Apostles': 'acts'}
        inferred = str(service).lower() + '_' + labels.get(kind, 'unknown')
        declared = row.get('slot')
        if declared not in (None, inferred, 'uncompared_psalm') or (declared == 'uncompared_psalm' and kind != 'Psalm'):
            raise ValueError('Whole-table slot/service/type drift')
        return inferred
    # Legacy APIs accept a complete six-slot compared projection or an exact
    # Annual16 vector. Neither is an arbitrary short version of a whole table.
    scope_bytes = (HARDENING_PATH.parent / 'input-scopes-recovery.json').read_bytes()
    if hashlib.sha256(scope_bytes).hexdigest() != 'be9bfd87d5d82b252f543aa93e19b4d0f3c44adb992a11a547a7c354b0ceb27a':
        raise ValueError('Annual input scope fingerprint drift')
    scopes = json.loads(scope_bytes)
    vector = False
    if source_kind == 'date_source' and rows and all(
            r.get('slot') in scopes['date_compared_slots'] for r in rows):
        baseline = [r for r in baseline if slot(r) in scopes['date_compared_slots']]
        if [slot(r) for r in baseline] != scopes['date_compared_slots']:
            raise ValueError('Unbound compared input scope')
    elif source_kind == 'cycle' and len(rows) == 1 and capture['id'] == scopes['cycle_vector_context_id']:
        required = set(scopes['cycle_vector_required_fields'])
        allowed = required | set(scopes['cycle_vector_optional_fields'])
        if required <= set(rows[0]) <= allowed:
            baseline = scopes['cycle_vector_rows']
            vector = True
    expected = [slot(r) for r in baseline]
    actual = [slot(r) for r in rows]
    allowed_missing = {s for s, r in rulemap.items() if r['allow_supplement']}
    if actual != [s for s in expected if s in actual] or set(expected) - set(actual) - allowed_missing:
        raise ValueError('Whole-table missing/duplicate/reordered/unknown slot')
    byslot = {slot(r): r for r in baseline}
    for row in rows:
        s = slot(row)
        if s not in byslot:
            raise ValueError('Unknown whole-table input slot')
        base = byslot[s]
        fields = ('source', 'gregorian_date', 'weekday', 'day_title', 'service_section', 'reading_type', 'url') if source_kind == 'date_source' else (
            'source', 'source_table', 'source_type', 'cycle', 'day_key', 'month_number', 'month_name', 'day',
            'week', 'day_of_week', 'day_name', 'season', 'other', 'reading_slot')
        if vector:
            fields = ('slot', 'service_section')
        rule = rulemap.get(s)
        if row.get('source') == 'Coptic Reader context-qualified supplement':
            if rule is None or not rule['allow_supplement']:
                raise ValueError('Unauthorized annual supplement')
            doc = next(d for d in capture['documents'] if rule['printed_ref'] in d['printedReferences'])
            expected_provenance = {
                'source_context': capture['context'], 'source_evidence': doc['textPath'],
                'source_sha256': doc['textSha256'], 'source_printed_ref': rule['printed_ref'],
                'source_order': [r['slot'] for r in capture['source_approved_nonPsalm']].index(s) + 1,
                'source_kind': 'coptic_reader_context_supplement',
            }
            if any(row.get(k) != v for k, v in expected_provenance.items()):
                raise ValueError('Annual supplement provenance drift')
        for key in fields:
            if (key in {'source', 'url'} and source_kind == 'date_source' and rule
                    and rule['allow_supplement'] and row.get('source') == 'Coptic Reader context-qualified supplement'
                    and row.get('url') == 'https://copticreader.org/app/#/document'
                    and row.get('raw_ref') == rule['printed_ref']
                    and row.get('source_context') == capture['context']):
                continue
            if str(row.get(key, '')) != str(base.get(key, '')):
                raise ValueError('Whole-table input context/source drift: ' + key)
        raw, normalized = row.get('raw_ref'), row.get('normalized_ref')
        if rule is None:
            if (raw, normalized) != (base['raw_ref'], base['normalized_ref']):
                raise ValueError('Whole-table nonrepair reference drift')
        elif not ((raw, normalized) == (base['raw_ref'], base['normalized_ref']) or
                  raw in {base['raw_ref'], rule['printed_ref']} and normalized == rule['normalized_ref']):
            raise ValueError('Whole-table repair reference drift')
        allowed_numeric = {None, '', base['raw_ref']}
        if rule is not None:
            allowed_numeric.add('60.1:25-2:10')
        if source_kind == 'cycle' and row.get('numeric_ref') not in allowed_numeric:
            raise ValueError('Whole-table cycle numeric drift')


def apply_annual_dated_hardening(rows: list[dict], fixture: dict) -> dict:
    """Materialize only the existing eight exact dated repairs, with history.

    The entire nine-slot table is authenticated before any changed slot is
    emitted. Storage ordering is not source ordering: the explicit service/type
    adapter supplies the trusted whole-table order without changing output order.
    """
    import datetime as dt
    from calendar_resolution import numeric_coptic_date

    active = deepcopy(rows)
    result = {'active': active, 'history': [], 'events': []}
    repair_ids = {rule['id'] for rule in fixture['repairs']}
    dates = {capture['date'] for capture in fixture['oracle'] if capture['id'] in repair_ids}
    slots = [('Vespers', 'Psalm'), ('Vespers', 'Gospel'),
             ('Matins', 'Psalm'), ('Matins', 'Gospel'),
             ('Liturgy', 'Pauline Epistle'), ('Liturgy', 'Catholic Epistle'),
             ('Liturgy', 'Acts of the Apostles'), ('Liturgy', 'Psalm'), ('Liturgy', 'Gospel')]
    names = ['vespers_psalm', 'vespers_gospel', 'matins_psalm', 'matins_gospel',
             'liturgy_pauline', 'liturgy_catholic', 'liturgy_acts', 'liturgy_psalm', 'liturgy_gospel']
    for date in sorted(dates & {row.get('gregorian_date') for row in active}):
        capture = next(c for c in fixture['oracle'] if c['date'] == date)
        context = capture['context']
        date_value = dt.date.fromisoformat(date)
        _, month, day = numeric_coptic_date(date_value)
        if (month, day, date_value.strftime('%A')) != (context['coptic_month'], context['coptic_day'], context['weekday']):
            raise ValueError('Selected annual date/calendar context disagrees')
        selected = [(i, row) for i, row in enumerate(active) if row.get('gregorian_date') == date]
        ordered = []
        positions = []
        for pair, name in zip(slots, names):
            found = [(i, row) for i, row in selected if (row.get('service_section'), row.get('reading_type')) == pair]
            if len(found) != 1:
                raise ValueError('Complete annual service/slot join required')
            i, row = found[0]
            positions.append(i)
            ordered.append(dict(row, slot=name))
        if len(selected) != len(ordered):
            raise ValueError('Unknown or duplicate annual table slot')
        repaired = repair_table(context, ordered, fixture, 'date_source')
        if len(repaired['active']) != len(positions):
            raise ValueError('Unexpected annual supplement on complete dated table')
        for i, new in zip(positions, repaired['active']):
            if 'slot' not in active[i]:
                new.pop('slot', None)
            if new.get('source_evidence'):
                relative = 'sources/coptic-reader/annual-reconciled-2026-10-07/' + new['source_evidence']
                new['correction_source'] = relative
                new['parse_status'] = 'source_context_correction'
                new['normalization_warning'] = ('verified exact annual context; evidence=' + relative
                    + '; verified_date=' + date + '; source_sha256=' + new['source_sha256'])
            active[i] = new
        result['history'].extend(repaired['history'])
        result['events'].extend(repaired['events'])
    return result


def apply_annual_cycle_hardening(rows: list[dict], fixture: dict) -> list[dict]:
    """Existing Annual16 cycle rule only; never project new dated recurrence."""
    selected = [r for r in rows if r.get('source_table') == 'AnnualReadings'
                and r.get('day_key') == 'Tut 16' and is_current_source_row(r)]
    if not selected:
        return deepcopy(rows)
    capture = next(c for c in fixture['oracle'] if c['id'] == 'AnnualReadings-16')
    adapted = [dict(r, slot=r.get('reading_slot'),
                    service_section=r.get('reading_slot', '').split('_')[0].title()) for r in selected]
    repaired = repair_table(capture['context'], adapted, fixture, 'cycle')
    iterator = iter(repaired['active'])
    out = []
    for row in rows:
        if row in selected:
            new = next(iterator)
            for key in ('slot', 'service_section'):
                if key not in row:
                    new.pop(key, None)
            out.append(new)
        else:
            out.append(deepcopy(row))
    # Idempotent current input already retains its historical counterpart.
    for row in repaired['history']:
        row.pop('slot', None)
        row.pop('service_section', None)
        out.append(row)
    return out


def repair_table(context: dict, rows: list[dict], fixture: dict,
                 source_kind: str) -> dict:
    """Return active/history/events without modifying arguments.

    source_kind: date_source or cycle. Applicability is exact captured date plus
    fixed Coptic day, weekday, selected season, occasion and variant. No future
    projection or primary-calendar selection is performed here.
    """
    active = deepcopy(rows)
    result = {'active': active, 'history': [], 'events': []}
    capture = next((c for c in fixture['oracle'] if all(
        context.get(k) == c['context'][k] for k in CONTEXT_KEYS)), None)
    if source_kind not in {'date_source', 'cycle'}:
        raise ValueError('Unknown explicitly requested annual source kind')
    if capture is None:
        return result
    rules = [deepcopy(r) for r in fixture['repairs'] if r['id'] == capture['id']]
    if any(not is_current_source_row(row) for row in active):
        raise ValueError('Inactive source input requires separate, explicit restoration policy')
    if source_kind == 'cycle':
        rules = [r for r in rules if r['id'] == 'AnnualReadings-16']
        for rule in rules:
            rule['raw_ref'] = '60.2:1-10'
            rule['allow_supplement'] = False
    if not rules:
        return result
    authenticate_table_input(capture, active, fixture, source_kind, rules)
    expected_order = [r['slot'] for r in capture['source_approved_nonPsalm']]
    if source_kind == 'date_source':
        if any(row.get('gregorian_date') != context['date'] or
               row.get('source') not in {'copticchurch.net daily scrape',
                                        'Coptic Reader context-qualified supplement'}
               for row in active):
            raise ValueError('Whole-table date/source policy disagrees')
        slots = [r['slot'] for r in active if r.get('slot') in expected_order]
        if slots != [slot for slot in expected_order if slot in slots]:
            raise ValueError('Duplicate or reordered source slots')
    for rule in rules:
        candidates = [r for r in active if r.get('slot') == rule['slot']]
        if len(candidates) > 1:
            raise ValueError('Duplicate repair slot')
        evidence_doc = next(d for d in capture['documents'] if rule['printed_ref'] in d['printedReferences'])
        provenance = {'source_context': deepcopy(context),
                      'source_evidence': evidence_doc['textPath'],
                      'source_sha256': evidence_doc['textSha256'],
                      'source_printed_ref': rule['printed_ref'],
                      'source_order': expected_order.index(rule['slot']) + 1}
        action = 'correction'
        if not candidates:
            if not rule['allow_supplement']:
                raise ValueError('Unproved missing slot; no blanket supplement')
            # Both adjacent explicit service slots must be present to locate it.
            position = expected_order.index(rule['slot'])
            before, after = expected_order[position - 1:position + 2:2]
            anchors = {slot: [i for i, r in enumerate(active) if r.get('slot') == slot]
                       for slot in [before, after]}
            if any(len(indices) != 1 for indices in anchors.values()):
                raise ValueError('Missing/duplicate supplement order anchors')
            insertion = anchors[after][0]
            if anchors[before][0] >= insertion:
                raise ValueError('Reversed supplement anchors')
            anchor = active[anchors[before][0]]
            row = {**{key: deepcopy(anchor[key]) for key in
                      ('gregorian_date', 'weekday', 'day_title', 'source_occasion')
                      if key in anchor},
                   'slot': rule['slot'], 'service_section': rule['service'],
                   'reading_type': 'Catholic Epistle',
                   'source': 'Coptic Reader context-qualified supplement',
                   'url': 'https://copticreader.org/app/#/document',
                   'parse_status': 'source_supplement', 'normalization_warning': '',
                   'raw_ref': rule['printed_ref'], 'normalized_ref': rule['normalized_ref'],
                   **provenance, 'source_kind': 'coptic_reader_context_supplement'}
            active.insert(insertion, row)
            action = 'supplement'
        else:
            row = candidates[0]
            if row.get('service_section') != rule['service']:
                raise ValueError('Wrong service for qualified repair')
            if source_kind == 'date_source':
                expected_type = 'Catholic Epistle' if rule['slot']=='liturgy_catholic' else 'Gospel'
                if (row.get('gregorian_date') != context['date'] or
                        row.get('reading_type') != expected_type or
                        row.get('source') not in {'copticchurch.net daily scrape',
                                                 'Coptic Reader context-qualified supplement'}):
                    raise ValueError('Wrong date/type/source policy for qualified repair')
            if row.get('normalized_ref') == rule['normalized_ref']:
                if row.get('raw_ref') not in {rule['raw_ref'], rule['printed_ref']}:
                    raise ValueError('Unrecognized raw reference on repaired slot')
                if source_kind == 'cycle':
                    row['numeric_ref'] = '60.1:25-2:10'
                continue
            if row.get('raw_ref') != rule['raw_ref']:
                raise ValueError('Raw source drift; correction quarantined')
            result['history'].append({**deepcopy(row),
                                      'active': False, 'state': 'superseded',
                                      'status': 'removed', 'include_in_current_index': False,
                                      'superseded_by_ref': rule['normalized_ref'],
                                      'superseded_reason': 'source_context_confirmed', **provenance})
            row.update(normalized_ref=rule['normalized_ref'], **provenance)
            if source_kind == 'cycle':
                row['numeric_ref'] = '60.1:25-2:10'
        result['events'].append({'id': capture['id'], 'date': capture['date'],
                                 'slot': rule['slot'], 'action': action,
                                 'raw_ref': row['raw_ref'],
                                 'normalized_ref': rule['normalized_ref'], **provenance})
    return result
