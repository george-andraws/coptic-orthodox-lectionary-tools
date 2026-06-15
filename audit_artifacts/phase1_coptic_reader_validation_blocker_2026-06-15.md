# Phase 1 Coptic Reader Validation Report — Blocked at Source-Access Check

- Date: 2026-06-15
- Repo: `/Users/georgeandraws/workspace/coptic-lectionary-research`
- HEAD: `f7692cc` (`Restore Wednesday fuller-edition Pascha readings`)
- Remote: `https://github.com/george-andraws/coptic-orthodox-lectionary-tools.git`

## Executive summary

Phase 1 is blocked before duplicate reproduction and before Wednesday-of-Pascha comparison.

Reason: I could not find any repo-backed Coptic Reader ingestion/access mechanism in the live files or in git history. The repo documents and implements these sources instead:

- `sources/katameros-api/Core/KatamerosDatabase.db` SQLite for annual/Sunday/Great Lent/Pentecost cycle readings.
- `https://copticchurch.net/readings?...` cache/scrape for date-resolved readings.
- Downloaded/extracted Katameros/Pascha text files, especially St. Mary Ottawa Holy Pascha text, for Pascha source text and cross-checking.
- Curated Python rows for special services and Agpeya.

Because the task explicitly says **do not improvise a new extraction if the original Coptic Reader access is not reproducible**, I stopped here. A fresh Coptic Reader read now requires George approval of the extraction method first.

No dataset files were modified.

## 1. Repo inventory

### Repository state

- Repo root: `/Users/georgeandraws/workspace/coptic-lectionary-research`
- Branch: `main`
- Remote: `origin https://github.com/george-andraws/coptic-orthodox-lectionary-tools.git`
- HEAD: `f7692cc`

### Ingestion/build scripts found

| Purpose | Path | Notes |
|---|---:|---|
| Main build/orchestrator | `/Users/georgeandraws/workspace/coptic-lectionary-research/build_lectionary_reference.py` | Exports SQLite cycle tables, scrapes/caches copticchurch.net date pages, copies Pascha/Bright inputs, runs downstream builders and verifier. |
| Reverse lookup crosswalk builder | `/Users/georgeandraws/workspace/coptic-lectionary-research/build_lectionary_crosswalk.py` | Combines cycle/date/special/Agpeya/Pascha/Bright Saturday indexes into reverse lookup crosswalk. |
| Chapter index builder | `/Users/georgeandraws/workspace/coptic-lectionary-research/build_bible_chapter_lectionary_index.py` | Builds chapter-level index and detailed occurrence CSV from crosswalk. |
| Pascha source text builder | `/Users/georgeandraws/workspace/coptic-lectionary-research/build_pascha_source_text_index.py` | Builds `pascha_source_text_index.*` from extracted Holy Pascha text. |
| Special service builder | `/Users/georgeandraws/workspace/coptic-lectionary-research/build_special_service_reference.py` | Curated `ROWS` generate special-service readings/indexes. |
| Agpeya builder | `/Users/georgeandraws/workspace/coptic-lectionary-research/build_agpeya_reference.py` | Curated rows generate Agpeya readings/indexes. |

### Large/source CSVs

There is no single CSV at exactly ~16 MiB. Closest and relevant large CSVs:

| CSV | Size | Rows | Role |
|---|---:|---:|---|
| `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/bible_chapter_lectionary_occurrences.csv` | 19,201,064 bytes / 18.31 MiB | 71,128 | Detailed generated chapter occurrence table. This is the closest match to the “~16MB source CSV” description. |
| `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/reverse_lookup_crosswalk.csv` | 27,505,750 bytes / 26.23 MiB | 66,367 | Reverse passage crosswalk. |
| `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/copticchurch_passage_index_2020_2035.csv` | 11,278,628 bytes / 10.76 MiB | 59,324 | Date-resolved passage index from copticchurch.net scrape/cache. |
| `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/copticchurch_date_readings_2020_2035.csv` | 9,740,879 bytes / 9.29 MiB | 50,382 | Date-resolved raw reading rows from copticchurch.net scrape/cache. |

Other Pascha-specific CSVs:

| CSV | Size | Rows | Role |
|---|---:|---:|---|
| `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/pascha_day_hour_index.csv` | 11,318 bytes | 172 | Curated Holy Pascha day/hour/slot readings. |
| `/Users/georgeandraws/workspace/coptic-lectionary-research/out2/pascha_day_hour_index.csv` | 11,318 bytes | not recounted here | Legacy/durable upstream fallback for Pascha day/hour rows. |
| `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/pascha_source_text_index.csv` | 58,858 bytes | 277 | Extracted Holy Pascha source text index. |

### Reverse-lookup crosswalk

- Primary current path: `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/reverse_lookup_crosswalk.csv`
  - Size: 27,505,750 bytes / 26.23 MiB
  - Rows: 66,367
- Builder side output also exists: `/Users/georgeandraws/workspace/coptic-lectionary-research/out4/reverse_lookup_crosswalk.csv`
  - Size: 27,505,750 bytes / 26.23 MiB

### SQLite DB

- Source DB: `/Users/georgeandraws/workspace/coptic-lectionary-research/sources/katameros-api/Core/KatamerosDatabase.db`
  - Size: 91,217,920 bytes / 86.99 MiB
  - `pragma integrity_check`: `ok`
  - Tables: 27
- Packaged provenance copy: `/Users/georgeandraws/workspace/coptic-lectionary-research/out/sources/KatamerosDatabase.sqlite`
  - Size: 91,217,920 bytes / 86.99 MiB
  - `pragma integrity_check`: `ok`
  - Tables: 27

### Python query script

- Tracked source: `/Users/georgeandraws/workspace/coptic-lectionary-research/query_lectionary.py`
- Packaged copy: `/Users/georgeandraws/workspace/coptic-lectionary-research/out/scripts/query_lectionary.py`

### Existing tests / verification

- Conventional tests: none found.
  - No `tests/` directory found.
  - No `test*.py`, `*_test.py`, `pytest.ini`, or `pyproject.toml` found.
- Existing verifier: `/Users/georgeandraws/workspace/coptic-lectionary-research/verify_lectionary_queries.py`
  - This is not a conventional test suite, but it asserts required artifacts, known-good lookups, parser edge cases, Pascha dedupe invariants, and Wednesday Pascha correction expectations.

## 2. Original Coptic Reader access mechanism

### What the repo actually documents/implements

Evidence from `build_lectionary_reference.py`:

- Lines 4-7 document sources as:
  - `pierresaid/katameros-api` SQLite database
  - `copticchurch.net` daily readings pages
  - downloaded Katameros PDFs and extracted text for Pascha/Holy Week cross-checking
- Lines 39-47 define local repo paths, SQLite DB, output dirs, and Obsidian package target.
- Lines 74-83 connect to the local SQLite DB.
- Lines 165-216 parse/fetch `copticchurch.net` reading pages.
- Lines 278-289 copy source DB/PDF/TXT files to packaged sources.
- Lines 295-311 copy required Pascha/Bright Saturday artifacts from `out/data`, falling back to `out2`/`out_bright`.
- Lines 326-329 run the Pascha source-text builder.
- Lines 373-417 run the full build and publish verified package artifacts.

Evidence from `RUNBOOK.md`:

- Lines 20-29 list data families as Katameros SQLite, copticchurch.net cache/scrape, Pascha day/hour, Bright Saturday, special-service readings, Agpeya, and reverse crosswalk.
- Lines 231-240 describe build inputs and reproducibility, including required Pascha/Bright Saturday artifacts and side-output fallback directories.

### Coptic Reader search results

Searches performed:

- Live repo content search for:
  - `Coptic Reader`
  - `CopticReader`
  - `copticreader`
  - `reader.coptic`
  - `main.dart.js`
  - `documentPath`
  - `AssetManifest`
  - `flutter`
- Markdown-only repo search for the same terms.
- Git-history search across all commits for exact Coptic Reader/bundle route terms, excluding bulky Bible-text cache/source folders.

Result: no Coptic Reader ingestion/access code or notes found in repo files or git history.

### Blocking conclusion

The original Coptic Reader access mechanism is not reproducible from this repo because I could not find one. The current repo-backed mechanism is **not Coptic Reader**; it is Katameros SQLite + copticchurch.net + extracted/curated Pascha/special-service sources.

Per instruction, I did not improvise a new Coptic Reader extraction method.

## 3. Duplicate reproduction

Not executed.

Reason: Phase 1 was stopped at Step 2 because the Coptic Reader access path is not repo-reproducible. Duplicate analysis can be run against local CSV/SQLite without Coptic Reader, but proceeding after the explicit Step 2 stop would violate the requested workflow.

## 4. Wednesday of Pascha comparison against Coptic Reader

Not executed.

Reason: a fresh Coptic Reader read would require selecting a new extraction/access method that is not documented in the repo. That needs George approval first.

Existing local files that would be inspected after approval:

- Stored day/hour data: `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/pascha_day_hour_index.csv`
- Durable fallback/upstream copy: `/Users/georgeandraws/workspace/coptic-lectionary-research/out2/pascha_day_hour_index.csv`
- Extracted source text index: `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/pascha_source_text_index.csv`
- Reverse crosswalk: `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/reverse_lookup_crosswalk.csv`

## 5. Holy Week schema check

Not executed for the same stop reason.

Known from inventory only: the Pascha-specific stored schema is **not** the ordinary Liturgy slot schema. `out/data/pascha_day_hour_index.csv` uses:

```text
day,hour,source,order,slot,refs
```

That indicates Holy Week is modeled by day/hour plus a Pascha slot, not only by ordinary Liturgy slots like Pauline/Catholicon/Praxis/Psalm/Gospel. A full schema impact check across all Pascha-week days remains pending after Coptic Reader source-access approval.

## 6. Required approval before continuing

To continue Phase 1, George needs to approve the Coptic Reader access method. Options to choose from:

1. Recover/inspect a Coptic Reader bundled app data route if available.
2. Use browser automation against the Coptic Reader app/site.
3. Use a manual/exported Coptic Reader source if George can provide one.
4. Use another explicitly approved source only as a secondary comparator, not as “Coptic Reader.”

Until then, this report is the stopping point.
