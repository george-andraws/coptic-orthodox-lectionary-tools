# Phase 1 Grok Audit Pass 1

## Findings

1. **Core schema coverage is mostly present.**
   - `reading_identity` covers identity keys, display refs, MT/LXX canonical refs, source convention, canonicalization confidence, notes, and span storage.
   - `liturgical_placement` covers day/hour/section placement, slot, and ordering.
   - `temporal_attestation` covers source, authority tier, current status, and validity window.
   - `synaxarium_commemoration` plus `synaxarium_reading_bridge` gives a workable Synaxarium model with commemoration identity, date, rank, type, source URL, bridge basis, confidence, and citation.

2. **Wednesday fixture shape is partly handled.**
   - Multiple prophecies per hour can be represented by repeated `liturgical_placement` rows using the same `service_day`, `service_hour`, and `service_section`, with distinct `slot` and `order`.
   - Composite Psalm references can be represented through `spans_json`, but the packet does not define the required internal shape of `spans_json`.
   - Named readings are not yet explicit. They might be forced into `slot` or `service_section`, but that is too brittle for Coptic Reader fixture governance.

3. **Psalm crosswalk posture is mostly correct.**
   - The packet does not claim that all verse offsets are solved.
   - High-confidence rows are tied to Brenton/KJV content comparison examples.
   - Medium-confidence rows correctly flag chapter seam checks where exact verse equivalence still needs text review.
   - The `Ps 63:1 -> LXX Ps 62` and `Ps 68:17 -> LXX Ps 67` examples are properly cautious because they do not assert exact LXX verse equivalence.

4. **There is one material confidence inconsistency.**
   - Crosswalk example: `Ps 69:17 -> LXX Ps 68:17` is marked `medium`, with basis only “chapter seam verified by phase2b audit.”
   - Fixture row: `Psalm 68:17` is mapped to `Ps 69:17 (LXX Ps 68:17)` with `high` confidence and note “fixture label mapped by prior content comparison.”
   - Those two claims conflict unless there is a separate content-comparison artifact not shown in the packet.

5. **Current Coptic Reader fixture labels are being respected in intent.**
   - Fixture labels are preserved in `source_ref`.
   - Pending MT equivalence is explicitly preserved for `Psalm 41:1`.
   - Medium-confidence notes such as `fixture_label_preserved_mt_equivalence_requires_text_review` and `chapter_mapped_verse_offset_not_guessed` are the right pattern.

6. **The schema vocabulary and table columns are not fully aligned.**
   - Vocab includes `occasion_type`, but `liturgical_placement` uses `occasion`.
   - Vocab includes `source_authority_tier`, but `temporal_attestation` uses `authority_tier`.
   - Vocab includes `attestation_bucket`, but no shown table includes it.
   - Vocab includes `current_authority`, but no shown table uses it.
   - This is not fatal for Phase 1, but it needs tightening before downstream build work treats the schema as stable.

7. **The verifier result is useful but not sufficient as acceptance evidence.**
   - `python3 verify_design_deliverables.py -> design deliverables verified` confirms internal deliverable checks passed.
   - It does not, by itself, prove that named readings, composite `spans_json`, or all confidence semantics are locked well enough for Phase 2 ingestion.

## Required Revisions

1. **Add an explicit raw fixture label field.**
   - Add a field such as `source_ref`, `source_label`, or `fixture_label` to the durable schema.
   - Do not leave Coptic Reader’s governing label only in an external fixture artifact.
   - This is needed so current fixture labels govern within scope after data is normalized.

2. **Define the `spans_json` contract.**
   - It should support ordered multiple spans.
   - Each span should carry at least:
     - source reference as printed
     - source convention
     - canonical MT ref, if text-anchored
     - canonical LXX ref, if text-anchored
     - confidence
     - note or validation basis
   - Composite cross-Psalm references should not depend on one flattened `canonical_mt_ref` and one flattened `canonical_lxx_ref`.

3. **Make named readings first-class.**
   - Add a field such as `reading_name`, `source_heading`, or `fixture_reading_label`.
   - `slot` and `order` are not enough for named Wednesday readings.
   - This matters for Coptic Reader labels such as prophecy blocks, Psalm/Alleluia forms, and other named service readings.

4. **Resolve the `Ps 69:17 / LXX Ps 68:17` confidence conflict.**
   - If Brenton/KJV content comparison exists, upgrade the crosswalk example with that validation basis.
   - If it does not exist, lower the fixture row from `high` to `medium`.
   - Do not let the fixture table claim stronger evidence than the crosswalk table.

5. **Do not store tentative MT equivalence as canonical equivalence.**
   - For rows like `Psalm 6:2-3`, if exact MT verse equivalence still requires Brenton/KJV text review, avoid setting `canonical_mt_ref` to the same verse range as though it were solved.
   - Safer pattern:
     - preserve the Coptic Reader source label
     - keep LXX/source-side reference
     - leave MT blank or mark it explicitly as pending
     - retain medium confidence

6. **Align vocabulary names with table columns.**
   - Either rename table fields to match vocab or add aliases with clear definitions.
   - Specific fixes:
     - `occasion` vs `occasion_type`
     - `authority_tier` vs `source_authority_tier`
     - place `attestation_bucket` in a concrete table
     - clarify whether `current_authority` is distinct from `current_status`

7. **Separate chapter-level seam mappings from verse-level examples.**
   - Crosswalk rows should distinguish:
     - chapter equivalence
     - split/merge seam behavior
     - anchored verse examples
     - unresolved verse offsets
   - This prevents downstream code from treating example refs as a complete verse-by-verse Psalm alignment.

## Outcome

**Conditional Phase 1 pass.**

The packet satisfies the main design direction: reading identity, liturgical placement, temporal attestation, Synaxarium bridge modeling, Wednesday hour structure, and cautious MT/LXX Psalm handling are all present.

It should not be treated as a frozen Phase 2 ingestion contract until the required revisions above are made, especially the raw fixture label field, named reading field, `spans_json` contract, and the `Ps 69:17 / LXX Ps 68:17` confidence correction.
