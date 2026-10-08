# Independent Sunday capture qualification

## Decision

**Accepted as exact dated source oracles: 12 tables / 84 documents and 32 dated-context probes.** This is not release approval, a correction implementation, generic replacement-template coverage, or completion of all 25 seeds.

Independent verification executed `review.py` successfully. It rehashed all **733 declared evidence pointers**, all **12 composite table hashes**, and the publisher's archived HTML declaration. Every original seed object was preserved. The resulting partition remains **9 qualified queued representatives, 12 awaiting whole-table capture, 4 bounded-policy replacement templates retained**; the three replacement canaries are additional actual-date oracles, not the missing generic templates.

The 44-entry context ledger separately records 32 probe observations and 12 whole-table observations (32 distinct civil dates). All selected civil dates, Sunday weekdays, numeric Coptic dates, and queued whole-table ordinals/months agree with independent civil-New-Year arithmetic. The actual package numeric calendar also agrees on all 32 dates.

## Evidence qualification

- All seven required documents occur in source order: Vespers; Matins Prophecies; Matins Psalm/Gospel; Pauline; Catholic; Praxis; Liturgy Psalm/Gospel.
- All 108 printed references were independently extracted from literal tabbed source headings, matched in order against the document and oracle arrays, and visually inspected in readable `literal-00.jpg` through `literal-17.jpg` sheets. All 84 complete raw documents, raw heading lines, line-bound assigned blocks, and ordered English verse lines are retained in `accepted-oracle.json`.
- All 72 non-Psalm appointments have complete English numbered-verse sequences matching their printed endpoints, including cross-chapter boundaries. Every Matins Prophecies page explicitly says **“No prophecies are read on this day.”** Absence was not inferred from an empty template.
- Every manifest PNG path was visually inspected by byte-identity deduplication: **424 paths / 244 distinct SHA-256 images**, indexed in `visual-index.json`, through `contact-00.jpg`–`contact-20.jpg`. These include date pickers, selected-date panels, home contexts, menus, reading documents, reference images, and retained failed-attempt context images. No loading/transitional reading image was found. Preselection panels remain navigation history, not accepted selected contexts. Whole screenshots certify only visible portions; complete offscreen bodies are authenticated from rendered text, not invented from screenshots.
- Psalms are accepted literally as Reader edition-qualified headings and bodies. **Canonical MT/LXX verse equivalence remains held**, not scored by a flat chapter shift. The oracle does not claim a fresh live app recapture or an independently translated biblical text.
- The 43 numeric survey rows were checked within 2020–2035. Inferred policy rows were not promoted to observed tables or universal absence claims. Prior 75 exclusions remain retained source inputs, not newly certified primary-source exclusions.

## Publisher rules and actual seam

The archived help HTML and a separately fetched current official help HTML both contain these exact statements under their respective Version headings:

- **2.92:** “When there is a 5th Sunday of Tobe, move the Sundays of Meshir up by one week to avoid duplicate readings on the 5th Sunday of Tobe and the 2nd Sunday of Meshir.”
- **2.55:** “Fixed bug that incorrectly considers the 4th Sunday of Thoout to be the 5th Sunday when Thoout 1 lands on a Sunday”
- **2.56:** “BUG FIX: When the month of Mesore has 5 Sundays and Nesi does not have any Sundays, the 5th Sunday of Mesore should be considered the 1st Sunday of Nesi.”

Primary observations confirm:

| Civil date | Numeric Coptic date | Actual Reader occasion |
|---|---|---|
| 2027-02-07 | Tobe 30, 1743 | First Meshir Sunday |
| 2027-02-14 | Meshir 7, 1743 | Second Meshir Sunday |
| 2027-02-21 | Meshir 14, 1743 | Third Meshir Sunday |
| 2027-02-28 | Meshir 21, 1743 | Fourth Meshir Sunday |
| 2027-03-07 | Meshir 28, 1743 | Sunday before the Great Fast |

This is a liturgical month-context shift, not a numeric Coptic conversion error or a universal ordinal formula. Paone 7/14/21/28 independently remains first/second/third/fourth.

## Findings by conflict class

### Calendar / dated-source selection conflicts

The current Python `calendar_resolution.resolve_current_date_rows` was executed on all requested date rows and preserves their source-selected Sunday appointments (same row multiset); it does not implement these Sunday policy corrections. The actual shipped package daily files and the supported design daily exports were read directly, without rebuilding.

Four fully captured dates show **six non-Psalm appointment mismatches each**, totaling **24 per output lane**:

| Actual date | Reader assignment | Existing daily assignment |
|---|---|---|
| 2027-02-21 | Third Meshir | Second Amshir |
| 2027-02-28 | Fourth Meshir | Third Amshir |
| 2028-01-09 | Second Day of Nativity | Generic fifth Koiahk/Kiahk |
| 2027-09-05 | First Nesi, on numeric Mesore 30 | Generic fifth Mesore/Mesra |

The Tobe30 and Meshir7 probes additionally prove caption/context selection differences against cached/current source titles; no full-table mismatch is asserted for those context-only dates.

Underlying proper tables confirm all six non-Psalm assignments for the three canaries:

- Joyful29 Paope 2026-11-08 corresponds to AnnualReadings Baramhat29 and Luke1:26–38, not generic fifth Paope. Both existing daily lanes match its six non-Psalm readings; the retained fifth-Sunday label in the title is not itself a content conflict.
- Post-Nativity 2028-01-09 corresponds to AnnualReadings Koiahk30, including Galatians4:19–5:1, 1John4:15–5:4, Acts13:36–43 and John1:1–13. The local C# source already explicitly handles Koiahk30 Sunday; existing daily exports nonetheless select the wrong generic table. This is a source/calendar-selection propagation conflict, not missing underlying post-Nativity data.
- Mesore30 2027-09-05 corresponds to SundayReadings Nesi1, including 2Thessalonians2:1–17, 2Peter3:1–18, Acts2:14–21 and Matthew24:3–35. Numeric Mesore and liturgical Nesi must stay separate. The 2026-09-06 probe is an actual numeric Nesi1 context but has no whole-table capture in this review.

### Underlying table / source-data conflicts

Third and Fourth Meshir are genuinely different underlying tables, not merely changed captions. Their six non-Psalm readings match their respective SQLite seeds:

| Slot | Third — 2027-02-21 | Fourth — 2027-02-28 |
|---|---|---|
| Vespers Gospel | John5:39–47 | Luke17:1–10 |
| Matins Gospel | John12:44–50 | Luke17:11–19 |
| Pauline | Hebrews3:1–4:2 | 1Corinthians1:1–16 |
| Catholic | Jude1:14–25 | James1:13–21 |
| Praxis | Acts20:7–16 | Acts8:5–13 |
| Liturgy Gospel | John6:27–46 | Luke19:1–10 |

Distinct source-data conflicts remain unchanged:

1. **Fifth Pashons / Paone / Epep:** Reader captures at 2026-06-07, 2024-07-07, 2028-08-06 all print **Acts24:1–9**, with the Ananias/Tertullus/Felix body, and agree in all nine literal references. SQLite SundayReadings65/66/62 and generated cycle rows retain **Acts14:1–9**. The existing date-resolved daily outputs already use Acts24:1–9; this is a cycle-source inconsistency, not an incorrect daily Praxis on those three dates.
2. **Additional independently found conflict:** actual fifth Thoout 2021-10-10 prints and includes **Acts18:9–21**. SQLite SundayReadings56 and its generated cycle row retain **Acts18:9–12**. The supported date-resolved design daily output already includes Acts18:9–21.

No seed, SQLite row, or generated export was repaired.

### Data projection / order conflicts

All **12 supported design daily tables** serialize ordinary Scripture slots in an order different from the captured service order. Of **9 shipped-year package tables**, **5** differ in order. The JSON mismatch report retains exact ordered rows; reference membership agreement is not treated as order agreement. The three supported historical/future tables outside 2026–2028 are explicitly unshipped in the package, not falsely reported as missing shipped dates.

### Psalm source-convention holds

All 36 Psalm appointments retain their literal Reader heading/body, source order, and hashes. Their underlying numeric seeds and existing display rows are included in the mismatch report, but canonical equivalence is unresolved until edition- and text-qualified verse alignment is available. Valid-looking chapter/verse numbers do not remove that requirement.

## Executed verification and limits

Command (exit 0):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /Users/ga/workspace/lectionary-comprehensive-audit-2026-10-07/sunday-independent-review/review.py
```

- Ten bounded in-memory corruption probes were detected: omitted/reordered document, wrong civil date/context, truncated reference, body-byte drift, mislabeled reference image, Third/Fourth swap, Acts24→14 substitution, and improper canary promotion. No production mutation was made.
- Thirty-three exact implementation/SQLite/current-data input files were hash-bound before and after the review execution and remained unchanged. The final receipt also binds all 800 producer source files and every final review artifact.
- .NET is unavailable here. The C# Sunday loop and special/feast precedence were inspected, and its isolated Sunday-branch arithmetic is explicitly labeled a **transcribed diagnostic**, not an executed C# API result. Node package calendar/classification and the actual Python resolution function were executed.
- One initial review execution failed on a review-only numeric parser field-name mismatch; it was corrected to the actual `normalized_segment` contract and rerun successfully. A missing optional BeautifulSoup dependency was avoided with stdlib HTML parsing; nothing was installed. These were reviewer infrastructure/script issues, not source defects.
- No core/calendar source, generated data, SITE, vault, build, parent tests, installation, deployment, commit, push, or publication was changed/run. The loaded Coptic lectionary skill's source-access reference was updated separately with reusable saved-Sunday qualification safeguards; no vault content was touched.

## Main deliverables

`accepted-oracle.json`; `per-context-verdict-ledger.json`; `seed-verdict-ledger.json`; `document-verdicts.json`; `calendar-data-mismatches.json`; `calendar-context-comparison.json`; `publisher-rules-verification.json`; `executed-package-calendar.json`; `executed-calendar-resolution.json`; `corruption-probes.json`; `hash-checks.json`; `visual-index.json`; `visual-verdicts.json`; `supported-policy-survey-review.json`; exact source/implementation hash manifests; final receipt; reproducible `review.py`; and 39 final readiness/reference contact sheets.
