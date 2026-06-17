#!/usr/bin/env python3
"""Build additive design-layer deliverables for the Coptic lectionary project.

This script does not replace the validated out/data package. It reads the
existing generated package and writes the new identity, attestation, temporal,
Synaxarium bridge, and site-facing deliverables under out/design plus the two
root Markdown deliverables requested by 05-LECTIONARY-DESIGN.md.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from passage_normalization import canonicalize_text_ref, extract_text_ref_tokens, parse_passage

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "out" / "data"
OUT = ROOT / "out" / "design"
AUDIT = ROOT / "audit_artifacts"
FIXTURE = ROOT / "tests" / "fixtures" / "pascha_wednesday_day_coptic_reader.json"
SYNAX = ROOT / "out3" / "synaxarium_day_index.csv"

OUT.mkdir(parents=True, exist_ok=True)
AUDIT.mkdir(parents=True, exist_ok=True)

SOURCE_REGISTRY = [
    {
        "source_key": "coptic_reader_fixture_wednesday_day",
        "title": "Coptic Reader app, Pascha Wednesday Day fixture supplied by George",
        "url": "tests/fixtures/pascha_wednesday_day_coptic_reader.json",
        "edition": "manual Coptic Reader fixture supplied by George, 2026-06-15",
        "default_locator": "tests/fixtures/pascha_wednesday_day_coptic_reader.json",
        "authority_tier": "current_authority",
        "confidence": "confirmed_for_wednesday_day_only",
        "notes": "Manual fixture from screenshots. Coptic Reader governs current practice where captured.",
    },
    {
        "source_key": "coptic_encyclopedia_lectionary",
        "title": "Coptic Encyclopedia, Lectionary entry, Claremont CCDL",
        "url": "https://ccdl.claremont.edu/digital/api/collection/cce/id/1199/download",
        "edition": "Claremont CCDL item 1199",
        "default_locator": "CCDL item 1199 download",
        "authority_tier": "scholarly_structural",
        "confidence": "confirmed",
        "notes": "Defines the lectionary as four books and explains historical development and calendar value.",
    },
    {
        "source_key": "fn_youssef_arrangement",
        "title": "Fouad Naguib Youssef, The Arrangement of the Church Lectionary, ACCOT",
        "url": "https://accot.stcyrils.edu.au/fny-read1/",
        "edition": "ACCOT web article accessed 2026-06-16",
        "default_locator": "ACCOT article page",
        "authority_tier": "scholarly_structural",
        "confidence": "confirmed_for_principles",
        "notes": "Explains calendar logic, Sunday cycle, and the relation of daily readings to the Synaxarium.",
    },
    {
        "source_key": "ugo_zanetti_annual_lectionaries",
        "title": "Ugo Zanetti, Les lectionnaires coptes annuels, Basse-Egypte",
        "url": "https://openlibrary.org/books/OL2304712M/Les_lectionnaires_coptes_annuels",
        "edition": "Publications de l'Institut Orientaliste de Louvain 33, Louvain-la-Neuve, 1985, xxiv + 383 p.",
        "default_locator": "BnF catalogue, Persee RHR review, and Zanetti published bibliography",
        "authority_tier": "scholarly_structural",
        "confidence": "bibliographic_confirmed_content_not_fully_ingested",
        "notes": "Standard scholarly study cited by the Coptic Encyclopedia for annual lectionaries.",
    },
    {
        "source_key": "st_mary_ottawa_days",
        "title": "St. Mary Ottawa / UKMID Katameros of the Days, Readings for Week Days and Feasts",
        "url": "https://ukmidcopts.org/pdf/Katameros_Days.pdf",
        "edition": "first edition, Christmas 1714 A.M., 1998 A.D.",
        "default_locator": "UKMID PDF TOC pages 23 to 26 plus printed section page",
        "authority_tier": "historical_printed_witness",
        "confidence": "confirmed_local_extraction_and_step1_audit",
        "notes": "First edition, Christmas 1714 A.M., 1998 A.D. Source for the 69 dated foundational-reading collection used as bridge taxonomy.",
    },
    {
        "source_key": "katameros_api_sqlite",
        "title": "pierresaid Katameros API SQLite source bundled in repo",
        "url": "sources/katameros-api/Core/KatamerosDatabase.db",
        "edition": "local repo snapshot of pierresaid Katameros API SQLite database",
        "default_locator": "source_file plus source_row_id",
        "authority_tier": "working_local_source",
        "confidence": "confirmed_local",
        "notes": "Main local structured source for annual, Sunday, Great Lent, and Holy Fifty cycle tables.",
    },
    {
        "source_key": "copticchurch_date_resolved",
        "title": "copticchurch.net date-resolved readings cache, 2020 to 2035",
        "url": "https://www.copticchurch.net/readings",
        "edition": "local cache covering 2020 to 2035",
        "default_locator": "row URL plus source_row_id",
        "authority_tier": "public_current_practice_reference",
        "confidence": "confirmed_local_cache",
        "notes": "Date-resolved public readings used by the existing local package.",
    },
    {
        "source_key": "st_mary_ottawa_pascha",
        "title": "St. Mary Ottawa Holy Pascha extracted text",
        "url": "out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt",
        "edition": "Lent 1734 A.M., 2018 A.D. eBook extracted text",
        "default_locator": "extracted text line and printed source page where available",
        "authority_tier": "historical_printed_witness",
        "confidence": "confirmed_local_extraction_with_known_parser_caveats",
        "notes": "Useful historical witness. Not current authority when it disagrees with Coptic Reader.",
    },
    {
        "source_key": "st_takla_synaxarium",
        "title": "St-Takla English Coptic Synaxarium day index",
        "url": "https://st-takla.org/Full-Free-Coptic-Books/Coptic-Synaxarium-or-Synaxarion_English/Eng-Synexarium-or-Synexarion-index.html",
        "edition": "St-Takla English web index accessed 2026-06-16",
        "default_locator": "source_url for each Coptic day page",
        "authority_tier": "synaxarium_text_source",
        "confidence": "confirmed_index_not_full_text_ingestion",
        "notes": "Used to store day commemorations and source URLs. Full text should be opened when exact wording matters.",
    },
    {
        "source_key": "special_service",
        "title": "Special-service readings extracted in the local package",
        "url": "out/data/reverse_lookup_crosswalk.csv",
        "edition": "local package snapshot",
        "default_locator": "source_file plus source_row_id",
        "authority_tier": "working_local_source",
        "confidence": "confirmed_local",
        "notes": "Local structured special-service rows retained with source labels and provenance.",
    },
    {
        "source_key": "agpeya",
        "title": "Agpeya readings extracted in the local package",
        "url": "out/data/reverse_lookup_crosswalk.csv",
        "edition": "local package snapshot",
        "default_locator": "source_file plus source_row_id",
        "authority_tier": "working_local_source",
        "confidence": "confirmed_local",
        "notes": "Local structured Agpeya rows retained with source labels and provenance.",
    },
    {
        "source_key": "bright_saturday_service_order",
        "title": "Bright Saturday service-order readings extracted in the local package",
        "url": "out/data/reverse_lookup_crosswalk.csv",
        "edition": "local package snapshot",
        "default_locator": "source_file plus source_row_id",
        "authority_tier": "working_local_source",
        "confidence": "confirmed_local",
        "notes": "Local structured Bright Saturday rows retained with source labels and provenance.",
    },
]

MONTH_MAP = {
    "tout": "Tut",
    "toot": "Tut",
    "tut": "Tut",
    "baba": "Babah",
    "babah": "Babah",
    "hator": "Hatur",
    "hatoor": "Hatur",
    "hatur": "Hatur",
    "kiahk": "Kiyahk",
    "kiyahk": "Kiyahk",
    "koiahk": "Kiyahk",
    "toba": "Tubah",
    "tubah": "Tubah",
    "amshir": "Amshir",
    "baramhat": "Baramhat",
    "bermoda": "Baramoudah",
    "baramoudah": "Baramoudah",
    "barmuda": "Baramoudah",
    "bashans": "Bashans",
    "baona": "Baunah",
    "baounah": "Baunah",
    "baunah": "Baunah",
    "abib": "Abib",
    "mesra": "Mesra",
    "nasie": "Al-Nasi",
    "nasi": "Al-Nasi",
    "al-nasi": "Al-Nasi",
}

SERVICE_ENUM = ["Vespers", "Matins", "Liturgy", "First Hour", "Third Hour", "Sixth Hour", "Ninth Hour", "Eleventh Hour", "Twelfth Hour", "Midnight Praises", "Special service", "Agpeya"]
HOUR_THEME = {
    "First Hour": "the beginning of the day and watchfulness",
    "Third Hour": "the descent of the Holy Spirit and the trial of the heart",
    "Sixth Hour": "the Cross and the Lord's willing suffering",
    "Ninth Hour": "the saving death of Christ and repentance",
    "Eleventh Hour": "the late call to repentance and mercy",
    "Twelfth Hour": "burial, waiting, and hope",
    "Liturgy": "the Eucharistic gathering of the Church",
    "Matins": "awakening to praise and repentance",
    "Vespers": "evening thanksgiving and watchfulness",
}

KNOWN_FIXTURE_MT_EQUIVALENTS = {
    "Ps 50:6": "Ps 51:4",
    "Ps 32:10": "Ps 33:10",
    "Ps 41:6": "Ps 42:5",
    "Ps 83:2": "Ps 84:1",
    "Ps 83:5": "Ps 84:4",
    "Ps 40:6-8": "Ps 41:5-7",
    "Ps 6:2-3": "Ps 6:1-2",
    "Ps 68:17": "Ps 69:16",
}

KNOWN_MT_TO_LXX_EQUIVALENTS = {mt: lxx for lxx, mt in KNOWN_FIXTURE_MT_EQUIVALENTS.items()}

UNRESOLVED_FIXTURE_LXX_REFS = {"Ps 41:1"}

FORBIDDEN_WORDS = ["delve", "multifaceted", "additionally", "landscape", "underscore", "foster", "interplay"]

FOUNDATIONAL_69_SOURCE_PROVENANCE = {
    "vocabulary_key": "foundational_reading_collections_69",
    "arabic_name": "al-qirā’āt al-āsāsiyya",
    "verdict_token": "CONFIRMED_SAME_SET",
    "membership_status": "confirmed_same_practical_second_volume_collection",
    "membership_basis": "Inferred from source identity, volume two placement, annual mapping function, commemoration categories, and count. The consulted Youssef page gives the concept, count, Arabic name, Synaxarium function, and second-volume placement, not the date-by-date roster.",
    "youssef_source": "F.N. Youssef, The Arrangement of the Church Lectionary, ACCOT",
    "youssef_locator": "Chapter 1, section 1.1, printed page marker 32; note 7 al-qirā’āt al-āsāsiyya",
    "ottawa_source": "St. Mary Ottawa / UKMID, Katameros of the Days, Readings for Week Days and Feasts",
    "ottawa_edition": "first edition, Christmas 1714 A.M., 1998 A.D.",
    "ottawa_url": "https://ukmidcopts.org/pdf/Katameros_Days.pdf",
    "ottawa_locator": "Introduction on PDF page 17; TOC dated reading sections on PDF pages 23 to 26; annual day table on PDF pages 31 to 65",
    "codex_audit_artifact": "audit_artifacts/phase7_codex_audit_of_grok_69_investigation.md",
}

FOUNDATIONAL_69_RAW = """1|Tut|1|37
2|Tut|2|47
3|Tut|8|55
4|Tut|16|64
5|Tut|17|72
6|Tut|18|81
7|Tut|19|88
8|Tut|21|96
9|Tut|26|102
10|Babah|12|111
11|Babah|14|118
12|Babah|22|127
13|Babah|27|135
14|Hatur|8|143
15|Hatur|9|151
16|Hatur|12|159
17|Hatur|15|169
18|Hatur|17|177
19|Hatur|22|187
20|Hatur|24|194
21|Hatur|25|202
22|Hatur|27|211
23|Hatur|28|218
24|Hatur|29|227
25|Kiyahk|22|236
26|Kiyahk|28|245
27|Kiyahk|29|255
28|Kiyahk|30|263
29|Tubah|1|270
30|Tubah|3|280
31|Tubah|4|288
32|Tubah|6|297
33|Tubah|10|305
34|Tubah|11|313
35|Tubah|12|322
36|Tubah|13|330
37|Tubah|22|338
38|Tubah|26|346
39|Tubah|30|354
40|Amshir|2|361
41|Baramhat|13|370
42|Baramhat|29|379
43|Baramoudah|23|388
44|Baramoudah|27|396
45|Baramoudah|30|404
46|Bashans|1|413
47|Bashans|10|423
48|Bashans|20|431
49|Bashans|24|439
50|Bashans|26|448
51|Baunah|2|456
52|Baunah|16|465
53|Baunah|30|473
54|Abib|3|481
55|Abib|5|491
56|Abib|20|500
57|Misra|3|507
58|Misra|13|515
59|Misra|17|524
60|Misra|25|532
61|Misra|26|540
62|Misra|28|547
63|Misra|29|555
64|Misra|30|562
65|Al-Nasi|1|569
66|Al-Nasi|2|579
67|Al-Nasi|3|586
68|Al-Nasi|4|595
69|Al-Nasi|6|602"""


REMOVED_PASCHA_WEDNESDAY_MARKER_BY_REF = {
    "Isa 48:1-6": "(removed, attested St. Mary Ottawa Holy Pascha p. 308 line 7779 as Isa 48:1-6; absent from Coptic Reader Wednesday Day fixture supplied by George)",
    "Isa 59:1-17": "(removed, attested St. Mary Ottawa Holy Pascha p. 320 line 8091 as Isa 59:1-17; absent from Coptic Reader Wednesday Day fixture supplied by George)",
    "Zech 11:11-14": "(removed, attested St. Mary Ottawa Holy Pascha p. 322 line 8133 as Zech 11:11-14; absent from Coptic Reader Wednesday Day fixture supplied by George)",
    "Prov 1:10-33": "(removed, attested St. Mary Ottawa Holy Pascha p. 318 line 8038 as Prov 1:10-33; absent from Coptic Reader Wednesday Day fixture supplied by George)",
    "Prov 4:4-27,5:1-4": "(removed, attested St. Mary Ottawa Holy Pascha p. 299 line 7552 as Prov 4:4-27,5:1-4; absent from Coptic Reader Wednesday Day fixture supplied by George)",
    "Prov 4:4-5:4": "(removed, attested St. Mary Ottawa Holy Pascha p. 299 line 7552 as Prov 4:4-27,5:1-4; absent from Coptic Reader Wednesday Day fixture supplied by George)",
    "Job 27:16-28:2": "(removed, attested St. Mary Ottawa Holy Pascha p. 298 line 7519 as Job 27:16-28:2; absent from Coptic Reader Wednesday Day fixture supplied by George)",
    "Job 27:16-20": "(removed, attested St. Mary Ottawa Holy Pascha p. 298 line 7519 as Job 27:16-28:2; absent from Coptic Reader Wednesday Day fixture supplied by George)",
    "Job 28:1-2": "(removed, attested St. Mary Ottawa Holy Pascha p. 298 line 7519 as Job 27:16-28:2; absent from Coptic Reader Wednesday Day fixture supplied by George)",
}

REMOVED_PASCHA_SOURCE_TEXT_REFS = {
    "Isa 48:1-6",
    "Isa 59:1-17",
    "Zech 11:11-14",
    "Prov 1:10-33",
    "Prov 4:4-27,5:1-4",
    "Job 27:16-28:2",
}


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Iterable[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value.lower()).strip("-")
    return value or "item"


def build_foundational_reading_collections_69() -> list[dict]:
    provenance = FOUNDATIONAL_69_SOURCE_PROVENANCE
    rows = []
    for line in FOUNDATIONAL_69_RAW.splitlines():
        sequence_s, month, day_s, section_page_s = line.split("|")
        sequence = int(sequence_s)
        day = int(day_s)
        section_page = int(section_page_s)
        collection_key = f"foundational-{sequence:02d}-{slugify(month)}-{day:02d}"
        coptic_day_key = f"{month} {day}"
        rows.append({
            "collection_key": collection_key,
            "sequence": sequence,
            "coptic_month": month,
            "coptic_day": day,
            "coptic_day_key": coptic_day_key,
            "calendar_key": coptic_day_key,
            "toc_label": f"{day} {month}",
            "reading_section_start_page": section_page,
            "source_key": "st_mary_ottawa_days",
            "source_title": provenance["ottawa_source"],
            "source_edition": provenance["ottawa_edition"],
            "source_url": provenance["ottawa_url"],
            "source_locator": f"TOC dated reading section, PDF pages 23 to 26; section begins on printed page {section_page}",
            "membership_status": provenance["membership_status"],
            "membership_verdict": provenance["verdict_token"],
            "membership_basis": provenance["membership_basis"],
            "verification_status": "read_from_ottawa_toc_inferred_same_set_from_step1_audit",
        })
    return rows


def foundational_69_by_day_key() -> dict[str, dict]:
    return {row["coptic_day_key"]: row for row in build_foundational_reading_collections_69()}


def removed_marker_for(row: dict, ident: dict) -> str:
    if row.get("day_title") != "Wednesday" or row.get("service_hour") not in {"First Hour", "Third Hour", "Sixth Hour", "Ninth Hour", "Eleventh Hour"}:
        return ""
    if row.get("source_kind") not in {"pascha_day_hour", "pascha_source_text"}:
        return ""
    candidates = [
        ident.get("display_ref", ""),
        ident.get("canonical_mt_ref", ""),
        row.get("normalized_ref", ""),
        row.get("normalized_segment", ""),
        row.get("source_ref", ""),
        row.get("raw_ref", ""),
        row.get("passage", ""),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        normalized = normalize_source_ref(candidate, row.get("source_kind", ""))
        if normalized in REMOVED_PASCHA_WEDNESDAY_MARKER_BY_REF:
            return REMOVED_PASCHA_WEDNESDAY_MARKER_BY_REF[normalized]
        if candidate in REMOVED_PASCHA_WEDNESDAY_MARKER_BY_REF:
            return REMOVED_PASCHA_WEDNESDAY_MARKER_BY_REF[candidate]
    return ""


def load_removed_pascha_source_text_supplement(base_rows: list[dict]) -> list[dict]:
    source_index = DATA / "pascha_source_text_index.csv"
    if not source_index.exists():
        return []
    existing = {
        (row.get("source_kind", ""), str(row.get("source_row_id", "") or row.get("source_line", "")))
        for row in base_rows
    }
    rows = []
    for source_row in read_csv(source_index):
        normalized_ref = source_row.get("normalized_ref", "")
        if source_row.get("day") != "Wednesday" or normalized_ref not in REMOVED_PASCHA_SOURCE_TEXT_REFS:
            continue
        source_line = source_row.get("source_line", "")
        if ("pascha_source_text", str(source_line)) in existing:
            continue
        hour = source_row.get("hour", "")
        rows.append({
            "passage": normalized_ref,
            "source_kind": "pascha_source_text",
            "source_family": source_row.get("source_family", "holy_pascha"),
            "source_table": "pascha_source_text_index",
            "source_file": source_row.get("source_file", ""),
            "source_row_id": source_line,
            "liturgical_place": f"Wednesday | {hour}",
            "calendar_key": f"Wednesday | {hour}",
            "day_title": "Wednesday",
            "service_day": "Wednesday",
            "service_hour": hour,
            "service_section": hour,
            "reading_slot": source_row.get("reading_type", "Prophecy"),
            "reading_type": source_row.get("reading_type", "Prophecy"),
            "source_ref": normalized_ref,
            "raw_ref": source_row.get("raw_ref", normalized_ref),
            "normalized_ref": normalized_ref,
            "normalized_segment": normalized_ref,
            "provenance": f"{source_row.get('source_file', '')}:{source_line}; source_page={source_row.get('source_page', '')}",
        })
    return rows


def norm_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def canonical_ref(value: str) -> str:
    value = value.replace("Psalm", "Ps").replace("Psalms", "Ps")
    return canonicalize_text_ref(value) or norm_space(value)


def fixture_preserve_ref(value: str) -> str:
    value = norm_space(value)
    value = re.sub(r"^Psalms?\b", "Ps", value)
    return value


def normalize_source_ref(value: str, source_kind: str = "") -> str:
    if source_kind == "coptic_reader_fixture" and re.match(r"^Psalms?\b|^Ps\b", norm_space(value)):
        return fixture_preserve_ref(value)
    return canonical_ref(value)


def mt_to_lxx_psalm_chapter(mt_chapter: int, verse_start: int | None = None) -> int | str:
    if 1 <= mt_chapter <= 8:
        return mt_chapter
    if mt_chapter in (9, 10):
        return 9
    if 11 <= mt_chapter <= 113:
        return mt_chapter - 1
    if mt_chapter in (114, 115):
        return 113
    if mt_chapter == 116:
        return 114 if verse_start is not None and verse_start <= 9 else 115
    if 117 <= mt_chapter <= 146:
        return mt_chapter - 1
    if mt_chapter == 147:
        return 146 if verse_start is not None and verse_start <= 11 else 147
    if 148 <= mt_chapter <= 150:
        return mt_chapter
    return "unmapped"


def lxx_to_mt_psalm_chapter(lxx_chapter: int) -> int | str:
    """Return chapter-level MT counterpart for a LXX Psalm chapter.

    This deliberately does not guess verse offsets. Merged/split seam chapters
    remain explicit because the project brief requires Brenton text validation,
    not a flat numeric shift.
    """
    if 1 <= lxx_chapter <= 8:
        return lxx_chapter
    if lxx_chapter == 9:
        return "MT 9-10"
    if 10 <= lxx_chapter <= 112:
        return lxx_chapter + 1
    if lxx_chapter == 113:
        return "MT 114-115"
    if lxx_chapter in (114, 115):
        return "MT 116"
    if 116 <= lxx_chapter <= 145:
        return lxx_chapter + 1
    if lxx_chapter in (146, 147):
        return "MT 147"
    if 148 <= lxx_chapter <= 150:
        return lxx_chapter
    if lxx_chapter == 151:
        return "none"
    return "unmapped"


def fixture_lxx_to_mt_ref(lxx_ref: str) -> tuple[str, str, str]:
    """Map a Coptic Reader fixture Psalm label from LXX to MT when safe.

    The active design brief says the Wednesday fixture labels, including Ps 41
    and Ps 83, are faithful to screenshots and govern within scope. This helper
    therefore preserves those labels and only flags exact MT verse equivalence
    when Brenton text comparison is not encoded.
    """
    lxx_ref = fixture_preserve_ref(lxx_ref)
    if lxx_ref in KNOWN_FIXTURE_MT_EQUIVALENTS:
        return KNOWN_FIXTURE_MT_EQUIVALENTS[lxx_ref], "known_fixture_equivalence", "high"
    if lxx_ref in UNRESOLVED_FIXTURE_LXX_REFS:
        return "", "fixture_label_preserved_mt_equivalence_requires_text_review", "medium"
    parsed = parse_passage(lxx_ref)
    if not parsed or parsed.book_abbrev != "Ps" or not parsed.parts:
        return lxx_ref, "not_psalm_or_unparsed", "n/a"
    mt_pieces = []
    notes = []
    confidence = "medium"
    for part in parsed.parts:
        mt_ch = lxx_to_mt_psalm_chapter(part.chapter_start)
        if isinstance(mt_ch, int):
            verse = ""
            if part.verse_start is not None:
                verse = f":{part.verse_start}"
                if part.verse_end is not None and part.verse_end != part.verse_start:
                    verse += f"-{part.verse_end}"
            mt_pieces.append(f"Ps {mt_ch}{verse}")
            notes.append("chapter_mapped_verse_offset_not_guessed")
        elif mt_ch == "none":
            notes.append("lxx_only_psalm_no_mt_counterpart")
            confidence = "high"
        else:
            mt_pieces.append(f"Ps {mt_ch}")
            notes.append("seam_chapter_ambiguous_text_match_required")
    return "; ".join(p for p in mt_pieces if p), "; ".join(sorted(set(notes))), confidence


def psalm_lxx_ref(mt_ref: str) -> tuple[str, str, str]:
    mt_ref = canonical_ref(mt_ref)
    if mt_ref in KNOWN_MT_TO_LXX_EQUIVALENTS:
        return KNOWN_MT_TO_LXX_EQUIVALENTS[mt_ref], "known_content_compared_mt_to_lxx_equivalence", "high"
    parsed = parse_passage(mt_ref)
    if not parsed or parsed.book_abbrev != "Ps" or not parsed.parts:
        return mt_ref, "not_psalm_or_unparsed", "n/a"
    pieces = []
    notes = []
    for part in parsed.parts:
        lxx_ch = mt_to_lxx_psalm_chapter(part.chapter_start, part.verse_start)
        if lxx_ch == "unmapped":
            pieces.append(mt_ref)
            notes.append("unmapped_psalm_chapter")
            continue
        if lxx_ch == part.chapter_start:
            pieces.append(mt_ref)
        else:
            verse = ""
            if part.verse_start is not None:
                verse = f":{part.verse_start}"
                if part.verse_end is not None and part.verse_end != part.verse_start:
                    verse += f"-{part.verse_end}"
            pieces.append(f"Ps {lxx_ch}{verse}")
            notes.append("chapter_mapped_verse_offset_not_guessed")
    if not notes:
        return mt_ref, "same_chapter", "high"
    return "; ".join(pieces), "; ".join(sorted(set(notes))), "medium"


def passage_type(passage: str) -> str:
    parsed = parse_passage(passage)
    if parsed:
        return "scripture"
    if passage.lower().startswith("memoirs of"):
        return "named-reading"
    return "named-reading"


def source_convention(row: dict) -> str:
    if row.get("source_kind") == "coptic_reader_fixture":
        return "lxx_liturgical_or_fixture_label"
    if (row.get("book_abbrev") or "") == "Ps" or canonical_ref(row.get("passage", "")).startswith("Ps "):
        return "mt_nkjv"
    return "modern_english_reference"


def identity_for(passage: str, source_kind: str = "") -> dict:
    passage = normalize_source_ref(passage, source_kind)
    parsed = parse_passage(passage)
    ptype = passage_type(passage)
    canonical_mt = passage if parsed else ""
    canonical_lxx = canonical_mt
    note = ""
    confidence = "high"
    convention = "modern_english_reference"
    if parsed and parsed.book_abbrev == "Ps":
        canonical_lxx, note, confidence = psalm_lxx_ref(canonical_mt)
        convention = "mt_nkjv"
    if source_kind == "coptic_reader_fixture":
        convention = "lxx_liturgical_or_fixture_label"
        if parsed and parsed.book_abbrev == "Ps":
            canonical_lxx = passage
            canonical_mt, note, confidence = fixture_lxx_to_mt_ref(passage)
            if note == "known_fixture_equivalence":
                note = "fixture label mapped by prior content comparison"
            else:
                note = "Coptic Reader fixture label preserved as authoritative; exact MT verse equivalent requires Brenton text comparison. " + note
    display = canonical_mt or passage
    if canonical_lxx and canonical_mt and canonical_lxx != canonical_mt:
        display = f"{canonical_mt} (LXX {canonical_lxx})"
    elif source_kind == "coptic_reader_fixture" and canonical_lxx and not canonical_mt:
        display = f"LXX {canonical_lxx} (MT equivalent pending)"
    if ptype == "scripture":
        key_material = "|".join([ptype, canonical_mt, canonical_lxx])
    else:
        key_material = "|".join([ptype, passage])
    identity_key = "rid_" + hashlib.sha256(key_material.encode("utf-8")).hexdigest()[:20]
    spans = []
    if parsed and parsed.parts:
        for part in parsed.parts:
            spans.append({
                "source_ref": passage,
                "source_convention": convention,
                "canonical_mt_ref": canonical_mt,
                "canonical_lxx_ref": canonical_lxx,
                "confidence": confidence,
                "validation_basis": note,
                "book": parsed.book_abbrev,
                "chapter_start": part.chapter_start,
                "verse_start": part.verse_start,
                "chapter_end": part.chapter_end,
                "verse_end": part.verse_end,
            })
    reading_name = passage if ptype != "scripture" else ""
    return {
        "identity_key": identity_key,
        "reading_type": ptype,
        "reading_name": reading_name,
        "source_label": passage,
        "display_ref": display,
        "canonical_mt_ref": canonical_mt,
        "canonical_lxx_ref": canonical_lxx,
        "source_convention": convention,
        "canonicalization_confidence": confidence,
        "canonicalization_note": note,
        "spans_json": json.dumps(spans, ensure_ascii=False, sort_keys=True),
    }


def load_fixture_rows() -> list[dict]:
    if not FIXTURE.exists():
        return []
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    rows = []
    order = 0
    for hour in data.get("hours", []):
        display_hour = hour.get("display_hour", "")
        hour_name = {
            "1st Hour": "First Hour",
            "3rd Hour": "Third Hour",
            "6th Hour": "Sixth Hour",
            "9th Hour": "Ninth Hour",
            "11th Hour": "Eleventh Hour",
        }.get(display_hour, display_hour)
        for reading in hour.get("readings", []):
            order += 1
            raw = reading.get("reading", "")
            cref = normalize_source_ref(raw, "coptic_reader_fixture") if reading.get("reference_status") != "named_non_versed" else raw
            ident = identity_for(cref, "coptic_reader_fixture")
            parsed_cref = parse_passage(cref)
            rows.append({
                "passage": cref,
                "source_kind": "coptic_reader_fixture",
                "source_family": "coptic_reader",
                "source_table": "pascha_wednesday_day_coptic_reader_fixture",
                "source_file": str(FIXTURE.relative_to(ROOT)),
                "source_row_id": order,
                "liturgical_place": "Wednesday of Holy Pascha",
                "calendar_key": f"Wednesday | {hour_name}",
                "gregorian_date": "",
                "coptic_date": "",
                "day_title": "Wednesday",
                "service_day": "Wednesday",
                "service_hour": hour_name,
                "service_section": hour_name,
                "reading_slot": reading.get("slot", ""),
                "reading_type": reading.get("slot", ""),
                "source_ref": raw,
                "raw_ref": raw,
                "normalized_ref": cref,
                "normalized_segment": cref,
                "book": "",
                "book_abbrev": parsed_cref.book_abbrev if parsed_cref else "",
                "chapter_start": "",
                "verse_start": "",
                "chapter_end": "",
                "verse_end": "",
                "significance_note": "Coptic Reader current-practice fixture for Wednesday Day",
                "synaxarium_note": "",
                "url": "",
                "provenance": "Coptic Reader screenshot fixture supplied by George",
            })
    return rows


def source_key_for(row: dict) -> str:
    sk = row.get("source_kind", "")
    if sk == "coptic_reader_fixture":
        return "coptic_reader_fixture_wednesday_day"
    if sk == "copticchurch_date":
        return "copticchurch_date_resolved"
    if sk == "katameros_cycle":
        return "katameros_api_sqlite"
    if sk == "pascha_source_text":
        return "st_mary_ottawa_pascha"
    if sk == "pascha_day_hour":
        return "katameros_api_sqlite"
    return sk or "unknown"


SOURCE_REGISTRY_BY_KEY = {row["source_key"]: row for row in SOURCE_REGISTRY}


def source_registry_for_key(source_key: str) -> dict:
    return SOURCE_REGISTRY_BY_KEY.get(source_key, {})


def source_locator_for(row: dict, registry_entry: dict) -> str:
    locators = []
    row_url = row.get("url", "")
    source_file = row.get("source_file", "")
    source_row_id = str(row.get("source_row_id", "") or "")
    if row_url:
        locators.append(row_url)
    if source_file and source_row_id:
        locator_kind = "line" if row.get("source_kind") == "pascha_source_text" else "row"
        locators.append(f"{source_file}:{locator_kind} {source_row_id}")
    elif source_file:
        locators.append(source_file)
    source_ref = row.get("source_ref", "") or row.get("raw_ref", "")
    if source_ref:
        locators.append(f"source_ref={source_ref}")
    if not locators and registry_entry.get("default_locator"):
        locators.append(registry_entry.get("default_locator", ""))
    return "; ".join(dict.fromkeys(part for part in locators if part))


def fixture_current_keys(fixture_rows: list[dict]) -> set[tuple[str, str, str]]:
    keys = set()
    for row in fixture_rows:
        ident = identity_for(row.get("normalized_ref") or row.get("passage") or "", row.get("source_kind", ""))
        ref = ident["canonical_mt_ref"] or ident["source_label"]
        keys.add((row.get("day_title", ""), row.get("service_hour", ""), canonical_ref(ref)))
    return keys


def status_for(row: dict, ident: dict, current_fixture_keys: set[tuple[str, str, str]]) -> tuple[str, str]:
    source_kind = row.get("source_kind", "")
    ref = canonical_ref(ident.get("canonical_mt_ref") or ident.get("source_label") or row.get("passage", ""))
    key = (row.get("day_title", ""), row.get("service_hour", ""), ref)
    if source_kind == "coptic_reader_fixture":
        return "current_confirmed_coptic_reader", "Current where fixture scope applies."
    if removed_marker_for(row, ident):
        return "historical_candidate_removed", "Older Pascha source attests this placement, but the scoped Coptic Reader Wednesday Day fixture lacks it."
    if row.get("day_title") == "Wednesday" and row.get("service_hour") in {"First Hour", "Third Hour", "Sixth Hour", "Ninth Hour", "Eleventh Hour"} and source_kind == "pascha_day_hour":
        if key in current_fixture_keys:
            return "current_confirmed_by_fixture_equivalence", "Matched the Coptic Reader Wednesday Day fixture after normalization."
        if row.get("reading_type") in {"Psalm+Gospel", "psalm", "gospel"}:
            return "pending_psalm_equivalence_unresolved", "Psalm or bundled Psalm+Gospel row needs screenshot-level Psalm convention review."
        return "historical_candidate_removed", "Present in older/local Pascha data but absent from the Coptic Reader Wednesday Day fixture."
    if source_kind == "pascha_source_text":
        return "historical_witness", "Printed-source witness retained for historical comparison."
    if source_kind == "pascha_day_hour":
        return "current_working_source_not_coptic_reader_checked", "Current candidate from local Pascha source layer. Not independently verified against Coptic Reader outside fixture scope."
    if source_kind in {"copticchurch_date", "katameros_cycle", "special_service", "agpeya", "bright_saturday_service_order"}:
        return "current_public_or_local_reference", "Current working reference in George's local package."
    return "unknown", "No status rule matched."


def build_reverse_presentation() -> tuple[list[dict], dict[str, dict]]:
    base_rows = read_csv(DATA / "reverse_lookup_crosswalk.csv")
    supplement_rows = load_removed_pascha_source_text_supplement(base_rows)
    fixture_rows = load_fixture_rows()
    all_rows = base_rows + supplement_rows + fixture_rows
    current_keys = fixture_current_keys(fixture_rows)
    identities: dict[str, dict] = {}
    presentation_rows = []
    for row in all_rows:
        if row.get("source_kind") == "coptic_reader_fixture":
            passage = row.get("normalized_segment") or row.get("normalized_ref") or row.get("source_ref") or row.get("passage") or ""
        else:
            passage = row.get("passage") or row.get("normalized_segment") or row.get("normalized_ref") or row.get("source_ref") or ""
        ident = identity_for(passage, row.get("source_kind", ""))
        identities[ident["identity_key"]] = ident
        current_status, status_note = status_for(row, ident, current_keys)
        removed_marker = removed_marker_for(row, ident)
        source_key = source_key_for(row)
        registry_entry = source_registry_for_key(source_key)
        source_locator = source_locator_for(row, registry_entry)
        section = row.get("service_section") or row.get("service_hour") or row.get("reading_type") or ""
        hour_theme = HOUR_THEME.get(row.get("service_hour") or row.get("service_section") or "", "")
        presentation_rows.append({
            **ident,
            "current_status": current_status,
            "status_note": status_note,
            "removed_marker": removed_marker,
            "source_key": source_key,
            "source_title": registry_entry.get("title", ""),
            "source_edition": registry_entry.get("edition", ""),
            "source_locator": source_locator,
            "source_url": row.get("url", "") or registry_entry.get("url", ""),
            "source_kind": row.get("source_kind", ""),
            "source_family": row.get("source_family", ""),
            "source_file": row.get("source_file", ""),
            "source_row_id": row.get("source_row_id", ""),
            "authority_tier": registry_entry.get("authority_tier", "unclassified"),
            "occasion": row.get("liturgical_place") or row.get("day_title") or row.get("calendar_key") or "",
            "calendar_key": row.get("calendar_key", ""),
            "gregorian_date": row.get("gregorian_date", ""),
            "coptic_date": row.get("coptic_date", ""),
            "day_title": row.get("day_title", ""),
            "service_day": row.get("service_day", ""),
            "service_hour": row.get("service_hour", ""),
            "service_section": section,
            "reading_slot": row.get("reading_slot", ""),
            "slot": row.get("reading_slot") or row.get("reading_type") or "",
            "order": row.get("source_row_id", ""),
            "hour_theme": hour_theme,
            "source_ref": row.get("source_ref", ""),
            "raw_ref": row.get("raw_ref", ""),
            "url": row.get("url", ""),
            "provenance": row.get("provenance", ""),
        })
    return presentation_rows, identities


def build_psalm_crosswalk() -> list[dict]:
    rows = []
    for mt in range(1, 151):
        lxx = mt_to_lxx_psalm_chapter(mt)
        if lxx == "unmapped":
            confidence = "none"
            note = "No LXX counterpart mapped."
        elif lxx == mt:
            confidence = "high"
            note = "Chapter number is the same in MT and LXX. Verse numbering still needs text check for exact quotation work."
        else:
            confidence = "high_chapter_medium_verse"
            note = "Chapter seam is mapped. Verse offsets are not guessed by this table. Validate exact verses by Brenton text comparison."
        rows.append({
            "mt_psalm": mt,
            "lxx_psalm": lxx,
            "map_direction": "mt_to_lxx",
            "mapping_scope": "chapter_equivalence" if confidence == "high" else "split_merge_chapter_seam",
            "confidence": confidence,
            "validation_basis": "Coptic lectionary design brief Section 7.2 plus phase2b Psalm numbering audit",
            "note": note,
        })
    rows.append({
        "mt_psalm": "none",
        "lxx_psalm": 151,
        "map_direction": "lxx_only",
        "mapping_scope": "lxx_unique_chapter",
        "confidence": "high_chapter",
        "validation_basis": "Coptic canon includes Psalm 151 in the LXX tradition",
        "note": "No MT counterpart.",
    })
    seam_examples = [
        ("Ps 51:4", "Ps 50:6", "content compared: Brenton LXX Ps 50:6 with KJV Ps 51:4"),
        ("Ps 33:10", "Ps 32:10", "content compared: Brenton LXX Ps 32:10 with KJV Ps 33:10"),
        ("Ps 42:5", "Ps 41:6", "content compared: Brenton LXX Ps 41:6 with KJV Ps 42:5"),
        ("Ps 84:1", "Ps 83:2", "content compared: Brenton LXX Ps 83:2 with KJV Ps 84:1"),
        ("Ps 84:4", "Ps 83:5", "content compared: Brenton LXX Ps 83:5 with KJV Ps 84:4"),
        ("Ps 41:5-7", "Ps 40:6-8", "content compared: Brenton LXX Ps 40:6-8 with KJV Ps 41:5-7"),
        ("Ps 6:1-2", "Ps 6:2-3", "content compared: Brenton LXX Ps 6:2-3 with KJV Ps 6:1-2"),
        ("Ps 69:16", "Ps 68:17", "content compared: Brenton LXX Ps 68:17 with KJV Ps 69:16"),
        ("Ps 63:1", "Ps 62", "chapter seam verified; exact verse needs text check"),
        ("Ps 68:17", "Ps 67", "chapter seam verified; Hatur 8 exact verse needs text check"),
    ]
    for mt_ref, lxx_ref, basis in seam_examples:
        rows.append({
            "mt_psalm": mt_ref,
            "lxx_psalm": lxx_ref,
            "map_direction": "example_ref",
            "mapping_scope": "anchored_verse_example" if "content compared" in basis else "unresolved_verse_offset_example",
            "confidence": "high" if "content" in basis else "medium",
            "validation_basis": basis,
            "note": "Reference-level seam example used by the verifier and audit notes. This is not a complete verse-by-verse Psalm alignment.",
        })
    return rows


def row_citation(row: dict) -> str:
    parts = [
        f"source_key={row.get('source_key', '')}",
        f"source_title={row.get('source_title', '')}",
        f"source_edition={row.get('source_edition', '')}",
        f"source_locator={row.get('source_locator', '')}",
        f"source_file={row.get('source_file', '')}",
        f"source_row_id={row.get('source_row_id', '')}",
        f"source_ref={row.get('source_ref', '') or row.get('raw_ref', '')}",
    ]
    provenance = row.get("provenance", "")
    if provenance and provenance != "api":
        parts.append(f"provenance={provenance}")
    elif provenance == "api":
        parts.append("provenance=api extraction, replay using source_file and source_row_id")
    url = row.get("url", "")
    if url:
        parts.append(f"url={url}")
    return " | ".join(part for part in parts if not part.endswith("="))


def attestation_note(bucket: str, rows: list[dict], statuses: list[str]) -> str:
    if "pending_psalm_equivalence_unresolved" in statuses:
        refs = "; ".join(sorted(set(r.get("source_ref", "") or r.get("raw_ref", "") for r in rows)))
        return "Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: " + refs
    if bucket == "old_edition_only_candidate_removed":
        return "Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture. Retained as candidate removed reading, not deleted."
    if bucket == "old_edition_only":
        return "Historical printed witness retained for comparison. Not current authority where Coptic Reader fixture applies."
    if bucket == "current_confirmed":
        return "Current within captured Coptic Reader fixture scope or matched to that fixture after canonical identity normalization."
    if bucket == "consensus_without_coptic_reader":
        return "Two or more non-Coptic Reader sources agree after normalization, but no Coptic Reader fixture is present for this placement."
    return "Single-source candidate retained with source citation. Not promoted to current Coptic Reader authority."


def build_attestation(presentation_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in presentation_rows:
        if row.get("source_kind") not in {"pascha_day_hour", "pascha_source_text", "coptic_reader_fixture"}:
            continue
        key = (row.get("day_title", ""), row.get("service_hour") or row.get("service_section", ""), row.get("identity_key", ""))
        groups[key].append(row)
    attestation = []
    temporal = []
    for (day, hour, identity_key), rows in sorted(groups.items()):
        source_keys = sorted(set(r.get("source_key", "") for r in rows))
        source_titles = sorted(set(r.get("source_title", "") for r in rows if r.get("source_title")))
        source_editions = sorted(set(r.get("source_edition", "") for r in rows if r.get("source_edition")))
        source_locators = sorted(set(r.get("source_locator", "") for r in rows if r.get("source_locator")))
        statuses = sorted(set(r.get("current_status", "") for r in rows))
        removed_markers = sorted(set(r.get("removed_marker", "") for r in rows if r.get("removed_marker")))
        if "coptic_reader_fixture_wednesday_day" in source_keys:
            bucket = "current_confirmed"
        elif any("historical_candidate_removed" == s for s in statuses):
            bucket = "old_edition_only_candidate_removed"
        elif len(source_keys) >= 2:
            bucket = "consensus_without_coptic_reader"
        elif source_keys == ["st_mary_ottawa_pascha"]:
            bucket = "old_edition_only"
        else:
            bucket = "single_source_candidate"
        sample = rows[0]
        attestation.append({
            "day_title": day,
            "service_hour": hour,
            "identity_key": identity_key,
            "display_ref": sample.get("display_ref", ""),
            "source_count": len(source_keys),
            "sources": "; ".join(source_keys),
            "source_titles": "; ".join(source_titles),
            "source_editions": "; ".join(source_editions),
            "source_locators": " || ".join(source_locators)[:2000],
            "bucket": bucket,
            "statuses": "; ".join(statuses),
            "removed_marker": "; ".join(removed_markers),
            "citation": "; ".join(row_citation(r) for r in rows)[:1000],
            "attestation_note": attestation_note(bucket, rows, statuses),
        })
        source_authority_tiers = sorted(set(r.get("authority_tier", "") for r in rows if r.get("authority_tier")))
        if bucket == "current_confirmed":
            valid_from, valid_to, lifecycle = "current", "", "current"
            current_authority = "Coptic Reader fixture where captured"
        elif bucket in {"old_edition_only", "old_edition_only_candidate_removed"}:
            valid_from, valid_to, lifecycle = "historical witness", "before current Coptic Reader fixture where fixture applies", "historical_or_removed"
            current_authority = "historical source is witness only"
        else:
            valid_from, valid_to, lifecycle = "undated", "", "candidate_current_pending_current_authority_check"
            current_authority = "no scoped current authority confirmation"
        temporal.append({
            "day_title": day,
            "service_hour": hour,
            "identity_key": identity_key,
            "display_ref": sample.get("display_ref", ""),
            "lifecycle_status": lifecycle,
            "current_status": "; ".join(statuses),
            "removed_marker": "; ".join(removed_markers),
            "source_authority_tier": "; ".join(source_authority_tiers),
            "source_titles": "; ".join(source_titles),
            "source_editions": "; ".join(source_editions),
            "source_locators": " || ".join(source_locators)[:2000],
            "attestation_bucket": bucket,
            "current_authority": current_authority,
            "valid_from": valid_from,
            "valid_to": valid_to,
            "derivation": bucket,
            "attesting_sources": "; ".join(source_keys),
        })
    return attestation, temporal


def build_attestation_bucket_manifest(attestation: list[dict], schema: dict) -> list[dict]:
    counts = Counter(row.get("bucket", "") for row in attestation)
    rows = []
    for bucket in schema["controlled_vocabularies"]["attestation_bucket"]:
        rows.append({
            "bucket": bucket,
            "row_count": counts.get(bucket, 0),
            "present_in_phase3": "yes" if counts.get(bucket, 0) else "no",
            "note": "Controlled bucket emitted by schema. Zero means this run had no rows in that class.",
        })
    return rows


def build_temporal_residue(temporal: list[dict], attestation: list[dict]) -> list[dict]:
    att_by_key = {
        (row.get("day_title", ""), row.get("service_hour", ""), row.get("identity_key", "")): row
        for row in attestation
    }
    rows = []
    for row in temporal:
        if row.get("lifecycle_status") == "current":
            continue
        key = (row.get("day_title", ""), row.get("service_hour", ""), row.get("identity_key", ""))
        att = att_by_key.get(key, {})
        statuses = row.get("current_status", "")
        bucket = row.get("attestation_bucket", "")
        if "pending_psalm_equivalence_unresolved" in statuses:
            residue_type = "psalm_equivalence_unresolved"
            reason = "Psalm candidate has not been promoted because the exact Brenton/KJV verse-boundary equivalence is not encoded."
        elif bucket == "old_edition_only_candidate_removed":
            residue_type = "candidate_removed_needs_current_authority_confirmation"
            reason = "Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture."
        elif bucket == "old_edition_only":
            residue_type = "historical_witness_no_current_comparator"
            reason = "Historical printed witness has no captured current Coptic Reader comparator in this run."
        elif bucket == "single_source_candidate":
            residue_type = "current_authority_pending"
            reason = "Single current/reference source candidate has no scoped current authority confirmation and is not confirmed by two independent sources."
        else:
            residue_type = "temporal_residue"
            reason = "Non-current temporal classification requires review before stronger publication wording."
        rows.append({
            "day_title": row.get("day_title", ""),
            "service_hour": row.get("service_hour", ""),
            "identity_key": row.get("identity_key", ""),
            "display_ref": row.get("display_ref", ""),
            "lifecycle_status": row.get("lifecycle_status", ""),
            "attestation_bucket": bucket,
            "current_status": statuses,
            "removed_marker": row.get("removed_marker", ""),
            "current_authority": row.get("current_authority", ""),
            "residue_type": residue_type,
            "reason": reason,
            "citation": att.get("citation", ""),
            "attestation_note": att.get("attestation_note", ""),
        })
    return rows


def build_temporal_residue_manifest(temporal_residue: list[dict]) -> list[dict]:
    counts = Counter(row.get("residue_type", "") for row in temporal_residue)
    rows = []
    for residue_type in [
        "current_authority_pending",
        "historical_witness_no_current_comparator",
        "candidate_removed_needs_current_authority_confirmation",
        "psalm_equivalence_unresolved",
        "true_source_disagreement",
    ]:
        rows.append({
            "residue_type": residue_type,
            "row_count": counts.get(residue_type, 0),
            "present_in_phase4": "yes" if counts.get(residue_type, 0) else "no",
            "note": "True source disagreements are zero in this run; unresolved rows are classified separately by evidence class." if residue_type == "true_source_disagreement" else "Temporal residue evidence class emitted for Phase 4 review.",
        })
    return rows


def parse_month_day(row: dict) -> tuple[str, int, str]:
    month_title = row.get("month_title", "")
    raw_month = re.sub(r"^\d+\s*-\s*", "", month_title).strip()
    month = MONTH_MAP.get(raw_month.lower(), raw_month)
    title = row.get("day_title", "")
    m = re.search(r"(\d+)\s+([A-Za-z-]+)", title)
    if m:
        day = int(m.group(1))
    else:
        url_name = row.get("day_url", "")
        m2 = re.search(r"Calendar_(\d{2})-", url_name)
        day = int(m2.group(1)) if m2 else 0
    coptic_key = f"{month} {day}" if day else month
    return month, day, coptic_key


def infer_synaxarium_title(raw_title: str) -> tuple[str, str]:
    title = norm_space(raw_title).strip().rstrip(" .")
    if re.search(r"marks\s+the\s+commemoration\s+of\s+(?:the\s+)?(?:honorable\s+)?archangel\s+gabriel", title, re.I) and re.search(r"church\s+in\s+caesari[ae]", title, re.I):
        return "The Commemoration of Archangel Gabriel and the Consecration of His Church in Caesaria", "Title shortened from a long numbered source entry; full source summary is preserved."
    if len(title) <= 180 and not re.match(r"^(On this day|Today also|On this day also)", title, re.I):
        return title, ""
    opener = r"(?:On this day(?: also)?|Today also|Also on this day)"
    martyr = re.search(rf"^{opener},?\s+(.*?)(?:,?\s+(?:was|were)\s+martyred\b|\s+received\s+the\s+crown\s+of\s+martyrdom\b)", title, re.I)
    if martyr:
        subject = martyr.group(1).strip(" ,.;")
        return f"The Martyrdom of {subject}", "Title inferred from prose martyrdom lead; check publication wording against the source page."
    departed = re.search(rf"^{opener},?\s+(.*?)(?:,?\s+departed\b|\s+departed\b)", title, re.I)
    if departed:
        subject = departed.group(1).strip(" ,.;")
        return f"The Departure of {subject}", "Title inferred from prose departure lead; check publication wording against the source page."
    commem = re.search(r"(?:celebrates?|is)\s+(?:the\s+)?commemoration\s+of\s+(.*?)(?:,|\.|\sand\s|$)", title, re.I)
    if commem:
        subject = commem.group(1).strip(" ,.;")
        return f"The Commemoration of {subject}", "Title inferred from prose commemoration lead; check publication wording against the source page."
    first_sentence = re.split(r"(?<=[.!?])\s+", title, maxsplit=1)[0].strip()
    if len(first_sentence) < len(title):
        return first_sentence.rstrip(" ."), "Long source prose title was shortened to the first sentence; check publication wording against the source page."
    return title, "Long source prose title could not be shortened safely."


def classify_commem(title: str) -> str:
    t = title.lower()
    if "lord" in t or "nativity" in t or "theophany" in t or "resurrection" in t or "cross" in t:
        return "lord_feast"
    if "martyr" in t or "martyrdom" in t:
        return "martyr"
    if "theotokos" in t or "virgin mary" in t or "st. mary" in t or "saint mary" in t or "holy virgin mary" in t:
        return "theotokos"
    if "apostle" in t:
        return "apostle"
    if "pope" in t or "patriarch" in t:
        return "patriarch"
    if "bishop" in t or "metropolitan" in t:
        return "hierarch"
    if "departure" in t:
        return "departure"
    if "prophet" in t:
        return "prophet"
    if "angel" in t or "michael" in t or "gabriel" in t:
        return "angel"
    if "monk" in t or "ascetic" in t or "anchorite" in t:
        return "ascetic"
    if "feast" in t:
        return "feast"
    return "commemoration"


def build_synaxarium() -> tuple[list[dict], list[dict]]:
    syn_rows = read_csv(SYNAX)
    commems = []
    for row in syn_rows:
        month, day, coptic_key = parse_month_day(row)
        pieces = [norm_space(p) for p in row.get("summary_lines", "").split(" | ") if norm_space(p)]
        titles = []
        title_caveats = {}
        seen_titles = set()
        extraction_method = "numbered_summary_entry"
        caveat = ""
        for piece in pieces:
            if re.match(r"^\d+\.\s+", piece):
                if titles and re.match(r"^\d+\.\s+(?:On this day|Today|On this)", piece, re.I):
                    break
                title_candidate = re.sub(r"^\d+\.\s+", "", piece).strip()
                title_candidate = re.split(r"\s+\d+\s*\.\s+(?:On this day|Today|On this)", title_candidate, maxsplit=1)[0].strip()
                title_candidate = title_candidate.rstrip(" .")
                title_candidate, inferred_caveat = infer_synaxarium_title(title_candidate)
                key = norm_space(title_candidate).lower()
                if title_candidate and key not in seen_titles:
                    titles.append(title_candidate)
                    seen_titles.add(key)
                    if inferred_caveat:
                        title_caveats[key] = inferred_caveat
            elif titles:
                break
        if not titles and pieces:
            inferred_title, inferred_caveat = infer_synaxarium_title(pieces[0])
            titles = [inferred_title]
            if inferred_caveat:
                title_caveats[norm_space(inferred_title).lower()] = inferred_caveat
            extraction_method = "prose_lead_inferred"
            caveat = "Source page did not expose a numbered list in the indexed summary. Title inferred from the first summary lead and should be checked against the source page for publication wording."
        if not titles:
            title = row.get("day_title", "") or coptic_key
            titles = [title]
            extraction_method = "day_title_fallback"
            caveat = "No numbered summary entry or prose lead was available in the indexed source row. Day title used as fallback."
        for idx, title in enumerate(titles, 1):
            row_caveat = caveat
            inferred_title_caveat = title_caveats.get(norm_space(title).lower(), "")
            if inferred_title_caveat:
                row_caveat = (row_caveat + " " if row_caveat else "") + inferred_title_caveat
            ctype = classify_commem(title)
            if ctype == "commemoration" and extraction_method != "day_title_fallback":
                row_caveat = (row_caveat + " " if row_caveat else "") + "Generic commemoration type used because title did not match a safer person, feast, or office rule."
            commem_id = f"{slugify(month)}-{day:02d}-{idx:02d}"
            commems.append({
                "commem_id": commem_id,
                "coptic_month": month,
                "coptic_day": day,
                "coptic_day_key": coptic_key,
                "rank": idx,
                "title": title,
                "type": ctype,
                "extraction_method": extraction_method,
                "caveat": row_caveat.strip(),
                "source": "St-Takla English Synaxarium",
                "source_url": row.get("day_url", ""),
                "source_day_title": row.get("day_title", ""),
                "source_summary": row.get("summary_lines", ""),
            })
    reverse_rows = read_csv(DATA / "reverse_lookup_crosswalk.csv")
    fixed_day_rows = defaultdict(list)
    for row in reverse_rows:
        if row.get("source_kind") != "katameros_cycle":
            continue
        key = norm_space(row.get("coptic_date", ""))
        if key:
            fixed_day_rows[key].append(row)
    bridge = []
    foundational_by_day = foundational_69_by_day_key()
    by_day = defaultdict(list)
    for c in commems:
        by_day[c["coptic_day_key"]].append(c)
    for day_key, day_commems in by_day.items():
        readings = fixed_day_rows.get(day_key, [])
        if not readings:
            alt_key = day_key.replace("Tut", "Tout").replace("Tubah", "Toba")
            readings = fixed_day_rows.get(alt_key, [])
        primary = sorted(day_commems, key=lambda c: int(c["rank"]))[0]
        foundational_row = foundational_by_day.get(day_key)
        if foundational_row:
            confidence = "high"
            basis = "explicit"
            base_citation = (
                f"Ottawa/UKMID Katameros of the Days, {foundational_row.get('source_edition')}, "
                f"{foundational_row.get('source_locator')}; F.N. Youssef on the 69 foundational readings; "
                "St-Takla day index; local Katameros fixed-day row."
            )
            bridge_note = "Explicit bridge because this Coptic day is enumerated in the Ottawa/UKMID 69 foundational-reading collection. This catalogs source-row or variant catalog entries; it is not a resolved daily service schedule and not direct proper-reading proof for the named commemoration."
        else:
            confidence = "medium"
            basis = "collection-type"
            base_citation = "F.N. Youssef on daily readings following the Synaxarium; St-Takla day index; local Katameros fixed-day row."
            bridge_note = "Collection-type bridge from fixed-day Synaxarium context to Katameros rows. This catalogs source-row or variant catalog entries; it is not a resolved daily service schedule and not direct proper-reading proof for the named commemoration."
        if len(day_commems) > 1:
            bridge_note += " Primary commemoration linked only; secondary commemorations require explicit proper-reading source before separate links are created."
        else:
            bridge_note += " Single commemoration day alignment."
        for row in readings:
            ident = identity_for(row.get("passage") or row.get("normalized_segment") or "")
            local_locator = f"source_file={row.get('source_file', '')} | source_row_id={row.get('source_row_id', '')} | source_ref={row.get('source_ref', '') or row.get('raw_ref', '')}"
            bridge.append({
                "commem_id": primary["commem_id"],
                "coptic_day_key": day_key,
                "commemoration_title": primary["title"],
                "commemoration_type": primary["type"],
                "reading_identity_key": ident["identity_key"],
                "display_ref": ident["display_ref"],
                "slot": row.get("reading_slot") or row.get("reading_type") or row.get("service_section") or "",
                "basis": basis,
                "confidence": confidence,
                "citation": base_citation + " " + local_locator,
                "note": bridge_note,
            })
    return commems, bridge


def build_today_rows(presentation_rows: list[dict]) -> list[dict]:
    today = dt.date.today().isoformat()
    rows = [r for r in presentation_rows if r.get("gregorian_date") == today]
    if rows:
        return rows
    # If the host date differs from the project date window or cache behavior, keep a stable example.
    fallback = "2026-06-16"
    return [r for r in presentation_rows if r.get("gregorian_date") == fallback]


def build_footprint(presentation_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in presentation_rows:
        if row.get("reading_type") == "named-reading":
            continue
        grouped[row["identity_key"]].append(row)
    rows = []
    for identity_key, items in sorted(grouped.items(), key=lambda kv: (kv[1][0].get("canonical_mt_ref", ""), kv[0])):
        first = items[0]
        statuses = Counter(i.get("current_status", "") for i in items)
        source_kinds = sorted(set(i.get("source_kind", "") for i in items))
        places = []
        for item in items[:12]:
            place = " | ".join(x for x in [item.get("day_title"), item.get("service_hour") or item.get("service_section"), item.get("slot")] if x)
            if place and place not in places:
                places.append(place)
        parsed = parse_passage(first.get("canonical_mt_ref") or "")
        slug = ""
        if parsed and parsed.parts:
            slug = f"{slugify(parsed.book_abbrev)}-{parsed.parts[0].chapter_start}"
        rows.append({
            "identity_key": identity_key,
            "display_ref": first.get("display_ref", ""),
            "canonical_mt_ref": first.get("canonical_mt_ref", ""),
            "canonical_lxx_ref": first.get("canonical_lxx_ref", ""),
            "total_occurrences": len(items),
            "current_occurrences": sum(v for k, v in statuses.items() if k.startswith("current")),
            "historical_occurrences": sum(v for k, v in statuses.items() if "historical" in k),
            "source_kinds": "; ".join(source_kinds),
            "sample_liturgical_places": " || ".join(places),
            "hour_themes": "; ".join(sorted(set(i.get("hour_theme", "") for i in items if i.get("hour_theme"))))[:500],
            "patristic_homily_slug": "",
            "chapter_study_slug": slug,
            "audio_slug": slug,
            "site_note": "Patristic homily linkage is not present in this repo and must be joined from the site corpus when George pushes.",
        })
    return rows



def build_passage_source_disclosure(presentation_rows: list[dict]) -> list[dict]:
    rows = []
    for row in presentation_rows:
        rows.append({
            "identity_key": row.get("identity_key", ""),
            "display_ref": row.get("display_ref", ""),
            "canonical_mt_ref": row.get("canonical_mt_ref", ""),
            "canonical_lxx_ref": row.get("canonical_lxx_ref", ""),
            "source_key": row.get("source_key", ""),
            "source_title": row.get("source_title", ""),
            "source_edition": row.get("source_edition", ""),
            "source_locator": row.get("source_locator", ""),
            "source_url": row.get("source_url", ""),
            "source_ref": row.get("source_ref", "") or row.get("raw_ref", ""),
            "occasion": row.get("occasion", ""),
            "calendar_key": row.get("calendar_key", ""),
            "day_title": row.get("day_title", ""),
            "service_hour": row.get("service_hour", ""),
            "slot": row.get("slot", ""),
            "current_status": row.get("current_status", ""),
            "removed_marker": row.get("removed_marker", ""),
            "citation": row_citation(row),
        })
    return rows


def write_schema() -> dict:
    foundational_69 = build_foundational_reading_collections_69()
    schema = {
        "version": "2026-06-16-design-layer-v1",
        "principles": [
            "MT or modern English display is primary for user input and site search.",
            "Psalm and LXX variants carry canonical fields so source labels do not control identity.",
            "Temporal status is derived from source attestation, not hand deletion.",
            "Synaxarium links store their basis and confidence because the Synaxarium text does not explicitly map readings to each commemoration.",
        ],
        "controlled_vocabularies": {
            "season": ["Annual", "Kiahk", "Great Lent", "Jonah Fast", "Holy Week", "Holy Pascha", "Bright Saturday", "Holy Fifty Days", "Apostles Fast", "St. Mary Fast", "Nativity Fast", "Fixed feast", "Special service", "Agpeya"],
            "occasion": ["annual_fixed_day", "annual_sunday", "great_lent_weekday", "great_lent_sunday", "jonah_fast", "holy_week_hour", "pascha_hour", "bright_saturday", "holy_fifty", "lord_feast", "theotokos_feast", "saint_commemoration", "martyr_commemoration", "patriarch_commemoration", "special_service", "agpeya_hour"],
            "occasion_type": {"alias_for": "occasion", "reason": "Use occasion in emitted rows; occasion_type is retained as the conceptual vocabulary name."},
            "source_authority_tier": ["current_authority", "public_current_practice_reference", "working_local_source", "historical_printed_witness", "scholarly_structural", "synaxarium_text_source", "unclassified"],
            "source_convention": ["modern_english_reference", "mt_nkjv", "lxx_liturgical_or_fixture_label"],
            "canonicalization_confidence": ["high", "medium", "low", "n/a"],
            "current_status": ["current_confirmed_coptic_reader", "current_confirmed_by_fixture_equivalence", "pending_psalm_equivalence_unresolved", "historical_candidate_removed", "historical_witness", "current_working_source_not_coptic_reader_checked", "current_public_or_local_reference", "unknown"],
            "attestation_bucket": ["current_confirmed", "consensus_without_coptic_reader", "old_edition_only", "old_edition_only_candidate_removed", "single_source_candidate"],
            "service": SERVICE_ENUM,
            "service_day": ["fixed_coptic_day", "ordinary_sunday", "holy_week_day", "pascha_eve", "pascha_day", "special_service", "agpeya_hour", "source_label_preserved"],
            "service_hour": ["Vespers", "Matins", "Liturgy", "First Hour", "Third Hour", "Sixth Hour", "Ninth Hour", "Eleventh Hour", "Twelfth Hour", "Midnight Praises", "source_label_preserved"],
            "service_section": ["Vespers", "Matins", "Liturgy", "Midnight Praises", "Prophecies", "Pascha Hour", "Agpeya", "Special Service", "source_label_preserved"],
            "hour": ["First Hour", "Third Hour", "Sixth Hour", "Ninth Hour", "Eleventh Hour", "Twelfth Hour"],
            "slot": ["prophecy-1", "prophecy-2", "prophecy-3", "prophecy-4", "prophecy-5", "psalm", "gospel", "pauline", "catholic", "praxis", "synaxarium", "homily", "exposition", "hymn", "litany", "source_label_preserved"],
            "synaxarium_type": ["lord_feast", "theotokos", "martyr", "apostle", "patriarch", "hierarch", "departure", "prophet", "angel", "ascetic", "feast", "commemoration"],
            "bridge_basis": ["explicit", "collection-type", "inferred"],
            "bridge_confidence": ["high", "medium", "low"],
            "psalm_mapping_scope": ["chapter_equivalence", "split_merge_chapter_seam", "lxx_unique_chapter", "anchored_verse_example", "unresolved_verse_offset_example"],
            "current_authority": ["Coptic Reader fixture where captured", "public date-resolved source is reference only", "historical source is witness only", "scholarly source governs structure, not current readings", "no scoped current authority confirmation"],
            "collection_types_69": {
                "status": FOUNDATIONAL_69_SOURCE_PROVENANCE["membership_status"],
                "verdict_token": FOUNDATIONAL_69_SOURCE_PROVENANCE["verdict_token"],
                "confirmed_count": 69,
                "membership_confirmation": "confirmed_same_set_inferred_from_source_combination_not_count_only",
                "membership_basis": FOUNDATIONAL_69_SOURCE_PROVENANCE["membership_basis"],
                "provenance": FOUNDATIONAL_69_SOURCE_PROVENANCE,
                "entries": foundational_69,
            },
        },
        "tables": {
            "reading_identity": ["identity_key", "reading_type", "reading_name", "source_label", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_convention", "canonicalization_confidence", "canonicalization_note", "spans_json"],
            "reverse_lectionary_presentation": ["identity_key", "reading_type", "reading_name", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_convention", "canonicalization_confidence", "canonicalization_note", "spans_json", "current_status", "status_note", "removed_marker", "source_key", "source_title", "source_edition", "source_locator", "source_url", "source_kind", "source_family", "source_file", "source_row_id", "authority_tier", "occasion", "calendar_key", "gregorian_date", "coptic_date", "day_title", "service_day", "service_hour", "service_section", "reading_slot", "slot", "order", "hour_theme", "source_ref", "raw_ref", "url", "provenance"],
            "todays_readings_current_practice": ["identity_key", "reading_type", "reading_name", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_convention", "canonicalization_confidence", "canonicalization_note", "spans_json", "current_status", "status_note", "removed_marker", "source_key", "source_title", "source_edition", "source_locator", "source_url", "source_kind", "source_family", "source_file", "source_row_id", "authority_tier", "occasion", "calendar_key", "gregorian_date", "coptic_date", "day_title", "service_day", "service_hour", "service_section", "reading_slot", "slot", "order", "hour_theme", "source_ref", "raw_ref", "url", "provenance"],
            "pascha_attestation": ["day_title", "service_hour", "identity_key", "display_ref", "source_count", "sources", "source_titles", "source_editions", "source_locators", "bucket", "statuses", "removed_marker", "citation", "attestation_note"],
            "temporal_classification": ["day_title", "service_hour", "identity_key", "display_ref", "lifecycle_status", "current_status", "removed_marker", "source_authority_tier", "source_titles", "source_editions", "source_locators", "attestation_bucket", "current_authority", "valid_from", "valid_to", "derivation", "attesting_sources"],
            "temporal_residue": ["day_title", "service_hour", "identity_key", "display_ref", "lifecycle_status", "attestation_bucket", "current_status", "removed_marker", "current_authority", "residue_type", "reason", "citation", "attestation_note"],
            "temporal_residue_manifest": ["residue_type", "row_count", "present_in_phase4", "note"],
            "psalm_mt_lxx_crosswalk": ["mt_psalm", "lxx_psalm", "map_direction", "mapping_scope", "confidence", "validation_basis", "note"],
            "pascha_attestation_bucket_manifest": ["bucket", "row_count", "present_in_phase3", "note"],
            "synaxarium_commemoration": ["commem_id", "coptic_month", "coptic_day", "coptic_day_key", "rank", "title", "type", "extraction_method", "caveat", "source", "source_url", "source_day_title", "source_summary"],
            "synaxarium_reading_bridge": ["commem_id", "coptic_day_key", "commemoration_title", "commemoration_type", "reading_identity_key", "display_ref", "slot", "basis", "confidence", "citation", "note"],
            "passage_liturgical_footprint": ["identity_key", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "total_occurrences", "current_occurrences", "historical_occurrences", "source_kinds", "sample_liturgical_places", "hour_themes", "patristic_homily_slug", "chapter_study_slug", "audio_slug", "site_note"],
            "source_registry": ["source_key", "title", "edition", "url", "default_locator", "authority_tier", "confidence", "notes"],
            "passage_source_disclosure": ["identity_key", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_key", "source_title", "source_edition", "source_locator", "source_url", "source_ref", "occasion", "calendar_key", "day_title", "service_hour", "slot", "current_status", "removed_marker", "citation"],
            "foundational_reading_collection": ["collection_key", "sequence", "coptic_month", "coptic_day", "coptic_day_key", "calendar_key", "toc_label", "reading_section_start_page", "source_key", "source_title", "source_edition", "source_url", "source_locator", "membership_status", "membership_verdict", "membership_basis", "verification_status"],
            "liturgical_placement": ["identity_key", "occasion", "calendar_key", "day_title", "service_day", "service_hour", "service_section", "slot", "order", "removed_marker", "source_title", "source_edition", "source_locator", "source_url"],
            "temporal_attestation": ["identity_key", "source_key", "source_title", "source_edition", "source_locator", "source_authority_tier", "current_status", "attestation_bucket", "current_authority", "valid_from", "valid_to", "removed_marker"],
        },
    }
    (OUT / "lectionary_schema.json").write_text(json.dumps(schema, indent=2, ensure_ascii=False), encoding="utf-8")
    return schema


def write_article() -> None:
    article = """---
title: "The Coptic Lectionary and the Synaxarium"
slug: coptic-lectionary-and-synaxarium
publish: true
type: lesson
summary: "A Coptic Orthodox lesson on how the Church's lectionary and Synaxarium teach us to receive Scripture inside worship, memory, repentance, and the life of the saints."
tags: [coptic-orthodox, lectionary, synaxarium, scripture, liturgy]
fathers: [Athanasius of Alexandria]
passages: ["Luke 4:16-21", "Acts 15:21", "2 Timothy 3:16-17"]
season: "Liturgical year"
---

The Coptic lectionary is not only a reading plan. It is the Church teaching her children how to hear the Lord. In the Church's worship, appointed readings are received in relation to feasts, fasts, hours, commemorations, and liturgical services, according to the sources and rites in view.

## The burden of the lesson

A Christian can read the Bible alone and still miss the mind of the Church. The lectionary trains us to hear Scripture with the Church, at the right hour, in the right season, before the altar, with the saints standing around us as witnesses.

When the deacon announces the reading, he is not filling a slot in a service. He serves the Lord by proclaiming the word entrusted to the Church. The people are not an audience. They are the Body of Christ receiving the voice of the Shepherd.

## Christ opens the book

In Luke 4, the Lord Jesus enters the synagogue, receives the book of Isaiah, reads, and declares, "Today this Scripture is fulfilled in your hearing." The pattern matters. Scripture is read in worship, and Christ Himself is the fulfillment.

Theologically, this helps explain the heart of the Coptic lectionary. The sources show more than a topical reading plan. They show Scripture received through the Church's feasts, fasts, hours, and commemorations, where Christ is confessed as the fulfillment of the Law, the Prophets, the Psalms, and the Gospel.

Saint Athanasius, in his Thirty-Ninth Festal Letter, calls the divine Scriptures "fountains of salvation." He is speaking about the Church receiving the canon, but the image also helps us understand the lectionary. The Church keeps bringing her children back to the fountains, not randomly, but with pastoral order.

## What the lectionary is

The Coptic Encyclopedia describes the lectionary as a set of four books used for the readings of the Coptic Church: the Annual Katameros, the Great Lent Katameros, the Pascha Katameros, and the Pentecost Katameros. This four-book description concerns the core Katameros lectionary books, not every liturgical, sacramental, Agpeya, Synaxarium, or rite-specific source that may contain readings or commemorative material. Source: Coptic Encyclopedia, "Lectionary."

A printed Katameros source gives the primary liturgical-book view from inside the tradition. The Ottawa Katameros of the Days says the Coptic and Arabic Katameros was published in five volumes: Volume I for Sundays and Feasts, Volume II for Week Days, Volume III for Great Lent, Volume IV for Holy Week of Pascha, and Volume V for the Fifty Days from Easter to Pentecost. It also says the Katameros of the Days contains Volume II and the church feasts. Source: St. Mary Ottawa, Katameros of the Days, Introduction.

These two descriptions should be read together. The scholarly four-book frame names the main lectionary families. The printed volume frame shows how the annual material is split for use, especially the Sunday and weekday materials of the Yearly Katameros. Source: Coptic Encyclopedia, "Lectionary"; St. Mary Ottawa, Katameros of the Days.

The word Katameros means "according to the parts" or "in parts." This is exactly what the book does. It gives the appointed parts of Scripture to be read at each service, feast, fast, and commemoration. Source: Coptic Encyclopedia, "Lectionary."

## How the lectionary has been documented

The documentation comes in layers. Read from source: the Ottawa Katameros books are printed English lectionary witnesses from St. Mary Coptic Orthodox Church, Ottawa, and St. George and St. Antony Coptic Orthodox Church, Ottawa. The Days volume identifies itself as Readings for Week Days and Feasts, first edition, Christmas 1714 A.M., 1998 A.D.; the Sundays volume identifies itself as Readings for Sundays and Feasts, including Sundays of Great Lent and Pentecost, second edition, Lent 1720 A.M., 2004 A.D.; the Pentecost volume identifies itself as Nativity Fast 1718 A.M., 2001 A.D.; and the Pascha eBook identifies itself as Lent 1734 A.M., 2018 A.D. Source: St. Mary Ottawa / UKMID PDF front matter for Katameros of the Days, Sundays, Pentecost, and Holy Pascha.

Read from source: the UKMID site hosts the same practical PDF family for Days, Sundays, Lent, and Pentecost, and St. Bishoy Deacons' Corner publicly organizes Katameros readings and Synaxarium materials for Annual Days, Sundays, Kiahk, Amshir, Lent, Passion Week, Pascha, and the Joyous Fifty Days. These are useful public documentation layers, but they are not by themselves the final current-practice authority when a scoped Coptic Reader fixture disagrees. Source: UKMID `Katameros_Days.pdf`, `Katameros_Sundays.pdf`, `Katameros_Lent.pdf`, and `Katameros_Pentecost.pdf`; St. Bishoy Deacons' Corner, `Katameros Readings and Synaxarium for all Seasons, Annual Days, Sundays, Kiahk and Amshir`.

Read from source: the scholarly layer explains structure and history rather than replacing the service books. The Coptic Encyclopedia `Lectionary` entry names the lectionary books and gives historical framing; its CCDL metadata lists Basilios, Archbishop, and Coquin, René-Georges as creators. Youssef explains the calendar logic and the relation of daily readings to the Synaxarium. Zanetti and Coquin are scholarly anchors for the annual lectionary tradition in the source bibliography. Sources: Coptic Encyclopedia, `Lectionary`; F.N. Youssef, `The Arrangement of the Church Lectionary`; Ugo Zanetti, Les lectionnaires coptes annuels, Basse-Egypte; René-Georges Coquin liturgical scholarship.

Read from source: Burmester's Scetis Holy Week lectionary is a historical witness to an older and fuller Holy Week layer. Inference from the design residue: it helps explain why some Pascha readings are retained as historical attestations when they appear in older/local Pascha data but are absent from the scoped Coptic Reader Wednesday Day fixture. Source: O.H.E. Burmester, `The Coptic-Greek-Arabic Holy Week Lectionary from Scetis`; St. Mary Ottawa Holy Pascha extracted text; Coptic Reader Pascha Wednesday Day fixture.

Read from source: Coptic Reader governs current practice where it has been captured in this project. The current captured scope is the Pascha Wednesday Day fixture supplied by George; outside that fixture, Coptic Reader coverage is not yet broad enough to classify every older or public row as current or removed. Source: Coptic Reader app Pascha Wednesday Day fixture supplied by George; source registry entry `coptic_reader_fixture_wednesday_day`.

Read from source: the design layer also separates Bible text anchors from liturgical placement sources. Brenton is used as the Septuagint comparison anchor for Psalm and Old Testament seam checks, while WEB and KJV are public-domain or public-domain-in-the-USA English anchors for future text comparison and display policy. The article itself does not reproduce Scripture text; it keeps Scripture references on NKJV versification. Sources: `out/design/psalm_mt_lxx_crosswalk.csv`; eBible World English Bible copyright information; Wikisource King James Bible copyright note.

## The year has a spiritual grammar

F.N. Youssef explains that the arrangement of Coptic Church readings depends on two calendars: the Coptic calendar and the Hebrew calendar. The Coptic calendar supplies the fixed structure of the year, while the Feast of the Resurrection follows the Hebrew calendar according to the Nicene Paschal rule. Here, "follows the Hebrew calendar" means the Church's Paschal computation, the Nicene norm of the Sunday following the first vernal full moon as later calculated through the Alexandrian mode, not a lookup of the present-day Hebrew calendar. The Coptic Church does not look up this date in the modern Jewish calendar. It computes the Paschal full moon by the Alexandrian reckoning set at Nicaea, the same nineteen-year cycle the Eastern Orthodox churches use, so the Coptic Pascha falls on the same Sunday as the Eastern Orthodox Pascha. In 2026, for example, the Coptic and the Russian Orthodox Pascha both fall on 12 April. Sources: F.N. Youssef, "The Arrangement of the Church Lectionary"; World Council of Churches and Middle East Council of Churches, "Towards a Common Date for Easter," Aleppo, 1997; Fr. Andrew Stephen Damick, "No, the Paschal date difference is not about Passover (and other Orthodox urban legends)," Ancient Faith Ministries, 2022; Greek Orthodox Archdiocese of America, "Some Common Misperceptions about the Date of Pascha/Easter"; timeanddate public Easter-date references for Coptic Orthodox Easter and Russian Orthodox Easter in 2026; OrthodoxWiki, "Coptic Calendar"; copticchurch.net calendar notes.

Youssef also names the Paschal calculation used to determine the Resurrection date. In the traditional attribution he reports, the Abuqti calculation was developed by the Egyptian astronomer Ptolemy al-Farmawi in the time of Pope Demetrius the Vinedresser, and became known as hisab al-karma, "the calculation of the vine." Source: F.N. Youssef, "The Arrangement of the Church Lectionary."

Youssef reads the Coptic agricultural year as a theological pattern. The first season is sowing, and the readings present the love of the Father and the mystery of the Incarnation. The second season is harvest, and the readings present the grace of the Son and the mystery of Redemption. The third season is flooding, and the readings present the gift and fellowship of the Holy Spirit and the mystery of the Church. Source: F.N. Youssef, "The Arrangement of the Church Lectionary."

The middle season is movable. Youssef says this harvest season follows the Hebrew calendar rather than the fixed Coptic calendar, because it is tied to Passover and the Resurrection. It runs from the Saturday before Great Lent to the feast of the Descent of the Holy Spirit, a span he gives as 15 weeks or 107 days. This article reports Youssef's figure as given; 15 weeks is 105 days. Source: F.N. Youssef, "The Arrangement of the Church Lectionary."

This is why the lectionary is not flat. A fixed weekday, a Sunday in the Annual cycle, a day of Great Lent, the Sixth Hour of Good Friday, and a day in the Holy Fifty do not function the same way. Each has its own source-governed logic.

## Sundays, feasts, and the Synaxarium

The Sunday readings are a distinct program. Youssef states that when a Coptic day falls on a Sunday, the rites and readings follow the Sunday program rather than the weekday program. The Church provides readings for four Sundays each month, and the readings of every two consecutive months form an eight-Sunday spiritual and theological program. Source: F.N. Youssef, "The Arrangement of the Church Lectionary."

Youssef gives a special rule for fifth Sundays. If the fifth Sunday falls on the 29th of the month, the readings commemorate the Annunciation, Nativity, and Resurrection. If it falls on the 30th, the readings present the feeding of the multitude and the mystery of the Church gathered around Christ. Source: F.N. Youssef, "The Arrangement of the Church Lectionary."

The Coptic Encyclopedia also describes the Sunday Gospel readings as methodically arranged, with the four Sundays of each Coptic month combining to present a theme. This supports treating Sundays as their own program rather than as ordinary weekdays with Sunday labels attached. Source: Coptic Encyclopedia, "Lectionary."

Feasts also have a governed place in the reading year. Youssef says the yearly program is fed not only by Sunday readings, but also by the readings for the seven Major Feasts of the Lord, the seven Minor Feasts of the Lord, and the two Feasts of the Cross. The Ottawa Katameros of the Days gives the primary printed rule that when a major or minor Lord's Feast falls on a Sunday, the feast lessons are read instead of the regular Sunday lessons, with related rules for the Cross Feast, Nayrouz, and the 29th of the month when it is a fifth Sunday. Sources: F.N. Youssef, "The Arrangement of the Church Lectionary"; St. Mary Ottawa, Katameros of the Days, General Remarks.

For ordinary weekdays, Youssef's principle is essential: the daily readings follow the Synaxarium. The theme of each day's readings turns around the occasions commemorated in the Synaxarium, including feasts of the Lord, the Theotokos, angels, martyrs, apostles, patriarchs, ascetics, hermits, and other saints. Source: F.N. Youssef, "The Arrangement of the Church Lectionary."

Youssef says the Church arranged 69 foundational readings, al-qira'at al-asasiyya, to cover these commemoration themes throughout the Coptic year, and that they are collected in the second volume of the Yearly Katameros. The Ottawa/UKMID Katameros of the Days presents that same practical second-volume collection in English: its table of contents lists 69 dated reading sections, and its annual day table maps daily commemorations to those sections. This identification is established as an inference from source identity, volume placement, function, and count; the consulted Youssef page gives the concept and count, not the date-by-date roster. Sources: F.N. Youssef, "The Arrangement of the Church Lectionary"; St. Mary Ottawa, Katameros of the Days.

## Why the reverse lectionary matters

Most lectionaries answer one question: what is read today?

A reverse lectionary answers another question: where does the Church read this passage?

That second question is powerful for Bible study. If Isaiah 53 is read in Holy Week, the placement tells us how the Church hears the suffering Servant. If John 2 appears in a wedding or feast context, the placement becomes interpretation. If a Psalm appears in an Agpeya hour and in Pascha, the repeated use teaches us how the Church prays the Psalm.

The reverse lectionary does not replace exegesis. It gives exegesis a liturgical witness.

## Numbering must be honest

Modern English Bibles often follow Masoretic Psalm numbering. Coptic liturgical tradition often follows the Septuagint numbering. The same Psalm may therefore appear under two numbers. For example, what many English Bibles call Psalm 51 may appear liturgically as Psalm 50.

The solution is not to erase one tradition. The solution is to store both responsibly:

- a display reference that English readers can search,
- a Septuagint reference where it differs,
- a stable identity key so that the same reading is recognized across sources,
- and a source note saying whether the source used English, Septuagint, or mixed labels.

This honesty prevents false contradictions. It also protects the Church's liturgical numbering.

## The Synaxarium bridge must be humble

The Synaxarium gives the commemorations of the day. It does not always say, "this reading belongs to this saint." The link between commemoration and reading must therefore be stored with a basis and a caution.

In this design layer, the Synaxarium bridge is deliberately humble. Rows whose Coptic day is enumerated in the Ottawa/UKMID 69 foundational-reading collection are marked `explicit` and `high` for the source-row bridge. Outside those 69 days, bridge rows remain `collection-type` and `medium`. The bridge is useful for discovery, but it is not direct proof that every reading is a proper reading for the named commemoration.

This matters because some days have multiple commemorations. A martyr, a patriarch, and a feast may share the same day. Secondary commemorations may have proper readings only in sources not ingested here. A faithful database should show the link and also show the limit of the evidence.

A faithful database should say what it knows and how it knows it.

## Spiritual fruit

The lectionary teaches obedience. We receive what the Church gives, even when another passage might feel more immediately interesting.

It teaches memory. The saints are not examples from the past only. They are part of the Church's living worship.

It teaches repentance. The same passage returns in different seasons and exposes a different wound in us.

It teaches Christ. Every reading, feast, fast, Psalm, prophecy, Gospel, and commemoration finds its center in Him.

## Teaching guide

### Opening question
Ask: When you hear a church reading, do you receive it as information, or as the Church interpreting this day for you?

### Main movement
1. Begin with Christ reading Isaiah in Luke 4.
2. Explain the core lectionary books and the printed Yearly Katameros volumes.
3. Show how the Coptic and Hebrew calendars shape fixed and movable readings.
4. Explain the three Youssef seasons: sowing, harvest, and flooding.
5. Explain Sundays, feasts, fifth Sundays, and the Synaxarium.
6. Show why a reverse lectionary helps Bible study.
7. End with spiritual obedience and repentance.

### Key sentence
The lectionary is the Church teaching us how to hear Scripture with Christ at the center.

### Teacher notes

- Emphasize: The Synaxarium is not an appendix. It is part of how the daily cycle is understood.
- Watch for: Do not imply every Synaxarium entry has an explicit reading assignment. The 69-covered bridge rows are explicit source-row links, outside-69 rows remain collection-type links, and neither class is direct proper-reading proof.
- Clarify: The Sunday program governs when a Coptic day falls on Sunday. Ordinary weekdays follow the Synaxarium.
- Clarify: Psalm numbering differences are not errors by themselves. They may reflect Masoretic and Septuagint traditions.
- Connect: The readings should lead to worship, repentance, and union with Christ, not only to data accuracy.

## Discussion Questions

1. How does hearing Scripture inside the liturgy change the way we receive it?
2. Why does it matter that the daily readings follow the Synaxarium?
3. How do the two calendars help explain fixed feasts and movable Pascha?
4. What is the spiritual pattern of sowing, harvest, and flooding?
5. How can Psalm numbering differences create false conflicts if we do not track the source convention?
6. What can a reverse lectionary teach that a normal daily-reading page cannot?

## Sources

Scripture references follow NKJV versification.

### Primary liturgical and Coptic Orthodox sources

- St. Mary Coptic Orthodox Church, Ottawa, Katameros of the Days: Readings for Week Days and Feasts, first edition, 1998. Used for the printed Volume II description, weekday and feast volume framing, general reading rules, and the 69 dated table-of-contents entries.
- St. Mary Coptic Orthodox Church, Ottawa, Katameros of the Sundays: Readings for Sundays and Feasts, second edition, 2004. Used as primary printed evidence for Sunday and feast coverage in the Yearly Katameros.
- Coptic Reader app, Diocese of the Southern United States, Pascha Wednesday Day screenshots supplied by George. Used as current-practice authority for that fixture scope.
- St-Takla English Coptic Synaxarium day pages. Used as a source map for daily commemorations.
- copticchurch.net daily readings pages. Used as a public date-resolved reading source.
- UKMID Copts PDF archive, https://ukmidcopts.org/pdf/Katameros_Days.pdf, https://ukmidcopts.org/pdf/Katameros_Sundays.pdf, https://ukmidcopts.org/pdf/Katameros_Lent.pdf, and https://ukmidcopts.org/pdf/Katameros_Pentecost.pdf. Used as public hosted copies of the Ottawa Katameros family.
- St. Bishoy Coptic Orthodox Church, Deacons' Corner, https://saintbishoy.ca/deacons-corner/katameros/. Used as a public documentation layer for Katameros readings and Synaxarium materials by season.

### Secondary scholarship and structural sources

- Coptic Encyclopedia, "Lectionary," Claremont Colleges Digital Library, https://ccdl.claremont.edu/digital/api/collection/cce/id/1199/download. The CCDL entry lists the creators as Basilios, Archbishop, and Coquin, René-Georges.
- Fouad Naguib Youssef, "The Arrangement of the Church Lectionary," ACCOT, https://accot.stcyrils.edu.au/fny-read1/.
- World Council of Churches and Middle East Council of Churches, "Towards a Common Date for Easter," Aleppo, 1997, https://www.oikoumene.org/resources/documents/towards-a-common-date-for-easter.
- Fr. Andrew Stephen Damick, "No, the Paschal date difference is not about Passover (and other Orthodox urban legends)," Ancient Faith Ministries, 2022. Supplied citation used for Coptic use of the traditional Julian Paschalion.
- Greek Orthodox Archdiocese of America, "Some Common Misperceptions about the Date of Pascha/Easter." Supplied citation used for the Orthodox Paschal formula as computation, not a lookup of the modern Jewish calendar.
- timeanddate public Easter-date references for Coptic Orthodox Easter and Russian Orthodox Easter in 2026. Supplied citation used for the worked 2026 date, 12 April.
- OrthodoxWiki, "Coptic Calendar," and copticchurch.net calendar notes. Supplied citations used for the Alexandrian computational role at Nicaea and the nineteen-year Paschal cycle, with the Demetrius the Vinedresser attribution kept traditional.
- Ugo Zanetti, Les lectionnaires coptes annuels: Basse-Egypte, Publications de l'Institut Orientaliste de Louvain 33, Louvain-la-Neuve, 1985, xxiv + 383 p.
- O.H.E. Burmester, "The Coptic-Greek-Arabic Holy Week Lectionary from Scetis," Bulletin de la Societe d'Archeologie Copte XVI, 1961-1962, pp. 83-137.
- René-Georges Coquin, Coptic Encyclopedia liturgical entries and related Coptic liturgical scholarship.
- Sir Lancelot Charles Lee Brenton, Septuagint translation, used as the design-layer Septuagint comparison anchor.
- eBible.org World English Bible copyright information, https://ebible.org/Scriptures/copyright.php. Used for public-domain English Bible text policy checks.
- Wikisource, King James Bible copyright note, https://en.wikisource.org/wiki/Bible_(King_James). Used for public-domain-in-the-USA English Bible text policy checks.

### Patristic anchor

- Saint Athanasius of Alexandria, Festal Letter 39, on the Scriptures as fountains of salvation.

## Glossary

- Katameros: A Coptic lectionary book or collection of appointed readings.
- Synaxarium: The Church's daily-cycle book or index of commemorations of saints, martyrs, feasts, and events.
- Pascha: Holy Week, centered on the saving Passion of Christ.
- Holy Fifty Days: The joyful season from the Resurrection to Pentecost.
- Abuqti calculation: The Paschal calculation traditionally connected, in the attribution Youssef reports, with Ptolemy al-Farmawi and Pope Demetrius the Vinedresser.
- Septuagint: The ancient Greek Old Testament tradition used deeply in Orthodox worship.
- Masoretic numbering: The Hebrew numbering often followed by modern English Old Testaments, especially in the Psalms.
- Attestation: The witness of a source or edition to a reading.
- Reverse lectionary: A passage-to-liturgical-use index, showing where a Scripture passage is read.
"""
    for word in FORBIDDEN_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", article, re.I):
            raise AssertionError(f"Forbidden word in article: {word}")
    if "—" in article:
        raise AssertionError("Em dash found in article")
    (ROOT / "coptic-lectionary-and-synaxarium.md").write_text(article, encoding="utf-8")


def write_spec(schema: dict) -> None:
    foundational_69 = build_foundational_reading_collections_69()
    foundational_table = "\n".join(
        ["| # | collection_key | Coptic day | section page |"]
        + ["|---|---|---|---|"]
        + [f"| {row['sequence']} | `{row['collection_key']}` | {row['coptic_day_key']} | {row['reading_section_start_page']} |" for row in foundational_69]
    )
    spec = f"""# Coptic Lectionary Internal Spec

Generated: 2026-06-16

## Purpose

This spec defines the additive design layer produced in this repo for George's Coptic lectionary project. It preserves the existing validated package in `out/data/` and adds identity, attestation, temporal status, Synaxarium commemoration storage, Synaxarium reading bridge records, and site-facing outputs in `out/design/`.

## Locked decisions implemented

1. MT or modern English display remains primary for site search and user-facing references.
2. Psalm and LXX differences are stored in separate canonical fields. The identity key is not the raw source label.
3. Temporal status is derived from source attestation. The current Coptic Reader fixture governs Wednesday Day where present.
4. Printed Pascha witnesses are retained as historical evidence rather than deleted.
5. The Synaxarium is modeled as multiple commemorations per Coptic day.
6. Synaxarium reading links record their basis and confidence.

## Source authority tiers

| Tier | Meaning |
|---|---|
| current_authority | Coptic Reader where manually captured in a locked fixture. |
| public_current_practice_reference | Public current reading page such as copticchurch.net. |
| working_local_source | Structured local source used by George's package. |
| historical_printed_witness | Older printed book or extracted text useful for historical comparison. |
| scholarly_structural | Scholarly source used for structure, vocabulary, and precedence. |
| synaxarium_text_source | Source for daily commemorations. |

## Reading identity

Each reading has:

- `identity_key`, a deterministic hash over reading type and canonical fields.
- `reading_name`, for named non-verse readings such as `Memoirs of Job`.
- `source_label`, the raw or preserved source label used for matching.
- `display_ref`, MT or modern English primary with LXX annotation for Psalms where different.
- `canonical_mt_ref`.
- `canonical_lxx_ref`.
- `source_convention`.
- `canonicalization_confidence`.
- `canonicalization_note`.
- `spans_json`, an ordered list of parsed spans.

The `spans_json` value is an ordered list of span objects. Each span carries `source_ref`, `source_convention`, `canonical_mt_ref`, `canonical_lxx_ref`, `confidence`, `validation_basis`, `book`, `chapter_start`, `verse_start`, `chapter_end`, and `verse_end`. Composite and cross-Psalm references are therefore not reduced to one flattened range.

Named readings such as `Memoirs of Job` are stored as `named-reading` with `reading_name`; they do not enter normal passage search unless later resolved to a verse span by source.

## Liturgical placement

The target placement path is:

`occasion -> service -> hour -> slot -> order`

The design layer stores this through:

- `occasion`
- `calendar_key`
- `day_title`
- `service_day`
- `service_hour`
- `service_section`
- `slot`
- `order`

This retires lossy labels such as generic `OT1` where a richer slot can be produced later, while preserving old slot values for traceability.

## Temporal lifecycle

The design layer uses these status classes:

- `current_confirmed_coptic_reader`
- `current_confirmed_by_fixture_equivalence`
- `pending_psalm_equivalence_unresolved`
- `historical_candidate_removed`
- `historical_witness`
- `current_working_source_not_coptic_reader_checked`
- `current_public_or_local_reference`

The main unresolved limitation is current-practice coverage outside the locked Coptic Reader Wednesday Day fixture. Those rows are not presented as Coptic Reader confirmed.

## Attestation

Pascha attestation groups rows by day, hour, and identity key. Buckets:

- `current_confirmed`: a Coptic Reader fixture row is present in the group.
- `consensus_without_coptic_reader`: two or more non-Coptic Reader sources agree after normalization.
- `old_edition_only`: only historical printed or extracted witnesses attest the row.
- `old_edition_only_candidate_removed`: older/local data attests the row but the current Coptic Reader fixture omits it within fixture scope.
- `single_source_candidate`: one source attests the row and no current-authority fixture confirms it.

Public or local current-reference rows are not the same as Coptic Reader-confirmed rows. `current_public_or_local_reference` means useful reference data, not final current-practice authority.

## Controlled vocabulary snapshot

The machine-readable source of truth is `out/design/lectionary_schema.json`. It includes explicit values for:

- `source_convention`: `modern_english_reference`, `mt_nkjv`, `lxx_liturgical_or_fixture_label`.
- `occasion`: emitted placement category; `occasion_type` is retained in the schema as an alias for the same conceptual vocabulary.
- `canonicalization_confidence`: `high`, `medium`, `low`, `n/a`.
- `current_status`: `current_confirmed_coptic_reader`, `current_confirmed_by_fixture_equivalence`, `pending_psalm_equivalence_unresolved`, `historical_candidate_removed`, `historical_witness`, `current_working_source_not_coptic_reader_checked`, `current_public_or_local_reference`, `unknown`.
- `current_authority`: separate from `current_status`; it states which authority, if any, is allowed to govern current practice for that row.
- `removed_marker`: uniform placement-level string for older Pascha placements absent from the scoped current Coptic Reader fixture. The marker cites the older source boundary and the current comparator that lacks it.
- `source_title`, `source_edition`, `source_locator`, and `source_url`: citable provenance fields carried by placement and disclosure rows. `source_locator` points to a page, URL, local source row, extracted text line, or API/cache field.
- `attestation_bucket`: `current_confirmed`, `consensus_without_coptic_reader`, `old_edition_only`, `old_edition_only_candidate_removed`, `single_source_candidate`.
- `service_day`, `service_hour`, and `service_section`: source labels are preserved when the source's service structure does not fit a normalized value.
- `slot`: normalized Scripture and liturgical slots plus `source_label_preserved`.
- Psalm `mapping_scope`: `chapter_equivalence`, `split_merge_chapter_seam`, `lxx_unique_chapter`, `anchored_verse_example`, `unresolved_verse_offset_example`.
- Synaxarium `type`: `lord_feast`, `theotokos`, `martyr`, `apostle`, `patriarch`, `hierarch`, `departure`, `prophet`, `angel`, `ascetic`, `feast`, `commemoration`.
- bridge `basis`: `explicit`, `collection-type`, `inferred`.
- bridge `confidence`: `high`, `medium`, `low`.
- `collection_types_69`: the 69 foundational reading collections keyed by `collection_key` and `coptic_day_key`, with membership verdict and source provenance.

## Foundational reading collections

The machine-readable vocabulary is `out/design/foundational_reading_collections_69.csv` and `out/design/foundational_reading_collections_69.jsonl`. It is also embedded under `controlled_vocabularies.collection_types_69` in `out/design/lectionary_schema.json`.

Membership verdict: `CONFIRMED_SAME_SET`. This means confirmed as the same practical second-volume foundational-reading collection, inferred from source identity, volume two placement, annual mapping function, commemoration categories, and count. It does not mean the consulted Youssef page prints the date-by-date roster.

Provenance:

- Youssef source: F.N. Youssef, `The Arrangement of the Church Lectionary`, ACCOT, Chapter 1, section 1.1, printed page marker 32, note 7 `al-qirā’āt al-āsāsiyya`.
- Ottawa source: St. Mary Ottawa / UKMID, `Katameros of the Days: Readings for Week Days and Feasts`, first edition, Christmas 1714 A.M., 1998 A.D.
- Ottawa locators: introduction on PDF page 17; TOC dated reading sections on PDF pages 23 to 26; annual day table on PDF pages 31 to 65.
- Source-vs-inference: the 69 dated entries and their section pages are read from Ottawa/UKMID; membership identity with Youssef's named 69 is inferred from the Step 1 audit, not from a Youssef-printed roster.

{foundational_table}

## Psalm MT to LXX crosswalk

The design layer includes `out/design/psalm_mt_lxx_crosswalk.csv`. It encodes chapter seams from the design brief and separates `mapping_scope` values for chapter equivalence, split/merge chapter seams, LXX-only Psalm 151, anchored verse examples, and unresolved verse-offset examples. It does not guess verse offsets except where Brenton/KJV content comparison established an example.

## Synaxarium model

Each commemoration is stored separately in `out/design/synaxarium_commemorations.csv`:

- `commem_id`
- `coptic_month`
- `coptic_day`
- `rank`
- `title`
- `type`
- `source`
- `source_url`

## Synaxarium bridge

Bridge rows live in `out/design/synaxarium_reading_bridge.csv`:

- `commem_id`
- `coptic_day_key`
- `commemoration_title`
- `commemoration_type`
- `reading_identity_key`
- `display_ref`
- `slot`
- `basis`
- `confidence`
- `citation`
- `note`

Rows whose Coptic day is enumerated in the Ottawa/UKMID 69 foundational-reading collection use `explicit` basis and `high` confidence. Outside those 69 days, bridge rows remain `collection-type` and `medium`. Repeated groups are source-row or variant catalog rows, not resolved daily service schedules.

## Controlled vocabularies

See `out/design/lectionary_schema.json` for machine-readable vocabularies. The 69 collection vocabulary is now enumerated from the Ottawa/UKMID TOC and records the Step 1 membership verdict, provenance, and source-vs-inference caveat.

## Site-facing outputs

- `out/design/reverse_lectionary_presentation.csv`
- `out/design/reverse_lectionary_presentation.jsonl`
- `out/design/todays_readings_current_practice.csv`
- `out/design/passage_liturgical_footprint.csv`
- `out/design/pascha_attestation.csv`
- `out/design/temporal_classification.csv`
- `out/design/synaxarium_commemorations.csv`
- `out/design/synaxarium_reading_bridge.csv`
- `out/design/foundational_reading_collections_69.csv`
- `out/design/foundational_reading_collections_69.jsonl`
- `out/design/passage_source_disclosure.csv`
- `out/design/passage_source_disclosure.jsonl`
- `site_integration_spec.md`

## Acceptance notes

- Structural claims in the article cite named sources.
- Inferences are flagged.
- The schema is complete enough to drive the additive design-layer outputs.
- Removed Pascha placements remain in the model with `removed_marker`; they are historical witnesses, not deleted rows.
- Full Coptic Reader ingestion is not claimed because the project brief states that Coptic Reader content is encrypted and manual fixtures are the route.
"""
    if "—" in spec:
        raise AssertionError("Em dash found in spec")
    (ROOT / "lectionary_spec.md").write_text(spec, encoding="utf-8")


def write_site_integration_spec(summary: dict) -> None:
    text = f"""# Site Integration Spec: Coptic Lectionary Design Layer

Generated: 2026-06-16

George will push these files into the site repo. Hermes does not have `coptic-corpus` access in this run.

## Files to copy

Copy the following from this repo:

- `coptic-lectionary-and-synaxarium.md`
- `lectionary_spec.md`
- `out/design/lectionary_schema.json`
- `out/design/foundational_reading_collections_69.csv`
- `out/design/foundational_reading_collections_69.jsonl`
- `out/design/reverse_lectionary_presentation.csv`
- `out/design/reverse_lectionary_presentation.jsonl`
- `out/design/todays_readings_current_practice.csv`
- `out/design/todays_readings_current_practice.jsonl`
- `out/design/passage_liturgical_footprint.csv`
- `out/design/passage_liturgical_footprint.jsonl`
- `out/design/passage_source_disclosure.csv`
- `out/design/passage_source_disclosure.jsonl`
- `out/design/pascha_attestation.csv`
- `out/design/pascha_attestation_bucket_manifest.csv`
- `out/design/temporal_classification.csv`
- `out/design/temporal_residue.csv`
- `out/design/temporal_residue_manifest.csv`
- `out/design/synaxarium_commemorations.csv`
- `out/design/synaxarium_reading_bridge.csv`
- `out/design/source_registry.csv`
- `out/design/psalm_mt_lxx_crosswalk.csv`
- `audit_artifacts/open_questions_for_george.md`
- `presentation/lectionary_design_layer_deck.pptx`
- `presentation/lectionary_design_layer_deck_outline.md`

## Required search behavior

1. Accept MT or modern English input by default, for example `Psalm 51`.
2. Accept LXX liturgical Psalm input, for example `Psalm 50`, by consulting `canonical_lxx_ref` and the Psalm crosswalk.
3. Resolve both to `identity_key` before showing results.
4. Show `display_ref` to users. If LXX differs, keep the inline LXX annotation.
5. Never collapse historical and current readings without displaying `current_status`.

## Reverse lectionary page behavior

For each passage page:

- group by `current_status`, then season or source kind,
- show current Coptic Reader confirmed rows first where available,
- label historical Pascha witnesses clearly,
- include source and provenance links when present,
- show Synaxarium bridge rows only with their `basis`, `confidence`, and `note`.

## Synaxarium bridge behavior

Rows whose Coptic day is enumerated in the Ottawa/UKMID 69 foundational-reading collection are `basis=explicit` and `confidence=high` in this run. Rows outside that 69 remain `basis=collection-type` and `confidence=medium`. They connect the primary commemoration of a fixed Coptic day to Katameros fixed-day rows. They are discovery links, not direct proper-reading proof for the named commemoration.

Repeated `(commem_id, coptic_day_key, slot)` groups are expected because the bridge catalogs source rows and variants. Do not render the bridge as a resolved daily service schedule without a later resolver.

Secondary commemorations are intentionally not linked unless a future source gives explicit proper-reading evidence.

## Today's readings behavior

Use `todays_readings_current_practice.csv` as the current static snapshot produced in this run. For dynamic production use, the site should generate a date key and resolve against the date-resolved reading table in the main lectionary package or a fresh current-practice source.

## Passage footprint behavior

Use `passage_liturgical_footprint.csv` for cards and chapter pages. It provides:

- occurrence counts,
- current and historical counts,
- sample liturgical places,
- hour themes,
- placeholder chapter-study and audio slugs.

The `patristic_homily_slug` field is blank in this repo because the site corpus is not available here. Join it in `coptic-corpus` where homily and chapter-study metadata live.

## Deck deliverables

The deck artifacts are handoff aids for George, not site source files:

- `presentation/lectionary_design_layer_deck.pptx`
- `presentation/lectionary_design_layer_deck_outline.md`

Use them to explain the reverse lectionary design, Psalm numbering, Pascha attestation, Synaxarium bridge limits, and open questions before the final site push.

## Counts from this run

```json
{json.dumps(summary, indent=2)}
```

## Deployment verification

After George pushes, verify the plain public URL, not only a cache-busted URL. A cache-buster can prove origin freshness but not normal user delivery.
"""
    if "—" in text:
        raise AssertionError("Em dash found in site integration spec")
    (ROOT / "site_integration_spec.md").write_text(text, encoding="utf-8")


def update_open_questions(commems: list[dict], bridge: list[dict], temporal_residue: list[dict]) -> None:
    multi_days = Counter(c["coptic_day_key"] for c in commems)
    ambiguous = sorted(day for day, count in multi_days.items() if count > 1)
    low_bridge = [b for b in bridge if b.get("confidence") == "low" or b.get("basis") == "inferred"]
    residue_counts = Counter(r.get("residue_type", "") for r in temporal_residue)
    candidate_removed = [r for r in temporal_residue if r.get("residue_type") == "candidate_removed_needs_current_authority_confirmation"]
    removed_marker_rows = [r for r in temporal_residue if r.get("removed_marker")]
    other_candidate_removed = [r for r in candidate_removed if not r.get("removed_marker")]
    psalm_pending = [r for r in temporal_residue if r.get("residue_type") == "psalm_equivalence_unresolved"]
    current_pending = [r for r in temporal_residue if r.get("residue_type") == "current_authority_pending"]
    foundational_rows = build_foundational_reading_collections_69()
    bridge_days = {row.get("coptic_day_key", "") for row in bridge}
    foundational_without_bridge = [row for row in foundational_rows if row.get("coptic_day_key", "") not in bridge_days]
    text = """# Open Questions and Decisions for George

This file collects only the questions that thorough research, source comparison, and independent audit could not settle during the autonomous lectionary execution run.

## Youssef 15 weeks or 107 days

ACCOT confirms the wording `(15 weeks or 107 days)`. Since 15 weeks is 105 days, the article reports Youssef's figure as given and notes the arithmetic issue.

## Psalm numbering text-equivalence review

The active execution brief states that the Coptic Reader Wednesday Day fixture is faithful to the screenshots, including Third Hour `Psalm 41` and Sixth Hour `Psalm 83`, and that Coptic Reader governs where external books disagree. During Phase 1, Brenton/KJV seam checks resolved several exact pairs: LXX `Ps 41:6` to MT `Ps 42:5`, LXX `Ps 83:2` to MT `Ps 84:1`, and LXX `Ps 83:5` to MT `Ps 84:4`.

Decision needed later: before presenting Third Hour `Psalm 41:1` as an exact MT-primary reference, compare the fixture Psalm text against Brenton and a public-domain MT text. Until then, the design layer preserves the Coptic Reader LXX label and marks the exact MT equivalence as unresolved.

## Coptic Reader coverage beyond Wednesday Day

The repo has a locked Coptic Reader fixture for Pascha Wednesday Day only. Current-vs-historical classifications outside that fixture are marked as candidates unless supported by other current sources. Do not treat them as fully Coptic Reader confirmed.

## Pascha removed-reading candidates

Rows absent from the Wednesday Day Coptic Reader fixture but present in older or local Pascha data are classified as `historical_candidate_removed` in `out/design/temporal_classification.csv`. Only the passages named in George's removed-marker instruction receive `removed_marker`; other old-edition-only rows remain review candidates without that marker. George or a liturgical reviewer should decide whether each unmarked candidate is truly removed, a named-reading equivalent, or a fixture scope issue.

Marker-format decision: this run keeps `removed_marker` as a uniform prose-pattern string that includes the older source and current comparator. A later model pass should decide whether to keep that pattern or split it into a single controlled token plus a separate note field.
"""
    text += "\n## Temporal residue summary\n\n"
    text += "See `out/design/temporal_residue.csv` and `out/design/temporal_residue_manifest.csv` for the full row-level list and counts. Counts by residue type:\n"
    for residue_type, count in sorted(residue_counts.items()):
        text += f"- `{residue_type}`: {count}\n"
    text += "- `true_source_disagreement`: 0\n"
    text += "\nNo true source-disagreement class was emitted in this run. Unsettled rows are classified as pending authority, historical witness without current comparator, candidate removed, or Psalm-equivalence unresolved.\n"
    text += "\n### Rows with `removed_marker` populated by George's list\n\n"
    for row in removed_marker_rows:
        text += f"- {row.get('day_title')} | {row.get('service_hour')} | {row.get('display_ref')} | {row.get('removed_marker')}\n"
    text += "\n### Other old-edition-only candidate-removed rows needing review\n\n"
    for row in other_candidate_removed:
        text += f"- {row.get('day_title')} | {row.get('service_hour')} | {row.get('display_ref')} | {row.get('reason')}\n"
    text += "\n### Psalm equivalence unresolved rows\n\n"
    for row in psalm_pending:
        text += f"- {row.get('day_title')} | {row.get('service_hour')} | {row.get('display_ref')} | {row.get('attestation_note') or row.get('reason')}\n"
    text += "\n### Current-authority pending class\n\n"
    text += f"There are {len(current_pending)} rows not checked by a captured Coptic Reader fixture and not confirmed by two independent sources. Use `out/design/temporal_residue.csv` for the full list. Sample rows:\n"
    for row in current_pending[:25]:
        text += f"- {row.get('day_title')} | {row.get('service_hour')} | {row.get('display_ref')}\n"
    if len(current_pending) > 25:
        text += f"- ... {len(current_pending) - 25} more current-authority pending rows.\n"
    text += """

## Synaxarium bridge review

The bridge links the primary commemoration of each fixed Coptic day to that day's Katameros readings. After Step 7, rows whose Coptic day is in the Ottawa/UKMID 69 foundational-reading collection are `basis=explicit` and `confidence=high`. Rows outside the 69 remain uniformly `basis=collection-type` and `confidence=medium`. These rows are discovery links, not direct proper-reading proof and not a resolved daily service schedule.

Bridge differentiation flag: outside the 69 foundational days, the bridge is still uniformly collection-type. A later pass should decide whether more non-69 days can be classified explicitly, left as collection-type, or marked inferred.

Foundational-day coverage flag: 11 of the 69 foundational days have no emitted bridge rows in this run, because the bridge only emits days that have both a Synaxarium primary commemoration row and local fixed-day Katameros rows. Missing foundational days:
"""
    for row in foundational_without_bridge:
        text += f"- {row.get('coptic_day_key')} | {row.get('source_locator')}\n"
    text += "\nAll repeated-slot groups are documented in `out/design/synaxarium_reading_bridge.csv` row notes as source-row or variant catalog entries.\n\n"
    text += "- Multi-commemoration days needing future ecclesiastical or source review: " + str(len(ambiguous)) + " days.\n"
    for day in ambiguous[:120]:
        text += f"  - {day}\n"
    if len(ambiguous) > 120:
        text += f"  - ... {len(ambiguous) - 120} more days. See out/design/synaxarium_commemorations.csv.\n"
    text += "\n"
    if low_bridge:
        text += "## Low-confidence bridge rows\n\n"
        for b in low_bridge[:200]:
            text += f"- {b.get('coptic_day_key')} | {b.get('commemoration_title')} | {b.get('display_ref')} | basis={b.get('basis')} | confidence={b.get('confidence')}\n"
        if len(low_bridge) > 200:
            text += f"- ... {len(low_bridge) - 200} more rows. See out/design/synaxarium_reading_bridge.csv.\n"
    else:
        text += "## Low-confidence bridge rows\n\nNo bridge rows were emitted with `basis=inferred` or `confidence=low`. Medium-confidence multi-commemoration days are listed above.\n"
    text += "\n## Site corpus joins not available in this repo\n\nThe presentation footprint output includes blank `patristic_homily_slug` values because Hermes did not have access to `coptic-corpus`. Join homily, chapter-study, and audio slugs in the site repo before publishing those UI links.\n"
    text += "\n## Final push package pointers\n\n"
    text += "- Article markdown: `coptic-lectionary-and-synaxarium.md`\n"
    text += "- Site integration spec: `site_integration_spec.md`\n"
    text += "- Presentation dataset: `out/design/reverse_lectionary_presentation.csv` and `.jsonl`\n"
    text += "- Today's readings snapshot: `out/design/todays_readings_current_practice.csv` and `.jsonl`\n"
    text += "- Passage footprint dataset: `out/design/passage_liturgical_footprint.csv` and `.jsonl`\n"
    text += "- Synaxarium datasets: `out/design/synaxarium_commemorations.csv` and `out/design/synaxarium_reading_bridge.csv`\n"
    text += "- Deck deliverables: `presentation/lectionary_design_layer_deck.pptx` and `presentation/lectionary_design_layer_deck_outline.md`\n"
    text += "- Execution log: `audit_artifacts/lectionary_execution_log.md`\n"
    if "—" in text:
        raise AssertionError("Em dash found in open questions")
    (AUDIT / "open_questions_for_george.md").write_text(text, encoding="utf-8")


def main() -> None:
    schema = write_schema()
    presentation_rows, identities = build_reverse_presentation()
    psalm_rows = build_psalm_crosswalk()
    attestation, temporal = build_attestation(presentation_rows)
    attestation_bucket_manifest = build_attestation_bucket_manifest(attestation, schema)
    temporal_residue = build_temporal_residue(temporal, attestation)
    temporal_residue_manifest = build_temporal_residue_manifest(temporal_residue)
    commems, bridge = build_synaxarium()
    foundational_69 = build_foundational_reading_collections_69()
    today_rows = build_today_rows(presentation_rows)
    footprint = build_footprint(presentation_rows)
    passage_source_disclosure = build_passage_source_disclosure(presentation_rows)

    presentation_fields = [
        "identity_key", "reading_type", "reading_name", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_convention", "canonicalization_confidence", "canonicalization_note", "spans_json", "current_status", "status_note", "removed_marker", "source_key", "source_title", "source_edition", "source_locator", "source_url", "source_kind", "source_family", "source_file", "source_row_id", "authority_tier", "occasion", "calendar_key", "gregorian_date", "coptic_date", "day_title", "service_day", "service_hour", "service_section", "reading_slot", "slot", "order", "hour_theme", "source_ref", "raw_ref", "url", "provenance",
    ]
    identity_fields = ["identity_key", "reading_type", "reading_name", "source_label", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_convention", "canonicalization_confidence", "canonicalization_note", "spans_json"]
    write_csv(OUT / "reading_identity.csv", identities.values(), identity_fields)
    write_jsonl(OUT / "reading_identity.jsonl", identities.values())
    write_csv(OUT / "reverse_lectionary_presentation.csv", presentation_rows, presentation_fields)
    write_jsonl(OUT / "reverse_lectionary_presentation.jsonl", presentation_rows)
    write_csv(OUT / "todays_readings_current_practice.csv", today_rows, presentation_fields)
    write_jsonl(OUT / "todays_readings_current_practice.jsonl", today_rows)
    write_csv(OUT / "psalm_mt_lxx_crosswalk.csv", psalm_rows, ["mt_psalm", "lxx_psalm", "map_direction", "mapping_scope", "confidence", "validation_basis", "note"])
    write_jsonl(OUT / "psalm_mt_lxx_crosswalk.jsonl", psalm_rows)
    write_csv(OUT / "pascha_attestation.csv", attestation, ["day_title", "service_hour", "identity_key", "display_ref", "source_count", "sources", "source_titles", "source_editions", "source_locators", "bucket", "statuses", "removed_marker", "citation", "attestation_note"])
    write_jsonl(OUT / "pascha_attestation.jsonl", attestation)
    write_csv(OUT / "pascha_attestation_bucket_manifest.csv", attestation_bucket_manifest, ["bucket", "row_count", "present_in_phase3", "note"])
    write_jsonl(OUT / "pascha_attestation_bucket_manifest.jsonl", attestation_bucket_manifest)
    write_csv(OUT / "temporal_classification.csv", temporal, ["day_title", "service_hour", "identity_key", "display_ref", "lifecycle_status", "current_status", "removed_marker", "source_authority_tier", "source_titles", "source_editions", "source_locators", "attestation_bucket", "current_authority", "valid_from", "valid_to", "derivation", "attesting_sources"])
    write_jsonl(OUT / "temporal_classification.jsonl", temporal)
    temporal_residue_fields = ["day_title", "service_hour", "identity_key", "display_ref", "lifecycle_status", "attestation_bucket", "current_status", "removed_marker", "current_authority", "residue_type", "reason", "citation", "attestation_note"]
    write_csv(OUT / "temporal_residue.csv", temporal_residue, temporal_residue_fields)
    write_jsonl(OUT / "temporal_residue.jsonl", temporal_residue)
    write_csv(OUT / "temporal_residue_manifest.csv", temporal_residue_manifest, ["residue_type", "row_count", "present_in_phase4", "note"])
    write_jsonl(OUT / "temporal_residue_manifest.jsonl", temporal_residue_manifest)
    write_csv(OUT / "synaxarium_commemorations.csv", commems, ["commem_id", "coptic_month", "coptic_day", "coptic_day_key", "rank", "title", "type", "extraction_method", "caveat", "source", "source_url", "source_day_title", "source_summary"])
    write_jsonl(OUT / "synaxarium_commemorations.jsonl", commems)
    write_csv(OUT / "synaxarium_reading_bridge.csv", bridge, ["commem_id", "coptic_day_key", "commemoration_title", "commemoration_type", "reading_identity_key", "display_ref", "slot", "basis", "confidence", "citation", "note"])
    write_jsonl(OUT / "synaxarium_reading_bridge.jsonl", bridge)
    write_csv(OUT / "passage_liturgical_footprint.csv", footprint, ["identity_key", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "total_occurrences", "current_occurrences", "historical_occurrences", "source_kinds", "sample_liturgical_places", "hour_themes", "patristic_homily_slug", "chapter_study_slug", "audio_slug", "site_note"])
    write_jsonl(OUT / "passage_liturgical_footprint.jsonl", footprint)
    disclosure_fields = ["identity_key", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_key", "source_title", "source_edition", "source_locator", "source_url", "source_ref", "occasion", "calendar_key", "day_title", "service_hour", "slot", "current_status", "removed_marker", "citation"]
    write_csv(OUT / "passage_source_disclosure.csv", passage_source_disclosure, disclosure_fields)
    write_jsonl(OUT / "passage_source_disclosure.jsonl", passage_source_disclosure)
    write_csv(OUT / "source_registry.csv", SOURCE_REGISTRY, ["source_key", "title", "edition", "url", "default_locator", "authority_tier", "confidence", "notes"])
    write_jsonl(OUT / "source_registry.jsonl", SOURCE_REGISTRY)
    foundational_fields = ["collection_key", "sequence", "coptic_month", "coptic_day", "coptic_day_key", "calendar_key", "toc_label", "reading_section_start_page", "source_key", "source_title", "source_edition", "source_url", "source_locator", "membership_status", "membership_verdict", "membership_basis", "verification_status"]
    write_csv(OUT / "foundational_reading_collections_69.csv", foundational_69, foundational_fields)
    write_jsonl(OUT / "foundational_reading_collections_69.jsonl", foundational_69)

    write_article()
    write_spec(schema)
    summary = {
        "reverse_lectionary_presentation_rows": len(presentation_rows),
        "reading_identity_rows": len(identities),
        "todays_readings_rows": len(today_rows),
        "psalm_crosswalk_rows": len(psalm_rows),
        "pascha_attestation_rows": len(attestation),
        "pascha_attestation_bucket_manifest_rows": len(attestation_bucket_manifest),
        "temporal_classification_rows": len(temporal),
        "temporal_residue_rows": len(temporal_residue),
        "temporal_residue_manifest_rows": len(temporal_residue_manifest),
        "synaxarium_commemoration_rows": len(commems),
        "synaxarium_bridge_rows": len(bridge),
        "passage_footprint_rows": len(footprint),
        "passage_source_disclosure_rows": len(passage_source_disclosure),
        "foundational_reading_collection_rows": len(foundational_69),
    }
    write_site_integration_spec(summary)
    update_open_questions(commems, bridge, temporal_residue)
    (OUT / "BUILD_DESIGN_SUMMARY.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
