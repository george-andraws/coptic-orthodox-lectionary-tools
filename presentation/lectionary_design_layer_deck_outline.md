# Coptic Lectionary Design Layer Deck Outline

Purpose: handoff deck for George before pushing the article and design-layer data into the site repo.

Visual direction: warm Coptic teaching deck with burgundy, cream, gold, and charcoal. Mostly visual, one idea per slide.

## Slide 1 - The Church teaches Scripture in time
- Title slide.
- Message: the lectionary is not a list. It is Scripture received in worship, season, and commemoration.

## Slide 2 - The problem with date-only tools
- Show date-to-readings, passage-to-uses, and source-status cards.
- Speaker note: the reverse lectionary answers where the Church reads a passage.

## Slide 3 - The design answer is identity first
- Show source label to canonical MT to canonical LXX to identity key.
- Counts: 2658 identities and 66381 presentation rows.

## Slide 4 - Psalm numbering must be honest
- Show Psalm 50 LXX and Psalm 51 MT as one identity with labeled witnesses.
- Speaker note: preserve source labels, do not flatten traditions.

## Slide 5 - Pascha needed attestation, not guessing
- Counts: 446 Pascha groups, 420 temporal residue rows.
- Speaker note: Coptic Reader fixture governs its captured scope.

## Slide 6 - Temporal classification prevents overclaiming
- Residue counts: {"candidate_removed_needs_current_authority_confirmation": 11, "current_authority_pending": 255, "historical_witness_no_current_comparator": 149, "psalm_equivalence_unresolved": 5}.
- Speaker note: unresolved rows are classified review residue, not hidden failures.

## Slide 7 - The Synaxarium bridge is useful and humble
- Counts: 664 commemorations, 4688 bridge rows.
- Methods: {"numbered_summary_entry": 523, "prose_lead_inferred": 141}.
- Bridge basis: {"collection-type": 3899, "explicit": 789}.
- Bridge confidence: {"high": 789, "medium": 3899}.
- Speaker note: 69-covered rows are explicit and high confidence; outside-69 rows remain collection-type and medium confidence.

## Slide 8 - What the site consumes
- Show article, presentation dataset, today's readings, passage footprint, bridge, open questions, and integration spec.

## Slide 9 - Open questions are batched
- Psalm equivalence, 69 collections list, Coptic Reader coverage beyond fixture, prose-lead Synaxarium wording, site corpus joins.

## Slide 10 - George's push path
- Copy files, wire search to identity keys, accept MT and LXX input, join site slugs, verify the plain URL after deploy.
