# Open Questions and Decisions for George

This file collects only the questions that thorough research, source comparison, and independent audit could not settle during the autonomous lectionary execution run.

## 2026-06-18 adjudication residue for George and Fr. Boulos

Use this section for a review session with Fr. Boulos where a liturgical or theological ruling is needed. Each item separates sourced evidence, local inference, and what would resolve the question.

### P2 genuine source disagreements

These are not span-format duplicates. They remain open because the competing verse sets or boundaries differ.

1. Great Thursday Eve, Ninth Hour: `Jer 9:6-10` vs `Jer 9:7-11`
   - Competing options: keep `Jer 9:6-10`; keep `Jer 9:7-11`; or preserve both as separate source witnesses until a current authority resolves the boundary.
   - Source situation: SOURCED disagreement inside the repo. The curated/API Pascha layer has `Jer 9:6-10`; the St. Mary Ottawa source-text layer has `Jer 9:7-11` in the same service hour.
   - What would resolve it: current Coptic Reader evidence, a current printed Pascha book, or Fr. Boulos ruling which boundary should be treated as current practice.
2. PRAISES OF THE PROPHETS, Midnight Praises: `Isa 26:9-20` vs `Isa 26:1-9`
   - Competing options: keep `Isa 26:9-20`; keep `Isa 26:1-9`; or preserve both as source-specific rows.
   - Source situation: SOURCED disagreement in local source rows for the same Midnight Praises placement. No controlling external source is encoded in this repo.
   - What would resolve it: the current service book or Coptic Reader source for Praises of the Prophets, plus Fr. Boulos review if both traditions are in active use.
3. Tuesday Eve, First Hour: `Ps 62:7,62:2` vs `Ps 62:7,62:6`
   - Competing options: keep the verse set `{62:7, 62:2}`; keep `{62:7, 62:6}`; or preserve both as source-specific Psalm witnesses.
   - Source situation: SOURCED disagreement after verse-set canonicalization. These are not equal sets, so CHANGE 1 intentionally did not collapse them.
   - What would resolve it: source text or Coptic Reader Psalm text for Tuesday Eve First Hour, with Psalm numbering and verse text checked explicitly.
4. `myron_consecration`, liturgy: `1Jn 5:5-13` vs `1Jn 5:1-21`
   - Competing options: keep the shorter Catholic Epistle `1Jn 5:5-13`; keep the longer `1Jn 5:1-21`; or preserve both until the rite-book source is checked.
   - Source situation: SOURCED disagreement in the local special-service layer. The repo does not encode a decisive external ruling.
   - What would resolve it: the current Myron consecration rite book or another authoritative printed source, followed by Fr. Boulos review if the sources differ.

### P2 inferred merges already applied locally, pending external confirmation

These local cleanups are low-risk because they join contiguous cross-chapter segments from the same source row. They remain flagged as INFERRED until a current external source confirms the continuous form.

1. Tuesday Eve Eleventh Hour: `Mark 13:32-14:2`
   - Applied local merge: `Mark 13:32-37` plus `Mark 14:1-2` became `Mark 13:32-14:2`.
   - Source situation: INFERRED local canonical merge of adjacent same-book segments.
   - What would resolve it: current Coptic Reader or printed Pascha source showing the continuous Mark span.
2. Tuesday Eve Ninth Hour: `Hos 10:12-11:2`
   - Applied local merge: `Hos 10:12-15` plus `Hos 11:1-2` became `Hos 10:12-11:2`.
   - Source situation: INFERRED local canonical merge of adjacent same-book segments.
   - What would resolve it: current Coptic Reader or printed Pascha source showing the continuous Hosea span.
3. Tuesday Eve Sixth Hour: `Hos 4:15-5:7`
   - Applied local merge: `Hos 4:15-19` plus `Hos 5:1-7` became `Hos 4:15-5:7`.
   - Source situation: INFERRED local canonical merge of adjacent same-book segments.
   - What would resolve it: current Coptic Reader or printed Pascha source showing the continuous Hosea span.

### P4 prophecy-ordering confirmation gaps

The order audit has 47 open rows whose order is held from the St. Mary Ottawa source text but not externally cross-confirmed. Summary from `audit_artifacts/slot_overlap_order_2026_06_18/problem4_pascha_prophecy_ordering.md`:

- `open_items`: 47
- `source_text_only_open`: 44
- `open_no_source_match`: 3
- `mismatches_after_fix`: 0

Review path: use `audit_artifacts/slot_overlap_order_2026_06_18/problem4_pascha_prophecy_ordering.md` as the row-level review agenda. What would resolve the group is a current Coptic Reader or curated/API source that confirms each source-text-only prophecy's order, or a ruling that St. Mary source-text order is sufficient for these rows.

## Youssef 15 weeks or 107 days

ACCOT confirms the wording `(15 weeks or 107 days)`. Since 15 weeks is 105 days, the article reports Youssef's figure as given and notes the arithmetic issue.

## Youssef 69 roster verification

Open item: verify the reading-by-reading roster mapping between Youssef's 69 foundational reading collections, arranged by kind of feast and commemoration, and the Ottawa Katameros of the Days table-of-contents entries, which are dated sections. Current verdict is `INFERRED_LIKELY_SAME_SET` (roster unverified). Read from source: Youssef gives 69 collections by commemoration type in volume two of the Yearly Katameros. Read from source: Ottawa presents 69 dated TOC entries in the weekday-and-feast volume. Inferred: alignment rests on shared source tradition, volume two placement, category match, and count.

## Psalm numbering text-equivalence review

The active execution brief states that the Coptic Reader Wednesday Day fixture is faithful to the screenshots, including Third Hour `Psalm 41` and Sixth Hour `Psalm 83`, and that Coptic Reader governs where external books disagree. During Phase 1, Brenton/KJV seam checks resolved several exact pairs: LXX `Ps 41:6` to MT `Ps 42:5`, LXX `Ps 83:2` to MT `Ps 84:1`, and LXX `Ps 83:5` to MT `Ps 84:4`.

Decision needed later: before presenting Third Hour `Psalm 41:1` as an exact MT-primary reference, compare the fixture Psalm text against Brenton and a public-domain MT text. Until then, the design layer preserves the Coptic Reader LXX label and marks the exact MT equivalence as unresolved.

## Coptic Reader coverage beyond Wednesday Day

The repo has a locked Coptic Reader fixture for Pascha Wednesday Day only. Current-vs-historical classifications outside that fixture are marked as candidates unless supported by other current sources. Do not treat them as fully Coptic Reader confirmed.

## Pascha removed-reading candidates

Rows absent from the Wednesday Day Coptic Reader fixture but present in older or local Pascha data are classified as `historical_candidate_removed` in `out/design/temporal_classification.csv`. Only the passages named in George's removed-marker instruction receive `removed_marker`; other old-edition-only rows remain review candidates without that marker. George or a liturgical reviewer should decide whether each unmarked candidate is truly removed, a named-reading equivalent, or a fixture scope issue.

Marker-format decision: this run keeps `removed_marker` as a uniform prose-pattern string that includes the older source and current comparator. A later model pass should decide whether to keep that pattern or split it into a single controlled token plus a separate note field.

## Phase 7 Step 4 data-review findings

- Proverbs 4 duplicate: `Prov 4:4-27,5:1-4` and `Prov 4:4-5:4` are the same continuous Proverbs span, stored two ways. The generator now normalizes the compact form to the explicit two-segment form, so the Wednesday Third Hour historical reading is one identity while retaining source-row provenance.
- Job span review: `Job 27:16-20` plus `Job 28:1-2` and `Job 27:16-28:2` are not silently deduped. The older Ottawa source gives `Job 27:16-28:2` in Wednesday Third Hour, the local corrected day/hour row gives `Job 27:16-20; Job 28:1-2` in Wednesday Sixth Hour, and the Coptic Reader fixture gives only named `Memoirs of Job` in Wednesday Sixth Hour without verse boundaries. This needs source review before any merge.
- Proverbs 1 review: older Ottawa gives Wednesday Ninth Hour `Prov 1:10-33`, while the current Coptic Reader fixture and local corrected day/hour row give `Prov 1:11-35`. These are treated as older-source and current-source variants of one slot, not one double-counted row. Current `Prov 1:11-35` is retained; older `Prov 1:10-33` remains historical.
- Wisdom review: `Wis 1:20-2:15` and `Wis 3:12-24` are API-only old-edition candidates. The repo parser maps `Wis` to Wisdom of Solomon, while Sirach is separately modeled as `Sir`; no evidence in this repo proves those two `Wis` rows are Sirach. They remain unmarked candidate-removed rows pending source review.

## Temporal residue summary

See `out/design/temporal_residue.csv` and `out/design/temporal_residue_manifest.csv` for the full row-level list and counts. Counts by residue type:
- `candidate_removed_needs_current_authority_confirmation`: 22
- `current_authority_pending`: 249
- `historical_witness_no_current_comparator`: 141
- `psalm_equivalence_unresolved`: 5
- `true_source_disagreement`: 0

No true source-disagreement class was emitted in this run. Unsettled rows are classified as pending authority, historical witness without current comparator, candidate removed, or Psalm-equivalence unresolved.

### Rows with `removed_marker` populated by George's list

- Monday | First Hour | Gen 2:1-3 | superseded by rid_1799bfb4477d9a219633
- Monday | First Hour | Gen 1:1-31 | superseded by rid_1799bfb4477d9a219633
- Monday | Ninth Hour | Gen 3:1-24 | superseded by rid_08ac8d6676963ff43fe0
- Monday | Ninth Hour | Gen 2:15-25 | superseded by rid_08ac8d6676963ff43fe0
- Tuesday | First Hour | Job 23:2-17 | superseded by rid_6546e2768925e859a2a6
- Tuesday | First Hour | Job 24:1-25 | superseded by rid_6546e2768925e859a2a6
- Tuesday Eve | Eleventh Hour | Mark 14:1-2 | superseded by rid_74d26750970f7379d7af
- Tuesday Eve | Eleventh Hour | Mark 13:32-37 | superseded by rid_74d26750970f7379d7af
- Tuesday Eve | Ninth Hour | Hos 10:12-15 | superseded by rid_bfa3449dafe309ebcb10
- Tuesday Eve | Ninth Hour | Hos 11:1-2 | superseded by rid_bfa3449dafe309ebcb10
- Tuesday Eve | Sixth Hour | Hos 4:15-19 | superseded by rid_6375e2206441e7c82c00
- Tuesday Eve | Sixth Hour | Hos 5:1-7 | superseded by rid_6375e2206441e7c82c00
- Wednesday | Ninth Hour | Isa 48:1-6 | (removed, attested St. Mary Ottawa Holy Pascha p. 308 line 7779 as Isa 48:1-6; absent from Coptic Reader Wednesday Day fixture supplied by George)
- Wednesday | Ninth Hour | Isa 59:1-17 | (removed, attested St. Mary Ottawa Holy Pascha p. 320 line 8091 as Isa 59:1-17; absent from Coptic Reader Wednesday Day fixture supplied by George)
- Wednesday | Ninth Hour | Prov 1:10-33 | (removed, attested St. Mary Ottawa Holy Pascha p. 318 line 8038 as Prov 1:10-33; absent from Coptic Reader Wednesday Day fixture supplied by George)
- Wednesday | Ninth Hour | Zech 11:11-14 | (removed, attested St. Mary Ottawa Holy Pascha p. 322 line 8133 as Zech 11:11-14; absent from Coptic Reader Wednesday Day fixture supplied by George)
- Wednesday | Sixth Hour | Job 28:1-2 | (removed, attested St. Mary Ottawa Holy Pascha p. 298 line 7519 as Job 27:16-28:2; absent from Coptic Reader Wednesday Day fixture supplied by George)
- Wednesday | Sixth Hour | Job 27:16-20 | (removed, attested St. Mary Ottawa Holy Pascha p. 298 line 7519 as Job 27:16-28:2; absent from Coptic Reader Wednesday Day fixture supplied by George)
- Wednesday | Third Hour | Prov 4:4-27,5:1-4 | (removed, attested St. Mary Ottawa Holy Pascha p. 299 line 7552 as Prov 4:4-27,5:1-4; absent from Coptic Reader Wednesday Day fixture supplied by George)
- Wednesday | Third Hour | Job 27:16-28:2 | (removed, attested St. Mary Ottawa Holy Pascha p. 298 line 7519 as Job 27:16-28:2; absent from Coptic Reader Wednesday Day fixture supplied by George)

### Other old-edition-only candidate-removed rows needing review

- Wednesday | First Hour | Wis 1:20-2:15 | Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture.
- Wednesday | First Hour | Wis 3:12-24 | Present in older/local Pascha data but absent from the scoped Coptic Reader Wednesday Day fixture.

### Psalm equivalence unresolved rows

- Wednesday | Eleventh Hour | Ps 6:2-3 | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 6:2-3; Ps 69:17; John 12:27-36
- Wednesday | Eleventh Hour | Ps 69:17 (LXX Ps 68:17) | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 6:2-3; Ps 69:17; John 12:27-36
- Wednesday | Ninth Hour | Ps 41:5-6 (LXX Ps 40:5-6) | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 41:5-6; Matt 26:3-16
- Wednesday | Sixth Hour | Ps 83:2,83:5 (LXX Ps 82:2; Ps 82:5) | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 83:2,5; John 12:1-8
- Wednesday | Third Hour | Ps 41:1,41:6 (LXX Ps 40:1; Ps 40:6) | Psalm row kept unresolved because source label, verse boundary, or bundled Psalm+Gospel extraction does not yet have an encoded Brenton/KJV text-equivalence match. Source refs: Ps 41:6,1; Luke 22:1-6

### Current-authority pending class

There are 249 rows not checked by a captured Coptic Reader fixture and not confirmed by two independent sources. Use `out/design/temporal_residue.csv` for the full list. Sample rows:
- Bright Saturday | Liturgy | 1Cor 15:1-22
- Bright Saturday | Liturgy | Acts 3:12-21
- Bright Saturday | Liturgy | Matt 28:1-20
- Bright Saturday | Liturgy | Ps 3:3,3:5
- Bright Saturday | Liturgy | 1Pet 1:1-9
- Bright Saturday | Liturgy | Ps 82:8 (LXX Ps 81:8)
- Good Friday | Eleventh Hour | Jer 12:1-14
- Good Friday | Eleventh Hour | Matt 27:51-56
- Good Friday | Eleventh Hour | Isa 3:5-12
- Good Friday | Eleventh Hour | Lk 23:47-49
- Good Friday | Eleventh Hour | Mark 15:38-41
- Good Friday | Eleventh Hour | Jn 19:31-37
- Good Friday | Eleventh Hour | Ps 143:6-7 (LXX Ps 142:6-7)
- Good Friday | Eleventh Hour | Ps 31:5 (LXX Ps 30:5)
- Good Friday | First Hour | Deut 8:19-9:24
- Good Friday | First Hour | Jn 18:28-40
- Good Friday | First Hour | Ps 35:11-12,35:16 (LXX Ps 34:11-12; Ps 34:16)
- Good Friday | First Hour | Job 12:18-13:1
- Good Friday | First Hour | Isa 24:1-13
- Good Friday | First Hour | Mic 7:1-8
- Good Friday | First Hour | Isa 1:2-9
- Good Friday | First Hour | Wis 2:12-22
- Good Friday | First Hour | Ps 27:12 (LXX Ps 26:12)
- Good Friday | First Hour | Jer 22:29-23:6
- Good Friday | First Hour | Mark 15:1-5
- ... 224 more current-authority pending rows.


## Synaxarium bridge review

The bridge links the primary commemoration of each fixed Coptic day to that day's Katameros readings. After Step 7, rows whose Coptic day is in the Ottawa/UKMID 69 dated-entry bridge taxonomy are `basis=explicit` and `confidence=high`. Rows outside that taxonomy remain uniformly `basis=collection-type` and `confidence=medium`. These rows are discovery links, not direct proper-reading proof and not a resolved daily service schedule.

Bridge differentiation flag: outside the Ottawa 69 dated-entry bridge taxonomy, the bridge is still uniformly collection-type. A later pass should decide whether more non-taxonomy days can be classified explicitly, left as collection-type, or marked inferred.

Ottawa taxonomy coverage flag: 11 of the 69 Ottawa dated entries have no emitted bridge rows in this run, because the bridge only emits days that have both a Synaxarium primary commemoration row and local fixed-day Katameros rows. Missing Ottawa dated entries:
- Baramoudah 23 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 388
- Baramoudah 27 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 396
- Baramoudah 30 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 404
- Misra 3 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 507
- Misra 13 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 515
- Misra 17 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 524
- Misra 25 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 532
- Misra 26 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 540
- Misra 28 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 547
- Misra 29 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 555
- Misra 30 | TOC dated reading section, PDF pages 23 to 26; section begins on printed page 562

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
- Reverse lectionary occasion index: `out/design/reverse_lectionary_index.jsonl`
- Daily readings files: `out/design/daily/lectionary-YYYY.json`
- Passage footprint dataset: `out/design/passage_liturgical_footprint.csv` and `.jsonl`
- Synaxarium datasets: `out/design/synaxarium_commemorations.csv` and `out/design/synaxarium_reading_bridge.csv`
- Deck deliverables: `presentation/lectionary_design_layer_deck.pptx` and `presentation/lectionary_design_layer_deck_outline.md`
- Execution log: `audit_artifacts/lectionary_execution_log.md`
