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
