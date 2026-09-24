# Phase 7 Pascha clarification and removed-row review pattern

Use this when continuing a lectionary design-layer correction pass that touches Pascha computation wording, the 69 foundational-reading verdict, or duplicate-looking Holy Pascha removed rows.

## External source fixtures when web is blocked

If the requester explicitly supplies externally verified citations and forbids web fetch/search:

1. Do not use web tools.
2. Treat the supplied citations as fixed fixtures for the current pass.
3. In the execution log, say source verification was externally supplied and that any an independent reviewer audit is limited to internal consistency, not independent web re-verification.
4. If a partial source-check artifact exists from a blocked web attempt, either delete it or fold only its useful limitation note into the execution log. Do not commit a misleading partial web-research artifact.
5. Regenerate from `build_design_deliverables.py`, then run the usual verification suite.

For the Coptic Pascha clarification, the approved fixture wording was:

> The Coptic Church does not look up this date in the modern Jewish calendar. It computes the Paschal full moon by the Alexandrian reckoning set at Nicaea, the same nineteen-year cycle the Eastern Orthodox churches use, so the Coptic Pascha falls on the same Sunday as the Eastern Orthodox Pascha. In 2026, for example, the Coptic and the Russian Orthodox Pascha both fall on 12 April.

Attach the supplied fixture citations, without live fetching, when the requester provides them:

- Fr. Andrew Stephen Damick, Ancient Faith Ministries, 2022, for Coptic use of the traditional Julian Paschalion.
- GOARCH Pascha date misperceptions article, for Pascha as computed formula rather than modern Jewish-calendar lookup.
- timeanddate 2026 Coptic and Russian Orthodox Easter references, for the worked 12 April 2026 example.
- OrthodoxWiki Coptic Calendar plus copticchurch.net calendar notes, for Alexandrian/Nicaea/nineteen-year-cycle framing. Keep Demetrius the Vinedresser attribution hedged as traditional.

## 69 foundational readings verdict wording

Do **not** overstate the 69 identity as `CONFIRMED_SAME_SET` unless a reading-by-reading roster has actually been matched. In the Phase 7 correction pass, the maintainer corrected the evidence standard:

- Correct active verdict: `INFERRED_LIKELY_SAME_SET` (roster unverified).
- Read from source: Youssef describes 69 foundational reading collections, `al-qira'at al-asasiyya`, arranged by kind of feast and commemoration and gathered in volume two of the Yearly Katameros.
- Read from source: Ottawa/UKMID Katameros of the Days is the weekday-and-feast volume in English and its TOC presents a matching count of 69 dated reading sections.
- Inferred: alignment rests on shared source tradition, volume two placement, category match, and count.
- Not established: a verified date-by-date or reading-by-reading identity between Youssef's 69 type-collections and Ottawa's dated entries.
- Article wording should avoid framing Youssef's 69 as 69 calendar days. Use language like "69 collections of readings" for Youssef and "69 dated entries" or "69 dated-entry bridge taxonomy" for Ottawa.
- The `basis=explicit` bridge upgrade can remain because it stands on Ottawa's direct dated reading sections, not on Youssef printing or matching the full roster.
- Add or retain an open question to verify the reading-by-reading roster mapping between Youssef's 69 type-collections and Ottawa's dated entries.

## Removed-row duplicate review pattern

When reviewing duplicate-looking Pascha removed rows, do not silently normalize unless the duplicate is unambiguous and source-row provenance can be retained.

Checklist:

1. Compare `out/design/temporal_classification.csv`, `out/design/temporal_residue.csv`, `out/design/reverse_lectionary_presentation.csv`, `out/design/reading_identity.csv`, `out/data/pascha_source_text_index.csv`, `out/data/pascha_day_hour_index.csv`, the raw Ottawa extracted text, and the Coptic Reader fixture.
2. Distinguish same-span alternate notation from true source disagreement.
3. If deduping, patch the generator, not generated CSVs, and add a verifier guard.
4. Report uncertain items in `audit_artifacts/open_questions_for_george.md` and the execution log.
5. Keep one logical commit per change. If generated files are missed from staging, amend the same commit rather than creating a second commit for the same logical change.

Durable findings from the continuation pass:

- `Prov 4:4-27,5:1-4` and `Prov 4:4-5:4` are the same continuous Proverbs span stored two ways. A narrow canonical alias may normalize `Prov 4:4-5:4` to `Prov 4:4-27,5:1-4` while preserving both source locators.
- Do not dedupe Job spans automatically: older Ottawa gives `Job 27:16-28:2` in Wednesday Third Hour, a local corrected day/hour row gives `Job 27:16-20; Job 28:1-2` in Wednesday Sixth Hour, and the Coptic Reader fixture gives only named `Memoirs of Job` without verse boundaries.
- Treat `Prov 1:10-33` and current `Prov 1:11-35` as older/current source variants of one slot, not a double-counted current reading.
- `Wis` maps to Wisdom of Solomon in the repo parser, while `Sir` is separate Sirach. Do not reclassify `Wis 1:20-2:15` or `Wis 3:12-24` as Sirach without source evidence. Keep them unmarked candidate-removed rows pending review.

## Audit pattern when web is blocked

Use an independent reviewer as independent auditor through Hermes CLI with only `file,terminal` toolsets when the maintainer forbids web use. The audit should explicitly say it did not use web/search/fetch tools and that Step 2 sourcing is internal-consistency-only if citations were externally supplied.

Run at least:

```bash
python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py
python3 build_design_deliverables.py
python3 verify_design_deliverables.py
git diff --check
```

Also scan generated article, log, open questions, spec/site spec for stale bridge prose, em dashes, and banned words when content rules are active.