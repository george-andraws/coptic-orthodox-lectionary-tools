# @andraws/lectionary-data

Coptic Orthodox reverse-lectionary occasion index, date-resolved daily readings and a fixed-day Synaxarium titles catalog for npm consumers. Package release: **1.3.8**.

## What this package contains

- `data/reverse_lectionary_index.jsonl`: one JSON object per line for reverse lookup by lectionary occasion and reading identity.
- `data/daily/lectionary-2026.json`, `lectionary-2027.json`, and `lectionary-2028.json`: date-resolved readings keyed by ISO date.
- `data/synaxarium/synaxarium.json`: 366 Coptic day objects with 868 audited Coptic Reader commemoration titles and common/leap-year validity flags.
- `calendar.js`: pure Gregorian-to-Coptic conversion and the frozen public month slugs, also suitable for browser bundling.
- `index.js`: CommonJS exports for stable paths, reading metadata/classification, the Synaxarium API and the calendar module.
- `meta.json`: package provenance, schema version, counts, shipped years, structural daily materialization summary, and schema notes. In `daily_files`, `rows` is retained as the legacy date-count field; use `date_count` and `reading_count` for explicit counts.

## Usage

```js
const lectionaryData = require('@andraws/lectionary-data');

console.log(lectionaryData.occasionIndexPath);
console.log(lectionaryData.dailyYearPath(2026));
console.log(lectionaryData.shippedYears);
console.log(lectionaryData.meta.source_repo_commit);
console.log(lectionaryData.classifyDate('2026-04-10'));
console.log(lectionaryData.isCurrentReading({ display_ref: 'Jn 1:1-17' }));
```

## Exports

- `occasionIndexPath`: absolute path to `data/reverse_lectionary_index.jsonl`.
- `dailyDir`: absolute path to `data/daily`.
- `dailyYearPath(year)`: returns the absolute path for a shipped daily lectionary JSON file.
- `classifyDate(date)`: classifies a shipped ISO date as present in daily JSON or as a documented structural-only Holy Week/Bright Saturday gap.
- `isRemovedReading(row)`: returns true for rows marked `active: false` or `status: "removed"`.
- `isActiveReading(row)`: backwards-compatible convenience negation of `isRemovedReading(row)`; it does not exclude every historical or superseded state.
- `isCurrentReading(row)`: returns true only for unmarked legacy rows or supported current-status values; removal markers, superseded rows, and historical witnesses are false.
- `structuralDateResolver`: resolver metadata copied from `meta.structural_date_resolver`.
- `shippedYears`: frozen array of shipped daily years.
- `meta`: parsed `meta.json`.

## Synaxarium co-display catalog

`data/synaxarium/synaxarium.json` contains 366 fixed Coptic days and 868 titles from the audited single-year 1743 capture. Source: Coptic Reader, Diocese of the Southern US, current-practice, single-year 1743 capture.

```js
const { gregorianToCoptic, synaxariumForCopticDay, synaxariumMeta } = require('@andraws/lectionary-data');
const date = gregorianToCoptic(2026, 9, 11);
const day = synaxariumForCopticDay(date.monthSlug, date.day);
console.log(day.commemorations, synaxariumMeta);
```

- `gregorianToCoptic(year, month, day)`: pure proleptic Gregorian conversion for valid civil dates in years 0001 through 9999, independent of shipped reading years and local timezone. Returns `{ year, monthSlug, day }`. Pre-epoch Coptic years use astronomical numbering.
- `synaxariumForCopticDay(monthSlug, day)`: immutable day object with an ordered `commemorations` array and `validInCommonYear` / `validInLeapYear`. Only Nasie 6 is leap-only. Invalid month/day arguments throw `RangeError`.
- `synaxariumMeta`: `day_count`, `total_commemorations`, and `source`.
- `synaxariumPath`: absolute catalog path. `frozenMonthSlugs`: immutable ordered month list.
- `calendar.js`: the same dependency-free converter module, suitable for bundling in a browser without the Node path-based entry point.

Frozen slugs: `tout`, `baba`, `hatour`, `kiahk`, `toba`, `amshir`, `baramhat`, `baramouda`, `bashans`, `paona`, `abib`, `mesra`, `nasie`.

Each commemoration has only `id`, `title`, `type`, `rank`, `displayOrder`, `displayGroupId`. IDs and titles preserve the audited capture exactly. Types are lexical catalog classifications, not new historical findings. Lower `rank` is first: rank and displayOrder preserve capture order, not a claim about liturgical precedence. `displayGroupId` is null because no grouping decisions were authorized. No entries are merged or split.

The readings and commemorations may share a Coptic date, but they are not liturgically linked. This catalog supplies no explanation for the choice of readings and makes no assertion that the Synaxarium is prescribed aloud at a given service.

Repository maintainers can regenerate with `python3 scripts/build_synaxarium.py SOURCE_DIR`, then run `npm run synaxarium:validate` and `npm run lectionary:validate` from the package directory. The source fingerprint fixture stays in the repository tests, outside the published package. The lectionary integrity gate includes synaxarium validation. Synaxarium capture provenance remains separate from the reading-source provenance recorded in `meta.json`. These maintainer commands require the source checkout; scripts and fingerprint fixtures are not included in an isolated npm installation.

The consuming site uses compact civil/Coptic date headings, an expanded Synaxarium entry after Praxis, and an expanded Today in the Church card. Consumers must keep the date-based catalog independent of reading selection, even when rendering it between reading slots. No full Synaxarium narratives are included.

## Occasion index schema

Each line in `data/reverse_lectionary_index.jsonl` is a JSON object. The published field set is:

- `occasion`
- `service_section`
- `service_hour`
- `slot`
- `slot_type`
- `slot_order`
- `occasion_kind`
- `identity_key`
- `display_ref`
- `canonical_mt_ref`
- `canonical_lxx_ref`
- `spans_json`
- `removed_marker`
- `hour_theme`
- `source_disclosure`
- `attestation_year_min`
- `attestation_year_max`

Rows that were removed from active lookup by source-priority projection include additional fields:

- `active: false`
- `status: "removed"`
- `removal_reason`
- `removal_context_key`
- `preferred_source_family`
- `preferred_display_ref`
- `preferred_identity_key`
- `consumer_note`
- `retained_for: "provenance_only"`

Default consumers should filter with `isCurrentReading(row)`. `isActiveReading(row)` retains its narrower backwards-compatible meaning and is appropriate only when historical/source-marked rows are intentionally included.

### Additive calendar, service and review metadata in 1.3.7

- `coptic_date_key`: fixed Coptic day in the public catalog's slug form, such as `kiahk-23`. Empty for movable and annual-Sunday contexts.
- `annual_sunday`: month and ordinal Sunday, such as `bashans-3`, independently qualified from the source table. It is never a fixed date.
- `display_label`: normalized reader-facing occasion terminology. Original `occasion`, raw calendar labels and source locators are retained.
- `pascha_service`, `pascha_offset_days`, `pascha_civil_date`: explicit day or Eve context. Civil-evening dating is not inferred from ambiguous legacy Eve labels.
- `occurs_in_shipped_years`: whether this appointment is present in the final packaged daily files. This is not a universal absence claim.
- `displaced_by`: possible seasonal overlap in the disclosed computus-cycle sample, not an ecclesiastical rank or a calendar-selection rule. See `occurrence_scope` before using it.
- `composite_fragments_json`: original source-qualified fragment rows retained inside a single ordered composite appointment.

New source-owned disclosures preserve exact source text, hashes, scope and qualification. Rows held for Reader review have `active: false`; use `isCurrentReading` rather than treating a date's nonempty array as proof of completeness. Never parse held printed Psalm labels into invented canonical coordinates. Normalized reading date keys permit date-only catalog lookup, not a reading-to-saint association.

### Dual-numbering display references

`display_ref` is the human-facing reference. Psalm references use Masoretic Text numbering as the primary display form with Septuagint numbering inline when available. Consumers that need machine normalization should use `canonical_mt_ref`, `canonical_lxx_ref`, and `spans_json` instead of parsing `display_ref`.

### Removed markers

`removed_marker` carries source-derived removal or omission markers where they exist. Consumers should preserve this value and should not treat marked readings as active without checking the field.

## Daily file schema

Each daily file is a JSON object keyed by ISO date, for example `2026-04-12`. Each value is an array of readings for that date.

Shipped years: 2026, 2027, 2028.

### Guaranteed fields by representation (T-L5)

Daily rows and reverse-index rows are different public representations. The following lists state which keys every row in that representation guarantees. A guaranteed key may contain an empty string or an empty JSON-encoded array; presence does not establish source confirmation or canonical-coordinate approval. Other fields are additive and source-dependent.

Reverse-index guaranteed keys:

<!-- reverse-guaranteed-fields -->
```json
[
  "attestation_year_max", "attestation_year_min", "authority_tier", "calendar_keys",
  "canonical_lxx_ref", "canonical_mt_ref", "current_status", "day_titles",
  "display_label", "display_ref", "hour_theme", "identity_key", "occasion",
  "occasion_kind", "provenance", "reading_name", "reading_type", "removed_marker",
  "service_hour", "service_section", "slot", "slot_order", "slot_type",
  "source_disclosure", "source_disclosure_count", "source_edition", "source_family",
  "source_kind", "source_locator", "source_title", "spans_json"
]
```

Daily-reading guaranteed keys:

<!-- daily-guaranteed-fields -->
```json
[
  "canonical_lxx_ref", "canonical_mt_ref", "current_status", "display_label",
  "display_ref", "identity_key", "occasion", "reading_order", "reading_type",
  "removed_marker", "service_hour", "service_order", "service_section", "slot",
  "slot_order", "slot_type", "source_disclosure", "source_family", "source_kind",
  "source_locator", "spans_json"
]
```

`day_titles` is not guaranteed in daily rows. It can be present on a source-qualified supplement, but consumers must not require it. Use `row.get('day_titles', '')` in Python or `row.day_titles ?? ''` in JavaScript for optional access. Use `display_label` for a reader-facing occasion and retain `occasion` as the raw appointment context. The ISO date belongs to the outer daily-object key, not a guaranteed `gregorian_date` cell inside every row.

Each daily reading includes a unique `reading_order` within that date. The package uses deterministic service-stage ordering, retaining source-backed prophecy, epistle, Psalm, Gospel and companion-fragment sequences. Ordinary Liturgy follows Pauline, Catholic, Acts, Psalm and Gospel; exceptional services use their qualified source tables rather than that ordinary cardinality rule. `slot_order` may repeat for split Psalm verses or readings that share one liturgical slot; use `reading_order` when a unique date-local order is required.

In `meta.daily_files`, `rows` is retained as a legacy alias for `date_count`. Use `date_count` for the number of ISO date keys and `reading_count` for the total number of readings across those dates.

## Structural Holy Week / Bright Saturday daily rows

The package date-resolves qualified Holy Week and Bright Saturday structural rows into the shipped daily files, including missing appointments on partially populated dates, and applies the documented Annunciation collision exception. Existing distinct services and source witnesses are preserved. Every shipped civil date in 2026, 2027, 2028 has a daily JSON key; that coverage alone does not establish independent primary-source verification of every reading.

`meta.structural_date_resolver.structural_daily_additions_by_year` lists the civil dates filled from structural Pascha/Bright Saturday rows. `classifyDate(date)` returns `hasDailyReadings: true` for every shipped civil date that has a daily key.

## Source-priority projection

The package projects the raw reverse index into a consumer-safe runtime index. When a copticchurch.net date-resolved row and a lower-priority local cycle row overlap the same normalized consumer occasion, service, service hour, and slot type but disagree on the passage span, the lower-priority variant is retained as inactive provenance rather than used as an active lookup row.

Inactive projection rows are marked with `active: false`, `status: "removed"`, `removed_marker: "removed_by_source_priority_projection"`, a `consumer_note`, and preferred-reading fields such as `preferred_source_family`, `preferred_display_ref`, and `preferred_identity_key`. Use `isCurrentReading(row)` for default current-reading lookups.

For fixed-date rows with a Sunday-specific counterpart, generic rows are disambiguated as non-Sunday contexts rather than silently duplicated.

Projection counts and examples are recorded in `meta.projection_rules`.

## Span and Psalm numbering contract

`spans_json` contains machine-readable canonical spans when the reading can be represented as biblical book/chapter/verse ranges. An authenticated source-only selection with unresolved edition coordinates, or a named unversified excerpt, can have empty canonical references and an empty span array. Preserve its printed selection, source disclosure and qualification; do not infer numeric coordinates from its display label. Named non-standard readings, such as `Memoirs of Job`, also use `reading_type`, `reading_name`, and `display_ref`.

Psalm `display_ref` values may include inline dual numbering, for example `Ps 105:14-15 (LXX Ps 104:14-15)`. Consumers should not parse `display_ref` for machine matching. Use `canonical_mt_ref`, `canonical_lxx_ref`, and `spans_json`.

## Provenance and composite evidence in 1.3.8

`provenance` is a reader-facing source name, plain text of at most 300 characters. It is not an authentication envelope. Source authority, current status, coordinate qualifications and literal source locators remain separate fields.

When a former provenance value contains structured evidence or exceeds the display limit, two additive public fields preserve that evidence:

- `provenance_format`: the literal string `lectionary_provenance_v1`.
- `provenance_evidence_json`: a serialized JSON object in exactly one of these two forms:

```json
{
  "schema": "lectionary_provenance_v1",
  "legacy_provenance": "<complete original serialized evidence or source qualification>"
}
```

For an R4 composite, fragment records belong in `composite_fragments_json`, not in `provenance` or duplicated in the evidence envelope:

```json
{
  "schema": "lectionary_provenance_v1",
  "composite_provenance_prefix": "<original source prefix>; R4 composite_fragments="
}
```

The latter form reconstructs the exact predecessor evidence by concatenating its prefix with the complete `composite_fragments_json` cell. It requires that companion cell. Duplicate members, extra envelope fields, missing evidence, unknown schemas and nonstring payloads are invalid.

`composite_fragments_json` is an ordered array of complete source fragment records. Ordered `spans_json` describes one composite appointment. The public key `original_source_row` retains source snapshots formerly held in an internal temporary-key spelling, including nested serialized snapshots. The internal validator adapter restores the prior spelling without dropping evidence. Source titles, locators, raw calendar keys, source identities, lifecycle fields and primary-source qualifications are retained.

The LK5 `composite_review` value `LK5_archived_source_cell_v1` identifies the bounded inactive-appointment projection. These composites stay inactive; their complete original split witnesses remain in their fragment arrays and unchanged in raw source data. They are not additions to current daily readings.

**Consumer migration:** these additive JSON cells transport evidence; they do not grant trust. Decode with `restore_public_row(s)` before existing exact source/disclosure/lifecycle checks. For historical reverse membership or retirement validation, `legacy_validation_rows` also authenticates the bounded LK5 composite and restores its original inactive witness records. Never replace membership/source checks with successful decoding, build new membership oracles from candidate rows, or present historical validator expansions as current daily appointments.

## Service evidence and Psalm annotations in 1.3.8

`evidence_status` and `evidence_json` preserve the exact retained document, reading heading, line, body hash and service context for reviewed special-service occurrences. The same source qualification is included in each affected `source_disclosure` entry. Reader-backed authority metadata is separate from `current_status`: attaching a retained capture does not silently activate an inactive witness or change the appointed reading. Uncaptured Agpeya and Palm Sunday printed-book witnesses retain `unverified_service_book`, their named editions and open revision-date questions.

The undated Covenant Thursday Lakkan Pauline carries a same-service marker based on the authenticated service title and complete Pauline body. This does not assert that its entire indexed table equals the dated Water Liturgy table, and neither source witness is deleted.

`psalm_annotation_review_json` documents bounded annotation corrections. MT/NKJV remains primary. Corrected LXX annotations are derived only after the stored coordinates have been qualified as MT; source-only selections, numeric source-coordinate holds and exact retained edition exceptions remain separately qualified. A chapter-number offset alone does not establish verse equivalence. Annotation repairs retain occurrence identities and raw source references.

These fields are additive. The source-owned Python validation adapters live in the source repository, not in the npm artifact. Consumers must preserve the evidence cells and cannot treat a successful JSON decode as source authentication.

## Known limitation

Structural-only occasions outside the shipped civil-year daily scope, such as some special services, remain available through `reverse_lectionary_index.jsonl`. Holy Week and Bright Saturday rows for shipped civil dates are included in daily files.

## Provenance

- Package version: 1.3.8.
- Existing reading schema version: 1.2.0. Package version and reading-schema version serve different purposes.
- Exact source commit, source-tree state, generation time, row counts and projection fingerprints are recorded in this artifact's `meta.json`, not a hardcoded historical README snapshot.
- Synaxarium provenance is separate: audited current-practice Coptic Reader capture of year 1743, 366 days and 868 titles. Do not present the older reading generation timestamp/commit as a new Synaxarium capture timestamp.

### Corrections in 1.3.7

- Kiahk 23's weekday table uses the authenticated complete Reader table, including Matins Matthew 12:1-8. The competing old table survives as inactive source evidence. The bounded weekday policy excludes Sundays and other selected occasions; 2028's Sunday table is not replaced.
- Last Friday of Great Lent Matins uses Luke 16:19-31 under the bounded retained Reader and recurring source-table policy.
- Source-confirmed Holy Week repairs and additions retain explicit Eve/civil-date context. Unconfirmed copied Tuesday-night rows and identified erroneous readings remain inactive holds; printed witnesses are not promoted by inference.
- Normalized fixed-date/Sunday metadata, reader-facing terminology and descriptive occurrence fields sit beside unchanged raw keys.
- Reviewed split source cells become single ordered composite appointments. Reader's Bel selection retains its source-coordinate qualification instead of claiming Daniel chapter 1 or unverified Brenton equivalence.

This is not a whole-corpus fresh Reader verification. Remaining Holy Week checks, source-edition questions and duplicate Great Thursday hours are tracked in the repository's release report and check sheet. The website is not updated by this release.

### Previous corrections in 1.3.6

- Third Sunday of Babah Pauline: `1Cor 16:12-24`, preserving the superseded printed reference and correction evidence.
- Source-qualified Jonah Fast and Lent prophecy supplementation, ordinary-reading parser/appointment repairs, and service-stage ordering.
- Bounded Psalmody, Bright Saturday and Covenant Thursday additions with source ordinals, printed references, provenance and historical witness qualifications retained.
- Historical witnesses cannot suppress current appointments through source-priority competition.
- Four Bright Saturday composite Psalm selections retain unresolved canonical-coordinate holds; Covenant Thursday's named Exodus/Joshua excerpts remain unversified. Psalm 151 has no invented MT counterpart. Unresolved source/edition questions are not silently activated or converted.

These are bounded source-qualified corrections, not a claim that every reading was newly verified against Coptic Reader. The public calendar converter and Synaxarium catalog remain unchanged. Repository documentation edits do not mutate immutable earlier npm artifacts.

## License

This package is licensed under CC-BY-4.0.

Required attribution:
Coptic lectionary data from Light and Logos (andraws.net), licensed under CC BY 4.0.

License deed: https://creativecommons.org/licenses/by/4.0/

Scope: The lectionary readings and their liturgical assignments are the tradition of the Coptic Orthodox Church. This license applies to the compilation, structure, encoding, identity keys, and editorial curation in this dataset, not to the underlying tradition.
