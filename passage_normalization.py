#!/usr/bin/env python3
"""Shared passage normalization and matching helpers for the local lectionary toolchain."""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Iterable, List, Optional

BOOK_ABBREV = {
    'Genesis':'Gen','Exodus':'Exod','Leviticus':'Lev','Numbers':'Num','Deuteronomy':'Deut','Joshua':'Josh','Judges':'Judg','Ruth':'Ruth',
    '1 Samuel':'1Sam','2 Samuel':'2Sam','1 Kings':'1Kgs','2 Kings':'2Kgs','1 Chronicles':'1Chr','2 Chronicles':'2Chr','Ezra':'Ezra','Nehemiah':'Neh','Esther':'Esth','Job':'Job','Psalms':'Ps','Psalm':'Ps','Proverbs':'Prov','Ecclesiastes':'Eccl','Song of Solomon':'Song','Isaiah':'Isa','Jeremiah':'Jer','Lamentations':'Lam','Ezekiel':'Ezek','Daniel':'Dan','Hosea':'Hos','Joel':'Joel','Amos':'Amos','Obadiah':'Obad','Jonah':'Jonah','Micah':'Mic','Nahum':'Nah','Habakkuk':'Hab','Zephaniah':'Zeph','Haggai':'Hag','Zechariah':'Zech','Malachi':'Mal',
    'Matthew':'Matt','Mark':'Mark','Luke':'Lk','John':'Jn','Acts':'Acts','Romans':'Rom','1 Corinthians':'1Cor','2 Corinthians':'2Cor','Galatians':'Gal','Ephesians':'Eph','Philippians':'Phil','Colossians':'Col','1 Thessalonians':'1Thess','2 Thessalonians':'2Thess','1 Timothy':'1Tim','2 Timothy':'2Tim','Titus':'Titus','Philemon':'Phlm','Hebrews':'Heb','James':'James','1 Peter':'1Pet','2 Peter':'2Pet','1 John':'1Jn','2 John':'2Jn','3 John':'3Jn','Jude':'Jude','Revelation':'Rev',
    'Baruch':'Bar','Tobit':'Tob','Judith':'Jdt','1 Maccabees':'1Macc','2 Maccabees':'2Macc','3 Maccabees':'3Macc','4 Maccabees':'4Macc','Wisdom of Solomon':'Wis','Wisdom':'Wis','Sirach':'Sir'
}

QUERY_BOOK_ALIASES = {
    'genesis': 'Gen', 'gen': 'Gen',
    'exodus': 'Exod', 'exod': 'Exod', 'exo': 'Exod', 'ex': 'Exod',
    'leviticus': 'Lev', 'lev': 'Lev',
    'numbers': 'Num', 'num': 'Num',
    'deuteronomy': 'Deut', 'deut': 'Deut',
    'joshua': 'Josh', 'josh': 'Josh',
    'judges': 'Judg', 'judg': 'Judg',
    'ruth': 'Ruth',
    '1samuel': '1Sam', '1 samuel': '1Sam', '1sam': '1Sam', 'i samuel': '1Sam',
    '2samuel': '2Sam', '2 samuel': '2Sam', '2sam': '2Sam', 'ii samuel': '2Sam',
    '1kings': '1Kgs', '1 kings': '1Kgs', '1kgs': '1Kgs', 'i kings': '1Kgs',
    '2kings': '2Kgs', '2 kings': '2Kgs', '2kgs': '2Kgs', 'ii kings': '2Kgs',
    '1chronicles': '1Chr', '1 chronicles': '1Chr', '1chr': '1Chr', 'i chronicles': '1Chr',
    '2chronicles': '2Chr', '2 chronicles': '2Chr', '2chr': '2Chr', 'ii chronicles': '2Chr',
    'ezra': 'Ezra', 'nehemiah': 'Neh', 'neh': 'Neh', 'esther': 'Esth', 'esth': 'Esth', 'job': 'Job',
    'psalm': 'Ps', 'psalms': 'Ps', 'ps': 'Ps',
    'proverbs': 'Prov', 'prov': 'Prov', 'ecclesiastes': 'Eccl', 'eccl': 'Eccl',
    'songofsolomon': 'Song', 'song of solomon': 'Song', 'song': 'Song',
    'isaiah': 'Isa', 'isa': 'Isa', 'jeremiah': 'Jer', 'jer': 'Jer', 'lamentations': 'Lam', 'lam': 'Lam',
    'ezekiel': 'Ezek', 'ezek': 'Ezek', 'daniel': 'Dan', 'dan': 'Dan', 'hosea': 'Hos', 'hos': 'Hos', 'joel': 'Joel',
    'amos': 'Amos', 'obadiah': 'Obad', 'obad': 'Obad', 'jonah': 'Jonah', 'micah': 'Mic', 'mic': 'Mic',
    'nahum': 'Nah', 'nah': 'Nah', 'habakkuk': 'Hab', 'hab': 'Hab', 'zephaniah': 'Zeph', 'zeph': 'Zeph',
    'haggai': 'Hag', 'hag': 'Hag', 'zechariah': 'Zech', 'zech': 'Zech', 'malachi': 'Mal', 'mal': 'Mal',
    'matthew': 'Matt', 'matt': 'Matt', 'mt': 'Matt', 'mark': 'Mark', 'mk': 'Mark',
    'luke': 'Lk', 'lk': 'Lk', 'john': 'Jn', 'jn': 'Jn', 'acts': 'Acts', 'romans': 'Rom', 'rom': 'Rom',
    '1corinthians': '1Cor', '1 corinthians': '1Cor', '1cor': '1Cor', 'i corinthians': '1Cor',
    '2corinthians': '2Cor', '2 corinthians': '2Cor', '2cor': '2Cor', 'ii corinthians': '2Cor',
    'galatians': 'Gal', 'gal': 'Gal', 'ephesians': 'Eph', 'eph': 'Eph', 'philippians': 'Phil', 'phil': 'Phil',
    'colossians': 'Col', 'col': 'Col', '1thessalonians': '1Thess', '1 thessalonians': '1Thess', '1thess': '1Thess',
    '2thessalonians': '2Thess', '2 thessalonians': '2Thess', '2thess': '2Thess', '1timothy': '1Tim', '1 timothy': '1Tim',
    '2timothy': '2Tim', '2 timothy': '2Tim', 'titus': 'Titus', 'philemon': 'Phlm', 'phlm': 'Phlm',
    'hebrews': 'Heb', 'heb': 'Heb', 'james': 'James', 'jas': 'James',
    '1peter': '1Pet', '1 peter': '1Pet', '1pet': '1Pet', '2peter': '2Pet', '2 peter': '2Pet', '2pet': '2Pet',
    '1john': '1Jn', '1 john': '1Jn', '1jn': '1Jn', '2john': '2Jn', '2 john': '2Jn', '2jn': '2Jn',
    '3john': '3Jn', '3 john': '3Jn', '3jn': '3Jn', 'jude': 'Jude', 'revelation': 'Rev', 'rev': 'Rev', 'apocalypse': 'Rev',
    'baruch': 'Bar', 'bar': 'Bar', 'tobit': 'Tob', 'tob': 'Tob', 'judith': 'Jdt', 'jdt': 'Jdt',
    'wisdom': 'Wis', 'wisdomofsolomon': 'Wis', 'wisdom of solomon': 'Wis', 'wis': 'Wis',
    'sirach': 'Sir', 'sir': 'Sir', 'ecclesiasticus': 'Sir',
    '1maccabees': '1Macc', '1 maccabees': '1Macc', '1macc': '1Macc', 'i maccabees': '1Macc',
    '2maccabees': '2Macc', '2 maccabees': '2Macc', '2macc': '2Macc', 'ii maccabees': '2Macc',
    '3maccabees': '3Macc', '3 maccabees': '3Macc', '3macc': '3Macc', 'iii maccabees': '3Macc',
    '4maccabees': '4Macc', '4 maccabees': '4Macc', '4macc': '4Macc', 'iv maccabees': '4Macc',
}

REF_TOKEN_RE = re.compile(r'(?P<book>\d+)\.(?P<chapter>\d+):(?P<verses>[0-9,\-–— ]+\*?)')
TEXT_BOOK_PATTERN = (
    r'(Genesis|Gen|Exodus|Exod|Exo|Leviticus|Lev|Numbers|Num|Deuteronomy|Deut|Joshua|Josh|Judges|Judg|Ruth|'
    r'1\s*Samuel|1Sam|2\s*Samuel|2Sam|1\s*Kings|1Kgs|2\s*Kings|2Kgs|1\s*Chronicles|1Chr|2\s*Chronicles|2Chr|'
    r'Ezra|Nehemiah|Neh|Esther|Esth|Job|Psalm|Psalms|Ps|Proverbs|Prov|Ecclesiastes|Eccl|Song\s+of\s+Solomon|Song|'
    r'Isaiah|Isa|Jeremiah|Jer|Lamentations|Lam|Ezekiel|Ezek|Daniel|Dan|Hosea|Hos|Joel|Amos|Obadiah|Obad|Jonah|Micah|Mic|'
    r'Nahum|Nah|Habakkuk|Hab|Zephaniah|Zeph|Haggai|Hag|Zechariah|Zech|Malachi|Mal|Matthew|Matt|Mt|Mark|Mk|Luke|Lk|'
    r'Wisdom\s+of\s+Solomon|Wisdom|Wis|Sirach|Sir|Ecclesiasticus|Baruch|Bar|Tobit|Tob|Judith|Jdt|'
    r'1\s*Maccabees|1Macc|2\s*Maccabees|2Macc|3\s*Maccabees|3Macc|4\s*Maccabees|4Macc|'
    r'John|Jn|Acts|Romans|Rom|1\s*Corinthians|1Cor|2\s*Corinthians|2Cor|Galatians|Gal|Ephesians|Eph|'
    r'Philippians|Phil|Colossians|Col|1\s*Thessalonians|1Thess|2\s*Thessalonians|2Thess|1\s*Timothy|1Tim|2\s*Timothy|2Tim|'
    r'Titus|Philemon|Phlm|Hebrews|Heb|James|Jas|1\s*Peter|1Pet|2\s*Peter|2Pet|1\s*John|1Jn|2\s*John|2Jn|3\s*John|3Jn|Jude|'
    r'Revelation|Rev|Apocalypse)'
)
TEXT_REF_RE = re.compile(
    TEXT_BOOK_PATTERN + r'\.?\s*\d+(?::\s*-?[0-9][0-9:,\s\-–—]*)?\s*[-–—]?',
    re.I,
)
ALT_PAIRS = [('Psalm', 'Ps'), ('Psalms', 'Ps'), ('John', 'Jn'), ('Luke', 'Lk'), ('Matthew', 'Matt'), ('Isaiah', 'Isa'), ('Romans', 'Rom'), ('Wisdom of Solomon', 'Wis'), ('Wisdom', 'Wis'), ('Sirach', 'Sir')]
NUMERIC_QUERY_RE = re.compile(r'^\d+\.\d+(?::[0-9,\-–— ]+)?$')


@dataclass(frozen=True)
class PassagePart:
    chapter_start: int
    verse_start: Optional[int]
    chapter_end: int
    verse_end: Optional[int]


@dataclass(frozen=True)
class ParsedPassage:
    book_abbrev: str
    canonical: str
    parts: List[PassagePart]


def compact(text: Optional[str]) -> str:
    return re.sub(r'\s+', '', (text or '').lower())


@lru_cache(maxsize=4096)
def normalize_text_query(query: Optional[str]) -> str:
    q = re.sub(r'\s+', ' ', (query or '').strip())
    q_compact = compact(q)
    for alias in sorted(QUERY_BOOK_ALIASES, key=len, reverse=True):
        alias_compact = compact(alias)
        if q_compact == alias_compact:
            return QUERY_BOOK_ALIASES[alias]
        if q_compact.startswith(alias_compact):
            if q.lower().startswith(alias.lower()):
                suffix = q[len(alias):].strip()
            else:
                suffix = q_compact[len(alias_compact):]
            suffix = suffix.lstrip('.').strip()
            return (QUERY_BOOK_ALIASES[alias] + (' ' + suffix if suffix else '')).strip()
    return q


@lru_cache(maxsize=4096)
def query_variants(query: Optional[str]) -> tuple[str, ...]:
    raw = re.sub(r'\s+', ' ', (query or '').strip())
    normalized = normalize_text_query(raw)
    variants = {raw, normalized}
    current = list(variants)
    for text in current:
        for long_name, short_name in ALT_PAIRS:
            if text.startswith(long_name + ' '):
                variants.add(short_name + text[len(long_name):])
            if text.startswith(short_name + ' '):
                variants.add(long_name + text[len(short_name):])
    return tuple(v for v in variants if v)


def contains_any(hay: str, needles: Iterable[str]) -> bool:
    hay_c = compact(hay)
    return any(compact(n) in hay_c for n in needles)


def is_numeric_query(query: Optional[str]) -> bool:
    return bool(NUMERIC_QUERY_RE.fullmatch((query or '').strip()))


def _clean_token_spacing(token: str) -> str:
    token = (token or '').replace('—', '-').replace('–', '-')
    token = re.sub(r'\s+', ' ', token).strip()
    token = re.sub(r'\s*:\s*', ':', token)
    token = re.sub(r'\s*,\s*', ',', token)
    token = re.sub(r'\s*;\s*', '; ', token)
    token = re.sub(r'\s*-\s*', '-', token)
    return token


SUSPICIOUS_REF_RE = re.compile(r':-|--|\d+:\d+\s*[-–—]\s*(?:[,;]|$)')


def source_ref_warnings(raw_ref: Optional[str]) -> List[str]:
    """Return warnings for source refs that require repair or should not parse silently."""
    text = raw_ref or ''
    warnings: List[str] = []
    if re.search(r':-\d', text):
        warnings.append('repaired_negative_verse_marker')
    if re.search(r'\d+:\d+\s*[-–—]\s*(?:[,;]|$)', text):
        warnings.append('dangling_range_marker')
    if '--' in text:
        warnings.append('double_dash_range_marker')
    return warnings


def repair_source_ref(raw_ref: Optional[str]) -> str:
    """Repair narrowly-known scraper glitches while preserving warnings separately."""
    text = raw_ref or ''
    text = text.replace('—', '-').replace('–', '-')
    text = re.sub(r':-(\d)', r':\1', text)
    text = re.sub(r',-(\d)', r',\1', text)
    return text


def source_ref_status(raw_ref: Optional[str]) -> tuple[str, str, str]:
    warnings = source_ref_warnings(raw_ref)
    repaired = repair_source_ref(raw_ref)
    if not warnings:
        return 'ok', '', repaired
    return 'repaired' if repaired != (raw_ref or '') else 'suspicious', ';'.join(warnings), repaired


def _canonical_from_parts(book_abbrev: str, parts: List[PassagePart]) -> str:
    rendered = []
    for part in parts:
        if part.verse_start is None:
            rendered.append(str(part.chapter_start))
        elif part.chapter_start == part.chapter_end and part.verse_start == part.verse_end:
            rendered.append(f"{part.chapter_start}:{part.verse_start}")
        elif part.chapter_start == part.chapter_end:
            rendered.append(f"{part.chapter_start}:{part.verse_start}-{part.verse_end}")
        else:
            rendered.append(f"{part.chapter_start}:{part.verse_start}-{part.chapter_end}:{part.verse_end}")
    return f"{book_abbrev} {','.join(rendered)}"


@lru_cache(maxsize=65536)
def parse_passage(text: Optional[str]) -> Optional[ParsedPassage]:
    token = _clean_token_spacing(normalize_text_query(text))
    if not token:
        return None
    m = re.match(r'^(?P<book>[1-4]?[A-Za-z]+)\s+(?P<body>.+)$', token)
    if not m:
        return None
    book = m.group('book')
    body = m.group('body').strip()
    if not body:
        return None
    if body.endswith('-') or '--' in body:
        return None
    if not re.fullmatch(r'[0-9:,-]+', body):
        return None

    parts: List[PassagePart] = []
    if ':' not in body:
        try:
            chapter = int(body)
        except ValueError:
            return None
        if chapter <= 0:
            return None
        parts.append(PassagePart(chapter, None, chapter, None))
        return ParsedPassage(book, _canonical_from_parts(book, parts), parts)

    chapter_text, verses_text = body.split(':', 1)
    try:
        chapter = int(chapter_text)
    except ValueError:
        return None
    if chapter <= 0:
        return None

    current_chapter = chapter
    for item in [x.strip() for x in verses_text.split(',') if x.strip()]:
        if '-' not in item:
            if ':' in item:
                item_chapter_text, item_verse_text = item.split(':', 1)
                try:
                    item_chapter = int(item_chapter_text)
                    verse = int(item_verse_text)
                except ValueError:
                    return None
            else:
                item_chapter = current_chapter
                try:
                    verse = int(item)
                except ValueError:
                    return None
            if item_chapter <= 0 or verse <= 0:
                return None
            parts.append(PassagePart(item_chapter, verse, item_chapter, verse))
            current_chapter = item_chapter
            continue

        left, right = [x.strip() for x in item.split('-', 1)]
        if ':' in left:
            left_chapter_text, left_verse_text = left.split(':', 1)
            try:
                start_chapter = int(left_chapter_text)
                start_verse = int(left_verse_text)
            except ValueError:
                return None
        else:
            start_chapter = current_chapter
            try:
                start_verse = int(left)
            except ValueError:
                return None
        if start_chapter <= 0 or start_verse <= 0:
            return None

        # Some source tables abbreviate cross-chapter ranges as C:V1-D:V2-V3
        # (meaning C:V1 through D:V3) or C:V1-Vend-D:V2
        # (meaning C:V1 through D:V2). Preserve these as one bounded span.
        m_cross_with_end_range = re.fullmatch(r'(?P<end_chapter>\d+):(?P<ignored_start_verse>\d+)-(?P<end_verse>\d+)', right)
        m_intermediate_then_cross = re.fullmatch(r'(?P<ignored_end_verse>\d+)-(?P<end_chapter>\d+):(?P<end_verse>\d+)', right)
        if m_cross_with_end_range:
            end_chapter = int(m_cross_with_end_range.group('end_chapter'))
            end_verse = int(m_cross_with_end_range.group('end_verse'))
        elif m_intermediate_then_cross:
            end_chapter = int(m_intermediate_then_cross.group('end_chapter'))
            end_verse = int(m_intermediate_then_cross.group('end_verse'))
        elif ':' in right:
            right_chapter, right_verse = right.split(':', 1)
            try:
                end_chapter = int(right_chapter)
                end_verse = int(right_verse)
            except ValueError:
                return None
        else:
            try:
                end_chapter = start_chapter
                end_verse = int(right)
            except ValueError:
                return None
        if end_chapter <= 0 or end_verse <= 0:
            return None
        parts.append(PassagePart(start_chapter, start_verse, end_chapter, end_verse))
        current_chapter = end_chapter

    return ParsedPassage(book, _canonical_from_parts(book, parts), parts)


def passages_overlap(query: ParsedPassage, candidate: ParsedPassage) -> bool:
    if query.book_abbrev != candidate.book_abbrev:
        return False

    def start_tuple(part: PassagePart):
        return (part.chapter_start, part.verse_start if part.verse_start is not None else 0)

    def end_tuple(part: PassagePart):
        return (part.chapter_end, part.verse_end if part.verse_end is not None else 10**9)

    for q in query.parts:
        for c in candidate.parts:
            if start_tuple(q) <= end_tuple(c) and start_tuple(c) <= end_tuple(q):
                return True
    return False


def passage_matches(query: Optional[str], candidate: Optional[str]) -> bool:
    query_variants_list = query_variants(query)
    candidate_parsed = parse_passage(candidate)
    if candidate_parsed:
        for variant in query_variants_list:
            query_parsed = parse_passage(variant)
            if query_parsed and passages_overlap(query_parsed, candidate_parsed):
                return True
    hay = compact(candidate or '')
    return any(compact(v) == hay for v in query_variants_list)


def normalize_numeric_ref(raw: Optional[str], books: Dict[int, str]) -> str:
    if not raw:
        return ''
    s = raw.strip()

    def repl(m):
        bid = int(m.group('book'))
        name = books.get(bid, f'Book{bid}')
        abbrev = BOOK_ABBREV.get(name, name)
        return f"{abbrev} {m.group('chapter')}:{m.group('verses').replace('*','')}"

    s = REF_TOKEN_RE.sub(repl, s)
    s = s.replace('@+', '; ').replace('@', '; ').replace('+', ' + ').replace('*', '')
    return re.sub(r'\s+', ' ', s).strip()


def iter_numeric_ref_segments(raw: str, books: Dict[int, str]):
    if not raw:
        return
    seen_segments: set[tuple[int, int, str]] = set()
    for m in REF_TOKEN_RE.finditer(raw):
        bid = int(m.group('book'))
        book = books.get(bid, f'Book{bid}')
        chapter = int(m.group('chapter'))
        verses = m.group('verses').replace('*', '').strip()
        for part in re.split(r'\s*,\s*', verses):
            part = part.strip()
            if not part:
                continue
            segment_key = (bid, chapter, part)
            if segment_key in seen_segments:
                continue
            seen_segments.add(segment_key)
            if '-' in part or '–' in part or '—' in part:
                nums = re.split(r'[-–—]', part, maxsplit=1)
                try:
                    start, end = int(nums[0]), int(nums[1])
                except Exception:
                    start = end = None
            else:
                try:
                    start = end = int(part)
                except Exception:
                    start = end = None
            yield {
                'book': book,
                'book_abbrev': BOOK_ABBREV.get(book, book),
                'chapter': chapter,
                'verse_start': start,
                'verse_end': end,
                'raw_segment': m.group(0),
                'normalized_segment': f"{BOOK_ABBREV.get(book, book)} {chapter}:{part}",
                'canonical_segment': f"{BOOK_ABBREV.get(book, book)} {chapter}:{part}",
            }


def _combine_open_ended(start: ParsedPassage, end: ParsedPassage) -> Optional[str]:
    if start.book_abbrev != end.book_abbrev or not start.parts or not end.parts:
        return None
    first = start.parts[0]
    last = end.parts[-1]
    combined = [PassagePart(first.chapter_start, first.verse_start, last.chapter_end, last.verse_end)]
    return _canonical_from_parts(start.book_abbrev, combined)


def extract_text_ref_tokens(raw_ref: Optional[str]) -> List[str]:
    if not raw_ref:
        return []
    raw_ref = repair_source_ref(raw_ref)
    raw_tokens = [_clean_token_spacing(m.group(0)) for m in TEXT_REF_RE.finditer(raw_ref)]
    out: List[str] = []
    i = 0
    while i < len(raw_tokens):
        token = raw_tokens[i]
        open_ended = token.endswith('-')
        base_token = token[:-1].strip() if open_ended else token
        parsed = parse_passage(base_token)
        if not parsed:
            i += 1
            continue
        if open_ended:
            if i + 1 < len(raw_tokens):
                next_parsed = parse_passage(raw_tokens[i + 1])
                combined = _combine_open_ended(parsed, next_parsed) if next_parsed else None
                if combined:
                    out.append(combined)
                    i += 2
                    continue
            i += 1
            continue
        out.append(parsed.canonical)
        i += 1
    return out


def canonicalize_text_ref(token: Optional[str]) -> str:
    parsed = parse_passage(token)
    if parsed:
        return parsed.canonical
    token = re.sub(r'\s+', ' ', (token or '').strip())
    return normalize_text_query(token)
