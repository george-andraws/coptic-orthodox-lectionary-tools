"""Bounded 1.3.10 outer projection; historical source contracts stay immutable.

Runs after the existing public follow-up/occurrence layers. Its authenticated
inverse runs BEFORE those layers' inverses, preserving foreign fields for their
own guards. No source table, historical membership oracle or recurrence changes.
"""
import copy
import gzip
import hashlib
import json
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parent
FIXTURE = 'sources/revelation-review-1.3.10/published-1.3.9-release-targets.json.gz'
FIXTURE_SHA256 = 'b78701c0262b49da8f8d31011c5fc760e333f58431edb31f34439f2e7871eca8'
OLD_ID = 'rid_8ae616e6b96572e37bd9'
NEW_REF = 'Deut 32:1-43'
NEW_ID = 'rid_' + hashlib.sha256(('scripture|' + NEW_REF + '|' + NEW_REF).encode()).hexdigest()[:20]
CAPTURE = 'sources/coptic-reader/psalmody-qualified-2026-10-25/bright-saturday-midnight-praises.full.txt'
CAPTURE_SHA256 = '3c858d0729c37fc420e08fb362967edf59d4316855d92840b9f4b4be4ede2d45'
CONTEXT = ('occasion', 'service_section', 'service_hour', 'slot', 'calendar_keys')
LIFECYCLE = ('active', 'status', 'state', 'include_in_current_index', 'removal_effective_version')


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _read(relative, digest):
    path = ROOT / relative
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('PK source path escape')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError('PK source authentication failed: ' + relative)
    return data


@lru_cache(maxsize=1)
def _decode_fixture(data):
    return json.loads(gzip.decompress(data))


def baseline():
    # Cache decoding only; every call still reads and authenticates source bytes.
    return _decode_fixture(_read(FIXTURE, FIXTURE_SHA256))


def authenticate_endpoint():
    """Heading AND numbered last verse, not a guessed biblical chapter end."""
    lines = _read(CAPTURE, CAPTURE_SHA256).decode().splitlines()
    if (lines[0] != 'Midnight Praises'
            or lines[198] != '\tSecond Praise of Moses the Prophet (Deuteronomy 32:1-43)'
            or lines[286] != '43 “Rejoice, O Gentiles, with His people; For He will avenge the blood of His servants, And render vengeance to His adversaries; He will provide atonement for His land and His people.”'
            or not lines[290].startswith('\tThe Prayer of Hannah, Mother of Samuel')):
        raise ValueError('PK2 retained heading/body boundary mismatch')
    return {'request': 'PK2', 'version': '1.3.10', 'source_path': CAPTURE,
            'source_sha256': CAPTURE_SHA256, 'heading_line': 199,
            'last_verse_line': 287, 'printed_ref': 'Deuteronomy 32:1-43',
            'prior_ref': 'Deut 32:1-42', 'fresh_app_verification': False,
            'recurrence': 'unchanged predecessor Bright Saturday 2026..2028',
            'qualification': 'retained English service endpoint; not exact cross-edition text equivalence'}


def _variants(original, date, proof):
    if original['identity_key'] != OLD_ID:
        new = copy.deepcopy(original)
        new['display_ref'] = original['display_ref'].split(' (Reader')[0]
        if new['display_ref'] == original['display_ref']:
            raise ValueError('PK11 unexpected retained display format')
        disclosures = json.loads(original['source_disclosure'])
        for source in disclosures:
            source['display_reference_review'] = {'request': 'PK11', 'version': '1.3.10',
                'raw_display_ref': original['display_ref'], 'display_ref': new['display_ref'],
                'canonical_alignment': 'unchanged_hold'}
        new['source_disclosure'] = _json(disclosures)
        return [new]
    new = copy.deepcopy(original)
    new.update(identity_key=NEW_ID, display_ref=NEW_REF, canonical_mt_ref=NEW_REF,
               canonical_lxx_ref=NEW_REF, current_status='current_confirmed_coptic_reader',
               source_locator=original['source_locator'] + '; corrected_endpoint_source=' + CAPTURE + ':199-290; sha256=' + CAPTURE_SHA256)
    spans = json.loads(original['spans_json'])
    for span in spans:
        span.update(source_ref=NEW_REF, canonical_mt_ref=NEW_REF, canonical_lxx_ref=NEW_REF, verse_end=43)
    new['spans_json'] = json.dumps(spans, ensure_ascii=False, sort_keys=True)
    disclosures = json.loads(original['source_disclosure'])
    for source in disclosures:
        source['endpoint_review'] = proof
    new['source_disclosure'] = _json(disclosures)
    if date is not None:
        return [new]
    # Preserve the prior source's entire coordinate/disclosure witness, including
    # its original current_status. Public current selection is false via removal.
    retired = copy.deepcopy(original)
    retired.update(active=False, status='removed', removed_marker='removed_by_PK2_endpoint_review',
                   removal_effective_version='1.3.10', superseded_by_ref=NEW_REF,
                   superseded_by_identity_key=NEW_ID)
    new.update(provenance='Source-derived Bright Saturday endpoint correction from retained Coptic Reader',
               source_title='Bright Saturday source-derived endpoint correction (retained Coptic Reader)',
               source_edition='Retained English service endpoint; not fresh app verification or exact cross-edition text equivalence')
    return [retired, new]


def _check(row, expected):
    for field, value in expected.items():
        if field not in row or _json(row[field]) != _json(value):
            raise ValueError('PK source/context/coordinate drift: ' + field)
    for field in LIFECYCLE:
        if field not in expected and field in row:
            raise ValueError('PK unexpected lifecycle field: ' + field)


def _rewrite(row, before, after):
    result = copy.deepcopy(row)
    for field in set(before) | set(after):
        if field not in after:
            result.pop(field, None)
        elif field not in before or _json(before[field]) != _json(after[field]):
            result[field] = copy.deepcopy(after[field])
    return result


def _related(row, known):
    same_context = all(row.get(f, '') == known.get(f, '') for f in CONTEXT)
    same_id = row.get('identity_key') == known.get('identity_key')
    same_locator = row.get('source_locator') == known.get('source_locator')
    # A family/kind or disclosure is not an authorization token. Identity plus
    # service catches compound stripping; locator plus context catches id swaps.
    return same_id and (same_context or same_locator) or same_locator and same_context


def _transform(rows, date, inverse):
    frozen = baseline()
    proof = authenticate_endpoint()  # Re-read authenticated source on every call.
    originals = frozen['reverse_rows'] if date is None else frozen['daily'].get(date, [])
    pairs = [(original, _variants(original, date, proof)) for original in originals]
    all_known = list(frozen['reverse_rows']) + [r for values in frozen['daily'].values() for r in values]
    all_known += [v for original in frozen['reverse_rows'] if original['identity_key'] == OLD_ID
                  for v in _variants(original, None, proof)]
    matches = [[] for _ in pairs]
    output = []
    for row in rows:
        candidates = [i for i, (old, variants) in enumerate(pairs)
                      if any(_related(row, known) for known in [old] + variants)]
        if len(candidates) > 1:
            raise ValueError('PK ambiguous source context')
        if not candidates:
            if (any(_related(row, known) for known in all_known)
                    or 'display_reference_review' in row.get('source_disclosure', '')
                    or 'endpoint_review' in row.get('source_disclosure', '')):
                raise ValueError('PK source/context rebound or wrong daily date')
            output.append(copy.deepcopy(row))
            continue
        i = candidates[0]
        old, variants = pairs[i]
        matches[i].append((len(output), row))
        if inverse:
            # The complete group is checked below; preserve its original position.
            output.append(None)
        else:
            # A complete already-projected table must authenticate before replay.
            if row.get('display_ref') != old['display_ref'] or row.get('removed_marker') != old.get('removed_marker'):
                return _project_replay(rows, date)
            _check(row, old)
            output.extend(_rewrite(row, old, v) for v in variants)
    for (old, variants), group in zip(pairs, matches):
        expected_count = len(variants) if inverse else 1
        if len(group) != expected_count:
            raise ValueError('PK target membership missing or duplicated')
        if inverse:
            # Exact source-backed successor and retirement, not candidate replay.
            for (_, row), expected in zip(group, variants):
                _check(row, expected)
            restored = _rewrite(group[0][1], variants[0], old)
            for (_, row), expected in zip(group[1:], variants[1:]):
                for key in row.keys() - expected.keys():
                    if key in restored and _json(restored[key]) != _json(row[key]):
                        raise ValueError('PK conflicting foreign fields')
                    restored[key] = copy.deepcopy(row[key])
            output[group[0][0]] = restored
    return [row for row in output if row is not None]


def _project_replay(rows, date):
    restored = restore_rows(rows, date=date)
    return _transform(restored, date, False)


def project_rows(rows, *, date=None):
    return _transform(rows, date, False)


def restore_rows(rows, *, date=None):
    return _transform(rows, date, True)
