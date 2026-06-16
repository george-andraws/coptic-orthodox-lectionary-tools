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
        "temporal_residue": ["residue_type", "reason", "citation", "attestation_note"],
        "temporal_residue_manifest": ["residue_type", "row_count", "present_in_phase4", "note"],
        "psalm_mt_lxx_crosswalk": ["map_direction", "mapping_scope", "validation_basis"],
        "pascha_attestation_bucket_manifest": ["bucket", "row_count", "present_in_phase3", "note"],
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
        "pascha_attestation_bucket_manifest_rows": OUT / "pascha_attestation_bucket_manifest.csv",
        "temporal_classification_rows": OUT / "temporal_classification.csv",
        "temporal_residue_rows": OUT / "temporal_residue.csv",
        "temporal_residue_manifest_rows": OUT / "temporal_residue_manifest.csv",
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
    attestation = read_csv(OUT / "pascha_attestation.csv")
    attestation_manifest = read_csv(OUT / "pascha_attestation_bucket_manifest.csv")
    temporal_residue = read_csv(OUT / "temporal_residue.csv")
    temporal_residue_manifest = read_csv(OUT / "temporal_residue_manifest.csv")
    allowed_current_authority = set(schema.get("controlled_vocabularies", {}).get("current_authority", []))
    for field in ["source_authority_tier", "attestation_bucket", "current_authority", "current_status"]:
        if any(field not in row for row in temporal[:10]):
            fail(f"Temporal classification missing field {field}")
    unknown_authority = sorted({row.get("current_authority", "") for row in temporal if row.get("current_authority", "") not in allowed_current_authority})
    if unknown_authority:
        fail(f"Temporal classification current_authority outside schema vocabulary: {unknown_authority}")
    non_current_temporal = [row for row in temporal if row.get("lifecycle_status") != "current"]
    if len(temporal_residue) != len(non_current_temporal):
        fail(f"Temporal residue row count {len(temporal_residue)} != non-current temporal rows {len(non_current_temporal)}")
    if any(not row.get("residue_type") or not row.get("reason") for row in temporal_residue):
        fail("Temporal residue row missing residue_type or reason")
    residue_types = {row.get("residue_type", "") for row in temporal_residue}
    required_residue_types = {"current_authority_pending", "historical_witness_no_current_comparator", "candidate_removed_needs_current_authority_confirmation", "psalm_equivalence_unresolved"}
    if not required_residue_types.issubset(residue_types):
        fail(f"Temporal residue missing required types: {sorted(required_residue_types - residue_types)}")
    unresolved_temporal = [row for row in temporal if "pending_psalm_equivalence_unresolved" in row.get("current_status", "")]
    unresolved_residue = [row for row in temporal_residue if row.get("residue_type") == "psalm_equivalence_unresolved"]
    if len(unresolved_temporal) != len(unresolved_residue):
        fail(f"Temporal unresolved Psalm residue count {len(unresolved_residue)} != temporal unresolved count {len(unresolved_temporal)}")
    residue_manifest_counts = {row.get("residue_type", ""): int(row.get("row_count", "0") or 0) for row in temporal_residue_manifest}
    for residue_type in required_residue_types:
        actual = sum(1 for row in temporal_residue if row.get("residue_type") == residue_type)
        if residue_manifest_counts.get(residue_type) != actual:
            fail(f"Temporal residue manifest count mismatch for {residue_type}: {residue_manifest_counts.get(residue_type)} != {actual}")
    if residue_manifest_counts.get("true_source_disagreement") != 0:
        fail("Temporal residue manifest should state zero true_source_disagreement rows for this run")
    if any(row.get("current_authority") == "not Coptic Reader confirmed" for row in temporal):
        fail("Temporal classification still uses overbroad current_authority wording")
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
    allowed_buckets = set(schema.get("controlled_vocabularies", {}).get("attestation_bucket", []))
    attestation_buckets = {row.get("bucket", "") for row in attestation}
    unknown_buckets = sorted(attestation_buckets - allowed_buckets)
    if unknown_buckets:
        fail(f"Pascha attestation buckets outside schema vocabulary: {unknown_buckets}")
    manifest_buckets = {row.get("bucket", "") for row in attestation_manifest}
    if manifest_buckets != allowed_buckets:
        fail(f"Attestation bucket manifest does not match schema vocabulary: missing={sorted(allowed_buckets - manifest_buckets)} extra={sorted(manifest_buckets - allowed_buckets)}")
    manifest_counts = {row.get("bucket", ""): int(row.get("row_count", "0") or 0) for row in attestation_manifest}
    actual_bucket_counts = {bucket: sum(1 for row in attestation if row.get("bucket") == bucket) for bucket in allowed_buckets}
    if manifest_counts != actual_bucket_counts:
        fail(f"Attestation bucket manifest counts do not match actual counts: manifest={manifest_counts} actual={actual_bucket_counts}")
    if manifest_counts.get("consensus_without_coptic_reader") != 0:
        fail("Phase 3 expected explicit zero-count consensus_without_coptic_reader bucket")
    if any(not row.get("attestation_note") for row in attestation):
        fail("Pascha attestation row missing attestation_note")
    bare_api = [row for row in attestation if row.get("citation", "").strip() == "api" or "; api" in row.get("citation", "")]
    if bare_api:
        fail(f"Pascha attestation rows with bare api citation: {len(bare_api)}")
    weak_citations = [row for row in attestation if "source_file=" not in row.get("citation", "") or "source_row_id=" not in row.get("citation", "")]
    if weak_citations:
        fail(f"Pascha attestation rows missing replayable source_file/source_row_id citation: {len(weak_citations)}")
    pascha_source_kinds = {"pascha_day_hour", "pascha_source_text", "coptic_reader_fixture"}
    expected_attestation_keys = {
        (row.get("day_title", ""), row.get("service_hour") or row.get("service_section", ""), row.get("identity_key", ""))
        for row in presentation
        if row.get("source_kind") in pascha_source_kinds
    }
    actual_attestation_keys = {
        (row.get("day_title", ""), row.get("service_hour", ""), row.get("identity_key", ""))
        for row in attestation
    }
    missing_attestation = expected_attestation_keys - actual_attestation_keys
    if missing_attestation:
        fail(f"Pascha source placements missing attestation groups: {len(missing_attestation)}")
    fixture_placement_keys = {
        (row.get("day_title", ""), row.get("service_hour") or row.get("service_section", ""), row.get("identity_key", ""))
        for row in presentation
        if row.get("source_kind") == "coptic_reader_fixture"
    }
    fixture_identity_keys = {key[2] for key in fixture_placement_keys}
    fixture_attestation_bad = [
        row for row in attestation
        if (row.get("day_title", ""), row.get("service_hour", ""), row.get("identity_key", "")) in fixture_placement_keys
        and row.get("bucket") != "current_confirmed"
    ]
    if fixture_attestation_bad:
        fail(f"Coptic Reader fixture placements not current_confirmed: {len(fixture_attestation_bad)}")
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
