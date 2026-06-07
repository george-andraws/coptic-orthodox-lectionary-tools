#!/usr/bin/env python3
"""Query George's local Coptic Orthodox lectionary reference package.

Examples:
  python3 query_lectionary.py --passage "John 20"
  python3 query_lectionary.py --date 2026-04-12
  python3 query_lectionary.py --cycle-passage "Isa 2"
  python3 query_lectionary.py --pascha-day "Good Friday" --hour "Sixth Hour"
"""
import argparse, csv
from pathlib import Path

from passage_normalization import contains_any, is_numeric_query, parse_passage, passage_matches, query_variants

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'

def rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        yield from csv.DictReader(f)

def print_unique(lines, limit):
    seen=set()
    count=0
    for line in lines:
        if line in seen:
            continue
        print(line)
        seen.add(line)
        count += 1
        if count >= limit:
            break

def print_section(title, lines, limit):
    unique=[]
    seen=set()
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        unique.append(line)
        if len(unique) >= limit:
            break
    if not unique:
        return
    print(f'## {title}')
    for line in unique:
        print(line)

def crosswalk_lines(query, limit):
    path = DATA / 'reverse_lookup_crosswalk.csv'
    if not path.exists():
        return []
    exact_lines=[]
    source_lines=[]
    for r in rows(path):
        passage = r.get('passage','').strip()
        source_ref = r.get('source_ref','').strip()
        title = (r.get('day_title','') or r.get('liturgical_place','') or r.get('calendar_key','')).strip()
        section = (r.get('service_section','') or r.get('reading_type','')).strip()
        day = (r.get('gregorian_date','') or '').strip() or (r.get('coptic_date','') or '').strip() or (r.get('calendar_key','') or '').strip() or (r.get('liturgical_place','') or '').strip() or title
        title = title or day
        display_prefix = day if day != title else title
        calendar_key = (r.get('calendar_key','') or '').strip()
        if title and section and day == calendar_key and title in day and section in day:
            display_prefix = title
        if section and section != title:
            display_prefix = f"{display_prefix} | {section}"
        line = f"{display_prefix} | {r.get('reading_type','')} | {passage} | source={r.get('source_kind','')}"
        if passage_matches(query, passage):
            exact_lines.append(line)
        elif passage_matches(query, source_ref):
            source_lines.append(line)
    return (exact_lines or source_lines)[:limit]

def pascha_lines(day_query, hour_query, limit):
    path = DATA / 'pascha_day_hour_index.csv'
    if not path.exists():
        return []
    day_needles = query_variants(day_query)
    hour_needles = query_variants(hour_query) if hour_query else []
    lines=[]
    for r in rows(path):
        if not contains_any(r.get('day',''), day_needles):
            continue
        if hour_needles and not contains_any(r.get('hour',''), hour_needles):
            continue
        lines.append(f"{r.get('day','')} | {r.get('hour','')} | {r.get('slot','')} | {r.get('refs','')}")
    return lines[:limit]


def source_text_lines(query, hour_query, limit):
    path = DATA / 'pascha_source_text_index.csv'
    if not path.exists():
        return []
    needles = query_variants(query)
    hour_needles = query_variants(hour_query) if hour_query else []
    query_words = [w for w in query.lower().replace('_', ' ').split() if w]
    lines=[]
    for r in rows(path):
        hay = ' | '.join([
            r.get('day',''),
            r.get('hour',''),
            r.get('reading_type',''),
            r.get('raw_ref',''),
            r.get('normalized_ref',''),
            r.get('source_file',''),
            r.get('source_page',''),
        ])
        hay_norm = hay.lower().replace('_', ' ')
        if hour_needles and not contains_any(r.get('hour',''), hour_needles):
            continue
        matches_text = contains_any(hay, needles) or (query_words and all(w in hay_norm for w in query_words))
        matches_passage = bool(r.get('normalized_ref')) and passage_matches(query, r.get('normalized_ref',''))
        if matches_text or matches_passage:
            lines.append(
                f"{r.get('day','')} | {r.get('hour','')} | {r.get('reading_type','')} | "
                f"{r.get('normalized_ref','') or r.get('raw_ref','')} | raw={r.get('raw_ref','')} | "
                f"source={r.get('source_file','')}:{r.get('source_line','')} page={r.get('source_page','')}"
            )
    return lines[:limit]

def special_service_lines(query, limit):
    path = DATA / 'special_service_readings_curated.csv'
    if not path.exists():
        return []
    needles = query_variants(query)
    lines = []
    for r in rows(path):
        hay = ' | '.join([
            r.get('service_family',''),
            r.get('service_variant',''),
            r.get('section',''),
            r.get('reading_type',''),
            r.get('raw_ref',''),
            r.get('notes',''),
        ])
        hay = hay + ' | ' + hay.replace('_', ' ')
        hay_norm = hay.lower().replace('_', ' ')
        query_words = [w for w in query.lower().replace('_', ' ').split() if w]
        if contains_any(hay, needles) or (query_words and all(w in hay_norm for w in query_words)):
            lines.append(f"{r.get('service_family','')} | {r.get('service_variant','')} | {r.get('section','')} | {r.get('reading_type','')} | {r.get('raw_ref','')}")
    return lines[:limit]

def chapter_lines(query, limit):
    path = DATA / 'bible_chapter_lectionary_index.csv'
    if not path.exists():
        return []
    parsed = parse_passage(query)
    exact_chapter_ref = ''
    if parsed and parsed.parts:
        part = parsed.parts[0]
        # For chapter queries, use the starting chapter. Verse-level input like
        # "John 2:1" intentionally resolves to the chapter row "Jn 2".
        exact_chapter_ref = f"{parsed.book_abbrev} {part.chapter_start}"

    needles = query_variants(query)
    query_words = [w for w in query.lower().replace('_', ' ').split() if w]
    exact_lines=[]
    fuzzy_lines=[]
    for r in rows(path):
        line = (
            f"{r.get('chapter_ref','')} | read={r.get('is_read','')} | occurrences={r.get('occurrence_count','')} | "
            f"sources={r.get('source_kinds','')} | places={r.get('liturgical_places','')} | samples={r.get('sample_occurrences','')}"
        )
        if exact_chapter_ref and r.get('chapter_ref') == exact_chapter_ref:
            exact_lines.append(line)
            continue
        hay = ' | '.join([
            r.get('book',''),
            r.get('book_abbrev',''),
            r.get('chapter_ref',''),
            r.get('source_kinds',''),
            r.get('liturgical_places',''),
            r.get('service_sections',''),
            r.get('reading_types',''),
            r.get('sample_occurrences',''),
        ])
        hay_norm = hay.lower().replace('_', ' ')
        if not exact_chapter_ref and (contains_any(hay, needles) or (query_words and all(w in hay_norm for w in query_words))):
            fuzzy_lines.append(line)
    return (exact_lines or fuzzy_lines)[:limit]


def agpeya_lines(query, limit):
    path = DATA / 'agpeya_hour_readings.csv'
    if not path.exists():
        return []
    needles = query_variants(query)
    lines = []
    for r in rows(path):
        hay = ' | '.join([
            r.get('prayer_group',''),
            r.get('prayer_key',''),
            r.get('prayer_name',''),
            r.get('reading_type',''),
            r.get('raw_ref',''),
            r.get('display_ref',''),
            r.get('notes',''),
        ])
        if contains_any(hay, needles):
            display_ref = r.get('display_ref','') or r.get('raw_ref','')
            lines.append(f"{r.get('prayer_group','')} | {r.get('prayer_name','')} | {r.get('reading_type','')} | {display_ref}")
    return lines[:limit]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--date', help='Gregorian date YYYY-MM-DD, using copticchurch.net date-resolved cache')
    ap.add_argument('--passage', help='Find date-resolved occurrences by passage text, e.g. "John 20" or "Jn 20:1"')
    ap.add_argument('--cycle-passage', help='Find core Katameros cycle occurrences by normalized/raw passage text, e.g. "Isa 2" or "40.5"')
    ap.add_argument('--special-service', help='Find curated sacramental and special-service readings by service family, variant, section, reading type, or passage')
    ap.add_argument('--source-text', help='Find source-text extracted Holy Pascha readings by day, hour, reading type, passage, source file, or page')
    ap.add_argument('--agpeya', help='Find Agpeya hour/watch readings by prayer group, prayer name, reading type, or passage')
    ap.add_argument('--chapter', help='Find chapter-level lectionary coverage, e.g. "John 2", "Isa 53", or "Genesis 1"')
    ap.add_argument('--pascha-day', help='Find Pascha / Holy Week readings by day title, e.g. "Good Friday" or "Great Thursday"')
    ap.add_argument('--hour', help='Optional Pascha hour filter, e.g. "Sixth Hour"')
    ap.add_argument('--include-crosswalk', action='store_true', help='For --passage lookups, append reverse-crosswalk matches instead of using it only as a fallback')
    ap.add_argument('--limit', type=int, default=80)
    args=ap.parse_args()
    if args.date:
        lines=[]
        for r in rows(DATA/'copticchurch_date_readings_2020_2035.csv'):
            if r['gregorian_date']==args.date:
                lines.append(f"{r['gregorian_date']} | {r['day_title']} | {r['service_section']} | {r['reading_type']} | {r['raw_ref']}")
        print_unique(lines, args.limit)
        return
    if args.passage:
        lines=[]
        for r in rows(DATA/'copticchurch_passage_index_2020_2035.csv'):
            if passage_matches(args.passage, r.get('matched_ref','')) or passage_matches(args.passage, r.get('raw_ref','')):
                lines.append(f"{r['gregorian_date']} | {r['day_title']} | {r['service_section']} | {r['reading_type']} | {r['raw_ref']}")
        crosswalk = crosswalk_lines(args.passage, args.limit)
        if args.include_crosswalk:
            print_section('date results', lines, args.limit)
            print_section('reverse crosswalk results', crosswalk, args.limit)
        else:
            print_unique(lines or crosswalk, args.limit)
        return
    if args.pascha_day:
        print_unique(pascha_lines(args.pascha_day, args.hour, args.limit), args.limit)
        return
    if args.source_text:
        print_unique(source_text_lines(args.source_text, args.hour, args.limit), args.limit)
        return
    if args.special_service:
        print_unique(special_service_lines(args.special_service, args.limit), args.limit)
        return
    if args.agpeya:
        print_unique(agpeya_lines(args.agpeya, args.limit), args.limit)
        return
    if args.chapter:
        print_unique(chapter_lines(args.chapter, args.limit), args.limit)
        return
    if args.cycle_passage:
        if is_numeric_query(args.cycle_passage):
            needles=query_variants(args.cycle_passage)
            lines=[]
            for r in rows(DATA/'katameros_cycle_readings.csv'):
                hay=r.get('normalized_ref','')+' '+r.get('raw_ref','')
                if contains_any(hay, needles):
                    lines.append(f"{r['source_table']} | {r['day_key']} | {r['season']} | {r['reading_slot']} | {r['normalized_ref']} | raw={r['raw_ref']}")
        else:
            lines=[]
            for r in rows(DATA/'katameros_cycle_passage_index.csv'):
                if passage_matches(args.cycle_passage, r.get('canonical_segment','')) or passage_matches(args.cycle_passage, r.get('normalized_segment','')):
                    lines.append(f"{r['source_table']} | {r['day_key']} | {r['season']} | {r['reading_slot']} | {r['normalized_segment']} | raw={r['raw_ref']}")
        print_unique(lines, args.limit)
        return
    ap.print_help()

if __name__ == '__main__':
    main()
