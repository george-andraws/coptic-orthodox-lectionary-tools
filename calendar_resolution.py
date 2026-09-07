"""Pure, source-boundary calendar collision resolution for generated artifacts."""
from __future__ import annotations

import copy
import datetime as dt
import re
from typing import Iterable


ANNUNCIATION_EXCEPTION = (
    "UK Midlands Katameros Days p.22 rule 13: Annunciation yields during the "
    "non-repeatable Lord-events window"
)


def julian_pascha_gregorian(year: int) -> dt.date:
    """Return Orthodox Pascha using the Julian computus, expressed Gregorian."""
    a, b, c = year % 4, year % 7, year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    julian = dt.date(year, 3, 22) + dt.timedelta(days=d + e)
    return julian + dt.timedelta(days=13)


def holy_week_day(date_value: dt.date) -> str | None:
    offset = (date_value - julian_pascha_gregorian(date_value.year)).days
    return {-6: "Monday", -5: "Tuesday", -4: "Wednesday", -3: "Great Thursday", -2: "Good Friday"}.get(offset)


def _reading_type(slot: str, ref: str) -> str:
    if slot == "Psalm+Gospel":
        return "Psalm" if re.match(r"^Ps(?:alm)?\s", ref) else "Gospel"
    if slot.startswith("OT"):
        return "Prophecy"
    return slot


def resolve_current_date_rows(raw_rows: Iterable[dict], pascha_rows: Iterable[dict]) -> list[dict]:
    """Overlay only documented Annunciation/Holy Week collisions.

    Raw source rows are copied and never relabelled. Unsupported collision shapes
    fail closed instead of guessing a broader movable-season endpoint.
    """
    rows = [copy.deepcopy(row) for row in raw_rows]
    pascha = [copy.deepcopy(row) for row in pascha_rows]
    by_date: dict[str, list[dict]] = {}
    for row in rows:
        by_date.setdefault(row.get("gregorian_date", ""), []).append(row)
    resolved: list[dict] = []
    for date_text, date_rows in by_date.items():
        is_annunciation = any("annunciation" in row.get("day_title", "").casefold() for row in date_rows)
        if not is_annunciation:
            resolved.extend(date_rows)
            continue
        date_value = dt.date.fromisoformat(date_text)
        day = holy_week_day(date_value)
        if day is None:
            resolved.extend(date_rows)
            continue
        occasions = {day, f"{day} Eve"}
        replacements = [row for row in pascha if row.get("day") in occasions]
        if not replacements:
            raise RuntimeError(f"Unsupported Annunciation collision on {date_text}: no source-backed {day} rows")
        seen: set[tuple[str, str, str, str]] = set()
        for source_row in replacements:
            for ref in (part.strip() for part in source_row.get("refs", "").split(";") if part.strip()):
                key = (source_row["day"], source_row.get("hour", ""), source_row.get("slot", ""), ref)
                if key in seen:
                    continue
                seen.add(key)
                resolved.append({
                    "source": "generated current-date overlay from local Holy Week source",
                    "gregorian_date": date_text,
                    "weekday": date_value.strftime("%A"),
                    "day_title": source_row["day"],
                    "service_section": source_row.get("hour", ""),
                    "reading_type": _reading_type(source_row.get("slot", ""), ref),
                    "raw_ref": ref,
                    "normalized_ref": ref,
                    "parse_status": "calendar_overlay",
                    "normalization_warning": ANNUNCIATION_EXCEPTION,
                    "url": "",
                    "source_occasion": source_row["day"],
                    "source_order": source_row.get("order", ""),
                    "source_slot": source_row.get("slot", ""),
                    "source_raw_refs": source_row.get("raw_refs", "") or source_row.get("refs", ""),
                    "correction_source": source_row.get("correction_source", ""),
                })
    return sorted(resolved, key=lambda row: (
        row.get("gregorian_date", ""), row.get("source_occasion", row.get("day_title", "")),
        row.get("service_section", ""), str(row.get("source_order", "")), row.get("reading_type", ""), row.get("raw_ref", "")
    ))
