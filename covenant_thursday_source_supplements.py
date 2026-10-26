"""Bounded Covenant Thursday retained-source raw rows; no activation or writes.

Exports load_covenant_thursday_rows() and qualify_covenant_thursday_row(row).
Qualify the unmodified RAW row before presentation construction. Qualification
returns fresh metadata, or raises ValueError; generic family/kind/path labels are
never authorization. All portable source bytes and ordinals are checked afresh.

Word: 3 appointments / 4 fragments; Waters: 11 appointments / 12 fragments.
Psalm references are body-verified covering MT/NKJV loci, not claims that entire
verses were read. Literal labels and Brenton displayed coordinates stay separate.
The Exodus/Joshua appointments are named, verse-unaddressable excerpts: they must
NOT become chapter-complete spans. Their empty coordinates are intentional.
Selected 2026 date context authenticates retained evidence, not future app state.
The parent owns Julian Pascha-minus-three recurrence and all runtime integration.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from passage_normalization import BOOK_ABBREV, parse_passage

ROOT = Path(__file__).resolve().parent
SOURCE_RELATIVE = Path('sources/coptic-reader/covenant-thursday-qualified-2026-10-25')
SOURCE_ROOT = ROOT / SOURCE_RELATIVE
APPROVAL_PATH = ROOT / 'sources/user-corrections/covenant-thursday-2026-10-25.json'
CONTRACT_SHA256 = 'd5436fbcef314640e9c5aa7223e9887ba89e48b5b03e32ee85369cd839261788'
APPROVAL_SHA256 = '6f55d664a385ff5f0efc7756936d9dd06bb2019a7d8cd361f25e2c2fb83bcb02'
SOURCE_KIND = 'coptic_reader_qualified_pascha_hour'
CURRENT_STATUS = 'source_qualified_retained_within_bounded_scope'
WATERS_SECTION = 'Liturgy of Blessing of the Water'
RAW_FIELDS = ('passage source_kind source_family source_table source_file source_row_id '
              'source_order source_token_order superseded_by_ref superseded_reason '
              'liturgical_place calendar_key gregorian_date coptic_date day_title '
              'service_day service_hour service_section reading_slot reading_type '
              'source_ref raw_ref normalized_ref normalized_segment book book_abbrev '
              'chapter_start verse_start chapter_end verse_end significance_note '
              'synaxarium_note url provenance').split()


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def load_covenant_thursday_contract():
    """Reauthenticate the entire portable pack; old reviews confer no activation."""
    root = Path(SOURCE_ROOT).resolve()
    try:
        raw = (root / 'source-contract.json').read_bytes()
        if _sha(raw) != CONTRACT_SHA256:
            raise ValueError('Covenant Thursday source contract drift')
        contract = json.loads(raw)
        if (_sha(APPROVAL_PATH.read_bytes()) != APPROVAL_SHA256
                or contract['fingerprints']['bounded-user-authorization.json'] != APPROVAL_SHA256):
            raise ValueError('Covenant Thursday bounded authorization drift')
        for relative, expected in contract['fingerprints'].items():
            path = root / relative
            if (Path(relative).is_absolute() or '..' in Path(relative).parts
                    or path.is_symlink() or not path.resolve().is_relative_to(root)
                    or _sha(path.read_bytes()) != expected):
                raise ValueError('Covenant Thursday portable evidence drift: ' + relative)
        if (contract['old_receipts_grant_activation'] is not False
                or contract['runtime_activation_approved'] is not False
                or contract['fresh_app_verification'] is not False
                or contract['current_status'] != CURRENT_STATUS
                or contract['selected_civil_date'] != '2026-04-09'):
            raise ValueError('Covenant Thursday contract state/date drift')
        old = json.loads((root / 'old-review-receipt.json').read_text())
        if (old['consumer_eligible'] is not False or old['release_approval'] is not False
                or old['runtime_contract_acceptance'] != 'pending'):
            raise ValueError('Covenant Thursday old receipt nonapproval changed')
        context = json.loads((root / 'thursday--context.json').read_text())
        if (context['selected_civil_date'] != contract['selected_civil_date']
                or context['home_occasion'] != contract['selected_home_occasion']
                or (root/'thursday--selected-home.txt').read_text().splitlines()[0] != context['home_occasion']):
            raise ValueError('Covenant Thursday selected context drift')
        for kind in ('home', 'picker'):
            for form in ('text', 'screenshot'):
                item = context[kind]
                if _sha((root/Path(item[form+'_path']).name).read_bytes()) != item[form+'_sha256']:
                    raise ValueError('Covenant Thursday selected date witness drift')
        captures = json.loads((root / 'captures.json').read_text())
        docs = {d['service_section']: d for d in contract['documents']}
        if set(docs) != {'Liturgy', WATERS_SECTION}:
            raise ValueError('Covenant Thursday service scope drift')
        for section, doc in docs.items():
            matches = [c for c in captures if c['text_path'] == doc['original_capture_path']]
            if len(matches) != 1:
                raise ValueError('Covenant Thursday capture identity drift')
            c = matches[0]
            text = (root/doc['file']).read_bytes()
            if (c['text_sha256'] != _sha(text) or doc['sha256'] != _sha(text)
                    or c['full_rendered_text'] is not True or doc['full_rendered_text'] is not True
                    or text.decode().splitlines()[0] != doc['title']
                    or doc['navigation'] != ['Special', 'Pascha'] + c['path']
                    or c['selected_context'] != context
                    or _sha((root/Path(c['screenshot_path']).name).read_bytes()) != c['screenshot_sha256']):
                raise ValueError('Covenant Thursday complete document/context mismatch')
            if c['path'][-1] not in (root/'thursday--thursday-day--menu.txt').read_text().splitlines():
                raise ValueError('Covenant Thursday selected service navigation mismatch')
        normalization = {e['selected_record']['id']: e['selected_record'] for e in
                         json.loads((root/'retained-normalization-records.json').read_text())}
        counts = {'Liturgy': 0, WATERS_SECTION: 0}
        for a in contract['appointments']:
            section = a['service_section']
            counts[section] += 1
            doc = docs[section]
            lines = (root / doc['file']).read_text().splitlines()
            first, last = a['body_first_line'], a['body_last_line']
            literal = '\n'.join(lines[first-1:last])
            if (a['source_order'] != counts[section] or a['source_row_id'] != str(counts[section])
                    or a['file'] != doc['file'] or a['full_capture_sha256'] != doc['sha256']
                    or not 1 <= first == a['heading_line'] <= last <= len(lines)
                    or lines[first-1] != '\t' + a['printed_ref']
                    or literal != a['body_envelope_literal']
                    or _sha(literal.encode()) != a['body_envelope_sha256']
                    or a['active'] is not True or a['include_in_current_index'] is not True
                    or a['runtime_activation_approved'] is not False
                    or a['current_status'] != CURRENT_STATUS or a['fresh_app_verification'] is not False):
                raise ValueError('Covenant Thursday appointment body/ordinal/state drift')
            if a['reading_slot'] == 'Psalm':
                n = normalization[a['normalization_record_id']]
                if (n['block_raw'] != literal or n['source_sha256'] != doc['sha256']
                        or n['canonical_mt_ref'] != '; '.join(a['normalized_fragments'])
                        or n['canonical_lxx_ref'] != '; '.join(a['canonical_lxx_fragments'])):
                    raise ValueError('Covenant Thursday Psalm body-coordinate mismatch')
                for witnesses in n['witnesses'].values():
                    for witness in witnesses:
                        path = root/'bible-witnesses'/Path(witness['raw_path']).name
                        if _sha(path.read_bytes()) != witness['raw_sha256']:
                            raise ValueError('Covenant Thursday Bible edition witness drift')
        if counts != {'Liturgy': 3, WATERS_SECTION: 11}:
            raise ValueError('Covenant Thursday incomplete appointment table')
        return contract
    except (OSError, KeyError, IndexError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('Covenant Thursday source evidence missing or malformed') from exc


def _row(appointment, doc, token_order, passage):
    named = appointment['coordinate_status'] == 'verse_unaddressable_named_excerpt'
    parsed = None if named else parse_passage(passage)
    if not named and (parsed is None or len(parsed.parts) != 1 or parsed.canonical != passage):
        raise ValueError('Covenant Thursday exact canonical token parse drift')
    section = appointment['service_section']
    source_file = str(SOURCE_RELATIVE / appointment['file'])
    q = {**appointment, 'contract_sha256': CONTRACT_SHA256,
         'source_family': SOURCE_KIND, 'source_kind': SOURCE_KIND,
         'source_file': source_file, 'source_token_order': token_order,
         'passage': passage, 'normalized_ref': '' if named else passage,
         'source_selected_civil_date': '2026-04-09',
         'source_selected_home_occasion': 'Selected Season Covenant Thursday Parmoute 1, 1742 Thursday, April 9, 2026',
         'source_edition': 'Coptic Reader retained bilingual/trilingual rendered text; qualification is not fresh app verification',
         'navigation': doc['navigation'], 'document_title': doc['title'],
         'old_receipts_grant_activation': False,
         'canonical_mt_ref': '' if named else passage,
         'canonical_lxx_ref': appointment.get('canonical_lxx_fragments', [''] * token_order)[token_order-1]
             if appointment['reading_slot'] == 'Psalm' else ('' if named else passage)}
    row: dict[str, str] = dict.fromkeys(RAW_FIELDS, '')
    row.update(passage=passage, source_kind=SOURCE_KIND, source_family=SOURCE_KIND,
               source_table='covenant_thursday_qualified_source_contract', source_file=source_file,
               source_row_id=appointment['source_row_id'], source_order=str(appointment['source_order']),
               source_token_order=str(token_order), liturgical_place='Great Thursday | '+section,
               calendar_key='Great Thursday', day_title='Great Thursday', service_day='Great Thursday',
               service_hour=section, service_section=section, reading_slot=appointment['reading_slot'],
               reading_type=appointment['reading_type'], source_ref=appointment['printed_ref'],
               raw_ref=appointment['printed_ref'], normalized_ref='' if named else passage,
               normalized_segment='' if named else passage,
               significance_note=appointment['coordinate_note'], url='https://copticreader.org/app/#/document',
               provenance=_json(q))
    if parsed:
        part = parsed.parts[0]
        row.update(book=next(name for name, abbrev in BOOK_ABBREV.items() if abbrev == parsed.book_abbrev),
                   book_abbrev=parsed.book_abbrev,
                   chapter_start=str(part.chapter_start), chapter_end=str(part.chapter_end),
                   verse_start='' if part.verse_start is None else str(part.verse_start),
                   verse_end='' if part.verse_end is None else str(part.verse_end))
    else:
        row.update(book='Exodus' if appointment['book_hint']=='Exod' else 'Joshua', book_abbrev=appointment['book_hint'])
    return row


def load_covenant_thursday_rows() -> list[dict]:
    """Fresh string-valued raw crosswalk rows; split Psalms share one row/order ID."""
    contract = load_covenant_thursday_contract()
    docs = {d['service_section']: d for d in contract['documents']}
    return [_row(a, docs[a['service_section']], i, token)
            for a in contract['appointments']
            for i, token in enumerate(a['normalized_fragments'] or [a['printed_ref']], 1)]


def qualify_covenant_thursday_row(row):
    """Return fresh qualified metadata for one exact raw row; otherwise fail closed.

    Includes family, kind, occasion, service, slot, all source ordinals, raw and
    canonical references, lifecycle flags, full-file and literal-body hashes.
    No mutable metadata cache, historical approval rewriting, or activation hook.
    """
    for expected in load_covenant_thursday_rows():
        if row == expected and all(type(v) is str for v in row.values()):
            return json.loads(expected['provenance'])
    raise ValueError('Unqualified Covenant Thursday raw row: source/context/ordinal/coordinate/state mismatch')
