# Coptic Reader check sheet: Holy Week H1-H8

Baseline: published `@andraws/lectionary-data@1.3.6`, authenticated `sha512-FD4T8t3ETBZLaWX359BnLBqglKmV1UeoX2j0MGxiJ3g4aRsqANGErVqnB+M7sCKjXV0/Z2zH8ItUJgS2ZtFAag==`.

Coverage: 481 baseline appointments: 414 across the two Holy Pascha families, 17 existing source-qualified Pascha rows and 50 Bright Saturday rows, each listed exactly once. This includes every one of the 247 H8 working rows, all 9 pending-alignment rows in these families and all inactive witnesses. Reader source captures are shown separately. Named groups absent from one source are stated as absent evidence, not filled from memory. No fresh app retrieval occurred.

Retained Reader captures are copied into `sources/coptic-reader/holy-week-review-qualified-2026-10-29/`; full bytes and printed headings are pinned by `source-manifest.json`. Psalm labels below are literal Reader print, not newly approved MT coordinate conversions. The package keeps MT/NKJV primary references with LXX annotations.

## Immediate checks

- H1: all five hours remain on this sheet. Wrong curated Tuesday Eve rows held. Retained Reader resolves First and Sixth only. Third and Ninth have printed candidates only; Eleventh remains uncaptured.
- H2: Eve of Monday Third and Eleventh hours have retained Reader support. First, Sixth and Ninth remain evidence-only printed candidates. No inferred missing Gospel is supplied.
- H4: Good Friday Sixth has Reader John 19:13-27; old John 19:1-12 held only at Sixth.
- H5: Third and Ninth Matthew 26:17-19 both retained. Reader confirms Ninth; Third still needs capture. A blanket duplicate-non-Psalm prohibition would incorrectly delete a source-backed appointment.
- H6: retained Reader prints Ezekiel 43:5-11; Jeremiah witness held, Ezekiel source-backed addition.
- H7: retained Friday Sixth prints Galatians 6:14-18. Retained Friday Eleventh contains no Pauline reading. Galatians 3:1-6 stays historical. Thursday Eleventh Isaiah 19:19-25 remains unconfirmed current working plus printed witness, not promoted.
- R2 Kiahk 23 and R5 Amshir 10 are outside this worker's H1-H8 ownership. Parent must add those check-sheet sections; this file does not adjudicate them.

## Explicit raw-label mappings

| Source family | Raw Eve label | pascha_service | civil date offset from Pascha | Display |
|---|---|---|---:|---|
| `holy_pascha_curated_day_hour` | Monday Eve | `eve_of_tuesday` | -6 | Eve of Tuesday |
| `holy_pascha_curated_day_hour` | Tuesday Eve | `eve_of_wednesday` | -5 | Eve of Wednesday |
| `holy_pascha_curated_day_hour` | Wednesday Eve | `eve_of_thursday` | -4 | Eve of Thursday |
| `holy_pascha_curated_day_hour` | Great Thursday Eve | `eve_of_friday` | -3 | Eve of Friday |
| `holy_pascha` | Monday Eve | `eve_of_monday` | -7 | Eve of Monday |
| `holy_pascha` | Tuesday Eve | `eve_of_tuesday` | -6 | Eve of Tuesday |
| `holy_pascha` | Wednesday Eve | `eve_of_wednesday` | -5 | Eve of Wednesday |
| `holy_pascha` | Thursday Eve | `eve_of_thursday` | -4 | Eve of Thursday |
| `holy_pascha` | Great Thursday Eve | `eve_of_thursday` | -4 | Eve of Thursday |
| `holy_pascha` | Good Friday Eve | `eve_of_friday` | -3 | Eve of Friday |

An undated reverse appointment carries its offset and an empty civil date; each daily projection carries the actual civil date. Raw labels and calendar keys are not rewritten.

## Eve of Wednesday: First Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/tuesday--wednesday-eve--1st-hour.txt`; SHA-256 `5837bee002f933bb108d0c353682385be8464f2afdf8d13a228a8a4083fb6177`; title `Wednesday Eve (The First Hour)`.

- Line 12: Ezekiel 22:17-22
- Line 41: Ezekiel 22:23-29
- Line 139: Psalm 58: 13,14
- Line 153: Matthew 22:1-14

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Tuesday Eve | Gospel | Lk 13:23-30 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_e2d8832a22e439862231` | `out/data/pascha_day_hour_index.csv:row 23262; source_ref=Lk 13:23-30` |
| Curated: Tuesday Eve | OT1 | Zech 1:1-6 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_0f4e1a985963d3c3064d` | `out/data/pascha_day_hour_index.csv:row 23261; source_ref=Zech 1:1-6` |
| Curated: Tuesday Eve | Psalm | Ps 62:6-7 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_8be9daf4ab53e4424614` | `out/data/pascha_day_hour_index.csv:row 23263; source_ref=Ps 62:6-7` |
| Printed: Wednesday Eve | Gospel | Matt 22:1-14 | `historical_witness` | `historical_witness` | `rid_067caec0901dc9284fdd` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6413; source_ref=Matt 22:1-14` |
| Printed: Wednesday Eve | Prophecy | Ezek 22:23-28 | `historical_witness` | `historical_witness` | `rid_b938964452264e52d765` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6361; source_ref=Ezek 22:23-28` |
| Printed: Wednesday Eve | Prophecy | Ezek 22:17-22 | `historical_witness` | `historical_witness` | `rid_e5780cc9c4eea5ac6dec` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6338; source_ref=Ezek 22:17-22` |
| Printed: Wednesday Eve | Psalm | Ps 59:16-17 | `historical_witness` | `historical_witness` | `rid_71e7910ac7d138e71853` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6406; source_ref=Ps 59:16-17` |
| New Reader source | OT1 | Ezek 22:17-22 | absent | `current_confirmed_coptic_reader` | `rid_e5780cc9c4eea5ac6dec` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/tuesday--wednesday-eve--1st-hour.txt:line 12; sha256=5837bee002f933bb108d0c353682385be8464f2afdf8d13a228a8a4083fb6177` |
| New Reader source | OT2 | Ezek 22:23-29 | absent | `current_confirmed_coptic_reader` | `rid_92c0582ba78eb6dec784` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/tuesday--wednesday-eve--1st-hour.txt:line 41; sha256=5837bee002f933bb108d0c353682385be8464f2afdf8d13a228a8a4083fb6177` |
| New Reader source | Gospel | Matt 22:1-14 | absent | `current_confirmed_coptic_reader` | `rid_067caec0901dc9284fdd` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/tuesday--wednesday-eve--1st-hour.txt:line 153; sha256=5837bee002f933bb108d0c353682385be8464f2afdf8d13a228a8a4083fb6177` |

## Eve of Wednesday: Third Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Tuesday Eve | Gospel | Lk 13:31-35 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_b9224e7edb547a30e943` | `out/data/pascha_day_hour_index.csv:row 23271; source_ref=Lk 13:31-35` |
| Curated: Tuesday Eve | OT1 | Mal 1:1-9 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_f5ce91b8996a871b27ba` | `out/data/pascha_day_hour_index.csv:row 23270; source_ref=Mal 1:1-9` |
| Curated: Tuesday Eve | Psalm | Ps 13:3,13:5 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_493778d4a6a4ba640417` | `out/data/pascha_day_hour_index.csv:row 23272; source_ref=Ps 13:3,13:5` |
| Printed: Wednesday Eve | Gospel | Matt 24:36-51 | `historical_witness` | `historical_witness` | `rid_bfedafb928b1c2a873a2` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6623; source_ref=Matt 24:36-51` |
| Printed: Wednesday Eve | Prophecy | Amos 5:18-27 | `historical_witness` | `historical_witness` | `rid_628304aab06e6513191b` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6545; source_ref=Amos 5:18-27` |
| Printed: Wednesday Eve | Psalm | Ps 65:4 | `historical_witness` | `historical_witness` | `rid_93b9a076018e4e819226` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6596; source_ref=Ps 65:4` |

## Eve of Wednesday: Sixth Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/tuesday--wednesday-eve--6th-hour.txt`; SHA-256 `6503406999863241704e911f84dab04ff2e3c69335cf4a6ab105dd4cb423c422`; title `Wednesday Eve (The Sixth Hour)`.

- Line 12: Jeremiah 16:9-13
- Line 119: Psalm 101:1,2
- Line 133: Matthew 25:1-13

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Tuesday Eve | Gospel | Lk 21:34-38 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_6a9295908d82ab679d2e` | `out/data/pascha_day_hour_index.csv:row 23268; source_ref=Lk 21:34-38` |
| Curated: Tuesday Eve | OT1 | Hos 4:15-19 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_4174ab42642c34a54f1e` | `out/data/pascha_day_hour_index.csv:row 50; source_ref=Hos 4:15-19` |
| Curated: Tuesday Eve | OT1 | Hos 4:15-5:7 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_6375e2206441e7c82c00` | `out/data/pascha_day_hour_index.csv:row 23267; source_ref=Hos 4:15-5:7` |
| Curated: Tuesday Eve | OT1 | Hos 5:1-7 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_a5512dbf2aba7b654f97` | `out/data/pascha_day_hour_index.csv:row 50; source_ref=Hos 5:1-7` |
| Curated: Tuesday Eve | Psalm | Ps 91:2-3 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_2e643183859724ae8469` | `out/data/pascha_day_hour_index.csv:row 23269; source_ref=Ps 91:2-3` |
| Printed: Wednesday Eve | Gospel | Matt 25:1-13 | `historical_witness` | `historical_witness` | `rid_32c43e508ddf3a451683` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6776; source_ref=Matt 25:1-13` |
| Printed: Wednesday Eve | Prophecy | Jer 16:9-13 | `historical_witness` | `historical_witness` | `rid_dfc183cd3c70f6d0c11e` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6713; source_ref=Jer 16:9-13` |
| Printed: Wednesday Eve | Psalm | Ps 102:1-2 | `historical_witness` | `historical_witness` | `rid_6f64b15a96190c357af6` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6763; source_ref=Ps 102:1-2` |
| New Reader source | OT1 | Jer 16:9-13 | absent | `current_confirmed_coptic_reader` | `rid_dfc183cd3c70f6d0c11e` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/tuesday--wednesday-eve--6th-hour.txt:line 12; sha256=6503406999863241704e911f84dab04ff2e3c69335cf4a6ab105dd4cb423c422` |
| New Reader source | Gospel | Matt 25:1-13 | absent | `current_confirmed_coptic_reader` | `rid_32c43e508ddf3a451683` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/tuesday--wednesday-eve--6th-hour.txt:line 133; sha256=6503406999863241704e911f84dab04ff2e3c69335cf4a6ab105dd4cb423c422` |

## Eve of Wednesday: Ninth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Tuesday Eve | Gospel | Lk 11:37-52 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_6aabe84d9ce769531566` | `out/data/pascha_day_hour_index.csv:row 23265; source_ref=Lk 11:37-52` |
| Curated: Tuesday Eve | OT1 | Hos 10:12-15 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_5aa65ef9c811a749bc66` | `out/data/pascha_day_hour_index.csv:row 52; source_ref=Hos 10:12-15` |
| Curated: Tuesday Eve | OT1 | Hos 11:1-2 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_a5542ccaf2c934bbd997` | `out/data/pascha_day_hour_index.csv:row 52; source_ref=Hos 11:1-2` |
| Curated: Tuesday Eve | OT1 | Hos 10:12-11:2 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_bfa3449dafe309ebcb10` | `out/data/pascha_day_hour_index.csv:row 23264; source_ref=Hos 10:12-11:2` |
| Curated: Tuesday Eve | Psalm | Ps 33:10-11 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_2636aa0f9502858413e1` | `out/data/pascha_day_hour_index.csv:row 23266; source_ref=Ps 33:10-11` |
| Printed: Wednesday Eve | Gospel | Matt 23:29-36 | `historical_witness` | `historical_witness` | `rid_d65723c38c9c1d636c4e` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6916; source_ref=Matt 23:29-36` |
| Printed: Wednesday Eve | Prophecy | Hos 9:14-10:2 | `historical_witness` | `historical_witness` | `rid_aea37d12f9fcde6a714f` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6875; source_ref=Hos 9:14-10:2` |
| Printed: Wednesday Eve | Psalm | Ps 22:20-21 | `historical_witness` | `historical_witness` | `rid_25361742c3226f05c434` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6911; source_ref=Ps 22:20-21` |

## Eve of Wednesday: Eleventh Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Tuesday Eve | Gospel | Mark 14:1-2 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_11bd89b024291dd99c06` | `out/data/pascha_day_hour_index.csv:row 55; source_ref=Mark 14:1-2` |
| Curated: Tuesday Eve | Gospel | Mark 13:32-37 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_84a2b9f4f6446d60c2e5` | `out/data/pascha_day_hour_index.csv:row 55; source_ref=Mark 13:32-37` |
| Curated: Tuesday Eve | Gospel | Mark 13:32-14:2 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_cb849036aa32c7c89b5b` | `out/data/pascha_day_hour_index.csv:row 23259; source_ref=Mark 13:32-14:2` |
| Curated: Tuesday Eve | OT1 | Amos 5:6-14 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_c73b635100bd6b70fcc0` | `out/data/pascha_day_hour_index.csv:row 23258; source_ref=Amos 5:6-14` |
| Curated: Tuesday Eve | Psalm | Ps 122:4 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_b0b0b448d3e7cffda464` | `out/data/pascha_day_hour_index.csv:row 23260; source_ref=Ps 122:4` |

## Eve of Monday: First Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Monday Eve | Gospel | Jn 12:20-36 | `historical_witness` | `historical_witness` | `rid_193f8aa3590344f358a1` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 1857; source_ref=Jn 12:20-36` |
| Printed: Monday Eve | Prophecy | Zeph 1:2-12 | `historical_witness` | `historical_witness` | `rid_8e922bc2d7a15a18ebfb` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 1782; source_ref=Zeph 1:2-12` |
| Printed: Monday Eve | Psalm | Ps 27:6-7 | `historical_witness` | `historical_witness` | `rid_7480a0d0f7e39097604a` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 1850; source_ref=Ps 27:6-7` |

## Eve of Monday: Third Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/sunday--monday-eve--3rd-hour.txt`; SHA-256 `a477b4f0f8d93c5bd2a672b20bc7317f03c181c7770ace1abcbfaabc57d75cf4`; title `Monday Eve (The Third Hour)`.

- Line 12: Zephaniah 1:14-2:2
- Line 128: Psalm 27:10, 2
- Line 142: Luke 9:18-22

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Monday Eve | Gospel | Lk 9:18-22 | `historical_witness` | `historical_witness` | `rid_752f74d0fb9e9f2a1459` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2046; source_ref=Lk 9:18-22` |
| Printed: Monday Eve | Prophecy | Zeph 1:14-2:2 | `historical_witness` | `historical_witness` | `rid_fefd589b78ce4cbbfed0` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 1967; source_ref=Zeph 1:14-2:2` |
| Printed: Monday Eve | Psalm | Ps 28:2,28:9 | `historical_witness` | `historical_witness` | `rid_6b37badae9b1d2fe42b9` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2013; source_ref=Ps 28:2,28:9` |
| New Reader source | OT1 | Zeph 1:14-2:2 | absent | `current_confirmed_coptic_reader` | `rid_fefd589b78ce4cbbfed0` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/sunday--monday-eve--3rd-hour.txt:line 12; sha256=a477b4f0f8d93c5bd2a672b20bc7317f03c181c7770ace1abcbfaabc57d75cf4` |
| New Reader source | Gospel | Lk 9:18-22 | absent | `current_confirmed_coptic_reader` | `rid_752f74d0fb9e9f2a1459` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/sunday--monday-eve--3rd-hour.txt:line 142; sha256=a477b4f0f8d93c5bd2a672b20bc7317f03c181c7770ace1abcbfaabc57d75cf4` |

## Eve of Monday: Sixth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Monday Eve | Prophecy | Joel 1:5-15 | `historical_witness` | `historical_witness` | `rid_890cfff10ed8cb0f7ab6` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2112; source_ref=Joel 1:5-15` |

## Eve of Monday: Ninth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Monday Eve | Gospel | Mark 8:27-33 | `historical_witness` | `historical_witness` | `rid_ba1bb0c70fce2675fe62` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2323; source_ref=Mark 8:27-33` |
| Printed: Monday Eve | Prophecy | Mic 2:3-10 | `historical_witness` | `historical_witness` | `rid_846ae462b5d3e3ce7e8f` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2271; source_ref=Mic 2:3-10` |
| Printed: Monday Eve | Psalm | Ps 8:1-2 | `historical_witness` | `historical_witness` | `rid_69ce2796e1b67810d549` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2318; source_ref=Ps 8:1-2` |

## Eve of Monday: Eleventh Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/sunday--monday-eve--11th-hour.txt`; SHA-256 `8107a7f76a3b66f21308f1be9488744cc850c51159f90f460105ccffa94c6b6a`; title `Monday Eve (The Eleventh Hour)`.

- Line 12: Micah 3:1-4
- Line 110: Psalm 17:16-17
- Line 124: Matthew 17:19-23

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Monday Eve | Gospel | Matt 17:19-23 | `historical_witness` | `historical_witness` | `rid_fbe720df2033b694cf9b` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2461; source_ref=Matt 17:19-23` |
| Printed: Monday Eve | Prophecy | Mic 3:1-4 | `historical_witness` | `historical_witness` | `rid_a7c9f87ecffeebc70662` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2426; source_ref=Mic 3:1-4` |
| Printed: Monday Eve | Psalm | Ps 18:17-18 | `historical_witness` | `historical_witness` | `rid_4a330dc2a8ba000cae81` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2456; source_ref=Ps 18:17-18` |
| New Reader source | OT1 | Mic 3:1-4 | absent | `current_confirmed_coptic_reader` | `rid_a7c9f87ecffeebc70662` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/sunday--monday-eve--11th-hour.txt:line 12; sha256=8107a7f76a3b66f21308f1be9488744cc850c51159f90f460105ccffa94c6b6a` |
| New Reader source | Gospel | Matt 17:19-23 | absent | `current_confirmed_coptic_reader` | `rid_fbe720df2033b694cf9b` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/sunday--monday-eve--11th-hour.txt:line 124; sha256=8107a7f76a3b66f21308f1be9488744cc850c51159f90f460105ccffa94c6b6a` |

## Good Friday: Sixth Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/friday--6th-hour.txt`; SHA-256 `aae5386449ddad8f45ca625402bd4ed3ee9c885c10c05e161e69f77e02110c57`; title `Great Friday (The Sixth Hour)`.

- Line 13: Numbers 21:1-9
- Line 51: Isaiah 53:7-12
- Line 83: Isaiah 12:2-13:10
- Line 141: Amos 8:9-12
- Line 304: Galatians 6:14-18
- Line 482: Psalm 37:21-22, 21:16-18,8
- Line 499: Matthew 27:27-45
- Line 592: Mark 15:26-33
- Line 635: Luke 23:26-44
- Line 711: John 19:13-27

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Good Friday | Gospel | Jn 19:13-27 | `historical_witness` | `historical_witness` | `rid_2afa3534e5c24e29a17a` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 15406; source_ref=Jn 19:13-27` |
| Curated: Good Friday | Gospel | Matt 27:27-45 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_afffc4e945b4f7124705` | `out/data/pascha_day_hour_index.csv:row 53155; source_ref=Matt 27:27-45` |
| Curated: Good Friday | Gospel | Lk 23:26-44 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_bf10fb2f935b760ee353` | `out/data/pascha_day_hour_index.csv:row 53153; source_ref=Lk 23:26-44` |
| Curated: Good Friday | Gospel | Mark 15:26-33 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_d07c8599ec57244053cc` | `out/data/pascha_day_hour_index.csv:row 53154; source_ref=Mark 15:26-33` |
| Curated: Good Friday | Gospel | Jn 19:1-12 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_d29544c970904a8ee5f2` | `out/data/pascha_day_hour_index.csv:row 53152; source_ref=Jn 19:1-12` |
| Curated: Good Friday | OT1 | Num 21:1-9 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_9944850087ec93cf1f1a` | `out/data/pascha_day_hour_index.csv:row 53147; source_ref=Num 21:1-9` |
| Curated: Good Friday | OT2 | Isa 53:7-12 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_29c24f86b54049f3ab8f` | `out/data/pascha_day_hour_index.csv:row 53148; source_ref=Isa 53:7-12` |
| Curated: Good Friday | OT3 | Isa 12:2-13:10 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_10578ba445da60f939f0` | `out/data/pascha_day_hour_index.csv:row 53149; source_ref=Isa 12:2-13:10` |
| Curated: Good Friday | OT4 | Amos 8:9-12 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_30b1ce8f518a66a02e22` | `out/data/pascha_day_hour_index.csv:row 53150; source_ref=Amos 8:9-12` |
| Curated: Good Friday | Pauline | Gal 6:14-18 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_a98f1b11fcc1e6089f13` | `out/data/pascha_day_hour_index.csv:row 53151; source_ref=Gal 6:14-18` |
| Printed: Good Friday | Psalm | Ps 21:8-9,21:16-17,37:21-22 | `historical_witness` | `historical_witness` | `rid_33dc8b5c1e34c09fe767` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 15247; source_ref=Ps 21:8-9,21:16-17,37:21-22` |
| Curated: Good Friday | Psalm | Ps 38:21-22 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_655bbf60c64b7ed7091d` | `out/data/pascha_day_hour_index.csv:row 53158; source_ref=Ps 38:21-22` |
| Curated: Good Friday | Psalm | Ps 22:16-18 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_94b925598101bd523346` | `out/data/pascha_day_hour_index.csv:row 53156; source_ref=Ps 22:16-18` |
| Curated: Good Friday | Psalm | Ps 22:7-8 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_a6519972386aa1af404e` | `out/data/pascha_day_hour_index.csv:row 53157; source_ref=Ps 22:7-8` |
| New Reader source | Gospel | Jn 19:13-27 | absent | `current_confirmed_coptic_reader` | `rid_2afa3534e5c24e29a17a` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/friday--6th-hour.txt:line 711; sha256=aae5386449ddad8f45ca625402bd4ed3ee9c885c10c05e161e69f77e02110c57` |

## Great Thursday: Third Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Great Thursday | Gospel | Matt 26:17-19 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_a3e2c8af7f4595282adb` | `out/data/pascha_day_hour_index.csv:row 98; source_ref=Ps 94:21,23; Matt 26:17-19` |
| Curated: Great Thursday | OT1 | Exod 32:30-33:5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_358e39ca423031cc9ba2` | `out/data/pascha_day_hour_index.csv:row 94; source_ref=Exod 32:30-33:5` |
| Curated: Great Thursday | OT2 | Sir 24:1-11 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_618ab50f3a40a058d9e6` | `out/data/pascha_day_hour_index.csv:row 95; source_ref=Sir 24:1-11` |
| Curated: Great Thursday | OT3 | Zech 10:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_1651b2a930115b2681ea` | `out/data/pascha_day_hour_index.csv:row 96; source_ref=Zech 9:11-14; Zech 10:1-2` |
| Curated: Great Thursday | OT3 | Zech 9:11-14 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_49a5e8e3dbaed635b621` | `out/data/pascha_day_hour_index.csv:row 96; source_ref=Zech 9:11-14; Zech 10:1-2` |
| Curated: Great Thursday | OT4 | Prov 4:4-27,5:1-4 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_848c8fc9d17938a036f1` | `out/data/pascha_day_hour_index.csv:row 97; source_ref=Prov 4:4-5:4` |
| Printed: Great Thursday | Prophecy | Prov 30:2-6 | `historical_witness` | `historical_witness` | `rid_21c8b4621845f47779c3` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 9897; source_ref=Prov 30:2-6` |
| Curated: Great Thursday | Psalm | Ps 94:21,94:23 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_975be8b876f7b879a34b` | `out/data/pascha_day_hour_index.csv:row 98; source_ref=Ps 94:21,23; Matt 26:17-19` |

## Great Thursday: Ninth Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/thursday--thursday-day--9th-hour.txt`; SHA-256 `087f6a8dd0e7868a64500185d2f9e4527ec90a11ae44d4ef6b678c539aab58b2`; title `Covenant Thursday (The Ninth Hour)`.

- Line 12: Genesis 22:1-19
- Line 83: Isaiah 61:1-7
- Line 126: Job 27:1-28:13
- Line 286: Psalm 22:1
- Line 300: Matthew 26:17-19

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Great Thursday | Gospel | Matt 26:17-19 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_a3e2c8af7f4595282adb` | `out/data/pascha_day_hour_index.csv:row 107; source_ref=Ps 23:1,2; Matt 26:17-19` |
| Printed: Great Thursday | Gospel | Matt 26:3-16 | `historical_witness` | `historical_witness` | `rid_ee62ed11065129a5f12c` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10462; source_ref=Matt 26:3-16` |
| Curated: Great Thursday | OT1 | Gen 22:1-19 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_1cc3bd69010af9825fa2` | `out/data/pascha_day_hour_index.csv:row 103; source_ref=Gen 22:1-19` |
| Curated: Great Thursday | OT2 | Isa 61:1-7 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_70f5df2017474bb92728` | `out/data/pascha_day_hour_index.csv:row 104; source_ref=Isa 61:1-7` |
| Curated: Great Thursday | OT3 | Gen 14:17-20 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_9bfffc9b854f3b3e550c` | `out/data/pascha_day_hour_index.csv:row 105; source_ref=Gen 14:17-20` |
| Curated: Great Thursday | OT4 | Job 27:2-28:13 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_eea6aa8f3a611b69760d` | `out/data/pascha_day_hour_index.csv:row 106; source_ref=Job 27:2-28:13` |
| Printed: Great Thursday | Prophecy | Isa 61:1-6 | `historical_witness` | `historical_witness` | `rid_e14a8c6fa7cab6a53d85` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10294; source_ref=Isa 61:1-6` |
| Curated: Great Thursday | Psalm | Ps 23:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_3f14d571baf20d8570ae` | `out/data/pascha_day_hour_index.csv:row 107; source_ref=Ps 23:1,2; Matt 26:17-19` |
| Printed: Great Thursday | Psalm | Ps 41:5-7 | `historical_witness` | `historical_witness` | `rid_c1d60b035931158ae984` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10446; source_ref=Ps 41:5-7` |
| Printed: Thursday | Prophecy | Gen 22:1-19 | `historical_witness` | `historical_witness` | `rid_1cc3bd69010af9825fa2` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10235; source_ref=Gen 22:1-19` |

## Eve of Thursday: First Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/wednesday--thursday-eve--1st-hour.txt`; SHA-256 `ea2dee966adbe3b50e174b5d668f8a84c1b824fc45c7fbd87abd6e598dbbe9f3`; title `Covenant Thursday Eve (The First Hour)`.

- Line 12: Ezekiel 43:5-11
- Line 122: Psalm 68:1, 13
- Line 136: John 10:17-21

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Great Thursday Eve | Prophecy | Ezek 43:5-11 | `historical_witness` | `historical_witness` | `rid_6627b953cbdb71691206` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8540; source_ref=Ezek 43:5-11` |
| Printed: Thursday Eve | Gospel | Jn 10:17-21 | `historical_witness` | `historical_witness` | `rid_4c8185db2dc57feb8771` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8607; source_ref=Jn 10:17-21` |
| Printed: Thursday Eve | Psalm | Ps 69:1,69:16 | `historical_witness` | `historical_witness` | `rid_149496b1ed25a9ed714c` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8593; source_ref=Ps 69:1,69:16` |
| Curated: Wednesday Eve | Gospel | Jn 10:17-21 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_4c8185db2dc57feb8771` | `out/data/pascha_day_hour_index.csv:row 79; source_ref=Ps 69:1,16; John 10:17-21` |
| Curated: Wednesday Eve | OT1 | Jer 43:5-11 | `current_working_source_not_coptic_reader_checked` | `pending_coptic_reader_review` | `rid_af6bf4bf6c1d0b812cd2` | `out/data/pascha_day_hour_index.csv:row 78; source_ref=Jer 43:5-11` |
| Curated: Wednesday Eve | Psalm | Ps 69:1,69:16 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_149496b1ed25a9ed714c` | `out/data/pascha_day_hour_index.csv:row 79; source_ref=Ps 69:1,16; John 10:17-21` |
| New Reader source | OT1 | Ezek 43:5-11 | absent | `current_confirmed_coptic_reader` | `rid_6627b953cbdb71691206` | `sources/coptic-reader/holy-week-review-qualified-2026-10-29/wednesday--thursday-eve--1st-hour.txt:line 12; sha256=ea2dee966adbe3b50e174b5d668f8a84c1b824fc45c7fbd87abd6e598dbbe9f3` |

## Good Friday: Eleventh Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/friday--11th-hour.txt`; SHA-256 `32e1cab53d275e25ff1b574c5bdaa624a95fecc935f19c38ef69f64835816d1b`; title `Great Friday (The Eleventh Hour)`.

- Line 12: Exodus 12:1-14
- Line 186: Psalm 142:6-7, 30:5
- Line 203: Matthew 27:51-56
- Line 256: Mark 15:38-41
- Line 287: Luke 23:47-49
- Line 315: John 19:31-37
- Complete retained hour has no Pauline heading or Galatians 3 selection. This is scoped source absence, not a claim about every historical book.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Good Friday | Gospel | Matt 27:51-56 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_2d11e348ed0fff139cbc` | `out/data/pascha_day_hour_index.csv:row 53119; source_ref=Matt 27:51-56` |
| Curated: Good Friday | Gospel | Lk 23:47-49 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_355c550ac44ac9c37fd4` | `out/data/pascha_day_hour_index.csv:row 53117; source_ref=Lk 23:47-49` |
| Curated: Good Friday | Gospel | Mark 15:38-41 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_35684aad2907eda3d30b` | `out/data/pascha_day_hour_index.csv:row 53118; source_ref=Mark 15:38-41` |
| Curated: Good Friday | Gospel | Jn 19:31-37 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_5e749b252589833af6cb` | `out/data/pascha_day_hour_index.csv:row 53116; source_ref=Jn 19:31-37` |
| Curated: Good Friday | OT1 | Jer 12:1-14 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_0946df3427160b8ebe38` | `out/data/pascha_day_hour_index.csv:row 53114; source_ref=Jer 12:1-14` |
| Curated: Good Friday | OT2 | Isa 3:5-12 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_2f2ca45446d156914dd8` | `out/data/pascha_day_hour_index.csv:row 53115; source_ref=Isa 3:5-12` |
| Printed: Good Friday | Pauline | Gal 3:1-6 | `historical_witness` | `historical_witness` | `rid_097e29504a6631f99f85` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 16278; source_ref=Gal 3:1-6` |
| Printed: Good Friday | Prophecy | Lev 23:5-12 | `historical_witness` | `historical_witness` | `rid_a971392ddfbc3a0f06b3` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 16231; source_ref=Lev 23:5-12` |
| Printed: Good Friday | Prophecy | Exod 12:1-14 | `historical_witness` | `historical_witness` | `rid_dd697f19c7c258dea773` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 16178; source_ref=Exod 12:1-14` |
| Printed: Good Friday | Psalm | Ps 31:5,143:6-7 | `historical_witness` | `historical_witness` | `rid_646c3f9b562becc071a7` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 16321; source_ref=Ps 31:5,143:6-7` |
| Curated: Good Friday | Psalm | Ps 143:6-7 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_9427edf3452b5acb16d7` | `out/data/pascha_day_hour_index.csv:row 53120; source_ref=Ps 143:6-7` |
| Curated: Good Friday | Psalm | Ps 31:5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_b645bce981a16ea01931` | `out/data/pascha_day_hour_index.csv:row 53121; source_ref=Ps 31:5` |

## Great Thursday: Eleventh Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Great Thursday | Gospel | Jn 13:21-30 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_6275cd3bdf99db46179c` | `out/data/pascha_day_hour_index.csv:row 112; source_ref=Ps 50:17,18; John 13:21-30` |
| Curated: Great Thursday | OT1 | Isa 52:13-53:12 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_03fafca6599b3a156cd0` | `out/data/pascha_day_hour_index.csv:row 109; source_ref=Isa 52:13-53:12` |
| Curated: Great Thursday | OT2 | Isa 19:19-25 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_c07f2d7123e4d534e97d` | `out/data/pascha_day_hour_index.csv:row 110; source_ref=Isa 19:19-25` |
| Curated: Great Thursday | OT3 | Zech 12:11-14 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_3c8ee31a9b4d60c55f7e` | `out/data/pascha_day_hour_index.csv:row 111; source_ref=Zech 12:11-14; Zech 13:1-9; Zech 14:1-4; Zech 14:6-9` |
| Curated: Great Thursday | OT3 | Zech 14:1-4 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_79857e7508f3b340e030` | `out/data/pascha_day_hour_index.csv:row 111; source_ref=Zech 12:11-14; Zech 13:1-9; Zech 14:1-4; Zech 14:6-9` |
| Curated: Great Thursday | OT3 | Zech 14:6-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_8bb8c23943892befc28a` | `out/data/pascha_day_hour_index.csv:row 111; source_ref=Zech 12:11-14; Zech 13:1-9; Zech 14:1-4; Zech 14:6-9` |
| Curated: Great Thursday | OT3 | Zech 13:1-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d035c3e81a697c85dbd0` | `out/data/pascha_day_hour_index.csv:row 111; source_ref=Zech 12:11-14; Zech 13:1-9; Zech 14:1-4; Zech 14:6-9` |
| Printed: Great Thursday | Prophecy | Zech 12:11-14:3,14:6-9 | `historical_witness` | `historical_witness` | `rid_9830b2bdd818213f8ed8` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 11882; source_ref=Zech 12:11-14:3,14:6-9` |
| Curated: Great Thursday | Psalm | Ps 50:17-18 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_ac1428ed452811b5d729` | `out/data/pascha_day_hour_index.csv:row 112; source_ref=Ps 50:17,18; John 13:21-30` |

## Palm Sunday: Ninth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Hosanna Sunday | Gospel | Matt 21:10-17 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_febdbadd9aea980d2dbb` | `out/data/pascha_day_hour_index.csv:row 163; source_ref=Ps 8:2,3; Matt 21:10-17` |
| Printed: Hosanna Sunday | Prophecy | Lam 1:1-4 | `historical_witness` | `historical_witness` | `rid_6f2b1cdfaffff2641d58` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 1393; source_ref=Lam 1:1-4` |
| Printed: Hosanna Sunday | Prophecy | Zeph 3:11-20 | `historical_witness` | `historical_witness` | `rid_7f6813e26ac3c06f0f47` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 1438; source_ref=Zeph 3:11-20` |
| Curated: Hosanna Sunday | Psalm | Ps 8:2-3 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d9f544171faf5b8bf1b4` | `out/data/pascha_day_hour_index.csv:row 163; source_ref=Ps 8:2,3; Matt 21:10-17` |

## Palm Sunday: Eleventh Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Hosanna Sunday | Gospel | Matt 20:20-28 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_3f05adb088ea4fb9b1e9` | `out/data/pascha_day_hour_index.csv:row 164; source_ref=Ps 22:22-23; Matt 20:20-28` |
| Printed: Hosanna Sunday | Prophecy | Isa 48:12-22 | `historical_witness` | `historical_witness` | `rid_308d53d2c6f594fc6484` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 1572; source_ref=Isa 48:12-22` |
| Printed: Hosanna Sunday | Prophecy | Nah 1:2-8 | `historical_witness` | `historical_witness` | `rid_66e208bd48104ce4ce54` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 1633; source_ref=Nah 1:2-8` |
| Curated: Hosanna Sunday | Psalm | Ps 22:22-23 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_f334b150887bd2f1bff5` | `out/data/pascha_day_hour_index.csv:row 164; source_ref=Ps 22:22-23; Matt 20:20-28` |

## Palm Sunday: Liturgy

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Palm Sunday | Acts | Acts 28:11-31 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d7b3f65948587b407146` | `out/data/pascha_day_hour_index.csv:row 171; source_ref=Acts 28:11-31` |
| Curated: Palm Sunday | Catholic | 1Pet 4:1-11 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_c8301ac6e0b3cf7e0fdb` | `out/data/pascha_day_hour_index.csv:row 170; source_ref=1Pet 4:1-11` |
| Curated: Palm Sunday | Gospel | Mark 11:1-11 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_086294f1b3af0bf3e9ff` | `out/data/pascha_day_hour_index.csv:row 172; source_ref=Ps 80:3,1,2; Matt 21:1-17; Mark 11:1-11; Luke 19:29-48; Ps 64:1,2; John 12:12-19` |
| Curated: Palm Sunday | Gospel | Jn 12:12-19 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_56258ae52dbbe285370a` | `out/data/pascha_day_hour_index.csv:row 172; source_ref=Ps 80:3,1,2; Matt 21:1-17; Mark 11:1-11; Luke 19:29-48; Ps 64:1,2; John 12:12-19` |
| Curated: Palm Sunday | Gospel | Lk 19:29-48 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_961bac1556ad1d6c41f0` | `out/data/pascha_day_hour_index.csv:row 172; source_ref=Ps 80:3,1,2; Matt 21:1-17; Mark 11:1-11; Luke 19:29-48; Ps 64:1,2; John 12:12-19` |
| Curated: Palm Sunday | Gospel | Matt 21:1-17 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_c41957d659db423dcab9` | `out/data/pascha_day_hour_index.csv:row 172; source_ref=Ps 80:3,1,2; Matt 21:1-17; Mark 11:1-11; Luke 19:29-48; Ps 64:1,2; John 12:12-19` |
| Curated: Palm Sunday | Pauline | Heb 9:11-28 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_f35aa8dad0b5d7ca3707` | `out/data/pascha_day_hour_index.csv:row 169; source_ref=Heb 9:11-28` |
| Curated: Palm Sunday | Psalm | Ps 80:1-3 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_3ec9d2a02a58af4a005d` | `out/data/pascha_day_hour_index.csv:row 172; source_ref=Ps 80:3,1,2; Matt 21:1-17; Mark 11:1-11; Luke 19:29-48; Ps 64:1,2; John 12:12-19` |
| Curated: Palm Sunday | Psalm | Ps 64:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_3fd4b87524624788bd66` | `out/data/pascha_day_hour_index.csv:row 172; source_ref=Ps 80:3,1,2; Matt 21:1-17; Mark 11:1-11; Luke 19:29-48; Ps 64:1,2; John 12:12-19` |

## Palm Sunday: Matins

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Palm Sunday | Gospel | Lk 19:1-10 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_5fc3baae94a37d1b025f` | `out/data/pascha_day_hour_index.csv:row 168; source_ref=Luke 19:1-10` |
| Curated: Palm Sunday | Psalm | Ps 68:19,68:35 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_8c93aa480c34163724ae` | `out/data/pascha_day_hour_index.csv:row 167; source_ref=Ps 68:19,35` |

## Palm Sunday: Vespers

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Palm Sunday | Gospel | Jn 12:1-11 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_1a9356fccd88919843b0` | `out/data/pascha_day_hour_index.csv:row 166; source_ref=John 12:1-11` |
| Curated: Palm Sunday | Psalm | Ps 118:26-27 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_bb5242ea646a3d18562d` | `out/data/pascha_day_hour_index.csv:row 165; source_ref=Ps 118:26-27` |

## Eve of Tuesday: First Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday Eve | Gospel | Lk 13:23-30 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_e2d8832a22e439862231` | `out/data/pascha_day_hour_index.csv:row 41952; source_ref=Lk 13:23-30` |
| Curated: Monday Eve | OT1 | Zech 1:1-6 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_0f4e1a985963d3c3064d` | `out/data/pascha_day_hour_index.csv:row 41951; source_ref=Zech 1:1-6` |
| Curated: Monday Eve | Psalm | Ps 62:6-7 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_8be9daf4ab53e4424614` | `out/data/pascha_day_hour_index.csv:row 41953; source_ref=Ps 62:6-7` |
| Printed: Tuesday Eve | Psalm | Ps 62:2,62:7 | `historical_witness` | `historical_witness` | `rid_00de28edc62a694408d5` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 3947; source_ref=Ps 62:2,62:7` |

## Eve of Tuesday: Third Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/monday--tuesday-eve--3rd-hour.txt`; SHA-256 `3ea341eaa6e0a2323c73a2d46684dfecd6c09be64ffadd9766a0a48db1c1a1ce`; title `Tuesday Eve (The Third Hour)`.

- Line 12: Malachi 1:1-9
- Line 128: Psalm 12:4,6
- Line 142: Luke 13:31-35

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday Eve | Gospel | Lk 13:31-35 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_b9224e7edb547a30e943` | `out/data/pascha_day_hour_index.csv:row 41963; source_ref=Lk 13:31-35` |
| Curated: Monday Eve | OT1 | Mal 1:1-9 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_f5ce91b8996a871b27ba` | `out/data/pascha_day_hour_index.csv:row 41962; source_ref=Mal 1:1-9` |
| Curated: Monday Eve | Psalm | Ps 13:3,13:5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_493778d4a6a4ba640417` | `out/data/pascha_day_hour_index.csv:row 41964; source_ref=Ps 13:3,13:5` |
| Printed: Tuesday Eve | Psalm | Ps 28:2,28:9 | `historical_witness` | `historical_witness` | `rid_6b37badae9b1d2fe42b9` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 4100; source_ref=Ps 28:2,28:9` |

## Eve of Tuesday: Sixth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday Eve | Gospel | Mark 10:32-34 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_c5eeff74dd07f0aa99f2` | `out/data/pascha_day_hour_index.csv:row 41960; source_ref=Mark 10:32-34` |
| Curated: Monday Eve | OT1 | Hos 4:15-19 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_4174ab42642c34a54f1e` | `out/data/pascha_day_hour_index.csv:row 41958; source_ref=Hos 4:15-19` |
| Curated: Monday Eve | OT1 | Hos 5:1-7 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_a5512dbf2aba7b654f97` | `out/data/pascha_day_hour_index.csv:row 41959; source_ref=Hos 5:1-7` |
| Curated: Monday Eve | Psalm | Ps 29:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_bb075d6d55756034bb0b` | `out/data/pascha_day_hour_index.csv:row 41961; source_ref=Ps 29:1-2` |
| Printed: Tuesday Eve | Psalm | Ps 29:1-2 | `historical_witness` | `historical_witness` | `rid_bb075d6d55756034bb0b` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 4249; source_ref=Ps 29:1-2` |

## Eve of Tuesday: Ninth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday Eve | Gospel | Lk 11:37-52 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_6aabe84d9ce769531566` | `out/data/pascha_day_hour_index.csv:row 41956; source_ref=Lk 11:37-52` |
| Curated: Monday Eve | OT1 | Hos 10:12-15 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_5aa65ef9c811a749bc66` | `out/data/pascha_day_hour_index.csv:row 41954; source_ref=Hos 10:12-15` |
| Curated: Monday Eve | OT1 | Hos 11:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_a5542ccaf2c934bbd997` | `out/data/pascha_day_hour_index.csv:row 41955; source_ref=Hos 11:1-2` |
| Curated: Monday Eve | Psalm | Ps 33:10-11 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_2636aa0f9502858413e1` | `out/data/pascha_day_hour_index.csv:row 41957; source_ref=Ps 33:10-11` |

## Eve of Tuesday: Eleventh Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/monday--tuesday-eve--11th-hour.txt`; SHA-256 `8de3be134a587d53d26c49bf33c8a05242c41959e4ef03de8af48a6e219fb232`; title `Tuesday Eve (The Eleventh Hour)`.

- Line 12: Amos 5:6-14
- Line 116: Psalm 121:4
- Line 130: Mark 13:32-14:2

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday Eve | Gospel | Mark 14:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_11bd89b024291dd99c06` | `out/data/pascha_day_hour_index.csv:row 41949; source_ref=Mark 14:1-2` |
| Curated: Monday Eve | Gospel | Mark 13:32-37 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_84a2b9f4f6446d60c2e5` | `out/data/pascha_day_hour_index.csv:row 41948; source_ref=Mark 13:32-37` |
| Curated: Monday Eve | OT1 | Amos 5:6-14 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_c73b635100bd6b70fcc0` | `out/data/pascha_day_hour_index.csv:row 41947; source_ref=Amos 5:6-14` |
| Curated: Monday Eve | Psalm | Ps 122:4 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_b0b0b448d3e7cffda464` | `out/data/pascha_day_hour_index.csv:row 41950; source_ref=Ps 122:4` |

## Monday: First Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/monday--monday-day--1st-hour.txt`; SHA-256 `969a75243def0a4ccb42bff8143893baa997fb644fb9141984a6e8bac2b7f4c0`; title `Monday (The First Hour)`.

- Line 12: Genesis 1:1-2:3
- Line 131: Isaiah 5:1-9
- Line 183: Sirach 1:1-24
- Line 333: Psalm 71:18
- Line 347: Mark 11:12-24

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday | Gospel | Mark 11:12-24 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_9b559d734f895f470341` | `out/data/pascha_day_hour_index.csv:row 41932; source_ref=Mark 11:12-24` |
| Curated: Monday | OT1 | Gen 2:1-3 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_1003c683c9f754a608c9` | `out/data/pascha_day_hour_index.csv:row 1; source_ref=Gen 2:1-3` |
| Curated: Monday | OT1 | Gen 1:1-2:3 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_1799bfb4477d9a219633` | `out/data/pascha_day_hour_index.csv:row 41929; source_ref=Gen 1:1-2:3` |
| Curated: Monday | OT1 | Gen 1:1-31 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_771aba4408e0d1979413` | `out/data/pascha_day_hour_index.csv:row 1; source_ref=Gen 1:1-31` |
| Curated: Monday | OT2 | Isa 5:1-9 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_613a5f1b1a33e624d353` | `out/data/pascha_day_hour_index.csv:row 41930; source_ref=Isa 5:1-9` |
| Curated: Monday | OT3 | Ps 72:1-19 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_dad5112f8b42c132267b` | `out/data/pascha_day_hour_index.csv:row 41931; source_ref=Ps 72:1-19` |
| Printed: Monday | Prophecy | Sir 1:1-14 | `historical_witness` | `historical_witness` | `rid_f0e2f487f6d7380c37b4` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2718; source_ref=Sir 1:1-14` |
| Printed: Monday | Psalm | Ps 71:18-19 | `historical_witness` | `historical_witness` | `rid_cdbc47d9e2e491867bfb` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 2797; source_ref=Ps 71:18-19` |
| Curated: Monday | Psalm | Ps 72:18-19 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_dc9da15e1e47924e6604` | `out/data/pascha_day_hour_index.csv:row 41933; source_ref=Ps 72:18-19` |

## Monday: Third Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/monday--monday-day--3rd-hour.txt`; SHA-256 `18f6143cbaaf3e281ff2f5da3a785445ab875c0ac224bf0f974ab552a53709bd`; title `Monday (The Third Hour)`.

- Line 12: Isaiah 5:20-30
- Line 71: Jeremiah 9:12-19
- Line 172: Psalm 121:1-2
- Line 186: Mark 11:11-19

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday | Gospel | Mark 11:11-19 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_d1cf895fb56180180bb0` | `out/data/pascha_day_hour_index.csv:row 41945; source_ref=Mark 11:11-19` |
| Curated: Monday | OT1 | Isa 5:20-30 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_dea460583107611686de` | `out/data/pascha_day_hour_index.csv:row 41943; source_ref=Isa 5:20-30` |
| Curated: Monday | OT2 | Jer 9:12-19 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_fcbca4c8026ae9ed4e8f` | `out/data/pascha_day_hour_index.csv:row 41944; source_ref=Jer 9:12-19` |
| Curated: Monday | Psalm | Ps 122:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_35e5e6d764183f72ad04` | `out/data/pascha_day_hour_index.csv:row 41946; source_ref=Ps 122:1-2` |

## Monday: Sixth Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/monday--monday-day--6th-hour.txt`; SHA-256 `cd70356d7bd60e8208db48de322e73f2be711059584114e550c9181782ea1462`; title `Monday (The Sixth Hour)`.

- Line 12: Exodus 32:7-15
- Line 56: Wisdom of Solomon 1:1-9
- Line 166: Psalm 121:4
- Line 180: John 2:13-17

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday | Gospel | Jn 2:13-17 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_09c47202658ca3a2f9c2` | `out/data/pascha_day_hour_index.csv:row 41941; source_ref=Jn 2:13-17` |
| Curated: Monday | OT1 | Exod 32:7-15 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_98338e5b95a885a3d127` | `out/data/pascha_day_hour_index.csv:row 41939; source_ref=Exod 32:7-15` |
| Curated: Monday | OT2 | Wis 1:1-9 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_8b2e40043dfc9bcb1c19` | `out/data/pascha_day_hour_index.csv:row 41940; source_ref=Wis 1:1-9` |
| Curated: Monday | Psalm | Ps 122:4 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_b0b0b448d3e7cffda464` | `out/data/pascha_day_hour_index.csv:row 41942; source_ref=Ps 122:4` |

## Monday: Ninth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday | Gospel | Matt 21:23-27 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_68809512622d19856234` | `out/data/pascha_day_hour_index.csv:row 41937; source_ref=Matt 21:23-27` |
| Curated: Monday | OT1 | Gen 2:15-3:24 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_08ac8d6676963ff43fe0` | `out/data/pascha_day_hour_index.csv:row 41934; source_ref=Gen 2:15-3:24` |
| Curated: Monday | OT1 | Gen 3:1-24 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_6e03959e33c5b565163e` | `out/data/pascha_day_hour_index.csv:row 11; source_ref=Gen 3:1-24` |
| Curated: Monday | OT1 | Gen 2:15-25 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_a807e22524aab669e3c2` | `out/data/pascha_day_hour_index.csv:row 11; source_ref=Gen 2:15-25` |
| Curated: Monday | OT2 | Isa 40:1-5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_07a98121b2a6c00d24d1` | `out/data/pascha_day_hour_index.csv:row 41935; source_ref=Isa 40:1-5` |
| Curated: Monday | OT3 | Prov 1:1-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_c68c8617c19b143a586d` | `out/data/pascha_day_hour_index.csv:row 41936; source_ref=Prov 1:1-9` |
| Curated: Monday | Psalm | Ps 65:4-5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_751349005e100c368a1f` | `out/data/pascha_day_hour_index.csv:row 41938; source_ref=Ps 65:4-5` |

## Monday: Eleventh Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Monday | Gospel | Jn 8:51-59 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_6297f04e598f02483db6` | `out/data/pascha_day_hour_index.csv:row 41927; source_ref=Jn 8:51-59` |
| Curated: Monday | OT1 | Isa 50:1-3 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d5c12afc31445328b9db` | `out/data/pascha_day_hour_index.csv:row 41925; source_ref=Isa 50:1-3` |
| Curated: Monday | OT2 | Wis 2:20-30 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_eead85a0820420a96aa4` | `out/data/pascha_day_hour_index.csv:row 41926; source_ref=Wis 2:20-30` |
| Printed: Monday | Prophecy | Sir 1:18-27 | `historical_witness` | `historical_witness` | `rid_8067d0f3c67b9104e6c9` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 3676; source_ref=Sir 1:18-27` |
| Curated: Monday | Psalm | Ps 13:3-4 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_40095a8e6eb6be324215` | `out/data/pascha_day_hour_index.csv:row 41928; source_ref=Ps 13:3-4` |
| Printed: Monday | Psalm | Ps 12:3-4 | `historical_witness` | `historical_witness` | `rid_fa9fd9c616ba14e4e096` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 3759; source_ref=Ps 12:3-4` |

## Tuesday: First Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Tuesday | Gospel | Jn 8:21-29 | `historical_witness` | `historical_witness` | `rid_0ad38842c158db44a98c` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 4877; source_ref=Jn 8:21-29` |
| Curated: Tuesday | Gospel | Jn 11:12-24 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_3503dab946c9a441f29a` | `out/data/pascha_day_hour_index.csv:row 23242; source_ref=Jn 11:12-24` |
| Curated: Tuesday | OT1 | Exod 19:1-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_2ef423835894cc5bd95c` | `out/data/pascha_day_hour_index.csv:row 23239; source_ref=Exod 19:1-9` |
| Curated: Tuesday | OT2 | Job 23:2-17 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_5f20dd8e89269bd707d6` | `out/data/pascha_day_hour_index.csv:row 29; source_ref=Job 23:2-17` |
| Curated: Tuesday | OT2 | Job 23:2-24:25 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_6546e2768925e859a2a6` | `out/data/pascha_day_hour_index.csv:row 23240; source_ref=Job 23:2-24:25` |
| Curated: Tuesday | OT2 | Job 24:1-25 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_a2e0d4c29f4097baa4a2` | `out/data/pascha_day_hour_index.csv:row 29; source_ref=Job 24:1-25` |
| Curated: Tuesday | OT3 | Hos 4:1-8 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_132d5d45dd7e31f004b7` | `out/data/pascha_day_hour_index.csv:row 23241; source_ref=Hos 4:1-8` |
| Curated: Tuesday | Psalm | Ps 120:2,120:6-7 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_6afa7496132d4eea46ad` | `out/data/pascha_day_hour_index.csv:row 23243; source_ref=Ps 120:2,120:6-7` |

## Tuesday: Third Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/tuesday--tuesday-day--3rd-hour.txt`; SHA-256 `9d140c21a75dda8de379fa9a8038e5a0b77a369a930410b5cb65221211ec1cc8`; title `Tuesday (The Third Hour)`.

- Line 12: Deuteronomy 8:11-20
- Line 53: Sirach 2:1-9
- Line 82: Job 27:1-28:2
- Line 159: 1 kings 19:9-14
- Line 257: Psalm 118:118, 119
- Line 271: Matthew 23:37-24:2

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Tuesday | Gospel | Matt 23:37-24:2 | `historical_witness` | `historical_witness` | `rid_9b1dabfd305d19da4f68` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5159; source_ref=Matt 23:37-24:2` |
| Curated: Tuesday | Gospel | Mark 11:11-19 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d1cf895fb56180180bb0` | `out/data/pascha_day_hour_index.csv:row 23256; source_ref=Mark 11:11-19` |
| Curated: Tuesday | OT1 | Isa 5:20-30 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_dea460583107611686de` | `out/data/pascha_day_hour_index.csv:row 23254; source_ref=Isa 5:20-30` |
| Curated: Tuesday | OT2 | Jer 9:12-19 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_fcbca4c8026ae9ed4e8f` | `out/data/pascha_day_hour_index.csv:row 23255; source_ref=Jer 9:12-19` |
| Printed: Tuesday | Prophecy | Deut 8:11-20 | `historical_witness` | `historical_witness` | `rid_4cb85af8725a70ba58e7` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 4997; source_ref=Deut 8:11-20` |
| Printed: Tuesday | Prophecy | Job 27:2-28:2 | `historical_witness` | `historical_witness` | `rid_5c3fb3c80463cc0380d6` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5056; source_ref=Job 27:2-28:2` |
| Printed: Tuesday | Prophecy | 1Kgs 19:9-14 | `historical_witness` | `historical_witness` | `rid_8d533cea2864b4615c79` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5111; source_ref=1Kgs 19:9-14` |
| Printed: Tuesday | Prophecy | Sir 1:1-14 | `historical_witness` | `historical_witness` | `rid_f0e2f487f6d7380c37b4` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5029; source_ref=Sir 1:1-14` |
| Curated: Tuesday | Psalm | Ps 122:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_35e5e6d764183f72ad04` | `out/data/pascha_day_hour_index.csv:row 23257; source_ref=Ps 122:1-2` |
| Printed: Tuesday | Psalm | Ps 119:154-155 | `historical_witness` | `historical_witness` | `rid_fb9b51f4d643d2e8c5fb` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5142; source_ref=Ps 119:154-155` |

## Tuesday: Sixth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Tuesday | Gospel | Jn 8:12-20 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_388d1961e4babe1f51e7` | `out/data/pascha_day_hour_index.csv:row 23252; source_ref=Jn 8:12-20` |
| Curated: Tuesday | OT1 | Ezek 21:3-13 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_2e7fe759de5c87f9e998` | `out/data/pascha_day_hour_index.csv:row 23249; source_ref=Ezek 21:3-13` |
| Curated: Tuesday | OT2 | Sir 4:20-5:2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_750abf01725b137f4df5` | `out/data/pascha_day_hour_index.csv:row 23250; source_ref=Sir 4:20-5:2` |
| Curated: Tuesday | OT3 | Isa 1:1-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_3653df6dccdcc78ae8c7` | `out/data/pascha_day_hour_index.csv:row 23251; source_ref=Isa 1:1-9` |
| Curated: Tuesday | Psalm | Ps 18:17,18:48 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_306c92572ab54418baf7` | `out/data/pascha_day_hour_index.csv:row 23253; source_ref=Ps 18:17,18:48` |

## Tuesday: Ninth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Tuesday | Gospel | Matt 24:3-35 | `historical_witness` | `historical_witness` | `rid_0235a0e85b16bc465a27` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5865; source_ref=Matt 24:3-35` |
| Curated: Tuesday | Gospel | Matt 21:23-27 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_68809512622d19856234` | `out/data/pascha_day_hour_index.csv:row 23247; source_ref=Matt 21:23-27` |
| Curated: Tuesday | OT1 | Gen 6:5-9:7 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_ac097753b41af879d334` | `out/data/pascha_day_hour_index.csv:row 23244; source_ref=Gen 6:5-9:7` |
| Curated: Tuesday | OT2 | Isa 40:1-5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_07a98121b2a6c00d24d1` | `out/data/pascha_day_hour_index.csv:row 23245; source_ref=Isa 40:1-5` |
| Curated: Tuesday | OT3 | Prov 1:1-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_c68c8617c19b143a586d` | `out/data/pascha_day_hour_index.csv:row 23246; source_ref=Prov 1:1-9` |
| Printed: Tuesday | Prophecy | Dan 7:9-15 | `historical_witness` | `historical_witness` | `rid_25c8c5d637c93bd11dcb` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5753; source_ref=Dan 7:9-15` |
| Printed: Tuesday | Prophecy | Isa 40:9-31 | `historical_witness` | `historical_witness` | `rid_4d92d06751339ef3ceae` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5694; source_ref=Isa 40:9-31` |
| Printed: Tuesday | Prophecy | Prov 8:1-12 | `historical_witness` | `historical_witness` | `rid_6a489a43e790eefa21bb` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5771; source_ref=Prov 8:1-12` |
| Printed: Tuesday | Prophecy | Prov 9:1-11 | `historical_witness` | `historical_witness` | `rid_f5bab1a621383392ade1` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5662; source_ref=Prov 9:1-11` |
| Curated: Tuesday | Psalm | Ps 65:4-5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_751349005e100c368a1f` | `out/data/pascha_day_hour_index.csv:row 23248; source_ref=Ps 65:4-5` |
| Printed: Tuesday | Psalm | Ps 25:1-3 | `historical_witness` | `historical_witness` | `rid_df5af56dbe2102144cea` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 5847; source_ref=Ps 25:1-3` |

## Tuesday: Eleventh Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Tuesday | Gospel | Matt 25:14-26:2 | `historical_witness` | `historical_witness` | `rid_3bc4b2afd00d29375c46` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6139; source_ref=Matt 25:14-26:2` |
| Curated: Tuesday | Gospel | Jn 8:51-59 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_6297f04e598f02483db6` | `out/data/pascha_day_hour_index.csv:row 23237; source_ref=Jn 8:51-59` |
| Curated: Tuesday | OT1 | Isa 50:1-3 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d5c12afc31445328b9db` | `out/data/pascha_day_hour_index.csv:row 23235; source_ref=Isa 50:1-3` |
| Curated: Tuesday | OT2 | Wis 2:20-30 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_eead85a0820420a96aa4` | `out/data/pascha_day_hour_index.csv:row 23236; source_ref=Wis 2:20-30` |
| Printed: Tuesday | Prophecy | Isa 30:25-30 | `historical_witness` | `historical_witness` | `rid_e26edbf31ba81691553f` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6015; source_ref=Isa 30:25-30` |
| Printed: Tuesday | Prophecy | Prov 6:20-7:4 | `historical_witness` | `historical_witness` | `rid_ee62339c9f14d60ecc90` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6036; source_ref=Prov 6:20-7:4` |
| Curated: Tuesday | Psalm | Ps 13:3-4 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_40095a8e6eb6be324215` | `out/data/pascha_day_hour_index.csv:row 23238; source_ref=Ps 13:3-4` |
| Printed: Tuesday | Psalm | Ps 12:3-4 | `historical_witness` | `historical_witness` | `rid_fa9fd9c616ba14e4e096` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 6129; source_ref=Ps 12:3-4` |

## Eve of Thursday: Third Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/wednesday--thursday-eve--3rd-hour.txt`; SHA-256 `82d58ce7caa09a34981bb0a76883109fd19196aa108388ae71719d86ec885423`; title `Covenant Thursday Eve (The Third Hour)`.

- Line 12: Amos 4:4-13
- Line 143: Psalm 54:18, 1
- Line 158: Mark 14:3-11

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Great Thursday Eve | Prophecy | Amos 4:4-13 | `historical_witness` | `historical_witness` | `rid_f23108743b2fcb166bc2` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8690; source_ref=Amos 4:4-13` |
| Printed: Thursday Eve | Gospel | Mark 14:3-11 | `historical_witness` | `historical_witness` | `rid_16b69d94202a0f29db61` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8775; source_ref=Mark 14:3-11` |
| Printed: Thursday Eve | Psalm | Ps 55:1,55:21 | `historical_witness` | `historical_witness` | `rid_27d71d747dfcfbcc912a` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8758; source_ref=Ps 55:1,55:21` |
| Curated: Wednesday Eve | Gospel | Mark 14:3-11 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_16b69d94202a0f29db61` | `out/data/pascha_day_hour_index.csv:row 81; source_ref=Ps 55:21,1; Mark 14:3-11` |
| Curated: Wednesday Eve | OT1 | Amos 4:4-13 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_f23108743b2fcb166bc2` | `out/data/pascha_day_hour_index.csv:row 80; source_ref=Amos 4:4-13` |
| Curated: Wednesday Eve | Psalm | Ps 55:1,55:21 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_27d71d747dfcfbcc912a` | `out/data/pascha_day_hour_index.csv:row 81; source_ref=Ps 55:21,1; Mark 14:3-11` |

## Eve of Thursday: Sixth Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/wednesday--thursday-eve--6th-hour.txt`; SHA-256 `f814e9a87ee846c623c65a12a3b9c3cfd32ce407848ffd8723f19be37c984da2`; title `Covenant Thursday Eve (The Sixth Hour)`.

- Line 12: Amos 3:1-11
- Line 128: Psalm 139:1,2
- Line 142: John 12:36-43

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Great Thursday Eve | Prophecy | Amos 3:1-11 | `historical_witness` | `historical_witness` | `rid_d9aa414c906f6cccaa02` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8861; source_ref=Amos 3:1-11` |
| Printed: Thursday Eve | Gospel | Jn 12:36-43 | `historical_witness` | `historical_witness` | `rid_5c9302e6d595d190dd11` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8926; source_ref=Jn 12:36-43` |
| Printed: Thursday Eve | Psalm | Ps 140:1-2 | `historical_witness` | `historical_witness` | `rid_2b3bfed7deba70a54429` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8913; source_ref=Ps 140:1-2` |
| Curated: Wednesday Eve | Gospel | Jn 12:36-43 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_5c9302e6d595d190dd11` | `out/data/pascha_day_hour_index.csv:row 83; source_ref=Ps 140:1,2; John 12:36-43` |
| Curated: Wednesday Eve | OT1 | Amos 3:1-11 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_d9aa414c906f6cccaa02` | `out/data/pascha_day_hour_index.csv:row 82; source_ref=Amos 3:1-11` |
| Curated: Wednesday Eve | Psalm | Ps 140:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_2b3bfed7deba70a54429` | `out/data/pascha_day_hour_index.csv:row 83; source_ref=Ps 140:1,2; John 12:36-43` |

## Eve of Thursday: Ninth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Great Thursday Eve | Prophecy | Jer 9:7-11 | `historical_witness` | `historical_witness` | `rid_000333f2b55f4f89b928` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13076; source_ref=Jer 9:7-11` |
| Printed: Great Thursday Eve | Prophecy | Ezek 20:27-33 | `historical_witness` | `historical_witness` | `rid_881bb20c0cd652123171` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 9049; source_ref=Ezek 20:27-33` |
| Printed: Thursday Eve | Gospel | Jn 10:29-38 | `historical_witness` | `historical_witness` | `rid_c131556038d5f2b24bfe` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 9100; source_ref=Jn 10:29-38` |
| Printed: Thursday Eve | Psalm | Ps 7:1-2 | `historical_witness` | `historical_witness` | `rid_e702dda75f0ea453f291` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 9080; source_ref=Ps 7:1-2` |
| Curated: Wednesday Eve | Gospel | Jn 10:29-38 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_c131556038d5f2b24bfe` | `out/data/pascha_day_hour_index.csv:row 85; source_ref=Ps 7:1-2; John 10:29-38` |
| Curated: Wednesday Eve | OT1 | Ezek 20:27-33 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_881bb20c0cd652123171` | `out/data/pascha_day_hour_index.csv:row 84; source_ref=Ezek 20:27-33` |
| Curated: Wednesday Eve | Psalm | Ps 7:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_e702dda75f0ea453f291` | `out/data/pascha_day_hour_index.csv:row 85; source_ref=Ps 7:1-2; John 10:29-38` |

## Eve of Thursday: Eleventh Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Great Thursday Eve | Prophecy | Jer 8:4-9 | `historical_witness` | `historical_witness` | `rid_16337d9b7cbd88ba893e` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 9194; source_ref=Jer 8:4-9` |
| Printed: Thursday Eve | Gospel | Jn 12:44-50 | `historical_witness` | `historical_witness` | `rid_5e19e735d67290e758ed` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 9233; source_ref=Jn 12:44-50` |
| Printed: Thursday Eve | Psalm | Ps 62:6-7 | `historical_witness` | `historical_witness` | `rid_8be9daf4ab53e4424614` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 9225; source_ref=Ps 62:6-7` |
| Curated: Wednesday Eve | Gospel | Jn 11:55-57 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_86a14760f5eee2200c69` | `out/data/pascha_day_hour_index.csv:row 87; source_ref=Ps 57:1; John 11:55-57` |
| Curated: Wednesday Eve | OT1 | Wis 7:24-30 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_911892923f645ebfa5fb` | `out/data/pascha_day_hour_index.csv:row 86; source_ref=Wis 7:24-30` |
| Curated: Wednesday Eve | Psalm | Ps 57:1 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_6dcf6122d785e98450f1` | `out/data/pascha_day_hour_index.csv:row 87; source_ref=Ps 57:1; John 11:55-57` |

## Wednesday: First Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Wednesday | OT4 | Wis 1:20-2:15 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_18b6dea20e9d1e9ef8dd` | `out/data/pascha_day_hour_index.csv:row 59; source_ref=Wis 1:20-2:15` |
| Curated: Wednesday | OT5 | Wis 3:12-24 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_636dfd619b2a6d26e7c7` | `out/data/pascha_day_hour_index.csv:row 60; source_ref=Wis 3:12-24` |

## Wednesday: Third Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Wednesday | OT3 | Prov 4:4-27,5:1-4 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_848c8fc9d17938a036f1` | `out/data/pascha_day_hour_index.csv:row 64; source_ref=Prov 4:4-5:4` |
| Printed: Wednesday | Prophecy | Prov 4:4-27,5:1-4 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_848c8fc9d17938a036f1` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 7552; source_ref=Prov 4:4-27,5:1-4` |
| Printed: Wednesday | Prophecy | Job 27:16-28:2 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_d6ad5776f0ccbae35639` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 7519; source_ref=Job 27:16-28:2` |
| Curated: Wednesday of Holy Pascha | Psalm | Ps 41:1,41:6 | `pending_psalm_equivalence_unresolved` | `pending_psalm_equivalence_unresolved` | `rid_ec764e70bc1afcf5a3fc` | `out/data/pascha_day_hour_index.csv:row 65; source_ref=Ps 41:6,1; Luke 22:1-6` |

## Wednesday: Sixth Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/wednesday--wednesday-day--6th-hour.txt`; SHA-256 `f6f24456423d691caa5bcad3aa46cd44c44c60646000b3cd2229c48b3180bfb5`; title `Wednesday (The Sixth Hour)`.

- Line 12: Exodus 14:13-15:1
- Line 86: Sirach 23:7-19
- Line 357: Psalm 82:2, 4
- Line 371: John 12:1-8

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Wednesday | OT3 | Job 28:1-2 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_bcacd0a510d40997540d` | `out/data/pascha_day_hour_index.csv:row 68; source_ref=Job 27:16-20; Job 28:1-2` |
| Curated: Wednesday | OT3 | Job 27:16-20 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_ca96f0f620d9e3e08225` | `out/data/pascha_day_hour_index.csv:row 68; source_ref=Job 27:16-20; Job 28:1-2` |
| Curated: Wednesday of Holy Pascha | Psalm | Ps 83:2,83:5 | `pending_psalm_equivalence_unresolved` | `pending_psalm_equivalence_unresolved` | `rid_494b4f4a32be5964f7a7` | `out/data/pascha_day_hour_index.csv:row 69; source_ref=Ps 83:2,5; John 12:1-8` |

## Wednesday: Ninth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Wednesday of Holy Pascha | OT3 | Prov 1:11-35 | `current_confirmed_by_fixture_equivalence` | `current_confirmed_by_fixture_equivalence` | `rid_b7a5aa85795a1f68b5a2` | `out/data/pascha_day_hour_index.csv:row 72; source_ref=Prov 1:11-35` |
| Curated: Wednesday | OT4 | Isa 59:1-17 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_4eb25ced32de0a82f2e8` | `out/data/pascha_day_hour_index.csv:row 73; source_ref=Isa 59:1-17` |
| Curated: Wednesday | OT5 | Zech 11:11-14 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_e09e980c6a31758ca3a0` | `out/data/pascha_day_hour_index.csv:row 74; source_ref=Zech 11:11-14` |
| Printed: Wednesday | Prophecy | Prov 1:10-33 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_8091c39de4e32d4ce20d` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8038; source_ref=Prov 1:10-33` |
| Printed: Wednesday | Psalm | Ps 41:5-7 | `historical_witness` | `historical_witness` | `rid_c1d60b035931158ae984` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8190; source_ref=Ps 41:5-7` |
| Curated: Wednesday | Psalm | Ps 41:5-6 | `pending_psalm_equivalence_unresolved` | `pending_psalm_equivalence_unresolved` | `rid_dacc0ef488f6aaeb8c7d` | `out/data/pascha_day_hour_index.csv:row 75; source_ref=Ps 41:5-6; Matt 26:3-16` |
| Printed: Wednesday | Ninth Hour | Prophecy | Isa 48:1-6 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_0454a5416c3e8f3cf699` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 7779; source_ref=Isa 48:1-6` |
| Printed: Wednesday | Ninth Hour | Prophecy | Isa 59:1-17 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_4eb25ced32de0a82f2e8` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8091; source_ref=Isa 59:1-17` |
| Printed: Wednesday | Ninth Hour | Prophecy | Zech 11:11-14 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_e09e980c6a31758ca3a0` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8133; source_ref=Zech 11:11-14` |

## Wednesday: Eleventh Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/wednesday--wednesday-day--11th-hour.txt`; SHA-256 `176c2b256e21c2a43045ae7c2f258d6b96212f7adabef669f92cde6c89180b13`; title `Wednesday (The Eleventh Hour)`.

- Line 12: Isaiah 28:16-29
- Line 174: Psalm 6:2-3,68:17
- Line 188: John 12:27-36

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Wednesday | Psalm | Ps 6:2-3,69:17 | `historical_witness` | `historical_witness` | `rid_074f82179a447e761e63` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 8419; source_ref=Ps 6:2-3,69:17` |
| Curated: Wednesday of Holy Pascha | Psalm | Ps 6:2-3 | `pending_psalm_equivalence_unresolved` | `pending_psalm_equivalence_unresolved` | `rid_6a749188726ed430761c` | `out/data/pascha_day_hour_index.csv:row 77; source_ref=Ps 6:2-3; Ps 69:17; John 12:27-36` |
| Curated: Wednesday | Psalm | Ps 69:17 | `pending_psalm_equivalence_unresolved` | `pending_psalm_equivalence_unresolved` | `rid_f7dce566f98596f724e3` | `out/data/pascha_day_hour_index.csv:row 77; source_ref=Ps 6:2-3; Ps 69:17; John 12:27-36` |

## Eve of Friday: First Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/thursday--friday-eve--1st-hour.txt`; SHA-256 `d0cb858677025a5968b48b27ebea7325d41a7240e8dc1b15704010a8c455a2fc`; title `Great Friday Eve (The First Hour)`.

- Line 12: Jeremiah 8:17-9:6
- Line 125: Psalm 101:1,7
- Line 139: John 13:33-14:25
- Line 258: John 14:26-15:25
- Line 355: John 15:26-16:33
- Line 458: John 17:1-26

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Good Friday Eve | Gospel | Jn 13:33-14:25 | `historical_witness` | `historical_witness` | `rid_773de5842dcd7f21c1c7` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12168; source_ref=Jn 13:33-14:25` |
| Printed: Good Friday Eve | Gospel | Jn 17:1-26 | `historical_witness` | `historical_witness` | `rid_bab24240810a4c3ee83b` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12448; source_ref=Jn 17:1-26` |
| Printed: Good Friday Eve | Gospel | Jn 15:26-16:33 | `historical_witness` | `historical_witness` | `rid_d2ef1aec8036b3eecd7d` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12353; source_ref=Jn 15:26-16:33` |
| Printed: Good Friday Eve | Gospel | Jn 14:26-15:25 | `historical_witness` | `historical_witness` | `rid_e69055fe05d746b7a23e` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12251; source_ref=Jn 14:26-15:25` |
| Printed: Good Friday Eve | Psalm | Ps 102:1,102:8 | `historical_witness` | `historical_witness` | `rid_42043da3e6566eeb0e98` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12153; source_ref=Ps 102:1,102:8` |
| Curated: Great Thursday Eve | Gospel | Jn 13:33-14:25 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_773de5842dcd7f21c1c7` | `out/data/pascha_day_hour_index.csv:row 114; source_ref=Ps 69:1,9; John 13:33-14:25; John 14:26-15:25; John 15:26-16:33; John 17:1-26` |
| Curated: Great Thursday Eve | Gospel | Jn 17:1-26 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_bab24240810a4c3ee83b` | `out/data/pascha_day_hour_index.csv:row 114; source_ref=Ps 69:1,9; John 13:33-14:25; John 14:26-15:25; John 15:26-16:33; John 17:1-26` |
| Curated: Great Thursday Eve | Gospel | Jn 15:26-16:33 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_d2ef1aec8036b3eecd7d` | `out/data/pascha_day_hour_index.csv:row 114; source_ref=Ps 69:1,9; John 13:33-14:25; John 14:26-15:25; John 15:26-16:33; John 17:1-26` |
| Curated: Great Thursday Eve | Gospel | Jn 14:26-15:25 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_e69055fe05d746b7a23e` | `out/data/pascha_day_hour_index.csv:row 114; source_ref=Ps 69:1,9; John 13:33-14:25; John 14:26-15:25; John 15:26-16:33; John 17:1-26` |
| Curated: Great Thursday Eve | OT1 | Jer 8:17-9:6 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_11318755d7e7bb01e045` | `out/data/pascha_day_hour_index.csv:row 113; source_ref=Jer 8:17-9:6` |
| Curated: Great Thursday Eve | Psalm | Ps 69:1,69:9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_73f7d128f9f5b1e1bb13` | `out/data/pascha_day_hour_index.csv:row 114; source_ref=Ps 69:1,9; John 13:33-14:25; John 14:26-15:25; John 15:26-16:33; John 17:1-26` |

## Eve of Friday: Third Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/thursday--friday-eve--3rd-hour.txt`; SHA-256 `5b80e7e053aaa9408689f1cf0ccfdc3a862f4b84be30899e64bed4fd88fb0c45`; title `Great Friday Eve (The Third Hour)`.

- Line 12: Ezekiel 36:16-23
- Line 113: Psalm 108:1,2
- Line 127: Matthew 26:30-35
- Line 177: Mark 14:26-31
- Line 211: Luke 22:31-39
- Line 251: John 18:1,2

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Good Friday Eve | Gospel | Jn 18:1-2 | `historical_witness` | `historical_witness` | `rid_7bbf527f8f5e9506d796` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12747; source_ref=Jn 18:1-2` |
| Printed: Good Friday Eve | Gospel | Mark 14:26-31 | `historical_witness` | `historical_witness` | `rid_7e14e2f07af8158c8b9b` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12696; source_ref=Mark 14:26-31` |
| Printed: Good Friday Eve | Gospel | Lk 22:31-39 | `historical_witness` | `historical_witness` | `rid_9e07e002c25695ea73d1` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12727; source_ref=Lk 22:31-39` |
| Printed: Good Friday Eve | Gospel | Matt 26:30-35 | `historical_witness` | `historical_witness` | `rid_e0e34ff78ea55157b2aa` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12667; source_ref=Matt 26:30-35` |
| Printed: Good Friday Eve | Psalm | Ps 55:1,55:21 | `historical_witness` | `historical_witness` | `rid_27d71d747dfcfbcc912a` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12643; source_ref=Ps 55:1,55:21` |
| Curated: Great Thursday Eve | Gospel | Jn 18:1-2 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_7bbf527f8f5e9506d796` | `out/data/pascha_day_hour_index.csv:row 116; source_ref=Ps 108:1,2; Matt 26:30-35; Mark 14:26-31; Luke 22:31-39; John 18:1,2` |
| Curated: Great Thursday Eve | Gospel | Mark 14:26-31 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_7e14e2f07af8158c8b9b` | `out/data/pascha_day_hour_index.csv:row 116; source_ref=Ps 108:1,2; Matt 26:30-35; Mark 14:26-31; Luke 22:31-39; John 18:1,2` |
| Curated: Great Thursday Eve | Gospel | Lk 22:31-39 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_9e07e002c25695ea73d1` | `out/data/pascha_day_hour_index.csv:row 116; source_ref=Ps 108:1,2; Matt 26:30-35; Mark 14:26-31; Luke 22:31-39; John 18:1,2` |
| Curated: Great Thursday Eve | Gospel | Matt 26:30-35 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_e0e34ff78ea55157b2aa` | `out/data/pascha_day_hour_index.csv:row 116; source_ref=Ps 108:1,2; Matt 26:30-35; Mark 14:26-31; Luke 22:31-39; John 18:1,2` |
| Curated: Great Thursday Eve | OT1 | Ezek 36:16-23 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_3576dbba679c4d5bfd4c` | `out/data/pascha_day_hour_index.csv:row 115; source_ref=Ezek 36:16-23` |
| Curated: Great Thursday Eve | Psalm | Ps 108:1-2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_4fc32b9f114c5f1160fd` | `out/data/pascha_day_hour_index.csv:row 116; source_ref=Ps 108:1,2; Matt 26:30-35; Mark 14:26-31; Luke 22:31-39; John 18:1,2` |

## Eve of Friday: Sixth Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/thursday--friday-eve--6th-hour.txt`; SHA-256 `2e7845ddfcb74941322020129c2d3078f7909aece7cd1c7c4c12522de1981001`; title `Great Friday Eve (The Sixth Hour)`.

- Line 12: Ezekiel 22:23-28
- Line 110: Psalm 58:1,68:18
- Line 124: Matthew 26:36-46
- Line 189: Mark 14:32-42
- Line 241: Luke 22:40-46
- Line 278: John 18:3-9

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Good Friday Eve | Gospel | Mark 14:32-42 | `historical_witness` | `historical_witness` | `rid_1bd466dd3b9c1441c100` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12916; source_ref=Mark 14:32-42` |
| Printed: Good Friday Eve | Gospel | Lk 22:40-46 | `historical_witness` | `historical_witness` | `rid_571eacc33855c99b5a88` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12950; source_ref=Lk 22:40-46` |
| Printed: Good Friday Eve | Gospel | Jn 18:3-9 | `historical_witness` | `historical_witness` | `rid_5cdda0225a73ab9902d6` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12972; source_ref=Jn 18:3-9` |
| Printed: Good Friday Eve | Gospel | Matt 26:36-46 | `historical_witness` | `historical_witness` | `rid_81b030906fd3b5f4e131` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12875; source_ref=Matt 26:36-46` |
| Printed: Good Friday Eve | Psalm | Ps 59:1,69:20 | `historical_witness` | `historical_witness` | `rid_4c448abd6b7a623e2919` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 12866; source_ref=Ps 59:1,69:20` |
| Curated: Great Thursday Eve | Gospel | Mark 14:32-42 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_1bd466dd3b9c1441c100` | `out/data/pascha_day_hour_index.csv:row 118; source_ref=Ps 58:2; Ps 68:21; Matt 26:36-46; Mark 14:32-42; Luke 22:40-46; John 18:3-9` |
| Curated: Great Thursday Eve | Gospel | Lk 22:40-46 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_571eacc33855c99b5a88` | `out/data/pascha_day_hour_index.csv:row 118; source_ref=Ps 58:2; Ps 68:21; Matt 26:36-46; Mark 14:32-42; Luke 22:40-46; John 18:3-9` |
| Curated: Great Thursday Eve | Gospel | Jn 18:3-9 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_5cdda0225a73ab9902d6` | `out/data/pascha_day_hour_index.csv:row 118; source_ref=Ps 58:2; Ps 68:21; Matt 26:36-46; Mark 14:32-42; Luke 22:40-46; John 18:3-9` |
| Curated: Great Thursday Eve | Gospel | Matt 26:36-46 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_81b030906fd3b5f4e131` | `out/data/pascha_day_hour_index.csv:row 118; source_ref=Ps 58:2; Ps 68:21; Matt 26:36-46; Mark 14:32-42; Luke 22:40-46; John 18:3-9` |
| Curated: Great Thursday Eve | OT1 | Ezek 22:23-28 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_b938964452264e52d765` | `out/data/pascha_day_hour_index.csv:row 117; source_ref=Ezek 22:23-28` |
| Curated: Great Thursday Eve | Psalm | Ps 58:2 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_536eb23be781b53a4cd0` | `out/data/pascha_day_hour_index.csv:row 118; source_ref=Ps 58:2; Ps 68:21; Matt 26:36-46; Mark 14:32-42; Luke 22:40-46; John 18:3-9` |
| Curated: Great Thursday Eve | Psalm | Ps 68:21 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_a4245be46930b4fccb8b` | `out/data/pascha_day_hour_index.csv:row 118; source_ref=Ps 58:2; Ps 68:21; Matt 26:36-46; Mark 14:32-42; Luke 22:40-46; John 18:3-9` |

## Eve of Friday: Ninth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Good Friday Eve | Gospel | Matt 26:47-58 | `historical_witness` | `historical_witness` | `rid_3fef339e84720cf43736` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13136; source_ref=Matt 26:47-58` |
| Printed: Good Friday Eve | Gospel | Mark 14:43-54 | `historical_witness` | `historical_witness` | `rid_9cb6d212470da10befe0` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13168; source_ref=Mark 14:43-54` |
| Printed: Good Friday Eve | Gospel | Lk 22:47-55 | `historical_witness` | `historical_witness` | `rid_b879c3ed81eee1a870e2` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13200; source_ref=Lk 22:47-55` |
| Printed: Good Friday Eve | Gospel | Jn 18:10-14 | `historical_witness` | `historical_witness` | `rid_e6215706f1c6ecf05620` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13230; source_ref=Jn 18:10-14` |
| Printed: Good Friday Eve | Prophecy | Ezek 21:28-32 | `historical_witness` | `historical_witness` | `rid_a8741a547e4efd582561` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13099; source_ref=Ezek 21:28-32` |
| Printed: Good Friday Eve | Psalm | Ps 28:3-4,35:4 | `historical_witness` | `historical_witness` | `rid_c5ea83e1e74bc08d8bcd` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13112; source_ref=Ps 28:3-4,35:4` |
| Curated: Great Thursday Eve | Gospel | Matt 26:47-58 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_3fef339e84720cf43736` | `out/data/pascha_day_hour_index.csv:row 121; source_ref=Ps 27:3,4; Ps 34:4,5; Matt 26:47-58; Mark 14:43-54; Luke 22:47-55; John 18:10-14` |
| Curated: Great Thursday Eve | Gospel | Mark 14:43-54 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_9cb6d212470da10befe0` | `out/data/pascha_day_hour_index.csv:row 121; source_ref=Ps 27:3,4; Ps 34:4,5; Matt 26:47-58; Mark 14:43-54; Luke 22:47-55; John 18:10-14` |
| Curated: Great Thursday Eve | Gospel | Lk 22:47-55 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_b879c3ed81eee1a870e2` | `out/data/pascha_day_hour_index.csv:row 121; source_ref=Ps 27:3,4; Ps 34:4,5; Matt 26:47-58; Mark 14:43-54; Luke 22:47-55; John 18:10-14` |
| Curated: Great Thursday Eve | Gospel | Jn 18:10-14 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_e6215706f1c6ecf05620` | `out/data/pascha_day_hour_index.csv:row 121; source_ref=Ps 27:3,4; Ps 34:4,5; Matt 26:47-58; Mark 14:43-54; Luke 22:47-55; John 18:10-14` |
| Curated: Great Thursday Eve | OT1 | Jer 9:6-10 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_6d48106270b82e0e3bd4` | `out/data/pascha_day_hour_index.csv:row 119; source_ref=Jer 9:6-10` |
| Curated: Great Thursday Eve | OT2 | Ezek 21:33-37 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_be75fb5a12d73aea27b2` | `out/data/pascha_day_hour_index.csv:row 120; source_ref=Ezek 21:33-37` |
| Curated: Great Thursday Eve | Psalm | Ps 34:4-5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_ba5d92f2cccde70ce528` | `out/data/pascha_day_hour_index.csv:row 121; source_ref=Ps 27:3,4; Ps 34:4,5; Matt 26:47-58; Mark 14:43-54; Luke 22:47-55; John 18:10-14` |
| Curated: Great Thursday Eve | Psalm | Ps 27:3-4 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d81492ec89e2325d0531` | `out/data/pascha_day_hour_index.csv:row 121; source_ref=Ps 27:3,4; Ps 34:4,5; Matt 26:47-58; Mark 14:43-54; Luke 22:47-55; John 18:10-14` |

## Eve of Friday: Eleventh Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Good Friday Eve | Gospel | Mark 14:55-72 | `historical_witness` | `historical_witness` | `rid_23f384e2033d8d427492` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13474; source_ref=Mark 14:55-72` |
| Printed: Good Friday Eve | Gospel | Jn 18:15-27 | `historical_witness` | `historical_witness` | `rid_36c4d61e50be4ea3e396` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13557; source_ref=Jn 18:15-27` |
| Printed: Good Friday Eve | Gospel | Matt 26:59-75 | `historical_witness` | `historical_witness` | `rid_d17124a46d930986c11b` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13422; source_ref=Matt 26:59-75` |
| Printed: Good Friday Eve | Gospel | Lk 22:56-65 | `historical_witness` | `historical_witness` | `rid_d6c8e6988b3a6d0846fb` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13526; source_ref=Lk 22:56-65` |
| Printed: Good Friday Eve | Psalm | Ps 2:1-2,2:4-5 | `historical_witness` | `historical_witness` | `rid_6e43995c594aaa1275b8` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13402; source_ref=Ps 2:1-2,2:4-5` |
| Curated: Great Thursday Eve | Gospel | Mark 14:55-72 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_23f384e2033d8d427492` | `out/data/pascha_day_hour_index.csv:row 123; source_ref=Ps 2:1-5; Matt 26:59-75; Mark 14:55-72; Luke 22:56-65; John 18:15-27` |
| Curated: Great Thursday Eve | Gospel | Jn 18:15-27 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_36c4d61e50be4ea3e396` | `out/data/pascha_day_hour_index.csv:row 123; source_ref=Ps 2:1-5; Matt 26:59-75; Mark 14:55-72; Luke 22:56-65; John 18:15-27` |
| Curated: Great Thursday Eve | Gospel | Matt 26:59-75 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d17124a46d930986c11b` | `out/data/pascha_day_hour_index.csv:row 123; source_ref=Ps 2:1-5; Matt 26:59-75; Mark 14:55-72; Luke 22:56-65; John 18:15-27` |
| Curated: Great Thursday Eve | Gospel | Lk 22:56-65 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d6c8e6988b3a6d0846fb` | `out/data/pascha_day_hour_index.csv:row 123; source_ref=Ps 2:1-5; Matt 26:59-75; Mark 14:55-72; Luke 22:56-65; John 18:15-27` |
| Curated: Great Thursday Eve | OT1 | Isa 27:11-28:15 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d0c31ecd81d3e2ebb47a` | `out/data/pascha_day_hour_index.csv:row 122; source_ref=Isa 27:11-28:15` |
| Curated: Great Thursday Eve | Psalm | Ps 2:1-5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_508ef855fc183ab65082` | `out/data/pascha_day_hour_index.csv:row 123; source_ref=Ps 2:1-5; Matt 26:59-75; Mark 14:55-72; Luke 22:56-65; John 18:15-27` |

## Great Thursday: First Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Great Thursday | Acts | Acts 1:15-20 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_9397f57ff763d3a220e3` | `out/data/pascha_day_hour_index.csv:row 92; source_ref=Acts 1:15-20` |
| Curated: Great Thursday | Gospel | Lk 22:7-13 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_1ff72330fa7eb181c3b0` | `out/data/pascha_day_hour_index.csv:row 93; source_ref=Ps 55:21,12; Luke 22:7-13` |
| Curated: Great Thursday | OT1 | Exod 17:8-16 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_191a72ac88bd1c4d0822` | `out/data/pascha_day_hour_index.csv:row 88; source_ref=Exod 17:8-16` |
| Curated: Great Thursday | OT2 | Exod 15:22-16:3 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_7397ed77b1c667a984cd` | `out/data/pascha_day_hour_index.csv:row 89; source_ref=Exod 15:22-16:3` |
| Curated: Great Thursday | OT3 | Isa 58:1-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_bead7107aacfe0ce9e81` | `out/data/pascha_day_hour_index.csv:row 90; source_ref=Isa 58:1-9` |
| Curated: Great Thursday | OT4 | Ezek 18:20-32 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_9ecc8c399393c3ead32d` | `out/data/pascha_day_hour_index.csv:row 91; source_ref=Ezek 18:20-32` |
| Printed: Great Thursday | Prophecy | Exod 15:23-16:3 | `historical_witness` | `historical_witness` | `rid_5d8c3d9ac563f4f03e39` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 9373; source_ref=Exod 15:23-16:3` |
| Printed: Great Thursday | Prophecy | Isa 58:1-11 | `historical_witness` | `historical_witness` | `rid_7002fcf1a7d6c8d16f97` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 9429; source_ref=Isa 58:1-11` |
| Curated: Great Thursday | Psalm | Ps 55:12,55:21 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_de17044db159b36da2c9` | `out/data/pascha_day_hour_index.csv:row 93; source_ref=Ps 55:21,12; Luke 22:7-13` |

## Great Thursday: Sixth Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/thursday--thursday-day--6th-hour.txt`; SHA-256 `4318fbbce5db75e4033b7f56f9487be2b4d9ffa051dfea33d78051984add367e`; title `Covenant Thursday (The Sixth Hour)`.

- Line 12: Jeremiah 7:1-15
- Line 68: Ezekiel 20:39-44
- Line 106: Sirach 12:13-13:1
- Line 207: Psalm 30:18,13
- Line 221: Mark 14:12-16

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Great Thursday | Gospel | Mark 14:12-16 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_a284b3c1bdcb5a87067f` | `out/data/pascha_day_hour_index.csv:row 102; source_ref=Ps 31:18,13; Mark 14:12-16` |
| Curated: Great Thursday | OT1 | Exod 7:2-15 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_f231e32d73929615cd22` | `out/data/pascha_day_hour_index.csv:row 99; source_ref=Exod 7:2-15` |
| Curated: Great Thursday | OT2 | Ezek 20:39-44 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_3494c221c851bd7abef8` | `out/data/pascha_day_hour_index.csv:row 100; source_ref=Ezek 20:39-44` |
| Curated: Great Thursday | OT3 | Wis 12:13-13:1 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_96f759a6c378438099f0` | `out/data/pascha_day_hour_index.csv:row 101; source_ref=Wis 12:13-13:1` |
| Printed: Great Thursday | Prophecy | Jer 7:2-15 | `historical_witness` | `historical_witness` | `rid_1cb2d1b2c02e66478268` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10028; source_ref=Jer 7:2-15` |
| Printed: Great Thursday | Prophecy | Sir 23:7-14 | `historical_witness` | `historical_witness` | `rid_95b8bc94505475351957` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10103; source_ref=Sir 23:7-14` |
| Curated: Great Thursday | Psalm | Ps 31:13,31:18 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_0460146cc97bb65878fc` | `out/data/pascha_day_hour_index.csv:row 102; source_ref=Ps 31:18,13; Mark 14:12-16` |

## Great Thursday: Liturgy

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: the Covenant Thursday | Psalm | Ps 23:5,41:9 | `historical_witness` | `historical_witness` | `rid_cc534b4c2513e420d4bb` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 11696; source_ref=Ps 23:5,41:9` |

## Great Thursday: Liturgy of Blessing of the Water

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Printed: Great Thursday | Prophecy | Ezek 47:1-9 | `historical_witness` | `historical_witness` | `rid_1f622641fffc8ac04b85` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10823; source_ref=Ezek 47:1-9` |
| Printed: Great Thursday | Prophecy | Isa 55:1-56:1 | `historical_witness` | `historical_witness` | `rid_2159320effb3da6bddcb` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10774; source_ref=Isa 55:1-56:1` |
| Printed: Great Thursday | Prophecy | Ezek 36:25-29 | `historical_witness` | `historical_witness` | `rid_c685890b74f9cd39b3d5` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10802; source_ref=Ezek 36:25-29` |
| Printed: Great Thursday | Prophecy | Isa 4:2-4 | `historical_witness` | `historical_witness` | `rid_f3a1ac3a67cfbdaf1456` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10741; source_ref=Isa 4:2-4` |
| Printed: Great Thursday | Prophecy | Prov 9:1-11 | `historical_witness` | `historical_witness` | `rid_f5bab1a621383392ade1` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10693; source_ref=Prov 9:1-11` |
| Printed: Great Thursday | Psalm | Ps 51:7,51:10 | `historical_witness` | `historical_witness` | `rid_96d87f4353e3c1832d01` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 10949; source_ref=Ps 51:7,51:10` |

## Good Friday: First Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Good Friday | Gospel | Jn 18:28-40 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_0e4e43f572c6fd382090` | `out/data/pascha_day_hour_index.csv:row 53124; source_ref=Jn 18:28-40` |
| Curated: Good Friday | Gospel | Mark 15:1-5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_8eedced3940450abfdfe` | `out/data/pascha_day_hour_index.csv:row 53126; source_ref=Mark 15:1-5` |
| Curated: Good Friday | Gospel | Lk 22:66-23:12 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_e8d2287daadb518b87d7` | `out/data/pascha_day_hour_index.csv:row 53125; source_ref=Lk 22:66-23:12` |
| Curated: Good Friday | Gospel | Matt 27:1-14 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_eb2cbf4361420fe5dd30` | `out/data/pascha_day_hour_index.csv:row 53127; source_ref=Matt 27:1-14` |
| Curated: Good Friday | OT1 | Deut 8:19-9:24 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_0081650c21f311321b1f` | `out/data/pascha_day_hour_index.csv:row 53122; source_ref=Deut 8:19-9:24` |
| Curated: Good Friday | OT10 | Mic 7:1-8 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_2761bfa9758c6e8b9d42` | `out/data/pascha_day_hour_index.csv:row 53123; source_ref=Mic 7:1-8` |
| Curated: Good Friday | OT2 | Isa 1:2-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_4c5e32ae725adad6fccd` | `out/data/pascha_day_hour_index.csv:row 53130; source_ref=Isa 1:2-9` |
| Curated: Good Friday | OT3 | Isa 2:10-21 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_e69cf669f4becb218ff3` | `out/data/pascha_day_hour_index.csv:row 53131; source_ref=Isa 2:10-21` |
| Curated: Good Friday | OT4 | Jer 22:29-23:6 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_83c98f60585bb30ff4b0` | `out/data/pascha_day_hour_index.csv:row 53132; source_ref=Jer 22:29-23:6` |
| Curated: Good Friday | OT5 | Isa 24:1-13 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_242bbbab85a3f359203a` | `out/data/pascha_day_hour_index.csv:row 53133; source_ref=Isa 24:1-13` |
| Curated: Good Friday | OT6 | Wis 2:12-22 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_76cf6c222d44a74c02da` | `out/data/pascha_day_hour_index.csv:row 53134; source_ref=Wis 2:12-22` |
| Curated: Good Friday | OT7 | Job 12:18-13:1 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_1bd94b83cab75135b002` | `out/data/pascha_day_hour_index.csv:row 53135; source_ref=Job 12:18-13:1` |
| Curated: Good Friday | OT8 | Zech 11:11-14 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_e09e980c6a31758ca3a0` | `out/data/pascha_day_hour_index.csv:row 53136; source_ref=Zech 11:11-14` |
| Curated: Good Friday | OT9 | Mic 1:16-2:3 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_bd2d2d2f3e0117058eb5` | `out/data/pascha_day_hour_index.csv:row 53137; source_ref=Mic 1:16-2:3` |
| Printed: Good Friday | Pauline | 1Cor 1:23-2:5 | `historical_witness` | `historical_witness` | `rid_65e4f9cea487eb2f68e7` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 14101; source_ref=1Cor 1:23-2:5` |
| Printed: Good Friday | Prophecy | Job 12:17-13:1 | `historical_witness` | `historical_witness` | `rid_7b236fc4fd0b2fc92efb` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13988; source_ref=Job 12:17-13:1` |
| Printed: Good Friday | Prophecy | Zech 11:14 | `historical_witness` | `historical_witness` | `rid_a9e8d8b0e27f61200a72` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 13900; source_ref=Zech 11:14` |
| Curated: Good Friday | Psalm | Ps 35:11-12,35:16 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_0f8e000caf63f3ea9464` | `out/data/pascha_day_hour_index.csv:row 53129; source_ref=Ps 35:11-12,35:16` |
| Curated: Good Friday | Psalm | Ps 27:12 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_7fcb8d6c012c0e48fded` | `out/data/pascha_day_hour_index.csv:row 53128; source_ref=Ps 27:12` |
| Printed: Good Friday | Psalm | Ps 27:12,35:11-12,35:16 | `historical_witness` | `historical_witness` | `rid_e9cac5a77676e66601d0` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 14158; source_ref=Ps 27:12,35:11-12,35:16` |

## Good Friday: Third Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Good Friday | Gospel | Lk 23:13-25 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_166ab888c1fa87ebe7de` | `out/data/pascha_day_hour_index.csv:row 53167; source_ref=Lk 23:13-25` |
| Curated: Good Friday | Gospel | Matt 27:15-26 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_9e88db33cb573e2da938` | `out/data/pascha_day_hour_index.csv:row 53169; source_ref=Matt 27:15-26` |
| Curated: Good Friday | Gospel | Jn 19:1-12 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d29544c970904a8ee5f2` | `out/data/pascha_day_hour_index.csv:row 53166; source_ref=Jn 19:1-12` |
| Curated: Good Friday | Gospel | Mark 15:6-25 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_ed470e4ffae755d81c63` | `out/data/pascha_day_hour_index.csv:row 53168; source_ref=Mark 15:6-25` |
| Curated: Good Friday | OT1 | Gen 48:1-19 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_0d9c06792fbd4d0fa751` | `out/data/pascha_day_hour_index.csv:row 53159; source_ref=Gen 48:1-19` |
| Curated: Good Friday | OT2 | Isa 50:4-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d6e8dfd11429bf871d5d` | `out/data/pascha_day_hour_index.csv:row 53160; source_ref=Isa 50:4-9` |
| Curated: Good Friday | OT3 | Isa 3:9-15 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_2d7636b67c778e36f4c5` | `out/data/pascha_day_hour_index.csv:row 53161; source_ref=Isa 3:9-15` |
| Curated: Good Friday | OT4 | Isa 63:1-7 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_1c04a2743cc97f065bd4` | `out/data/pascha_day_hour_index.csv:row 53162; source_ref=Isa 63:1-7` |
| Curated: Good Friday | OT5 | Amos 9:8-10 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_37d3df227f76d85086d8` | `out/data/pascha_day_hour_index.csv:row 53164; source_ref=Amos 9:8-10` |
| Curated: Good Friday | OT5 | Amos 9:4-6 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_71b6ff712e8b6696be78` | `out/data/pascha_day_hour_index.csv:row 53163; source_ref=Amos 9:4-6` |
| Curated: Good Friday | OT6 | Job 29:21-30:10 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_d1444a3b6a7ac131d921` | `out/data/pascha_day_hour_index.csv:row 53165; source_ref=Job 29:21-30:10` |
| Printed: Good Friday | Pauline | Col 2:13-15 | `historical_witness` | `historical_witness` | `rid_4b26b5bdc4d77f17c9a4` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 14617; source_ref=Col 2:13-15` |
| Printed: Good Friday | Prophecy | Amos 9:4-5,9:7-10 | `historical_witness` | `historical_witness` | `rid_027380b484c903e50881` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 14547; source_ref=Amos 9:4-5,9:7-10` |
| Printed: Good Friday | Prophecy | Job 29:21-25,30:1-10 | `historical_witness` | `historical_witness` | `rid_70428ebc4e8c9db0312c` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 14580; source_ref=Job 29:21-25,30:1-10` |
| Curated: Good Friday | Psalm | Ps 38:17 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_221d40bdd395f63e0153` | `out/data/pascha_day_hour_index.csv:row 53171; source_ref=Ps 38:17` |
| Curated: Good Friday | Psalm | Ps 22:16 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_f36140316f1c664a1669` | `out/data/pascha_day_hour_index.csv:row 53170; source_ref=Ps 22:16` |

## Good Friday: Ninth Hour

Reader evidence: `sources/coptic-reader/holy-week-review-qualified-2026-10-29/friday--9th-hour.txt`; SHA-256 `be608e44de875f94139f230f9170d23ee3d81a9af56de3cf9e5f9d9dec6312ae`; title `Great Friday (The Ninth Hour)`.

- Line 13: Jeremiah 11:17-12:13
- Line 81: Zechariah 14:5-11
- Line 255: Philippians 2:4-11
- Line 425: Psalm 69:1-2,21
- Line 439: Matthew 27:46-50
- Line 489: Mark 15:34-37
- Line 523: Luke 23:45-46
- Line 548: John 19:28-30

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Good Friday | Gospel | Matt 27:46-50 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_0b612c8635ac0a8f3e74` | `out/data/pascha_day_hour_index.csv:row 53145; source_ref=Matt 27:46-50` |
| Curated: Good Friday | Gospel | Jn 19:28-30 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_33b101d296d4091859e9` | `out/data/pascha_day_hour_index.csv:row 53142; source_ref=Jn 19:28-30` |
| Curated: Good Friday | Gospel | Lk 23:45-46 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_531fe2f5362c3cb5861e` | `out/data/pascha_day_hour_index.csv:row 53143; source_ref=Lk 23:45-46` |
| Curated: Good Friday | Gospel | Mark 15:34-37 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_bd7ac0a5c58afe9d44af` | `out/data/pascha_day_hour_index.csv:row 53144; source_ref=Mark 15:34-37` |
| Curated: Good Friday | OT1 | Jer 11:18-12:13 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_145d2c9c04a366b7ee0b` | `out/data/pascha_day_hour_index.csv:row 53138; source_ref=Jer 11:18-12:13` |
| Curated: Good Friday | OT2 | Zech 14:5-11 | `current_working_source_not_coptic_reader_checked` | `current_confirmed_coptic_reader` | `rid_ac444f7c6aad65034bf2` | `out/data/pascha_day_hour_index.csv:row 53139; source_ref=Zech 14:5-11` |
| Curated: Good Friday | OT3 | Hos 2:1-3,2:10-11 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_51b705f0fe56936ed731` | `out/data/pascha_day_hour_index.csv:row 53140; source_ref=Hos 2:1-3,2:10-11` |
| Printed: Good Friday | Pauline | Phil 2:4-11 | `historical_witness` | `historical_witness` | `rid_459d5b9ccee8e5bb221f` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 15847; source_ref=Phil 2:4-11` |
| Curated: Good Friday | Pauline | Phil 2:5-11 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_f2a5f5034b0412b941ad` | `out/data/pascha_day_hour_index.csv:row 53141; source_ref=Phil 2:5-11` |
| Printed: Good Friday | Prophecy | Joel 2:1-3,2:10-11 | `historical_witness` | `historical_witness` | `rid_4bd7efb34bc72cf518de` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 15774; source_ref=Joel 2:1-3,2:10-11` |
| Printed: Good Friday | Prophecy | Zech 14:6-11 | `historical_witness` | `historical_witness` | `rid_fa9737841503cc362b7b` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 15745; source_ref=Zech 14:6-11` |
| Curated: Good Friday | Psalm | Ps 69:2-3,69:21 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_aeefff0cfc6d2be5b175` | `out/data/pascha_day_hour_index.csv:row 53146; source_ref=Ps 69:2-3,69:21` |
| Printed: Good Friday | Psalm | Ps 69:1-2,69:21 | `historical_witness` | `historical_witness` | `rid_b12c328eec8b0a237b95` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 15975; source_ref=Ps 69:1-2,69:21` |

## Good Friday: Twelfth Hour

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Good Friday | Gospel | Jn 19:38-42 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_012e29237f7019faa707` | `out/data/pascha_day_hour_index.csv:row 53174; source_ref=Jn 19:38-42` |
| Curated: Good Friday | Gospel | Lk 23:50-56 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_32a40ab8ada951a59f7a` | `out/data/pascha_day_hour_index.csv:row 53175; source_ref=Lk 23:50-56` |
| Curated: Good Friday | Gospel | Mark 15:42-16:1 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_354aecd9e2e00fd91078` | `out/data/pascha_day_hour_index.csv:row 53176; source_ref=Mark 15:42-16:1` |
| Curated: Good Friday | Gospel | Matt 27:57-61 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_9edabff24638eaef7b45` | `out/data/pascha_day_hour_index.csv:row 53177; source_ref=Matt 27:57-61` |
| Curated: Good Friday | OT1 | Lam 3:1-66 | `current_confirmed_coptic_reader` | `current_confirmed_coptic_reader` | `rid_af82ad7320273c8eff8f` | `out/data/pascha_day_hour_index.csv:row 53172; source_ref=Lam 3:1-66; sources/coptic-reader/pascha-resolution-qualified-2026-10-25/fresh-pascha/friday--12th-hour.txt:lines 13-90; sha256=9a6bd0b11b67fa6d3cfbe10a99b84a085796b8b3e886ddec4d191ef02dbe2e0e` |
| Curated: Good Friday | OT2 | Jonah 1:10-2:8 | `historical_candidate_removed` | `historical_candidate_removed` | `rid_d468220423ee60d06941` | `out/data/pascha_day_hour_index.csv:row 53173; source_ref=Jonah 1:10-2:8; sources/coptic-reader/pascha-resolution-qualified-2026-10-25/fresh-pascha/friday--12th-hour.txt:lines 13-90; sha256=9a6bd0b11b67fa6d3cfbe10a99b84a085796b8b3e886ddec4d191ef02dbe2e0e` |
| Printed: Good Friday | Prophecy | Jonah 1:10-2:7 | `historical_witness` | `historical_witness` | `rid_c7eb1b93e16f07615b88` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 16643; source_ref=Jonah 1:10-2:7` |
| Curated: Good Friday | Psalm | Ps 88:6 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_8277ab883aace1bee05b` | `out/data/pascha_day_hour_index.csv:row 53180; source_ref=Ps 88:6` |
| Printed: Good Friday | Psalm | Ps 23:4,88:6 | `historical_witness` | `historical_witness` | `rid_8eae32534ce55c8fd946` | `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:line 16683; source_ref=Ps 23:4,88:6` |
| Curated: Good Friday | Psalm | Ps 23:4 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_b32020518c0ff5e87408` | `out/data/pascha_day_hour_index.csv:row 53178; source_ref=Ps 23:4` |
| Curated: Good Friday | Psalm | Ps 45:6,45:8 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_f01b656f3eed91b94a1d` | `out/data/pascha_day_hour_index.csv:row 53179; source_ref=Ps 45:6,45:8` |

## Bright Saturday: Liturgy

Reader: no qualified capture in this retained source pack. Keep unresolved appointments on the check sheet.

| Source/raw label | Slot | Package MT reference | Baseline status | Repair status | Identity | Original source locator |
|---|---|---|---|---|---|---|
| Curated: Bright Saturday | Acts | Acts 3:12-21 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_5312571ad2ea75579e4e` | `out/data/pascha_day_hour_index.csv:row 161; source_ref=Acts 3:12-21` |
| Curated: Bright Saturday | Catholic | 1Pet 1:1-9 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_be832a860aaa1ccbd7b0` | `out/data/pascha_day_hour_index.csv:row 160; source_ref=1Pet 1:1-9` |
| Curated: Bright Saturday | Gospel | Matt 28:1-20 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_58f31273e478759fa7af` | `out/data/pascha_day_hour_index.csv:row 162; source_ref=Ps 3:5,3; Ps 82:8; Matt 28:1-20` |
| Curated: Bright Saturday | Pauline | 1Cor 15:1-22 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_510ef64cea70eb604bf0` | `out/data/pascha_day_hour_index.csv:row 159; source_ref=1Cor 15:1-22` |
| Curated: Bright Saturday | Psalm | Ps 3:3,3:5 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_6c9303917ae652573ee4` | `out/data/pascha_day_hour_index.csv:row 162; source_ref=Ps 3:5,3; Ps 82:8; Matt 28:1-20` |
| Curated: Bright Saturday | Psalm | Ps 82:8 | `current_working_source_not_coptic_reader_checked` | `current_working_source_not_coptic_reader_checked` | `rid_c6e5abb3b44d8783f05f` | `out/data/pascha_day_hour_index.csv:row 162; source_ref=Ps 3:5,3; Ps 82:8; Matt 28:1-20` |

## Existing qualified Pascha and Bright Saturday boundaries, unchanged

The following 67 retained rows complete the explicit Pascha-family and Bright Saturday inventory. They include four Bright Saturday Psalm-alignment holds. They are not members of H8's 247 working rows. Their pre-existing qualifications and statuses are unchanged; no new approval is implied.

### 3RD HOUR:

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| Gospel | Matt 16:24-28 | `current_public_or_local_reference` | `rid_ccab95826fc87dbb6a67` | `out/data/bright_saturday_service_order.csv:row 30; source_ref=Ps. 16:10-11 + Matt. 16:24-28` |
| Prophecy | Jer 13:15-22 | `current_public_or_local_reference` | `rid_b5805b639a39b0478c1e` | `out/data/bright_saturday_service_order.csv:row 29; source_ref=Jeremiah 13:15-22` |
| Psalm | Ps 16:10-11 | `current_public_or_local_reference` | `rid_ebbb9e1ddb4ef2bd2604` | `out/data/bright_saturday_service_order.csv:row 30; source_ref=Ps. 16:10-11 + Matt. 16:24-28` |

### 6TH HOUR:

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| Gospel | Matt 5:3-12 | `current_public_or_local_reference` | `rid_909168ec2eff9427953a` | `out/data/bright_saturday_service_order.csv:row 32; source_ref=Ps. 130:1; 142:7 + Matt. 5:3-12` |
| Prophecy | Isa 50:10-51:8 | `current_public_or_local_reference` | `rid_71b3fe84003b92418b6f` | `out/data/bright_saturday_service_order.csv:row 31; source_ref=Isaiah 50:10–51:8` |
| Psalm | Ps 130:1 | `current_public_or_local_reference` | `rid_d67eb5775ad58c8d3a10` | `out/data/bright_saturday_service_order.csv:row 32; source_ref=Ps. 130:1; 142:7 + Matt. 5:3-12` |
| Psalm | Ps 142:7 | `historical_candidate_removed` | `rid_f8f64afe999bed4ad0e1` | `out/data/bright_saturday_service_order.csv:row 32; source_ref=Ps. 130:1; 142:7 + Matt. 5:3-12` |

### 9TH HOUR:

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| Gospel | Jn 5:21-30 | `current_public_or_local_reference` | `rid_de26b8575994a6fd759d` | `out/data/bright_saturday_service_order.csv:row 35; source_ref=Ps. 41:10, 5 + John 5:21-30` |
| Prophecy | Jer 31:31-34 | `current_public_or_local_reference` | `rid_927f8866ee2b958ca552` | `out/data/bright_saturday_service_order.csv:row 34; source_ref=Jeremiah 31:31-34` |
| Prophecy | Isa 45:15-20 | `current_public_or_local_reference` | `rid_f9c44ef673989a2ef9c9` | `out/data/bright_saturday_service_order.csv:row 33; source_ref=Isaiah 45:15-20` |
| Psalm | Ps 41:5,41:10 | `current_public_or_local_reference` | `rid_fa44089aa2993cc17312` | `out/data/bright_saturday_service_order.csv:row 35; source_ref=Ps. 41:10, 5 + John 5:21-30` |

### Bright Saturday:

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| Psalm | Ps 142:7 (Reader selection; canonical coordinates held) | `pending_psalm_equivalence_unresolved` | `rid_969f73205a3c4d8ceef6` | `sources/coptic-reader/bright-composites-qualified-2026-10-25/saturday--third-and-sixth-hours.txt:lines 337-367; sha256=36637b897d93e0405d35dec4e92430935f60262aad955560ca85681b13840b01; body_sha256=404ae914192e80f560315c52af1175152aa6d6c9df941b088cbdbf320174a1af; printed_ref=Psalm 130:1; 142:7; selection=Ps 142:7; canonical coordinates held` |
| Psalm | Ps 82:8 (Reader selection; canonical coordinates held) | `pending_psalm_equivalence_unresolved` | `rid_5be18395526b0ff8b009` | `sources/coptic-reader/bright-composites-qualified-2026-10-25/saturday--liturgy-of-the-word.txt:lines 433-459; sha256=78570c0a89319493c6a1bade8fd41fbe64cf3c80b145deaf817ab8156b80df8f; body_sha256=dce26d29933c0d1204d3e1d848f6ad8e2ba3c40d0cb299bf2f411a776a2d99fb; printed_ref=Psalms 82:8; selection=Ps 82:8; canonical coordinates held` |
| Psalm | Ps 126:2-3 (Reader selection; canonical coordinates held) | `pending_psalm_equivalence_unresolved` | `rid_16e3ff8ccefe525d98e0` | `sources/coptic-reader/bright-composites-qualified-2026-10-25/saturday--matins.txt:lines 1664-1694; sha256=eb373a8c80ae9fcb658c1726c38a1815281a078217a5d61e1bb305b08cedbb7f; body_sha256=286e7fce1895477d8f3b21db1fad6db1f294fc67e943f130ed3b4fbc75535a45; printed_ref=Psalm 88:4-5; 44:23,26; 126:2-3; selection=Ps 126:2-3; canonical coordinates held` |
| Psalm | Ps 44:23,44:26 (Reader selection; canonical coordinates held) | `pending_psalm_equivalence_unresolved` | `rid_d58dc513121900158fc9` | `sources/coptic-reader/bright-composites-qualified-2026-10-25/saturday--matins.txt:lines 1664-1694; sha256=eb373a8c80ae9fcb658c1726c38a1815281a078217a5d61e1bb305b08cedbb7f; body_sha256=286e7fce1895477d8f3b21db1fad6db1f294fc67e943f130ed3b4fbc75535a45; printed_ref=Psalm 88:4-5; 44:23,26; 126:2-3; selection=Ps 44:23,44:26; canonical coordinates held` |
| Psalm151 | Ps 151 (Reader Psalmody; LXX/source chapter only) | `current_confirmed_coptic_reader` | `rid_803a7b6de46806e9e2d7` | `sources/coptic-reader/psalmody-qualified-2026-10-25/bright-saturday-midnight-praises.full.txt:lines 5-43; sha256=3c858d0729c37fc420e08fb362967edf59d4316855d92840b9f4b4be4ede2d45` |

### Great Thursday: Liturgy of Blessing of the Water

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| Gospel | Jn 13:1-17 | `current_public_or_local_reference` | `rid_0835e229a159266e1b48` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 734-789; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=781f4e0f1554aef4a7fe2e8ccfcabc02b4045ea0be61eaf934946cbd8fe97b66; printed_ref=John 13:1-17; selected=2026-04-09` |
| OT1 | Gen 18:1-23 | `current_public_or_local_reference` | `rid_8d1cd43d499e5e040ff1` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 280-316; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=429f1f6ba78880c1e5a515d67924845ed79dd4d512db1dda21d3643b634a4a1d; printed_ref=Genesis 18:1-23; selected=2026-04-09` |
| OT2 | Prov 9:1-11 | `current_public_or_local_reference` | `rid_f5bab1a621383392ade1` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 317-348; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=c5325428c04ae090d9d4b4d18f21f6722313a26666db681f994de23f242796ed; printed_ref=Proverbs 9:1-11; selected=2026-04-09` |
| OT3 | Exodus from 14, 15 (source-qualified named excerpt) | `current_public_or_local_reference` | `rid_982eff0981aac9ba60ec` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 349-363; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=82521a22743887ee4e41815440c6a333d164d031afb62300ec62310f051a7892; printed_ref=Exodus from 14, 15; selected=2026-04-09` |
| OT4 | Joshua from 1, 3 (source-qualified named excerpt) | `current_public_or_local_reference` | `rid_a74cbb9bd6b59c314222` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 364-374; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=73693e8e6e897ba051059fafade51dfcc1b40485eb5e17ac3b39d38c72ecafa8; printed_ref=Joshua from 1, 3; selected=2026-04-09` |
| OT5 | Isa 4:2-4 | `current_public_or_local_reference` | `rid_f3a1ac3a67cfbdaf1456` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 375-389; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=69aaf8ddefbe386c0738a22c948ddf590b8d14d2ba68f08fd16b6036ef82aefc; printed_ref=Isaiah 4:2-4; selected=2026-04-09` |
| OT6 | Isa 55:1-56:1 | `current_public_or_local_reference` | `rid_2159320effb3da6bddcb` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 390-422; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=4f9641a630b9ddc0ca87155932d439e5ff341f685bc777eb73bcdbd486c4318f; printed_ref=Isaiah 55:1-56:1; selected=2026-04-09` |
| OT7 | Ezek 36:25-29 | `current_public_or_local_reference` | `rid_c685890b74f9cd39b3d5` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 423-439; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=52188b77aef90c3f7435fcb5bdf8f89bca29781a134c44c58f3251b4667aca20; printed_ref=Ezekiel 36:25-29; selected=2026-04-09` |
| OT8 | Ezek 47:1-9 | `current_public_or_local_reference` | `rid_1f622641fffc8ac04b85` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 440-468; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=0bbd4bd6fcbb3c10442873a942345ef8d154ddf3252273c5f1af4dc27520d9dd; printed_ref=Ezekiel 47:1-9; selected=2026-04-09` |
| Pauline | 1Tim 4:9-5:10 | `current_public_or_local_reference` | `rid_5cd67675f32c75db9167` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 513-574; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=0f17366d5f7eb69f926b9a95afbe9906d9382087cd663ebab844702ffa15a8fd; printed_ref=1 Timothy 4:9-5:10; selected=2026-04-09` |
| Psalm | Ps 51:10 | `current_public_or_local_reference` | `rid_4e94fbdc2a3d936100b7` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 704-717; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=53a573eb2de7ed16d48222caf0e1d48c874512d4724f4593bcd604dc1a23763b; printed_ref=Psalms 51:7, 10; selected=2026-04-09` |
| Psalm | Ps 51:7 | `current_public_or_local_reference` | `rid_c07ee2db248f57c9c5d8` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 704-717; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=53a573eb2de7ed16d48222caf0e1d48c874512d4724f4593bcd604dc1a23763b; printed_ref=Psalms 51:7, 10; selected=2026-04-09` |

### Hosanna Sunday: Ninth Hour

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| OT1 | Lam 1:1-4 | `current_confirmed_coptic_reader` | `rid_6f2b1cdfaffff2641d58` | `https://copticreader.org/app/; sources/coptic-reader/pascha-resolution-qualified-2026-10-25/hosanna-sunday/Sunday--Sunday_Day--9th_Hour.txt:row hosanna-sunday-day-ninth-hour-lam-1; source_ref=Lamentations 1:1-4; sources/coptic-reader/pascha-resolution-qualified-2026-10-25/hosanna-sunday/Sunday--Sunday_Day--9th_Hour.txt:lines 12-46,47-105; sha256=ea7e186ff09fe3ab46ee4dc16aa7ba6e4a740060d714bec78aaf30ea49bebd74` |

### MATINS / RAISING OF INCENSE:

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| Gospel | Matt 27:62-66 | `current_public_or_local_reference` | `rid_cfbba3cbfe82f0f857a7` | `out/data/bright_saturday_service_order.csv:row 28; source_ref=Ps. 88:4-5; 44:23-26; 126:2-3 + Matt. 27:62-66` |
| Pauline Epistle | Eph 4:1-5 | `current_public_or_local_reference` | `rid_0341c4e20a37f1b4cc0e` | `out/data/bright_saturday_service_order.csv:row 27; source_ref=Ephesians 4:1-5` |
| Prophecy of Isaiah | Isa 55:2-13 | `current_public_or_local_reference` | `rid_908610343ba98cc31797` | `out/data/bright_saturday_service_order.csv:row 26; source_ref=Isaiah 55:2-13` |
| Psalm | Ps 126:2-3 | `historical_candidate_removed` | `rid_01f32bd787164f059e93` | `out/data/bright_saturday_service_order.csv:row 28; source_ref=Ps. 88:4-5; 44:23-26; 126:2-3 + Matt. 27:62-66` |
| Psalm | Ps 88:4-5 | `current_public_or_local_reference` | `rid_44f70dae19d3d56f3d30` | `out/data/bright_saturday_service_order.csv:row 28; source_ref=Ps. 88:4-5; 44:23-26; 126:2-3 + Matt. 27:62-66` |
| Psalm | Ps 44:23-26 | `historical_candidate_removed` | `rid_cf1a402c8a2d11ef55de` | `out/data/bright_saturday_service_order.csv:row 28; source_ref=Ps. 88:4-5; 44:23-26; 126:2-3 + Matt. 27:62-66` |

### PRAISES OF THE PROPHETS:

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| First Prayer of Isaiah | Isa 26:9-20 | `current_public_or_local_reference` | `rid_e013d16647a0acb4732f` | `out/data/bright_saturday_service_order.csv:row 10; source_ref=Isaiah 26:9-20` |
| Praise of the Prophet Jeremiah | Lam 5:16-22 | `current_public_or_local_reference` | `rid_365eb7845f47e990c4c9` | `out/data/bright_saturday_service_order.csv:row 13; source_ref=Lamentations 5:16-22` |
| Praise of the Virgin Mary | Lk 1:46-55 | `current_public_or_local_reference` | `rid_aa8b1eaebc51c5cf573a` | `out/data/bright_saturday_service_order.csv:row 22; source_ref=Luke 1:46-55` |
| Prayer of Azariah (Part 1) | Dan 3:25-51 | `current_public_or_local_reference` | `rid_990f4c692fe3f22a1d39` | `out/data/bright_saturday_service_order.csv:row 20; source_ref=Daniel 3:25-51` |
| Prayer of Azariah (Part 2) | Dan 3:91-97 | `current_public_or_local_reference` | `rid_db388feca4ae08da77fb` | `out/data/bright_saturday_service_order.csv:row 21; source_ref=Daniel 3:91-97` |
| Prayer of Baruch | Bar 2:11-16 | `current_public_or_local_reference` | `rid_e0586304d8ad566c6c0a` | `out/data/bright_saturday_service_order.csv:row 14; source_ref=Baruch 2:11-16` |
| Prayer of Daniel | Dan 9:4-19 | `current_public_or_local_reference` | `rid_c5b80ec460797376e7e0` | `out/data/bright_saturday_service_order.csv:row 18; source_ref=Daniel 9:4-19` |
| Prayer of David | 1Chr 29:10-13 | `current_public_or_local_reference` | `rid_c31cd01a2624fa13620d` | `out/data/bright_saturday_service_order.csv:row 16; source_ref=1 Chronicles 29:10-13` |
| Prayer of Elijah | 1Kgs 18:36-39 | `current_public_or_local_reference` | `rid_00a7e0b4cb4de20cd357` | `out/data/bright_saturday_service_order.csv:row 15; source_ref=1 Kings 18:36-39` |
| Prayer of Habakkuk | Hab 3:2-19 | `current_public_or_local_reference` | `rid_ae935a5d9cc3c760e89a` | `out/data/bright_saturday_service_order.csv:row 6; source_ref=Habakkuk 3:2-19` |
| Prayer of Hannah | 1Sam 2:1-11 | `current_public_or_local_reference` | `rid_a70ed0e29b6ef0a8836b` | `out/data/bright_saturday_service_order.csv:row 5; source_ref=1 Samuel 2:1-11` |
| Prayer of Hezekiah | Isa 38:10-20 | `current_public_or_local_reference` | `rid_796d3974d64c02889ca1` | `out/data/bright_saturday_service_order.csv:row 8; source_ref=Isaiah 38:10-20` |
| Prayer of Jonah | Jonah 2:2-10 | `current_public_or_local_reference` | `rid_9914d4c45c6fa8e141cc` | `out/data/bright_saturday_service_order.csv:row 7; source_ref=Jonah 2:2-10` |
| Prayer of King Manasseh | PrMan 1:1-15 | `current_public_or_local_reference` | `rid_acf0a949bfcf5ac2b8de` | `out/data/bright_saturday_service_order.csv:row 9; source_ref=Prayer of Manasseh 1:1-15` |
| Prayer of Simeon the Elder | Lk 2:29-32 | `current_public_or_local_reference` | `rid_5d2fe211f1b9d8ed7107` | `out/data/bright_saturday_service_order.csv:row 24; source_ref=Luke 2:29-32` |
| Prayer of Solomon | 1Kgs 8:22-30 | `current_public_or_local_reference` | `rid_7f3d14172f64dd5abb0c` | `out/data/bright_saturday_service_order.csv:row 17; source_ref=1 Kings 8:22-30` |
| Prayer of Zacharias the Priest | Lk 1:68-79 | `current_public_or_local_reference` | `rid_e4859f1ca244e7ed7bfb` | `out/data/bright_saturday_service_order.csv:row 23; source_ref=Luke 1:68-79` |
| Second Praise of Moses | Deut 32:1-42 | `current_public_or_local_reference` | `rid_8ae616e6b96572e37bd9` | `out/data/bright_saturday_service_order.csv:row 4; source_ref=Deuteronomy 32:1-42` |
| Second Prayer of Isaiah | Isa 25:1-12 | `current_public_or_local_reference` | `rid_8e142dce9dfba9abf968` | `out/data/bright_saturday_service_order.csv:row 11; source_ref=Isaiah 25:1-12` |
| Story of Susannah and Daniel the Prophet | Sus 1:1-64 | `current_public_or_local_reference` | `rid_f03236b560295567779e` | `out/data/bright_saturday_service_order.csv:row 25; source_ref=Susanna 1:1-64` |
| Third Prayer of Isaiah | Isa 26:1-9 | `current_public_or_local_reference` | `rid_bb48bc796b8760df10fa` | `out/data/bright_saturday_service_order.csv:row 12; source_ref=Isaiah 26:1-9` |
| Vision of Daniel – Three Youth in the Fiery Furnace | Dan 3:1-23 | `current_public_or_local_reference` | `rid_48ef963652e2632b596b` | `out/data/bright_saturday_service_order.csv:row 19; source_ref=Daniel 3:1-23` |

### ST. BASIL LITURGY – LITURGY OF THE WORD:

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| Catholic Epistle | 1Pet 1:1-9 | `current_public_or_local_reference` | `rid_be832a860aaa1ccbd7b0` | `out/data/bright_saturday_service_order.csv:row 37; source_ref=1 Peter 1:1-9` |
| Gospel | Matt 28:1-20 | `current_public_or_local_reference` | `rid_58f31273e478759fa7af` | `out/data/bright_saturday_service_order.csv:row 39; source_ref=Ps. 3:5, 3; 82:8 + Matt. 28:1-20` |
| Pauline Epistle | 1Cor 15:1-22 | `current_public_or_local_reference` | `rid_510ef64cea70eb604bf0` | `out/data/bright_saturday_service_order.csv:row 36; source_ref=1 Corinthians 15:1-22` |
| Praxis | Acts 3:12-21 | `current_public_or_local_reference` | `rid_5312571ad2ea75579e4e` | `out/data/bright_saturday_service_order.csv:row 38; source_ref=Acts 3:12-21` |
| Psalm | Ps 3:3,3:5 | `current_public_or_local_reference` | `rid_6c9303917ae652573ee4` | `out/data/bright_saturday_service_order.csv:row 39; source_ref=Ps. 3:5, 3; 82:8 + Matt. 28:1-20` |
| Psalm | Ps 82:8 | `historical_candidate_removed` | `rid_c6e5abb3b44d8783f05f` | `out/data/bright_saturday_service_order.csv:row 39; source_ref=Ps. 3:5, 3; 82:8 + Matt. 28:1-20` |

### the Covenant Thursday: Liturgy

| Slot | Reference | Status | Identity | Source locator |
|---|---|---|---|---|
| Gospel | Matt 26:20-29 | `current_public_or_local_reference` | `rid_d4896e0e8c34cd17fa1c` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-word.txt:lines 239-273; sha256=a856ec50d967e00a99d49d702a55ecf451a43d6e47f68f3f63d360600eff31cd; body_sha256=ed443749fb02e2ca40172203e17523dbcf33577512830583f56e0cbf81ef6b60; printed_ref=Matthew 26:20-29; selected=2026-04-09` |
| Pauline | 1Cor 11:23-34 | `current_public_or_local_reference` | `rid_050475f781f932c674c6` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-word.txt:lines 29-72; sha256=a856ec50d967e00a99d49d702a55ecf451a43d6e47f68f3f63d360600eff31cd; body_sha256=601adc2003e7cf77d35ffb32822fe741c19f3e61a230e04e50750b4fc17f1979; printed_ref=1 Corinthians 11:23-34; selected=2026-04-09` |
| Psalm | Ps 23:5 | `current_public_or_local_reference` | `rid_1104fd6177fc11b72194` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-word.txt:lines 209-222; sha256=a856ec50d967e00a99d49d702a55ecf451a43d6e47f68f3f63d360600eff31cd; body_sha256=5323863a0c3f0893e5050ec0512cbff11ba678f0b72ec9d259895e0e5898a935; printed_ref=Psalms 22:5;40:9; selected=2026-04-09` |
| Psalm | Ps 41:9 | `current_public_or_local_reference` | `rid_c60390570a2dbfe58f13` | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-word.txt:lines 209-222; sha256=a856ec50d967e00a99d49d702a55ecf451a43d6e47f68f3f63d360600eff31cd; body_sha256=5323863a0c3f0893e5050ec0512cbff11ba678f0b72ec9d259895e0e5898a935; printed_ref=Psalms 22:5;40:9; selected=2026-04-09` |
