# HANDOFF

This directory is the package George reviews and selectively pushes into `coptic-corpus`.

Hermes did not access `coptic-corpus` in this run. Everything here was produced in `coptic-lectionary-research` only.

## Shipped runtime files

These are the files intended for site runtime import.

| Artifact | Path in `out/handoff/` | What George does with it |
|---|---|---|
| Publish-candidate article | `coptic-lectionary-and-synaxarium.md` | Copy into the site's lesson content area, keep `publish: false`, keep the visible draft note, and complete deacon review before live publish. |
| Working spec | `lectionary_spec.md` | Keep as the research-side schema and terminology reference while integrating the site files. |
| Schema | `lectionary_schema.json` | Use as the machine-readable contract for these datasets. |
| Identity key map | `reading_identity.csv` | Import as the canonical reading identity table. Use `identity_key` as the join key across search, reverse lectionary, footprint, and source disclosure tables. |
| Reverse lectionary occasion index | `reverse_lectionary_index.jsonl` | Import as the year-independent passage-to-occasion index. Render `removed_marker` inline, preserve dual MT/LXX numbering, and show source disclosure. |
| Daily readings, 2026 | `daily/lectionary-2026.json` | Use for Today's Readings by direct ISO date lookup in 2026. |
| Daily readings, 2027 | `daily/lectionary-2027.json` | Use for the next-year Today's Readings window. |
| Daily readings, 2028 | `daily/lectionary-2028.json` | Use as the second next-year file because it is small. |
| Per-passage liturgical footprint | `passage_liturgical_footprint.csv` | Import for chapter pages and passage cards. Wire `hour_themes`, `patristic_homily_slug`, `chapter_study_slug`, and `audio_slug`. |
| Per-passage source disclosure | `passage_source_disclosure.csv` | Import to render per-passage source/provenance disclosure on site pages. |
| Source registry | `source_registry.csv` | Import as the normalized source lookup behind `source_key`. |
| Psalm MT/LXX crosswalk | `psalm_mt_lxx_crosswalk.csv` | Use in search and display logic so MT and LXX Psalm numbering resolve to the same `identity_key`. |
| Foundational 69 collections table | `foundational_reading_collections_69.csv` | Keep as supporting design data. If surfaced in the site, preserve the verdict `INFERRED_LIKELY_SAME_SET` and the roster-unverified caution. |
| Pascha attestation table | `pascha_attestation.csv` | Keep as audit/supporting data for historical Pascha witness rendering. |
| Pascha attestation bucket manifest | `pascha_attestation_bucket_manifest.csv` | Keep as supporting audit metadata for the Pascha attestation table. |
| Temporal classification | `temporal_classification.csv` | Keep as supporting design data for current vs historical Pascha logic. |
| Temporal residue | `temporal_residue.csv` | Keep as supporting design/audit data for unresolved or historical Pascha residue. |
| Temporal residue manifest | `temporal_residue_manifest.csv` | Keep as supporting audit metadata for residue buckets. |
| Synaxarium commemorations | `synaxarium_commemorations.csv` | Import if the site will expose commemoration-level metadata. |
| Synaxarium reading bridge | `synaxarium_reading_bridge.csv` | Import only as a discovery-link layer. Render `basis` and `confidence`; do not present it as a final proper-reading schedule. |
| Site integration spec | `site_integration_spec.md` | Follow this document when importing into `coptic-corpus`. |

## Archive and audit files

These are retained for George's review, not for normal site runtime.

| Artifact | Path | Status |
|---|---|---|
| Old reverse presentation CSV | `reverse_lectionary_presentation.csv` | Archive only. Superseded by `reverse_lectionary_index.jsonl` plus daily JSON files. |
| Retired reverse presentation JSONL | `out/design/reverse_lectionary_presentation.jsonl` | Not present in the working tree. History only until George removes old blobs with filter-repo. |
| Today's readings snapshot | `todays_readings_current_practice.csv` | Archive fixture only. Superseded by daily JSON files for runtime. |
| Full per-year daily set | `../design/daily/lectionary-2020.json` through `../design/daily/lectionary-2035.json` | Research archive. Only 2026, 2027, and 2028 are shipped here. |
| Grouped change manifest | `lectionary_change_manifest.csv` | Review grouped data changes by passage, change type, commit, and artifact before touching chapter studies. |
| Exact raw change manifest | `lectionary_change_manifest.raw.csv.gz` | Use when George wants the exact row-level CSV audit archive for every committed data diff. |
| Change manifest summary | `lectionary_change_manifest.md` | Read first for totals by change type and book, and for the execution-log cross-check. |
| Affected-passages index | `affected_passages.csv` | Use as the join key against chapter studies that reference affected passages. |
| Open questions | `open_questions_for_george.md` | Review remaining questions and decide what to resolve before or after the site push. |

## Practical import order

1. Import `reading_identity.csv`.
2. Import `psalm_mt_lxx_crosswalk.csv`.
3. Import `reverse_lectionary_index.jsonl` and `passage_source_disclosure.csv`.
4. Import `passage_liturgical_footprint.csv`.
5. Import `daily/lectionary-2026.json`, `daily/lectionary-2027.json`, and `daily/lectionary-2028.json` for Today's Readings.
6. Import optional/supporting Synaxarium and Pascha audit datasets.
7. Review `affected_passages.csv` and `lectionary_change_manifest.md` before updating chapter studies.
8. Import the article only as a draft.

## Guardrails George should preserve

- Do not publish the article until deacon review is complete.
- Do not over-claim the 69 identity. Use `INFERRED_LIKELY_SAME_SET`, roster unverified.
- Do not treat Synaxarium bridge rows as direct proper-reading proof.
- Keep `removed_marker` visible for historical Pascha rows.
- Accept both MT and LXX Psalm numbering in site search and map both to `identity_key`.
- Today's Readings reads the current-year daily file by ISO date with no site-side lectionary computation.
- The daily rebuild cron should roll the shipped window forward each year.
