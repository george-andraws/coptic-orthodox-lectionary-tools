# Synaxarium 1.3.0: Runtime Contract and Release Workflow

Updated September 8, 2026. This is the current public-catalog contract for `@andraws/lectionary-data`. Older research specs and bridge audits describe different internal artifacts, not this runtime schema.

## Release status

**`@andraws/lectionary-data@1.3.0` is published on npm.** It extends the existing CommonJS package; it is not a separate Synaxarium package. Reading data and the existing lookup/status APIs were preserved.

The published 1.3.0 artifact is immutable. Source-checkout documentation can be corrected afterward without changing that artifact. Publishing a revised package README or any other packed file requires a new version and explicit release authorization; this documentation update does not publish another version.

## Source and coverage

Use the audited, purified single-year 1743 files:

```text
synaxarium_from_coptic_reader.jsonl
coptic_reader_index.json
```

George's capture directory is `/Users/ga/workspace/synaxarium-coptic-reader-authority`. Do not use the `pre-purification/` copies. Private raw captures and review evidence stay outside the published runtime package.

Source note, preserved exactly:

> Coptic Reader, Diocese of the Southern US, current-practice, single-year 1743 capture

The catalog has **366 fixed Coptic day keys and 868 unique commemoration titles**. It is not a collection of full historical narratives and does not establish prescribed Synaxarium reading at a particular service.

## Public shape

File: `packages/lectionary-data/data/synaxarium/synaxarium.json`.

Each `month-day` key maps to:

```json
{
  "commemorations": [],
  "validInCommonYear": true,
  "validInLeapYear": true
}
```

Only Nasie 6 has `validInCommonYear: false`; all catalog days have `validInLeapYear: true`.

Each commemoration has exactly these fields:

| Field | Contract |
| --- | --- |
| `id` | Audited opaque ID, preserved without regeneration. |
| `title` | Canonical Coptic Reader spelling, verbatim. |
| `type` | `departure`, `martyrdom`, `feast`, or `commemoration`, preserving audited lexical classification. |
| `rank` | Capture ordinal used for display priority, lower first. Not liturgical precedence. |
| `displayOrder` | Capture ordinal, preserving order. |
| `displayGroupId` | Null. No grouping decisions, merges or splits were authorized. |

Frozen public slugs:

```text
tout, baba, hatour, kiahk, toba, amshir, baramhat,
baramouda, bashans, paona, abib, mesra, nasie
```

The source projection explicitly maps `hator` to `hatour` and `epep` to `abib`. It does not change IDs or titles. These public slugs are distinct from legacy reading display labels such as Babah.

Exact allowlists apply at day and record levels. Do not ship sources, sourceFamilies, attestation, reviewStatus, revisions, grouping_review_required, raw capture text, research bridge fields or any reason field in this catalog.

## API and calendar

The existing `index.js` CommonJS entry point exports:

- `synaxariumForCopticDay(monthSlug, day)`: immutable day object with the ordered titles and year-validity flags. Invalid slugs or days throw RangeError.
- `synaxariumMeta`: `day_count`, `total_commemorations`, and the exact source note.
- `synaxariumPath`: absolute public catalog path.
- `gregorianToCoptic(year, month, day)`: pure conversion, returning `{ year, monthSlug, day }`.
- `frozenMonthSlugs`: immutable ordered list.

Existing reading APIs, including `classifyDate`, `dailyYearPath`, `shippedYears`, `meta` and reading filters, remain available.

`calendar.js` is the only shipped Gregorian-to-Coptic converter. It uses integer Julian-day arithmetic, validates civil dates, and supports Gregorian years 0001 through 9999 independently of the bounded 2026-2028 reading files. It does not inspect the current clock, local timezone, occasion labels or captured-year lookup tables. Pre-epoch Coptic years use astronomical numbering.

A browser consumer should bundle this same module, not import the Node path-based package entry point or create a second converter.

Example from repository root:

```bash
node -e 'const p=require("./packages/lectionary-data"); const d=p.gregorianToCoptic(2026,9,8); console.log(d); console.log(p.synaxariumForCopticDay(d.monthSlug,d.day).commemorations.map(c=>c.title));'
```

The returned date is Nasie 3, 1742.

## Reproducible projection and source fingerprints

```bash
python3 scripts/build_synaxarium.py /path/to/audited-source-directory
```

The builder reads both audited files, checks their counts and heading order, writes the public catalog, and writes `tests/fixtures/synaxarium-1743.json`. The fixture records source file hashes and per-day public-projection fingerprints, counts and civil dates. It is not included in npm files.

Do not regenerate both the catalog and its expected fixture from unreviewed source changes merely to make validation pass. A change to source capture, IDs, titles or grouping requires a renewed source review.

## Acceptance commands

From repository root:

```bash
uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate python -m unittest discover -s tests
node --test tests/synaxarium.test.cjs
python3 scripts/validate_synaxarium.py
python3 scripts/verify_package_integrity.py --strict-file-set
git diff --check
```

An existing Python environment with those dependencies can run the unittest command directly. The uv command avoids changing system Python.

Maintainer npm aliases, run from `packages/lectionary-data` in a source checkout:

```bash
npm test
npm run synaxarium:validate
npm run lectionary:validate
```

These aliases depend on repository scripts/tests outside the packed module. They are not consumer runtime commands for an isolated npm installation.

The Synaxarium validator is integrated into package integrity. It rejects missing/substituted day keys, invalid slugs, duplicate/malformed IDs, per-day source-count changes even when the total remains 868, changed public projections, invalid types/order/grouping, wrong year flags, malformed records and private/unknown fields.

## Recorded 1.3.0 validation

- 58 Python tests and 3 package Node tests passed.
- All 11 seeded corruption cases failed after repair. Six had incorrectly passed the prior incomplete validator.
- All 366 captured civil dates matched the final converter.
- 5,716 independent comparisons to Python convertdate across years 1 through 9999 matched, with zero differences.
- UTC, Los Angeles and Kiritimati checks, new-year/Nasie-6 boundaries, Gregorian centuries, early years and invalid dates passed.
- Direct source comparison preserved all 868 IDs, titles, types and source ordinals.
- Strict packed-file inspection passed with 11 expected files, including calendar.js and the public Synaxarium JSON; no fixture or raw capture files shipped.
- Registry integrity and installed package bytes matched the inspected release artifact.

These are recorded release results, not an independent-model audit claim. George waived model separation for the final implementation; Astra performed the repair and verification.

## Future release sequence

1. Preserve existing reading behavior unless the intended change explicitly alters it. Keep reading provenance and Synaxarium capture provenance separate.
2. Run the acceptance path and inspect the public field allowlists.
3. Pack outside the runtime package directory so strict-file-set checks do not see a tarball as an extra runtime file.
4. Inspect the actual tarball with `scripts/verify_package_integrity.py --tarball PATH_TO_TGZ`, not just package.json files[].
5. Choose the appropriate semantic version. Version 1.3.0 used `npm version minor --no-git-tag-version` because it added backward-compatible data and APIs. Update meta.version to match and revalidate afterward.
6. Commit the reviewed local source. Publish only when explicitly authorized. Stop on publication/authentication failure rather than working around it.
7. If npm accepts the upload but reports processing, do not republish. Confirm `npm view @andraws/lectionary-data version` and the intended version's dist.integrity after processing completes.
8. Install the exact published version in the consuming site and confirm the lockfile's registry URL/integrity. Do not substitute a local link.
9. Verify the site's tests/build/type check and rendered behavior. Git push, deployment and real-phone verification remain separate gates controlled by George unless explicitly authorized otherwise.

For reading-source rebuilds, also follow the broader [validation plan](LECTIONARY_VALIDATION_PLAN.md). Do not run the full historical research pipeline merely to update this fixed-day titles catalog.

## Current consuming site

Repository: `george-andraws/coptic-corpus`. Canonical checkout: `/Users/ga/code/coptic-corpus/stgeorge-lessons`.

The site uses one compact civil/Coptic date heading, a Synaxarium list after the first Praxis (or after available readings if Praxis is absent), and a Today in the Church card beside Continue reading. All titles are expanded. Peer cards are equal-width on desktop and stacked on mobile, with matching typography and no divider. A Reverse Lectionary link points to `/lectionary` above the reading results.

The site does not display a separate commemorations panel or the old explanatory disclaimer. The underlying data relationship remains date-only, with no reason or saint-to-reading link. Its exact current UX and runtime ownership are documented in that repository's `docs/lectionary-and-synaxarium.md`; those UI details are not additional package-schema fields.

The Coptic Reader public catalog is separate from the older St-Takla research index and experimental reading bridge. Those internal artifacts and their audits remain historical/research material, not a production Synaxarium input.
