# 05 — Coptic Lectionary: Design & Hermes Execution Brief

This file is both the design for an accurate, usable Coptic lectionary dataset and the
execution brief for the **Hermes** agent to carry it out end to end. Hermes acts as an
**orchestrator**: it reads this file, runs the phases in order, spawns subagent instances or uses
`delegate_task` as needed, runs an independent audit at each checkpoint, and proceeds autonomously
to completion WITHOUT stopping to ask George. Goal: a lectionary that is accurate, usable as a
Bible-study and spiritual reference, and properly structured, plus a published article explaining
the lectionary and synaxarium.

---

## 0. How Hermes should run this

### 0.1 Role
Orchestrator. Drive all phases to completion. Do not stop for George mid-run (see 0.4).

### 0.2 Model assignments (fixed by role, reasoning=xhigh in all cases)
- **`openai-codex/gpt-5.5`, reasoning=xhigh** — article generation and all data analysis: schema
  design, the re-key/migration logic, attestation and reconciliation computation, the
  synaxarium-to-lectionary bridge reasoning.
- **`xai-oauth/grok-4.3`, reasoning=xhigh** — research, web search, data ingestion (source
  extraction), and independent audits/reviews of plans and data designs.

**Independence rule (this is the point of having two models):** an audit is ALWAYS performed by
the model that did NOT produce the artifact under review.
- Grok-4.3 audits everything Codex produces: the article, the spec, the schema, the migration,
  the attestation logic, the temporal classification, the bridge reasoning.
- Codex/gpt-5.5 audits what Grok produces: the ingested/extracted source data and the research
  compilation. (Grok cannot independently audit its own ingestion, so that audit goes to Codex.)

Full subagent instances do the substantive work at xhigh. `delegate_task` is for bounded
mechanical sub-steps within a role (extraction loops, dedup, numbering conversion, running tests,
committing). If a `delegate_task` limit blocks the scope, fall back to a full instance of the
role's assigned model.

### 0.3 Audit protocol
At each checkpoint named in Section 6, run an independent audit:
1. The non-producing model (per 0.2), at reasoning=xhigh, reviews the artifact against the phase
   acceptance criteria, the source registry (Section 5), and the locked decisions (Section 2). It
   returns concrete, specific suggested revisions, not a pass/fail blessing.
2. The orchestrator considers the revisions and updates the artifact before proceeding.
3. If the audit finds too many fundamental issues, the orchestrator revises and RE-RUNS the audit.
   The audit may be re-run at most **twice** (three audit passes total per checkpoint). After the
   third pass, proceed regardless and record every remaining issue in the end-of-run Open Questions
   list (Section 8).
4. Record each audit pass in the execution log: findings, revisions made, and outcome.

### 0.4 Autonomy: run to done, do not stop for George
With the model assignments and the independent audits in place, the audits are the quality gates,
not George. Run all phases to completion without pausing for human input. Research thoroughly and
resolve your own questions before deferring any. It is acceptable to finish with a small set of
genuine ambiguities or decisions that thorough research could not settle. Collect those into ONE
end-of-run "Open Questions and Decisions for George" document (Section 8). Do not ask one at a
time, and do not stop mid-run.

### 0.5 Execution log (required)
Maintain `audit_artifacts/lectionary_execution_log.md`. For every task record: phase, what was
done, model/role used, subagent-vs-delegate choice and why, sources used, audit passes and their
outcomes, commit hash, acceptance result, and any open question.

### 0.6 Commit discipline
One logical change per commit. No bundling of unrelated changes. Proceed across commits and phases
autonomously.

### 0.7 Verification discipline (these caught real failures, keep them)
- A site claim verified with a cache-buster (`?cb=`) only proves the origin updated. Acceptance is
  the plain URL from a fresh browser/network. (Site go-live is George's step; see Phase 6.)
- Test features the way a human uses them (type into the real input), not the way the engine prefers.
- "Works locally, broken on prod" almost always means gitignored files. Force a fresh-clone build.
- Do not treat a passing verifier check as proof of correctness if the check encodes pre-fix
  expectations (several Pascha checks do; see Section 3).

### 0.8 Content rules for anything generated (article, notes, summaries)
- No em dashes. Use commas, periods, or "...".
- Avoid: delve, multifaceted, additionally, landscape, underscore, foster, interplay.
- Research Coptic-specific content from named sources, do not generate from memory.
- Ground claims in NAMED Church Fathers (Cyril of Alexandria, Athanasius, John Chrysostom, the
  Gregories, Ephrem), not "the Fathers."
- Two errors never to repeat: deacons serve the LORD (not "the congregation"); Christ was NOT
  "helpless" in the Passion (it was sovereign, willing obedience).
- Distinguish "read from the source" from "inferred." Flag inferences.
- Pascha framing: the Coptic Pascha is fixed by the Church's own Alexandrian computation
  standardized at the Council of Nicaea and falls on the SAME date as the Eastern Orthodox Pascha.
  When a source says the Resurrection "follows the Hebrew calendar" (Youssef does), keep the source's
  wording but never let the article imply the date is looked up from the modern rabbinic calendar or
  differs from the other Orthodox churches.
- Traditional attributions: the Abuqti calculation and its ascription to Ptolemy al-Farmawi in the
  time of Pope Demetrius the Vinedresser is a traditional attribution, not established history.
  Attribute it to the source ("Youssef says...") and mark it traditional; do not state it as fact.
- NKJV is used for VERSIFICATION (the numbering shown in references), not as reproduced text. Do not
  reproduce copyrighted NKJV verse text in the public-repo article; cite versification only.

---

## 1. Project context

- **Site:** Light and Logos, https://andraws.net. Coptic Orthodox Bible study. Quartz 5 static
  site, Cloudflare Workers, audio on R2 at media.andraws.net. Site repo: `coptic-corpus`.
- **Lectionary data repo:** `coptic-lectionary-research` (local path uses `/Users/georgeandraws/...`
  for native agents). Contains the ingestion/build scripts (`build_lectionary_reference.py`,
  `build_lectionary_crosswalk.py`, `build_bible_chapter_lectionary_index.py`,
  `build_pascha_source_text_index.py`), the occurrence CSV (~71k rows),
  `reverse_lookup_crosswalk.csv`, the local Katameros SQLite
  (`sources/katameros-api/Core/KatamerosDatabase.db`), `query_lectionary.py`, and
  `verify_lectionary_queries.py`.
- **Repo access:** Hermes works ONLY in `coptic-lectionary-research`. It does NOT have access to
  the `coptic-corpus` site repo. All site-facing deliverables (the article, the presentation data)
  are produced as files here; George does the final push to production.
- **Signature feature:** the reverse lectionary (passage -> every liturgical day/service where it
  is read), the inverse of the usual date -> readings tools.

---

## 2. Locked decisions

1. **Numbering:** primary references match modern English Bibles (NKJV / Masoretic). Where the
   Septuagint differs, annotate inline, e.g. `Psalm 51:1 (LXX Ps 50:1)`. Applies especially to
   Psalms and the deuterocanonical books. Display is MT-primary; an internal, convention-proof
   identity key resolves both so cross-source matching still works.
2. **Temporal / removed-readings tracking:** populate for Pascha only for now. The model must be
   occasion-agnostic so that if other altered services are found later, it is data entry, not a
   redesign.
3. **Synaxarium:** include full sanctoral readings. Per F.N. Youssef, the daily readings follow the
   Synaxarium, so the synaxarium is the index of the daily cycle, not a bolt-on.
4. **Authority tiers:** Coptic Reader (Diocese of the Southern US) is the authority for CURRENT
   practice. Older printed books are witnesses for the HISTORICAL layer.
5. **Text validation:** validate references against public-domain text (Brenton Septuagint for
   Psalms, a public-domain Bible such as WEB or KJV for prophecies and gospels). Do NOT store full
   copyrighted Bible text (NKJV, NRSV) in this public repo.

---

## 3. Carried findings (do not redo these)

- **Coptic Reader** content is encrypted Flutter assets (no plaintext readings endpoint). MANUAL
  comparator only: readings captured by screenshot and entered as fixtures. Used in prior Hermes
  sessions as a browse reference, never as a committed pipeline.
- **Katameros API** (`api.katameros.app`) DOES cover the Pascha hours via the live endpoint (the
  local SQLite copy does not). Returns Masoretic/NKJV numbering. Scored ~54% against the Coptic
  Reader Wednesday fixture.
- **St. Mary source-text index** (`build_pascha_source_text_index.py`) has parser/header bugs and
  scored ~58% against the fixture. Suspect until repaired.
- **The stored dataset is uniformly MT/NKJV numbered** across Pascha and Katameros-cycle rows. NOT
  internally mixed. (Spot-confirm any St. Mary-sourced rows during re-keying.)
- **The "extra" readings the dataset has on Pascha Wednesday that Coptic Reader lacks (Isaiah
  48:1-6, Isaiah 59:1-17, Zechariah 11:11-14, extra Proverbs, Job 27-28) are most likely the
  REMOVED readings, not errors.** Built from older sources, so it carries the older fuller
  lectionary. Classify as historical, do not delete as bugs.
- **Phase 2a (done):** removed the duplicated Great Lent row (kept `Id=46` `Ps 63:1`, dropped
  `Id=53` `Ps 63:1 + Ps 64:2-4`), fixed Hatur 8 segmentation (`19.68:17,16,17` no longer emits
  Ps 68:17 twice), added duplicate-tuple and Hatur 8 guards. Both decisions were on MT/NKJV labels
  and need re-confirmation under the canonical identity key (Katameros "Ps 63" is LXX 62).
- **LXX<->MT offset is not chapter-only.** It also shifts verses inside a psalm because the LXX
  counts the superscription as verses (LXX Ps 50:6 lines up with MT Ps 51:4). The crosswalk must
  handle both the psalm-number seam and the within-psalm verse offset. Brenton text comparison
  sidesteps this.
- **The 69 "foundational readings" (al-qira'at al-asasiyya) need set-identity confirmation, not just
  a count.** Youssef names 69 foundational readings in volume two of the Yearly Katameros; the Ottawa
  Katameros of the Days table of contents yields 69 dated feast/commemoration sets. The matching
  count is suggestive, NOT proof the two are the same 69 entries. Confirm membership before the
  article or the bridge states them as the same set. Store the 69 as a controlled vocabulary with
  provenance (source, edition, locator) once settled.
- **The Phase 5 bridge came out uniformly `collection-type` / medium confidence across all rows
  (~4,688).** That uniformity is suspect: a bridge that differentiates should not put every link in
  one bucket. The days covered by the 69 foundational reading sets should be `basis=explicit` with
  the Ottawa citation. If, after that upgrade, the rest is still uniform, flag it as a sign the bridge
  is not differentiating rather than rebuilding it blind.
- **Autonomous article output ran THIN.** The first autonomous Phase 0 article omitted the Abuqti
  calculation, the three seasons, the movable middle season, the Sunday program specifics, the
  7 Major / 7 Minor / 2 Cross feasts, and the 69 entirely. Model-only generation is not a substitute
  for source-grounded research; every structural claim in the article needs a named-source citation.

---

## 4. Target data model (ideal design)

**4.1 Reading identity (numbering-proof).** Each reading is a first-class record:
- `display_ref`: MT/NKJV primary, with LXX annotation where it differs (`Psalm 51:1 (LXX Ps 50:1)`).
- `identity_key`: a canonical verse-set identity independent of label, so two sources match even
  when their numbers differ. Anchor to Brenton (LXX) text for Psalms.
- `type`: scripture | named-reading | homily | hymn/praise | exposition | litany. Only scripture
  types enter the passage index; the rest are liturgical context.
- Composite/non-contiguous references are an ordered list of verse-spans (e.g. Ps 50:6 + Ps 32:10),
  not a single range.
- Named readings (e.g. "Memoirs of Job") carry a resolved passage where one exists.

**4.2 Liturgical placement (retire the lossy slots).**
`occasion -> service (eve/day, or Vespers/Matins/Liturgy) -> hour (1/3/6/9/11/12) -> slot
(prophecy-1..n, psalm, gospel; for liturgy days pauline/catholicon/praxis) -> order`. Replaces
`OT1/OT2` and the collapsed `Psalm+Gospel`.

**4.3 Temporal lifecycle (computed, not hand-flagged).** Each placement records which source
EDITIONS attest it, each edition carrying a date and authority tier. "Current" = attested by the
latest authority (Coptic Reader). "Removed" = attested by older editions, absent from the current
one, with `valid_to` set to that boundary and a citation. Removals are derived from attestation,
not tagged by hand. Display: "read historically, removed as of [edition]." Occasion-agnostic, so
extendable beyond Pascha with no redesign.
Store the display as a uniform `removed_marker` string reflecting the ACTUAL attested boundary, e.g.
"(removed, Coptic Reader 2022)" or "(removed, [edition/year])". NEVER invent a synod or a year; the
marker cites the older source that attests the reading and the current source that lacks it. For now
this is populated for the Pascha removed readings only (Isaiah 48:1-6, Isaiah 59:1-17, Zechariah
11:11-14, the extra Proverbs, Job 27-28).

**4.4 Synaxarium model (multiple entries per day + a reasoned bridge).**
- A Coptic calendar day carries MULTIPLE commemorations (1..n: martyrs, popes/patriarchs, the
  Virgin, angels, apostles, ascetics, Lord's feasts). Store each commemoration as its OWN record,
  keyed by `(coptic_month, coptic_day, commem_id)`, with `type`, `title`, `rank`, `source`, and the
  commemoration's proper readings where the source supplies them.
- **The synaxarium text does NOT contain explicit links to the lectionary readings.** The link is
  built by reasoning, not copied. See Phase 5 for the bridge method and storage.

**4.5 Validation by attestation.** A reading is "confirmed" when two or more independent sources
agree after numbering normalization and Brenton text matching. The count of attesting sources tells
outlier from consensus. Unresolved disagreements go to the end-of-run Open Questions list, not to a
mid-run stop.
Every placement carries citable provenance: source, edition, and locator (page, URL, or API field),
not just a source name. The presentation layer exposes this as a per-passage "which source attests
which reading" disclosure, so a reader can see the basis for every reading and every removal.

---

## 5. Source registry (gather and cross-reference)

Use attestation counts across these to separate consensus from outlier. Ingestion and web search
are Grok's role; Hermes should search out further credible sources and add them here in the log.

**Current-practice authority**
- Coptic Reader (Diocese of the Southern US). Manual capture (screenshots -> fixtures).

**Scholarly / structural (for the article and the precedence rules)**
- Coptic Encyclopedia, "Lectionary" entry (Claremont CCDL). Treats it as a set of four books.
- Ugo Zanetti, "Les Lectionnaires coptes annuels — Basse Égypte" (Institut orientaliste de
  Louvain 31). The standard scholarly study.
- F.N. Youssef, "Arrangement of the Church Lectionary" (St Cyril's / ACCOT). Sunday readings are a
  separate program that governs when a Coptic day falls on a Sunday; the daily readings follow the
  Synaxarium; the lectionary is arranged into 69 collections by feast/commemoration type.
- Fr Manqaryus Awadalla, "The Lamp of the Holy Places" (referenced by Youssef).

**Printed Katameros editions (cross-reference + edition history for the temporal layer)**
- St. Mary Coptic Orthodox Church, Ottawa: Katameros of the Sundays / Holy Lent (1st ed. 1995,
  2nd ed. 2004).
- ukmidcopts.org PDFs: "Katameros of the Sundays," "Katameros of the Days."
- St. Bishoy Coptic Orthodox Church, Deacons' Corner: Katameros + Synaxarium for all seasons in
  Coptic, English, and Arabic. Already a cited source in the current dataset.

**Date-to-readings APIs**
- Katameros API, `api.katameros.app` (has Pascha hours and synaxarium; Masoretic numbering).
- coptic.io.

**Text anchors (public domain)**
- Brenton's Septuagint (Psalm identity, LXX numbering and versification).
- A public-domain Bible (WEB or KJV) for prophecies and gospels.

**Synaxarium full text**
- St-Takla.org (Synaxarium commemoration + Katameros readings per Coptic day).
- copticchurch.net.

**Historical witness for removed readings**
- The archived St. Mark / CopticChurch.net "Holy Pascha Book" (NKJV) recovered via Internet
  Archive. A witness for the historical layer, NOT current practice.

---

## 6. Phased execution plan

Each phase lists goal, tasks, the model/role split, the audit (independent model), and acceptance.
There are NO mid-run George stops; the audit is the gate.

### Phase 0 — Research and author the lectionary reference (FOUNDATION)
- **Goal:** one research effort, two outputs: a public article (Orthodox lesson, for George to push
  to the site) and an internal spec. The spec's taxonomy becomes the schema's controlled
  vocabularies.
- **Research (Grok-4.3):** gather and cross-reference Section 5 sources. Document the lectionary's
  structure and books; the seasons (Annual, Kiahk, Great Lent with its Sundays, Holy Week/Pascha,
  the Holy Fifty, the fasts); the date-calculation rules (Coptic calendar, movable feasts hinged on
  Pascha computation, fixed feasts); and the precedence rules (Sunday program governs when a day
  falls on Sunday; feasts govern over Sundays; daily readings follow the synaxarium). Define the
  controlled vocabularies: season list, occasion types, the 69 collection types, service/hour/slot
  enums, authority tiers.
- **Authoring (Codex/gpt-5.5):** write the article and the spec from the research. Format the
  article as an Orthodox **lesson** per the Hermes content schema (frontmatter: title, slug,
  publish, type: lesson, summary, tags, fathers, passages, season; canonical apparatus H2s where
  apt: Lesson Guide, Teacher's Notes, Discussion Questions, Sources, Glossary). It is a markdown
  file in this repo for George to push; Hermes does NOT push it.
- **AUDIT (Grok-4.3, independent of the authoring):** review the article and spec for unsourced
  claims, precedence/date errors, and vocabulary gaps. Suggest revisions. Re-run per 0.3 (max twice).
- **Acceptance:** every structural and precedence claim cited to a named source; inferences flagged;
  vocabularies complete enough to drive the schema.
- **Artifacts:** `article: coptic-lectionary-and-synaxarium.md` (lesson) + `spec: lectionary_spec.md`.

### Phase 1 — Lock the data model from the spec
- **Goal:** turn the spec into the concrete schema.
- **Design (Codex/gpt-5.5):** reading identity (4.1), placement (4.2), temporal attestation (4.3),
  synaxarium model (4.4). Build the verified LXX<->MT crosswalk including within-psalm verse
  offsets, with Brenton text anchors at the seams (Pss 9-10, 113-116, 147, Psalm 151).
- **Split:** `delegate_task` builds the crosswalk table; Codex designs the schema.
- **AUDIT (Grok-4.3):** verify the schema represents every shape in the Wednesday fixture (multiple
  OT prophecies per hour, composite cross-psalm references, named readings) and that the crosswalk
  passes Brenton text validation at the seams. Suggest revisions; re-run per 0.3.

### Phase 2 — Re-key the existing dataset to the model
- **Migration (Codex/gpt-5.5; `delegate_task` for the mechanical pass):** migrate the uniformly-MT
  dataset with `display_ref` (MT + LXX annotation), `identity_key`, and per-row source/edition
  provenance. Re-confirm the Phase 2a `Id=46/53` and Hatur 8 decisions under the identity key
  (ensure both sides were the same convention; Katameros "Ps 63" is LXX 62).
- **AUDIT (Grok-4.3):** no data lost; every row carries identity, display, provenance; 2a decisions
  re-confirmed or flagged. Suggest revisions; re-run per 0.3.

### Phase 3 — Multi-source attestation pass
- **Ingestion (Grok-4.3; `delegate_task` per source):** ingest the Section 5 sources, normalize
  numbering, validate on Brenton text.
- **AUDIT of ingestion (Codex/gpt-5.5, independent of Grok's ingestion):** extraction fidelity,
  numbering convention tagged per source, Brenton validation correct. Suggest revisions; re-run.
- **Attestation (Codex/gpt-5.5):** compute per-placement attestation and bucket into consensus
  (>=2 independent sources agree), outlier/disagreement, and old-edition-only (candidate removed
  readings, e.g. the Wednesday Isaiah/Zechariah/Job extras).
- **AUDIT of attestation (Grok-4.3):** every Pascha placement has an attestation set and a bucket;
  the Wednesday fixture reconciles (psalm "misses" resolve to numbering; prophecy differences
  resolve to consensus or removed). Suggest revisions; re-run.

### Phase 4 — Temporal classification
- **Classification (Codex/gpt-5.5):** mark current vs removed from edition attestation. Produce the
  residue: genuine disagreements and removed-reading classifications that consensus plus Coptic
  Reader cannot settle.
- **AUDIT (Grok-4.3):** classification logic and the residue list. Suggest revisions; re-run.
- The residue goes into the end-of-run Open Questions list (Section 8), NOT a mid-run stop.

### Phase 5 — Synaxarium / sanctoral readings (ingest, store, BRIDGE)
- **Ingestion (Grok-4.3; `delegate_task` per source: St-Takla, copticchurch.net, Katameros API):**
  for each Coptic day, extract ALL commemorations. Store each as a `synaxarium_commemoration`
  record: `(coptic_month, coptic_day, commem_id, type, title, rank, source)`, plus the
  commemoration's proper readings where the source supplies them. Expect multiple commemorations per
  day; do not collapse them.
- **AUDIT of ingestion (Codex/gpt-5.5):** completeness (no dropped commemorations), correct type
  classification, source citations. Re-run per 0.3.
- **BRIDGE (Codex/gpt-5.5) — the hard part, reasoned not copied:** the synaxarium source does not
  state which lectionary reading belongs to which commemoration. Build the link:
  1. For each Coptic day, gather both the daily lectionary readings (Katameros daily cycle) and the
     day's synaxarium commemorations.
  2. Classify each commemoration by type using the 69-collection taxonomy from the Phase 0 spec.
  3. Link readings to commemorations: per Youssef, the daily readings follow the synaxarium and each
     commemoration type maps to a standard reading collection (one of the 69). For a single
     commemoration, the link is direct. For multiple, the ranking commemoration governs the day's
     readings; secondary commemorations carry their own collection readings only where a source
     supplies them.
  4. Record the bridge BASIS on every link in a `synaxarium_reading_bridge` record:
     `(commem_id, reading_identity_key, slot, basis, confidence, citation)`, where `basis` is one of
     `explicit` (the source stated it), `collection-type` (matched via the 69-collection taxonomy),
     or `inferred` (reasoned, lower confidence).
  5. Flag every `inferred` link and every ambiguous multi-commemoration day for the end-of-run Open
     Questions list. Do not silently guess.
- **AUDIT of the bridge (Grok-4.3):** spot-check high-stakes links, review the basis distribution,
  challenge every `inferred` link. Suggest revisions; re-run per 0.3.
- The reverse lectionary indexes passage -> commemoration THROUGH this bridge, so a page can say
  "read at the 6th hour of Pascha Wednesday and on the commemoration of St. X," with the basis on
  record.

### Phase 6 — Presentation deliverables (Hermes produces, George pushes)
- Hermes has NO access to `coptic-corpus`, so it produces deliverables, it does not deploy.
- **Produce (Codex/gpt-5.5):** the final article markdown (Orthodox lesson, ready to push); the
  presentation-ready dataset (reverse-lectionary index with current/historical status and dual
  numbering, Today's-Readings data from current practice, per-passage liturgical-footprint data
  including the hour theme, the patristic homily, and slugs to link the chapter study and audio);
  and an integration spec describing how the site repo should consume them (including: accept both
  MT and LXX input in search and map to the identity key).
- **AUDIT (Grok-4.3):** the deliverables match the spec and the data is internally consistent.
- George does the final push to production and the plain-URL live verification.

### Phase 7 — Corrections and completion pass (current)
After Phases 0-6 ran autonomously, an external review of the enrichment found items to settle before
the article is final. Same model roles, same audit-as-gate discipline, one commit per change, no site
push.
- **Investigate the 69 (Grok):** confirm or deny that Youssef's 69 = the Ottawa TOC's 69 (set, not
  count). Codex audits the ingestion.
- **Article corrections (Codex):** the Pascha-computation clarity sentence (computus + Nicaea + same
  date as Eastern Orthodox, per 0.8); the 69 hedged or confirmed per the investigation; "Scripture is
  from NKJV" reworded to versification (or flagged for George's copyright call if verse text is
  reproduced); citation locators (Burmester pages, Zanetti volume/year, Coptic Encyclopedia byline);
  the Abuqti traditional-attribution clause; the 107-vs-105-day footnote.
- **Documentation-history section (Codex):** add a sourced "Sources and the history of the
  documentation" section explaining the source layers (printed Katameros editions, the scholarly
  studies, Burmester's Scetis Holy Week lectionary as the witness for the older fuller layer, Coptic
  Reader as current authority, the public-domain text anchors).
- **Spec/schema (Codex):** store the 69 as a controlled vocabulary with provenance (Section 3); add
  the `removed_marker` field (4.3).
- **Provenance + disclosure (Codex):** every placement carries source/edition/locator; produce the
  per-passage sources-disclosure data (4.5).
- **69-explicit bridge upgrade (Codex):** set `basis=explicit` for the days covered by the 69; report
  the full basis distribution before and after.
- **AUDIT (Grok):** review the whole pass per 0.3, then update the log and the Open Questions list.
- **Deferred to a later revision audit:** the inline "Source:" apparatus to footnotes and any prose
  voice pass. Do NOT touch presentation/voice in this pass.

---

## 7. Reference data

**7.1 Pascha Wednesday DAY fixture (Coptic Reader, authoritative for Wednesday Day).** Scripture
only; liturgical items are context. Numbers are LXX as shown in Coptic Reader.
- 1st Hour: Exodus 17:1-7; Proverbs 3:5-14; Hosea 5:13-6:3 | Psalm 50:6, 32:10 | John 11:46-57
- 3rd Hour: Exodus 13:17-22; Sirach 22:7-18 | Psalm 41:6, 1 | Luke 22:1-6  (screenshot cut off
  after the Gospel; may be incomplete)
- 6th Hour: Exodus 14:13-15:1; Sirach 23:7-14; "Memoirs of Job" (named) | Psalm 83:2, 5 |
  John 12:1-8
- 9th Hour: Genesis 24:1-9; Numbers 20:1-13; Proverbs 1:11-35 (Prov 1 has 33 verses in standard
  texts; record as shown, flag, do not auto-correct) | Psalm 40:6-8 | Matthew 26:3-16
- 11th Hour: Isaiah 28:16-29 | Psalm 6:2-3, 68:17 | John 12:27-36

Confirmed faithful to the screenshots, including 3rd Hour `Ps 41` and 6th Hour `Ps 83`. Where an
external book disagrees on those, Coptic Reader governs.

**7.2 LXX<->MT psalm crosswalk seams (do not apply a flat offset across these).**
- Pss 1-8: same in both.
- MT 10 through 113 = LXX 9 through 112 (LXX is one less); MT 9-10 merge into LXX 9.
- MT 114-115 = LXX 113; MT 116 = LXX 114-115.
- MT 117-146 = LXX 116-145; MT 147 = LXX 146-147.
- MT 148-150 = LXX 148-150. LXX 151 has no MT counterpart (Coptic canon).
- Within-psalm: LXX counts superscriptions as verses, so verse numbers also shift in titled psalms.
  Validate on Brenton text, not labels.

---

## 8. Audit checkpoints and the end-of-run handoff

Hermes does NOT stop for George during the run. The independent audits in Section 6 are the gates:
Phase 0 (article + spec), Phase 1 (schema + crosswalk), Phase 2 (re-key), Phase 3 (ingestion, then
attestation), Phase 4 (temporal classification), Phase 5 (synaxarium ingestion, then bridge),
Phase 6 (deliverables). Each runs the 0.3 protocol (revise, re-run at most twice, then proceed and
log).

**End-of-run deliverable: `audit_artifacts/open_questions_for_george.md`.** A single batched
document of everything thorough research could not settle, for George (and Fr. Boulos where
theological): genuine source disagreements, removed-reading classifications needing a ruling,
liturgical judgment calls the sources could not settle, and every low-confidence (`inferred`)
synaxarium bridge. Plus pointers to: the article markdown to push, the final dataset, and the
site-integration spec.

---

## 9. Definition of done

- Article on the Coptic lectionary and synaxarium written as an Orthodox lesson markdown file
  (ready for George to push), and the internal spec committed.
- Dataset re-keyed to the model: MT-primary display with LXX annotation, identity keys, per-row
  source/edition provenance.
- Pascha readings reconciled against Coptic Reader; removed readings retained and marked historical
  with citations; psalm-numbering artifacts resolved.
- Removed readings carry a uniform `removed_marker`; the 69 foundational-reading collection is stored
  as a provenance-bearing controlled vocabulary; every placement carries a citable source/edition/
  locator and feeds the per-passage sources disclosure.
- Synaxarium ingested with all commemorations per day, and bridged to the lectionary readings with
  a recorded basis per link.
- Presentation-ready dataset and a site-integration spec produced (George pushes and verifies live).
- `open_questions_for_george.md` produced; execution log complete with every audit pass recorded.
