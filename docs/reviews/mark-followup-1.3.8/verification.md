# Mark L1-L10 diagnostic verification

These results cover the Mark follow-up source snapshot, not final integrated release acceptance. The parent is coordinating further T-L/LK work and owns the complete frozen-candidate inventories, clean-source build and any authorized release. This worker did not commit, push, publish or touch the site.

## Environment

All Python commands and Node commands with Python children use:

```sh
uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate --with pytest python ...
```

Node is launched with `subprocess.run` from that Python environment so its `python3` children inherit the same dependencies. The repository is `/Users/ga/.hermes/cache/scratch/mark-lectionary-138/repo`.

## Baseline and RED

- Before source edits: `python -m pytest -q tests/test_holy_week_review_repairs.py tests/test_review_release_contract.py tests/test_calendar_review_repairs.py`, through the uv prefix above: **36 passed, 16 skipped, 731 subtests passed**.
- New package tests against published 1.3.7: `node --test tests/npm_mark_followup.test.cjs`: **0 passed, 7 failed**, child exit **1**. Exact transcript: `RED-node.txt`.
- The complete-day-set regression also demonstrates the duplicated Monday/Tuesday Third Hour set directly from the authenticated predecessor and passes after the overlay.

## Real builders and current projection

- `node scripts/build_npm_package.mjs`, launched through uv Python: actual candidate builder completed, child exit **0**. Final Mark source build log: `build-diagnostic-final.txt`. No clean-source flag or commit hash was forced.
- `python scripts/report_mark_followup.py --baseline /Users/ga/.hermes/cache/scratch/mark-lectionary-138/baseline/package`: reauthenticates all **11** published predecessor members and renders the complete check sheet, identity report, counts and full **551-row** 2026 before/after table.
- `python scripts/verify_package_integrity.py --package-dir ./packages/lectionary-data --strict-file-set`: **pass**, no failures; receipt `integrity-diagnostic.json`.
- `python scripts/compare_external_sources.py --package-dir ./packages/lectionary-data --output docs/reviews/mark-followup-1.3.8/cache-comparison-diagnostic.json --csv-output docs/reviews/mark-followup-1.3.8/cache-comparison-diagnostic.csv`: **pass**, **zero mismatches in each of 2026, 2027 and 2028**. This is cached-source preservation after exact bounded successor authentication, not fresh whole-service Reader verification.

## Focused GREEN

```sh
python -m pytest -q \
  tests/test_mark_followup_repairs.py \
  tests/test_review_release_contract.py \
  tests/test_review_comparison_contract.py \
  tests/test_daily_current_validation.py \
  tests/test_holy_week_review_repairs.py \
  tests/test_calendar_review_repairs.py
```

Through the uv dependency prefix: **178 passed, 16 skipped, 731 subtests passed**, exit **0**, 166.02 seconds. Transcript: `GREEN-python.txt`. The 16 skips are pre-existing historical optional cases, not new quarantines. After adding an exact comparison against actual complete current candidate arrays, the final dedicated Mark suite passed **69 tests**, exit **0**. The larger result and dedicated result overlap and are not additive.

```sh
node --test \
  tests/npm_mark_followup.test.cjs \
  tests/npm_review_release.test.cjs \
  tests/npm_pascha_daily.test.cjs
```

Launched through uv Python: **27 passed, 0 failed, 0 skipped**, child exit **0**. Transcript: `GREEN-node.txt`.

## Failure classification and repairs

- The first real overlay build refused expected post-build occurrence fields missing at its pre-occurrence stage. Qualification now excludes only the declared derived occurrence/order cells while preserving all source, coordinate, disclosure and lifecycle fields.
- The first strict CLI replay exposed a missing repository import path at its new earliest import. The CLI prerequisite was fixed, not its validation expectations.
- Structural fill changed surviving Wednesday Eve row positions when L9 rows became inactive before daily projection. The overlay now preserves the authenticated complete predecessor service sequence for the actual surviving rows. It never supplies candidate content from the expected table.
- A shared raw source cell owns both an older retired Psalm and a reviewed fragment. Exact source-qualified neighbor authentication distinguishes them instead of confusing a shared locator with identical occurrence identity.
- Historical H/K/R tests initially read successor data with new holds/display labels. Their literal predecessor count/order assertions and corruption oracles were retained, with hash-pinned 1.3.7 inputs selected explicitly. The new Mark suite independently checks complete current arrays, all new holds and mutation rejection. The historical Node transition produced **21 passes and 6 failures** before that fixture pairing was corrected; its transcript is `node-historical-transition.txt`.
- New source dependencies were added to the real-builder fixture copier. Source authentication remains enabled; no repair hook was mocked out.

## Verified Mark-only counts

| Year | Civil dates | Published 1.3.7 readings | Candidate readings | Pending before | Supported pending retained |
| --- | --- | --- | --- | --- | --- |
| 2026 | 365 | 4088 | 4078 | 10 | 7 |
| 2027 | 365 | 4079 | 4069 | 25 | 22 |
| 2028 | 366 | 4096 | 4087 | 10 | 7 |

Reverse rows: **12,334**, including four added inactive candidates and their four preserved historical source witnesses. No historical membership ledger was refreshed. Source-only and numeric-source-coordinate held Psalms remain distinct from the three excluded stale canonical Pascha witnesses per year.

## Integration interfaces and remaining gates

- `mark_followup_repairs.repair_rows(rows, date=None)` is the reverse overlay; `repair_daily(days)` is the date-map overlay after old H/K/R repairs. Both preserve input source fields and retain inactive history.
- `qualify_emitted(row, date=None)` authenticates owned output, with the trusted outer date supplied for daily rows. `validate_pending_reading(row, date)` enforces exact accepted pending occurrences.
- `validate_eve_coverage(days, year)` returns 25 hour-accountability entries: 19 current and six explicit Reader gaps. `validate_day_hour_sets(days)` rejects cross-day full Gospel/prophecy set copies.
- `restore_predecessor_for_comparison(daily, year)` first checks complete Mark successor date arrays, then returns the authenticated predecessor view for the retained historical comparator. If T-L/LK legitimately changes one of those same 36 dates, parent integration must compose its independently authenticated delta explicitly. Do not remove the complete-table guard or refresh the Mark fixture from integrated candidate output.
- Shared integration files changed here: `scripts/apply_review_repairs.py`, `scripts/build_npm_package.mjs`, `scripts/review_release_contract.py`, `scripts/verify_package_integrity.py`, `scripts/compare_external_sources.py`; they are ready for parent-controlled integration. The builder source version is 1.3.8 and explicitly accepts predecessor package 1.3.7. The public `isCurrentReading` implementation is unchanged.
- Complete Python and Node inventories, tracked-only real-builder replay, isolated tarball installation, final integrated provenance and final consumer acceptance are **not claimed** by these diagnostic runs. The parent owns them after all writers stop. Do not overwrite the parent's independently updated package README.
