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
from collections import Counter, defaultdict
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
    "slot_type",
    "occasion_kind",
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
    "collection_types_69",
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


def read_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def norm(text: str) -> str:
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def occasion_index_key(row: dict) -> tuple[str, str, str, str, str]:
    return (
        row.get("occasion", ""),
        row.get("service_section", ""),
        row.get("service_hour", ""),
        row.get("slot", ""),
        row.get("identity_key", ""),
    )


def ordered_unique(values) -> list[str]:
    seen = set()
    out = []
    for value in values:
        value = str(value or "").strip()
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def join_unique(values) -> str:
    return " || ".join(ordered_unique(values))


def gregorian_year(value: str) -> int | None:
    value = str(value or "").strip()
    if not value:
        return None
    try:
        return int(value[:4])
    except ValueError:
        return None


def years_are_contiguous(years) -> bool:
    year_list = sorted(set(years))
    if len(year_list) < 2:
        return True
    return year_list == list(range(year_list[0], year_list[-1] + 1))


def source_disclosure_key(row: dict) -> tuple[str, str, str, str]:
    return (
        row.get("source_family", ""),
        row.get("source_kind", ""),
        row.get("source_edition", ""),
        row.get("source_title", ""),
    )


def expected_source_disclosure(source_rows: list[dict]) -> tuple[list[dict], list[str]]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for source_row in source_rows:
        grouped[source_disclosure_key(source_row)].append(source_row)
    disclosure = []
    locators = []
    for key, rows in sorted(grouped.items(), key=lambda item: item[0]):
        family, kind, edition, title = key
        item = {
            "source_family": family,
            "source_kind": kind,
            "source_edition": edition,
            "source_title": title,
        }
        row_locators = ordered_unique(row.get("source_locator", "") for row in rows)
        if row_locators:
            item["source_locator"] = row_locators[0]
            locators.append(row_locators[0])
        years = sorted(year for year in (gregorian_year(row.get("gregorian_date", "")) for row in rows) if year is not None)
        if years:
            item["attested_year_min"] = str(min(years))
            item["attested_year_max"] = str(max(years))
            if not years_are_contiguous(years):
                item["attested_years"] = "; ".join(str(year) for year in sorted(set(years)))
        disclosure.append({field: value for field, value in item.items() if value})
    return disclosure, locators


def verify_content_rules() -> None:
    for path in TEXT_FILES:
        text = path.read_text(encoding="utf-8")
        if "—" in text:
            fail(f"Em dash found in {path}")
        bad = [w for w in FORBIDDEN_WORDS if re.search(rf"\b{re.escape(w)}\b", text, re.I)]
        if bad:
            fail(f"Forbidden words in {path}: {bad}")
    article = (ROOT / "coptic-lectionary-and-synaxarium.md").read_text(encoding="utf-8")
    if "publish: true" not in article.split("---", 2)[1]:
        fail("Article frontmatter must be publish: true after George's approval")
    if "> **DRAFT, pending deacon review.**" in article:
        fail("Article must not show the draft pending deacon review note after publish approval")
    if "## Notes" not in article:
        fail("Article must include endnotes for source trailers")
    article_body_before_sources = article.split("\n## Sources\n", 1)[0]
    if re.search(r"\s+Sources?:\s+", article_body_before_sources):
        fail("Article body still has inline Source/Sources trailers")
    if "Read from source:" in article_body_before_sources:
        fail("Article body still has templated Read from source transition")
    if "John Chrysostom" in article:
        fail("Article still contains uncited John Chrysostom reference")
    if "## Teaching guide" not in article:
        fail("Article must use Teaching guide heading")
    if "Lesson Guide" in article:
        fail("Article must not use Lesson Guide wording")
    if "Scripture references follow NKJV versification." not in article:
        fail("Reader-facing Scripture source wording must be exactly: Scripture references follow NKJV versification.")
    if "Scripture is from NKJV." in article:
        fail("Article must not claim NKJV verse text is reproduced when only versification is used")
    reader_facing_policy_terms = ["permission", "permissions", "rights", "source-policy", "source policy"]
    policy_hits = [term for term in reader_facing_policy_terms if re.search(rf"\b{re.escape(term)}\b", article, re.I)]
    if policy_hits:
        fail(f"Reader-facing article contains internal permission/source-policy terms: {policy_hits}")
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
    collection_69 = vocabs["collection_types_69"]
    if collection_69.get("confirmed_count") != 69:
        fail("69 collection count not preserved")
    if collection_69.get("status") != "inferred_likely_same_set_roster_unverified":
        fail("69 collection status should record the roster-unverified inferred verdict")
    if collection_69.get("verdict_token") != "INFERRED_LIKELY_SAME_SET":
        fail("69 collection verdict token should record inferred likely same set")
    if collection_69.get("membership_confirmation") != "inferred_likely_same_set_roster_unverified":
        fail("69 collection membership caveat missing")
    if len(collection_69.get("entries", [])) != 69:
        fail("69 collection schema entries not enumerated")
    if collection_69.get("provenance", {}).get("ottawa_edition") != "first edition, Christmas 1714 A.M., 1998 A.D.":
        fail("69 collection provenance missing Ottawa edition")
    tables = schema.get("tables", {})
    table_requirements = {
        "reading_identity": ["reading_type", "reading_name", "source_label", "spans_json"],
        "reverse_lectionary_index": ["occasion", "calendar_keys", "day_titles", "service_section", "service_hour", "slot", "slot_type", "slot_order", "occasion_kind", "identity_key", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "spans_json", "removed_marker", "hour_theme", "reading_type", "reading_name", "authority_tier", "current_status", "provenance", "source_family", "source_kind", "source_edition", "source_locator", "source_title", "source_disclosure_count", "source_disclosure", "attestation_year_min", "attestation_year_max"],
        "daily_lectionary_year": ["occasion", "service_section", "service_hour", "slot", "display_ref", "identity_key", "reading_type", "removed_marker"],
        "temporal_attestation": ["source_authority_tier", "source_title", "source_edition", "source_locator", "attestation_bucket", "current_authority", "removed_marker"],
        "temporal_classification": ["day_title", "service_hour", "display_ref", "lifecycle_status", "current_status", "removed_marker", "source_authority_tier", "source_titles", "source_editions", "source_locators", "attestation_bucket", "current_authority", "derivation", "attesting_sources"],
        "temporal_residue": ["residue_type", "reason", "removed_marker", "citation", "attestation_note"],
        "temporal_residue_manifest": ["residue_type", "row_count", "present_in_phase4", "note"],
        "synaxarium_commemoration": ["extraction_method", "caveat", "source_summary"],
        "psalm_mt_lxx_crosswalk": ["map_direction", "mapping_scope", "validation_basis"],
        "pascha_attestation_bucket_manifest": ["bucket", "row_count", "present_in_phase3", "note"],
        "source_registry": ["source_key", "title", "edition", "default_locator"],
        "passage_source_disclosure": ["identity_key", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_key", "source_title", "source_edition", "source_locator", "day_title", "service_hour", "citation"],
        "foundational_reading_collection": ["collection_key", "coptic_day_key", "reading_section_start_page", "membership_status", "membership_verdict", "source_locator"],
        "synaxarium_reading_bridge": ["commem_id", "coptic_day_key", "commemoration_title", "commemoration_type", "reading_identity_key", "display_ref", "slot", "basis", "confidence", "citation", "note"],
    }
    for table, fields in table_requirements.items():
        missing_fields = [field for field in fields if field not in tables.get(table, [])]
        if missing_fields:
            fail(f"Schema table {table} missing fields: {missing_fields}")
    csv_contracts = {
        "reading_identity": OUT / "reading_identity.csv",
        "reverse_lectionary_presentation": OUT / "reverse_lectionary_presentation.csv",
        "todays_readings_current_practice": OUT / "todays_readings_current_practice.csv",
        "pascha_attestation": OUT / "pascha_attestation.csv",
        "temporal_classification": OUT / "temporal_classification.csv",
        "temporal_residue": OUT / "temporal_residue.csv",
        "temporal_residue_manifest": OUT / "temporal_residue_manifest.csv",
        "psalm_mt_lxx_crosswalk": OUT / "psalm_mt_lxx_crosswalk.csv",
        "pascha_attestation_bucket_manifest": OUT / "pascha_attestation_bucket_manifest.csv",
        "synaxarium_commemoration": OUT / "synaxarium_commemorations.csv",
        "synaxarium_reading_bridge": OUT / "synaxarium_reading_bridge.csv",
        "passage_liturgical_footprint": OUT / "passage_liturgical_footprint.csv",
        "source_registry": OUT / "source_registry.csv",
        "passage_source_disclosure": OUT / "passage_source_disclosure.csv",
        "foundational_reading_collection": OUT / "foundational_reading_collections_69.csv",
    }
    for table, path in csv_contracts.items():
        if table not in tables:
            fail(f"Schema missing emitted table contract: {table}")
        actual = read_header(path)
        expected = tables[table]
        if actual != expected:
            fail(f"Schema table {table} header mismatch. actual={actual} expected={expected}")


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
        "passage_source_disclosure_rows": OUT / "passage_source_disclosure.csv",
        "foundational_reading_collection_rows": OUT / "foundational_reading_collections_69.csv",
    }
    for key, path in files.items():
        rows = read_csv(path)
        if len(rows) != summary[key]:
            fail(f"{path} row count {len(rows)} != summary {summary[key]}")
        if not rows:
            fail(f"{path} has no rows")
    foundational = read_csv(OUT / "foundational_reading_collections_69.csv")
    if len(foundational) != 69:
        fail("foundational_reading_collections_69.csv must contain 69 rows")
    if foundational[0].get("coptic_day_key") != "Tut 1" or foundational[-1].get("coptic_day_key") != "Al-Nasi 6":
        fail("foundational 69 boundary entries are not the expected Ottawa TOC range")
    if {row.get("membership_status") for row in foundational} != {"inferred_likely_same_set_roster_unverified"}:
        fail("foundational 69 membership status must record roster-unverified inferred alignment")
    if {row.get("membership_verdict") for row in foundational} != {"INFERRED_LIKELY_SAME_SET"}:
        fail("foundational 69 membership verdict token must record inferred likely same set")
    presentation = read_csv(OUT / "reverse_lectionary_presentation.csv")
    reverse_index = read_jsonl(OUT / "reverse_lectionary_index.jsonl")
    if summary.get("reverse_lectionary_index_rows") != len(reverse_index):
        fail(f"reverse_lectionary_index row count {len(reverse_index)} != summary {summary.get('reverse_lectionary_index_rows')}")
    if len(reverse_index) != 8003:
        fail(f"reverse_lectionary_index row count {len(reverse_index)} != expected 8003")
    grouped_index_source: dict[tuple[str, str, str, str, str], list[dict]] = defaultdict(list)
    for row in presentation:
        grouped_index_source[occasion_index_key(row)].append(row)
    index_keys = [occasion_index_key(row) for row in reverse_index]
    duplicate_index_keys = [key for key, count in Counter(index_keys).items() if count != 1]
    if duplicate_index_keys:
        fail(f"reverse_lectionary_index duplicate keys: {len(duplicate_index_keys)}")
    expected_keys = set(grouped_index_source)
    actual_keys = set(index_keys)
    if expected_keys != actual_keys:
        fail(f"reverse_lectionary_index key mismatch missing={len(expected_keys - actual_keys)} extra={len(actual_keys - expected_keys)}")
    for row in reverse_index:
        if "gregorian_date" in row or "coptic_date" in row:
            fail("reverse_lectionary_index must not carry gregorian_date or coptic_date")
        if row.get("slot_type") not in schema.get("controlled_vocabularies", {}).get("slot_type", []):
            fail(f"reverse_lectionary_index slot_type outside schema vocabulary: {row.get('slot_type')}")
        if row.get("occasion_kind") not in schema.get("controlled_vocabularies", {}).get("occasion_kind", []):
            fail(f"reverse_lectionary_index occasion_kind outside schema vocabulary: {row.get('occasion_kind')}")
        if row.get("slot_type") != "source_label_preserved" and row.get("slot_order") is None:
            fail(f"reverse_lectionary_index mapped slot missing slot_order: {occasion_index_key(row)}")
        if row.get("slot_type") == "source_label_preserved" and row.get("slot_order") is not None:
            fail(f"reverse_lectionary_index preserved source-label slot should not have slot_order: {occasion_index_key(row)}")
        source_rows = grouped_index_source[occasion_index_key(row)]
        statuses = set(r.get("current_status", "") for r in source_rows)
        markers = set(r.get("removed_marker", "") for r in source_rows)
        if len(statuses) > 1:
            fail(f"reverse_lectionary_index source current_status disagreement not flagged separately: {occasion_index_key(row)} {statuses}")
        if len(markers) > 1:
            fail(f"reverse_lectionary_index source removed_marker disagreement not flagged separately: {occasion_index_key(row)} {markers}")
        if row.get("calendar_keys", "") != join_unique(r.get("calendar_key", "") for r in source_rows):
            fail(f"reverse_lectionary_index calendar key union mismatch: {occasion_index_key(row)}")
        if row.get("source_family", "") != join_unique(r.get("source_family", "") for r in source_rows):
            fail(f"reverse_lectionary_index source_family union mismatch: {occasion_index_key(row)}")
        if row.get("source_kind", "") != join_unique(r.get("source_kind", "") for r in source_rows):
            fail(f"reverse_lectionary_index source_kind union mismatch: {occasion_index_key(row)}")
        years = sorted(year for year in (gregorian_year(r.get("gregorian_date", "")) for r in source_rows) if year is not None)
        expected_min = str(min(years)) if years else ""
        expected_max = str(max(years)) if years else ""
        if row.get("attestation_year_min", "") != expected_min or row.get("attestation_year_max", "") != expected_max:
            fail(f"reverse_lectionary_index attestation year span mismatch: {occasion_index_key(row)}")
        expected_disclosure, representative_locators = expected_source_disclosure(source_rows)
        if row.get("source_locator", "") != " || ".join(representative_locators):
            fail(f"reverse_lectionary_index representative locator mismatch: {occasion_index_key(row)}")
        if " || " in row.get("source_locator", "") and len(representative_locators) == 1:
            fail(f"reverse_lectionary_index stores repeated same-source locators: {occasion_index_key(row)}")
        disclosure = json.loads(row.get("source_disclosure", "[]") or "[]")
        if disclosure != expected_disclosure:
            fail(f"reverse_lectionary_index collapsed source disclosure mismatch: {occasion_index_key(row)}")
        if row.get("source_disclosure_count", "") != str(len(expected_disclosure)):
            fail(f"reverse_lectionary_index disclosure count mismatch: {occasion_index_key(row)}")
        if len(disclosure) != len({source_disclosure_key(r) for r in source_rows}):
            fail(f"reverse_lectionary_index distinct-source count changed: {occasion_index_key(row)}")
        for item in disclosure:
            if "source_locator" in item and " || " in item["source_locator"]:
                fail(f"reverse_lectionary_index source disclosure locator is not representative: {occasion_index_key(row)}")
    if summary.get("reverse_lectionary_index_status_disagreement_rows") != 0:
        fail("reverse_lectionary_index should have zero status disagreement rows in this run")
    daily_fields = schema.get("tables", {}).get("daily_lectionary_year", [])
    expected_daily_by_year: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in presentation:
        date_value = row.get("gregorian_date", "")
        if not date_value:
            continue
        year = date_value[:4]
        expected_daily_by_year[year][date_value].append({field: row.get(field, "") for field in daily_fields})
    expected_year_counts = {year: sum(len(readings) for readings in days.values()) for year, days in sorted(expected_daily_by_year.items())}
    if summary.get("daily_lectionary_years") != expected_year_counts:
        fail(f"daily_lectionary_years summary mismatch: {summary.get('daily_lectionary_years')} != {expected_year_counts}")
    if summary.get("daily_lectionary_total_rows") != sum(expected_year_counts.values()):
        fail("daily_lectionary_total_rows does not match dated presentation rows")
    daily_paths = sorted((OUT / "daily").glob("lectionary-*.json"))
    if [path.stem.rsplit("-", 1)[-1] for path in daily_paths] != sorted(expected_year_counts):
        fail("daily lectionary year files do not match expected dated-year range")
    for path in daily_paths:
        year = path.stem.rsplit("-", 1)[-1]
        data = json.loads(path.read_text(encoding="utf-8"))
        expected_days = dict(sorted(expected_daily_by_year[year].items()))
        if data != expected_days:
            fail(f"daily file {path} does not exactly match dated presentation rows")
        if sum(len(readings) for readings in data.values()) != expected_year_counts[year]:
            fail(f"daily file {path} row count mismatch")
        for date_value, readings in data.items():
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_value):
                fail(f"daily file {path} has malformed ISO date key: {date_value}")
            for reading in readings:
                if list(reading.keys()) != daily_fields:
                    fail(f"daily file {path} reading fields mismatch: {list(reading.keys())}")
    identity = read_csv(OUT / "reading_identity.csv")
    crosswalk = read_csv(OUT / "psalm_mt_lxx_crosswalk.csv")
    scopes = {r.get("mapping_scope") for r in crosswalk}
    required_scopes = {"chapter_equivalence", "split_merge_chapter_seam", "lxx_unique_chapter", "anchored_verse_example", "unresolved_verse_offset_example"}
    if not required_scopes.issubset(scopes):
        fail(f"Crosswalk missing mapping scopes: {sorted(required_scopes - scopes)}")
    temporal = read_csv(OUT / "temporal_classification.csv")
    attestation = read_csv(OUT / "pascha_attestation.csv")
    attestation_manifest = read_csv(OUT / "pascha_attestation_bucket_manifest.csv")
    removed_rows = [r for r in presentation if r.get("removed_marker")]
    removed_refs = {r.get("display_ref") for r in removed_rows}
    required_removed_refs = {"Isa 48:1-6", "Isa 59:1-17", "Zech 11:11-14", "Prov 1:10-33", "Prov 4:4-27,5:1-4", "Job 27:16-28:2", "Job 27:16-20", "Job 28:1-2"}
    if not required_removed_refs.issubset(removed_refs):
        fail(f"Removed Pascha markers missing refs: {sorted(required_removed_refs - removed_refs)}")
    if any(r.get("day_title") == "Wednesday" and r.get("service_hour") == "Third Hour" and r.get("display_ref") == "Prov 4:4-5:4" for r in removed_rows):
        fail("Prov 4:4-5:4 must be normalized into Prov 4:4-27,5:1-4, not retained as a separate Wednesday Third Hour removed row")
    for row in removed_rows:
        marker = row.get("removed_marker", "")
        is_wednesday_fixture_marker = marker.startswith("(removed, attested St. Mary Ottawa Holy Pascha") and "absent from Coptic Reader Wednesday Day fixture supplied by George" in marker
        is_superseded_marker = re.fullmatch(r"superseded by rid_[0-9a-f]{20}", marker) is not None
        if not (is_wednesday_fixture_marker or is_superseded_marker):
            fail(f"Malformed removed_marker: {marker}")
    if any(r.get("display_ref") == "Isa 48:1-6" and r.get("current_status") != "historical_candidate_removed" for r in removed_rows):
        fail("Isa 48:1-6 must be retained only as a historical removed candidate")
    temporal_residue = read_csv(OUT / "temporal_residue.csv")
    temporal_residue_manifest = read_csv(OUT / "temporal_residue_manifest.csv")
    passage_source_disclosure = read_csv(OUT / "passage_source_disclosure.csv")
    allowed_current_authority = set(schema.get("controlled_vocabularies", {}).get("current_authority", []))
    for field in ["source_authority_tier", "source_titles", "source_editions", "source_locators", "attestation_bucket", "current_authority", "current_status"]:
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
    required = ["identity_key", "reading_type", "reading_name", "display_ref", "canonical_mt_ref", "canonical_lxx_ref", "source_convention", "source_key", "source_title", "source_edition", "source_locator", "source_url", "current_status", "authority_tier", "spans_json"]
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
    for field in ["title", "edition", "default_locator", "url"]:
        blanks = [row.get("source_key", "") for row in registry if not row.get(field)]
        if blanks:
            fail(f"Source registry rows missing {field}: {blanks}")
    for field in ["source_title", "source_edition", "source_locator", "source_url"]:
        blanks = sum(1 for row in presentation if not row.get(field))
        if blanks:
            fail(f"Presentation rows missing {field}: {blanks}")
    if len(passage_source_disclosure) != len(presentation):
        fail(f"Passage source disclosure row count {len(passage_source_disclosure)} != presentation rows {len(presentation)}")
    for field in ["source_title", "source_edition", "source_locator", "citation"]:
        blanks = sum(1 for row in passage_source_disclosure if not row.get(field))
        if blanks:
            fail(f"Passage source disclosure rows missing {field}: {blanks}")
    removed_disclosure = [row for row in passage_source_disclosure if row.get("removed_marker")]
    if len(removed_disclosure) != len(removed_rows):
        fail("Passage source disclosure does not preserve removed_marker rows")
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
    for field in ["source_titles", "source_editions", "source_locators"]:
        blanks = [row for row in attestation if not row.get(field)]
        if blanks:
            fail(f"Pascha attestation rows missing {field}: {len(blanks)}")
    if any(not row.get("attestation_note") for row in attestation):
        fail("Pascha attestation row missing attestation_note")
    bare_api = [row for row in attestation if row.get("citation", "").strip() == "api" or "; api" in row.get("citation", "")]
    if bare_api:
        fail(f"Pascha attestation rows with bare api citation: {len(bare_api)}")
    weak_citations = [row for row in attestation if "source_file=" not in row.get("citation", "") or "source_row_id=" not in row.get("citation", "") or "source_title=" not in row.get("citation", "") or "source_edition=" not in row.get("citation", "") or "source_locator=" not in row.get("citation", "")]
    if weak_citations:
        fail(f"Pascha attestation rows missing replayable source_file/source_row_id citation: {len(weak_citations)}")
    commems = read_csv(OUT / "synaxarium_commemorations.csv")
    bridge = read_csv(OUT / "synaxarium_reading_bridge.csv")
    commem_ids = [row.get("commem_id", "") for row in commems]
    if len(commem_ids) != len(set(commem_ids)):
        fail("Synaxarium commem_id values are not unique")
    if any(not row.get("source_url") for row in commems):
        fail("Synaxarium commemoration row missing source_url")
    if any(not row.get("source_summary") for row in commems):
        fail("Synaxarium commemoration row missing source_summary")
    if any(not row.get("title") or not row.get("type") for row in commems):
        fail("Synaxarium commemoration row missing title or type")
    if any(row.get("extraction_method") == "day_title_fallback" for row in commems):
        fail("Synaxarium extraction still uses day-title fallback rows")
    inferred_without_caveat = [row for row in commems if row.get("extraction_method") == "prose_lead_inferred" and not row.get("caveat")]
    if inferred_without_caveat:
        fail(f"Synaxarium prose-lead inferred rows missing caveat: {len(inferred_without_caveat)}")
    day_title_like = [row for row in commems if re.match(r"^\d+\s+\w+\s*\(", row.get("title", ""))]
    if day_title_like:
        fail(f"Synaxarium rows still have day-title fallback looking titles: {len(day_title_like)}")
    long_titles = [row for row in commems if len(row.get("title", "")) > 160]
    if long_titles:
        fail(f"Synaxarium rows still have long prose-like titles: {len(long_titles)}")
    martyr_misclassified = [row for row in commems if re.search(r"\bmartyrdom\b|\bwas martyred\b|\bwere martyred\b", row.get("title", ""), re.I) and row.get("type") != "martyr"]
    if martyr_misclassified:
        fail(f"Synaxarium martyr title rows misclassified: {len(martyr_misclassified)}")
    theotokos_bad = [row for row in commems if row.get("type") == "theotokos" and not re.search(r"theotokos|virgin mary|st\. mary|saint mary|holy virgin mary", row.get("title", ""), re.I)]
    if theotokos_bad:
        fail(f"Synaxarium theotokos rows not explicitly Mary/Theotokos: {len(theotokos_bad)}")
    day_counts = {}
    for row in commems:
        day_counts[row.get("coptic_day_key", "")] = day_counts.get(row.get("coptic_day_key", ""), 0) + 1
    if sum(1 for count in day_counts.values() if count > 1) < 100:
        fail("Synaxarium ingestion did not preserve expected multiple-commemoration days")
    valid_commem_ids = set(commem_ids)
    reading_identity_keys = {row.get("identity_key", "") for row in identity}
    bridge_bad_ids = [row for row in bridge if row.get("commem_id") not in valid_commem_ids]
    if bridge_bad_ids:
        fail(f"Synaxarium bridge rows reference missing commem_id: {len(bridge_bad_ids)}")
    bridge_bad_readings = [row for row in bridge if row.get("reading_identity_key") not in reading_identity_keys]
    if bridge_bad_readings:
        fail(f"Synaxarium bridge rows reference missing reading_identity_key: {len(bridge_bad_readings)}")
    if any(not row.get("display_ref") or not row.get("slot") for row in bridge):
        fail("Synaxarium bridge row missing display_ref or slot")
    allowed_basis = set(schema.get("controlled_vocabularies", {}).get("bridge_basis", []))
    allowed_bridge_confidence = set(schema.get("controlled_vocabularies", {}).get("bridge_confidence", []))
    if any(row.get("basis") not in allowed_basis for row in bridge):
        fail("Synaxarium bridge basis outside schema vocabulary")
    if any(row.get("confidence") not in allowed_bridge_confidence for row in bridge):
        fail("Synaxarium bridge confidence outside schema vocabulary")
    foundational_days = {row.get("coptic_day_key", "") for row in foundational}
    explicit_bridge = [row for row in bridge if row.get("basis") == "explicit"]
    if not explicit_bridge:
        fail("Step 7 expected explicit bridge rows for the 69 foundational-reading days")
    explicit_outside_69 = [row for row in explicit_bridge if row.get("coptic_day_key", "") not in foundational_days]
    if explicit_outside_69:
        fail(f"Explicit bridge rows outside the Ottawa 69 dated-entry taxonomy: {len(explicit_outside_69)}")
    if any(row.get("confidence") != "high" for row in explicit_bridge):
        fail("Explicit Ottawa 69 taxonomy bridge rows must use high confidence")
    if any("Ottawa/UKMID Katameros of the Days" not in row.get("citation", "") for row in explicit_bridge):
        fail("Explicit 69 bridge rows missing Ottawa citation")
    outside_69 = [row for row in bridge if row.get("coptic_day_key", "") not in foundational_days]
    outside_bases = {row.get("basis") for row in outside_69}
    outside_confidences = {row.get("confidence") for row in outside_69}
    if outside_69 and outside_bases != {"collection-type"}:
        fail(f"Outside-69 bridge rows should remain collection-type in this run: {outside_bases}")
    if outside_69 and outside_confidences != {"medium"}:
        fail(f"Outside-69 bridge rows should remain medium confidence in this run: {outside_confidences}")
    overstrong_collection = [row for row in bridge if row.get("basis") == "collection-type" and row.get("confidence") != "medium"]
    if overstrong_collection:
        fail(f"Collection-type bridge rows must use medium confidence unless direct proper-reading evidence exists: {len(overstrong_collection)}")
    rank_by_id = {row.get("commem_id", ""): int(row.get("rank", "0") or 0) for row in commems}
    if any(rank_by_id.get(row.get("commem_id", "")) != 1 for row in bridge):
        fail("Synaxarium bridge should link only primary commemoration unless proper-reading source is explicit")
    duplicate_slot_groups = Counter((row.get("commem_id", ""), row.get("coptic_day_key", ""), row.get("slot", "")) for row in bridge)
    has_duplicate_slot_groups = any(count > 1 for count in duplicate_slot_groups.values())
    if has_duplicate_slot_groups:
        undocumented = [row for row in bridge if "not a resolved daily service schedule" not in row.get("note", "") or "not direct proper-reading proof" not in row.get("note", "") or "source-row or variant catalog" not in row.get("note", "")]
        if undocumented:
            fail(f"Bridge has duplicate slot groups without explicit catalog/not-resolved-schedule note: {len(undocumented)}")
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


def verify_pascha_source_text_prophecy_orders() -> None:
    reverse_index = read_jsonl(OUT / "reverse_lectionary_index.jsonl")
    rows_by_key = {
        (
            row.get("occasion", ""),
            row.get("service_hour", ""),
            row.get("slot", ""),
            row.get("display_ref", ""),
        ): row
        for row in reverse_index
    }
    expected_orders = {
        ("Good Friday", "First Hour", "Prophecy", "Job 12:17-13:1"): 7,
        ("Good Friday", "First Hour", "Prophecy", "Zech 11:14"): 8,
        ("Great Thursday", "Ninth Hour", "Prophecy", "Isa 61:1-6"): 2,
        ("Great Thursday Eve", "Ninth Hour", "Prophecy", "Jer 9:7-11"): 1,
        ("Tuesday", "Ninth Hour", "Prophecy", "Prov 9:1-11"): 2,
        ("Tuesday", "Ninth Hour", "Prophecy", "Isa 40:9-31"): 3,
        ("Tuesday", "Ninth Hour", "Prophecy", "Dan 7:9-15"): 4,
        ("Tuesday", "Ninth Hour", "Prophecy", "Prov 8:1-12"): 5,
    }
    for key, expected in expected_orders.items():
        row = rows_by_key.get(key)
        if row is None:
            fail(f"Missing Pascha source-text prophecy order guard row: {key}")
            continue
        if row.get("source_kind") != "pascha_source_text":
            fail(f"Pascha prophecy order guard row should come from source text: {key} source_kind={row.get('source_kind')}")
        if row.get("slot_order") != expected:
            fail(f"Pascha prophecy order guard row {key} expected slot_order {expected}, got {row.get('slot_order')}")


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
    verify_pascha_source_text_prophecy_orders()
    verify_psalm_seams()
    print("design deliverables verified")


if __name__ == "__main__":
    main()
