## Verdict: PASS

The current working tree is internally consistent with the two-layer split model. I found no evidence that a distinct reading was lost between the retired monolith and the union of:

- `out/design/reverse_lectionary_index.jsonl`
- `out/design/daily/lectionary-YYYY.json`

## Evidence reviewed

- `build_design_deliverables.py`
  - Builds `reverse_lectionary_index.jsonl` from distinct `(occasion, service_section, service_hour, slot, identity_key)` tuples.
  - Enforces `8005` index rows.
  - Builds daily JSON files from all rows with `gregorian_date`.
  - No longer writes `out/design/reverse_lectionary_presentation.jsonl`.
  - Still writes `reverse_lectionary_presentation.csv` as a research/archive materialization, which is consistent with the docs.

- `verify_design_deliverables.py`
  - Verifies index row count and exact key equality against the presentation CSV.
  - Verifies daily files exactly match dated presentation rows by year/date and preserve date-local row order.
  - Verifies daily fields match schema.

- `out/design/BUILD_DESIGN_SUMMARY.json`
  - `reverse_lectionary_presentation_rows`: `66381`
  - `reverse_lectionary_index_rows`: `8005`
  - `daily_lectionary_total_rows`: `59324`
  - `reverse_lectionary_index_status_disagreement_rows`: `0`

- Deterministic comparison evidence supplied
  - Old monolith: `66381` rows.
  - Dated rows: `59324`, all preserved in daily files.
  - Undated/date-independent distinct occasion tuples: `8005`, all preserved in the index.
  - Missing/extra/duplicate index keys: `0`.
  - Missing/extra dates and date-order mismatches: `0`.

- `lectionary_spec.md` and `out/handoff/lectionary_spec.md`
  - Both now describe the split files as site-facing outputs.
  - Both state the previous JSONL monolith is retired from the working tree.

- `site_integration_spec.md` and `out/handoff/site_integration_spec.md`
  - Both align with the split model.
  - Handoff site spec clearly states:
    - use `reverse_lectionary_index.jsonl` for reverse lectionary rendering,
    - use daily JSON by ISO date for Today’s Readings,
    - shipped window is `2026`, `2027`, `2028`,
    - full `2020-2035` daily set remains research/archive material in `out/design/daily/`.

- `out/handoff/HANDOFF.md`
  - Runtime files include `reverse_lectionary_index.jsonl` and daily files for `2026`, `2027`, `2028`.
  - Old `reverse_lectionary_presentation.csv` is archive-only.
  - Retired JSONL is explicitly documented as not present in the working tree and history-only.

- `out/design/lectionary_change_manifest.md` and `out/handoff/lectionary_change_manifest.md`
  - Correctly frame the split as a materialization reshape.
  - Explicitly state it adds `NO new affected passages` for Bible-study audit.

- `.gitignore`
  - Explicitly ignores `out/design/reverse_lectionary_presentation.jsonl`.

- Working-tree file search
  - No `reverse_lectionary_presentation.jsonl` exists in the repo working tree.
  - Only `reverse_lectionary_presentation.csv` remains, and it is documented as archive/research support.

- `audit_artifacts/lectionary_execution_log.md`
  - Now records:
    - Step 1 commit `c785f61`
    - Step 2 commit `60e45ca`
    - Step 3 commit `475f9f6`
    - Step 4 reconciliation commit `d0f46d7`
    - Final Step 4 verification, including `test ! -e out/design/reverse_lectionary_presentation.jsonl`.

## Audit answers

1. **Is the two-layer split internally consistent with the stated goal?**

   Yes. The index preserves distinct occasion/placement/identity tuples, while the daily files preserve date-resolved rows. This matches the stated goal of separating reverse-lectionary lookup from Today’s Readings runtime lookup.

2. **Is there evidence that a distinct reading was lost?**

   No. The supplied deterministic evidence plus the current generator/verifier logic support preservation:
   - `8005` distinct undated/occasion tuples preserved in the index.
   - `59324` dated rows preserved in daily JSON.
   - `66381 = 59324 + 7057`, with the undated/date-independent material collapsed into `8005` distinct index tuples by identity/placement.
   - No missing, extra, or duplicate index keys.
   - No missing or extra dates.
   - No daily date-order mismatches.

3. **Are handoff and site-integration docs consistent with the new split model and shipped window?**

   Yes. The prior issue with stale `out/handoff/lectionary_spec.md` has been fixed. The handoff package now points to:
   - `reverse_lectionary_index.jsonl`
   - `daily/lectionary-2026.json`
   - `daily/lectionary-2027.json`
   - `daily/lectionary-2028.json`

   It also clearly marks the full daily range and presentation CSV as archive/research support.

4. **Does the manifest correctly frame this as a materialization reshape with NO new affected passages?**

   Yes. Both design and handoff manifest summaries state this is a materialization reshape and adds `NO new affected passages` for Bible-study audit.

5. **Does the old oversized JSONL remain only in git history, not the working tree?**

   Yes. File search found no working-tree `reverse_lectionary_presentation.jsonl`; `.gitignore` blocks it; docs and execution log state it is history-only.

## Issues

None blocking.

Non-blocking note: the prior audit artifact still records the earlier pre-revision findings, but that is historical audit evidence, not current-state documentation. The current spec, handoff docs, manifest, and execution log supersede it.

## Required revisions

None.
