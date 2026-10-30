# R2 fixed-day repair approval and executed evidence

This is a **new current implementation contract**, separate from the recovered exact-date receipt. It does not edit or retroactively activate that receipt. The original `genericTemplateQualification=false` and `qualified_exact_observed_date_table` remain intact.

## Scope and parent hooks

```python
import kiahk23_review_repairs as r2
corrected_reverse = r2.repair_reverse_rows(published_rows)
corrected_daily = r2.repair_daily(daily_dict, corrected_reverse)
```

Call the first after the unchanged `canonicalizeOccurrences`; call the second after existing structural daily fill. Both actual callers authenticate `repair-plan.json` and every pinned evidence file, including all seven full source documents and the explicit no-prophecies rubric. No design/raw corpus membership guard is weakened. The public `isCurrentReading` predicate is faithfully mirrored and contract-tested against the actual builder's JavaScript function before selecting competitors; unknown explicit statuses are refused, not implicitly current.

The new table has all **nine** selections, in service order: Vespers Psalm and John 7:40–53; Matins Psalm and Matthew 12:1–8; Hebrews 11:32–40, James 5:7–13, Acts 2:22–36, Liturgy Psalm and Matthew 22:35–46. All three Psalm selections retain literal Reader labels, blank canonical refs and `spans_json=[]`. Exact cross-edition Psalm alignment is **not** approved.

Bounded recurrence: Gregorian 2020–2035, actual Coptic 4/23, **non-Sunday only**, exact resolved annual occasion, no conflicting current feast/occasion, and consistent supplied calendar/date/weekday fields. This is approved current repair scope, not a claim of fresh observation in every year. All original rows and cycle labels/locators survive; current lower witnesses become inactive history, and previously inactive witnesses remain byte-equivalent dictionaries.

Keep optional `kiahk23_review_evidence`, `kiahk23_retirement`, source labels/edition and source disclosure in npm output. The module already returns complete public-shaped rows, so applying an old projection allowlist afterward would discard the qualification. Full-source hashes are checked again on real reverse/daily calls, not just in test helpers.

## Executed verification

- RED: the full-table regression was observed failing against a no-op baseline with the actual 20 published Kiahk23 reverse witnesses; it exposed the wrong Moses table plus duplicate cycle rows, not an import failure.
- GREEN: `uv run --python 3.11 --with convertdate python -m unittest tests.test_kiahk23_review_repairs -v`: **14 tests passed**, exit 0.
- Tests cover all supported weekday dates in 2020–2035 and adjacent excluded years, Sunday/feast exclusions, every pinned evidence-file mutation through both real module callers, transplanted projected row/context/disclosure mutations, actual JS current-status parity, source-only Psalm holds, idempotency and inactive-witness preservation.
- Direct execution over the authenticated full published **1.3.6** reverse artifact: **12,206 → 12,215 rows; 9 new, 20 existing rows retained inactive**.
- Direct execution over all three actually shipped baseline daily files: only **2026-01-01** and **2027-01-01** changed, each to 9 active full-table readings plus retained inactive original witnesses. **2028 changed no dates**; the actual published Sunday **2028-01-02** stayed unchanged, including Mark 3:28–35 and Luke 1:57–80.
- An initial attempted full 2020–2035 baseline replay correctly reported absent 2020 daily file; baseline ships only 2026–2028. Recurrence testing outside those shipped years uses explicitly labeled constructed date contexts, not invented npm artifacts.

## Fresh Sunday Reader check

`./sunday-2028-01-02/capture-receipt.json` records actual fresh UI evidence:

- Ready selected home: **4th Sunday of Koiahk; Koiahk 23, 1744; Sunday, January 2, 2028**.
- Explicit Morning envelope, picker **12:00 PM**. Do not relabel this as 10 AM or as a before-noon clock.
- Full Matins body: literal **Psalms 95:10,11,12; Mark 3:28-35**, with all English numbered verses 28–35.
- Visually inspected ready Gospel reference screenshot: `sunday-2028-01-02/attempt02/matins-gospel-heading-ready.png`.
- Home and picker screenshots also visually inspected. Rejected evening/blank/locator attempts remain separately labeled in the receipt.

This is a **narrow fresh Matins confirmation**, not a fresh whole Sunday table. Sunday Liturgy Luke 1:57–80 remains the authenticated package/database witness here. The browser unexpectedly reset to blank targets around separate visual-inspection calls; accepted captures and hash receipt survived. Exact document-route URL was not recorded before the final reset, so only the actual public app entry URL is cited.

No shared builder, package output, original receipt, site, vault, commit, push or publication was changed by this lane. Parent owns integration and release acceptance.
