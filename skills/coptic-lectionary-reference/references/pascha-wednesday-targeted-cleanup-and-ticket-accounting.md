# Pascha Wednesday Targeted Cleanup and Ticket Accounting

Use this reference for bounded Pascha Wednesday cleanup/reporting work in `coptic-lectionary-research`, especially when the requester asks for corrected source data, regenerated reverse-index handoff files, or ticket-accounting after a scoped fix.

## Scope guard

- Stay inside `coptic-lectionary-research` when the requester explicitly says he will move deliverables to `coptic-corpus` himself.
- Do not apply B/C adjudications during a Category A duplicate-collapse pass.
- Treat Coptic Reader Wednesday Day fixture rows as current authority for scoped Wednesday Day comparisons.
- Do not hand-patch JSONL outputs. Patch the builder/source path, regenerate outputs, then verify generated artifacts.

## Independent audit gate

For A/B/C classification, enforce the independence rule:

1. Producer model drafts the Phase 0 classification.
2. Auditor model that did not produce it reviews the classification before edits.
3. If the audit is PASS WITH FIXES, update the classification artifact and rerun a focused audit.
4. Do not begin Phase 1 edits until the audit says no blocker remains.
5. Preserve audit artifacts with verdict, required fixes, and what changed.

Useful audit outcomes to capture:
- PASS WITH FIXES: record findings and required changes.
- PASS: record that Phase 1 may proceed, with explicit scope limits.
- Phase 1 audit: confirm B/C rows unchanged, only A changed, source disclosure retained, verifier passes.

## Category handling

- A = exact duplicate/current duplicate attestations eligible for collapse if provenance is retained.
- B = old-edition-only, historical, removed, or unresolved absent-from-Coptic-Reader candidates. Route to the maintainer and Fr. Boulos, do not delete.
- C = Psalm numbering seams, verse-range artifacts, named-reading mappings, or unresolved current-source conflicts. Route as proposed-not-applied, do not renumber or merge.
- Named current fixture rows such as `Memoirs of Job` must not be classified as B merely because they lack verse boundaries. Route as C/unresolved named-reading mapping if needed.
- Wisdom rows absent from Coptic Reader but not explicitly named by Section 3 should be described as unresolved B candidates, not confirmed removed readings.

## Attestation retention check

For at least one collapsed A row, paste before/after evidence:

- Before: two rows with the same `identity_key`, one from bare `Wednesday` and one from `Wednesday of Holy Pascha` or Coptic Reader fixture.
- After: one row with `occasion = Wednesday of Holy Pascha` and `source_disclosure_count >= 2`.
- The `source_disclosure` should include both source families/locators, not just one row's source.

Example source families to expect:
- `holy_pascha_curated_day_hour` / `pascha_day_hour`
- `coptic_reader` / `coptic_reader_fixture`

## Identity-key check

When the requester asks whether byte-identical A pairs shared identity keys:

- Query the before state and show one concrete pair.
- For exact duplicate A rows, expect same `identity_key`; if any exact duplicate pair differs by identity key, report it explicitly as a defect candidate.
- Do not infer this from row labels alone. Inspect the before JSONL or generated rows.

## Count reconciliation pattern

When accounting against a ticket, produce a table that sums to the stated before/after counts.

For the 2026 Pascha Wednesday cleanup, the reconciled slice was:

| Category | Before rows | After rows | Before identities | After identities | Notes |
|---|---:|---:|---:|---:|---|
| A exact duplicates / attestation collapse | 35 | 17 | 18 | 17 | 17 duplicate pairs collapsed; one First Hour Psalm composite moved into split Psalm attestations rather than remaining as a separate card. |
| B removed/historical candidates | 12 | 12 | 9 | 9 | Unchanged in the Pascha Wednesday slice. |
| C numbering/range/named-reading artifacts | 18 | 18 | 16 | 16 | Unchanged in the Pascha Wednesday slice. |
| Single-layer untouched rows | 0 | 0 | 0 | 0 | No rows in that 65-row collision slice were outside A/B/C. |
| Total | 65 | 47 |  |  | Sums reconcile. |

Also run a whole reverse-index B/C unchanged check, because slice counts alone do not prove no hidden B/C changes elsewhere:

- B before rows = after rows, added keys = 0, removed keys = 0, changed common rows = 0.
- C before rows = after rows, added keys = 0, removed keys = 0, changed common rows = 0.

## B/C open-questions section

When appending or reporting the Pascha Wednesday B/C section, include:

- Path: `audit_artifacts/open_questions_for_george.md`.
- A B section with each candidate's hour/slot, Section 3 match, evidence, and proposed status.
- A C section with each numbering/range/named-reading artifact and proposed-not-applied resolution.
- Explicit statement that nothing in B or C was edited in the data.

## Report-only ticket accounting

If the requester asks `Report only, NO further data edits`:

- Do not regenerate, patch, format, stage, or commit.
- Use read-only inspection of committed artifacts and git refs.
- Paste concrete evidence: affected rows, audit snippets, open-question section, count table.
- If a requested field name does not exist, say so plainly and name the actual field used. In the reverse index, `canonical_occasion` may not exist; the public label field is `occasion`.
- Distinguish source-disclosure provenance from raw duplicate `occasion` strings. After collapse, provenance is retained as source families/locators, not duplicate row labels.

## Verification notes

For focused behavioral proof after code/data changes, a temporary ad-hoc verifier can be created under the OS temp directory with a `hermes-verify-` prefix, then removed. Report it as ad-hoc verification, not as full suite green.

For package integrity verification, call `scripts/verify_package_integrity.py --package-dir` with an absolute path or explicit `./` relative path so the CommonJS probe does not try `require('packages/lectionary-data')` as a module name.
