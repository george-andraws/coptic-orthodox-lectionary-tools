# Coptic Lectionary Data Change Manifest — Final 2026-06-06

Created: 2026-06-06T13:58:53
Baseline: `/Users/georgeandraws/workspace/coptic-lectionary-research/audit_artifacts/lectionary_full_audit_baseline_2026-06-06.json`
Final verifier: `/Users/georgeandraws/workspace/coptic-lectionary-research/audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

## Authoritative source-of-truth map

### raw/provenance layer
- `sources/**`
- `out/sources/**`
- `cache/copticchurch_html/**`
- `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt`

### curated normalized source layer
- `out/data/pascha_day_hour_index.*`
- `out/data/pascha_source_text_index.*`
- `out/data/bright_saturday_service_order.*`
- `out/data/special_service_readings_curated.*`
- `out/data/agpeya_hour_readings.*`

### generated index layer
- `out/data/katameros_cycle_passage_index.*`
- `out/data/copticchurch_passage_index_2020_2035.*`
- `out/data/reverse_lookup_crosswalk.*`
- `out/data/reverse_lookup_summary.*`
- `out/data/bible_chapter_lectionary_index.*`
- `out/data/bible_chapter_lectionary_occurrences.*`
- `out/data/source_ref_repair_report.csv`

### query helper layer
- `query_lectionary.py`
- `passage_normalization.py`
- `out/scripts/query_lectionary.py`
- `out/scripts/passage_normalization.py`

### vault publication layer
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data`
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/scripts`
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/sources`

## Build order

1. source extraction and copticchurch cache parse
2. ordinary cycle/date data generation
3. Pascha/Bright Saturday/special-service/Agpeya normalized data
4. Pascha source-text extraction
5. normalized passage indexes
6. reverse lookup crosswalk
7. Bible chapter index and occurrences
8. packaged query helper/scripts
9. verification gate
10. vault publication

## Summary

### scripts changed (9)
- `build_lectionary_reference.py`
- `build_lectionary_crosswalk.py`
- `build_bible_chapter_lectionary_index.py`
- `verify_lectionary_queries.py`
- `query_lectionary.py`
- `passage_normalization.py`
- `out/scripts/query_lectionary.py`
- `out/scripts/passage_normalization.py`
- `build_pascha_source_text_index.py`

### curated source data changed (8)
- `out/data/pascha_day_hour_index.csv`
- `out2/pascha_day_hour_index.csv`
- `out/data/pascha_source_text_index.csv`
- `out/data/pascha_source_text_index.jsonl`
- `out/data/pascha_day_hour_index.jsonl`
- `out/data/bright_saturday_service_order.jsonl`
- `out/data/special_service_readings_curated.jsonl`
- `out/data/special_service_passage_index.jsonl`

### generated artifacts rebuilt (11)
- `out/BUILD_SUMMARY.json`
- `out/sources/SOURCE_MANIFEST.json`
- `out/data/reverse_lookup_crosswalk.csv`
- `out/data/reverse_lookup_summary.csv`
- `out/data/bible_chapter_lectionary_index.csv`
- `out/data/bible_chapter_lectionary_occurrences.csv`
- `out/data/katameros_cycle_passage_index.jsonl`
- `out/data/copticchurch_passage_index_2020_2035.jsonl`
- `out/data/reverse_lookup_crosswalk.jsonl`
- `out/data/bible_chapter_lectionary_index.jsonl`
- `out/data/bible_chapter_lectionary_occurrences.jsonl`

### vault published files changed (51)
- `vault:Coptic Orthodox Lectionary Reference/BUILD_SUMMARY.json`
- `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_readings.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_passage_index.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_readings_2020_2035.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_passage_index_2020_2035.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/pascha_day_hour_index.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_crosswalk.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_summary.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_index.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_occurrences.csv`
- `vault:Coptic Orthodox Lectionary Reference/scripts/query_lectionary.py`
- `vault:Coptic Orthodox Lectionary Reference/scripts/passage_normalization.py`
- `vault:Coptic Orthodox Lectionary Reference/data/agpeya_hour_readings.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/pascha_source_text_index.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_passage_index.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_passage_index_2020_2035.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/agpeya_hour_readings.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/special_service_readings_curated.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/special_service_passage_index.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_crosswalk.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/agpeya_passage_index.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/bright_saturday_service_order.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_readings_2020_2035.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/source_ref_repair_report.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/GENESIS_PASCHA_CORRECTION_2026-06-06.json`
- `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_readings.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/bright_saturday_service_order.md`
- `vault:Coptic Orthodox Lectionary Reference/data/source_ref_repair_report.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/pascha_source_text_index.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/pascha_day_hour_index.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_occurrences.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/special_service_readings_curated.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_index.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_meta_2020_2035.csv`
- `vault:Coptic Orthodox Lectionary Reference/data/special_service_passage_index.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/agpeya_passage_index.jsonl`
- `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_scrape_errors.json`
- `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Days.pdf`
- `vault:Coptic Orthodox Lectionary Reference/sources/SOURCE_MANIFEST.json`
- `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Sundays.txt`
- `vault:Coptic Orthodox Lectionary Reference/sources/KatamerosDatabase.sqlite`
- `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Days.txt`
- `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Sundays.pdf`
- `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Lent.pdf`
- `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Pentecost.txt`
- `vault:Coptic Orthodox Lectionary Reference/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN_Coptic_AR.txt`
- `vault:Coptic Orthodox Lectionary Reference/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt`
- `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Pentecost.pdf`
- `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Lent.txt`
- `vault:Coptic Orthodox Lectionary Reference/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.pdf`
- `vault:Coptic Orthodox Lectionary Reference/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN_Coptic_AR.pdf`

## Row count and schema deltas

| File | Layer | Rows before | Rows after | Delta | Schema changed |
|---|---:|---:|---:|---:|---|
| `out/sources/SOURCE_MANIFEST.json` | generated-index-layer | 14 | 14 | 0 | False |
| `out/data/pascha_day_hour_index.csv` | curated/generated-source-layer | 172 | 173 | 1 | False |
| `out/data/reverse_lookup_crosswalk.csv` | generated-index-layer | 66208 | 66504 | 296 | True |
| `out/data/reverse_lookup_summary.csv` | generated-index-layer | 2528 | 2650 | 122 | True |
| `out/data/bible_chapter_lectionary_index.csv` | generated-index-layer | 1326 | 1351 | 25 | False |
| `out/data/bible_chapter_lectionary_occurrences.csv` | generated-index-layer | 68914 | 71315 | 2401 | False |
| `out2/pascha_day_hour_index.csv` | curated/generated-source-layer | 172 | 173 | 1 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_readings.csv` | vault-publication-layer | 4637 | 4637 | 0 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_passage_index.csv` | vault-publication-layer | 6224 | 6224 | 0 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_readings_2020_2035.csv` | vault-publication-layer | 50382 | 50382 | 0 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_passage_index_2020_2035.csv` | vault-publication-layer | 62006 | 59340 | -2666 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/pascha_day_hour_index.csv` | vault-publication-layer | 172 | 173 | 1 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_crosswalk.csv` | vault-publication-layer | 66208 | 66504 | 296 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_summary.csv` | vault-publication-layer | 2528 | 2650 | 122 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_index.csv` | vault-publication-layer | 1326 | 1351 | 25 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_occurrences.csv` | vault-publication-layer | 68914 | 71315 | 2401 | False |
| `out/data/pascha_source_text_index.csv` | curated/generated-source-layer | None | 277 | 277 | True |
| `out/data/pascha_source_text_index.jsonl` | curated/generated-source-layer | None | 277 | 277 | False |
| `out/data/pascha_day_hour_index.jsonl` | curated/generated-source-layer | None | 173 | 173 | False |
| `out/data/bright_saturday_service_order.jsonl` | curated/generated-source-layer | None | 38 | 38 | False |
| `out/data/special_service_readings_curated.jsonl` | curated/generated-source-layer | None | 161 | 161 | False |
| `out/data/special_service_passage_index.jsonl` | curated/generated-source-layer | None | 196 | 196 | False |
| `out/data/katameros_cycle_passage_index.jsonl` | generated-index-layer | None | 6224 | 6224 | False |
| `out/data/copticchurch_passage_index_2020_2035.jsonl` | generated-index-layer | None | 59340 | 59340 | False |
| `out/data/reverse_lookup_crosswalk.jsonl` | generated-index-layer | None | 66504 | 66504 | False |
| `out/data/bible_chapter_lectionary_index.jsonl` | generated-index-layer | None | 1351 | 1351 | False |
| `out/data/bible_chapter_lectionary_occurrences.jsonl` | generated-index-layer | None | 71315 | 71315 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/agpeya_hour_readings.csv` | vault-publication-layer | None | 20 | 20 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/pascha_source_text_index.csv` | vault-publication-layer | None | 277 | 277 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_passage_index.jsonl` | vault-publication-layer | None | 6224 | 6224 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_passage_index_2020_2035.jsonl` | vault-publication-layer | None | 59340 | 59340 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/agpeya_hour_readings.jsonl` | vault-publication-layer | None | 20 | 20 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/special_service_readings_curated.csv` | vault-publication-layer | None | 161 | 161 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/special_service_passage_index.csv` | vault-publication-layer | None | 196 | 196 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_crosswalk.jsonl` | vault-publication-layer | None | 66504 | 66504 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/agpeya_passage_index.csv` | vault-publication-layer | None | 149 | 149 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/bright_saturday_service_order.jsonl` | vault-publication-layer | None | 38 | 38 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_readings_2020_2035.jsonl` | vault-publication-layer | None | 50382 | 50382 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/source_ref_repair_report.csv` | vault-publication-layer | None | 19 | 19 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_readings.jsonl` | vault-publication-layer | None | 4637 | 4637 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/source_ref_repair_report.jsonl` | vault-publication-layer | None | 19 | 19 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/pascha_source_text_index.jsonl` | vault-publication-layer | None | 277 | 277 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/pascha_day_hour_index.jsonl` | vault-publication-layer | None | 173 | 173 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_occurrences.jsonl` | vault-publication-layer | None | 71315 | 71315 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/special_service_readings_curated.jsonl` | vault-publication-layer | None | 161 | 161 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_index.jsonl` | vault-publication-layer | None | 1351 | 1351 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_meta_2020_2035.csv` | vault-publication-layer | None | 5844 | 5844 | True |
| `vault:Coptic Orthodox Lectionary Reference/data/special_service_passage_index.jsonl` | vault-publication-layer | None | 196 | 196 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/agpeya_passage_index.jsonl` | vault-publication-layer | None | 149 | 149 | False |
| `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_scrape_errors.json` | vault-publication-layer | None | 0 | 0 | False |
| `vault:Coptic Orthodox Lectionary Reference/sources/SOURCE_MANIFEST.json` | vault-publication-layer | None | 14 | 14 | False |

## Schema changes

### `out/data/reverse_lookup_crosswalk.csv`
- Before: `['passage', 'source_kind', 'liturgical_place', 'calendar_key', 'gregorian_date', 'coptic_date', 'day_title', 'service_section', 'reading_type', 'significance_note', 'synaxarium_note', 'source_ref', 'url']`
- After: `['passage', 'source_kind', 'source_family', 'source_table', 'source_file', 'source_row_id', 'liturgical_place', 'calendar_key', 'gregorian_date', 'coptic_date', 'day_title', 'service_day', 'service_hour', 'service_section', 'reading_slot', 'reading_type', 'source_ref', 'raw_ref', 'normalized_ref', 'normalized_segment', 'book', 'book_abbrev', 'chapter_start', 'verse_start', 'chapter_end', 'verse_end', 'significance_note', 'synaxarium_note', 'url', 'provenance']`

### `out/data/reverse_lookup_summary.csv`
- Before: `['passage', 'cycle_occurrences', 'date_occurrences', 'special_service_occurrences', 'agpeya_occurrences', 'pascha_occurrences', 'bright_saturday_occurrences', 'total_occurrences']`
- After: `['passage', 'cycle_occurrences', 'date_occurrences', 'special_service_occurrences', 'agpeya_occurrences', 'pascha_occurrences', 'pascha_source_text_occurrences', 'bright_saturday_occurrences', 'total_occurrences']`

### `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_passage_index.csv`
- Before: `['book', 'book_abbrev', 'chapter', 'verse_start', 'verse_end', 'raw_segment', 'normalized_segment', 'source', 'source_table', 'source_type', 'cycle', 'day_key', 'month_number', 'month_name', 'day', 'week', 'day_of_week', 'day_name', 'season', 'other', 'reading_slot', 'raw_ref', 'normalized_ref']`
- After: `['book', 'book_abbrev', 'chapter', 'verse_start', 'verse_end', 'raw_segment', 'normalized_segment', 'canonical_segment', 'source', 'source_table', 'source_type', 'cycle', 'day_key', 'month_number', 'month_name', 'day', 'week', 'day_of_week', 'day_name', 'season', 'other', 'reading_slot', 'raw_ref', 'normalized_ref']`

### `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_readings_2020_2035.csv`
- Before: `['source', 'gregorian_date', 'weekday', 'day_title', 'service_section', 'reading_type', 'raw_ref', 'normalized_ref', 'url']`
- After: `['source', 'gregorian_date', 'weekday', 'day_title', 'service_section', 'reading_type', 'raw_ref', 'normalized_ref', 'parse_status', 'normalization_warning', 'url']`

### `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_passage_index_2020_2035.csv`
- Before: `['source', 'gregorian_date', 'weekday', 'day_title', 'service_section', 'reading_type', 'matched_ref', 'raw_ref', 'url']`
- After: `['source', 'gregorian_date', 'weekday', 'day_title', 'service_section', 'reading_type', 'matched_ref', 'raw_ref', 'source_ref_status', 'normalization_warning', 'url']`

### `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_crosswalk.csv`
- Before: `['passage', 'source_kind', 'liturgical_place', 'calendar_key', 'gregorian_date', 'coptic_date', 'day_title', 'service_section', 'reading_type', 'significance_note', 'synaxarium_note', 'source_ref', 'url']`
- After: `['passage', 'source_kind', 'source_family', 'source_table', 'source_file', 'source_row_id', 'liturgical_place', 'calendar_key', 'gregorian_date', 'coptic_date', 'day_title', 'service_day', 'service_hour', 'service_section', 'reading_slot', 'reading_type', 'source_ref', 'raw_ref', 'normalized_ref', 'normalized_segment', 'book', 'book_abbrev', 'chapter_start', 'verse_start', 'chapter_end', 'verse_end', 'significance_note', 'synaxarium_note', 'url', 'provenance']`

### `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_summary.csv`
- Before: `['passage', 'cycle_occurrences', 'date_occurrences', 'special_service_occurrences', 'agpeya_occurrences', 'pascha_occurrences', 'bright_saturday_occurrences', 'total_occurrences']`
- After: `['passage', 'cycle_occurrences', 'date_occurrences', 'special_service_occurrences', 'agpeya_occurrences', 'pascha_occurrences', 'pascha_source_text_occurrences', 'bright_saturday_occurrences', 'total_occurrences']`

### `out/data/pascha_source_text_index.csv`
- Before: `None`
- After: `['day', 'hour', 'source_kind', 'source_family', 'source_file', 'source_line', 'source_page', 'order', 'reading_type', 'raw_ref', 'normalized_ref', 'parse_status', 'provenance_note']`

### `vault:Coptic Orthodox Lectionary Reference/data/agpeya_hour_readings.csv`
- Before: `None`
- After: `['prayer_group', 'prayer_key', 'prayer_name', 'service_order', 'reading_type', 'raw_ref', 'display_ref', 'source_title', 'source_url', 'source_page', 'notes', 'canonical_ref']`

### `vault:Coptic Orthodox Lectionary Reference/data/pascha_source_text_index.csv`
- Before: `None`
- After: `['day', 'hour', 'source_kind', 'source_family', 'source_file', 'source_line', 'source_page', 'order', 'reading_type', 'raw_ref', 'normalized_ref', 'parse_status', 'provenance_note']`

### `vault:Coptic Orthodox Lectionary Reference/data/special_service_readings_curated.csv`
- Before: `None`
- After: `['service_family', 'service_variant', 'section', 'reading_type', 'raw_ref', 'source_title', 'source_url', 'source_page', 'notes', 'canonical_ref']`

### `vault:Coptic Orthodox Lectionary Reference/data/special_service_passage_index.csv`
- Before: `None`
- After: `['service_family', 'service_variant', 'section', 'reading_type', 'raw_ref', 'canonical_ref', 'matched_ref', 'source_title', 'source_url', 'source_page', 'notes', 'source_kind']`

### `vault:Coptic Orthodox Lectionary Reference/data/agpeya_passage_index.csv`
- Before: `None`
- After: `['prayer_group', 'prayer_key', 'prayer_name', 'service_order', 'reading_type', 'raw_ref', 'display_ref', 'canonical_ref', 'matched_ref', 'source_title', 'source_url', 'source_page', 'notes', 'source_kind']`

### `vault:Coptic Orthodox Lectionary Reference/data/source_ref_repair_report.csv`
- Before: `None`
- After: `['gregorian_date', 'day_title', 'service_section', 'reading_type', 'raw_ref', 'repaired_ref', 'source_ref_status', 'normalization_warning', 'url']`

### `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_meta_2020_2035.csv`
- Before: `None`
- After: `['date', 'title', 'day_title', 'reading_count']`


## Affected passages/services

| Passage | Service/day/hour | Reason |
|---|---|---|
| Genesis 18:1-23 | Great Thursday Liturgy of Blessing of the Water OT1 | verified preservation after Pascha day/hour correction |
| Genesis 2:15-25; Genesis 3:1-24 | Monday Ninth Hour OT1 | verified not duplicated under Tuesday Ninth Hour |
| Genesis 6:5-9:7 | Tuesday Ninth Hour OT1 | restored correct Tuesday row |
| Genesis 22:1-19 | Great Thursday Ninth Hour OT1 | regression preservation |
| Genesis 14:17-20 | Great Thursday Ninth Hour OT3 | regression preservation |
| Wisdom 1:1-9 | Monday Sixth Hour Prophecy/OT2 | Wisdom alias parsing and Pascha source-text/crosswalk inclusion |
| Wisdom 7:24-30 | Wednesday Eve Eleventh Hour Prophecy/OT1 | Wisdom alias parsing and Pascha source-text/crosswalk inclusion |
| Wisdom 2:12-22 | Good Friday First Hour Prophecy/OT6 | Wisdom alias parsing and Pascha source-text/crosswalk inclusion |
| Sirach 4:20-5:2 | Tuesday Sixth Hour Prophecy/OT2 | Sirach alias parsing and Pascha source-text inclusion |
| Ezekiel 21:3-13 | Tuesday Sixth Hour OT1 | Tuesday Sixth Hour corrected/verified |
| Isaiah 1:1-9 | Tuesday Sixth Hour OT3 | Tuesday Sixth Hour corrected/verified |
| John 8:12-20 | Tuesday Sixth Hour Gospel | Tuesday Sixth Hour corrected/verified; guide claims updated |
| John 2:13-17 | Monday Sixth Hour Gospel | false Tuesday Sixth Hour guide claims removed |
| Exodus 32:7-15 | Monday Sixth Hour Prophecy/OT1 | normalizer repaired malformed Exod d d-style variants |
| Psalm 62:7,6 / Psalm 62:7,2 | Pascha Monday/Tuesday Eve First Hour and Thursday Eve Eleventh Hour source text | combined Psalm verse parsing repaired and guide claims corrected |
| Psalm 18:48,17 | Tuesday Sixth Hour Psalm | combined Psalm verse parsing repaired |
| Psalm 122:4 | Monday Sixth Hour and Monday/Tuesday Eve Eleventh Hour | removed false Holy Tuesday Sixth Hour guide claim |
| Jeremiah 8:17-9:6 | Great Thursday Eve First Hour | removed false Wednesday Eve Eleventh Hour guide claim |

## Changed files with checksums

### `build_lectionary_reference.py`
- Layer: script-layer
- Before rows/checksum: None / `c51bcebd7e8fd9f0`
- After rows/checksum: None / `3429fbdddfcc41a5`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `build_lectionary_crosswalk.py`
- Layer: script-layer
- Before rows/checksum: None / `cb486986fdf180e5`
- After rows/checksum: None / `42dc8f1943c1c1b0`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `build_bible_chapter_lectionary_index.py`
- Layer: script-layer
- Before rows/checksum: None / `c470dc136a0a5597`
- After rows/checksum: None / `d882e91c3f2c91fa`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `verify_lectionary_queries.py`
- Layer: script-layer
- Before rows/checksum: None / `493da4d0ef3749b1`
- After rows/checksum: None / `60276a986e8deb53`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `query_lectionary.py`
- Layer: query-helper-layer
- Before rows/checksum: None / `84777d626d280afc`
- After rows/checksum: None / `d1d2f9893d3f54bc`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `passage_normalization.py`
- Layer: query-helper-layer
- Before rows/checksum: None / `f1d9cca5ed2a524a`
- After rows/checksum: None / `1286c5870aafc923`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/BUILD_SUMMARY.json`
- Layer: generated-index-layer
- Before rows/checksum: None / `ebf0e8b6cdefc5f4`
- After rows/checksum: None / `5ebd1403af735296`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/sources/SOURCE_MANIFEST.json`
- Layer: generated-index-layer
- Before rows/checksum: 14 / `eb44dc98b03d3831`
- After rows/checksum: 14 / `bc580f848a392c30`
- Row delta: 0
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/pascha_day_hour_index.csv`
- Layer: curated/generated-source-layer
- Before rows/checksum: 172 / `c89bc1c173f38aad`
- After rows/checksum: 173 / `6ba376421814cf97`
- Row delta: 1
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/reverse_lookup_crosswalk.csv`
- Layer: generated-index-layer
- Before rows/checksum: 66208 / `5ce80bcf91cd1e4c`
- After rows/checksum: 66504 / `057081672b36992d`
- Row delta: 296
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/reverse_lookup_summary.csv`
- Layer: generated-index-layer
- Before rows/checksum: 2528 / `32a2c67eb9e55e91`
- After rows/checksum: 2650 / `2b42150e845737f1`
- Row delta: 122
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/bible_chapter_lectionary_index.csv`
- Layer: generated-index-layer
- Before rows/checksum: 1326 / `1bcf2f5fc7d90b1c`
- After rows/checksum: 1351 / `429795c05f707bf8`
- Row delta: 25
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/bible_chapter_lectionary_occurrences.csv`
- Layer: generated-index-layer
- Before rows/checksum: 68914 / `c6d07f5b996a797c`
- After rows/checksum: 71315 / `36f9cd49569de3a6`
- Row delta: 2401
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/scripts/query_lectionary.py`
- Layer: query-helper-layer
- Before rows/checksum: None / `84777d626d280afc`
- After rows/checksum: None / `d1d2f9893d3f54bc`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/scripts/passage_normalization.py`
- Layer: query-helper-layer
- Before rows/checksum: None / `f1d9cca5ed2a524a`
- After rows/checksum: None / `1286c5870aafc923`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out2/pascha_day_hour_index.csv`
- Layer: curated/generated-source-layer
- Before rows/checksum: 172 / `c89bc1c173f38aad`
- After rows/checksum: 173 / `6ba376421814cf97`
- Row delta: 1
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/BUILD_SUMMARY.json`
- Layer: vault-publication-layer
- Before rows/checksum: None / `1d0e9ef73877dbf3`
- After rows/checksum: None / `5ebd1403af735296`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_readings.csv`
- Layer: vault-publication-layer
- Before rows/checksum: 4637 / `aac34da5c45499f6`
- After rows/checksum: 4637 / `b1aaeb09655078c2`
- Row delta: 0
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_passage_index.csv`
- Layer: vault-publication-layer
- Before rows/checksum: 6224 / `1bfc8d297e777db5`
- After rows/checksum: 6224 / `b666782f54424f68`
- Row delta: 0
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_readings_2020_2035.csv`
- Layer: vault-publication-layer
- Before rows/checksum: 50382 / `8bd941bc56c6fc7b`
- After rows/checksum: 50382 / `1db3dcca82e3da8e`
- Row delta: 0
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_passage_index_2020_2035.csv`
- Layer: vault-publication-layer
- Before rows/checksum: 62006 / `d3be38b62b192540`
- After rows/checksum: 59340 / `aefc39122454047b`
- Row delta: -2666
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/pascha_day_hour_index.csv`
- Layer: vault-publication-layer
- Before rows/checksum: 172 / `c89bc1c173f38aad`
- After rows/checksum: 173 / `6ba376421814cf97`
- Row delta: 1
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_crosswalk.csv`
- Layer: vault-publication-layer
- Before rows/checksum: 66208 / `5ce80bcf91cd1e4c`
- After rows/checksum: 66504 / `057081672b36992d`
- Row delta: 296
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_summary.csv`
- Layer: vault-publication-layer
- Before rows/checksum: 2528 / `32a2c67eb9e55e91`
- After rows/checksum: 2650 / `2b42150e845737f1`
- Row delta: 122
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_index.csv`
- Layer: vault-publication-layer
- Before rows/checksum: 1326 / `1bcf2f5fc7d90b1c`
- After rows/checksum: 1351 / `429795c05f707bf8`
- Row delta: 25
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_occurrences.csv`
- Layer: vault-publication-layer
- Before rows/checksum: 68914 / `c6d07f5b996a797c`
- After rows/checksum: 71315 / `36f9cd49569de3a6`
- Row delta: 2401
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/scripts/query_lectionary.py`
- Layer: vault-publication-layer
- Before rows/checksum: None / `84777d626d280afc`
- After rows/checksum: None / `d1d2f9893d3f54bc`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/scripts/passage_normalization.py`
- Layer: vault-publication-layer
- Before rows/checksum: None / `f1d9cca5ed2a524a`
- After rows/checksum: None / `1286c5870aafc923`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `build_pascha_source_text_index.py`
- Layer: script-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `498940c2fcd2807f`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/pascha_source_text_index.csv`
- Layer: curated/generated-source-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 277 / `96181c9ec471c9b9`
- Row delta: 277
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/pascha_source_text_index.jsonl`
- Layer: curated/generated-source-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 277 / `bb5ac16f6d58df25`
- Row delta: 277
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/pascha_day_hour_index.jsonl`
- Layer: curated/generated-source-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 173 / `71027be6bcb35322`
- Row delta: 173
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/bright_saturday_service_order.jsonl`
- Layer: curated/generated-source-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 38 / `2a4f212afdfb0ff4`
- Row delta: 38
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/special_service_readings_curated.jsonl`
- Layer: curated/generated-source-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 161 / `c5c08f9beebebd70`
- Row delta: 161
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/special_service_passage_index.jsonl`
- Layer: curated/generated-source-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 196 / `f6d3d2fe7b36b137`
- Row delta: 196
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/katameros_cycle_passage_index.jsonl`
- Layer: generated-index-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 6224 / `bdc4288b5b04ee48`
- Row delta: 6224
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/copticchurch_passage_index_2020_2035.jsonl`
- Layer: generated-index-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 59340 / `24be5945eefa4031`
- Row delta: 59340
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/reverse_lookup_crosswalk.jsonl`
- Layer: generated-index-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 66504 / `cacc1eda4e1ffbfe`
- Row delta: 66504
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/bible_chapter_lectionary_index.jsonl`
- Layer: generated-index-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 1351 / `18e00db47400d44c`
- Row delta: 1351
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `out/data/bible_chapter_lectionary_occurrences.jsonl`
- Layer: generated-index-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 71315 / `268e54888b08f79b`
- Row delta: 71315
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/agpeya_hour_readings.csv`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 20 / `3fed8c7cb67930d2`
- Row delta: 20
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/pascha_source_text_index.csv`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 277 / `96181c9ec471c9b9`
- Row delta: 277
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_passage_index.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 6224 / `bdc4288b5b04ee48`
- Row delta: 6224
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_passage_index_2020_2035.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 59340 / `24be5945eefa4031`
- Row delta: 59340
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/agpeya_hour_readings.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 20 / `61d293ad77b20fde`
- Row delta: 20
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/special_service_readings_curated.csv`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 161 / `e7ed10b754e885e6`
- Row delta: 161
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/special_service_passage_index.csv`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 196 / `ccac3d96cf5a2a8a`
- Row delta: 196
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/reverse_lookup_crosswalk.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 66504 / `cacc1eda4e1ffbfe`
- Row delta: 66504
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/agpeya_passage_index.csv`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 149 / `d5c41027f101cd66`
- Row delta: 149
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/bright_saturday_service_order.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 38 / `2a4f212afdfb0ff4`
- Row delta: 38
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_readings_2020_2035.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 50382 / `71fc13c09ff1b7a0`
- Row delta: 50382
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/source_ref_repair_report.csv`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 19 / `2a888014934fb4fa`
- Row delta: 19
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/GENESIS_PASCHA_CORRECTION_2026-06-06.json`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `0dcd66ffaa98f7e3`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/katameros_cycle_readings.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 4637 / `6e4088187de72566`
- Row delta: 4637
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/bright_saturday_service_order.md`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `47b94e107a651f50`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/source_ref_repair_report.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 19 / `db10babc39d3d0d9`
- Row delta: 19
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/pascha_source_text_index.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 277 / `bb5ac16f6d58df25`
- Row delta: 277
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/pascha_day_hour_index.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 173 / `71027be6bcb35322`
- Row delta: 173
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_occurrences.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 71315 / `268e54888b08f79b`
- Row delta: 71315
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/special_service_readings_curated.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 161 / `c5c08f9beebebd70`
- Row delta: 161
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_index.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 1351 / `18e00db47400d44c`
- Row delta: 1351
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_date_meta_2020_2035.csv`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 5844 / `77f1fd83aaf7679c`
- Row delta: 5844
- Schema changed: True
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/special_service_passage_index.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 196 / `f6d3d2fe7b36b137`
- Row delta: 196
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/agpeya_passage_index.jsonl`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 149 / `a5fce85e6726a88d`
- Row delta: 149
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/data/copticchurch_scrape_errors.json`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 0 / `4f53cda18c2baa0c`
- Row delta: 0
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Days.pdf`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `f4eb3465542af3bf`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/SOURCE_MANIFEST.json`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: 14 / `bc580f848a392c30`
- Row delta: 14
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Sundays.txt`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `bf49a59e64b36668`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/KatamerosDatabase.sqlite`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `19fe28dffc810070`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Days.txt`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `b81d990f48d0923f`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Sundays.pdf`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `798c388ae8be7bf9`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Lent.pdf`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `8cb023ea51ba51bc`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Pentecost.txt`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `a48869f3e26d5e5a`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN_Coptic_AR.txt`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `59de8b5e594e3be9`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `d37ef1df5ff9e5ca`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Pentecost.pdf`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `3e6b0b54155fad46`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/UK_Midlands_Katameros_Lent.txt`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `831e8b37328aa97d`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.pdf`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `afddea9372689625`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`

### `vault:Coptic Orthodox Lectionary Reference/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN_Coptic_AR.pdf`
- Layer: vault-publication-layer
- Before rows/checksum: None / `None`
- After rows/checksum: None / `e7ff308bfc18ecdd`
- Row delta: None
- Schema changed: False
- Added/removed/modified row bodies: not row-enumerable from baseline snapshot; use checksum + row delta + affected passage list above.
- Verification: `python3 build_lectionary_reference.py && python3 verify_lectionary_queries.py > audit_artifacts/final_verify_lectionary_queries_2026-06-06.json`
