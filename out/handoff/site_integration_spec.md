# Coptic-Corpus Site Integration Spec

Generated for the `out/handoff/` package.

Hermes has not touched `coptic-corpus` in this run. George reviews this package, then pushes selected files to `coptic-corpus` himself.

## Safety gate

- Keep `coptic-lectionary-and-synaxarium.md` as `publish: false` until George completes the deacon review.
- Keep the visible draft note at the top of the article body.
- If the 69 reading collections are displayed, use the verdict `INFERRED_LIKELY_SAME_SET` with roster unverified. Do not state that Youssef's 69 collections and the Ottawa dated entries are confirmed as the same roster.

## Required search behavior

1. Accept MT or modern English input by default, such as `Psalm 51`.
2. Accept LXX liturgical Psalm input, such as `Psalm 50`, using `canonical_lxx_ref`, `reading_identity.csv`, and `psalm_mt_lxx_crosswalk.csv`.
3. Resolve both inputs to `identity_key` before showing results.
4. Show `display_ref` to users. If the LXX reference differs, keep the inline LXX annotation.
5. Do not merge current and historical readings without showing `current_status`.

## Reverse lectionary rendering

Use `reverse_lectionary_presentation.csv` as the main passage-to-liturgical-use index.

For each passage result:

- group by `current_status`, then by season or source kind,
- show current Coptic Reader confirmed rows first when present,
- render `removed_marker` inline for historical Pascha rows,
- render source provenance from `passage_source_disclosure.csv`,
- link source metadata through `source_registry.csv`,
- preserve both `canonical_mt_ref` and `canonical_lxx_ref`.

## Today's readings rendering

Use `todays_readings_current_practice.csv` as the static current-practice snapshot produced in this run. For dynamic production behavior, generate the date key in the site and resolve against the current reading source available there.

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

Use `passage_source_disclosure.csv` for per-passage source disclosure.

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

1. Verify the article remains unpublished.
2. Search by MT and LXX Psalm numbering for at least Psalm 51 and Psalm 50.
3. Verify a historical Pascha reading shows `removed_marker` inline.
4. Verify passage pages display source disclosure.
5. Verify slug joins do not fail when placeholder slug fields are blank.
