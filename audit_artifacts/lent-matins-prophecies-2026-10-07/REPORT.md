# Third-Week Great Fast Wednesday Matins correction

## Status
Execution verification complete. **Independent final read-only review approved, with no blocking defect** (`deleg_a6f0ccd7`). All 11 reviewed source/test hashes match the final execution-verified snapshot, and the packed tarball checksum remains unchanged.

The reviewer inspected code and existing execution records, not an independent rerun of the suites. Its additional comparison attempt was approval-blocked and did not run; the parent's full non-target comparison did run and passed. Approval applies only to this narrow correction, not broader lectionary completeness.
Local uncommitted `@andraws/lectionary-data@1.3.1` candidate. No commit, push, npm publication, site deployment, or vault promotion.

## Exact correction and source confidence
Confirmed by saved rendered evidence from the official Coptic Reader web app, publisher Coptic Orthodox Metropolis of the Southern United States, selected civil date **2026-03-04**, Meshir 25, 1742, Wednesday of the Third Week of Great Fast, **Matins / Prophecies**:

1. Exodus 4:19–6:13, including all of chapter 5.
2. Joel 2:21–27.
3. Isaiah 9:9–10:4.
4. Job 12:1–14:22.

The four prophecies precede the existing Matins Psalm and Gospel. The cycle already included Exodus 5, but the daily materialization omitted the entire prophecy block. Its normalized Joel endpoint was also incorrectly verse 26. The raw API string and source SQLite bytes are preserved.

Evidence lives in `sources/coptic-reader/lent-week3-wednesday-2026-10-07/`, with source fingerprints recorded in `comparisons.json`. This is authenticated saved evidence, not a new live sweep of all Coptic Reader contexts. The stateful app URL is https://copticreader.org/app/; the selected date and service are essential context, not a permanent dated link.

## Scope and risk model
The supplement requires both the exact recurring occasion and Pascha offset -39. Date helpers and design data cover **2020–2035**; the candidate ships **2026–2028**. Target shipped dates are **2026-03-04, 2027-03-24, 2028-03-08**. No other Lenten tables have been populated from inference.

Risks tested: date/context leakage, missing or duplicate readings, order, Joel endpoint, Exodus chapter overlap, loss of removed-state flags, downstream lookup propagation, package-builder data loss, schema compatibility, and accidental modification of unrelated snapshots.

## Production and validator changes
- Context-qualified verified source overlay and normalized cycle boundary correction.
- Current date helper, reverse/chapter index and design materialization propagation.
- Explicit preservation modes for source/date rebuilding and design-data-only rebuilding.
- npm builder preserves the current catalog/calendar runtime, exports, schema, Synaxarium data, README and license; unsupported newer package versions are rejected.
- New source authority tier uses existing `current_authority` vocabulary. The initially introduced `primary_current_practice` label was rejected by the full validator and corrected before packing.
- Design validator's old 11920-row expectation disagreed with committed baseline 11921. Correct expectation is 11925, consisting of the committed baseline plus four new occasion-level prophecy rows; replacing Joel does not increase that total.
- Independent daily projection checks lock the supplement's references, service, occasion, slots and order. Corruption tests reject omitted, reordered and endpoint-truncated prophecy rows.
- Existing no-service removal markers are recognized only for documented suppression contexts with matching source, status, title, service and optional civil date. No suppression source/data was broadened by this compatibility repair.

## Verification evidence
All commands below actually ran with exit 0. Full execution commands, environment overrides, logs and final source hashes are in `commands.json` and `final-evidence.json`.

| Check | Final result |
|---|---|
| Source build, `build_lectionary_reference.py --preserve-legacy-passage-snapshot` | Pass |
| Design build, `build_design_deliverables.py --data-only` | Pass |
| Package build, `node scripts/build_npm_package.mjs` | Pass |
| Python unittest discovery | **67 passed** |
| Node test suites | **23 passed**, zero failures/skips |
| Full `verify_design_deliverables.py` | Pass |
| Source manifest and strict calendar coverage | Pass |
| Full source/date/non-target comparison | Pass |
| Strict package and tarball integrity | Pass |
| Offline isolated tarball installation | Pass |
| Installed runtime/readings/reverse/calendar/Synaxarium smoke | Pass |
| `query_lectionary.py --passage "Exodus 5" --limit 50` | All 16 recurring dates returned |
| `git diff --check` | Pass |

The Python suite emits an existing unclosed-fixture-file ResourceWarning in `test_reading_semantics.py`; there are no test failures. Original source and builder RED receipts are retained, plus `parent-validator-regression-red.log` and final green suite receipts. Repeated runner labels use the latest log file; consult final command selection in `final-evidence.json` for final-state claims.

## Preservation and precise delta
`comparisons.json` verifies:
- Only one target date changes per supported year. Existing seven readings become eleven; original readings remain semantically identical except their shifted `reading_order`.
- All non-target daily date blocks remain byte-identical for both design and shipped-package files.
- Source/current-date tables each gain 64 sourced prophecies: four readings for each of 16 recurring dates. Existing rows remain semantically unchanged, ignoring absent-vs-empty newly added metadata.
- Reverse index delta is four added verified prophecy readings and replacement of the normalized Joel reading; final total 11925 rows.
- Exodus 5 is present on every supported target date. Chapter propagation adds 144 date-chapter occurrences and replaces one cycle Joel row.
- Package runtime, calendar, README, license, Synaxarium JSON, raw SQLite, Pascha direct tables, current-day snapshots, specs and the two preserved legacy passage-index snapshots match committed baseline bytes.
- Synaxarium remains **366 days / 868 commemorations**. Package exports and schema are unchanged.

Two historical passage-index snapshots exhibited unrelated rebuild drift and were restored unchanged. Their receipt is `legacy-snapshot-drift.json`; current helpers use corrected current-date sidecars. Do not treat preserved historical snapshots as newly regenerated corrected exports.

## Downloadable candidate
`andraws-lectionary-data-1.3.1.tgz`

- Bytes: 2128263
- SHA-256: `5abfab18ee8228d54470661d4a6ccf597208cebd92e5cf8627498818a42fae02`
- Packed runtime files: 11, exact expected set.
- Each tarball file matches its package source bytes, and each offline-installed runtime file matches the packed bytes.

`meta.source_repo_commit` refers to baseline **0664a4acbdef2ad65ee0bbd7666e73cedd572e3f**, not a committed final correction. Source hashes in `final-evidence.json` identify the uncommitted candidate. Publication is deliberately outside this task.

## Remaining completeness limits and recommended next stage
The packed candidate still has **95** other explicitly labelled Monday–Friday Great Lent dates without prophecy rows: 2026=32, 2027=31, 2028=32. Exact dates are recorded in `packed-candidate-verification.json`. This is a coverage warning, not independent authentication of each missing table.

Recommend a separately authorized full **distinct-context reconciliation**, starting with Lent/Jonah, then Pascha/Bright Saturday, then ordinary/seasonal/feast and special services. Capture each primary-source table once and test calendar selection/collisions separately across shipped years. Require independent service/slot/order/reference/status oracles throughout source, helper, reverse/chapter index, packed runtime and consumer. Distinguish not captured, captured absent and captured present. Do not call this narrow candidate a complete lectionary or silently apply unresolved Good Friday alternatives.

The site remains on its prior installed package; no site update or deployment is included here.
