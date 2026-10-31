"""Apply already accepted Coptic Reader annual corrections to other years.

A captured annual-table repair is the reading for that occasion, not for one
civil date. Sunday and differently labeled feast rows are left alone. First
Monday of Great Fast Matins is activated only for the accepted 2026-02-16
capture. Its Liturgy was not captured and is not copied from the Lent cycle.
"""
from __future__ import annotations

import copy
import hashlib
import json

SUPERSEDED = 'superseded by annual Reader identity repair'
LENT_DATE = '2026-02-16'
LENT_OCCASION = 'First Monday of Great Fast'
PROPHECY_LOCATOR = (
    'sources/coptic-reader/matins-source-accepted-2026-10-07/evidence/'
    'lent-source-completion-04/attempts/2026-02-16-ready02/Prophecies.txt'
    '; sha256=c8007a0978980f19d128229550a7e08065566da79aab085ccbe739988e2f099a'
)
PSALM_GOSPEL_LOCATOR = (
    'sources/coptic-reader/matins-source-accepted-2026-10-07/evidence/'
    'lent-source-completion-04/attempts/2026-02-16-ready02/Psalm_and_Gospel.txt'
    '; sha256=9a6e2baa32b25b147c1b761b3be778943bb9e87f271d2712c886e5df43bc0a01'
)

IDENTITIES = {
    '1Pet 1:25-2:10': {
        'identity_key': 'rid_7587173374425d8e1e91',
        'display_ref': '1Pet 1:25-2:10',
        'canonical_mt_ref': '1Pet 1:25-2:10',
        'canonical_lxx_ref': '1Pet 1:25-2:10',
        'spans_json': '[{"book": "1Pet", "canonical_lxx_ref": "1Pet 1:25-2:10", "canonical_mt_ref": "1Pet 1:25-2:10", "chapter_end": 2, "chapter_start": 1, "confidence": "high", "source_convention": "modern_english_reference", "source_ref": "1Pet 1:25-2:10", "validation_basis": "", "verse_end": 10, "verse_start": 25}]',
    },
    '1Pet 2:11-25': {
        'identity_key': 'rid_f255dc86622c22f90539',
        'display_ref': '1Pet 2:11-25',
        'canonical_mt_ref': '1Pet 2:11-25',
        'canonical_lxx_ref': '1Pet 2:11-25',
        'spans_json': '[{"book": "1Pet", "canonical_lxx_ref": "1Pet 2:11-25", "canonical_mt_ref": "1Pet 2:11-25", "chapter_end": 2, "chapter_start": 2, "confidence": "high", "source_convention": "modern_english_reference", "source_ref": "1Pet 2:11-25", "validation_basis": "", "verse_end": 25, "verse_start": 11}]',
    },
    'Lk 14:25-35': {
        'identity_key': 'rid_6e1ac90c24fcf4391a9b',
        'display_ref': 'Lk 14:25-35',
        'canonical_mt_ref': 'Lk 14:25-35',
        'canonical_lxx_ref': 'Lk 14:25-35',
        'spans_json': '[{"book": "Lk", "canonical_lxx_ref": "Lk 14:25-35", "canonical_mt_ref": "Lk 14:25-35", "chapter_end": 14, "chapter_start": 14, "confidence": "high", "source_convention": "modern_english_reference", "source_ref": "Lk 14:25-35", "validation_basis": "", "verse_end": 35, "verse_start": 25}]',
    },
    'Matt 4:23-5:16': {
        'identity_key': 'rid_42e4974f3dd164818cbb',
        'display_ref': 'Matt 4:23-5:16',
        'canonical_mt_ref': 'Matt 4:23-5:16',
        'canonical_lxx_ref': 'Matt 4:23-5:16',
        'spans_json': '[{"book": "Matt", "canonical_lxx_ref": "Matt 4:23-5:16", "canonical_mt_ref": "Matt 4:23-5:16", "chapter_end": 5, "chapter_start": 4, "confidence": "high", "source_convention": "modern_english_reference", "source_ref": "Matt 4:23-5:16", "validation_basis": "", "verse_end": 16, "verse_start": 23}]',
    },
    'Matt 12:24-34': {
        'identity_key': 'rid_8bd8c1d0b59b3e302f06',
        'display_ref': 'Matt 12:24-34',
        'canonical_mt_ref': 'Matt 12:24-34',
        'canonical_lxx_ref': 'Matt 12:24-34',
        'spans_json': '[{"book": "Matt", "canonical_lxx_ref": "Matt 12:24-34", "canonical_mt_ref": "Matt 12:24-34", "chapter_end": 12, "chapter_start": 12, "confidence": "high", "source_convention": "modern_english_reference", "source_ref": "Matt 12:24-34", "validation_basis": "", "verse_end": 34, "verse_start": 24}]',
    },
    'Ps 6:1-2': {
        'identity_key': 'rid_7727752ced614b97f28b',
        'display_ref': 'Ps 6:1-2 (LXX Ps 6:2-3)',
        'canonical_mt_ref': 'Ps 6:1-2',
        'canonical_lxx_ref': 'Ps 6:2-3',
        'spans_json': '[{"book": "Ps", "canonical_lxx_ref": "Ps 6:2-3", "canonical_mt_ref": "Ps 6:1-2", "chapter_end": 6, "chapter_start": 6, "confidence": "high", "source_convention": "mt_nkjv", "source_ref": "Ps 6:1-2", "validation_basis": "known_content_compared_mt_to_lxx_equivalence", "verse_end": 2, "verse_start": 1}]',
    },
    'Isa 1:2-18': {
        'identity_key': 'rid_e6af0766ab457676feb2',
        'display_ref': 'Isa 1:2-18',
        'canonical_mt_ref': 'Isa 1:2-18',
        'canonical_lxx_ref': 'Isa 1:2-18',
        'spans_json': '[{"book": "Isa", "canonical_lxx_ref": "Isa 1:2-18", "canonical_mt_ref": "Isa 1:2-18", "chapter_end": 1, "chapter_start": 1, "confidence": "high", "source_convention": "modern_english_reference", "source_ref": "Isa 1:2-18", "validation_basis": "", "verse_end": 18, "verse_start": 2}]',
    },
    'Exod 2:23-3:5': {
        'identity_key': 'rid_797c61fedd32edc49a1e',
        'display_ref': 'Exod 2:23-3:5',
        'canonical_mt_ref': 'Exod 2:23-3:5',
        'canonical_lxx_ref': 'Exod 2:23-3:5',
        'spans_json': '[{"book": "Exod", "canonical_lxx_ref": "Exod 2:23-3:5", "canonical_mt_ref": "Exod 2:23-3:5", "chapter_end": 3, "chapter_start": 2, "confidence": "high", "source_convention": "modern_english_reference", "source_ref": "Exod 2:23-3:5", "validation_basis": "", "verse_end": 5, "verse_start": 23}]',
    },
}

ANNUAL_RULES = (
    {
        'daily_occasions': {'Tout 16', 'Tut 16'},
        'coptic_keys': {'tout-16'},
        'slot': 'Catholic Epistle',
        'old': '2Pet 2:1-10',
        'new': '1Pet 1:25-2:10',
        'bad_occasions': {'Tut 16', 'Tout 16'},
        'good_occasion': 'Tut 16',
    },
    {
        'daily_occasions': {'Tout 17 (Feast of the Cross)', 'Tut 17 (Feast of the Cross)'},
        'coptic_keys': {'tout-17'},
        'slot': 'Catholic Epistle',
        'old': '1Pet 2:1-25',
        'new': '1Pet 2:11-25',
        'bad_occasions': {'Non-Sunday Tut 17 (Feast of the Cross)'},
        'good_occasion': 'Tut 17 (Feast of the Cross)',
    },
    {
        'daily_occasions': {'Tout 19 (Feast of the Cross)', 'Tut 19 (Feast of the Cross)'},
        'coptic_keys': {'tout-19'},
        'slot': 'Gospel',
        'old': 'Lk 14:25-32',
        'new': 'Lk 14:25-35',
        'bad_occasions': {'Non-Sunday Tut 19 (Feast of the Cross)'},
        'good_occasion': 'Tut 19 (Feast of the Cross)',
    },
    {
        'daily_occasions': {'Babah 27', 'Baba 27'},
        'coptic_keys': {'baba-27', 'babah-27'},
        'slot': 'Gospel',
        'old': 'Matt 5:1-16',
        'new': 'Matt 4:23-5:16',
        'bad_occasions': {'Babah 27', 'Baba 27'},
        'good_occasion': 'Babah 27',
    },
)


def _sunday(row):
    occasion = row.get('occasion') or ''
    label = row.get('display_label') or ''
    return occasion.startswith('Sunday') or label.startswith('Sunday') or bool(row.get('annual_sunday'))


def _replace_ref(value, old, new):
    if not isinstance(value, str) or old not in value:
        return value
    return value.replace(old, new)


def _apply_identity(row, old, new_key):
    identity = IDENTITIES[new_key]
    for field, value in identity.items():
        row[field] = value
    for field in ('source_locator', 'source_disclosure', 'source_group_key'):
        if field in row:
            row[field] = _replace_ref(row.get(field), old, identity['canonical_mt_ref'])
    locators = row.get('calendar_review_source_locators')
    if isinstance(locators, list):
        row['calendar_review_source_locators'] = [_replace_ref(item, old, identity['canonical_mt_ref']) for item in locators]
    row['superseded_by_ref'] = ''
    return row


def _matches_annual(row, rule):
    if _sunday(row) or row.get('removed_marker'):
        return False
    if row.get('slot') != rule['slot'] or row.get('service_section') != 'Liturgy':
        return False
    if (row.get('display_ref') or row.get('canonical_mt_ref')) != rule['old']:
        return False
    occasion = row.get('occasion') or ''
    key = row.get('coptic_date_key') or ''
    return occasion in rule['daily_occasions'] or key in rule['coptic_keys']


def repair_daily(days):
    output = {}
    for date, rows in days.items():
        repaired = []
        for row in rows:
            updated = copy.deepcopy(row)
            for rule in ANNUAL_RULES:
                if _matches_annual(updated, rule):
                    _apply_identity(updated, rule['old'], rule['new'])
                    break
            repaired.append(updated)
        output[date] = _repair_lent_monday(repaired, date)
    return output


def _reader_row(template, slot, slot_type, slot_order, identity_key, locator):
    row = copy.deepcopy(template)
    identity = IDENTITIES[identity_key]
    row.update(identity)
    row.update(
        occasion=LENT_OCCASION,
        service_section='Matins',
        service_hour='',
        slot=slot,
        slot_type=slot_type,
        slot_order=slot_order,
        reading_type='scripture',
        reading_name='',
        removed_marker='',
        current_status='current_public_or_local_reference',
        source_kind='annual_reader_identity_repair',
        source_family='annual_reader_identity_repair',
        source_file=locator.split(';')[0].strip(),
        source_locator=locator,
        source_row_id='2026-02-16:' + slot,
        source_group_key='coptic_reader_matins|2026-02-16|First Monday of Great Fast|Matins|' + slot,
        superseded_by_ref='',
        coptic_date_key='amshir-9',
    )
    if 'display_label' in template or 'display_label' in row:
        row['display_label'] = LENT_OCCASION
    disclosure = {
        'source_kind': 'annual_reader_identity_repair',
        'source_family': 'annual_reader_identity_repair',
        'source_file': row['source_file'],
        'source_row_id': row['source_row_id'],
        'scope': '2026-02-16 Matins only; recurrence and Liturgy not approved',
    }
    row['source_disclosure'] = json.dumps([disclosure], ensure_ascii=False, separators=(',', ':'))
    return row


def _repair_lent_monday(rows, date):
    if date != LENT_DATE:
        return rows
    if any(row.get('service_section') == 'Matins' and row.get('canonical_mt_ref') == 'Matt 12:24-34'
           and not row.get('removed_marker') for row in rows):
        return rows
    template = next(row for row in rows if row.get('service_section') == 'Matins' and row.get('slot') == 'Gospel')
    matins = [
        _reader_row(template, 'OT1', 'prophecy', 1, 'Exod 2:23-3:5', PROPHECY_LOCATOR),
        _reader_row(template, 'OT2', 'prophecy', 2, 'Isa 1:2-18', PROPHECY_LOCATOR),
        _reader_row(template, 'Psalm', 'psalm', 3, 'Ps 6:1-2', PSALM_GOSPEL_LOCATOR),
        _reader_row(template, 'Gospel', 'gospel', 4, 'Matt 12:24-34', PSALM_GOSPEL_LOCATOR),
    ]
    vespers = [row for row in rows if row.get('service_section') == 'Vespers']
    rest = [row for row in rows if row.get('service_section') not in {'Vespers', 'Matins'}]
    output = vespers + matins + rest
    for index, row in enumerate(output, 1):
        row['reading_order'] = index
    return output


def _fresh_identity(label):
    return 'rid_' + hashlib.sha256(('annual-occasion-repair|' + label).encode()).hexdigest()[:20]


def _years(value):
    return [int(part) for part in str(value or '').split(';') if part.strip().isdigit()]


def _write_years(row, years):
    years = sorted(set(years))
    text = '; '.join(str(year) for year in years)
    row['attestation_years'] = text
    row['attestation_year_min'] = str(years[0]) if years else ''
    row['attestation_year_max'] = str(years[-1]) if years else ''
    row['collapsed_row_count'] = str(len(years))
    row['occurs_in_shipped_years'] = any(year in {2026, 2027, 2028} for year in years)
    disclosure = row.get('source_disclosure')
    if isinstance(disclosure, str) and disclosure.startswith('['):
        try:
            parsed = json.loads(disclosure)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
            parsed[0]['attested_year_min'] = row['attestation_year_min']
            parsed[0]['attested_year_max'] = row['attestation_year_max']
            row['source_disclosure'] = json.dumps(parsed, ensure_ascii=False, separators=(',', ':'))
    return years


def _current_public(row):
    return (not row.get('removed_marker') and row.get('source_family') == 'ordinary_date_resolved'
            and row.get('service_section') == 'Liturgy')


def repair_reverse_rows(rows):
    """Retire the uncorrected public rows and add a dated repair witness.

    Existing attestation fields stay untouched. The 1.3.8 restore contract
    treats those fields as owned by an earlier layer, so a new witness carries
    the transferred years instead of rewriting the predecessor row.
    """
    output = [copy.deepcopy(row) for row in rows]
    additions = []
    for rule in ANNUAL_RULES:
        bad = [row for row in output if _current_public(row) and row.get('occasion') in rule['bad_occasions']
               and row.get('slot') == rule['slot'] and row.get('display_ref') == rule['old']
               and not _sunday(row)]
        if not bad:
            continue
        identity = _fresh_identity(rule['good_occasion'] + '|' + rule['slot'] + '|' + rule['new'])
        if any(row.get('identity_key') == identity for row in output):
            continue
        years = []
        for row in bad:
            years.extend(_years(row.get('attestation_years')))
            row['removed_marker'] = SUPERSEDED
            row['current_status'] = 'superseded_by_annual_reader_identity_repair'
            row['occurs_in_shipped_years'] = False
        witness = copy.deepcopy(bad[0])
        witness['removed_marker'] = ''
        witness['current_status'] = 'current_public_or_local_reference'
        _apply_identity(witness, rule['old'], rule['new'])
        witness['identity_key'] = identity
        witness['source_locator'] = 'annual_occasion_repairs.py:' + rule['new']
        witness['source_file'] = 'annual_occasion_repairs.py'
        witness['source_kind'] = 'annual_reader_identity_repair'
        witness['source_family'] = 'annual_reader_identity_repair'
        witness['source_title'] = 'Coptic Reader annual identity repair applied to non-Sunday years'
        for field in ('coptic_date_key', 'annual_sunday', 'calendar_review_status'):
            witness[field] = ''
        witness['calendar_review_source_locators'] = []
        witness['calendar_review_calendar_keys'] = []
        _write_years(witness, years)
        additions.append(witness)
    output.extend(additions)
    return _repair_lent_reverse(output)


def _lent_reverse_row(template, slot, slot_type, identity_key, locator):
    row = copy.deepcopy(template)
    row.update(IDENTITIES[identity_key])
    row['identity_key'] = _fresh_identity('2026-02-16|Matins|' + slot)
    row.update(
        occasion=LENT_OCCASION,
        display_label=LENT_OCCASION,
        calendar_keys=LENT_OCCASION,
        day_titles=LENT_OCCASION,
        service_section='Matins',
        service_hour='',
        slot=slot,
        slot_type=slot_type,
        reading_type='scripture',
        removed_marker='',
        current_status='current_public_or_local_reference',
        source_kind='annual_reader_identity_repair',
        source_family='annual_reader_identity_repair',
        source_file=locator.split(';')[0].strip(),
        source_locator=locator,
        source_title='Coptic Reader accepted First Monday of Great Fast Matins, 2026-02-16 only',
        coptic_date_key='',
        annual_sunday='',
        calendar_review_status='',
        calendar_review_source_locators=[],
        calendar_review_calendar_keys=[],
    )
    _write_years(row, [2026])
    return row


def _repair_lent_reverse(rows):
    if any(row.get('occasion') == LENT_OCCASION and row.get('canonical_mt_ref') == 'Matt 12:24-34'
           and not row.get('removed_marker') for row in rows):
        return rows
    templates = [row for row in rows if row.get('occasion') == 'Great Lent' and row.get('service_section') == 'Matins'
                 and not row.get('removed_marker') and _years(row.get('attestation_years')) == [2026]]
    if not templates:
        return rows
    for row in templates:
        row['removed_marker'] = SUPERSEDED
        row['current_status'] = 'superseded_by_annual_reader_identity_repair'
        row['occurs_in_shipped_years'] = False
    template = templates[-1]
    rows.extend([
        _lent_reverse_row(template, 'OT1', 'prophecy', 'Exod 2:23-3:5', PROPHECY_LOCATOR),
        _lent_reverse_row(template, 'OT2', 'prophecy', 'Isa 1:2-18', PROPHECY_LOCATOR),
        _lent_reverse_row(template, 'Psalm', 'psalm', 'Ps 6:1-2', PSALM_GOSPEL_LOCATOR),
        _lent_reverse_row(template, 'Gospel', 'gospel', 'Matt 12:24-34', PSALM_GOSPEL_LOCATOR),
    ])
    return rows


CACHE_REPLACEMENTS = (
    (('2027-09-27', '2028-09-26'), 'Liturgy', 'Catholic Epistle', '2Pet 2:1-10', '1Pet 1:25-2:10'),
    (('2028-09-27',), 'Liturgy', 'Catholic Epistle', '1Pet 2:1-25', '1Pet 2:11-25'),
    (('2027-09-30', '2028-09-29'), 'Liturgy', 'Gospel', 'Lk 14:25-32', 'Lk 14:25-35'),
    (('2028-11-06',), 'Liturgy', 'Gospel', 'Matt 5:1-16', 'Matt 4:23-5:16'),
)
LENT_CACHE_REFS = {'Lk 13:23-30', 'Ps 89:19', 'Ps 89:24'}
LENT_PACKAGE_REFS = {'Exod 2:23-3:5', 'Isa 1:2-18', 'Ps 6:1-2', 'Matt 12:24-34'}


def _issue(issues, year, date, status):
    issues.append(dict(year=year, status=status, count=1, gregorian_date=date,
                       service_section='', reading_type_or_slot='', normalized_ref=''))


def apply_cache_comparison(source_rows, daily, year, additions, retired, dispositions, issues, source_signature):
    """Retire only the exact cached predecessors these Reader repairs replace."""
    from pathlib import Path
    for dates, section, slot, old, new in CACHE_REPLACEMENTS:
        for date in dates:
            if not date.startswith(str(year)) or date not in daily:
                continue
            package_rows = [row for row in daily[date] if row.get('service_section') == section
                            and row.get('slot') == slot and row.get('display_ref') == new
                            and not row.get('removed_marker')]
            cache_rows = [row for row in source_rows if row.get('gregorian_date') == date
                          and row.get('service_section') == section and row.get('reading_type') == slot
                          and row.get('matched_ref') == old]
            if len(package_rows) != 1 or len(cache_rows) != 1:
                _issue(issues, year, date, 'invalid_annual_reader_identity_repair')
                continue
            for row in cache_rows:
                retired[source_signature(row)] += 1
                dispositions.append(dict(year=year, gregorian_date=date, occasion=row.get('day_title', ''),
                                         service_section=section, count=1, normalized_ref=old,
                                         disposition='authenticated_annual_reader_cached_retirement',
                                         evidence='annual_occasion_repairs.py', evidence_sha256=''))
            additions.append((date, package_rows[0]))
            dispositions.append(dict(year=year, gregorian_date=date, occasion=package_rows[0].get('occasion', ''),
                                     service_section=section, count=1, normalized_ref=new,
                                     disposition='source_qualified_annual_reader_identity_repair',
                                     evidence='annual_occasion_repairs.py', evidence_sha256=''))
    if not LENT_DATE.startswith(str(year)) or LENT_DATE not in daily:
        return
    for locator in (PROPHECY_LOCATOR, PSALM_GOSPEL_LOCATOR):
        relative, digest = locator.split(';')[0].strip(), locator.split('sha256=')[1]
        if hashlib.sha256(Path(relative).read_bytes()).hexdigest() != digest:
            raise ValueError('Lent Reader evidence drift: ' + relative)
    package_rows = [row for row in daily[LENT_DATE] if row.get('service_section') == 'Matins'
                    and row.get('canonical_mt_ref') in LENT_PACKAGE_REFS and not row.get('removed_marker')]
    cache_rows = [row for row in source_rows if row.get('gregorian_date') == LENT_DATE
                  and row.get('service_section') == 'Matins' and row.get('matched_ref') in LENT_CACHE_REFS]
    if len(package_rows) != 4 or len(cache_rows) != 3:
        _issue(issues, year, LENT_DATE, 'invalid_lent_monday_reader_repair')
        return
    for row in cache_rows:
        retired[source_signature(row)] += 1
        dispositions.append(dict(year=year, gregorian_date=LENT_DATE, occasion=row.get('day_title', ''),
                                 service_section='Matins', count=1, normalized_ref=row.get('matched_ref'),
                                 disposition='authenticated_lent_monday_cached_retirement',
                                 evidence=PROPHECY_LOCATOR, evidence_sha256=PROPHECY_LOCATOR.split('sha256=')[1]))
    for row in package_rows:
        additions.append((LENT_DATE, row))
        dispositions.append(dict(year=year, gregorian_date=LENT_DATE, occasion=row.get('occasion', ''),
                                 service_section='Matins', count=1, normalized_ref=row.get('display_ref'),
                                 disposition='source_qualified_lent_monday_reader_repair',
                                 evidence=row.get('source_locator', ''), evidence_sha256=''))
