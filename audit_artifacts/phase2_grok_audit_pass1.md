# Phase 2 Grok Audit Pass 1

## Findings

- Based on the supplied Phase 2 packet, the re-keying architecture is sound.
- The dataset reports 66,378 presentation rows and 2,663 reading identity rows, with 2,663 unique identity rows.
- `missing_identity_joins` is 0, which satisfies the joinability requirement between presentation rows and `reading_identity`.
- No blank structural evidence fields are reported:
  - `blank_source_key`: 0
  - `blank_display_ref`: 0
  - `blank_provenance_url_source_file`: 0
- The source-kind counts sum exactly to 66,378, matching the presentation row count.
- The current-status counts also sum exactly to 66,378.
- The authority-tier counts also sum exactly to 66,378.
- The Coptic Reader fixture rows look correctly constrained:
  - They preserve supplied source labels in `source_ref`.
  - They normalize display references for user-facing use.
  - They keep Psalm MT/LXX distinctions visible.
  - They do not invent an MT equivalent for the unresolved `Psalm 41:1` row. The row correctly leaves `canonical_mt_ref` blank and displays `LXX Ps 41:1 (MT equivalent pending)`.
  - The named reading `Memoirs of Job` is correctly modeled as `named-reading` with no fabricated canonical biblical reference.
- The source registry includes the emitted source keys shown in the samples:
  - `coptic_reader_fixture_wednesday_day`
  - `katameros_api_sqlite`
  - `copticchurch_date_resolved`
  - `st_mary_ottawa_pascha`
  - `special_service`
  - `agpeya`
  - `bright_saturday_service_order`
- Authority tiers appear controlled in the emitted rows:
  - `current_authority`
  - `public_current_practice_reference`
  - `working_local_source`
  - `historical_printed_witness`
- The packet correctly avoids requiring full Coptic Reader ingestion. The fixture is treated as a confirmed slice, not as proof of full app coverage.

## Required Revisions

- The packet does not visibly demonstrate a `source_convention` field on presentation rows. The audit criteria require presentation rows to include source convention. Codex should either:
  - add `source_convention` to the emitted presentation schema if it is missing, or
  - provide a validator excerpt showing the field exists and is populated or intentionally nullable under controlled rules.
- Codex should include one explicit registry validation metric in the next packet:
  - unregistered emitted source keys: 0
  - uncontrolled emitted authority tiers: 0
- Codex should include the exact distinct emitted source-key list from the full presentation dataset, not only samples, so registry coverage can be confirmed without inference.
- Codex should document the allowed status values and allowed authority tiers in the schema or validator output. The current counts look controlled, but the packet does not show the allowlist itself.

## Outcome

Conditional pass.

The Phase 2 dataset satisfies the main identity, display, provenance, fixture, and blank-field requirements based on the supplied packet. The one blocking audit gap is evidentiary, not clearly a data failure: the packet does not show the required source-convention field. If Codex proves that field exists and is governed, or adds it, Phase 2 should pass this audit round.
