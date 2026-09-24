# Lectionary package validation release gates

Use this reference when the requester asks to validate, audit, package, or decide whether to update `@andraws/lectionary-data`.

## Durable workflow

1. **Document the validation plan in the repo, not only in chat.**
   - Stable doc path used successfully: `docs/LECTIONARY_VALIDATION_PLAN.md`.
   - Keep generated/draft implementation plans separate from durable repo runbooks; remove stale drafts once a stable doc exists.

2. **Validate source manifests before generated artifacts.**
   - Add/run a source manifest gate such as `scripts/verify_source_manifest.py`.
   - A manifest should not list itself (`SOURCE_MANIFEST.json`), because self-hashes are unstable validation evidence.
   - Patch the generator, not just the generated manifest, so future rebuilds exclude the self-entry.
   - Gate checks: file exists, basename only, no duplicates, byte count matches, SHA-256 matches, no unmanifested source files.

3. **Compare the right source layer.**
   - For shipped daily files, compare against `out/data/copticchurch_passage_index_2020_2035.csv`, not the raw `copticchurch_date_readings_2020_2035.csv`.
   - The raw date file can contain multi-reference rows before splitting; the passage index is the correct split-reference layer for package daily comparison.
   - Normalize package display refs before comparison by stripping inline LXX annotations such as `Ps 105:14-15 (LXX Ps 104:14-15)`. Otherwise Psalm dual-numbering display creates false mismatches.
   - When package daily files materialize Holy Week/Bright Saturday structural rows, skip only rows explicitly marked with `structural_day` or structural source families for this copticchurch-cache parity check; still require every copticchurch cached row to be preserved.

4. **Require complete shipped civil-date coverage.**
   - Release validation should run `scripts/verify_calendar_coverage.py --strict-complete-calendar`.
   - All shipped civil dates must exist as daily JSON keys, including Holy Week and Bright Saturday.
   - If copticchurch.net has no date-resolved rows for a shipped Holy Week/Bright Saturday date, materialize structural Pascha/Bright Saturday rows into the daily file and document them under `meta.structural_date_resolver.structural_daily_additions_by_year`.

5. **Validate the package and the tarball, not just `out/design`.**
   - Use a package validator such as `scripts/verify_package_integrity.py`.
   - Check `package.json` vs `meta.json`, required runtime files, JSONL parsing, duplicate reverse-index keys, `spans_json`, `source_disclosure`, CommonJS exports, daily counts, and tarball exact file set.
   - Run `npm pack --json` from `packages/lectionary-data`, not repo root.
   - Never run `npm publish` unless the requester explicitly approves.

6. **Fix high-confidence metadata issues as patch releases.**
   - If `meta.daily_files[*].rows` is ambiguous, keep it as a legacy alias for date count and add explicit `date_count` and `reading_count`.
   - Consumer validation now expects `meta.schemaVersion` or `meta.schema_version`; publish both aliases with the same semver-like schema contract value.
   - Do not ship daily files with missing civil dates for shipped years. If copticchurch.net daily cache lacks Holy Week / Bright Saturday rows for a shipped date, materialize structural Pascha/Bright Saturday rows into the daily file, mark them with structural metadata, and document the additions under `meta.structural_date_resolver.structural_daily_additions_by_year`. `missing_dates_by_year` should be empty for released complete-coverage packages.
   - Daily JSON arrays should be deterministic for consumers: add unique per-date `reading_order`, service-specific `service_order`, normalized `slot_type`, and `slot_order`. Document that `slot_order` can repeat for split Psalm/reading fragments; consumers needing a unique order should use `reading_order`.
   - One known spanless named reading, `Memoirs of Job` (`rid_8b0ba0644695bd53a112`), is valid because it is a Coptic Reader named reading, not a canonical biblical span. Document that `spans_json: []` is allowed for named non-standard readings.
   - Document Psalm dual-numbering display refs: `display_ref` may include inline LXX notation; machine consumers should use `canonical_mt_ref`, `canonical_lxx_ref`, and `spans_json`.
   - Identity keys appearing across multiple `source_family` values are expected attestation breadth across distinct occasions, not duplicates by themselves.
   - Add a package-side validator for `PACKAGE_CONTEXT_PASSAGE_CONFLICT`: group active reverse-index rows by normalized consumer context + normalized service + service hour + `slot_type`; if a current copticchurch.net `ordinary_date_resolved` row overlaps a lower-priority cycle row but disagrees on span, the npm projection may preserve the lower-priority row as inactive/removed evidence instead of deleting it. Removed rows must be clearly marked (`active: false` or `status: "removed"`) with a user-facing note/reason, preferred source/ref, and enough provenance to audit the decision. Active lookup APIs and conflict validators must ignore removed rows by default; package consumers can use `isActiveReading(row)` / `isRemovedReading(row)` when those helpers are exported. Include shorthand end-chapter variants such as `Acts 2:42-3` vs `Acts 2:42-3:9` and `1Thess 4:13-5` vs `1Thess 4:13-5:11`, even when the parsed span is malformed or same-chapter only.
   - Normalize package-facing Coptic month labels: `Kiak` -> `Kiahk`, `Baba` -> `Babah`. Validate exact word-boundary spellings in reverse and daily runtime files.
   - For weekday-specific fixed-date duplicates such as `Sunday, Tout 18`, do not delete valid non-Sunday evidence; disambiguate the generic sibling as a non-Sunday context when the dated evidence supports that split.
   - If the currently published npm version already exists (`npm view @andraws/lectionary-data versions --json`), bump to the next patch before rebuilding the package candidate.
   - After committing source/package changes, rebuild the npm package once more from the pushed commit before publishing so `meta.source_repo_commit` points at a real pushed SHA and `meta.source_tree_dirty` is false. Commit and push that provenance refresh before `npm publish`.
   - After publishing, verify both registry state and consumer install behavior: `npm view @andraws/lectionary-data version`, `npm view @andraws/lectionary-data dist-tags --json`, then install `@latest` in a temp project and assert the specific regression cases that motivated the release.
   - External release notes should be consumer-facing: package/version, install command, fixed validator failures, behavior/API changes, validation highlights, and migration impact. Avoid internal task narrative.

7. **Report package-update recommendation based on runtime file changes.**
   - Recommend npm update when any runtime package file changes: `package.json`, `meta.json`, `README.md`, `index.js`, `data/reverse_lectionary_index.jsonl`, or `data/daily/*.json`.
   - Do not recommend an npm update for validation scripts/docs/audit artifacts alone.

## Release-gate command pattern

Adapt the exact package version/tarball name as needed:

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
# For releases that add inactive/removed provenance rows, install the previous package version
# into a temporary baseline dir and compare active behavior against the candidate package.
python3 scripts/compare_package_active_equivalence.py <previous-package-dir> packages/lectionary-data
python3 scripts/verify_package_integrity.py --tarball packages/lectionary-data/andraws-lectionary-data-<version>.tgz
git diff --check
```

## Pitfalls

- Do not compare raw copticchurch date rows to package daily rows; use the split passage index.
- Do not count inline LXX Psalm annotations as mismatches.
- Do not let source manifest self-hash failures persist as a known warning; fix the generator.
- Do not publish from Hermes unless the requester explicitly approves publishing in the active request; otherwise hand the maintainer the publish command only after tarball validation passes.
- Do not treat Coptic Reader as a comparator unless using locked fixtures or a documented reproducible app-data path.
