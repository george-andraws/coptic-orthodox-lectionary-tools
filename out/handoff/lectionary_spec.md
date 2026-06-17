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
- `reading_name`, for named non-verse readings such as `Memoirs of Job`.
- `source_label`, the raw or preserved source label used for matching.
- `display_ref`, MT or modern English primary with LXX annotation for Psalms where different.
- `canonical_mt_ref`.
- `canonical_lxx_ref`.
- `source_convention`.
- `canonicalization_confidence`.
- `canonicalization_note`.
- `spans_json`, an ordered list of parsed spans.

The `spans_json` value is an ordered list of span objects. Each span carries `source_ref`, `source_convention`, `canonical_mt_ref`, `canonical_lxx_ref`, `confidence`, `validation_basis`, `book`, `chapter_start`, `verse_start`, `chapter_end`, and `verse_end`. Composite and cross-Psalm references are therefore not reduced to one flattened range.

Named readings such as `Memoirs of Job` are stored as `named-reading` with `reading_name`; they do not enter normal passage search unless later resolved to a verse span by source.

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
- `pending_psalm_equivalence_unresolved`
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
- `occasion`: emitted placement category; `occasion_type` is retained in the schema as an alias for the same conceptual vocabulary.
- `canonicalization_confidence`: `high`, `medium`, `low`, `n/a`.
- `current_status`: `current_confirmed_coptic_reader`, `current_confirmed_by_fixture_equivalence`, `pending_psalm_equivalence_unresolved`, `historical_candidate_removed`, `historical_witness`, `current_working_source_not_coptic_reader_checked`, `current_public_or_local_reference`, `unknown`.
- `current_authority`: separate from `current_status`; it states which authority, if any, is allowed to govern current practice for that row.
- `removed_marker`: uniform placement-level string for older Pascha placements absent from the scoped current Coptic Reader fixture. The marker cites the older source boundary and the current comparator that lacks it.
- `source_title`, `source_edition`, `source_locator`, and `source_url`: citable provenance fields carried by placement and disclosure rows. `source_locator` points to a page, URL, local source row, extracted text line, or API/cache field.
- `attestation_bucket`: `current_confirmed`, `consensus_without_coptic_reader`, `old_edition_only`, `old_edition_only_candidate_removed`, `single_source_candidate`.
- `service_day`, `service_hour`, and `service_section`: source labels are preserved when the source's service structure does not fit a normalized value.
- `slot`: normalized Scripture and liturgical slots plus `source_label_preserved`.
- Psalm `mapping_scope`: `chapter_equivalence`, `split_merge_chapter_seam`, `lxx_unique_chapter`, `anchored_verse_example`, `unresolved_verse_offset_example`.
- Synaxarium `type`: `lord_feast`, `theotokos`, `martyr`, `apostle`, `patriarch`, `hierarch`, `departure`, `prophet`, `angel`, `ascetic`, `feast`, `commemoration`.
- bridge `basis`: `explicit`, `collection-type`, `inferred`.
- bridge `confidence`: `high`, `medium`, `low`.
- `collection_types_69`: the 69 foundational reading collections keyed by `collection_key` and `coptic_day_key`, with membership verdict and source provenance.

## Foundational reading collections

The machine-readable vocabulary is `out/design/foundational_reading_collections_69.csv` and `out/design/foundational_reading_collections_69.jsonl`. It is also embedded under `controlled_vocabularies.collection_types_69` in `out/design/lectionary_schema.json`.

Membership verdict: `INFERRED_LIKELY_SAME_SET` (roster unverified). Youssef gives 69 collections by commemoration type; the Ottawa Katameros of the Days TOC presents a matching count of dated entries. Alignment is inferred from shared source tradition, volume two placement, category match, and count, not from a matched reading-by-reading roster.

Provenance:

- Youssef source: F.N. Youssef, `The Arrangement of the Church Lectionary`, ACCOT, Chapter 1, section 1.1, printed page marker 32, note 7 `al-qirā’āt al-āsāsiyya`.
- Ottawa source: St. Mary Ottawa / UKMID, `Katameros of the Days: Readings for Week Days and Feasts`, first edition, Christmas 1714 A.M., 1998 A.D.
- Ottawa locators: introduction on PDF page 17; TOC dated reading sections on PDF pages 23 to 26; annual day table on PDF pages 31 to 65.
- Source-vs-inference: the 69 dated entries and their section pages are read from Ottawa/UKMID; alignment with Youssef's named 69 collections is inferred, roster unverified, and not read from a Youssef-printed roster.

| # | collection_key | Coptic day | section page |
|---|---|---|---|
| 1 | `foundational-01-tut-01` | Tut 1 | 37 |
| 2 | `foundational-02-tut-02` | Tut 2 | 47 |
| 3 | `foundational-03-tut-08` | Tut 8 | 55 |
| 4 | `foundational-04-tut-16` | Tut 16 | 64 |
| 5 | `foundational-05-tut-17` | Tut 17 | 72 |
| 6 | `foundational-06-tut-18` | Tut 18 | 81 |
| 7 | `foundational-07-tut-19` | Tut 19 | 88 |
| 8 | `foundational-08-tut-21` | Tut 21 | 96 |
| 9 | `foundational-09-tut-26` | Tut 26 | 102 |
| 10 | `foundational-10-babah-12` | Babah 12 | 111 |
| 11 | `foundational-11-babah-14` | Babah 14 | 118 |
| 12 | `foundational-12-babah-22` | Babah 22 | 127 |
| 13 | `foundational-13-babah-27` | Babah 27 | 135 |
| 14 | `foundational-14-hatur-08` | Hatur 8 | 143 |
| 15 | `foundational-15-hatur-09` | Hatur 9 | 151 |
| 16 | `foundational-16-hatur-12` | Hatur 12 | 159 |
| 17 | `foundational-17-hatur-15` | Hatur 15 | 169 |
| 18 | `foundational-18-hatur-17` | Hatur 17 | 177 |
| 19 | `foundational-19-hatur-22` | Hatur 22 | 187 |
| 20 | `foundational-20-hatur-24` | Hatur 24 | 194 |
| 21 | `foundational-21-hatur-25` | Hatur 25 | 202 |
| 22 | `foundational-22-hatur-27` | Hatur 27 | 211 |
| 23 | `foundational-23-hatur-28` | Hatur 28 | 218 |
| 24 | `foundational-24-hatur-29` | Hatur 29 | 227 |
| 25 | `foundational-25-kiyahk-22` | Kiyahk 22 | 236 |
| 26 | `foundational-26-kiyahk-28` | Kiyahk 28 | 245 |
| 27 | `foundational-27-kiyahk-29` | Kiyahk 29 | 255 |
| 28 | `foundational-28-kiyahk-30` | Kiyahk 30 | 263 |
| 29 | `foundational-29-tubah-01` | Tubah 1 | 270 |
| 30 | `foundational-30-tubah-03` | Tubah 3 | 280 |
| 31 | `foundational-31-tubah-04` | Tubah 4 | 288 |
| 32 | `foundational-32-tubah-06` | Tubah 6 | 297 |
| 33 | `foundational-33-tubah-10` | Tubah 10 | 305 |
| 34 | `foundational-34-tubah-11` | Tubah 11 | 313 |
| 35 | `foundational-35-tubah-12` | Tubah 12 | 322 |
| 36 | `foundational-36-tubah-13` | Tubah 13 | 330 |
| 37 | `foundational-37-tubah-22` | Tubah 22 | 338 |
| 38 | `foundational-38-tubah-26` | Tubah 26 | 346 |
| 39 | `foundational-39-tubah-30` | Tubah 30 | 354 |
| 40 | `foundational-40-amshir-02` | Amshir 2 | 361 |
| 41 | `foundational-41-baramhat-13` | Baramhat 13 | 370 |
| 42 | `foundational-42-baramhat-29` | Baramhat 29 | 379 |
| 43 | `foundational-43-baramoudah-23` | Baramoudah 23 | 388 |
| 44 | `foundational-44-baramoudah-27` | Baramoudah 27 | 396 |
| 45 | `foundational-45-baramoudah-30` | Baramoudah 30 | 404 |
| 46 | `foundational-46-bashans-01` | Bashans 1 | 413 |
| 47 | `foundational-47-bashans-10` | Bashans 10 | 423 |
| 48 | `foundational-48-bashans-20` | Bashans 20 | 431 |
| 49 | `foundational-49-bashans-24` | Bashans 24 | 439 |
| 50 | `foundational-50-bashans-26` | Bashans 26 | 448 |
| 51 | `foundational-51-baunah-02` | Baunah 2 | 456 |
| 52 | `foundational-52-baunah-16` | Baunah 16 | 465 |
| 53 | `foundational-53-baunah-30` | Baunah 30 | 473 |
| 54 | `foundational-54-abib-03` | Abib 3 | 481 |
| 55 | `foundational-55-abib-05` | Abib 5 | 491 |
| 56 | `foundational-56-abib-20` | Abib 20 | 500 |
| 57 | `foundational-57-misra-03` | Misra 3 | 507 |
| 58 | `foundational-58-misra-13` | Misra 13 | 515 |
| 59 | `foundational-59-misra-17` | Misra 17 | 524 |
| 60 | `foundational-60-misra-25` | Misra 25 | 532 |
| 61 | `foundational-61-misra-26` | Misra 26 | 540 |
| 62 | `foundational-62-misra-28` | Misra 28 | 547 |
| 63 | `foundational-63-misra-29` | Misra 29 | 555 |
| 64 | `foundational-64-misra-30` | Misra 30 | 562 |
| 65 | `foundational-65-al-nasi-01` | Al-Nasi 1 | 569 |
| 66 | `foundational-66-al-nasi-02` | Al-Nasi 2 | 579 |
| 67 | `foundational-67-al-nasi-03` | Al-Nasi 3 | 586 |
| 68 | `foundational-68-al-nasi-04` | Al-Nasi 4 | 595 |
| 69 | `foundational-69-al-nasi-06` | Al-Nasi 6 | 602 |

## Psalm MT to LXX crosswalk

The design layer includes `out/design/psalm_mt_lxx_crosswalk.csv`. It encodes chapter seams from the design brief and separates `mapping_scope` values for chapter equivalence, split/merge chapter seams, LXX-only Psalm 151, anchored verse examples, and unresolved verse-offset examples. It does not guess verse offsets except where Brenton/KJV content comparison established an example.

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
- `coptic_day_key`
- `commemoration_title`
- `commemoration_type`
- `reading_identity_key`
- `display_ref`
- `slot`
- `basis`
- `confidence`
- `citation`
- `note`

Rows whose Coptic day is enumerated in the Ottawa/UKMID 69 dated-entry bridge taxonomy use `explicit` basis and `high` confidence. Outside those 69 days, bridge rows remain `collection-type` and `medium`. Repeated groups are source-row or variant catalog rows, not resolved daily service schedules.

## Controlled vocabularies

See `out/design/lectionary_schema.json` for machine-readable vocabularies. The 69 collection vocabulary is enumerated from the Ottawa/UKMID TOC and records the inferred-likely membership verdict, provenance, and source-vs-inference caveat.

## Site-facing outputs

- `out/design/reverse_lectionary_presentation.csv`
- `out/design/reverse_lectionary_presentation.jsonl`
- `out/design/todays_readings_current_practice.csv`
- `out/design/passage_liturgical_footprint.csv`
- `out/design/pascha_attestation.csv`
- `out/design/temporal_classification.csv`
- `out/design/synaxarium_commemorations.csv`
- `out/design/synaxarium_reading_bridge.csv`
- `out/design/foundational_reading_collections_69.csv`
- `out/design/foundational_reading_collections_69.jsonl`
- `out/design/passage_source_disclosure.csv`
- `out/design/passage_source_disclosure.jsonl`
- `site_integration_spec.md`

## Acceptance notes

- Structural claims in the article cite named sources.
- Inferences are flagged.
- The schema is complete enough to drive the additive design-layer outputs.
- Removed Pascha placements remain in the model with `removed_marker`; they are historical witnesses, not deleted rows.
- Full Coptic Reader ingestion is not claimed because the project brief states that Coptic Reader content is encrypted and manual fixtures are the route.
