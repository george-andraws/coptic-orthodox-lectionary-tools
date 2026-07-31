# Coptic Lectionary Research Runbook

Operational notes for rebuilding, validating, querying, and maintaining George's local Coptic Orthodox lectionary reference package.

## Project location

```bash
cd "$HOME/workspace/coptic-lectionary-research"
```

## What this package contains

Main generated package:

- `out/data/` - generated CSV/JSONL data files
- `out/scripts/query_lectionary.py` - generated query helper copied from tracked `query_lectionary.py`
- `out/scripts/passage_normalization.py` - generated copy of tracked `passage_normalization.py`
- Obsidian-published copies under George's lectionary reference folder

Primary data families:

- Katameros cycle data from the local SQLite source
- Date-resolved readings from copticchurch.net cache/scrape, 2020-2035
- Pascha day/hour data
- Bright Saturday service order
- Special-service readings
- Agpeya hour/watch readings
- Reverse passage crosswalk

Synaxarium is separate. See [Synaxarium](#synaxarium).

## Standard full rebuild

Run this from the project root:

```bash
python3 build_lectionary_reference.py
```

This rebuilds the main package and runs verification as part of the build.

Expected outputs include:

- `out/BUILD_SUMMARY.json`
- `out/data/katameros_cycle_readings.csv`
- `out/data/katameros_cycle_passage_index.csv`
- `out/data/copticchurch_date_readings_2020_2035.csv`
- `out/data/copticchurch_passage_index_2020_2035.csv`
- `out/data/special_service_readings_curated.csv`
- `out/data/special_service_passage_index.csv`
- `out/data/agpeya_hour_readings.csv`
- `out/data/agpeya_passage_index.csv`
- `out/data/reverse_lookup_crosswalk.csv`
- `out/data/reverse_lookup_summary.csv`
- `out/data/bible_chapter_lectionary_index.csv`
- `out/data/bible_chapter_lectionary_occurrences.csv`
- `out/data/source_ref_repair_report.csv`
- `out/scripts/query_lectionary.py`
- `out/scripts/passage_normalization.py`

## Verification

Run the explicit verifier after any meaningful code or data change:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py
```

The verifier checks:

- required artifacts exist
- known-good lookups work
- false positives stay fixed, especially:
  - `John 2` must not match `John 20`, `John 21`, or `1Jn 2`
  - `Isa 5` must not match `Isa 50`, `Isa 52`, `Isa 53`, or `Isa 58`
- parser edge cases behave intentionally
- malformed raw refs are accounted for
- generated helper copies do not drift from source

## Recommended sanity checks

After a rebuild, run:

```bash
cmp -s passage_normalization.py out/scripts/passage_normalization.py
cmp -s query_lectionary.py out/scripts/query_lectionary.py

test -f out/data/reverse_lookup_crosswalk.csv
test -f out/data/pascha_day_hour_index.csv
test -f out/data/bright_saturday_service_order.csv
test -f out/data/source_ref_repair_report.csv
test -f out/scripts/query_lectionary.py
```

Suspicious-ref scan:

```bash
rg -n ':-|--|[0-9]+:[0-9]+\s*[-–—]\s*$' out/data/*.csv
```

Expected result:

- matches may appear in raw source fields and in `source_ref_repair_report.csv`
- normalized refs and `reverse_lookup_crosswalk.csv` should remain clean
- `verify_lectionary_queries.py` is the authority on whether these defects are properly accounted for

## Query examples

Use the generated helper:

```bash
python3 out/scripts/query_lectionary.py --help
```

Date-resolved readings:

```bash
python3 out/scripts/query_lectionary.py --date 2032-04-07
```

Passage lookup:

```bash
python3 out/scripts/query_lectionary.py --passage "John 2"
python3 out/scripts/query_lectionary.py --passage "Isaiah 53"
```

Passage lookup with reverse crosswalk:

```bash
python3 out/scripts/query_lectionary.py --passage "John 2" --include-crosswalk --limit 10
```

With `--include-crosswalk`, output is split into:

- `## date results`
- `## reverse crosswalk results`

This prevents cycle, Pascha, Agpeya, and special-service hits from being hidden behind many date rows.

Katameros cycle lookup:

```bash
python3 out/scripts/query_lectionary.py --cycle-passage "Matt 5:1"
python3 out/scripts/query_lectionary.py --cycle-passage "40.5"
```

Pascha lookup:

```bash
python3 out/scripts/query_lectionary.py --pascha-day "Good Friday" --hour "Sixth Hour"
python3 out/scripts/query_lectionary.py --pascha-day "Great Thursday" --hour "Eleventh Hour"
```

Special-service lookup:

```bash
python3 out/scripts/query_lectionary.py --special-service "palm sunday procession"
python3 out/scripts/query_lectionary.py --special-service "palm sunday liturgy"
python3 out/scripts/query_lectionary.py --special-service "general funeral"
```

Chapter-level lookup:

```bash
python3 out/scripts/query_lectionary.py --chapter "John 2"
python3 out/scripts/query_lectionary.py --chapter "Genesis 1"
```

The aggregate chapter table is `out/data/bible_chapter_lectionary_index.csv`; the detailed occurrence table is `out/data/bible_chapter_lectionary_occurrences.csv`. The aggregate includes unread chapters with `is_read=no`.

Agpeya lookup:

```bash
python3 out/scripts/query_lectionary.py --agpeya "first hour"
python3 out/scripts/query_lectionary.py --agpeya "veil"
python3 out/scripts/query_lectionary.py --passage "John 14:26-15:4" --include-crosswalk --limit 50
```

## Malformed source refs

Some copticchurch.net rows contain malformed raw refs, for example:

- `Mk 14:-3-9`
- `Mk 14:-39`

Policy:

- direct parsing rejects malformed forms
- known source defects are repaired for indexing
- every repair is explicit and reported

Generated repair files:

- `out/data/source_ref_repair_report.csv`
- `out/data/source_ref_repair_report.jsonl`

Relevant fields:

- `source_ref_status`
- `parse_status`
- `normalization_warning`
- `raw_ref`
- `repaired_ref`

Current expected repair count after the last validation pass: **19 rows**.

Do not delete raw malformed refs from source fields unless the source data itself is corrected. The raw values are evidence. The repair report is the audit trail.

## Parser rules worth preserving

The verifier asserts these behaviors:

```python
passage_matches("John 2", "Jn 20:1-18") is False
passage_matches("John 2", "1Jn 2:1-6") is False
passage_matches("Isa 5", "Isa 58:1-11") is False
passage_matches("Isa 53", "Isa 52:13-53:12") is True
parse_passage("John 3:16--18") is None
parse_passage("Mk 14:-39") is None
parse_passage("John 19:1-") is None
extract_text_ref_tokens("John 19:1- John 19:16") == ["Jn 19:1-16"]
extract_text_ref_tokens("Mk 14:-39") == ["Mark 14:39"]
```

The distinction is intentional:

- direct parser should be strict
- extraction can repair known source glitches while emitting/reporting metadata at the build layer

## Build inputs and reproducibility

The main build is repo-relative.

Pascha and Bright Saturday artifacts are treated as required package inputs. The builder prefers canonical copies in `out/data/` and falls back to legacy side-output directories when needed:

- `out2/`
- `out_bright/`

If these artifacts are missing, restore or regenerate them before running the full package build.

Required artifacts checked by the verifier include:

- `out/data/pascha_day_hour_index.csv`
- `out/data/bright_saturday_service_order.csv`

## Query helper maintenance

Tracked source files:

- `query_lectionary.py`
- `passage_normalization.py`

Generated copies:

- `out/scripts/query_lectionary.py`
- `out/scripts/passage_normalization.py`

Do not edit generated copies directly. Edit the tracked source, then rebuild.

Check drift with:

```bash
cmp -s query_lectionary.py out/scripts/query_lectionary.py
cmp -s passage_normalization.py out/scripts/passage_normalization.py
```

## Synaxarium

`build_synaxarium_index.py` is intentionally separate from the main lectionary package.

Run it only when you want the St-Takla Synaxarium source map:

```bash
python3 build_synaxarium_index.py
```

Output:

- `out_synaxarium/`

It is not currently included in:

- `out/BUILD_SUMMARY.json`
- `query_lectionary.py`
- the main verifier

Reason: Synaxarium is a related text/source-map corpus, not a reading-table dataset. Integrating it into queries is a future enhancement, not part of the current finalized lectionary package.

## When adding new lectionary data

1. Use explicit source-backed rows only.
2. Preserve raw source references.
3. Add normalized/canonical refs for lookup.
4. Add source status/warning metadata if any repair is needed.
5. Rebuild:

```bash
python3 build_lectionary_reference.py
```

6. Verify:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py
```

7. Run drift checks.
8. Update Obsidian notes if the change affects the reference state.

## Last known good validation snapshot

From the latest completed pass:

- `source_ref_repair_report.csv`: 19 rows
- `copticchurch_date_readings_2020_2035.csv`: 50,382 rows
- `copticchurch_passage_index_2020_2035.csv`: 59,340 rows
- `reverse_lookup_crosswalk.csv`: 66,208 rows
- `bible_chapter_lectionary_index.csv`: generated one row per supported Bible chapter
- `bible_chapter_lectionary_occurrences.csv`: generated detailed chapter occurrence rows
- date scrape errors: 0
- generated helper drift checks: passed
