#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from passage_normalization import parse_passage

ROOT = Path(__file__).resolve().parent


def env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name)
    return Path(value).expanduser() if value else default


def env_flag(name: str) -> bool:
    return os.environ.get(name, '').strip().lower() in {'1', 'true', 'yes', 'on'}


DATA = env_path('LECTIONARY_DATA_DIR', env_path('LECTIONARY_WORK_OUT_DATA', ROOT / 'out' / 'data'))
VAULT = Path('/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault')
VAULT_DATA = env_path('LECTIONARY_VAULT_DATA', VAULT / 'Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data')
DISABLE_VAULT_PUBLISH = env_flag('LECTIONARY_DISABLE_VAULT_PUBLISH')

# Chapter counts for the books supported by passage_normalization.py.
# This uses the standard 66-book Bible plus the deuterocanonical books currently
# recognized by the local parser. Greek additions to Esther/Daniel are not
# modeled as separate chapter rows because the parser does not currently expose
# them as separate book/chapter references.
BOOKS: List[Tuple[str, str, str, int]] = [
    ('Old Testament', 'Genesis', 'Gen', 50),
    ('Old Testament', 'Exodus', 'Exod', 40),
    ('Old Testament', 'Leviticus', 'Lev', 27),
    ('Old Testament', 'Numbers', 'Num', 36),
    ('Old Testament', 'Deuteronomy', 'Deut', 34),
    ('Old Testament', 'Joshua', 'Josh', 24),
    ('Old Testament', 'Judges', 'Judg', 21),
    ('Old Testament', 'Ruth', 'Ruth', 4),
    ('Old Testament', '1 Samuel', '1Sam', 31),
    ('Old Testament', '2 Samuel', '2Sam', 24),
    ('Old Testament', '1 Kings', '1Kgs', 22),
    ('Old Testament', '2 Kings', '2Kgs', 25),
    ('Old Testament', '1 Chronicles', '1Chr', 29),
    ('Old Testament', '2 Chronicles', '2Chr', 36),
    ('Old Testament', 'Ezra', 'Ezra', 10),
    ('Old Testament', 'Nehemiah', 'Neh', 13),
    ('Old Testament', 'Esther', 'Esth', 10),
    ('Old Testament', 'Job', 'Job', 42),
    ('Old Testament', 'Psalms', 'Ps', 150),
    ('Old Testament', 'Proverbs', 'Prov', 31),
    ('Old Testament', 'Ecclesiastes', 'Eccl', 12),
    ('Old Testament', 'Song of Solomon', 'Song', 8),
    ('Old Testament', 'Isaiah', 'Isa', 66),
    ('Old Testament', 'Jeremiah', 'Jer', 52),
    ('Old Testament', 'Lamentations', 'Lam', 5),
    ('Old Testament', 'Ezekiel', 'Ezek', 48),
    ('Old Testament', 'Daniel', 'Dan', 12),
    ('Old Testament', 'Hosea', 'Hos', 14),
    ('Old Testament', 'Joel', 'Joel', 3),
    ('Old Testament', 'Amos', 'Amos', 9),
    ('Old Testament', 'Obadiah', 'Obad', 1),
    ('Old Testament', 'Jonah', 'Jonah', 4),
    ('Old Testament', 'Micah', 'Mic', 7),
    ('Old Testament', 'Nahum', 'Nahum', 3),
    ('Old Testament', 'Habakkuk', 'Hab', 3),
    ('Old Testament', 'Zephaniah', 'Zeph', 3),
    ('Old Testament', 'Haggai', 'Hag', 2),
    ('Old Testament', 'Zechariah', 'Zech', 14),
    ('Old Testament', 'Malachi', 'Mal', 4),
    ('Deuterocanonical', 'Tobit', 'Tob', 14),
    ('Deuterocanonical', 'Judith', 'Jdt', 16),
    ('Deuterocanonical', 'Wisdom of Solomon', 'Wis', 19),
    ('Deuterocanonical', 'Sirach', 'Sir', 51),
    ('Deuterocanonical', 'Baruch', 'Bar', 6),
    ('Deuterocanonical', '1 Maccabees', '1Macc', 16),
    ('Deuterocanonical', '2 Maccabees', '2Macc', 15),
    ('Deuterocanonical', '3 Maccabees', '3Macc', 7),
    ('Deuterocanonical', '4 Maccabees', '4Macc', 18),
    ('New Testament', 'Matthew', 'Matt', 28),
    ('New Testament', 'Mark', 'Mark', 16),
    ('New Testament', 'Luke', 'Lk', 24),
    ('New Testament', 'John', 'Jn', 21),
    ('New Testament', 'Acts', 'Acts', 28),
    ('New Testament', 'Romans', 'Rom', 16),
    ('New Testament', '1 Corinthians', '1Cor', 16),
    ('New Testament', '2 Corinthians', '2Cor', 13),
    ('New Testament', 'Galatians', 'Gal', 6),
    ('New Testament', 'Ephesians', 'Eph', 6),
    ('New Testament', 'Philippians', 'Phil', 4),
    ('New Testament', 'Colossians', 'Col', 4),
    ('New Testament', '1 Thessalonians', '1Thess', 5),
    ('New Testament', '2 Thessalonians', '2Thess', 3),
    ('New Testament', '1 Timothy', '1Tim', 6),
    ('New Testament', '2 Timothy', '2Tim', 4),
    ('New Testament', 'Titus', 'Titus', 3),
    ('New Testament', 'Philemon', 'Phlm', 1),
    ('New Testament', 'Hebrews', 'Heb', 13),
    ('New Testament', 'James', 'James', 5),
    ('New Testament', '1 Peter', '1Pet', 5),
    ('New Testament', '2 Peter', '2Pet', 3),
    ('New Testament', '1 John', '1Jn', 5),
    ('New Testament', '2 John', '2Jn', 1),
    ('New Testament', '3 John', '3Jn', 1),
    ('New Testament', 'Jude', 'Jude', 1),
    ('New Testament', 'Revelation', 'Rev', 22),
]

BOOK_BY_ABBREV = {abbrev: {'testament': testament, 'book': book, 'chapters': chapters} for testament, book, abbrev, chapters in BOOKS}

AGG_FIELDS = [
    'testament',
    'book',
    'book_abbrev',
    'chapter',
    'chapter_ref',
    'is_read',
    'occurrence_count',
    'source_kinds',
    'liturgical_places',
    'service_sections',
    'reading_types',
    'sample_occurrences',
]

DETAIL_FIELDS = [
    'testament',
    'book',
    'book_abbrev',
    'chapter',
    'chapter_ref',
    'passage',
    'source_kind',
    'liturgical_place',
    'calendar_key',
    'gregorian_date',
    'coptic_date',
    'day_title',
    'service_section',
    'reading_type',
    'source_ref',
    'url',
    'occasion_label',
    'service_label',
    'reading_label',
]



KATAMEROS_SLOT_LABELS = {
    'matins_psalm': ('Matins', 'Psalm'),
    'matins_gospel': ('Matins', 'Gospel'),
    'vespers_psalm': ('Vespers', 'Psalm'),
    'vespers_gospel': ('Vespers', 'Gospel'),
    'liturgy_psalm': ('Liturgy', 'Psalm'),
    'liturgy_pauline': ('Liturgy', 'Pauline'),
    'liturgy_catholic': ('Liturgy', 'Catholicon'),
    'liturgy_acts': ('Liturgy', 'Praxis'),
    'liturgy_gospel': ('Liturgy', 'Gospel'),
    'prophecy': ('Prophecy', ''),
}


def occurrence_labels(row: dict) -> dict[str, str]:
    occasion = row.get('day_title') or row.get('liturgical_place') or row.get('calendar_key') or ''
    if row.get('source_kind') == 'katameros_cycle':
        service_label, reading_label = KATAMEROS_SLOT_LABELS.get(
            row.get('service_section', ''),
            (row.get('service_section', ''), row.get('reading_type', '')),
        )
    else:
        service_label = row.get('service_section', '')
        reading_label = row.get('reading_type', '')
    return {
        'occasion_label': occasion,
        'service_label': service_label,
        'reading_label': reading_label,
    }

def read_csv(path: Path) -> List[dict]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: List[dict], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def chapter_keys_for_passage(passage: str) -> List[Tuple[str, int]]:
    parsed = parse_passage(passage)
    if not parsed:
        return []
    meta = BOOK_BY_ABBREV.get(parsed.book_abbrev)
    if not meta:
        return []
    max_chapter = meta['chapters']
    keys = set()
    for part in parsed.parts:
        start = max(1, part.chapter_start)
        end = min(max_chapter, part.chapter_end)
        for chapter in range(start, end + 1):
            keys.add((parsed.book_abbrev, chapter))
    return sorted(keys, key=lambda item: item[1])


def compact_values(rows: List[dict], field: str, limit: int = 12) -> str:
    seen = []
    for row in rows:
        val = (row.get(field) or '').strip()
        if val and val not in seen:
            seen.append(val)
    suffix = '' if len(seen) <= limit else f' (+{len(seen)-limit} more)'
    return '; '.join(seen[:limit]) + suffix


def sample_occurrences(rows: List[dict], limit: int = 5) -> str:
    samples = []
    seen = set()
    for row in rows:
        label_parts = [
            row.get('source_kind', ''),
            row.get('liturgical_place', ''),
            row.get('service_section', ''),
            row.get('reading_type', ''),
            row.get('passage', ''),
        ]
        label = ' | '.join(part for part in label_parts if part)
        if label and label not in seen:
            seen.add(label)
            samples.append(label)
        if len(samples) >= limit:
            break
    suffix = '' if len(seen) <= limit else ' ...'
    return ' || '.join(samples) + suffix


def main() -> None:
    crosswalk_path = DATA / 'reverse_lookup_crosswalk.csv'
    if not crosswalk_path.exists():
        raise FileNotFoundError(f'Missing reverse crosswalk: {crosswalk_path}')

    crosswalk_rows = read_csv(crosswalk_path)
    by_chapter: Dict[Tuple[str, int], List[dict]] = defaultdict(list)
    detail_rows: List[dict] = []

    for row in crosswalk_rows:
        for book_abbrev, chapter in chapter_keys_for_passage(row.get('passage', '')):
            meta = BOOK_BY_ABBREV[book_abbrev]
            chapter_ref = f'{book_abbrev} {chapter}'
            detail = {
                'testament': meta['testament'],
                'book': meta['book'],
                'book_abbrev': book_abbrev,
                'chapter': chapter,
                'chapter_ref': chapter_ref,
                'passage': row.get('passage', ''),
                'source_kind': row.get('source_kind', ''),
                'liturgical_place': row.get('liturgical_place', ''),
                'calendar_key': row.get('calendar_key', ''),
                'gregorian_date': row.get('gregorian_date', ''),
                'coptic_date': row.get('coptic_date', ''),
                'day_title': row.get('day_title', ''),
                'service_section': row.get('service_section', ''),
                'reading_type': row.get('reading_type', ''),
                'source_ref': row.get('source_ref', ''),
                'url': row.get('url', ''),
                **occurrence_labels(row),
            }
            by_chapter[(book_abbrev, chapter)].append(detail)
            detail_rows.append(detail)

    detail_rows.sort(key=lambda r: (r['testament'], r['book'], int(r['chapter']), r['source_kind'], r['liturgical_place'], r['gregorian_date'], r['passage']))

    agg_rows: List[dict] = []
    for testament, book, book_abbrev, chapter_count in BOOKS:
        for chapter in range(1, chapter_count + 1):
            rows = by_chapter.get((book_abbrev, chapter), [])
            agg_rows.append({
                'testament': testament,
                'book': book,
                'book_abbrev': book_abbrev,
                'chapter': chapter,
                'chapter_ref': f'{book_abbrev} {chapter}',
                'is_read': 'yes' if rows else 'no',
                'occurrence_count': len(rows),
                'source_kinds': compact_values(rows, 'source_kind'),
                'liturgical_places': compact_values(rows, 'liturgical_place'),
                'service_sections': compact_values(rows, 'service_section'),
                'reading_types': compact_values(rows, 'reading_type'),
                'sample_occurrences': sample_occurrences(rows),
            })

    agg_csv = DATA / 'bible_chapter_lectionary_index.csv'
    detail_csv = DATA / 'bible_chapter_lectionary_occurrences.csv'
    agg_jsonl = DATA / 'bible_chapter_lectionary_index.jsonl'
    detail_jsonl = DATA / 'bible_chapter_lectionary_occurrences.jsonl'

    write_csv(agg_csv, agg_rows, AGG_FIELDS)
    write_csv(detail_csv, detail_rows, DETAIL_FIELDS)
    write_jsonl(agg_jsonl, agg_rows)
    write_jsonl(detail_jsonl, detail_rows)

    published_to = []
    if not DISABLE_VAULT_PUBLISH and VAULT_DATA.exists():
        for src in [agg_csv, detail_csv, agg_jsonl, detail_jsonl]:
            shutil.copy2(src, VAULT_DATA / src.name)
        published_to.append(str(VAULT_DATA))

    print(json.dumps({
        'chapter_rows': len(agg_rows),
        'read_chapters': sum(1 for r in agg_rows if r['is_read'] == 'yes'),
        'unread_chapters': sum(1 for r in agg_rows if r['is_read'] == 'no'),
        'chapter_occurrence_rows': len(detail_rows),
        'aggregate_csv': str(agg_csv),
        'detail_csv': str(detail_csv),
        'data_dir': str(DATA),
        'published_to': published_to,
    }, indent=2))


if __name__ == '__main__':
    main()
