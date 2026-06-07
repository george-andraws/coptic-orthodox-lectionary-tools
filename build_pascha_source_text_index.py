#!/usr/bin/env python3
"""Extract reference-level Holy Pascha readings from the St. Mary Ottawa source text.

This is a provenance-backed normalized source layer. It does not replace the
curated day/hour table; it gives the reverse crosswalk and chapter index direct
coverage from the source text so Bible-study lookup does not have to re-scan the
raw PDF text for known placements.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
from pathlib import Path
from typing import Iterable, List

from passage_normalization import canonicalize_text_ref, extract_text_ref_tokens

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'out' / 'data'
SOURCES = ROOT / 'out' / 'sources'
SOURCE_FILE = SOURCES / 'St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt'
VAULT = Path('/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault')
VAULT_DATA = VAULT / 'Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data'

BOOK_PATTERN = (
    r'(Genesis|Gen|Exodus|Exod|Leviticus|Lev|Numbers|Num|Deuteronomy|Deut|Joshua|Josh|Judges|Judg|Ruth|'
    r'1\s*Samuel|1Sam|2\s*Samuel|2Sam|1\s*Kings|1Kgs|2\s*Kings|2Kgs|1\s*Chronicles|1Chr|2\s*Chronicles|2Chr|'
    r'Ezra|Nehemiah|Neh|Esther|Esth|Job|Psalm|Psalms|Ps|Proverbs|Prov|Ecclesiastes|Eccl|Song\s+of\s+Solomon|Song|'
    r'Isaiah|Isa|Jeremiah|Jer|Lamentations|Lam|Ezekiel|Ezek|Daniel|Dan|Hosea|Hos|Joel|Amos|Obadiah|Obad|Jonah|Micah|Mic|'
    r'Nahum|Nah|Habakkuk|Hab|Zephaniah|Zeph|Haggai|Hag|Zechariah|Zech|Malachi|Mal|'
    r'Wisdom\s+of\s+Solomon|Wisdom|Wis|Sirach|Sir|Tobit|Tob|Judith|Jdt|'
    r'1\s*Maccabees|1Macc|2\s*Maccabees|2Macc|3\s*Maccabees|3Macc|4\s*Maccabees|4Macc|'
    r'Matthew|Matt|Mt|Mark|Mk|Luke|Lk|John|Jn|Acts|Romans|Rom|1\s*Corinthians|1Cor|2\s*Corinthians|2Cor|'
    r'Galatians|Gal|Ephesians|Eph|Philippians|Phil|Colossians|Col|1\s*Thessalonians|1Thess|2\s*Thessalonians|2Thess|'
    r'1\s*Timothy|1Tim|2\s*Timothy|2Tim|Titus|Philemon|Phlm|Hebrews|Heb|James|Jas|1\s*Peter|1Pet|2\s*Peter|2Pet|'
    r'1\s*John|1Jn|2\s*John|2Jn|3\s*John|3Jn|Jude|Revelation|Rev|Apocalypse)'
)

REF_LINE_RE = re.compile(
    r'^' + BOOK_PATTERN + r'\.?\s*\d+\s*:\s*[0-9][0-9\s,;&:()\-–—]*\s*$',
    re.IGNORECASE,
)
HEADING_RE = re.compile(
    r'^(?:The\s+)?(?P<hour>First Hour|Third Hour|Sixth Hour|Ninth Hour|Eleventh Hour|Twelfth Hour|Liturgy(?:\s+of\s+[^\n]+)?|Vespers|Matins)\s+of\s+(?P<day>.+)$',
    re.IGNORECASE,
)
PAGE_RE = re.compile(r'^===== PAGE (?P<page>\d+) =====$')

DAY_REWRITES = {
    'eve of monday': 'Monday Eve',
    'eve of tuesday': 'Tuesday Eve',
    'eve of wednesday': 'Wednesday Eve',
    'eve of great thursday': 'Great Thursday Eve',
    'eve of good friday': 'Great Thursday Eve',
    'eve of friday': 'Great Thursday Eve',
}

FIELDS = [
    'day',
    'hour',
    'source_kind',
    'source_family',
    'source_file',
    'source_line',
    'source_page',
    'order',
    'reading_type',
    'raw_ref',
    'normalized_ref',
    'parse_status',
    'provenance_note',
]


def normalize_day(raw: str) -> str:
    text = re.sub(r'\s+', ' ', (raw or '').strip())
    key = text.lower()
    if key in DAY_REWRITES:
        return DAY_REWRITES[key]
    # Preserve common headings exactly but normalize repeated whitespace.
    return text


def normalize_hour(raw: str) -> str:
    return re.sub(r'\s+', ' ', (raw or '').strip())


def clean_raw_ref(line: str) -> str:
    text = re.sub(r'\s+', ' ', (line or '').strip())
    text = re.sub(r'\s*:\s*', ':', text)
    text = text.replace(' -- ', '-').replace('–', '-').replace('—', '-')
    text = re.sub(r'\s*-\s*', '-', text)
    text = text.replace(' & ', ', ')
    # PDF extraction sometimes drops the space before the chapter number.
    text = re.sub(r'^(Wisdom of Solomon)(\d)', r'\1 \2', text, flags=re.IGNORECASE)
    return text


def classify_reading(normalized_ref: str, raw_ref: str) -> str:
    ref = normalized_ref or canonicalize_text_ref(raw_ref)
    if ref.startswith('Ps '):
        return 'Psalm'
    if ref.startswith(('Matt ', 'Mark ', 'Lk ', 'Jn ')):
        return 'Gospel'
    if ref.startswith(('Rom ', '1Cor ', '2Cor ', 'Gal ', 'Eph ', 'Phil ', 'Col ', '1Thess ', '2Thess ', '1Tim ', '2Tim ', 'Titus ', 'Phlm ', 'Heb ')):
        return 'Pauline'
    if ref.startswith(('James ', '1Pet ', '2Pet ', '1Jn ', '2Jn ', '3Jn ', 'Jude ')):
        return 'Catholic'
    if ref.startswith('Acts '):
        return 'Acts'
    return 'Prophecy'


def write_csv(path: Path, rows: List[dict], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def extract_rows() -> List[dict]:
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f'Missing Holy Pascha source text: {SOURCE_FILE}')

    current_day = ''
    current_hour = ''
    current_page = ''
    order_by_service: dict[tuple[str, str], int] = {}
    rows: List[dict] = []

    for line_number, raw_line in enumerate(SOURCE_FILE.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        page_match = PAGE_RE.match(line)
        if page_match:
            current_page = page_match.group('page')
            continue

        heading = HEADING_RE.match(line)
        if heading:
            current_hour = normalize_hour(heading.group('hour'))
            current_day = normalize_day(heading.group('day'))
            continue

        if not current_day or not current_hour or not REF_LINE_RE.match(line):
            continue

        raw_ref = clean_raw_ref(line)
        tokens = extract_text_ref_tokens(raw_ref)
        if not tokens:
            # Preserve the raw source evidence even when the parser cannot yet split it.
            service_key = (current_day, current_hour)
            order_by_service[service_key] = order_by_service.get(service_key, 0) + 1
            rows.append({
                'day': current_day,
                'hour': current_hour,
                'source_kind': 'pascha_source_text',
                'source_family': 'holy_pascha',
                'source_file': str(SOURCE_FILE.relative_to(ROOT)),
                'source_line': line_number,
                'source_page': current_page,
                'order': order_by_service[service_key],
                'reading_type': 'Unparsed source ref',
                'raw_ref': raw_ref,
                'normalized_ref': '',
                'parse_status': 'unparsed',
                'provenance_note': 'St. Mary Ottawa Holy Pascha extracted text line retained for source recovery.',
            })
            continue

        for token in tokens:
            service_key = (current_day, current_hour)
            order_by_service[service_key] = order_by_service.get(service_key, 0) + 1
            rows.append({
                'day': current_day,
                'hour': current_hour,
                'source_kind': 'pascha_source_text',
                'source_family': 'holy_pascha',
                'source_file': str(SOURCE_FILE.relative_to(ROOT)),
                'source_line': line_number,
                'source_page': current_page,
                'order': order_by_service[service_key],
                'reading_type': classify_reading(token, raw_ref),
                'raw_ref': raw_ref,
                'normalized_ref': token,
                'parse_status': 'parsed',
                'provenance_note': 'St. Mary Ottawa Holy Pascha extracted text.',
            })
    return rows


def main() -> None:
    rows = extract_rows()
    csv_path = DATA / 'pascha_source_text_index.csv'
    jsonl_path = DATA / 'pascha_source_text_index.jsonl'
    write_csv(csv_path, rows, FIELDS)
    write_jsonl(jsonl_path, rows)
    if VAULT_DATA.exists():
        shutil.copy2(csv_path, VAULT_DATA / csv_path.name)
        shutil.copy2(jsonl_path, VAULT_DATA / jsonl_path.name)
    print(json.dumps({
        'pascha_source_text_rows': len(rows),
        'parsed_rows': sum(1 for r in rows if r['parse_status'] == 'parsed'),
        'unparsed_rows': sum(1 for r in rows if r['parse_status'] != 'parsed'),
        'csv': str(csv_path),
        'jsonl': str(jsonl_path),
    }, indent=2))


if __name__ == '__main__':
    main()
