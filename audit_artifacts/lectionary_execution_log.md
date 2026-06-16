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
- Verdict: `CONFIRMED_SAME_SET` with wording caveat. The Ottawa/UKMID dated TOC entries may be treated as the same practical second-volume collection Youssef names, based on source identity, volume placement, annual mapping function, commemoration categories, and count. The consulted ACCOT Youssef page gives the concept, count, Arabic name, function, and second-volume placement, but not a date-by-date roster.
- Verification: Codex re-pulled the Ottawa PDF, extracted pages 23 to 26 with `pypdf`, confirmed 69 dated TOC entries, confirmed sample annual table rows mapping days to the same dated sections, and fetched ACCOT with `curl -L --compressed` after plain Python returned HTTP 406.
- Acceptance result: Step 1 accepted for Steps 2b, 4, and 7. Commit hash: pending this commit.

### 2026-06-16 - Step 2a Pascha computation clarity
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Sources checked: World Council of Churches and Middle East Council of Churches, `Towards a Common Date for Easter`, Aleppo, 1997; Orthodox Church in America, `Concerning the Date of Pascha and the 1st Ecumenical Council`; F.N. Youssef, `The Arrangement of the Church Lectionary`.
- What was done: Added one article sentence clarifying that Youssef's phrase about the Hebrew calendar is about the Church's Paschal computation, the Nicene norm of the Sunday following the first vernal full moon as later calculated through the Alexandrian mode, not a lookup of the present-day Hebrew calendar. Added the WCC/MECC source to the article source list.
- Source limitation: A clean source for the claim that Coptic Pascha always falls on the same date as Eastern Orthodox Pascha was not found in this step. The article omits that clause, and `audit_artifacts/open_questions_for_george.md` now records the shared-date source check.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 2a accepted. Commit hash: pending this commit.

### 2026-06-16 - Step 2b 69 identity wording
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Step 1 dependency used: `CONFIRMED_SAME_SET`, with caveat that the consulted Youssef page does not print a date-by-date roster.
- What was done: Updated the article to state that the Ottawa/UKMID Katameros of the Days presents the same practical second-volume collection in English, with the basis stated as source identity, volume placement, function, and count. Removed the stale open question about the full English list of the 69 because the Ottawa/UKMID TOC now supplies the controlled roster for this run.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 2b accepted. Commit hash: pending this commit.

### 2026-06-16 - Step 2c NKJV wording
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Check performed: Scanned `coptic-lectionary-and-synaxarium.md` for NKJV references, block quotes, and verse-like reproduced text. The article contains Scripture references and no NKJV verse text.
- What was done: Changed the source line from `Scripture is from NKJV.` to `Scripture references follow NKJV versification.` Updated `verify_design_deliverables.py` so the verifier enforces the new Step 2c wording and rejects the old wording.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed after the verifier was updated to match the Step 2c requirement.
- Acceptance result: Step 2c accepted. Commit hash: pending this commit.

### 2026-06-16 - Step 2d citation locators and minor notes
- Producer: `openai-codex/gpt-5.5`, xhigh. Intended Grok research worker timed out before writing an artifact; source evidence was pulled directly with terminal HTTP and PDF extraction. Independent Grok audit remains the Step 8 gate.
- Sources checked: CCDL API item 1199; CCDL `Lectionary` PDF text; ACCOT Youssef page; Open Library OL2304712M JSON; Crossref, Open Library search, Internet Archive advanced search, and repo local search for Burmester.
- What was done: Confirmed the Coptic Encyclopedia byline from CCDL and updated the article wording to `Basilios, Archbishop, and Coquin, René-Georges`. Added traditional-attribution language to the Abuqti paragraph and glossary. Added a note that the article reports Youssef's `15 weeks or 107 days` figure as given, while 15 weeks is 105 days.
- Items flagged instead of guessed: Burmester pages 83 to 137 were not confirmed. Zanetti series/year was not cleanly confirmable because Open Library gives Publications de l'Institut orientaliste de Louvain 33, 1985, while the CCDL Coptic Encyclopedia PDF bibliography gives 31, 1988.
- Audit artifact: `audit_artifacts/phase7_step2d_source_check.md`.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`. All passed.
- Acceptance result: Step 2d accepted. Commit hash: pending this commit.

### 2026-06-16 - Step 3 documentation-history section
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Sources checked: Ottawa/UKMID extracted PDF front matter for Days, Sundays, Pentecost, and Holy Pascha; direct HTTP availability for UKMID PDF URLs; St. Bishoy Deacons' Corner Katameros page; CCDL Coptic Encyclopedia metadata; ACCOT Youssef page; repository source registry; `out/design/psalm_mt_lxx_crosswalk.csv`; eBible World English Bible copyright information; Wikisource King James Bible copyright note.
- What was done: Added `## How the lectionary has been documented` to the generated article, explaining printed Katameros witnesses, public documentation layers, scholarly structural sources, Burmester as older Holy Week witness, scoped Coptic Reader current authority, and Bible text comparison anchors. Added UKMID, St. Bishoy, Brenton, WEB, and KJV policy anchors to the Sources list without changing the existing inline `Source:` attribution style.
- Attribution discipline: New section labels `Read from source` and one explicit `Inference from the design residue` statement.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; generated-article scan for em dash and banned words. All passed.
- Acceptance result: Step 3 accepted. Commit hash: pending this commit.

### 2026-06-16 - Step 4 foundational-reading controlled vocabulary
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Inputs: Step 1 Grok investigation and Codex audit; Ottawa/UKMID `Katameros_Days.pdf`; ACCOT Youssef page.
- What was done: Replaced the old count-only `collection_types_69` placeholder with an enumerated controlled vocabulary. Added `FOUNDATIONAL_69_SOURCE_PROVENANCE`, `FOUNDATIONAL_69_RAW`, generated `out/design/foundational_reading_collections_69.csv`, generated `out/design/foundational_reading_collections_69.jsonl`, embedded 69 entries in `out/design/lectionary_schema.json`, added a `foundational_reading_collection` schema table, added `st_mary_ottawa_days` to the source registry, and documented the vocabulary in `lectionary_spec.md`.
- Membership verdict: `CONFIRMED_SAME_SET`, with caveat that identity is inferred from source identity, volume two placement, annual mapping function, commemoration categories, and count. The consulted Youssef page does not print the date-by-date roster.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; explicit row-count sanity check. All passed.
- Acceptance result: Step 4 accepted. Commit hash: pending this commit.

### 2026-06-16 - Step 5 removed-marker model field
- Producer: `openai-codex/gpt-5.5`, xhigh.
- Inputs: Ottawa Holy Pascha extracted source text, Coptic Reader Wednesday Day fixture supplied by George, generated `pascha_source_text_index.csv`, generated Pascha day-hour rows, and Step 5 requirements from the locked design brief.
- What was done: Added a uniform `removed_marker` field to the presentation, attestation, temporal classification, and residue outputs. The marker is populated only for older Pascha Wednesday placements absent from the scoped Coptic Reader Wednesday Day fixture. Retained the removed readings as historical rows, including Isaiah 48:1-6, Isaiah 59:1-17, Zechariah 11:11-14, extra Proverbs rows, and Job 27 to 28 rows.
- Boundary note: Markers cite the actual older source witness and current comparator. Example source boundaries include St. Mary Ottawa Holy Pascha p. 308 line 7779 for Isaiah 48:1-6, p. 320 line 8091 for Isaiah 59:1-17, p. 322 line 8133 for Zechariah 11:11-14, p. 318 line 8038 for Proverbs 1:10-33, p. 299 line 7552 for Proverbs 4:4-27,5:1-4, and p. 298 line 7519 for Job 27:16-28:2.
- Generated output impact: `reverse_lectionary_presentation` now has 66,381 rows, `reading_identity` has 2,658 rows, `pascha_attestation` has 446 rows, and `temporal_residue` has 420 rows. The generator now retains 11 rows with `removed_marker`.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; explicit removed-marker row check. All passed.
- Acceptance result: Step 5 accepted. Commit hash: pending this commit.

### 2026-06-16 - Step 6 citable provenance and source-disclosure data
- Producer: `openai-codex/gpt-5.5`, xhigh.
- What was done: Added registry-level `edition` and `default_locator` metadata, carried `source_title`, `source_edition`, `source_locator`, and `source_url` into placement rows, aggregated source titles, editions, and locators into Pascha attestation and temporal classification rows, and created `out/design/passage_source_disclosure.csv/jsonl` for page-level source disclosure.
- Disclosure output: `passage_source_disclosure` emits one row per presentation placement/source row, with identity, display reference, source key, title, edition, locator, URL, source reference, occasion, slot, current status, removed marker, and replayable citation.
- Generated output impact: `passage_source_disclosure` has 66,381 rows. Existing design-row counts are otherwise unchanged from Step 5.
- Verification: `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py`; `python3 build_design_deliverables.py`; `python3 verify_design_deliverables.py`; `git diff --check`; explicit disclosure schema and row-count checks. All passed.
- Acceptance result: Step 6 accepted. Commit hash: pending this commit.
