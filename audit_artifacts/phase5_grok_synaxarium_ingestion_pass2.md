# Phase 5 Grok Synaxarium Ingestion Memo Pass 2

## Findings

- Pass 1 blocker issues appear fixed in the revised extraction packet.
- Coverage is complete at the day level:
  - `source_rows`: 366
  - `unique_coptic_days`: 366
  - `commemoration_rows`: 664
  - `multi_commemoration_day_count`: 221
- The prior day-title fallback problem appears resolved:
  - `day_title_fallback_count`: 0
  - `day_title_like_count`: 0
  - `long_title_count`: 0
- The prior inferred-title caveat problem appears resolved:
  - `prose_lead_inferred`: 141
  - `inferred_without_caveat_count`: 0
  - Sample inferred rows such as `Tut 4`, `Tut 5`, `Tut 9`, `Tut 11`, `Tut 14`, `Tut 15`, and `Tut 19` all carry explicit caveats.
- The prior duplicate prose-title issue appears resolved. The packet states that numbered prose paragraphs after clean heading snippets are skipped, repeated heading snippets are deduplicated, and no long prose-like titles remain.
- Multi-commemoration extraction looks materially better:
  - `Babah 26` correctly separates Timon the Apostle from the Seven Martyrs on the Mount of St. Antonius.
  - `Baunah 15` correctly separates the return of St. Mark’s relics from the consecration of Mari Mina at Maryut.
  - `Abib 3` correctly separates St. Cyril I from St. Celestine.
  - `Abib 9` correctly separates St. Simon Cleophas from Pope Cladianus.
- Classification changes look safer than pass 1:
  - Theotokos classification is narrowed to explicit Mary/Theotokos titles.
  - Generic `commemoration` is used where the extractor cannot safely identify a person, feast, or office category.
  - Generic classifications are caveated, as seen in `Tut 3`, `Tut 10`, `Tut 12`, `Baunah 15`, and similar rows.
- Required metadata now appears present:
  - `extraction_method` is emitted.
  - `caveat` is emitted where needed.
  - `source_url` is present in samples.
  - The packet states that full `source_summary` is stored without truncation.
- The verifier coverage is now aligned with the ingestion risks from pass 1. It checks:
  - no day-title fallback rows
  - no long prose-like titles
  - caveats for prose-lead rows
  - unique `commem_id`
  - `source_url` and `source_summary` presence
  - bridge integrity
- Reported verification passed:
  - `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py`
  - `python3 build_design_deliverables.py`
  - `python3 verify_design_deliverables.py`
  - result: design deliverables verified

## Remaining Caveats

- The 141 `prose_lead_inferred` rows are still inferred from the first source-summary lead rather than extracted from numbered summary entries. This is acceptable for ingestion because every such row is explicitly caveated, but these rows should not be treated as final publication wording without later source-page review.
- Type labels remain heuristic. The safer behavior is now in place, but some entries may still be debatable at the boundary between `departure`, `hierarch`, `patriarch`, `martyr`, `apostle`, and generic `commemoration`.
- Generic `commemoration` rows are intentionally conservative. They are suitable for design-layer ingestion, but they may need manual enrichment if the final product requires precise saint, event, church-consecration, or relic-translation taxonomy.
- The sample shows `Tut 12` rank 1 classified as `hierarch` because the title includes Nestorius, Archbishop of Constantinople, though the event itself is the Third Ecumenical Council. This is not a blocker, but it is a good example of why type should be treated as an assistive category, not a canonical theological classification.
- The packet reports successful verifier output, but this pass is based on the supplied packet rather than a fresh independent re-run of the CSV in this response.

## Outcome

Ready for Codex final ingestion audit.

The pass 1 caveats have been addressed well enough for the Synaxarium commemoration ingestion to proceed to final audit. The remaining risks are bounded, visible in metadata, and suitable for downstream handling: inferred rows are caveated, generic classifications are caveated, full day coverage is preserved, multi-entry days are represented, and the verifier now guards the exact failure classes that caused concern in pass 1.
