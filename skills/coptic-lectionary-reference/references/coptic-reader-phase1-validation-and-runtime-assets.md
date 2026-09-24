# Coptic Reader Phase 1 Validation and Runtime Asset Surface

Use this reference when the requester asks to validate the lectionary dataset against Coptic Reader, especially after duplicate reverse-lookup results or Pascha/Holy Week mismatches.

## Core workflow rule

Do Phase 1 as a **report-only audit** unless the requester explicitly approves dataset changes. Do not edit CSV, SQLite, builders, query scripts, or generated data during Phase 1.

When the user says Coptic Reader was used as a resource, do not re-run a naive page scrape. `https://copticreader.org/app/` is a Flutter web app that renders client-side to canvas; plain page fetches and DOM scraping are not a reliable reading source.

## Required discovery sequence

1. Inventory the repo and exact artifact paths:
   - ingestion/build scripts
   - large source/derived CSVs
   - reverse lookup crosswalk
   - SQLite DB
   - query helper
   - verifier/tests
2. Search prior session footprints before concluding Coptic Reader was not used:
   - Codex logs, typically `~/.codex`
   - Hermes sessions, typically `~/.hermes/sessions`
   - Search terms: `copticreader`, `Coptic Reader`, `copticreader.org`, `main.dart.js`, `generated_assets`, `documentPath`, `AssetManifest`.
3. Search live repo and full git history for the same terms, including commit messages and `git log --all -S <term>`.
4. Inspect Coptic Reader app runtime/network only for endpoint and response shape. Do not build a comparator/extraction pipeline unless the maintainer approves.
5. Reproduce duplicate symptoms locally by layer: source/stored data, passage index/crosswalk, then rendered query output.
6. Compare Pascha/Holy Week rows against controlled source text if Coptic Reader comparator is not yet approved, but label it as St. Mary/source-text comparison, not Coptic Reader ground truth.
7. Write/update a markdown discrepancy report and commit only the report.

## Coptic Reader runtime asset findings

The app has a real static runtime asset surface, but not a simple plaintext day-readings API.

Useful URLs:

- `https://copticreader.org/app/` — Flutter shell; not useful as DOM text.
- `https://copticreader.org/app/manifest.json` — PWA manifest.
- `https://copticreader.org/app/version.json` — app version metadata.
- `https://copticreader.org/app/flutter_service_worker.js` — small service worker.
- `https://copticreader.org/app/flutter_bootstrap.js` — Flutter bootstrap JS.
- `https://copticreader.org/app/main.dart.js` — minified bundle; useful route map. Search it for service-family names and metadata strings such as `documentPath`, `documentTitle`, `menuHierarchyIds`, and `historyDocumentPaths`.
- `https://copticreader.org/app/assets/generated_assets/manifest.json` — generated asset manifest.
- `https://copticreader.org/app/assets/generated_assets/search/manifest_runtime.json` — encrypted runtime search catalog manifest.
- `https://copticreader.org/app/assets/generated_assets/search/manifest_static.json` — encrypted static search catalog manifest.

`generated_assets/manifest.json` shape:

```json
{
  "assets": [
    {
      "logical_id": "About the Season",
      "asset_class": "encrypted_document",
      "source_path": "CopticReader/unencrypted_assets/documents/About the Season.xml",
      "generated_asset_key": "generated_assets/encrypted_documents/About%20the%20Season.bin",
      "content_type": "application/xml",
      "sha256": "...",
      "encrypted": true
    }
  ]
}
```

Observed live counts on 2026-06-15:

| Asset class | Count |
|---|---:|
| `encrypted_document` | 5,729 |
| `encrypted_image` | 57 |
| `html_asset` | 12 |
| `encrypted_search_index` | 235 |
| Total | 6,033 |

Do not describe this as “no Coptic Reader access possible.” The accurate statement is: there is a static encrypted asset surface that may support a comparator, but using it requires the maintainer approval because it is a different extraction route than a committed repo artifact or simple public JSON endpoint.

## Duplicate-layer diagnostic pattern

Check duplicates by increasingly derived layers:

1. Source/stored reading rows, keyed by day/service/slot/reading.
2. Passage index and crosswalk expansion, especially repeated verse lists like `19.68:17,16,17` that can emit the same segment twice.
3. Query/render output, remembering the query helper may suppress exact duplicate printed lines.

Example durable findings from 2026-06-15:

- Katameros SQLite `GreatLentReadings`, `Week=7`, `DayOfWeek=4`, rows `Id=46` and `Id=53` produced real stored duplicates for most slots.
- Hatur 8 raw Psalm `19.68:17,16,17` produced duplicate `Ps 68:17` through passage-index/crosswalk segmentation.
- The query helper’s exact-line dedupe can hide underlying data/crosswalk duplication, so report the layer explicitly instead of calling it render-only.

## Wednesday Pascha / source-text audit pitfalls

When comparing Wednesday Pascha against St. Mary Ottawa Holy Pascha source text:

- Do not rely solely on `pascha_source_text_index.csv`; inspect raw extracted text when the PDF headers look wrong.
- The raw St. Mary text can have bad page headers. On Wednesday, pages around the Sixth/Ninth Hour showed `The Ninth Hour of Wednesday` while the Doxology/Exposition text identified the material as Sixth Hour.
- Classify parser/index defects separately from stored-data defects.
- Known mismatch classes from the audit:
  - Wednesday Eve rows were mostly stale/wrong except Eleventh Hour matched at reference level.
  - Wednesday First Hour stored Wisdom readings where raw source had Sirach 1:16-2:15; source index missed it because the text says `Sircah`.
  - Wednesday Third Hour omitted Job 27:16-28:2 and truncated Proverbs.
  - Wednesday Sixth Hour missed Isaiah 48:1-6 and carried a Job reading from Third Hour.
  - Wednesday Ninth Hour had boundary mismatches for Proverbs and Psalm.
  - Wednesday Eleventh Hour matched at reference level.

## Schema/blast-radius rule

Do not reduce Holy Week schema diagnosis to “normal Liturgy slots vs not.” In the maintainer’s dataset, Pascha uses a day/hour schema with slots like `OT1`, `OT2`, and collapsed `Psalm+Gospel`, while some days still use `Pauline`, `Catholic`, `Acts`, `Psalm`, or `Gospel`.

Likely root cause for Pascha mismatch work is a lossy/legacy curated Pascha table plus a fragile source-text parser, not simply forcing Holy Week into ordinary Liturgy slots.

Before Phase 2, ask the requester to choose scope:

1. Fix only approved duplicate and Wednesday rows.
2. Broaden to a full Pascha source-text rebuild/audit because the mismatch blast radius is wider than Wednesday.
3. Approve or reject the Coptic Reader encrypted static-asset comparator route.

## Report-only commit standard

For Phase 1:

- Write a markdown discrepancy report under repo audit artifacts.
- Verify `git diff --name-only` includes only the report.
- Run `git diff --check`.
- Commit one report-only commit.
- Stop and wait for the maintainer’s approval before Phase 2.
