# Lectionary 1.3.3: canonical appointments and retained evidence

## Root causes and bounded correction

The package's previous projection treated different month spellings, Sunday prefixes, and service-slot labels as different appointments. Its overlap grouping compared `prophecy` separately from the source-established Matins service. Numeric cycle fragments remained searchable beside complete source-qualified readings. SQLite preparation sentinel keys were exported as though they were recurring numbered weeks.

The durable correction is in `scripts/build_npm_package.mjs` and the retained, source-qualified `sources/canonical-occurrence-policy.json`, not a generated-only site filter. All raw references, existing spans, source disclosures, and inactive witnesses remain available. Current lookup uses one preferred appointment, with alternate evidence retained separately where an authenticated Sunday disclosure cannot be altered.

### Scope

- Normalize current reading labels for Tout/Tut, Hator/Hatur (including Hatoor), Kiahk/Kiyahk (including Kiak), Toba/Tubah, Amshir/Meshir, Bashans/Bashons, Paona/Baunah, Baba/Babah, Baramoudah/Barmuda, and Al-Nasi/Nesi. Calendar and Synaxarium public slugs are unchanged.
- Normalize source-established Sunday prefixes and the four Christmas Fast/Kiyahk lesson labels. This does not assign uncaptured civil dates or modify feast precedence.
- Preserve separate Pascha Day/Eve and hour contexts. Wednesday Day uses `Wednesday of Holy Pascha`; retain its source-confirmed Ninth Hour Psalm 41:5-7 and Eleventh Hour Psalm 69:16 instead of the stale working witnesses Psalm 41:5-6 and Psalm 69:17.
- Collapse exact canonical appointment aliases, including Ninth Hour Proverbs 1:11-35, Third Sunday of Meshir Hebrews 3:1-4:2, Baunah 30 Luke 1:57-80, and Mesra 7 same-service duplicates.
- Reconcile 512 source-proven complete-slot split representations, including Numbers 10:35-11:35 and the duplicated Great Lent Proverbs contexts.
- Resolve 80 explicitly source-qualified precedence conflicts under the repository's existing authority policy. These are **not all coverage-equivalent duplicates**. For example, Tut 4's active Gospel appointment prefers the retained date-resolved Matthew 23:13-26 rather than the conflicting cycle Matthew 23:13-36. Conflicting raw evidence remains inactive; no source text is rewritten.
- Week 99 is authentic Preparation Saturday/Sunday, established by the retained SQLite and feast factories. Preserve all 20 readings under named occasions. Week 49 duplicates Week 4 Wednesday and is unreachable through the retained factory implementation; retain its source evidence but exclude the false recurring context.

## Independent data preservation

The independent semantic inventory measures 3,354 duplicate appointment groups and 3,407 redundant context members before correction, zero afterward. Reverse rows are retained rather than deleted: 12,185 becomes 12,205 with the 20 explicit named preparation projections. Current rows change from 11,499 to 7,610. All 686 prior inactive rows and 18 qualified Sunday Psalm holds are retained exactly.

Only three daily dates change: 2026-04-08, 2027-04-28, and 2028-04-12, each from 41 to 39 rows. The two stale Wednesday Day Psalm witnesses are excluded; all 21 current Reader rows and Wednesday Eve remain. Every other packaged daily date is unchanged. `index.js`, `calendar.js`, the README, license, and public Synaxarium bytes are preserved.

## Authentication and regression design

Source fingerprints alone cannot authenticate projected row metadata. The canonicalizer binds the **complete ordered input**, including locator, disclosure, spans, status, context, and order, to the reviewed 1.3.2 source projection. Every initial selector must identify exactly one current row. The emitted array must match the independently reviewed complete output fingerprint before publication. Exact reviewed output is allowed only as an idempotent replay. Any source/policy evolution requires renewed review; do not automatically refresh fingerprints to make a failed build pass.

`tests/fixtures/canonical-occurrences-input-1.3.2.jsonl.gz` preserves the authenticated pre-canonical projection outside npm files. Tests exercise the first transformation separately from replay. The no-op canonicalizer mutation fails seven of eight tests. Forged preferred locator/disclosure/spans/order, moved context, wrong kind, inactive state, missing preferred rows, and extra ordinal variants are rejected before suppression.

## Verification status

This document records the candidate scope. Publication and live-site acceptance must be recorded separately after exact-tarball and registry verification.

- Initial Python baseline: 328 tests passed.
- Full candidate Python discovery before the final fingerprint guard: 332 tests passed.
- Focused guarded canonicalization plus builder-preservation tests: 9 passed.
- Full guarded Node suite: 44 passed, 2 pre-existing failures reproduced against exact published 1.3.2. Neither assertion was weakened or skipped:
  - `remaining authoritative Psalm readings retain text-aligned MT coordinates and source order`: February 18 fragment order.
  - `remaining Coptic Reader corrections preserve exact context and Psalm companions`: absent retained Nineveh no-Vespers marker.
- Candidate package integrity, source manifest, complete-calendar, design/query validation, and cached source comparison passed before final clean-provenance rebuild.
- Candidate consumer: production build, TypeScript, 1,722 unit tests, and 48 Chromium desktop/mobile browser cases passed. Repeat affected gates with the final registry artifact and latest site head.

No unrelated Psalm coordinate remediation or Nineveh restoration is included. These existing findings remain separate from the canonical-occasion repair.
