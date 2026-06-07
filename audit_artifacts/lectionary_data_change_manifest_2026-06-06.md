# Coptic Lectionary Data Change Manifest — 2026-06-06

Baseline: `/Users/georgeandraws/workspace/coptic-lectionary-research/audit_artifacts/lectionary_full_audit_baseline_2026-06-06.json`
Post-build inventory: `/Users/georgeandraws/workspace/coptic-lectionary-research/audit_artifacts/post_rebuild_inventory_2026-06-06.json`
Git status: git status failed: not a git repository

## Source-of-truth map
- **raw/provenance layer**: `sources/**`; `out/sources/**`; `cache/copticchurch_html/**`; `St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt`
- **curated normalized source layer**: `out/data/pascha_day_hour_index.*`; `out2/pascha_day_hour_index.*`; `special service curated builders/data`; `Agpeya curated builder/data`; `out/data/pascha_source_text_index.*`
- **generated index layer**: `katameros_cycle_passage_index.*`; `copticchurch_passage_index_2020_2035.*`; `reverse_lookup_crosswalk.*`; `reverse_lookup_summary.*`; `bible_chapter_lectionary_index.*`; `bible_chapter_lectionary_occurrences.*`
- **query helper layer**: `query_lectionary.py`; `passage_normalization.py`; `out/scripts/query_lectionary.py`; `out/scripts/passage_normalization.py`
- **vault publication layer**: `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data`; `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/scripts`; `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/sources`

## Build order verified
1. export Katameros SQLite cycle readings
2. scrape/parse copticchurch.net date cache 2020-2035
3. copy curated Pascha/Bright Saturday datasets
4. extract Pascha source text index
5. build special-service and Agpeya curated indexes
6. build reverse lookup crosswalk
7. build Bible chapter index/occurrences
8. copy sources/support modules/query helper
9. run verification
10. publish all verified data/scripts/sources to vault

## Row-level data changes
### modified_row — `out/data/pascha_day_hour_index.csv + out2/pascha_day_hour_index.csv`
- Layer: curated-layer
- Reason: St Mary Ottawa Holy Pascha source text line 3154 reads Wisdom of Solomon 1:1-9.
- Affected services: Monday of Holy Pascha Sixth Hour OT2
- Affected passages before: ['Wis 2:1-9']
- Affected passages after: ['Wis 1:1-9']
- Verification: `PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py` plus targeted `query_lectionary.py` checks
### replaced_service_rows — `out/data/pascha_day_hour_index.csv + out2/pascha_day_hour_index.csv`
- Layer: curated-layer
- Reason: St Mary Ottawa Holy Pascha source text pages 210-216 showed current table duplicated Monday Sixth Hour.
- Affected services: Tuesday of Holy Pascha Sixth Hour
- Affected passages before: ['Exod 32:7-15', 'Wis 2:1-9', 'Ps 122:4', 'John 2:13-17']
- Affected passages after: ['Ezek 21:3-13', 'Sir 4:20-5:2', 'Isa 1:1-9', 'Ps 18:48,17', 'John 8:12-20']
- Verification: `PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py` plus targeted `query_lectionary.py` checks
### replaced_service_rows — `out/data/pascha_day_hour_index.csv + out2/pascha_day_hour_index.csv`
- Layer: curated-layer
- Reason: St Mary Ottawa Holy Pascha source text pages 278-281 showed Wednesday Eve Eleventh Hour as Wisdom 7:24-30, Psalm 57:1, John 11:55-57.
- Affected services: Wednesday Eve of Holy Pascha Eleventh Hour
- Affected passages before: ['Jer 8:17-9:6', 'Ps 62:7,6', 'John 12:44-50']
- Affected passages after: ['Wis 7:24-30', 'Ps 57:1', 'John 11:55-57']
- Verification: `PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py` plus targeted `query_lectionary.py` checks
### added_file — `out/data/pascha_source_text_index.csv`
- Layer: generated-source-layer
- Reason: Added provenance-backed source-text index to support authoritative crosswalk and source-text lookup.
- Affected services: Holy Pascha source text day/hour headings
- Affected passages before: 
- Affected passages after: All parsed St Mary Ottawa Holy Pascha source-text references; see CSV for source_file/source_line/source_page.
- Verification: `PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py` plus targeted `query_lectionary.py` checks

## Changed files and artifacts
| Layer | Path | Rows before | Rows after | Row Δ | SHA before | SHA after | Schema changed |
|---|---|---:|---:|---:|---|---|---|
| script-layer | `build_lectionary_reference.py` |  |  | None | `c51bcebd7e8f` | `3429fbdddfcc` | False |
| script-layer | `build_lectionary_crosswalk.py` |  |  | None | `cb486986fdf1` | `42dc8f1943c1` | False |
| script-layer | `build_bible_chapter_lectionary_index.py` |  |  | None | `c470dc136a0a` | `d882e91c3f2c` | False |
| script-layer | `build_pascha_source_text_index.py` |  |  | None | `` | `498940c2fcd2` | False |
| script-layer | `query_lectionary.py` |  |  | None | `84777d626d28` | `d1d2f9893d3f` | False |
| script-layer | `passage_normalization.py` |  |  | None | `f1d9cca5ed2a` | `94d3391747dd` | False |
| script-layer | `verify_lectionary_queries.py` |  |  | None | `493da4d0ef37` | `4d6b8e5763ea` | False |
| generated-layer | `out/data/pascha_day_hour_index.csv` | 172 | 173 | 1 | `c89bc1c173f3` | `6ba376421814` | False |
| generated-layer | `out/data/pascha_day_hour_index.jsonl` |  | 173 | None | `` | `71027be6bcb3` | False |
| curated-layer | `out2/pascha_day_hour_index.csv` | 172 | 173 | 1 | `c89bc1c173f3` | `6ba376421814` | False |
| curated-layer | `out2/pascha_day_hour_index.jsonl` |  | 173 | None | `` | `71027be6bcb3` | False |
| generated-layer | `out/data/pascha_source_text_index.csv` |  | 277 | None | `` | `96181c9ec471` | False |
| generated-layer | `out/data/pascha_source_text_index.jsonl` |  | 277 | None | `` | `bb5ac16f6d58` | False |
| generated-layer | `out/data/bright_saturday_service_order.jsonl` |  | 38 | None | `` | `2a4f212afdfb` | False |
| generated-layer | `out/data/special_service_readings_curated.jsonl` |  | 161 | None | `` | `c5c08f9beebe` | False |
| generated-layer | `out/data/special_service_passage_index.jsonl` |  | 196 | None | `` | `f6d3d2fe7b36` | False |
| generated-layer | `out/data/katameros_cycle_readings.jsonl` |  | 4637 | None | `` | `6e4088187de7` | False |
| generated-layer | `out/data/katameros_cycle_passage_index.jsonl` |  | 6224 | None | `` | `bdc4288b5b04` | False |
| generated-layer | `out/data/copticchurch_date_readings_2020_2035.jsonl` |  | 50382 | None | `` | `71fc13c09ff1` | False |
| generated-layer | `out/data/copticchurch_passage_index_2020_2035.jsonl` |  | 59340 | None | `` | `24be5945eefa` | False |
| generated-layer | `out/data/reverse_lookup_crosswalk.csv` | 66208 | 66495 | 287 | `5ce80bcf91cd` | `b83a6a5a8224` | True |
| generated-layer | `out/data/reverse_lookup_crosswalk.jsonl` |  | 66495 | None | `` | `4e0c80febacb` | False |
| generated-layer | `out/data/reverse_lookup_summary.csv` | 2528 | 2648 | 120 | `32a2c67eb9e5` | `95882a1ee870` | True |
| generated-layer | `out/data/bible_chapter_lectionary_index.csv` | 1326 | 1351 | 25 | `1bcf2f5fc7d9` | `c7e93b9835d1` | False |
| generated-layer | `out/data/bible_chapter_lectionary_index.jsonl` |  | 1351 | None | `` | `37f3c583ae9f` | False |
| generated-layer | `out/data/bible_chapter_lectionary_occurrences.csv` | 68914 | 69184 | 270 | `c6d07f5b996a` | `d0c5a4d0db2d` | False |
| generated-layer | `out/data/bible_chapter_lectionary_occurrences.jsonl` |  | 69184 | None | `` | `ef9bf995fcd1` | False |
| generated-layer | `out/data/agpeya_hour_readings.jsonl` |  | 20 | None | `` | `61d293ad77b2` | False |
| generated-layer | `out/data/agpeya_passage_index.jsonl` |  | 149 | None | `` | `a5fce85e6726` | False |
| generated-layer | `out/data/source_ref_repair_report.jsonl` |  | 19 | None | `` | `db10babc39d3` | False |
| query-helper-layer | `out/scripts/query_lectionary.py` |  |  | None | `84777d626d28` | `d1d2f9893d3f` | False |
| query-helper-layer | `out/scripts/passage_normalization.py` |  |  | None | `f1d9cca5ed2a` | `94d3391747dd` | False |
| generated-layer | `out/BUILD_SUMMARY.json` |  |  | None | `ebf0e8b6cdef` | `1bfc9e2f0872` | False |
| vault-publication-layer | `vault:data/pascha_day_hour_index.csv` | 172 | 173 | 1 | `c89bc1c173f3` | `6ba376421814` | False |
| vault-publication-layer | `vault:data/pascha_day_hour_index.jsonl` |  | 173 | None | `` | `71027be6bcb3` | False |
| vault-publication-layer | `vault:data/pascha_source_text_index.csv` |  | 277 | None | `` | `96181c9ec471` | False |
| vault-publication-layer | `vault:data/pascha_source_text_index.jsonl` |  | 277 | None | `` | `bb5ac16f6d58` | False |
| vault-publication-layer | `vault:data/bright_saturday_service_order.jsonl` |  | 38 | None | `` | `2a4f212afdfb` | False |
| vault-publication-layer | `vault:data/special_service_readings_curated.csv` |  | 161 | None | `` | `e7ed10b754e8` | False |
| vault-publication-layer | `vault:data/special_service_readings_curated.jsonl` |  | 161 | None | `` | `c5c08f9beebe` | False |
| vault-publication-layer | `vault:data/special_service_passage_index.csv` |  | 196 | None | `` | `ccac3d96cf5a` | False |
| vault-publication-layer | `vault:data/special_service_passage_index.jsonl` |  | 196 | None | `` | `f6d3d2fe7b36` | False |
| vault-publication-layer | `vault:data/katameros_cycle_readings.csv` | 4637 | 4637 | 0 | `aac34da5c454` | `b1aaeb096550` | False |
| vault-publication-layer | `vault:data/katameros_cycle_readings.jsonl` |  | 4637 | None | `` | `6e4088187de7` | False |
| vault-publication-layer | `vault:data/katameros_cycle_passage_index.csv` | 6224 | 6224 | 0 | `1bfc8d297e77` | `b666782f5442` | True |
| vault-publication-layer | `vault:data/katameros_cycle_passage_index.jsonl` |  | 6224 | None | `` | `bdc4288b5b04` | False |
| vault-publication-layer | `vault:data/copticchurch_date_meta_2020_2035.csv` |  | 5844 | None | `` | `77f1fd83aaf7` | False |
| vault-publication-layer | `vault:data/copticchurch_date_readings_2020_2035.csv` | 50382 | 50382 | 0 | `8bd941bc56c6` | `1db3dcca82e3` | True |
| vault-publication-layer | `vault:data/copticchurch_date_readings_2020_2035.jsonl` |  | 50382 | None | `` | `71fc13c09ff1` | False |
| vault-publication-layer | `vault:data/copticchurch_passage_index_2020_2035.csv` | 62006 | 59340 | -2666 | `d3be38b62b19` | `aefc39122454` | True |
| vault-publication-layer | `vault:data/copticchurch_passage_index_2020_2035.jsonl` |  | 59340 | None | `` | `24be5945eefa` | False |
| vault-publication-layer | `vault:data/copticchurch_scrape_errors.json` |  | 0 | None | `` | `4f53cda18c2b` | False |
| vault-publication-layer | `vault:data/reverse_lookup_crosswalk.csv` | 66208 | 66495 | 287 | `5ce80bcf91cd` | `b83a6a5a8224` | True |
| vault-publication-layer | `vault:data/reverse_lookup_crosswalk.jsonl` |  | 66495 | None | `` | `4e0c80febacb` | False |
| vault-publication-layer | `vault:data/reverse_lookup_summary.csv` | 2528 | 2648 | 120 | `32a2c67eb9e5` | `95882a1ee870` | True |
| vault-publication-layer | `vault:data/bible_chapter_lectionary_index.csv` | 1326 | 1351 | 25 | `1bcf2f5fc7d9` | `c7e93b9835d1` | False |
| vault-publication-layer | `vault:data/bible_chapter_lectionary_index.jsonl` |  | 1351 | None | `` | `37f3c583ae9f` | False |
| vault-publication-layer | `vault:data/bible_chapter_lectionary_occurrences.csv` | 68914 | 69184 | 270 | `c6d07f5b996a` | `d0c5a4d0db2d` | False |
| vault-publication-layer | `vault:data/bible_chapter_lectionary_occurrences.jsonl` |  | 69184 | None | `` | `ef9bf995fcd1` | False |
| vault-publication-layer | `vault:data/agpeya_hour_readings.csv` |  | 20 | None | `` | `3fed8c7cb679` | False |
| vault-publication-layer | `vault:data/agpeya_hour_readings.jsonl` |  | 20 | None | `` | `61d293ad77b2` | False |
| vault-publication-layer | `vault:data/agpeya_passage_index.csv` |  | 149 | None | `` | `d5c41027f101` | False |
| vault-publication-layer | `vault:data/agpeya_passage_index.jsonl` |  | 149 | None | `` | `a5fce85e6726` | False |
| vault-publication-layer | `vault:data/source_ref_repair_report.csv` |  | 19 | None | `` | `2a888014934f` | False |
| vault-publication-layer | `vault:data/source_ref_repair_report.jsonl` |  | 19 | None | `` | `db10babc39d3` | False |
| vault-publication-layer | `vault:scripts/query_lectionary.py` |  |  | None | `84777d626d28` | `d1d2f9893d3f` | False |
| vault-publication-layer | `vault:scripts/passage_normalization.py` |  |  | None | `f1d9cca5ed2a` | `94d3391747dd` | False |
| vault-publication-layer | `vault:BUILD_SUMMARY.json` |  |  | None | `1d0e9ef73877` | `1bfc9e2f0872` | False |

## Summary
- Changed/new tracked files: 68
- Reverse crosswalk after rebuild: 66495 rows
- Bible chapter occurrence rows after rebuild: 69184
- Pascha source-text index: 277 rows, 273 parsed, 4 unparsed source-recovery rows
- Vault publication: package-level publish copied 50 verified files; spot-checked local/vault SHA equality for representative CSV/JSONL artifacts.