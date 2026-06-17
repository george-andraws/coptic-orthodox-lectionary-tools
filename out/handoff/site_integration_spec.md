# Coptic-Corpus Site Integration Spec

Generated for the `out/handoff/` package.

Hermes has not touched `coptic-corpus` in this run. George reviews this package, then pushes selected files to `coptic-corpus` himself.

## Safety gate

- `coptic-lectionary-and-synaxarium.md` is publish-ready with `publish: true` after George's approval.
- Do not restore the prior draft warning unless George asks for a fresh review hold.
- If the 69 reading collections are displayed, use the verdict `INFERRED_LIKELY_SAME_SET` with roster unverified. Do not state that Youssef's 69 collections and the Ottawa dated entries are confirmed as the same roster.

## Required search behavior

1. Accept MT or modern English input by default, such as `Psalm 51`.
2. Accept LXX liturgical Psalm input, such as `Psalm 50`, using `canonical_lxx_ref`, `reading_identity.csv`, and `psalm_mt_lxx_crosswalk.csv`.
3. Resolve both inputs to `identity_key` before showing results.
4. Show `display_ref` to users. If the LXX reference differs, keep the inline LXX annotation.
5. Do not merge current and historical readings without showing `current_status`.

## Two-layer lectionary model

The old monolith mixed two different concerns:

1. A year-independent occasion index for reverse lectionary and footprint pages.
2. A date-resolved daily file set for Today's Readings.

The shipped site model uses those as separate layers.

## Reverse lectionary rendering

Use `reverse_lectionary_index.jsonl` as the main passage-to-occasion index.

This file has one row per distinct `(occasion, service_section, service_hour, slot, identity_key)` tuple from the source monolith. It drops `gregorian_date` and `coptic_date`, aggregates collapsed source disclosure by distinct source tuple, and records ordinary-reading attestation years in `attestation_year_min`, `attestation_year_max`, and `attestation_years`. Each `source_disclosure` entry keeps one representative `source_locator`; full row-level source locators remain in `passage_source_disclosure.csv` and the raw audit archive.

For each passage result:

- group by `current_status`, then by season or source kind,
- show current Coptic Reader confirmed rows first when present,
- render `removed_marker` inline for historical Pascha rows,
- render collapsed source provenance from `source_disclosure` and `source_disclosure_count`,
- link source metadata through `source_registry.csv`,
- preserve both `canonical_mt_ref` and `canonical_lxx_ref`.

## Today's Readings rendering

Use the daily JSON file for the current Gregorian year. The page should read today's ISO date key directly, with no site-side lectionary computation.

Current shipped window:

- `daily/lectionary-2026.json`
- `daily/lectionary-2027.json`
- `daily/lectionary-2028.json`

Runtime behavior:

1. Choose the current Gregorian year file.
2. Lookup today's ISO date key, for example `2026-06-17`.
3. Render the ordered readings stored under that key.
4. If the key is absent, fail visibly and alert the daily rebuild process.

The daily rebuild cron should roll the shipped window forward. The full 2020 to 2035 file set remains in `out/design/daily/` in the research repo as archive and source material for future windows.

Date coverage limitation: daily files contain only rows with `gregorian_date`. Structural-only occasions without a date key, including Bright Saturday service-order rows and special services, remain in `reverse_lectionary_index.jsonl` and support tables but do not appear in `daily/lectionary-YYYY.json` yet.

## Passage liturgical footprint rendering

Use `passage_liturgical_footprint.csv` for cards, chapter pages, and passage pages.

Fields to wire:

- `identity_key`: join key to reading identity and reverse lectionary rows,
- `hour_themes`: display liturgical context in passage cards,
- `patristic_homily_slug`: placeholder field to join to site homily metadata,
- `chapter_study_slug`: placeholder field to join to chapter studies,
- `audio_slug`: placeholder field to join to audio pages,
- `site_note`: display note for current or historical scope.

The slug fields are intentionally placeholders in this repo because `coptic-corpus` was not available here.

## Source disclosure rendering

Use `passage_source_disclosure.csv` for per-passage source disclosure, or the `source_disclosure` field in `reverse_lectionary_index.jsonl` when rendering occasion-index rows directly.

Render these fields when present:

- `source_key`,
- `source_title`,
- `source_edition`,
- `source_locator`,
- `source_url`,
- `citation`,
- `current_status`,
- `removed_marker`.

For Synaxarium bridge rows, render `basis`, `confidence`, and `note` from `synaxarium_reading_bridge.csv`. Bridge rows are discovery links, not direct proof that a named commemoration has that proper reading.

## Historical and current-practice boundaries

- Coptic Reader governs current practice only where a fixture was captured in this project.
- The captured Coptic Reader scope is Pascha Wednesday Day.
- Rows absent from that fixture but present in older Pascha witnesses can be marked historical only inside that captured scope.
- Outside that scope, do not mark older/public rows removed unless a later current-practice source supports it.

## Change audit workflow

Use these files before updating chapter studies:

1. `affected_passages.csv`: unique affected passage keys to join against chapter studies.
2. `lectionary_change_manifest.csv`: grouped review manifest by passage, placement, change type, commit, and artifact.
3. `lectionary_change_manifest.raw.csv.gz`: exact row-level CSV audit archive for every committed CSV row delta in the data range.
4. `lectionary_change_manifest.md`: summary by change type and book, plus execution-log cross-check.

## Verification after site import

After George imports into `coptic-corpus`:

1. Verify the article has `publish: true` and no draft warning.
2. Search by MT and LXX Psalm numbering for at least Psalm 51 and Psalm 50.
3. Verify a historical Pascha reading shows `removed_marker` inline.
4. Verify passage pages display source disclosure.
5. Verify Today's Readings loads `daily/lectionary-YYYY.json` by ISO date and does not read the archive monolith.
6. Verify slug joins do not fail when placeholder slug fields are blank.
