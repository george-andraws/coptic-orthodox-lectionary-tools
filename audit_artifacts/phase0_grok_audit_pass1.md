# Phase 0 Grok Audit Pass 1

## High-Priority Findings

- The article is mostly safe, but it still contains a few unqualified structural claims:
  - “It joins Scripture to feast, fast, hour, commemoration, and sacrament” may imply the core lectionary structure covers all sacramental reading contexts. Qualify this unless a rite-specific source is cited.
  - “The Church does not arrange readings merely by topic” is reasonable as theological framing, but should be marked as interpretation unless the cited source explicitly makes that claim.
  - “She places the readings where Christ can be seen” is a theological inference and should be phrased as such.

- The Athanasius use is acceptable because the article says the “fountains of salvation” image is being applied by analogy. That inference is flagged well.

- The John Chrysostom reference is too thin for the frontmatter and source list. He is named, which satisfies the “named Fathers only” rule, but the article cites no specific homily, work, or passage. Either remove him from `fathers` and the patristic anchor section, or cite a specific Chrysostom text.

- The deacon language passes the content rule. The article says the deacon “serves the Lord by proclaiming the word entrusted to the Church,” not the rejected deacon-service phrasing.

- The Christ language passes the content rule. The article presents Christ as the fulfillment and opener of Scripture, not as helpless or acted upon passively.

- The glossary definition of “Katameros” is risky: “literally readings arranged in parts” should be checked or softened. Prefer: “Katameros: a Coptic lectionary book or collection of appointed readings.” Do not make a literal etymology claim unless sourced.

- The spec implements the key locked decisions in broad form, but the compressed packet does not prove vocabulary completeness. The packet points to `out/design/lectionary_schema.json`, but the audit packet itself does not list the controlled values for several fields needed by the schema.

## Suggested Revisions

- Revise the article’s opening claim to avoid overreach:
  - Current: “It joins Scripture to feast, fast, hour, commemoration, and sacrament...”
  - Safer: “In the Church’s worship, appointed readings are received in relation to feasts, fasts, hours, commemorations, and liturgical services, according to the sources and rites in view.”

- Mark theological readings as interpretation:
  - Current: “This is the heart of the Coptic lectionary.”
  - Safer: “Theologically, this helps explain the heart of the Coptic lectionary.”

- Qualify source-backed structure:
  - Current: “The Coptic Encyclopedia describes the lectionary as a set of four books...”
  - Safer: “For the core lectionary books, the Coptic Encyclopedia describes four books...”
  - This avoids implying that all special services, sacramental rites, or later local practice are exhausted by the four-book list.

- Fix the John Chrysostom entry:
  - Option 1: remove `John Chrysostom` from `fathers` and remove the source bullet.
  - Option 2: cite a specific homily or treatise and say exactly how it supports Scripture as proclamation, exhortation, and repentance.

- Revise the glossary:
  - “Katameros: A Coptic lectionary book or collection of appointed readings.”
  - “Synaxarium: The Church’s daily-cycle book or index of commemorations of saints, martyrs, feasts, and events.”
  - This supports the locked decision that the Synaxarium functions as a daily-cycle index, not as a reading-precedence authority.

- In the spec, add explicit controlled vocabularies or confirm they are present in `out/design/lectionary_schema.json` for:
  - `source_convention`
  - `canonicalization_confidence`
  - `service_day`
  - `service_hour`
  - `service_section`
  - `slot`
  - `temporal_status`
  - `attestation`
  - `current_authority`
  - Synaxarium `type`
  - bridge `basis`
  - bridge `confidence`

- Clarify overlapping status terms:
  - `current_confirmed`
  - `current_confirmed_coptic_reader`
  - `current_confirmed_by_fixture_equivalence`
  - `current_public_or_local_reference`
  
  These need definitions that prevent a public/local source row from being mistaken for Coptic Reader-confirmed current practice.

- Fix the numbered list in “Locked decisions implemented.” It jumps from 3 to 5. Renumber it so audit readers do not suspect a missing decision.

## Acceptance Risks

- Main article risk: unmarked theological inference could be mistaken for source-backed lectionary structure.

- Main spec risk: vocabulary sufficiency cannot be accepted from the compressed packet alone. The packet claims the machine-readable schema contains controlled vocabularies, but the values are not shown here.

- Source authority risk: the source tier table is too compressed. It only shows `current_authority` for manually captured Coptic Reader fixture material. It should also define how public date-resolved sources, old editions, scholarly structural sources, and local references rank or do not rank.

- Synaxarium risk: the article and spec are close, but should explicitly say the Synaxarium is a daily-cycle commemoration index and not a source that automatically determines lectionary reading precedence.

- Pascha temporal risk: the spec handles historical candidates, current confirmation, and unresolved Psalm equivalence, but acceptance depends on clear downstream display rules so historical Pascha witnesses are not presented as current Coptic Reader practice.

## Outcome

Conditional pass with required edits.

The artifacts are directionally sound and mostly respect the locked decisions. They do not violate the deacon, Christology, or named-Fathers content rules in a severe way. The main blockers are precision issues: unflagged inference in the article, a weak Chrysostom citation, a risky Katameros glossary definition, and incomplete visible controlled vocabularies in the compressed spec packet.
