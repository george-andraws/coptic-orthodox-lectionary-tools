# Pascha Source Pack

Purpose: structured source material for later authoring of the `In the Church's Worship` Pascha sections. This file collects and labels source material only; it does not author final explanatory prose.

## Source inventory

- source: `local_pascha_day_hour_index`
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - provenance: `out/data/pascha_day_hour_index.csv`
  - use: readings and hour slot data
- source: `st_mary_ottawa_source_text_index`
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - provenance: `out/data/pascha_source_text_index.csv` and `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt`
  - use: source-text witness with line and page locators
- source: `treasures_holy_pascha`
  - author: St Paul Brotherhood, prepared by Fr John Paul, prefaced by Bishop Serapion
  - copyright_status: modern_copyrighted / translation_copyrighted
  - provenance: `Treasures of the Fathers of the Church: The Holy Pascha` saved extracted text; source URL https://copticvault.wordpress.com/2024/04/26/treasures-of-the-fathers-of-the-church-volume-3-the-holy-pascha/
  - use: day/hour introductions and patristic layer
- source: `fr_matthew_holy_week`
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - provenance: https://coptictreasuresenglish.wordpress.com/category/father-matthew-the-poor/holy-week/book-reflections-on-holy-week/
  - use: category index crawled with curl; article pages crawled: 9

## Build counts

- day_hour_entries_built: 53
- fr_matthew_articles_crawled: 9
- blank_theme_coverage_rows_scoped_to_study_coverage: 30

## Day-hour entries

### Palm Sunday | Vespers

- hour_theme_from_data: evening thanksgiving and watchfulness
- source_count: 3
- sources_used: `local_pascha_day_hour_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot Psalm; refs Ps 118:26-27; data_source api
  - order 2; slot Gospel; refs John 12:1-11; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `evening thanksgiving and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Palm Sunday as the King entering Jerusalem and receiving Hosanna praise. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 4, Palm Sunday, "Behold Your King", printed page 45, extracted text line 1966.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew presents Palm Sunday as the public revelation of Christ as peaceful King after Lazarus is raised. Article: The Gospel of Palm Sunday (The Sunday of Salvation); URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-gospel-of-palm-sunday-the-sunday-of-salvation/.

#### Per-reading anchors

- reading: Ps 118:26-27
  - slot: Psalm
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot Psalm, for Palm Sunday Vespers.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 2566; nearby named Fathers: Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Augustine
- reading: John 12:1-11
  - slot: Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Gospel, for Palm Sunday Vespers.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 2034; nearby named Fathers: no named Father surfaced in the nearby window.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Palm Sunday | Matins

- hour_theme_from_data: awakening to praise and repentance
- source_count: 3
- sources_used: `local_pascha_day_hour_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot Psalm; refs Ps 68:19,35; data_source api
  - order 2; slot Gospel; refs Luke 19:1-10; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `awakening to praise and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Palm Sunday as the King entering Jerusalem and receiving Hosanna praise. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 4, Palm Sunday, "Behold Your King", printed page 45, extracted text line 1966.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew presents Palm Sunday as the public revelation of Christ as peaceful King after Lazarus is raised. Article: The Gospel of Palm Sunday (The Sunday of Salvation); URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-gospel-of-palm-sunday-the-sunday-of-salvation/.

#### Per-reading anchors

- reading: Ps 68:19,35
  - slot: Psalm
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot Psalm, for Palm Sunday Matins.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 19:1-10
  - slot: Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Gospel, for Palm Sunday Matins.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 2242; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine

### Palm Sunday | Liturgy

- hour_theme_from_data: the Eucharistic gathering of the Church
- source_count: 3
- sources_used: `local_pascha_day_hour_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot Pauline; refs Heb 9:11-28; data_source api
  - order 2; slot Catholic; refs 1Pet 4:1-11; data_source api
  - order 3; slot Acts; refs Acts 28:11-31; data_source api
  - order 4; slot Psalm+Gospel; refs Ps 80:3,1,2; Matt 21:1-17; Mark 11:1-11; Luke 19:29-48; Ps 64:1,2; John 12:12-19; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Eucharistic gathering of the Church` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Palm Sunday as the King entering Jerusalem and receiving Hosanna praise. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 4, Palm Sunday, "Behold Your King", printed page 45, extracted text line 1966.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew presents Palm Sunday as the public revelation of Christ as peaceful King after Lazarus is raised. Article: The Gospel of Palm Sunday (The Sunday of Salvation); URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-gospel-of-palm-sunday-the-sunday-of-salvation/.

#### Per-reading anchors

- reading: Heb 9:11-28
  - slot: Pauline
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot Pauline, for Palm Sunday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: 1Pet 4:1-11
  - slot: Catholic
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Catholic, for Palm Sunday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Acts 28:11-31
  - slot: Acts
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Acts, for Palm Sunday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 80:3,1,2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Palm Sunday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Matt 21:1-17
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Palm Sunday Liturgy.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 3235; nearby named Fathers: Cyril, Origen, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Origen; Augustine; Ambrose
- reading: Mark 11:1-11
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Palm Sunday Liturgy.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 2584; nearby named Fathers: Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Augustine
- reading: Luke 19:29-48
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Palm Sunday Liturgy.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 2242; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine
- reading: Ps 64:1,2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Palm Sunday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 12:12-19
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Palm Sunday Liturgy.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 2034; nearby named Fathers: no named Father surfaced in the nearby window.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Hosanna Sunday | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot Psalm+Gospel; refs Ps 8:2,3; Matt 21:10-17; data_source book

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 4 readings for this hour; pages 57, 58, 60; refs include Lam 1:1-4; Zeph 3:11-20; Ps 8:2-3; Matt 21:10-17.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Hosanna Sunday around the King entering Jerusalem and the cry for salvation. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 4, Palm Sunday, "Behold Your King", printed page 45, extracted text line 1966.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew presents Hosanna as the cry for salvation to the King who enters Jerusalem in humility. Article: The Gospel of Palm Sunday (The Sunday of Salvation); URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-gospel-of-palm-sunday-the-sunday-of-salvation/.

#### Per-reading anchors

- reading: Ps 8:2,3
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot Psalm+Gospel, for Hosanna Sunday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 3235; nearby named Fathers: Cyril, Origen, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Origen; Augustine; Ambrose
- reading: Matt 21:10-17
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot Psalm+Gospel, for Hosanna Sunday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 3235; nearby named Fathers: Cyril, Origen, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Origen; Augustine; Ambrose

### Hosanna Sunday | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot Psalm+Gospel; refs Ps 22:22-23; Matt 20:20-28; data_source book

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 4 readings for this hour; pages 64, 66, 68; refs include Isa 48:12-22; Nah 1:2-8; Ps 22:22-23; Matt 20:20-28.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Hosanna Sunday around the King entering Jerusalem and the cry for salvation. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 4, Palm Sunday, "Behold Your King", printed page 45, extracted text line 1966.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew presents Hosanna as the cry for salvation to the King who enters Jerusalem in humility. Article: The Gospel of Palm Sunday (The Sunday of Salvation); URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-gospel-of-palm-sunday-the-sunday-of-salvation/.

#### Per-reading anchors

- reading: Ps 22:22-23
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot Psalm+Gospel, for Hosanna Sunday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 3664; nearby named Fathers: Augustine, Theodoret.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 27:35; Matthew 27:46; John 19:24
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Augustine; Theodoret
- reading: Matt 20:20-28
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot Psalm+Gospel, for Hosanna Sunday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 2242; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine

### Monday Eve | First Hour

- hour_theme_from_data: the beginning of the day and watchfulness
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Zech 1:1-6; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 62:7,6; Luke 13:23-30; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the beginning of the day and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 73, 76; refs include Zeph 1:2-12; Ps 27:6-7; Jn 12:20-36.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents this eve as preparation for the Lord revealing His Passion. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 5, Eve of Holy Monday, "He Prepares Them", printed page 81, extracted text line 3903.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Holy Week supplies the broad setting of Pascha as crossing over through the Lamb and His voluntary love. Article: Reflections on Holy Week; URL: https://coptictreasuresenglish.wordpress.com/2018/04/01/reflections-on-holy-week/.

#### Per-reading anchors

- reading: Zech 1:1-6
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Eve First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 62:7,6
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 13:23-30
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Monday Eve | Third Hour

- hour_theme_from_data: the descent of the Holy Spirit and the trial of the heart
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Mal 1:1-9; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 13:3,5; Luke 13:31-35; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the descent of the Holy Spirit and the trial of the heart` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 80, 82, 83; refs include Zeph 1:14-2:2; Ps 28:2,28:9; Lk 9:18-22.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents this eve as preparation for the Lord revealing His Passion. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 5, Eve of Holy Monday, "He Prepares Them", printed page 81, extracted text line 3903.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Holy Week supplies the broad setting of Pascha as crossing over through the Lamb and His voluntary love. Article: Reflections on Holy Week; URL: https://coptictreasuresenglish.wordpress.com/2018/04/01/reflections-on-holy-week/.

#### Per-reading anchors

- reading: Mal 1:1-9
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Eve Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 13:3,5
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 13:31-35
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Monday Eve | Sixth Hour

- hour_theme_from_data: the Cross and the Lord's willing suffering
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Hos 4:15-19; Hos 5:1-7; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 91:2,3; John 21:34-38; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Cross and the Lord's willing suffering` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 86, 88, 89; refs include Joel 1:5-15; Ps 29:1-2; Mark 10:32-34.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents this eve as preparation for the Lord revealing His Passion. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 5, Eve of Holy Monday, "He Prepares Them", printed page 81, extracted text line 3903.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Holy Week supplies the broad setting of Pascha as crossing over through the Lamb and His voluntary love. Article: Reflections on Holy Week; URL: https://coptictreasuresenglish.wordpress.com/2018/04/01/reflections-on-holy-week/.

#### Per-reading anchors

- reading: Hos 4:15-19
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Hos 5:1-7
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 91:2,3
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 21:34-38
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Monday Eve | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Hos 10:12-15; Hos 11:1-2; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 33:10,11; Luke 11:37-52; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 92, 95; refs include Mic 2:3-10; Ps 8:1-2; Mark 8:27-33.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents this eve as preparation for the Lord revealing His Passion. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 5, Eve of Holy Monday, "He Prepares Them", printed page 81, extracted text line 3903.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Holy Week supplies the broad setting of Pascha as crossing over through the Lamb and His voluntary love. Article: Reflections on Holy Week; URL: https://coptictreasuresenglish.wordpress.com/2018/04/01/reflections-on-holy-week/.

#### Per-reading anchors

- reading: Hos 10:12-15
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Eve Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Hos 11:1-2
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Eve Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 33:10,11
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4574; nearby named Fathers: Cyril, Chrysostom, Ambrose, Irenaeus, Hippolytus.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Ambrose; Irenaeus; Hippolytus
- reading: Luke 11:37-52
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Monday Eve | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Amos 5:6-14; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 122:4; Mark 13:32-37; Mark 14:1-2; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 101, 99; refs include Mic 3:1-4; Ps 18:17-18; Matt 17:19-23.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents this eve as preparation for the Lord revealing His Passion. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 5, Eve of Holy Monday, "He Prepares Them", printed page 81, extracted text line 3903.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Holy Week supplies the broad setting of Pascha as crossing over through the Lamb and His voluntary love. Article: Reflections on Holy Week; URL: https://coptictreasuresenglish.wordpress.com/2018/04/01/reflections-on-holy-week/.

#### Per-reading anchors

- reading: Amos 5:6-14
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Eve Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 122:4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Mark 13:32-37
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Mark 14:1-2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Monday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 3910; nearby named Fathers: Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyprian

### Monday | First Hour

- hour_theme_from_data: the beginning of the day and watchfulness
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Gen 1:1-31; Gen 2:1-3; data_source api
  - order 2; slot OT2; refs Isa 5:1-9; data_source api
  - order 3; slot OT3; refs Ps 72:1-19; data_source api
  - order 4; slot Psalm+Gospel; refs Ps 72:18-19; Mark 11:12-24; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the beginning of the day and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 5 readings for this hour; pages 106, 109, 111, 115; refs include Gen 1:1-2:3; Isa 5:1-9; Sir 1:1-14; Ps 71:18-19; Mark 11:12-24.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents Holy Monday through the Tree of Life and the barren fig tree warning. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 6, Holy Monday, "The Tree of Life", printed page 99, extracted text line 4806.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew reads Holy Monday through the barren fig tree, external leaves without fruit, and judgment on fruitless religion. Article: The Homily of Monday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-homily-of-monday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Gen 1:1-31
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4853; nearby named Fathers: Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Augustine; Shenouda
- reading: Gen 2:1-3
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4813; nearby named Fathers: Chrysostom, Basil, Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Romans 5:12-19; 1 Corinthians 15:45-49
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 2:23-24
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Chrysostom; Basil; Augustine; Shenouda
- reading: Isa 5:1-9
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Monday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4891; nearby named Fathers: Origen, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Augustine; Shenouda
- reading: Ps 72:1-19
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Monday First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 72:18-19
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Monday First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Mark 11:12-24
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Monday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 5193; nearby named Fathers: Athanasius, Chrysostom, Gregory, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Chrysostom; Gregory; Augustine

### Monday | Third Hour

- hour_theme_from_data: the descent of the Holy Spirit and the trial of the heart
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Isa 5:20-30; data_source api
  - order 2; slot OT2; refs Jer 9:12-19; data_source api
  - order 3; slot Psalm+Gospel; refs Ps 122:1-2; Mark 11:11-19; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the descent of the Holy Spirit and the trial of the heart` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 4 readings for this hour; pages 119, 121, 123; refs include Isa 5:20-30; Jer 9:12-19; Ps 122:1-2; Mark 11:11-19.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents Holy Monday through the Tree of Life and the barren fig tree warning. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 6, Holy Monday, "The Tree of Life", printed page 99, extracted text line 4806.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew reads Holy Monday through the barren fig tree, external leaves without fruit, and judgment on fruitless religion. Article: The Homily of Monday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-homily-of-monday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Isa 5:20-30
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4891; nearby named Fathers: Origen, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Augustine; Shenouda
- reading: Jer 9:12-19
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Monday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4854; nearby named Fathers: Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Augustine; Shenouda
- reading: Ps 122:1-2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Monday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 5709; nearby named Fathers: Chrysostom, Augustine, Jerome, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine; Jerome; Cyprian
- reading: Mark 11:11-19
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Monday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 5193; nearby named Fathers: Athanasius, Chrysostom, Gregory, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Chrysostom; Gregory; Augustine

### Monday | Sixth Hour

- hour_theme_from_data: the Cross and the Lord's willing suffering
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Exod 32:7-15; data_source api
  - order 2; slot OT2; refs Wis 1:1-9; data_source api+St Mary Ottawa Holy Pascha source-text correction 2026-06-06
  - order 3; slot Psalm+Gospel; refs Ps 122:4; John 2:13-17; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Cross and the Lord's willing suffering` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 4 readings for this hour; pages 127, 128, 130, 131; refs include Exod 32:7-15; Wis 1:1-9; Ps 122:4; Jn 2:13-17.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents Holy Monday through the Tree of Life and the barren fig tree warning. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 6, Holy Monday, "The Tree of Life", printed page 99, extracted text line 4806.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew reads Holy Monday through the barren fig tree, external leaves without fruit, and judgment on fruitless religion. Article: The Homily of Monday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-homily-of-monday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Exod 32:7-15
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=1 Corinthians 10:7
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Wis 1:1-9
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Monday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4841; nearby named Fathers: Chrysostom, Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Ephrem the Syrian; Augustine; Shenouda
- reading: Ps 122:4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Monday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 5709; nearby named Fathers: Chrysostom, Augustine, Jerome, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine; Jerome; Cyprian
- reading: John 2:13-17
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Monday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4859; nearby named Fathers: Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Augustine; Shenouda

### Monday | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Gen 2:15-25; Gen 3:1-24; data_source api
  - order 2; slot OT2; refs Isa 40:1-5; data_source api
  - order 3; slot OT3; refs Prov 1:1-9; data_source api
  - order 4; slot Psalm+Gospel; refs Ps 65:5,4; Matt 21:23-27; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 5 readings for this hour; pages 134, 137, 138, 140; refs include Gen 2:15-3:24; Isa 40:1-5; Prov 1:1-9; Ps 65:4-5; Matt 21:23-27.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents Holy Monday through the Tree of Life and the barren fig tree warning. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 6, Holy Monday, "The Tree of Life", printed page 99, extracted text line 4806.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew reads Holy Monday through the barren fig tree, external leaves without fruit, and judgment on fruitless religion. Article: The Homily of Monday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-homily-of-monday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Gen 2:15-25
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4813; nearby named Fathers: Chrysostom, Basil, Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Romans 5:12-19; 1 Corinthians 15:45-49
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 2:23-24
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Chrysostom; Basil; Augustine; Shenouda
- reading: Gen 3:1-24
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4813; nearby named Fathers: Chrysostom, Basil, Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Romans 5:12-19; 1 Corinthians 15:45-49
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 2:23-24
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Chrysostom; Basil; Augustine; Shenouda
- reading: Isa 40:1-5
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Monday Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 3:3; Mark 1:3; Luke 3:4; John 1:23
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=inferred_patristic_cross_reference_to_verify; items=John Chrysostom; Augustine
- reading: Prov 1:1-9
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Monday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4856; nearby named Fathers: Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Augustine; Shenouda
- reading: Ps 65:5,4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Monday Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Matt 21:23-27
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Monday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4859; nearby named Fathers: Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Augustine; Shenouda

### Monday | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Isa 50:1-3; data_source api
  - order 2; slot OT2; refs Wis 2:20-30; data_source api
  - order 3; slot Psalm+Gospel; refs Ps 13:3-4; John 8:51-59; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 4 readings for this hour; pages 147, 148, 151, 152; refs include Isa 50:1-3; Sir 1:18-27; Ps 12:3-4; Jn 8:51-59.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title presents Holy Monday through the Tree of Life and the barren fig tree warning. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 6, Holy Monday, "The Tree of Life", printed page 99, extracted text line 4806.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew reads Holy Monday through the barren fig tree, external leaves without fruit, and judgment on fruitless religion. Article: The Homily of Monday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/02/the-homily-of-monday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Isa 50:1-3
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Monday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6341; nearby named Fathers: Cyril, Chrysostom, Origen, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 26:67; Mark 14:65
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Origen; Augustine; Shenouda
- reading: Wis 2:20-30
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Monday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 5168; nearby named Fathers: Chrysostom, Gregory.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 27:43
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 2:12-20; The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Gregory
- reading: Ps 13:3-4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Monday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 5741; nearby named Fathers: Chrysostom, Augustine, Jerome, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine; Jerome; Cyprian
- reading: John 8:51-59
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Monday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 4859; nearby named Fathers: Ephrem the Syrian, Augustine, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Augustine; Shenouda

### Tuesday Eve | First Hour

- hour_theme_from_data: the beginning of the day and watchfulness
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Zech 1:1-6; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 62:7,6; Luke 13:23-30; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the beginning of the day and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 157, 159, 160; refs include Zech 1:1-6; Ps 62:2,62:7; Lk 13:23-30.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the Judge of the World. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 7, Eve of Holy Tuesday, "The Judge of the World", printed page 131, extracted text line 6498.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Zech 1:1-6
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Eve First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6544; nearby named Fathers: Cyril, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine
- reading: Ps 62:7,6
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 13:23-30
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6522; nearby named Fathers: Cyril, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine

### Tuesday Eve | Third Hour

- hour_theme_from_data: the descent of the Holy Spirit and the trial of the heart
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Mal 1:1-9; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 13:3,5; Luke 13:31-35; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the descent of the Holy Spirit and the trial of the heart` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 163, 165, 166; refs include Mal 1:1-9; Ps 28:2,28:9; Lk 13:31-35.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the Judge of the World. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 7, Eve of Holy Tuesday, "The Judge of the World", printed page 131, extracted text line 6498.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Mal 1:1-9
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Eve Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6730; nearby named Fathers: Chrysostom, Augustine, Cassian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine; Cassian
- reading: Ps 13:3,5
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6564; nearby named Fathers: Cyril, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine
- reading: Luke 13:31-35
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6522; nearby named Fathers: Cyril, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine

### Tuesday Eve | Sixth Hour

- hour_theme_from_data: the Cross and the Lord's willing suffering
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Hos 4:15-19; Hos 5:1-7; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 91:2,3; John 21:34-38; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Cross and the Lord's willing suffering` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 169, 171, 172; refs include Hos 4:15-5:7; Ps 29:1-2; Lk 21:34-38.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the Judge of the World. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 7, Eve of Holy Tuesday, "The Judge of the World", printed page 131, extracted text line 6498.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Hos 4:15-19
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Eve Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6532; nearby named Fathers: Cyril, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine
- reading: Hos 5:1-7
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Eve Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6544; nearby named Fathers: Cyril, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine
- reading: Ps 91:2,3
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 21:34-38
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Tuesday Eve | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Hos 10:12-15; Hos 11:1-2; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 33:10,11; Luke 11:37-52; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 175, 177; refs include Hos 10:12-11:2; Ps 33:10-11; Lk 11:37-52.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the Judge of the World. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 7, Eve of Holy Tuesday, "The Judge of the World", printed page 131, extracted text line 6498.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Hos 10:12-15
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6544; nearby named Fathers: Cyril, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine
- reading: Hos 11:1-2
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6532; nearby named Fathers: Cyril, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine
- reading: Ps 33:10,11
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 11:37-52
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7120; nearby named Fathers: Cyril, Chrysostom, Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Augustine; Jerome

### Tuesday Eve | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Amos 5:6-14; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 122:4; Mark 13:32-37; Mark 14:1-2; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 181, 183, 184; refs include Amos 5:6-14; Ps 122:4; Mark 13:32-14:2.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the Judge of the World. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 7, Eve of Holy Tuesday, "The Judge of the World", printed page 131, extracted text line 6498.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Amos 5:6-14
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 6544; nearby named Fathers: Cyril, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine
- reading: Ps 122:4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Mark 13:32-37
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7275; nearby named Fathers: Athanasius, Cyril, Chrysostom, Basil, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Cyril; Chrysostom; Basil; Augustine
- reading: Mark 14:1-2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Tuesday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7275; nearby named Fathers: Athanasius, Cyril, Chrysostom, Basil, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Cyril; Chrysostom; Basil; Augustine

### Tuesday | First Hour

- hour_theme_from_data: the beginning of the day and watchfulness
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Exod 19:1-9; data_source api
  - order 2; slot OT2; refs Job 23:2-17; Job 24:1-25; data_source api
  - order 3; slot OT3; refs Hos 4:1-8; data_source api
  - order 4; slot Psalm+Gospel; refs Ps 120:2,6,7; John 11:12-24; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the beginning of the day and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 5 readings for this hour; pages 188, 189, 192, 195, 196; refs include Exod 19:1-9; Job 23:2-24:25; Hos 4:1-8; Ps 120:2,120:6-7; Jn 8:21-29.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Tuesday around the Bridegroom and readiness. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 8, Holy Tuesday, "Behold the Bridegroom", printed page 151, extracted text line 7539.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Exod 19:1-9
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7648; nearby named Fathers: Chrysostom, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Augustine
- reading: Job 23:2-17
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Tuesday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7562; nearby named Fathers: Origen, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Shenouda
- reading: Job 24:1-25
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Tuesday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7582; nearby named Fathers: Origen, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Shenouda
- reading: Hos 4:1-8
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Tuesday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7584; nearby named Fathers: Origen, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Shenouda
- reading: Ps 120:2,6,7
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Tuesday First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 11:12-24
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Tuesday First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Tuesday | Third Hour

- hour_theme_from_data: the descent of the Holy Spirit and the trial of the heart
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Isa 5:20-30; data_source api
  - order 2; slot OT2; refs Jer 9:12-19; data_source api
  - order 3; slot Psalm+Gospel; refs Ps 122:1-2; Mark 11:11-19; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the descent of the Holy Spirit and the trial of the heart` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 6 readings for this hour; pages 200, 201, 202, 204, 206, 207; refs include Deut 8:11-20; Sir 1:1-14; Job 27:2-28:2; 1Kgs 19:9-14; Ps 119:154-155; Matt 23:37-24:2.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Tuesday around the Bridegroom and readiness. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 8, Holy Tuesday, "Behold the Bridegroom", printed page 151, extracted text line 7539.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Isa 5:20-30
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Jer 9:12-19
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Tuesday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 122:1-2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Tuesday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Mark 11:11-19
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Tuesday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Tuesday | Sixth Hour

- hour_theme_from_data: the Cross and the Lord's willing suffering
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Ezek 21:3-13; data_source St Mary Ottawa Holy Pascha source-text correction 2026-06-06
  - order 2; slot OT2; refs Sir 4:20-5:2; data_source St Mary Ottawa Holy Pascha source-text correction 2026-06-06
  - order 3; slot OT3; refs Isa 1:1-9; data_source St Mary Ottawa Holy Pascha source-text correction 2026-06-06
  - order 4; slot Psalm+Gospel; refs Ps 18:48,17; John 8:12-20; data_source St Mary Ottawa Holy Pascha source-text correction 2026-06-06

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Cross and the Lord's willing suffering` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 5 readings for this hour; pages 210, 211, 213, 215, 216; refs include Ezek 21:3-13; Sir 4:20-5:2; Isa 1:1-9; Ps 18:17,18:48; Jn 8:12-20.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Tuesday around the Bridegroom and readiness. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 8, Holy Tuesday, "Behold the Bridegroom", printed page 151, extracted text line 7539.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Ezek 21:3-13
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7581; nearby named Fathers: Origen, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Shenouda
- reading: Sir 4:20-5:2
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Tuesday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7582; nearby named Fathers: Origen, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Shenouda
- reading: Isa 1:1-9
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Tuesday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 8183; nearby named Fathers: Athanasius, Chrysostom, Origen.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Chrysostom; Origen
- reading: Ps 18:48,17
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Tuesday Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 8:12-20
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Tuesday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7589; nearby named Fathers: Chrysostom, Origen, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Shenouda

### Tuesday | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Gen 6:5-9:7; data_source api+St Mary Ottawa Holy Pascha PDF cross-check 2026-06-06
  - order 2; slot OT2; refs Isa 40:1-5; data_source api
  - order 3; slot OT3; refs Prov 1:1-9; data_source api
  - order 4; slot Psalm+Gospel; refs Ps 65:5,4; Matt 21:23-27; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 7 readings for this hour; pages 219, 225, 226, 228, 229, 232; refs include Gen 6:5-9:7; Prov 9:1-11; Isa 40:9-31; Dan 7:9-15; Prov 8:1-12; Ps 25:1-3; Matt 24:3-35.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Tuesday around the Bridegroom and readiness. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 8, Holy Tuesday, "Behold the Bridegroom", printed page 151, extracted text line 7539.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Gen 6:5-9:7
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 8488; nearby named Fathers: Chrysostom, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Shenouda
- reading: Isa 40:1-5
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Tuesday Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 3:3; Mark 1:3; Luke 3:4; John 1:23
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=inferred_patristic_cross_reference_to_verify; items=John Chrysostom; Augustine
- reading: Prov 1:1-9
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Tuesday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7582; nearby named Fathers: Origen, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Shenouda
- reading: Ps 65:5,4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Tuesday Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Matt 21:23-27
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Tuesday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7589; nearby named Fathers: Chrysostom, Origen, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Shenouda

### Tuesday | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Isa 50:1-3; data_source api
  - order 2; slot OT2; refs Wis 2:20-30; data_source api
  - order 3; slot Psalm+Gospel; refs Ps 13:3-4; John 8:51-59; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 4 readings for this hour; pages 238, 239, 243; refs include Isa 30:25-30; Prov 6:20-7:4; Ps 12:3-4; Matt 25:14-26:2.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Tuesday around the Bridegroom and readiness. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 8, Holy Tuesday, "Behold the Bridegroom", printed page 151, extracted text line 7539.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Tuesday centers the Bridegroom, readiness, and the virgins waiting for His coming. Article: The Homily of Tuesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/03/the-homily-of-tuesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Isa 50:1-3
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Tuesday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 9506; nearby named Fathers: Cyril, Chrysostom, Augustine, Ambrose, Irenaeus.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 26:67; Mark 14:65
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Augustine; Ambrose; Irenaeus
- reading: Wis 2:20-30
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Tuesday Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 27:43
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 2:12-20; The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 13:3-4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Tuesday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 8170; nearby named Fathers: Chrysostom, Origen, Irenaeus.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Irenaeus
- reading: John 8:51-59
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Tuesday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 7589; nearby named Fathers: Chrysostom, Origen, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Shenouda

### Wednesday Eve | First Hour

- hour_theme_from_data: the beginning of the day and watchfulness
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Jer 43:5-11; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 69:1,16; John 10:17-21; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the beginning of the day and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 4 readings for this hour; pages 251, 252, 254; refs include Ezek 22:17-22; Ezek 22:23-28; Ps 59:16-17; Matt 22:1-14.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the wedding feast and watchful entrance. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 9, Eve of Holy Wednesday, "The Wedding Feast", printed page 193, extracted text line 9826.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Jer 43:5-11
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday Eve First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 69:1,16
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=John 2:17; John 19:28-29; Acts 1:20
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 10:17-21
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 10120; nearby named Fathers: Cyril, Chrysostom, Gregory, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Augustine; Ambrose

### Wednesday Eve | Third Hour

- hour_theme_from_data: the descent of the Holy Spirit and the trial of the heart
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Amos 4:4-13; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 55:21,1; Mark 14:3-11; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the descent of the Holy Spirit and the trial of the heart` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 259, 261, 262; refs include Amos 5:18-27; Ps 65:4; Matt 24:36-51.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the wedding feast and watchful entrance. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 9, Eve of Holy Wednesday, "The Wedding Feast", printed page 193, extracted text line 9826.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Amos 4:4-13
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday Eve Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 10243; nearby named Fathers: Cyril, Chrysostom, Gregory, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Origen; Augustine
- reading: Ps 55:21,1
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 10880; nearby named Fathers: Cyril, Chrysostom, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Origen; Augustine
- reading: Mark 14:3-11
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Wednesday Eve | Sixth Hour

- hour_theme_from_data: the Cross and the Lord's willing suffering
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Amos 3:1-11; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 140:1,2; John 12:36-43; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Cross and the Lord's willing suffering` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 266, 268, 269; refs include Jer 16:9-13; Ps 102:1-2; Matt 25:1-13.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the wedding feast and watchful entrance. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 9, Eve of Holy Wednesday, "The Wedding Feast", printed page 193, extracted text line 9826.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Amos 3:1-11
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 140:1,2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 12:36-43
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Wednesday Eve | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Ezek 20:27-33; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 7:1-2; John 10:29-38; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 272, 274; refs include Hos 9:14-10:2; Ps 22:20-21; Matt 23:29-36.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the wedding feast and watchful entrance. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 9, Eve of Holy Wednesday, "The Wedding Feast", printed page 193, extracted text line 9826.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Ezek 20:27-33
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 9848; nearby named Fathers: no named Father surfaced in the nearby window.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 7:1-2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 10299; nearby named Fathers: Chrysostom, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Augustine
- reading: John 10:29-38
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 10120; nearby named Fathers: Cyril, Chrysostom, Gregory, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Augustine; Ambrose

### Wednesday Eve | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Wis 7:24-30; data_source St Mary Ottawa Holy Pascha source-text correction 2026-06-06
  - order 2; slot Psalm+Gospel; refs Ps 57:1; John 11:55-57; data_source St Mary Ottawa Holy Pascha source-text correction 2026-06-06

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 278, 280, 281; refs include Wis 7:24-30; Ps 57:1; Jn 11:55-57.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around the wedding feast and watchful entrance. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 9, Eve of Holy Wednesday, "The Wedding Feast", printed page 193, extracted text line 9826.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Wis 7:24-30
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 9946; nearby named Fathers: Gregory, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Augustine
- reading: Ps 57:1
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 10880; nearby named Fathers: Cyril, Chrysostom, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Origen; Augustine
- reading: John 11:55-57
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 9949; nearby named Fathers: Gregory, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Augustine

### Wednesday | First Hour

- hour_theme_from_data: the beginning of the day and watchfulness
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Exod 17:1-7; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 2; slot OT2; refs Prov 3:5-14; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 3; slot OT3; refs Hos 5:13-6:3; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 4; slot OT4; refs Wis 1:20-2:15; data_source api
  - order 5; slot OT5; refs Wis 3:12-24; data_source api
  - order 6; slot Psalm+Gospel; refs Ps 51:4; Ps 33:10; John 11:46-57; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the beginning of the day and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 5 readings for this hour; pages 285, 286, 287, 292; refs include Exod 17:1-7; Prov 3:5-14; Hos 5:13-6:3; Ps 33:10,51:4; Jn 11:46-57.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Wednesday around love offered to Christ and betrayal against Him. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 10, Holy Wednesday, "Kisses of Love and Betrayal", printed page 217, extracted text line 11028.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Exod 17:1-7
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=1 Corinthians 10:4
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Prov 3:5-14
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Wednesday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11106; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda
- reading: Hos 5:13-6:3
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Wednesday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11107; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda
- reading: Wis 1:20-2:15
  - slot: OT4
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot OT4, for Wednesday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11334; nearby named Fathers: Cyril, Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine; Jerome
- reading: Wis 3:12-24
  - slot: OT5
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot OT5, for Wednesday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11334; nearby named Fathers: Cyril, Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine; Jerome
- reading: Ps 51:4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Wednesday First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 33:10
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Wednesday First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 11:46-57
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Wednesday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11114; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda

### Wednesday | Third Hour

- hour_theme_from_data: the descent of the Holy Spirit and the trial of the heart
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Exod 13:17-22; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 2; slot OT2; refs Sir 22:7-18; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 3; slot OT3; refs Prov 4:4-5:4; data_source api
  - order 4; slot Psalm+Gospel; refs Ps 41:6,1; Luke 22:1-6; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the descent of the Holy Spirit and the trial of the heart` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 6 readings for this hour; pages 296, 297, 298, 299, 301, 302; refs include Exod 13:17-22; Sir 22:7-18; Job 27:16-28:2; Prov 4:4-27,5:1-4; Ps 41:1,41:6; Lk 22:1-6.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Wednesday around love offered to Christ and betrayal against Him. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 10, Holy Wednesday, "Kisses of Love and Betrayal", printed page 217, extracted text line 11028.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Exod 13:17-22
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Sir 22:7-18
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Wednesday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11106; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda
- reading: Prov 4:4-5:4
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Wednesday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11108; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda
- reading: Ps 41:6,1
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Wednesday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=John 13:18
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 22:1-6
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Wednesday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11114; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda

### Wednesday | Sixth Hour

- hour_theme_from_data: the Cross and the Lord's willing suffering
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Exod 14:13-15:1; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 2; slot OT2; refs Sir 23:7-14; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 3; slot OT3; refs Job 27:16-20; Job 28:1-2; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 4; slot Psalm+Gospel; refs Ps 83:2,5; John 12:1-8; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Cross and the Lord's willing suffering` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 1 readings for this hour; pages 305; refs include Exod 14:13-15:1.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Wednesday around love offered to Christ and betrayal against Him. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 10, Holy Wednesday, "Kisses of Love and Betrayal", printed page 217, extracted text line 11028.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Exod 14:13-15:1
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11827; nearby named Fathers: Chrysostom, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=1 Corinthians 10:1-4
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril of Jerusalem; Chrysostom; Jerome
- reading: Sir 23:7-14
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Wednesday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11107; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda
- reading: Job 27:16-20
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Wednesday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11520; nearby named Fathers: Athanasius, Gregory, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Gregory; Origen; Augustine
- reading: Job 28:1-2
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Wednesday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11520; nearby named Fathers: Athanasius, Gregory, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Gregory; Origen; Augustine
- reading: Ps 83:2,5
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Wednesday Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 12:1-8
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Wednesday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11114; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda

### Wednesday | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Gen 24:1-9; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 2; slot OT2; refs Num 20:1-13; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 3; slot OT3; refs Prov 1:11-35; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 4; slot OT4; refs Isa 59:1-17; data_source api
  - order 5; slot OT5; refs Zech 11:11-14; data_source api
  - order 6; slot Psalm+Gospel; refs Ps 41:5-6; Matt 26:3-16; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 11 readings for this hour; pages 308, 309, 311, 312, 315, 316; refs include Isa 48:1-6; Sir 23:7-14; Ps 83:2,83:5; Jn 12:1-8; Gen 24:1-9; Num 20:1-13; Prov 1:10-33; Isa 59:1-17.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Wednesday around love offered to Christ and betrayal against Him. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 10, Holy Wednesday, "Kisses of Love and Betrayal", printed page 217, extracted text line 11028.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Gen 24:1-9
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11105; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Romans 5:12-19; 1 Corinthians 15:45-49
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 2:23-24
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Gregory; Origen; Ambrose; Shenouda
- reading: Num 20:1-13
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Wednesday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12143; nearby named Fathers: Augustine, Hippolytus.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Augustine; Hippolytus
- reading: Prov 1:11-35
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Wednesday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11106; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda
- reading: Isa 59:1-17
  - slot: OT4
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot OT4, for Wednesday Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Zech 11:11-14
  - slot: OT5
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot OT5, for Wednesday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11109; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 27:9-10
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda
- reading: Ps 41:5-6
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Wednesday Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=John 13:18
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Matt 26:3-16
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Wednesday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12050; nearby named Fathers: Chrysostom, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine; Ambrose

### Wednesday | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Isa 28:16-29; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14
  - order 2; slot Psalm+Gospel; refs Ps 6:2-3; Ps 69:17; John 12:27-36; data_source St Mary Ottawa Holy Pascha book correction 2026-06-14

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 3 readings for this hour; pages 330, 334, 335; refs include Isa 28:16-29; Ps 6:2-3,69:17; Jn 12:27-36.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Holy Wednesday around love offered to Christ and betrayal against Him. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 10, Holy Wednesday, "Kisses of Love and Betrayal", printed page 217, extracted text line 11028.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Wednesday contrasts Mary’s hidden love offered to Christ with the betrayal that follows. Article: The Homily of Wednesday of the Holy Pascha; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-wednesday-of-the-holy-pascha/.

#### Per-reading anchors

- reading: Isa 28:16-29
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Wednesday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12496; nearby named Fathers: Cyril, Augustine, Severus.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Augustine; Severus
- reading: Ps 6:2-3
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11478; nearby named Fathers: Cyril, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Origen; Augustine
- reading: Ps 69:17
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=John 2:17; John 19:28-29; Acts 1:20
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 12:27-36
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Wednesday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 11114; nearby named Fathers: Gregory, Origen, Ambrose, Shenouda.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Origen; Ambrose; Shenouda

### Great Thursday Eve | First Hour

- hour_theme_from_data: the beginning of the day and watchfulness
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Jer 8:17-9:6; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 69:1,9; John 13:33-14:25; John 14:26-15:25; John 15:26-16:33; John 17:1-26; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the beginning of the day and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 2 readings for this hour; pages 339, 475; refs include Ezek 43:5-11; Jer 8:17-9:6.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around betrayal and the movement toward Gethsemane. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 11, Eve of Great Thursday, "The Betrayal", printed page 249, extracted text line 12707.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Jer 8:17-9:6
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Eve First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12734; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine
- reading: Ps 69:1,9
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=John 2:17; John 19:28-29; Acts 1:20
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 13:33-14:25
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12751; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine
- reading: John 14:26-15:25
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12849; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine
- reading: John 15:26-16:33
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 17:1-26
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12751; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine

### Great Thursday Eve | Third Hour

- hour_theme_from_data: the descent of the Holy Spirit and the trial of the heart
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Ezek 36:16-23; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 108:1,2; Matt 26:30-35; Mark 14:26-31; Luke 22:31-39; John 18:1,2; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the descent of the Holy Spirit and the trial of the heart` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 2 readings for this hour; pages 345, 493; refs include Amos 4:4-13; Ezek 36:16-23.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around betrayal and the movement toward Gethsemane. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 11, Eve of Great Thursday, "The Betrayal", printed page 249, extracted text line 12707.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Ezek 36:16-23
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Eve Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 108:1,2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Matt 26:30-35
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12972; nearby named Fathers: Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Augustine; Jerome
- reading: Mark 14:26-31
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12726; nearby named Fathers: no named Father surfaced in the nearby window.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 22:31-39
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 18:1,2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Great Thursday Eve | Sixth Hour

- hour_theme_from_data: the Cross and the Lord's willing suffering
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Ezek 22:23-28; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 58:2; Ps 68:21; Matt 26:36-46; Mark 14:32-42; Luke 22:40-46; John 18:3-9; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Cross and the Lord's willing suffering` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 2 readings for this hour; pages 352, 502; refs include Amos 3:1-11; Ezek 22:23-28.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around betrayal and the movement toward Gethsemane. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 11, Eve of Great Thursday, "The Betrayal", printed page 249, extracted text line 12707.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Ezek 22:23-28
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 58:2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 68:21
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12735; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine
- reading: Matt 26:36-46
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12972; nearby named Fathers: Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Augustine; Jerome
- reading: Mark 14:32-42
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12726; nearby named Fathers: no named Father surfaced in the nearby window.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 22:40-46
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 18:3-9
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Great Thursday Eve | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Jer 9:6-10; data_source api
  - order 2; slot OT2; refs Ezek 21:33-37; data_source api
  - order 3; slot Psalm+Gospel; refs Ps 27:3,4; Ps 34:4,5; Matt 26:47-58; Mark 14:43-54; Luke 22:47-55; John 18:10-14; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 2 readings for this hour; pages 359, 511; refs include Ezek 20:27-33; Jer 9:7-11.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around betrayal and the movement toward Gethsemane. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 11, Eve of Great Thursday, "The Betrayal", printed page 249, extracted text line 12707.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Jer 9:6-10
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Eve Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ezek 21:33-37
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Great Thursday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12751; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine
- reading: Ps 27:3,4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Great Thursday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13267; nearby named Fathers: Chrysostom, Gregory, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Gregory; Augustine
- reading: Ps 34:4,5
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Great Thursday Eve Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Matt 26:47-58
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Great Thursday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12972; nearby named Fathers: Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Augustine; Jerome
- reading: Mark 14:43-54
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Great Thursday Eve Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12726; nearby named Fathers: no named Father surfaced in the nearby window.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 22:47-55
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Great Thursday Eve Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 18:10-14
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Great Thursday Eve Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Great Thursday Eve | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Isa 27:11-28:15; data_source api
  - order 2; slot Psalm+Gospel; refs Ps 2:1-5; Matt 26:59-75; Mark 14:55-72; Luke 22:56-65; John 18:15-27; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 2 readings for this hour; pages 365, 520; refs include Jer 8:4-9; Isa 27:11-28:15.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames the eve around betrayal and the movement toward Gethsemane. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 11, Eve of Great Thursday, "The Betrayal", printed page 249, extracted text line 12707.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Isa 27:11-28:15
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Eve Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 2:1-5
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12735; nearby named Fathers: Chrysostom, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine
- reading: Matt 26:59-75
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12972; nearby named Fathers: Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Augustine; Jerome
- reading: Mark 14:55-72
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 12726; nearby named Fathers: no named Father surfaced in the nearby window.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Luke 22:56-65
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: John 18:15-27
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Psalm+Gospel, for Great Thursday Eve Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

### Great Thursday | First Hour

- hour_theme_from_data: the beginning of the day and watchfulness
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Exod 17:8-16; data_source api
  - order 2; slot OT2; refs Exod 15:22-16:3; data_source api
  - order 3; slot OT3; refs Isa 58:1-9; data_source api
  - order 4; slot OT4; refs Ezek 18:20-32; data_source api
  - order 5; slot Acts; refs Acts 1:15-20; data_source api
  - order 6; slot Psalm+Gospel; refs Ps 55:21,12; Luke 22:7-13; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the beginning of the day and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 6 readings for this hour; pages 372, 373, 375, 376, 381, 386; refs include Exod 17:8-16; Exod 15:23-16:3; Isa 58:1-11; Ezek 18:20-32; Acts 1:15-20; Lk 22:7-13.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Great Thursday around the Great Sacrifice, Passover preparation, foot washing, Eucharist, and betrayal. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 12, Great Thursday, "The Great Sacrifice", printed page 269, extracted text line 13700.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Exod 17:8-16
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13764; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=1 Corinthians 10:4
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian
- reading: Exod 15:22-16:3
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Great Thursday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13764; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=1 Corinthians 10:1-4
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril of Jerusalem; Origen; Tertullian; Shenouda; Cyprian
- reading: Isa 58:1-9
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Great Thursday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13764; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian
- reading: Ezek 18:20-32
  - slot: OT4
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot OT4, for Great Thursday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13751; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Tertullian; Shenouda; Cyprian
- reading: Acts 1:15-20
  - slot: Acts
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Acts, for Great Thursday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13800; nearby named Fathers: Origen, Ambrose, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Ambrose; Tertullian; Shenouda; Cyprian
- reading: Ps 55:21,12
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Great Thursday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 16411; nearby named Fathers: Cyril, Chrysostom, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Origen; Augustine
- reading: Luke 22:7-13
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Great Thursday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13764; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian

### Great Thursday | Third Hour

- hour_theme_from_data: the descent of the Holy Spirit and the trial of the heart
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Exod 32:30-33:5; data_source api
  - order 2; slot OT2; refs Wis 24:1-11; data_source api
  - order 3; slot OT3; refs Zech 9:11-14; Zech 10:1-2; data_source api
  - order 4; slot OT4; refs Prov 4:4-5:4; data_source api
  - order 5; slot Psalm+Gospel; refs Ps 94:21,23; Matt 26:17-19; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the descent of the Holy Spirit and the trial of the heart` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 6 readings for this hour; pages 389, 391, 392, 393, 394, 395; refs include Exod 32:30-33:5; Sir 24:1-11; Zech 9:11-14; Prov 30:2-6; Ps 94:21,94:23; Matt 26:17-19.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Great Thursday around the Great Sacrifice, Passover preparation, foot washing, Eucharist, and betrayal. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 12, Great Thursday, "The Great Sacrifice", printed page 269, extracted text line 13700.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Exod 32:30-33:5
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13764; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=1 Corinthians 10:7
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian
- reading: Wis 24:1-11
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Great Thursday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 27:43
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 2:12-20; The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Zech 9:11-14
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Great Thursday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13750; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 21:5; John 12:15
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Tertullian; Shenouda; Cyprian
- reading: Zech 10:1-2
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Great Thursday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Prov 4:4-5:4
  - slot: OT4
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot OT4, for Great Thursday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 94:21,23
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Psalm+Gospel, for Great Thursday Third Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Matt 26:17-19
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Psalm+Gospel, for Great Thursday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13753; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian

### Great Thursday | Sixth Hour

- hour_theme_from_data: the Cross and the Lord's willing suffering
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Exod 7:2-15; data_source api
  - order 2; slot OT2; refs Ezek 20:39-44; data_source api
  - order 3; slot OT3; refs Wis 12:13-13:1; data_source api
  - order 4; slot Psalm+Gospel; refs Ps 31:18,13; Mark 14:12-16; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Cross and the Lord's willing suffering` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 5 readings for this hour; pages 398, 400, 401, 402, 403; refs include Jer 7:2-15; Ezek 20:39-44; Sir 23:7-14; Ps 31:13,31:18; Mark 14:12-16.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Great Thursday around the Great Sacrifice, Passover preparation, foot washing, Eucharist, and betrayal. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 12, Great Thursday, "The Great Sacrifice", printed page 269, extracted text line 13700.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Exod 7:2-15
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13764; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian
- reading: Ezek 20:39-44
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Great Thursday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13749; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Tertullian; Shenouda; Cyprian
- reading: Wis 12:13-13:1
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Great Thursday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 14222; nearby named Fathers: Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Augustine; Ambrose
- reading: Ps 31:18,13
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Great Thursday Sixth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Luke 23:46
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Mark 14:12-16
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Great Thursday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13753; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian

### Great Thursday | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Gen 22:1-19; data_source api
  - order 2; slot OT2; refs Isa 61:1-7; data_source api
  - order 3; slot OT3; refs Gen 14:17-20; data_source api
  - order 4; slot OT4; refs Job 27:2-28:13; data_source api
  - order 5; slot Psalm+Gospel; refs Ps 23:1,2; Matt 26:17-19; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 5 readings for this hour; pages 408, 409, 410, 414, 415; refs include Isa 61:1-6; Gen 14:17-20; Job 27:2-28:13; Ps 41:5-7; Matt 26:3-16.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Great Thursday around the Great Sacrifice, Passover preparation, foot washing, Eucharist, and betrayal. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 12, Great Thursday, "The Great Sacrifice", printed page 269, extracted text line 13700.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Gen 22:1-19
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13748; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Hebrews 11:17-19; Romans 8:32; Romans 5:12-19; 1 Corinthians 15:45-49
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 2:23-24
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Tertullian; Shenouda; Cyprian
- reading: Isa 61:1-7
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Great Thursday Ninth Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Luke 4:18-21
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=inferred_patristic_cross_reference_to_verify; items=Cyril of Alexandria
- reading: Gen 14:17-20
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Great Thursday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13750; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Hebrews 7:1-17
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=John Chrysostom; Tertullian; Shenouda; Cyprian
- reading: Job 27:2-28:13
  - slot: OT4
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot OT4, for Great Thursday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13751; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Tertullian; Shenouda; Cyprian
- reading: Ps 23:1,2
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Psalm+Gospel, for Great Thursday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13752; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Tertullian; Shenouda; Cyprian
- reading: Matt 26:17-19
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Psalm+Gospel, for Great Thursday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13753; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian

### Great Thursday | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Isa 52:13-53:12; data_source api
  - order 2; slot OT2; refs Isa 19:19-25; data_source api
  - order 3; slot OT3; refs Zech 12:11-14; Zech 13:1-9; Zech 14:1-4; Zech 14:6-9; data_source api
  - order 4; slot Psalm+Gospel; refs Ps 50:17,18; John 13:21-30; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 5 readings for this hour; pages 463, 465, 466, 469; refs include Isa 52:13-53:12; Isa 19:19-25; Zech 12:11-14:3,14:6-9; Ps 50:17-18; Jn 13:21-30.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Great Thursday around the Great Sacrifice, Passover preparation, foot washing, Eucharist, and betrayal. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 12, Great Thursday, "The Great Sacrifice", printed page 269, extracted text line 13700.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.

#### Per-reading anchors

- reading: Isa 52:13-53:12
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Acts 8:32-35; 1 Peter 2:22-25
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=inferred_patristic_cross_reference_to_verify; items=Athanasius; Cyril of Alexandria
- reading: Isa 19:19-25
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Great Thursday Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Zech 12:11-14
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Great Thursday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13750; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=John 19:37; Revelation 1:7
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Tertullian; Shenouda; Cyprian
- reading: Zech 13:1-9
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Great Thursday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13750; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 26:31; Mark 14:27
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Tertullian; Shenouda; Cyprian
- reading: Zech 14:1-4
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Great Thursday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13750; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Tertullian; Shenouda; Cyprian
- reading: Zech 14:6-9
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Great Thursday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13750; nearby named Fathers: Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Tertullian; Shenouda; Cyprian
- reading: Ps 50:17,18
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Great Thursday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13790; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian
- reading: John 13:21-30
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Great Thursday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 13753; nearby named Fathers: Origen, Tertullian, Shenouda, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Origen; Tertullian; Shenouda; Cyprian

### Great Thursday | Liturgy of Blessing of the Water

- hour_theme_from_data: blank
- sourced_theme_candidate_for_blank: Sourced theme: washing of the disciples’ feet, purification, living water, and preparation for the Eucharistic covenant. Source basis: Treasures chapter 12 and the St Mary Ottawa service title.
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Gen 18:1-23; data_source St Mary Ottawa Holy Pascha PDF cross-check 2026-06-06

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `blank` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 9 readings for this hour; pages 421, 423, 425, 426, 428, 429; refs include Gen 18:1-23; Prov 9:1-11; Isa 4:2-4; Isa 55:1-56:1; Ezek 36:25-29; Ezek 47:1-9; 1Tim 4:9-5:10; Ps 51:7,51:10.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter frames Great Thursday around the Great Sacrifice, Passover preparation, foot washing, Eucharist, and betrayal. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 12, Great Thursday, "The Great Sacrifice", printed page 269, extracted text line 13700.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Covenant Thursday centers the New Covenant, the Eucharist, and forgiveness through Christ’s Body and Blood. Article: The Homily of Covenant Thursday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/05/the-homily-of-covenant-thursday/.
- snippet:
  - basis: read_from_source
  - scope: blank-theme coverage
  - source: special_theme_synthesis_from_collected_sources
  - author: source collector
  - copyright_status: modern_copyrighted
  - summary: Sourced theme: washing of the disciples’ feet, purification, living water, and preparation for the Eucharistic covenant. Source basis: Treasures chapter 12 and the St Mary Ottawa service title.

#### Per-reading anchors

- reading: Gen 18:1-23
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Great Thursday Liturgy of Blessing of the Water.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 14992; nearby named Fathers: Cyril, Gregory, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Gregory; Augustine; Ambrose

### Good Friday | First Hour

- hour_theme_from_data: the beginning of the day and watchfulness
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Deut 8:19-9:24; data_source api
  - order 2; slot OT2; refs Isa 1:2-9; data_source api
  - order 3; slot OT3; refs Isa 2:10-21; data_source api
  - order 4; slot OT4; refs Jer 22:29-23:6; data_source api
  - order 5; slot OT5; refs Isa 24:1-13; data_source api
  - order 6; slot OT6; refs Wis 2:12-22; data_source api
  - order 7; slot OT7; refs Job 12:18-13:1; data_source api
  - order 8; slot OT8; refs Zech 11:11-14; data_source api
  - order 9; slot OT9; refs Mic 1:16-2:3; data_source api
  - order 10; slot OT10; refs Mic 7:1-8; data_source api
  - order 11; slot Psalm+Gospel; refs Ps 27:12; Ps 35:11,12,16; Matt 27:1-14; Mark 15:1-5; Luke 22:66-23:12; John 18:28-40; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the beginning of the day and watchfulness` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 16 readings for this hour; pages 534, 538, 539, 540, 541, 542; refs include Deut 8:19-9:24; Isa 1:2-9; Isa 2:10-21; Jer 22:29-23:6; Zech 11:14; Isa 24:1-13; Wis 2:12-22; Job 12:17-13:1.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Great Friday around the hymn and confession, This is He. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 14, Great Friday, "This is He", printed page 381, extracted text line 19567.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Great Friday treats the trial and crucifixion as the fulfillment of prophecy and symbol. Article: The Homily of Great Friday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/06/the-homily-of-great-friday/.

#### Per-reading anchors

- reading: Deut 8:19-9:24
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Good Friday First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Isa 1:2-9
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20756; nearby named Fathers: Cyril, Chrysostom, Gregory, Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Augustine; Jerome
- reading: Isa 2:10-21
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19808; nearby named Fathers: Athanasius, Irenaeus.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Irenaeus
- reading: Jer 22:29-23:6
  - slot: OT4
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot OT4, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19614; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Isa 24:1-13
  - slot: OT5
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot OT5, for Good Friday First Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Wis 2:12-22
  - slot: OT6
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot OT6, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19615; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 27:43
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 2:12-20; The reading itself is deuterocanonical in the Coptic Orthodox canon.
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Job 12:18-13:1
  - slot: OT7
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 7, slot OT7, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19615; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Zech 11:11-14
  - slot: OT8
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 8, slot OT8, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19614; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 27:9-10
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Mic 1:16-2:3
  - slot: OT9
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 9, slot OT9, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19615; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Mic 7:1-8
  - slot: OT10
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 10, slot OT10, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20001; nearby named Fathers: Cyril, Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom
- reading: Ps 27:12
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 11, slot Psalm+Gospel, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 21873; nearby named Fathers: Chrysostom, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Augustine
- reading: Ps 35:11,12,16
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 11, slot Psalm+Gospel, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19666; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Matt 27:1-14
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 11, slot Psalm+Gospel, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Mark 15:1-5
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 11, slot Psalm+Gospel, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Luke 22:66-23:12
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 11, slot Psalm+Gospel, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: John 18:28-40
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 11, slot Psalm+Gospel, for Good Friday First Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom

### Good Friday | Third Hour

- hour_theme_from_data: the descent of the Holy Spirit and the trial of the heart
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Gen 48:1-19; data_source api
  - order 2; slot OT2; refs Isa 50:4-9; data_source api
  - order 3; slot OT3; refs Isa 3:9-15; data_source api
  - order 4; slot OT4; refs Isa 63:1-7; data_source api
  - order 5; slot OT5; refs Amos 9:4-6; Amos 9:8-10; data_source api
  - order 6; slot OT6; refs Job 29:21-30:10; data_source api
  - order 7; slot Psalm+Gospel; refs Ps 38:17; Ps 22:16; Matt 27:15-26; Mark 15:6-25; Luke 23:13-25; John 19:1-12; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the descent of the Holy Spirit and the trial of the heart` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 12 readings for this hour; pages 560, 562, 563, 564, 565, 566; refs include Gen 48:1-19; Isa 50:4-9; Isa 3:9-15; Isa 63:1-7; Amos 9:4-5,9:7-10; Job 29:21-25,30:1-10; Col 2:13-15; Ps 38:17.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Great Friday around the hymn and confession, This is He. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 14, Great Friday, "This is He", printed page 381, extracted text line 19567.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Great Friday treats the trial and crucifixion as the fulfillment of prophecy and symbol. Article: The Homily of Great Friday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/06/the-homily-of-great-friday/.

#### Per-reading anchors

- reading: Gen 48:1-19
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20491; nearby named Fathers: Chrysostom, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine; Ambrose
- reading: Isa 50:4-9
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20661; nearby named Fathers: Athanasius, Cyril, Chrysostom, Gregory, Ephrem the Syrian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 26:67; Mark 14:65
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Cyril; Chrysostom; Gregory; Ephrem the Syrian
- reading: Isa 3:9-15
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20721; nearby named Fathers: Cyril, Chrysostom, Gregory, Jerome, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Jerome; Cyprian
- reading: Isa 63:1-7
  - slot: OT4
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot OT4, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20756; nearby named Fathers: Cyril, Chrysostom, Gregory, Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Augustine; Jerome
- reading: Amos 9:4-6
  - slot: OT5
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot OT5, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20517; nearby named Fathers: Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Augustine
- reading: Amos 9:8-10
  - slot: OT5
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot OT5, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20517; nearby named Fathers: Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Augustine
- reading: Job 29:21-30:10
  - slot: OT6
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot OT6, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20491; nearby named Fathers: Chrysostom, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Augustine; Ambrose
- reading: Ps 38:17
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 7, slot Psalm+Gospel, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 21817; nearby named Fathers: Chrysostom, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Augustine
- reading: Ps 22:16
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 7, slot Psalm+Gospel, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19615; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 27:35; Matthew 27:46; John 19:24
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Matt 27:15-26
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 7, slot Psalm+Gospel, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Mark 15:6-25
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 7, slot Psalm+Gospel, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Luke 23:13-25
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 7, slot Psalm+Gospel, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: John 19:1-12
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 7, slot Psalm+Gospel, for Good Friday Third Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20357; nearby named Fathers: Cyril, Chrysostom, Gregory, Ephrem the Syrian, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Ephrem the Syrian; Ambrose

### Good Friday | Sixth Hour

- hour_theme_from_data: the Cross and the Lord's willing suffering
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Num 21:1-9; data_source api
  - order 2; slot OT2; refs Isa 53:7-12; data_source api
  - order 3; slot OT3; refs Isa 12:2-13:10; data_source api
  - order 4; slot OT4; refs Amos 8:9-12; data_source api
  - order 5; slot Pauline; refs Gal 6:14-18; data_source api
  - order 6; slot Psalm+Gospel; refs Ps 38:21,22; Ps 22:17,18,19,8,9; Matt 27:27-45; Mark 15:26-33; Luke 23:26-44; John 19:1-12; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Cross and the Lord's willing suffering` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 10 readings for this hour; pages 578, 579, 580, 582, 585, 591; refs include Num 21:1-9; Isa 53:7-12; Isa 12:2-13:10; Amos 8:9-12; Gal 6:14-18; Ps 21:8-9,21:16-17,37:21-22; Matt 27:27-45; Mark 15:26-33.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Great Friday around the hymn and confession, This is He. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 14, Great Friday, "This is He", printed page 381, extracted text line 19567.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Great Friday treats the trial and crucifixion as the fulfillment of prophecy and symbol. Article: The Homily of Great Friday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/06/the-homily-of-great-friday/.

#### Per-reading anchors

- reading: Num 21:1-9
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 21331; nearby named Fathers: Chrysostom, Gregory, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=John 3:14-15
    - coptic_canon_witness: status=present; basis=inferred_cross_reference_or_canon_status; items=Wisdom 16:5-7
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Gregory; Augustine
- reading: Isa 53:7-12
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20908; nearby named Fathers: Athanasius, Augustine, Jerome, Tertullian.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Acts 8:32-35; 1 Peter 2:22-25
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Athanasius; Cyril of Alexandria; Augustine; Jerome; Tertullian
- reading: Isa 12:2-13:10
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 21372; nearby named Fathers: Gregory, Ephrem the Syrian, Augustine, Tertullian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Gregory; Ephrem the Syrian; Augustine; Tertullian
- reading: Amos 8:9-12
  - slot: OT4
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot OT4, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 21331; nearby named Fathers: Chrysostom, Gregory, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Gregory; Augustine
- reading: Gal 6:14-18
  - slot: Pauline
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Pauline, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 21332; nearby named Fathers: Chrysostom, Gregory, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Gregory; Augustine
- reading: Ps 38:21,22
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 21817; nearby named Fathers: Chrysostom, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Augustine
- reading: Ps 22:17,18,19,8,9
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19615; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 27:35; Matthew 27:46; John 19:24
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Matt 27:27-45
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Mark 15:26-33
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Luke 23:26-44
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: John 19:1-12
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 6, slot Psalm+Gospel, for Good Friday Sixth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20357; nearby named Fathers: Cyril, Chrysostom, Gregory, Ephrem the Syrian, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Ephrem the Syrian; Ambrose

### Good Friday | Ninth Hour

- hour_theme_from_data: the saving death of Christ and repentance
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Jer 11:18-12:13; data_source api
  - order 2; slot OT2; refs Zech 14:5-11; data_source api
  - order 3; slot OT3; refs Hos 2:1-3,10-11; data_source api
  - order 4; slot Pauline; refs Phil 2:5-11; data_source api
  - order 5; slot Psalm+Gospel; refs Ps 69:2,3,21; Matt 27:46-50; Mark 15:34-37; Luke 23:45-46; John 19:28-30; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the saving death of Christ and repentance` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 9 readings for this hour; pages 607, 609, 610, 613, 618, 619; refs include Jer 11:18-12:13; Zech 14:6-11; Joel 2:1-3,2:10-11; Phil 2:4-11; Ps 69:1-2,69:21; Matt 27:46-50; Mark 15:34-37; Lk 23:45-46.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Great Friday around the hymn and confession, This is He. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 14, Great Friday, "This is He", printed page 381, extracted text line 19567.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Great Friday treats the trial and crucifixion as the fulfillment of prophecy and symbol. Article: The Homily of Great Friday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/06/the-homily-of-great-friday/.

#### Per-reading anchors

- reading: Jer 11:18-12:13
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Good Friday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19614; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Zech 14:5-11
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Good Friday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19614; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Hos 2:1-3,10-11
  - slot: OT3
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot OT3, for Good Friday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20533; nearby named Fathers: Ephrem the Syrian, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Ephrem the Syrian; Augustine
- reading: Phil 2:5-11
  - slot: Pauline
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Pauline, for Good Friday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 22084; nearby named Fathers: Cyril, Gregory, Origen, Ephrem the Syrian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Gregory; Origen; Ephrem the Syrian
- reading: Ps 69:2,3,21
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Psalm+Gospel, for Good Friday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 22412; nearby named Fathers: Cyril, Chrysostom, Ephrem the Syrian, Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=John 2:17; John 19:28-29; Acts 1:20
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Ephrem the Syrian; Augustine; Jerome
- reading: Matt 27:46-50
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Psalm+Gospel, for Good Friday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Mark 15:34-37
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Psalm+Gospel, for Good Friday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Luke 23:45-46
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Psalm+Gospel, for Good Friday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: John 19:28-30
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 5, slot Psalm+Gospel, for Good Friday Ninth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20357; nearby named Fathers: Cyril, Chrysostom, Gregory, Ephrem the Syrian, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Ephrem the Syrian; Ambrose

### Good Friday | Eleventh Hour

- hour_theme_from_data: the late call to repentance and mercy
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Jer 12:1-14; data_source api
  - order 2; slot OT2; refs Isa 3:5-12; data_source api
  - order 3; slot Psalm+Gospel; refs Ps 143:6,7; Ps 31:5; Matt 27:51-56; Mark 15:38-41; Luke 23:47-49; John 19:31-37; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the late call to repentance and mercy` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 8 readings for this hour; pages 625, 627, 629, 631, 632, 633; refs include Exod 12:1-14; Lev 23:5-12; Gal 3:1-6; Ps 31:5,143:6-7; Matt 27:51-56; Mark 15:38-41; Lk 23:47-49; Jn 19:31-37.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Great Friday around the hymn and confession, This is He. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 14, Great Friday, "This is He", printed page 381, extracted text line 19567.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Great Friday treats the trial and crucifixion as the fulfillment of prophecy and symbol. Article: The Homily of Great Friday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/06/the-homily-of-great-friday/.

#### Per-reading anchors

- reading: Jer 12:1-14
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Good Friday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19663; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Isa 3:5-12
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Good Friday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20721; nearby named Fathers: Cyril, Chrysostom, Gregory, Jerome, Cyprian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Jerome; Cyprian
- reading: Ps 143:6,7
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 24461; nearby named Fathers: Chrysostom, Gregory, Origen, Augustine, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Gregory; Origen; Augustine; Ambrose
- reading: Ps 31:5
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Eleventh Hour.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Luke 23:46
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Matt 27:51-56
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Mark 15:38-41
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Luke 23:47-49
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: John 19:31-37
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Eleventh Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20357; nearby named Fathers: Cyril, Chrysostom, Gregory, Ephrem the Syrian, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Ephrem the Syrian; Ambrose

### Good Friday | Twelfth Hour

- hour_theme_from_data: burial, waiting, and hope
- source_count: 4
- sources_used: `local_pascha_day_hour_index`, `st_mary_ottawa_source_text_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot OT1; refs Lam 3:1-66; data_source api
  - order 2; slot OT2; refs Jonah 1:10-2:8; data_source api
  - order 3; slot Psalm+Gospel; refs Ps 88:6; Ps 23:4; Ps 45:6,8; Matt 27:57-61; Mark 15:42-16:1; Luke 23:50-56; John 19:38-42; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `burial, waiting, and hope` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: reading roster
  - source: st_mary_ottawa_source_text_index
  - author: St Mary Ottawa / UKMID Holy Pascha
  - copyright_status: modern_copyrighted
  - summary: Source-text index attests 7 readings for this hour; pages 638, 642, 644, 645, 646, 647; refs include Lam 3:1-66; Jonah 1:10-2:7; Ps 23:4,88:6; Matt 27:57-61; Mark 15:42-16:1; Lk 23:50-56; Jn 19:38-42.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Great Friday around the hymn and confession, This is He. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 14, Great Friday, "This is He", printed page 381, extracted text line 19567.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew on Great Friday treats the trial and crucifixion as the fulfillment of prophecy and symbol. Article: The Homily of Great Friday; URL: https://coptictreasuresenglish.wordpress.com/2018/04/06/the-homily-of-great-friday/.

#### Per-reading anchors

- reading: Lam 3:1-66
  - slot: OT1
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot OT1, for Good Friday Twelfth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 22392; nearby named Fathers: Cyril, Chrysostom, Ephrem the Syrian, Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Ephrem the Syrian; Augustine; Jerome
- reading: Jonah 1:10-2:8
  - slot: OT2
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot OT2, for Good Friday Twelfth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 24786; nearby named Fathers: Chrysostom, Ambrose, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=present; basis=inferred_cross_reference; items=Matthew 12:40
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril of Jerusalem; Chrysostom; Ambrose; Jerome
- reading: Ps 88:6
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Twelfth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 23198; nearby named Fathers: Chrysostom, Origen, Augustine.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Origen; Augustine
- reading: Ps 23:4
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Twelfth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 21738; nearby named Fathers: Chrysostom, Gregory, Augustine, Jerome.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom; Gregory; Augustine; Jerome
- reading: Ps 45:6,8
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Twelfth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 22002; nearby named Fathers: Cyril, Gregory, Origen, Ephrem the Syrian.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Gregory; Origen; Ephrem the Syrian
- reading: Matt 27:57-61
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Twelfth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Mark 15:42-16:1
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Twelfth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: Luke 23:50-56
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Twelfth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 19616; nearby named Fathers: Chrysostom.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Chrysostom
- reading: John 19:38-42
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Psalm+Gospel, for Good Friday Twelfth Hour.
    - basis: read_from_source
      source: treasures_holy_pascha
      author: compiled patristic excerpts in the Treasures volume
      copyright_status: translation_copyrighted
      summary: Treasures has nearby source context for this reference at extracted text line 20357; nearby named Fathers: Cyril, Chrysostom, Gregory, Ephrem the Syrian, Ambrose.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=present; basis=read_from_source_nearby; items=Cyril; Chrysostom; Gregory; Ephrem the Syrian; Ambrose

### Bright Saturday | Liturgy

- hour_theme_from_data: the Eucharistic gathering of the Church
- source_count: 3
- sources_used: `local_pascha_day_hour_index`, `treasures_holy_pascha`, `fr_matthew_holy_week`
- readings_from_data:
  - order 1; slot Pauline; refs 1Cor 15:1-22; data_source api
  - order 2; slot Catholic; refs 1Pet 1:1-9; data_source api
  - order 3; slot Acts; refs Acts 3:12-21; data_source api
  - order 4; slot Psalm+Gospel; refs Ps 3:5,3; Ps 82:8; Matt 28:1-20; data_source api

#### Collected snippets

- snippet:
  - basis: read_from_source
  - scope: hour theme
  - source: local_pascha_day_hour_index
  - author: George local lectionary data build
  - copyright_status: modern_copyrighted
  - summary: Data theme is `the Eucharistic gathering of the Church` for this day/hour.
- snippet:
  - basis: read_from_source
  - scope: day/hour framing
  - source: treasures_holy_pascha
  - author: St Paul Brotherhood, prepared by Fr John Paul
  - copyright_status: modern_copyrighted
  - summary: The Treasures chapter title frames Bright Saturday around Christ lifting humanity up through His descent and victory. Locator: Treasures of the Fathers: The Holy Pascha, Chapter 15, Bright Saturday, "He Lifts Us Up", printed page 491, extracted text line 25401.
- snippet:
  - basis: read_from_source
  - scope: patristic layer
  - source: treasures_holy_pascha
  - author: compiled patristic excerpts in the Treasures volume
  - copyright_status: translation_copyrighted
  - summary: Use this chapter as a patristic discovery layer; exact Father wording should be traced before reader-facing quotation.
- snippet:
  - basis: read_from_source
  - scope: modern Coptic spiritual reflection
  - source: fr_matthew_holy_week
  - author: Father Matthew the Poor
  - copyright_status: modern_copyrighted
  - summary: Fr Matthew’s Holy Week reflection supplies the Paschal frame of crossing over through the slain Lamb; the Bright Saturday source layer comes mainly from Treasures and the local service-order data. Article: Reflections on Holy Week; URL: https://coptictreasuresenglish.wordpress.com/2018/04/01/reflections-on-holy-week/.
- snippet:
  - basis: read_from_source
  - scope: blank-theme coverage
  - source: special_theme_synthesis_from_collected_sources
  - author: source collector
  - copyright_status: modern_copyrighted
  - summary: Sourced theme: Bright Saturday/Apocalypse gathers praise and Scripture around Christ descending to Hades and lifting humanity up. Source basis: Treasures chapter 15 and local Bright Saturday service-order rows.

#### Per-reading anchors

- reading: 1Cor 15:1-22
  - slot: Pauline
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 1, slot Pauline, for Bright Saturday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: 1Pet 1:1-9
  - slot: Catholic
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 2, slot Catholic, for Bright Saturday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Acts 3:12-21
  - slot: Acts
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 3, slot Acts, for Bright Saturday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 3:5,3
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Bright Saturday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Ps 82:8
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Bright Saturday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced
- reading: Matt 28:1-20
  - slot: Psalm+Gospel
  - source_notes:
    - basis: read_from_source
      source: local_pascha_day_hour_index
      author: George local lectionary data build
      copyright_status: modern_copyrighted
      summary: Appointed in order 4, slot Psalm+Gospel, for Bright Saturday Liturgy.
    - basis: inferred
      source: source-pack search note
      author: source collector
      copyright_status: modern_copyrighted
      summary: No exact nearby Treasures context was surfaced by the simple reference search in this pass.
  - anchors:
    - dominical_or_apostolic_citation: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - coptic_canon_witness: status=not_surfaced; basis=not_surfaced; items=none surfaced
    - named_father_reading: status=not_surfaced; basis=not_surfaced; items=none surfaced

## Blank-hour-theme coverage note

- scoped_blank_rows: 30
- now_have_sourced_theme: 30
- remain_gaps_for_George: 0

| day | hour | slot | reading | matched_study_slug | coverage_status | source_basis |
| --- | --- | --- | --- | --- | --- | --- |
| Great Thursday | Liturgy of Blessing of the Water | OT1 | Gen 18:1-23 | genesis-18-the-lord-visits-abraham-and-intercession-for-sodom | covered_by_sourced_theme | Treasures chapter 12; St Mary Ottawa service title; Fr Matthew Covenant Thursday |
| Great Thursday | Liturgy of Blessing of the Water | Prophecy | Ezek 36:25-29 | ezekiel-35-36-edom-judged-and-the-new-heart-promised | covered_by_sourced_theme | Treasures chapter 12; St Mary Ottawa service title; Fr Matthew Covenant Thursday |
| Great Thursday | Liturgy of Blessing of the Water | Prophecy | Ezek 47:1-9 | ezekiel-47-48-river-of-life-and-the-lord-is-there | covered_by_sourced_theme | Treasures chapter 12; St Mary Ottawa service title; Fr Matthew Covenant Thursday |
| Great Thursday | Liturgy of Blessing of the Water | Prophecy | Isa 4:2-4 | isaiah-2-4-zion-judgment-and-the-branch | covered_by_sourced_theme | Treasures chapter 12; St Mary Ottawa service title; Fr Matthew Covenant Thursday |
| Great Thursday | Liturgy of Blessing of the Water | Prophecy | Isa 55:1-56:1 | isaiah-56-57-inclusion-and-false-worship | covered_by_sourced_theme | Treasures chapter 12; St Mary Ottawa service title; Fr Matthew Covenant Thursday |
| Great Thursday | Liturgy of Blessing of the Water | Prophecy | Prov 9:1-11 | proverbs-9-two-banquets-wisdom-and-folly | covered_by_sourced_theme | Treasures chapter 12; St Mary Ottawa service title; Fr Matthew Covenant Thursday |
| Great Thursday | Liturgy of Blessing of the Water | Psalm | Ps 51:7,51:10 (LXX Ps 50:7; Ps 50:10) | psalm-51-lxx-50-have-mercy-upon-me-o-god | covered_by_sourced_theme | Treasures chapter 12; St Mary Ottawa service title; Fr Matthew Covenant Thursday |
| PRAISES OF THE PROPHETS | Midnight Praises | First Prayer of Isaiah | Isa 26:9-20 | isaiah-24-27-apocalypse-feast-and-resurrection-hope | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of Azariah (Part 1) | Dan 3:25-51 | daniel-3-the-fiery-furnace-and-the-three-holy-youths | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of Baruch | Bar 2:11-16 | baruch-overview | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of Daniel | Dan 9:4-19 | prayer-of-azariah-and-song-of-the-three-holy-children-5-bright-saturday | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of David | 1Chr 29:10-13 | 1-chronicles-28-29-davids-final-charge-offering-prayer-and-solomons-accession | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of Habakkuk | Hab 3:2-19 | habakkuk-3-prayer-theophany-and-rejoicing-without-visible-deliverance | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of Hannah | 1Sam 2:1-11 | 1-samuel-1-2-hannah-samuel-and-the-corruption-of-eli-s-house | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of Hezekiah | Isa 38:10-20 | isaiah-36-39-hezekiah-assyria-and-babylon | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of Jeremiah | Lam 5:16-22 | lamentations-4-5-collapse-and-final-prayer | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of Jonah | Jonah 2:2-10 | jonah-2-prayer-from-the-belly-of-the-fish | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Prayer of Solomon | 1Kgs 8:22-30 | 1-kings-08-the-dedication-of-the-temple | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Second Praise of Moses | Deut 32:1-42 | deuteronomy-32-the-song-of-moses | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Second Prayer of Isaiah | Isa 25:1-12 | isaiah-24-27-apocalypse-feast-and-resurrection-hope | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Third Prayer of Isaiah | Isa 26:1-9 | isaiah-24-27-apocalypse-feast-and-resurrection-hope | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| PRAISES OF THE PROPHETS | Midnight Praises | Vision of Daniel – Three Youth in the Fiery Furnace | Dan 3:1-23 | prayer-of-azariah-and-song-of-the-three-holy-children-5-bright-saturday | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| 3RD HOUR | 3rd Hour | Prophecy | Jer 13:15-22 | jeremiah-13-the-ruined-linen-girdle-and-bright-saturday-warning | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| 3RD HOUR | 3rd Hour | Psalm | Ps 16:10-11 (LXX Ps 15:10-11) | psalm-16-lxx-15-the-holy-one-who-does-not-see-corruption | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| 6TH HOUR | 6th Hour | Gospel | Matt 5:3-12 | matthew-5-1-16-beatitudes-salt-and-light | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| 6TH HOUR | 6th Hour | Prophecy | Isa 50:10-51:8 | isaiah-51-52-zion-awake-and-good-news | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| 6TH HOUR | 6th Hour | Psalm | Ps 130:1 (LXX Ps 129:1) | psalm-130-lxx-129-out-of-the-depths-i-have-cried | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| 9TH HOUR | 9th Hour | Prophecy | Isa 45:15-20 | isaiah-45-46-cyrus-and-the-lord-alone | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| 9TH HOUR | 9th Hour | Prophecy | Jer 31:31-34 | jeremiah-30-31-book-of-consolation-and-new-covenant | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |
| 9TH HOUR | 9th Hour | Psalm | Ps 41:5,41:10 (LXX Ps 40:5; Ps 40:10) | psalm-41-lxx-40-the-betrayed-friend-and-the-poor-man | covered_by_sourced_theme | Treasures chapter 15; local Bright Saturday service-order rows |

## Metrics

- source_pack_entries: 53
- source_snippets_total: 833
- snippets_by_copyright_status:
  - modern_copyrighted: 586
  - translation_copyrighted: 247
- source_count_by_day_hour:
  - Palm Sunday | Vespers: 3
  - Palm Sunday | Matins: 3
  - Palm Sunday | Liturgy: 3
  - Hosanna Sunday | Ninth Hour: 4
  - Hosanna Sunday | Eleventh Hour: 4
  - Monday Eve | First Hour: 4
  - Monday Eve | Third Hour: 4
  - Monday Eve | Sixth Hour: 4
  - Monday Eve | Ninth Hour: 4
  - Monday Eve | Eleventh Hour: 4
  - Monday | First Hour: 4
  - Monday | Third Hour: 4
  - Monday | Sixth Hour: 4
  - Monday | Ninth Hour: 4
  - Monday | Eleventh Hour: 4
  - Tuesday Eve | First Hour: 4
  - Tuesday Eve | Third Hour: 4
  - Tuesday Eve | Sixth Hour: 4
  - Tuesday Eve | Ninth Hour: 4
  - Tuesday Eve | Eleventh Hour: 4
  - Tuesday | First Hour: 4
  - Tuesday | Third Hour: 4
  - Tuesday | Sixth Hour: 4
  - Tuesday | Ninth Hour: 4
  - Tuesday | Eleventh Hour: 4
  - Wednesday Eve | First Hour: 4
  - Wednesday Eve | Third Hour: 4
  - Wednesday Eve | Sixth Hour: 4
  - Wednesday Eve | Ninth Hour: 4
  - Wednesday Eve | Eleventh Hour: 4
  - Wednesday | First Hour: 4
  - Wednesday | Third Hour: 4
  - Wednesday | Sixth Hour: 4
  - Wednesday | Ninth Hour: 4
  - Wednesday | Eleventh Hour: 4
  - Great Thursday Eve | First Hour: 4
  - Great Thursday Eve | Third Hour: 4
  - Great Thursday Eve | Sixth Hour: 4
  - Great Thursday Eve | Ninth Hour: 4
  - Great Thursday Eve | Eleventh Hour: 4
  - Great Thursday | First Hour: 4
  - Great Thursday | Third Hour: 4
  - Great Thursday | Sixth Hour: 4
  - Great Thursday | Ninth Hour: 4
  - Great Thursday | Eleventh Hour: 4
  - Great Thursday | Liturgy of Blessing of the Water: 4
  - Good Friday | First Hour: 4
  - Good Friday | Third Hour: 4
  - Good Friday | Sixth Hour: 4
  - Good Friday | Ninth Hour: 4
  - Good Friday | Eleventh Hour: 4
  - Good Friday | Twelfth Hour: 4
  - Bright Saturday | Liturgy: 3
