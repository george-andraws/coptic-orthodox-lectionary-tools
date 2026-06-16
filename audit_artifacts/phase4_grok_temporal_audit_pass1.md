# Phase 4 Grok Temporal Classification Audit Pass 1

## Findings

- Scope note: this pass uses the supplied packet and does not claim a fresh independent rerun.
- The row math is internally consistent:
  - 445 temporal classification rows.
  - 260 candidate current rows equals 255 current-authority pending rows plus 5 Psalm equivalence unresolved rows.
  - 159 historical or removed rows equals 152 old-edition-only rows plus 7 candidate removed rows.
  - 26 current rows equals 26 current-confirmed rows.
- The classification model mostly respects the design brief:
  - Current readings are only promoted where the scoped Coptic Reader fixture confirms them.
  - Single-source candidates are not promoted to current.
  - Historical printed witnesses without a current comparator remain in residue.
  - The seven Wednesday Day candidate removed readings are correctly isolated as candidates, not silently treated as ordinary historical witnesses.
- The residue artifact is present and useful:
  - 419 total residue rows.
  - 255 current authority pending rows.
  - 152 historical witness rows with no current comparator.
  - 5 Psalm equivalence unresolved rows.
  - 7 candidate removed rows needing current authority confirmation.
- The seven candidate removed readings are properly backed by source citations and reasons:
  - Wis 1:20-2:15
  - Wis 3:12-24
  - Isa 59:1-17
  - Zech 11:11-14
  - Job 28:1-2
  - Job 27:16-20
  - Prov 4:4-5:4
- The Psalm unresolved handling is appropriate in principle. The rows were not promoted because Brenton/KJV verse-boundary equivalence is not encoded, which matches the design requirement not to force Psalm equivalence by assumption.
- The strongest issue is terminology. Some labels can be read as final current-status judgments when the evidence only supports pending or candidate status.

## Required Revisions

- Add an explicit disagreements section or count to the residue output.
  - The design brief requires disagreements, candidate removed readings, and classifications that current authority cannot settle.
  - The packet has candidate removed and unsettled classifications, but no explicit disagreement type.
  - If no true disagreements were found, the artifact should state that directly with a zero count.

- Tighten the label for the 260 non-confirmed candidate rows.
  - Current wording: `not Coptic Reader confirmed`.
  - Better wording: `not checked by captured Coptic Reader fixture` or `no scoped current authority confirmation`.
  - Reason: outside the captured fixture scope, Coptic Reader has not rejected the reading. It is simply not available as current authority in this run.

- Tighten the labels for the seven candidate removed rows.
  - Keep them in the candidate removed bucket.
  - Avoid wording that implies final removal unless a broader current authority check has been completed.
  - Suggested status meaning: historical witness present, absent from the scoped Wednesday Day Coptic Reader fixture, candidate removed pending current-authority confirmation.

- Rename or clarify `current_psalm_equivalence_unresolved`.
  - The current wording can imply the Psalm row is current.
  - Better wording: `pending_psalm_equivalence_unresolved`.
  - These rows should remain candidates until the exact Psalm equivalence is encoded.

- Ensure `open_questions_for_george.md` receives the unresolved residue, not just a summary.
  - Include the seven candidate removed Wednesday readings.
  - Include the five unresolved Psalm equivalence cases.
  - Include the current-authority pending class, preferably summarized by day and service hour with a path to the full CSV.
  - Include any zero-count disagreement statement if no disagreements were found.

- Preserve fixture-scope limits in all public-facing wording.
  - Coptic Reader is current authority only where the fixture was captured.
  - Absence outside that fixture scope must not be phrased as a current-authority rejection.

## Outcome

Conditional pass.

The Phase 4 artifacts satisfy the core temporal classification structure and the row counts are coherent. The main evidence classes are present: current confirmed, historical or removed, candidate current, candidate removed, and unresolved Psalm equivalence.

Before treating Phase 4 as publication-ready, Codex should revise the status wording, add an explicit disagreement residue category or zero-count note, and make sure all unresolved issues are carried into `open_questions_for_george.md`.
