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
        "authority_tier": "current_authority",
        "confidence": "confirmed_for_wednesday_day_only",
        "notes": "Manual fixture from screenshots. Coptic Reader governs current practice where captured.",
    },
    {
        "source_key": "coptic_encyclopedia_lectionary",
        "title": "Coptic Encyclopedia, Lectionary entry, Claremont CCDL",
        "url": "https://ccdl.claremont.edu/digital/api/collection/cce/id/1199/download",
        "authority_tier": "scholarly_structural",
        "confidence": "confirmed",
        "notes": "Defines the lectionary as four books and explains historical development and calendar value.",
    },
    {
        "source_key": "fn_youssef_arrangement",
        "title": "Fouad Naguib Youssef, The Arrangement of the Church Lectionary, ACCOT",
        "url": "https://accot.stcyrils.edu.au/fny-read1/",
        "authority_tier": "scholarly_structural",
        "confidence": "confirmed_for_principles",
        "notes": "Explains calendar logic, Sunday cycle, and the relation of daily readings to the Synaxarium.",
    },
    {
        "source_key": "ugo_zanetti_annual_lectionaries",
        "title": "Ugo Zanetti, Les lectionnaires coptes annuels, Basse-Egypte",
        "url": "https://openlibrary.org/books/OL2304712M/Les_lectionnaires_coptes_annuels",
        "authority_tier": "scholarly_structural",
        "confidence": "bibliographic_confirmed_content_not_fully_ingested",
        "notes": "Standard scholarly study cited by the Coptic Encyclopedia for annual lectionaries.",
    },
    {
        "source_key": "katameros_api_sqlite",
        "title": "pierresaid Katameros API SQLite source bundled in repo",
        "url": "sources/katameros-api/Core/KatamerosDatabase.db",
        "authority_tier": "working_local_source",
        "confidence": "confirmed_local",
        "notes": "Main local structured source for annual, Sunday, Great Lent, and Holy Fifty cycle tables.",
    },
    {
        "source_key": "copticchurch_date_resolved",
        "title": "copticchurch.net date-resolved readings cache, 2020 to 2035",
        "url": "https://www.copticchurch.net/readings",
        "authority_tier": "public_current_practice_reference",
        "confidence": "confirmed_local_cache",
        "notes": "Date-resolved public readings used by the existing local package.",
    },
    {
        "source_key": "st_mary_ottawa_pascha",
        "title": "St. Mary Ottawa Holy Pascha extracted text",
        "url": "out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt",
        "authority_tier": "historical_printed_witness",
        "confidence": "confirmed_local_extraction_with_known_parser_caveats",
        "notes": "Useful historical witness. Not current authority when it disagrees with Coptic Reader.",
    },
    {
        "source_key": "st_takla_synaxarium",
        "title": "St-Takla English Coptic Synaxarium day index",
        "url": "https://st-takla.org/Full-Free-Coptic-Books/Coptic-Synaxarium-or-Synaxarion_English/Eng-Synexarium-or-Synexarion-index.html",
        "authority_tier": "synaxarium_text_source",
        "confidence": "confirmed_index_not_full_text_ingestion",
        "notes": "Used to store day commemorations and source URLs. Full text should be opened when exact wording matters.",
    },
    {
        "source_key": "special_service",
        "title": "Special-service readings extracted in the local package",
        "url": "out/data/reverse_lookup_crosswalk.csv",
        "authority_tier": "working_local_source",
        "confidence": "confirmed_local",
        "notes": "Local structured special-service rows retained with source labels and provenance.",
    },
    {
        "source_key": "agpeya",
        "title": "Agpeya readings extracted in the local package",
        "url": "out/data/reverse_lookup_crosswalk.csv",
        "authority_tier": "working_local_source",
        "confidence": "confirmed_local",
        "notes": "Local structured Agpeya rows retained with source labels and provenance.",
    },
    {
        "source_key": "bright_saturday_service_order",
        "title": "Bright Saturday service-order readings extracted in the local package",
        "url": "out/data/reverse_lookup_crosswalk.csv",
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
    fixture_rows = load_fixture_rows()
    all_rows = base_rows + fixture_rows
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
        section = row.get("service_section") or row.get("service_hour") or row.get("reading_type") or ""
        hour_theme = HOUR_THEME.get(row.get("service_hour") or row.get("service_section") or "", "")
        presentation_rows.append({
            **ident,
            "current_status": current_status,
            "status_note": status_note,
            "source_key": source_key_for(row),
            "source_kind": row.get("source_kind", ""),
            "source_family": row.get("source_family", ""),
            "source_file": row.get("source_file", ""),
            "source_row_id": row.get("source_row_id", ""),
            "authority_tier": next((s["authority_tier"] for s in SOURCE_REGISTRY if s["source_key"] == source_key_for(row)), "unclassified"),
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
        statuses = sorted(set(r.get("current_status", "") for r in rows))
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
            "bucket": bucket,
            "statuses": "; ".join(statuses),
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
            "source_authority_tier": "; ".join(source_authority_tiers),
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


def classify_commem(title: str) -> str:
    t = title.lower()
    if "lord" in t or "nativity" in t or "theophany" in t or "resurrection" in t or "cross" in t:
        return "lord_feast"
    if "theotokos" in t or "virgin" in t or "st. mary" in t or "holy virgin" in t:
        return "theotokos"
    if "martyr" in t or "martyrdom" in t:
        return "martyr"
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
        for piece in pieces:
            if re.match(r"^\d+\.\s+", piece):
                titles.append(re.sub(r"^\d+\.\s+", "", piece).strip())
            elif titles:
                break
        if not titles:
            title = row.get("day_title", "") or coptic_key
            titles = [title]
        for idx, title in enumerate(titles, 1):
            commem_id = f"{slugify(month)}-{day:02d}-{idx:02d}"
            commems.append({
                "commem_id": commem_id,
                "coptic_month": month,
                "coptic_day": day,
                "coptic_day_key": coptic_key,
                "rank": idx,
                "title": title,
                "type": classify_commem(title),
                "source": "St-Takla English Synaxarium",
                "source_url": row.get("day_url", ""),
                "source_day_title": row.get("day_title", ""),
                "source_summary": row.get("summary_lines", "")[:1000],
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
    by_day = defaultdict(list)
    for c in commems:
        by_day[c["coptic_day_key"]].append(c)
    for day_key, day_commems in by_day.items():
        readings = fixed_day_rows.get(day_key, [])
        if not readings:
            alt_key = day_key.replace("Tut", "Tout").replace("Tubah", "Toba")
            readings = fixed_day_rows.get(alt_key, [])
        primary = sorted(day_commems, key=lambda c: int(c["rank"]))[0]
        confidence = "medium" if len(day_commems) > 1 else "high"
        basis = "collection-type"
        for row in readings:
            ident = identity_for(row.get("passage") or row.get("normalized_segment") or "")
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
                "citation": "F.N. Youssef on daily readings following the Synaxarium; St-Takla day index; local Katameros fixed-day row.",
                "note": "Primary commemoration linked to fixed-day readings. Secondary commemorations require explicit proper-reading source before separate links are created." if len(day_commems) > 1 else "Single commemoration day alignment.",
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


def write_schema() -> dict:
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
                "status": "source_confirmed_count_not_fully_enumerated",
                "confirmed_count": 69,
                "working_types": ["Lord feasts", "Theotokos feasts", "angels", "apostles", "martyrs", "patriarchs", "hierarchs", "monastics and ascetics", "prophets", "ordinary fixed day", "Sunday monthly program"],
                "gap": "Accessible English sources confirm the 69 collections but did not expose the full enumerated list during this run.",
            },
        },
        "tables": {
            "reading_identity": ["identity_key", "reading_type", "reading_name", "source_label", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_convention", "canonicalization_confidence", "canonicalization_note", "spans_json"],
            "liturgical_placement": ["identity_key", "occasion", "calendar_key", "day_title", "service_day", "service_hour", "service_section", "slot", "order"],
            "temporal_attestation": ["identity_key", "source_key", "source_authority_tier", "current_status", "attestation_bucket", "current_authority", "valid_from", "valid_to"],
            "temporal_classification": ["day_title", "service_hour", "identity_key", "display_ref", "lifecycle_status", "current_status", "source_authority_tier", "attestation_bucket", "current_authority", "valid_from", "valid_to", "derivation", "attesting_sources"],
            "temporal_residue": ["day_title", "service_hour", "identity_key", "display_ref", "lifecycle_status", "attestation_bucket", "current_status", "current_authority", "residue_type", "reason", "citation", "attestation_note"],
            "temporal_residue_manifest": ["residue_type", "row_count", "present_in_phase4", "note"],
            "psalm_mt_lxx_crosswalk": ["mt_psalm", "lxx_psalm", "map_direction", "mapping_scope", "confidence", "validation_basis", "note"],
            "pascha_attestation_bucket_manifest": ["bucket", "row_count", "present_in_phase3", "note"],
            "synaxarium_commemoration": ["commem_id", "coptic_month", "coptic_day", "rank", "title", "type", "source_url"],
            "synaxarium_reading_bridge": ["commem_id", "reading_identity_key", "slot", "basis", "confidence", "citation"],
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

For the core lectionary books, the Coptic Encyclopedia describes four books used for the readings of the Coptic Church:

1. The Annual Katameros, for Sundays and weekdays through the year.
2. The Great Lent Katameros.
3. The Pascha Katameros, arranged by the hours of Holy Week.
4. The Pentecost Katameros, for the Holy Fifty Days.

This four-book description concerns the core Katameros lectionary books, not every liturgical, sacramental, Agpeya, Synaxarium, or rite-specific source that may contain readings or commemorative material.

The word Katameros means "according to the parts" or "in parts." This is exactly what the book does. It gives the appointed parts of Scripture to be read at each service, feast, fast, and commemoration.

## The year has a spiritual grammar

The Coptic calendar gives the fixed framework of the year. Feasts such as Nayrouz, Nativity, Theophany, and the feasts of saints are tied to Coptic dates. Pascha and the Resurrection are movable, calculated according to the Paschal rule received from the ancient Church. Around that movable center, Great Lent, Holy Week, the Resurrection, Ascension, and Pentecost take their place.

F.N. Youssef explains that the Coptic readings depend on both the Coptic calendar and the Paschal calculation. The fixed calendar gives the daily and sanctoral rhythm. Pascha gives the saving center of the year.

This is why the lectionary is not flat. A weekday in the Annual cycle, a Sunday of Great Lent, the Sixth Hour of Good Friday, and a day in the Holy Fifty do not function the same way. Each has its own spiritual logic.

## Sundays, feasts, and the Synaxarium

The Sunday readings are a distinct program. The Sundays of each Coptic month unfold a spiritual theme, especially through the Gospel. When a Coptic day falls on a Sunday, the Sunday program has its own authority.

Major feasts also govern the day. The feast is not decoration around the readings. The feast tells us how to receive the readings.

For ordinary weekdays, Youssef's principle is essential: the daily readings follow the Synaxarium. The Synaxarium is therefore not a side note after the readings. It is a living index of the daily cycle. The lives of the saints, martyrs, patriarchs, prophets, ascetics, and righteous ones help explain why the Church chose these readings for this day.

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

The Synaxarium gives the commemorations of the day. It does not always say, "this reading belongs to this saint." The link between commemoration and reading must therefore be stored with a basis:

- explicit, when a source directly states the reading,
- collection-type, when the commemoration type matches the known reading family,
- inferred, when the link is reasoned and lower confidence.

This matters because some days have multiple commemorations. A martyr, a patriarch, and a feast may share the same day. The ranking commemoration may govern the public daily reading, while a secondary commemoration may have proper readings only in another source.

A faithful database should say what it knows and how it knows it.

## Spiritual fruit

The lectionary teaches obedience. We receive what the Church gives, even when another passage might feel more immediately interesting.

It teaches memory. The saints are not examples from the past only. They are part of the Church's living worship.

It teaches repentance. The same passage returns in different seasons and exposes a different wound in us.

It teaches Christ. Every reading, feast, fast, Psalm, prophecy, Gospel, and commemoration finds its center in Him.

## Lesson Guide

### Opening question
Ask: When you hear a church reading, do you receive it as information, or as the Church interpreting this day for you?

### Main movement
1. Begin with Christ reading Isaiah in Luke 4.
2. Explain the four lectionary books.
3. Show how fixed dates and movable Pascha shape the year.
4. Explain Sundays, feasts, and the Synaxarium.
5. Show why a reverse lectionary helps Bible study.
6. End with spiritual obedience and repentance.

### Key sentence
The lectionary is the Church teaching us how to hear Scripture with Christ at the center.

## Teacher's Notes

- Emphasize: The Synaxarium is not an appendix. It is part of how the daily cycle is understood.
- Watch for: Do not imply every Synaxarium entry has an explicit reading assignment. Many bridges are reasoned from commemoration type and day ranking.
- Clarify: Psalm numbering differences are not errors by themselves. They may reflect Masoretic and Septuagint traditions.
- Connect: The readings should lead to worship, repentance, and union with Christ, not only to data accuracy.

## Discussion Questions

1. How does hearing Scripture inside the liturgy change the way we receive it?
2. Why does it matter that the daily readings follow the Synaxarium?
3. How can Psalm numbering differences create false conflicts if we do not track the source convention?
4. What can a reverse lectionary teach that a normal daily-reading page cannot?
5. Which reading has changed for you because of where the Church places it?

## Sources

### Primary and Coptic Orthodox sources

- Coptic Reader app, Pascha Wednesday Day screenshots supplied by George, used as current-practice authority for that fixture scope.
- St-Takla English Coptic Synaxarium day pages, used as a source map for daily commemorations.
- copticchurch.net daily readings pages, used as a public date-resolved reading source.

### Scholarly and structural sources

- Coptic Encyclopedia, "Lectionary," Claremont Colleges Digital Library, https://ccdl.claremont.edu/digital/api/collection/cce/id/1199/download.
- Fouad Naguib Youssef, "The Arrangement of the Church Lectionary," ACCOT, https://accot.stcyrils.edu.au/fny-read1/.
- Ugo Zanetti, Les lectionnaires coptes annuels, Basse-Egypte, Publications de l'Institut orientaliste de Louvain.

### Patristic anchor

- Saint Athanasius of Alexandria, Festal Letter 39, on the Scriptures as fountains of salvation.

## Glossary

- Katameros: A Coptic lectionary book or collection of appointed readings.
- Synaxarium: The Church's daily-cycle book or index of commemorations of saints, martyrs, feasts, and events.
- Pascha: Holy Week, centered on the saving Passion of Christ.
- Holy Fifty Days: The joyful season from the Resurrection to Pentecost.
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
- `attestation_bucket`: `current_confirmed`, `consensus_without_coptic_reader`, `old_edition_only`, `old_edition_only_candidate_removed`, `single_source_candidate`.
- `service_day`, `service_hour`, and `service_section`: source labels are preserved when the source's service structure does not fit a normalized value.
- `slot`: normalized Scripture and liturgical slots plus `source_label_preserved`.
- Psalm `mapping_scope`: `chapter_equivalence`, `split_merge_chapter_seam`, `lxx_unique_chapter`, `anchored_verse_example`, `unresolved_verse_offset_example`.
- Synaxarium `type`: `lord_feast`, `theotokos`, `martyr`, `apostle`, `patriarch`, `hierarch`, `departure`, `prophet`, `angel`, `ascetic`, `feast`, `commemoration`.
- bridge `basis`: `explicit`, `collection-type`, `inferred`.
- bridge `confidence`: `high`, `medium`, `low`.

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
- `reading_identity_key`
- `slot`
- `basis`
- `confidence`
- `citation`

The bridge uses `collection-type` basis for primary day commemorations linked to fixed-day Katameros readings. Multi-commemoration days are confidence `medium` and are listed for review in the open questions file.

## Controlled vocabularies

See `out/design/lectionary_schema.json` for machine-readable vocabularies. The 69 collection count is source-confirmed through F.N. Youssef, but the accessible sources in this run did not expose a fully enumerated English list. The spec therefore stores a working type list and records the full list as a source gap rather than inventing it.

## Site-facing outputs

- `out/design/reverse_lectionary_presentation.csv`
- `out/design/reverse_lectionary_presentation.jsonl`
- `out/design/todays_readings_current_practice.csv`
- `out/design/passage_liturgical_footprint.csv`
- `out/design/pascha_attestation.csv`
- `out/design/temporal_classification.csv`
- `out/design/synaxarium_commemorations.csv`
- `out/design/synaxarium_reading_bridge.csv`
- `site_integration_spec.md`

## Acceptance notes

- Structural claims in the article cite named sources.
- Inferences are flagged.
- The schema is complete enough to drive the additive design-layer outputs.
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
- `out/design/reverse_lectionary_presentation.csv`
- `out/design/reverse_lectionary_presentation.jsonl`
- `out/design/todays_readings_current_practice.csv`
- `out/design/passage_liturgical_footprint.csv`
- `out/design/pascha_attestation.csv`
- `out/design/temporal_classification.csv`
- `out/design/synaxarium_commemorations.csv`
- `out/design/synaxarium_reading_bridge.csv`
- `out/design/source_registry.csv`
- `out/design/psalm_mt_lxx_crosswalk.csv`

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
- show Synaxarium bridge rows only with their `basis` and `confidence`.

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
    psalm_pending = [r for r in temporal_residue if r.get("residue_type") == "psalm_equivalence_unresolved"]
    current_pending = [r for r in temporal_residue if r.get("residue_type") == "current_authority_pending"]
    text = """# Open Questions and Decisions for George

This file collects only the questions that thorough research, source comparison, and independent audit could not settle during the autonomous lectionary execution run.

## Psalm numbering text-equivalence review

The active execution brief states that the Coptic Reader Wednesday Day fixture is faithful to the screenshots, including Third Hour `Psalm 41` and Sixth Hour `Psalm 83`, and that Coptic Reader governs where external books disagree. During Phase 1, Brenton/KJV seam checks resolved several exact pairs: LXX `Ps 41:6` to MT `Ps 42:5`, LXX `Ps 83:2` to MT `Ps 84:1`, and LXX `Ps 83:5` to MT `Ps 84:4`.

Decision needed later: before presenting Third Hour `Psalm 41:1` as an exact MT-primary reference, compare the fixture Psalm text against Brenton and a public-domain MT text. Until then, the design layer preserves the Coptic Reader LXX label and marks the exact MT equivalence as unresolved.

## Full list of F.N. Youssef's 69 collections

The accessible source confirms the lectionary is arranged into 69 collections by feast or commemoration type, but the full English enumerated list was not available in the source text retrieved in this run. The schema stores the confirmed count and a working type vocabulary. The full list should be entered when a reliable source is available.

## Coptic Reader coverage beyond Wednesday Day

The repo has a locked Coptic Reader fixture for Pascha Wednesday Day only. Current-vs-historical classifications outside that fixture are marked as candidates unless supported by other current sources. Do not treat them as fully Coptic Reader confirmed.

## Pascha removed-reading candidates

Rows absent from the Wednesday Day Coptic Reader fixture but present in older or local Pascha data are classified as `historical_candidate_removed` in `out/design/temporal_classification.csv`. George or a liturgical reviewer should decide whether each is truly removed, a named-reading equivalent, or a fixture scope issue.
"""
    text += "\n## Temporal residue summary\n\n"
    text += "See `out/design/temporal_residue.csv` and `out/design/temporal_residue_manifest.csv` for the full row-level list and counts. Counts by residue type:\n"
    for residue_type, count in sorted(residue_counts.items()):
        text += f"- `{residue_type}`: {count}\n"
    text += "- `true_source_disagreement`: 0\n"
    text += "\nNo true source-disagreement class was emitted in this run. Unsettled rows are classified as pending authority, historical witness without current comparator, candidate removed, or Psalm-equivalence unresolved.\n"
    text += "\n### Candidate removed readings needing current-authority confirmation\n\n"
    for row in candidate_removed:
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

The bridge links the primary commemoration of each fixed Coptic day to that day's Katameros readings with basis `collection-type`. Multi-commemoration days are confidence `medium`, because secondary commemorations may have proper readings only in sources not ingested here.

- Multi-commemoration days needing future ecclesiastical or source review: """ + str(len(ambiguous)) + " days.\n"
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
    today_rows = build_today_rows(presentation_rows)
    footprint = build_footprint(presentation_rows)

    presentation_fields = [
        "identity_key", "reading_type", "reading_name", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_convention", "canonicalization_confidence", "canonicalization_note", "spans_json", "current_status", "status_note", "source_key", "source_kind", "source_family", "source_file", "source_row_id", "authority_tier", "occasion", "calendar_key", "gregorian_date", "coptic_date", "day_title", "service_day", "service_hour", "service_section", "reading_slot", "slot", "order", "hour_theme", "source_ref", "raw_ref", "url", "provenance",
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
    write_csv(OUT / "pascha_attestation.csv", attestation, ["day_title", "service_hour", "identity_key", "display_ref", "source_count", "sources", "bucket", "statuses", "citation", "attestation_note"])
    write_jsonl(OUT / "pascha_attestation.jsonl", attestation)
    write_csv(OUT / "pascha_attestation_bucket_manifest.csv", attestation_bucket_manifest, ["bucket", "row_count", "present_in_phase3", "note"])
    write_jsonl(OUT / "pascha_attestation_bucket_manifest.jsonl", attestation_bucket_manifest)
    write_csv(OUT / "temporal_classification.csv", temporal, ["day_title", "service_hour", "identity_key", "display_ref", "lifecycle_status", "current_status", "source_authority_tier", "attestation_bucket", "current_authority", "valid_from", "valid_to", "derivation", "attesting_sources"])
    write_jsonl(OUT / "temporal_classification.jsonl", temporal)
    temporal_residue_fields = ["day_title", "service_hour", "identity_key", "display_ref", "lifecycle_status", "attestation_bucket", "current_status", "current_authority", "residue_type", "reason", "citation", "attestation_note"]
    write_csv(OUT / "temporal_residue.csv", temporal_residue, temporal_residue_fields)
    write_jsonl(OUT / "temporal_residue.jsonl", temporal_residue)
    write_csv(OUT / "temporal_residue_manifest.csv", temporal_residue_manifest, ["residue_type", "row_count", "present_in_phase4", "note"])
    write_jsonl(OUT / "temporal_residue_manifest.jsonl", temporal_residue_manifest)
    write_csv(OUT / "synaxarium_commemorations.csv", commems, ["commem_id", "coptic_month", "coptic_day", "coptic_day_key", "rank", "title", "type", "source", "source_url", "source_day_title", "source_summary"])
    write_jsonl(OUT / "synaxarium_commemorations.jsonl", commems)
    write_csv(OUT / "synaxarium_reading_bridge.csv", bridge, ["commem_id", "coptic_day_key", "commemoration_title", "commemoration_type", "reading_identity_key", "display_ref", "slot", "basis", "confidence", "citation", "note"])
    write_jsonl(OUT / "synaxarium_reading_bridge.jsonl", bridge)
    write_csv(OUT / "passage_liturgical_footprint.csv", footprint, ["identity_key", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "total_occurrences", "current_occurrences", "historical_occurrences", "source_kinds", "sample_liturgical_places", "hour_themes", "patristic_homily_slug", "chapter_study_slug", "audio_slug", "site_note"])
    write_jsonl(OUT / "passage_liturgical_footprint.jsonl", footprint)
    write_csv(OUT / "source_registry.csv", SOURCE_REGISTRY, ["source_key", "title", "url", "authority_tier", "confidence", "notes"])
    write_jsonl(OUT / "source_registry.jsonl", SOURCE_REGISTRY)

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
    }
    write_site_integration_spec(summary)
    update_open_questions(commems, bridge, temporal_residue)
    (OUT / "BUILD_DESIGN_SUMMARY.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
