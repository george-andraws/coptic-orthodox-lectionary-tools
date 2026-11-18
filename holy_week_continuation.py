"""1.3.12 outer Holy Week successor; historical contracts remain immutable.

Only the independently reviewed recurring proper is changed. Wrong-night working
witnesses stay in reverse history. No Jeremiah/Psalm coordinates are approved.
The exact inverse authenticates owned cells before older production guards run.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = 'sources/holy-week-continuation-1.3.12/'
MARKER = 'holy_week_continuation_json'
EVE_DATES = ('2026-04-08', '2027-04-28', '2028-04-12')
FRIDAY_DATES = ('2026-04-10', '2027-04-30', '2028-04-14')
DATES = EVE_DATES + FRIDAY_DATES
NEW_ID = 'rid_5e19e735d67290e758ed'
HOLD = 'held_wrong_context_holy_week_1.3.12'
PINS = {
    'tests/fixtures/holy-week-continuation-published-1.3.11.json.gz': '8f0f938699ea7073beaee0ac70708e04fbbc9bb9ad875e1f66c42b85a31e8b25',
    SOURCE+'source-plan-receipt.json': '1945e180cadea178cfb67d1b46e86862a4b8322ee434d449cc9b562dd5c9febc',
    SOURCE+'capture-receipt.json': '1d2cb394d9fd0a1ba2f59730affd13213582d55efec8991cea7b9034bf3221f9',
    'sources/coptic-reader/pascha-resolution-qualified-2026-10-25/fresh-pascha/friday--12th-hour.txt': '9a6bd0b11b67fa6d3cfbe10a99b84a085796b8b3e886ddec4d191ef02dbe2e0e',
    'sources/katameros-api/Core/Factories/Feasts/PaschaWednesday.cs': 'd20d188c35ccd3321bda95d06051ab42d0fa373dad0417f13b7cf150c5fb53fc',
    'sources/katameros-api/Core/Factories/Feasts/PaschaFriday.cs': '8d0b0ebe09ea8b4fbcc4fbb0d395bead0b1468c44d2ffc8876d3800c76dbf164',
    'sources/katameros-api/Core/Factories/FeastsFactory.cs': 'ca78d610bb1d7c5463432c5c4947f29f01dd71f738d867ebafd171e00781ea50',
    'out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt': 'd37ef1df5ff9e5caadfe77a2b45a6e21b66bf69005715c93ed11e7004f1c872d',
}
REVERSE_FIXTURE = 'tests/fixtures/holy-week-continuation-reverse-1.3.11.jsonl.gz'
REVERSE_SHA256 = '0f69b27574f82354e6e0fbac895c55855ae2bd8d9eefb90df9f0d8902ea0849f'
TWELFTH = {'Matt 27:57-61': (1, 182), 'Mark 15:42-16:1': (2, 232),
           'Lk 23:50-56': (3, 272), 'Jn 19:38-42': (4, 312)}
KEY = ('identity_key', 'source_family', 'source_kind', 'occasion', 'service_section', 'service_hour', 'slot')


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _read(path, digest):
    p = ROOT / path
    raw = p.read_bytes()
    if p.is_symlink() or not p.resolve().is_relative_to(ROOT.resolve()) or hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('Holy Week continuation source authentication failed: '+path)
    return raw


@lru_cache(maxsize=2)
def _decode(raw):
    return json.loads(gzip.decompress(raw))


def predecessor():
    path = next(iter(PINS))
    return _decode(_read(path, PINS[path]))


def published_reverse():
    return [json.loads(line) for line in gzip.decompress(_read(REVERSE_FIXTURE, REVERSE_SHA256)).splitlines()]


def authenticate():
    for path, digest in PINS.items():
        _read(path, digest)


def _key(row):
    return tuple(row.get(f, '') for f in KEY)


def _proof(kind, ref, line, date=None):
    eve = kind != 'burial_gospel_qualification'
    path = SOURCE+'capture-receipt.json' if eve else list(PINS)[3]
    proof = dict(version='1.3.12', kind=kind, source_path=path, source_sha256=PINS[path],
                heading_line=line, printed_reference=ref, eligible_dates=list(EVE_DATES if eve else FRIDAY_DATES),
                recurring_proper=True, capture_selected_year=None if eve else 2026,
                capture_context='generic Pascha menu; not selected-date attestations' if eve else 'selected 2026 Great Friday capture; recurring proper applied in shipped years',
                fresh_app_verification=False, date=date,
                qualification='Gospel only; Jeremiah 8:4-10 heading/body endpoint and Psalm 61:4,1 coordinate alignment remain held' if eve else 'Exact existing Gospel endpoints; retained Reader body and source order; no Jonah activation or Psalm alignment approval')
    if eve:
        # The public pin authenticates a factual receipt, not unavailable archive bytes.
        proof.update(evidence_kind='factual_capture_receipt',
                     archived_source_sha256='10d981e8fa068a4b49a7227f62955a3a26f1efbc785f514cb274277fc5434443',
                     archived_source_publicly_distributed=False)
    return proof


def _disclose(row, proof, source=None):
    row = copy.deepcopy(row)
    row[MARKER] = _json(proof)
    sources = json.loads(row['source_disclosure'])
    if source is not None:
        sources.append(source)
    # Preserve complete original disclosure objects; attach new approval separately.
    row['source_disclosure'] = _json(sources)
    row['source_disclosure_count'] = str(len(sources))
    return row


def _source(proof):
    receipt = proof.get('evidence_kind') == 'factual_capture_receipt'
    locator = (proof['source_path']+'#/readings/2; receipt sha256='+proof['source_sha256']+
               '; archived heading line '+str(proof['heading_line'])+'; archived sha256='+proof['archived_source_sha256']+
               '; full capture retained locally, not publicly distributed') if receipt else (
                   proof['source_path']+':line '+str(proof['heading_line'])+'; sha256='+proof['source_sha256'])
    return dict(source_family='coptic_reader_source_derived_holy_week_continuation',
                source_kind='pascha_day_hour', source_title='Retained Coptic Reader recurring Pascha proper',
                source_edition='Retained English service; generic-menu versus selected-2026 capture explicitly qualified',
                source_locator=locator,
                holy_week_continuation=proof)


def _hold(row):
    proof = _proof('wrong_night_working_witness_hold', row['canonical_mt_ref'], 124)
    proof['qualification'] = 'Wrong-night curated transcription, not a Reader appointment here. Original witness cells retained; no universal historical removal or removal date asserted.'
    row = _disclose(row, proof)
    row.update(current_status='pending_coptic_reader_review', active=False, removed_marker=HOLD)
    return row


def _qualify(row, date=None):
    ref = row['canonical_mt_ref']
    ordinal, line = TWELFTH[ref]
    proof = _proof('burial_gospel_qualification', ref, line, date)
    proof['source_ordinal'] = ordinal
    row = _disclose(row, proof, _source(proof))
    row.update(current_status='current_confirmed_coptic_reader')
    # Original SQLite witness source fields/ordinals are preserved, not relabeled.
    return row


def _new(row, date=None):
    proof = _proof('eve_of_thursday_gospel_replacement', 'John 12:44-50', 124, date)
    row = copy.deepcopy(row)
    source = _source(proof)
    row.update(identity_key=NEW_ID, canonical_mt_ref='Jn 12:44-50', canonical_lxx_ref='Jn 12:44-50',
               display_ref='Jn 12:44-50', current_status='current_confirmed_coptic_reader', removed_marker='',
               source_disclosure='[]', source_disclosure_count='0', **{k:v for k,v in source.items() if k != 'holy_week_continuation'})
    # Do not inherit the erroneous curated provenance or its named source edition.
    if 'provenance' in row:
        row['provenance'] = 'Retained Reader named recurring proper; generic-menu capture, not dated 2027/2028 attestations'
    if 'authority_tier' in row:
        row['authority_tier'] = 'primary_reader_source'
    span = dict(book='Jn', chapter_start=12, chapter_end=12, verse_start=44, verse_end=50,
                source_ref='John 12:44-50', source_convention='modern_english_reference',
                canonical_mt_ref='Jn 12:44-50', canonical_lxx_ref='Jn 12:44-50', confidence='source_qualified',
                validation_basis='Factual capture receipt records original independent review of retained heading and selected Gospel body, archived lines 147-164; full capture retained locally, not publicly distributed')
    row['spans_json'] = _json([span])
    return _disclose(row, proof, source)


def _reverse_pair():
    before = predecessor()['reverse']
    after = [_hold(r) if r['occasion']=='Wednesday Eve' else _qualify(r) for r in before]
    template = next(r for r in before if r['occasion']=='Wednesday Eve' and r['slot']=='Gospel')
    return before, after+[_new(template)]


def _recognize(row):
    # Identity+context recognition survives stripped markers and lifecycle forgery.
    return (MARKER in row or 'holy_week_continuation' in row.get('source_disclosure', '')
            or row.get('source_family')=='coptic_reader_source_derived_holy_week_continuation'
            or row.get('identity_key')==NEW_ID and row.get('occasion')=='Wednesday Eve' and row.get('service_hour')=='Eleventh Hour')


def _same(actual, expected):
    if _json(actual) != _json(expected):
        raise ValueError('Holy Week continuation complete source/context/lifecycle/coordinate drift')


def project_reverse(rows):
    authenticate()
    if any(_recognize(r) for r in rows):
        return project_reverse(restore_reverse(rows))
    before, after = _reverse_pair()
    keys = {_key(r) for r in before}
    owned = [r for r in rows if _key(r) in keys]
    _same(owned, before)
    replacements = {_key(a): b for a,b in zip(before, after)}
    result = [copy.deepcopy(replacements.get(_key(r), r)) for r in rows]+[copy.deepcopy(after[-1])]
    verify_membership(result)
    return result


def restore_reverse(rows):
    authenticate()
    before, after = _reverse_pair()
    keys = {_key(r) for r in before+after}
    owned = [r for r in rows if _key(r) in keys or _recognize(r)]
    _same(owned, after)
    replacements = {_key(b): a for a,b in zip(before, after)}
    return [copy.deepcopy(replacements.get(_key(r), r)) for r in rows if _key(r) != _key(after[-1])]


def verify_membership(rows):
    # One literal source-approved addition, zero removals. Lifecycle/coordinates
    # qualify first; then the unchanged predecessor production multiset guard.
    import final_site_review_repairs as earlier
    restored = restore_reverse(rows)
    result = earlier.verify_successor_membership(restored)
    return dict(row_count=result['row_count']+1, predecessor_rows=result['row_count'], additions=1, removals=0)


def _ordered(rows):
    from good_friday_order_review import TABLES
    original = rows
    rows = copy.deepcopy(rows)
    for hour, refs in TABLES.items():
        positions = [i for i,r in enumerate(rows) if r.get('occasion')=='Good Friday' and r['service_hour']==hour and r['slot']=='Gospel']
        for i, ref in zip(positions, refs):
            rows[i] = copy.deepcopy(next(r for r in original if r['service_hour']==hour and r['canonical_mt_ref']==ref))
    for i,r in enumerate(rows,1):
        r['reading_order'] = i
    return rows


def _daily_pair(date):
    before = predecessor()['daily'][date]
    after = []
    for row in before:
        if date in EVE_DATES and row.get('pascha_service')=='eve_of_thursday' and row['service_hour']=='Eleventh Hour':
            if row['slot']=='Gospel':
                after.append(_new(row, date))
        elif date in FRIDAY_DATES and row.get('occasion')=='Good Friday' and row['service_hour']=='Twelfth Hour' and row['slot']=='Gospel':
            after.append(_qualify(row, date))
        else:
            after.append(copy.deepcopy(row))
    if date in FRIDAY_DATES:
        after = _ordered(after)
    for i,r in enumerate(after,1):
        r['reading_order'] = i
    return before, after


def project_daily(rows, date):
    if date not in DATES:
        if any(_recognize(r) for r in rows):
            raise ValueError('Holy Week continuation wrong daily date')
        return copy.deepcopy(rows)
    authenticate()
    before, after = _daily_pair(date)
    if any(_recognize(r) for r in rows):
        _same(rows, after)
    else:
        # Both allowed input sequences have identical published cells and only
        # the previously approved complete Gospel permutation differs.
        from good_friday_order_review import restore_daily_order
        normalized = restore_daily_order(rows, date) if date in FRIDAY_DATES else rows
        _same(normalized, before)
    return after


def restore_daily(rows, date):
    if date not in DATES:
        if any(_recognize(r) for r in rows):
            raise ValueError('Holy Week continuation wrong daily date')
        return copy.deepcopy(rows)
    authenticate()
    before, after = _daily_pair(date)
    _same(rows, after)
    # Restore the immediately preceding ordering layer, not its older input.
    return _ordered(before) if date in FRIDAY_DATES else copy.deepcopy(before)
