# @andraws/lectionary-data

Coptic Orthodox reverse-lectionary occasion index and date-resolved daily readings packaged for npm consumers.

## What this package contains

- `data/reverse_lectionary_index.jsonl`: one JSON object per line for reverse lookup by lectionary occasion and reading identity.
- `data/daily/lectionary-2026.json`, `lectionary-2027.json`, and `lectionary-2028.json`: date-resolved readings keyed by ISO date.
- `index.js`: CommonJS exports for stable resolved paths and package metadata.
- `meta.json`: package provenance, counts, shipped years, and schema notes.

## Usage

```js
const lectionaryData = require('@andraws/lectionary-data');

console.log(lectionaryData.occasionIndexPath);
console.log(lectionaryData.dailyYearPath(2026));
console.log(lectionaryData.shippedYears);
console.log(lectionaryData.meta.source_repo_commit);
```

## Exports

- `occasionIndexPath`: absolute path to `data/reverse_lectionary_index.jsonl`.
- `dailyDir`: absolute path to `data/daily`.
- `dailyYearPath(year)`: returns the absolute path for a shipped daily lectionary JSON file.
- `shippedYears`: frozen array of shipped daily years.
- `meta`: parsed `meta.json`.

## Occasion index schema

Each line in `data/reverse_lectionary_index.jsonl` is a JSON object. The published field set is:

- `occasion`
- `service_section`
- `service_hour`
- `slot`
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

### Dual-numbering display references

`display_ref` is the human-facing reference. Psalm references use Masoretic Text numbering as the primary display form with Septuagint numbering inline when available. Consumers that need machine normalization should use `canonical_mt_ref`, `canonical_lxx_ref`, and `spans_json` instead of parsing `display_ref`.

### Removed markers

`removed_marker` carries source-derived removal or omission markers where they exist. Consumers should preserve this value and should not treat marked readings as active without checking the field.

## Daily file schema

Each daily file is a JSON object keyed by ISO date, for example `2026-04-12`. Each value is an array of readings for that date.

Shipped years: 2026, 2027, 2028.

## Known limitation

Structural-only occasions without a `gregorian_date` are not present in the daily files yet. This includes Bright Saturday and special services.

## Provenance

- Package version: 1.0.0
- Source repo commit: d256c7affd1db09c7b77364911de64fc79d314a5
- Generated at: 2026-06-18T01:31:44.710Z
- Occasion index rows: 8005

## License

This package is licensed under CC-BY-4.0.

Required attribution:
Coptic lectionary data from Light and Logos (andraws.net), licensed under CC BY 4.0.

License deed: https://creativecommons.org/licenses/by/4.0/

Scope: The lectionary readings and their liturgical assignments are the tradition of the Coptic Orthodox Church. This license applies to the compilation, structure, encoding, identity keys, and editorial curation in this dataset, not to the underlying tradition.
