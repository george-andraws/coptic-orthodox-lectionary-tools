from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import compare_external_sources as external_compare
from scripts import compare_package_active_equivalence as active_equivalence
from scripts import verify_calendar_coverage as calendar_coverage
from scripts import verify_package_integrity as package_integrity
from scripts import verify_source_manifest as source_manifest


class CalendarCoverageTests(unittest.TestCase):
    def test_julian_pascha_known_dates(self) -> None:
        self.assertEqual(calendar_coverage.julian_pascha_gregorian(2026), dt.date(2026, 4, 12))
        self.assertEqual(calendar_coverage.julian_pascha_gregorian(2027), dt.date(2027, 5, 2))
        self.assertEqual(calendar_coverage.julian_pascha_gregorian(2028), dt.date(2028, 4, 16))

    def test_holy_week_missing_date_is_classified_structural_gap(self) -> None:
        classification = calendar_coverage.classify_missing_date(dt.date(2026, 4, 6))
        self.assertEqual(classification["classification"], "holy_week_structural_only_not_in_daily")
        self.assertEqual(classification["expected_source"], "pascha_or_bright_saturday_structural_rows")
        self.assertEqual(classification["severity"], "known_gap")

    def test_non_holy_week_missing_date_is_unclassified_failure(self) -> None:
        classification = calendar_coverage.classify_missing_date(dt.date(2026, 1, 2))
        self.assertEqual(classification["classification"], "unclassified_missing_daily_date")
        self.assertEqual(classification["severity"], "fail")

    def test_missing_holy_week_date_fails_strict_complete_calendar(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = Path(tmp)
            daily_dir = package_dir / "data" / "daily"
            daily_dir.mkdir(parents=True)
            missing = "2026-04-06"
            start = dt.date(2026, 1, 1)
            end = dt.date(2026, 12, 31)
            daily = {
                (start + dt.timedelta(days=offset)).isoformat(): []
                for offset in range((end - start).days + 1)
                if (start + dt.timedelta(days=offset)).isoformat() != missing
            }
            (daily_dir / "lectionary-2026.json").write_text(json.dumps(daily), encoding="utf-8")
            meta = {
                "schemaVersion": "1.1.0",
                "shipped_years": [2026],
                "daily_files": [{"year": 2026, "rows": len(daily), "date_count": len(daily), "reading_count": 0}],
                "structural_date_resolver": {"missing_dates_by_year": {"2026": [{"date": missing}]}},
            }
            (package_dir / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "holy_week_structural_only_not_in_daily"):
                calendar_coverage.verify_calendar_coverage(package_dir, strict_complete_calendar=True)

    def test_current_package_has_complete_daily_coverage(self) -> None:
        summary = calendar_coverage.verify_calendar_coverage(calendar_coverage.PACKAGE_DIR, strict_complete_calendar=True)
        self.assertEqual(summary["status"], "pass")
        for year in ["2026", "2027", "2028"]:
            self.assertEqual(summary["years"][year]["missing_dates"], [])


class PackageIntegrityTests(unittest.TestCase):
    def test_context_passage_conflict_detects_lower_priority_overlap(self) -> None:
        def row(source_family: str, display_ref: str, spans_json: str) -> dict[str, str]:
            return {
                "occasion": "Wednesday of the first week of the holy fifty days" if source_family == "ordinary_date_resolved" else "Holy Fifty Days/Pentecost cycle",
                "calendar_keys": "Wednesday of the first week of the holy fifty days" if source_family == "ordinary_date_resolved" else "week 1 day_of_week 3",
                "day_titles": "Wednesday of the first week of the holy fifty days" if source_family == "ordinary_date_resolved" else "",
                "service_section": "Matins" if source_family == "ordinary_date_resolved" else "matins_gospel",
                "service_hour": "",
                "slot": "Gospel" if source_family == "ordinary_date_resolved" else "matins_gospel",
                "slot_type": "gospel",
                "source_family": source_family,
                "source_kind": "copticchurch_date" if source_family == "ordinary_date_resolved" else "katameros_cycle",
                "display_ref": display_ref,
                "identity_key": f"rid_{source_family}",
                "spans_json": spans_json,
                "removed_marker": "",
                "current_status": "current_public_or_local_reference",
            }

        conflicts = package_integrity.detect_context_passage_conflicts([
            row("katameros_cycle", "Jn 1:9-15", '[{"book":"Jn","chapter_start":1,"chapter_end":1,"verse_start":9,"verse_end":15}]'),
            row("ordinary_date_resolved", "Jn 1:9-14", '[{"book":"Jn","chapter_start":1,"chapter_end":1,"verse_start":9,"verse_end":14}]'),
        ])
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["preferred_source_family"], "ordinary_date_resolved")
        self.assertEqual(conflicts[0]["lower_priority_source_family"], "katameros_cycle")

    def test_context_passage_conflict_detects_bare_chapter_end_shorthand(self) -> None:
        def row(source_family: str, occasion: str, calendar_keys: str, service_section: str, slot: str, slot_type: str, display_ref: str, span: dict[str, int | str]) -> dict[str, str]:
            return {
                "occasion": occasion,
                "calendar_keys": calendar_keys,
                "day_titles": occasion if source_family == "ordinary_date_resolved" else "",
                "service_section": service_section,
                "service_hour": "",
                "slot": slot,
                "slot_type": slot_type,
                "source_family": source_family,
                "source_kind": "copticchurch_date" if source_family == "ordinary_date_resolved" else "katameros_cycle",
                "display_ref": display_ref,
                "canonical_mt_ref": display_ref,
                "identity_key": f"rid_{source_family}_{display_ref}",
                "spans_json": json.dumps([span]),
                "removed_marker": "",
                "current_status": "current_public_or_local_reference",
            }

        conflicts = package_integrity.detect_context_passage_conflicts([
            row("ordinary_date_resolved", "Friday of the first week of Great Lent", "Friday of the first week of Great Lent", "Liturgy", "Acts of the Apostles", "praxis", "Acts 2:42-3:9", {"book": "Acts", "chapter_start": 2, "chapter_end": 3, "verse_start": 42, "verse_end": 9}),
            row("katameros_cycle", "Great Lent/Jonah/Nineveh cycle", "week 1 day_of_week 5", "liturgy_acts", "liturgy_acts", "praxis", "Acts 2:42-3", {"book": "Acts", "chapter_start": 2, "chapter_end": 2, "verse_start": 42, "verse_end": 3}),
            row("ordinary_date_resolved", "Monday of the first week of the holy fifty days", "Monday of the first week of the holy fifty days", "Liturgy", "Pauline Epistle", "pauline", "1Thess 4:13-5:11", {"book": "1Thess", "chapter_start": 4, "chapter_end": 5, "verse_start": 13, "verse_end": 11}),
            row("katameros_cycle", "Holy Fifty Days/Pentecost cycle", "week 1 day_of_week 1", "liturgy_pauline", "liturgy_pauline", "pauline", "1Thess 4:13-5", {"book": "1Thess", "chapter_start": 4, "chapter_end": 4, "verse_start": 13, "verse_end": 5}),
        ])
        self.assertEqual(len(conflicts), 2)
        self.assertEqual({conflict["lower_priority_source_family"] for conflict in conflicts}, {"katameros_cycle"})

    def test_legacy_month_spellings_are_detected(self) -> None:
        rows = [
            {"occasion": "Kiak 23", "calendar_keys": "Kiak 23", "day_titles": "Kiak 23"},
            {"occasion": "Baba 6", "calendar_keys": "Baba 6", "day_titles": "Baba 6"},
            {"occasion": "Kiahk 23", "calendar_keys": "Babah 6", "day_titles": ""},
        ]
        findings = package_integrity.find_legacy_month_spellings(rows)
        self.assertEqual({finding["legacy"] for finding in findings}, {"Kiak", "Baba"})

    def test_daily_counts_separates_date_count_from_reading_count(self) -> None:
        counts = package_integrity.daily_counts({
            "2026-01-01": [{"display_ref": "Jn 1:1-17"}, {"display_ref": "Ps 1"}],
            "2026-01-02": [],
        })
        self.assertEqual(counts, {"date_count": 2, "reading_count": 2})

    def test_count_jsonl_rows_ignores_blank_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.jsonl"
            path.write_text('{"a": 1}\n\n{"b": 2}\n', encoding="utf-8")
            self.assertEqual(package_integrity.count_jsonl_rows(path), 2)

    def test_parse_jsonl_reports_bad_line_number(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.jsonl"
            path.write_text('{"a": 1}\nnot-json\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "line 2"):
                package_integrity.parse_jsonl(path)
    def test_removed_projection_rows_are_ignored_by_context_conflict_detector(self) -> None:
        preferred = {
            "occasion": "Friday of the first week of Great Lent",
            "calendar_keys": "Friday of the first week of Great Lent",
            "day_titles": "Friday of the first week of Great Lent",
            "service_section": "Liturgy",
            "service_hour": "",
            "slot": "Acts of the Apostles",
            "slot_type": "praxis",
            "source_family": "ordinary_date_resolved",
            "display_ref": "Acts 2:42-3:9",
            "canonical_mt_ref": "Acts 2:42-3:9",
            "identity_key": "rid_preferred",
            "spans_json": '[{"book":"Acts","chapter_start":2,"chapter_end":3,"verse_start":42,"verse_end":9}]',
            "removed_marker": "",
            "current_status": "current_public_or_local_reference",
        }
        removed = {
            "occasion": "Great Lent/Jonah/Nineveh cycle",
            "calendar_keys": "week 1 day_of_week 5",
            "day_titles": "",
            "service_section": "liturgy_acts",
            "service_hour": "",
            "slot": "liturgy_acts",
            "slot_type": "praxis",
            "source_family": "katameros_cycle",
            "display_ref": "Acts 2:42-3",
            "canonical_mt_ref": "Acts 2:42-3",
            "identity_key": "rid_removed",
            "spans_json": '[{"book":"Acts","chapter_start":2,"chapter_end":2,"verse_start":42,"verse_end":3}]',
            "active": False,
            "status": "removed",
            "removed_marker": "removed_by_source_priority_projection",
            "removal_reason": "lower_priority_overlap_with_date_resolved_source",
            "preferred_source_family": "ordinary_date_resolved",
            "preferred_display_ref": "Acts 2:42-3:9",
            "consumer_note": "Retained for provenance only. Ignore by default in active lookups.",
        }
        self.assertEqual(package_integrity.detect_context_passage_conflicts([preferred, removed]), [])

    def test_removed_projection_rows_require_user_facing_annotation(self) -> None:
        rows = [{"active": False, "status": "removed", "display_ref": "Acts 2:42-3"}]
        failures = package_integrity.validate_removed_projection_rows(rows)
        self.assertEqual(failures[0]["reason"], "removed_projection_row_missing_annotation")
        self.assertIn("consumer_note", failures[0]["missing_fields"])


class ActiveEquivalenceTests(unittest.TestCase):
    def write_package(self, package_dir: Path, reverse_rows: list[dict], daily: dict[str, dict]) -> None:
        (package_dir / "data" / "daily").mkdir(parents=True)
        (package_dir / "data" / "reverse_lectionary_index.jsonl").write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in reverse_rows),
            encoding="utf-8",
        )
        for year, data in daily.items():
            (package_dir / "data" / "daily" / f"lectionary-{year}.json").write_text(json.dumps(data, sort_keys=True), encoding="utf-8")

    def test_active_equivalence_allows_extra_removed_rows_only(self) -> None:
        active_row = {"occasion": "A", "service_section": "Liturgy", "service_hour": "", "slot": "Gospel", "identity_key": "rid_active", "display_ref": "Jn 1:1-17"}
        removed_row = {"occasion": "B", "service_section": "Liturgy", "service_hour": "", "slot": "Gospel", "identity_key": "rid_removed", "display_ref": "Acts 2:42-3", "active": False, "status": "removed"}
        with tempfile.TemporaryDirectory() as tmp:
            baseline = Path(tmp) / "baseline"
            candidate = Path(tmp) / "candidate"
            daily = {"2026": {"2026-01-01": [{"display_ref": "Jn 1:1-17"}]}}
            self.write_package(baseline, [active_row], daily)
            self.write_package(candidate, [active_row, removed_row], daily)
            summary = active_equivalence.compare_packages(baseline, candidate)
            self.assertEqual(summary["status"], "pass")
            self.assertEqual(summary["candidate_removed_rows"], 1)

    def test_active_equivalence_fails_when_active_rows_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            baseline = Path(tmp) / "baseline"
            candidate = Path(tmp) / "candidate"
            daily = {"2026": {"2026-01-01": []}}
            self.write_package(baseline, [{"identity_key": "rid_a", "display_ref": "Jn 1:1-17"}], daily)
            self.write_package(candidate, [{"identity_key": "rid_b", "display_ref": "Lk 1:1-4"}], daily)
            summary = active_equivalence.compare_packages(baseline, candidate)
            self.assertEqual(summary["status"], "fail")
            self.assertTrue(summary["failures"])


class SourceManifestTests(unittest.TestCase):
    def test_manifest_rejects_self_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sources = Path(tmp)
            (sources / "SOURCE_MANIFEST.json").write_text(
                json.dumps([{"file": "SOURCE_MANIFEST.json", "bytes": 2, "sha256": "x"}]),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(AssertionError, "must not list itself"):
                source_manifest.verify_source_manifest(sources)

    def test_manifest_verifies_file_hash_and_size(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sources = Path(tmp)
            data = sources / "sample.txt"
            data.write_text("abc", encoding="utf-8")
            digest = source_manifest.sha256_file(data)
            (sources / "SOURCE_MANIFEST.json").write_text(
                json.dumps([{"file": "sample.txt", "bytes": 3, "sha256": digest}]),
                encoding="utf-8",
            )
            summary = source_manifest.verify_source_manifest(sources)
            self.assertEqual(summary["files_checked"], 1)
            self.assertEqual(summary["status"], "pass")


class ExternalComparisonTests(unittest.TestCase):
    def test_reference_normalization_strips_inline_lxx_display(self) -> None:
        self.assertEqual(
            external_compare.normalize_reference_for_compare("Ps 105:14-15 (LXX Ps 104:14-15)"),
            external_compare.normalize_reference_for_compare("Ps 105:14-15"),
        )

    def test_counter_delta_reports_missing_and_extra(self) -> None:
        left = external_compare.Counter({("2026-01-01", "Liturgy", "Gospel", "Jn 1:1-17"): 1})
        right = external_compare.Counter({("2026-01-01", "Liturgy", "Gospel", "Lk 1:1-4"): 1})
        rows = external_compare.counter_delta_rows(2026, left, right)
        self.assertEqual({row["status"] for row in rows}, {"source_only_missing_from_package", "package_only_extra_vs_source"})
    def test_package_counter_skips_structural_daily_rows_for_copticchurch_compare(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = Path(tmp)
            daily_dir = package_dir / "data" / "daily"
            daily_dir.mkdir(parents=True)
            (daily_dir / "lectionary-2026.json").write_text(json.dumps({
                "2026-04-10": [
                    {"service_section": "First Hour", "slot": "Gospel", "display_ref": "Jn 18:1-11", "structural_day": "Good Friday", "source_family": "holy_pascha_curated_day_hour"},
                    {"service_section": "Liturgy", "slot": "Gospel", "display_ref": "Jn 1:1-17"},
                ]
            }), encoding="utf-8")
            counter, total, skipped = external_compare.package_counter(package_dir, 2026)
            self.assertEqual(total, 2)
            self.assertEqual(skipped, 1)
            self.assertEqual(sum(counter.values()), 1)


if __name__ == "__main__":
    unittest.main()
