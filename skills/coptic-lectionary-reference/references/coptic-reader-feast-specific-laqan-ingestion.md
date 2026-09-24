# Adding a Feast-Specific Laqan Variant from Coptic Reader Screenshots

Use this pattern when Coptic Reader exposes a feast-specific Liturgy of the Waters / Laqan table that is absent from the local special-service dataset.

## Classification

- Do not merge feast-specific readings into an existing generic or Epiphany Laqan row set.
- Keep the class-level family stable, for example `liturgy_of_the_waters`.
- Add a distinct variant, for example `apostles_feast_laqan`.
- Separate prophecy rows from the final Pauline/Psalm/Gospel block with sections such as `prophecies` and `main_readings`.

## Source preservation

1. Read every visible reference directly from the screenshots. Do not infer cropped or unseen readings.
2. Archive the original screenshots under a durable repo path such as `sources/coptic-reader/<service-and-date>/`.
3. Give the files descriptive sequence names and record checksums when practical.
4. In each curated row, cite Coptic Reader as the source, link its official site, and store the relative archived screenshot path in the source locator field.
5. Preserve Psalm numbering exactly as displayed and state that the source numbering was preserved. Do not silently convert it.

## Data update

1. Search the live curated generator and generated CSVs for the family and proposed variant.
2. Compare at the reading-block level, not just variant presence. A feast variant may already exist but contain only its Pauline/Psalm/Gospel block while its prophecies are missing.
3. If the variant is absent, add it distinctly. If it is partial, preserve its existing rows and add only the screenshot-confirmed missing blocks under the correct section. Never create a duplicate variant merely because the existing table is incomplete.
4. Add source-backed rows to `build_special_service_reference.py` rather than editing generated CSV files directly.
5. Use one curated row per displayed reading block. A multi-verse Psalm citation can remain one curated row; the passage-index builder should split it into normalized segments.
6. Update the human-readable downstream documentation special-service table with the completed variant and source provenance.
7. Rebuild in dependency order:
   - `build_special_service_reference.py`
   - `build_lectionary_crosswalk.py`
   - `build_bible_chapter_lectionary_index.py`
8. Publish through the existing builders so repo and downstream documentation package copies stay synchronized.

## Verification

- Direct service query returns every displayed reading under the new variant.
- Curated-row count matches the number of displayed reading blocks.
- Passage-index and reverse-crosswalk normalized sets match the expected set. Their row count may be higher when a combined Psalm row splits into multiple segments.
- For crowded passages, use the query helper's supported `--include-crosswalk` option and a sufficient `--limit`; an ordinary `--passage` result can be truncated before the special-service placement appears.
- Read the published downstream documentation package CSV and human-readable Markdown section back.
- Run the repository validation tests.
- Keep unrelated pre-existing git changes out of the task.

## Design-layer and verifier pitfalls

- Rebuild design deliverables after the crosswalk and chapter indexes; confirming only the curated CSV is not enough for npm consumers.
- Adding a variant may legitimately change an exact reverse-index row-count invariant. Update both builder and verifier to the newly measured count after proving the normalized added-row set. Do not weaken the invariant or guess the delta.
- If the builder emits one authoritative `source_family`/`source_kind` scalar plus full `source_disclosure`, the verifier must enforce the same contract. Select the winning disclosure using the builder's authority rule, require family/kind/edition/title/locator from that same winner, forbid `" || "` in atomic source fields, and retain every attestation in `source_disclosure`.
- Generated current-day snapshots and their build-summary counts must remain consistent. If unrelated generated prose is restored to reduce churn, rerun the verifier to ensure the retained artifact set is still internally coherent.

## npm release extension

When the requester also asks to publish `@andraws/lectionary-data`:

1. Confirm `npm whoami`, registry `latest`, and that the target patch version is absent.
2. Bump both `packages/lectionary-data/package.json` and the `VERSION` constant in `scripts/build_npm_package.mjs`.
3. Commit the source rows, evidence, generated indexes/design artifacts, verifier changes, and version source before package generation.
4. If unrelated working-tree changes exist, stash only those paths temporarily. Build from the clean committed source so `meta.source_tree_dirty` is false and `meta.source_repo_commit` is reproducible; restore the stash after release.
5. Require zero historical removal-version baseline misses.
6. Run package-integrity and strict-calendar verification.
7. Pack with `npm pack --json`, validate the tarball's exact file set, and install the tarball into a temporary prefix. Query the new variant through the package exports.
8. Commit generated package files, then publish only with explicit authorization.
9. Verify npm dist-tags and checksums, install the published registry version into a fresh temporary prefix, and query the new rows again.
10. Push commits and require local HEAD, remote-tracking HEAD, and `git ls-remote` to match before restoring the scoped stash.

Retain the curated/normalized row counts, exact normalized references, package source commit, reverse-index SHA-256, tarball shasum/integrity, file count, and fresh install results as release evidence.

## Example shape

For the Apostles' Feast Laqan captured on 2026-07-12, the local model used:

- family: `liturgy_of_the_waters`
- variant: `apostles_feast_laqan`
- sections: `prophecies`, `main_readings`
- source: official Coptic Reader screenshots archived in the repository

For the Theophany/Epiphany Laqan captured later that day, `epiphany_laqan` already existed with Pauline, Psalm, and Gospel rows from a rite book. The correct action was to complete that same variant with the seven screenshot-confirmed prophecy rows, not create another Epiphany variant or replace the stronger existing main-reading provenance. This yielded 10 curated reading blocks and 11 normalized passage rows because the combined Psalm row split into two segments.

These examples are illustrative. Always derive actual readings and variant names from the current source and local naming conventions.
