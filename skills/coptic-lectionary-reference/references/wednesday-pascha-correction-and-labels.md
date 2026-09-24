# Wednesday Holy Pascha correction and katameros label hygiene

Use this reference when maintaining the maintainer's local Coptic lectionary builder repo (`coptic-orthodox-lectionary-tools`) around Pascha day/hour rows and occurrence labels.

## Durable source layer for Pascha day/hour rows

`out/data/pascha_day_hour_index.*` is the working generated-source copy, but the durable upstream used by `build_lectionary_reference.py` is:

- `out2/pascha_day_hour_index.csv`
- `out2/pascha_day_hour_index.jsonl`

`build_lectionary_reference.py::copy_special_datasets()` copies from `out2` into `out/data` during a full build. Therefore, when correcting Pascha day/hour rows, update both:

1. `out2/pascha_day_hour_index.*` for durability across future full builds.
2. `out/data/pascha_day_hour_index.*` so standalone crosswalk/chapter runs immediately reflect the correction.

For provenance, add a dated correction manifest next to both layers, mirroring the Genesis correction precedent, and copy the manifest plus corrected `pascha_day_hour_index.*` to the downstream documentation package if running only standalone builders. The standalone crosswalk/chapter builders publish downstream crosswalk/chapter outputs, but do not copy the Pascha input CSV/JSONL itself.

## Wednesday Holy Pascha authoritative rows

For Wednesday Holy Pascha, authoritative scripture-only set from the St. Mary Ottawa Pascha book:

- First Hour: Exodus 17:1-7; Proverbs 3:5-14; Hosea 5:13-6:3; Psalm 50:6,32:10; John 11:46-57
- Third Hour: Exodus 13:17-22; Sirach 22:7-18; Psalm 41:6,1; Luke 22:1-6
- Sixth Hour: Exodus 14:13-15:1; Sirach 23:7-14; a Job reading labeled “Memoirs of Job” with no verse in the provided set; Psalm 83:2,5; John 12:1-8
- Ninth Hour: Genesis 24:1-9; Numbers 20:1-13; Proverbs 1:11-35; Psalm 40:6-8; Matthew 26:3-16
- Eleventh Hour: Isaiah 28:16-29; Psalm 6:2-3,68:17; John 12:27-36

Known corrected problem: remove Wednesday Sixth Hour `Isa 48:1-6` from `pascha_day_hour`; replace with `Sir 23:7-14`.

Do not invent references. If the service book gives “Memoirs of Job” without verses, preserve the existing local Job reference and flag it. Current preserved row: `Job 27:16-20; Job 28:1-2` at Wednesday Sixth Hour OT3.

Psalm-numbering flags to report rather than silently overwrite:

- First Hour book `Psalm 50:6,32:10` vs local canonical `Ps 51:4; Ps 33:10`
- Ninth Hour book `Psalm 40:6-8` vs local canonical `Ps 41:5-6`
- Eleventh Hour book `Psalm 68:17` vs local canonical `Ps 69:17`; expand `Ps 6` to `Ps 6:2-3` when correcting this row

## Label hygiene

Katameros occurrence label mapping in `build_bible_chapter_lectionary_index.py` should align the `liturgy_catholic` slot with date/Bright Saturday wording:

- `liturgy_catholic -> service_label "Liturgy", reading_label "Catholic Epistle"`

Avoid emitting `Catholicon` in generated display-label columns (`occasion_label`, `service_label`, `reading_label`). Keep `Pauline`, `Psalm`, `Gospel`, and `Praxis` as already mapped.

## Verification assertions to keep

Extend/run `verify_lectionary_queries.py` for this class of change. Useful assertions:

- `bible_chapter_lectionary_occurrences.csv` contains `occasion_label`, `service_label`, `reading_label`.
- No generated display label contains `Catholicon`.
- At least one `katameros_cycle` `liturgy_catholic` row has `service_label == "Liturgy"` and `reading_label == "Catholic Epistle"`.
- No Wednesday `pascha_day_hour` crosswalk row has passage `Isa 48:1-6`.
- Wednesday Sixth Hour includes `Sir 23:7-14`.
- Wednesday corrected rows preserve/cover expected split crosswalk passages, including split Job segments `Job 27:16-20` and `Job 28:1-2`.

Standard command sequence for this narrow builder-only path:

```bash
python3 build_lectionary_crosswalk.py
python3 build_bible_chapter_lectionary_index.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py
git diff --check
```

Do not run `build_lectionary_reference.py` unless explicitly asked for a full build/scrape/package refresh. `BUILD_SUMMARY.json` may be stale after standalone builds; report that clearly.
