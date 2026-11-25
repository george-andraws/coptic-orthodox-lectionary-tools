"""Reader-priority 1.3.13 outer projection with an exact authenticated inverse.

The unchanged 1.3.12 witness corpus is the predecessor, not a new authority.
Factual receipts preserve private-capture identities without distributing bodies.
Current appointments, inactive transcriptions and edition annotations are distinct.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = 'sources/jeremiah-followup-1.3.13/source-facts.json'
FIXTURE = 'tests/fixtures/jeremiah-published-1.3.12.json.gz'
MARKER = 'jeremiah_followup_json'
PINS = {
    SOURCE: 'de85c7763eb0f0b221c30f8423152eb8ac210fa48a98d07e047ed43b6614d465',
    'sources/coptic-reader/holy-week-review-qualified-2026-10-29/thursday--thursday-day--6th-hour.txt': '4318fbbce5db75e4033b7f56f9487be2b4d9ffa051dfea33d78051984add367e',
    'sources/coptic-reader/holy-week-review-qualified-2026-10-29/friday--11th-hour.txt': '32e1cab53d275e25ff1b574c5bdaa624a95fecc935f19c38ef69f64835816d1b',
    FIXTURE: '51459e51f14f3a6593acd3c43e45ce0db6d35e0fd61b73afaeadfa334a6e16a6',
    'sources/katameros-api/Core/Factories/Feasts/PaschaThursday.cs': '415378944739bcaa0484498b7ea905543de33a17031582d68de9f87a2224620a',
    'sources/katameros-api/Core/Factories/Feasts/PaschaFriday.cs': '8d0b0ebe09ea8b4fbcc4fbb0d395bead0b1468c44d2ffc8876d3800c76dbf164',
    'out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt': 'd37ef1df5ff9e5caadfe77a2b45a6e21b66bf69005715c93ed11e7004f1c872d',
    'sources/site-review-1.3.11/bible/Brenton-040.html': '48f2925441729bc0fc0268c71aed38d0f1ef0d4b340f4e02b0ca936c014ce06d',
    'sources/site-review-1.3.11/bible/NKJV-041.html': '3df9b56dcb51004af89cbe8e67db6a93818ab4669ebde20a9f9cccf70beed85f',
}
# Literal independently traced constructor/Reader deltas, not candidate-derived.
RULES = {
    'rid_0946df3427160b8ebe38': ('Exod 12:1-14', '2.12:1-14', 80, 'Exod 12:1-14', 'reader_good_friday_eleventh'),
    'rid_2f2ca45446d156914dd8': ('Lev 23:5-12', '3.23:5-12', 81, None, 'reader_good_friday_eleventh'),
    'rid_f231e32d73929615cd22': ('Jer 7:2-15', '24.7:2-15', 51, 'Jer 7:1-15', 'reader_great_thursday_sixth'),
    'rid_96f759a6c378438099f0': ('Sir 12:13-13:1', '73.12:13-13:1', 53, 'Sir 12:13-13:1', 'reader_great_thursday_sixth'),
    'rid_6d48106270b82e0e3bd4': (None, '24.9:6-10', 107, 'Jer 9:7-11', 'reader_eve_friday_ninth'),
}
OTTAWA_JER = 'rid_000333f2b55f4f89b928'
OTTAWA_SIR = 'rid_95b8bc94505475351957'
PSALM = 'rid_fa44089aa2993cc17312'


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _read(path):
    p = ROOT / path
    raw = p.read_bytes()
    if p.is_symlink() or not p.resolve().is_relative_to(ROOT.resolve()) or hashlib.sha256(raw).hexdigest() != PINS[path]:
        raise ValueError('Jeremiah follow-up source authentication failed: '+path)
    return raw


def authenticate():
    for path in PINS:
        _read(path)


@lru_cache(maxsize=1)
def _baseline(raw):
    return json.loads(gzip.decompress(raw))


def predecessor():
    return _baseline(_read(FIXTURE))


def _proof(kind, **fields):
    return dict(version='1.3.13', kind=kind, source_path=SOURCE, source_sha256=PINS[SOURCE],
                evidence_kind='factual_receipt_not_public_service_body', fresh_app_verification=False,
                **fields)


def _attach(original, proof, source=None):
    row = copy.deepcopy(original)
    row[MARKER] = _json(proof)
    disclosures = json.loads(row['source_disclosure'])
    # Preserve original source witnesses verbatim; new qualification is separate.
    if source is None:
        source = dict(source_family='jeremiah_followup_qualification', source_kind='factual_source_receipt',
                      source_title='Jeremiah source/edition qualification', source_edition='Named source only',
                      source_locator=SOURCE, jeremiah_followup=proof)
    disclosures.append(source)
    row['source_disclosure'] = _json(disclosures)
    row['source_disclosure_count'] = str(len(disclosures))
    return row


def _hold(row):
    api, literal, line, reader, capture = RULES[row['identity_key']]
    proof = _proof('inactive_original_transcription', original_ref=row['canonical_mt_ref'],
                   api_literal=literal, corrected_api_ref=api, reader_ref=reader,
                   qualification='Preserved source witness, not a current Reader appointment; no historical removal date asserted')
    result = _attach(row, proof)
    result.update(active=False, current_status='historical_witness', removed_marker='inactive_original_jeremiah_1.3.13')
    return result


def _span(ref, lxx, convention):
    m = re.fullmatch(r'(\w+) (\d+):(\d+)-(?:([0-9]+):)?([0-9]+)', ref)
    if m is None:
        raise ValueError('Unsupported literal Jeremiah appointment')
    book, ch, start, endch, end = m.groups()
    return dict(book=book, chapter_start=int(ch), chapter_end=int(endch or ch),
                verse_start=int(start), verse_end=int(end), source_ref=ref, source_convention=convention,
                canonical_mt_ref=ref, canonical_lxx_ref=lxx, confidence='source_qualified',
                validation_basis='Literal source appointment; edition-specific qualifications in '+MARKER)


def _new(original, *, api=False):
    corrected, literal, line, reader, capture = RULES[original['identity_key']]
    ref = corrected if api else reader
    if ref is None:
        raise ValueError('No authorized appointment for this source')
    row = copy.deepcopy(original)
    kind = 'inactive_corrected_api_witness' if api else 'reader_current_appointment'
    lxx = 'Jer 9:6-10' if not api and capture == 'reader_eve_friday_ninth' else ref
    proof = _proof(kind, predecessor_identity=original['identity_key'], source_ref=ref,
                   api_literal=literal, reader_printed=reader, active=not api,
                   qualification='API literal preserved separately; Reader controls current selection. Printed labels are not a general cross-edition equivalence map.')
    path = 'sources/katameros-api/Core/Factories/Feasts/Pascha'+('Friday' if original['occasion']=='Good Friday' else 'Thursday')+'.cs'
    facts = json.loads(_read(SOURCE))
    if api:
        locator = path+':line '+str(line)+'; source_literal='+literal
        family, title, edition = 'katameros_api_jeremiah_variant', 'Corrected Katameros API transcription (inactive)', 'Literal API constructor; edition alignment not universally certified'
    else:
        c = facts['captures'][capture]
        proof.update(capture=capture, archived_sha256=c['archived_sha256'],
                     archived_body_publicly_distributed=False, recurring_proper=True,
                     attestation='Retained named service, not fresh shipped-year observations')
        locator = SOURCE+'#/captures/'+capture+'; archived sha256='+c['archived_sha256']+'; full capture retained privately'
        family, title, edition = 'coptic_reader_jeremiah_followup', 'Retained Coptic Reader Holy Pascha appointment', 'Reader printed English label; named Brenton alignment only where explicitly qualified'
    identity = 'rid_'+hashlib.sha256((kind+'|'+original['identity_key']+'|'+ref).encode()).hexdigest()[:20]
    source = dict(source_family=family, source_kind='pascha_day_hour', source_title=title,
                  source_edition=edition, source_locator=locator, jeremiah_followup=proof)
    row.update(identity_key=identity, canonical_mt_ref=ref, canonical_lxx_ref=lxx, display_ref=ref,
               current_status='historical_witness' if api else 'current_confirmed_coptic_reader',
               active=not api, removed_marker='inactive_api_variant_1.3.13' if api else '',
               source_disclosure='[]', source_disclosure_count='0',
               **{k:v for k,v in source.items() if k != 'jeremiah_followup'})
    if 'provenance' in row:
        row['provenance'] = 'Source-qualified API transcription retained inactive' if api else 'Reader-priority named Holy Pascha recurring proper; retained capture, not new yearly attestation'
    if 'authority_tier' in row:
        row['authority_tier'] = 'working_local_source' if api else 'primary_reader_source'
    if not api and capture == 'reader_eve_friday_ninth':
        row['display_ref'] = ref+' (Brenton '+lxx+')'
    row['spans_json'] = _json([_span(ref, lxx, 'api_literal_reference' if api else 'modern_english_reference')])
    return _attach(row, proof, source)


def _annotate(row):
    identity = row['identity_key']
    if identity == OTTAWA_JER and row.get('source_family') == 'holy_pascha' and row.get('source_kind') == 'pascha_source_text' and row.get('occasion') == 'Great Thursday Eve':
        proof = _proof('ottawa_historical_service_and_edition', printed_reference='Jer 9:7-11',
                       brenton='Jer 9:6-10', printed_page=511, active=False,
                       qualification='Ottawa heading explicitly Eve of Good Friday; historical witness remains inactive')
        out = _attach(row, proof)
        out.update(pascha_service='eve_of_friday', pascha_offset_days=-3,
                   display_occasion='Eve of Friday', display_label='Eve of Good Friday', canonical_lxx_ref='Jer 9:6-10')
        spans = json.loads(out['spans_json'])
        for span in spans:
            span['canonical_lxx_ref'] = 'Jer 9:6-10'
            span['validation_basis'] = 'Named Brenton counterpart; Ottawa printed reference retained'
        out['spans_json'] = _json(spans)
        return out
    if identity == OTTAWA_SIR and row.get('source_family') == 'holy_pascha' and row.get('source_kind') == 'pascha_source_text' and row.get('occasion') == 'Great Thursday':
        return _attach(row, _proof('ottawa_printed_heading_body_discrepancy', printed_reference='Sir 23:7-14',
                                  body_counterpart='Sir 12:13-13:1', printed_page=401, active=False,
                                  qualification='Sixth Hour of Great Thursday unchanged; printed heading preserved, not a new current appointment'))
    if identity == PSALM:
        proof = _proof('named_brenton_covering_annotation', canonical_mt_ref='Ps 41:5,41:10',
                       brenton_covering_ref='Ps 40:6; Ps 40:11', source_order='Psalm 41:10, 5',
                       brenton_source_order='Ps 40:11; Ps 40:6',
                       qualification='Named English Brenton covering loci, not universal whole-verse LXX equivalence')
        out = _attach(row, proof)
        out.update(canonical_lxx_ref='Ps 40:6; Ps 40:11',
                   display_ref='Ps 41:5,41:10 (Brenton covering locus Ps 40:6; Ps 40:11)',
                   edition_psalm_covering_json=_json(proof))
        spans = json.loads(out['spans_json'])
        for span in spans:
            span.update(canonical_lxx_ref=out['canonical_lxx_ref'],
                        validation_basis='Named Brenton covering locus; source order retained separately',
                        confidence='bounded_parallel_locus_not_exact_edition_equivalence')
        out['spans_json'] = _json(spans)
        return out
    return copy.deepcopy(row)


def _expected_reverse():
    before = predecessor()['reverse']
    # Add the four corrected API witnesses and four current Reader appointments
    # at the former working row's physical location, retaining all originals.
    result = []
    for row in before:
        identity = row['identity_key']
        if identity in RULES:
            result.append(_hold(row))
            if RULES[identity][0] is not None:
                result.append(_new(row, api=True))
            if RULES[identity][3] is not None:
                result.append(_new(row))
        else:
            result.append(_annotate(row))
    return result


def _same(actual, expected):
    if _json(actual) != _json(expected):
        raise ValueError('Jeremiah follow-up complete source/context/lifecycle/coordinate/order drift')


def project_reverse(rows):
    authenticate()
    before, after = predecessor()['reverse'], _expected_reverse()
    if _json(rows) != _json(before):
        _same(rows, after)
    return copy.deepcopy(after)


def restore_reverse(rows):
    authenticate()
    _same(rows, _expected_reverse())
    return copy.deepcopy(predecessor()['reverse'])


def verify_membership(rows):
    restore_reverse(rows)
    return dict(row_count=12308, predecessor_rows=12300, additions=8, removals=0)


def _before_day(date):
    return predecessor()['daily'].get(date[:4], {}).get(date)


def _expected_day(date):
    result = []
    for row in _before_day(date):
        identity = row['identity_key']
        if identity in RULES:
            if RULES[identity][3] is not None:
                result.append(_new(row))
        else:
            result.append(_annotate(row))
    for ordinal, row in enumerate(result, 1):
        row['reading_order'] = ordinal
    return result


def _recognized(row):
    added_ids = {'rid_'+hashlib.sha256((kind+'|'+identity+'|'+ref).encode()).hexdigest()[:20]
                 for identity, rule in RULES.items()
                 for kind, ref in [('inactive_corrected_api_witness', rule[0]), ('reader_current_appointment', rule[3])]
                 if ref is not None}
    original_context = row.get('identity_key') in set(RULES) | {PSALM, OTTAWA_JER, OTTAWA_SIR} and any(row.get('identity_key') == r['identity_key']
                           and row.get('occasion') == r['occasion']
                           and row.get('service_hour', '') == r.get('service_hour', '')
                           for r in predecessor()['reverse']
                           if r['identity_key'] in set(RULES) | {PSALM}
                           or r['identity_key'] in {OTTAWA_JER, OTTAWA_SIR} and r.get('source_family') == 'holy_pascha')
    return (row.get('identity_key') in added_ids or original_context
            or MARKER in row or 'jeremiah_followup' in row.get('source_disclosure', '')
            or row.get('source_family') in {'coptic_reader_jeremiah_followup', 'katameros_api_jeremiah_variant'})


def project_daily(rows, date):
    before = _before_day(date)
    if before is None:
        if any(_recognized(r) for r in rows):
            raise ValueError('Jeremiah follow-up wrong daily date')
        return rows
    authenticate()
    after = _expected_day(date)
    if _json(rows) != _json(before):
        _same(rows, after)
    return copy.deepcopy(after)


def restore_daily(rows, date):
    if _before_day(date) is None:
        if any(_recognized(r) for r in rows):
            raise ValueError('Jeremiah follow-up wrong daily date')
        return rows
    authenticate()
    _same(rows, _expected_day(date))
    return copy.deepcopy(_before_day(date))
