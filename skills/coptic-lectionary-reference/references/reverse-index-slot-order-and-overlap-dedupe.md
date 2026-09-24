# Lectionary reverse-index slot/order metadata and overlap dedupe

Use when the requester asks to add or audit `slot_type`, `slot_order`, `occasion_kind`, intra-day duplicate readings, or Pascha prophecy ordering in `coptic-lectionary-research` / `@andraws/lectionary-data`.

## Source-of-truth rule

Fix the build pipeline and richer source data, not the lean JSONL by hand. Trace through:

1. occurrence / source CSVs and raw extracted sources
2. `build_lectionary_crosswalk.py`
3. `build_design_deliverables.py`
4. generated `out/design/reverse_lectionary_index.jsonl`
5. npm package projection under `packages/lectionary-data/`

When a shipped lean index is missing new fields that exist in `out/design`, treat that as a packaging/projection bug and validate the tarball itself.

## Slot normalization pattern

- Preserve original `slot` for provenance.
- Add `slot_type` as normalized class: `prophecy`, `psalm`, `gospel`, `pauline`, `catholicon`, `praxis`, or `source_label_preserved`.
- Add `slot_order` only when source-backed. Use explicit suffixes (`OT2 -> 2`), source CSV/API order, fixture order, source text order, or composite token order. Leave `null` for preserved/unmapped labels.
- Add `occasion_kind`: `cycle` for generic rule/cycle labels and `specific` for dated/named occasions.
- Report distinct slot values and the full cycle-label list. Report source-preserved labels as open items, not dropped rows.

## Intra-day overlap dedupe pattern

Within `(occasion, service_section, service_hour)`, compare structured scripture spans, not only identical strings or slot labels. Same book plus overlapping chapter/verse ranges can reveal duplicates such as split-vs-continuous Pascha readings.

For each cluster:

1. Print all members side by side: occasion, hour, slot, span, `identity_key`, source kind, and current `removed_marker`.
2. Query the strongest source available: Section 7.1 Coptic Reader fixture for Pascha Wednesday; otherwise Katameros API / copticchurch.net / local authoritative extracted source.
3. If source gives one continuous reading and local rows are split variants, keep the source-matching identity and set `removed_marker="superseded by <identity_key>"` on split rows. Do not delete rows.
4. If source shows genuinely distinct readings in one hour, keep both and assign distinct `slot_order`.
5. If no authoritative source is available, leave the cluster open. Do not invent a dedupe.

## Pascha prophecy ordering pattern

Pascha has mixed source layers: curated `OT#` day/hour rows and bare `Prophecy` source-text rows. Do not renumber bare `Prophecy` rows 1..n after `OT#` rows have already claimed positions.

- Build an authoritative per-day/hour order map from the curated/API day-hour source.
- For bare source-text prophecies that overlap a curated/API reading, inherit the curated/API absolute order.
- For source-text-only rows with no curated/API overlap, keep source-text sequence and flag as open against API confirmation.
- For Wednesday Day, use the Section 7.1 Coptic Reader fixture as the controlling source.
- Add regression guards for corrected rows so future rebuilds cannot silently revert ordering.

## Verification checklist

- Rebuild crosswalk and design outputs.
- Run both `verify_lectionary_queries.py` and `verify_design_deliverables.py`.
- Assert all JSONL rows parse.
- Assert every row has the new metadata fields when they are documented for the package.
- Validate the packed `.tgz`, not just source files.
- Report sourced vs inferred for every correction, count, and ordering decision.
- Keep open-item lists explicit and reviewable by the maintainer.
