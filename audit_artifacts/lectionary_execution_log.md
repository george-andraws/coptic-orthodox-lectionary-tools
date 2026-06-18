# Lectionary Execution Log

- Started: 2026-06-16
- Orchestrator: Hermes, current main role `openai-codex/gpt-5.5`, reasoning configured globally as `xhigh`
- Repo: `/Users/georgeandraws/workspace/coptic-lectionary-research`
- Source execution brief: `05-LECTIONARY-DESIGN.md`

## Phase 0 - Research and author the lectionary reference

### 2026-06-16 - Phase 0 setup
- Role/model used: Orchestrator, `openai-codex/gpt-5.5`, xhigh.
- What was done: Read the execution brief, Orthodox lesson runbooks, lectionary runbook, repo README, current builders, current verifier, and current generated data fields/counts.
- Subagent-vs-delegate choice: Full Hermes CLI instance will be used for Grok research and Grok audits because Section 0.2 assigns research/audit to `xai-oauth/grok-4.3` and delegate_task does not expose per-call provider/model routing in this session.
- Sources used: `05-LECTIONARY-DESIGN.md`, `README.md`, `RUNBOOK.md`, `build_lectionary_reference.py`, `build_lectionary_crosswalk.py`, `build_synaxarium_index.py`, `query_lectionary.py`, `verify_lectionary_queries.py`, `audit_artifacts/phase2b_sus_source_psalm_numbering_2026-06-15.md`, ACCOT F.N. Youssef page, Coptic Encyclopedia lectionary entry, coptic.net lectionary article.
- Acceptance result: Setup complete. Phase 0 research worker queued.
- Open question: none yet.

### 2026-06-16 - Phase 0 completed
- Research producer: `xai-oauth/grok-4.3`, xhigh. First full Grok worker looped without writing; restarted as a constrained final-output Grok run using the source packet gathered from web/file research. Artifact: `audit_artifacts/phase0_grok_research.md`.
- Research auditor: `openai-codex/gpt-5.5`, xhigh. Artifact: `audit_artifacts/phase0_codex_audit_of_grok_research.md`. Outcome: pass; source gaps correctly flagged.
- Article/spec producer: `openai-codex/gpt-5.5`, xhigh. Artifacts: `coptic-lectionary-and-synaxarium.md`, `lectionary_spec.md`.
- Article/spec auditor: `xai-oauth/grok-4.3`, xhigh. Audit pass 1 artifact: `audit_artifacts/phase0_grok_audit_pass1.md`. Findings: qualify four-book scope, mark theological inference, remove weak Chrysostom citation, improve glossary, add explicit controlled vocabularies.
- Revisions made after pass 1: removed John Chrysostom from frontmatter/source list, qualified theological claims, qualified the four-book claim as core Katameros books, softened glossary, expanded schema/spec vocabulary definitions.
- Audit pass 2 artifact: `audit_artifacts/phase0_grok_audit_pass2.md`. Outcome: conditional approval after one small clarification.
- Revisions made after pass 2: added a sentence that the four-book description does not exhaust every liturgical, sacramental, Agpeya, Synaxarium, or rite-specific source.
- Verification: `python3 build_design_deliverables.py`; `python3 -m py_compile build_design_deliverables.py`; content scan for em dash and banned words. All passed for article/spec/open questions/research/audit deliverables.
- Acceptance result: Phase 0 accepted. Commit hash: `815aca1`.
- Open questions carried forward: full English list of Youssef's 69 collections; exact ranked feast precedence; source-confirmed Kiahk and non-Lent fast rules.

### 2026-06-16 - Phase 1 completed
- Producer: `openai-codex/gpt-5.5`, xhigh. Artifacts: `build_design_deliverables.py`, `verify_design_deliverables.py`, `out/design/lectionary_schema.json`, `out/design/psalm_mt_lxx_crosswalk.csv`, `out/design/psalm_mt_lxx_crosswalk.jsonl`, and regenerated `lectionary_spec.md` plus open questions.
- Auditor: `xai-oauth/grok-4.3`, xhigh. Pass 1 artifact: `audit_artifacts/phase1_grok_audit_pass1.md`.
- Pass 1 required revisions: durable source label field, explicit `spans_json` contract, first-class named readings, Psalm confidence conflict resolution, no tentative MT equivalence for unresolved rows, table/vocabulary alignment, and separation of chapter-level Psalm mappings from verse examples.
- Revisions after pass 1: added `reading_name`; expanded `spans_json`; preserved `source_label`; corrected Coptic Reader Psalm mappings including LXX `Ps 68:17` to MT `Ps 69:16` and LXX `Ps 6:2-3` to MT `Ps 6:1-2`; left LXX `Ps 41:1` MT equivalent pending; added `mapping_scope`; added temporal authority fields.
- Auditor pass 2 artifact: `audit_artifacts/phase1_grok_audit_pass2.md`.
- Pass 2 remaining findings: `current_authority` emitted values were not fully aligned with the controlled vocabulary, and `temporal_classification` emitted fields were not all listed in schema.
- Revisions after pass 2: expanded the `current_authority` vocabulary, normalized emitted values, and added `temporal_classification` to the schema tables.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; content scan for em dash and banned words. All passed.
- Acceptance result: Phase 1 accepted after two audit passes with post-pass-2 corrections logged per protocol. Commit hash: `a5a79c0`.

### 2026-06-16 - Phase 2 completed
- Producer: `openai-codex/gpt-5.5`, xhigh. Artifacts: `out/design/reverse_lectionary_presentation.csv/jsonl`, `out/design/reading_identity.csv/jsonl`, `out/design/source_registry.csv/jsonl`, `out/design/todays_readings_current_practice.csv/jsonl`, `out/design/BUILD_DESIGN_SUMMARY.json`, plus generator/verifier updates.
- Auditor: `xai-oauth/grok-4.3`, xhigh. Pass 1 artifact: `audit_artifacts/phase2_grok_audit_pass1.md`.
- Pass 1 result: conditional pass. Required stronger evidence for `source_convention`, explicit registry coverage metrics, exact emitted source-key list, and allowlists.
- Revisions after pass 1: added verifier checks for `source_convention`, emitted source-key registration, controlled authority tiers, source-registry authority tiers, and controlled current statuses. Added source registry rows for `special_service`, `agpeya`, and `bright_saturday_service_order`. Replaced stale `current_needs_psalm_fixture_review` with schema-approved `current_psalm_equivalence_unresolved`.
- Auditor pass 2 artifact: `audit_artifacts/phase2_grok_audit_pass2.md`. Outcome: commit-ready; no required revisions.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; data-quality metrics for identity joins, source keys, display refs, provenance/source evidence, source conventions, registry coverage, and authority tiers. All passed.
- Acceptance result: Phase 2 accepted after two audit passes. Commit hash: `6c0cb65`.

### 2026-06-16 - Phase 3 completed
- Source ingestion producer: `xai-oauth/grok-4.3`, xhigh. Artifact: `audit_artifacts/phase3_grok_source_ingestion.md`.
- Source ingestion audit: `openai-codex/gpt-5.5`, xhigh. Artifact: `audit_artifacts/phase3_codex_audit_of_grok_ingestion.md`. Outcome: pass.
- Attestation producer: `openai-codex/gpt-5.5`, xhigh. Artifacts: `out/design/pascha_attestation.csv/jsonl`, `out/design/pascha_attestation_bucket_manifest.csv/jsonl`, plus generator and verifier updates.
- Attestation auditor: `xai-oauth/grok-4.3`, xhigh. Pass 1 artifact: `audit_artifacts/phase3_grok_attestation_audit_pass1.md`. Outcome: conditional pass.
- Pass 1 required revisions: add explicit zero-count `consensus_without_coptic_reader` bucket, add row-level notes for five unresolved Wednesday Psalm candidates, and replace bare `api` citations with replayable source references.
- Revisions after pass 1: added bucket manifest output, added `attestation_note`, expanded citations to include source key/file/row/ref/provenance, and strengthened verifier coverage for all three audit findings.
- Auditor pass 2 artifact: `audit_artifacts/phase3_grok_attestation_audit_pass2.md`. Outcome: pass, commit-ready.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; content-rule scan of Phase 3 audit files. All passed.
- Acceptance result: Phase 3 accepted after two attestation audit passes. Commit hash: `6a15663`.
- Open questions carried forward: five Wednesday Psalm candidates remain explicitly unresolved pending deeper text-boundary review; Coptic Reader scope remains limited to the captured Wednesday Day fixture.

### 2026-06-16 - Phase 4 completed
- Producer: `openai-codex/gpt-5.5`, xhigh. Artifacts: `out/design/temporal_classification.csv/jsonl`, `out/design/temporal_residue.csv/jsonl`, `out/design/temporal_residue_manifest.csv/jsonl`, plus `audit_artifacts/open_questions_for_george.md` updates.
- Auditor: `xai-oauth/grok-4.3`, xhigh. Pass 1 artifact: `audit_artifacts/phase4_grok_temporal_audit_pass1.md`. Outcome: conditional pass.
- Pass 1 required revisions: add explicit zero-count true-disagreement handling, soften non-fixture current-authority wording, clarify candidate-removed wording, rename Psalm unresolved status so it does not imply current confirmation, and route unresolved residue into open questions.
- Revisions after pass 1: added `temporal_residue_manifest`, changed authority wording to `no scoped current authority confirmation`, renamed status to `pending_psalm_equivalence_unresolved`, expanded open questions with candidate-removed rows, Psalm unresolved rows, current-authority pending summary, and true-source-disagreement zero statement.
- Auditor pass 2 artifact: `audit_artifacts/phase4_grok_temporal_audit_pass2.md`. Outcome: pass, commit-ready.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; content-rule scan of Phase 4 audit files and open questions. All passed.
- Acceptance result: Phase 4 accepted after two audit passes. Commit hash: `04cc512`.
- Open questions carried forward: 419 temporal residue rows remain review residue, including 7 candidate removed readings and 5 Psalm-equivalence unresolved rows.

### 2026-06-16 - Phase 5 completed
- Ingestion reviewer: `xai-oauth/grok-4.3`, xhigh. Pass 1 artifact: `audit_artifacts/phase5_grok_synaxarium_ingestion.md`. Outcome: conditional readiness with extraction caveats.
- Ingestion revisions: inferred unnumbered single-entry titles from source-summary leads, stopped duplicate detailed-prose title emission after clean headings, deduplicated repeated heading snippets, preserved full `source_summary`, emitted `extraction_method` and `caveat`, and narrowed Theotokos classification to explicit Mary/Theotokos titles.
- Ingestion reviewer pass 2: `audit_artifacts/phase5_grok_synaxarium_ingestion_pass2.md`. Outcome: ready for Codex audit.
- Ingestion auditor: `openai-codex/gpt-5.5`, xhigh. Artifact: `audit_artifacts/phase5_codex_audit_of_grok_synaxarium_ingestion.md`. Outcome: pass.
- Bridge producer: `openai-codex/gpt-5.5`, xhigh. Artifacts: `out/design/synaxarium_commemorations.csv/jsonl`, `out/design/synaxarium_reading_bridge.csv/jsonl`.
- Bridge auditor: `xai-oauth/grok-4.3`, xhigh. Pass 1 artifact: `audit_artifacts/phase5_grok_synaxarium_bridge_audit_pass1.md`. Outcome: conditional pass.
- Bridge revisions after pass 1: downgraded all collection-type bridge rows to `medium` confidence, documented that repeated slots are source-row or variant catalog entries and not a resolved daily service schedule, retained primary-commemoration-only linking.
- Bridge auditor pass 2: `audit_artifacts/phase5_grok_synaxarium_bridge_audit_pass2.md`. Outcome: pass, commit-ready.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; content-rule scan of Phase 5 audit files. All passed.
- Acceptance result: Phase 5 accepted after two ingestion review passes and two bridge audit passes. Commit hash: `350a0bd`.
- Open questions carried forward: 141 `prose_lead_inferred` Synaxarium rows require source-page wording review before final publication wording; bridge remains medium-confidence collection-type, not direct proper-reading proof.

## Phase 6 - Presentation deliverables

### 2026-06-16 - Phase 6 regeneration and local verification
- Producer: `openai-codex/gpt-5.5`, xhigh. Artifacts regenerated: `coptic-lectionary-and-synaxarium.md`, `site_integration_spec.md`, `audit_artifacts/open_questions_for_george.md`, all final `out/design/*` design-layer datasets, `presentation/lectionary_design_layer_deck.pptx`, and `presentation/lectionary_design_layer_deck_outline.md`.
- Subagent-vs-delegate choice: Codex orchestrator performed the deterministic generator/verifier changes directly. A full Hermes CLI instance was used for Grok audit because Phase 6 artifacts were Codex-produced and Section 0.2 requires the independent auditor to be `xai-oauth/grok-4.3`.
- Revisions made before independent audit: added exact reader-facing source wording `Scripture is from NKJV.` to the article; changed article heading to `Teaching guide`; strengthened Synaxarium bridge wording as medium-confidence collection-type discovery links, not direct proper-reading proof and not a resolved daily service schedule; added final push-package pointers; added `scripts/build_phase6_deck.py`; added stricter verifier guards for article wording, long Synaxarium titles, and repeated bridge slot notes.
- Additional local correction during verification: shortened the Kiyahk 22 Archangel Gabriel title in the generator while preserving the full source summary, and changed bridge notes to use the literal `source-row or variant catalog` wording required by the Phase 5 final state.
- Verification commands run:
  - `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`
  - `python3 build_design_deliverables.py`
  - `python3 scripts/build_phase6_deck.py`
  - `python3 verify_design_deliverables.py`
  - Custom Phase 6 checks over article/spec/open questions/deck outline/PPTX text, row counts, JSONL counts, identity joins, source registry coverage, Synaxarium counts, bridge semantics, and deck placeholders.
- Verification result: all commands passed. `build_design_deliverables.py` emitted 66,378 reverse presentation rows, 2,657 reading identity rows, 11 today's-reading rows, 161 Psalm crosswalk rows, 445 Pascha attestation rows, 5 Pascha bucket manifest rows, 445 temporal classification rows, 419 temporal residue rows, 5 temporal residue manifest rows, 664 Synaxarium commemoration rows, 4,688 bridge rows, and 2,656 passage-footprint rows.
- Preserved Phase 5 state: 366 source Coptic days; 664 commemorations; 141 `prose_lead_inferred` rows, all caveated; 0 day-title fallback rows; 0 long prose-like titles; 4,688 bridge rows; all bridge basis values `collection-type`; all bridge confidence values `medium`; repeated slot groups documented as source-row or variant catalog entries; no bridge wording describes direct proper-reading proof or a resolved daily service schedule.
- Deck verification: `scripts/build_phase6_deck.py` regenerated a 10-slide PPTX and outline. PPTX text extraction found no placeholders, no em dashes, and no banned words. QuickLook generated a non-empty thumbnail at `/tmp/phase6_deck_preview/lectionary_design_layer_deck.pptx.png` for visual sanity. The vision helper could not run in this session due auxiliary model routing, so visual verification is limited to QuickLook thumbnail generation plus PPTX structural/text checks.

### 2026-06-16 - Phase 6 independent audit pass 1
- Auditor: `xai-oauth/grok-4.3`, xhigh, full Hermes CLI instance with file and terminal toolsets. Artifact: `audit_artifacts/phase6_grok_audit_pass1.md`.
- Audit pass 1 verdict: conditional pass.
- Audit pass 1 findings: article, data outputs, site integration spec, deck outline, PPTX structure/text, open questions handoff, Synaxarium bridge semantics, and Section 9 Definition of Done content checks passed. Required process revisions remained: record Phase 6 and the audit in the execution log, then commit the Phase 6 package.
- Revisions after pass 1: updated this execution log with Phase 6 regeneration, verification evidence, audit pass 1 result, and unresolved questions. No article, dataset, site spec, deck, or open-questions content revision was required by Grok pass 1.
- Unresolved questions carried forward: Psalm 41:1 exact MT equivalence; full enumerated English list of Youssef's 69 collections; Coptic Reader coverage beyond the Wednesday Day fixture; 141 prose-lead Synaxarium titles needing source-page wording review; site-side joins for patristic homily, chapter-study, and audio slugs in `coptic-corpus`.
- Acceptance state before commit: Phase 6 artifact content accepted by audit pass 1, pending focused audit-loop closure, final commit, and second log-only commit with the Phase 6 commit hash.

### 2026-06-16 - Phase 6 independent audit pass 2
- Auditor: `xai-oauth/grok-4.3`, xhigh, full Hermes CLI instance with file and terminal toolsets. Artifact: `audit_artifacts/phase6_grok_audit_pass2.md`.
- Audit pass 2 verdict: pass.
- Audit pass 2 findings: pass 1 required process revisions were resolved enough to proceed to the Phase 6 artifact commit. The execution log now records Phase 6 regeneration, artifacts, verification commands and row counts, Phase 5 preservation checks, audit pass 1 result, revisions, unresolved questions, and acceptance state before commit.
- Required revisions before Phase 6 artifact commit: none.
- Final acceptance state: Phase 6 artifacts were committed in `440001d`; this hash is recorded in the required follow-up log-only commit.
- Acceptance result: Phase 6 accepted after two independent Grok audit passes. Phase 6 artifact commit hash: `440001d`.

## Phase 7 - Corrections and completion pass

### 2026-06-16 - Step 0 orientation and Step 1 investigation of the 69
- Role/model used: Orchestrator and ingestion auditor, `openai-codex/gpt-5.5`, xhigh. Research producer, `xai-oauth/grok-4.3`, xhigh, through a full Hermes CLI instance because the model assignment required Grok for research.
- Step 0 source note: repo HEAD was confirmed as `a2f39d52c21a10f8c2d48420401fb5c745ef00c1`, and the working tree was clean except the allowed untracked `audit_artifacts/phase2b_sus_source_psalm_numbering_2026-06-15.md`. The repo copy of `05-LECTIONARY-DESIGN.md` was absent, so George supplied `/Users/georgeandraws/.hermes/webui/attachments/ec88b422f574/05-LECTIONARY-DESIGN-2-1.md` as the substitute locked design brief.
- Schema/control-vocabulary locator: `lectionary_spec.md` and `build_design_deliverables.py` identify `out/design/lectionary_schema.json` as the machine-readable source of truth for controlled vocabularies.
- Step 1 research artifact: `audit_artifacts/phase7_grok_69_investigation.md`.
- Step 1 ingestion audit artifact: `audit_artifacts/phase7_codex_audit_of_grok_69_investigation.md`.
- Sources used: Ottawa/UKMID `Katameros_Days.pdf`, re-pulled from `https://ukmidcopts.org/pdf/Katameros_Days.pdf`; F.N. Youssef, `The Arrangement of the Church Lectionary`, ACCOT, `https://accot.stcyrils.edu.au/fny-read1/`.
- Verdict later corrected by Step 6: `INFERRED_LIKELY_SAME_SET` (roster unverified), not confirmed same set. The Step 1 investigation established that Youssef describes 69 collections by commemoration type in volume two and that Ottawa presents a matching count of dated entries in the weekday-and-feast volume. Alignment is inferred from shared source tradition, volume two placement, category match, and count, not from a matched reading-by-reading roster.
- Verification: Codex re-pulled the Ottawa PDF, extracted pages 23 to 26 with `pypdf`, confirmed 69 dated TOC entries, confirmed sample annual table rows mapping days to the same dated sections, and fetched ACCOT with `curl -L --compressed` after plain Python returned HTTP 406.
- Acceptance result: Step 1 accepted for Steps 2b, 4, and 7. Commit hash: `ef55101`.

### 2026-06-16 - Step 2a Pascha computation clarity
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Sources checked: World Council of Churches and Middle East Council of Churches, `Towards a Common Date for Easter`, Aleppo, 1997; Orthodox Church in America, `Concerning the Date of Pascha and the 1st Ecumenical Council`; F.N. Youssef, `The Arrangement of the Church Lectionary`.
- What was done: Added one article sentence clarifying that Youssef's phrase about the Hebrew calendar is about the Church's Paschal computation, the Nicene norm of the Sunday following the first vernal full moon as later calculated through the Alexandrian mode, not a lookup of the present-day Hebrew calendar. Added the WCC/MECC source to the article source list.
- Source limitation: A clean source for the claim that Coptic Pascha always falls on the same date as Eastern Orthodox Pascha was not found in this step. The article omits that clause, and `audit_artifacts/open_questions_for_george.md` now records the shared-date source check.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 2a accepted. Commit hash: `b50e91b`.

### 2026-06-16 - Step 2b 69 identity wording
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Step 1 dependency later corrected by Step 6: `INFERRED_LIKELY_SAME_SET` (roster unverified). The consulted Youssef page describes 69 collections by commemoration type and does not print a date-by-date roster.
- What was done at the time: Updated the article to identify the Ottawa/UKMID Katameros of the Days with Youssef's second-volume collection in English. Step 6 later corrected this to an inferred-likely alignment, roster unverified, and reopened roster verification as an open question.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 2b accepted. Commit hash: `169f8a2`.

### 2026-06-16 - Step 2c NKJV wording
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Check performed: Scanned `coptic-lectionary-and-synaxarium.md` for NKJV references, block quotes, and verse-like reproduced text. The article contains Scripture references and no NKJV verse text.
- What was done: Changed the source line from `Scripture is from NKJV.` to `Scripture references follow NKJV versification.` Updated `verify_design_deliverables.py` so the verifier enforces the new Step 2c wording and rejects the old wording.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed after the verifier was updated to match the Step 2c requirement.
- Acceptance result: Step 2c accepted. Commit hash: `9a46291`.

### 2026-06-16 - Step 2d citation locators and minor notes
- Producer: `openai-codex/gpt-5.5`, xhigh. Intended Grok research worker timed out before writing an artifact; source evidence was pulled directly with terminal HTTP and PDF extraction. Independent Grok audit remains the Step 8 gate.
- Sources checked: CCDL API item 1199; CCDL `Lectionary` PDF text; ACCOT Youssef page; Open Library OL2304712M JSON; Crossref, Open Library search, Internet Archive advanced search, and repo local search for Burmester.
- What was done: Confirmed the Coptic Encyclopedia byline from CCDL and updated the article wording to `Basilios, Archbishop, and Coquin, René-Georges`. Added traditional-attribution language to the Abuqti paragraph and glossary. Added a note that the article reports Youssef's `15 weeks or 107 days` figure as given, while 15 weeks is 105 days.
- Items flagged instead of guessed: Burmester pages 83 to 137 were not confirmed. Zanetti series/year was not cleanly confirmable because Open Library gives Publications de l'Institut orientaliste de Louvain 33, 1985, while the CCDL Coptic Encyclopedia PDF bibliography gives 31, 1988.
- Audit artifact: `audit_artifacts/phase7_step2d_source_check.md`.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 2d accepted. Commit hash: `db025be`.

### 2026-06-16 - Step 3 documentation-history section
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Sources checked: Ottawa/UKMID extracted PDF front matter for Days, Sundays, Pentecost, and Holy Pascha; direct HTTP availability for UKMID PDF URLs; St. Bishoy Deacons' Corner Katameros page; CCDL Coptic Encyclopedia metadata; ACCOT Youssef page; repository source registry; `out/design/psalm_mt_lxx_crosswalk.csv`; eBible World English Bible copyright information; Wikisource King James Bible copyright note.
- What was done: Added `## How the lectionary has been documented` to the generated article, explaining printed Katameros witnesses, public documentation layers, scholarly structural sources, Burmester as older Holy Week witness, scoped Coptic Reader current authority, and Bible text comparison anchors. Added UKMID, St. Bishoy, Brenton, WEB, and KJV policy anchors to the Sources list without changing the existing inline `Source:` attribution style.
- Attribution discipline: New section labels `Read from source` and one explicit `Inference from the design residue` statement.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; generated-article scan for em dash and banned words. All passed.
- Acceptance result: Step 3 accepted. Commit hash: `ef4aaf1`.

### 2026-06-16 - Step 4 foundational-reading controlled vocabulary
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Inputs: Step 1 Grok investigation and Codex audit; Ottawa/UKMID `Katameros_Days.pdf`; ACCOT Youssef page.
- What was done: Replaced the old count-only `collection_types_69` placeholder with an enumerated controlled vocabulary. Added `FOUNDATIONAL_69_SOURCE_PROVENANCE`, `FOUNDATIONAL_69_RAW`, generated `out/design/foundational_reading_collections_69.csv`, generated `out/design/foundational_reading_collections_69.jsonl`, embedded 69 entries in `out/design/lectionary_schema.json`, added a `foundational_reading_collection` schema table, added `st_mary_ottawa_days` to the source registry, and documented the vocabulary in `lectionary_spec.md`.
- Membership verdict later corrected by Step 6: `INFERRED_LIKELY_SAME_SET` (roster unverified). Youssef gives collections by commemoration type; Ottawa gives dated entries. Alignment is inferred from shared source tradition, volume two placement, category match, and count.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; explicit row-count sanity check. All passed.
- Acceptance result: Step 4 accepted. Commit hash: `85e7422`.

### 2026-06-16 - Step 5 removed-marker model field
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Inputs: Ottawa Holy Pascha extracted source text, Coptic Reader Wednesday Day fixture supplied by George, generated `pascha_source_text_index.csv`, generated Pascha day-hour rows, and Step 5 requirements from the locked design brief.
- What was done: Added a uniform `removed_marker` field to the presentation, attestation, temporal classification, and residue outputs. The marker is populated only for older Pascha Wednesday placements absent from the scoped Coptic Reader Wednesday Day fixture. Retained the removed readings as historical rows, including Isaiah 48:1-6, Isaiah 59:1-17, Zechariah 11:11-14, extra Proverbs rows, and Job 27 to 28 rows.
- Boundary note: Markers cite the actual older source witness and current comparator. Example source boundaries include St. Mary Ottawa Holy Pascha p. 308 line 7779 for Isaiah 48:1-6, p. 320 line 8091 for Isaiah 59:1-17, p. 322 line 8133 for Zechariah 11:11-14, p. 318 line 8038 for Proverbs 1:10-33, p. 299 line 7552 for Proverbs 4:4-27,5:1-4, and p. 298 line 7519 for Job 27:16-28:2.
- Generated output impact: `reverse_lectionary_presentation` now has 66,381 rows, `reading_identity` has 2,658 rows, `pascha_attestation` has 446 rows, and `temporal_residue` has 420 rows. The generator now retains 11 rows with `removed_marker`.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; explicit removed-marker row check. All passed.
- Acceptance result: Step 5 accepted. Commit hash: `2622ee2`.

### 2026-06-16 - Step 6 citable provenance and source-disclosure data
- Producer: `openai-codex/gpt-5.5`, xhigh.
- What was done: Added registry-level `edition` and `default_locator` metadata, carried `source_title`, `source_edition`, `source_locator`, and `source_url` into placement rows, aggregated source titles, editions, and locators into Pascha attestation and temporal classification rows, and created `out/design/passage_source_disclosure.csv/jsonl` for page-level source disclosure.
- Disclosure output: `passage_source_disclosure` emits one row per presentation placement/source row, with identity, display reference, source key, title, edition, locator, URL, source reference, occasion, slot, current status, removed marker, and replayable citation.
- Generated output impact: `passage_source_disclosure` has 66,381 rows. Existing design-row counts are otherwise unchanged from Step 5.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; explicit disclosure schema and row-count checks. All passed.
- Acceptance result: Step 6 accepted. Commit hash: `f79cbbc`.

### 2026-06-16 - Step 7 69-explicit Synaxarium bridge upgrade
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Before distribution: basis `collection-type`: 4,688. Confidence `medium`: 4,688.
- What was done: Upgraded bridge rows whose Coptic day is enumerated in the Ottawa/UKMID 69 foundational-reading collection to `basis=explicit` and `confidence=high`. Added Ottawa/UKMID Katameros of the Days edition and locator to the bridge citation while retaining St-Takla and local Katameros row citation data.
- After distribution: basis `explicit`: 789, `collection-type`: 3,899. Confidence `high`: 789, `medium`: 3,899.
- Coverage note: 58 foundational Coptic days produced bridge rows and were upgraded. 11 foundational days had no emitted bridge rows because the bridge only emits days that have both a Synaxarium primary commemoration row and local fixed-day Katameros rows.
- Outside-69 flag: outside the 69, the bridge remains uniformly `basis=collection-type` and `confidence=medium`. This is recorded in `audit_artifacts/open_questions_for_george.md` as a bridge differentiation flag.
- Supersession note: Earlier Phase 6 bridge basis and confidence counts are historical and are superseded by this Step 7 distribution.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; explicit before/after distribution check. All passed.
- Acceptance result: Step 7 accepted. Commit hash: `efbf63c`.

### 2026-06-16 - Step 8 independent audit and revisions
- Producer of revisions: `openai-codex/gpt-5.5`, xhigh.
- Auditor: `xai-oauth/grok-4.3`, xhigh, via Hermes CLI one-shot with file, terminal, and web toolsets. Auditor was instructed to inspect only this repo and not edit, commit, or push.
- Audit pass 1 artifact: `audit_artifacts/step8_grok_audit_pass1.md`.
- Pass 1 required findings: repo-local locked brief was absent; article and spec bridge prose were stale after Step 7; schema table contracts under-documented emitted outputs; verifier lacked schema/header parity; open questions blurred `removed_marker` rows with other candidate-removed rows.
- Revisions made after pass 1: added repo-local `05-LECTIONARY-DESIGN.md` from George's supplied identical attachment; updated article/spec bridge wording; expanded schema table contracts; added verifier CSV-header parity; split open-question sections; added per-row membership verdict data, later corrected by Step 6 to `INFERRED_LIKELY_SAME_SET`; added foundational 69 files to the site copy list.
- Audit pass 2 artifact: `audit_artifacts/step8_grok_audit_pass2.md`.
- Pass 2 outcome: no data/model required revisions remained. Required repo-state item was to add `05-LECTIONARY-DESIGN.md` to the commit. Advisable items were the Step 7 supersession note and preserving the `removed_marker` prose-pattern vs token decision as an open question.
- Verification after revisions: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 8 accepted. Commit hash: `e2a5773`.


### 2026-06-16 - Step 9 final log and consolidated report
- Producer: `openai-codex/gpt-5.5`, xhigh.
- What was done: Replaced Step 1 through Step 8 pending commit placeholders with actual hashes, reviewed `audit_artifacts/open_questions_for_george.md`, and prepared the consolidated final report for George.
- Sources used: `git log --oneline --reverse a2f39d5..HEAD`, `audit_artifacts/open_questions_for_george.md`, and Grok Step 8 audit reports.
- Final bridge distribution recorded for report: before Step 7, basis `collection-type`: 4,688 and confidence `medium`: 4,688. After Step 7, basis `explicit`: 789 and `collection-type`: 3,899; confidence `high`: 789 and `medium`: 3,899.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `python3 scripts/build_phase6_deck.py`; `git diff --check`. All passed in the final Step 9 verification run.
- Acceptance result: Step 9 accepted. Commit hash: final log commit reported in George's consolidated end-of-run response.


## Phase 7 continuation - 2026-06-16 requested corrections

### Step 0 - Orientation for continuation pass
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Files read in full: `05-LECTIONARY-DESIGN.md`, `coptic-lectionary-and-synaxarium.md`, `lectionary_spec.md`, and `audit_artifacts/lectionary_execution_log.md`.
- Repo brief verification: the attached `05-LECTIONARY-DESIGN-2-1.md` matches the repo `05-LECTIONARY-DESIGN.md`; first 20 lines were printed in the run output; the repo brief contains a Phase 7 header and Section 0.8 contains a `Pascha framing` bullet.
- Git gate: HEAD was `16febe5`; working tree was clean except the known untracked `audit_artifacts/phase2b_sus_source_psalm_numbering_2026-06-15.md`.
- Acceptance result: Step 0 accepted.

### Step 1 - Bibliographic corrections
- Producer: `openai-codex/gpt-5.5`, xhigh.
- What was done: Applied George's externally confirmed bibliographic corrections without re-researching. Updated Zanetti to `Les lectionnaires coptes annuels: Basse-Egypte`, Publications de l'Institut Orientaliste de Louvain 33, Louvain-la-Neuve, 1985, xxiv + 383 p. Updated Burmester to `Bulletin de la Societe d'Archeologie Copte XVI, 1961-1962, pp. 83-137`.
- Open questions: closed the unresolved Burmester and Zanetti locator items; retained the Youssef 15 weeks or 107 days arithmetic note as a separate open item.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 1 accepted. Commit hash: `c9dd8bf`.

### Step 2 - Pascha clarification with supplied external source fixtures
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Web constraint: No web fetch or search was attempted in this session. George supplied the external source verification as fixed citation fixtures because web tools are blocked.
- Source fixtures used: Fr. Andrew Stephen Damick, `No, the Paschal date difference is not about Passover (and other Orthodox urban legends)`, Ancient Faith Ministries, 2022; Greek Orthodox Archdiocese of America, `Some Common Misperceptions about the Date of Pascha/Easter`; timeanddate public Easter-date references for Coptic Orthodox Easter and Russian Orthodox Easter in 2026; OrthodoxWiki `Coptic Calendar`; copticchurch.net calendar notes.
- What was done: Added George's supplied clarification sentence to the article while keeping the existing Nicene/computus wording. The sentence states that the Coptic Church does not look up the date in the modern Jewish calendar, uses Alexandrian reckoning set at Nicaea and the same nineteen-year cycle used by Eastern Orthodox churches, and gives 12 April 2026 as the shared Coptic/Russian Orthodox Pascha example.
- Resolved item: Removed the Pascha shared-date source check from `audit_artifacts/open_questions_for_george.md`. The resolved note records that verification was externally supplied and not independently web-rechecked in this blocked session.
- Partial artifact handling: The uncommitted `audit_artifacts/phase7_step2_pascha_source_check_grok.md` contained a blocked-web limitation and a partial GOARCH/timeanddate note. Its limitation is folded into this log entry, and the file was removed rather than committed.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 2 accepted. Commit hash: `5396e43`.

### Step 3 - Explicit 69 verdict wording
- Producer: `openai-codex/gpt-5.5`, xhigh.
- What was done at the time: Updated the execution log and generated article with a same-set claim. Step 6 later corrected this as overstated because Youssef's 69 are type-collections and Ottawa's 69 are dated entries.
- Corrected caveat after Step 6: the verdict is `INFERRED_LIKELY_SAME_SET` (roster unverified), because Youssef's type-collections and Ottawa's dated entries are different objects until a reading-by-reading roster is matched.
- Bridge note retained: The Step 7 `basis=explicit` bridge upgrade still stands on the Ottawa/UKMID volume's direct dated reading sections and does not require Youssef's page to print the roster.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 3 accepted. Commit hash: `2ad64ea`.

### Step 4 - Data review of duplicate-looking removed rows
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Evidence checked: `out/design/temporal_classification.csv`, `out/design/temporal_residue.csv`, `out/design/reverse_lectionary_presentation.csv`, `out/design/reading_identity.csv`, `out/data/pascha_source_text_index.csv`, `out/data/pascha_day_hour_index.csv`, `out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt`, `tests/fixtures/pascha_wednesday_day_coptic_reader.json`, and parser aliases in `passage_normalization.py`.
- Fix made: unambiguous Proverbs duplicate normalized. `Prov 4:4-5:4` is the same continuous span as `Prov 4:4-27,5:1-4`; the generator now normalizes the compact form to the explicit two-segment form and keeps source-row provenance.
- Reported without reclassification: Job rows remain unresolved because the older Ottawa source, local corrected day/hour row, and Coptic Reader fixture differ in hour and boundary detail. `Prov 1:10-33` and current `Prov 1:11-35` are treated as older/current variants of one slot, not a double-counted row. `Wis` rows remain Wisdom of Solomon candidates because repo aliases map `Wis` to Wisdom of Solomon and `Sir` separately to Sirach.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; data-effect check confirming one Wednesday Third Hour Proverbs 4 temporal row and one Proverbs 4 identity. All passed.
- Acceptance result: Step 4 accepted. Commit hash: `03fb997`.


### Step 5 - Grok audit, final log, and report
- Producer of revisions: `openai-codex/gpt-5.5`, xhigh.
- Auditor: `xai-oauth/grok-4.3`, xhigh, via Hermes CLI one-shot with file and terminal toolsets only. No web/search/fetch tools were enabled or used.
- Web limitation: Grok's audit of Step 2 was limited to internal consistency, citation handling, wording, content rules, and log disclosure. Step 2 Pascha source verification was supplied externally by George/Claude as fixed citation fixtures because web tools were blocked.
- Audit pass 1 artifact: `audit_artifacts/phase7_step5_grok_audit_pass1.md`. Outcome: no required revisions. Advisable article clarification was to state that the explicit bridge classification rests on Ottawa's direct dated reading sections, not on Youssef printing the full roster.
- Revision after pass 1: added the advised bridge-independence sentence to the generated article through `build_design_deliverables.py`, then regenerated and verified.
- Audit pass 2 artifact: `audit_artifacts/phase7_step5_grok_audit_pass2.md`. Outcome: no required revisions remain.
- Open questions updated: `audit_artifacts/open_questions_for_george.md` now carries the Step 4 data-review findings for Job span/hour disagreement, Proverbs 1 older/current variants, and Wisdom of Solomon candidate rows.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 5 accepted. Commit hash: `8c67d63`.

### Step 6 - Corrected 69 verdict
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Web constraint: No web fetch or search was attempted. This correction uses George's instruction and existing repo-local evidence.
- Corrected verdict: `INFERRED_LIKELY_SAME_SET` (roster unverified).
- Read from source: Youssef gives 69 collections by commemoration type, one program per kind of feast and commemoration, gathered in volume two of the Yearly Katameros. Read from source: the Ottawa Katameros of the Days table of contents presents a matching count of dated entries in the weekday-and-feast volume. Inferred: alignment rests on shared source tradition, volume two placement, category match, and count, not on a matched reading-by-reading roster.
- What was done: Corrected the generated article, spec text, source registry note, controlled-vocabulary verdict token, per-row membership status, site integration bridge wording, verifier expectations, and open questions. Left bridge rows unchanged because `basis=explicit` rests on Ottawa's direct dated reading sections.
- Open question added: verify the reading-by-reading roster mapping between Youssef's 69 type-collections and the Ottawa dated entries.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; targeted scan for stale overclaim phrases. All passed.
- Acceptance result: Step 6 accepted. Commit hash: `f1b0fbd`.

### Step 7 - Grok audit of corrected 69 verdict
- Producer of revisions: `openai-codex/gpt-5.5`, xhigh.
- Auditor: `xai-oauth/grok-4.3`, xhigh, via Hermes CLI one-shot with file and terminal toolsets only. No web/search/fetch tools were enabled or used.
- Audit pass 1 artifact: `audit_artifacts/phase7_step7_grok_audit_pass1.md`. Outcome: no required revisions. Advisable revisions: article should say "kind of feast and commemoration" and should call Ottawa rows the `69 dated-entry bridge taxonomy` in the Synaxarium bridge paragraph.
- Revision after pass 1: applied both advisable article refinements through `build_design_deliverables.py`, regenerated the article, and verified.
- Audit pass 2 artifact: `audit_artifacts/phase7_step7_grok_audit_pass2.md`. Outcome: no required revisions remain. Article overclaim status is clean; bridge distribution remains `explicit=789`, `collection-type=3899`, with confidence `high=789`, `medium=3899`.
- Corrected verdict text: `INFERRED_LIKELY_SAME_SET` (roster unverified). Youssef gives 69 foundational reading collections arranged by kind of feast and commemoration in volume two of the Yearly Katameros. Ottawa presents 69 dated entries in the weekday-and-feast volume. Alignment is inferred from shared source tradition, volume two placement, category match, and count, not from an independently matched reading-by-reading roster.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 7 accepted. Commit hash: `248e11a`.

### Step 8 - Article publish-readiness pass
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Scope: presentation pass only, no sourced-claim rewrite.
- What was done: updated `build_design_deliverables.py` to convert inline `Source:` and `Sources:` trailers into endnotes, set the article frontmatter to `publish: false`, added the visible `DRAFT, pending deacon review` note at the top of the article body, and smoothed the templated `Read from source:` transitions in the documentation-history section without changing the sourced substance.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; targeted scans confirming `publish: false`, draft note present, `## Notes` present, no inline source trailers before `## Sources`, and no article over-claim of the 69 identity. All passed.
- Acceptance result: Step 8 article pass accepted. Commit hash: `d632a8b`.

### Step 9 - Lectionary data change manifest
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Baseline selection: tagged pre-Phase-2 baseline `lectionary-baseline` at `af25b02cc152c4e0d35e2a8a06754fd1857ed16e`, the clean state immediately before the re-keyed dataset commit `6c0cb65`.
- What was done: added `scripts/build_lectionary_change_manifest.py`; generated `out/design/lectionary_change_manifest.csv` as the grouped review manifest, `out/design/lectionary_change_manifest.raw.csv.gz` as the exact row-level CSV audit archive, `out/design/affected_passages.csv` as the unique affected-passage join index, and `out/design/lectionary_change_manifest.md` as the human-readable summary and execution-log cross-check.
- Counts at generation time: grouped manifest rows `32921`; exact raw row-level CSV changes `427922`; affected passage keys `2791`.
- Data-diff commits captured in the baseline range: `03fb997`, `04cc512`, `2622ee2`, `350a0bd`, `440001d`, `6a15663`, `6c0cb65`, `85e7422`, `c9dd8bf`, `e2a5773`, `efbf63c`, `f1b0fbd`, `f79cbbc`.
- Verification: `python3 -m py_compile scripts/build_lectionary_change_manifest.py`; `python3 scripts/build_lectionary_change_manifest.py --baseline lectionary-baseline --head HEAD`; row-count and byte-size checks on the grouped CSV, raw gzip archive, affected-passages CSV, and manifest summary; banned-word and em-dash scan on the manifest artifacts; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 9 manifest pass accepted. Commit hash: `31eacaa`.

### Step 10 - Coptic-corpus handoff package
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Repo-access boundary: Hermes remained inside `coptic-lectionary-research` only and did not access or push `coptic-corpus`.
- What was done: assembled `out/handoff/` with the publish-candidate article, working spec, identity map, reverse lectionary index, today's-readings snapshot, passage footprint data, passage source disclosure data, source registry, Psalm MT/LXX crosswalk, foundational 69 table, Pascha and temporal support datasets, Synaxarium datasets, schema, grouped manifest, raw manifest gzip, affected-passage index, manifest summary, `open_questions_for_george.md`, `site_integration_spec.md`, and the `HANDOFF.md` index.
- Handoff guardrails recorded in `out/handoff/HANDOFF.md`: keep the article as a draft, preserve `INFERRED_LIKELY_SAME_SET` with roster unverified, keep `removed_marker` visible, treat the Synaxarium bridge as discovery links rather than direct proper-reading proof, and accept both MT and LXX Psalm numbering in search via `identity_key`.
- Verification: package inventory and size check over every `out/handoff/*` artifact; banned-word and em-dash scan on `HANDOFF.md` and `site_integration_spec.md`; `git diff --check`. All passed.
- Acceptance result: Step 10 handoff package accepted. Commit hash: `a04e64e`.

### Step 11 - Grok consistency audit of Steps 8 through 10 and final logging prep
- Producer of revisions: `openai-codex/gpt-5.5`, xhigh.
- Auditor: `xai-oauth/grok-4.3`, xhigh, via Hermes CLI one-shot with the `file` toolset only. No web/search/fetch tools were enabled or used. Audit prompt artifact was temporary and removed after the run.
- Audit artifact: `audit_artifacts/phase7_grok_steps1to3_audit.md`.
- Audit verdict at run time: conditional pass. Content, article guardrails, handoff guardrails, and 69 caveats passed. One required revision remained: execution-log and manifest cross-check alignment for commit `f1b0fbd`.
- Revision applied after the audit: recorded the exact commit hashes for Steps 5, 6, and 7 in this execution log; regenerated `out/design/lectionary_change_manifest.md` and refreshed the handoff copy so the cross-check now states that every committed CSV data-diff commit in the baseline range is found in the execution log by hash.
- Final consistency state after the revision: article still states `INFERRED_LIKELY_SAME_SET`, roster unverified; article still does not treat the 69 as calendar days; grouped manifest rows remain `32921`; exact raw row-level CSV changes remain `427922`; affected passage keys remain `2791`.
- Final artifact pointers: grouped manifest `out/design/lectionary_change_manifest.csv`; exact raw audit archive `out/design/lectionary_change_manifest.raw.csv.gz`; affected-passage index `out/design/affected_passages.csv`; handoff index `out/handoff/HANDOFF.md`.
- Verification: `python3 scripts/build_lectionary_change_manifest.py --baseline lectionary-baseline --head HEAD`; refreshed handoff manifest copies; `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_lectionary_change_manifest.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; targeted scans for banned words, em dashes, and stale 69 over-claim phrases. All passed.

### Step 12 - Push attempt to origin/main
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Push command: `git push origin main`.
- Remote state before the attempt: `origin/main` at `f7692ccbb5bd9c2ab109693c806945a9bd342e19`; local `main` 41 commits ahead.
- Result: push failed. GitHub rejected historical blobs over the 100 MB hard limit, specifically prior `out/design/reverse_lectionary_presentation.jsonl` blobs introduced in the unpublished local history. GitHub also warned about several 50 MB to 87 MB files that are above the recommended size.
- Side-effect boundary: no history rewrite, LFS migration, or branch surgery was attempted after the rejection because that would be a repo-wide history operation rather than a routine final push.
- Final local state: all requested work is committed locally; repo remains unpushed beyond `origin/main` because of the large-file history block. The only remaining untracked file is the pre-existing `audit_artifacts/phase2b_sus_source_psalm_numbering_2026-06-15.md`.

### Step 13 - Split reverse lectionary materialization into occasion and daily layers
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Identity-key guard: spot-checked an ordinary Great Lent weekday reading shared by `ordinary_date_resolved` and `katameros_cycle`. `1Cor 10:1-13` on Friday of the sixth week of Great Lent and `week 6 day_of_week 5` in the Katameros cycle both used identity key `rid_f72fd6622211f0669570`. A broader Great Lent shared-reference check found 280 shared weekday reference keys and zero identity-key mismatches.
- Step 1 commit: `c785f61` added `out/design/reverse_lectionary_index.jsonl`, with 8005 surviving occasion tuples, zero current-status or removed-marker disagreements, aggregated source disclosure, and attestation year spans.
- Step 2 commit: `60e45ca` added `out/design/daily/lectionary-2020.json` through `out/design/daily/lectionary-2035.json`, preserving 59324 dated rows from the source presentation table.
- Step 3 commit: `475f9f6` copied the shipped window into `out/handoff/`: `reverse_lectionary_index.jsonl`, `daily/lectionary-2026.json`, `daily/lectionary-2027.json`, and `daily/lectionary-2028.json`; it also updated the handoff and site integration specs.
- Step 4 reconciliation commit: `d0f46d7` retired `out/design/reverse_lectionary_presentation.jsonl` from the working tree, added it to `.gitignore`, regenerated deliverables, refreshed the manifest note, and recorded that the split is a materialization reshape with NO new affected passages for Bible-study audit.
- Final Step 4 verification: `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `python3 scripts/build_lectionary_change_manifest.py --baseline lectionary-baseline --head HEAD`; refreshed handoff manifest copies; `test ! -e out/design/reverse_lectionary_presentation.jsonl`; `git diff --check`. All passed.

### Step 14 - Grok split-materialization audit
- Auditor: `xai-oauth/grok-4.3`, using Hermes one-shot with the `file` toolset only. No web/search/fetch tools were enabled.
- Audit artifact: `audit_artifacts/phase8_grok_split_materialization_audit.md`.
- Initial audit found two documentation/process issues and no data-loss issue: stale `out/handoff/lectionary_spec.md` and Step 4 wording still marked in progress in this log.
- Revision applied: refreshed `out/handoff/lectionary_spec.md` from the generated root `lectionary_spec.md`; updated this execution log to record final Step 4 commit `d0f46d7` and verification state.
- Final audit verdict: PASS. Grok found no evidence that a distinct reading was lost between the retired monolith and the union of `out/design/reverse_lectionary_index.jsonl` plus `out/design/daily/lectionary-YYYY.json` files. Required revisions: none.

### Step 15 - Collapse split-index disclosure and refresh handoff
- Producer: `openai-codex/gpt-5.5`.
- History check: `7159e36` touched only `.DS_Store` and `.gitignore`; split reshape work remained in separate commits.
- Commit `a9f405e` collapsed `reverse_lectionary_index.jsonl` source disclosure by distinct `(source_family, source_kind, source_edition, source_title)` and kept representative locators plus per-source year spans. Verification reported 8005 index rows and zero distinct-source count mismatches.
- Commit `3fd410a` refreshed handoff/spec wording and copied the collapsed handoff index. Specs now state the two-layer model, shipped 2026 to 2028 daily window, collapsed source disclosure, and the structural-only daily-file limit.
- Commit `2459783` refreshed the manifest materialization note. Affected passages stayed at 2791 and the generated execution-log cross-check remained clean.
- Auditor: `xai-oauth/grok-4.3`, using Hermes one-shot with the `file` toolset only. No web/search/fetch tools were enabled.
- Audit artifact: `audit_artifacts/phase9_grok_split_collapse_audit.md`.
- Final audit verdict: PASS. Grok found no sign of reading loss and confirmed the distinct-source count per reading was unchanged by the disclosure collapse.

### Step 16 - 2026-06-18 cleanup adjudication prep
- Producer: `openai-codex/gpt-5.5`.
- Version decision: `npm view @andraws/lectionary-data versions --json` showed `1.0.0` and `1.0.1`; `1.1.0` remains unpublished and is the selected package version for this cleanup.
- CHANGE 1 commit: `6322280` canonicalized verse-set span references so contiguous comma-list forms and range forms collapse when they represent the same sorted verse set. Targeted validation passed for `Ps 33:10,33:11` to `Ps 33:10-11`, while `Ps 62:7,62:2` and `Ps 62:7,62:6` remained distinct; `python3 -m py_compile passage_normalization.py`; `git diff --check -- passage_normalization.py`.
- CHANGE 2 commit: `7c210b6` corrected the exact `Fast of Ninevah` source title/day-title label to `Fast of Nineveh` and left `Great Lent/Jonah/Nineveh cycle` unchanged. Targeted validation passed against cached `2026-02-02` copticchurch HTML; `python3 -m py_compile build_lectionary_reference.py build_design_deliverables.py`; `git diff --check -- build_lectionary_reference.py build_design_deliverables.py`.
- CHANGE 3 commit: `ab0a677` retired `Psalm+Gospel` and `Psalm + Gospel` token rows by assigning each extracted passage token to `Psalm`, `Gospel`, or `source_label_preserved`. Targeted validation over existing Pascha and Bright Saturday source rows found `67` active Psalm tokens, `92` active Gospel tokens, `2` superseded Gospel audit tokens, and `0` ambiguous preserved tokens; `python3 -m py_compile build_lectionary_crosswalk.py build_design_deliverables.py`; `git diff --check -- build_lectionary_crosswalk.py build_design_deliverables.py`.
- Documentation update: `audit_artifacts/open_questions_for_george.md` now has a 2026-06-18 adjudication section for George and Fr. Boulos covering the P2 genuine source disagreements, the P2 inferred local merges pending external confirmation, and the P4 prophecy-ordering gap pointer.
- Full rebuild and package validation outcome: `PYTHONDONTWRITEBYTECODE=1 LECTIONARY_DISABLE_VAULT_PUBLISH=1 python3 build_lectionary_reference.py` passed; `python3 build_design_deliverables.py` produced `reverse_lectionary_index_rows=8003`; `python3 verify_lectionary_queries.py` passed with `invalid_spans=0`; `python3 verify_design_deliverables.py` passed; explicit JSONL parsing checked 31 files and 413440 rows; every occasion-index row carries `slot_type`, `slot_order`, and `occasion_kind` keys, with the 63 nullable `slot_order` values limited to `source_label_preserved` rows by schema; `node scripts/build_npm_package.mjs` produced version `1.1.0`, `source_repo_commit=4a78ec59580ad31fc6a17cec03544bba81241917`, and `occasion_index_rows=8003`; `npm pack --json` produced `andraws-lectionary-data-1.1.0.tgz` with 9 files, tarball size 942224 bytes, max unpacked file size 16333963 bytes, and all package rows parsed.

### Step 17 - 2026-06-18 fixed Coptic day package cleanup
- Producer: `openai-codex/gpt-5.5`.
- Version decision: `npm view @andraws/lectionary-data versions --json` showed `1.1.0` is published, so this cleanup uses package version `1.1.1`.
- Source/data cleanup commit: `57636a1` resolved fixed Coptic day occasions by using the concrete Katameros `day_name` / `day_key` as the public reverse-lectionary `occasion` when `source_type=annual fixed Coptic day`. The generic source-type label remains only source metadata, not a public occasion.
- Duplicate validation: `audit_artifacts/annual_fixed_coptic_day_duplicate_audit_2026-06-18.csv` records all `606` old generic reverse-index rows; all `606` had concrete fixed-day duplicate/source rows, representing `4526` presentation rows across `366` fixed Coptic days. Missing duplicate/source rows: `0`.
- Source of confusion: `build_lectionary_crosswalk.py` used Katameros `source_type` as `liturgical_place`; for AnnualReadings fixed days, `source_type` is the generic label while `day_name` / `day_key` already carries the specific Coptic date.
- Rebuild and validation outcome: `PYTHONDONTWRITEBYTECODE=1 LECTIONARY_DISABLE_VAULT_PUBLISH=1 python3 build_lectionary_reference.py` passed; `PYTHONDONTWRITEBYTECODE=1 python3 build_design_deliverables.py` produced `reverse_lectionary_index_rows=11923`; `PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py` passed with `invalid_spans=0`; `PYTHONDONTWRITEBYTECODE=1 python3 verify_design_deliverables.py` passed; generated public outputs checked with `0` rows containing `annual fixed Coptic day`.
- Package rebuild: `node scripts/build_npm_package.mjs` produced `@andraws/lectionary-data@1.1.1`, `source_repo_commit=57636a15a6fb363847cd72492f531b64a8ac9c35`, and `occasion_index_rows=11923`.
- Package validation: `npm pack --json` from `packages/lectionary-data` produced `andraws-lectionary-data-1.1.1.tgz` with `9` files, tarball size `1221466` bytes, max unpacked file size `23251619` bytes, all JSON/JSONL rows parsed, and `0` package reverse-index hits for `annual fixed Coptic day`.
- Publish note: package was packed and validated only. `npm publish` was not run.
