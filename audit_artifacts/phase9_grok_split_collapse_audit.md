# Grok Audit: Split Lectionary Disclosure Collapse

Verdict: PASS

## Checks
- PASS: Source disclosure collapse.
- PASS: Handoff and specs.
- PASS: Manifest.
- PASS: Safety.

## Evidence
- `/tmp/lectionary_split_audit_packet.json`
  - `index_rows`: 8,005.
  - `source_disclosure_count_distribution`: `{"1": 8005}`.
  - `source_count_mismatch_count`: 0.
  - `retired_monolith_exists`: false.
  - `affected_passages_count`: 2,791.
  - `manifest_has_materialization_note`: true.
  - `manifest_has_collapsed_note`: true.
  - `manifest_cross_check_clean`: true.
- `out/design/reverse_lectionary_index.jsonl`
  - File has 8,005 lines.
  - Rows include `attestation_year_min`, `attestation_year_max`, `attestation_years`, and `collapsed_row_count`.
  - Sample rows show `source_disclosure_count`, collapsed `source_disclosure`, and no `gregorian_date` or `coptic_date`.
- `out/handoff/reverse_lectionary_index.jsonl`
  - File has 8,005 lines.
  - Handoff copy matches the intended split artifact shape.
- `build_design_deliverables.py`
  - Lines 918 to 924 define `source_disclosure_key` as `(source_family, source_kind, source_edition, source_title)`.
  - Lines 927 to 953 group by that key, keep one representative `source_locator`, and attach attested year metadata.
  - Lines 996 to 1062 build one reverse index row per `(occasion, service_section, service_hour, slot, identity_key)`, enforce key equality, and enforce 8,005 rows.
  - Lines 1046 to 1051 write `source_disclosure_count`, `source_disclosure`, `attestation_year_min`, `attestation_year_max`, `attestation_years`, and `collapsed_row_count`.
- `verify_design_deliverables.py`
  - Lines 302 to 318 verify reverse index row count, uniqueness, and exact key-set equality against the presentation rows.
  - Lines 340 to 354 verify representative locator handling, collapsed source disclosure equality, `source_disclosure_count`, distinct-source count preservation, and no repeated same-source locators.
  - Lines 357 to 386 verify daily files are derived only from dated presentation rows and match the daily schema.
- `out/design/lectionary_schema.json`
  - Lines 1587 to 1616 define `reverse_lectionary_index` with the collapsed disclosure and row-level attestation fields.
  - Lines 1618 to 1626 define the `daily_lectionary_year` table.
- `site_integration_spec.md`
  - Lines 48 to 60 describe `reverse_lectionary_index.jsonl` as the year-independent reverse lectionary layer.
  - Lines 62 to 74 describe Today's Readings using `daily/lectionary-YYYY.json`, the shipped window, and the limitation that Bright Saturday and special services without `gregorian_date` are not in daily files yet.
- `out/handoff/site_integration_spec.md`
  - Lines 21 to 34 describe the two-layer model and `reverse_lectionary_index.jsonl`.
  - Lines 45 to 64 describe Today's Readings using daily JSON files, shipped files for 2026 to 2028, and the same date-coverage limitation.
- `out/handoff/HANDOFF.md`
  - Lines 17 to 20 list `reverse_lectionary_index.jsonl` plus daily files for 2026, 2027, and 2028.
  - Lines 41 to 44 state the retired monolith is not present in the working tree and the full daily set is archive only.
  - Lines 69 to 70 state Today's Readings uses daily files and structural-only occasions remain outside daily files for now.
- `out/design/lectionary_change_manifest.md`
  - Lines 10 to 15 record the split and disclosure collapse as a materialization reshape, with no reading content change and no new affected passages.
  - Lines 6 to 8 report 32,941 grouped manifest rows, 427,942 raw row-level CSV changes, and 2,791 affected passage keys.
  - Lines 2883 onward include the execution-log cross-check section.
- `scripts/build_lectionary_change_manifest.py`
  - Lines 489 to 494 generate the materialization reshape note.
  - Lines 511 to 525 generate the execution-log cross-check and clean message when no data-diff commits are missing from the log.
- `out/design/affected_passages.csv`
  - File has 2,792 lines including header, so 2,791 affected passages, matching the packet and manifest.
- Safety check:
  - `out/design/reverse_lectionary_presentation.jsonl` was not found in the working tree.
  - `.gitignore` lines 13 to 14 explicitly ignore the retired monolith path.

## Required revisions
None.
