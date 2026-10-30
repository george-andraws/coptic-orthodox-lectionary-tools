# LK5 and LK6 frozen source handoff

## Files owned and frozen

- New `composite_followup_repairs.py`.
- Modified `source_reading_contracts.py`: four added lines, importing and calling the public transport decoder at `row_envelope` and `validate_consumer_rows`. No oracle, activation, schema, disclosure or source-authentication assertion was removed.
- New `tests/test_luke_composite_followup.py`, `tests/test_luke_provenance_transport.py`, `tests/test_luke_evidence_consumers.py`.
- New files in this directory: this handoff, `baseline-report.json`, `published-1.3.7-composite-witnesses.json`, and `README-schema-fragment.md`.
- No shared builder/script, root document, generated package, membership ledger, historical fixture or historical policy was edited by this worker. `resolver_review_repairs.py` is unchanged.

## LK5 evidence and exact scope

The independently frozen published 1.3.7 reverse file has SHA-256 `4b785a5c626eaf4809f74738bfb3be05d7c8d0ae095b51bf98e72cad55559bf9` and 12,330 rows. The pinned fixture in this directory contains 104 complete predecessor witnesses, not candidate-derived membership. Its hash is checked by production code. Every merged pair is also authenticated against the existing pinned raw-fragment contract and hash-bound SQLite database cell, date, service, slot and complementary source order.

Exactly 52 pairs remain: Matthew 21, Mark 17, Luke 14. All are already inactive: 28 have `superseded_by_canonical_occurrence_projection`, 24 have `removed_by_source_priority_projection`. The new projection yields 52 inactive composite appointment rows with 104 complete original fragment records. It does not activate history. Source titles, locators, raw keys, original identity and every retirement field survive in the fragment records. The composite's locator is the literal first fragment locator; both original disclosures and locators are retained explicitly.

Standalone LK5 projection is 12,330 -> 12,278 reverse rows. Applying only this delta to the parent's stated Mark projection is a subtraction of 52, not approval of its final count. Daily reading counts are unchanged by LK5/LK6.

## APIs and integration order

```python
from composite_followup_repairs import (
    merge_remaining_composites,
    qualify_archived_composite,
    compact_public_row, compact_public_rows,
    restore_public_row, restore_public_rows,
    legacy_validation_rows,
)
```

1. Keep the existing raw whole-corpus ledger and all historical fixture-policy pairs unchanged. Run the ordinary raw authentication/membership gates as before.
2. Finish ordinary canonicalization, resolver repairs and occurrence annotations. `merge_remaining_composites(rows)` then returns `(rows, events)`. It accepts exact published predecessors plus the independently constrained LK2 fixed-date display-label spelling, not arbitrary metadata drift. Put this after the occurrence annotation boundary because its pinned predecessors include that descriptive metadata. It can precede LK2 normalization or follow its exact fixed-date normalization. Do not put it ahead of occurrence annotation and then weaken its exact check.
3. Run remaining approved label/evidence repairs and exact source-specific qualification on the internal evidence-bearing rows.
4. At final public serialization call `compact_public_rows(rows)` on reverse and each daily array. It is lossless and idempotent. For R4, fragment bodies live only in `composite_fragments_json`, not duplicated in provenance evidence. This final boundary removes all occurrences of the private `_review_original_row` spelling, including inside nested serialized evidence, using the documented public spelling `original_source_row`.
5. At validator/comparator boundaries, decode FIRST. `restore_public_rows` restores only the original provenance and reserved internal key spelling, not arbitrary row scalars. It is a strict transport decoder, NOT authentication. It checks the exact two allowed envelope schemas, duplicate members, scalar types, public-label consistency and required companion fragment cell. Immediately pass the returned rows to the existing real source/disclosure/lifecycle guards. A copied envelope is never proof of authority.
6. For legacy reverse corpus, retirement and calendar checks that expect the original 104 inactive split witnesses, use `legacy_validation_rows(public_rows)`. It first decodes LK6, then authenticates each LK5 composite against its independently pinned complete predecessors and the SQLite source, and expands only these exact inactive composites to their original witness records. It does not create or change a membership oracle. The frozen baseline complete row multiset is recovered exactly, including every inactive source witness. It recognizes known merged locators even if the new marker is stripped and then fails exact qualification.
7. Mark's `qualify_emitted` and `restore_predecessor_for_comparison` require the decoded internal evidence view BEFORE their existing full-payload checks. Preserve the exact existing checks. Build expected LK5/LK6 transformations independently from pinned predecessors; do not repair candidate rows and treat idempotency as authentication.

## Parent-owned changes still required

This worker intentionally did not edit shared scripts or builders. The following wiring remains required before release acceptance:

- Add the merge in the final occurrence phase of `scripts/apply_review_repairs.py`, after all per-row occurrence annotations; preserve events/counts.
- Add compaction at the final reverse/daily serialization boundary, after other source-owned modules finish. Carry `provenance_format`, `provenance_evidence_json`, `composite_fragments_json` and `composite_review` through relevant explicit field allowlists and disposable fixture input copies.
- Feed `legacy_validation_rows` to existing reverse keyset/retirement/calendar-source guards when they need the historical witness domain. Feed `restore_public_rows` to daily, Mark and comparison/source validators, preserving the public row view for the separate LK6 plain-text check. Do not count expanded historical validator rows as public reverse rows.
- `scripts/review_release_contract.py::_originals` expects `_review_original_row` wrappers in existing R4 evidence. The LK6 decoder restores that historical form. New LK5 inactive composites instead need the explicit authenticated expansion above, not a weakened generic fallback or a fabricated wrapper.
- `scripts/verify_package_integrity.py`, `scripts/compare_external_sources.py`, `scripts/review_comparison_contract.py`, and direct `verify_design_deliverables.py` provenance readers need the decoded view before their exact evidence checks. Source-reading contract validation already decodes directly; its builder callers that later read provenance independently still need their own boundary decoding.
- Direct raw source qualifiers for Psalmody, Bright and Covenant continue to require the legacy authenticated raw shape. New compatibility tests explicitly decode before those real qualifiers and prove body/missing-evidence/lifecycle/context rejection. Do not claim they natively consume the new public schema.
- Add the final public LK6 assertions: provenance is a string, plain text, <=300 characters; no `_review_original_row` token anywhere in serialized daily output. Authenticate evidence separately, never use this cosmetic check as a security gate.
- Run the final integrated artifact verifier, comparator, clean builder and exported consumer gates only after all workers and parent shared-file changes freeze. None of the evidence below constitutes whole-release acceptance.

## Verification actually executed

- Initial RED: new module absent, two collection errors. System `python3` lacked pytest; switched to the established isolated `uv` Python 3.11 environment without altering checks.
- Behavioral RED: direct `source_reading_contracts.validate_consumer_rows` rejected compacted valid complete candidate output with `source contract malformed provenance transport`. Added the four-line decoder integration, retaining its exact original authentication lane.
- Focused surrounding command before the final new-label/R4-storage refinements: 108 tests and 309 subtests passed in 372.00 seconds. This covered the three new modules plus `test_edition_transport_modes.py`, `test_edition_fragment_consumers.py`, `test_resolver_review_repairs.py`, and `test_resolver_comparison_contract.py`. Historical resolver fixtures and their policies were not refreshed.
- Final focused command after those refinements: `uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate --with pytest python -m pytest -q tests/test_luke_composite_followup.py tests/test_luke_provenance_transport.py tests/test_luke_evidence_consumers.py`: 30 passed in 161.79 seconds, exit 0.
- Independent full-baseline in-memory projection: exact complete legacy reverse multiset recovered, all 52 merges authenticated, all daily arrays roundtrip exactly, no private token remains, all provenance is plain text <=300. Actual exported contract validated all 55 published Sunday rows with new transport. Actual exported package bounds checker validated all four decoded source-only Bright composite rows.
- Tested real output consumers: reverse builder, daily builder, passage disclosure builder, shared source contract, and source-contract verifier. Complete valid candidate controls pass; body forgery, missing evidence, missing disclosure and context mutations reject. Raw source-owned Psalmody, Bright and Covenant valid inventories and mutations also pass/reject correctly after explicit decoding.

## Baseline count reconciliation

The reported 52 groups and 181 JSON-object provenance rows reproduce exactly. The reported 226 R4/full-original-row provenance rows do not: published 1.3.7 has 17 R4 provenance rows, 198 provenance strings containing JSON in total, 162 over 300 characters, and maximum length 52,951. Union of rows requiring compaction is 207. Maximum public provenance after this projection is 296. Each daily year contains four private-token occurrences, not only 2026; all become zero. Daily transport changes 11, 11 and 5 rows in 2026, 2027 and 2028 respectively, without changing the 4,088 / 4,079 / 4,096 published baseline reading totals. See machine-readable `baseline-report.json`.

## Acceptance limitation

Source modules and bounded compatibility are implemented and tested. Shared runtime wiring, independently expected integrated transformations, final generated counts and final whole-corpus release acceptance remain the parent's work. No npm, site, commit or push action was taken.
