# Phase 5 Grok Synaxarium Bridge Audit Pass 1

## Findings

- Referential integrity passes at the packet level:
  - 4,688 bridge rows emitted.
  - 0 missing `commem_id`.
  - 0 missing `reading_identity_key`.
  - 0 blank `display_ref` or `slot`.
  - 0 reported multi-day confidence errors.
  - 0 non-primary commemoration links.

- Primary-vs-secondary commemoration handling is conservative and correct:
  - The bridge links only rank 1 commemorations.
  - Secondary commemorations are not assigned fixed-day readings by inference.
  - The medium-confidence note is honest: secondary commemorations require explicit proper-reading evidence before separate links are created.

- `basis = "collection-type"` is the correct label for the evidence shown:
  - The citation chain supports a collection-level bridge: F.N. Youssef on daily readings following the Synaxarium, St-Takla day indexing, and local Katameros fixed-day rows.
  - The rows do not claim direct proper-reading evidence for each individual saint or feast.
  - Keeping all rows as `collection-type` is more honest than calling them direct, date-only, or proper-reading links.

- Confidence labeling is the main weakness:
  - `high` appears to mean “single commemoration day alignment.”
  - It does not mean “direct source proves this exact reading belongs to this exact commemoration.”
  - Because every row is still `collection-type`, downstream users may overread `high` as stronger evidence than the bridge actually has.

- The high-confidence Tut 4 sample exposes a second semantic risk:
  - The same commemoration/day has multiple readings for the same slot family, including repeated `liturgy_catholic`, `liturgy_pauline`, `liturgy_acts`, `matins_gospel`, and `liturgy_gospel` slots.
  - That can be valid if the bridge is a collection catalog or variant-bearing relation.
  - It is not valid if consumers expect one resolved reading per liturgical slot for that Coptic day.

## Required Revisions

- Required before commit: clarify or revise the confidence semantics.
  - Best option: define `confidence` as commemoration-target confidence, not source-directness confidence.
  - Safer option: downgrade all `collection-type` rows to `medium` unless a direct proper-reading source exists.
  - If `high` is retained, the documentation must explicitly say that high collection-type rows are not direct proof of a proper reading for the named commemoration.

- Required before commit: clarify repeated-slot semantics.
  - If repeated slots are intentional, document that the bridge is not a resolved daily service schedule.
  - If repeated slots are not intentional, add a check for duplicate `(commem_id, coptic_day_key, slot)` groups and revise the emitted rows.

- Keep the primary-only rule.
  - Do not create secondary commemoration links without explicit proper-reading evidence.
  - The current `non_primary_commem_links = 0` result is a strength, not a defect.

- Keep `basis = "collection-type"` for these rows.
  - Changing the basis to a stronger label would overclaim the evidence.

## Outcome

Conditional pass.

There is no referential-integrity blocker in the reported verifier output. The bridge joins are clean, primary-only handling is defensible, and the collection-type basis is honest.

There is a commit blocker unless the confidence and repeated-slot semantics are revised or documented before commit. The emitted data is usable as a cautious collection-type bridge, but not yet safe as a direct proper-reading bridge or a resolved per-day reading schedule.
