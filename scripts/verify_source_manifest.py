#!/usr/bin/env python3
"""Validate out/sources/SOURCE_MANIFEST.json against local source files."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCES_DIR = ROOT / "out" / "sources"
MANIFEST_NAME = "SOURCE_MANIFEST.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(sources_dir: Path) -> list[dict[str, Any]]:
    manifest_path = sources_dir / MANIFEST_NAME
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssertionError(f"Missing source manifest: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Invalid JSON in {manifest_path}: {exc}") from exc
    if not isinstance(manifest, list):
        raise AssertionError(f"{manifest_path} must be a JSON list")
    return manifest


def verify_source_manifest(sources_dir: Path = SOURCES_DIR) -> dict[str, Any]:
    manifest = load_manifest(sources_dir)
    failures: list[dict[str, Any]] = []
    seen: set[str] = set()

    for index, entry in enumerate(manifest, 1):
        if not isinstance(entry, dict):
            failures.append({"entry": index, "reason": "entry_not_object"})
            continue
        file_name = entry.get("file")
        if not file_name:
            failures.append({"entry": index, "reason": "missing_file_field"})
            continue
        if file_name == MANIFEST_NAME:
            raise AssertionError("SOURCE_MANIFEST.json must not list itself; self-hashes are not stable validation evidence")
        if "/" in file_name or "\\" in file_name or Path(file_name).name != file_name:
            failures.append({"entry": index, "file": file_name, "reason": "manifest_file_must_be_basename"})
            continue
        if file_name in seen:
            failures.append({"entry": index, "file": file_name, "reason": "duplicate_manifest_file"})
            continue
        seen.add(file_name)

        path = sources_dir / file_name
        if not path.exists():
            failures.append({"entry": index, "file": file_name, "reason": "missing_source_file"})
            continue
        actual_size = path.stat().st_size
        expected_size = entry.get("bytes")
        if expected_size != actual_size:
            failures.append({"entry": index, "file": file_name, "reason": "byte_count_mismatch", "expected": expected_size, "actual": actual_size})
        expected_sha = entry.get("sha256")
        actual_sha = sha256_file(path)
        if expected_sha != actual_sha:
            failures.append({"entry": index, "file": file_name, "reason": "sha256_mismatch", "expected": expected_sha, "actual": actual_sha})

    source_files = {path.name for path in sources_dir.iterdir() if path.is_file() and path.name != MANIFEST_NAME}
    unmanifested = sorted(source_files - seen)
    if unmanifested:
        failures.append({"reason": "unmanifested_source_files", "files": unmanifested})

    summary = {
        "sources_dir": str(sources_dir),
        "manifest": str(sources_dir / MANIFEST_NAME),
        "files_checked": len(seen),
        "failures": failures,
        "status": "pass" if not failures else "fail",
    }
    if failures:
        raise AssertionError(json.dumps(summary, indent=2))
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify source manifest hashes and byte counts.")
    parser.add_argument("--sources-dir", type=Path, default=SOURCES_DIR)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    try:
        summary = verify_source_manifest(args.sources_dir)
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
