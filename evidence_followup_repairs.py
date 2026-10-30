"""T-L6 / LK7 evidence metadata and frame-qualified LK9 annotations.

Pure transformations, no output writes, activation, recurrence or deletion.
The pinned predecessor target ledger is not generated from candidate rows.
Call repair_rows before serializing reverse output and validate_rows on the
serialized readback. Daily rows use repair_psalm_annotations separately.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER_RELATIVE = Path('docs/reviews/timothy-luke-evidence-1.3.8/baseline-targets.json')
LEDGER_SHA256 = 'de51c94fa1c988a1d5e40f5ef2b8f4cebb84de5051dd05fa3031d978f1e14bbe'
SPECIAL_RELATIVE = Path('sources/coptic-reader/special-context-projection-2026-10-07')
MANIFEST_SHA256 = 'cad392515629f98d3685ba0c1f0f8254d1c3d420c398b82ce3a9bc1a24e03c4d'
SELECTOR_FIELDS = ('source_kind', 'source_family', 'calendar_keys', 'service_section', 'slot', 'canonical_mt_ref')
PROTECTED_FIELDS = ('identity_key', 'canonical_lxx_ref', 'spans_json', 'source_locator', 'source_title', 'source_edition', 'provenance')
LIFECYCLE_FIELDS = ('current_status', 'removed_marker', 'active', 'include_in_current_index', 'state', 'status')
OUTPUT_FIELDS = ('authority_tier', 'evidence_status', 'evidence_json', 'source_disclosure')


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _read(root, relative, digest):
    path = Path(root) / relative
    try:
        if path.is_symlink() or not path.resolve().is_relative_to(Path(root).resolve()):
            raise ValueError('evidence path escape')
        data = path.read_bytes()
    except OSError as exc:
        raise ValueError('evidence missing: ' + str(relative)) from exc
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError('evidence hash mismatch: ' + str(relative))
    return data


def load_target_ledger(root=None):
    return json.loads(_read(root or ROOT, LEDGER_RELATIVE, LEDGER_SHA256))


def _key(row):
    return tuple(row.get(k, '') for k in SELECTOR_FIELDS)


def _special_records(root):
    manifest = json.loads(_read(root, SPECIAL_RELATIVE / 'manifest.json', MANIFEST_SHA256))
    records = json.loads(_read(root, SPECIAL_RELATIVE / 'records.json', manifest['files']['records.json']))
    return manifest, records


def _captures(entry, root, manifest, records):
    evidence = []
    for pin in entry['records']:
        matches = [r for r in records if r['capture_id'] == pin['capture_id'] and r['ordinal'] == pin['ordinal']]
        if len(matches) != 1:
            raise ValueError('evidence source identity mismatch')
        r = matches[0]
        expected = {'line': pin['line'], 'raw_heading': pin['heading'], 'navigation': pin['navigation'],
                    'raw_text_sha256': pin['sha256'], 'section': pin['section'],
                    'printed_ref': pin['printed_ref'], 'kind': pin['kind'],
                    'reading_type': pin['reading_type'], 'canonical_mt_ref': pin['canonical_mt_ref'],
                    'selected': True, 'context': pin['context']}
        if any(type(r.get(k)) is not type(v) or r.get(k) != v for k, v in expected.items()):
            raise ValueError('evidence selected source/context mismatch')
        if type(r['ordinal']) is not int or r['ordinal'] <= 0 or type(r['line']) is not int or r['line'] <= 0:
            raise ValueError('evidence ordinal type mismatch')
        relative = SPECIAL_RELATIVE / 'raw' / (pin['capture_id'] + '.txt')
        if manifest['files'].get('raw/' + pin['capture_id'] + '.txt') != pin['sha256']:
            raise ValueError('evidence manifest document mismatch')
        text = _read(root, relative, pin['sha256']).decode()
        lines = text.splitlines()
        if (lines[0] != pin['document_title'] or lines[pin['line']-1] != pin['heading']
                or not text[r['offset']:].startswith(pin['heading'])):
            raise ValueError('evidence document heading/context mismatch')
        item = {**pin, 'path': relative.as_posix(), 'fresh_app_verification': False}
        if r['reading_type'] == 'unclassified':
            proof_path = Path('sources/coptic-reader/special-classification-integration-2026-10-07/source-classification-verdicts.json')
            proof_sha = 'de56efa0c2009b32359dbd2e1901a2848f04a3dc35dee10d2ad3302799f0bf19'
            proofs = json.loads(_read(root, proof_path, proof_sha))
            proof, = [p for p in proofs if p['capture_id'] == r['capture_id'] and p['ordinal'] == r['ordinal']]
            if (proof['classification'] != 'assigned_reading' or proof['proposed_reading_type'] != 'gospel'
                    or proof['navigation'] != r['navigation'] or proof['section'] != r['section']
                    or proof['printed_ref'] != r['printed_ref'] or proof['sha256'] != pin['sha256']
                    or any(lines[p['line']-1] != p['text'] for p in proof['evidence'] + proof['governing_rubric'])):
                raise ValueError('evidence assigned-reading classification mismatch')
            item['classification_evidence'] = {'path': proof_path.as_posix(), 'sha256': proof_sha,
                                               'classification': 'assigned_reading', 'reading_type': 'gospel'}
        evidence.append(item)
    return evidence


def _same_service(capture, root):
    # Authenticate both service paths, complete dated table and exact Pauline body.
    # Do not infer equality of the whole two tables, which differ in indexed scope.
    import covenant_thursday_source_supplements as covenant
    if Path(root).resolve() != ROOT.resolve():
        raise ValueError('evidence Covenant Thursday qualification requires the complete repository source pack')
    contract = covenant.load_covenant_thursday_contract()
    appointment, = [a for a in contract['appointments']
                    if a['service_section'] == covenant.WATERS_SECTION and a['printed_ref'] == '1 Timothy 4:9-5:10']
    document, = [d for d in contract['documents'] if d['service_section'] == covenant.WATERS_SECTION]
    lines = _read(root, capture['path'], capture['sha256']).decode().splitlines()
    body_lines = appointment['body_envelope_literal'].splitlines()
    body = '\n'.join(lines[capture['line']-1:capture['line']-1+len(body_lines)])
    if (capture['navigation'] != ['Special', 'Lakkan', 'Covenant Thursday']
            or lines[0] != document['title'] or body != appointment['body_envelope_literal']):
        raise ValueError('evidence Lakkan same-service/body mismatch')
    return {'calendar_keys': 'Great Thursday', 'service_section': covenant.WATERS_SECTION,
            'matching_ref': '1Tim 4:9-5:10', 'document_title': document['title'],
            'dated_path': (covenant.SOURCE_RELATIVE / appointment['file']).as_posix(),
            'dated_sha256': appointment['full_capture_sha256'],
            'dated_heading_line': appointment['heading_line'],
            'matching_body_sha256': appointment['body_envelope_sha256'],
            'source_contract_sha256': covenant.CONTRACT_SHA256,
            'entire_tables_equivalent': False, 'deduplication_action': 'metadata_only_no_deletion'}


def _eligible(row, baseline):
    if (row.get('current_status') != baseline['current_status']
            or type(row.get('removed_marker')) is not str or row.get('removed_marker')):
        return False
    if row.get('state', '') not in ('', 'current') or row.get('status', '') not in ('', 'current'):
        return False
    for field in ('active', 'include_in_current_index'):
        if field in row and row[field] is not True:
            return False
    return True


def _expected(row, entry, root, manifest, records):
    baseline = entry['baseline']
    for field in PROTECTED_FIELDS:
        if type(row.get(field)) is not type(baseline.get(field)) or row.get(field) != baseline.get(field):
            raise ValueError('evidence target source/coordinate drift: ' + field)
    eligible = _eligible(row, baseline)
    proof = {'requests': entry['requests'], 'baseline_version': '1.3.7',
             'occurrence': {k: row.get(k, '') for k in SELECTOR_FIELDS},
             'lifecycle': {k: row.get(k) for k in LIFECYCLE_FIELDS},
             'fresh_app_verification': False, 'status_change_authorized': False,
             'captures': _captures(entry, root, manifest, records) if entry['records'] else []}
    if entry['records']:
        status = 'retained_reader_capture' if eligible else 'retained_reader_capture_inactive_witness'
        tier = 'current_authority' if eligible else baseline['authority_tier']
        if baseline['calendar_keys'] == 'lakkan_covenant_thursday':
            proof['same_service'] = _same_service(proof['captures'][0], root)
    else:
        status = 'unverified_service_book'
        tier = baseline['authority_tier']
        proof.update(edition=entry['edition'], check_sheet_section='service book',
                     limitation='No exact Reader context accepted for this printed-edition target in this bounded review; not a global absence claim.')
    disclosures = json.loads(row['source_disclosure'])
    original_disclosures = json.loads(baseline['source_disclosure'])
    if len(disclosures) != len(original_disclosures):
        raise ValueError('evidence source disclosure cardinality drift')
    for disclosure, original in zip(disclosures, original_disclosures):
        if any(type(disclosure.get(k)) is not type(v) or disclosure.get(k) != v for k, v in original.items()):
            raise ValueError('evidence original source disclosure drift')
        disclosure['evidence_followup'] = proof
    return {'authority_tier': tier, 'evidence_status': status, 'evidence_json': _json(proof),
            'source_disclosure': _json(disclosures)}


def repair_evidence_rows(rows, *, root=None):
    """Return fresh rows and exact metadata counts; never change lifecycle/selection.

    Accept predecessor or idempotent successor rows. A copied existing evidence
    payload is reauthenticated, never used as an authorization token.
    """
    root = Path(root or ROOT)
    entries = {_key(t['baseline']): t for t in load_target_ledger(root)['targets']}
    result = copy.deepcopy(rows)
    counts = dict(targets=0, captured=0, unverified_service_book=0, authority_tier_changed=0, same_service_marked=0)
    manifest = records = None
    for row in result:
        entry = entries.get(_key(row))
        if entry is None:
            if row.get('evidence_json'):
                raise ValueError('evidence attached to an unqualified occurrence')
            continue
        if entry['records'] and manifest is None:
            manifest, records = _special_records(root)
        expected = _expected(row, entry, root, manifest, records)
        if row.get('evidence_json'):
            for field in OUTPUT_FIELDS:
                # JSON object order is not authority; scalar types/values are.
                a, b = row.get(field), expected[field]
                if field in ('evidence_json', 'source_disclosure'):
                    a, b = json.loads(a), json.loads(b)
                if _json(a) != _json(b):
                    raise ValueError('evidence output/context drift: ' + field)
        counts['targets'] += 1
        counts['captured' if entry['records'] else 'unverified_service_book'] += 1
        counts['authority_tier_changed'] += row['authority_tier'] != expected['authority_tier']
        counts['same_service_marked'] += entry['baseline']['calendar_keys'] == 'lakkan_covenant_thursday'
        row.update(expected)
    return result, counts


def validate_evidence_rows(rows, *, root=None, require_all_targets=False):
    expected, _ = repair_evidence_rows(rows, root=root)
    if require_all_targets:
        targets = {_key(t['baseline']) for t in load_target_ledger(root)['targets']}
        selected = [_key(r) for r in rows if _key(r) in targets]
        if len(selected) != len(targets) or set(selected) != targets:
            raise ValueError('evidence target membership incomplete or duplicated')
    for before, after in zip(rows, expected):
        if any(before.get(k) != after.get(k) for k in OUTPUT_FIELDS):
            raise ValueError('evidence metadata missing or stale')


def _psalm_frame(row, spans):
    """Numeric source coordinates are not automatically canonical MT coordinates."""
    from passage_normalization import parse_passage
    if not row.get('canonical_mt_ref') or not spans:
        return 'held_or_source_only'
    if any(s.get('source_convention') != 'mt_nkjv' or s.get('confidence') in ('held', 'source_coordinates') for s in spans):
        return 'non_mt_or_qualified_hold'
    parsed = parse_passage(row['canonical_mt_ref'])
    if not parsed or parsed.book_abbrev != 'Ps':
        return 'frame_mismatch'
    coordinates = [(p.chapter_start, p.verse_start, p.chapter_end, p.verse_end) for p in parsed.parts]
    actual = [tuple(s.get(k) for k in ('chapter_start', 'verse_start', 'chapter_end', 'verse_end')) for s in spans]
    if (any(s.get('book') != 'Ps' for s in spans)
            or any(value is not None and type(value) is not int for point in actual for value in point)
            or coordinates != actual or any(s.get('canonical_mt_ref') != row['canonical_mt_ref'] for s in spans)):
        return 'frame_mismatch'
    return 'mt_nkjv'


def frame_qualified_lxx(mt_ref):
    """Current converter plus authenticated superscription-sensitive counterpart.

    The generic converter intentionally returns chapter-only medium-confidence
    proposals. Its success is not evidence of verse identity. Covenant Thursday's
    retained Brenton/NKJV body witnesses qualify 51:7 and 51:10 as covering loci,
    not an automatic +2 rule or authority for other printed source frames.
    """
    from build_design_deliverables import psalm_lxx_ref
    proposal, basis, confidence = psalm_lxx_ref(mt_ref)
    if mt_ref in ('Ps 51:7', 'Ps 51:10'):
        import covenant_thursday_source_supplements as covenant
        contract = covenant.load_covenant_thursday_contract()
        appointment, = [a for a in contract['appointments']
                        if a['service_section'] == covenant.WATERS_SECTION and a['printed_ref'] == 'Psalms 51:7, 10']
        mapping = dict(zip(appointment['normalized_fragments'], appointment['canonical_lxx_fragments']))
        return mapping[mt_ref], 'retained Brenton/NKJV covering locus; contract sha256=' + covenant.CONTRACT_SHA256, 'bounded_parallel_locus_not_exact_edition_equivalence'
    return proposal, basis, confidence


def repair_psalm_annotations(rows):
    """Recompute only MT-qualified annotations, preserving every source coordinate.

    Changed identity keys are intentionally NOT invented here. These are retained
    occurrence identifiers; correction metadata changes annotation, not selection.
    Qualified source-owned/held frames never compete in a global one-to-one map.
    """
    result = copy.deepcopy(rows)
    counts = dict(psalm_rows=0, mt_qualified=0, annotations_changed=0, held_or_source_only=0,
                  non_mt_or_qualified_hold=0, frame_mismatch=0, qualified_mapping_preserved=0,
                  unresolved_disagreements=0)
    cache = {}
    for row in result:
        spans = row.get('spans_json', '[]')
        spans = json.loads(spans) if isinstance(spans, str) else spans
        if not (str(row.get('canonical_mt_ref', '')).startswith('Ps ') or str(row.get('canonical_lxx_ref', '')).startswith('Ps ')
                or any(s.get('book') == 'Ps' for s in spans)):
            continue
        counts['psalm_rows'] += 1
        frame = _psalm_frame(row, spans)
        if frame != 'mt_nkjv':
            counts[frame] += 1
            continue
        counts['mt_qualified'] += 1
        mt = row['canonical_mt_ref']
        if mt not in cache:
            cache[mt] = frame_qualified_lxx(mt)
        lxx, basis, confidence = cache[mt]
        if lxx == row.get('canonical_lxx_ref'):
            continue
        # Source-owned covering loci outrank an unqualified chapter-only proposal.
        if any(s.get('confidence') == 'bounded_parallel_locus_not_exact_edition_equivalence' for s in spans):
            counts['qualified_mapping_preserved'] += 1
            continue
        # A medium chapter proposal must never replace a text-qualified result.
        if confidence not in ('high', 'bounded_parallel_locus_not_exact_edition_equivalence'):
            counts['unresolved_disagreements'] += 1
            continue
        if any(s.get('confidence') not in ('medium', 'high') for s in spans):
            counts['unresolved_disagreements'] += 1
            continue
        old = row.get('canonical_lxx_ref', '')
        row['canonical_lxx_ref'] = lxx
        row['display_ref'] = f'{mt} (LXX {lxx})' if lxx != mt else mt
        for span in spans:
            span.update(canonical_lxx_ref=lxx, validation_basis=basis, confidence=confidence)
        row['spans_json'] = json.dumps(spans, ensure_ascii=False, sort_keys=True)
        row['psalm_annotation_review_json'] = _json({'request': 'LK9', 'mt_frame': 'mt_nkjv',
            'old_lxx_ref': old, 'canonical_lxx_ref': lxx, 'basis': basis,
            'qualification': confidence, 'source_coordinates_changed': False})
        counts['annotations_changed'] += 1
    return result, counts


def validate_psalm_annotations(rows):
    expected, counts = repair_psalm_annotations(rows)
    if counts['annotations_changed']:
        raise ValueError('Psalm annotation stale in frame-qualified MT rows')
    # A converter proposal is report-only when evidence or edition alignment is held.
    return counts


def repair_rows(rows, *, root=None):
    result, evidence = repair_evidence_rows(rows, root=root)
    result, psalms = repair_psalm_annotations(result)
    return result, {'evidence': evidence, 'psalms': psalms}


def validate_rows(rows, *, root=None, require_all_targets=False):
    validate_evidence_rows(rows, root=root, require_all_targets=require_all_targets)
    return validate_psalm_annotations(rows)


def restore_rows_for_comparison(rows, *, date=None, require_all_targets=False):
    """Authenticate final deltas against frozen inputs, then undo only this layer.

    Converter idempotency is not an annotation oracle: exact expected annotations
    come from the authenticated published predecessor, never from candidate rows.
    """
    import metadata_followup_repairs as metadata
    if date is None:
        validate_evidence_rows(rows, require_all_targets=require_all_targets)
    frozen = metadata.baseline()
    originals = frozen['reverse_rows'] if date is None else frozen['daily'].get(date[:4], {}).get(date, [])
    projected, _ = repair_psalm_annotations(originals)
    annotation_fields = ('canonical_lxx_ref', 'display_ref', 'spans_json', 'psalm_annotation_review_json')
    identity = lambda r: tuple(r.get(k, '') for k in
        ('identity_key', 'source_locator', 'source_family', 'source_kind', 'occasion', 'service_section', 'slot'))
    annotations = {identity(a): (a, b) for a, b in zip(originals, projected)
                   if a != b}
    targets = {_key(t['baseline']): t['baseline'] for t in load_target_ledger()['targets']} if date is None else {}
    output = copy.deepcopy(rows)
    for row in output:
        pair = annotations.get(identity(row))
        if pair:
            before, expected = pair
            for field in annotation_fields:
                if (field in row) != (field in expected) or (field in expected and
                        (type(row[field]) is not type(expected[field]) or row[field] != expected[field])):
                    raise ValueError('Psalm annotation authenticated delta drift: ' + field)
            for field in annotation_fields:
                if field in before:
                    row[field] = before[field]
                else:
                    row.pop(field, None)
        elif row.get('psalm_annotation_review_json'):
            raise ValueError('Psalm annotation unqualified source context')
        original = targets.get(_key(row))
        if original:
            for field in OUTPUT_FIELDS:
                if field in original:
                    row[field] = original[field]
                else:
                    row.pop(field, None)
    return output
