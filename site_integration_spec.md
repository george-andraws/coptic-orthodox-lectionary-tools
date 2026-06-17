# Site Integration Spec: Coptic Lectionary Design Layer

Generated: 2026-06-17

George will push selected files into the site repo. Hermes does not have `coptic-corpus` access in this run.

## Files to copy

Copy the shipped files from `out/handoff/`:

- `coptic-lectionary-and-synaxarium.md`
- `lectionary_spec.md`
- `lectionary_schema.json`
- `reading_identity.csv`
- `reverse_lectionary_index.jsonl`
- `daily/lectionary-2026.json`
- `daily/lectionary-2027.json`
- `daily/lectionary-2028.json`
- `passage_liturgical_footprint.csv`
- `passage_source_disclosure.csv`
- `source_registry.csv`
- `psalm_mt_lxx_crosswalk.csv`
- `foundational_reading_collections_69.csv`
- `pascha_attestation.csv`
- `pascha_attestation_bucket_manifest.csv`
- `temporal_classification.csv`
- `temporal_residue.csv`
- `temporal_residue_manifest.csv`
- `synaxarium_commemorations.csv`
- `synaxarium_reading_bridge.csv`
- `open_questions_for_george.md`

Archive files that remain research support, not shipped runtime data:

- `out/design/reverse_lectionary_presentation.csv`
- `out/design/todays_readings_current_practice.csv`
- `out/design/todays_readings_current_practice.jsonl`
- `out/design/daily/lectionary-2020.json` through `out/design/daily/lectionary-2035.json`, except the shipped window copied above

## Required search behavior

1. Accept MT or modern English input by default, for example `Psalm 51`.
2. Accept LXX liturgical Psalm input, for example `Psalm 50`, by consulting `canonical_lxx_ref`, `reading_identity.csv`, and `psalm_mt_lxx_crosswalk.csv`.
3. Resolve both forms to `identity_key` before showing results.
4. Show `display_ref` to users. If LXX differs, keep the inline LXX annotation.
5. Never collapse historical and current readings without displaying `current_status`.

## Reverse lectionary behavior

Use `reverse_lectionary_index.jsonl` for passage-to-occasion results and per-passage footprint pages. It is year-independent and has one row per distinct `(occasion, service_section, service_hour, slot, identity_key)` tuple from the source monolith.

For each passage result:

- group by `current_status`, then season or source kind,
- show current Coptic Reader confirmed rows first where available,
- render `removed_marker` inline for historical Pascha rows,
- preserve dual MT/LXX numbering through `display_ref`, `canonical_mt_ref`, and `canonical_lxx_ref`,
- render collapsed source disclosure from `source_disclosure` and `source_disclosure_count`, with per-row detail available in `passage_source_disclosure.csv`.

The index aggregates provenance and source disclosure across collapsed duplicates. Each `source_disclosure` entry represents one distinct source tuple, keeps one representative `source_locator`, and records `attested_year_min` and `attested_year_max` where dated rows exist. Row-level `attestation_year_min`, `attestation_year_max`, `attestation_years`, and `collapsed_row_count` remain on the index row.

## Today's readings behavior

Use the daily JSON file for the current Gregorian year. Today's Readings should read the current ISO date key directly, with no site-side lectionary computation.

Example for 2026:

1. Load `daily/lectionary-2026.json`.
2. Lookup today's ISO key, such as `2026-06-17`.
3. Render the ordered readings stored under that key.

The daily rebuild cron rolls the shipped window. The current handoff ships 2026, 2027, and 2028. Keep future window updates as file copies from `out/design/daily/` after this repo regenerates.

Date coverage limitation: daily files contain only rows with `gregorian_date`. Structural-only occasions without a date key, including Bright Saturday service-order rows and special services, remain in `reverse_lectionary_index.jsonl` and support tables but do not appear in `daily/lectionary-YYYY.json` yet.

## Passage footprint behavior

Use `passage_liturgical_footprint.csv` for cards and chapter pages. It provides:

- occurrence counts,
- current and historical counts,
- sample liturgical places,
- hour themes,
- `patristic_homily_slug`,
- `chapter_study_slug`,
- `audio_slug`.

The slug fields are placeholders in this repo because the site corpus is not available here. Join them in `coptic-corpus` where homily, chapter-study, and audio metadata live.

## Synaxarium bridge behavior

Rows whose Coptic day is enumerated in the Ottawa/UKMID 69 dated-entry bridge taxonomy are `basis=explicit` and `confidence=high` in this run. Rows outside that taxonomy remain `basis=collection-type` and `confidence=medium`. They connect the primary commemoration of a fixed Coptic day to Katameros fixed-day rows. They are discovery links, not direct proper-reading proof for the named commemoration.

Repeated `(commem_id, coptic_day_key, slot)` groups are expected because the bridge catalogs source rows and variants. Do not render the bridge as a resolved daily service schedule without a later resolver.

Secondary commemorations are intentionally not linked unless a future source gives explicit proper-reading evidence.

## Deck deliverables

The deck artifacts are handoff aids for George, not site source files:

- `presentation/lectionary_design_layer_deck.pptx`
- `presentation/lectionary_design_layer_deck_outline.md`

Use them to explain the reverse lectionary design, Psalm numbering, Pascha attestation, Synaxarium bridge limits, and open questions before the final site push.

## Counts from this run

```json
{
  "reverse_lectionary_presentation_rows": 66381,
  "reverse_lectionary_index_rows": 8005,
  "reverse_lectionary_index_status_disagreement_rows": 0,
  "daily_lectionary_years": {
    "2020": 3713,
    "2021": 3716,
    "2022": 3711,
    "2023": 3683,
    "2024": 3711,
    "2025": 3678,
    "2026": 3718,
    "2027": 3714,
    "2028": 3709,
    "2029": 3716,
    "2030": 3696,
    "2031": 3702,
    "2032": 3722,
    "2033": 3711,
    "2034": 3716,
    "2035": 3708
  },
  "daily_lectionary_total_rows": 59324,
  "reading_identity_rows": 2657,
  "todays_readings_rows": 9,
  "psalm_crosswalk_rows": 161,
  "pascha_attestation_rows": 445,
  "pascha_attestation_bucket_manifest_rows": 5,
  "temporal_classification_rows": 445,
  "temporal_residue_rows": 419,
  "temporal_residue_manifest_rows": 5,
  "synaxarium_commemoration_rows": 664,
  "synaxarium_bridge_rows": 4688,
  "passage_footprint_rows": 2656,
  "passage_source_disclosure_rows": 66381,
  "foundational_reading_collection_rows": 69
}
```

## Deployment verification

After George pushes, verify the plain public URL, not only a cache-busted URL. A cache-buster can prove origin freshness but not normal user delivery.
