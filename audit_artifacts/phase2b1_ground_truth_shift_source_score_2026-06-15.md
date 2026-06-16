# Phase 2b-1 Report — Ground Truth Fixture, Eve/Day Shift Test, Source Scoring

- Date: 2026-06-15
- Scope: measurement only
- Dataset/parser/schema/verifier changes: **none**
- Committed artifacts intended for this phase:
  - `tests/fixtures/pascha_wednesday_day_coptic_reader.json`
  - `audit_artifacts/phase2b1_ground_truth_shift_source_score_2026-06-15.md`

## Executive summary

1. I added a locked JSON fixture for **Wednesday of Pascha, Day hours**, sourced from George's Coptic Reader screenshots/manual read.
2. The Eve/Day shift does **not** explain the Wednesday Day issue.
   - Stored **Wednesday Day** matches the fixture at **21/26** unique `(canonical hour, slot group, reading)` items.
   - Stored **Wednesday Eve** matches the Day fixture at **0/26** when re-keyed as Eve.
   - So this is not primarily an off-by-one Eve/Day relabeling bug for Wednesday Day.
3. The earlier Phase 1 “62” number is not a machine-readable Wednesday Day mismatch artifact. In the current repo report it refers to **62 mismatching Pascha day/hour groups against St. Mary source text across the whole Pascha blast radius**, and separately a **62-line rendered query** for `Mark 12:18-27`. Treat any pre-canonical 62-count as unreliable for Wednesday Day.
4. Live Katameros API result contradicted the expected probe result:
   - `https://api.katameros.app/readings/gregorian/16-04-2025?languageId=2` returns `title: Pascha Wednesday` and Pascha hour sections.
   - Same for `08-04-2026`.
   - But the local `sources/katameros-api/Core/KatamerosDatabase.db` has no Pascha/Holy Week tables. Local SQLite is annual/Sunday/Great Lent/Pentecost structure only.
5. Against the Coptic Reader Day fixture, source scoring is:
   - Stored dataset: **21/26 = 80.77%**
   - St. Mary source-text index: **15/26 = 57.69%**
   - Live Katameros API 2025: **14/26 = 53.85%**
   - Live Katameros API 2026: **14/26 = 53.85%**
6. Stored dataset scores best, but that does **not** make it an independent source. Among external sources, St. Mary slightly beats live Katameros but still misses too much to auto-extend confidently without more Coptic Reader fixtures.
7. Phase 2a Great Lent conflict re-check: live Katameros API for the best available dates supports keeping `Id=46` over `Id=53` for Matins Psalm.
   - 2025-04-10: `Ps 63:1`, no `Ps 64:2-4`
   - 2026-04-02: `Ps 63:1`, no `Ps 64:2-4`
8. Several existing Pascha verifier checks encode pre-Coptic-Reader expectations and would need rewrite before being used as correctness evidence.

## 1. Locked ground-truth fixture

Created:

```text
tests/fixtures/pascha_wednesday_day_coptic_reader.json
```

Fixture metadata:

- `fixture_id`: `pascha_wednesday_day_coptic_reader`
- `locked`: `true`
- Scope: `Holy Pascha / Wednesday / day`
- Source: Coptic Reader app, provided by George
- Rule: Scripture readings only. Liturgical/homiletic items are context, not lectionary readings.

Fixture item count: **26** unique reading items after splitting combined Psalm references.

| Hour | Fixture items |
|---|---:|
| 1st Hour | 6 |
| 3rd Hour | 5 |
| 6th Hour | 6 |
| 9th Hour | 5 |
| 11th Hour | 4 |
| **Total** | **26** |

Notable fixture flags preserved:

- 3rd Hour screenshot cut off after the Gospel; may be incomplete below the Gospel.
- 6th Hour includes `Memoirs of Job` as a named, non-versed reading.
- 9th Hour records `Proverbs 1:11-35` exactly as shown. I did not auto-correct it even though standard Proverbs 1 has 33 verses.

## 2. Canonical label mapping

I used this canonical key format before diffing:

```text
pascha:<day>:<eve_or_day>:<hour>
```

Examples:

```text
pascha:wednesday:day:first_hour
pascha:wednesday:day:third_hour
pascha:wednesday:day:sixth_hour
pascha:wednesday:day:ninth_hour
pascha:wednesday:day:eleventh_hour
pascha:wednesday:eve:first_hour
...
```

### Mapping rules

| Source | Native labels | Canonical mapping |
|---|---|---|
| Ground-truth fixture | `Wednesday`, `day`, `1st/3rd/6th/9th/11th Hour` | `pascha:wednesday:day:<hour>` |
| Stored dataset `pascha_day_hour_index.csv` | `day`, `hour`, `slot`, `refs` | `Wednesday` → `pascha:wednesday:day:<hour>`; `Wednesday Eve` → `pascha:wednesday:eve:<hour>` |
| St. Mary source text index | `day`, `hour`, `reading_type`, `normalized_ref` | Same day/hour mapping as stored dataset |
| Live Katameros API for `16-04-2025` / `08-04-2026` | top-level `sections` such as `First Hour`, `Third Hour`, and `First Hour Eve of Pascha Thursday` | plain hour sections → `pascha:wednesday:day:<hour>`; `Eve of Pascha Thursday` sections are **after Wednesday Day**, so I mapped them separately as `pascha:wednesday:eve_after_day:<hour>` and did not use them as Wednesday Eve/Tues-evening comparator |

### Why pre-canonical mismatch counts are unreliable

Before this mapping, `Wednesday Eve`, `Wednesday Day`, `Eve of Pascha Thursday`, `Psalm+Gospel`, `Psalm`, `Gospel`, and `OTn/Prophecy` labels can be mixed incorrectly. The Phase 1 62-count was not a Coptic Reader Wednesday Day mismatch count. It was a broader Pascha/St. Mary source-text blast-radius count.

## 3. Eve/Day shift test

### Result table

| Compared source | Expected fixture items | Actual source items | Matches | Match rate |
|---|---:|---:|---:|---:|
| Stored Wednesday Day vs Day fixture | 26 | 32 | 21 | 80.77% |
| Stored Wednesday Eve vs Day fixture re-keyed to Eve | 26 | 18 | 0 | 0.00% |
| St. Mary Wednesday Day vs Day fixture | 26 | 32 | 15 | 57.69% |
| St. Mary Wednesday Eve vs Day fixture re-keyed to Eve | 26 | 17 | 0 | 0.00% |

### Conclusion

The dataset's stored **Wednesday Day**, not Wednesday Eve, lines up with the Coptic Reader Day fixture.

The Eve/Day shift explains **0** of the measured fixture misses. The remaining fixture misses are genuine content/reference mismatches, not a relabeling fix.

### Stored Wednesday Day missing fixture items

These fixture items are missing from stored Wednesday Day:

```text
pascha:wednesday:day:first_hour | psalm | Ps 50:6
pascha:wednesday:day:first_hour | psalm | Ps 32:10
pascha:wednesday:day:sixth_hour | prophecy | Memoirs of Job
pascha:wednesday:day:ninth_hour | psalm | Ps 40:6-8
pascha:wednesday:day:eleventh_hour | psalm | Ps 68:17
```

### Stored Wednesday Day extra items not in fixture

```text
pascha:wednesday:day:first_hour | prophecy | Wis 1:20-2:15
pascha:wednesday:day:first_hour | prophecy | Wis 3:12-24
pascha:wednesday:day:first_hour | psalm | Ps 51:4
pascha:wednesday:day:first_hour | psalm | Ps 33:10
pascha:wednesday:day:third_hour | prophecy | Prov 4:4-5:4
pascha:wednesday:day:sixth_hour | prophecy | Job 27:16-20
pascha:wednesday:day:sixth_hour | prophecy | Job 28:1-2
pascha:wednesday:day:ninth_hour | prophecy | Isa 59:1-17
pascha:wednesday:day:ninth_hour | prophecy | Zech 11:11-14
pascha:wednesday:day:ninth_hour | psalm | Ps 41:5-6
pascha:wednesday:day:eleventh_hour | psalm | Ps 69:17
```

### Stored Wednesday Eve result

Stored Wednesday Eve had **0** fixture matches after re-keying.

Examples of stored Wednesday Eve extras compared to Day fixture:

```text
pascha:wednesday:eve:first_hour | prophecy | Jer 43:5-11
pascha:wednesday:eve:first_hour | psalm | Ps 69:1
pascha:wednesday:eve:first_hour | psalm | Ps 69:16
pascha:wednesday:eve:first_hour | gospel | Jn 10:17-21
pascha:wednesday:eve:third_hour | prophecy | Amos 4:4-13
pascha:wednesday:eve:third_hour | psalm | Ps 55:21
pascha:wednesday:eve:third_hour | psalm | Ps 55:1
pascha:wednesday:eve:third_hour | gospel | Mark 14:3-11
pascha:wednesday:eve:sixth_hour | prophecy | Amos 3:1-11
pascha:wednesday:eve:sixth_hour | psalm | Ps 140:1
pascha:wednesday:eve:sixth_hour | psalm | Ps 140:2
pascha:wednesday:eve:sixth_hour | gospel | Jn 12:36-43
pascha:wednesday:eve:ninth_hour | prophecy | Ezek 20:27-33
pascha:wednesday:eve:ninth_hour | gospel | Jn 10:29-38
pascha:wednesday:eve:eleventh_hour | prophecy | Wis 7:24-30
pascha:wednesday:eve:eleventh_hour | psalm | Ps 57:1
pascha:wednesday:eve:eleventh_hour | gospel | Jn 11:55-57
```

### Quantifying the prior 62

The current repo contains a Phase 1 St. Mary blast-radius count:

- `62` mismatching day/hour groups across the whole Pascha source-text comparison.
- `16` affected source day labels.
- Wednesday Day accounted for `5` of those source day/hour groups and Wednesday Eve for `4`.

Against the new Coptic Reader Day fixture:

| Category | Count |
|---|---:|
| Fixture unique `(slot group, reading)` items | 26 |
| Present in stored Wednesday Day | 21 |
| Missing from Day but present in stored Wednesday Eve | 0 |
| Not fixed by Eve/Day shift | 5 |

So, for the new Coptic Reader Day fixture, **0** mismatches are explained by Eve/Day shift; **5** fixture misses are genuine content/reference differences.

## 4. Katameros coverage probe

### Live API

Commands probed:

```bash
curl -L -sS --fail 'https://api.katameros.app/readings/gregorian/16-04-2025?languageId=2'
curl -L -sS --fail 'https://api.katameros.app/readings/gregorian/08-04-2026?languageId=2'
```

Both returned JSON with:

```text
title: Pascha Wednesday
sections:
- First Hour
- Third Hour
- Sixth Hour
- Ninth Hour
- Eleventh hour
- First Hour Eve of Pascha Thursday
- Third Hour Eve of Pascha Thursday
- Sixth Hour Eve of Pascha Thursday
- Ninth Hour Eve of Pascha Thursday
- Eleventh hour Eve of Pascha Thursday
```

Each response produced **46** extracted passage items including Pascha hour prophecies and Psalm/Gospel pairs.

Conclusion for live API: **it does contain Pascha hour-day coverage** for the requested Wednesday dates. This differs from the expected result in the task.

### Live API Wednesday Day examples

For `16-04-2025`, live Katameros API had:

```text
First Hour: Exod 17:1-7; Prov 3:5-15; Hos 5:13-6:3; Sir 1:20-2:15; Sir 3:12-24; Ps 51:4; Ps 33:10; Jn 11:46-57
Third Hour: Exod 13:17-22; Sir 22:7-18; Job 27:16-20; Job 28:1-2; Prov 4:4-5:4; Ps 41:6,41:1; Lk 22:1-6
Sixth Hour: Exod 14:13-15:1; Isa 48:1-6; Sir 23:7-14; Ps 83:2,83:5; Jn 12:1-8
Ninth Hour: Gen 24:1-9; Num 20:1-13; Prov 1:10-23; Isa 59:1-17; Zech 11:11-14; Ps 41:5-6; Matt 26:3-16
Eleventh Hour: Isa 28:16-29; Ps 6:2; Ps 69:17; Jn 12:27-36
```

### Local Katameros SQLite

Local DB inspected:

```text
sources/katameros-api/Core/KatamerosDatabase.db
```

Tables found: **27**

```text
AnnualReadings
Bibles
Books
BooksTranslations
Feasts
FeastsTranslations
GreatLentReadings
Languages
PentecostReadings
Readings
ReadingsMetadatas
ReadingsMetadatasTranslations
Sections
SectionsMetadatas
SectionsMetadatasTranslations
Sentences
SentencesTranslations
SubSections
SubSectionsMetadatas
SubSectionsMetadatasTranslations
SundayReadings
Synaxarium
VerseRefMappings
Verses
VersificationSchemes
__EFMigrationsHistory
sqlite_sequence
```

Pascha/Holy/Palm/Bright/Covenant-like tables: **none**.

Conclusion for local SQLite: **not usable for Pascha hour-days**. It only has annual/Sunday/Great Lent/Pentecost-style cycle tables plus metadata/Bible text tables.

### Katameros conclusion

- Live Katameros API is usable as a comparator for Pascha hour-days, but it conflicts with George's Coptic Reader fixture on several Wednesday Day references.
- Local Katameros SQLite is **not** usable for Pascha hour-days.
- Treat Coptic Reader fixture as source of record for this pass.
- Treat live Katameros API as secondary comparator only, not controlling authority.
- Treat local SQLite as comparator only for annual/Great Lent cycle rows and, where appropriate, liturgy-day structures already represented in its cycle tables.

## 5. Source scoring against Wednesday Day fixture

Scoring unit: unique `(canonical hour, slot group, normalized reading)`.

| Source | Expected fixture items | Source items | Matches | Match rate |
|---|---:|---:|---:|---:|
| Stored dataset `pascha_day_hour_index.csv` | 26 | 32 | 21 | 80.77% |
| St. Mary `pascha_source_text_index.csv` | 26 | 32 | 15 | 57.69% |
| Live Katameros API 2025-04-16 | 26 | 31 | 14 | 53.85% |
| Live Katameros API 2026-04-08 | 26 | 31 | 14 | 53.85% |

### Interpretation

The stored dataset currently matches George's fixture best, but it is not an independent source and already includes post-hoc St. Mary corrections plus leftover `api` rows.

Among external comparators:

1. St. Mary source-text index: 15/26
2. Live Katameros API: 14/26

That margin is too small and the absolute match rates are too low to auto-extend unscreenshotted Holy Week days with high confidence. My recommendation from this measurement: do **not** auto-extend solely from St. Mary or live Katameros yet. Use the Coptic Reader fixture pattern for approved day-by-day corrections, and gather more Coptic Reader fixtures before broad Holy Week rewrite.

## 6. Provenance

### Stored Pascha data source counts

Current `out/data/pascha_day_hour_index.csv` source counts:

| Source marker | Rows |
|---|---:|
| `api` | 144 |
| `St Mary Ottawa Holy Pascha book correction 2026-06-14` | 17 |
| `St Mary Ottawa Holy Pascha source-text correction 2026-06-06` | 6 |
| `book` | 2 |
| `api+St Mary Ottawa Holy Pascha source-text correction 2026-06-06` | 1 |
| `api+St Mary Ottawa Holy Pascha PDF cross-check 2026-06-06` | 1 |
| `St Mary Ottawa Holy Pascha PDF cross-check 2026-06-06` | 1 |

### Wednesday Day provenance

For `day=Wednesday`:

| Source marker | Rows |
|---|---:|
| `St Mary Ottawa Holy Pascha book correction 2026-06-14` | 17 |
| `api` | 5 |

Those five remaining `api` rows in Wednesday Day are:

```text
Wednesday First Hour OT4 Wis 1:20-2:15
Wednesday First Hour OT5 Wis 3:12-24
Wednesday Third Hour OT3 Prov 4:4-5:4
Wednesday Ninth Hour OT4 Isa 59:1-17
Wednesday Ninth Hour OT5 Zech 11:11-14
```

### Wednesday Eve provenance

For `day=Wednesday Eve`:

| Source marker | Rows |
|---|---:|
| `api` | 8 |
| `St Mary Ottawa Holy Pascha source-text correction 2026-06-06` | 2 |

### Source independence conclusion

The stored Pascha data was not built from the local Katameros SQLite. It is a curated/generated Pascha table with many `api` rows and later St. Mary Ottawa corrections.

The repo does not contain a committed Coptic Reader extraction artifact. Phase 1 recovered Coptic Reader app runtime/asset discovery from transcripts, but the current stored rows cite `api`, `book`, and St. Mary Ottawa correction markers, not Coptic Reader.

Therefore:

- Stored-vs-live-Katameros comparison is partly a consistency check for the original `api` source rows.
- Stored-vs-St. Mary is a comparison against an independent St. Mary Ottawa source-text extraction layer.
- Stored-vs-Coptic-Reader-fixture is the controlling comparison for Wednesday Day in this pass.

## 7. Phase 2a Great Lent conflict re-check: `Id=46` vs `Id=53`

Question: Was dropping `GreatLentReadings.Id=53`'s composite Matins Psalm (`Ps 63:1 + Ps 64:2-4`) correct?

Best external source available in this phase: live Katameros API for real dates corresponding to **Thursday of the 7th week of Great Lent**.

Probed:

```bash
curl -L -sS --fail 'https://api.katameros.app/readings/gregorian/10-04-2025?languageId=2'
curl -L -sS --fail 'https://api.katameros.app/readings/gregorian/02-04-2026?languageId=2'
```

Both returned annual/Great Lent Matins/Liturgy structure with Matins Psalm:

| Date | Matins Psalm from live API | Contains `Ps 64:2-4`? |
|---|---|---:|
| 2025-04-10 | `Ps 63:1` | No |
| 2026-04-02 | `Ps 63:1` | No |

Live API also returned the same Matins Gospel and Liturgy readings as the retained row family:

```text
Matins Prophecies: Prov 11:13-26; Isa 65:8-16; Job 42:1-6; 2Kgs 6:8-7:20
Matins Psalm/Gospel: Ps 63:1; Matt 20:20-28
Liturgy: 2Cor 4:5-18; 1Jn 3:13-24; Acts 25:23-27; Acts 26:1-6; Ps 122:1-2; Mark 12:18-27
```

Conclusion: Phase 2a's choice to keep `Id=46` and drop `Id=53` is supported by live Katameros API. The concern was valid because composites are normal, but in this specific case the best external source checked does **not** include `Ps 64:2-4`.

## 8. Audit of existing Pascha verifier checks

File audited:

```text
verify_lectionary_queries.py
```

Important: current passing verifier output is **not** evidence of Coptic Reader correctness for Wednesday Day. Several checks encode old expectations.

| Check | Touches Pascha/Holy Week? | Conflict with Coptic Reader Day fixture? | Rewrite needed? |
|---|---|---|---|
| `assert_required_pascha_genesis_rows()` | Yes. Queries multiple Pascha day/hour rows, including Wednesday Sixth/Ninth. | Yes. It expects Wednesday Sixth `Job 27:16-20; Job 28:1-2` as OT3, while fixture has named non-versed `Memoirs of Job`; expects Wednesday Ninth `Isa 59:1-17` and `Zech 11:11-14`, omitted by fixture; indirectly preserves old Psalm boundary expectations. | Yes |
| `assert_known_good()` | Yes. Many Pascha known-good checks and source-text/crosswalk checks. | Partial. `pascha_wednesday_eve_eleventh` validates a Wednesday Eve St. Mary row, not Wednesday Day; `source_text_wisdom_*` checks validate source-text expectations, not Coptic Reader fixture correctness. | Partial rewrite/scope split |
| `assert_pascha_source_text_fully_parsed()` | Yes. Checks St. Mary source-text parse completeness. | No direct fixture content claim, but it can pass while source text conflicts with Coptic Reader fixture. | Keep as parse-only, relabel so it is not treated as correctness evidence |
| `assert_pascha_source_text_dedupe_invariants()` | Yes. Dedupe invariant between source text and day-hour rows. | Yes. It hard-codes `Ps 83:2,83:5` and `Jn 12:1-8` as bad Wednesday source-text rows if duplicated. The fixture includes those Sixth Hour readings. | Yes |
| `assert_wednesday_pascha_day_hour_corrections()` | Yes. Exact expected set for Wednesday Pascha Day. | Yes. It expects extra First Hour Wisdom readings, Third Hour Proverbs, Sixth Hour Job verses instead of `Memoirs of Job`, Ninth Hour Isaiah/Zechariah, `Ps 41:5-6`, and `Ps 69:17`. Fixture differs. | Yes, highest priority |
| `assert_artifacts_exist()` | Includes Pascha artifacts. | No content expectation. | No, unless fixture artifacts are added to required list in a later approved phase |
| `assert_four_maccabees_local_absence_documented()` | Searches Pascha files among others for `4 Maccabees`. | No Wednesday fixture conflict. | No |
| `assert_malformed_refs_accounted_for()` | Includes reverse crosswalk, which contains Pascha rows. | No direct fixture content expectation. | No |
| `assert_no_duplicate_reading_tuples()` | Includes reverse lookup and cycle passage indexes; not Pascha-specific but scans Pascha crosswalk rows. | No direct fixture conflict. | No |
| `assert_chapter_occurrence_label_columns()` / `assert_chapter_occurrence_row_count()` | Generated occurrence rows include Pascha rows. | No direct fixture content expectation, but row-count checks will change when approved Pascha fixes are applied. | Later update after approved data changes |

Highest-risk checks before Phase 2b-2/2c edits:

1. `assert_wednesday_pascha_day_hour_corrections()`
2. `assert_pascha_source_text_dedupe_invariants()`
3. `assert_required_pascha_genesis_rows()`
4. Relevant parts of `assert_known_good()`

## 9. Measurement commands / artifacts

Temporary analysis artifacts, not committed:

```text
/tmp/coptic_phase2b/katameros_16-04-2025.json
/tmp/coptic_phase2b/katameros_08-04-2026.json
/tmp/coptic_phase2b/katameros_10-04-2025.json
/tmp/coptic_phase2b/katameros_02-04-2026.json
/tmp/coptic_phase2b/phase2b_measurement.json
/tmp/coptic_phase2b/phase2b_measurement_corrected.json
```

Read-only commands/probes used:

```bash
curl -L -sS --fail --max-time 30 'https://api.katameros.app/readings/gregorian/16-04-2025?languageId=2'
curl -L -sS --fail --max-time 30 'https://api.katameros.app/readings/gregorian/08-04-2026?languageId=2'
curl -L -sS --fail --max-time 30 'https://api.katameros.app/readings/gregorian/10-04-2025?languageId=2'
curl -L -sS --fail --max-time 30 'https://api.katameros.app/readings/gregorian/02-04-2026?languageId=2'
```

SQLite schema check was read-only against:

```text
sources/katameros-api/Core/KatamerosDatabase.db
```

## 10. Bottom line / recommended next gate

Do not proceed as if this is only an Eve/Day shift. Wednesday Day is already the better matching label.

Do not use current verifier pass/fail as correctness proof for Wednesday Day. The checks need to be rewritten around the Coptic Reader fixture before any final data-fix phase.

For the next approved phase, the clean sequence is:

1. Decide whether Coptic Reader fixture overrides source-text/API for all mismatches listed here.
2. Rewrite verifier expectations against `tests/fixtures/pascha_wednesday_day_coptic_reader.json`.
3. Apply only approved Wednesday Day data changes.
4. Re-run source scoring and verifier.
5. Only then decide whether to gather more Coptic Reader fixtures for the rest of Holy Week.
