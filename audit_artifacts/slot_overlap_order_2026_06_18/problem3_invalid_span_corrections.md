# Problem 3 Invalid Span Corrections

All seven requested invalid-span cases are **sourced**, not inferred. No unconfirmable Problem 3 items remain open.

| Case | Raw in repo | Corrected to | Basis | Source / pipeline location |
|---|---|---|---|---|
| Acts 34:42 | Mesra 29 | `Acts 5:34:42` | `Acts 5:34-42` | sourced | Katameros API api.katameros.app, queried 2026-06-18; repair note says live API returned Acts 5:34-42; build_lectionary_reference.py COPTICCHURCH_SOURCE_CORRECTIONS; source_ref_repair_report.csv rows for Mesra 29 |
| Mark 19:9-13 | Abib 21 | `Mk 19:9-13` | `Mark 13:9-13` | sourced | Katameros API api.katameros.app, queried 2026-06-18; repair note says live API returned Mark 13:9-13; build_lectionary_reference.py COPTICCHURCH_SOURCE_CORRECTIONS; source_ref_repair_report.csv rows for Abib 21 |
| Ps 610:5 | Saturday of the fourth week of Great Lent | `Psalm 61:1  &  Psalm 610:5` | `Psalm 61:1,5` | sourced | Katameros API api.katameros.app, queried 2026-06-18; repair note says live API returned Ps 61:1,5; build_lectionary_reference.py COPTICCHURCH_SOURCE_CORRECTIONS; source_ref_repair_report.csv rows for Saturday of the fourth week of Great Lent |
| Rom 28:39 | Mesra 23 | `Rom 8:28:39` | `Rom 8:28-39` | sourced | Katameros API api.katameros.app, queried 2026-06-18; repair note says live API returned Rom 8:28-39; build_lectionary_reference.py COPTICCHURCH_SOURCE_CORRECTIONS; source_ref_repair_report.csv rows for Mesra 23 |
| Rom 28:39 | Mesra 27 | `Rom 8:28:39` | `Rom 8:28-39` | sourced | Katameros API api.katameros.app, queried 2026-06-18; repair note says live API returned Rom 8:28-39; build_lectionary_reference.py COPTICCHURCH_SOURCE_CORRECTIONS; source_ref_repair_report.csv rows for Mesra 27 |
| Wis 24:1-11 | Great Thursday | `Wis 24:1-11` | `Sir 24:1-11` | sourced | Katameros API api.katameros.app Great Thursday Third Hour, saved in audit_artifacts/slot_overlap_order_2026_06_18/raw/great_thursday_2026_katameros.json; extracted CSV shows Sirach 24:1-11; build_lectionary_crosswalk.py PASCHA_CURATED_REF_CORRECTIONS |
| Acts 18:24-9:6 | Mesra 25 | `Acts 18:24—  &  Acts 9:1-6` | `Acts 18:24-28; Acts 19:1-6` | sourced | Katameros API api.katameros.app, queried 2026-06-18; repair note says live API returned Acts 18:24-28 and Acts 19:1-6; build_lectionary_reference.py COPTICCHURCH_SOURCE_CORRECTIONS; source_ref_repair_report.csv rows for Mesra 25 |

## Validation

- `source_ref_repair_report.csv` rows: 104
- Normalized bad-hit count in `reverse_lookup_crosswalk.csv`: 0
- New verifier guard: `problem3_invalid_span_repairs` in `verify_lectionary_queries.py`.
