# Coptic Lectionary Internal Spec

Generated: 2026-06-16

## Purpose

This spec defines the additive design layer produced in this repo for George's Coptic lectionary project. It preserves the existing validated package in `out/data/` and adds identity, attestation, temporal status, Synaxarium commemoration storage, Synaxarium reading bridge records, and site-facing outputs in `out/design/`.

## Locked decisions implemented

1. MT or modern English display remains primary for site search and user-facing references.
2. Psalm and LXX differences are stored in separate canonical fields. The identity key is not the raw source label.
3. Temporal status is derived from source attestation. The current Coptic Reader fixture governs Wednesday Day where present.
4. Printed Pascha witnesses are retained as historical evidence rather than deleted.
5. The Synaxarium is modeled as multiple commemorations per Coptic day.
6. Synaxarium reading links record their basis and confidence.

## Source authority tiers

| Tier | Meaning |
|---|---|
| current_authority | Coptic Reader where manually captured in a locked fixture. |
| public_current_practice_reference | Public current reading page such as copticchurch.net. |
| working_local_source | Structured local source used by George's package. |
| historical_printed_witness | Older printed book or extracted text useful for historical comparison. |
| scholarly_structural | Scholarly source used for structure, vocabulary, and precedence. |
| synaxarium_text_source | Source for daily commemorations. |

## Reading identity

Each reading has:

- `identity_key`, a deterministic hash over reading type and canonical fields.
- `display_ref`, MT or modern English primary with LXX annotation for Psalms where different.
- `canonical_mt_ref`.
- `canonical_lxx_ref`.
- `source_convention`.
- `canonicalization_confidence`.
- `canonicalization_note`.
- `spans_json`, an ordered list of parsed spans.

Named readings such as `Memoirs of Job` are stored as `named-reading` and do not enter normal passage search unless later resolved to a verse span by source.

## Liturgical placement

The target placement path is:

`occasion -> service -> hour -> slot -> order`

The design layer stores this through:

- `occasion`
- `calendar_key`
- `day_title`
- `service_day`
- `service_hour`
- `service_section`
- `slot`
- `order`

This retires lossy labels such as generic `OT1` where a richer slot can be produced later, while preserving old slot values for traceability.

## Temporal lifecycle

The design layer uses these status classes:

- `current_confirmed_coptic_reader`
- `current_confirmed_by_fixture_equivalence`
- `current_psalm_equivalence_unresolved`
- `historical_candidate_removed`
- `historical_witness`
- `current_working_source_not_coptic_reader_checked`
- `current_public_or_local_reference`

The main unresolved limitation is current-practice coverage outside the locked Coptic Reader Wednesday Day fixture. Those rows are not presented as Coptic Reader confirmed.

## Attestation

Pascha attestation groups rows by day, hour, and identity key. Buckets:

- `current_confirmed`: a Coptic Reader fixture row is present in the group.
- `consensus_without_coptic_reader`: two or more non-Coptic Reader sources agree after normalization.
- `old_edition_only`: only historical printed or extracted witnesses attest the row.
- `old_edition_only_candidate_removed`: older/local data attests the row but the current Coptic Reader fixture omits it within fixture scope.
- `single_source_candidate`: one source attests the row and no current-authority fixture confirms it.

Public or local current-reference rows are not the same as Coptic Reader-confirmed rows. `current_public_or_local_reference` means useful reference data, not final current-practice authority.

## Controlled vocabulary snapshot

The machine-readable source of truth is `out/design/lectionary_schema.json`. It includes explicit values for:

- `source_convention`: `modern_english_reference`, `mt_nkjv`, `lxx_liturgical_or_fixture_label`.
- `canonicalization_confidence`: `high`, `medium`, `low`, `n/a`.
- `current_status`: `current_confirmed_coptic_reader`, `current_confirmed_by_fixture_equivalence`, `current_psalm_equivalence_unresolved`, `historical_candidate_removed`, `historical_witness`, `current_working_source_not_coptic_reader_checked`, `current_public_or_local_reference`, `unknown`.
- `attestation_bucket`: `current_confirmed`, `consensus_without_coptic_reader`, `old_edition_only`, `old_edition_only_candidate_removed`, `single_source_candidate`.
- `service_day`, `service_hour`, and `service_section`: source labels are preserved when the source's service structure does not fit a normalized value.
- `slot`: normalized Scripture and liturgical slots plus `source_label_preserved`.
- Synaxarium `type`: `lord_feast`, `theotokos`, `martyr`, `apostle`, `patriarch`, `hierarch`, `departure`, `prophet`, `angel`, `ascetic`, `feast`, `commemoration`.
- bridge `basis`: `explicit`, `collection-type`, `inferred`.
- bridge `confidence`: `high`, `medium`, `low`.

## Psalm MT to LXX crosswalk

The design layer includes `out/design/psalm_mt_lxx_crosswalk.csv`. It encodes the chapter seams from the design brief. It does not guess verse offsets except where prior content comparison already established an example. Exact verse work still requires Brenton text comparison.

## Synaxarium model

Each commemoration is stored separately in `out/design/synaxarium_commemorations.csv`:

- `commem_id`
- `coptic_month`
- `coptic_day`
- `rank`
- `title`
- `type`
- `source`
- `source_url`

## Synaxarium bridge

Bridge rows live in `out/design/synaxarium_reading_bridge.csv`:

- `commem_id`
- `reading_identity_key`
- `slot`
- `basis`
- `confidence`
- `citation`

The bridge uses `collection-type` basis for primary day commemorations linked to fixed-day Katameros readings. Multi-commemoration days are confidence `medium` and are listed for review in the open questions file.

## Controlled vocabularies

See `out/design/lectionary_schema.json` for machine-readable vocabularies. The 69 collection count is source-confirmed through F.N. Youssef, but the accessible sources in this run did not expose a fully enumerated English list. The spec therefore stores a working type list and records the full list as a source gap rather than inventing it.

## Site-facing outputs

- `out/design/reverse_lectionary_presentation.csv`
- `out/design/reverse_lectionary_presentation.jsonl`
- `out/design/todays_readings_current_practice.csv`
- `out/design/passage_liturgical_footprint.csv`
- `out/design/pascha_attestation.csv`
- `out/design/temporal_classification.csv`
- `out/design/synaxarium_commemorations.csv`
- `out/design/synaxarium_reading_bridge.csv`
- `site_integration_spec.md`

## Acceptance notes

- Structural claims in the article cite named sources.
- Inferences are flagged.
- The schema is complete enough to drive the additive design-layer outputs.
- Full Coptic Reader ingestion is not claimed because the project brief states that Coptic Reader content is encrypted and manual fixtures are the route.
