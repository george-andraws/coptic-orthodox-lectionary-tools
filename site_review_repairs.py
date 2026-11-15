"""Source-bound 1.3.11 outer lane; predecessors and held coordinates unchanged.

Exact-context Brenton covering annotations are not reading appointments or exact
cross-edition equivalences. Waters materialization uses the complete existing
current reverse groups, retaining working status. The authenticated inverse runs
before every older source validator; it is not an exemption from those gates.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = 'sources/site-review-1.3.11/'
MANIFEST_SHA256 = '33dcf74761e82b0f50364b1621580064de1734fc164365fc6b162dd9c004c1dd'
MARKERS = ('edition_psalm_covering_json', 'waters_materialization_json')
CONTEXT = ('identity_key', 'source_family', 'source_kind', 'occasion', 'service_section', 'slot')
LIFECYCLE = ('active', 'status', 'state', 'include_in_current_index', 'removal_effective_version')
ANNOTATION_FIELDS = ('canonical_lxx_ref', 'display_ref', 'spans_json', 'source_disclosure', 'edition_psalm_covering_json')


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _read(relative, digest):
    p = ROOT / relative
    if p.is_symlink() or not p.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('site review source path escape')
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('site review source hash mismatch: ' + relative)
    return raw


@lru_cache(maxsize=1)
def _decode(raw):
    return json.loads(gzip.decompress(raw))


def baseline():
    manifest = json.loads(_read(SOURCE+'manifest.json', MANIFEST_SHA256))
    return _decode(_read(SOURCE+'published-1.3.10-targets.json.gz', manifest['fixture_sha256']))


def authenticate_sources():
    manifest = json.loads(_read(SOURCE+'manifest.json', MANIFEST_SHA256))
    for relative, witness in manifest['bible_files'].items():
        _read(SOURCE+relative, witness['sha256'])
    for witness in manifest['body_checks']:
        _read(witness['path'], witness['sha256'])
    for relative, digest in manifest['source_files'].items():
        _read(relative, digest)
    return manifest


def _key(row):
    return tuple(row.get(f, '') for f in CONTEXT + ('source_locator', 'calendar_keys', 'service_hour', 'coptic_date_key', 'annual_sunday'))


def _proof_key(row):
    return tuple(row.get(f, '') for f in CONTEXT)


def _same(row, expected):
    for f, v in expected.items():
        if f not in row or _json(row[f]) != _json(v):
            raise ValueError('site review source/context/coordinate drift: ' + f)
    for f in LIFECYCLE + MARKERS:
        if f not in expected and f in row:
            raise ValueError('site review unexpected lifecycle/evidence field: ' + f)


def _related(row, known):
    context = all(row.get(f, '') == known.get(f, '') for f in ('occasion', 'service_section', 'slot'))
    identity = row.get('identity_key') == known.get('identity_key')
    locator = bool(row.get('source_locator')) and row.get('source_locator') == known.get('source_locator')
    return identity and context or locator and (context or identity)


def _annotate(original, proof):
    from evidence_followup_repairs import _psalm_frame
    from metadata_followup_repairs import is_current
    spans = json.loads(original['spans_json'])
    if not is_current(original) or _psalm_frame(original, spans) != 'mt_nkjv':
        raise ValueError('site review annotation hold or lifecycle mismatch')
    row = copy.deepcopy(original)
    lxx = proof['brenton_covering_ref']
    row['canonical_lxx_ref'] = lxx
    row['display_ref'] = original['canonical_mt_ref'] + ' (Brenton covering locus ' + lxx + ')'
    for span in spans:
        span.update(canonical_lxx_ref=lxx, validation_basis='edition-qualified covering locus; manifest sha256='+MANIFEST_SHA256,
                    confidence='bounded_parallel_locus_not_exact_edition_equivalence')
    row['spans_json'] = json.dumps(spans, ensure_ascii=False, sort_keys=True)
    row['edition_psalm_covering_json'] = _json(proof)
    sources = json.loads(original['source_disclosure'])
    for source in sources:
        source['edition_psalm_covering'] = proof
    row['source_disclosure'] = _json(sources)
    return row


def _annotations(rows, date, inverse, frozen):
    definitions = frozen['reverse_annotations']
    by_key = {_proof_key(d['original']): d for d in definitions}
    originals = [d['original'] for d in definitions] if date is None else frozen['daily_annotations'].get(date, [])
    expected = {_key(old): (old, _annotate(old, by_key[_proof_key(old)]['proof'])) for old in originals}
    if originals:
        authenticate_sources()
    matches = {key: 0 for key in expected}
    preserved = frozen['reverse_preserved_related'] if date is None else frozen['daily_preserved_related'].get(date, [])
    result = []
    for row in rows:
        pair = expected.get(_key(row))
        if pair is None:
            retained = [r for r in preserved if _key(row) == _key(r)]
            if len(retained) == 1:
                _same(row, retained[0])
                result.append(copy.deepcopy(row))
                continue
            if row.get(MARKERS[0]) or 'edition_psalm_covering' in row.get('source_disclosure', '') or any(_related(row, d['original']) for d in definitions):
                # An unchanged witness from another source/date can share MT/identity;
                # only retained full context and locator recognize this layer.
                raise ValueError('site review annotation source/context rebound or wrong daily date')
            result.append(copy.deepcopy(row))
            continue
        key = _key(row)
        matches[key] += 1
        old, new = pair
        _same(row, new if inverse else old)
        output = copy.deepcopy(row)
        for f in ANNOTATION_FIELDS:
            source = old if inverse else new
            if f in source:
                output[f] = source[f]
            else:
                output.pop(f, None)
        result.append(output)
    if any(n != 1 for n in matches.values()):
        raise ValueError('site review annotation membership missing or duplicated')
    return result


def _water_rows(date, frozen):
    context = frozen['waters_dates'][date]
    result = []
    for ordinal, original in enumerate(frozen['waters_groups'][context], 1):
        from metadata_followup_repairs import is_current
        if not is_current(original):
            raise ValueError('site review waters inactive source')
        row = copy.deepcopy(original)
        proof = {'version': '1.3.11', 'date': date, 'source_context': context, 'source_ordinal': ordinal,
                 'source_locator': original['source_locator'], 'fresh_app_verification': False,
                 'authority_status_changed': False, 'basis': 'Complete existing current reverse group in authenticated npm 1.3.10; fixed feast-date materialization only'}
        row.update(service_section='Liturgy of Blessing of the Water', service_hour='', service_order=45,
                   slot_order=ordinal, display_label=('Theophany' if context == 'epiphany_laqan' else 'Apostles Feast')+' — Liturgy of the Waters',
                   source_group_key='waters|'+context+'|'+original['identity_key'], waters_materialization_json=_json(proof))
        disclosures = json.loads(row['source_disclosure'])
        for disclosure in disclosures:
            disclosure['waters_materialization'] = proof
        row['source_disclosure'] = _json(disclosures)
        result.append(row)
    return result


def _qualify_waters_reverse(rows, frozen):
    originals = [r for group in frozen['waters_groups'].values() for r in group]
    expected = {_key(r): r for r in originals}
    counts = {key: 0 for key in expected}
    locators = {r['source_locator'] for r in originals}
    identities = {r['identity_key'] for r in originals}
    contexts = {r['calendar_keys'] for r in originals}
    for row in rows:
        key = _key(row)
        if key in expected:
            try:
                _same(row, expected[key])
            except ValueError as exc:
                raise ValueError('site review waters reverse qualification: ' + str(exc)) from exc
            counts[key] += 1
        elif row.get('source_locator') in locators or (row.get('calendar_keys') in contexts and row.get('identity_key') in identities):
            raise ValueError('site review waters reverse source/context rebound')
    if any(n != 1 for n in counts.values()):
        raise ValueError('site review waters reverse membership missing or duplicated')


def _waters(rows, date, inverse, frozen):
    known = [r for group in frozen['waters_groups'].values() for r in group]
    signal = lambda r: bool(r.get(MARKERS[1])) or 'waters_materialization' in r.get('source_disclosure', '') or (
        r.get('occasion') == 'liturgy_of_the_waters' and r.get('service_section') == 'Liturgy of Blessing of the Water' and any(r.get('identity_key') == k['identity_key'] for k in known))
    if date not in frozen['waters_dates']:
        if any(signal(r) for r in rows):
            raise ValueError('site review waters wrong daily date')
        return copy.deepcopy(rows)
    authenticate_sources()
    original = _annotations(frozen['waters_daily_predecessors'][date], date, False, frozen)
    added = _water_rows(date, frozen)
    # Preserve every unrelated service and its sequence; insert the complete rite
    # before Liturgy, rather than alphabetizing prophetic books or reordering OT.
    pos = next((i for i,r in enumerate(original) if r.get('service_order', 0) > 45), len(original))
    successor = copy.deepcopy(original[:pos]) + added + copy.deepcopy(original[pos:])
    for i, row in enumerate(successor, 1):
        row['reading_order'] = i
    expected = successor if inverse else original
    if len(rows) != len(expected):
        raise ValueError('site review waters complete service membership mismatch')
    for row, target in zip(rows, expected):
        _same(row, target)
        if signal(target) and row.keys() != target.keys():
            raise ValueError('site review waters unexpected addition fields')
    if not inverse:
        return successor
    result = []
    for row, target in zip(rows, successor):
        if signal(target):
            continue
        restored = copy.deepcopy(row)
        restored['reading_order'] = original[len(result)]['reading_order']
        result.append(restored)
    return result


def project_rows(rows, *, date=None):
    frozen = baseline()
    if date is None:
        _qualify_waters_reverse(rows, frozen)
    if any(any(marker in row for marker in MARKERS) for row in rows):
        return project_rows(restore_rows(rows, date=date), date=date)
    result = _annotations(rows, date, False, frozen)
    return _waters(result, date, False, frozen) if date is not None else result


def restore_rows(rows, *, date=None):
    frozen = baseline()
    if date is None:
        _qualify_waters_reverse(rows, frozen)
    result = _waters(rows, date, True, frozen) if date is not None else rows
    return _annotations(result, date, True, frozen)
