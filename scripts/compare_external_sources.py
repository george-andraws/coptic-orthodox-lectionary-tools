#!/usr/bin/env python3
"""Compare shipped daily package rows against copticchurch.net cached passage rows.

This is an external-source comparison against the repo's copticchurch.net daily
scrape cache, not a fresh live scrape. It verifies that the package daily files
preserve the public date-resolved passage-index rows for shipped years after
normalizing package-only inline LXX Psalm display annotations.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from passage_normalization import canonicalize_text_ref  # noqa: E402

PACKAGE_DIR = ROOT / "packages" / "lectionary-data"
SOURCE_INDEX = ROOT / "out" / "data" / "copticchurch_passage_index_2020_2035.csv"
INLINE_LXX_RE = re.compile(r"\s*\(LXX [^)]+\)")
STRUCTURAL_PACKAGE_SOURCE_FAMILIES = {
    "holy_pascha_curated_day_hour",
    "bright_saturday",
}
ComparisonKey = tuple[str, str, str, str]


def normalize_reference_for_compare(value: str) -> str:
    stripped = INLINE_LXX_RE.sub("", value or "")
    return canonicalize_text_ref(stripped)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def source_counter(source_rows: list[dict[str, str]], year: int) -> Counter[ComparisonKey]:
    counter: Counter[ComparisonKey] = Counter()
    for row in source_rows:
        date_value = row.get("gregorian_date", "")
        if not date_value.startswith(str(year)):
            continue
        counter[
            (
                date_value,
                row.get("service_section", ""),
                row.get("reading_type", ""),
                normalize_reference_for_compare(row.get("matched_ref", "")),
            )
        ] += 1
    return counter


def is_package_structural_daily_row(reading: dict[str, Any]) -> bool:
    return bool(reading.get("structural_day")) or str(reading.get("source_family") or "") in STRUCTURAL_PACKAGE_SOURCE_FAMILIES


def package_counter(package_dir: Path, year: int) -> tuple[Counter[ComparisonKey], int, int]:
    daily_path = package_dir / "data" / "daily" / f"lectionary-{year}.json"
    daily = load_json(daily_path)
    if not isinstance(daily, dict):
        raise AssertionError(f"{daily_path} must be a JSON object keyed by date")
    counter: Counter[ComparisonKey] = Counter()
    skipped_structural_rows = 0
    total_rows = 0
    for date_value, readings in daily.items():
        if not isinstance(readings, list):
            raise AssertionError(f"{daily_path} date {date_value} must contain a reading array")
        for reading in readings:
            total_rows += 1
            if isinstance(reading, dict) and is_package_structural_daily_row(reading):
                skipped_structural_rows += 1
                continue
            counter[
                (
                    date_value,
                    str(reading.get("service_section", "")),
                    str(reading.get("slot", "")),
                    normalize_reference_for_compare(str(reading.get("display_ref", ""))),
                )
            ] += 1
    return counter, total_rows, skipped_structural_rows


def counter_delta_rows(year: int, source: Counter[ComparisonKey], package: Counter[ComparisonKey]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, count in sorted((source - package).items()):
        rows.append({
            "year": year,
            "status": "source_only_missing_from_package",
            "count": count,
            "gregorian_date": key[0],
            "service_section": key[1],
            "reading_type_or_slot": key[2],
            "normalized_ref": key[3],
        })
    for key, count in sorted((package - source).items()):
        rows.append({
            "year": year,
            "status": "package_only_extra_vs_source",
            "count": count,
            "gregorian_date": key[0],
            "service_section": key[1],
            "reading_type_or_slot": key[2],
            "normalized_ref": key[3],
        })
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["year", "status", "count", "gregorian_date", "service_section", "reading_type_or_slot", "normalized_ref"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def compare_copticchurch_cache(package_dir: Path = PACKAGE_DIR, source_index: Path = SOURCE_INDEX, years: list[int] | None = None) -> dict[str, Any]:
    meta = load_json(package_dir / "meta.json")
    shipped_years = years or list(meta.get("shipped_years", []))
    source_rows = load_csv(source_index)
    failures: list[dict[str, Any]] = []
    comparison_rows: list[dict[str, Any]] = []
    year_summaries: dict[str, Any] = {}

    for year in shipped_years:
        source = source_counter(source_rows, int(year))
        package, package_total_rows, skipped_structural_rows = package_counter(package_dir, int(year))
        delta_rows = counter_delta_rows(int(year), source, package)
        comparison_rows.extend(delta_rows)
        source_count = sum(source.values())
        package_count = sum(package.values())
        mismatch_count = sum(row["count"] for row in delta_rows)
        if mismatch_count:
            failures.append({"year": int(year), "mismatch_count": mismatch_count})
        year_summaries[str(year)] = {
            "source_rows": source_count,
            "package_rows": package_total_rows,
            "comparable_package_rows": package_count,
            "skipped_structural_package_rows": skipped_structural_rows,
            "unique_source_keys": len(source),
            "unique_package_keys": len(package),
            "mismatch_rows": mismatch_count,
            "status": "pass" if mismatch_count == 0 else "fail",
        }

    return {
        "comparison": "package_daily_vs_copticchurch_cached_passage_index",
        "package_dir": str(package_dir),
        "source_index": str(source_index),
        "years": year_summaries,
        "comparison_rows": comparison_rows,
        "failures": failures,
        "status": "pass" if not failures else "fail",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare package daily files against copticchurch cached passage index.")
    parser.add_argument("--package-dir", type=Path, default=PACKAGE_DIR)
    parser.add_argument("--source-index", type=Path, default=SOURCE_INDEX)
    parser.add_argument("--years", nargs="*", type=int)
    parser.add_argument("--output", type=Path, help="Optional JSON summary path.")
    parser.add_argument("--csv-output", type=Path, help="Optional CSV discrepancy output path.")
    args = parser.parse_args(argv)

    try:
        summary = compare_copticchurch_cache(args.package_dir, args.source_index, args.years)
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.csv_output:
        write_csv(args.csv_output, summary["comparison_rows"])
    text_summary = {k: v for k, v in summary.items() if k != "comparison_rows"}
    text = json.dumps(text_summary, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
