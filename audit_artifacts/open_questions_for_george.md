# Open Questions and Decisions for George

This file collects only the questions that thorough research, source comparison, and independent audit could not settle during the autonomous lectionary execution run.

## Pascha shared-date source check

Step 2a found reliable support for the Nicene Paschal norm and the Alexandrian calculation history in the WCC/MECC Aleppo statement, but did not find a clean source stating that the Coptic Pascha always falls on the same date as Eastern Orthodox Pascha. The article therefore clarifies the computus and the present-day Hebrew-calendar issue only. Add the shared-date clause later only if a reliable source states it clearly.

## Step 2d bibliographic locator checks

- Burmester page span: The run did not confirm the requested pages 83 to 137 for O.H.E. Burmester, "The Coptic-Greek-Arabic Holy Week Lectionary from Scetis," in `Bulletin de la Societe d'Archeologie Copte XVI, 1961-1962`. Leave the citation without the page span until a catalog scan or article PDF confirms it.
- Zanetti series and year: Open Library records `Les lectionnaires coptes annuels: Basse-Egypte` as Publications de l'Institut orientaliste de Louvain 33, 1985. The Coptic Encyclopedia PDF bibliography for `Lectionary` cites Publications de l'Institut orientaliste de Louvain 31, 1988. Because these conflict, the article does not add a series number or year yet.
- Youssef 15 weeks or 107 days: ACCOT confirms the wording `(15 weeks or 107 days)`. Since 15 weeks is 105 days, the article reports Youssef's figure as given and notes the arithmetic issue.

## Psalm numbering text-equivalence review

The active execution brief states that the Coptic Reader Wednesday Day fixture is faithful to the screenshots, including Third Hour `Psalm 41` and Sixth Hour `Psalm 83`, and that Coptic Reader governs where external books disagree. During Phase 1, Brenton/KJV seam checks resolved several exact pairs: LXX `Ps 41:6` to MT `Ps 42:5`, LXX `Ps 83:2` to MT `Ps 84:1`, and LXX `Ps 83:5` to MT `Ps 84:4`.

Decision needed later: before presenting Third Hour `Psalm 41:1` as an exact MT-primary reference, compare the fixture Psalm text against Brenton and a public-domain MT text. Until then, the design layer preserves the Coptic Reader LXX label and marks the exact MT equivalence as unresolved.

## Coptic Reader coverage beyond Wednesday Day

The repo has a locked Coptic Reader fixture for Pascha Wednesday Day only. Current-vs-historical classifications outside that fixture are marked as candidates unless supported by other current sources. Do not treat them as fully Coptic Reader confirmed.

## Pascha removed-reading candidates

Rows absent from the Wednesday Day Coptic Reader fixture but present in older or local Pascha data are classified as `historical_candidate_removed` in `out/design/temporal_classification.csv`. George or a liturgical reviewer should decide whether each is truly removed, a named-reading equivalent, or a fixture scope issue.

## Temporal residue summary

See `out/design/temporal_residue.csv` and `out/design/temporal_residue_manifest.csv` for the full row-level list and counts. Counts by residue type:
- `candidate_removed_needs_current_authority_confirmation`: 7
- `current_authority_pending`: 255
- `historical_witness_no_current_comparator`: 152
- `psalm_equivalence_unresolved`: 5
- `true_source_disagreement`: 0

No true source-disagreement class was emitted in this run. Unsettled rows are classified as pending authority, historical witness without current comparator, candidate removed, or Psalm-equivalence unresolved.

### Candidate removed readings needing current-authority confirmation

- Wednesday | First Hour | Wis 1:20-2:15 | Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture.
- Wednesday | First Hour | Wis 3:12-24 | Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture.
- Wednesday | Ninth Hour | Isa 59:1-17 | Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture.
- Wednesday | Ninth Hour | Zech 11:11-14 | Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture.
- Wednesday | Sixth Hour | Job 28:1-2 | Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture.
- Wednesday | Sixth Hour | Job 27:16-20 | Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture.
- Wednesday | Third Hour | Prov 4:4-5:4 | Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture.

### Psalm equivalence unresolved rows

- Wednesday | Eleventh Hour | Ps 6:2-3 | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 6:2-3; Ps 69:17; John 12:27-36
- Wednesday | Eleventh Hour | Ps 69:17 (LXX Ps 68:17) | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 6:2-3; Ps 69:17; John 12:27-36
- Wednesday | Ninth Hour | Ps 41:5-6 (LXX Ps 40:5-6) | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 41:5-6; Matt 26:3-16
- Wednesday | Sixth Hour | Ps 83:2,83:5 (LXX Ps 82:2; Ps 82:5) | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 83:2,5; John 12:1-8
- Wednesday | Third Hour | Ps 41:6,41:1 (LXX Ps 40:6; Ps 40:1) | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 41:6,1; Luke 22:1-6

### Current-authority pending class

There are 255 rows not checked by a captured Coptic Reader fixture and not confirmed by two independent sources. Use `out/design/temporal_residue.csv` for the full list. Sample rows:
- Bright Saturday | Liturgy | Ps 3:5,3:3
- Bright Saturday | Liturgy | 1Cor 15:1-22
- Bright Saturday | Liturgy | Acts 3:12-21
- Bright Saturday | Liturgy | Matt 28:1-20
- Bright Saturday | Liturgy | 1Pet 1:1-9
- Bright Saturday | Liturgy | Ps 82:8 (LXX Ps 81:8)
- Good Friday | Eleventh Hour | Jer 12:1-14
- Good Friday | Eleventh Hour | Matt 27:51-56
- Good Friday | Eleventh Hour | Isa 3:5-12
- Good Friday | Eleventh Hour | Lk 23:47-49
- Good Friday | Eleventh Hour | Mark 15:38-41
- Good Friday | Eleventh Hour | Jn 19:31-37
- Good Friday | Eleventh Hour | Ps 31:5 (LXX Ps 30:5)
- Good Friday | Eleventh Hour | Ps 143:6,143:7 (LXX Ps 142:6; Ps 142:7)
- Good Friday | First Hour | Deut 8:19-9:24
- Good Friday | First Hour | Jn 18:28-40
- Good Friday | First Hour | Job 12:18-13:1
- Good Friday | First Hour | Isa 24:1-13
- Good Friday | First Hour | Mic 7:1-8
- Good Friday | First Hour | Ps 35:11,35:12,35:16 (LXX Ps 34:11; Ps 34:12; Ps 34:16)
- Good Friday | First Hour | Isa 1:2-9
- Good Friday | First Hour | Wis 2:12-22
- Good Friday | First Hour | Ps 27:12 (LXX Ps 26:12)
- Good Friday | First Hour | Jer 22:29-23:6
- Good Friday | First Hour | Mark 15:1-5
- ... 230 more current-authority pending rows.


## Synaxarium bridge review

The bridge links the primary commemoration of each fixed Coptic day to that day's Katameros readings with basis `collection-type` and confidence `medium`. These rows are discovery links, not direct proper-reading proof and not a resolved daily service schedule.

All repeated-slot groups are documented in `out/design/synaxarium_reading_bridge.csv` row notes as source-row or variant catalog entries.

- Multi-commemoration days needing future ecclesiastical or source review: 221 days.
  - Abib 1
  - Abib 10
  - Abib 11
  - Abib 12
  - Abib 13
  - Abib 14
  - Abib 15
  - Abib 16
  - Abib 19
  - Abib 21
  - Abib 22
  - Abib 23
  - Abib 24
  - Abib 25
  - Abib 26
  - Abib 27
  - Abib 29
  - Abib 3
  - Abib 6
  - Abib 7
  - Abib 8
  - Abib 9
  - Al-Nasi 1
  - Al-Nasi 3
  - Al-Nasi 4
  - Al-Nasi 5
  - Amshir 10
  - Amshir 12
  - Amshir 13
  - Amshir 14
  - Amshir 15
  - Amshir 2
  - Amshir 20
  - Amshir 21
  - Amshir 24
  - Amshir 25
  - Amshir 26
  - Amshir 5
  - Amshir 6
  - Amshir 7
  - Amshir 9
  - Babah 11
  - Babah 12
  - Babah 16
  - Babah 19
  - Babah 21
  - Babah 23
  - Babah 24
  - Babah 25
  - Babah 26
  - Babah 3
  - Babah 30
  - Babah 8
  - Babah 9
  - Baramhat 1
  - Baramhat 12
  - Baramhat 13
  - Baramhat 14
  - Baramhat 15
  - Baramhat 17
  - Baramhat 19
  - Baramhat 20
  - Baramhat 21
  - Baramhat 22
  - Baramhat 24
  - Baramhat 25
  - Baramhat 26
  - Baramhat 27
  - Baramhat 28
  - Baramhat 29
  - Baramhat 3
  - Baramhat 30
  - Baramhat 4
  - Baramhat 5
  - Baramhat 6
  - Baramhat 7
  - Baramhat 8
  - Baramhat 9
  - Baramoudah 1
  - Baramoudah 10
  - Baramoudah 11
  - Baramoudah 12
  - Baramoudah 13
  - Baramoudah 15
  - Baramoudah 19
  - Baramoudah 2
  - Baramoudah 21
  - Baramoudah 22
  - Baramoudah 24
  - Baramoudah 25
  - Baramoudah 26
  - Baramoudah 29
  - Baramoudah 3
  - Baramoudah 5
  - Baramoudah 6
  - Baramoudah 7
  - Baramoudah 8
  - Baramoudah 9
  - Bashans 11
  - Bashans 12
  - Bashans 14
  - Bashans 15
  - Bashans 18
  - Bashans 19
  - Bashans 2
  - Bashans 21
  - Bashans 23
  - Bashans 24
  - Bashans 25
  - Bashans 27
  - Bashans 3
  - Bashans 30
  - Bashans 4
  - Bashans 6
  - Bashans 8
  - Bashans 9
  - Baunah 1
  - Baunah 10
  - Baunah 11
  - Baunah 12
  - ... 101 more days. See out/design/synaxarium_commemorations.csv.

## Low-confidence bridge rows

No bridge rows were emitted with `basis=inferred` or `confidence=low`. Medium-confidence multi-commemoration days are listed above.

## Site corpus joins not available in this repo

The presentation footprint output includes blank `patristic_homily_slug` values because Hermes did not have access to `coptic-corpus`. Join homily, chapter-study, and audio slugs in the site repo before publishing those UI links.

## Final push package pointers

- Article markdown: `coptic-lectionary-and-synaxarium.md`
- Site integration spec: `site_integration_spec.md`
- Presentation dataset: `out/design/reverse_lectionary_presentation.csv` and `.jsonl`
- Today's readings snapshot: `out/design/todays_readings_current_practice.csv` and `.jsonl`
- Passage footprint dataset: `out/design/passage_liturgical_footprint.csv` and `.jsonl`
- Synaxarium datasets: `out/design/synaxarium_commemorations.csv` and `out/design/synaxarium_reading_bridge.csv`
- Deck deliverables: `presentation/lectionary_design_layer_deck.pptx` and `presentation/lectionary_design_layer_deck_outline.md`
- Execution log: `audit_artifacts/lectionary_execution_log.md`
