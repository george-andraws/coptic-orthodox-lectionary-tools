# Lectionary data 1.3.10 release

Package: [`@andraws/lectionary-data@1.3.10`](https://www.npmjs.com/package/@andraws/lectionary-data/v/1.3.10). Predecessor: authenticated published 1.3.9.

The release is published. Registry bytes matched the exact tested archive, not just its version label. The [portable receipt](releases/lectionary-data-1.3.10.json) records archive size, SHA-1, SHA-256, npm integrity, all 11 packed members and 42 reviewed source/test inputs. Initial repository reconciliation on November 13, 2026 confirmed those publication input and member hashes without rebuilding or modifying the published data. The later repository-only validator correction below intentionally changes two source files; its inputs are bound separately rather than refreshing the original publication pins.

## Changes and source boundaries

- **PK2:** The retained Bright Saturday Reader witness has Deuteronomy 32:1–43, including numbered verse 43. Preserve the previous 32:1–42 witness as inactive history and introduce the source-backed successor. Replace the old witness in its three shipped daily occurrences without reordering companions.
- **PK4/PK5/PK10:** Apply six reviewed Psalm annotations from the retained MT/NKJV and Brenton witnesses. Keep source coordinates and annotation history. A superscription offset is not a universal numbering rule.
- **PK6:** The old Good Friday Ninth Hour Hosea identity was a local transcription error: the upstream constructor/book ID identifies Joel. Preserve the erroneous identity as inactive audit history. Ottawa's 2018 *Katameros of the Holy Pascha*, printed pp. 610–611, names Joel 2:1–3, 2:10–11. Preserve this as an edition-qualified historical witness, not a current Reader appointment. The retained Reader capture and Fr. Jacob Nadian service book omit a third prophecy. Neither establishes when or why it was removed. Preserve that uncertainty and do not introduce a third current prophecy or a Joel daily occurrence.
- **PK11:** Remove internal review prose from current display references, retain the exact previous labels in structured disclosure and leave empty canonical arrays and held numeric source coordinates qualified. No speculative verse alignment is added.
- Extend the version-aware release projections and inverse checks. Historical source fixtures remain pinned; adapters authenticate the final public stage before applying earlier-stage oracles. Serialized report counts and source attestations remain checked rather than bypassed.

Evidence and predecessor fixtures live in [`sources/revelation-review-1.3.10/`](../sources/revelation-review-1.3.10/). Source-owned stages are `revelation_release_repairs.py` and `pk6_release_repairs.py`. Psalm annotations are applied through `evidence_followup_repairs.py` before the final release stages. `scripts/review_release_contract.py` owns stage projections and exact inverse validation. The npm builder and actual package validators consume those stages.

## Preserved behavior

- Calendar and Synaxarium bytes, the CommonJS API and the named coverage gaps are unchanged from published 1.3.9.
- Current reverse inventory: 7,658 readings. Shipped daily inventory: 12,232 rows. Retired witnesses remain available as inactive history, not current appointments.
- Qualified empty canonical fields and numeric coordinate holds are intentional. Consumer transport is not permission to fabricate canonical spans.
- The separately authorized site consumer passed the real parser/validator checks for all current reverse witnesses, preserved the complete ordered daily arrays and transported exactly two explicitly historical-only PK6 source disclosures. Those disclosures are excluded from current search, daily readings and footprints. Direct archive access is `sources/<identity>.json`; it is not a new service appointment or a package API addition.
- Fresh Quartz lazy-search compatibility is a website loader concern. Its repair changes no lectionary package source or data and requires no additional package release.

## Verification record

Before publication:

- Independent exact-candidate review authenticated 38 frozen source inputs and the 11-member archive. Final README correction changed only `package/README.md`; the other 10 archive members were byte-identical to the reviewed candidate.
- Full declared Node inventory passed: **114 tests**, across 23 files, using `node --test --test-concurrency=1`.
- The initial full Python run recorded **1,302 passed, 16 skipped, 6,168 subtests passed and 13 failures**. Those failures were in two stage-dependent adapter modules. After correcting the adapters, the affected modules passed **79 tests and 56 subtests**. The complete Python suite was not rerun after those adapter-only fixes; do not describe this as a newly executed all-green full run.
- Optional historical-calendar controls passed **16 tests and 21 subtests** against authenticated 1.3.6 with `LECTIONARY_CALENDAR_BASELINE` set explicitly.
- Exact-archive strict membership/integrity and external-source comparison commands exited zero. Package README and metadata version agreement passed. Registry tarball bytes matched the tested archive.

The portable source inventory includes the original 38 frozen inputs, the final package README, its version assertion and the two corrected test adapters. Hash reconciliation permits reuse of the unchanged release evidence; it is not a claim that every earlier test was freshly rerun during repository documentation reconciliation.

## Repository-only historical-validator follow-up

Pre-push independent review found that the new six-locus Psalm policy also changed the inverse expectations for explicitly supported 1.3.8/1.3.9 packages. Authentic predecessor data was wrongly refused. Version-scoped reconstruction restores the original historical expectations while preserving the default/current 1.3.10 behavior, all exact inverse checks and corruption refusals.

The correction touches only `evidence_followup_repairs.py` and `scripts/review_release_contract.py`. New offline regression tests authenticate independently extracted slices from both actual historical archives, exercise reverse and daily callers, and retain current-version and wrong-annotation/disclosure controls. No existing fixture or assertion was rewritten. Full historical reverse/all-years daily comparisons recovered the original base implementation's outputs for each version; 1.3.10 runtime members remain byte-identical.

The receipt's `repository_followup` records the two corrected source files, the new regression test and its bounded authenticated fixture. Its original 42 publication-input hashes and all 11 archive-member hashes remain unchanged. This is a repository verifier compatibility repair, not a new npm release or a change to published reading appointments.

## Publication provenance

Published SHA-256:

```text
fdbb681c0c6cc15c255d7af8f36371c9aa1229d9b14b57c023d82f4c4780064e
```

The published metadata truthfully records source commit `5e49467412919e16bf5c7e751da562380d5a1ca7` and `source_tree_dirty: true`. The release changes were intentionally uncommitted during package acceptance/publication. That commit alone does not reproduce the release. The portable input/member inventory binds the actual accepted bytes.

A later authorized repository commit preserves these source changes but does not retroactively change the npm archive's source commit or dirty flag. Do not rebuild or republish immutable 1.3.10 to make its provenance appear clean. Any future package release needs its own version, source provenance, exact-artifact gates and publication authorization.
