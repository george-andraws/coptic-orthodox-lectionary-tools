# @andraws/lectionary-data

Coptic Orthodox reverse-lectionary occasion index, date-resolved daily readings and a fixed-day Synaxarium titles catalog for npm consumers. Package release: **1.3.6**.

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

### Dual-numbering display references

`display_ref` is the human-facing reference. Psalm references use Masoretic Text numbering as the primary display form with Septuagint numbering inline when available. Consumers that need machine normalization should use `canonical_mt_ref`, `canonical_lxx_ref`, and `spans_json` instead of parsing `display_ref`.

### Removed markers

`removed_marker` carries source-derived removal or omission markers where they exist. Consumers should preserve this value and should not treat marked readings as active without checking the field.

## Daily file schema

Each daily file is a JSON object keyed by ISO date, for example `2026-04-12`. Each value is an array of readings for that date.

Shipped years: 2026, 2027, 2028.

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

## Known limitation

Structural-only occasions outside the shipped civil-year daily scope, such as some special services, remain available through `reverse_lectionary_index.jsonl`. Holy Week and Bright Saturday rows for shipped civil dates are included in daily files.

## Provenance

- Package version: 1.3.6.
- Existing reading schema version: 1.2.0. Package version and reading-schema version serve different purposes.
- Exact source commit, source-tree state, generation time, row counts and projection fingerprints are recorded in this artifact's `meta.json`, not a hardcoded historical README snapshot.
- Synaxarium provenance is separate: audited current-practice Coptic Reader capture of year 1743, 366 days and 868 titles. Do not present the older reading generation timestamp/commit as a new Synaxarium capture timestamp.

### Corrections in 1.3.6

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
