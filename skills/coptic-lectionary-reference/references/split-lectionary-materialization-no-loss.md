# Split lectionary materialization without losing readings

Use this when the requester asks to split a large mixed lectionary artifact into smaller site-facing layers, especially a reverse-lectionary occurrence index plus date-resolved Today's Readings files.

## Trigger

- A monolith mixes year-independent passage-to-occasion data with date-resolved daily readings.
- the requester says this is a repartition/dedup/materialization reshape, not a recomputation.
- the requester says STOP on any sign a reading would be lost.

## Pattern

1. **Profile before changing anything.**
   - Total rows.
   - Counts by `source_family` and `source_kind`.
   - Count rows with and without `gregorian_date`.
   - Count date-resolved rows by Gregorian year.
   - Count distinct `(occasion, service_section, service_hour, slot, identity_key)` tuples.

2. **Verify `identity_key` is cross-source canonical before building.**
   - Spot-check an ordinary Great Lent weekday present in both `ordinary_date_resolved` and `katameros_cycle`.
   - Normalize the date-resolved prose label, such as `Friday of the sixth week of Great Lent`, to the cycle key, such as `week 6 day_of_week 5`.
   - Match by reading reference and confirm both rows share the same `identity_key`.
   - If they do not match, stop and fix identity generation before building any collapsed index.

3. **Build the year-independent occasion index by aggregation, never first-row-wins.**
   - Key: `(occasion, service_section, service_hour, slot, identity_key)` unless the requester explicitly changes it.
   - Preserve one output row per distinct key.
   - Aggregate `calendar_key` and `day_title` values because some generic occasion labels cover many calendar keys.
   - Aggregate source disclosure as the union of `(source_family, source_kind, source_edition, source_locator, source_title)`.
   - Preserve `display_ref`, `canonical_mt_ref`, `canonical_lxx_ref`, `spans_json`, `removed_marker`, `hour_theme`, `reading_type`, `reading_name`, `authority_tier`, and `current_status`.
   - Record `attestation_year_min`, `attestation_year_max`, and optionally the set of years for collapsed date-resolved ordinary readings.

4. **Handle status and removed-marker disagreements conservatively.**
   - Count disagreements across collapsed duplicates.
   - If `current_status` or `removed_marker` differs within a collapsed group, keep the current/conservative value only if the rule is explicit, and append the disagreement to `open_questions_for_george.md`.
   - Do not silently pick the first row.

5. **Build daily per-year files directly from dated rows.**
   - Input rows are only those with `gregorian_date`.
   - Emit `out/design/daily/lectionary-YYYY.json` keyed by ISO date.
   - Each date value is an ordered array of compact readings: `occasion`, `service_section`, `service_hour`, `slot`, `display_ref`, `identity_key`, `reading_type`, `removed_marker`.
   - Preserve source row order within each date.

6. **Add deterministic no-loss checks.**
   - Compare the old monolith's distinct occasion keys with the new index keys:
     - missing keys = 0
     - extra keys = 0
     - duplicate keys = 0
   - Compare dated rows grouped by ISO date against daily JSON:
     - old dated row count equals daily row count
     - missing dates = 0
     - extra dates = 0
     - date-local order mismatches = 0
   - If the monolith is retired, compare against the previous git object, for example `git show <pre-retirement-commit>:out/design/reverse_lectionary_presentation.jsonl`.

7. **Retire oversized monoliths safely.**
   - Stop generating the retired file.
   - `git rm` the tracked oversized file from the working tree.
   - Add the retired path to `.gitignore`.
   - Document that it remains in git history until the maintainer runs `git filter-repo` and force-pushes.
   - Do not attempt history rewrite unless the requester explicitly asks for repo-history surgery.

8. **Update handoff and manifest wording.**
   - Handoff runtime files should point to the split layers, not the retired monolith.
   - Mark old CSV materializations as archive/research-only if they remain.
   - Add a manifest note: materialization reshape only, no reading content changed, and no new affected passages for Bible-study audit.
   - Refresh handoff copies of generated specs after root specs are regenerated. Stale handoff specs are easy to miss.

9. **Audit pass.**
   - Have an independent reviewer audit internal consistency only when web tools are blocked.
   - If an independent reviewer finds stale docs or logs, patch those and rerun the audit.
   - Commit the final PASS audit artifact and record the audit outcome in the execution log.

## Known pitfalls

- The distinct key `(occasion, service_section, service_hour, slot, identity_key)` may merge multiple `calendar_key` values. That is acceptable only if `calendar_keys` is aggregated and no distinct reading placement is lost.
- Do not compare daily rows by global monolith order. Compare grouped by ISO date and preserve each date's local source-row order.
- `git diff --check` can flag regenerated CSVs with CRLF line endings as trailing whitespace. Set `lineterminator="\n"` on `csv.DictWriter`, including gzip-wrapped CSV writers.
- A handoff copy can become stale even when the root generated spec is correct. Refresh `out/handoff/lectionary_spec.md` and handoff specs after regeneration.
- If a verifier uses the CSV research materialization as the source for no-loss checks, keep that CSV documented as archive/research support even after retiring the oversized JSONL.
- Before continuing a split-materialization follow-up, audit recent history with `git log --oneline -12` and `git show --stat` for any hygiene or generated-data commits the user names. If a large reshape is accidentally bundled into a mislabeled hygiene commit, fix history before changing data. If hygiene is cleanly separate, do not rewrite history.
- When `.DS_Store` or similar local metadata appears during a lectionary data run, add it to `.gitignore` and remove tracked instances in a standalone hygiene commit after data commits. Do not bundle that with generator or artifact changes.
- For source disclosure in an occasion index, avoid per-year disclosure bloat. Collapse `source_disclosure` by the distinct source tuple `(source_family, source_kind, source_edition, source_title)`. Keep one representative `source_locator` per distinct source in the index, preserve full row-level locators in `passage_source_disclosure.csv` or the raw audit archive, and verify `source_disclosure_count` equals the distinct-source count for each reading.
- For same-source per-year date-resolved rows, keep row-level `attestation_year_min`, `attestation_year_max`, `attestation_years`, and `collapsed_row_count`. Inside each collapsed disclosure entry, include `attested_year_min` and `attested_year_max`; include `attested_years` only when the years are non-contiguous.
- When invoking Hermes CLI one-shot audits with restricted toolsets, the compact option is `-t file`; do not assume a long `--enabled-toolsets file` flag is accepted by every installed Hermes CLI.

## Verification commands to adapt

```bash
python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_lectionary_change_manifest.py
python3 build_design_deliverables.py
python3 verify_design_deliverables.py
python3 scripts/build_lectionary_change_manifest.py --baseline lectionary-baseline --head HEAD
test ! -e out/design/reverse_lectionary_presentation.jsonl
git diff --check
```
