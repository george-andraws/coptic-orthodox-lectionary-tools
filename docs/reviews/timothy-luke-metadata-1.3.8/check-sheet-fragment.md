# Timothy and Luke metadata check-sheet fragment

No status promotion, endpoint choice or new Reader verification is recorded.

## T-L7: confirm, no change expected

Exactly seven appointment confirmations, all low priority. Six retain their copticchurch.net locator. The Great Thursday Water Liturgy is already backed by retained Reader source evidence in 1.3.7; the package has no copticchurch.net witness for that service. Its actual locator is retained instead of inventing one.

| Identity | Reading | Occasion and service | Source locator |
|---|---|---|---|
| `rid_1cb21a9e546625f8b503` | 1Tim 1:12-19 | First Sunday of Tout, Liturgy | `https://copticchurch.net/readings?g_year=2022&g_month=09&g_day=18; cache/copticchurch_html:row 10045; source_ref=1Tim 1:12-19` |
| `rid_539d72ebd85c4b03eaf1` | 1Tim 2:1-3:4 | Thursday of the sixth week of Great Lent, Liturgy | `https://copticchurch.net/readings?g_year=2023&g_month=03&g_day=30; cache/copticchurch_html:row 12027; source_ref=1Tim 2:1-3:4` |
| `rid_f7ab1aa9ada78662622d` | 1Tim 3:13-16 | The Feast of the Ascension, Liturgy | `https://copticchurch.net/readings?g_year=2023&g_month=05&g_day=25; cache/copticchurch_html:row 12527; source_ref=1Tim 3:13-16` |
| `rid_5cd67675f32c75db9167` | 1Tim 4:9-5:10 | Great Thursday, Liturgy of Blessing of the Water | `sources/coptic-reader/covenant-thursday-qualified-2026-10-25/thursday--thursday-day--liturgy-of-the-waters.txt:lines 513-574; sha256=a66ddc71a6443580577463041ec55c9a419c23c593c4e652d171b4f9d9279f45; body_sha256=0f17366d5f7eb69f926b9a95afbe9906d9382087cd663ebab844702ffa15a8fd; printed_ref=1 Timothy 4:9-5:10; selected=2026-04-09` |
| `rid_e475dd1bbf8b05b45910` | 1Tim 5:17-6:2 | Hatour 24, Liturgy | `https://copticchurch.net/readings?g_year=2022&g_month=12&g_day=03; cache/copticchurch_html:row 10881; source_ref=1Tim 5:17-6:2` |
| `rid_62f86c38e99a8b80724a` | 1Tim 6:3-16 | Third Sunday of Abib, Liturgy | `https://copticchurch.net/readings?g_year=2023&g_month=07&g_day=23; cache/copticchurch_html:row 13168; source_ref=1Tim 6:3-16` |
| `rid_2ba106e64365ef933085` | 1Tim 6:3-21 | Fourth Sunday of Baba, Liturgy | `https://copticchurch.net/readings?g_year=2022&g_month=11&g_day=06; cache/copticchurch_html:row 10579; source_ref=1Tim 6:3-21` |

## LK1: Abib 26, do not choose

Both three-Gospel sets are flagged. Calendar co-display does not say why a reading was selected for a saint.

| Source family | Raw day wording | Service | Reading | Identity and locator |
|---|---|---|---|---|
| ordinary_date_resolved | Abib 26 | Liturgy | Matt 23:13-26 | `rid_84ed6fb31aac63feec5f`; `https://copticchurch.net/readings?g_year=2023&g_month=08&g_day=02; cache/copticchurch_html:row 13266; source_ref=Matt 23:13-26` |
| ordinary_date_resolved | Abib 26 | Matins | Matt 17:1-9 | `rid_90f9856d0b9722750c38`; `https://copticchurch.net/readings?g_year=2023&g_month=08&g_day=02; cache/copticchurch_html:row 13269; source_ref=Matt 17:1-9` |
| ordinary_date_resolved | Abib 26 | Vespers | Lk 11:37-51 | `rid_875283c8a2bfb534d4ab`; `https://copticchurch.net/readings?g_year=2023&g_month=08&g_day=02; cache/copticchurch_html:row 13273; source_ref=Lk 11:37-51` |
| katameros_cycle | Feast of St. Joseph the Carpenter | liturgy_gospel | Matt 2:13-23 | `rid_9b9fb26c186e72003e9c`; `sources/katameros-api/Core/KatamerosDatabase.db:row 4061; source_ref=Matt 2:13-23` |
| katameros_cycle | Feast of St. Joseph the Carpenter | matins_gospel | Matt 12:15-23 | `rid_37424e94554789b41fc3`; `sources/katameros-api/Core/KatamerosDatabase.db:row 4055; source_ref=Matt 12:15-23` |
| katameros_cycle | Feast of St. Joseph the Carpenter | vespers_gospel | Matt 4:12-17 | `rid_d2857a5170e70b6bb682`; `sources/katameros-api/Core/KatamerosDatabase.db:row 4051; source_ref=Matt 4:12-17` |

## LK4: preserve both printed ranges

Fourth Sunday of Mesra, Vespers: Luke 17:20-36 versus 17:20-37. Tout 8, Liturgy: Matthew 23:13-26 versus 23:13-36. The latter Katameros witness is already inactive. Both named pairs receive flags without lifecycle or coordinate changes.

Report-only current inventory: 31 context/service/slot/start groups, 365 dated groups and 365 distinct dated slots. Each exact date and source tuple is retained in endpoint-conflicts.json. The next table lists the complete inventory, not only the two examples.

| Context | Service and slot | Canonical MT variants | Retained dates |
|---|---|---|---|
| annual_sunday:amshir-2 | Liturgy , psalm | Ps 96:7 / Ps 96:7-8 | 2024-02-18, 2025-02-16, 2030-02-17, 2035-02-18 |
| annual_sunday:amshir-4 | Liturgy , psalm | Ps 24:1 / Ps 24:1-2 | 2024-03-03 |
| annual_sunday:bashans-4 | Matins , psalm | Ps 47:6 / Ps 47:6-7 | 2029-06-03, 2034-06-04 |
| annual_sunday:hatour-4 | Liturgy , catholicon | 2Pet 1:1-18 / 2Pet 1:1-8 | 2020-12-06, 2021-12-05, 2022-12-04, 2023-12-03, 2024-12-01, 2025-12-07, 2026-12-06, 2027-12-05, 2028-12-03, 2029-12-02, 2030-12-01, 2031-12-07, 2032-12-05, 2033-12-04, 2034-12-03, 2035-12-02 |
| annual_sunday:kiahk-1 | Matins , psalm | Ps 102:19 / Ps 102:19-21 | 2020-12-13, 2021-12-12, 2022-12-11, 2024-12-15, 2025-12-14, 2026-12-13, 2027-12-12, 2028-12-10, 2030-12-15, 2031-12-14, 2032-12-12, 2033-12-11, 2034-12-10, 2035-12-16 |
| annual_sunday:kiahk-3 | Matins , psalm | Ps 85:7 / Ps 85:7-8 | 2020-12-27, 2021-12-26, 2022-12-25, 2024-12-29, 2025-12-28, 2026-12-27, 2027-12-26, 2028-12-24, 2030-12-29, 2031-12-28, 2032-12-26, 2033-12-25, 2034-12-24, 2035-12-30 |
| annual_sunday:mesra-3 | Liturgy , gospel | Mark 3:22-34 / Mark 3:22-35 | 2020-08-23, 2022-08-21, 2023-08-27, 2024-08-25, 2025-08-24, 2026-08-23, 2028-08-27, 2029-08-26, 2030-08-25, 2031-08-24, 2033-08-21, 2034-08-27, 2035-08-26 |
| annual_sunday:mesra-4 | Vespers , gospel | Lk 17:20-36 / Lk 17:20-37 | 2020-08-30, 2021-08-29, 2022-08-28, 2023-09-03, 2024-09-01, 2025-08-31, 2026-08-30, 2027-08-29, 2028-09-03, 2029-09-02, 2030-09-01, 2031-08-31, 2032-08-29, 2033-08-28, 2034-09-03, 2035-09-02 |
| annual_sunday:paona-2 | Liturgy , catholicon | 2Pet 1:1-8 / 2Pet 1:1-9 | 2020-06-21, 2022-06-19, 2023-06-18, 2025-06-15, 2026-06-21, 2028-06-18, 2029-06-17, 2031-06-15, 2033-06-19, 2034-06-18 |
| coptic_date:baramhat-2 | Liturgy , catholicon | 3Jn 1:1-14 / 3Jn 1:1-15 | 2024-03-11 |
| coptic_date:baramhat-2 | Liturgy , pauline | Heb 7:18-28 / Heb 7:18-8:13 | 2024-03-11 |
| coptic_date:baramhat-2 | Liturgy , praxis | Acts 15:36-16:5 / Acts 15:36-41 | 2024-03-11 |
| coptic_date:baramhat-29 | Liturgy , catholicon | 1Jn 1:1-10 / 1Jn 1:1-2:6 | 2020-04-07, 2021-04-07, 2022-04-07, 2024-04-07, 2025-04-07, 2027-04-07, 2029-04-07, 2030-04-07, 2032-04-07, 2033-04-07, 2035-04-07 |
| coptic_date:hatour-16 | Liturgy , pauline | Heb 11:32-12:2 / Heb 11:32-40 | 2020-11-25, 2021-11-25, 2022-11-25, 2024-11-25, 2025-11-25, 2026-11-25, 2027-11-26, 2028-11-25, 2030-11-25, 2031-11-26, 2032-11-25, 2033-11-25, 2034-11-25, 2035-11-26 |
| coptic_date:hatour-16 | Liturgy , praxis | Acts 18:24-19:6 / Acts 18:24-28 | 2020-11-25, 2021-11-25, 2022-11-25, 2024-11-25, 2025-11-25, 2026-11-25, 2027-11-26, 2028-11-25, 2030-11-25, 2031-11-26, 2032-11-25, 2033-11-25, 2034-11-25, 2035-11-26 |
| coptic_date:kiahk-28 | Liturgy , pauline | Gal 3:15-29 / Gal 3:15-4:18 | 2021-01-06, 2022-01-06, 2023-01-06, 2025-01-06, 2026-01-06, 2027-01-06, 2029-01-06, 2030-01-06, 2031-01-06, 2033-01-06, 2034-01-06, 2035-01-06 |
| coptic_date:kiahk-28 | Matins , psalm | Ps 76:1 / Ps 76:1-2 | 2021-01-06, 2022-01-06, 2023-01-06, 2025-01-06, 2026-01-06, 2027-01-06, 2029-01-06, 2030-01-06, 2031-01-06, 2033-01-06, 2034-01-06, 2035-01-06 |
| coptic_date:kiahk-29 | Liturgy , pauline | Heb 1:1-14 / Heb 1:1-2:4 | 2020-01-08, 2021-01-07, 2022-01-07, 2023-01-07, 2024-01-08, 2025-01-07, 2026-01-07, 2027-01-07, 2028-01-08, 2029-01-07, 2030-01-07, 2031-01-07, 2032-01-08, 2033-01-07, 2034-01-07, 2035-01-07 |
| coptic_date:mesra-1 | Liturgy , praxis | Acts 7:44-60 / Acts 7:44-8:1 | 2020-08-07, 2021-08-07, 2022-08-07, 2023-08-07, 2024-08-07, 2025-08-07, 2026-08-07, 2027-08-07, 2028-08-07, 2029-08-07, 2030-08-07, 2031-08-07, 2032-08-07, 2033-08-07, 2034-08-07, 2035-08-07 |
| coptic_date:mesra-13 | Liturgy , praxis | Acts 7:44-60 / Acts 7:44-8:1 | 2020-08-19, 2021-08-19, 2022-08-19, 2023-08-19, 2024-08-19, 2025-08-19, 2026-08-19, 2027-08-19, 2028-08-19, 2029-08-19, 2030-08-19, 2031-08-19, 2032-08-19, 2033-08-19, 2034-08-19, 2035-08-19 |
| coptic_date:nasie-2 | Liturgy , pauline | 2Cor 3:12-18 / 2Cor 3:12-4:4 | 2020-09-07, 2021-09-07, 2022-09-07, 2023-09-07, 2024-09-07, 2026-09-07, 2027-09-07, 2028-09-07, 2029-09-07, 2030-09-07, 2032-09-07, 2033-09-07, 2034-09-07, 2035-09-07 |
| coptic_date:nasie-3 | Liturgy , psalm | Ps 138:1-2 / Ps 138:1-3 | 2020-09-08, 2021-09-08, 2022-09-08, 2023-09-08, 2025-09-08, 2026-09-08, 2027-09-08, 2028-09-08, 2029-09-08, 2031-09-08, 2032-09-08, 2033-09-08, 2034-09-08, 2035-09-08 |
| coptic_date:nasie-4 | Liturgy , praxis | Acts 18:24-19:6 / Acts 18:24-28 | 2020-09-09, 2021-09-09, 2022-09-09, 2023-09-09, 2024-09-09, 2025-09-09, 2026-09-09, 2027-09-09, 2028-09-09, 2030-09-09, 2031-09-09, 2032-09-09, 2033-09-09, 2034-09-09 |
| coptic_date:nasie-5 | Liturgy , catholicon | 3Jn 1:1-14 / 3Jn 1:1-15 | 2020-09-10, 2021-09-10, 2022-09-10, 2024-09-10, 2025-09-10, 2026-09-10, 2027-09-10, 2029-09-10, 2030-09-10, 2031-09-10, 2032-09-10, 2033-09-10, 2035-09-10 |
| coptic_date:nasie-5 | Liturgy , pauline | Heb 7:18-28 / Heb 7:18-8:13 | 2020-09-10, 2021-09-10, 2022-09-10, 2024-09-10, 2025-09-10, 2026-09-10, 2027-09-10, 2029-09-10, 2030-09-10, 2031-09-10, 2032-09-10, 2033-09-10, 2035-09-10 |
| coptic_date:nasie-5 | Liturgy , praxis | Acts 15:36-16:5 / Acts 15:36-41 | 2020-09-10, 2021-09-10, 2022-09-10, 2024-09-10, 2025-09-10, 2026-09-10, 2027-09-10, 2029-09-10, 2030-09-10, 2031-09-10, 2032-09-10, 2033-09-10, 2035-09-10 |
| coptic_date:toba-10 | Matins , psalm | Ps 42:7 / Ps 42:7-8 | 2020-01-19, 2021-01-18, 2022-01-18, 2023-01-18, 2024-01-19, 2025-01-18, 2026-01-18, 2027-01-18, 2028-01-19, 2029-01-18, 2030-01-18, 2031-01-18, 2032-01-19, 2033-01-18, 2034-01-18, 2035-01-18 |
| coptic_date:toba-11 | Liturgy , pauline | Titus 2:11-15 / Titus 2:11-3:7 | 2020-01-20, 2021-01-19, 2022-01-19, 2023-01-19, 2024-01-20, 2025-01-19, 2026-01-19, 2027-01-19, 2028-01-20, 2029-01-19, 2030-01-19, 2031-01-19, 2032-01-20, 2033-01-19, 2034-01-19, 2035-01-19 |
| coptic_date:toba-11 | Liturgy , praxis | Acts 18:24-19:6 / Acts 18:24-28 | 2020-01-20, 2021-01-19, 2022-01-19, 2023-01-19, 2024-01-20, 2025-01-19, 2026-01-19, 2027-01-19, 2028-01-20, 2029-01-19, 2030-01-19, 2031-01-19, 2032-01-20, 2033-01-19, 2034-01-19, 2035-01-19 |
| coptic_date:toba-12 | Liturgy , psalm | Ps 104:1 / Ps 104:1-2 | 2020-01-21, 2021-01-20, 2022-01-20, 2023-01-20, 2024-01-21, 2025-01-20, 2026-01-20, 2027-01-20, 2028-01-21, 2029-01-20, 2030-01-20, 2031-01-20, 2032-01-21, 2033-01-20, 2034-01-20, 2035-01-20 |
| coptic_date:tout-19 | Liturgy , gospel | Lk 14:25-32 / Lk 14:25-35 | 2020-09-29, 2021-09-29, 2022-09-29, 2023-09-30, 2024-09-29, 2025-09-29, 2026-09-29, 2027-09-30, 2028-09-29, 2029-09-29, 2030-09-29, 2031-09-30, 2032-09-29, 2033-09-29, 2034-09-29, 2035-09-30 |

## LK3: unresolved source sentinel

The two inactive Exodus witnesses under source week 49 remain inactive. Their label discloses the unresolved source week instead of inventing a forty-ninth liturgical week.
