# Lectionary-data fixed Coptic day occasion cleanup

Use this reference when the maintainer reports generic `annual fixed Coptic day` rows in `@andraws/lectionary-data` or the `coptic-lectionary-research` reverse index.

## Durable lesson

For Katameros `AnnualReadings` fixed Coptic days, `source_type` can be the generic label `annual fixed Coptic day` while the same source row already carries the concrete fixed Coptic date in `day_name` / `day_key` (for example `Mesra 29`, `Tubah 13`). The public reverse-lectionary `occasion` should use the concrete day, not the generic source category.

Do not hand-edit generated package rows. Fix the upstream pipeline and rebuild.

## Successful fix pattern

1. Confirm published package versions first:
   - `npm view @andraws/lectionary-data versions --json`
   - If the intended version is already published, bump because npm versions are immutable.
2. Audit the generic rows before editing:
   - Count rows in package/design outputs where any public field contains `annual fixed Coptic day`.
   - For each old generic reverse-index row, join back to `reverse_lectionary_presentation.csv` on identity/service/slot and prove concrete `service_day` values exist.
   - Write a row-level audit artifact summarizing old generic rows, concrete source rows, unique fixed days, and any missing mappings.
3. Patch the source pipeline, not generated outputs:
   - In `build_lectionary_crosswalk.py`, for `katameros_cycle` rows with `source_type == 'annual fixed Coptic day'`, set `liturgical_place` to `day_name` / `day_key` when present.
   - Keep source provenance (`source_kind`, `source_family`, `source_table`, row ids) intact.
4. Rebuild and guard:
   - Run the full reference/data rebuild and `build_design_deliverables.py`.
   - Update the expected reverse-index row count guard when generic aggregates expand into concrete dated rows.
   - Add an explicit verifier guard that public `reverse_lectionary_index.jsonl` must not expose `occasion == 'annual fixed Coptic day'`.
5. Validate:
   - `python3 verify_lectionary_queries.py` must have `invalid_spans = 0`.
   - `python3 verify_design_deliverables.py` must pass.
   - Check all public generated outputs and the package reverse index have zero `annual fixed Coptic day` hits.
6. Commit shape:
   - Commit source/data cleanup first.
   - Then update the package builder version and pin package `source_repo_commit` to the cleanup commit, rebuild the package, pack and validate the tarball, and commit package files separately.
   - Do not run `npm publish`; the maintainer publishes.

## Validation checklist for the npm handoff

After `node scripts/build_npm_package.mjs` and `npm pack --json` from `packages/lectionary-data`, validate the actual tarball:

- package name and version
- `meta.json.version`
- `meta.json.source_repo_commit` equals the source/data cleanup commit
- exact expected packed file set and count
- no packed file over 100 MB
- all JSON and JSONL parse
- reverse-index row count equals package metadata
- zero package reverse-index hits for `annual fixed Coptic day`
- entrypoint can be loaded and exported paths resolve

## Classification

This cleanup is sourced, not inferred, when every old generic row maps back to one or more concrete `service_day` values already present in source/presentation rows. Report counts explicitly: old generic rows, validated rows, missing rows, concrete presentation/source rows, and unique Coptic days.
