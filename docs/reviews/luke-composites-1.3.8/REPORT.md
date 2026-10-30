# Luke composites and public provenance follow-up

## Scope

LK5 and LK6 were reproduced against authenticated published `@andraws/lectionary-data@1.3.7`. This is a component report. The parent release report owns combined-source verification, final clean-clone provenance and publication status.

## LK5: remaining complementary source cells

All 52 reported pairs reproduce: Matthew 4:23-25 with 5:1-16 in 21 groups, Mark 8:34-38 with 9:1 in 17 groups, and Luke 11:53-54 with 12:1-12 in 14 groups. Each pair has the same source-qualified calendar/service/slot appointment. All 104 predecessor witnesses are inactive, so these merges do not remove any daily appointment or activate any historical reading.

`composite_followup_repairs.py` merges only the authenticated pair inventory. One row contains ordered `spans_json` and exactly two ordered `composite_fragments_json` records. Each fragment preserves the complete original source row, raw fields, disclosure, retirement marker and endpoint. A fragment's public witness key is `original_source_row`. Complete historical witness membership remains recoverable; retaining an original witness is not the same as exposing both fragments as separate appointments.

The exact pair inventory, original bodies and hashes are in [published-1.3.7-composite-witnesses.json](published-1.3.7-composite-witnesses.json). The baseline reverse index decreases from 12,330 to 12,278 before Mark's four added held candidates. Final combined counts must come from the real integrated build, not this arithmetic expectation.

## LK6: public provenance transport

The claimed 181 JSON-object provenance values reproduce. The claimed 226 R4 provenance rows do not. The pinned inventory records 17 R4 rows, 198 rows containing JSON and 207 rows requiring public transport. The maximum baseline provenance length is 52,951 characters. The component projection's maximum is 296 characters, within the 300-character limit.

Human-facing `provenance` is short plain text. Non-R4 structured content survives in `provenance_evidence_json` with `provenance_format: lectionary_provenance_v1`. R4 original rows reside only in their dedicated fragment cell rather than being copied into the short summary or another evidence cell. Exact legacy JSON is recoverable for source-owned validators. No `_review_original_row` token remains in public daily serialization.

The decoder checks the public transport format, exact summary, field shape and canonical evidence representation. Successful decoding is not source authentication. After decoding, the original source, lifecycle, coordinates and whole-table membership guards must still run. Corrupted evidence must not gain authority from a marker, a short summary or a successful JSON parse.

See [public schema](README-schema-fragment.md) and [integration contract](INTEGRATION.md). Those source-repository Python adapters are not shipped as JavaScript exports in the npm package.

## Component verification

- Focused final suite: 30 tests passed.
- Surrounding regression run: 108 tests and 309 subtests passed.
- All 55 baseline Sunday rows and four source-only Bright composites were exercised through real exported consumers.
- Counterexamples covered forged bodies, missing evidence/disclosures, wrong context, lifecycle changes and stripped markers.
- A no-op LK5 mutation was killed by the focused tests.
- Compile and diff checks passed.

The original reproduction inventory is [baseline-report.json](baseline-report.json). Component success does not replace the combined full suite, cached-source comparison, strict serialized integrity checks, clean-source artifact verification or consumer build.
