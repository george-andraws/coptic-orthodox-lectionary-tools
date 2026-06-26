# @andraws/lectionary-data

Coptic Orthodox reverse-lectionary occasion index and date-resolved daily readings packaged for npm consumers.

## What this package contains

- `data/reverse_lectionary_index.jsonl`: one JSON object per line for reverse lookup by lectionary occasion and reading identity.
- `data/daily/lectionary-2026.json`, `lectionary-2027.json`, and `lectionary-2028.json`: date-resolved readings keyed by ISO date.
- `index.js`: CommonJS exports for stable resolved paths, package metadata, and date classification.
- `meta.json`: package provenance, schema version, counts, shipped years, structural daily materialization summary, and schema notes. In `daily_files`, `rows` is retained as the legacy date-count field; use `date_count` and `reading_count` for explicit counts.

## Usage

```js
const lectionaryData = require('@andraws/lectionary-data');

console.log(lectionaryData.occasionIndexPath);
console.log(lectionaryData.dailyYearPath(2026));
console.log(lectionaryData.shippedYears);
console.log(lectionaryData.meta.source_repo_commit);
console.log(lectionaryData.classifyDate('2026-04-10'));
console.log(lectionaryData.isActiveReading({ display_ref: 'Jn 1:1-17' }));
```

## Exports

- `occasionIndexPath`: absolute path to `data/reverse_lectionary_index.jsonl`.
- `dailyDir`: absolute path to `data/daily`.
- `dailyYearPath(year)`: returns the absolute path for a shipped daily lectionary JSON file.
- `classifyDate(date)`: classifies a shipped ISO date as present in daily JSON or as a documented structural-only Holy Week/Bright Saturday gap.
- `isRemovedReading(row)`: returns true for rows marked `active: false` or `status: "removed"`.
- `isActiveReading(row)`: convenience negation of `isRemovedReading(row)`; use this to filter active reverse-index rows.
- `structuralDateResolver`: resolver metadata copied from `meta.structural_date_resolver`.
- `shippedYears`: frozen array of shipped daily years.
- `meta`: parsed `meta.json`.

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

Consumers should filter with `isActiveReading(row)` unless they are building an audit/provenance view.

### Dual-numbering display references

`display_ref` is the human-facing reference. Psalm references use Masoretic Text numbering as the primary display form with Septuagint numbering inline when available. Consumers that need machine normalization should use `canonical_mt_ref`, `canonical_lxx_ref`, and `spans_json` instead of parsing `display_ref`.

### Removed markers

`removed_marker` carries source-derived removal or omission markers where they exist. Consumers should preserve this value and should not treat marked readings as active without checking the field.

## Daily file schema

Each daily file is a JSON object keyed by ISO date, for example `2026-04-12`. Each value is an array of readings for that date.

Shipped years: 2026, 2027, 2028.

Each daily reading includes a unique `reading_order` within that date. The package writes daily arrays sorted by `reading_order`, using deterministic service and slot ordering: Vespers, Matins, then Liturgy; within those services, Psalm/Gospel for Vespers and Matins, and Pauline, Catholic, Acts, Psalm, Gospel for Liturgy. `slot_order` may repeat for split Psalm verses or readings that share one liturgical slot; use `reading_order` when a unique date-local order is required.

In `meta.daily_files`, `rows` is retained as a legacy alias for `date_count`. Use `date_count` for the number of ISO date keys and `reading_count` for the total number of readings across those dates.

## Structural Holy Week / Bright Saturday daily rows

The package date-resolves Holy Week and Bright Saturday structural rows into the shipped daily files when the public copticchurch.net daily cache does not provide rows for that civil date. As a result, every shipped civil date in 2026, 2027, 2028 has a daily JSON key.

`meta.structural_date_resolver.structural_daily_additions_by_year` lists the civil dates filled from structural Pascha/Bright Saturday rows. `classifyDate(date)` returns `hasDailyReadings: true` for every shipped civil date that has a daily key.

## Source-priority projection

The package projects the raw reverse index into a consumer-safe runtime index. When a copticchurch.net date-resolved row and a lower-priority local cycle row overlap the same normalized consumer occasion, service, service hour, and slot type but disagree on the passage span, the lower-priority variant is retained as inactive provenance rather than used as an active lookup row.

Inactive projection rows are marked with `active: false`, `status: "removed"`, `removed_marker: "removed_by_source_priority_projection"`, a `consumer_note`, and preferred-reading fields such as `preferred_source_family`, `preferred_display_ref`, and `preferred_identity_key`. Use `isActiveReading(row)` to exclude these rows from active lookups.

For fixed-date rows with a Sunday-specific counterpart, generic rows are disambiguated as non-Sunday contexts rather than silently duplicated.

Projection counts and examples are recorded in `meta.projection_rules`.

## Span and Psalm numbering contract

`spans_json` contains machine-readable canonical spans when the reading can be represented as biblical book/chapter/verse ranges. It may be an empty array for named non-standard readings supplied by Coptic Reader fixtures, such as `Memoirs of Job`; in that case use `reading_type`, `reading_name`, and `display_ref`.

Psalm `display_ref` values may include inline dual numbering, for example `Ps 105:14-15 (LXX Ps 104:14-15)`. Consumers should not parse `display_ref` for machine matching. Use `canonical_mt_ref`, `canonical_lxx_ref`, and `spans_json`.

## Known limitation

Structural-only occasions outside the shipped civil-year daily scope, such as some special services, remain available through `reverse_lectionary_index.jsonl`. Holy Week and Bright Saturday rows for shipped civil dates are included in daily files.

## Provenance

- Package version: 1.1.8
- Source repo commit: bd10e4371e510c6c794cdd14851f8a0bb6e5f312
- Generated at: 2026-06-26T01:00:39.965Z
- Occasion index rows: 11905

## License

This package is licensed under CC-BY-4.0.

Required attribution:
Coptic lectionary data from Light and Logos (andraws.net), licensed under CC BY 4.0.

License deed: https://creativecommons.org/licenses/by/4.0/

Scope: The lectionary readings and their liturgical assignments are the tradition of the Coptic Orthodox Church. This license applies to the compilation, structure, encoding, identity keys, and editorial curation in this dataset, not to the underlying tradition.
