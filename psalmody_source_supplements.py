"""Authenticated, twelve-occurrence Psalmody source supplement (stdlib only).

Integration contract:
* ``load_psalmody_source_rows()`` returns string-valued raw crosswalk FIELDS;
  provenance is canonical JSON carrying the complete bounded source evidence.
* ``qualify_psalmody_row(row)`` reauthenticates ALL manifest/document bytes and
  exact raw fields, returning source metadata or raising ValueError. Do not use
  family/kind strings alone as an authorization or special-service hold bypass.
* ``psalmody_identity_for(row)`` qualifies first, then returns the same identity
  field shape as build_design_deliverables.identity_for, with numeric SOURCE/LXX
  chapter-only spans. It never passes these references through the MT default.

Bright Saturday is an undated cycle row with a Pascha-minus-one recurrence rule,
Midnight Praises, source_order/source_row_id 0 (before existing first readings).
Only the calendar consumer expands that rule. Other rites have NO date rule;
selected capture context is provenance, never a consecration appointment date.
In particular Pentecost Praises expansion requires separate recurrence approval.

No historical normalization ledgers are altered. These four full retained Reader
witnesses support liturgical chapter appointments, not exact translation/verse
coverage. Psalm 151 has no MT counterpart. Alleluia responses are not verse
numbers or additional occurrences; final Fourth Canticle doxology is excluded.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_RELATIVE = Path('sources/coptic-reader/psalmody-qualified-2026-10-25')
SOURCE_ROOT = ROOT / SOURCE_RELATIVE
MANIFEST_SHA256 = 'dd13f79eedbc8ee4c3b330ec7d172655103692d3c9a04977157ab065214e6f14'
SOURCE_KIND = 'psalmody_source_supplement'
SOURCE_CONVENTION = 'coptic_reader_psalmody_lxx_chapter_only'
QUALIFICATION = 'authenticated_prescribed_psalmody_chapter_only'
# Kept local so importing the supplement cannot import builders with write effects.
RAW_FIELDS = ('passage source_kind source_family source_table source_file source_row_id '
              'source_order source_token_order superseded_by_ref superseded_reason '
              'liturgical_place calendar_key gregorian_date coptic_date day_title '
              'service_day service_hour service_section reading_slot reading_type '
              'source_ref raw_ref normalized_ref normalized_segment book book_abbrev '
              'chapter_start verse_start chapter_end verse_end significance_note '
              'synaxarium_note url provenance').split()
OCCASIONS = {
    'bright_saturday': 'Bright Saturday',
    'church_consecration_part1': 'Church Consecration (Part 1)',
    'myron_preparation': 'Preparation of the Holy Myron',
    'pentecost_prostration_praises': 'Pentecost Prostration Praises',
}


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _load_manifest(root):
    root = Path(root).resolve()
    try:
        raw = (root / 'source-manifest.json').read_bytes()
        if _sha(raw) != MANIFEST_SHA256:
            raise ValueError('Psalmody source manifest authentication failed')
        manifest = json.loads(raw)
        documents = {d['rite']: d for d in manifest['documents']}
        if len(documents) != 4 or len(manifest['records']) != 12:
            raise ValueError('Psalmody source document/occurrence completeness drift')
        lines = {}
        for rite, doc in documents.items():
            relative = Path(doc['file'])
            path = root / relative
            if relative.is_absolute() or '..' in relative.parts or path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError('Psalmody source path escape')
            data = path.read_bytes()
            if _sha(data) != doc['sha256'] or len(data) != doc['bytes']:
                raise ValueError('Psalmody full capture authentication failed: ' + doc['file'])
            lines[rite] = data.decode('utf-8').splitlines()
            if lines[rite][0] != doc['title'] or doc['full_rendered_text'] is not True:
                raise ValueError('Psalmody full capture title/state drift')
        handles = set()
        for record in manifest['records']:
            doc = documents[record['rite']]
            source = lines[record['rite']]
            body = '\n'.join(source[record['body_first_line'] - 1:record['body_last_line']])
            context = '\n'.join(source[record['context_first_line'] - 1:record['context_last_line']])
            if (record['handle'] in handles or record['active'] is not True
                    or record['qualification'] != QUALIFICATION
                    or record['stage'] != doc['stage']
                    or record['full_capture_sha256'] != doc['sha256']
                    or source[record['heading_line'] - 1] != record['heading_exact']
                    or record['heading_exact'].strip() != 'Psalm ' + str(record['chapter'])
                    or not 1 <= record['context_first_line'] <= record['heading_line'] < record['body_first_line'] <= record['body_last_line'] <= record['context_last_line'] <= len(source)
                    or body != record['body_literal'] or _sha(body.encode()) != record['body_sha256']
                    or _sha(context.encode()) != record['context_sha256']):
                raise ValueError('Psalmody bounded heading/body/context/state drift')
            handles.add(record['handle'])
        return manifest, documents
    except (OSError, KeyError, IndexError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('Psalmody source evidence missing or malformed') from exc


def _row(record, doc, edition):
    bright = record['rite'] == 'bright_saturday'
    family = 'bright_saturday' if bright else 'special_service_psalmody'
    occasion = OCCASIONS[record['rite']]
    ref = 'Ps ' + str(record['chapter'])
    metadata = {**record, 'source_kind': SOURCE_KIND, 'source_family': family,
                'source_edition': edition, 'navigation': doc['navigation'],
                'captured_context': doc['captured_context'], 'capture_time': doc['capture_time'],
                'original_capture_path': doc['original_capture_path'],
                'full_capture_path': str(SOURCE_RELATIVE / doc['file']),
                'document_title': doc['title'], 'manifest_sha256': MANIFEST_SHA256}
    row: dict[str, str] = dict.fromkeys(RAW_FIELDS, '')
    row.update(passage=ref, source_kind=SOURCE_KIND, source_family=family,
               source_table='psalmody_qualified_source_manifest',
               source_file=metadata['full_capture_path'], source_row_id=str(record['source_order']),
               source_order=str(record['source_order']), source_token_order='1',
               liturgical_place=occasion, calendar_key=occasion if bright else record['rite'],
               day_title=occasion, service_day=occasion,
               service_section='Midnight Praises' if bright else record['stage'],
               reading_slot=record['reading_slot'], reading_type='prescribed_psalmody',
               source_ref=record['heading_exact'].strip(), raw_ref=record['heading_exact'].strip(),
               normalized_ref=ref, normalized_segment=ref, book='Psalms', book_abbrev='Ps',
               chapter_start=str(record['chapter']), chapter_end=str(record['chapter']),
               significance_note='Authenticated prescribed Psalmody; source/LXX chapter only, not exact MT text/verse equivalence.',
               url=doc['source_url'], provenance=_json(metadata))
    return row


def load_psalmody_source_rows(root=None):
    """Return fresh authenticated raw rows; optional root permits portable fixtures.

    All values are strings and all fields match build_lectionary_crosswalk.FIELDS.
    Full capture paths are repository-relative; original capture paths are retained
    only as provenance labels. No files outside the supplied source root are read.
    """
    manifest, documents = _load_manifest(SOURCE_ROOT if root is None else root)
    return [_row(r, documents[r['rite']], manifest['source_edition']) for r in manifest['records']]


def qualify_psalmody_row(row):
    """Reauthenticate an exact RAW row and return its source-qualified metadata.

    Raises ValueError for unknown, incomplete, inactive, altered or extra-field
    rows (including invented coordinates or lifecycle flags). Requalify raw input
    before presentation construction; this is not a presentation-row validator.
    No cached object or caller-provided source metadata is a trust boundary.
    """
    for expected in load_psalmody_source_rows():
        if row == expected and all(type(v) is str for v in row.values()):
            return json.loads(expected['provenance'])
    raise ValueError('Unqualified Psalmody raw occurrence: source/context/state/field mismatch')


def psalmody_identity_for(row):
    """Return source/LXX chapter identity only AFTER exact raw qualification.

    Shared chapter identities intentionally do not collapse rite occurrences;
    retain source_file/source_row_id and metadata.handle in occurrence keys.
    """
    q = qualify_psalmody_row(row)
    chapter = q['chapter']
    ref = f'Ps {chapter}'
    note = ('Authenticated Coptic Reader prescribed Psalmody; source/LXX chapter-only '
            'coordinates, not exact MT text or verse equivalence; no inferred verse endpoints. '
            'Liturgical responses and doxologies are not additional Scripture appointments.')
    if chapter == 151:
        note += ' NO_MT_COUNTERPART_PSALM151: no MT counterpart; no superscription/verse coverage inferred.'
    span = {'source_ref': row['source_ref'], 'source_convention': SOURCE_CONVENTION,
            'canonical_mt_ref': '', 'canonical_lxx_ref': ref,
            'confidence': 'source_chapter_qualified', 'validation_basis': note,
            'book': 'Ps', 'chapter_start': chapter, 'verse_start': None,
            'chapter_end': chapter, 'verse_end': None}
    return {'identity_key': 'rid_' + _sha(('scripture|' + SOURCE_CONVENTION + '|' + ref).encode())[:20],
            'reading_type': 'scripture', 'reading_name': '', 'source_label': row['source_ref'],
            'display_ref': ref + ' (Reader Psalmody; LXX/source chapter only)',
            'canonical_mt_ref': '', 'canonical_lxx_ref': ref,
            'source_convention': SOURCE_CONVENTION,
            'canonicalization_confidence': 'source_chapter_qualified',
            'canonicalization_note': note, 'spans_json': json.dumps([span], ensure_ascii=False, sort_keys=True)}
