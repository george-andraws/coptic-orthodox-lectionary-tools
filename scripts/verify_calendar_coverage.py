#!/usr/bin/env python3
"""Validate shipped daily lectionary calendar coverage.

The daily files intentionally contain only date-resolved readings. Holy Week / Pascha
and Bright Saturday structural rows currently live in the reverse index/supporting
sources until a date resolver maps them into daily files. This verifier makes that
boundary explicit: missing dates are allowed only when they fall in the known Holy
Week structural window, unless --strict-complete-calendar is passed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "packages" / "lectionary-data"
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def julian_pascha_gregorian(year: int) -> dt.date:
    """Return Orthodox/Coptic Pascha date on the Gregorian calendar.

    Uses the Julian computus and applies the 13-day Gregorian offset valid for
    the current dataset range. The repo currently ships and builds 2020-2035,
    where this offset is stable.
    """
    if not 1900 <= year <= 2099:
        raise ValueError("julian_pascha_gregorian currently supports years 1900-2099")
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31
    day = ((d + e + 114) % 31) + 1
    julian_pascha = dt.date(year, month, day)
    return julian_pascha + dt.timedelta(days=13)


def holy_week_structural_window(year: int) -> set[dt.date]:
    pascha = julian_pascha_gregorian(year)
    return {pascha - dt.timedelta(days=offset) for offset in range(1, 7)}


def classify_missing_date(date_value: dt.date) -> dict[str, str]:
    if date_value in holy_week_structural_window(date_value.year):
        return {
            "classification": "holy_week_structural_only_not_in_daily",
            "expected_source": "pascha_or_bright_saturday_structural_rows",
            "severity": "known_gap",
            "next_action": "date-resolve Pascha and Bright Saturday structural rows before requiring complete daily files",
        }
    return {
        "classification": "unclassified_missing_daily_date",
        "expected_source": "unknown",
        "severity": "fail",
        "next_action": "investigate missing date-resolved readings or add a documented exception",
    }


def all_dates_for_year(year: int) -> set[str]:
    start = dt.date(year, 1, 1)
    end = dt.date(year, 12, 31)
    return {(start + dt.timedelta(days=i)).isoformat() for i in range((end - start).days + 1)}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssertionError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Invalid JSON in {path}: {exc}") from exc


def verify_calendar_coverage(package_dir: Path, strict_complete_calendar: bool = False) -> dict[str, Any]:
    meta = load_json(package_dir / "meta.json")
    shipped_years = meta.get("shipped_years")
    if not (meta.get("schemaVersion") or meta.get("schema_version")):
        raise AssertionError("meta.json must contain schemaVersion or schema_version")
    structural_resolver = meta.get("structural_date_resolver")
    if not isinstance(structural_resolver, dict):
        raise AssertionError("meta.json must contain structural_date_resolver when daily files omit structural Holy Week dates")
    resolver_missing_by_year = structural_resolver.get("missing_dates_by_year") or {}
    if not isinstance(shipped_years, list) or not shipped_years:
        raise AssertionError("meta.json must contain non-empty shipped_years list")

    meta_daily = {entry.get("year"): entry for entry in meta.get("daily_files", [])}
    failures: list[dict[str, Any]] = []
    warnings: list[str] = []
    years: dict[str, Any] = {}

    for year in shipped_years:
        if not isinstance(year, int):
            failures.append({"year": year, "reason": "shipped_years entry is not an integer"})
            continue
        path = package_dir / "data" / "daily" / f"lectionary-{year}.json"
        data = load_json(path)
        if not isinstance(data, dict):
            raise AssertionError(f"{path} must be a JSON object keyed by ISO date")

        malformed_dates = sorted(date_key for date_key in data if not ISO_DATE.fullmatch(date_key))
        wrong_year_dates = sorted(date_key for date_key in data if ISO_DATE.fullmatch(date_key) and int(date_key[:4]) != year)
        if malformed_dates:
            failures.append({"year": year, "reason": "malformed_date_keys", "dates": malformed_dates[:20]})
        if wrong_year_dates:
            failures.append({"year": year, "reason": "date_keys_outside_year", "dates": wrong_year_dates[:20]})

        non_array_dates = sorted(date_key for date_key, readings in data.items() if not isinstance(readings, list))
        if non_array_dates:
            failures.append({"year": year, "reason": "date_value_not_reading_array", "dates": non_array_dates[:20]})

        expected_dates = all_dates_for_year(year)
        present_dates = set(data)
        missing = sorted(expected_dates - present_dates)
        extra = sorted(present_dates - expected_dates)
        classified_missing = []
        resolver_dates = {
            entry.get("date")
            for entry in (resolver_missing_by_year.get(str(year)) or [])
            if isinstance(entry, dict)
        }
        for date_key in missing:
            date_value = dt.date.fromisoformat(date_key)
            classification = classify_missing_date(date_value)
            classified_missing.append({"date": date_key, **classification})
            if date_key not in resolver_dates:
                failures.append({"year": year, "date": date_key, "reason": "daily_date_missing_without_structural_resolver", **classification})
            if strict_complete_calendar or classification["severity"] == "fail":
                failures.append({"year": year, "date": date_key, **classification})
        if extra:
            failures.append({"year": year, "reason": "extra_dates_outside_calendar_year", "dates": extra[:20]})

        date_count = len(data)
        reading_count = sum(len(readings) for readings in data.values() if isinstance(readings, list))
        meta_entry = meta_daily.get(year)
        if not meta_entry:
            failures.append({"year": year, "reason": "missing_meta_daily_files_entry"})
        else:
            if meta_entry.get("rows") != date_count:
                failures.append({
                    "year": year,
                    "reason": "meta_daily_rows_mismatch",
                    "meta_rows": meta_entry.get("rows"),
                    "actual_date_count": date_count,
                })
            if "reading_count" not in meta_entry:
                warnings.append(f"daily_files[{year}].rows is a legacy date-count field; add reading_count in the next package metadata revision")
            elif meta_entry.get("reading_count") != reading_count:
                failures.append({
                    "year": year,
                    "reason": "meta_daily_reading_count_mismatch",
                    "meta_reading_count": meta_entry.get("reading_count"),
                    "actual_reading_count": reading_count,
                })

        years[str(year)] = {
            "calendar_days": len(expected_dates),
            "dates_present": date_count,
            "reading_count": reading_count,
            "missing_dates": classified_missing,
            "extra_dates": extra,
            "pascha_date": julian_pascha_gregorian(year).isoformat(),
        }

    summary = {
        "package_dir": str(package_dir),
        "strict_complete_calendar": strict_complete_calendar,
        "years": years,
        "warnings": warnings,
        "failures": failures,
        "status": "pass" if not failures else "fail",
    }
    if failures:
        raise AssertionError(json.dumps(summary, indent=2))
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify shipped lectionary daily calendar coverage.")
    parser.add_argument("--package-dir", type=Path, default=PACKAGE_DIR)
    parser.add_argument("--strict-complete-calendar", action="store_true", help="Fail on any missing calendar date, even known Holy Week structural gaps.")
    parser.add_argument("--output", type=Path, help="Optional JSON summary path.")
    args = parser.parse_args(argv)

    try:
        summary = verify_calendar_coverage(args.package_dir, args.strict_complete_calendar)
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    text = json.dumps(summary, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
