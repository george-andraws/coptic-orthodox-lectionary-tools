#!/usr/bin/env python3
"""Validate the generated @andraws/lectionary-data package directory and tarball."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "packages" / "lectionary-data"
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_PACKAGE_FILES = {
    "LICENSE",
    "README.md",
    "data/daily/lectionary-2026.json",
    "data/daily/lectionary-2027.json",
    "data/daily/lectionary-2028.json",
    "data/reverse_lectionary_index.jsonl",
    "index.js",
    "meta.json",
    "package.json",
}
REQUIRED_REVERSE_FIELDS = [
    "occasion",
    "service_section",
    "service_hour",
    "slot",
    "slot_type",
    "slot_order",
    "occasion_kind",
    "identity_key",
    "display_ref",
    "canonical_mt_ref",
    "canonical_lxx_ref",
    "spans_json",
    "removed_marker",
    "hour_theme",
    "source_disclosure",
    "attestation_year_min",
    "attestation_year_max",
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssertionError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Invalid JSON in {path}: {exc}") from exc


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path} line {line_number}: invalid JSONL row: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path} line {line_number}: JSONL row must be an object")
            rows.append(row)
    return rows


def count_jsonl_rows(path: Path) -> int:
    return len(parse_jsonl(path))


def daily_counts(data: dict[str, Any]) -> dict[str, int]:
    return {
        "date_count": len(data),
        "reading_count": sum(len(readings) for readings in data.values() if isinstance(readings, list)),
    }


LEGACY_MONTH_SPELLINGS = {
    "Kiak": "Kiahk",
    "Baba": "Babah",
}
TEXT_FIELDS_FOR_MONTH_SCAN = ["occasion", "calendar_keys", "day_titles", "source_disclosure"]
SOURCE_PRIORITY = {
    "ordinary_date_resolved": 10,
    "coptic_reader_fixture": 20,
    "holy_pascha_curated_day_hour": 30,
    "holy_pascha": 40,
    "katameros_cycle": 90,
}
WEEKDAYS = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
ORDINALS = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth",
    7: "seventh",
    8: "eighth",
}


def normalize_context_text(value: Any) -> str:
    text = str(value or "")
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\bKiak\b", "Kiahk", text)
    text = re.sub(r"\bBaba\b", "Babah", text)
    text = text.replace("/Pentecost", "")
    text = re.sub(r"[(),]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().casefold()
    return text


def normalized_service(value: Any) -> str:
    compact = re.sub(r"[^a-z]", "", str(value or "").casefold())
    if "vespers" in compact:
        return "vespers"
    if "matins" in compact:
        return "matins"
    if "liturgy" in compact:
        return "liturgy"
    return normalize_context_text(value)


def normalized_slot_type(row: dict[str, Any]) -> str:
    slot_type = row.get("slot_type")
    if slot_type:
        return normalize_context_text(slot_type)
    compact = re.sub(r"[^a-z]", "", str(row.get("slot") or "").casefold())
    if "psalm" in compact:
        return "psalm"
    if "gospel" in compact:
        return "gospel"
    if "pauline" in compact:
        return "pauline"
    if "catholic" in compact or "catholicon" in compact:
        return "catholicon"
    if "acts" in compact or "praxis" in compact:
        return "praxis"
    if "prophecy" in compact or compact.startswith("ot"):
        return "prophecy"
    return normalize_context_text(row.get("slot"))


def source_priority(row: dict[str, Any]) -> int:
    return SOURCE_PRIORITY.get(str(row.get("source_family") or ""), 100)


def mapped_cycle_contexts(row: dict[str, Any]) -> set[str]:
    contexts: set[str] = set()
    source_family = str(row.get("source_family") or "")
    if source_family != "katameros_cycle":
        return contexts
    occasion = str(row.get("occasion") or "")
    calendar_keys = str(row.get("calendar_keys") or "")
    if "week" not in calendar_keys or "day_of_week" not in calendar_keys:
        return contexts
    for week_text, day_text in re.findall(r"week\s+(\d+)\s+day_of_week\s+(\d+)", calendar_keys):
        week = int(week_text)
        day = int(day_text)
        if week not in ORDINALS or day >= len(WEEKDAYS):
            continue
        weekday = WEEKDAYS[day]
        ordinal = ORDINALS[week]
        if "Holy Fifty" in occasion:
            contexts.add(f"{weekday} of the {ordinal} week of the holy fifty days")
        elif "Great Lent" in occasion:
            contexts.add(f"{weekday} of the {ordinal} week of great lent")
    return {normalize_context_text(context) for context in contexts}


def consumer_contexts(row: dict[str, Any]) -> set[str]:
    contexts = mapped_cycle_contexts(row)
    for field in ["occasion", "calendar_keys", "day_titles"]:
        raw = str(row.get(field) or "")
        for part in re.split(r"\s*(?:;|\|\|)\s*", raw):
            normalized = normalize_context_text(part)
            if normalized and normalized not in {"holy fifty days cycle", "holy fifty days", "great lent jonah nineveh cycle"}:
                contexts.add(normalized)
    return contexts


def parse_spans(row: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        spans = json.loads(row.get("spans_json") or "[]")
    except json.JSONDecodeError:
        return []
    return [span for span in spans if isinstance(span, dict)] if isinstance(spans, list) else []


def span_interval(span: dict[str, Any]) -> tuple[str, int, int] | None:
    try:
        book = str(span.get("book") or "").casefold()
        chapter_start = int(span.get("chapter_start"))
        chapter_end = int(span.get("chapter_end") or chapter_start)
        verse_start = int(span.get("verse_start") or 0)
        verse_end = int(span.get("verse_end") or verse_start)
    except (TypeError, ValueError):
        return None
    if not book:
        return None
    return (book, chapter_start * 1000 + verse_start, chapter_end * 1000 + verse_end)


def spans_overlap(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_intervals = [interval for interval in (span_interval(span) for span in parse_spans(left)) if interval]
    right_intervals = [interval for interval in (span_interval(span) for span in parse_spans(right)) if interval]
    for left_book, left_start, left_end in left_intervals:
        for right_book, right_start, right_end in right_intervals:
            if left_book == right_book and left_start <= right_end and right_start <= left_end:
                return True
    return False


def passage_variant(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_ref = normalize_context_text(left.get("canonical_mt_ref") or left.get("display_ref"))
    right_ref = normalize_context_text(right.get("canonical_mt_ref") or right.get("display_ref"))
    return bool(left_ref and right_ref and left_ref != right_ref)


def parse_reference_shape(value: Any) -> dict[str, Any] | None:
    text = re.sub(r"\([^)]*\)", "", str(value or "")).strip()
    match = re.match(r"^\s*([1-3]?\s*[A-Za-z]+)\s+(\d+):(\d+)\s*-\s*(\d+)(?::(\d+))?\s*$", text)
    if not match:
        return None
    return {
        "book": re.sub(r"\s+", "", match.group(1)).casefold(),
        "start_chapter": int(match.group(2)),
        "start_verse": int(match.group(3)),
        "end_chapter": int(match.group(4)),
        "end_verse": int(match.group(5)) if match.group(5) is not None else None,
    }


def shorthand_chapter_variant(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_shape = parse_reference_shape(left.get("canonical_mt_ref") or left.get("display_ref"))
    right_shape = parse_reference_shape(right.get("canonical_mt_ref") or right.get("display_ref"))
    if not left_shape or not right_shape:
        return False
    if left_shape["book"] != right_shape["book"]:
        return False
    if left_shape["start_chapter"] != right_shape["start_chapter"] or left_shape["start_verse"] != right_shape["start_verse"]:
        return False
    left_shorthand = left_shape["end_verse"] is None
    right_shorthand = right_shape["end_verse"] is None
    if left_shorthand == right_shorthand:
        return False
    shorthand = left_shape if left_shorthand else right_shape
    expanded = right_shape if left_shorthand else left_shape
    return shorthand["end_chapter"] == expanded["end_chapter"] and expanded["end_verse"] is not None


def passage_overlap_or_shorthand_variant(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return spans_overlap(left, right) or shorthand_chapter_variant(left, right)


def detect_context_passage_conflicts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str, str], list[tuple[int, dict[str, Any]]]] = {}
    for row_number, row in enumerate(rows, 1):
        if str(row.get("removed_marker") or "").strip():
            continue
        if str(row.get("current_status") or "").casefold().startswith("superseded"):
            continue
        service = normalized_service(row.get("service_section"))
        hour = normalize_context_text(row.get("service_hour"))
        slot = normalized_slot_type(row)
        for context in consumer_contexts(row):
            groups.setdefault((context, service, hour, slot), []).append((row_number, row))

    conflicts: list[dict[str, Any]] = []
    seen: set[tuple[int, int, tuple[str, str, str, str]]] = set()
    for key, members in groups.items():
        for index, (left_number, left) in enumerate(members):
            for right_number, right in members[index + 1 :]:
                if source_priority(left) == source_priority(right):
                    continue
                if not passage_overlap_or_shorthand_variant(left, right) or not passage_variant(left, right):
                    continue
                preferred_number, preferred = (left_number, left) if source_priority(left) < source_priority(right) else (right_number, right)
                lower_number, lower = (right_number, right) if preferred is left else (left_number, left)
                conflict_key = (min(left_number, right_number), max(left_number, right_number), key)
                if conflict_key in seen:
                    continue
                seen.add(conflict_key)
                conflicts.append({
                    "context_key": "|".join(key),
                    "preferred_row": preferred_number,
                    "preferred_source_family": preferred.get("source_family"),
                    "preferred_display_ref": preferred.get("display_ref"),
                    "lower_priority_row": lower_number,
                    "lower_priority_source_family": lower.get("source_family"),
                    "lower_priority_display_ref": lower.get("display_ref"),
                    "lower_priority_identity_key": lower.get("identity_key"),
                })
    return conflicts


def find_legacy_month_spellings(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    seen: set[tuple[int, str, str]] = set()
    for row_number, row in enumerate(rows, 1):
        for field in TEXT_FIELDS_FOR_MONTH_SCAN:
            value = str(row.get(field) or "")
            for legacy, replacement in LEGACY_MONTH_SPELLINGS.items():
                if re.search(rf"\b{re.escape(legacy)}\b", value):
                    key = (row_number, field, legacy)
                    if key not in seen:
                        findings.append({"row": row_number, "field": field, "legacy": legacy, "replacement": replacement, "value": value[:200]})
                        seen.add(key)
    return findings


def list_package_files(package_dir: Path) -> set[str]:
    return {
        path.relative_to(package_dir).as_posix()
        for path in package_dir.rglob("*")
        if path.is_file() and not path.name.endswith(".tgz")
    }


def validate_tarball_file_set(tarball: Path) -> dict[str, Any]:
    with tarfile.open(tarball, "r:gz") as archive:
        names = {member.name.removeprefix("package/") for member in archive.getmembers() if member.isfile()}
    missing = sorted(REQUIRED_PACKAGE_FILES - names)
    extra = sorted(names - REQUIRED_PACKAGE_FILES)
    return {
        "tarball": str(tarball),
        "files": sorted(names),
        "missing": missing,
        "extra": extra,
        "status": "pass" if not missing and not extra else "fail",
    }


def validate_commonjs_exports(package_dir: Path) -> dict[str, Any]:
    script = """
const pkg = require(process.argv[1]);
const fs = require('node:fs');
const result = {
  shippedYears: pkg.shippedYears,
  occasionIndexExists: fs.existsSync(pkg.occasionIndexPath),
  daily2026Exists: fs.existsSync(pkg.dailyYearPath(2026)),
  structuralDateResolver: pkg.structuralDateResolver,
  classifiedStructuralDate: pkg.classifyDate('2026-04-10'),
  classifiedDailyDate: pkg.classifyDate('2026-01-01'),
};
console.log(JSON.stringify(result));
"""
    try:
        completed = subprocess.run(
            ["node", "-e", script, str(package_dir)],
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError:
        return {"status": "skipped", "reason": "node executable not found"}
    except subprocess.CalledProcessError as exc:
        return {"status": "fail", "stdout": exc.stdout, "stderr": exc.stderr}
    parsed = json.loads(completed.stdout)
    ok = (
        parsed.get("occasionIndexExists") is True
        and parsed.get("daily2026Exists") is True
        and parsed.get("classifiedStructuralDate", {}).get("classification") == "daily_file_present"
        and parsed.get("classifiedStructuralDate", {}).get("hasDailyReadings") is True
        and parsed.get("classifiedDailyDate", {}).get("hasDailyReadings") is True
    )
    return {"status": "pass" if ok else "fail", **parsed}


def validate_package_integrity(package_dir: Path, tarball: Path | None = None, strict_file_set: bool = False) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    warnings: list[str] = []

    package_json = load_json(package_dir / "package.json")
    meta = load_json(package_dir / "meta.json")
    if package_json.get("name") != meta.get("package_name"):
        failures.append({"reason": "package_name_mismatch", "package_json": package_json.get("name"), "meta": meta.get("package_name")})
    if package_json.get("version") != meta.get("version"):
        failures.append({"reason": "version_mismatch", "package_json": package_json.get("version"), "meta": meta.get("version")})
    if not (meta.get("schemaVersion") or meta.get("schema_version")):
        failures.append({"reason": "package_schema_version_missing"})
    if meta.get("schemaVersion") and meta.get("schema_version") and meta.get("schemaVersion") != meta.get("schema_version"):
        failures.append({"reason": "package_schema_version_alias_mismatch", "schemaVersion": meta.get("schemaVersion"), "schema_version": meta.get("schema_version")})
    structural_resolver = meta.get("structural_date_resolver")
    if not isinstance(structural_resolver, dict):
        failures.append({"reason": "structural_date_resolver_missing"})
        structural_resolver = {}

    package_files = list_package_files(package_dir)
    missing_files = sorted(REQUIRED_PACKAGE_FILES - package_files)
    if missing_files:
        failures.append({"reason": "missing_required_package_files", "files": missing_files})
    extra_files = sorted(package_files - REQUIRED_PACKAGE_FILES)
    if strict_file_set and extra_files:
        failures.append({"reason": "extra_package_files", "files": extra_files})

    reverse_path = package_dir / "data" / "reverse_lectionary_index.jsonl"
    try:
        reverse_rows = parse_jsonl(reverse_path)
    except ValueError as exc:
        failures.append({"reason": "invalid_reverse_jsonl", "error": str(exc)})
        reverse_rows = []
    if meta.get("occasion_index_rows") != len(reverse_rows):
        failures.append({"reason": "occasion_index_row_count_mismatch", "meta": meta.get("occasion_index_rows"), "actual": len(reverse_rows)})

    duplicate_keys: dict[tuple[Any, ...], int] = {}
    duplicate_count = 0
    for row_number, row in enumerate(reverse_rows, 1):
        missing = [field for field in REQUIRED_REVERSE_FIELDS if field not in row]
        if missing:
            failures.append({"reason": "reverse_row_missing_required_fields", "row": row_number, "fields": missing})
            continue
        key = (row.get("occasion"), row.get("service_section"), row.get("service_hour"), row.get("slot"), row.get("identity_key"))
        if key in duplicate_keys:
            duplicate_count += 1
        else:
            duplicate_keys[key] = row_number
        for json_field in ["spans_json", "source_disclosure"]:
            try:
                parsed = json.loads(row.get(json_field) or "[]")
            except json.JSONDecodeError as exc:
                failures.append({"reason": f"invalid_{json_field}", "row": row_number, "error": str(exc)})
                continue
            if json_field == "source_disclosure":
                expected_count = str(len(parsed))
                if str(row.get("source_disclosure_count", "")) != expected_count:
                    failures.append({"reason": "source_disclosure_count_mismatch", "row": row_number, "expected": expected_count, "actual": row.get("source_disclosure_count")})
    if duplicate_count:
        failures.append({"reason": "duplicate_reverse_index_keys", "duplicate_count": duplicate_count})

    legacy_month_spellings = find_legacy_month_spellings(reverse_rows)
    if legacy_month_spellings:
        failures.append({"reason": "legacy_month_spelling", "examples": legacy_month_spellings[:20], "count": len(legacy_month_spellings)})

    context_passage_conflicts = detect_context_passage_conflicts(reverse_rows)
    if context_passage_conflicts:
        failures.append({"reason": "package_context_passage_conflict", "examples": context_passage_conflicts[:20], "count": len(context_passage_conflicts)})

    shipped_years = meta.get("shipped_years", [])
    daily_meta = {entry.get("year"): entry for entry in meta.get("daily_files", [])}
    daily_summary: dict[str, Any] = {}
    for year in shipped_years:
        daily_path = package_dir / "data" / "daily" / f"lectionary-{year}.json"
        data = load_json(daily_path)
        if not isinstance(data, dict):
            failures.append({"reason": "daily_file_not_object", "year": year})
            continue
        malformed_dates = sorted(date_key for date_key in data if not ISO_DATE.fullmatch(date_key))
        wrong_year_dates = sorted(date_key for date_key in data if ISO_DATE.fullmatch(date_key) and int(date_key[:4]) != year)
        non_array_dates = sorted(date_key for date_key, readings in data.items() if not isinstance(readings, list))
        if malformed_dates:
            failures.append({"reason": "daily_malformed_dates", "year": year, "dates": malformed_dates[:20]})
        if wrong_year_dates:
            failures.append({"reason": "daily_wrong_year_dates", "year": year, "dates": wrong_year_dates[:20]})
        if non_array_dates:
            failures.append({"reason": "daily_values_not_arrays", "year": year, "dates": non_array_dates[:20]})
        counts = daily_counts(data)
        expected_orders = {date_key: list(range(1, len(readings) + 1)) for date_key, readings in data.items() if isinstance(readings, list)}
        actual_order_failures = []
        for date_key, readings in data.items():
            if not isinstance(readings, list):
                continue
            orders = [reading.get("reading_order") for reading in readings if isinstance(reading, dict)]
            if orders != expected_orders[date_key]:
                actual_order_failures.append(date_key)
            for index, reading in enumerate(readings, 1):
                if not isinstance(reading, dict):
                    continue
                for field in ["reading_order", "service_order", "slot_type", "slot_order"]:
                    if field not in reading:
                        failures.append({"reason": "daily_reading_missing_order_field", "year": year, "date": date_key, "reading_index": index, "field": field})
        if actual_order_failures:
            failures.append({"reason": "daily_reading_order_not_unique_sequential", "year": year, "dates": actual_order_failures[:20]})
        expected_dates = set()
        if isinstance(year, int):
            import datetime as dt
            start = dt.date(year, 1, 1)
            end = dt.date(year, 12, 31)
            expected_dates = {(start + dt.timedelta(days=offset)).isoformat() for offset in range((end - start).days + 1)}
        missing_dates = sorted(expected_dates - set(data)) if expected_dates else []
        if missing_dates:
            failures.append({"reason": "daily_date_missing", "year": year, "dates": missing_dates[:20], "count": len(missing_dates)})
        meta_entry = daily_meta.get(year, {})
        if meta_entry.get("rows") != counts["date_count"]:
            failures.append({"reason": "daily_meta_rows_mismatch", "year": year, "meta_rows": meta_entry.get("rows"), **counts})
        if "date_count" in meta_entry and meta_entry.get("date_count") != counts["date_count"]:
            failures.append({"reason": "daily_meta_date_count_mismatch", "year": year, "meta_date_count": meta_entry.get("date_count"), **counts})
        if "reading_count" not in meta_entry:
            warnings.append(f"daily_files[{year}].rows currently means date_count; add reading_count in next package metadata")
        elif meta_entry.get("reading_count") != counts["reading_count"]:
            failures.append({"reason": "daily_meta_reading_count_mismatch", "year": year, "meta_reading_count": meta_entry.get("reading_count"), **counts})
        daily_summary[str(year)] = counts

    commonjs = validate_commonjs_exports(package_dir)
    if commonjs.get("status") == "fail":
        failures.append({"reason": "commonjs_exports_failed", "details": commonjs})

    tarball_summary = None
    if tarball:
        tarball_summary = validate_tarball_file_set(tarball)
        if tarball_summary["status"] != "pass":
            failures.append({"reason": "tarball_file_set_mismatch", **tarball_summary})

    return {
        "package_dir": str(package_dir),
        "package_name": package_json.get("name"),
        "version": package_json.get("version"),
        "schemaVersion": meta.get("schemaVersion") or meta.get("schema_version"),
        "source_repo_commit": meta.get("source_repo_commit"),
        "required_files_present": not missing_files,
        "extra_files": extra_files,
        "reverse_index_rows": len(reverse_rows),
        "reverse_index_duplicate_keys": duplicate_count,
        "daily_summary": daily_summary,
        "commonjs_exports": commonjs,
        "tarball": tarball_summary,
        "warnings": warnings,
        "failures": failures,
        "status": "pass" if not failures else "fail",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify @andraws/lectionary-data package integrity.")
    parser.add_argument("--package-dir", type=Path, default=PACKAGE_DIR)
    parser.add_argument("--tarball", type=Path)
    parser.add_argument("--strict-file-set", action="store_true", help="Fail if the package directory has files beyond the required runtime file set. Tarball checks are always exact when provided.")
    parser.add_argument("--output", type=Path, help="Optional JSON summary path.")
    args = parser.parse_args(argv)

    try:
        summary = validate_package_integrity(args.package_dir, args.tarball, args.strict_file_set)
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    text = json.dumps(summary, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
