# Phase 0 Grok Research Memo

## Executive Findings

- The Coptic Orthodox lectionary is best modeled as four principal books: Annual, Great Lent, Pascha, and Pentecost or Holy Fifty. This is directly supported by the Coptic Encyclopedia.
- The Annual Katameros contains Sundays and weekdays not assigned to the other principal books. Sunday readings form their own thematic program, with the four Sundays of a Coptic month usually read together as a theme.
- Weekday readings are tied to the Synaxarium calendar. The lectionary rubrics name feasts and saints, so the lectionary itself functions as a calendar witness, not only a Bible reading index.
- Great Lent, Holy Week or Pascha, and Holy Fifty have distinct reading logic and should not be flattened into the Annual cycle.
- Pascha must be modeled by day, eve or day segment, hour, and slot. Current project evidence confirms that Coptic Reader Pascha Wednesday Day differs from older or local witnesses in several readings.
- Date logic has three classes: fixed Coptic calendar dates, movable dates hinged on Pascha, and daily Synaxarium commemorations.
- Precedence must be explicit in schema. Sunday readings are a separate program, major feasts can override Sundays, and weekday readings follow Synaxarium unless a higher ranked feast, season, or service applies.
- Youssef confirms a 69-collection arrangement by feast or commemoration type, but the full English list was not exposed in the accessible source packet. Do not hardcode 69 collection names yet.
- Psalm handling needs source-aware numbering. Coptic liturgical Psalms are LXX in principle, but the current local dataset is uniformly MT/NKJV-numbered across Pascha and Katameros-cycle rows. Verse shifts cannot be handled by chapter-only mapping.

## Source Registry

| Source | URL | Confidence | Supports |
|---|---:|---:|---|
| Coptic Encyclopedia, “Lectionary,” Claremont CCDL | https://ccdl.claremont.edu/digital/api/collection/cce/id/1199/download | High | Four lectionary books, Katameros meaning, Annual scope, Sunday monthly themes, rubrics as calendar evidence, historical variation before print uniformity |
| Fouad Naguib Youssef, “The Arrangement of the Church Lectionary,” ACCOT | https://accot.stcyrils.edu.au/fny-read1/ | High for principles, partial for collection list | Coptic calendar basis, Hebrew calendar and Nicene Pascha rule, Sunday program, Synaxarium basis for daily readings, 69 collections claim |
| Fr. Mikhail E. Mikhail, “Scriptural and Liturgical Guide Based on the Coptic Orthodox Lectionary” | http://www.coptic.net/articles/copticlectionary.txt | Medium-high | Sundays, weekdays, Great Lent, Holy Week, Pentecost, theological arc of readings, Lent prophecy and fulfillment, Passion Week by day and hour |
| Coptic Reader, Diocese of the Southern US, manual fixture | No public plaintext endpoint confirmed | Highest within captured fixture scope | Current-practice authority for manually captured readings, especially Pascha Wednesday Day Psalm labels and current reading set |
| Project design brief and locked findings | Local project source packet, Section 6 Phase 0 | High for project constraints | Current authority tiers, Coptic Reader encryption constraint, historical Pascha witness policy, Psalm mapping risks, local dataset row counts |
| Local reverse lookup crosswalk | `reverse_lookup_crosswalk.csv` | High for local package state, medium for current church authority | 66,352 base rows before fixture layer, source kinds, MT/NKJV numbering convention in stored rows |
| Additive Coptic Reader fixture layer | Local generated design layer | High for fixture rows only | Adds 26 Pascha Wednesday Day rows, producing 66,378 presentation rows |
| St-Takla Synaxarium parsed local index | Local parsed dataset, source URL not supplied in packet | Medium | 366 Coptic day rows, 919 extracted commemoration records |
| Public-domain Brenton Septuagint, local copy | Local resource | High for validation use | Psalm identity checks and LXX comparison without storing copyrighted Bible text |

## Lectionary Structure

The Coptic lectionary is a set of books containing Scripture readings and rubrics for the Church’s liturgies.

Confirmed principal books:

1. Annual Katameros
   - Covers ordinary Sundays and weekdays except readings assigned to other lectionary books.
   - Sunday readings form a structured program. The four Sundays of each Coptic month together present a theme.
   - Weekday readings are tied to the Synaxarium and saints’ commemorations.

2. Great Lent Katameros
   - Separate book or reading cycle for Great Lent.
   - Fr. Mikhail describes Lenten readings as showing Old Testament prophecy and New Testament fulfillment.
   - Should be modeled separately from ordinary Annual weekdays.

3. Pascha or Holy Week book
   - Separate structure for Passion Week.
   - Readings follow the Lord’s suffering day by day and hour by hour.
   - Requires day, eve/day segment, hour, and reading slot fields.

4. Pentecost or Holy Fifty book
   - Separate book for the Resurrection season.
   - Fr. Mikhail describes these readings as presenting the risen Christ, the fruits of the Resurrection, Ascension, and Pentecost themes.

Historical note:

- Different Upper Egyptian and Lower Egyptian lectionary traditions existed before print uniformity.
- Older Pascha readings in local or historical sources should be retained as witnesses when current Coptic Reader differs.

## Seasons and Cycles

| Season or cycle | Status | Structure notes |
|---|---:|---|
| Annual | Confirmed | Fixed Coptic calendar cycle. Includes ordinary Sundays and weekdays not assigned to other books. Sundays form monthly themes. Weekdays follow Synaxarium. |
| Kiahk | Needs exact source confirmation | Should be treated as a fixed Coptic-month seasonal subcycle within the Annual system unless a source proves a separate book. Schema should support Kiahk Sunday and weekday labels. |
| Great Lent | Confirmed | Separate lectionary. Includes weekday and Sunday readings. Common Sunday labels should be stored as controlled labels only after checking current-practice source. |
| Great Lent Sundays | Confirmed as category, exact names need current-source check | Working labels: Treasures, Temptation, Prodigal Son, Samaritan Woman, Paralytic, Man Born Blind, then Palm Sunday as transition into Holy Week. Confirm against Coptic Reader before locking. |
| Holy Week or Pascha | Confirmed | Separate book. Day and hour structure. Must preserve historical witnesses and current Coptic Reader fixtures distinctly. |
| Holy Fifty or Pentecost | Confirmed | Separate Resurrection-season lectionary through Pentecost. Includes Ascension and Pentecost logic as Pascha-relative movable dates. |
| Fixed fasts | Partly sourced | Nativity Fast and St. Mary Fast belong in calendar vocabulary, but source packet does not confirm exact lectionary override rules. |
| Movable fasts | Partly sourced | Great Lent is confirmed. Jonah/Nineveh Fast and Apostles’ Fast should be represented as possible fast periods, but exact reading rules need source confirmation. |
| Special services | Confirmed by local data kinds | Includes rite-specific reading tables outside ordinary day cycles. Current local kinds include special service, Agpeya, and Bright Saturday service order. |

## Date Calculation and Precedence

### Date calculation rules

1. Coptic fixed calendar
   - Fixed feasts and Synaxarium commemorations are assigned by Coptic month and day.
   - The Coptic year has fixed month/day placement, with a leap-day issue for the small month that schema must handle.

2. Movable feasts hinged on Pascha
   - Youssef states that the Feast of the Resurrection follows the Hebrew calendar and the Nicene rule: the Sunday following Jewish Passover, following Alexandrian and Roman custom.
   - Great Lent, Holy Week, Resurrection, Ascension, Pentecost, and related movable fasts or feasts should be stored by offset from Pascha, not by fixed Gregorian date.

3. Fixed feasts
   - Fixed feasts should be stored by Coptic month and day.
   - Examples should be source-confirmed before being used as precedence tests.

4. Daily Synaxarium
   - Daily commemorations are Coptic fixed-date records.
   - A single Coptic day can carry multiple commemorations.

### Precedence rules

Working precedence order for schema design:

1. Current-practice service fixture when manually captured from Coptic Reader.
2. Pascha or Holy Week service assignment.
3. Major feast of the Lord or other high-rank feast.
4. Great Lent or Holy Fifty seasonal assignment.
5. Sunday program.
6. Weekday Synaxarium-based reading.
7. Ordinary Annual weekday fallback.
8. Historical witness layer, retained but not treated as current-practice unless confirmed.

Specific supported rules:

- Sunday readings are a separate program when a Coptic day falls on Sunday.
- Daily readings follow the Synaxarium.
- Feasts can override ordinary Sunday or weekday assignments, but the exact ranked list and edge cases need source confirmation.
- Special service readings should be tied to the service being performed, not treated as the calendar day’s ordinary readings.
- Pascha readings must not be resolved by date alone. They need day/hour context.

## Controlled Vocabularies

### Season values

Recommended initial season enum:

- `annual`
- `kiahk`
- `great-lent`
- `holy-week-pascha`
- `holy-fifty`
- `fixed-fast`
- `movable-fast`
- `special-service`
- `agpeya`
- `historical-witness`

### Occasion type values

Recommended initial occasion enum:

- `ordinary-sunday`
- `ordinary-weekday`
- `synaxarium-commemoration`
- `fixed-feast`
- `movable-feast`
- `feast-of-the-Lord`
- `fast-day`
- `paramoun`
- `kiahk-sunday`
- `great-lent-sunday`
- `great-lent-weekday`
- `pascha-day-hour`
- `holy-fifty-day`
- `bright-saturday`
- `special-service`
- `agpeya-hour`
- `historical-removed-reading`
- `historical-source-witness`

### Collection types

Confirmed:

- Youssef supports that the lectionary is arranged into 69 collections by feast or commemoration type.

Not confirmed:

- The accessible packet does not expose the full English list of all 69 collection types.

Schema recommendation:

- Store `collection-number` only when source-confirmed.
- Store `collection-label-raw` from source.
- Store `collection-label-normalized` after authority review.
- Do not invent or infer the 69 labels.

### Service, hour, and slot enums

Recommended service enum:

- `vespers`
- `matins`
- `divine-liturgy`
- `pascha-eve`
- `pascha-day`
- `bright-saturday`
- `agpeya`
- `special-service`

Recommended Pascha hour enum:

- `first-hour`
- `third-hour`
- `sixth-hour`
- `ninth-hour`
- `eleventh-hour`
- `twelfth-hour`

Recommended reading slot enum:

- `prophecy`
- `pauline-epistle`
- `catholic-epistle`
- `acts`
- `synaxarium`
- `psalm`
- `gospel`
- `homily`
- `exposition`
- `apocalypse`
- `other-source-labeled-slot`

Slot caution:

- Preserve raw slot labels. For example, current project findings prefer “Catholic Epistle” rather than replacing it with “Catholicon” in generated labels.

### Authority tiers

Recommended authority enum:

- `current-practice-coptic-reader`
- `manual-current-fixture`
- `scholarly-structural`
- `published-liturgical-study`
- `public-web-reference`
- `local-generated-index`
- `local-parsed-synaxarium`
- `historical-source-text`
- `uncertain-or-derived`

### Source kind values from local package

Known current source kinds:

- `copticchurch-date`
- `katameros-cycle`
- `pascha-day-hour`
- `special-service`
- `pascha-source-text`
- `agpeya`
- `bright-saturday-service-order`
- `coptic-reader-fixture`

## Synaxarium Implications

- Daily readings follow the Synaxarium, so the Synaxarium is not optional metadata. It is part of the reading-selection model for weekdays.
- The Coptic Encyclopedia notes that lectionary rubrics naming feasts and saints form a valuable calendar. These rubrics should be preserved as source evidence.
- The local St-Takla Synaxarium index has 366 day rows and 919 extracted commemoration records. This means a day-to-commemoration relationship is one-to-many.
- Synaxarium parsing should produce separate commemoration records with source title, normalized title, Coptic month, Coptic day, and confidence.
- Do not assume every commemoration controls the reading. A day may have multiple commemorations, and feast precedence or Sunday precedence may control the final assigned readings.
- Sunday readings can override the weekday Synaxarium reading logic. The Synaxarium still remains useful for annotation, search, and feast context.
- The schema should distinguish:
  - calendar commemoration
  - lectionary occasion
  - reading assignment
  - source rubric
  - computed presentation row

## Unresolved Source Gaps

- Full list of the 69 Youssef collection types is not confirmed from the accessible text. The claim is confirmed, the list is not.
- Exact feast precedence hierarchy is not fully sourced. The project needs a ranked list covering feasts of the Lord, fixed feasts, movable feasts, Sundays, Lent, Holy Fifty, and weekday Synaxarium cases.
- Kiahk needs current-source confirmation: exact Sunday names, weekday handling, and whether it is only an Annual subcycle or has distinct collection treatment.
- Great Lent Sunday labels should be checked against Coptic Reader before being locked as canonical enum values.
- Fast reading rules outside Great Lent need source confirmation, especially Jonah/Nineveh Fast, Apostles’ Fast, Nativity Fast, and St. Mary Fast.
- Coptic Reader has no confirmed plaintext public endpoint. Current-practice validation depends on manual fixtures unless a lawful extraction path is approved.
- Pascha Wednesday Day has a current Coptic Reader fixture, but other Pascha days and hours still need current-practice fixture coverage.
- Older/local Pascha readings absent from the Coptic Reader Wednesday Day fixture should be retained as historical witnesses, not deleted as errors.
- Psalm numbering must remain source-aware. LXX to MT mapping can shift verses due to superscriptions, so chapter-only conversion is unsafe.
- St-Takla Synaxarium source URL and extraction method should be recorded in the source registry if the parsed 919 commemoration records become schema inputs.
