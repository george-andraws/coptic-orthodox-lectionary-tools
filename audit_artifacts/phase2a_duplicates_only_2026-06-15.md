# Phase 2a Duplicate Fix Report — Duplicates Only

- Date: 2026-06-15
- Scope approved: **duplicates only**
- Explicitly out of scope: Pascha / Holy Week data corrections and `pascha_source_text_index.*`
- Dataset mutation in this phase: Katameros duplicate removal, numeric-segment duplicate suppression, generated dependent indexes rebuilt
- No Coptic Reader comparator pipeline built

## 1. Pre-change duplicate inventory

Before any change, the duplicate count was confirmed as **14 duplicate groups**:

- **13 Great Lent duplicate groups** from the same SQLite source-row pair:
  - `GreatLentReadings.Id=46`, `Week=7`, `DayOfWeek=4`
  - `GreatLentReadings.Id=53`, `Week=7`, `DayOfWeek=4`
- **1 Hatur 8 segmentation group** from raw Psalm encoding `19.68:17,16,17`, which emitted `Ps 68:17` twice.

### Full Great Lent source rows before change

The same two source rows were responsible for all 13 Great Lent duplicate groups. Full row contents were printed before editing:

```json
{
  "Id": 46,
  "Week": 7,
  "DayOfWeek": 4,
  "DayName": null,
  "Seasonal_Tune": "Lenten Tune ",
  "Weather_Prayers": "Winds of Heaven",
  "V_Psalm_Ref": null,
  "V_Gospel_Ref": null,
  "M_Psalm_Ref": "19.63:1-1",
  "M_Gospel_Ref": "40.20:20-28",
  "P_Gospel_Ref": "47.4:5-18",
  "C_Gospel_Ref": "62.3:13-24",
  "X_Gospel_Ref": "44.25:23-27*@+44.26:1-6",
  "L_Psalm_Ref": "19.122:1-2",
  "L_Gospel_Ref": "41.12:18-27",
  "Prophecy": "20.11:13-26@23.65:8-16@18.42:1-6@12.6:8-33*@+12.7:1-20"
}
```

```json
{
  "Id": 53,
  "Week": 7,
  "DayOfWeek": 4,
  "DayName": null,
  "Seasonal_Tune": "Lenten Tune ",
  "Weather_Prayers": "Winds of Heaven",
  "V_Psalm_Ref": null,
  "V_Gospel_Ref": null,
  "M_Psalm_Ref": "19.63:1-1*@+19.64:2-4",
  "M_Gospel_Ref": "40.20:20-28",
  "P_Gospel_Ref": "47.4:5-18",
  "C_Gospel_Ref": "62.3:13-24",
  "X_Gospel_Ref": "44.25:23-27*@+44.26:1-6",
  "L_Psalm_Ref": "19.122:1-2",
  "L_Gospel_Ref": "41.12:18-27",
  "Prophecy": "20.11:13-26@23.65:8-16@18.42:1-6@12.6:8-33*@+12.7:1-20"
}
```

The only non-primary-key content difference was:

| Field | `Id=46` | `Id=53` |
|---|---|---|
| `M_Psalm_Ref` | `19.63:1-1` | `19.63:1-1*@+19.64:2-4` |

This was **not** treated as a silent pure duplicate. It was flagged and resolved using the independent date-resolved cache: every 2020-2035 occurrence of `Thursday of the seventh week of Great Lent` has Matins Psalm `Psalm 63:1`, matching `Id=46`, not the extra `Ps 64:2-4` in `Id=53`.

### The 13 Great Lent duplicate groups

For every group below, the canonical source row kept was `GreatLentReadings.Id=46`; the redundant source row dropped was `GreatLentReadings.Id=53`.

| # | Day | Slot | Duplicate passage | Kept | Dropped |
|---:|---|---|---|---:|---:|
| 1 | `week 7 day_of_week 4` | `matins_psalm` | `Ps 63:1` | 46 | 53 |
| 2 | `week 7 day_of_week 4` | `matins_gospel` | `Matt 20:20-28` | 46 | 53 |
| 3 | `week 7 day_of_week 4` | `liturgy_pauline` | `2Cor 4:5-18` | 46 | 53 |
| 4 | `week 7 day_of_week 4` | `liturgy_catholic` | `1Jn 3:13-24` | 46 | 53 |
| 5 | `week 7 day_of_week 4` | `liturgy_acts` | `Acts 25:23-27` | 46 | 53 |
| 6 | `week 7 day_of_week 4` | `liturgy_acts` | `Acts 26:1-6` | 46 | 53 |
| 7 | `week 7 day_of_week 4` | `liturgy_psalm` | `Ps 122:1-2` | 46 | 53 |
| 8 | `week 7 day_of_week 4` | `liturgy_gospel` | `Mark 12:18-27` | 46 | 53 |
| 9 | `week 7 day_of_week 4` | `prophecy` | `Prov 11:13-26` | 46 | 53 |
| 10 | `week 7 day_of_week 4` | `prophecy` | `Isa 65:8-16` | 46 | 53 |
| 11 | `week 7 day_of_week 4` | `prophecy` | `Job 42:1-6` | 46 | 53 |
| 12 | `week 7 day_of_week 4` | `prophecy` | `2Kgs 6:8-33` | 46 | 53 |
| 13 | `week 7 day_of_week 4` | `prophecy` | `2Kgs 7:1-20` | 46 | 53 |

### Hatur 8 before change

Source row:

```text
AnnualReadings | Hatur 8 | vespers_psalm | raw_ref=19.68:17,16,17 | normalized_ref=Ps 68:17,16,17
```

Pre-change emitted segments:

```text
Ps 68:17
Ps 68:16
Ps 68:17
```

Flag: `17,16,17` is out of order and repeats verse 17. I did **not** silently assume the source intended a different ordered verse list. I only prevented duplicate emission of the repeated verse.

## 2. Changes made

### Great Lent data-layer dedupe

Removed redundant source row from both SQLite copies:

| DB | Kept | Dropped | Integrity |
|---|---:|---:|---|
| `sources/katameros-api/Core/KatamerosDatabase.db` | 46 | 53 | `ok` |
| `out/sources/KatamerosDatabase.sqlite` | 46 | 53 | `ok` |

Post-change DB facts:

- `GreatLentReadings.Id=46`: present
- `GreatLentReadings.Id=53`: absent
- `GreatLentReadings` row count: 52
- duplicate `(Week, DayOfWeek)` groups in `GreatLentReadings`: 0

### Hatur 8 segmentation fix

Updated `passage_normalization.iter_numeric_ref_segments()` to skip a repeated numeric segment while preserving first-seen source order.

Post-change Hatur 8 output:

```text
Ps 68:17
Ps 68:16
```

The raw source value remains flagged for review:

```text
19.68:17,16,17
```

### Rebuilt dependent artifacts

Targeted rebuild only, not a full Pascha/Holy Week correction pass:

- `katameros_cycle_readings.csv/jsonl`
- `katameros_cycle_passage_index.csv/jsonl`
- `reverse_lookup_crosswalk.csv/jsonl`
- `reverse_lookup_summary.csv`
- `bible_chapter_lectionary_index.csv/jsonl`
- `bible_chapter_lectionary_occurrences.csv/jsonl`
- matching `out4/reverse_lookup_*` builder side outputs
- `out/scripts/passage_normalization.py` synced with source

Current generated counts:

| Artifact | Count |
|---|---:|
| `katameros_cycle_readings.csv` rows | 4,629 |
| `katameros_cycle_passage_index.csv` rows | 6,209 |
| `reverse_lookup_crosswalk.csv` rows | 66,352 |
| `bible_chapter_lectionary_occurrences.csv` rows | 71,113 |

## 3. New uniqueness guard

Added verifier checks in `verify_lectionary_queries.py`:

- `assert_no_duplicate_reading_tuples()`
  - checks `reverse_lookup_crosswalk.csv`
  - checks `katameros_cycle_passage_index.csv`
  - enforces duplicate-free day/service/slot/reading natural keys, using Gregorian date for date-resolved rows because those intentionally recur across years
- `assert_hatur8_segmentation_deduped()`
  - asserts raw `19.68:17,16,17` emits exactly `Ps 68:17`, `Ps 68:16`
  - keeps the source-warning text in the verifier output

Guard result from `PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py`:

```json
{
  "duplicate_reading_tuple_guard": {
    "reverse_lookup_rows_checked": 66352,
    "katameros_cycle_passage_rows_checked": 6209,
    "duplicate_reading_tuples": 0
  },
  "hatur8_segmentation_deduped": {
    "raw_ref": "19.68:17,16,17",
    "emitted_segments": ["Ps 68:17", "Ps 68:16"],
    "raw_ref_warning": "source repeats verse 17 and lists verses out of order; verifier only dedupes emission"
  }
}
```

## 4. Verification results by check

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py
```

Exit code: 0

| Verifier check | Result |
|---|---|
| `artifacts` | PASS |
| `false_positive_checks` | PASS |
| `required_pascha_genesis_rows` | PASS |
| `known_good_checks` | PASS |
| `parser_edge_cases` | PASS |
| `pascha_source_text_fully_parsed` | PASS |
| `four_maccabees_local_absence` | PASS |
| `malformed_ref_checks` | PASS |
| `duplicate_reading_tuple_guard` | PASS |
| `hatur8_segmentation_deduped` | PASS |
| `chapter_occurrence_label_columns` | PASS |
| `chapter_occurrence_row_count` | PASS (`71,113`) |
| `pascha_source_text_dedupe_invariants` | PASS |
| `wednesday_pascha_day_hour_corrections` | PASS |

Additional duplicate verification:

| Check | Result |
|---|---|
| Post-change Katameros duplicate groups in reverse crosswalk | 0 |
| Post-change excess Katameros duplicate rows | 0 |
| Post-change Hatur 8 raw `19.68:17,16,17` segment rows | 2 (`Ps 68:17`, `Ps 68:16`) |
| Source DB `pragma integrity_check` | `ok` |
| Packaged DB `pragma integrity_check` | `ok` |

## 5. Pascha/Holy Week non-modification check

No Pascha/Holy Week/source-text input files were modified in this phase.

Files matching `pascha`, `holy`, or `source_text_index` in the current git diff:

```text
(none)
```

Full current unstaged/staged diff path list at report-writing time:

```text
M	out/data/bible_chapter_lectionary_index.csv
M	out/data/bible_chapter_lectionary_index.jsonl
M	out/data/bible_chapter_lectionary_occurrences.csv
M	out/data/bible_chapter_lectionary_occurrences.jsonl
M	out/data/katameros_cycle_passage_index.csv
M	out/data/katameros_cycle_passage_index.jsonl
M	out/data/katameros_cycle_readings.csv
M	out/data/katameros_cycle_readings.jsonl
M	out/data/reverse_lookup_crosswalk.csv
M	out/data/reverse_lookup_crosswalk.jsonl
M	out/data/reverse_lookup_summary.csv
M	out/scripts/passage_normalization.py
M	out/sources/KatamerosDatabase.sqlite
M	out4/reverse_lookup_crosswalk.csv
M	out4/reverse_lookup_crosswalk.jsonl
M	out4/reverse_lookup_summary.csv
M	passage_normalization.py
M	sources/katameros-api/Core/KatamerosDatabase.db
M	verify_lectionary_queries.py
```

## 6. Summary

- Rows removed: **1 SQLite source row from each SQLite copy**
  - kept `GreatLentReadings.Id=46`
  - dropped `GreatLentReadings.Id=53`
- Duplicate groups fixed:
  - 13 Great Lent duplicate groups removed at the data layer
  - 1 Hatur 8 segmentation duplicate fixed in the parser/index generation layer
- Hatur 8 before/after:
  - before: `Ps 68:17`, `Ps 68:16`, `Ps 68:17`
  - after: `Ps 68:17`, `Ps 68:16`
  - raw value remains flagged: `19.68:17,16,17`
- New guard: verifier now fails if duplicate reading tuples recur in the generated reverse/cycle indexes.
- Pascha/Holy Week rows and source-text index inputs: **not modified**.
