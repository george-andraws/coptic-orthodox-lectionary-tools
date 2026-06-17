#!/usr/bin/env python3
"""Build a lectionary data change manifest from git history."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import subprocess
from collections import Counter, defaultdict
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out" / "design"
MANIFEST_CSV = OUT / "lectionary_change_manifest.csv"
RAW_MANIFEST_GZ = OUT / "lectionary_change_manifest.raw.csv.gz"
AFFECTED_CSV = OUT / "affected_passages.csv"
MANIFEST_MD = OUT / "lectionary_change_manifest.md"
LOG_PATH = ROOT / "audit_artifacts" / "lectionary_execution_log.md"

DATA_PREFIXES = ("out/design/", "out/data/")
DATA_SUFFIXES = (".csv",)
EXCLUDED_DATA_PATHS = {
    "out/design/lectionary_change_manifest.csv",
    "out/design/affected_passages.csv",
}

SELECTED_VALUE_FIELDS = [
    "identity_key",
    "reading_identity_key",
    "display_ref",
    "canonical_mt_ref",
    "canonical_lxx_ref",
    "source_ref",
    "raw_ref",
    "source_label",
    "source_key",
    "source_title",
    "source_edition",
    "source_locator",
    "current_status",
    "lifecycle_status",
    "removed_marker",
    "basis",
    "confidence",
    "citation",
    "provenance",
    "status_note",
    "day_title",
    "occasion",
    "calendar_key",
    "service_day",
    "service_hour",
    "service_section",
    "slot",
    "reading_slot",
    "order",
    "commem_id",
    "commemoration_title",
    "membership_verdict",
    "membership_status",
]

BOOK_ORDER = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther",
    "Job", "Psalm", "Psalms", "Proverbs", "Ecclesiastes", "Song of Songs", "Wisdom", "Sirach",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation",
]
BOOK_RANK = {book: i for i, book in enumerate(BOOK_ORDER)}
BOOK_ALIASES = {
    "Gen": "Genesis", "Ex": "Exodus", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers", "Deut": "Deuteronomy",
    "Josh": "Joshua", "Judg": "Judges", "Ruth": "Ruth", "1Sam": "1 Samuel", "2Sam": "2 Samuel",
    "1Kgs": "1 Kings", "2Kgs": "2 Kings", "1Chr": "1 Chronicles", "2Chr": "2 Chronicles",
    "Ezra": "Ezra", "Neh": "Nehemiah", "Esth": "Esther", "Job": "Job", "Ps": "Psalm", "Pss": "Psalms",
    "Prov": "Proverbs", "Eccl": "Ecclesiastes", "Song": "Song of Songs", "Wis": "Wisdom", "Sir": "Sirach",
    "Isa": "Isaiah", "Jer": "Jeremiah", "Lam": "Lamentations", "Ezek": "Ezekiel", "Dan": "Daniel",
    "Hos": "Hosea", "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah", "Jon": "Jonah", "Mic": "Micah",
    "Nah": "Nahum", "Hab": "Habakkuk", "Zeph": "Zephaniah", "Hag": "Haggai", "Zech": "Zechariah", "Mal": "Malachi",
    "Matt": "Matthew", "Mt": "Matthew", "Mark": "Mark", "Mk": "Mark", "Luke": "Luke", "Lk": "Luke", "John": "John", "Jn": "John",
    "Acts": "Acts", "Rom": "Romans", "1Cor": "1 Corinthians", "2Cor": "2 Corinthians", "Gal": "Galatians", "Eph": "Ephesians", "Phil": "Philippians", "Col": "Colossians",
    "1Thess": "1 Thessalonians", "2Thess": "2 Thessalonians", "1Tim": "1 Timothy", "2Tim": "2 Timothy", "Tit": "Titus", "Phlm": "Philemon", "Heb": "Hebrews", "Jas": "James", "1Pet": "1 Peter", "2Pet": "2 Peter", "1Jn": "1 John", "2Jn": "2 John", "3Jn": "3 John", "Rev": "Revelation",
}

FIELD_PRIORITY = {
    "out/design/reading_identity.csv": ["identity_key"],
    "out/design/reverse_lectionary_presentation.csv": ["identity_key", "source_key", "source_file", "source_row_id", "occasion", "calendar_key", "day_title", "service_hour", "slot", "order", "source_ref"],
    "out/design/todays_readings_current_practice.csv": ["identity_key", "source_key", "source_file", "source_row_id", "occasion", "calendar_key", "day_title", "service_hour", "slot", "order", "source_ref"],
    "out/design/pascha_attestation.csv": ["day_title", "service_hour", "identity_key", "display_ref"],
    "out/design/temporal_classification.csv": ["day_title", "service_hour", "identity_key", "display_ref"],
    "out/design/temporal_residue.csv": ["day_title", "service_hour", "identity_key", "display_ref", "residue_type"],
    "out/design/temporal_residue_manifest.csv": ["residue_type"],
    "out/design/pascha_attestation_bucket_manifest.csv": ["bucket"],
    "out/design/psalm_mt_lxx_crosswalk.csv": ["mt_psalm", "lxx_psalm", "map_direction", "mapping_scope", "note"],
    "out/design/synaxarium_commemorations.csv": ["commem_id"],
    "out/design/synaxarium_reading_bridge.csv": ["commem_id", "coptic_day_key", "reading_identity_key", "slot", "display_ref"],
    "out/design/passage_liturgical_footprint.csv": ["identity_key"],
    "out/design/source_registry.csv": ["source_key"],
    "out/design/passage_source_disclosure.csv": ["identity_key", "source_key", "source_locator", "occasion", "calendar_key", "day_title", "service_hour", "slot", "source_ref"],
    "out/design/foundational_reading_collections_69.csv": ["collection_key"],
}


def run_git(args: list[str]) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout


def git_show(commit: str, path: str) -> str | None:
    proc = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    return proc.stdout


def list_commits(baseline: str, head: str) -> list[dict]:
    text = run_git(["log", "--reverse", "--pretty=format:%H%x00%P%x00%s", f"{baseline}..{head}"])
    commits = []
    for line in text.splitlines():
        if not line.strip():
            continue
        sha, parents, subject = line.split("\x00")
        parent = parents.split()[0] if parents else f"{sha}^"
        commits.append({"sha": sha, "parent": parent, "subject": subject})
    return commits


def changed_data_paths(parent: str, sha: str) -> list[str]:
    text = run_git(["diff", "--name-only", parent, sha])
    paths = []
    for path in text.splitlines():
        if path in EXCLUDED_DATA_PATHS:
            continue
        if path.startswith(DATA_PREFIXES) and path.endswith(DATA_SUFFIXES):
            paths.append(path)
    return sorted(paths)


def read_csv_text(text: str | None) -> tuple[list[str], list[dict]]:
    if text is None or not text.strip():
        return [], []
    reader = csv.DictReader(StringIO(text))
    return list(reader.fieldnames or []), list(reader)


def stable_key(path: str, row: dict, index: int) -> str:
    fields = [field for field in FIELD_PRIORITY.get(path, []) if field in row]
    if not fields:
        fields = [field for field in ["identity_key", "display_ref", "source_key", "source_row_id", "source_ref", "day_title", "service_hour", "slot", "order"] if field in row]
    if not fields:
        fields = sorted(row)
    values = [str(row.get(field, "")) for field in fields]
    if any(values):
        return "|".join(f"{field}={row.get(field, '')}" for field in fields)
    return f"row_index={index}|row={json.dumps(row, sort_keys=True, ensure_ascii=False)}"


def index_rows(path: str, rows: list[dict]) -> dict[str, dict]:
    indexed = {}
    collisions = Counter()
    for i, row in enumerate(rows):
        key = stable_key(path, row, i)
        if key in indexed:
            collisions[key] += 1
            key = f"{key}|duplicate_index={collisions[key]}"
        indexed[key] = row
    return indexed


def shorten(value: object, limit: int = 80) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def row_digest(row: dict) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def selected_value(row: dict | None) -> str:
    if not row:
        return ""
    parts = [f"row_sha256={row_digest(row)}"]
    for field in ["identity_key", "reading_identity_key", "display_ref", "source_key", "current_status", "removed_marker"]:
        value = row.get(field)
        if value not in (None, ""):
            parts.append(f"{field}={shorten(value, 48)}")
    return "; ".join(parts)


def affected_passage(before: dict | None, after: dict | None) -> str:
    row = after or before or {}
    for field in ["display_ref", "canonical_mt_ref", "source_ref", "raw_ref", "source_label", "canonical_lxx_ref"]:
        value = (row.get(field) or "").strip()
        if value:
            lxx = str(row.get("canonical_lxx_ref") or "")
            if lxx and lxx not in value and "LXX" not in value:
                value = f"{value} (LXX {lxx})"
            return re.sub(r"\s+", " ", value)
    return ""


def occasion_path(before: dict | None, after: dict | None) -> str:
    row = after or before or {}
    parts = []
    for field in ["occasion", "calendar_key", "day_title", "service_day", "service_hour", "service_section", "slot", "reading_slot", "order", "commemoration_title", "coptic_day_key"]:
        value = shorten(row.get(field, ""), 40)
        if value and value not in parts:
            parts.append(value)
    return shorten(" | ".join(parts), 220)


def basis_or_source(path: str, before: dict | None, after: dict | None) -> str:
    row = after or before or {}
    parts = [path]
    for field in ["source_key", "basis", "confidence", "current_status"]:
        value = str(row.get(field, "") or "").strip()
        if value:
            parts.append(f"{field}={shorten(value, 40)}")
    return "; ".join(parts)


def classify_change(path: str, subject: str, before: dict | None, after: dict | None) -> str:
    subj = subject.lower()
    if before is None and after is not None:
        if after.get("removed_marker") or after.get("current_status") == "historical_candidate_removed":
            return "removed_marked_historical"
        return "added"
    if before is not None and after is None:
        if "duplicate" in subj or "dedupe" in subj:
            return "deduped"
        if before.get("removed_marker") or before.get("current_status") == "historical_candidate_removed":
            return "removed_marked_historical"
        return "other"
    if before is None or after is None:
        return "other"
    if path.endswith("synaxarium_reading_bridge.csv") and (before.get("basis") != after.get("basis") or before.get("confidence") != after.get("confidence")):
        return "bridge_basis_changed"
    if before.get("removed_marker") != after.get("removed_marker") or after.get("removed_marker"):
        return "removed_marked_historical"
    if any(before.get(f) != after.get(f) for f in ["canonical_mt_ref", "canonical_lxx_ref", "source_convention", "canonicalization_note", "spans_json"]):
        return "renumbered_MT_LXX"
    provenance_fields = ["source_key", "source_title", "source_edition", "source_locator", "source_url", "citation", "provenance", "authority_tier"]
    if path.endswith("passage_source_disclosure.csv") or path.endswith("source_registry.csv") or any(before.get(f) != after.get(f) for f in provenance_fields):
        return "provenance_added"
    if any(before.get(f) != after.get(f) for f in ["display_ref", "source_label", "raw_ref", "reading_name", "title", "commemoration_title", "membership_verdict", "membership_status"]):
        return "relabeled"
    if "duplicate" in subj or "dedupe" in subj:
        return "deduped"
    return "other"


def phase_for(subject: str, sha: str) -> str:
    low = subject.lower()
    for phase in range(0, 8):
        if f"phase {phase}" in low:
            return f"Phase {phase}"
    if "rekey" in low or "rekeyed" in low:
        return "Phase 2"
    if "attestation" in low:
        return "Phase 3"
    if "temporal" in low or "removed" in low:
        return "Phase 4/7"
    if "synaxarium" in low or "bridge" in low:
        return "Phase 5/7"
    if "foundational" in low or "69" in low:
        return "Phase 7"
    if "source disclosure" in low or "provenance" in low:
        return "Phase 7"
    return "Unlabeled"


def normalize_book(raw: str) -> tuple[str, int]:
    text = raw.strip()
    text = re.sub(r"\(.*?\)", "", text)
    match = re.match(r"(?P<book>(?:[1234]\s*)?[A-Za-z][A-Za-z.\- ]*?)\s*(?P<chapter>\d+)", text)
    if not match:
        return "", 0
    book = match.group("book").strip().replace(".", "")
    book = re.sub(r"\s+", "", book) if re.match(r"^[1234]\s", book) else book
    book = BOOK_ALIASES.get(book, BOOK_ALIASES.get(book.replace(" ", ""), book))
    chapter = int(match.group("chapter"))
    return book, chapter


def split_passages(value: str) -> list[str]:
    if not value:
        return []
    if value.lower() in {"n/a", "none"}:
        return []
    # Keep composite displays intact unless they contain clear semicolon-separated passages.
    parts = [p.strip() for p in re.split(r"\s*;\s*", value) if p.strip()]
    return parts or [value]


def build_manifest(baseline: str, head: str) -> tuple[list[dict], dict]:
    commits = list_commits(baseline, head)
    manifest = []
    data_diff_commits = set()
    commit_subjects = {}
    for commit in commits:
        sha = commit["sha"]
        parent = commit["parent"]
        subject = commit["subject"]
        commit_subjects[sha[:7]] = subject
        paths = changed_data_paths(parent, sha)
        if paths:
            data_diff_commits.add(sha[:7])
        for path in paths:
            before_header, before_rows = read_csv_text(git_show(parent, path))
            after_header, after_rows = read_csv_text(git_show(sha, path))
            before_index = index_rows(path, before_rows)
            after_index = index_rows(path, after_rows)
            for key in sorted(set(before_index) | set(after_index)):
                before = before_index.get(key)
                after = after_index.get(key)
                if before == after:
                    continue
                change_type = classify_change(path, subject, before, after)
                row = {
                    "affected_passage_or_passages": affected_passage(before, after),
                    "occasion_service_hour_slot": occasion_path(before, after),
                    "change_type": change_type,
                    "before_value": selected_value(before),
                    "after_value": selected_value(after),
                    "commit_hash": sha,
                    "phase": phase_for(subject, sha),
                    "basis_or_source": basis_or_source(path, before, after),
                }
                manifest.append(row)
    metadata = {"data_diff_commits": data_diff_commits, "commit_subjects": commit_subjects, "commits": commits}
    return manifest, metadata


def truncate_value(value: str, limit: int = 180) -> str:
    value = value.replace("\n", " ")
    return value if len(value) <= limit else value[: limit - 3] + "..."


def aggregate_manifest(raw_manifest: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str, str, str, str], dict] = {}
    for row in raw_manifest:
        source_path = row["basis_or_source"].split(";", 1)[0]
        key = (
            row["affected_passage_or_passages"],
            row["change_type"],
            row["commit_hash"],
            row["phase"],
            source_path,
        )
        group = groups.setdefault(
            key,
            {
                "affected_passage_or_passages": row["affected_passage_or_passages"],
                "change_type": row["change_type"],
                "commit_hash": row["commit_hash"],
                "phase": row["phase"],
                "source_path": source_path,
                "count": 0,
                "occasion_samples": [],
                "before_samples": [],
                "after_samples": [],
                "basis_samples": [],
            },
        )
        group["count"] += 1
        occasion = row.get("occasion_service_hour_slot", "")
        if occasion and len(group["occasion_samples"]) < 3:
            clipped_occasion = truncate_value(occasion)
            if clipped_occasion not in group["occasion_samples"]:
                group["occasion_samples"].append(clipped_occasion)
        for sample_key, value_key in [("before_samples", "before_value"), ("after_samples", "after_value"), ("basis_samples", "basis_or_source")]:
            value = row.get(value_key, "")
            if value and len(group[sample_key]) < 1:
                clipped = truncate_value(value)
                if clipped not in group[sample_key]:
                    group[sample_key].append(clipped)
    aggregated = []
    for group in groups.values():
        before = f"compressed_row_count={group['count']}"
        after = f"compressed_row_count={group['count']}"
        if group["before_samples"]:
            before += "; samples=" + " || ".join(group["before_samples"])
        if group["after_samples"]:
            after += "; samples=" + " || ".join(group["after_samples"])
        basis = group["source_path"]
        if group["basis_samples"]:
            basis += "; samples=" + " || ".join(group["basis_samples"])
        occasion = f"compressed_placement_count={group['count']}"
        if group["occasion_samples"]:
            occasion += "; samples=" + " || ".join(group["occasion_samples"])
        aggregated.append({
            "affected_passage_or_passages": group["affected_passage_or_passages"],
            "occasion_service_hour_slot": occasion,
            "change_type": group["change_type"],
            "before_value": before,
            "after_value": after,
            "commit_hash": group["commit_hash"],
            "phase": group["phase"],
            "basis_or_source": basis,
        })
    aggregated.sort(key=lambda r: (r["commit_hash"], r["basis_or_source"], r["affected_passage_or_passages"], r["occasion_service_hour_slot"], r["change_type"]))
    return aggregated


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_raw_manifest_gz(rows: list[dict], fields: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with RAW_MANIFEST_GZ.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            wrapper = io.TextIOWrapper(gz, encoding="utf-8", newline="")
            writer = csv.DictWriter(wrapper, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
            wrapper.flush()


def write_outputs(manifest: list[dict], metadata: dict, baseline: str, head: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fields = ["affected_passage_or_passages", "occasion_service_hour_slot", "change_type", "before_value", "after_value", "commit_hash", "phase", "basis_or_source"]
    write_csv(MANIFEST_CSV, manifest, fields)

    affected_count: Counter[str] = Counter()
    affected_change_types: dict[str, Counter[str]] = defaultdict(Counter)
    affected_commits: dict[str, set[str]] = defaultdict(set)
    affected_book: dict[str, str] = {}
    affected_chapter: dict[str, int] = {}
    for row in manifest:
        for passage in split_passages(row["affected_passage_or_passages"]):
            book, chapter = normalize_book(passage)
            if not book:
                continue
            affected_count[passage] += 1
            affected_change_types[passage][row["change_type"]] += 1
            affected_commits[passage].add(row["commit_hash"][:7])
            affected_book[passage] = book
            affected_chapter[passage] = chapter
    affected_rows = []
    for passage, count in affected_count.items():
        affected_rows.append({
            "book": affected_book[passage],
            "chapter": affected_chapter[passage],
            "affected_passage": passage,
            "change_count": count,
            "change_types": "; ".join(sorted(affected_change_types[passage])),
            "commits": "; ".join(sorted(affected_commits[passage])),
        })
    affected_rows.sort(key=lambda r: (BOOK_RANK.get(r["book"], 999), int(r["chapter"] or 0), r["affected_passage"]))
    with AFFECTED_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["book", "chapter", "affected_passage", "change_count", "change_types", "commits"])
        writer.writeheader()
        writer.writerows(affected_rows)

    type_counts = Counter(row["change_type"] for row in manifest)
    book_counts = Counter()
    for r in affected_rows:
        book_counts[r["book"]] += int(r["change_count"])

    log_text = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() else ""
    logged_hashes = set(re.findall(r"\b[0-9a-f]{7,40}\b", log_text))
    logged_short = {h[:7] for h in logged_hashes}
    logged_with_no_data = sorted(h for h in logged_short if h in metadata["commit_subjects"] and h not in metadata["data_diff_commits"])
    data_without_log = sorted(h for h in metadata["data_diff_commits"] if h not in logged_short)

    md = []
    md.append("# Lectionary Change Manifest")
    md.append("")
    md.append(f"Baseline: `{baseline}`")
    md.append(f"Data range HEAD: `{head}`")
    md.append("The manifest files themselves are excluded from future data-diff scans to avoid recursive diffs.")
    md.append(f"Grouped manifest rows: {len(manifest)}")
    if metadata.get("raw_change_rows"):
        md.append(f"Exact raw row-level CSV changes archived: {metadata['raw_change_rows']}")
    md.append(f"Affected passage keys: {len(affected_rows)}")
    md.append("")
    md.append("## Totals by change type")
    md.append("")
    for change_type, count in sorted(type_counts.items()):
        md.append(f"- `{change_type}`: {count}")
    md.append("")
    md.append("## Totals by book")
    md.append("")
    for book, count in sorted(book_counts.items(), key=lambda item: (BOOK_RANK.get(item[0], 999), item[0])):
        md.append(f"- {book}: {count}")
    md.append("")
    md.append("## Affected passages")
    md.append("")
    for row in affected_rows:
        md.append(f"- {row['affected_passage']} ({row['change_count']} changes; {row['change_types']})")
    md.append("")
    md.append("## Execution-log cross-check")
    md.append("")
    if logged_with_no_data:
        md.append("Logged commits in the baseline range with no committed CSV data diff:")
        for h in logged_with_no_data:
            md.append(f"- `{h}` {metadata['commit_subjects'].get(h, '')}")
    else:
        md.append("No logged baseline-range commits lacked a CSV data diff.")
    md.append("")
    if data_without_log:
        md.append("Committed CSV data diffs not explicitly found in the execution log:")
        for h in data_without_log:
            md.append(f"- `{h}` {metadata['commit_subjects'].get(h, '')}")
    else:
        md.append("Every committed CSV data-diff commit in the baseline range was found in the execution log by hash.")
    md.append("")
    md.append("## Artifact paths")
    md.append("")
    md.append(f"- Grouped review manifest: `{MANIFEST_CSV.relative_to(ROOT)}`")
    md.append(f"- Exact row-level manifest gzip: `{RAW_MANIFEST_GZ.relative_to(ROOT)}`")
    md.append(f"- Affected-passage index: `{AFFECTED_CSV.relative_to(ROOT)}`")
    MANIFEST_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", default="lectionary-baseline")
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args()
    baseline = run_git(["rev-parse", args.baseline]).strip()
    head = run_git(["rev-parse", args.head]).strip()
    raw_manifest, metadata = build_manifest(baseline, head)
    metadata["raw_change_rows"] = len(raw_manifest)
    fields = ["affected_passage_or_passages", "occasion_service_hour_slot", "change_type", "before_value", "after_value", "commit_hash", "phase", "basis_or_source"]
    write_raw_manifest_gz(raw_manifest, fields)
    manifest = aggregate_manifest(raw_manifest)
    write_outputs(manifest, metadata, baseline, head)
    print(json.dumps({
        "baseline": baseline,
        "head": head,
        "manifest_rows": len(manifest),
        "raw_change_rows": len(raw_manifest),
        "data_diff_commits": sorted(metadata["data_diff_commits"]),
        "manifest_path": str(MANIFEST_CSV.relative_to(ROOT)),
        "raw_manifest_path": str(RAW_MANIFEST_GZ.relative_to(ROOT)),
        "affected_path": str(AFFECTED_CSV.relative_to(ROOT)),
        "summary_path": str(MANIFEST_MD.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
