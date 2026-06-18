#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, List, Optional

from convertdate import coptic

from passage_normalization import BOOK_ABBREV, canonicalize_text_ref, extract_text_ref_tokens, parse_passage

WORK = Path(__file__).resolve().parent


def env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name)
    return Path(value).expanduser() if value else default


def env_flag(name: str) -> bool:
    return os.environ.get(name, '').strip().lower() in {'1', 'true', 'yes', 'on'}


VAULT = Path('/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault')
REF = VAULT / 'Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary'
LOCAL = REF / 'Coptic Orthodox Lectionary Reference'
DISABLE_VAULT_PUBLISH = env_flag('LECTIONARY_DISABLE_VAULT_PUBLISH')
VAULT_DATA = env_path('LECTIONARY_VAULT_DATA', LOCAL / 'data')
WORK_OUT_DATA = env_path('LECTIONARY_WORK_OUT_DATA', WORK / 'out' / 'data')
OUT = env_path('LECTIONARY_CROSSWALK_OUT', WORK / 'out4')
PASCHA_CSV = WORK_OUT_DATA / 'pascha_day_hour_index.csv'
PASCHA_JSONL = WORK_OUT_DATA / 'pascha_day_hour_index.jsonl'
PASCHA_SOURCE_TEXT_CSV = WORK_OUT_DATA / 'pascha_source_text_index.csv'
PASCHA_SOURCE_TEXT_JSONL = WORK_OUT_DATA / 'pascha_source_text_index.jsonl'
BRIGHT_CSV = WORK_OUT_DATA / 'bright_saturday_service_order.csv'
BRIGHT_JSONL = WORK_OUT_DATA / 'bright_saturday_service_order.jsonl'
PASCHA_FALLBACK_CSV = WORK / 'out2' / 'pascha_day_hour_index.csv'
PASCHA_FALLBACK_JSONL = WORK / 'out2' / 'pascha_day_hour_index.jsonl'
BRIGHT_FALLBACK_CSV = WORK / 'out_bright' / 'bright_saturday_service_order.csv'
BRIGHT_FALLBACK_JSONL = WORK / 'out_bright' / 'bright_saturday_service_order.jsonl'
OUT.mkdir(parents=True, exist_ok=True)
WORK_OUT_DATA.mkdir(parents=True, exist_ok=True)
if not DISABLE_VAULT_PUBLISH:
    VAULT_DATA.mkdir(parents=True, exist_ok=True)

BOOK_NAME_BY_ABBREV = {}
for name, abbrev in BOOK_ABBREV.items():
    BOOK_NAME_BY_ABBREV.setdefault(abbrev, name)
BOOK_NAME_BY_ABBREV['Ps'] = 'Psalms'
BOOK_NAME_BY_ABBREV['Wis'] = 'Wisdom of Solomon'

FIELDS = [
    'passage',
    'source_kind',
    'source_family',
    'source_table',
    'source_file',
    'source_row_id',
    'liturgical_place',
    'calendar_key',
    'gregorian_date',
    'coptic_date',
    'day_title',
    'service_day',
    'service_hour',
    'service_section',
    'reading_slot',
    'reading_type',
    'source_ref',
    'raw_ref',
    'normalized_ref',
    'normalized_segment',
    'book',
    'book_abbrev',
    'chapter_start',
    'verse_start',
    'chapter_end',
    'verse_end',
    'significance_note',
    'synaxarium_note',
    'url',
    'provenance',
]

SUMMARY_FIELDS = [
    'passage',
    'cycle_occurrences',
    'date_occurrences',
    'special_service_occurrences',
    'agpeya_occurrences',
    'pascha_occurrences',
    'pascha_source_text_occurrences',
    'bright_saturday_occurrences',
    'total_occurrences',
]


def read_csv(path: Path) -> List[dict]:
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Iterable[dict], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def norm_passage(row: dict) -> str:
    p = row.get('normalized_segment') or row.get('matched_ref') or row.get('normalized_ref') or row.get('canonical_ref') or row.get('raw_ref') or ''
    p = re.sub(r'\s+', ' ', p).strip()
    return canonicalize_text_ref(p)


def norm_key(value: str) -> str:
    return re.sub(r'\s+', ' ', (value or '').strip()).casefold()


def pascha_day_passage_key(day: str, passage: str) -> tuple[str, str]:
    return (norm_key(day), canonicalize_text_ref(passage))


# Known Pascha source-text mis-extractions confirmed absent from the official
# Wednesday Pascha hours after checking the St. Mary Ottawa Pascha book. This
# exclusion list can grow as more source-text extraction errors are confirmed.
KNOWN_PASCHA_SOURCE_TEXT_MISEXTRACTIONS = {
    pascha_day_passage_key('Wednesday', 'Isa 48:1-6'),
}


def pascha_ref_correction_key(day: str, hour: str, slot: str, refs: str) -> tuple[str, str, str, str]:
    return (
        norm_key(day),
        norm_key(hour),
        norm_key(slot),
        re.sub(r'\s+', ' ', (refs or '').replace('—', '-').replace('–', '-').strip()).casefold(),
    )


PASCHA_CURATED_REF_CORRECTIONS = {
    pascha_ref_correction_key('Great Thursday', 'Third Hour', 'OT2', 'Wis 24:1-11'): {
        'refs': 'Sir 24:1-11',
        'note': 'source_corrected_from_katameros_api_2026_06_18; live API returned Sir 24:1-11',
    },
}


def apply_pascha_curated_ref_correction(row: dict) -> dict:
    key = pascha_ref_correction_key(
        row.get('day', ''),
        row.get('hour', ''),
        row.get('slot', ''),
        row.get('refs', ''),
    )
    correction = PASCHA_CURATED_REF_CORRECTIONS.get(key)
    if not correction:
        return row
    corrected = dict(row)
    corrected['_raw_refs'] = row.get('refs', '')
    corrected['_ref_correction_note'] = correction['note']
    corrected['refs'] = correction['refs']
    return corrected


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def sample_pascha_row(row: dict, passage: str, **extra: object) -> dict:
    sample = {
        'day': row.get('day', ''),
        'hour': row.get('hour', ''),
        'reading_type': row.get('reading_type', ''),
        'raw_ref': row.get('raw_ref', ''),
        'normalized_ref': row.get('normalized_ref', ''),
        'passage': passage,
        'source_line': row.get('source_line', ''),
        'source_page': row.get('source_page', ''),
    }
    sample.update(extra)
    return sample


def coptic_date_for(gregorian_date: str) -> str:
    if not gregorian_date:
        return ''
    try:
        y, m, d = map(int, gregorian_date.split('-'))
        cy, cm, cd = coptic.from_gregorian(y, m, d)
        return f'{cy}-{cm:02d}-{cd:02d}'
    except Exception:
        return ''


def passage_fields(passage: str) -> dict:
    parsed = parse_passage(passage)
    if not parsed or not parsed.parts:
        return {
            'book': '',
            'book_abbrev': '',
            'chapter_start': '',
            'verse_start': '',
            'chapter_end': '',
            'verse_end': '',
        }
    first = parsed.parts[0]
    last = parsed.parts[-1]
    return {
        'book': BOOK_NAME_BY_ABBREV.get(parsed.book_abbrev, ''),
        'book_abbrev': parsed.book_abbrev,
        'chapter_start': first.chapter_start,
        'verse_start': first.verse_start if first.verse_start is not None else '',
        'chapter_end': last.chapter_end,
        'verse_end': last.verse_end if last.verse_end is not None else '',
    }


def add_row(rows: List[dict], summary_counts: dict[str, Counter], passage: str, source_kind: str, **kwargs) -> None:
    passage = canonicalize_text_ref(passage)
    if not passage:
        return
    base = {field: '' for field in FIELDS}
    base.update({
        'passage': passage,
        'source_kind': source_kind,
        'normalized_segment': passage,
    })
    base.update(passage_fields(passage))
    base.update({k: '' if v is None else v for k, v in kwargs.items()})
    rows.append(base)
    summary_counts[passage][source_kind] += 1


def main() -> None:
    cycle_rows = read_csv(WORK_OUT_DATA / 'katameros_cycle_passage_index.csv')
    date_rows = read_csv(WORK_OUT_DATA / 'copticchurch_passage_index_2020_2035.csv')
    special_rows = read_csv(WORK_OUT_DATA / 'special_service_passage_index.csv')
    agpeya_rows = read_csv(WORK_OUT_DATA / 'agpeya_passage_index.csv')
    pascha_source = PASCHA_CSV if PASCHA_CSV.exists() else PASCHA_FALLBACK_CSV
    pascha_jsonl_source = PASCHA_JSONL if PASCHA_JSONL.exists() else PASCHA_FALLBACK_JSONL
    bright_source = BRIGHT_CSV if BRIGHT_CSV.exists() else BRIGHT_FALLBACK_CSV
    bright_jsonl_source = BRIGHT_JSONL if BRIGHT_JSONL.exists() else BRIGHT_FALLBACK_JSONL
    pascha_rows = read_csv(pascha_source)
    pascha_source_text_rows = read_csv(PASCHA_SOURCE_TEXT_CSV)
    bright_rows = read_csv(bright_source)

    rows: List[dict] = []
    summary_counts: dict[str, Counter] = defaultdict(Counter)

    for idx, row in enumerate(cycle_rows, 1):
        passage = norm_passage(row)
        add_row(
            rows,
            summary_counts,
            passage,
            'katameros_cycle',
            source_family='katameros_cycle',
            source_table=row.get('source_table') or '',
            source_file='sources/katameros-api/Core/KatamerosDatabase.db',
            source_row_id=idx,
            liturgical_place=row.get('source_type') or row.get('cycle') or '',
            calendar_key=row.get('day_key') or '',
            coptic_date=f"{row.get('month_name','')} {row.get('day','')}",
            day_title=row.get('day_name') or '',
            service_day=row.get('day_name') or row.get('day_key') or '',
            service_section=row.get('reading_slot') or '',
            reading_slot=row.get('reading_slot') or '',
            reading_type=row.get('source_table') or '',
            source_ref=row.get('normalized_segment') or row.get('canonical_segment') or row.get('normalized_ref') or row.get('raw_ref') or '',
            raw_ref=row.get('raw_ref') or '',
            normalized_ref=row.get('normalized_ref') or row.get('normalized_segment') or '',
            significance_note=row.get('season') or row.get('other') or row.get('day_name') or '',
            provenance=row.get('source') or 'katameros-api sqlite',
        )

    for idx, row in enumerate(date_rows, 1):
        passage = norm_passage(row)
        g = row.get('gregorian_date') or ''
        add_row(
            rows,
            summary_counts,
            passage,
            'copticchurch_date',
            source_family='ordinary_date_resolved',
            source_table='copticchurch_date_readings_2020_2035',
            source_file='cache/copticchurch_html',
            source_row_id=idx,
            liturgical_place=row.get('day_title') or '',
            calendar_key=row.get('day_title') or '',
            gregorian_date=g,
            coptic_date=coptic_date_for(g),
            day_title=row.get('day_title') or '',
            service_day=row.get('day_title') or '',
            service_section=row.get('service_section') or '',
            reading_type=row.get('reading_type') or '',
            source_ref=row.get('matched_ref') or row.get('raw_ref') or '',
            raw_ref=row.get('raw_ref') or '',
            normalized_ref=row.get('matched_ref') or '',
            significance_note=row.get('service_section') or row.get('reading_type') or '',
            url=row.get('url') or '',
            provenance=row.get('source') or 'copticchurch.net daily scrape',
        )

    for idx, row in enumerate(special_rows, 1):
        passage = norm_passage(row)
        add_row(
            rows,
            summary_counts,
            passage,
            'special_service',
            source_family=row.get('service_family') or 'special_service',
            source_table='special_service_passage_index',
            source_file='build_special_service_reference.py curated rows',
            source_row_id=idx,
            liturgical_place=row.get('service_family') or 'special_service',
            calendar_key=row.get('service_variant') or '',
            day_title=row.get('service_family') or '',
            service_day=row.get('service_family') or '',
            service_section=row.get('section') or '',
            reading_slot=row.get('section') or '',
            reading_type=row.get('reading_type') or '',
            source_ref=row.get('matched_ref') or row.get('canonical_ref') or row.get('raw_ref') or '',
            raw_ref=row.get('raw_ref') or '',
            normalized_ref=row.get('canonical_ref') or row.get('matched_ref') or '',
            significance_note=row.get('notes') or '',
            url=row.get('source_url') or row.get('source_page') or '',
            provenance=row.get('source_title') or 'curated special-service data',
        )

    for idx, row in enumerate(agpeya_rows, 1):
        passage = norm_passage(row)
        add_row(
            rows,
            summary_counts,
            passage,
            'agpeya',
            source_family=row.get('prayer_group') or 'agpeya',
            source_table='agpeya_passage_index',
            source_file='build_agpeya_reference.py curated rows',
            source_row_id=idx,
            liturgical_place=row.get('prayer_group') or 'agpeya',
            calendar_key=row.get('prayer_key') or '',
            day_title=row.get('prayer_name') or row.get('prayer_key') or 'Agpeya',
            service_day=row.get('prayer_group') or 'Agpeya',
            service_hour=row.get('prayer_name') or row.get('prayer_key') or '',
            service_section=row.get('prayer_name') or row.get('prayer_key') or '',
            reading_slot=row.get('reading_type') or '',
            reading_type=row.get('reading_type') or '',
            source_ref=row.get('matched_ref') or row.get('canonical_ref') or row.get('raw_ref') or '',
            raw_ref=row.get('raw_ref') or '',
            normalized_ref=row.get('canonical_ref') or row.get('matched_ref') or '',
            significance_note=row.get('notes') or '',
            url=row.get('source_url') or row.get('source_page') or '',
            provenance=row.get('source_title') or 'curated Agpeya data',
        )

    pascha_day_hour_keys: set[tuple[str, str]] = set()

    for idx, row in enumerate(pascha_rows, 1):
        corrected_row = apply_pascha_curated_ref_correction(row)
        source_refs = corrected_row.get('refs', '')
        raw_refs = corrected_row.get('_raw_refs') or row.get('refs', '')
        correction_note = corrected_row.get('_ref_correction_note', '')
        significance_note = f"Pascha source={row.get('source','')}"
        if correction_note:
            significance_note = f"{significance_note}; {correction_note}"
        for token in extract_text_ref_tokens(source_refs):
            passage = canonicalize_text_ref(token)
            pascha_day_hour_keys.add(pascha_day_passage_key(row.get('day', ''), passage))
            add_row(
                rows,
                summary_counts,
                passage,
                'pascha_day_hour',
                source_family='holy_pascha_curated_day_hour',
                source_table='pascha_day_hour_index',
                source_file=display_path(pascha_source) if pascha_source.exists() else '',
                source_row_id=idx,
                liturgical_place=row.get('day') or '',
                calendar_key=f"{row.get('day','')} | {row.get('hour','')}",
                day_title=row.get('day') or '',
                service_day=row.get('day') or '',
                service_hour=row.get('hour') or '',
                service_section=row.get('hour') or '',
                reading_slot=row.get('slot') or '',
                reading_type=row.get('slot') or '',
                source_ref=source_refs or token,
                raw_ref=raw_refs,
                normalized_ref=passage,
                significance_note=significance_note,
                provenance=row.get('source') or 'pascha_day_hour_index',
            )

    pascha_source_text_input_rows = len(pascha_source_text_rows)
    pascha_source_text_comparable_rows = 0
    pascha_source_text_dropped_count = 0
    pascha_source_text_quarantined_count = 0
    pascha_source_text_kept_count = 0
    pascha_source_text_dropped_samples = []
    pascha_source_text_quarantined_samples = []
    pascha_source_text_kept_samples = []

    for idx, row in enumerate(pascha_source_text_rows, 1):
        token = row.get('normalized_ref') or ''
        if not token:
            continue
        passage = canonicalize_text_ref(token)
        pascha_source_text_comparable_rows += 1
        dedupe_key = pascha_day_passage_key(row.get('day', ''), passage)
        if dedupe_key in KNOWN_PASCHA_SOURCE_TEXT_MISEXTRACTIONS:
            pascha_source_text_quarantined_count += 1
            if len(pascha_source_text_quarantined_samples) < 50:
                pascha_source_text_quarantined_samples.append(sample_pascha_row(row, passage))
            continue
        if dedupe_key in pascha_day_hour_keys:
            pascha_source_text_dropped_count += 1
            if len(pascha_source_text_dropped_samples) < 50:
                pascha_source_text_dropped_samples.append(sample_pascha_row(row, passage))
            continue
        pascha_source_text_kept_count += 1
        if len(pascha_source_text_kept_samples) < 50:
            pascha_source_text_kept_samples.append(sample_pascha_row(row, passage))
        add_row(
            rows,
            summary_counts,
            passage,
            'pascha_source_text',
            source_family=row.get('source_family') or 'holy_pascha',
            source_table='pascha_source_text_index',
            source_file=row.get('source_file') or display_path(PASCHA_SOURCE_TEXT_CSV),
            source_row_id=row.get('source_line') or idx,
            liturgical_place=row.get('day') or '',
            calendar_key=f"{row.get('day','')} | {row.get('hour','')}",
            day_title=row.get('day') or '',
            service_day=row.get('day') or '',
            service_hour=row.get('hour') or '',
            service_section=row.get('hour') or '',
            reading_slot=row.get('reading_type') or '',
            reading_type=row.get('reading_type') or '',
            source_ref=row.get('normalized_ref') or row.get('raw_ref') or '',
            raw_ref=row.get('raw_ref') or '',
            normalized_ref=passage,
            significance_note=row.get('provenance_note') or '',
            provenance=f"{row.get('source_file','')}:{row.get('source_line','')}",
        )

    for idx, row in enumerate(bright_rows, 1):
        for token in extract_text_ref_tokens(row.get('reference', '')):
            passage = canonicalize_text_ref(token)
            add_row(
                rows,
                summary_counts,
                passage,
                'bright_saturday_service_order',
                source_family='bright_saturday',
                source_table='bright_saturday_service_order',
                source_file=display_path(bright_source) if bright_source.exists() else '',
                source_row_id=idx,
                liturgical_place=row.get('section') or row.get('subsection') or 'Bright Saturday',
                calendar_key=f"Bright Saturday | {row.get('subsection','') or row.get('section','')}",
                day_title='Bright Saturday',
                service_day='Bright Saturday',
                service_section=row.get('subsection') or row.get('section') or '',
                reading_slot=row.get('reading_name') or '',
                reading_type=row.get('reading_name') or '',
                source_ref=row.get('reference') or token,
                raw_ref=row.get('reference') or '',
                normalized_ref=passage,
                significance_note=row.get('notes') or '',
                provenance='bright_saturday_service_order',
            )

    rows.sort(key=lambda r: (r['passage'], r['source_kind'], str(r['calendar_key']), str(r['service_section']), str(r['source_row_id'])))

    csv_path = OUT / 'reverse_lookup_crosswalk.csv'
    jsonl_path = OUT / 'reverse_lookup_crosswalk.jsonl'
    write_csv(csv_path, rows, FIELDS)
    write_jsonl(jsonl_path, rows)

    summary = []
    for passage in sorted(summary_counts):
        counts = summary_counts[passage]
        cycle = counts['katameros_cycle']
        date = counts['copticchurch_date']
        special = counts['special_service']
        agpeya = counts['agpeya']
        pascha = counts['pascha_day_hour']
        pascha_text = counts['pascha_source_text']
        bright = counts['bright_saturday_service_order']
        summary.append({
            'passage': passage,
            'cycle_occurrences': cycle,
            'date_occurrences': date,
            'special_service_occurrences': special,
            'agpeya_occurrences': agpeya,
            'pascha_occurrences': pascha,
            'pascha_source_text_occurrences': pascha_text,
            'bright_saturday_occurrences': bright,
            'total_occurrences': cycle + date + special + agpeya + pascha + pascha_text + bright,
        })

    summary_path = OUT / 'reverse_lookup_summary.csv'
    write_csv(summary_path, summary, SUMMARY_FIELDS)

    dedupe_report = {
        'pascha_source_text_input_rows': pascha_source_text_input_rows,
        'pascha_source_text_comparable_rows': pascha_source_text_comparable_rows,
        'dropped_duplicate_count': pascha_source_text_dropped_count,
        'quarantined_misextraction_count': pascha_source_text_quarantined_count,
        'total_dropped_count': pascha_source_text_dropped_count + pascha_source_text_quarantined_count,
        'kept_unique_count': pascha_source_text_kept_count,
        'match_key': 'same normalized day + same canonical normalized passage segment',
        'dropped_duplicate_samples': pascha_source_text_dropped_samples,
        'quarantined_misextraction_samples': pascha_source_text_quarantined_samples,
        'kept_unique_samples': pascha_source_text_kept_samples,
    }
    for src in [
        pascha_source,
        pascha_jsonl_source,
        PASCHA_SOURCE_TEXT_CSV,
        PASCHA_SOURCE_TEXT_JSONL,
        bright_source,
        bright_jsonl_source,
        csv_path,
        jsonl_path,
        summary_path,
    ]:
        if src.exists():
            target_dirs = [WORK_OUT_DATA]
            if not DISABLE_VAULT_PUBLISH:
                target_dirs.append(VAULT_DATA)
            for target_dir in target_dirs:
                dst = target_dir / src.name
                if src.resolve() == dst.resolve():
                    continue
                shutil.copy2(src, dst)

    published_to = [str(WORK_OUT_DATA)]
    if not DISABLE_VAULT_PUBLISH:
        published_to.append(str(VAULT_DATA))

    print(json.dumps({
        'crosswalk_rows': len(rows),
        'passages': len(summary_counts),
        'source_kind_counts': dict(Counter(r['source_kind'] for r in rows)),
        'pascha_rows': len(pascha_rows),
        'pascha_source_text_input_rows': pascha_source_text_input_rows,
        'pascha_source_text_comparable_rows': pascha_source_text_comparable_rows,
        'pascha_source_text_dropped_duplicates': dedupe_report['dropped_duplicate_count'],
        'pascha_source_text_quarantined_misextractions': dedupe_report['quarantined_misextraction_count'],
        'pascha_source_text_total_dropped': dedupe_report['total_dropped_count'],
        'pascha_source_text_kept_unique': dedupe_report['kept_unique_count'],
        'bright_rows': len(bright_rows),
        'csv': str(csv_path),
        'jsonl': str(jsonl_path),
        'summary': str(summary_path),
        'dedupe': dedupe_report,
        'published_to': published_to,
    }, indent=2))


if __name__ == '__main__':
    main()
