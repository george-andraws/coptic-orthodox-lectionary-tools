# Site Integration Spec: Coptic Lectionary Design Layer

Generated: 2026-06-16

George will push these files into the site repo. Hermes does not have `coptic-corpus` access in this run.

## Files to copy

Copy the following from this repo:

- `coptic-lectionary-and-synaxarium.md`
- `lectionary_spec.md`
- `out/design/lectionary_schema.json`
- `out/design/reverse_lectionary_presentation.csv`
- `out/design/reverse_lectionary_presentation.jsonl`
- `out/design/todays_readings_current_practice.csv`
- `out/design/todays_readings_current_practice.jsonl`
- `out/design/passage_liturgical_footprint.csv`
- `out/design/passage_liturgical_footprint.jsonl`
- `out/design/pascha_attestation.csv`
- `out/design/pascha_attestation_bucket_manifest.csv`
- `out/design/temporal_classification.csv`
- `out/design/temporal_residue.csv`
- `out/design/temporal_residue_manifest.csv`
- `out/design/synaxarium_commemorations.csv`
- `out/design/synaxarium_reading_bridge.csv`
- `out/design/source_registry.csv`
- `out/design/psalm_mt_lxx_crosswalk.csv`
- `audit_artifacts/open_questions_for_george.md`
- `presentation/lectionary_design_layer_deck.pptx`
- `presentation/lectionary_design_layer_deck_outline.md`

## Required search behavior

1. Accept MT or modern English input by default, for example `Psalm 51`.
2. Accept LXX liturgical Psalm input, for example `Psalm 50`, by consulting `canonical_lxx_ref` and the Psalm crosswalk.
3. Resolve both to `identity_key` before showing results.
4. Show `display_ref` to users. If LXX differs, keep the inline LXX annotation.
5. Never collapse historical and current readings without displaying `current_status`.

## Reverse lectionary page behavior

For each passage page:

- group by `current_status`, then season or source kind,
- show current Coptic Reader confirmed rows first where available,
- label historical Pascha witnesses clearly,
- include source and provenance links when present,
- show Synaxarium bridge rows only with their `basis`, `confidence`, and `note`.

## Synaxarium bridge behavior

All rows in `synaxarium_reading_bridge.csv` are `basis=collection-type` and `confidence=medium` in this run. They connect the primary commemoration of a fixed Coptic day to Katameros fixed-day rows. They are discovery links, not direct proper-reading proof for the named commemoration.

Repeated `(commem_id, coptic_day_key, slot)` groups are expected because the bridge catalogs source rows and variants. Do not render the bridge as a resolved daily service schedule without a later resolver.

Secondary commemorations are intentionally not linked unless a future source gives explicit proper-reading evidence.

## Today's readings behavior

Use `todays_readings_current_practice.csv` as the current static snapshot produced in this run. For dynamic production use, the site should generate a date key and resolve against the date-resolved reading table in the main lectionary package or a fresh current-practice source.

## Passage footprint behavior

Use `passage_liturgical_footprint.csv` for cards and chapter pages. It provides:

- occurrence counts,
- current and historical counts,
- sample liturgical places,
- hour themes,
- placeholder chapter-study and audio slugs.

The `patristic_homily_slug` field is blank in this repo because the site corpus is not available here. Join it in `coptic-corpus` where homily and chapter-study metadata live.

## Deck deliverables

The deck artifacts are handoff aids for George, not site source files:

- `presentation/lectionary_design_layer_deck.pptx`
- `presentation/lectionary_design_layer_deck_outline.md`

Use them to explain the reverse lectionary design, Psalm numbering, Pascha attestation, Synaxarium bridge limits, and open questions before the final site push.

## Counts from this run

```json
{
  "reverse_lectionary_presentation_rows": 66378,
  "reading_identity_rows": 2657,
  "todays_readings_rows": 11,
  "psalm_crosswalk_rows": 161,
  "pascha_attestation_rows": 445,
  "pascha_attestation_bucket_manifest_rows": 5,
  "temporal_classification_rows": 445,
  "temporal_residue_rows": 419,
  "temporal_residue_manifest_rows": 5,
  "synaxarium_commemoration_rows": 664,
  "synaxarium_bridge_rows": 4688,
  "passage_footprint_rows": 2656,
  "foundational_reading_collection_rows": 69
}
```

## Deployment verification

After George pushes, verify the plain public URL, not only a cache-busted URL. A cache-buster can prove origin freshness but not normal user delivery.
