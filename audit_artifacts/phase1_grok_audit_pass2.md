# Phase 1 Grok Audit Pass 2

## Findings

- Resolved: `reading_identity.source_label` gives a durable raw fixture/source label field.
- Resolved: `spans_json` now carries source convention, canonical MT/LXX refs, confidence, validation basis, and source ref for scriptural spans.
- Resolved: named readings are first-class through `reading_type = named-reading`, `reading_name`, empty canonical refs, and empty `spans_json`.
- Resolved: the Ps 68:17 LXX fixture row is no longer stored as the prior conflicting Ps 69:17 MT mapping. It is now anchored as `LXX Ps 68:17` to `MT Ps 69:16` with high confidence.
- Resolved: unresolved `LXX Ps 41:1` no longer stores a tentative MT equivalent. `canonical_mt_ref` is blank and the note clearly requires text review.
- Resolved: chapter-level Psalm mappings are separated from anchored verse examples through `mapping_scope`.
- Not fully resolved: vocabulary/table field alignment still has a mismatch in `temporal_sample`.

## Required Revisions

1. Align `temporal_sample.current_authority` with the controlled vocabulary or expand the vocabulary.

   The schema defines `temporal_attestation.current_authority`, and the controlled vocabulary allows only:

   - `Coptic Reader fixture where captured`
   - `public date-resolved source is reference only`
   - `historical source is witness only`
   - `scholarly source governs structure, not current readings`

   But the emitted sample uses:

   - `not Coptic Reader confirmed`

   That value is not in the controlled vocabulary.

2. Clarify whether extra `temporal_sample` fields are emitted table fields or joined/reporting fields.

   The `temporal_attestation` schema lists:

   - `identity_key`
   - `source_key`
   - `source_authority_tier`
   - `current_status`
   - `attestation_bucket`
   - `current_authority`
   - `valid_from`
   - `valid_to`

   But `temporal_sample` also includes fields such as:

   - `day_title`
   - `service_hour`
   - `display_ref`
   - `lifecycle_status`
   - `derivation`
   - `attesting_sources`

   If these are from a joined audit view, label them as such. If they are emitted in the core table, add them to the schema and align their vocabularies.

## Outcome

Not approved for Phase 1 commit yet.

The main schema and Psalm crosswalk revisions are substantially fixed, but the vocabulary/table alignment requirement remains open because `temporal_sample.current_authority` is outside the declared controlled vocabulary and the sample includes unmodeled fields. Once that is corrected or explicitly documented as a reporting view, Phase 1 is commit-ready.
