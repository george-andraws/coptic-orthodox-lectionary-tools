"""Source-qualified H1-H8 repair lane, deliberately not wired into shared builders.

Integration: call repair_reverse_rows after npm canonicalizeOccurrences and
repair_daily_year after npm structural daily fill, passing the complete daily
year and corrected reverse rows. The JSON stdin/stdout bridge in main exposes
both hooks. Existing design whole-corpus membership validation remains unchanged.
repair_presentation_rows/project_review_dates are lower-level diagnostic helpers,
not instructions to bypass that gate. Retained Reader text governs only literal
non-Psalm selections;
printed witnesses stay inactive, including Galatians 3 at Friday's Eleventh Hour.
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = 'sources/coptic-reader/holy-week-review-qualified-2026-10-29'
MANIFEST_SHA256 = '16737be9590c5df2020e494b4950b1142347887f71a9b91f28b5601d66adf257'
PRINTED_EVIDENCE_SHA256 = '99a696ca3a69869bed1ef5d1d3530a05ecb3b6d6aeab31eab579dda13b3be2ff'
LEGACY = 'holy_pascha_curated_day_hour'
FAMILY = 'coptic_reader_qualified_holy_week_review'
HOLD = 'pending_coptic_reader_review'
CONTEXT_FIELDS = ['pascha_service', 'pascha_civil_date', 'pascha_offset_days', 'display_occasion']
EVIDENCE_FIELDS = ['holy_week_review_note', 'holy_week_review_evidence']

# Family-qualified raw labels, not a title-wide Eve heuristic.
CURATED_EVE = {'Monday Eve': 'eve_of_tuesday', 'Tuesday Eve': 'eve_of_wednesday',
               'Wednesday Eve': 'eve_of_thursday', 'Great Thursday Eve': 'eve_of_friday'}
PRINTED_EVE = {'Monday Eve': 'eve_of_monday', 'Tuesday Eve': 'eve_of_tuesday',
               'Wednesday Eve': 'eve_of_wednesday', 'Thursday Eve': 'eve_of_thursday',
               'Great Thursday Eve': 'eve_of_thursday', 'Good Friday Eve': 'eve_of_friday'}
DAY = {'Hosanna Sunday': 'palm_sunday', 'Palm Sunday': 'palm_sunday',
       'Monday': 'monday', 'Tuesday': 'tuesday', 'Wednesday': 'wednesday',
       'Wednesday of Holy Pascha': 'wednesday', 'Great Thursday': 'great_thursday',
       'the Covenant Thursday': 'great_thursday', 'Thursday': 'great_thursday',
       'Good Friday': 'good_friday', 'Bright Saturday': 'bright_saturday'}
OFFSET = dict(palm_sunday=-7, eve_of_monday=-7, monday=-6, eve_of_tuesday=-6,
              tuesday=-5, eve_of_wednesday=-5, wednesday=-4, eve_of_thursday=-4,
              great_thursday=-3, eve_of_friday=-3, good_friday=-2, bright_saturday=-1)
LABEL = {s: ('Eve of ' + s.removeprefix('eve_of_').title()) if s.startswith('eve_of_')
         else s.replace('_', ' ').title() for s in OFFSET}
RAW_READER_DAY = {'eve_of_monday': 'Eve of Monday', 'eve_of_wednesday': 'Tuesday Eve',
                  'eve_of_thursday': 'Wednesday Eve', 'good_friday': 'Good Friday'}
# New appointments are restricted to the reported defects, not every heading in
# retained captures. Other H8 captures qualify exact existing appointments only.
ADDITIONS = {
    'tuesday--wednesday-eve--1st-hour': {'Ezek 22:17-22', 'Ezek 22:23-29', 'Matt 22:1-14'},
    'tuesday--wednesday-eve--6th-hour': {'Jer 16:9-13', 'Matt 25:1-13'},
    'sunday--monday-eve--3rd-hour': {'Zeph 1:14-2:2', 'Lk 9:18-22'},
    'sunday--monday-eve--11th-hour': {'Mic 3:1-4', 'Matt 17:19-23'},
    'friday--6th-hour': {'Jn 19:13-27', 'Gal 6:14-18'},
    'wednesday--thursday-eve--1st-hour': {'Ezek 43:5-11'},
}


def _read(relative):
    target = ROOT
    for part in Path(relative).parts:
        if part in {'..', '/', ''} or part not in {p.name for p in target.iterdir()}:
            raise ValueError('Holy Week evidence literal path rejected')
        target /= part
        if target.is_symlink():
            raise ValueError('Holy Week evidence symlink rejected')
    if not target.is_file() or not target.resolve().is_relative_to(ROOT):
        raise ValueError('Holy Week evidence path rejected')
    return target.read_bytes()


def _manifest():
    try:
        data = _read(SOURCE + '/source-manifest.json')
        if hashlib.sha256(data).hexdigest() != MANIFEST_SHA256:
            raise ValueError('Holy Week manifest authentication failed')
        return json.loads(data)
    except (OSError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError('Holy Week manifest missing or malformed') from exc


def authenticate_document(key):
    """Reread complete pinned capture and exact literal heading/context each call."""
    try:
        m = _manifest()
        if type(key) is not str or key not in m['documents']:
            raise ValueError('Unknown Holy Week document')
        doc = m['documents'][key]
        data = _read(SOURCE + '/' + doc['file'])
        if len(data) != doc['bytes'] or hashlib.sha256(data).hexdigest() != doc['sha256']:
            raise ValueError('Holy Week capture authentication failed')
        lines = data.decode().splitlines()
        if lines[0] != doc['document_title']:
            raise ValueError('Holy Week source context drift')
        for reading in doc['readings']:
            if lines[reading['heading_line'] - 1] != reading['heading_exact']:
                raise ValueError('Holy Week reading heading drift')
        return dict(copy.deepcopy(doc), key=key, path=SOURCE + '/' + doc['file'])
    except (OSError, KeyError, IndexError, UnicodeError) as exc:
        raise ValueError('Holy Week evidence missing or malformed') from exc


def pascha_context(row, civil_date=None):
    family = row.get('source_family')
    title = row.get('day_title') or row.get('occasion') or ''
    # Some printed rows carry the hour as a title suffix. Keep raw text intact.
    title = title.split(' | ', 1)[0]
    if family == FAMILY:
        service = row.get('pascha_service')
    elif family == LEGACY:
        service = CURATED_EVE.get(title) or DAY.get(title)
    elif family == 'holy_pascha':
        service = PRINTED_EVE.get(title) or DAY.get(title)
    else:
        return {}
    if service not in OFFSET:
        return {}
    date_text = civil_date or row.get('gregorian_date') or ''
    if date_text:
        from calendar_resolution import julian_pascha_gregorian
        date = dt.date.fromisoformat(date_text)
        if (date - julian_pascha_gregorian(date.year)).days != OFFSET[service]:
            raise ValueError('Pascha civil date disagrees with service identity')
    return dict(pascha_service=service, pascha_civil_date=date_text,
                pascha_offset_days=OFFSET[service], display_occasion=LABEL[service])


def _ref(row):
    return row.get('canonical_mt_ref') or row.get('normalized_ref') or row.get('passage') or ''


def _evidence(doc, reading):
    return dict(source_url='https://copticreader.org/app/', path=doc['path'],
                sha256=doc['sha256'], manifest_sha256=MANIFEST_SHA256,
                service=doc['service'], hour=doc['hour'], document_key=doc['key'],
                heading_line=reading['heading_line'], printed_ref=reading['printed_ref'],
                canonical_mt_ref=reading['canonical_mt_ref'], fresh_app_verification=False,
                qualification='Retained full Reader capture; exact printed non-Psalm selection. No new Psalm numbering approval.')


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _slot(ref, prophecy_ordinal):
    book = ref.split(' ', 1)[0]
    if book in {'Matt', 'Mark', 'Lk', 'Jn'}:
        return 'Gospel', 'gospel'
    if book in {'Rom', '1Cor', '2Cor', 'Gal', 'Eph', 'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus', 'Phlm', 'Heb'}:
        return 'Pauline', 'pauline'
    return 'OT' + str(prophecy_ordinal), 'prophecy'


def _new_row(doc, reading):
    from build_design_deliverables import identity_for
    ref = reading['canonical_mt_ref']
    ordinal = doc['readings'].index(reading) + 1
    prophecy_ordinal = sum(1 for r in doc['readings'][:ordinal]
                          if _slot(r['canonical_mt_ref'], 1)[1] == 'prophecy')
    slot, slot_type = _slot(ref, prophecy_ordinal)
    evidence = _evidence(doc, reading)
    locator = doc['path'] + ':line ' + str(reading['heading_line']) + '; sha256=' + doc['sha256']
    day = RAW_READER_DAY[doc['service']]
    row = dict(identity_for(ref, 'pascha_day_hour'),
               source_kind=FAMILY, source_family=FAMILY, source_key=FAMILY,
               source_title='Coptic Reader retained Holy Week service',
               source_edition='Retained rendered text; capture time and app version unspecified',
               source_locator=locator, source_url='https://copticreader.org/app/',
               source_file=doc['path'], source_row_id=doc['key'] + ':' + str(reading['heading_line']),
               source_order=ordinal, source_token_order=1, authority_tier='primary_reader_source',
               occasion=day, day_title=day, day_titles=day, service_day=day, occasion_kind='specific',
               calendar_key=doc['document_title'], calendar_keys=doc['document_title'],
               attestation_year_min='', attestation_year_max='', attestation_years='',
               collapsed_row_count='1', reading_name='', hour_theme='',
               gregorian_date='', coptic_date='',
               service_hour=doc['hour'], service_section=doc['hour'],
               slot=slot, reading_slot=slot, reading_type='scripture', slot_type=slot_type,
               slot_order=ordinal, source_ref=reading['printed_ref'], raw_ref=reading['printed_ref'],
               provenance='Retained Reader evidence: ' + locator,
               current_status='current_confirmed_coptic_reader', removed_marker='',
               status_note='H1/H2/H4/H6/H7 bounded source-backed repair; no printed-only promotion.',
               holy_week_review_note='Literal source-backed repair from retained Reader capture.',
               holy_week_review_evidence=_json(evidence), pascha_service=doc['service'])
    row.update(pascha_context(row))
    row['source_disclosure'] = _json([{k: row[k] for k in
        ('source_family', 'source_kind', 'source_edition', 'source_title', 'source_locator')}
        | {'holy_week_review_evidence': evidence, 'current_status': row['current_status'],
           'removed_marker': '', 'pascha_service': doc['service']}])
    row['source_disclosure_count'] = '1'
    return row


def _review_match(row, documents):
    context = pascha_context(row)
    if not context or row.get('source_family') != LEGACY or row.get('source_kind') != 'pascha_day_hour':
        return None
    slot, kind = _slot(_ref(row), 1)
    actual_slot = row.get('slot') or row.get('reading_slot') or ''
    if ((kind == 'prophecy' and not (actual_slot.startswith('OT') and actual_slot[2:].isdigit()))
            or (kind != 'prophecy' and actual_slot != slot)
            or (row.get('slot_type') and row['slot_type'] != kind)):
        return None
    for doc in documents:
        if (doc['service'], doc['hour']) != (context['pascha_service'], row.get('service_hour')):
            continue
        for reading in doc['readings']:
            if not reading['is_psalm'] and reading['canonical_mt_ref'] == _ref(row):
                return doc, reading
    return None


def repair_presentation_rows(rows, *, add_reader=True):
    """Copy input; preserve raw labels/locators/keys and inactive witnesses.

    H8 is not a blanket retirement. Only exact existing live non-Psalm matches
    receive confirmation. H5 remains unchanged as requested, even where one
    hour has Reader support. Source-only printed candidates are disclosed in the
    check sheet and retain historical status and original numeric witnesses.
    """
    documents = [authenticate_document(k) for k in _manifest()['documents']]
    out = []
    for original in rows:
        row = copy.deepcopy(original)
        context = pascha_context(row)
        if context:
            row.update(context)
        ref = _ref(row)
        legacy = row.get('source_family') == LEGACY and row.get('source_kind') == 'pascha_day_hour'
        live = (row.get('current_status') == 'current_working_source_not_coptic_reader_checked'
                and not row.get('removed_marker') and row.get('active') is not False
                and row.get('status') != 'removed' and not row.get('superseded_by_ref'))
        hold_id = ('H1' if legacy and row.get('occasion') == 'Tuesday Eve' else
                   'H4' if legacy and row.get('occasion') == 'Good Friday' and row.get('service_hour') == 'Sixth Hour' and ref == 'Jn 19:1-12' else
                   'H6' if legacy and row.get('occasion') == 'Wednesday Eve' and row.get('service_hour') == 'First Hour' and ref == 'Jer 43:5-11' else '')
        if hold_id and (live or row.get('current_status') == HOLD):
            row['current_status'] = HOLD
            row['active'] = False
            row['holy_week_review_note'] = hold_id + ': incorrect working-source appointment held; original witness and locator preserved.'
        h5 = legacy and row.get('occasion') == 'Great Thursday' and row.get('service_hour') in {'Third Hour', 'Ninth Hour'} and ref == 'Matt 26:17-19'
        match = _review_match(row, documents)
        if match and live and not hold_id:
            doc, reading = match
            row['holy_week_review_evidence'] = _json(_evidence(doc, reading))
            if not h5:
                row['current_status'] = 'current_confirmed_coptic_reader'
                row['holy_week_review_note'] = 'H8: exact non-Psalm appointment matches retained Reader service/hour.'
        if h5:
            row['holy_week_review_note'] = 'H5: duplicate reference flagged; neither hour removed or silently replaced. Ninth Hour has retained Reader support; Third Hour remains to check.'
        if (ref in {'Gal 3:1-6', 'Gal 6:14-18', 'Isa 19:19-25'}
                and row.get('source_family') in {LEGACY, 'holy_pascha'}
                and 'H7: attachment reports' not in row.get('holy_week_review_note', '')):
            printed_path = SOURCE + '/printed-h7-evidence.json'
            if hashlib.sha256(_read(printed_path)).hexdigest() != PRINTED_EVIDENCE_SHA256:
                raise ValueError('Holy Week printed evidence authentication failed')
            row['holy_week_review_note'] = (row.get('holy_week_review_note', '') + ' H7: attachment reports Book of the Holy Pascha, archive.org Section12HCM, as printed corroboration only. Authenticated Ottawa excerpts: ' + printed_path + '; sha256=' + PRINTED_EVIDENCE_SHA256 + '. Printed evidence alone grants no current status.').strip()
        if row.get('source_family') == 'holy_pascha' and context:
            candidate_id = ('H2' if context['pascha_service'] == 'eve_of_monday' else
                            'H1' if context['pascha_service'] == 'eve_of_wednesday' else
                            'H4' if context['pascha_service'] == 'good_friday' and row.get('service_hour') == 'Sixth Hour' and ref == 'Jn 19:13-27' else
                            'H6' if context['pascha_service'] == 'eve_of_thursday' and row.get('service_hour') == 'First Hour' and ref == 'Ezek 43:5-11' else '')
            if candidate_id:
                row['holy_week_review_note'] = candidate_id + ': printed evidence-only candidate; original historical lifecycle retained. No printed-only activation.'
        out.append(row)
    if add_reader:
        for key, allowed in ADDITIONS.items():
            doc = next(d for d in documents if d['key'] == key)
            for reading in doc['readings']:
                if reading['canonical_mt_ref'] not in allowed:
                    continue
                # A qualified existing live appointment wins over a duplicate
                # added capture. Historical witnesses never suppress a repair.
                if any(r.get('current_status') == 'current_confirmed_coptic_reader'
                       and r.get('pascha_service') == doc['service']
                       and r.get('service_hour') == doc['hour']
                       and _ref(r) == reading['canonical_mt_ref'] and not r.get('removed_marker') for r in out):
                    continue
                out.append(_new_row(doc, reading))
    validate_review_projection(out)
    return out


def _is_reader(row):
    return (row.get('source_family') == FAMILY or row.get('source_kind') == FAMILY
            or SOURCE in str(row.get('source_file', ''))
            or SOURCE in str(row.get('source_locator', '')))


def validate_review_projection(rows):
    """Authenticate the actual presentation payload, not just the source helper."""
    for row in rows:
        if not _is_reader(row):
            if row.get('holy_week_review_evidence'):
                try:
                    evidence = json.loads(row['holy_week_review_evidence'])
                    doc = authenticate_document(evidence['document_key'])
                    reading = next(r for r in doc['readings'] if r['heading_line'] == evidence['heading_line'])
                    context = pascha_context(row)
                    if (row.get('source_family') != LEGACY or row.get('source_kind') != 'pascha_day_hour'
                            or not context or context['pascha_service'] != doc['service']
                            or row.get('service_hour') != doc['hour'] or _ref(row) != reading['canonical_mt_ref']
                            or _review_match(row, [doc]) != (doc, reading)
                            or reading['is_psalm'] or evidence != _evidence(doc, reading)
                            or row.get('removed_marker')
                            or row.get('current_status') not in {'current_confirmed_coptic_reader', 'current_working_source_not_coptic_reader_checked'}):
                        raise ValueError('Holy Week existing appointment evidence rebound')
                except (KeyError, TypeError, StopIteration, json.JSONDecodeError) as exc:
                    raise ValueError('Holy Week existing qualification missing') from exc
            continue
        try:
            evidence = json.loads(row['holy_week_review_evidence'])
            doc = authenticate_document(evidence['document_key'])
            reading = next(r for r in doc['readings'] if r['heading_line'] == evidence['heading_line'])
            if reading['canonical_mt_ref'] not in ADDITIONS.get(doc['key'], set()):
                raise ValueError('Holy Week new appointment outside bounded repair')
            expected = _new_row(doc, reading)
            # The trusted caller may assign only a supported civil date.
            for field, value in expected.items():
                if field in {'gregorian_date', 'pascha_civil_date'}:
                    continue
                if row.get(field) != value or (field in {'source_order', 'source_token_order', 'slot_order'} and type(row.get(field)) is not int):
                    raise ValueError('Holy Week Reader projection drift: ' + field)
            context = pascha_context(row)
            if row.get('pascha_civil_date', '') != context['pascha_civil_date']:
                raise ValueError('Holy Week civil date disclosure drift')
        except (KeyError, TypeError, StopIteration, json.JSONDecodeError) as exc:
            raise ValueError('Holy Week Reader projection missing qualification') from exc


def project_review_dates(rows, years=(2026, 2027, 2028)):
    """Materialize only the new authenticated Reader lane on civil evenings."""
    from calendar_resolution import julian_pascha_gregorian
    validate_review_projection(rows)
    out = []
    for row in rows:
        if not _is_reader(row) or row.get('gregorian_date'):
            out.append(copy.deepcopy(row))
            continue
        for year in years:
            date = (julian_pascha_gregorian(year) + dt.timedelta(days=row['pascha_offset_days'])).isoformat()
            dated = dict(copy.deepcopy(row), gregorian_date=date, pascha_civil_date=date)
            out.append(dated)
    validate_review_projection(out)
    return out


def _disclose_legacy_review(row):
    if row.get('source_family') not in {LEGACY, 'holy_pascha'}:
        return row
    if not row.get('holy_week_review_note') and not row.get('holy_week_review_evidence'):
        return row
    disclosure = json.loads(row.get('source_disclosure') or '[]')
    qualification = {k: row[k] for k in CONTEXT_FIELDS + EVIDENCE_FIELDS if k in row}
    for item in disclosure:
        item['holy_week_review'] = copy.deepcopy(qualification)
    row['source_disclosure'] = _json(disclosure)
    return row


def repair_reverse_rows(rows):
    """Npm hook AFTER canonicalizeOccurrences; accepts published-like rows.

    No design-ledger replacement or generated-file patching. New Reader rows
    carry source qualifications; printed candidates retain historical status.
    """
    return [_disclose_legacy_review(row) for row in repair_presentation_rows(rows)]


def _daily_order_key(row):
    service = row.get('pascha_service', '')
    hour = {'First Hour': 0, 'Third Hour': 1, 'Sixth Hour': 2,
            'Ninth Hour': 3, 'Eleventh Hour': 4, 'Twelfth Hour': 5}
    stage = {'prophecy': 0, 'pauline': 1, 'psalm': 2, 'gospel': 3}
    evidence = json.loads(row.get('holy_week_review_evidence') or '{}')
    return (1 if service.startswith('eve_of_') else 0,
            hour.get(row.get('service_hour'), 50), stage.get(row.get('slot_type'), 50),
            evidence.get('heading_line', 0))


def repair_daily_year(year, days, corrected_reverse):
    """Npm hook AFTER structural fill, with full day arrays and repaired reverse.

    Original daily locators and unrelated rows survive. Holds cannot be restored
    by structural fill. No printed-only or uncaptured Psalm selection is supplied.
    """
    from calendar_resolution import julian_pascha_gregorian
    if type(year) is not int or not isinstance(days, dict):
        raise ValueError('Holy Week daily hook requires an integer year and complete date map')
    validate_review_projection(corrected_reverse)
    additions = [r for r in corrected_reverse if _is_reader(r)]
    out = copy.deepcopy(days)
    for date_text, original in days.items():
        if dt.date.fromisoformat(date_text).year != year:
            raise ValueError('Holy Week daily date map contains another year')
        if not any(r.get('source_family') == LEGACY for r in original):
            continue
        repaired = repair_presentation_rows(original, add_reader=False)
        for row in repaired:
            if row.get('source_family') == LEGACY:
                row.update(pascha_context(row, date_text))
                _disclose_legacy_review(row)
        out[date_text] = [r for r in repaired if r.get('current_status') != HOLD]
    for row in additions:
        date_text = (julian_pascha_gregorian(year) + dt.timedelta(days=row['pascha_offset_days'])).isoformat()
        if date_text not in out:
            raise ValueError('Holy Week daily map is missing the affected civil date')
        key = (row['identity_key'], row['pascha_service'], row['service_hour'], row['slot'])
        if any((r.get('identity_key'), r.get('pascha_service'), r.get('service_hour'), r.get('slot')) == key for r in out[date_text]):
            continue
        dated = dict(copy.deepcopy(row), gregorian_date=date_text, pascha_civil_date=date_text,
                     source_group_key='|'.join((FAMILY, row['source_row_id'], row['pascha_service'], row['service_hour'], row['slot'])))
        out[date_text].append(dated)
    for date_text, readings in out.items():
        if not any(r.get('pascha_service') for r in readings):
            continue
        positions = [i for i, r in enumerate(readings) if r.get('pascha_service') and r.get('service_hour') in {'First Hour', 'Third Hour', 'Sixth Hour', 'Ninth Hour', 'Eleventh Hour', 'Twelfth Hour'}]
        ordered = sorted((readings[i] for i in positions), key=_daily_order_key)
        for i, row in zip(positions, ordered):
            readings[i] = row
        for i, row in enumerate(readings, 1):
            row['reading_order'] = i
    validate_review_projection([r for readings in out.values() for r in readings])
    return out


def main():
    """JSON bridge: reverse {mode,rows}; daily {mode,year,days,reverse_rows}."""
    import sys
    payload = json.load(sys.stdin)
    if payload.get('mode') == 'reverse':
        result = repair_reverse_rows(payload['rows'])
    elif payload.get('mode') == 'daily':
        result = repair_daily_year(payload['year'], payload['days'], payload['reverse_rows'])
    else:
        raise ValueError('Unknown Holy Week review bridge mode')
    json.dump(result, sys.stdout, ensure_ascii=False, separators=(',', ':'))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
