# Phase 3 Grok Attestation Audit Pass 1

## Findings

- Phase 3 is structurally on track. The artifact reports 445 attestation rows, with every row assigned to a controlled bucket.
- Bucket separation is mostly correct:
  - `current_confirmed`: 26
  - `single_source_candidate`: 260
  - `old_edition_only`: 152
  - `old_edition_only_candidate_removed`: 7
- Coptic Reader scope is handled correctly. The 26 current-confirmed rows are confined to the captured Wednesday Day fixture. The packet does not use Coptic Reader as a global current authority.
- The Wednesday fixture is reconciled in the main cases. Coptic Reader plus Katameros matches are marked current confirmed by fixture equivalence. Coptic Reader-only fixture placements are marked current confirmed. Removed Katameros prophecy candidates are marked historical candidate removed.
- Prophecy conflicts are bucketed correctly. The Wednesday Wisdom, Isaiah, Zechariah, Job, and older Proverbs candidates are not promoted as current against the fixture.
- St. Mary Ottawa is treated as historical evidence, not current authority. That matches the ingestion memo and Phase 2 correction posture.
- The packet correctly avoids requiring full Coptic Reader ingestion. It treats the fixture as scoped evidence only.
- The main gap is audit readability. The artifact does not show a zero-count `consensus_without_coptic_reader` bucket, and the five unresolved Wednesday Psalm rows need row-level reasons or conversions.

## Required Revisions

1. Add an explicit controlled-bucket manifest or zero-count row for `consensus_without_coptic_reader`.
   - The design brief requires this bucket type to be distinguished.
   - If Phase 3 has no such rows, show `consensus_without_coptic_reader: 0` or include it in the allowed-bucket list used by verification.
   - Without that, the packet proves current, old-edition, removed, and single-source buckets, but not the consensus-without-Coptic-Reader branch.

2. Add row-level notes for the five `current_psalm_equivalence_unresolved` Wednesday Psalm candidates.
   - Eleventh Hour: `Ps 6:2-3`
   - Eleventh Hour: `Ps 69:17`
   - Ninth Hour: `Ps 41:5-6`
   - Sixth Hour: `Ps 83:2,83:5`
   - Third Hour: `Ps 41:6,41:1`
   - For each row, either promote it to fixture equivalence where the LXX or MT numbering match is encoded, or keep it unresolved with a concrete note explaining the remaining verse-number or text-boundary problem.

3. Strengthen weak citations for removed candidates that currently cite only `api`.
   - `api` is not enough for later audit replay.
   - Use a reproducible citation such as Katameros API extraction identifier, SQLite row identifier, source path, or comparison note against the Wednesday Coptic Reader fixture.

4. Keep the existing caveat that Coptic Reader confirms only Wednesday Day fixture scope.
   - Do not expand Phase 3 into full Coptic Reader ingestion.
   - Do not treat non-Wednesday candidates as current unless another current source confirms them.

## Outcome

Conditional pass.

The artifact meets the core Phase 3 attestation design: every reported Pascha placement has an attestation bucket, Coptic Reader authority is limited to the captured fixture, Wednesday prophecy conflicts are resolved into current, historical, or removed buckets, and full Coptic Reader ingestion is not required.

Acceptance is conditional on the three auditability fixes above: expose the zero-count consensus bucket or manifest, document the five unresolved Psalm cases row by row, and replace bare `api` citations with reproducible source references. After those changes, Phase 3 should be accepted.
