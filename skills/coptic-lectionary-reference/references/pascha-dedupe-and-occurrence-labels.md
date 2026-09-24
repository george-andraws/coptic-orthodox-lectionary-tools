# Pascha dedupe and occurrence display-label workflow

Use this reference when modifying the local lectionary builder pipeline around `build_lectionary_crosswalk.py`, `build_bible_chapter_lectionary_index.py`, and `verify_lectionary_queries.py`.

## Durable lessons

- The published downstream documentation data package is downstream. Builder changes belong in `$REPO_ROOT`; regenerate `out/data` there, then let the normal standalone builders publish generated copies to the downstream documentation package when the user asks for a real run.
- For Pascha crosswalk dedupe, treat `pascha_day_hour` as authoritative over `pascha_source_text` when they overlap. The accepted Phase 2A rule is: drop a `pascha_source_text` row when the same normalized day and same canonical normalized passage segment already appears in `pascha_day_hour`, regardless of hour.
- Keep confirmed extraction errors separate from dedupe. Use a small commented quarantine/exclusion set for source-text mis-extractions, with comments explaining the source verification and that the list may grow as more errors are confirmed.
- Known confirmed quarantine from Phase 2A: Wednesday / `Isa 48:1-6` from `pascha_source_text`, confirmed absent from the official Wednesday Pascha hours in the St. Mary Ottawa Pascha book.
- Regression expectations after Phase 2A: no `pascha_source_text` row shares `(normalized day, canonical passage)` with any `pascha_day_hour` row; Wednesday source-text rows `Ps 83:2,83:5`, `Jn 12:1-8`, and `Isa 48:1-6` are absent; Hosanna Sunday `Lam 1:1-4` remains.
- `bible_chapter_lectionary_occurrences.csv/.jsonl` now carries display helper columns: `occasion_label`, `service_label`, `reading_label`. Existing raw columns remain untouched.
- For `katameros_cycle`, display labels come from `service_section`, not `reading_type`, because `reading_type` stores source table names like `AnnualReadings`, `GreatLentReadings`, `PentecostReadings`, and `SundayReadings`. Example: `matins_psalm -> Matins / Psalm`, `vespers_psalm -> Vespers / Psalm`, `liturgy_acts -> Liturgy / Praxis`, `prophecy -> Prophecy / ''`.
- For non-`katameros_cycle` families, label columns should initially pass through raw values: `occasion_label = existing occasion`, `service_label = service_section`, `reading_label = reading_type`. Do not silently prettify special-service or Pascha labels until the maintainer approves those label rules.

## Safe build sequence for this class of change

1. Confirm repo and remote:
   - repo: `$REPO_ROOT`
   - remote should be `https://github.com/george-andraws/coptic-orthodox-lectionary-tools.git`
2. Precheck standalone inputs in `out/data`: `reverse_lookup_crosswalk.csv`, all seven per-family passage indexes, Pascha/Bright Saturday artifacts.
3. Do **not** run `build_lectionary_reference.py` unless explicitly requested. For no-scrape/no-SQLite rebuilds, run only:
   - `python3 build_lectionary_crosswalk.py`
   - `python3 build_bible_chapter_lectionary_index.py`
4. For scratch dry runs, use env overrides instead of editing hardcoded paths:
   - `LECTIONARY_WORK_OUT_DATA=/tmp/lectionary_scratch/data`
   - `LECTIONARY_DATA_DIR=/tmp/lectionary_scratch/data`
   - `LECTIONARY_CROSSWALK_OUT=/tmp/lectionary_scratch/out4`
   - `LECTIONARY_DISABLE_VAULT_PUBLISH=1`
5. For a real run, omit those scratch env vars so tracked `out/data` is regenerated and the normal downstream documentation package publish occurs.
6. Run verification before reporting or committing:
   - `PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py`
   - `git diff --check`
   - inspect `git status --short`, staged paths, and generated-output scope.

## Pitfalls

- `verify_lectionary_queries.py` may encode old crosswalk expectations. If dedupe intentionally removes duplicated `pascha_source_text`, update verifier assertions to express the new invariant rather than preserving obsolete duplicate expectations.
- Generated CSVs can trip `git diff --check` if writers emit CRLF line endings. Prefer setting `lineterminator='\n'` in project CSV writers instead of ignoring the failure.
- `BUILD_SUMMARY.json` is not refreshed by the two standalone builders. If the user explicitly forbids the full builder, report that the summary is stale rather than running the full package build.
- Do not create or commit ad-hoc report JSON files from diagnostic runs unless they are intentionally tracked artifacts. In Phase 2A, the dedupe report was useful as stdout evidence but should not persist as an untracked repo file.
