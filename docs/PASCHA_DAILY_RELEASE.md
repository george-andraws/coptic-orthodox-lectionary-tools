# Pascha daily materialization correction

## Corrected request and acceptance criteria

Restore missing Wednesday daytime readings in the daily materialization of
`@andraws/lectionary-data`, then verify the published package and the real
`stgeorge-lessons` consumer. The malformed `@file` tokens in the original issue
refer to the npm package `@andraws/lectionary-data`, not local filenames.

- Trace current source rows through reverse projection, daily serialization,
  packaged bytes and site date shards before assigning the fix.
- Admit the retained Wednesday Day Reader fixture under its exact occasion and
  source kind. Do not allow arbitrary Reader-labeled ordinary services.
- Preserve current-status filtering, historical witnesses, inactive rows,
  source disclosures, existing Psalm coordinates and unresolved equivalence
  qualifications. This release is not a new Psalm-coordinate adjudication.
- Verify all five daytime hours have prophecy, Psalm and Gospel coverage on
  `2026-04-08`, `2027-04-28`, and `2028-04-12`; retain Wednesday Eve separately.
- Audit other structural days for the same occasion/source-family exclusion,
  including collapsed records whose representative family changed.
- Add executable regressions before changes, with observed RED-GREEN evidence.
  Test wrong-day/wrong-source and removed/historical negatives as well as
  complete reading preservation and deterministic unique date-local order.
- Compare every non-target daily date and protected runtime file against the
  previous package. Preserve reverse-index data unless a separately established
  same-root-cause correction requires changing it.
- Bump the builder-owned package version and retain the 1.3 calendar/catalog
  runtime. Verify source provenance against a committed clean source tree.
- Validate the actual npm tarball, perform an isolated install, publish only
  with explicit release authorization, and read back registry version and bytes.
- Install the exact registry release in the canonical consumer. Update the
  liturgical catalog's package version binding without weakening its mismatch
  test. Run `npm run lectionary`, `npm run lectionary:validate`, `npm test`,
  `npm run build`, and `npx tsc --noEmit`; exercise the real date UI.
- Preserve existing site work. Include reviewed Bible-study changes and their
  required generated metadata only when coherent and tested. Do not assume all
  unrelated dirty files are authorized merely because Bible studies are.
- Review staged changes and whitespace before commit/push; verify remote heads
  and the site deployment separately. Classify pre-existing failures honestly.

## Verified scope and retained limitation

Wednesday daily materialization restores all 21 Reader rows already current in
1.3.1. An identical Ninth Hour Proverbs appointment under the two Wednesday Day
labels is emitted once using the Reader representative; both original reverse
attestations remain unchanged. The resulting daily table has 41 rows, including
Wednesday Eve. Hosanna Sunday gains four existing current Ninth/Eleventh Hour
Psalm/Gospel appointments while preserving all 16 ordinary Palm Sunday rows.
Only these six civil dates change across the three shipped years.

The retained Wednesday fixture has 26 rows. Five Psalm rows were already inactive
in the npm reverse projection because `SOURCE_PRIORITY` names a source kind
(`coptic_reader_fixture`) rather than the actual scalar family (`coptic_reader`);
some competing rows are historical or have unresolved Psalm equivalence. That
priority defect predates this release and is bound into the 1.1.6 removal-version
baseline. This daily repair does not reactivate those five rows, alter Psalm
coordinates, or silently adjudicate their competing witnesses. All five hours
still retain the existing current Psalm coverage with its qualifications.

The cached-source comparator qualifies restored structural rows against a
hash-pinned 1.3.1 reverse-row baseline and independent Pascha date offsets. It
checks exact references, slots, source locators, disclosures, identities and
spans, rather than exempting any row carrying a structural marker.

## Focused regression command

```sh
node --test tests/npm_pascha_daily.test.cjs tests/npm_builder_preservation.test.cjs
```

The wider source, package and tarball gates are documented in
[LECTIONARY_VALIDATION_PLAN.md](LECTIONARY_VALIDATION_PLAN.md).
