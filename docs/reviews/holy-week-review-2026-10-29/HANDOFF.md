# Holy Week H1-H8 implementation handoff

## Outcome

The new source-owned repair lane is implemented and exercised against the exact published `@andraws/lectionary-data@1.3.6` artifact. Its SHA-512 integrity matches the parent-authenticated baseline. No shared builder, package artifact, site, vault, commit, push or publication was changed by this worker.

| ID | Reproduced against published 1.3.6 | Implemented result and remaining source limit |
|---|---|---|
| H1 | Yes, with qualification: Tuesday Eve has 21 curated rows, 15 live and 6 already inactive. The Sixth Hour Gospel/Psalm differ from Monday Eve, so the complete literal sets are not identical. Four other hours contain the reported copy pattern; split versus continuous references also differ. | Hold the 15 live wrong-night rows with `pending_coptic_reader_review` and `active: false`. Preserve the 6 inactive witnesses. Add 5 Reader-backed First/Sixth Hour appointments. First Hour Reader Ezekiel 22:23-29 differs from the printed 22:23-28 endpoint. Third/Ninth have printed candidates only; Eleventh remains uncaptured. |
| H2 | Yes. Palm Sunday has 21 daily rows and no Eve of Monday hours. Printed Monday Eve has 13 witness rows. | Add the four literal non-Psalm appointments from retained Reader Third/Eleventh Hour captures. Palm Sunday becomes 25 rows. First/Sixth/Ninth remain printed evidence-only candidates. No missing Gospel or Psalm range inferred. |
| H3 | Yes. Eve labels are source-specific. The attachment's label distinction is correct, but its hour-for-hour equivalence should not be treated as a complete table equality: Eleventh Hour witnesses differ. | Add `pascha_service`, `pascha_offset_days`, `display_occasion` and daily `pascha_civil_date`, preserving original titles, raw labels and calendar keys. Curated Monday Eve is `eve_of_tuesday`; printed Monday Eve is `eve_of_monday`. The check sheet contains the full explicit mapping. |
| H4 | Yes. `rid_d29544c970904a8ee5f2` occurs at both Third and Sixth. Identity alone is not a service key. | Hold only Sixth Hour John 19:1-12; add Reader-backed John 19:13-27. Preserve Third Hour. Also restore the source-attested Sixth Hour Gospel sequence Matthew, Mark, Luke, John using captured heading ordinals. |
| H5 | Yes. `rid_a3e2c8af7f4595282adb` occurs at Great Thursday Third and Ninth. | Flag both and leave both statuses/readings unchanged as requested. Reader confirms Ninth. Third remains to check. Do not use an unconditional non-Psalm duplicate rejection as a deletion rule. |
| H6 | Yes. Curated `rid_af6bf4bf6c1d0b812cd2` is Jeremiah 43:5-11. | Hold that witness; add literal Reader Ezekiel 43:5-11 from Covenant Thursday Eve First Hour. No printed-only promotion. |
| H7 | The missing current Eleventh Hour Pauline reproduces, but it is not an established current-practice omission. | Retained complete Reader Friday Eleventh has no Pauline reading. Galatians 3:1-6 stays historical. Reader Friday Sixth confirms Galatians 6:14-18. Isaiah 19:19-25 at Thursday Eleventh remains working/unconfirmed. Authenticated Ottawa excerpts and the attachment's separately reported Section12HCM evidence are recorded as printed corroboration only. No fresh archive verification is claimed. |
| H8 | Yes, exactly 247 working curated appointment rows in the published reverse artifact. | 53 exact existing non-Psalm appointments receive retained Reader confirmation; 17 targeted defects are held; 177 remain working/unverified. Existing inactive witnesses and five curated Psalm-alignment holds are unchanged. No blanket holding or promotion. |

## API for parent integration

```python
from holy_week_review_repairs import repair_reverse_rows, repair_daily_year
corrected_reverse = repair_reverse_rows(canonical_reverse_rows)
corrected_year = repair_daily_year(year, complete_daily_date_map, corrected_reverse)
```

- Reverse hook: after existing npm `canonicalizeOccurrences`.
- Daily hook: after structural fill, not before, so fill cannot restore the holds.
- The daily hook requires the complete date map for the requested year and validates that affected dates exist. It preserves original daily locators instead of replacing them with a reverse representative locator.
- Parent may assign the new daily rows' `service_order` after this hook without another sort. The hook already orders source-backed companions by authenticated heading order.
- Both hooks are idempotent. They copy their input and preserve unrelated rows, original source fields, inactive statuses and raw calendar keys.
- Every H1/H4/H6 hold explicitly has `active: false`. The actual package JavaScript `isCurrentReading` returns false for these holds. Its rejection of unsupported statuses is not relaxed.
- Printed candidates reuse preserved historical witnesses; the lane does not duplicate or activate them.
- Keep the original design whole-corpus membership gate unchanged. A diagnostic attempt to insert these additions at presentation level correctly failed that gate, with expected 12186, actual 12196, missing 0 and extra 10. That diagnostic was not package acceptance. The coordinated supported architecture is the source-owned npm overlay above.

JSON stdin/stdout bridge, for use by the parent's router:

```text
python -m holy_week_review_repairs
{"mode":"reverse","rows":[...]}

python -m holy_week_review_repairs
{"mode":"daily","year":2026,"days":{...},"reverse_rows":[...]}
```

Run with the project's Python dependency environment, not the incompatible system Python. The exercised environment is:

```text
uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate python ...
```

## Verified standalone overlay results

The reverse count changes from 12,206 to 12,217. There are 11 new Reader-backed appointments, 17 held existing appointments and 53 source-confirmed existing appointments. No baseline witness is dropped. Full original title, locator, key, identity and span preservation is asserted for the two affected source families.

| Daily year | Published rows | Repaired rows | Held rows emitted |
|---|---:|---:|---:|
| 2026 | 4097 | 4091 | 0 |
| 2027 | 4088 | 4082 | 0 |
| 2028 | 4103 | 4097 | 0 |

Complete Palm Sunday through Good Friday before/after records, including service, hour, slot, reference, status, identity and locator, are in `before-after-daily-holy-week.csv`. All 18 affected civil dates are included. The detailed per-date counts and all 70 status transitions are in `published-audit.json`.

The check sheet contains 481 baseline appointments, each once: 414 across the two Holy Pascha source families, 17 existing qualified Pascha rows, and 50 Bright Saturday rows. This includes every H8 working row and all nine pending-alignment rows in these families. Source-backed additions are separately labeled, not counted as baseline appointments. R2 and R5 remain the other workers' check-sheet responsibility.

## Files owned by this worker

- `holy_week_review_repairs.py`: authenticated repair decisions, explicit source-family Eve mapping, reverse/daily overlays and JSON bridge.
- `tests/test_holy_week_review_repairs.py`: 17 behavior, source, replay, ordering and public JavaScript predicate tests.
- `tests/fixtures/holy_week_review_1_3_6.json`: immutable exact published affected-family inventory and complete Holy Week day arrays for 2026, 2027 and 2028, with authenticated package identity and pinned fixture hash.
- `sources/coptic-reader/holy-week-review-qualified-2026-10-29/`: 23 full retained Reader documents, a pinned source manifest, and separately pinned printed H7 evidence excerpts. No live app visit.
- This report directory: check sheet, audit JSON, complete daily before/after CSV and actual verification logs/receipt.

## Verification and limits

- New Holy Week suite: 17 tests pass, no skips. Source tampering fails both creation and downstream validation. Reversed reverse-input order preserves source reading order. The JSON bridge runs in fresh processes on complete published arrays. The suite also passes with a fresh nonexistent HOME.
- Existing Pascha suites: 18 tests pass.
- Existing Lamentations/Joel correction suite: 4 tests pass.
- RED evidence includes three failures with the repair lane disabled, the actual public-predicate hold failure before `active: false`, and an actual failed Gospel-order assertion before source-heading ordering was applied. GREEN logs and the verification receipt are retained beside this report.
- Full parent combined npm build, package-wide tests, candidate pack, release and consumer acceptance remain parent-owned. This report does not claim those gates passed.
- H1 and H2 are still partial source recovery. Uncaptured hours and Psalm edition-alignment questions remain explicit on the check sheet. H5 Third Hour and Thursday Eleventh prophecy boundaries remain unresolved.
