# Lectionary full audit baseline — 2026-06-06

Created: 2026-06-06T13:13:31
Repo root: `/Users/georgeandraws/workspace/coptic-lectionary-research`
Git: not a git repo; git status unavailable

## Source/control layer map baseline

| Layer | Local paths | Role |
|---|---|---|
| Raw/provenance | `sources/`, `web_special_service_sources/`, `local_special_service_sources/`, `cache/copticchurch_html/` | Source PDFs/TXT, SQLite, scraped HTML, rite PDFs |
| Curated normalized source | tracked Python row constants and canonical CSV inputs in `out/data` for Pascha/Bright | source-backed curated readings before crosswalk/index generation |
| Generated index | `out/data/*passage_index*`, `reverse_lookup_*`, `bible_chapter_*` | downstream lookup data |
| Query helper | `query_lectionary.py`, `passage_normalization.py`, `out/scripts/` copies | runtime lookup behavior |
| Vault publication | Obsidian Lectionary reference folder copies | published local package for future sessions |

## Category counts

| Category | Files | Bytes |
|---|---:|---:|
| `local_special_service_sources` | 1 | 0 |
| `out/data` | 31 | 168360319 |
| `out/scripts` | 3 | 56836 |
| `out/sources` | 14 | 176425414 |
| `out2` | 3 | 32377 |
| `out_bright` | 3 | 16814 |
| `sources` | 1015 | 298707798 |
| `sources/pdfs` | 12 | 85205211 |
| `web_special_service_sources` | 14 | 41105594 |

## Key file baseline

| Label | Exists | Rows | Size | SHA-256 | Modified |
|---|---:|---:|---:|---|---|
| `repo:README.md` | True |  | 1732 | `9f6f215afeaedffd` | 2026-05-20T08:14:16 |
| `repo:RUNBOOK.md` | True |  | 9120 | `7dc4b8ffee1413ac` | 2026-05-20T08:14:16 |
| `repo:build_lectionary_reference.py` | True |  | 15872 | `c51bcebd7e8fd9f0` | 2026-05-20T08:13:55 |
| `repo:build_lectionary_crosswalk.py` | True |  | 10640 | `cb486986fdf180e5` | 2026-05-20T07:49:56 |
| `repo:build_bible_chapter_lectionary_index.py` | True |  | 10915 | `c470dc136a0a5597` | 2026-05-20T08:13:07 |
| `repo:build_special_service_reference.py` | True |  | 85348 | `9cb9ee3538d291b0` | 2026-05-20T01:15:32 |
| `repo:build_agpeya_reference.py` | True |  | 15851 | `0b77c1090f535d40` | 2026-05-20T00:52:58 |
| `repo:verify_lectionary_queries.py` | True |  | 9701 | `493da4d0ef3749b1` | 2026-05-20T08:13:55 |
| `repo:query_lectionary.py` | True |  | 10447 | `84777d626d280afc` | 2026-05-20T08:17:40 |
| `repo:passage_normalization.py` | True |  | 17073 | `f1d9cca5ed2a524a` | 2026-05-20T07:41:48 |
| `repo:out/BUILD_SUMMARY.json` | True |  | 309 | `ebf0e8b6cdefc5f4` | 2026-05-20T08:20:01 |
| `repo:out/sources/SOURCE_MANIFEST.json` | True | 14 | 2283 | `eb44dc98b03d3831` | 2026-05-20T08:19:27 |
| `repo:out/data/katameros_cycle_readings.csv` | True | 4637 | 685420 | `b1aaeb09655078c2` | 2026-05-20T08:17:58 |
| `repo:out/data/katameros_cycle_passage_index.csv` | True | 6224 | 1288089 | `b666782f54424f68` | 2026-05-20T08:17:58 |
| `repo:out/data/copticchurch_date_readings_2020_2035.csv` | True | 50382 | 9740879 | `1db3dcca82e3da8e` | 2026-05-20T08:19:16 |
| `repo:out/data/copticchurch_passage_index_2020_2035.csv` | True | 59340 | 11276963 | `aefc39122454047b` | 2026-05-20T08:19:19 |
| `repo:out/data/copticchurch_date_meta_2020_2035.csv` | True | 5844 | 774160 | `77f1fd83aaf7679c` | 2026-05-20T08:19:16 |
| `repo:out/data/copticchurch_scrape_errors.json` | True | 0 | 2 | `4f53cda18c2baa0c` | 2026-05-20T08:19:20 |
| `repo:out/data/pascha_day_hour_index.csv` | True | 172 | 10236 | `c89bc1c173f38aad` | 2026-06-06T12:20:39 |
| `repo:out/data/bright_saturday_service_order.csv` | True | 38 | 6053 | `4b3669221243e2fc` | 2026-05-19T16:49:42 |
| `repo:out/data/special_service_readings_curated.csv` | True | 161 | 48197 | `e7ed10b754e885e6` | 2026-05-20T08:19:20 |
| `repo:out/data/special_service_passage_index.csv` | True | 196 | 65510 | `ccac3d96cf5a2a8a` | 2026-05-20T08:19:20 |
| `repo:out/data/agpeya_hour_readings.csv` | True | 20 | 11074 | `3fed8c7cb67930d2` | 2026-05-20T08:19:20 |
| `repo:out/data/agpeya_passage_index.csv` | True | 149 | 130719 | `d5c41027f101cd66` | 2026-05-20T08:19:20 |
| `repo:out/data/reverse_lookup_crosswalk.csv` | True | 66208 | 13790111 | `5ce80bcf91cd1e4c` | 2026-06-06T12:21:43 |
| `repo:out/data/reverse_lookup_summary.csv` | True | 2528 | 70381 | `32a2c67eb9e55e91` | 2026-06-06T12:21:43 |
| `repo:out/data/bible_chapter_lectionary_index.csv` | True | 1326 | 393736 | `1bcf2f5fc7d90b1c` | 2026-06-06T12:21:44 |
| `repo:out/data/bible_chapter_lectionary_occurrences.csv` | True | 68914 | 16098147 | `c6d07f5b996a797c` | 2026-06-06T12:21:45 |
| `repo:out/data/source_ref_repair_report.csv` | True | 19 | 3185 | `2a888014934fb4fa` | 2026-05-20T08:19:19 |
| `repo:out/scripts/query_lectionary.py` | True |  | 10447 | `84777d626d280afc` | 2026-05-20T08:17:40 |
| `repo:out/scripts/passage_normalization.py` | True |  | 17073 | `f1d9cca5ed2a524a` | 2026-05-20T07:41:48 |
| `repo:out2/pascha_day_hour_index.csv` | True | 172 | 10236 | `c89bc1c173f38aad` | 2026-06-06T12:20:39 |
| `repo:out_bright/bright_saturday_service_order.csv` | True | 38 | 6053 | `4b3669221243e2fc` | 2026-05-19T16:49:42 |
| `vault:Coptic Orthodox Lectionary Reference/BUILD_SUMMARY.json` | True |  | 1218 | `1d0e9ef73877dbf3` | 2026-06-06T12:28:01 |
| `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_readings.csv` | True | 4637 | 687102 | `aac34da5c45499f6` | 2026-05-19T12:26:59 |
| `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_passage_index.csv` | True | 6224 | 1223615 | `1bfc8d297e777db5` | 2026-05-19T12:26:59 |
| `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_readings_2020_2035.csv` | True | 50382 | 9548017 | `8bd941bc56c6fc7b` | 2026-05-19T12:32:34 |
| `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_passage_index_2020_2035.csv` | True | 62006 | 11578377 | `d3be38b62b192540` | 2026-05-19T12:32:35 |
| `vault:Coptic Orthodox Lectionary Reference/data/pascha_day_hour_index.csv` | True | 172 | 10236 | `c89bc1c173f38aad` | 2026-06-06T12:20:39 |
| `vault:Coptic Orthodox Lectionary Reference/data/bright_saturday_service_order.csv` | True | 38 | 6053 | `4b3669221243e2fc` | 2026-05-19T16:49:42 |
| `vault:special_service_readings_curated.csv` | True | 161 | 48197 | `e7ed10b754e885e6` | 2026-05-20T08:19:20 |
| `vault:special_service_passage_index.csv` | True | 196 | 65510 | `ccac3d96cf5a2a8a` | 2026-05-20T08:19:20 |
| `vault:agpeya_hour_readings.csv` | True | 20 | 11074 | `3fed8c7cb67930d2` | 2026-05-20T08:19:20 |
| `vault:agpeya_passage_index.csv` | True | 149 | 130719 | `d5c41027f101cd66` | 2026-05-20T08:19:20 |
| `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_crosswalk.csv` | True | 66208 | 13790111 | `5ce80bcf91cd1e4c` | 2026-06-06T12:21:43 |
| `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_summary.csv` | True | 2528 | 70381 | `32a2c67eb9e55e91` | 2026-06-06T12:21:43 |
| `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_index.csv` | True | 1326 | 393736 | `1bcf2f5fc7d90b1c` | 2026-06-06T12:21:44 |
| `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_occurrences.csv` | True | 68914 | 16098147 | `c6d07f5b996a797c` | 2026-06-06T12:21:45 |
| `vault:Coptic Orthodox Lectionary Reference/scripts/query_lectionary.py` | True |  | 10447 | `84777d626d280afc` | 2026-05-20T08:17:40 |
| `vault:Coptic Orthodox Lectionary Reference/scripts/passage_normalization.py` | True |  | 17073 | `f1d9cca5ed2a524a` | 2026-05-20T07:41:48 |
| `vault:Coptic Orthodox Lectionary Index.md` | True |  | 3279 | `47d79f335ee37633` | 2026-06-06T12:28:01 |
| `vault:Coptic Orthodox Lectionary Reference.md` | True |  | 19466 | `845f75ab83f5c641` | 2026-06-06T13:01:57 |
| `vault:Coptic Orthodox Special Services Missing Tracker.md` | True |  | 10905 | `c76836f1c949e3ac` | 2026-05-20T01:27:32 |
| `vault:Coptic Orthodox Special Service Reading Tables.md` | True |  | 10869 | `51cab430d85e5e9f` | 2026-05-20T01:27:31 |
| `vault:Coptic Orthodox Agpeya Hour Reading Map.md` | True |  | 2274 | `54afad9ba37495f9` | 2026-05-20T01:05:43 |
