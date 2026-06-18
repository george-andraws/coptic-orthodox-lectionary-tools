# Problem 4 Pascha Prophecy Ordering Audit

Wednesday day rows are checked against the Section 7.1 Coptic Reader fixture. Other Pascha rows are checked against the source pipeline's curated/API day-hour list. Where a kept St. Mary source-text row overlaps a curated/API reading, its `slot_order` is now inherited from that source reading order; otherwise it keeps St. Mary source-text order and is listed as open against API confirmation.

## Summary

- confirmed: 143
- open_no_source_match: 3
- removed_not_in_fixture: 10
- source_text_only_open: 44
- open_items: 47
- mismatches_after_fix: 0

## Good Friday — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Jer 12:1-14 | 1 | confirmed | api |
| 1 | Prophecy | Exod 12:1-14 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 2 | OT2 | Isa 3:5-12 | 2 | confirmed | api |
| 2 | Prophecy | Lev 23:5-12 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Good Friday — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Deut 8:19-9:24 | 1 | confirmed | api |
| 2 | OT2 | Isa 1:2-9 | 2 | confirmed | api |
| 3 | OT3 | Isa 2:10-21 | 3 | confirmed | api |
| 4 | OT4 | Jer 22:29-23:6 | 4 | confirmed | api |
| 5 | OT5 | Isa 24:1-13 | 5 | confirmed | api |
| 6 | OT6 | Wis 2:12-22 | 6 | confirmed | api |
| 7 | OT7 | Job 12:18-13:1 | 7 | confirmed | api |
| 7 | Prophecy | Job 12:17-13:1 | 7 | confirmed | api |
| 8 | OT8 | Zech 11:11-14 | 8 | confirmed | api |
| 8 | Prophecy | Zech 11:14 | 8 | confirmed | api |
| 9 | OT9 | Mic 1:16-2:3 | 9 | confirmed | api |
| 10 | OT10 | Mic 7:1-8 | 10 | confirmed | api |

## Good Friday — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Jer 11:18-12:13 | 1 | confirmed | api |
| 2 | OT2 | Zech 14:5-11 | 2 | confirmed | api |
| 2 | Prophecy | Zech 14:6-11 | 2 | confirmed | api |
| 3 | OT3 | Hos 2:1-3,2:10-11 | 3 | confirmed | api |
| 3 | Prophecy | Joel 2:1-3,2:10-11 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Good Friday — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Num 21:1-9 | 1 | confirmed | api |
| 2 | OT2 | Isa 53:7-12 | 2 | confirmed | api |
| 3 | OT3 | Isa 12:2-13:10 | 3 | confirmed | api |
| 4 | OT4 | Amos 8:9-12 | 4 | confirmed | api |

## Good Friday — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Gen 48:1-19 | 1 | confirmed | api |
| 2 | OT2 | Isa 50:4-9 | 2 | confirmed | api |
| 3 | OT3 | Isa 3:9-15 | 3 | confirmed | api |
| 4 | OT4 | Isa 63:1-7 | 4 | confirmed | api |
| 5 | OT5 | Amos 9:4-6 | 5 | confirmed | api |
| 5 | OT5 | Amos 9:8-10 | 5 | confirmed | api |
| 5 | Prophecy | Amos 9:4-5,9:7-10 | 5 | confirmed | api |
| 6 | OT6 | Job 29:21-30:10 | 6 | confirmed | api |
| 6 | Prophecy | Job 29:21-25,30:1-10 | 6 | confirmed | api |

## Good Friday — Twelfth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Lam 3:1-66 | 1 | confirmed | api |
| 2 | OT2 | Jonah 1:10-2:8 | 2 | confirmed | api |
| 2 | Prophecy | Jonah 1:10-2:7 | 2 | confirmed | api |

## Good Friday Eve — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | Prophecy | Ezek 21:28-32 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Great Thursday — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Isa 52:13-53:12 | 1 | confirmed | api |
| 2 | OT2 | Isa 19:19-25 | 2 | confirmed | api |
| 3 | OT3 | Zech 12:11-14 | 3 | confirmed | api |
| 3 | OT3 | Zech 13:1-9 | 3 | confirmed | api |
| 3 | OT3 | Zech 14:1-4 | 3 | confirmed | api |
| 3 | OT3 | Zech 14:6-9 | 3 | confirmed | api |
| 3 | Prophecy | Zech 12:11-14:3,14:6-9 | 3 | confirmed | api |

## Great Thursday — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Exod 17:8-16 | 1 | confirmed | api |
| 2 | OT2 | Exod 15:22-16:3 | 2 | confirmed | api |
| 2 | Prophecy | Exod 15:23-16:3 | 2 | confirmed | api |
| 3 | OT3 | Isa 58:1-9 | 3 | confirmed | api |
| 3 | Prophecy | Isa 58:1-11 | 3 | confirmed | api |
| 4 | OT4 | Ezek 18:20-32 | 4 | confirmed | api |

## Great Thursday — Liturgy of Blessing of the Water

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Gen 18:1-23 | 1 | confirmed | St Mary Ottawa Holy Pascha PDF cross-check 2026-06-06 |
| 2 | Prophecy | Prov 9:1-11 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 3 | Prophecy | Isa 4:2-4 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 4 | Prophecy | Isa 55:1-56:1 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 5 | Prophecy | Ezek 36:25-29 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 6 | Prophecy | Ezek 47:1-9 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Great Thursday — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Gen 22:1-19 | 1 | confirmed | api |
| 2 | OT2 | Isa 61:1-7 | 2 | confirmed | api |
| 2 | Prophecy | Isa 61:1-6 | 2 | confirmed | api |
| 3 | OT3 | Gen 14:17-20 | 3 | confirmed | api |
| 4 | OT4 | Job 27:2-28:13 | 4 | confirmed | api |

## Great Thursday — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Exod 7:2-15 | 1 | confirmed | api |
| 1 | Prophecy | Jer 7:2-15 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 2 | OT2 | Ezek 20:39-44 | 2 | confirmed | api |
| 3 | OT3 | Wis 12:13-13:1 | 3 | confirmed | api |
| 3 | Prophecy | Sir 23:7-14 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Great Thursday — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Exod 32:30-33:5 | 1 | confirmed | api |
| 2 | OT2 | Sir 24:1-11 |  | open_no_source_match | No fixture/API/curated source match found by exact or overlap comparison |
| 3 | OT3 | Zech 10:1-2 | 3 | confirmed | api |
| 3 | OT3 | Zech 9:11-14 | 3 | confirmed | api |
| 4 | OT4 | Prov 4:4-27,5:1-4 | 4 | confirmed | api |
| 4 | Prophecy | Prov 30:2-6 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Great Thursday Eve — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Isa 27:11-28:15 | 1 | confirmed | api |
| 1 | Prophecy | Jer 8:4-9 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Great Thursday Eve — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Jer 8:17-9:6 | 1 | confirmed | api |
| 1 | Prophecy | Ezek 43:5-11 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Great Thursday Eve — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Jer 9:6-10 | 1 | confirmed | api |
| 1 | Prophecy | Ezek 20:27-33 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 1 | Prophecy | Jer 9:7-11 | 1 | confirmed | api |
| 2 | OT2 | Ezek 21:33-37 | 2 | confirmed | api |

## Great Thursday Eve — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Ezek 22:23-28 | 1 | confirmed | api |
| 1 | Prophecy | Amos 3:1-11 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Great Thursday Eve — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Ezek 36:16-23 | 1 | confirmed | api |
| 1 | Prophecy | Amos 4:4-13 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Hosanna Sunday — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | Prophecy | Isa 48:12-22 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 2 | Prophecy | Nah 1:2-8 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Hosanna Sunday — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | Prophecy | Lam 1:1-4 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 2 | Prophecy | Zeph 3:11-20 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Monday — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Isa 50:1-3 | 1 | confirmed | api |
| 2 | OT2 | Wis 2:20-30 | 2 | confirmed | api |
| 2 | Prophecy | Sir 1:18-27 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Monday — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Gen 1:1-2:3 | 1 | confirmed | api |
| 1 | OT1 | Gen 1:1-31 | 1 | confirmed | api |
| 1 | OT1 | Gen 2:1-3 | 1 | confirmed | api |
| 2 | OT2 | Isa 5:1-9 | 2 | confirmed | api |
| 3 | OT3 | Ps 72:1-19 (LXX Ps 71:1-19) | 3 | confirmed | api |
| 3 | Prophecy | Sir 1:1-14 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Monday — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Gen 2:15-25 | 1 | confirmed | api |
| 1 | OT1 | Gen 2:15-3:24 | 1 | confirmed | api |
| 1 | OT1 | Gen 3:1-24 | 1 | confirmed | api |
| 2 | OT2 | Isa 40:1-5 | 2 | confirmed | api |
| 3 | OT3 | Prov 1:1-9 | 3 | confirmed | api |

## Monday — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Exod 32:7-15 | 1 | confirmed | api |
| 2 | OT2 | Wis 1:1-9 | 2 | confirmed | api+St Mary Ottawa Holy Pascha source-text correction 2026-06-06 |

## Monday — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Isa 5:20-30 | 1 | confirmed | api |
| 2 | OT2 | Jer 9:12-19 | 2 | confirmed | api |

## Monday Eve — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Amos 5:6-14 | 1 | confirmed | api |
| 1 | Prophecy | Mic 3:1-4 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Monday Eve — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Zech 1:1-6 | 1 | confirmed | api |
| 1 | Prophecy | Zeph 1:2-12 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Monday Eve — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Hos 10:12-15 | 1 | confirmed | api |
| 1 | OT1 | Hos 11:1-2 | 1 | confirmed | api |
| 1 | Prophecy | Mic 2:3-10 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Monday Eve — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Hos 4:15-19 | 1 | confirmed | api |
| 1 | OT1 | Hos 5:1-7 | 1 | confirmed | api |
| 1 | Prophecy | Joel 1:5-15 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Monday Eve — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Mal 1:1-9 | 1 | confirmed | api |
| 1 | Prophecy | Zeph 1:14-2:2 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Thursday — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | Prophecy | Gen 22:1-19 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Tuesday — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Isa 50:1-3 | 1 | confirmed | api |
| 1 | Prophecy | Isa 30:25-30 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 2 | OT2 | Wis 2:20-30 | 2 | confirmed | api |
| 2 | Prophecy | Prov 6:20-7:4 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Tuesday — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Exod 19:1-9 | 1 | confirmed | api |
| 2 | OT2 | Job 23:2-17 | 2 | confirmed | api |
| 2 | OT2 | Job 23:2-24:25 | 2 | confirmed | api |
| 2 | OT2 | Job 24:1-25 | 2 | confirmed | api |
| 3 | OT3 | Hos 4:1-8 | 3 | confirmed | api |

## Tuesday — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Gen 6:5-9:7 | 1 | confirmed | api+St Mary Ottawa Holy Pascha PDF cross-check 2026-06-06 |
| 2 | OT2 | Isa 40:1-5 | 2 | confirmed | api |
| 2 | Prophecy | Prov 9:1-11 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 3 | OT3 | Prov 1:1-9 | 3 | confirmed | api |
| 3 | Prophecy | Isa 40:9-31 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 4 | Prophecy | Dan 7:9-15 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 5 | Prophecy | Prov 8:1-12 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Tuesday — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Ezek 21:3-13 | 1 | confirmed | St Mary Ottawa Holy Pascha source-text correction 2026-06-06 |
| 2 | OT2 | Sir 4:20-5:2 | 2 | confirmed | St Mary Ottawa Holy Pascha source-text correction 2026-06-06 |
| 3 | OT3 | Isa 1:1-9 | 3 | confirmed | St Mary Ottawa Holy Pascha source-text correction 2026-06-06 |

## Tuesday — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Isa 5:20-30 | 1 | confirmed | api |
| 1 | Prophecy | Deut 8:11-20 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 2 | OT2 | Jer 9:12-19 | 2 | confirmed | api |
| 2 | Prophecy | Sir 1:1-14 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 3 | Prophecy | Job 27:2-28:2 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 4 | Prophecy | 1Kgs 19:9-14 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Tuesday Eve — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Amos 5:6-14 | 1 | confirmed | api |

## Tuesday Eve — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Zech 1:1-6 | 1 | confirmed | api |

## Tuesday Eve — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Hos 10:12-11:2 | 1 | confirmed | api |
| 1 | OT1 | Hos 10:12-15 | 1 | confirmed | api |
| 1 | OT1 | Hos 11:1-2 | 1 | confirmed | api |

## Tuesday Eve — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Hos 4:15-19 | 1 | confirmed | api |
| 1 | OT1 | Hos 4:15-5:7 | 1 | confirmed | api |
| 1 | OT1 | Hos 5:1-7 | 1 | confirmed | api |

## Tuesday Eve — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Mal 1:1-9 | 1 | confirmed | api |

## Wednesday — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Isa 28:16-29 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |

## Wednesday — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Exod 17:1-7 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 2 | OT2 | Prov 3:5-14 | 2 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | OT3 | Hos 5:13-6:3 | 3 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 4 | OT4 | Wis 1:20-2:15 |  | open_no_source_match | No fixture/API/curated source match found by exact or overlap comparison |
| 5 | OT5 | Wis 3:12-24 |  | open_no_source_match | No fixture/API/curated source match found by exact or overlap comparison |

## Wednesday — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Gen 24:1-9 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 2 | OT2 | Num 20:1-13 | 2 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | OT3 | Prov 1:11-35 | 3 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | Prophecy | Prov 1:10-33 | 3 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 4 | OT4 | Isa 59:1-17 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |
| 5 | OT5 | Zech 11:11-14 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |

## Wednesday — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Exod 14:13-15:1 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 2 | OT2 | Sir 23:7-14 | 2 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | OT3 | Job 27:16-20 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | OT3 | Job 28:1-2 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |

## Wednesday — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Exod 13:17-22 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 2 | OT2 | Sir 22:7-18 | 2 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | OT3 | Prov 4:4-27,5:1-4 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | Prophecy | Job 27:16-28:2 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | Prophecy | Prov 4:4-27,5:1-4 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |

## Wednesday Eve — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Wis 7:24-30 | 1 | confirmed | St Mary Ottawa Holy Pascha source-text correction 2026-06-06 |

## Wednesday Eve — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Jer 43:5-11 | 1 | confirmed | api |
| 1 | Prophecy | Ezek 22:17-22 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |
| 2 | Prophecy | Ezek 22:23-28 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Wednesday Eve — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Ezek 20:27-33 | 1 | confirmed | api |
| 1 | Prophecy | Hos 9:14-10:2 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Wednesday Eve — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Amos 3:1-11 | 1 | confirmed | api |
| 1 | Prophecy | Jer 16:9-13 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Wednesday Eve — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | OT1 | Amos 4:4-13 | 1 | confirmed | api |
| 1 | Prophecy | Amos 5:18-27 |  | source_text_only_open | St. Mary Ottawa Holy Pascha source-text sequence; no curated/API overlap found |

## Wednesday of Holy Pascha — Eleventh Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | prophecy | Isa 28:16-29 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |

## Wednesday of Holy Pascha — First Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | prophecy | Exod 17:1-7 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 2 | prophecy | Prov 3:5-14 | 2 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | prophecy | Hos 5:13-6:3 | 3 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |

## Wednesday of Holy Pascha — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | prophecy | Gen 24:1-9 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 2 | prophecy | Num 20:1-13 | 2 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | prophecy | Prov 1:11-35 | 3 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |

## Wednesday of Holy Pascha — Sixth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | prophecy | Exod 14:13-15:1 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 2 | prophecy | Sir 23:7-14 | 2 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 3 | prophecy | Memoirs of Job | 3 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |

## Wednesday of Holy Pascha — Third Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | prophecy | Exod 13:17-22 | 1 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |
| 2 | prophecy | Sir 22:7-18 | 2 | confirmed | Section 7.1 Coptic Reader Wednesday fixture |

## Wednesday | Ninth Hour — Ninth Hour

| order | slot | ref | expected | verdict | source |
|---:|---|---|---:|---|---|
| 1 | Prophecy | Isa 48:1-6 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |
| 8 | Prophecy | Isa 59:1-17 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |
| 9 | Prophecy | Zech 11:11-14 |  | removed_not_in_fixture | Section 7.1 Coptic Reader Wednesday fixture |

## Open items

- Good Friday Eleventh Hour `Prophecy` `Exod 12:1-14` order 1: No curated/API overlap found; order kept from source-text sequence.
- Good Friday Eleventh Hour `Prophecy` `Lev 23:5-12` order 2: No curated/API overlap found; order kept from source-text sequence.
- Good Friday Ninth Hour `Prophecy` `Joel 2:1-3,2:10-11` order 3: No curated/API overlap found; order kept from source-text sequence.
- Good Friday Eve Ninth Hour `Prophecy` `Ezek 21:28-32` order 1: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Liturgy of Blessing of the Water `Prophecy` `Prov 9:1-11` order 2: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Liturgy of Blessing of the Water `Prophecy` `Isa 4:2-4` order 3: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Liturgy of Blessing of the Water `Prophecy` `Isa 55:1-56:1` order 4: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Liturgy of Blessing of the Water `Prophecy` `Ezek 36:25-29` order 5: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Liturgy of Blessing of the Water `Prophecy` `Ezek 47:1-9` order 6: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Sixth Hour `Prophecy` `Jer 7:2-15` order 1: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Sixth Hour `Prophecy` `Sir 23:7-14` order 3: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Third Hour `OT2` `Sir 24:1-11` order 2: No fixture/API/curated source match found by exact or overlap comparison.
- Great Thursday Third Hour `Prophecy` `Prov 30:2-6` order 4: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Eve Eleventh Hour `Prophecy` `Jer 8:4-9` order 1: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Eve First Hour `Prophecy` `Ezek 43:5-11` order 1: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Eve Ninth Hour `Prophecy` `Ezek 20:27-33` order 1: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Eve Sixth Hour `Prophecy` `Amos 3:1-11` order 1: No curated/API overlap found; order kept from source-text sequence.
- Great Thursday Eve Third Hour `Prophecy` `Amos 4:4-13` order 1: No curated/API overlap found; order kept from source-text sequence.
- Hosanna Sunday Eleventh Hour `Prophecy` `Isa 48:12-22` order 1: No curated/API overlap found; order kept from source-text sequence.
- Hosanna Sunday Eleventh Hour `Prophecy` `Nah 1:2-8` order 2: No curated/API overlap found; order kept from source-text sequence.
- Hosanna Sunday Ninth Hour `Prophecy` `Lam 1:1-4` order 1: No curated/API overlap found; order kept from source-text sequence.
- Hosanna Sunday Ninth Hour `Prophecy` `Zeph 3:11-20` order 2: No curated/API overlap found; order kept from source-text sequence.
- Monday Eleventh Hour `Prophecy` `Sir 1:18-27` order 2: No curated/API overlap found; order kept from source-text sequence.
- Monday First Hour `Prophecy` `Sir 1:1-14` order 3: No curated/API overlap found; order kept from source-text sequence.
- Monday Eve Eleventh Hour `Prophecy` `Mic 3:1-4` order 1: No curated/API overlap found; order kept from source-text sequence.
- Monday Eve First Hour `Prophecy` `Zeph 1:2-12` order 1: No curated/API overlap found; order kept from source-text sequence.
- Monday Eve Ninth Hour `Prophecy` `Mic 2:3-10` order 1: No curated/API overlap found; order kept from source-text sequence.
- Monday Eve Sixth Hour `Prophecy` `Joel 1:5-15` order 1: No curated/API overlap found; order kept from source-text sequence.
- Monday Eve Third Hour `Prophecy` `Zeph 1:14-2:2` order 1: No curated/API overlap found; order kept from source-text sequence.
- Thursday Ninth Hour `Prophecy` `Gen 22:1-19` order 1: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Eleventh Hour `Prophecy` `Isa 30:25-30` order 1: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Eleventh Hour `Prophecy` `Prov 6:20-7:4` order 2: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Ninth Hour `Prophecy` `Prov 9:1-11` order 2: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Ninth Hour `Prophecy` `Isa 40:9-31` order 3: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Ninth Hour `Prophecy` `Dan 7:9-15` order 4: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Ninth Hour `Prophecy` `Prov 8:1-12` order 5: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Third Hour `Prophecy` `Deut 8:11-20` order 1: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Third Hour `Prophecy` `Sir 1:1-14` order 2: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Third Hour `Prophecy` `Job 27:2-28:2` order 3: No curated/API overlap found; order kept from source-text sequence.
- Tuesday Third Hour `Prophecy` `1Kgs 19:9-14` order 4: No curated/API overlap found; order kept from source-text sequence.
- Wednesday First Hour `OT4` `Wis 1:20-2:15` order 4: No fixture/API/curated source match found by exact or overlap comparison.
- Wednesday First Hour `OT5` `Wis 3:12-24` order 5: No fixture/API/curated source match found by exact or overlap comparison.
- Wednesday Eve First Hour `Prophecy` `Ezek 22:17-22` order 1: No curated/API overlap found; order kept from source-text sequence.
- Wednesday Eve First Hour `Prophecy` `Ezek 22:23-28` order 2: No curated/API overlap found; order kept from source-text sequence.
- Wednesday Eve Ninth Hour `Prophecy` `Hos 9:14-10:2` order 1: No curated/API overlap found; order kept from source-text sequence.
- Wednesday Eve Sixth Hour `Prophecy` `Jer 16:9-13` order 1: No curated/API overlap found; order kept from source-text sequence.
- Wednesday Eve Third Hour `Prophecy` `Amos 5:18-27` order 1: No curated/API overlap found; order kept from source-text sequence.
