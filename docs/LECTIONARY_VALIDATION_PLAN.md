# Lectionary Data Validation Plan

Last updated: 2026-06-19

## Purpose

This document defines the release validation plan for the Coptic lectionary data package and generated design artifacts. The goal is to prove, with repeatable checks, that the data is structurally valid, source-backed, findable by date and passage, free of unclassified duplicates/loss, and honestly classified against available authority sources.

This is not a one-file diff. The lectionary data has multiple layers:

1. raw and copied source files
2. parsed source indexes under `out/data/`
3. design-layer artifacts under `out/design/`
4. runtime package files under `packages/lectionary-data/`
5. optional npm tarball produced from the package directory

Each layer has a separate validation gate.

## Authority model

Use source authority tiers. Do not merge all sources into one undifferentiated truth set.

| Tier | Source | Role |
|---|---|---|
| 1 | Coptic Reader locked fixtures | Current-practice authority only inside captured fixture scope |
| 2 | copticchurch.net date-resolved readings | Public current-practice reference for daily readings |
| 3 | Katameros SQLite/API source | Structured cycle source for annual, Sunday, Great Lent, and Holy Fifty readings |
| 4 | St. Mary Ottawa / UKMID Katameros PDFs and extracted text | Printed witness, Pascha source text, and historical comparison |
| 5 | Curated special-service, Bright Saturday, and Agpeya data | Local structured source with explicit provenance |
| 6 | Synaxarium bridge | Discovery-link layer only, not proof of assigned proper readings |

Rules:

- Coptic Reader governs only where fixture/captured data exists.
- Do not invent Coptic Reader extraction. Use locked fixtures or a documented reproducible access path.
- Printed Pascha witnesses are retained and classified. They are not automatically current authority when Coptic Reader differs.
- Synaxarium bridge rows must show basis/confidence and must not be presented as direct proper-reading proof.
- Psalm comparisons must normalize MT/LXX numbering before diffing.

## Release validation commands

Run from repo root:

```bash
python3 -m unittest tests/test_validation_scripts.py
python3 -m py_compile \
  scripts/verify_calendar_coverage.py \
  scripts/verify_package_integrity.py \
  scripts/verify_source_manifest.py \
  scripts/compare_external_sources.py \
  tests/test_validation_scripts.py
python3 verify_design_deliverables.py
python3 verify_lectionary_queries.py
python3 scripts/verify_source_manifest.py
python3 scripts/verify_calendar_coverage.py --strict-complete-calendar
python3 scripts/compare_external_sources.py
python3 scripts/verify_package_integrity.py
python3 scripts/verify_package_integrity.py --tarball packages/lectionary-data/andraws-lectionary-data-<version>.tgz
git diff --check
```

For a JSON/CSV audit packet, run:

```bash
mkdir -p audit_artifacts/validation_release_gate_YYYY-MM-DD
python3 scripts/verify_source_manifest.py \
  --output audit_artifacts/validation_release_gate_YYYY-MM-DD/source_manifest.json
python3 scripts/verify_calendar_coverage.py \
  --strict-complete-calendar \
  --output audit_artifacts/validation_release_gate_YYYY-MM-DD/calendar_coverage.json
python3 scripts/compare_external_sources.py \
  --output audit_artifacts/validation_release_gate_YYYY-MM-DD/copticchurch_comparison.json \
  --csv-output audit_artifacts/validation_release_gate_YYYY-MM-DD/copticchurch_comparison.csv
python3 scripts/verify_package_integrity.py \
  --output audit_artifacts/validation_release_gate_YYYY-MM-DD/package_integrity.json
python3 scripts/verify_package_integrity.py \
  --tarball packages/lectionary-data/andraws-lectionary-data-<version>.tgz \
  --output audit_artifacts/validation_release_gate_YYYY-MM-DD/package_tarball_integrity.json
```

## Gate 1: source manifest integrity

Script: `scripts/verify_source_manifest.py`

Validates:

- `out/sources/SOURCE_MANIFEST.json` parses as JSON.
- Manifest entries are unique basenames.
- The manifest does not list itself. Self-hashes are unstable and are not valid evidence.
- Every manifest entry exists.
- Byte counts match.
- SHA-256 hashes match.
- No source files exist under `out/sources/` without a manifest entry.

Hard failures:

- missing source file
- byte-count mismatch
- SHA-256 mismatch
- duplicate manifest file
- self-entry for `SOURCE_MANIFEST.json`
- unmanifested source files

## Gate 2: generated design deliverables

Script: `verify_design_deliverables.py`

Validates:

- schema vocabularies and field contracts
- row counts against `out/design/BUILD_DESIGN_SUMMARY.json`
- reverse-index no-loss materialization from presentation rows
- duplicate reverse-index keys
- source disclosure aggregation
- status/removed-marker disagreement handling
- daily JSON exact match against dated presentation rows
- Psalm crosswalk coverage
- Pascha attestation/residue classifications
- Synaxarium and bridge integrity

Hard failures include malformed schema, missing required fields, duplicate reverse-index keys, status disagreements not classified, missing source disclosure, malformed removed markers, and stale generated daily files.

## Gate 3: query/reverse-lookup behavior

Script: `verify_lectionary_queries.py`

Validates:

- required artifacts exist
- query helper source and packaged helper are in sync
- false-positive guards such as `John 2` not matching `John 20` or `1 John 2`
- Pascha regression rows
- parser edge cases
- malformed raw-reference repair report
- duplicate source reading tuples
- canonical span validity
- Pascha source-text dedupe invariants
- chapter occurrence labels and row counts

Hard failures include parser gaps, invalid canonical spans, duplicate source tuples, known Pascha regression loss, and query false positives.

## Gate 4: daily calendar coverage

Script: `scripts/verify_calendar_coverage.py`

Validates:

- package daily files exist for all `meta.shipped_years`
- `meta.json` exposes `schemaVersion` / `schema_version`
- every shipped civil date exists as a daily JSON key, including Holy Week and Bright Saturday dates
- structural Holy Week/Bright Saturday rows materialized into daily files are documented in `meta.structural_date_resolver.structural_daily_additions_by_year`
- every key is an ISO date in the correct year
- every date maps to an array of readings
- package daily arrays are sorted by unique `reading_order`; `slot_order` may repeat for split Psalm/reading fragments
- package metadata count fields match actual file contents

Hard failure:

- any missing shipped civil date, including Holy Week or Bright Saturday

Strict mode is required for release validation:

```bash
python3 scripts/verify_calendar_coverage.py --strict-complete-calendar
```

## Gate 5: copticchurch cached external-source comparison

Script: `scripts/compare_external_sources.py`

Validates:

- shipped daily package rows match `out/data/copticchurch_passage_index_2020_2035.csv` for shipped years
- comparison uses the split passage-index layer, not raw multi-reference date rows
- package-only inline LXX Psalm annotations are stripped before comparison so dual-numbering display does not create false mismatches
- explicitly marked structural Holy Week / Bright Saturday materialized rows are skipped for this copticchurch-cache parity check because those rows come from structural Pascha sources, not the public daily cache

Current comparison source:

- local cached copticchurch.net passage index under `out/data/`

This is not a fresh live scrape. It validates package preservation against the repo's public-current-practice cache. A separate live-fetch comparator can be added later if needed.

Hard failures:

- any source-only row missing from package
- any package-only row not present in source cache unless it is explicitly marked as a structural Holy Week / Bright Saturday materialized row
- row-count mismatch after normalization

## Gate 6: package and tarball integrity

Script: `scripts/verify_package_integrity.py`

Validates:

- `package.json` and `meta.json` agree on package name and version
- required runtime files exist
- reverse-index JSONL parses
- `meta.occasion_index_rows` matches actual JSONL row count
- reverse-index duplicate keys are zero
- package reverse-index rows have no legacy `Kiak` or `Baba` spellings in consumer-facing labels; runtime labels use `Kiahk` and `Babah`
- package reverse-index rows have no unresolved source-priority passage conflicts where lower-priority cycle rows overlap current copticchurch.net rows for the same normalized consumer context/service/hour/slot but disagree on the passage span
- every row has required runtime fields
- `spans_json` and `source_disclosure` parse
- `source_disclosure_count` matches parsed disclosure length
- daily `rows`, `date_count`, and `reading_count` match actual files
- CommonJS exports resolve package paths
- tarball file set is exactly the expected runtime set when `--tarball` is supplied

Expected runtime tarball file set:

```text
LICENSE
README.md
data/daily/lectionary-2026.json
data/daily/lectionary-2027.json
data/daily/lectionary-2028.json
data/reverse_lectionary_index.jsonl
index.js
meta.json
package.json
```

## High-confidence fixes policy

Fix immediately when:

- a generated manifest is internally invalid
- metadata labels are demonstrably ambiguous or wrong
- package projection does not match verified design outputs
- a validator can prove row loss, duplicate keys, invalid spans, or malformed JSON
- a source typo correction is backed by concrete source evidence

Do not auto-fix when:

- the difference requires Coptic Reader confirmation but no locked fixture exists
- a Psalm mismatch has not been normalized across MT/LXX conventions
- a printed witness and current-practice source disagree but the correct status is not source-backed
- a Synaxarium association is thematic rather than explicit

## Current known limitations

1. Shipped daily files cover 2026-2028 but omit Holy Week / Bright Saturday structural dates.
2. Structural-only occasions, Bright Saturday service-order rows, and special services are in the reverse/supporting layers, not daily files.
3. Coptic Reader validation is fixture-limited. Do not mark rows as Coptic Reader-confirmed outside captured fixture scope.
4. `rows` in `meta.daily_files` is retained as a legacy alias for `date_count`. Use `date_count` and `reading_count` going forward.

## Package update decision rule

Recommend an npm package update when any runtime package file changes:

- `package.json`
- `meta.json`
- `README.md`
- `index.js`
- `data/reverse_lectionary_index.jsonl`
- `data/daily/*.json`

Do not recommend an npm package update for repo-only validation scripts, docs, or audit artifacts unless the package runtime files also changed.

Because npm versions are immutable, if the current published version already exists, bump to the next patch version and validate the tarball before George publishes.
