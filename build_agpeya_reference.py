#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Dict, List

from passage_normalization import canonicalize_text_ref, extract_text_ref_tokens

ROOT = Path('/Users/georgeandraws/workspace/coptic-lectionary-research')
OUT = ROOT / 'out' / 'data'
VAULT = Path('/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary')


def env_flag(name: str) -> bool:
    return os.environ.get(name, '').strip().lower() in {'1', 'true', 'yes', 'on'}


DISABLE_VAULT_PUBLISH = env_flag('LECTIONARY_DISABLE_VAULT_PUBLISH')

SOURCE_TITLE = 'Book of Agpeya'
SOURCE_URL = 'https://www.saintbishoy.ca/wp-content/uploads/Rites_Agpeya_Book.pdf'
SOURCE_PAGE = 'St. Bishoy Agpeya PDF (text extracted locally for validation)'


def ps(*refs: str) -> str:
    return '; '.join(f'Psalm {r}' for r in refs)


ROWS: List[Dict[str, str]] = [
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'first_hour',
        'prayer_name': 'First Hour (Prime / Morning Prayer)',
        'service_order': '1',
        'reading_type': 'psalm',
        'raw_ref': ps('1', '2', '3', '4', '5', '6', '8', '12', '13', '15', '16', '19', '25', '27', '63', '67', '70', '113', '143'),
        'display_ref': 'Psalm 1; Psalm 2; Psalm 3; Psalm 4; Psalm 5; Psalm 6; Psalm 8; Psalm 11 (12); Psalm 12 (13); Psalm 14 (15); Psalm 15 (16); Psalm 18 (19); Psalm 24 (25); Psalm 26 (27); Psalm 62 (63); Psalm 66 (67); Psalm 69 (70); Psalm 112 (113); Psalm 142 (143)',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Canonical raw_ref uses standard English numbering; display_ref preserves the Agpeya printed numbering.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'first_hour',
        'prayer_name': 'First Hour (Prime / Morning Prayer)',
        'service_order': '1',
        'reading_type': 'gospel',
        'raw_ref': 'John 1:1-17',
        'display_ref': 'John 1:1-17',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the First Hour.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'third_hour',
        'prayer_name': 'Third Hour (Terce)',
        'service_order': '2',
        'reading_type': 'psalm',
        'raw_ref': ps('20', '23', '24', '26', '29', '30', '34', '41', '43', '45', '46', '47'),
        'display_ref': 'Psalm 19 (20); Psalm 22 (23); Psalm 23 (24); Psalm 25 (26); Psalm 28 (29); Psalm 29 (30); Psalm 33 (34); Psalm 40 (41); Psalm 42 (43); Psalm 44 (45); Psalm 45 (46); Psalm 46 (47)',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Canonical raw_ref uses standard English numbering; display_ref preserves the Agpeya printed numbering.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'third_hour',
        'prayer_name': 'Third Hour (Terce)',
        'service_order': '2',
        'reading_type': 'gospel',
        'raw_ref': 'John 14:26-15:4',
        'display_ref': 'John 14:26-15:4',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the Third Hour.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'sixth_hour',
        'prayer_name': 'Sixth Hour (Sext)',
        'service_order': '3',
        'reading_type': 'psalm',
        'raw_ref': ps('54', '57', '61', '63', '67', '70', '84', '85', '86', '87', '91', '93'),
        'display_ref': 'Psalm 53 (54); Psalm 56 (57); Psalm 60 (61); Psalm 62 (63); Psalm 66 (67); Psalm 69 (70); Psalm 83 (84); Psalm 84 (85); Psalm 85 (86); Psalm 86 (87); Psalm 90 (91); Psalm 92 (93)',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Canonical raw_ref uses standard English numbering; display_ref preserves the Agpeya printed numbering.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'sixth_hour',
        'prayer_name': 'Sixth Hour (Sext)',
        'service_order': '3',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 5:1-16',
        'display_ref': 'Matthew 5:1-16',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the Sixth Hour.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'ninth_hour',
        'prayer_name': 'Ninth Hour (None)',
        'service_order': '4',
        'reading_type': 'psalm',
        'raw_ref': ps('96', '97', '98', '99', '100', '101', '110', '111', '112', '113', '116:1-9', '116:10-19'),
        'display_ref': 'Psalm 95 (96); Psalm 96 (97); Psalm 97 (98); Psalm 98 (99); Psalm 99 (100); Psalm 100 (101); Psalm 109 (110); Psalm 110 (111); Psalm 111 (112); Psalm 112 (113); Psalm 114 (116:1-9); Psalm 115 (116:10-19)',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'The Agpeya splits Psalm 116 into two Psalm headings here; canonical raw_ref preserves the standard numbering as Psalm 116:1-9 and Psalm 116:10-19.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'ninth_hour',
        'prayer_name': 'Ninth Hour (None)',
        'service_order': '4',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 9:10-17',
        'display_ref': 'Luke 9:10-17',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the Ninth Hour.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'eleventh_hour',
        'prayer_name': 'Eleventh Hour (Vespers)',
        'service_order': '5',
        'reading_type': 'psalm',
        'raw_ref': ps('117', '118', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129'),
        'display_ref': 'Psalm 116 (117); Psalm 117 (118); Psalm 119 (120); Psalm 120 (121); Psalm 121 (122); Psalm 122 (123); Psalm 123 (124); Psalm 124 (125); Psalm 125 (126); Psalm 126 (127); Psalm 127 (128); Psalm 128 (129)',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Canonical raw_ref uses standard English numbering; display_ref preserves the Agpeya printed numbering.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'eleventh_hour',
        'prayer_name': 'Eleventh Hour (Vespers)',
        'service_order': '5',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 4:38-41',
        'display_ref': 'Luke 4:38-41',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the Eleventh Hour.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'twelfth_hour',
        'prayer_name': 'Twelfth Hour (Compline / Before Sleep)',
        'service_order': '6',
        'reading_type': 'psalm',
        'raw_ref': ps('130', '131', '132', '133', '134', '137', '138', '141', '142', '146', '147:1-11', '147:12-20'),
        'display_ref': 'Psalm 129 (130); Psalm 130 (131); Psalm 131 (132); Psalm 132 (133); Psalm 133 (134); Psalm 136 (137); Psalm 137 (138); Psalm 140 (141); Psalm 141 (142); Psalm 145 (146); Psalm 146 (147:1-11); Psalm 147 (147:12-20)',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Twelfth Hour only; the Veil prayer below is stored separately.',
    },
    {
        'prayer_group': 'daily_hours',
        'prayer_key': 'twelfth_hour',
        'prayer_name': 'Twelfth Hour (Compline / Before Sleep)',
        'service_order': '6',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 2:25-32',
        'display_ref': 'Luke 2:25-32',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the Twelfth Hour.',
    },
    {
        'prayer_group': 'optional_prayers',
        'prayer_key': 'veil_prayer',
        'prayer_name': 'Veil Prayer',
        'service_order': '7',
        'reading_type': 'psalm',
        'raw_ref': ps('4', '6', '13', '16', '25', '27', '67', '70', '23', '30', '43', '57', '86', '91', '97', '110', '116:1-9', '116:10-19', '121', '129', '130', '131', '132', '133', '134', '137', '141', '146', '119:20-22'),
        'display_ref': 'Psalm 4; Psalm 6; Psalm 12 (13); Psalm 15 (16); Psalm 24 (25); Psalm 26 (27); Psalm 66 (67); Psalm 69 (70); Psalm 22 (23); Psalm 29 (30); Psalm 42 (43); Psalm 56 (57); Psalm 85 (86); Psalm 90 (91); Psalm 96 (97); Psalm 109 (110); Psalm 114 (116:1-9); Psalm 115 (116:10-19); Psalm 120 (121); Psalm 128 (129); Psalm 129 (130); Psalm 130 (131); Psalm 131 (132); Psalm 132 (133); Psalm 133 (134); Psalm 136 (137); Psalm 140 (141); Psalm 145 (146); Psalm 118 (119):20-22',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Optional Veil prayer, especially associated with monastic use. Canonical raw_ref uses standard English numbering.',
    },
    {
        'prayer_group': 'optional_prayers',
        'prayer_key': 'veil_prayer',
        'prayer_name': 'Veil Prayer',
        'service_order': '7',
        'reading_type': 'gospel',
        'raw_ref': 'John 6:15-23',
        'display_ref': 'John 6:15-23',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the Veil Prayer.',
    },
    {
        'prayer_group': 'midnight_prayer',
        'prayer_key': 'first_watch',
        'prayer_name': 'Midnight Prayer - First Watch',
        'service_order': '8',
        'reading_type': 'psalm',
        'raw_ref': ps('3', '6', '13', '70', '86', '91', '117', '118', '119'),
        'display_ref': 'Psalm 3; Psalm 6; Psalm 12 (13); Psalm 69 (70); Psalm 85 (86); Psalm 90 (91); Psalm 116 (117); Psalm 117 (118); Psalm 118 (119)',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'First watch of the Midnight Prayer. Canonical raw_ref uses standard English numbering.',
    },
    {
        'prayer_group': 'midnight_prayer',
        'prayer_key': 'first_watch',
        'prayer_name': 'Midnight Prayer - First Watch',
        'service_order': '8',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 25:1-13',
        'display_ref': 'Matthew 25:1-13',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the First Watch.',
    },
    {
        'prayer_group': 'midnight_prayer',
        'prayer_key': 'second_watch',
        'prayer_name': 'Midnight Prayer - Second Watch',
        'service_order': '9',
        'reading_type': 'psalm',
        'raw_ref': ps('120', '121', '122', '123', '124', '125', '126', '127', '128', '129'),
        'display_ref': 'Psalm 119 (120); Psalm 120 (121); Psalm 121 (122); Psalm 122 (123); Psalm 123 (124); Psalm 124 (125); Psalm 125 (126); Psalm 126 (127); Psalm 127 (128); Psalm 128 (129)',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Second watch of the Midnight Prayer. Canonical raw_ref uses standard English numbering.',
    },
    {
        'prayer_group': 'midnight_prayer',
        'prayer_key': 'second_watch',
        'prayer_name': 'Midnight Prayer - Second Watch',
        'service_order': '9',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 7:36-50',
        'display_ref': 'Luke 7:36-50',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the Second Watch.',
    },
    {
        'prayer_group': 'midnight_prayer',
        'prayer_key': 'third_watch',
        'prayer_name': 'Midnight Prayer - Third Watch',
        'service_order': '10',
        'reading_type': 'psalm',
        'raw_ref': ps('130', '131', '132', '133', '134', '137', '138', '141', '142', '146', '147:1-11', '147:12-20'),
        'display_ref': 'Psalm 129 (130); Psalm 130 (131); Psalm 131 (132); Psalm 132 (133); Psalm 133 (134); Psalm 136 (137); Psalm 137 (138); Psalm 140 (141); Psalm 141 (142); Psalm 145 (146); Psalm 146 (147:1-11); Psalm 147 (147:12-20)',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Third watch of the Midnight Prayer. Canonical raw_ref uses standard English numbering.',
    },
    {
        'prayer_group': 'midnight_prayer',
        'prayer_key': 'third_watch',
        'prayer_name': 'Midnight Prayer - Third Watch',
        'service_order': '10',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 12:32-46',
        'display_ref': 'Luke 12:32-46',
        'source_title': SOURCE_TITLE,
        'source_url': SOURCE_URL,
        'source_page': SOURCE_PAGE,
        'notes': 'Gospel of the Third Watch.',
    },
]


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not DISABLE_VAULT_PUBLISH:
        VAULT.mkdir(parents=True, exist_ok=True)



def canonicalize_row_refs(row: Dict[str, str]) -> Dict[str, str]:
    row = dict(row)
    row['canonical_ref'] = canonicalize_text_ref(row['raw_ref'])
    return row



def build_passage_index(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for row in rows:
        base = canonicalize_row_refs(row)
        seen = set()
        for seg in extract_text_ref_tokens(base['raw_ref']):
            normalized = canonicalize_text_ref(seg)
            if not normalized:
                continue
            key = (base['prayer_key'], base['reading_type'], normalized)
            if key in seen:
                continue
            seen.add(key)
            out.append({
                'prayer_group': base['prayer_group'],
                'prayer_key': base['prayer_key'],
                'prayer_name': base['prayer_name'],
                'service_order': base['service_order'],
                'reading_type': base['reading_type'],
                'raw_ref': base['raw_ref'],
                'display_ref': base['display_ref'],
                'canonical_ref': base['canonical_ref'],
                'matched_ref': normalized,
                'source_title': base['source_title'],
                'source_url': base['source_url'],
                'source_page': base['source_page'],
                'notes': base['notes'],
                'source_kind': 'agpeya',
            })
    return out



def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)



def write_jsonl(path: Path, rows: List[Dict[str, str]]) -> None:
    with path.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')



def main() -> None:
    ensure_dirs()
    curated = [canonicalize_row_refs(r) for r in ROWS]
    pidx = build_passage_index(ROWS)
    write_csv(OUT / 'agpeya_hour_readings.csv', curated)
    write_jsonl(OUT / 'agpeya_hour_readings.jsonl', curated)
    write_csv(OUT / 'agpeya_passage_index.csv', pidx)
    write_jsonl(OUT / 'agpeya_passage_index.jsonl', pidx)
    if not DISABLE_VAULT_PUBLISH:
        write_csv(VAULT / 'agpeya_hour_readings.csv', curated)
        write_csv(VAULT / 'agpeya_passage_index.csv', pidx)
    print(json.dumps({'curated_rows': len(curated), 'passage_rows': len(pidx)}, indent=2))


if __name__ == '__main__':
    main()
