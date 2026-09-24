# Local lectionary data stack

Use this when working on the maintainer's local Coptic Orthodox lectionary package.

## Core local datasets
- `katameros_cycle_readings.csv` and `katameros_cycle_passage_index.csv`
- `copticchurch_date_readings_2020_2035.csv` and `copticchurch_passage_index_2020_2035.csv`
- `reverse_lookup_crosswalk.csv` and `reverse_lookup_summary.csv`
- `pascha_day_hour_index.csv`
- `bright_saturday_service_order.csv`

## Query behavior now expected
- Full names and abbreviations should normalize together, e.g. `John 20` / `Jn 20`, `Psalm 51` / `Ps 51`, `Isaiah 53` / `Isa 53`.
- Ordinary calendar passage lookup should search the date-resolved passage index first, then fall back to the reverse crosswalk.
- Pascha / Holy Week lookup should be source-text-first: check extracted Holy Pascha source text and direct day/hour rows before relying on reverse crosswalk or generated chapter indexes.
- Pascha / Holy Week should be queryable directly by day and hour, not only by generic passage search.
- Treat `bible_chapter_lectionary_index.*` as downstream verification output for Pascha, not as the controlling source. If it disagrees with source text or day/hour rows, repair the upstream Pascha data and regenerate.
- For final verification in `$REPO_ROOT`, prefer the packaged helper `python3 out/scripts/query_lectionary.py ...` from the repo root. If a source-tree helper resolves data outside `$REPO_ROOT/out/data` and fails, rerun with the packaged helper before drawing any content conclusion.

## High-value validation cases
- `--date 2032-04-07`
- `--date 2029-03-21`
- `--passage "John 20"`
- `--passage "Psalm 51"`
- `--passage "Isaiah 53"`
- `--cycle-passage "John 20:1-18"`
- `--cycle-passage "40.5"`
- `--pascha-day "Good Friday" --hour "Sixth Hour"`
- `--pascha-day "Great Thursday" --hour "Eleventh Hour"`
- `--pascha-day "Bright Saturday"`

## Interpretation rules
- If a passage is absent from the ordinary date index and cycle index, check Pascha / Bright Saturday data before calling it missing.
- `Isaiah 53` is a known example: it resolves through Good Friday Sixth Hour, not through the ordinary annual package.
- A cycle-only fallback result without a Gregorian date is acceptable if it comes from the reverse crosswalk.

## Remaining hard gap
The unresolved problem is exact page-level extraction for sacramental and special-service reading tables such as Baptism, Crowning, Unction, Funeral Prayer, Home Blessing, Liturgy of the Waters, Prostrations, Cornerstone, Myron Consecration, and consecration services. Do not mark those as final unless backed by an explicit table or service-book page.