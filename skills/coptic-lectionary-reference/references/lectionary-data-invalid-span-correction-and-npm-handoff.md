# Lectionary-data cleanup, validation, and npm handoff

Use when the requester asks to validate or repair impossible span coordinates, clean/re-adjudicate source rows, rebuild `@andraws/lectionary-data`, or prepare a package handoff from the `coptic-lectionary-research` source pipeline.

## Repo-only release discipline

When the requester says the task is repo-only and he will publish:

- Work only inside the named repo. Do not modify downstream repos such as `coptic-corpus` unless explicitly instructed.
- Start with `npm view @andraws/lectionary-data versions --json`. If the prepared version is not on npm, keep it; if it is already published, bump to the next patch because npm versions are immutable.
- Do not run `npm publish`. End with the exact publish command for the maintainer.
- Use one commit per logical data change, one documentation/adjudication commit if requested, and one final rebuild/package commit.
- If package `meta.json.source_repo_commit` is generated before the rebuild commit exists, pin it to the intended data/source commit immediately before package generation and report that hash explicitly.

## Core rule

Fix the source pipeline, not only generated package files. For invalid spans in `out/design/reverse_lectionary_index.jsonl`, trace the row back through:

1. ordinary date scrape parsing in `build_lectionary_reference.py`
2. Pascha/day-hour curated rows in `build_lectionary_crosswalk.py`
3. design materialization in `build_design_deliverables.py`
4. handoff package files in `out/handoff/`
5. generated npm package files under `packages/lectionary-data/`

Generated rows can preserve bad-looking raw source text for provenance, but shipped canonical refs and `spans_json` must validate against book chapter counts.

## Live-source evidence pattern

For each suspect span:

1. Query Katameros API by 2026 Gregorian occasion date when possible, e.g. `https://api.katameros.app/readings/gregorian/DD-MM-2026?languageId=2`.
2. Save the raw response under an audit folder.
3. Record query, source URL, raw response path, SHA-256, byte count, slot, and returned reference in a manifest.
4. Mark each correction as SOURCED or INFERRED. Do not correct an uncertain span from hunch alone.

## Durable pipeline patch pattern

- Date-scrape typo corrections belong in a keyed correction table inside `build_lectionary_reference.py`, applied during parse before passage-index generation.
- Pascha curated-source corrections belong in `build_lectionary_crosswalk.py`, applied before extracting passage tokens.
- Preserve `_raw_refs` or equivalent provenance for source transparency when changing a curated reference.
- Add or update a verifier that validates canonical spans against book chapter counts. This catches impossible chapters and end-before-start ranges better than string searches alone.
- For false duplicate cleanup, canonicalize verse references to sorted verse sets before comparing rows. Collapse only same `(occasion, service_section, service_hour, slot)` rows whose canonical verse sets are identical; keep non-contiguous or different sets separate even if the source strings look similar.
- Use canonical range formatting only after confirming equal verse sets. Example: `Ps 33:10-11` equals `Ps 33:10,33:11`, but `Ps 62:7,62:2` and `Ps 62:7,62:6` are distinct sets and belong in open questions, not a merge.
- Retire lossy composite slots such as `Psalm+Gospel` or `Psalm + Gospel` at the source-token/model layer. If the row already contains passage tokens, relabel each token by book (`Ps` -> psalm, Gospel books -> gospel). If a single record truly carries two unsplit readings, split into two identity rows. If book classification is unsafe, preserve the source label and document the ambiguity; never lose a reading.
- When source labels change row counts by one because rows collapse into one corrected identity, update generated-count assertions and document the count change as rebuilt-data evidence.

## Rebuild order

1. Run the full local data pipeline with downstream documentation package publishing disabled when the task is repo-only.
2. Run the existing verifier and the canonical-span guard; `invalid_spans` must be 0.
3. Rebuild design deliverables.
4. Validate JSONL parsing and canonical spans in `out/design/reverse_lectionary_index.jsonl`.
5. Confirm every occasion-index row carries required model fields such as `slot_type`, `slot_order`, and `occasion_kind`. If `slot_order` is nullable by schema for `source_label_preserved`, assert the nulls are limited to that slot type rather than requiring non-null globally.
6. If canonicalization changes text ordering (`Ps 41:6,41:1` -> `Ps 41:1,41:6`, `Ps 18:48,17` -> `Ps 18:17,18:48`), update verifier fixtures to assert semantic distinctness and canonical forms, not stale source-string order.
7. Check `scripts/build_npm_package.mjs` before packaging. Prefer sourcing npm data directly from verified `out/design` (`DESIGN_DIR`) rather than stale tracked `out/handoff` artifacts. If the builder still reads `out/handoff`, either refresh every shipped handoff file from `out/design` first or patch the builder to read `out/design` before packaging.
8. Rebuild `packages/lectionary-data` with the package builder.
9. Run `npm pack --json` from `packages/lectionary-data`, never from the repo root and never `npm publish` unless the requester explicitly authorizes publish.
10. Validate the packed `.tgz` and unpacked package data after the final rebuild commit inputs are settled; earlier pack checks can go stale after regenerating line endings or metadata.

## npm validation checklist

Validate the tarball itself, not just the working tree:

- exact 9-file set for this package: `LICENSE`, `README.md`, three shipped daily JSON files, `data/reverse_lectionary_index.jsonl`, `index.js`, `meta.json`, `package.json`
- no packed file over 100 MB
- package version matches requested version and is still unpublished according to `npm view`
- `meta.json.version` matches package version
- `meta.json.source_repo_commit` points to the intended data-rebuild/source commit, not a later packaging-only commit unless the maintainer asked otherwise
- `meta.json.occasion_index_rows` equals actual packed JSONL rows
- packed JSON and JSONL parse cleanly
- every newly documented packaged field is present in the packed JSONL, not just in `out/design`; when adding metadata such as `slot_type`, `slot_order`, or `occasion_kind`, validate both `packages/lectionary-data/data/reverse_lectionary_index.jsonl` and the extracted `.tgz` copy
- invalid target strings are absent from packed reverse index, including retired source labels such as `Psalm+Gospel` / `Psalm + Gospel` when a cleanup claims they are gone
- CommonJS exports resolve package paths

## Adjudication documentation standard

When the requester asks for cleanup adjudication or Fr. Boulos review material, update the open-questions document in review-session shape:

- separate genuine source disagreements from inferred local merges and ordering-confirmation gaps
- for each unresolved item, state competing options, current source situation, and what would resolve it
- explicitly flag inferred vs sourced changes in both the doc and final handoff
- append the execution log with commit hashes and real validation outcomes, not planned outcomes

## Commit hygiene

Use separate commits for:

1. source-pipeline corrections plus raw source evidence
2. regenerated data/design outputs plus verifier changes
3. package version bump, refreshed handoff files, and generated package directory

Leave the `.tgz` untracked unless the requester explicitly asks to commit release artifacts.
