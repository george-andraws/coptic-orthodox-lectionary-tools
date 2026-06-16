# Phase 0 Grok Audit Pass 2

## Remaining Findings

1. Pass 1 fixes are mostly satisfied.

2. The article now qualifies the main overreach:
   - "according to the sources and rites in view"
   - "Theologically, this helps explain"
   - "sources show more than a topical reading plan"

3. The theological claim is now marked as theological interpretation rather than presented as a direct source conclusion.

4. The four-book claim is improved:
   - "For the core lectionary books"
   - "the Coptic Encyclopedia describes four books"
   
   This is acceptable, but it would be stronger if the article explicitly says this does not exhaust every liturgical or rite-specific reading source.

5. John Chrysostom no longer appears in the supplied snippet. If removed from the full article, Pass 1 is satisfied.

6. The Katameros and Synaxarium glossary entries are improved. The Synaxarium entry is now less likely to imply that the Synaxarium itself assigns readings.

7. The spec now includes explicit source authority tiers, current-status definitions, attestation buckets, and a controlled vocabulary snapshot. This satisfies the requested design-layer clarification.

8. Minor remaining gap: the current-status definitions are clear in prose, but the article and spec should keep repeating that Coptic Reader confirmation currently applies only to the locked Wednesday Day fixture scope. The spec says this, but any summary prose should avoid implying wider Coptic Reader coverage.

## Required Revisions

1. Add one clarifying sentence near the four-book paragraph:

   "This four-book description concerns the core Katameros lectionary books, not every liturgical, sacramental, Agpeya, Synaxarium, or rite-specific source that may contain readings or commemorative material."

2. Keep the current theological-inference language. Do not remove "Theologically" from the Luke 4 paragraph.

3. Keep the Synaxarium distinction explicit. The Synaxarium should be described as commemorative source material, not as a direct reading-assignment table unless a specific source proves a direct link.

4. In the spec, keep `current_public_or_local_reference` visibly distinct from Coptic Reader confirmation. The current wording is good:

   "`current_public_or_local_reference` means useful reference data, not final current-practice authority."

5. If the full article still contains John Chrysostom elsewhere, either remove the reference or add a precise citation. It is absent from the supplied snippet.

## Outcome

Pass 2 result: conditionally approved after one small clarification.

Codex addressed the substantive Pass 1 issues. The remaining revision is not a blocker to the design layer, but the article should explicitly state that the four Katameros books are the core lectionary books rather than the complete universe of Coptic liturgical reading sources.
