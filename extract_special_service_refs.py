from __future__ import annotations

import json
import re
from pathlib import Path

FILES = {
    'baptism': Path('/tmp/baptism_service.txt'),
    'wedding': Path('/tmp/wedding_service.txt'),
    'unction': Path('/tmp/unction_service.txt'),
    'funeral': Path('/tmp/funeral_service.txt'),
}

BOOK_RE = re.compile(
    r'\b(?:'
    r'Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|'
    r'1\s*Samuel|2\s*Samuel|1\s*Kings|2\s*Kings|1\s*Chronicles|2\s*Chronicles|'
    r'Ezra|Nehemiah|Esther|Job|Psalms?|Psalm|Proverbs|Ecclesiastes|Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|'
    r'Matthew|Mark|Luke|John|Acts|Romans|1\s*Corinthians|2\s*Corinthians|Galatians|Ephesians|Philippians|Colossians|1\s*Thessalonians|2\s*Thessalonians|1\s*Timothy|2\s*Timothy|Titus|Philemon|Hebrews|James|1\s*Peter|2\s*Peter|1\s*John|2\s*John|3\s*John|Jude|Revelation'
    r')\s*\d+\s*:\s*\d+(?:\s*[-–]\s*\d+)?(?:\s*[-–]\s*\d+\s*:\s*\d+)?\b',
    re.I,
)

SECTION_HINTS = {
    'baptism': ['Part 1:', 'Part 2:', 'Part 3:', 'Sanctification of the Baptismal Water', 'The Pauline Epistle', 'The Catholic Epistle', 'The Acts', 'The Gospel'],
    'wedding': ['Pauline', 'The Psalm', 'The Gospel'],
    'unction': ['First Prayer', 'Second Prayer', 'Third Prayer', 'Fourth Prayer', 'Fifth Prayer', 'Sixth Prayer', 'Seventh Prayer', 'The Pauline Epistle', 'The Catholic Epistle', 'The Gospel'],
    'funeral': ['Part 1:', 'Part 2:', 'Part 3:', 'Part 4:', 'Part 5:', 'Part 6:', 'Isaiah 26', 'Genesis 23', 'Genesis 24', 'Judges 11', 'The Pauline Epistle', 'The Psalm', 'The Gospel'],
}


def load_lines(path: Path):
    return path.read_text(encoding='utf-8', errors='ignore').splitlines()


def extract_refs(lines):
    out = []
    for i, line in enumerate(lines, start=1):
        if BOOK_RE.search(line):
            out.append((i, line.strip()))
    return out


def nearby_heading(lines, idx, hints):
    start = max(0, idx - 40)
    for j in range(idx - 1, start - 1, -1):
        line = lines[j].strip()
        if not line:
            continue
        if any(h.lower() in line.lower() for h in hints):
            return line
    return ''


def main():
    report = {}
    for name, path in FILES.items():
        lines = load_lines(path)
        refs = []
        for idx, line in extract_refs(lines):
            heading = nearby_heading(lines, idx, SECTION_HINTS[name])
            refs.append({'line': idx, 'heading': heading, 'ref_line': line})
        report[name] = refs
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
