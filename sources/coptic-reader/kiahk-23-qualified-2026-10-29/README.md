# Kiahk 23 — recovered retained Reader evidence

## Result and scope

**Confirmed:** the retained Coptic Reader capture selected **Thursday, January 1, 2026, 10:00 AM; Koiahk 23, 1742; 4th Week of Koiahk**. Its Matins Gospel is **Matthew 12:1–8**, not Matthew 17:1–9. The full multilingual rendered body contains every English verse 1–8, ending “For the Son of Man is Lord even of the Sabbath.”

This is recovered evidence originally captured October 7, 2026, **not a fresh app observation**. All 38 original files in this bounded capture directory were recovered and authenticated: seven full reading documents, reference/document screenshots, selected home/date/picker evidence, menus and ancillary navigation history. The retained preselection screen remains navigation history, not selected-date proof.

The controlling retained record is `sources/coptic-reader/matins-source-accepted-2026-10-07/evidence/ordinary-coverage-current/accepted-contexts-03.jsonl`, physical line 113, `id=AnnualReadings-113`. Its literal line is preserved as `retained-accepted-context.jsonl`; its original fields remain unchanged, including `review_status=qualified_exact_observed_date_table`, `genericTemplateQualification=false` and `seedSemanticStatus=calendar_coordinates_match_only_no_recurrence_claim`.

## Complete ordinary Scripture table, printed literally

| Document | Printed references |
|---|---|
| Vespers | Psalms 131:7,8; John 7:40-53 |
| Matins Prophecies | Explicit rubric: “No prophecies are read on this day.” |
| Matins Psalm and Gospel | Psalms 88:13-15; Matthew 12:1-8 |
| Liturgy Pauline | Hebrews 11:32-40 |
| Liturgy Catholic | James 5:7-13 |
| Liturgy Praxis | Acts 2:22-36 |
| Liturgy Psalm and Gospel | Psalms 77:61-63; Matthew 22:35-46 |

All nine tabbed source-reference headings were authenticated at the original line numbers and UTF-8 byte offsets. Every English numbered NT verse sequence was verified against its complete printed interval. The composite table hash, computed as SHA-256 of the seven `label + '\n' + full body` strings joined with a newline in retained document order, matches **340828acacebcb385a5220261a73574cc24a4d6954443f2865435b4e49e0de29**.

Do not silently normalize the printed Psalm numbers. The Matins printed Psalm body begins “Then You spoke in a vision to Your holy one…” and names David and his anointing; its printed label is Psalms 88:13-15. The local database separately uses Psalm 89:19-21 for its Matins slot. Exact edition/content alignment is distinct from accepting the source label.

## Authentication and bounded recovery

- `retained-authentication.json`: controlling ledger hash/line, original-context identity, per-document body hashes, literal references and complete English numbered verse lines.
- `retained-recovery-receipt.json`: all 38 recovered files, exact archive members, sizes and SHA-256 values; stable cloud archive identity before/after retrieval.
- `archive-manifest-bounded.json`: only the AnnualReadings-113 entries selected from the authenticated full archive manifest. Full manifest SHA-256 is **92082a73dbdb6cf885defcda395d45f403f95041a20d9137e875bc15569d0ebc**, matching the retained archive receipt; its Drive MD5 and size also matched.
- `retained-2026-01-01/`: original bytes, not reconstructed prose or regenerated images.

No full 9,354,731,560-byte archive was downloaded. After bounded range probes, recovery streamed 208,666,624 compressed bytes from a suffix range, resynchronized raw DEFLATE at a stored-block boundary, discarded warm-up through a validated PAX header, and accepted **only exact size/SHA-256 matches against the authenticated archive manifest**. The entire archive SHA-256/global gzip checksum was not recomputed. Recovery authenticity is the complete individual-member hash match to the authenticated manifest plus agreement with the independently retained accepted-context hashes. No unrelated archive members were written.

Selected home/date and both Matins reference screenshots were visually rechecked after recovery. Home and selected date are fully rendered, and the selected hour is 10:00 AM. Matins Gospel screenshot prints Matthew 12:1-8; the complete body, not the screenshot's visible viewport, establishes all eight verses.

## Local precedence evidence — code inspection, not executed C#

Exact source files are copied under `precedence-local/` and hash-bound in `precedence-source-manifest.json`. `.NET` is not installed here; no C# API/runtime result is claimed.

1. `Core/Repositories/LectionaryRepository.cs:79–120` evaluates special cases first, then registered feast constructors, then Lent, Pentecost, the qualifying Sunday 29th, ordinary Sunday, and finally annual weekdays. Thus registered constructed feasts can take precedence over Sunday; an ordinary saint-day annual row does not automatically override Sunday.
2. `Core/Factories/FeastsFactory.cs:21–49` registers Nativity/Paramoun and several other named feasts, **but not Kiahk 23**. `:55–68` picks the first qualifying registered feast; fixed Coptic entries are skipped during Easter offsets -8 through 0. This registry is not proof of a complete universal Church precedence policy.
3. `Core/Factories/SpecialCases/Kiahk.cs:26–48` explicitly handles Kiahk 30 on Sunday with the annual second-day-of-Nativity table, repeats Nativity when celebrated on Kiahk 28, and describes borrowing the fifth Hathor Sunday when Kiahk would have only three Sundays. Its literal `gregorianDate.Year + 1` calculation at line 41 must not be silently repaired or treated as independently verified Reader behavior.
4. `Core/Repositories/ReadingsRepository.cs:46–65` selects SundayReadings for the Sunday branch and AnnualReadings by fixed month/day only in the annual branch. Its Sunday loop counts forward from the selected Coptic date; do not promote that implementation to a generally correct ordinal algorithm. For a Sunday on Kiahk 23, its count is four, consistent with the fourth-Sunday seed.
5. `local-katameros-kiahk-rows.json` contains actual **read-only SQLite** rows and the database SHA-256. AnnualReadings 113 has `M_Gospel_Ref=40.12:1-8`, `L_Gospel_Ref=40.22:35-46`; SundayReadings 16 (fourth Kiahk) has `M_Gospel_Ref=41.3:28-35`, `L_Gospel_Ref=42.1:57-80`. These are database witnesses, not fresh Reader Sunday confirmation.

Calendar-only diagnostic: 2026-01-01 Thursday; 2027-01-01 Friday; 2028-01-02 Sunday; 2034-01-01 Sunday. On the latter dates, fixed-day weekday projection cannot replace the Sunday table merely because the numeric date is Kiahk 23. Exact Reader Sunday assignment remains a separate source check.

## Retained official Reader help

`official-reader-help-retained.html` is byte-identical to the already-qualified publisher help snapshot, SHA-256 **21b77dc3b6ceb40cf1d7e6174f914930b142b3439c4b1625499ccaf31f9cfb11**. Its retained source URL is `https://wiki.suscopts.org/index.php?title=Coptic_Reader&oldid=5`. This is retained official evidence, not a new web fetch.

- **Version 2.43, line 1091:** “Updated readings for Koiahk 23 for the commemoration of King David the Prophet.”
- **Version 2.81, line 749:** “Corrected Liturgy Gospel reading for Koiahk 23.”
- **Version 2.64, line 940:** “Fixed bug where the Sundays of Koiahk can be miscalculated during certain years.”
- **Dates, line 179:** after the configurable Day Transition Time, the Coptic day advances to the next day, including Saturday-night Vespers using Sunday's readings. The selected source hour is therefore material.

The changelog supports that Reader intentionally revised this commemoration's readings; it does **not** name the old/new Matins Gospel or prove why a particular external witness has Matthew 17. Preserve printed witnesses as their own editions rather than rewriting them into Reader provenance.

## Limits

This pack authenticates the exact retained 2026 dated table and provides read-only local precedence witnesses. It does not itself approve all-year recurrence, every collision, package implementation, release or publication. Parent-provided fresh 2027 evidence remains separately owned and is not relabeled as part of this retained capture. No builder, package data, site, vault, existing source, commit, push or publication was changed by this research lane.
