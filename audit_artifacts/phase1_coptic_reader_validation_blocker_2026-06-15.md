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

---

# Phase 1 Addendum — Coptic Reader Footprint Recovered, Local Validation Continued

- Date: 2026-06-15
- Scope: report-only continuation after George clarified that Coptic Reader had been used as a resource and that `https://copticreader.org/app/` is a Flutter canvas app.
- Dataset mutation: **none**. No CSV, SQLite, Python script, or generated data file was edited.
- Comparator rule followed: Coptic Reader was inspected only for access-path discovery. No comparator pipeline was built.

## A. Reconstructing how Coptic Reader was accessed

### A1. Previous-session transcript/log search

Search locations and counts:

| Location | Files scanned | Hit files | Matching lines |
|---|---:|---:|---:|
| `/Users/georgeandraws/.codex` | 7,994 | 0 | 0 |
| `/Users/georgeandraws/.hermes/sessions` | 1,403 | 89 | 2,213 |

The meaningful hits are in Hermes session transcripts, mostly from 2026-05-19. Many later hits are context-compaction repeats of the same Coptic Reader bundle work.

Representative transcript files:

- `/Users/georgeandraws/.hermes/sessions/session_20260519_193138_030502.json`
- `/Users/georgeandraws/.hermes/sessions/session_20260519_181113_b132a3.json`
- `/Users/georgeandraws/.hermes/sessions/session_20260519_173747_ca6fdf.json`
- `/Users/georgeandraws/.hermes/sessions/session_20260519_171231_4acf66.json`
- `/Users/georgeandraws/.hermes/sessions/session_20260519_185122_f10df6.json`

#### Verbatim transcript evidence: initial direct fetch failed, browser fetch succeeded

From Hermes state DB message `30192`, session `20260519_150403_05c7e9`:

```python
python3 - <<'PY'
import urllib.request
for path in ['https://copticreader.org/app/flutter_bootstrap.js','https://copticreader.org/app/','https://copticreader.org/app/main.dart.js','https://copticreader.org/app/assets/AssetManifest.json','https://copticreader.org/app/assets/FontManifest.json']:
    try:
        data=urllib.request.urlopen(path, timeout=20).read(2000)
        print('\nURL', path, 'OK', len(data), data[:200].decode('utf-8','ignore').replace('\n',' '))
    except Exception as e:
        print('\nURL', path, 'ERR', repr(e))
PY
```

From message `30193`:

```text
URL https://copticreader.org/app/flutter_bootstrap.js ERR <HTTPError 403: 'Forbidden'>

URL https://copticreader.org/app/ ERR <HTTPError 403: 'Forbidden'>

URL https://copticreader.org/app/main.dart.js ERR <HTTPError 403: 'Forbidden'>

URL https://copticreader.org/app/assets/AssetManifest.json ERR <HTTPError 403: 'Forbidden'>

URL https://copticreader.org/app/assets/FontManifest.json ERR <HTTPError 403: 'Forbidden'>
```

From message `30203`:

```text
The shell is a Flutter app with no direct DOM links, so the remaining path is to inspect `main.dart.js` and possibly the service worker for embedded endpoints or data file names. That should tell us how to pull content without the UI.
```

Tool calls in that same message:

```json
{"url": "https://copticreader.org/app/main.dart.js"}
{"url": "https://copticreader.org/app/flutter_service_worker.js?v=3.6"}
{"url": "https://copticreader.org/app/assets/AssetManifest.json"}
```

#### Verbatim transcript evidence: static app probe

From message `31085`, session `20260519_171231_4acf66`:

```python
python3 - <<'PY'
import requests,re,sys
from urllib.parse import urljoin
base='https://copticreader.org/app/'
html=requests.get(base,headers={'User-Agent':'Mozilla/5.0'},timeout=30).text
print('HTML len',len(html))
for pat in [r'src="([^"]+)"',r'href="([^"]+)"']:
    hits=re.findall(pat,html,re.I)
    print('hits',len(hits))
    for h in hits[:20]:
        print(h)
    print('---')
# print script/style refs and service worker refs
for m in re.finditer(r'(?:src|href)="([^"]+)"',html):
    u=m.group(1)
    if any(x in u for x in ['main.dart.js','flutter','manifest','service_worker','assets','json']):
        print('REF',u)
PY
```

Second probe from the same message:

```python
python3 - <<'PY'
import requests,re
cands=[
'https://copticreader.org/app/manifest.json',
'https://copticreader.org/app/flutter_service_worker.js',
'https://copticreader.org/app/assets/AssetManifest.json',
'https://copticreader.org/app/assets/FontManifest.json',
'https://copticreader.org/app/main.dart.js',
'https://copticreader.org/app/version.json',
'https://copticreader.org/app/index.html',
'https://copticreader.org/app/manifest.webmanifest'
]
for u in cands:
    try:
        r=requests.get(u,headers={'User-Agent':'Mozilla/5.0'},timeout=30)
        print('\n###',u,r.status_code,r.headers.get('content-type'),len(r.text))
        print(r.text[:500].replace('\n',' ') if 'text' in r.headers.get('content-type','') or 'json' in r.headers.get('content-type','') else r.content[:30])
    except Exception as e:
        print('\n###',u,'ERR',e)
PY
```

From message `31087`:

```text
### https://copticreader.org/app/manifest.json 200 application/json 922
{     "name": "Coptic Reader",     "short_name": "Coptic Reader",     "start_url": ".",     "display": "standalone", ...

### https://copticreader.org/app/flutter_service_worker.js 200 text/javascript 815
'use strict';

 self.addEventListener('install', () => { ...

### https://copticreader.org/app/assets/AssetManifest.json 200 text/html 5176
<!DOCTYPE html>
 <html>
 <head> ...

### https://copticreader.org/app/assets/FontManifest.json 200 application/json 655
[{"family":"MaterialIcons","fonts":[{"asset":"fonts/MaterialIcons-Regular.otf"}]},{"family":"CREnglishMenu","fonts":[{"asset":"generated_assets/html_assets/fonts/Georgia.ttf"}]}, ...

### https://copticreader.org/app/main.dart.js 200 text/javascript 3957446
(function dartProgram(){function copyProperties(a,b){var s=Object.keys(a) ...

### https://copticreader.org/app/version.json 200 application/json 104
{"app_name":"coptic_reader_app","version":"3.6","build_number":"381","package_name":"coptic_reader_app"}
```

#### Verbatim transcript evidence: bundle route-map mining

From message `31089`:

```javascript
fetch('/app/main.dart.js').then(r=>r.text()).then(t=>({len:t.length, hasBaptism:t.includes('Baptism'), hasUnction:t.includes('Unction'), hasCrowning:t.includes('Crowning'), hasFuneral:t.includes('Funeral'), hasHouse:t.includes('House'), hasMyron:t.includes('Myron'), hasCornerstone:t.includes('Cornerstone'), hasWaters:t.includes('Waters'), snippets:[...t.matchAll(/(?:Baptism|Unction|Crowning|Funeral|House Blessing|Myron|Cornerstone|Liturgy of the Waters|First Prostration|Second Prostration|Church Consecration Special Prayer)/g)].slice(0,40).map(m=>m[0])})).catch(e=>({error:String(e)}))
```

From message `31129`:

```python
python - <<'PY'
import re,sys,subprocess,os,json
from urllib.request import urlopen
url='https://copticreader.org/app/main.dart.js'
text=urlopen(url, timeout=30).read().decode('utf-8','ignore')
print('len', len(text))
# Find service-family blocks around keywords
keywords=['Unction','Baptism','Crowning','FuneralPrayer','AltarConsecration','Cornerstone','MyronConsecration','HomeBlessing','FirstProstration','SecondProstration','LiturgyOfTheWaters','ChurchConsecrationSpecialPrayer','PaschaWeek']
for kw in keywords:
    m=re.search(kw, text)
    if m:
        s=max(0,m.start()-500)
        e=min(len(text),m.end()+1200)
        snippet=text[s:e]
        print('\n###',kw,'at',m.start())
        print(snippet[:1700])
        print('\n---ENDSNIP---')
PY
```

From message `31610`, the local note that was written after that session said:

```text
- Creative scraping route discovered: the Flutter app shell exposes `manifest.json`, `flutter_bootstrap.js`, `flutter_service_worker.js`, and `main.dart.js` directly under `/app/`.
- Bundle inspection of `main.dart.js` surfaced the service-family selector `b5u()` / similar logic with document names:
  - `Unction`
  - `Baptism`
  - `Crowning`
  - `FuneralPrayer`
  - `AltarConsecration`
  - `Cornerstone`
  - `MyronConsecration`
  - `HomeBlessing`
  - `FirstProstration`
  - `SecondProstration`
  - `LiturgyOfTheWaters`
  - `ChurchConsecrationSpecialPrayer`
- The same bundle also exposes feast/service gating strings for major feast families and Pascha-related documents, which makes the JS bundle a useful route map even when the Flutter DOM is not readable.
- Practical use: fetch `/app/main.dart.js` and search for service family names to discover internal document selectors before trying browser automation.
- Confirmed the app contains major service families beyond the ordinary Katameros: Baptism, Crowning, Unction, Funeral Prayer, Altar Consecration, Cornerstone, Myron Consecration, Home Blessing, First/Second Prostration, Liturgy of the Waters, Church Consecration Special Prayer, and Pascha Week.
- Confirmed the app has day/feast evaluators for Theophany, Wedding Cana, Circumcision, Presentation in Temple, Transfiguration, Entrance of the Lord Christ, Resurrection, Ascension, Pentecost, Thomas Sunday, Covenant Thursday, Great Friday, and Pascha Week.
- Bundle metadata that matters for route discovery:
  - `documentPath`
  - `documentTitle`
  - `menuHierarchyIds`
  - `historyDocumentPaths`
- The bundle is readable via browser-context fetch even when direct curl requests are blocked, so it is a stable discovery source for future scraping.
- Additional static-app finding: `AssetManifest.json` and `AssetManifest.bin.json` currently fall through to the app shell rather than exposing a clean asset index, so `main.dart.js` remains the more reliable discovery surface.
```

### A2. Repo, git history, cached artifacts, and curated rows

Repo/git footprint from this pass:

| Search area | Result |
|---|---|
| Live repo content for `copticreader`, `Coptic Reader`, `copticreader.org`, `main.dart.js`, `generated_assets`, `documentPath`, `AssetManifest` | 1 hit file only: this report itself (`audit_artifacts/phase1_coptic_reader_validation_blocker_2026-06-15.md`) |
| Git commit messages for the same terms | Only commit `7691f98 Document Phase 1 Coptic Reader validation blocker` |
| `git log --all -S <term>` for the same terms | Only the blocker report commit for `copticreader`, `main.dart.js`, `documentPath`, `AssetManifest`, and `Coptic Reader`; no earlier ingestion code |
| Cached/network artifacts in repo | 5,977 HTML/JSON/artifact candidates, but none named or matching `copticreader`, `main.dart`, `AssetManifest`, or `generated_assets` |
| Curated special-service / Agpeya rows | No Coptic Reader comments or source URLs. Rows cite Saint Bishoy PDFs / service-books and St. Mary Ottawa Holy Pascha text. |

Curated-row provenance examples found:

- `build_special_service_reference.py` cites Saint Bishoy PDFs such as `Rites_Wedding_Ceremony.pdf`, `Rites_Baptism.pdf`, service-books page, etc.
- `build_agpeya_reference.py` cites `https://www.saintbishoy.ca/wp-content/uploads/Rites_Agpeya_Book.pdf`.
- `build_pascha_source_text_index.py` cites `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt`.

Working hypothesis status: **confirmed in repo**. Coptic Reader appears to have been used manually/as a browser-bundle route map in prior sessions, but the committed curated Python rows do not cite or derive from Coptic Reader in comments or source fields. The rows themselves are backed by in-repo PDFs/text and Saint Bishoy/St. Mary sources, not by a committed Coptic Reader extraction artifact.

## B. Coptic Reader runtime data surface: endpoints found, no comparator pipeline built

Important correction to the earlier blocker: there is a real runtime static-asset surface. It is not DOM scraping and not a plain REST reading API.

### B1. Shell/runtime URLs verified

| URL | Response / shape |
|---|---|
| `https://copticreader.org/app/` | Flutter web shell; canvas/app surface, not useful as DOM reading text |
| `https://copticreader.org/app/manifest.json` | PWA JSON, 922 chars, keys include `name`, `short_name`, `start_url`, `display`, icons |
| `https://copticreader.org/app/version.json` | `{"app_name":"coptic_reader_app","version":"3.6","build_number":"381","package_name":"coptic_reader_app"}` |
| `https://copticreader.org/app/flutter_service_worker.js` | Small service worker, unregister/reload behavior |
| `https://copticreader.org/app/flutter_bootstrap.js` | Flutter bootstrap JS |
| `https://copticreader.org/app/main.dart.js` | Minified JS bundle; prior run length 3,957,446 chars; exposes route/service strings and document metadata names |
| `https://copticreader.org/app/assets/FontManifest.json` | Font manifest; includes `generated_assets/html_assets/fonts/...` |
| `https://copticreader.org/app/AssetManifest.json` and `/app/AssetManifest.bin.json` | Fall through to HTML shell in direct fetch; app itself later fetched `/app/assets/AssetManifest.bin.json` |

### B2. Runtime resource list showed generated/encrypted assets

From live browser `performance.getEntriesByType('resource')`, the app fetched, among many others:

```text
https://copticreader.org/app/assets/generated_assets/manifest.json
https://copticreader.org/app/assets/tool/deploy/config.json
https://copticreader.org/app/assets/tool/deploy/PCBuildNumber.json
https://copticreader.org/app/assets/generated_assets/search/manifest_runtime.json
https://copticreader.org/app/assets/generated_assets/search/manifest_static.json
https://copticreader.org/app/assets/generated_assets/encrypted_documents/system%25252FBibleBooks.bin
https://copticreader.org/app/assets/generated_assets/encrypted_documents/system%25252FMenus.bin
https://copticreader.org/app/assets/generated_assets/encrypted_documents/system%25252FStringTable.bin
https://copticreader.org/app/assets/generated_assets/search/catalog_runtime.bin.gz.enc
https://copticreader.org/app/assets/generated_assets/search/catalog_static.bin.gz.enc
```

### B3. `generated_assets/manifest.json` response shape

Verified live endpoint:

```text
https://copticreader.org/app/assets/generated_assets/manifest.json
```

Shape:

```json
{
  "assets": [
    {
      "logical_id": "About the Season",
      "asset_class": "encrypted_document",
      "source_path": "CopticReader/unencrypted_assets/documents/About the Season.xml",
      "generated_asset_key": "generated_assets/encrypted_documents/About%20the%20Season.bin",
      "content_type": "application/xml",
      "sha256": "eae91d0e8110314964f2e9761f5c07ea45806db90c89f15010168c09cf05426b",
      "encrypted": true
    }
  ]
}
```

Live counts:

| Asset class | Count |
|---|---:|
| `encrypted_document` | 5,729 |
| `encrypted_image` | 57 |
| `html_asset` | 12 |
| `encrypted_search_index` | 235 |
| **Total** | **6,033** |

Representative logical IDs found in the manifest include:

- `baptism/Baptism - Holy Baptism`
- `baptism/Baptism - Holy Myron`
- `crowning/Crowning Prayer`
- `crowning/Liturgy of the Word (Weddings)`
- `unction/Unction - First Prayer`
- `unction/Unction - Fifth Prayer`

### B4. Search manifest response shapes

```json
// https://copticreader.org/app/assets/generated_assets/search/manifest_runtime.json
{
  "schemaVersion": 71,
  "appVersion": "3.6",
  "createdUtcIso8601": "2000-01-01T00:00:00.000Z",
  "resultCount": 376847,
  "dataStorageKey": "generated_assets/search/catalog_runtime.bin.gz.enc",
  "runtimeScopeKey": "symbolic_exact_dates_v1",
  "dataChunkCount": 185
}
```

```json
// https://copticreader.org/app/assets/generated_assets/search/manifest_static.json
{
  "schemaVersion": 71,
  "appVersion": "3.6",
  "createdUtcIso8601": "2000-01-01T00:00:00.000Z",
  "resultCount": 97822,
  "dataStorageKey": "generated_assets/search/catalog_static.bin.gz.enc",
  "runtimeScopeKey": "",
  "dataChunkCount": 48
}
```

### B5. Endpoint conclusion

I did **not** find a simple REST/JSON API that returns a day’s readings in plaintext.

I did find a reusable **static asset manifest** and encrypted generated document/search assets. That is a plausible Coptic Reader comparator route, but it requires a separate decision before use because it means decoding/reading Coptic Reader’s encrypted static assets, not just hitting a public JSON reading endpoint.

Phase 2 should not build on this until George approves this comparator route.

## C. Local checks that did not require Coptic Reader

## C1. Duplicate reproduction and layer location

### Reading-level source/stored files

| Layer/file | Duplicate groups | Excess duplicate rows | Affected days |
|---|---:|---:|---|
| `out/data/katameros_cycle_readings.csv` | 7 | 7 | `week 7 day_of_week 4` |
| SQLite `out/sources/KatamerosDatabase.sqlite`, table `GreatLentReadings` | 7 | 7 | `Week=7`, `DayOfWeek=4`, rows `Id=46` and `Id=53` |
| `out/data/copticchurch_date_readings_2020_2035.csv` | 0 | 0 | none |
| `out/data/pascha_day_hour_index.csv` | 0 | 0 | none |
| `out/data/pascha_source_text_index.csv` | 0 | 0 | none |
| `out/data/special_service_readings_curated.csv` | 0 | 0 | none |
| `out/data/agpeya_hour_readings.csv` | 0 | 0 | none |

SQLite/source duplicates, all in `GreatLentReadings`, rows `Id=46` and `Id=53`:

| Slot | Duplicate reading |
|---|---|
| `M_Gospel_Ref` / `matins_gospel` | `40.20:20-28` / `Matt 20:20-28` |
| `P_Gospel_Ref` / `liturgy_pauline` | `47.4:5-18` / `2Cor 4:5-18` |
| `C_Gospel_Ref` / `liturgy_catholic` | `62.3:13-24` / `1Jn 3:13-24` |
| `X_Gospel_Ref` / `liturgy_acts` | `44.25:23-27*@+44.26:1-6` / `Acts 25:23-27; Acts 26:1-6` |
| `L_Psalm_Ref` / `liturgy_psalm` | `19.122:1-2` / `Ps 122:1-2` |
| `L_Gospel_Ref` / `liturgy_gospel` | `41.12:18-27` / `Mark 12:18-27` |
| `Prophecy` / `prophecy` | `20.11:13-26@23.65:8-16@18.42:1-6@12.6:8-33*@+12.7:1-20` / `Prov 11:13-26; Isa 65:8-16; Job 42:1-6; 2Kgs 6:8-33; 2Kgs 7:1-20` |

Additional nuance: `M_Psalm_Ref` is not exactly identical in raw source rows:

- row `Id=46`: `19.63:1-1`
- row `Id=53`: `19.63:1-1*@+19.64:2-4`

But the crosswalk emits duplicate rendered `Ps 63:1` because both rows include that segment.

### Reverse lookup crosswalk

| Check | Result |
|---|---:|
| Exact whole-row duplicates in `out/data/reverse_lookup_crosswalk.csv` | 0 groups |
| Same source-row/display-passage duplicates | 0 groups |
| Duplicate lines as rendered by the query helper’s crosswalk display logic | 14 groups / 14 excess lines |

The 14 duplicate-render groups are:

- 13 groups from the duplicated Great Lent source rows (`week 7 day_of_week 4`, `katameros_cycle`, `GreatLentReadings`).
- 1 group from Annual Hatur 8 Psalm segmentation: raw `19.68:17,16,17` produces `Ps 68:17` twice in `katameros_cycle_passage_index.csv` and therefore twice in the crosswalk.

Examples from `reverse_lookup_crosswalk.csv`:

```text
week 7 day_of_week 4 | liturgy_catholic | GreatLentReadings | 1Jn 3:13-24 | source=katameros_cycle
week 7 day_of_week 4 | liturgy_pauline | GreatLentReadings | 2Cor 4:5-18 | source=katameros_cycle
week 7 day_of_week 4 | prophecy | GreatLentReadings | 2Kgs 6:8-33 | source=katameros_cycle
week 7 day_of_week 4 | prophecy | GreatLentReadings | 2Kgs 7:1-20 | source=katameros_cycle
week 7 day_of_week 4 | liturgy_acts | GreatLentReadings | Acts 25:23-27 | source=katameros_cycle
week 7 day_of_week 4 | liturgy_acts | GreatLentReadings | Acts 26:1-6 | source=katameros_cycle
week 7 day_of_week 4 | prophecy | GreatLentReadings | Isa 65:8-16 | source=katameros_cycle
week 7 day_of_week 4 | prophecy | GreatLentReadings | Job 42:1-6 | source=katameros_cycle
week 7 day_of_week 4 | liturgy_gospel | GreatLentReadings | Mark 12:18-27 | source=katameros_cycle
week 7 day_of_week 4 | matins_gospel | GreatLentReadings | Matt 20:20-28 | source=katameros_cycle
week 7 day_of_week 4 | prophecy | GreatLentReadings | Prov 11:13-26 | source=katameros_cycle
week 7 day_of_week 4 | liturgy_psalm | GreatLentReadings | Ps 122:1-2 | source=katameros_cycle
week 7 day_of_week 4 | matins_psalm | GreatLentReadings | Ps 63:1 | source=katameros_cycle
Hatur 8 | vespers_psalm | AnnualReadings | Ps 68:17 | source=katameros_cycle
```

Hatur 8 details:

```text
katameros_cycle_passage_index.csv row 847: raw_ref=19.68:17,16,17 normalized_segment=Ps 68:17
katameros_cycle_passage_index.csv row 849: raw_ref=19.68:17,16,17 normalized_segment=Ps 68:17
```

### Render/query layer

The current query helper has duplicate suppression:

- `print_unique()` suppresses exact duplicate printed lines.
- `print_section()` also suppresses exact duplicate section lines.

Commands run and observed exact duplicate-line counts:

| Command | Lines | Exact duplicate printed lines |
|---|---:|---:|
| `python3 scripts/query_lectionary.py --pascha-day "Wednesday" --limit 200` | 32 | 0 |
| `python3 scripts/query_lectionary.py --source-text "Wednesday" --limit 200` | 42 | 0 |
| `python3 scripts/query_lectionary.py --passage "Gen 6" --include-crosswalk --limit 200` | 2 | 0 |
| `python3 scripts/query_lectionary.py --passage "Matt 24" --include-crosswalk --limit 200` | 402 | 0 |
| `python3 scripts/query_lectionary.py --passage "Mark 12:18-27" --include-crosswalk --limit 200` | 62 | 0 |
| `python3 scripts/query_lectionary.py --cycle-passage "Mark 12:18-27" --limit 50` | 2 | 0 |

Layer conclusion:

- Duplicate root cause #1: **source/stored data** duplication in raw Katameros SQLite `GreatLentReadings` rows `46` and `53`, propagated to `katameros_cycle_readings.csv`, passage index, and crosswalk.
- Duplicate root cause #2: **crosswalk/passage-index segmentation** duplicates `Ps 68:17` from Hatur 8 raw ref `19.68:17,16,17`.
- Current rendered query output suppresses exact duplicate strings, so if the user sees duplicate-looking results today, the underlying issue is data/crosswalk duplication potential, not a pure print-loop bug.

## C2. Wednesday of Pascha vs St. Mary Ottawa Holy Pascha source text

Files compared:

- Stored day/hour data: `out/data/pascha_day_hour_index.csv`
- Parsed source-text index: `out/data/pascha_source_text_index.csv`
- Raw source text: `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt`

Important caveat: `pascha_source_text_index.csv` itself is imperfect. The raw St. Mary text has page-header defects around Wednesday Sixth/Ninth Hour: pages 308-312 say `The Ninth Hour of Wednesday`, but the Doxology and Exposition on those pages say **Sixth Hour**. So I used the raw extracted text lines to classify Wednesday, not only the parsed index.

### C2a. Wednesday Eve

Stored Wednesday Eve rows:

```text
Wednesday Eve | First Hour | OT1 | Jer 43:5-11
Wednesday Eve | First Hour | Psalm+Gospel | Ps 69:1,16; John 10:17-21
Wednesday Eve | Third Hour | OT1 | Amos 4:4-13
Wednesday Eve | Third Hour | Psalm+Gospel | Ps 55:21,1; Mark 14:3-11
Wednesday Eve | Sixth Hour | OT1 | Amos 3:1-11
Wednesday Eve | Sixth Hour | Psalm+Gospel | Ps 140:1,2; John 12:36-43
Wednesday Eve | Ninth Hour | OT1 | Ezek 20:27-33
Wednesday Eve | Ninth Hour | Psalm+Gospel | Ps 7:1-2; John 10:29-38
Wednesday Eve | Eleventh Hour | OT1 | Wis 7:24-30
Wednesday Eve | Eleventh Hour | Psalm+Gospel | Ps 57:1; John 11:55-57
```

Line-by-line comparison against St. Mary source-text index:

| Hour | Stored | St. Mary source | Classification |
|---|---|---|---|
| First | `Jer 43:5-11`; `Ps 69:1,16`; `John 10:17-21` | `Ezek 22:17-22`; `Ezek 22:23-28`; `Ps 59:16-17`; `Matt 22:1-14` | Builder/data bug: stored Wednesday Eve does not match source. |
| Third | `Amos 4:4-13`; `Ps 55:21,1`; `Mark 14:3-11` | `Amos 5:18-27`; `Ps 65:4`; `Matt 24:36-51` | Builder/data bug. |
| Sixth | `Amos 3:1-11`; `Ps 140:1,2`; `John 12:36-43` | `Jer 16:9-13`; `Ps 102:1,2`; `Matt 25:1-13` | Builder/data bug. |
| Ninth | `Ezek 20:27-33`; `Ps 7:1-2`; `John 10:29-38` | `Hos 9:14-10:2`; `Ps 22:20-21`; `Matt 23:29-36` | Builder/data bug. |
| Eleventh | `Wis 7:24-30`; `Ps 57:1`; `John 11:55-57` | `Wis 7:24-30`; `Ps 57:1`; `Jn 11:55-57` | Match at reference level. |

Conclusion: Wednesday Eve is mostly wrong against St. Mary Ottawa. It looks shifted/stale, not just a citation-format issue.

### C2b. Wednesday daytime

Stored Wednesday rows:

```text
Wednesday | First Hour | OT1 | Exod 17:1-7
Wednesday | First Hour | OT2 | Prov 3:5-14
Wednesday | First Hour | OT3 | Hos 5:13-6:3
Wednesday | First Hour | OT4 | Wis 1:20-2:15
Wednesday | First Hour | OT5 | Wis 3:12-24
Wednesday | First Hour | Psalm+Gospel | Ps 51:4; Ps 33:10; John 11:46-57
Wednesday | Third Hour | OT1 | Exod 13:17-22
Wednesday | Third Hour | OT2 | Sir 22:7-18
Wednesday | Third Hour | OT3 | Prov 4:4-5:4
Wednesday | Third Hour | Psalm+Gospel | Ps 41:6,1; Luke 22:1-6
Wednesday | Sixth Hour | OT1 | Exod 14:13-15:1
Wednesday | Sixth Hour | OT2 | Sir 23:7-14
Wednesday | Sixth Hour | OT3 | Job 27:16-20; Job 28:1-2
Wednesday | Sixth Hour | Psalm+Gospel | Ps 83:2,5; John 12:1-8
Wednesday | Ninth Hour | OT1 | Gen 24:1-9
Wednesday | Ninth Hour | OT2 | Num 20:1-13
Wednesday | Ninth Hour | OT3 | Prov 1:11-35
Wednesday | Ninth Hour | OT4 | Isa 59:1-17
Wednesday | Ninth Hour | OT5 | Zech 11:11-14
Wednesday | Ninth Hour | Psalm+Gospel | Ps 41:5-6; Matt 26:3-16
Wednesday | Eleventh Hour | OT1 | Isa 28:16-29
Wednesday | Eleventh Hour | Psalm+Gospel | Ps 6:2-3; Ps 69:17; John 12:27-36
```

Raw St. Mary source evidence and diffs:

| Hour | Stored | St. Mary source text | Raw source lines | Classification |
|---|---|---|---:|---|
| First | `Exod 17:1-7`; `Prov 3:5-14`; `Hos 5:13-6:3`; `Wis 1:20-2:15`; `Wis 3:12-24`; `Ps 51:4`; `Ps 33:10`; `John 11:46-57` | `Exod 17:1-7`; `Prov 3:5-14`; `Hos 5:13-6:3`; `Sirach 1:16-2:15`; `Ps 51:4 & 33:10`; `John 11:46-57` | 7173, 7197, 7218, 7255, 7341, 7351 | Builder/data bug: stored has two Wisdom readings not in source and misses Sirach 1:16-2:15. Source-index parser also has a gap because line 7255 says `Sircah`, so `pascha_source_text_index.csv` missed that source reading. |
| Third | `Exod 13:17-22`; `Sir 22:7-18`; `Prov 4:4-5:4`; `Ps 41:6,1`; `Luke 22:1-6` | `Exod 13:17-22`; `Sir 22:7-18`; `Job 27:16-28:2`; `Prov 4:4-27, 5:1-4`; `Ps 41:6 & 1`; `Luke 22:1-6` | 7463, 7493, 7519, 7552, 7596, 7610 | Builder/data bug: stored omits Job 27:16-28:2 and truncates Proverbs to `Prov 4:4-5:4`. |
| Sixth | `Exod 14:13-15:1`; `Sir 23:7-14`; `Job 27:16-20; Job 28:1-2`; `Ps 83:2,5`; `John 12:1-8` | `Exod 14:13-15:1`; `Isa 48:1-6`; `Sir 23:7-14`; `Ps 83:2 & 5`; `John 12:1-8` | 7701, 7779, 7808, 7839, 7857 | Builder/data bug plus source-index bug: stored wrongly carries the Job reading from Third Hour into Sixth and misses `Isa 48:1-6`. The parsed source index mis-buckets `Isa 48`, `Sir 23`, `Ps 83`, and `John 12` under Ninth because of bad PDF page headers, while the raw Doxology/Exposition says Sixth Hour. |
| Ninth | `Gen 24:1-9`; `Num 20:1-13`; `Prov 1:11-35`; `Isa 59:1-17`; `Zech 11:11-14`; `Ps 41:5-6`; `Matt 26:3-16` | `Gen 24:1-9`; `Num 20:1-13`; `Prov 1:10-33`; `Isa 59:1-17`; `Zech 11:11-14`; `Ps 41:5-7`; `Matt 26:3-16` | 7954, 7980, 8038, 8091, 8133, 8190, 8208 | Builder/data bug: Proverbs and Psalm boundaries differ (`1:11-35` vs `1:10-33`; `Ps 41:5-6` vs `Ps 41:5-7`). |
| Eleventh | `Isa 28:16-29`; `Ps 6:2-3`; `Ps 69:17`; `John 12:27-36` | `Isa 28:16-29`; `Ps 6:2,3 & 69:17`; `John 12:27-36` | 8334, 8419, 8437 | Match at reference level. Stored splits Psalm refs differently but carries the same references. |

Conclusion: Wednesday daytime has real stored-data inaccuracies against St. Mary Ottawa. They are not a display-only problem.

## C3. Holy Week schema and blast radius

### Stored Pascha schema

`out/data/pascha_day_hour_index.csv` uses:

```text
day,hour,source,order,slot,refs
```

It does **not** force all Pascha days into the normal Liturgy-only slot structure of `Pauline / Catholicon / Praxis / Psalm / Gospel`.

However, it does use a lossy/legacy Pascha slot model:

- Prophecies are collapsed into `OT1`, `OT2`, etc.
- Psalm and Gospel are frequently collapsed into one `Psalm+Gospel` slot.
- Some special days also use normal-ish labels (`Pauline`, `Catholic`, `Acts`, `Psalm`, `Gospel`), especially Palm Sunday, Bright Saturday, and Good Friday Pauline rows.

So the likely root cause is **not** “Holy Week was forced into a normal Liturgy schema.” The likely root cause is a curated/legacy Pascha table that has wrong or stale day/hour rows, plus a source-text parser that is not robust enough against St. Mary PDF header/text-order defects.

### Stored slot inventory by day

| Day | Rows | Stored slots |
|---|---:|---|
| Bright Saturday | 4 | `Pauline`, `Catholic`, `Acts`, `Psalm+Gospel` |
| Good Friday | 35 | `OT1`-`OT10`, `Psalm+Gospel`, `Pauline` |
| Great Thursday | 25 | `OT1`-`OT4`, `Acts`, `Psalm+Gospel` |
| Great Thursday Eve | 11 | `OT1`, `OT2`, `Psalm+Gospel` |
| Hosanna Sunday | 2 | `Psalm+Gospel` |
| Monday | 17 | `OT1`-`OT3`, `Psalm+Gospel` |
| Monday Eve | 10 | `OT1`, `Psalm+Gospel` |
| Palm Sunday | 8 | `Psalm`, `Gospel`, `Pauline`, `Catholic`, `Acts`, `Psalm+Gospel` |
| Tuesday | 18 | `OT1`-`OT3`, `Psalm+Gospel` |
| Tuesday Eve | 10 | `OT1`, `Psalm+Gospel` |
| Wednesday | 22 | `OT1`-`OT5`, `Psalm+Gospel` |
| Wednesday Eve | 10 | `OT1`, `Psalm+Gospel` |

### Blast radius against St. Mary source-text index

Set comparison of stored Pascha refs against `pascha_source_text_index.csv` found:

- 62 mismatching day/hour groups.
- 16 affected source day labels.

Affected day/hour-group counts:

| Day label | Mismatching hour groups |
|---|---:|
| Good Friday | 6 |
| Great Thursday | 6 |
| Good Friday Eve | 5 |
| Great Thursday Eve | 5 |
| Monday Eve | 5 |
| Thursday Eve | 5 |
| Tuesday | 5 |
| Tuesday Eve | 5 |
| Wednesday | 5 |
| Wednesday Eve | 4 |
| Monday | 3 |
| Palm Sunday | 3 |
| Hosanna Sunday | 2 |
| Bright Saturday | 1 |
| Thursday | 1 |
| the Covenant Thursday | 1 |

Caution: not every mismatch is automatically a stored-data bug, because the source-text index is incomplete/imperfect for some sections and does not cover every Palm/Bright Saturday line the same way. But Wednesday is not isolated; the local Pascha structure needs a broader source-controlled audit before Phase 2 fixes.

## C4. Phase 1 stopping point

No dataset changes were made.

Recommended Phase 2 decision points before edits:

1. Approve whether Coptic Reader’s static encrypted asset surface is an acceptable comparator route, or require manual Coptic Reader readings for target days only.
2. Approve whether Wednesday corrections should use raw St. Mary Ottawa source text as controlling evidence where `pascha_source_text_index.csv` is known to mis-bucket readings.
3. Decide whether Phase 2 should fix only Wednesday/duplicates or broaden to a full Pascha source-text rebuild, because the blast radius is wider than Wednesday.
