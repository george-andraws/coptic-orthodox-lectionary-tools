# Open Questions and Decisions for George

This file collects only the questions that thorough research, source comparison, and independent audit could not settle during the autonomous lectionary execution run.

## Psalm numbering text-equivalence review

The active execution brief states that the Coptic Reader Wednesday Day fixture is faithful to the screenshots, including Third Hour `Psalm 41` and Sixth Hour `Psalm 83`, and that Coptic Reader governs where external books disagree. During Phase 1, Brenton/KJV seam checks resolved several exact pairs: LXX `Ps 41:6` to MT `Ps 42:5`, LXX `Ps 83:2` to MT `Ps 84:1`, and LXX `Ps 83:5` to MT `Ps 84:4`.

Decision needed later: before presenting Third Hour `Psalm 41:1` as an exact MT-primary reference, compare the fixture Psalm text against Brenton and a public-domain MT text. Until then, the design layer preserves the Coptic Reader LXX label and marks the exact MT equivalence as unresolved.

## Full list of F.N. Youssef's 69 collections

The accessible source confirms the lectionary is arranged into 69 collections by feast or commemoration type, but the full English enumerated list was not available in the source text retrieved in this run. The schema stores the confirmed count and a working type vocabulary. The full list should be entered when a reliable source is available.

## Coptic Reader coverage beyond Wednesday Day

The repo has a locked Coptic Reader fixture for Pascha Wednesday Day only. Current-vs-historical classifications outside that fixture are marked as candidates unless supported by other current sources. Do not treat them as fully Coptic Reader confirmed.

## Pascha removed-reading candidates

Rows absent from the Wednesday Day Coptic Reader fixture but present in older or local Pascha data are classified as `historical_candidate_removed` in `out/design/temporal_classification.csv`. George or a liturgical reviewer should decide whether each is truly removed, a named-reading equivalent, or a fixture scope issue.

## Synaxarium bridge review

The bridge links the primary commemoration of each fixed Coptic day to that day's Katameros readings with basis `collection-type`. Multi-commemoration days are confidence `medium`, because secondary commemorations may have proper readings only in sources not ingested here.

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
