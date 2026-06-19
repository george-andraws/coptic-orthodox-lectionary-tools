# Phase 2b Addendum — SUS Pascha Source Probe and Psalm Numbering Audit

- Date: 2026-06-15 PDT
- Scope: measurement/report only
- Dataset/parser/schema/verifier changes: **none intended**
- Report artifact only: `audit_artifacts/phase2b_sus_source_psalm_numbering_2026-06-15.md`

## Executive summary

1. The live old SUS/St. Pishoy Nashville PDF URL is dead:
   - `https://suscopts.org/stpishoynashville/pascha%20book.pdf` returned HTTP `404`.
   - Search and current SUS/deacons sitemaps did not expose a current live Holy Pascha book PDF.
2. The Internet Archive has full PDF captures of that old URL. I downloaded the full 2022 capture, which is byte-identical to the 2011 capture.
   - Archived URL source: `https://web.archive.org/web/20220902045824if_/https://suscopts.org/stpishoynashville/pascha%20book.pdf`
   - PDF SHA256: `213d7404fb0aa8da925815477dd24a8703162d0e0672d8e69002a12a6ba2512f`
   - Size: `7,868,151` bytes
   - Pages: `1,243`
   - Metadata title: `Holy Pascha Book`
   - Metadata author: `CopticChurch.net - St. Mark's, Jersey City, NJ`
3. Important correction: the archived PDF is **not clearly a current SUS-published/Coptic Reader book**. It is an old St. Mark / CopticChurch.net Holy Pascha book hosted at the old SUS path.
4. The archived PDF does **not** state “Psalms = Septuagint” in extracted text. It states: `Scripture taken from the New King James Version`.
5. The archived PDF is bilingual/trilingual in practice: the English Psalm headings are NKJV/Masoretic-style, while Coptic/Arabic Psalm labels visibly use liturgical/LXX-style chapter numbers. The repo’s St. Mary source-text index and stored dataset store the **English heading** convention, i.e. Masoretic/NKJV-looking Psalm refs.
6. After correcting for Psalm convention, the archived SUS-path PDF still does **not exactly match** George’s Coptic Reader Wednesday Day fixture.
   - Non-Psalm fixture matches: `15/17`.
   - Psalm comparison is not safe as a pure numeric diff yet because the Coptic Reader fixture itself contains apparent numbering inconsistencies if it is supposed to be standard LXX.
   - Content-aware Psalm comparison suggests the Psalm verses mostly align, but this needs screenshot-level confirmation for Third and Sixth Hour Psalm labels.
7. I would **not** promote this archived SUS-path book as a trustworthy auto-extension source for unscreenshotted Holy Week days. It is useful as a comparator, not a controlling source.
8. Re-checks under corrected Psalm convention:
   - Phase 2a `Id=46` vs `Id=53`: conclusion unchanged. The live Katameros API supports the shorter reading, but the labels in the prior report were Masoretic/NKJV, not LXX canonical.
   - Hatur 8 duplicate: conclusion unchanged for dedupe. But if canonical storage becomes LXX, the Psalm chapter should normalize from MT `Ps 68` to LXX `Ps 67` before display/diff.

## 1. SUS Pascha book fetch/provenance

### Live URL attempt

Tried:

```text
https://suscopts.org/stpishoynashville/pascha%20book.pdf
```

Result:

```text
HTTP 404
HTML error page, 17,282 bytes
```

Additional searches performed:

- `site:suscopts.org/stpishoynashville Pascha PDF "Pascha Book"`
- `site:suscopts.org filetype:pdf "Holy Pascha" "Psalm" "Wednesday" "Eleventh Hour"`
- `site:deacons.suscopts.org Pascha book PDF "Holy Pascha"`
- SUS/deacons sitemap and WordPress media/search endpoints.

Current live result: **no current SUS Holy Pascha book PDF found**.

### Archived SUS-path PDF

Internet Archive CDX showed successful PDF captures:

| Timestamp | Original | Status | MIME | Digest |
|---|---|---:|---|---|
| `20111216060000` | `http://suscopts.org:80/stpishoynashville/pascha%20book.pdf` | 200 | `application/pdf` | `HXCLWYZDXGJESCZZGJE4ESYQUGFZ63QI` |
| `20210917003557` | `https://suscopts.org/stpishoynashville/pascha%20book.pdf` | 200 | `application/pdf` | `TLHGQHZEOXZ2BLZZMU6VX4OCXP3K6SCJ` |
| `20220902045824` | `https://suscopts.org/stpishoynashville/pascha%20book.pdf` | 200 | `application/pdf` | `HXCLWYZDXGJESCZZGJE4ESYQUGFZ63QI` |

Downloaded files:

| Capture | Bytes | SHA256 prefix | Assessment |
|---|---:|---|---|
| `20111216060000` | 7,868,151 | `213d7404fb0aa8da` | Full PDF |
| `20210917003557` | 1,048,576 | `ec9599d8d2ca1cc4` | Likely truncated |
| `20220902045824` | 7,868,151 | `213d7404fb0aa8da` | Full PDF, same as 2011 |

Used for extraction:

```text
/tmp/coptic_sus_pascha/sus_pascha_20220902045824.pdf
```

PDF metadata extracted by PyMuPDF:

```json
{
  "format": "PDF 1.5",
  "title": "Holy Pascha Book",
  "author": "CopticChurch.net - St. Mark's, Jersey City, NJ",
  "creator": "PScript5.dll Version 5.2.2",
  "producer": "Acrobat Distiller 6.0 (Windows)",
  "creationDate": "D:20060412015947-04'00'",
  "modDate": "D:20060412135913-04'00'",
  "encryption": "Standard V4 R4 128-bit RC4"
}
```

Copyright/version statement found in extracted text:

```text
Scripture taken from the New King James Version. Copyright © 1979,
1980, 1982 by Thomas Nelson, Inc. Used by permission. All rights
reserved.
```

No extracted occurrence of `Septuagint` was found in this PDF.

## 2. Extracted Wednesday Day reading references from archived SUS-path PDF

Extraction method:

- Python/PyMuPDF text extraction.
- Pages around PDF pages `420-522`.
- Reference headings only, not homily/exposition/commentary prose.

### Extracted references

| Hour | Extracted references from archived SUS-path PDF |
|---|---|
| First Hour | `Exodus 17:1-7`; `Proverbs 3:5-14`; `Hosea 5:13-6:3`; `Sircah 3:12,17,26-30, Sirach 2:1-15`; `Psalm 51:4 and 33:10`; `John 11:46-57` |
| Third Hour | `Exodus 13:17-22`; `Sirach 22:7-18`; `Job 27:16-20`; `Proverbs 4:4-27, 5:1-4`; `Psalm 41:6 and 1`; `Luke 22:1-6` |
| Sixth Hour | `Exodus 14:13-15:1`; `Isaiah 48:1-6`; `Sirach 23:7-14`; `Psalm 83:2 and 5`; `John 12:1-8` |
| Ninth Hour | `Genesis 24:1-9`; `Numbers 20:1-13`; `Proverbs 1:10-33`; `Isaiah 59:1-17`; `Zechariah 11:11-14`; `Psalm 41:5,7,6`; `Matthew 26:3-16` |
| Eleventh Hour | `Isaiah 28:16-29`; `Psalm 6:2,3 and 69:17`; `John 12:27-36` |

### First test against George's Coptic Reader Wednesday Day fixture

Ignoring Psalm-numbering until normalized, the non-Psalm comparison is:

| Category | Count |
|---|---:|
| Fixture non-Psalm readings | 17 |
| SUS-path PDF non-Psalm readings | 22 |
| Non-Psalm fixture readings matched | 15 |
| Non-Psalm fixture readings missing | 2 |

Non-Psalm fixture items missing from archived SUS-path PDF:

```text
Sixth Hour | Memoirs of Job
Ninth Hour | Proverbs 1:11-35
```

Non-Psalm extras in archived SUS-path PDF not in the fixture:

```text
First Hour | Sircah 3:12,17,26-30; Sirach 2:1-15
Third Hour | Job 27:16-20
Third Hour | Proverbs 4:4-27; Proverbs 5:1-4
Sixth Hour | Isaiah 48:1-6
Ninth Hour | Proverbs 1:10-33
Ninth Hour | Isaiah 59:1-17
Ninth Hour | Zechariah 11:11-14
```

Conclusion: **No**, this archived SUS-path PDF does not exactly match the Coptic Reader Wednesday Day fixture. It should not be auto-promoted as trustworthy for all unscreenshotted Holy Week days.

## 3. Psalm numbering conventions by source

| Source | Convention observed/reported | Evidence | Confidence |
|---|---|---|---|
| Coptic Reader fixture | Intended/report says LXX. | User explicitly instructed: `Coptic Reader (LXX)`. Fixture also has LXX-looking entries such as `Psalm 50` vs external English/NKJV `Psalm 51`, `Psalm 32` vs `Psalm 33`, `Psalm 40` vs `Psalm 41`, and `Psalm 68` vs `Psalm 69`. | High for user intent; mixed for individual fixture labels, see warning below. |
| Katameros live API | Masoretic/NKJV. | User explicitly said confirmed. Live API Wednesday returns English refs such as `Ps 51:4`, `Ps 33:10`, `Ps 41:5-6`, `Ps 69:17`. | High |
| Archived SUS-path PDF | English headings are NKJV/Masoretic; Coptic/Arabic labels are liturgical/LXX-ish. | PDF states `Scripture taken from the New King James Version`; English headings show `Psalm 51:4 and 33:10`; same page's Coptic/Arabic Psalm label shows Coptic/Arabic liturgical numbering. No extracted `Septuagint` statement found. | High for English headings; medium for exact Coptic/Arabic verse offsets. |
| St. Mary source-text index | Stored index uses English/NKJV/Masoretic-looking refs. | `pascha_source_text_index.csv` has Wednesday First `Ps 51:4,33:10`, Ninth `Ps 41:5-7`, Eleventh `Ps 6:2,6:3,69:17`. | High for index; source book may also contain Coptic/LXX labels not represented in the CSV. |
| Stored dataset | Stored refs are mostly English/NKJV/Masoretic-looking across Pascha and Katameros cycle. | `pascha_day_hour_index.csv` stores Wednesday First `Ps 51:4; Ps 33:10`; Great Lent/Annual data derives from Katameros SQLite/API, which is Masoretic/NKJV. | High |

### Warning: fixture Psalm labels need screenshot-level verification

If the Coptic Reader fixture is supposed to be standard LXX chapter numbering, two fixture Psalm groups look inconsistent against the standard MT↔LXX chapter map:

| Hour | Fixture Psalm | External English/NKJV source Psalm | Standard chapter-only LXX normalization of external source | Issue |
|---|---|---|---|---|
| Third Hour | `Psalm 41:6`, `Psalm 41:1` | `Psalm 41:6 and 1` | LXX chapter should normally be `Psalm 40` | Fixture label matches MT/NKJV chapter, not standard LXX chapter. |
| Sixth Hour | `Psalm 83:2`, `Psalm 83:5` | `Psalm 83:2 and 5` | LXX chapter should normally be `Psalm 82` | Fixture label matches MT/NKJV chapter, not standard LXX chapter. |

Other fixture Psalm groups **do** look LXX-like:

| Hour | Fixture | External English/NKJV source |
|---|---|---|
| First Hour | `Psalm 50:6`; `Psalm 32:10` | `Psalm 51:4`; `Psalm 33:10` |
| Ninth Hour | `Psalm 40:6-8` | `Psalm 41:5,7,6` |
| Eleventh Hour | `Psalm 68:17` | `Psalm 69:17` |

So a pure numeric Psalm diff is still unsafe until George verifies whether the Third/Sixth Hour Coptic Reader Psalm labels were copied exactly or whether those two should be LXX-renumbered.

## 4. Verified LXX ↔ Masoretic Psalm chapter map

This is the chapter map to use before any cross-source Psalm diff. It is **not** a flat offset.

### Masoretic/Hebrew chapter to LXX chapter

| Masoretic/Hebrew Psalm | LXX Psalm |
|---|---|
| `1-8` | same |
| `9-10` | `9` |
| `11-113` | MT minus 1 |
| `114-115` | `113` |
| `116:1-9` | `114` |
| `116:10-19` | `115` |
| `117-146` | MT minus 1 |
| `147:1-11` | `146` |
| `147:12-20` | `147` |
| `148-150` | same |

### LXX chapter to Masoretic/Hebrew chapter

| LXX Psalm | Masoretic/Hebrew Psalm |
|---|---|
| `1-8` | same |
| `9` | `9-10` |
| `10-112` | LXX plus 1 |
| `113` | `114-115` |
| `114-115` | `116` split by verse range |
| `116-145` | LXX plus 1 |
| `146-147` | `147` split by verse range |
| `148-150` | same |
| `151` | no Hebrew counterpart |

### Verse-numbering note

The chapter map is necessary but not sufficient. Some Psalm verse numbers differ because of superscriptions/titles and tradition-specific verse numbering.

Concrete examples from this pass:

| English/NKJV/MT source ref | Coptic Reader fixture/ref-equivalent | Evidence |
|---|---|---|
| `Psalm 51:4` | `Psalm 50:6` | Same text: “That You may be found just when You speak...” |
| `Psalm 33:10` | `Psalm 32:10` | Same text: “The Lord brings the counsel of the nations to nothing...” |
| `Psalm 41:5,7,6` | likely `Psalm 40:6-8` | Same Psalm content cluster, but order/range normalization needs Coptic Reader screenshot confirmation. |
| `Psalm 69:17` | `Psalm 68:17` | Standard chapter shift; verse text aligns by content. |

Recommendation: implement canonical Psalm storage as LXX **with source convention metadata**, not by overwriting raw source refs. Store at least:

```text
source_ref
source_convention: mt_nkjv | lxx_liturgical | mixed_bilingual
canonical_lxx_ref
canonicalization_confidence
canonicalization_note
```

For display/input, convert between LXX and Masoretic/NKJV on demand.

## 5. Dataset internal Psalm mixing check

### Stored Pascha rows

`out/data/pascha_day_hour_index.csv` currently stores Psalm refs in English/NKJV-looking form. Examples:

```text
Wednesday First Hour | Ps 51:4; Ps 33:10
Wednesday Ninth Hour | Ps 41:5-6
Wednesday Eleventh Hour | Ps 6:2-3; Ps 69:17
Good Friday Ninth Hour | Ps 69:2,3,21
Palm Sunday Liturgy | Ps 80:3,1,2; Ps 64:1,2
```

The source markers are mixed (`api`, `St Mary Ottawa...`, `book`), but the visible Psalm convention is consistently English/NKJV/Masoretic-looking in the sampled rows.

### Great Lent / Annual cycle rows

Great Lent and Annual rows come from Katameros SQLite/API-style refs and are also Masoretic/NKJV-looking.

Examples:

```text
Great Lent Week 7 DayOfWeek 4 retained Matins Psalm: MT/NKJV Ps 63:1
Hatur 8 vespers psalm raw: 19.68:17,16,17 -> stored/displayed Ps 68:17; Ps 68:16
```

### Conclusion on internal mixing

I do **not** see evidence that stored Pascha Psalms are LXX while Great Lent Psalms are Masoretic, or vice versa. The stored dataset appears internally consistent in using English/NKJV/Masoretic-looking Psalm refs for both Pascha and Katameros cycle rows.

The real mixing is at the **source layer**:

- Bilingual/trilingual rite books may print Coptic/Arabic LXX labels alongside English NKJV labels.
- The current repo extracted/stored the English NKJV/Masoretic labels.
- George's Coptic Reader fixture is intended to be LXX/liturgical, but at least two Psalm labels need screenshot re-check.

## 6. Re-check: archived SUS-path PDF vs Coptic Reader fixture under Psalm normalization

### Strict numeric comparison without Psalm normalization

Not valid as a correctness score, but useful as a baseline:

| Category | Fixture count | Matched exactly |
|---|---:|---:|
| Non-Psalm readings | 17 | 15 |
| Psalm readings | 9 | 5 |
| Total | 26 | 20 |

### After Psalm normalization

A clean numeric score is blocked by the fixture Psalm-label inconsistency described above.

If I apply content-aware Psalm equivalence for the Wednesday Psalm lines, the Psalm content mostly aligns between the archived SUS-path PDF and the fixture. But even under that generous Psalm treatment, the source still fails to match the fixture exactly because of non-Psalm differences:

- Missing fixture item: `Sixth Hour | Memoirs of Job`
- Missing fixture item: `Ninth Hour | Proverbs 1:11-35`
- Extra SUS-path PDF items: `Sircah/Sirach 3/2`, `Job 27:16-20`, `Proverbs 4:4-27; 5:1-4`, `Isaiah 48:1-6`, `Proverbs 1:10-33`, `Isaiah 59:1-17`, `Zechariah 11:11-14`

Therefore the answer to the first SUS test is still: **No, this archived SUS-path PDF does not exactly match the Coptic Reader Wednesday Day fixture.**

## 7. Re-check: Phase 2a `Id=46` vs `Id=53` under correct Psalm convention

Prior state:

- `Id=46`: raw `M_Psalm_Ref = 19.63:1-1`
- `Id=53`: raw `M_Psalm_Ref = 19.63:1-1*@+19.64:2-4`

Those raw `19.x` refs came from the Katameros SQLite/API family, which is Masoretic/NKJV-looking.

Corrected convention interpretation:

| Raw/source ref | Source convention | LXX chapter-level canonical equivalent |
|---|---|---|
| `Ps 63:1` | MT/NKJV | LXX `Ps 62` chapter, exact verse needs verse-map validation |
| `Ps 64:2-4` | MT/NKJV | LXX `Ps 63` chapter, exact verse range needs verse-map validation |

External check already run in Phase 2b-1:

| Date | Live Katameros API Matins Psalm | Contains composite second Psalm? |
|---|---|---:|
| 2025-04-10 | `Ps 63:1` MT/NKJV | No |
| 2026-04-02 | `Ps 63:1` MT/NKJV | No |

Conclusion: the **data decision does not change**. Dropping the `Id=53` composite remains supported by live Katameros API. What changes is the language in reports/display: prior `Ps 63:1` was MT/NKJV notation, not LXX/liturgical canonical notation.

## 8. Re-check: Hatur 8 `Ps 68` under correct Psalm convention

Current stored/source row:

```text
AnnualReadings | Hatur 8 | vespers_psalm | raw_ref=19.68:17,16,17
```

Stored emitted segments after Phase 2a dedupe:

```text
Ps 68:17
Ps 68:16
```

Convention interpretation:

- Source family: Katameros SQLite/API style.
- Therefore the stored `Ps 68` is MT/NKJV-looking.
- Chapter-level LXX canonical equivalent is `Ps 67`, not `Ps 68`.

Conclusion: the **dedupe resolution does not change**. The repeated third segment is still a duplicate in the source string and should not emit twice.

But if the project moves to LXX canonical storage/display, Hatur 8 should be normalized from MT `Ps 68` to LXX `Ps 67` before future Psalm diffs. Exact verse numbering should be verified with a verse-level map before editing data.

## 9. Recommendations before the next data-changing phase

1. Resolve the Coptic Reader fixture Psalm-label contradiction before any Psalm diff becomes authoritative.
   - Specifically re-check Third Hour `Psalm 41:6,1` and Sixth Hour `Psalm 83:2,5` screenshots.
   - If Coptic Reader is truly standard LXX, these may need to be `Psalm 40...` and `Psalm 82...` equivalents.
2. Do not promote the archived SUS-path PDF as a controlling source for unscreenshotted Holy Week days.
   - It is old, not clearly current SUS/Coptic Reader, and does not match Wednesday exactly.
3. Use LXX as the canonical liturgical storage convention going forward, but keep raw source refs and source convention metadata.
4. Build Psalm canonicalization before rewriting verifier expectations.
   - Chapter seams must be explicit.
   - Verse offsets need a verified table, not a flat chapter offset.
5. Treat all prior Psalm mismatch counts as suspect until rerun through the canonical Psalm layer.
