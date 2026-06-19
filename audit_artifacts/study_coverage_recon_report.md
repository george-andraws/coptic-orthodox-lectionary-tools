# Study Coverage Recon Report

Generated: 2026-06-19 13:29:20

## A1. Existing crosswalk and index artifacts

| Path | Rows or entries | Key | Shape | Freshness |
|---|---:|---|---|---|
| `out/data/reverse_lookup_crosswalk.csv` | 66348 | passage plus source row fields; verse-range rows | passage, source_kind, source_family, source_table, source_file, source_row_id, source_order, source_token_order, superseded_by_ref, superseded_reason, liturgical_place, calendar_key ... | existing generated artifact in working tree |
| `out/data/bible_chapter_lectionary_occurrences.csv` | 71195 | chapter_ref and passage occurrence rows | testament, book, book_abbrev, chapter, chapter_ref, passage, source_kind, liturgical_place, calendar_key, gregorian_date, coptic_date, day_title ... | existing generated artifact in working tree |
| `out/design/affected_passages.csv` | 2791 | book, chapter, affected_passage | book, chapter, affected_passage, change_count, change_types, commits | existing generated artifact in working tree |
| `out/design/reverse_lectionary_index.jsonl` | 11923 | identity_key plus placement fields | jsonl keys: attestation_year_max, attestation_year_min, attestation_years, authority_tier, calendar_keys, canonical_lxx_ref, canonical_mt_ref, collapsed_row_count, current_status, day_titles, display_ref, hour_theme, identity_key, occasion, occasion_kind, provenance, reading_name, reading_type, removed_marker, service_hour, service_section, slot, slot_order, slot_type, source_disclosure, source_disclosure_count, source_edition, source_family, source_kind, source_locator, source_title, spans_json | existing generated artifact in working tree |
| `out/design/daily/lectionary-2020.json` | 360 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2021.json` | 359 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2022.json` | 359 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2023.json` | 359 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2024.json` | 360 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2025.json` | 359 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2026.json` | 360 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2027.json` | 359 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2028.json` | 360 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2029.json` | 360 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2030.json` | 359 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2031.json` | 360 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2032.json` | 360 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2033.json` | 359 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2034.json` | 360 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |
| `out/design/daily/lectionary-2035.json` | 359 | Gregorian date | JSON object keyed by Gregorian date | existing generated artifact in working tree |

Package contents checked: `packages/lectionary-data` contains `package.json`, `meta.json`, `index.js`, `README.md`, `LICENSE`, `data/reverse_lectionary_index.jsonl`, daily JSON files for 2026, 2027, and 2028, plus the local tarball. The shipped reverse index has 11,923 JSONL rows.

Conclusion: a passage to occasions reverse lookup already exists and is complete enough to drive a per-study join. This run extended nothing and rebuilt nothing in the lectionary dataset.

## A2. Bible-study frontmatter reality

Studies parsed from active OT/Deuterocanon and NT folders: 843. Excluded archives, audits, indexes, resources, assets, and superseded notes.

| Field | Populated | Blank | Examples |
|---|---:|---:|---|
| `passages` | 843 | 0 | Matthew 5 17-26 The Law Fulfilled and the Heart Reconciled.md: ['Matthew 5:17-26']; Matthew 6 1-18 Secret Almsgiving, Prayer, and Fasting.md: ['Matthew 6:1-18']; Matthew 8 1-17 The King Who Cleanses and Heals.md: ['Matthew 8:1-17'] |
| `lectionary` | 314 | 529 | Matthew 5 17-26 The Law Fulfilled and the Heart Reconciled.md: Matthew 5:17-24 is appointed as the Matins Gospel for Wednesday of the second week of Great Lent in checked rows; Matthew 5:25-37 is appointed as the Matins Gospel for Saturday of the first week of Great Lent in checked rows, so Matthew 5:25-26 overlaps that reading.; Matthew 6 1-18 Secret Almsgiving, Prayer, and Fasting.md: Matthew 6:1-18 is appointed as the Liturgy Gospel for the Sunday of the week before Great Lent. Matthew 6:14-18 also appears as the Gospel for the seventh prayer in the Unction of the Sick.; Matthew 8 1-17 The King Who Cleanses and Heals.md: Matthew 8:5-13 appears repeatedly in checked Coptic lectionary sources, including fixed-day Vespers readings and Matins on the third Sunday of Tout; no ordinary reading surfaced for Matthew 8:1-4 or Matthew 8:14-17 in the checked sources. |
| `season` | 3 | 840 | Wisdom of Solomon 2 - The Righteous Son Condemned.md: Holy Pascha; Lamentations 3 - Mercy in the middle of affliction.md: Holy Pascha; Lamentations 1 - Lonely Jerusalem.md: Holy Pascha |
| `feast` | 3 | 840 | Wisdom of Solomon 2 - The Righteous Son Condemned.md: Good Friday; Lamentations 3 - Mercy in the middle of affliction.md: Good Friday; Lamentations 1 - Lonely Jerusalem.md: Hosanna Sunday |

Passage granularity distribution:

| Granularity | Count | Examples |
|---|---:|---|
| verse_range | 97 | Matthew 5:17-26; Matthew 6:1-18; Matthew 8:1-17; Matthew 13:44-52; Matthew 4:1-11 |
| whole_chapter_or_chapter_range | 1089 | 1 Kings 1; 1 Kings 2; 1 Kings 9; 1 Kings 10; 1 Kings 11 |

Representative full-frontmatter examples:

### psalm: `Hermes/04-Reference/Coptic Orthodox Lessons/References/Biblical Explanations/Kings Bible Study Project/025 - Psalms/Psalm 86 (LXX 85) - Incline Thine Ear O Lord.md`

```yaml
title: Psalm 86 (LXX 85) - Incline Thine Ear O Lord
created: 2026-05-26T22:31:06Z
book: Psalms
psalm_nkjv: 86
psalm_lxx: 85
accepted_author: A Prayer of David.
period: >-
messianic_status: >-
lectionary: >-
tags: ["biblical-explanation", "bible-study", "psalms", "David", "prayer", "mercy", "nations", "coptic-lectionary", "lxx-numbering"]
publish: true
type: chapter-study
audience: ["parish", "servant"]
summary: Psalm 86 is the prayer of a poor and needy servant who lifts up his soul to the Lord.
date: 2026-05-26
updated: 2026-05-29
passages: ["Psalm 86"]
fathers: ["Augustine of Hippo", "Theodoret of Cyrus"]
audio: []
```

### pentateuch: `Hermes/04-Reference/Coptic Orthodox Lessons/References/Biblical Explanations/Kings Bible Study Project/001 - Genesis/Genesis 20-21 - Abimelech Isaac Born and Hagar Comforted.md`

```yaml
title: Genesis 20-21 - Abimelech Isaac Born and Hagar Comforted
publish: true
type: chapter-study
book: Genesis
audience: ["parish", "servant"]
summary: Genesis 20-21 shows God protecting Sarah, fulfilling the birth of Isaac, and hearing Hagar and Ishmael in the wilderness. The study holds covenant promise and compassion together, revealing a God who guards His word while caring for the vulnerable.
date: 2026-05-29
updated: 2026-06-08
audio: []
tags: []
passages: ["Genesis 20", "Genesis 21"]
fathers: ["John Chrysostom", "Ephrem the Syrian", "Augustine of Hippo", "Isaac the Syrian", "Pope Shenouda III", "Fr. Bishoy Kamel"]
```

### major_prophet: `Hermes/04-Reference/Coptic Orthodox Lessons/References/Biblical Explanations/Kings Bible Study Project/032 - Isaiah/Isaiah 49 - Servant Light to the Nations and Zion Remembered.md`

```yaml
title: Isaiah 49 - Servant Light to the Nations and Zion Remembered
created: 2026-05-28
last_revised: 2026-06-05
updated: 2026-06-05
book: Isaiah
chapters: 49
series: Orthodox Bible Study Guides
status: revised-source-text
tags: ["biblical-explanation", "bible-study", "isaiah", "prophecy", "servant", "gentiles", "zion", "church"]
publish: true
type: chapter-study
audience: ["parish", "servant"]
summary: Revision note: This standalone guide was created by splitting the former combined Isaiah 49-50 - Servant Mission and Obedience guide.
date: 2026-05-28
passages: ["Isaiah 49"]
fathers: ["Gregory of Nazianzus", "Cyril of Alexandria", "Cyril of Jerusalem", "Ephrem the Syrian", "John Cassian", "Jerome", "Ambrose of Milan"]
```

### deuterocanon: `Hermes/04-Reference/Coptic Orthodox Lessons/References/Biblical Explanations/Kings Bible Study Project/030 - Wisdom of Solomon/Wisdom of Solomon 2 - The Righteous Son Condemned.md`

```yaml
title: Wisdom of Solomon 2 - The Righteous Son Condemned
type: chapter-study
project: Old Testament Orthodox Bible Study Guides
series: Wisdom of Solomon Bible Study Project
series_order: 2
book: Wisdom of Solomon
passages: ["Wisdom of Solomon 2"]
audience: ["parish", "servant"]
publish: true
status: revised
date: 2026-06-03
updated: 2026-06-04
audio: []
translation_basis: Brenton Septuagint
lectionary: In checked Coptic Holy Pascha source material, Wisdom 2:12-22 appears at Good Friday First Hour.
season: Holy Pascha
feast: Good Friday
summary: Wisdom 2 exposes the reasoning of the ungodly and is fulfilled most fully in Christ, the righteous Son mocked, tested, condemned to shameful death, and vindicated by the Father.
fathers: ["John Chrysostom"]
tags: ["biblical-explanation", "orthodox-scripture", "bible-study", "deuterocanon", "septuagint", "wisdom-literature", "holy-pascha", "good-friday", "passion-of-christ"]
```

### nt: `Hermes/04-Reference/Coptic Orthodox Lessons/References/Biblical Explanations/New Testament Bible Study Project/001 - Matthew/Matthew 5 17-26 The Law Fulfilled and the Heart Reconciled.md`

```yaml
title: Matthew 5 17-26 The Law Fulfilled and the Heart Reconciled
type: chapter-study
project: New Testament Orthodox Bible Study Guides
book: Matthew
passages: ["Matthew 5:17-26"]
audience: ["parish", "servant"]
status: draft
publish: true
date: 2026-06-12
updated: 2026-06-12
tags: ["biblical-explanation", "orthodox-scripture", "bible-study", "matthew", "gospel"]
fathers: ["John Chrysostom"]
lectionary: Matthew 5:17-24 is appointed as the Matins Gospel for Wednesday of the second week of Great Lent in checked rows; Matthew 5:25-37 is appointed as the Matins Gospel for Saturday of the first week of Great Lent in checked rows, so Matthew 5:25-26 overlaps that reading.
summary: Matthew 5:17-26 shows Christ fulfilling the Law by bringing righteousness from external restraint into healed anger, reconciled worship, and love that makes peace quickly.
```

## A3. Why source fields in the lectionary data

The placement data carries `hour_theme` on some rows. It does not carry a populated placement-level `homily_ref` or equivalent patristic homily reference field in the reverse index. Prior audit notes state patristic homily slugs are site-side joins, not present in this repo.

Real Genesis 24:1-9 placement record located:

```json
{
  "attestation_year_max": "",
  "attestation_year_min": "",
  "attestation_years": "",
  "authority_tier": "working_local_source",
  "calendar_keys": "Wednesday | Ninth Hour",
  "canonical_lxx_ref": "Gen 24:1-9",
  "canonical_mt_ref": "Gen 24:1-9",
  "collapsed_row_count": "1",
  "current_status": "current_confirmed_by_fixture_equivalence",
  "day_titles": "Wednesday",
  "display_ref": "Gen 24:1-9",
  "hour_theme": "the saving death of Christ and repentance",
  "identity_key": "rid_70dcf815719cbba3ec68",
  "occasion": "Wednesday",
  "occasion_kind": "specific",
  "provenance": "St Mary Ottawa Holy Pascha book correction 2026-06-14",
  "reading_name": "",
  "reading_type": "scripture",
  "removed_marker": "",
  "service_hour": "Ninth Hour",
  "service_section": "Ninth Hour",
  "slot": "OT1",
  "slot_order": 1,
  "slot_type": "prophecy",
  "source_disclosure": "[{\"source_family\":\"holy_pascha_curated_day_hour\",\"source_kind\":\"pascha_day_hour\",\"source_edition\":\"local repo snapshot of pierresaid Katameros API SQLite database\",\"source_title\":\"pierresaid Katameros API SQLite source bundled in repo\",\"source_locator\":\"out/data/pascha_day_hour_index.csv:row 70; source_ref=Gen 24:1-9\"}]",
  "source_disclosure_count": "1",
  "source_edition": "local repo snapshot of pierresaid Katameros API SQLite database",
  "source_family": "holy_pascha_curated_day_hour",
  "source_kind": "pascha_day_hour",
  "source_locator": "out/data/pascha_day_hour_index.csv:row 70; source_ref=Gen 24:1-9",
  "source_title": "pierresaid Katameros API SQLite source bundled in repo",
  "spans_json": "[{\"book\": \"Gen\", \"canonical_lxx_ref\": \"Gen 24:1-9\", \"canonical_mt_ref\": \"Gen 24:1-9\", \"chapter_end\": 24, \"chapter_start\": 24, \"confidence\": \"high\", \"source_convention\": \"modern_english_reference\", \"source_ref\": \"Gen 24:1-9\", \"validation_basis\": \"\", \"verse_end\": 9, \"verse_start\": 1}]"
}
```

## A4. Occasion and bridge metadata

The reverse placement rows carry `occasion`, `service_section`, `service_hour`, `slot`, `current_status`, and source attestation fields. The Synaxarium bridge carries `commemoration_title`, `commemoration_type`, `basis`, and `confidence`, keyed by `reading_identity_key` plus Coptic day. The literal fields `occasion_short_label`, `collection_type`, and `bridge_basis` are not stored under those names and were derived for coverage output.

Coverage bridge-basis distribution:

| basis | rows |
|---|---:|
| missing | 3248 |
| collection-type | 2767 |
| explicit | 526 |

Coverage derived collection_type distribution, top 30:

| collection_type | rows |
|---|---:|
| blank | 5988 |
| foundational-40-amshir-02 | 22 |
| foundational-54-abib-03 | 22 |
| foundational-07-tut-19 | 21 |
| foundational-01-tut-01 | 20 |
| foundational-55-abib-05 | 19 |
| foundational-02-tut-02 | 18 |
| foundational-51-baunah-02 | 18 |
| foundational-09-tut-26 | 15 |
| foundational-13-babah-27 | 15 |
| foundational-65-al-nasi-01 | 14 |
| foundational-56-abib-20 | 13 |
| foundational-08-tut-21 | 12 |
| foundational-53-baunah-30 | 12 |
| foundational-66-al-nasi-02 | 12 |
| foundational-52-baunah-16 | 12 |
| foundational-49-bashans-24 | 11 |
| foundational-18-hatur-17 | 11 |
| foundational-12-babah-22 | 10 |
| foundational-22-hatur-27 | 10 |
| foundational-68-al-nasi-04 | 10 |
| foundational-10-babah-12 | 10 |
| foundational-30-tubah-03 | 10 |
| foundational-03-tut-08 | 10 |
| foundational-06-tut-18 | 10 |
| foundational-24-hatur-29 | 9 |
| foundational-29-tubah-01 | 9 |
| foundational-38-tubah-26 | 9 |
| foundational-31-tubah-04 | 9 |
| foundational-46-bashans-01 | 8 |

Season vocabulary as instantiated in coverage:

| season | rows |
|---|---:|
| Annual / fixed or ordinary cycle | 4718 |
| Great Lent | 625 |
| Holy Fifty Days | 532 |
| Pascha / Holy Week | 440 |
| Agpeya | 140 |
| Special service | 86 |

Bridge source table basis distribution:

| basis | rows |
|---|---:|
| collection-type | 3899 |
| explicit | 789 |

Bridge commemoration type distribution:

| type | rows |
|---|---:|
| martyr | 1416 |
| departure | 1103 |
| patriarch | 740 |
| commemoration | 527 |
| hierarch | 220 |
| theotokos | 201 |
| lord_feast | 189 |
| angel | 155 |
| apostle | 69 |
| prophet | 32 |
| feast | 24 |
| ascetic | 12 |

The 69 collection vocabulary is stored in `out/design/foundational_reading_collections_69.csv` and has 69 rows.

## A5. Field-gap finding

| Field | Current support | Gap |
|---|---|---|
| occasion_short_label | derivable from Synaxarium bridge `commemoration_title` or placement `occasion` | not stored as a first-class placement field |
| collection_type | derivable only when placement day matches `foundational_reading_collections_69` | no first-class field on placement rows |
| collection-level why field | source article/spec explains class-level basis | no machine field per collection |
| placement-level why field | `hour_theme` exists on some rows | no populated homily or why-link field per placement |
## B and C outputs

- `out/study_lectionary_coverage.csv` (2399583 bytes)
- `out/study_coverage_rollup.csv` (104206 bytes)
- `out/lectionary_gap_no_study.csv` (803757 bytes)
- `out/why_flags.csv` (2872807 bytes)
- `out/why_source_map.md` (4856 bytes)

Row counts:

- `study_lectionary_coverage.csv`: 6541
- `study_coverage_rollup.csv`: 843
- `lectionary_gap_no_study.csv`: 3016
- `why_flags.csv`: 8207

## Determinism and audit notes

The join used existing `reading_identity.csv`, `reverse_lectionary_index.jsonl`, `reverse_lookup_crosswalk.csv`, and `bible_chapter_lectionary_occurrences.csv`. No Bible-study note was edited. No lectionary source row was changed. No thematic commentary was authored.

