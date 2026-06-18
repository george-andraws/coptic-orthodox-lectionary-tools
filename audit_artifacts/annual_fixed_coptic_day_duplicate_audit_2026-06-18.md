# Annual fixed Coptic day duplicate audit

Generated before the 1.1.1 cleanup to prove every exposed `annual fixed Coptic day` reverse-index row had concrete fixed Coptic day rows in the presentation layer.

- old package reverse-index rows with `occasion=annual fixed Coptic day`: 606
- rows with at least one concrete duplicate/source row: 606
- rows missing concrete duplicate/source rows: 0
- concrete presentation rows represented by those old aggregates: 4526
- unique fixed Coptic days represented: 366

## Source of confusion

`build_lectionary_crosswalk.py` used the Katameros `source_type` field as `liturgical_place`. For AnnualReadings fixed Coptic days, `source_type` is the generic label `annual fixed Coptic day`, while the same source row already carries the specific day in `day_name` / `day_key`.

## Fix direction

For `source_type=annual fixed Coptic day`, use `day_name` / `day_key` as the row `liturgical_place` so downstream `occasion` values become the specific Coptic date. Keep the generic source type only as source context, not as the public occasion.

Row-level audit: `audit_artifacts/annual_fixed_coptic_day_duplicate_audit_2026-06-18.csv`
