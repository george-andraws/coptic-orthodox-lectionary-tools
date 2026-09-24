# Lectionary design-layer orchestration and Psalm crosswalk lessons

Use this reference when the requester asks for a multi-phase Coptic lectionary design/data effort, especially one involving Coptic Reader fixtures, MT/LXX Psalm identities, source attestation, Synaxarium bridges, or site-facing presentation datasets.

## Orchestration pattern

- Treat the written phase plan as an execution contract. Maintain an execution log under `audit_artifacts/` and update it after each checkpoint, not only at the end.
- Enforce artifact independence in audits: the auditor must be a different model/worker than the artifact producer. If Codex generates article/data artifacts, use an independent reviewer for independent audit when available; if an independent reviewer generates research, audit it with Codex.
- Run at most two audit passes per checkpoint when the plan says revise and re-run at most twice. After pass 2, apply narrow corrective fixes, log the remaining issue and correction, then proceed instead of starting an unbounded audit loop.
- If an independent reviewer or another external worker loops or returns mostly reasoning, restart with a bounded source packet and require final Markdown only. Preserve the final memo/audit artifact, not raw hidden-reasoning captures.
- Keep generated outputs reproducible from a script. Prefer `build_design_deliverables.py` plus `verify_design_deliverables.py` style artifacts over manual CSV edits.

## Coptic Reader fixture identity rules

- Coptic Reader fixture labels govern within their captured scope. Preserve the original fixture label in durable fields such as `source_ref` and `source_label`.
- Do not pass Coptic Reader Psalm labels through a generic MT/NKJV canonicalizer before the LXX-preserving fixture path sees them. This can shift labels twice and produce false mappings.
- For fixture rows, build identity from the preserved source-side LXX/liturgical label, then add MT equivalence only when text-anchored.
- Named readings such as `Memoirs of Job` must be first-class: `reading_type = named-reading`, `reading_name` populated, canonical biblical refs blank, and no fabricated passage span.

## Psalm MT/LXX crosswalk rules

- Separate chapter-level mapping from verse-level examples. Add an explicit scope field such as `mapping_scope` with values like:
  - `chapter_equivalence`
  - `split_merge_chapter_seam`
  - `lxx_unique_chapter`
  - `anchored_verse_example`
  - `unresolved_verse_offset_example`
- Do not claim complete verse-by-verse Psalm alignment when only selected Brenton/KJV comparisons were performed.
- Use public-domain Brenton LXX and KJV text comparison for exact fixture Psalm offsets where possible.
- Keep unresolved fixture Psalm refs visibly pending. Example pattern: `LXX Ps 41:1 (MT equivalent pending)` with blank `canonical_mt_ref` and medium confidence.

Verified example offsets from the design-layer run:

| LXX / fixture ref | MT / KJV ref | Basis |
|---|---|---|
| Ps 50:6 | Ps 51:4 | Brenton/KJV content comparison |
| Ps 32:10 | Ps 33:10 | Brenton/KJV content comparison |
| Ps 41:6 | Ps 42:5 | Brenton/KJV content comparison |
| Ps 83:2 | Ps 84:1 | Brenton/KJV content comparison |
| Ps 83:5 | Ps 84:4 | Brenton/KJV content comparison |
| Ps 40:6-8 | Ps 41:5-7 | Brenton/KJV content comparison |
| Ps 6:2-3 | Ps 6:1-2 | Brenton/KJV content comparison |
| Ps 68:17 | Ps 69:16 | Brenton/KJV content comparison |
| Ps 41:1 | unresolved | Preserve LXX label and leave MT pending until text review |

Pitfall: LXX Ps 68:17 is not MT Ps 69:17. Brenton's “Hear me, O Lord; for thy mercy is good...” matches KJV Psalm 69:16, not Psalm 69:17.

## Schema and verifier rules

For a presentation-ready design layer, include these fields and enforce them in a verifier:

- reading identity: `identity_key`, `reading_type`, `reading_name`, `source_label`, `display_ref`, `canonical_mt_ref`, `canonical_lxx_ref`, `source_convention`, `canonicalization_confidence`, `canonicalization_note`, `spans_json`
- presentation rows: `source_key`, `source_kind`, `source_family`, `source_file`, `source_row_id`, `authority_tier`, liturgical placement fields, `source_ref`, `raw_ref`, `url`, `provenance`
- temporal view: `current_status`, `source_authority_tier`, `attestation_bucket`, `current_authority`, `valid_from`, `valid_to`, plus any emitted reporting fields listed in schema
- source registry: every emitted `source_key` must be registered; every emitted `authority_tier` must be in the controlled vocabulary

Verifier checks that prevented regressions:

- row counts match the build summary
- all presentation rows join to `reading_identity`
- no blank source keys, display refs, or provenance/url/source-file evidence
- all `source_convention`, `current_status`, `authority_tier`, and `current_authority` values are controlled
- no unregistered emitted source keys
- Coptic Reader fixture rows preserve Psalm LXX labels and do not invent unresolved MT equivalents
- `spans_json` has source ref, convention, canonical refs, confidence, validation basis, book, chapter, and verse fields for scripture rows

## Phase commit hygiene

- Commit phase-scoped artifacts only. Do not commit later-phase generated datasets early just because the generator already emitted them.
- If a commit hash is written into an execution log, record it in a follow-up log-only commit, because amending the same commit changes the hash.
- Keep transient raw audit captures out of commits when they contain tool chatter or hidden reasoning text.

## Source attestation and temporal residue rules

- Scripture identity keys must be independent of source label. For Scripture rows, hash identity from canonical MT and canonical LXX refs, not from the raw source label; otherwise Coptic Reader and Katameros rows for the same reading can fail to join.
- When adding text-anchored Psalm mappings in one direction, also add the inverse direction used by MT-source rows. Otherwise fixture rows may map correctly while Katameros rows still produce naive chapter-shift LXX refs.
- Pascha attestation should emit both row-level evidence and a bucket manifest. The manifest should include zero-count controlled buckets, so absence is explicit rather than inferred.
- Attestation citations should be replayable. Prefer `source_key`, `source_file`, `source_row_id`, and `source_ref` in the citation string over weak labels such as `api`.
- Keep `attestation_note` as a row-level field for unresolved or single-source cases. This prevents audit reasoning from being stranded only in prose reports.
- Temporal classification needs a residue table and a manifest. The residue count should equal non-current temporal rows, and the manifest should include a `true_source_disagreement` row even when the count is zero.
- Avoid wording that implies a row is current or removed when the source scope does not prove it. Use terms like `pending_psalm_equivalence_unresolved`, `candidate_removed_needs_current_authority_confirmation`, and `no scoped current authority confirmation` rather than overclaiming Coptic Reader confirmation or removal.

## Synaxarium ingestion pitfalls

- St-Takla Synaxarium index rows can mix clean numbered heading snippets with repeated full prose paragraphs. Do not emit the repeated prose as separate commemoration titles. Stop parsing once detailed prose begins after clean heading snippets.
- Some single-entry days lack numbered heading snippets. For those, infer the title from the first source-summary lead, mark `extraction_method = prose_lead_inferred`, and add a caveat that publication wording needs source-page review.
- Emit `extraction_method`, `caveat`, `source_url`, `source_day_title`, and full `source_summary` for every commemoration. Do not truncate `source_summary` when it is the replay evidence.
- Deduplicate repeated numbered headings before assigning ranks.
- Add verifier guards for: unique `commem_id`, no day-title fallback rows, no day-title-looking titles, no long prose-like titles, prose-lead rows have caveats, source URLs and summaries are present, and broad generic classifications are caveated.
- Theotokos classification must be narrow. Do not classify every title containing “virgin” as Theotokos; require explicit Mary/Theotokos wording such as Theotokos, Virgin Mary, St. Mary, Saint Mary, or Holy Virgin Mary.
- Treat commemoration `type` as assistive metadata, not a canonical theological taxonomy. Generic `commemoration` is acceptable when safer than forcing an uncertain saint/event class.

## Synaxarium bridge semantics

- For fixed-day Synaxarium to Katameros links without explicit proper-reading evidence, use `basis = collection-type` and conservative `confidence = medium`.
- The bridge should link only the primary commemoration unless a future source gives explicit proper-reading evidence for secondary commemorations.
- Do not let `high` confidence mean “single commemoration day” when the evidence is still collection-type. That overstates source-directness.
- Repeated `(commem_id, coptic_day_key, slot)` groups can be valid when the bridge catalogs source rows or variants, but every row note must say it is not a resolved daily service schedule and not direct proper-reading proof.
- Verifier checks should enforce: bridge `commem_id` exists, `reading_identity_key` exists, `display_ref` and `slot` are present, collection-type rows are medium confidence, non-primary links are absent, and duplicate slot groups are explicitly documented as catalog or variant rows.

## Phase 6 handoff deliverables

- Site-facing deliverables should separate reader-facing article, machine datasets, integration spec, open questions, and deck handoff files. Do not rely on a single narrative article to carry implementation warnings.
- The site integration spec should explicitly tell the maintainer that Synaxarium bridge rows are medium-confidence discovery links, not direct proper-reading proof and not a resolved daily service schedule.
- `open_questions_for_george.md` should end with direct push-package pointers: article, integration spec, reverse presentation dataset, today snapshot, passage footprint, Synaxarium datasets, deck files, and execution log.
- Deck deliverables for this class should be treated as handoff aids. Minimum useful deck: story of the problem, identity model, Psalm numbering, Pascha attestation, temporal residue, Synaxarium bridge limits, site package, open questions, and the maintainer’s push path.

## Phase 6 finalization and audit closure pattern

Use this checklist when finishing the lectionary design-layer Phase 6 package or a similar final publication handoff:

1. Start from live repo state, not handoff memory: `git status --short`, recent commits, existing generated outputs, and execution log.
2. Regenerate from scripts rather than hand-editing outputs: compile generator/verifier/deck script, run `build_design_deliverables.py`, run the deck builder, then run `verify_design_deliverables.py`.
3. Add deterministic guards for any audit-discovered wording or data invariant. Useful Phase 6 guards include exact `Scripture is from NKJV.`, `Teaching guide` not `Lesson Guide`, no reader-facing permission/source-policy wording, no long Synaxarium titles over the agreed threshold, and repeated bridge rows documenting `source-row or variant catalog` plus not-direct-proof and not-resolved-schedule language.
4. Verify all CSV and JSONL counts against `BUILD_DESIGN_SUMMARY.json`, not just CSV counts. Check presentation rows join to `reading_identity`, emitted `source_key` values are registered, and controlled vocabulary fields are valid.
5. Preserve Phase 5 Synaxarium invariants explicitly: 366 source Coptic days, 664 commemorations, 141 caveated prose-lead rows, 0 day-title fallback rows, 0 long prose-like titles, 4,688 bridge rows, all `basis=collection-type`, all `confidence=medium`.
6. For deck QA, inspect PPTX structure by extracting slide XML/text and counting slides. Check no placeholders, no em dashes, no banned terms. If visual-model inspection is unavailable, generating a non-empty macOS QuickLook thumbnail is acceptable as a limited visual sanity check, but report it as limited.
7. When running a an independent reviewer audit through Hermes CLI, the captured stdout may include visible reasoning/tool chatter before the final Markdown. Before committing the audit artifact, strip everything before the final `# Phase ... Audit ...` heading. Preserve the final memo, not raw reasoning captures.
8. If the independent audit gives a process-only conditional pass, update the execution log, rerun verification, and run a focused second audit pass. Do not rerun an unbounded audit loop.
9. Commit the full Phase 6 artifact package first, then record that commit hash in `audit_artifacts/lectionary_execution_log.md` with a second log-only commit. Leave unrelated untracked files unstaged.
10. Final response should separate artifact commit hash from log-only hash, list the push/review package, state unresolved questions, and explicitly say no site push was done.
