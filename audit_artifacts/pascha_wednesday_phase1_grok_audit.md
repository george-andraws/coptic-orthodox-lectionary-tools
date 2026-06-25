# Phase 1 Grok Audit - Pascha Wednesday Exact Duplicate Collapse

- Verdict: PASS WITH FIXES

- Evidence checked
  - Reviewed uncommitted diff.
  - Reviewed:
    - `audit_artifacts/pascha_wednesday_phase0_classification.md`
    - `audit_artifacts/pascha_wednesday_phase0_grok_audit.md`
    - `audit_artifacts/pascha_wednesday_phase0_grok_audit_pass2.md`
  - Parsed and compared `out/design/reverse_lectionary_index.jsonl` against `HEAD`.
  - Ran targeted JSONL checks for Category A, B, and C identity keys.
  - Ran `python verify_design_deliverables.py`.

- Findings
  - Category A collapse is correct in `out/design/reverse_lectionary_index.jsonl`.
    - Pascha Wednesday-like reverse-index rows decreased from 65 to 47.
    - Category A rows decreased from 34 to 17.
    - All 17 Category A identity keys are now single rows.
    - All 17 have `occasion: "Wednesday of Holy Pascha"`.
    - Normal A rows have `collapsed_row_count: 2` and `source_disclosure_count: 2`.
    - First Hour Psalm rows have `collapsed_row_count: 3` and `source_disclosure_count: 3`.
  - First Hour Psalm composite handling is correct.
    - Old standalone composite row `rid_0f3829504fa23a82482d`, `Ps 33:10,51:4`, no longer emits its own reverse-index card.
    - Its St. Mary source-text attestation is retained on:
      - `rid_03fee652493b21f24f4e`, `Ps 51:4`
      - `rid_e2e0dbf183569f4ac715`, `Ps 33:10`
  - Category B rows are still present and unchanged.
    - Exact canonical row comparison against `HEAD`: unchanged.
    - Count remains 12 rows, 9 unique B identities.
  - Category C rows are still present and unchanged.
    - Exact canonical row comparison against `HEAD`: unchanged.
    - Count remains 18 rows, 16 unique C identities.
  - No other reverse-index records changed.
    - Non-Pascha-Wednesday reverse-index multiset comparison against `HEAD`: identical.
  - Blocker found in generated deliverable validation.
    - `python verify_design_deliverables.py` fails:
      - `out/design/todays_readings_current_practice.csv row count 11 != summary 14`
    - `out/design/BUILD_DESIGN_SUMMARY.json` now reports:
      - `reverse_lectionary_index_status_disagreement_rows: 17`
    - Existing verifier expects this value to be `0`, so after the todays-readings mismatch is fixed, the verifier is likely still blocked unless the status disagreement behavior is corrected or the verifier is intentionally updated.

- Required fixes before commit
  - Regenerate or reconcile `out/design/todays_readings_current_practice.csv` and `.jsonl` so their row counts match `BUILD_DESIGN_SUMMARY.json`, or revert the summary count if the todays files should not change.
  - Resolve the 17 reverse-index status disagreements caused by the Category A collapses, or explicitly update the verifier and validation policy if these are now intended.
    - Preferred fix: treat `current_confirmed_by_fixture_equivalence` and `current_confirmed_coptic_reader` as compatible for these exact Pascha Wednesday collapses so validation remains clean.
  - Re-run `python verify_design_deliverables.py` and require a passing result before commit.

- Commit recommendation
  - Do not commit yet.
  - The reverse-index Phase 1 data behavior passes the Pascha Wednesday scope audit, but generated deliverable validation currently fails. Commit after the validation blockers are fixed and verified.
