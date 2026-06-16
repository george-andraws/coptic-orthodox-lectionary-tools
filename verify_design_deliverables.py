#!/usr/bin/env python3
"""Verify additive Coptic lectionary design-layer deliverables."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out" / "design"
BRENTON = Path("/Users/georgeandraws/workspace/extract_brenton.py")

FORBIDDEN_WORDS = ["delve", "multifaceted", "additionally", "landscape", "underscore", "foster", "interplay"]
TEXT_FILES = [
    ROOT / "coptic-lectionary-and-synaxarium.md",
    ROOT / "lectionary_spec.md",
    ROOT / "site_integration_spec.md",
    ROOT / "audit_artifacts" / "open_questions_for_george.md",
]
REQUIRED_SCHEMA_VOCABS = [
    "season",
    "occasion",
    "occasion_type",
    "source_authority_tier",
    "source_convention",
    "canonicalization_confidence",
    "current_status",
    "attestation_bucket",
    "service_day",
    "service_hour",
    "service_section",
    "slot",
    "synaxarium_type",
    "bridge_basis",
    "bridge_confidence",
    "psalm_mapping_scope",
    "current_authority",
]
SEAM_PAIRS = [
    ("Ps", 50, 6, "Psalm 51:4", ["sinned", "justified"]),
    ("Ps", 32, 10, "Psalm 33:10", ["counsel", "nought"]),
    ("Ps", 41, 6, "Psalm 42:5", ["soul", "hope", "God"]),
    ("Ps", 83, 2, "Psalm 84:1", ["amiable", "tabernacles"]),
    ("Ps", 83, 5, "Psalm 84:4", ["dwell", "house"]),
    ("Ps", 40, 6, "Psalm 41:5", ["enemies", "evil"]),
    ("Ps", 6, 2, "Psalm 6:1", ["rebuke", "anger"]),
    ("Ps", 68, 17, "Psalm 69:16", ["hear", "multitude"]),
]


def fail(message: str) -> None:
    raise AssertionError(message)


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def norm(text: str) -> str:
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def verify_content_rules() -> None:
    for path in TEXT_FILES:
        text = path.read_text(encoding="utf-8")
        if "—" in text:
            fail(f"Em dash found in {path}")
        bad = [w for w in FORBIDDEN_WORDS if re.search(rf"\b{re.escape(w)}\b", text, re.I)]
        if bad:
            fail(f"Forbidden words in {path}: {bad}")
    article = (ROOT / "coptic-lectionary-and-synaxarium.md").read_text(encoding="utf-8")
    if "John Chrysostom" in article:
        fail("Article still contains uncited John Chrysostom reference")
    if "serve the congregation" in article.lower():
        fail("Article repeats rejected deacon-service phrasing")
    if "helpless" in article.lower():
        fail("Article uses forbidden Passion language")


def verify_schema() -> None:
    schema = json.loads((OUT / "lectionary_schema.json").read_text(encoding="utf-8"))
    vocabs = schema.get("controlled_vocabularies", {})
    missing = [k for k in REQUIRED_SCHEMA_VOCABS if not vocabs.get(k)]
    if missing:
        fail(f"Missing schema vocabularies: {missing}")
    if vocabs["collection_types_69"].get("confirmed_count") != 69:
        fail("69 collection count not preserved")
    if vocabs["collection_types_69"].get("status") != "source_confirmed_count_not_fully_enumerated":
        fail("69 collection status should remain source-confirmed but not enumerated")
    tables = schema.get("tables", {})
    table_requirements = {
        "reading_identity": ["reading_type", "reading_name", "source_label", "spans_json"],
        "temporal_attestation": ["source_authority_tier", "attestation_bucket", "current_authority"],
        "temporal_classification": ["day_title", "service_hour", "display_ref", "lifecycle_status", "current_status", "source_authority_tier", "attestation_bucket", "current_authority", "derivation", "attesting_sources"],
        "psalm_mt_lxx_crosswalk": ["map_direction", "mapping_scope", "validation_basis"],
    }
    for table, fields in table_requirements.items():
        missing_fields = [field for field in fields if field not in tables.get(table, [])]
        if missing_fields:
            fail(f"Schema table {table} missing fields: {missing_fields}")


def verify_rows() -> None:
    summary = json.loads((OUT / "BUILD_DESIGN_SUMMARY.json").read_text(encoding="utf-8"))
    schema = json.loads((OUT / "lectionary_schema.json").read_text(encoding="utf-8"))
    files = {
        "reverse_lectionary_presentation_rows": OUT / "reverse_lectionary_presentation.csv",
        "reading_identity_rows": OUT / "reading_identity.csv",
        "todays_readings_rows": OUT / "todays_readings_current_practice.csv",
        "psalm_crosswalk_rows": OUT / "psalm_mt_lxx_crosswalk.csv",
        "pascha_attestation_rows": OUT / "pascha_attestation.csv",
        "temporal_classification_rows": OUT / "temporal_classification.csv",
        "synaxarium_commemoration_rows": OUT / "synaxarium_commemorations.csv",
        "synaxarium_bridge_rows": OUT / "synaxarium_reading_bridge.csv",
        "passage_footprint_rows": OUT / "passage_liturgical_footprint.csv",
    }
    for key, path in files.items():
        rows = read_csv(path)
        if len(rows) != summary[key]:
            fail(f"{path} row count {len(rows)} != summary {summary[key]}")
        if not rows:
            fail(f"{path} has no rows")
    presentation = read_csv(OUT / "reverse_lectionary_presentation.csv")
    crosswalk = read_csv(OUT / "psalm_mt_lxx_crosswalk.csv")
    scopes = {r.get("mapping_scope") for r in crosswalk}
    required_scopes = {"chapter_equivalence", "split_merge_chapter_seam", "lxx_unique_chapter", "anchored_verse_example", "unresolved_verse_offset_example"}
    if not required_scopes.issubset(scopes):
        fail(f"Crosswalk missing mapping scopes: {sorted(required_scopes - scopes)}")
    temporal = read_csv(OUT / "temporal_classification.csv")
    allowed_current_authority = set(schema.get("controlled_vocabularies", {}).get("current_authority", []))
    for field in ["source_authority_tier", "attestation_bucket", "current_authority", "current_status"]:
        if any(field not in row for row in temporal[:10]):
            fail(f"Temporal classification missing field {field}")
    unknown_authority = sorted({row.get("current_authority", "") for row in temporal if row.get("current_authority", "") not in allowed_current_authority})
    if unknown_authority:
        fail(f"Temporal classification current_authority outside schema vocabulary: {unknown_authority}")
    required = ["identity_key", "reading_type", "reading_name", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_convention", "source_key", "current_status", "authority_tier", "spans_json"]
    allowed_statuses = set(schema.get("controlled_vocabularies", {}).get("current_status", []))
    allowed_authority_tiers = set(schema.get("controlled_vocabularies", {}).get("source_authority_tier", []))
    allowed_source_conventions = set(schema.get("controlled_vocabularies", {}).get("source_convention", []))
    for field in required:
        if any(field not in row for row in presentation[:10]):
            fail(f"Missing presentation field {field}")
    unknown_statuses = sorted({row.get("current_status", "") for row in presentation if row.get("current_status", "") not in allowed_statuses})
    if unknown_statuses:
        fail(f"Presentation current_status outside schema vocabulary: {unknown_statuses}")
    unknown_tiers = sorted({row.get("authority_tier", "") for row in presentation if row.get("authority_tier", "") not in allowed_authority_tiers})
    if unknown_tiers:
        fail(f"Presentation authority_tier outside schema vocabulary: {unknown_tiers}")
    unknown_source_conventions = sorted({row.get("source_convention", "") for row in presentation if row.get("source_convention", "") not in allowed_source_conventions})
    if unknown_source_conventions:
        fail(f"Presentation source_convention outside schema vocabulary: {unknown_source_conventions}")
    blank_source_conventions = sum(1 for row in presentation if not row.get("source_convention"))
    if blank_source_conventions:
        fail(f"Presentation rows with blank source_convention: {blank_source_conventions}")
    registry = read_csv(OUT / "source_registry.csv")
    registered_source_keys = {row.get("source_key", "") for row in registry}
    emitted_source_keys = {row.get("source_key", "") for row in presentation}
    unregistered_source_keys = sorted(emitted_source_keys - registered_source_keys)
    if unregistered_source_keys:
        fail(f"Presentation emits unregistered source keys: {unregistered_source_keys}")
    registry_bad = sorted({row.get("authority_tier", "") for row in registry if row.get("authority_tier", "") not in allowed_authority_tiers})
    if registry_bad:
        fail(f"Source registry authority_tier outside schema vocabulary: {registry_bad}")
    fixture_rows = [r for r in presentation if r.get("source_kind") == "coptic_reader_fixture"]
    if len(fixture_rows) != 26:
        fail(f"Expected 26 Coptic Reader fixture rows, found {len(fixture_rows)}")
    named = [r for r in fixture_rows if r.get("reading_type") == "named-reading"]
    if not any(r.get("reading_name") == "Memoirs of Job" for r in named):
        fail("Named reading Memoirs of Job is not first-class in fixture rows")
    for row in fixture_rows:
        if row.get("reading_type") == "scripture":
            spans = json.loads(row.get("spans_json") or "[]")
            if not spans:
                fail(f"Scripture fixture row missing spans_json: {row.get('source_ref')}")
            for span in spans:
                for key in ["source_ref", "source_convention", "canonical_mt_ref", "canonical_lxx_ref", "confidence", "validation_basis", "book", "chapter_start", "verse_start", "chapter_end", "verse_end"]:
                    if key not in span:
                        fail(f"Span missing {key} for {row.get('source_ref')}")
    by_lxx = {r.get("canonical_lxx_ref"): r for r in fixture_rows if r.get("canonical_lxx_ref")}
    expected = {"Ps 50:6": "Ps 51:4", "Ps 32:10": "Ps 33:10", "Ps 41:6": "Ps 42:5", "Ps 83:2": "Ps 84:1", "Ps 83:5": "Ps 84:4", "Ps 40:6-8": "Ps 41:5-7", "Ps 6:2-3": "Ps 6:1-2", "Ps 68:17": "Ps 69:16"}
    for lxx, mt in expected.items():
        if lxx not in by_lxx:
            fail(f"Missing fixture LXX ref {lxx}")
        if by_lxx[lxx].get("canonical_mt_ref") != mt:
            fail(f"Fixture {lxx} expected MT {mt}, got {by_lxx[lxx].get('canonical_mt_ref')}")
    if "Ps 41:1" not in by_lxx:
        fail("Missing unresolved fixture LXX ref Ps 41:1")
    if by_lxx["Ps 41:1"].get("canonical_mt_ref"):
        fail("Fixture Ps 41:1 should remain MT-equivalence pending")
    if "MT equivalent pending" not in by_lxx["Ps 41:1"].get("display_ref", ""):
        fail("Fixture Ps 41:1 display should state MT equivalent pending")


def fetch_kjv(ref: str) -> str:
    url = "https://bible-api.com/" + urllib.parse.quote(ref) + "?translation=kjv"
    with urllib.request.urlopen(url, timeout=15) as fh:
        data = json.load(fh)
    return data.get("text", "")


def brenton(book: str, chapter: int, verse: int) -> str:
    if not BRENTON.exists():
        fail(f"Brenton helper missing: {BRENTON}")
    return subprocess.check_output([sys.executable, str(BRENTON), book, str(chapter), str(verse), str(verse)], text=True).strip()


def verify_psalm_seams() -> None:
    crosswalk = read_csv(OUT / "psalm_mt_lxx_crosswalk.csv")
    for book, lxx_chapter, lxx_verse, kjv_ref, keywords in SEAM_PAIRS:
        lxx_text = norm(brenton(book, lxx_chapter, lxx_verse))
        kjv_text = norm(fetch_kjv(kjv_ref))
        missing = [kw for kw in keywords if kw.lower() not in lxx_text or kw.lower() not in kjv_text]
        if missing:
            fail(f"Psalm seam {book} {lxx_chapter}:{lxx_verse} vs {kjv_ref} missing shared keywords {missing}")
        lxx_ref = f"Ps {lxx_chapter}:{lxx_verse}"
        mt_ref = kjv_ref.replace("Psalm", "Ps")
        if not any((r.get("lxx_psalm") == lxx_ref and r.get("mt_psalm") == mt_ref) or (r.get("lxx_psalm", "").startswith(lxx_ref) and r.get("mt_psalm", "").startswith(mt_ref)) for r in crosswalk):
            fail(f"Crosswalk missing example row {lxx_ref} -> {kjv_ref}")
    if not any(r.get("lxx_psalm") == "151" and r.get("mt_psalm") == "none" for r in crosswalk):
        fail("Crosswalk missing LXX Psalm 151 row")


def main() -> None:
    verify_content_rules()
    verify_schema()
    verify_rows()
    verify_psalm_seams()
    print("design deliverables verified")


if __name__ == "__main__":
    main()
