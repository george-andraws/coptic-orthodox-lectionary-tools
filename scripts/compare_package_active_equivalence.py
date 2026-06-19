#!/usr/bin/env python3
"""Compare active runtime behavior between two @andraws/lectionary-data package dirs.

This is intended for releases that add inactive/removed provenance rows. The candidate
may contain extra rows marked inactive/removed, but active reverse-index rows and daily
files must remain equivalent to the baseline package.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "packages" / "lectionary-data"


def is_removed_projection_row(row: dict[str, Any]) -> bool:
    return row.get("active") is False or str(row.get("status") or "").casefold() == "removed"


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise AssertionError(f"{path} line {line_number}: invalid JSONL: {exc}") from exc
            if not isinstance(row, dict):
                raise AssertionError(f"{path} line {line_number}: row must be an object")
            rows.append(row)
    return rows


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def active_reverse_counter(package_dir: Path) -> tuple[Counter[str], int, int]:
    rows = parse_jsonl(package_dir / "data" / "reverse_lectionary_index.jsonl")
    active_rows = [row for row in rows if not is_removed_projection_row(row)]
    removed_count = len(rows) - len(active_rows)
    return Counter(canonical(row) for row in active_rows), len(active_rows), removed_count


def daily_file_canonicals(package_dir: Path) -> dict[str, str]:
    daily_dir = package_dir / "data" / "daily"
    files = sorted(daily_dir.glob("lectionary-*.json"))
    if not files:
        raise AssertionError(f"No daily files found under {daily_dir}")
    out: dict[str, str] = {}
    for path in files:
        out[path.name] = canonical(json.loads(path.read_text(encoding="utf-8")))
    return out


def counter_delta(left: Counter[str], right: Counter[str], limit: int = 5) -> dict[str, Any]:
    left_only = list((left - right).elements())[:limit]
    right_only = list((right - left).elements())[:limit]
    return {
        "left_only_count": sum((left - right).values()),
        "right_only_count": sum((right - left).values()),
        "left_only_examples": [json.loads(item) for item in left_only],
        "right_only_examples": [json.loads(item) for item in right_only],
    }


def compare_packages(baseline_dir: Path, candidate_dir: Path) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []

    baseline_reverse, baseline_active_count, baseline_removed_count = active_reverse_counter(baseline_dir)
    candidate_reverse, candidate_active_count, candidate_removed_count = active_reverse_counter(candidate_dir)
    if baseline_reverse != candidate_reverse:
        failures.append({
            "reason": "active_reverse_rows_changed",
            **counter_delta(baseline_reverse, candidate_reverse),
        })

    baseline_daily = daily_file_canonicals(baseline_dir)
    candidate_daily = daily_file_canonicals(candidate_dir)
    if baseline_daily.keys() != candidate_daily.keys():
        failures.append({
            "reason": "daily_file_set_changed",
            "baseline_files": sorted(baseline_daily),
            "candidate_files": sorted(candidate_daily),
        })
    else:
        changed_daily = sorted(name for name in baseline_daily if baseline_daily[name] != candidate_daily[name])
        if changed_daily:
            failures.append({"reason": "daily_files_changed", "files": changed_daily})

    return {
        "baseline_dir": str(baseline_dir),
        "candidate_dir": str(candidate_dir),
        "baseline_active_rows": baseline_active_count,
        "baseline_removed_rows": baseline_removed_count,
        "candidate_active_rows": candidate_active_count,
        "candidate_removed_rows": candidate_removed_count,
        "failures": failures,
        "status": "pass" if not failures else "fail",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare active @andraws/lectionary-data behavior against a baseline package directory.")
    parser.add_argument("baseline_dir", type=Path)
    parser.add_argument("candidate_dir", type=Path, nargs="?", default=PACKAGE_DIR)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    try:
        summary = compare_packages(args.baseline_dir, args.candidate_dir)
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
