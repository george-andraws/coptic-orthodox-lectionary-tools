"""Authenticated, exact-dated Matins candidate projection; never a recurrence rule.

The hash pins bind independently accepted source evidence, NOT runtime approval.
Raw original corpus records (including producer flags and original locators) stay
unchanged. Portable path-map resolves their evidence without rewriting history.
"""
from __future__ import annotations

import base64
from copy import deepcopy
import datetime as dt
import hashlib
import json
from pathlib import Path
import re

from calendar_resolution import julian_pascha_gregorian
from passage_normalization import parse_passage, passage_matches
from reading_context_overlays import is_current_source_row

FIXTURE_ROOT = Path(__file__).resolve().parent / 'sources/coptic-reader/matins-source-accepted-2026-10-07'
CORPUS_SHA256 = '5f7558115e4743e08febe5e5ecd7f350573c3b80af1d517951db6cc0db9526d2'
FINGERPRINTS_SHA256 = 'b660243a6c145c3890b5ead2dd71681f95594fc8b4bb03ec30d0886979641589'
CONTEXT_KEYS = ('civil_date', 'occasion_key', 'actual_occasion', 'actual_home_line',
                'numeric_coptic_calendar_crosscheck', 'pascha_offset_days', 'weekday', 'service')
CANDIDATE_SOURCE = 'Coptic Reader authenticated exact-dated Matins candidate'


def is_dated_matins_candidate(row):
    """Redundant preserved markers prevent source-label forgery from evading holds."""
    context = row.get('source_context')
    retained_history = (row.get('superseded_reason') == 'exact_dated_Matins_source_candidate' and
                        row.get('active') is False and row.get('include_in_current_index') is False and
                        row.get('state') == 'superseded' and row.get('status') == 'removed')
    return (row.get('source') == CANDIDATE_SOURCE or
            row.get('parse_status') == 'candidate_matins_source_coordinate_hold' or
            isinstance(context, dict) and context.get('accepted_corpus_sha256') == CORPUS_SHA256 and not retained_history or
            any(key in row for key in ('candidate_only', 'source_document_body',
                'source_document_sha256', 'source_captured_context', 'source_navigation',
                'source_coordinate_hold', 'normalization_hold', 'source_body',
                'source_body_sha256', 'source_body_qualification')) or
            str(row.get('source_evidence', '')).startswith('evidence/') and
                Path(str(row.get('source_evidence', ''))).name in {
                    'Matins-Prophecies.txt', 'Matins-Psalm_and_Gospel.txt',
                    'Prophecies.txt', 'Psalm_and_Gospel.txt'})


def _validate_boolean_contract(actual, expected):
    """Python equality is not typed authentication (False == 0, True == 1)."""
    if type(expected) is bool:
        if type(actual) is not bool or actual is not expected:
            raise ValueError('Matins literal boolean contract drift')
    elif isinstance(expected, dict) and isinstance(actual, dict):
        for key, value in expected.items():
            _validate_boolean_contract(actual.get(key), value)
    elif isinstance(expected, list) and isinstance(actual, list):
        for left, right in zip(actual, expected):
            _validate_boolean_contract(left, right)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _json(path):
    return json.loads(path.read_bytes())


def _bound_file(root, relative, fingerprints):
    path = (root / relative).resolve()
    if Path(relative).is_absolute() or not path.is_relative_to(root.resolve()):
        raise ValueError('Matins source evidence escapes portable fixture')
    data = path.read_bytes()
    if fingerprints.get(relative) != _sha(data):
        raise ValueError(f'Matins source evidence drift: {relative}')
    return data


def load_dated_matins_fixture(root=FIXTURE_ROOT):
    """Recheck all raw documents, context evidence and independent review bytes."""
    root = Path(root).resolve()
    raw = (root / 'fingerprints.json').read_bytes()
    if _sha(raw) != FINGERPRINTS_SHA256:
        raise ValueError('Untrusted Matins fixture manifest')
    fingerprints = json.loads(raw)
    for relative in fingerprints:
        _bound_file(root, relative, fingerprints)
    if fingerprints.get('accepted-source-corpus.json') != CORPUS_SHA256:
        raise ValueError('Untrusted Matins accepted corpus')
    corpus = _json(root / 'accepted-source-corpus.json')
    fixture = {'root': root, 'fingerprints': fingerprints, 'corpus': corpus,
               'path_map': _json(root / 'path-map.json')}
    authenticate_dated_matins_fixture(fixture)
    return fixture


def _evidence(fixture, original):
    relative = fixture['path_map'].get(original)
    if not relative:
        raise ValueError('Unbound Matins original evidence locator')
    return _bound_file(fixture['root'], relative, fixture['fingerprints'])


def authenticate_dated_matins_fixture(fixture):
    """Authenticate source order/envelopes plus exact civil and selected context.

    Rechecks relevant immutable bytes on every helper call; a mutable cached
    in-memory object is not an authentication boundary.
    """
    root = Path(fixture['root']).resolve()
    raw = (root / 'fingerprints.json').read_bytes()
    if _sha(raw) != FINGERPRINTS_SHA256 or fixture['fingerprints'] != json.loads(raw):
        raise ValueError('Matins fixture trust-root drift')
    for key, filename in [('corpus', 'accepted-source-corpus.json'), ('path_map', 'path-map.json')]:
        data = _bound_file(root, filename, fixture['fingerprints'])
        expected = json.loads(data)
        _validate_boolean_contract(fixture[key], expected)
        if fixture[key] != expected:
            raise ValueError(f'Matins in-memory {key} drift')
    corpus = fixture['corpus']
    if len(corpus['records']) != 119 or len(corpus['complete_exact_dated_Matins_pairs']) != 59:
        raise ValueError('Matins corpus completeness changed')
    for name, review in corpus['review_receipts'].items():
        data = _bound_file(root, 'evidence/' + name + '/FINAL-RECEIPT.json', fixture['fingerprints'])
        if _sha(data) != review['receipt_sha256'] or review['hash_mismatches']:
            raise ValueError('Matins independent review receipt drift')
    keys = set()
    for accepted in corpus['records']:
        if (accepted['acceptance'] != 'exact_dated_source_only' or
                any(accepted[k] for k in ('canonical_equivalence_approved', 'recurrence_approved', 'runtime_activation'))):
            raise ValueError('Matins acceptance is source-only, not activation')
        record = accepted['source_record']
        key = (record['civil_date'], record['occasion_key'], record['slot'])
        if key in keys:
            raise ValueError('Duplicate Matins dated child witness')
        keys.add(key)
        date = dt.date.fromisoformat(record['civil_date'])
        if ((date - julian_pascha_gregorian(date.year)).days != record['pascha_offset_days'] or
                date.strftime('%A') != record['weekday'] or record['service'] != 'Matins' or
                record['navigation'] != ['Readings', 'Matins', record['slot']]):
            raise ValueError('Matins source date/navigation/offset disagrees')
        data = _evidence(fixture, record['text_path'])
        if _sha(data) != record['text_sha256'] or _sha(data) != record['whole_rendered_body_sha256']:
            raise ValueError('Matins full source body drift')
        lines = data.decode('utf-8').splitlines(keepends=True)
        last = -1
        headings = []
        for order, block in enumerate(record['ordered_source_blocks'], 1):
            literal = block['body_envelope_literal']
            raw_line = base64.b64decode(block['raw_line_utf8_base64'])
            offset = block['source_byte_offset']
            if (block['source_order'] != order or offset <= last or
                    data[offset:offset+len(raw_line)] != raw_line or
                    raw_line.decode().rstrip('\n') != block['raw_reference_line'] or
                    ''.join(lines[block['body_envelope_first_line']-1:block['body_envelope_last_line']]) != literal or
                    _sha(literal.encode()) != block['body_envelope_sha256'] or
                    block['source_line'] != block['body_envelope_first_line']):
                raise ValueError('Matins raw heading/body/order envelope drift')
            last = offset
            headings.append(block['raw_reference_line'])
        if headings != record['raw_reference_lines']:
            raise ValueError('Matins heading completeness disagrees')
        if record['slot'] == 'Psalm and Gospel' and len(headings) != 2:
            raise ValueError('Matins Psalm/Gospel companion missing')
        if record['slot'] == 'Prophecies':
            state = record['semantic_state']
            if state == 'explicit_no_prophecies_rubric':
                if headings or 'No prophecies are read on this day.' not in data.decode():
                    raise ValueError('No-prophecy rubric is not a no-Matins rubric')
            elif state != 'assigned_scripture_table' or not headings:
                raise ValueError('Unqualified prophecy table')
        contexts = record.get('context_files', {})
        if isinstance(contexts, dict):
            contexts = [{'path': p, 'sha256': h} for p, h in contexts.items()]
        if not contexts:
            supplementary = json.loads(_bound_file(root, 'supplementary-contexts.json', fixture['fingerprints']))
            contexts = [{'path': p} for p in supplementary.get(record['text_path'], [])]
        if not contexts:
            raise ValueError('Matins captured selected context missing')
        for evidence in contexts:
            content = _evidence(fixture, evidence['path'])
            if evidence.get('sha256') and _sha(content) != evidence['sha256']:
                raise ValueError('Matins original context hash disagrees')
            if Path(evidence['path']).name in {'context.txt', 'home-selected.txt'}:
                captured = content.decode().strip()
                declared = record['context'].strip()
                if captured != declared and not (declared == record['actual_home_line'] and
                                                  captured.splitlines()[0] == declared):
                    raise ValueError('Matins actual selected context disagrees')
        images = record.get('reference_screenshots', [])
        if record.get('screenshot'):
            images = images + [{'path': record['screenshot'], 'sha256': record.get('screenshot_sha256') or
                                fixture['fingerprints'][fixture['path_map'][record['screenshot']]]}]
        for image in images:
            expected = image.get('sha256') or fixture['fingerprints'][fixture['path_map'][image['path']]]
            if _sha(_evidence(fixture, image['path'])) != expected:
                raise ValueError('Matins accepted reference screenshot drift')


def _pair(context, fixture):
    authenticate_dated_matins_fixture(fixture)
    if set(context) != set(CONTEXT_KEYS):
        raise ValueError('Full actual captured Matins context required, not date-only assertion')
    records = [x['source_record'] for x in fixture['corpus']['records']
               if all(context[k] == x['source_record'][k] for k in CONTEXT_KEYS)]
    if len(records) != 2 or {r['slot'] for r in records} != {'Prophecies', 'Psalm and Gospel'}:
        raise ValueError('No complete accepted exact-dated Matins pair; no recurrence or cross-date pairing')
    return (next(r for r in records if r['slot'] == 'Prophecies'),
            next(r for r in records if r['slot'] == 'Psalm and Gospel'))


def _parse_input(raw):
    """Held source-label search syntax, respecting observed resets/omissions."""
    text = re.sub(r'\s*:\s*', ':', raw.strip())
    # These exact accepted envelopes expose chapter-reset/omitted labels. The
    # source-search syntax must not manufacture absent 2:1 or Mark 44/46.
    # This is held Reader-coordinate syntax, never canonical/MT equivalence.
    observed = {
        'Isaiah 1:19-2:2-3': 'Isaiah 1:19-31; Isaiah 2:2-3',
        'Jonah 1:1-2:1': 'Jonah 1:1-16; Jonah 2:1',
        'Mark 9:43-50': 'Mark 9:43; Mark 9:45; Mark 9:47-50',
    }
    if text in observed:
        return observed[text]
    match = re.match(r'(.+?)\s+\d+\s*:', text)
    if match:
        book = match[1]
        text = '; '.join((book + ' ' + part.strip()) if i and re.match(r'^\d+:', part.strip())
                         else part.strip() for i, part in enumerate(text.split(';')))
    return text


def _qualification(block):
    labels = []
    for line in block['body_envelope_literal'].splitlines():
        if re.search(r'[\u0600-\u06ff\u2c80-\u2cff]', line):
            continue
        match = re.match(r'^(\d+)\s+(.+)', line)
        if match and re.search('[A-Za-z]', match[2]):
            labels.append({'label': int(match[1]), 'raw_line': line})
    ref = block['raw_reference_line'].strip()
    notes = {
        'Isaiah 1:19-2:2-3': 'labels 19-31 then 2,3; no source 2:1; final label 3 is partial',
        'Jonah 1:1-2:1': 'labels 1-16 then 1 great fish; no canonical chapter-reset equivalence asserted',
        'Isaiah 2:3-11': 'last source verse 11 is partial',
        'Isaiah 2:11-19': 'first source verse 11 is partial',
        'Isaiah 49:6-10': 'first source verse 6 is partial',
        'Isaiah 65:8-16': 'last source verse 16 is partial',
        'Zechariah 9:9-15': 'verse 15 contains only its first sentence',
        'Mark 9:43-50': 'source omits numbered verses 44 and 46; never interpolate',
        'John 12:26-36': 'last source verse 36 is partial',
        'Luke 9:37-43': 'last source verse 43 is partial',
    }
    partial = [notes[ref]] if ref in notes and ('partial' in notes[ref] or 'first sentence' in notes[ref]) else []
    return {'boundary_claim': block['boundary_claim'], 'english_numbered_lines': labels,
            'qualification': notes.get(ref, 'Literal source envelope; printed endpoints are not a full-verse/canonical equivalence assertion'),
            'partial_boundary_notes': partial, 'omitted_verses': [44,46] if ref == 'Mark 9:43-50' else [],
            'source_numbering': 'literal_reader_edition_unmapped', 'canonical_equivalence_approved': False}


def _source_rows(context, fixture):
    prophecy, pg = _pair(context, fixture)
    source_context = {**deepcopy(context), 'prophecy_semantic_state': prophecy['semantic_state'],
                      'accepted_corpus_sha256': CORPUS_SHA256,
                      'review_receipt_hashes': {k:v['receipt_sha256'] for k,v in fixture['corpus']['review_receipts'].items()}}
    out = []
    for record in (prophecy, pg):
        for local_order, block in enumerate(record['ordered_source_blocks'], 1):
            kind = 'Prophecy' if record['slot'] == 'Prophecies' else 'Psalm' if local_order == 1 else 'Gospel'
            order = len(out) + 1
            out.append({'source': CANDIDATE_SOURCE, 'gregorian_date': context['civil_date'],
                        'weekday': context['weekday'], 'day_title': context['actual_occasion'],
                        'service_section': 'Matins', 'reading_type': kind,
                        'raw_ref': block['raw_reference_line'].strip(), 'normalized_ref': '', 'canonical_ref': '',
                        'source_parse_input': _parse_input(block['raw_reference_line']),
                        'parse_status': 'candidate_matins_source_coordinate_hold',
                        'normalization_warning': 'source coordinates held; edition/canonical/runtime/recurrence approval absent',
                        'url': record['url'], 'source_order': order,
                        'source_slot': f'OT{local_order}' if kind == 'Prophecy' else 'matins_' + kind.lower(),
                        'source_body': block['body_envelope_literal'],
                        'source_body_sha256': block['body_envelope_sha256'],
                        'source_raw_reference_line': block['raw_reference_line'],
                        'source_line': block['source_line'], 'source_byte_offset': block['source_byte_offset'],
                        'source_document_sha256': record['text_sha256'],
                        'source_document_body': _evidence(fixture, record['text_path']).decode('utf-8'),
                        'source_captured_context': record['context'],
                        'source_navigation': deepcopy(record['navigation']),
                        'source_evidence_state': record['evidence_state'],
                        'source_evidence': fixture['path_map'][record['text_path']],
                        'source_context': deepcopy(source_context),
                        'source_body_qualification': _qualification(block),
                        'source_coordinate_hold': True, 'normalization_hold': True,
                        'source_convention': 'literal_reader_edition_unmapped',
                        'canonical_equivalence_approved': False, 'recurrence_approved': False,
                        'runtime_activation_approved': False, 'candidate_only': True,
                        'active': True, 'state': 'current', 'include_in_current_index': False})
    return out, source_context


def _removed(row):
    return (not is_current_source_row(row) or
            str(row.get('current_status') or '').lower() not in {'', 'active', 'current'})


def project_dated_matins_source(rows, context, fixture=None):
    """Replace only the exact captured active Matins block; preserve raw history.

    This explicitly invoked source candidate is excluded from default canonical
    date indexes. Current means current *candidate* table, not package activation.
    Other services/date rows (including their history) pass through unchanged.
    """
    fixture = fixture if fixture is not None else load_dated_matins_fixture()
    replacement, source_context = _source_rows(context, fixture)
    date = context['civil_date']
    target = [i for i,r in enumerate(rows) if r.get('gregorian_date') == date and r.get('service_section') == 'Matins']
    if not target or target != list(range(target[0], target[-1]+1)):
        raise ValueError('Missing/interleaved exact-date Matins block')
    originals = [rows[i] for i in target]
    if any(_removed(r) for r in originals):
        raise ValueError('Removed/inactive Matins input cannot be restored implicitly')
    if any(r.get('source') == CANDIDATE_SOURCE or r.get('candidate_only') for r in originals):
        raise ValueError('Candidate replay/overlap is not an upstream source block')
    if any(r.get('reading_type') not in {'Prophecy', 'Prophecies', 'Psalm', 'Gospel'} for r in originals):
        raise ValueError('Unqualified target Matins reading type')
    for kind in ('Psalm', 'Gospel'):
        if sum(r['reading_type'] == kind for r in originals) != 1:
            raise ValueError('Missing/duplicate Matins Psalm/Gospel anchors')
    prophecies = [r for r in originals if r['reading_type'] in {'Prophecy', 'Prophecies'}]
    for i,row in enumerate(prophecies):
        for other in prophecies[:i]:
            left, right = parse_passage(row['raw_ref']), parse_passage(other['raw_ref'])
            overlaps = left and right and left.book_abbrev == right.book_abbrev and any(
                (a.chapter_start, a.verse_start or 0) <= (b.chapter_end, b.verse_end or 999) and
                (b.chapter_start, b.verse_start or 0) <= (a.chapter_end, a.verse_end or 999)
                for a in left.parts for b in right.parts)
            if row['raw_ref'] == other['raw_ref'] or overlaps:
                raise ValueError('Duplicate/overlapping upstream prophecy inputs')
    history = [{**deepcopy(r), 'active': False, 'state': 'superseded', 'status': 'removed',
                'include_in_current_index': False, 'superseded_reason': 'exact_dated_Matins_source_candidate',
                'source_context': deepcopy(source_context)} for r in originals]
    return {'active': deepcopy(rows[:target[0]]) + replacement + deepcopy(rows[target[-1]+1:]),
            'history': history, 'source_context': source_context,
            'runtime_activation_approved': False, 'canonical_equivalence_approved': False,
            'recurrence_approved': False, 'candidate_only': True}


def candidate_matins_index(rows, fixture=None):
    """Authenticate whole candidate tables before exposing source-only search rows.

    matched_ref/canonical_ref stay blank. source_parse_input is syntactic search
    input, NOT an authorized canonical span. Missing/removed rows fail closed.
    """
    fixture = fixture if fixture is not None else load_dated_matins_fixture()
    authenticate_dated_matins_fixture(fixture)
    candidates = [r for r in rows if is_dated_matins_candidate(r)]
    if rows and not candidates:
        raise ValueError('Matins candidate API requires candidate witnesses, not an empty authentication result')
    groups = {}
    for row in candidates:
        flags = {'source_coordinate_hold': True, 'normalization_hold': True,
                 'canonical_equivalence_approved': False, 'recurrence_approved': False,
                 'runtime_activation_approved': False, 'candidate_only': True,
                 'active': True, 'include_in_current_index': False}
        _validate_boolean_contract(row, flags)
        if (row.get('state') != 'current' or
                any(key in row for key in ('status', 'current_status', 'superseded_reason',
                    'removal_reason', 'removed_reason', 'removal_effective_version',
                    'removed_from_standard_lectionary'))):
            raise ValueError('Matins candidate current-state contract drift')
        if not isinstance(row.get('source_context'), dict):
            raise ValueError('Matins candidate source context missing')
        groups.setdefault(row.get('gregorian_date'), []).append(row)
    for table in groups.values():
        context = {key: deepcopy(table[0]['source_context'].get(key)) for key in CONTEXT_KEYS}
        expected, _ = _source_rows(context, fixture)
        _validate_boolean_contract(table, expected)
        if table != expected:
            raise ValueError('Matins candidate whole-table body/order/scope/state/hold drift')
    return [{**deepcopy(row), 'matched_ref': '', 'canonical_ref': '',
             'source_ref_status': row['parse_status'], 'search_coordinate_kind': 'held_source_only'}
            for row in candidates]


def query_candidate_matins_source(query, rows, fixture=None):
    """Explicit trusted held-source lane, NOT canonical/MT or package search.

    Authenticate the complete dated candidate table before filtering, including
    queries with no results. Search only observed source components and return
    all body/partial-boundary/printed-edition disclosures unchanged.
    """
    index = candidate_matins_index(rows, fixture)
    return [row for row in index if passage_matches(query, row['source_parse_input'])]
