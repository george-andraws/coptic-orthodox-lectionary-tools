# Katameros duplicate dedupe and uniqueness guard

Use this reference when the requester asks to fix duplicate reverse-lookup results in the Coptic lectionary builder while explicitly excluding Pascha/Holy Week work.

## Scope rule

If the user says duplicates only, do not edit Pascha / Holy Week inputs or `pascha_source_text_index.*`. It is acceptable to rebuild downstream aggregate artifacts such as reverse crosswalks and chapter occurrence indexes when they depend on the duplicate fix, but verify no diff paths match `pascha`, `holy`, or `source_text_index` before committing.

## Durable duplicate case

Phase 2a duplicate fix on 2026-06-15 found 14 duplicate groups:

- 13 Great Lent groups from one SQLite source-row pair:
  - `GreatLentReadings.Id=46`, `Week=7`, `DayOfWeek=4`
  - `GreatLentReadings.Id=53`, `Week=7`, `DayOfWeek=4`
- 1 Hatur 8 segmentation group from raw Psalm encoding `19.68:17,16,17` emitting `Ps 68:17` twice.

## Great Lent dedupe pattern

Before deleting, print full source rows with primary keys and confirm the exact duplicate group count. The Great Lent pair was not byte-identical:

- `Id=46` `M_Psalm_Ref`: `19.63:1-1`
- `Id=53` `M_Psalm_Ref`: `19.63:1-1*@+19.64:2-4`

Do not silently call this a pure duplicate. Use independent evidence before deciding which row to keep. In this case, the date-resolved cache for every 2020-2035 occurrence of `Thursday of the seventh week of Great Lent` had Matins Psalm `Psalm 63:1`, so keep `Id=46` and drop `Id=53`.

Apply the deletion to both SQLite copies:

```text
sources/katameros-api/Core/KatamerosDatabase.db
out/sources/KatamerosDatabase.sqlite
```

Verify after edit:

```sql
pragma integrity_check;
select count(*) from GreatLentReadings where Id=46;
select count(*) from GreatLentReadings where Id=53;
select Week, DayOfWeek, count(*) from GreatLentReadings group by Week, DayOfWeek having count(*) > 1;
```

Expected post-fix facts:

- `Id=46`: present
- `Id=53`: absent
- `GreatLentReadings` row count: 52
- duplicate `(Week, DayOfWeek)` groups: 0

## Hatur 8 repeated-segment pattern

Raw value:

```text
19.68:17,16,17
```

This is out of order and repeats verse 17. Do not infer the intended corrected raw source. Fix only the segmentation emission by skipping repeated numeric segments while preserving first-seen order.

Expected emitted segments after fix:

```text
Ps 68:17
Ps 68:16
```

Keep the raw value flagged in the report/verifier output.

## Rebuild pattern

For a duplicate-only targeted rebuild:

1. Export Katameros cycle rows from the SQLite source DB.
2. Rebuild:
   - `out/data/katameros_cycle_readings.csv/jsonl`
   - `out/data/katameros_cycle_passage_index.csv/jsonl`
3. Sync `passage_normalization.py` to `out/scripts/passage_normalization.py`.
4. Run `build_lectionary_crosswalk.py` with `LECTIONARY_DISABLE_VAULT_PUBLISH=1`.
5. Run `build_bible_chapter_lectionary_index.py` with `LECTIONARY_DISABLE_VAULT_PUBLISH=1`.

`build_lectionary_crosswalk.py` writes primary outputs to `out4/` and copies them to `out/data/`; keep both in sync if they are tracked.

Known post-fix counts from the duplicate-only pass:

| Artifact | Count |
|---|---:|
| `katameros_cycle_readings.csv` rows | 4,629 |
| `katameros_cycle_passage_index.csv` rows | 6,209 |
| `reverse_lookup_crosswalk.csv` rows | 66,352 |
| `bible_chapter_lectionary_occurrences.csv` rows | 71,113 |

## Verifier guard to preserve

`verify_lectionary_queries.py` should include duplicate guards:

- `assert_no_duplicate_reading_tuples()` checks generated reverse/cycle indexes for duplicate day/service/slot/reading natural keys.
- `assert_hatur8_segmentation_deduped()` asserts raw `19.68:17,16,17` emits `Ps 68:17`, `Ps 68:16` and carries a warning that the raw source repeats/out-of-orders the verse list.

Verification command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py
```

Report pass/fail per verifier check, not a blanket pass.

## Commit/report hygiene

Write a Phase 2a report under `audit_artifacts/` with:

- pre-change duplicate count and full source-row enumeration
- kept/dropped IDs and why
- Hatur 8 before/after plus raw source warning
- generated row counts
- verifier results per check
- explicit confirmation that no Pascha/Holy/source-text files were modified

Before commit:

```bash
git diff --name-only | grep -Ei 'pascha|holy|source_text_index' || true
git diff --check
git diff --cached --name-only | grep -Ei 'pascha|holy|source_text_index' || true
git diff --cached --check
```
