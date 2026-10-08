#!/usr/bin/env python3
"""Compare shipped daily package rows against copticchurch.net cached passage rows.

This is a preservation gate for the reconciled current date sidecar, not a live
scrape or independent primary-source authenticity check. The historical index
is available only by explicit selection. Qualified supplements retain raw OT
slots and source order. Calendar overlays are compared on both sides, not
blanket-excluded; no-service dispositions require exact context and hashed
correction evidence. Structural-only dates outside cache scope remain disclosed.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from passage_normalization import canonicalize_text_ref  # noqa: E402

from calendar_resolution import holy_week_day, julian_pascha_gregorian  # noqa: E402

PACKAGE_DIR = ROOT / "packages" / "lectionary-data"
LEGACY_SOURCE_INDEX = ROOT / "out" / "data" / "copticchurch_passage_index_2020_2035.csv"
SOURCE_INDEX = ROOT / "out" / "data" / "copticchurch_passage_index_current_2020_2035.csv"
CORRECTIONS = ROOT / "sources" / "lectionary_corrections.json"
INLINE_LXX_RE = re.compile(r"\s*\(LXX [^)]+\)")
STRUCTURAL_PACKAGE_SOURCE_FAMILIES = {
    "holy_pascha_curated_day_hour",
    "bright_saturday",
}
ComparisonKey = tuple[str, ...]


def normalize_reference_for_compare(value: str) -> str:
    stripped = INLINE_LXX_RE.sub("", value or "")
    return canonicalize_text_ref(stripped)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def source_counter(source_rows: list[dict[str, str]], year: int) -> Counter[ComparisonKey]:
    """Compatibility four-field extractor; the gate uses contextual_counters."""
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
    """Compatibility extractor, not the context/evidence-qualified gate."""
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
    for status, delta in [('source_only_missing_from_package', source - package),
                          ('package_only_extra_vs_source', package - source)]:
        for key, count in sorted(delta.items()):
            row = {'year': year, 'status': status, 'count': count,
                   'gregorian_date': key[0], 'service_section': key[1],
                   'reading_type_or_slot': key[2], 'normalized_ref': key[3]}
            # Preserve the original four-field API while reporting full context.
            if len(key) > 4:
                row.update(occasion=key[4], service_hour=key[5], slot_order=key[6], source_family=key[7])
            rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["year", "status", "count", "gregorian_date", "service_section", "reading_type_or_slot", "normalized_ref", "occasion", "service_hour", "slot_order", "source_family"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize_occasion(value: str) -> str:
    # Published Coptic month spellings, not broad feast/day aliases.
    value = re.sub(r"\bKiak\b", "Kiahk", value or "", flags=re.I)
    value = re.sub(r"\bBaba\b", "Babah", value, flags=re.I)
    return value.casefold().strip()


def authenticated_evidence(policy: dict, relative: str) -> str:
    """Authenticate direct fingerprints or entries in a fingerprinted manifest."""
    path = ROOT / relative
    assert not Path(relative).is_absolute() and path.resolve().is_relative_to(ROOT.resolve()), "Evidence path escapes repository"
    fingerprints = policy.get("source_fingerprints", {})
    expected = fingerprints.get(relative)
    if expected is None:
        manifest = path.parent / "SHA256SUMS"
        manifest_relative = manifest.relative_to(ROOT).as_posix()
        assert manifest_relative in fingerprints, f"No authenticated evidence fingerprint: {relative}"
        authenticated_evidence(policy, manifest_relative)
        matches = [line.split()[0] for line in manifest.read_text().splitlines()
                   if len(line.split()) == 2 and line.split()[1].lstrip('*') == path.name]
        assert len(matches) == 1, f"Evidence not uniquely bound in manifest: {relative}"
        expected = matches[0]
    assert path.is_file(), f"Evidence missing: {relative}"
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == expected, f"Evidence SHA-256 mismatch: {relative}"
    return actual


def is_removed_daily_row(row: dict) -> bool:
    status = str(row.get('current_status') or row.get('status') or '').strip().lower()
    return (row.get("active") is False or str(row.get("status", '')).lower() == "removed"
            or status in {"removed", "historical_candidate_removed", "historical_witness"}
            or status.startswith('superseded')
            or bool(row.get("removed_marker")) or bool(row.get("superseded_by_ref")))


def authenticated_sunday_table(date: str, policy: dict) -> list[dict]:
    """Reconstruct only the resolver's selected, pinned table (not package membership)."""
    import calendar_resolution as calendar
    import sunday_consumer_contracts as sunday
    from passage_normalization import extract_text_ref_tokens

    # Sunday has its own immutable manifest pin, rather than a correction-file
    # SHA256SUMS entry. Also reject a contradictory explicit policy fingerprint.
    if sunday.FILE in policy.get('source_fingerprints', {}):
        authenticated_evidence(policy, sunday.FILE)
    oracle = calendar.load_sunday_evidence()  # Pins manifest, bodies, oracle and SQLite.
    date_value = dt.date.fromisoformat(date)
    assert calendar.sunday_policy_selection(date_value) is not None, f'Unqualified Sunday date: {date}'
    _, month, _ = calendar.numeric_coptic_date(date_value)
    # A read-only resolver input: nine ordinary upstream positions in the actual
    # civil month, deliberately not the selected target ordinal. No source writes
    # or calendar/selection changes are made by this comparison.
    month_name = {1: 'Tout', 4: 'Kiak', 5: 'Toba', 6: 'Meshir', 12: 'Mesra'}[month]
    seeds = [dict(day_title=f'Fifth Sunday of {month_name}', service_section=section,
                  reading_type=slot) for section, slot, _ in calendar.SUNDAY_POSITIONS]
    table = calendar.sunday_policy_rows(date_value, seeds, oracle)
    assert all(row.get('source') == sunday.SOURCE for row in table), f'Sunday selected table unavailable: {date}'
    result = []
    for row in table:
        for token in extract_text_ref_tokens(row['normalized_ref']):
            result.append({**{k: str(v) for k, v in row.items() if k not in ('normalized_ref', 'parse_status')},
                           'matched_ref': canonicalize_text_ref(token),
                           'source_ref_status': row['parse_status']})
    return result


def contextual_counters(source_rows: list[dict], daily: dict, year: int, policy: dict, *, complete_year=False):
    """Qualified parity; independent correction/calendar predicates never use package membership."""
    source, package = Counter(), Counter()
    dispositions, issues = [], []
    skipped = 0
    overlay_dates = {r['gregorian_date'] for r in source_rows
                     if r.get('source') == 'generated current-date overlay from local Holy Week source'}
    supplement_rules = policy.get('recurring_date_supplements', [])
    suppression_rules = policy.get('suppressed_date_contexts', [])
    pascha_contexts = {(r['day'], r['hour']) for r in load_csv(ROOT / 'out/data/pascha_day_hour_index.csv')}
    bright_sections = {r['subsection'] for r in load_csv(ROOT / 'out/data/bright_saturday_service_order.csv') if r['section']}

    if overlay_dates:
        overlays = [r for r in policy.get('calendar_overlays', [])
                    if r.get('feast') == 'Annunciation' and r.get('scope') == 'Holy Week only'
                    and r.get('replacement_source') == 'out/data/pascha_day_hour_index.csv'
                    and r.get('unsupported_collision_policy') == 'fail']
        assert len(overlays) == 1, 'Calendar overlay lacks the exact documented correction context'

    def issue(date, reason, row):
        issues.append({'year': year, 'status': reason, 'count': 1, 'gregorian_date': date,
                       'service_section': row.get('service_section', ''),
                       'reading_type_or_slot': row.get('slot', row.get('reading_type', '')),
                       'normalized_ref': normalize_reference_for_compare(row.get('display_ref', row.get('matched_ref', '')))})

    import sunday_consumer_contracts as sunday
    sunday_dates = {r.get('gregorian_date', '') for r in source_rows
                    if r.get('gregorian_date', '').startswith(f'{year}-') and sunday.is_sunday(r)}
    sunday_dates.update(date for date, rows in daily.items() if any(sunday.is_sunday(r) for r in rows))
    sunday_tables = {date: authenticated_sunday_table(date, policy) for date in sunday_dates}
    for date, expected in sunday_tables.items():
        actual = [r for r in source_rows if r.get('gregorian_date') == date]
        fields = tuple(expected[0])
        def witness(row):
            return tuple(str(row.get(field, '')) for field in fields)
        if Counter(map(witness, actual)) != Counter(map(witness, expected)):
            issue(date, 'invalid_sunday_source_table', {})
        # Extra context/state cannot hide outside the pinned table's fields.
        for row in actual:
            if (not sunday.current_source_row(row) or is_removed_daily_row(row) or any(row.get(k) for k in
                    ('service_hour', 'source_occasion', 'source_convention', 'canonicalization_confidence', 'canonicalization_note'))
                    or any(flag in row and row[flag] is not False for flag in ('runtime_activation', 'consumer_eligible'))):
                issue(date, 'invalid_sunday_source_context', row)

    def key(date, row, source_side):
        section = str(row.get('service_section', ''))
        occasion = row.get('day_title', '') if source_side else row.get('occasion', '')
        hour = section if source_side and date in overlay_dates else str(row.get('service_hour', ''))
        slot = str(row.get('reading_type', '')) if source_side else str(row.get('slot', ''))
        ref = normalize_reference_for_compare(row.get('matched_ref', '') if source_side else row.get('display_ref', ''))
        family = 'ordinary_date_resolved' if source_side else str(row.get('source_family', 'ordinary_date_resolved'))
        order = ''
        if source_side and row.get('source') == sunday.SOURCE:
            family = sunday.FAMILY
            slot = row.get('source_slot', '')
            order = str(row.get('source_order', ''))
        elif not source_side and sunday.is_sunday(row):
            # The held display suffix is never stripped generically. Its exact
            # emitted identity and disclosure must first pass the daily contract.
            sunday.validate_rows([dict(row, gregorian_date=date)], transport_mode='daily')
            envelope = sunday.strict_json(row['source_disclosure'])[0]['consumer_source_transport'][0]
            context = envelope['consumer_context']
            ref = normalize_reference_for_compare(context['passage'])
            order = str(context['source_order'])
            # Bind the envelope warning (including numeric Coptic date and rule)
            # to the exact resolver witness, not just a matching table label.
            expected = next((r for r in sunday_tables[date]
                             if r['service_section'] == section and r['source_slot'] == slot
                             and r['matched_ref'] == context['passage']), None)
            assert expected is not None and envelope['normalization_warning'] == expected['normalization_warning'], 'Sunday envelope/resolver witness mismatch'
            stage = {'Pauline Epistle': 1, 'Catholic Epistle': 2, 'Acts of the Apostles': 3,
                     'Psalm': 4 if section == 'Liturgy' else 1, 'Gospel': 5 if section == 'Liturgy' else 2}[slot]
            assert type(row.get('reading_order')) is int and row['reading_order'] > 0, 'Sunday missing/invalid physical reading order'
            expected_type = {'Pauline Epistle': 'pauline', 'Catholic Epistle': 'catholicon',
                             'Acts of the Apostles': 'praxis', 'Psalm': 'psalm', 'Gospel': 'gospel'}[slot]
            assert row['slot_type'] == expected_type, 'Sunday package slot type mismatch'
            assert (type(row['slot_order']) is int and row['slot_order'] == stage
                    and type(row['service_order']) is int
                    and row['service_order'] == {'Vespers': 1, 'Matins': 2, 'Liturgy': 99}[section]), 'Sunday package stage/order mismatch'
        elif source_side and row.get('source') == 'Coptic Reader verified recurring supplement':
            family = 'coptic_reader_verified_supplement'
            slot = row.get('source_slot', '')
            order = str(row.get('source_order', ''))
        elif source_side and row.get('source') == 'Coptic Reader verified calendar boundary':
            family = 'coptic_reader_verified_calendar_boundary'
            slot = row.get('source_slot', '')
            if re.fullmatch(r'OT\d+', slot): order = str(row.get('source_order', ''))
        elif source_side and date in overlay_dates:
            family = 'holy_pascha_curated_day_hour'
            if row.get('reading_type') == 'Prophecy':
                slot = row.get('source_slot', '')
                order = str(row.get('source_order', ''))
        elif not source_side and (family in {'coptic_reader_verified_supplement', 'coptic_reader_verified_calendar_boundary'} or date in overlay_dates) and re.fullmatch(r'OT\d+', slot):
            order = str(row.get('slot_order', ''))
        return date, section, slot, ref, normalize_occasion(occasion), hour, order, family

    def supplement_rule(date, occasion):
        offset = (dt.date.fromisoformat(date) - julian_pascha_gregorian(year)).days
        return next((r for r in supplement_rules if r['pascha_offset_days'] == offset
                     and r['day_title'] == occasion), None)

    for row in source_rows:
        date = row.get('gregorian_date', '')
        if not date.startswith(f'{year}-'):
            continue
        title, section = row.get('day_title', ''), row.get('service_section', '')
        rule = next((r for r in suppression_rules if r['day_title'] == title and r['service_section'] == section), None)
        if rule:
            expected_titles = {-69: 'Fast of Nineveh', -68: "Tuesday of Ninevah's Fast", -67: "Wednesday of Ninevah's Fast"}
            offset = (dt.date.fromisoformat(date) - julian_pascha_gregorian(year)).days
            qualified = (row.get('source') == 'copticchurch.net daily scrape'
                         and section == 'Vespers' and rule.get('service_section') == 'Vespers'
                         and expected_titles.get(offset) == title and not row.get('source_occasion')
                         and not row.get('service_hour') and rule.get('reason') == 'coptic_reader_no_service'
                         and rule.get('authority') == 'Coptic Reader web app 3.7')
            if qualified:
                evidence_hash = authenticated_evidence(policy, rule['evidence'])
                assert "Vespers and Vesper Praises are not prayed during Jonah's Fast" in (ROOT / rule['evidence']).read_text(), 'No-service evidence does not state the suppression'
                dispositions.append({'year': year, 'gregorian_date': date, 'occasion': title,
                                     'service_section': section, 'normalized_ref': normalize_reference_for_compare(row['matched_ref']),
                                     'count': 1, 'disposition': 'authenticated_no_service_suppression',
                                     'evidence': rule['evidence'], 'evidence_sha256': evidence_hash})
                continue
            issue(date, 'invalid_suppression_context', row)
        if row.get('source') == 'Coptic Reader verified recurring supplement':
            rule = supplement_rule(date, title)
            assert rule is not None, f'Unqualified recurring supplement: {date} {title}'
            authenticated_evidence(policy, rule['evidence'])
            expected = {(str(r['source_order']), r['source_slot'], normalize_reference_for_compare(r['normalized_ref'])) for r in rule['readings']}
            if (section != rule['service_section'] or row.get('reading_type') != rule['reading_type']
                    or row.get('correction_source') != rule['evidence'] or row.get('source_ref_status') != 'source_supplement'
                    or (str(row.get('source_order', '')), row.get('source_slot'), normalize_reference_for_compare(row['matched_ref'])) not in expected):
                issue(date, 'invalid_supplement_context', row)
        elif row.get('source') == 'Coptic Reader verified calendar boundary':
            from calendar_resolution import load_last_friday_boundary
            rule, table = load_last_friday_boundary()
            authenticated_evidence(policy, rule['evidence'])
            if (title != rule['day_title'] or (dt.date.fromisoformat(date) - julian_pascha_gregorian(year)).days != -9
                    or date[5:] != '04-07' or row.get('correction_source') != rule['evidence']
                    or row.get('source_ref_status') != 'source_boundary_overlay'):
                issue(date, 'invalid_calendar_boundary_context', row)
        elif row.get('source') == sunday.SOURCE:
            # Exact whole-table authentication above; no generic Reader bypass.
            pass
        elif row.get('source') != 'copticchurch.net daily scrape' and date not in overlay_dates:
            issue(date, 'unrecognized_source', row)
        if date in overlay_dates:
            day = holy_week_day(dt.date.fromisoformat(date))
            if (date[5:] != '04-07' or not day or title not in {day, f'{day} Eve'}
                    or row.get('source_occasion') != title or (title, section) not in pascha_contexts
                    or row.get('source_ref_status') != 'calendar_overlay'
                    or row.get('source') != 'generated current-date overlay from local Holy Week source'):
                issue(date, 'invalid_calendar_overlay_context', row)
        source[key(date, row, True)] += 1

    for date, readings in daily.items():
        assert isinstance(readings, list), f'Date {date} must contain a reading array'
        previous_order = 0
        prophecy_sequences = {}
        structural_seen = set()
        overlay_prophecy_orders = {}
        for row in readings:
            assert isinstance(row, dict), f'Date {date} contains a non-object reading'
            if is_removed_daily_row(row):
                issue(date, 'removed_state_in_daily', row)
            # The package's unique per-date order must describe physical consumer order.
            if 'reading_order' in row:
                order = row['reading_order']
                if not isinstance(order, int) or order <= previous_order:
                    issue(date, 'invalid_reading_order', row)
                if isinstance(order, int): previous_order = order
            family = row.get('source_family', '')
            if date in overlay_dates and re.fullmatch(r'OT\d+', str(row.get('slot', ''))):
                context = (row.get('occasion'), row.get('service_hour'))
                order = int(row['slot'][2:])
                if order <= overlay_prophecy_orders.get(context, 0):
                    issue(date, 'invalid_overlay_prophecy_sequence', row)
                overlay_prophecy_orders[context] = order
            if is_package_structural_daily_row(row) and date not in overlay_dates:
                structural_key = key(date, row, False)
                if structural_key in structural_seen:
                    issue(date, 'duplicate_structural_daily_row', row)
                structural_seen.add(structural_key)
                date_value = dt.date.fromisoformat(date)
                day = holy_week_day(date_value)
                if date_value == julian_pascha_gregorian(year) - dt.timedelta(days=1): day = 'Bright Saturday'
                occasions = {day, f'{day} Eve'} if day not in {'Good Friday', 'Bright Saturday', None} else {day}
                if (day and row.get('occasion') in occasions and family in STRUCTURAL_PACKAGE_SOURCE_FAMILIES
                        and row.get('structural_day') == day
                        and row.get('service_hour') == row.get('service_section')
                        and ((family == 'holy_pascha_curated_day_hour' and (row.get('occasion'), row.get('service_hour')) in pascha_contexts)
                             or (family == 'bright_saturday' and row.get('service_section') in bright_sections))
                        and (family != 'bright_saturday' or day == 'Bright Saturday') and not is_removed_daily_row(row)):
                    skipped += 1
                    dispositions.append({'year': year, 'gregorian_date': date, 'occasion': row.get('occasion'),
                                         'service_section': row.get('service_section'), 'count': 1,
                                         'disposition': 'structural_outside_cached_source_scope'})
                    continue
                issue(date, 'invalid_structural_exclusion_context', row)
            if family == 'coptic_reader_verified_supplement':
                rule = supplement_rule(date, row.get('occasion', ''))
                if not rule or row.get('source_file') != rule['evidence'] or row.get('service_section') != rule['service_section'] or row.get('service_hour'):
                    issue(date, 'invalid_package_supplement_context', row)
                else:
                    sequence = prophecy_sequences.setdefault(row['occasion'], [])
                    sequence.append((row.get('slot'), normalize_reference_for_compare(row.get('display_ref', ''))))
            package[key(date, row, False)] += 1
        if date in sunday_tables:
            expected_sequence = [key(date, r, True) for r in sunday_tables[date]]
            actual_sequence = [key(date, r, False) for r in readings]
            if actual_sequence != expected_sequence:
                issue(date, 'invalid_sunday_package_sequence', {})
        for occasion, sequence in prophecy_sequences.items():
            rule = supplement_rule(date, occasion)
            assert rule is not None, f'Missing supplement oracle: {date} {occasion}'
            expected = [(r['source_slot'], normalize_reference_for_compare(r['normalized_ref'])) for r in rule['readings']]
            if sequence != expected:
                issue(date, 'invalid_prophecy_sequence', {'slot': 'Prophecy'})
    from verify_design_deliverables import verify_seasonal_daily
    try:
        verify_seasonal_daily([r for r in source_rows if r.get('gregorian_date', '').startswith(f'{year}-')], daily, policy, complete_year=complete_year)
    except (AssertionError, RuntimeError) as error:
        issue('', 'invalid_seasonal_primary_table: ' + str(error), {})
    return source, package, skipped, dispositions, issues


def compare_copticchurch_cache(package_dir: Path = PACKAGE_DIR, source_index: Path = SOURCE_INDEX, years: list[int] | None = None, *, corrections_path: Path = CORRECTIONS) -> dict[str, Any]:
    meta = load_json(package_dir / "meta.json")
    shipped_years = years or list(meta.get("shipped_years", []))
    source_rows = load_csv(source_index)
    failures: list[dict[str, Any]] = []
    comparison_rows: list[dict[str, Any]] = []
    year_summaries: dict[str, Any] = {}

    policy = load_json(corrections_path)
    audit_dispositions = []
    for year in shipped_years:
        daily = load_json(package_dir / "data" / "daily" / f"lectionary-{year}.json")
        assert isinstance(daily, dict), "Daily file must be a JSON object keyed by date"
        package_total_rows = sum(len(rows) for rows in daily.values())
        # The canonical current sidecar declares full-year scope. An explicitly
        # supplied subset index is a bounded parity probe, not a full-year claim.
        source, package, skipped_structural_rows, dispositions, issues = contextual_counters(source_rows, daily, int(year), policy, complete_year=source_index.resolve() == SOURCE_INDEX.resolve())
        audit_dispositions.extend(dispositions)
        delta_rows = counter_delta_rows(int(year), source, package) + issues
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
        "source_snapshot": "legacy_preserved_snapshot" if source_index.name == LEGACY_SOURCE_INDEX.name else "reconciled_current_or_explicit_index",
        "preservation_only_not_primary_source_authentication": True,
        "audit_dispositions": audit_dispositions,
        "years": year_summaries,
        "comparison_rows": comparison_rows,
        "failures": failures,
        "status": "pass" if not failures else "fail",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cached-source preservation gate (not primary-source authentication).")
    parser.add_argument("--package-dir", type=Path, default=PACKAGE_DIR)
    source_choice = parser.add_mutually_exclusive_group()
    source_choice.add_argument("--source-index", type=Path, help="Explicit index; default is the reconciled current sidecar (no legacy fallback).")
    source_choice.add_argument("--legacy-snapshot", action="store_true", help="Diagnose the preserved historical index explicitly; not the current preservation gate.")
    parser.add_argument("--years", nargs="*", type=int)
    parser.add_argument("--output", type=Path, help="Optional JSON summary path.")
    parser.add_argument("--csv-output", type=Path, help="Optional CSV discrepancy output path.")
    args = parser.parse_args(argv)

    try:
        index = LEGACY_SOURCE_INDEX if args.legacy_snapshot else (args.source_index or SOURCE_INDEX)
        summary = compare_copticchurch_cache(args.package_dir, index, args.years)
    except (AssertionError, OSError, ValueError, RuntimeError) as exc:
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
