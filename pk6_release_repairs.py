"""PK6 audit retirement, after PK2/PK11; no third current Reader appointment.

Historical source tables stay immutable. The inverse authenticates the exact
retirement/note and complete affected daily arrays before restoring prior views.
"""
import copy
import gzip
import json
import sqlite3
from functools import lru_cache
import revelation_release_repairs as shared

FIXTURE = 'sources/revelation-review-1.3.10/published-1.3.9-PK6-targets.json.gz'
FIXTURE_SHA256 = '92dfe0ff360c8a10b7771ec089d76a734b1585f0979202f83a8829354c48857a'
PROOF = 'sources/revelation-review-1.3.10/PK6-source-review.json'
PROOF_SHA256 = '337e30219dd476a21d7cc98734589efe1cb766acbc896d02866ec432555f35eb'
ERROR_ID = 'rid_51b705f0fe56936ed731'
JOEL_ID = 'rid_4bd7efb34bc72cf518de'


@lru_cache(maxsize=1)
def _decode_fixture(data):
    return json.loads(gzip.decompress(data))


def baseline():
    # Byte-keyed decode caching cannot bypass the fresh hash check.
    return _decode_fixture(shared._read(FIXTURE, FIXTURE_SHA256))


def authenticate():
    proof = json.loads(shared._read(PROOF, PROOF_SHA256))
    for path, digest in proof['files'].items():
        shared._read(path, digest)
    constructor = (shared.ROOT / 'sources/katameros-api/Core/Factories/Feasts/PaschaFriday.cs').read_text()
    reader = (shared.ROOT / proof['reader_omission']['source_path']).read_text().splitlines()
    if ('MakeOldTestament("29.2:1-3*@+29.2:10-11")' not in constructor
            or 'Jeremiah' not in reader[12] or 'Zechariah' not in reader[80]
            or reader[117].strip() != 'Introduction to the Paschal Praise'):
        raise ValueError('PK6 retained source context drift')
    db = shared.ROOT / 'sources/katameros-api/Core/KatamerosDatabase.db'
    with sqlite3.connect(db.as_uri() + '?mode=ro&immutable=1', uri=True) as connection:
        if connection.execute('select Id,Name from Books where Id in (28,29) order by Id').fetchall() != [(28, 'Hosea'), (29, 'Joel')]:
            raise ValueError('PK6 upstream book identity mismatch')
    return proof


def _expected(original, proof):
    result = copy.deepcopy(original)
    disposition = ('local_transcription_error_inactive_audit_witness' if original['identity_key'] == ERROR_ID
                   else 'historical_printed_joel_not_current_reader_appointment')
    disclosure = json.loads(original['source_disclosure'])
    for source in disclosure:
        source['historical_reference_review'] = {**proof, 'disposition': disposition,
                                                'source_review_path': PROOF, 'source_review_sha256': PROOF_SHA256}
    result['source_disclosure'] = shared._json(disclosure)
    if original['identity_key'] == ERROR_ID:
        result.update(active=False, status='removed', current_status='historical_witness',
                      removed_marker='removed_by_PK6_local_transcription_error_review',
                      removal_effective_version='1.3.10')
    return result


def _reverse(rows, inverse):
    originals = baseline()['reverse_rows']
    proof = authenticate()
    seen = set()
    output = []
    for row in rows:
        matches = [old for old in originals if row.get('identity_key') == old['identity_key']
                   or row.get('source_locator') == old['source_locator']]
        if not matches:
            if 'historical_reference_review' in row.get('source_disclosure', ''):
                raise ValueError('PK6 source note attached to an unqualified context')
            output.append(copy.deepcopy(row))
            continue
        if len(matches) != 1 or matches[0]['identity_key'] in seen:
            raise ValueError('PK6 reverse membership duplicated or ambiguous')
        old = matches[0]
        seen.add(old['identity_key'])
        expected = _expected(old, proof)
        before, after = (expected, old) if inverse else (old, expected)
        if not inverse and row.get('source_disclosure') == expected['source_disclosure']:
            shared._check(row, expected)
            output.append(copy.deepcopy(row))
        else:
            shared._check(row, before)
            output.append(shared._rewrite(row, before, after))
    if seen != {ERROR_ID, JOEL_ID}:
        raise ValueError('PK6 reverse membership incomplete')
    return output


def project_reverse(rows):
    return _reverse(rows, False)


def restore_reverse(rows):
    return _reverse(rows, True)


def _daily(rows, date, inverse):
    frozen = baseline()['daily']
    if date not in frozen:
        if any(r.get('identity_key') in (ERROR_ID, JOEL_ID)
               or 'historical_reference_review' in r.get('source_disclosure', '') for r in rows):
            raise ValueError('PK6 appointment/note rebound to wrong daily date')
        return copy.deepcopy(rows)
    authenticate()
    originals = frozen[date]
    kept = [r for r in originals if r['identity_key'] != ERROR_ID]
    expected = [dict(r, reading_order=i) for i, r in enumerate(kept, 1)]
    if not inverse and len(rows) == len(expected):
        # Explicit replay control, not an authenticity oracle for new data.
        restored = restore_daily(rows, date)
        return _daily(restored, date, False)
    before = expected if inverse else originals
    if len(rows) != len(before):
        raise ValueError('PK6 complete daily membership drift')
    for row, original in zip(rows, before):
        shared._check(row, original)
    if inverse:
        result = []
        supplied = iter(rows)
        for old in originals:
            if old['identity_key'] == ERROR_ID:
                result.append(copy.deepcopy(old))
            else:
                row = copy.deepcopy(next(supplied))
                row['reading_order'] = old['reading_order']
                result.append(row)
        return result
    return [dict(row, reading_order=i) for i, row in enumerate(
        (r for r in rows if r['identity_key'] != ERROR_ID), 1)]


def project_daily(rows, date):
    return _daily(rows, date, False)


def restore_daily(rows, date):
    return _daily(rows, date, True)
