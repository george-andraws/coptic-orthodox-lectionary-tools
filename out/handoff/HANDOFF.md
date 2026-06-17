# HANDOFF

This directory is the package George reviews and selectively pushes into `coptic-corpus`.

Hermes did not access `coptic-corpus` in this run. Everything here was produced in `coptic-lectionary-research` only.

## Push candidates and what George does with them

| Artifact | Path in `out/handoff/` | What George does with it |
|---|---|---|
| Publish-candidate article | `coptic-lectionary-and-synaxarium.md` | Copy into the site's lesson content area, keep `publish: false`, keep the visible draft note, and complete deacon review before any live publish. |
| Working spec | `lectionary_spec.md` | Keep as the research-side schema and terminology reference while integrating the site files. |
| Identity key map | `reading_identity.csv` | Import as the canonical reading identity table. Use `identity_key` as the join key across search, reverse lectionary, footprint, and source disclosure tables. |
| Reverse lectionary index | `reverse_lectionary_presentation.csv` | Import as the main passage-to-liturgical-use dataset. Render `removed_marker` inline and preserve dual MT/LXX numbering. |
| Today's readings snapshot | `todays_readings_current_practice.csv` | Import as the current-practice snapshot for today's readings pages or verification fixtures. |
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
| Schema | `lectionary_schema.json` | Keep as the machine-readable contract for these datasets. |
| Site integration spec | `site_integration_spec.md` | Follow this document when importing into `coptic-corpus`. |
| Grouped change manifest | `lectionary_change_manifest.csv` | Review grouped data changes by passage, change type, commit, and artifact before touching chapter studies. |
| Exact raw change manifest | `lectionary_change_manifest.raw.csv.gz` | Use when George wants the exact row-level CSV audit archive for every committed data diff. |
| Change manifest summary | `lectionary_change_manifest.md` | Read first for totals by change type and book, and for the execution-log cross-check. |
| Affected-passages index | `affected_passages.csv` | Use as the join key against chapter studies that reference affected passages. |
| Open questions | `open_questions_for_george.md` | Review remaining questions and decide what to resolve before or after the site push. |

## Practical import order

1. Import `reading_identity.csv`.
2. Import `psalm_mt_lxx_crosswalk.csv`.
3. Import `reverse_lectionary_presentation.csv` and `passage_source_disclosure.csv`.
4. Import `passage_liturgical_footprint.csv`.
5. Import `todays_readings_current_practice.csv`.
6. Import optional/supporting Synaxarium and Pascha audit datasets.
7. Review `affected_passages.csv` and `lectionary_change_manifest.md` before updating chapter studies.
8. Import the article only as a draft.

## Guardrails George should preserve

- Do not publish the article until deacon review is complete.
- Do not over-claim the 69 identity. Use `INFERRED_LIKELY_SAME_SET`, roster unverified.
- Do not treat Synaxarium bridge rows as direct proper-reading proof.
- Keep `removed_marker` visible for historical Pascha rows.
- Accept both MT and LXX Psalm numbering in site search and map both to `identity_key`.
