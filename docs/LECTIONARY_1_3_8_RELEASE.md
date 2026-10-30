# Lectionary 1.3.8 follow-up report

## Scope and provenance

Combined Mark, 1 Timothy and Luke follow-up against authenticated published 1.3.7. The source-specific implementations and reports are integrated in one candidate. Component runs remain diagnostic until the complete frozen candidate, clean-source artifact and consumer acceptance pass. George's latest instruction authorizes confident commit/push and npm publication; the earlier Mark instruction also covers the local consumer pin and lectionary regeneration. No site push or deployment is authorized by this report. Dirty candidate metadata remains truthful; only a fresh build from the final committed source can record clean release provenance.

Authenticated predecessor: `@andraws/lectionary-data@1.3.7`, registry `https://registry.npmjs.org`, resolved latest at `2026-10-30T15:03:42.748306+00:00`. Integrity: `sha512-dw+mJ8msUB74tezQFZ8CSw2irSyI9pW94IakftrzdiNUgPfaUT7ZnxDP9AL352rbPXPoI+DUviMkfpuD2mH2GA==`. All 11 members were reauthenticated before this report was rendered. Reverse SHA-256: `4b785a5c626eaf4809f74738bfb3be05d7c8d0ae095b51bf98e72cad55559bf9`.

The compressed frozen predecessor subset is `sources/mark-followup-1.3.8/published-1.3.7.json.gz`, SHA-256 `c67a9d2699a368f028850e52ebdc3568dccdc327a5ab8afafebe794b47d7d1e5`. The independent pre-candidate source oracle is `sources/mark-followup-1.3.8/independent-acceptance-oracle.json`, SHA-256 `2d0dcb7c2072de7965ff0ab75af3deab0fd313143afe44b894ead7dcc0ada153`. It is source acceptance evidence, not candidate approval. No candidate-generated membership ledger or historical fixture-policy renewal is used.

## L1-L10 dispositions

| ID | Reproduced | Action or hold |
| --- | --- | --- |
| L1 | Yes | Hold one reverse witness and its two dated occurrences; malformed source heading does not establish 3-9. |
| L2 | Yes | Hold six exact working Tuesday appointments, not Monday or Tuesday Sixth Hour. No replacement added despite separately retained Third Hour evidence. |
| L3 | Yes | Add four inactive candidates beside four preserved historical witnesses. Third/Ninth/Eleventh remain Reader coverage holds; printed Eleventh exists. |
| L4 | Yes | Every Pascha display label is source-qualified and Coptic-form; Palm/Hosanna and Bright Saturday aliases normalize. Q1 remains unanswered, so the recommended Coptic form is used. |
| L5 | Yes, count corrected | 30 records carry 60 Kiyank tokens, not 60 records; normalize 30 display labels. Normalize 19 Ninevah display labels. Raw text retained. |
| L6 | Yes | Both Hator 11 Vespers witnesses carry conflict metadata. No selection or saint association; Q-L1 open. |
| L7 | Rows yes; absent evidence no | Six requested annotations, with existing retained Reader evidence and statuses preserved. Old inactive Mark 16 lead means the whole chapter. |
| L8 | Yes | No reading, span, status or catalog change. Q-L2 open. |
| L9 | Yes, conditional narrowing | Exclude exactly three stale legacy Psalms per year without changing status. Preserve supported pending counts 7/22/7, including numeric Sunday source coordinates. |
| L10 | Requested inventory supplied | All 21 service/hour groups, 176 predecessor source witnesses, literal printed tables and indexed retained Reader captures are on the full check sheet. No blanket promotions. |

### Exact affected occurrence identities

The following table contains the complete source-qualified metadata/hold target set, including the four new L3 candidates. Identity keys alone are not unique occurrence selectors. The machine-readable companion is [identities-and-dispositions.json](reviews/mark-followup-1.3.8/identities-and-dispositions.json). L4/L5 apply display-only to their complete source cohorts; L8 exact unchanged selectors and all L10 baseline identities are preserved in the check sheet and independent oracle.

| Identity | Source family / kind | Raw occasion / calendar | Hour / slot | Source reference | Status / removal | Locator |
| --- | --- | --- | --- | --- | --- | --- |
| rid_cdab176cfc55e6981df0 | ordinary_date_resolved / copticchurch_date | Hatur 11 / Hator 11 |  / Gospel | Matt 10:24-33 | current_public_or_local_reference /  | https://copticchurch.net/readings?g_year=2023&g_month=11&g_day=21; cache/copticchurch_html:row 14462; source_ref=Matt 10:24-33 |
| rid_10a2de1e2fe898df43b5 | katameros_cycle / katameros_cycle | Hatur 11 / Hatur 11 |  / vespers_gospel | Mark 14:3-9 | current_public_or_local_reference /  | sources/katameros-api/Core/KatamerosDatabase.db:row 882; source_ref=Mark 14:3-9 |
| rid_24a3269b0d1a1fb0412d | ordinary_date_resolved / copticchurch_date | Mesra 7 / Mesra 7 |  / Gospel | Mark 14:39 | pending_coptic_reader_review /  | https://copticchurch.net/readings?g_year=2024&g_month=08&g_day=13; cache/copticchurch_html:row 17111; source_ref=Mark 14:39 |
| rid_6297f04e598f02483db6 | holy_pascha_curated_day_hour / pascha_day_hour | Tuesday / Tuesday &#124;&#124; Tuesday &#124; Eleventh Hour | Eleventh Hour / Gospel | Jn 8:51-59 | pending_coptic_reader_review /  | out/data/pascha_day_hour_index.csv:row 23237; source_ref=Jn 8:51-59 |
| rid_3503dab946c9a441f29a | holy_pascha_curated_day_hour / pascha_day_hour | Tuesday / Tuesday &#124;&#124; Tuesday &#124; First Hour | First Hour / Gospel | Jn 11:12-24 | pending_coptic_reader_review /  | out/data/pascha_day_hour_index.csv:row 23242; source_ref=Jn 11:12-24 |
| rid_68809512622d19856234 | holy_pascha_curated_day_hour / pascha_day_hour | Tuesday / Tuesday &#124;&#124; Tuesday &#124; Ninth Hour | Ninth Hour / Gospel | Matt 21:23-27 | pending_coptic_reader_review /  | out/data/pascha_day_hour_index.csv:row 23247; source_ref=Matt 21:23-27 |
| rid_d1cf895fb56180180bb0 | holy_pascha_curated_day_hour / pascha_day_hour | Tuesday / Tuesday &#124;&#124; Tuesday &#124; Third Hour | Third Hour / Gospel | Mark 11:11-19 | pending_coptic_reader_review /  | out/data/pascha_day_hour_index.csv:row 23256; source_ref=Mark 11:11-19 |
| rid_dea460583107611686de | holy_pascha_curated_day_hour / pascha_day_hour | Tuesday / Tuesday &#124;&#124; Tuesday &#124; Third Hour | Third Hour / OT1 | Isa 5:20-30 | pending_coptic_reader_review /  | out/data/pascha_day_hour_index.csv:row 23254; source_ref=Isa 5:20-30 |
| rid_fcbca4c8026ae9ed4e8f | holy_pascha_curated_day_hour / pascha_day_hour | Tuesday / Tuesday &#124;&#124; Tuesday &#124; Third Hour | Third Hour / OT2 | Jer 9:12-19 | pending_coptic_reader_review /  | out/data/pascha_day_hour_index.csv:row 23255; source_ref=Jer 9:12-19 |
| rid_6a749188726ed430761c | holy_pascha_curated_day_hour / pascha_day_hour | Wednesday of Holy Pascha / Wednesday &#124; Eleventh Hour | Eleventh Hour / Psalm | Ps 6:2-3 | pending_psalm_equivalence_unresolved /  | out/data/pascha_day_hour_index.csv:row 77; source_ref=Ps 6:2-3; Ps 69:17; John 12:27-36 |
| rid_494b4f4a32be5964f7a7 | holy_pascha_curated_day_hour / pascha_day_hour | Wednesday of Holy Pascha / Wednesday &#124; Sixth Hour | Sixth Hour / Psalm | Ps 83:2,83:5 (LXX Ps 82:2; Ps 82:5) | pending_psalm_equivalence_unresolved /  | out/data/pascha_day_hour_index.csv:row 69; source_ref=Ps 83:2,5; John 12:1-8 |
| rid_ec764e70bc1afcf5a3fc | holy_pascha_curated_day_hour / pascha_day_hour | Wednesday of Holy Pascha / Wednesday &#124; Third Hour | Third Hour / Psalm | Ps 41:1,41:6 (LXX Ps 40:1; Ps 40:6) | pending_psalm_equivalence_unresolved /  | out/data/pascha_day_hour_index.csv:row 65; source_ref=Ps 41:6,1; Luke 22:1-6 |
| rid_d65723c38c9c1d636c4e | holy_pascha / pascha_source_text | Wednesday Eve / Wednesday Eve &#124; Ninth Hour | Ninth Hour / Gospel | Matt 23:29-36 | pending_coptic_reader_review /  | out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6916; source_ref=Matt 23:29-36 |
| rid_aea37d12f9fcde6a714f | holy_pascha / pascha_source_text | Wednesday Eve / Wednesday Eve &#124; Ninth Hour | Ninth Hour / Prophecy | Hos 9:14-10:2 | pending_coptic_reader_review /  | out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6875; source_ref=Hos 9:14-10:2 |
| rid_bfedafb928b1c2a873a2 | holy_pascha / pascha_source_text | Wednesday Eve / Wednesday Eve &#124; Third Hour | Third Hour / Gospel | Matt 24:36-51 | pending_coptic_reader_review /  | out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6623; source_ref=Matt 24:36-51 |
| rid_628304aab06e6513191b | holy_pascha / pascha_source_text | Wednesday Eve / Wednesday Eve &#124; Third Hour | Third Hour / Prophecy | Amos 5:18-27 | pending_coptic_reader_review /  | out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6545; source_ref=Amos 5:18-27 |
| rid_d07db8507f5c44129ec1 | consecration / special_service | consecration / consecrations_monk |  / main_readings | Mark 8:34-9:1 | current_public_or_local_reference /  | https://copticreader.org/app/#/document; build_special_service_reference.py curated rows:row 123; source_ref=Mark 8:34-9:1 |
| rid_10a2de1e2fe898df43b5 | myron_consecration / special_service | myron_consecration / consecrations_oil_myron_consecration |  / main_readings | Mark 14:3-9 | current_public_or_local_reference /  | https://copticreader.org/app/#/document; build_special_service_reference.py curated rows:row 140; source_ref=Mark 14:3-9 |
| rid_efb81984aa3123a4af0a | myron_consecration / special_service | myron_consecration / consecrations_oil_oil_of_gladness |  / offering_of_morning_incense | Mark 16:1-20 | current_public_or_local_reference /  | https://copticreader.org/app/#/document; build_special_service_reference.py curated rows:row 174; source_ref=Mark 16:1-20 |
| rid_10a2de1e2fe898df43b5 | myron_consecration / special_service | myron_consecration / consecrations_oil_pre_sanctified_chrism |  / second_liturgy_liturgy_of_the_word | Mark 14:3-9 | current_public_or_local_reference /  | https://copticreader.org/app/#/document; build_special_service_reference.py curated rows:row 190; source_ref=Mark 14:3-9 |
| rid_3d206cb8f6b88bbc796b | wedding_crowning / special_service | wedding_crowning / holy_matrimony_main |  / main_readings | Eph 5:22-6:3 | current_public_or_local_reference /  | https://copticreader.org/app/#/document; build_special_service_reference.py curated rows:row 210; source_ref=Eph 5:22-6:3 |
| rid_99b65b301c403b103eae | wedding_crowning / special_service | wedding_crowning / holy_matrimony_main |  / main_readings | Matt 19:1-6 | current_public_or_local_reference /  | https://copticreader.org/app/#/document; build_special_service_reference.py curated rows:row 213; source_ref=Matt 19:1-6 |

## 1 Timothy and Luke disposition

Source-specific identity ledgers form part of this report:

- [Metadata defects and identities](reviews/timothy-luke-metadata-1.3.8/report.md), [source-qualified scope](reviews/timothy-luke-metadata-1.3.8/scope.json), [endpoint groups and dates](reviews/timothy-luke-metadata-1.3.8/endpoint-conflicts.json).
- [Special-service and Psalm report](reviews/timothy-luke-evidence-1.3.8/REPORT.md), [45 exact service targets](reviews/timothy-luke-evidence-1.3.8/retained-evidence.md), [qualified annotations and exceptions](reviews/timothy-luke-evidence-1.3.8/verification.json).
- [Composite/provenance reproduction and pair inventory](reviews/luke-composites-1.3.8/REPORT.md).

| ID | Reproduced against 1.3.7 | Applied disposition |
|---|---|---|
| T-L1 | Yes, package-wide totals differ from brief | 2,326 removed-witness true claims cleared; explicit false added/changed on 3,253 rows. All 4,509 removed predecessor views report not occurring before the 52-pair merge. |
| T-L2 | Yes | 25 Hatour 24 views get exact date-only Synaxarium titles; split witnesses remain inactive and raw titles survive. |
| T-L3 | Yes | 1,090 cycle views get source-qualified keys. Active single-key counts: 156 Great Lent, 64 Holy Fifty, plus one two-key Holy Fifty view. |
| T-L4 | Yes | Display-only spellings follow LK2's later Hatour recommendation. Raw month names survive. |
| T-L5 | Yes | README documents both guaranteed schemas; daily `day_titles` remains optional. No synthetic ecclesiastical rank added. |
| T-L6 | Targets found; capture premise differs | Together with LK7: 34 captured rows receive actual evidence/current authority, 11 print-only rows remain unverified. Lakkan marker authenticates the complete Pauline body and service name, not whole-table equality. |
| T-L7 | Yes, one source-locator correction | Exactly seven low-priority appointments added. Water Liturgy already has a retained Reader capture, not a seventh copticchurch locator. |
| LK1 | Yes | Both three-Gospel Abib 26 tables flagged, six witnesses, no choice or appointment changes. |
| LK2 | Yes | Thirteen display month forms normalized; Q-LK2 stays open while its recommended default is used. |
| LK3 | Yes | Actual source weekdays and feast sentinel names used. Two inactive week-49 Exodus witnesses remain explicitly unresolved. |
| LK4 | Yes; Tout 8 longer witness already inactive | Four named witnesses flagged. No endpoint changes. Report-only inventory: 31 current groups across 365 exact dated slots. |
| LK5 | Yes, all 52 pairs inactive | Merge proven pairs only; preserve all 104 ordered originals, raw provenance and removed state. No daily membership changes. |
| LK6 | Yes, 181 JSON objects; 226 does not reproduce | Baseline has 198 JSON-containing provenance rows, 207 requiring transport. Short plain summaries replace public blobs; exact structured evidence remains reversible and authenticated. No private `_review_original_row` token in daily output. |
| LK7 | Yes; 34 already have retained captures | Statuses unchanged. Attach actual capture evidence and established authority tier; keep 11 Agpeya/Palm printed witnesses unverified with editions and check-sheet items. |
| LK8 | Yes | 145 synthetic year triples emptied and disclosed separately. Genuine source observations survive. |
| LK9 | Four incorrect annotation views | Qualify MT before conversion; preserve 37 held/non-MT views and exact edition exception. Daily annotation-only deltas: 2026-05-23, 2027-06-12, 2028-05-27. |

## Daily counts against the published predecessor

| Year | Dates before | Dates after | Readings before | Readings after | Delta | Pending before | Pending after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | 365 | 365 | 4088 | 4078 | -10 | 10 | 7 |
| 2027 | 365 | 365 | 4079 | 4069 | -10 | 25 | 22 |
| 2028 | 366 | 366 | 4096 | 4087 | -9 | 10 | 7 |

Counting unit: every unfiltered serialized appointment row in every daily date array. All civil dates remain present. L1 removes one row in 2026 and one in 2027; L2 removes six per year; L9 removes three per year. No other reading-count change is authorized. The combined reverse index has 12,282 rows: 12,330 predecessor rows, four held Mark candidates, and a 52-row reduction from merging inactive source pairs while preserving all 104 original witnesses. Projection-active and publicly current reverse populations retain their distinct metadata semantics.

## Full 2026 Pascha before and after

[Complete table: Palm Sunday through Good Friday, every daily row](reviews/mark-followup-1.3.8/pascha-2026-before-after.md). Columns include actual service, hour, slot, reading, status and `display_label` in physical array order. Neither matching totals nor a populated date is presented as complete Reader service verification.

## Abib 26 before and after

[Complete 2027-08-02 daily arrays](reviews/timothy-luke-metadata-1.3.8/2027-08-02-before-after.md), all 11 appointments before and after, include raw source locators, identities, statuses and display labels. The disputed Gospel choices are unchanged.

## Complete check sheet and open questions

The [full check sheet](../coptic-reader-check-sheet.md) also includes the combined 1 Timothy and Luke confirmations, source conflicts, endpoint inventory and print-book edition questions. It contains all L1-L10 follow-up targets, every Tuesday hour, all three missing Reader Eve-of-Wednesday hours with actual printed evidence, service-book witnesses and all 21 L10 service/hour groups. [Q-L1, Q-L2 and Q-L3](../open_questions_for_george.md) remain unanswered. Q1 has no new answer; Coptic eve labels use its recommended default.

## Contracts and tests

The source-owned runtime overlay runs after the existing H/K/R repairs, without changing the historical design membership gate. Holds have explicit boolean inactivity so unknown-status refusal is not weakened. Raw source title, locator, calendar keys, coordinates, composite spans and source disclosures are retained. New candidates do not remove the old historical rows. Exact emitted-row qualification rejects evidence/context rebinding, coordinate edits, type substitutions and unauthorized reactivation. Whole-date comparison first authenticates the independently projected successor arrays and only then replays the historical cached-source comparator against pinned predecessor rows.

The five-hour check accounts separately for 19 current eve hours and six explicitly held Reader gaps across five eves. It does not claim 25 current hours. The duplicate-set check compares complete non-Psalm day-hour Gospel/prophecy sets across distinct days, not an isolated shared Gospel or the same-day H5 repetition. The pending allowance binds all 36 retained occurrences to exact date/source/coordinates and disclosure hash; no arbitrary pending status is admitted.

Observed RED: the seven new package tests failed against the published predecessor; retained log [RED-node.txt](reviews/mark-followup-1.3.8/RED-node.txt) records child exit 1. Focused Python tests include complete valid controls and source, context, coordinate, lifecycle, type, omission, addition and order corruptions. Actual builder/test commands and fresh results are recorded in [verification.md](reviews/mark-followup-1.3.8/verification.md). Full final acceptance belongs to the parent after source freeze.

## Final combined validation

[Final full-suite and artifact validation](reviews/final-validation-1.3.8.md) records 1,235 Python tests passed, 16 retained skips, 6,183 subtests passed, and all 112 Node tests passed. Initial failed runs, their test-domain classification and complete corrected replays are disclosed there. Clean-clone tarball and registry publication remain separate acceptance steps.

## Clean-source finish for the parent

1. Review all source/generated diffs and run the complete mixed Python and full Node inventories in the uv Python 3.11 dependency environment. Preserve the historic fixture/policy pairings; do not refresh a ledger from candidate output.
2. Make the one authorized repository commit with the approved source and candidate data. Do not claim the dirty candidate metadata identifies the final source. A second artifact-only commit is not required by this handoff.
3. Clone that committed source into a second fresh release checkout. Verify `git status --short` is empty before running `node scripts/build_npm_package.mjs` through the same uv environment. The generated metadata must naturally record that committed revision and `source_tree_dirty: false`; never force the flag or hash.
4. Compare every packed non-provenance member to the reviewed candidate; only expected clean-provenance `meta.json` differences are permitted. Run strict integrity, cached-source comparison, exact npm pack/install tests and artifact hash checks in the release clone. Parent owns final integrated review and any currently authorized repository, registry or site work. Never pin a nonexistent registry 1.3.8; keep a local candidate isolated until final integrated acceptance and the parent's release decision.
5. If adding final receipts changes the source commit, rebuild from that final committed source rather than editing metadata. The release tarball may remain uncommitted as explicitly coordinated by the parent.
