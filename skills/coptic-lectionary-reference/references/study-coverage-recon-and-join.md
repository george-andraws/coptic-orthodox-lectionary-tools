# Study coverage reconnaissance and join

Use this pattern when the requester asks to join existing Bible-study notes to the Coptic lectionary dataset, produce coverage artifacts, or prepare revision triage data.

## Scope boundary

- Treat the lectionary dataset as final input unless the requester explicitly asks for a data repair.
- Do not edit Bible-study notes or downstream documentation package bodies during reconnaissance.
- Build reports and deterministic artifacts only.
- Do not author thematic or spiritual "why" commentary. Source-map and flag only.

## Inputs that worked

Primary repo: `$REPO_ROOT`.

Useful files:

- `out/design/reading_identity.csv`, stable reading identities and `spans_json`.
- `out/design/reverse_lectionary_index.jsonl`, placement rows keyed by `identity_key`.
- `out/data/reverse_lookup_crosswalk.csv`, existing passage to occurrence crosswalk.
- `out/data/bible_chapter_lectionary_occurrences.csv`, chapter occurrence inventory.
- `out/design/synaxarium_reading_bridge.csv`, bridge `basis` and `confidence` keyed by `reading_identity_key` plus Coptic day.
- `out/design/foundational_reading_collections_69.csv`, 69 foundational collection vocabulary.
- `out/design/source_registry.csv`, source list.
- `lectionary_spec.md` and `coptic-lectionary-and-synaxarium.md`, controlled vocabulary and prose source context.

For Bible studies, scan active notes under the Biblical Explanations tree, but exclude `Audits`, `Archive`, `_superseded`, `Assets`, audio folders, index notes, and resources notes. Active notes usually have `type: chapter-study` and populated `passages` frontmatter.

## Join pattern

1. Parse study `passages` from frontmatter.
2. Parse `reading_identity.csv` `spans_json` into verse spans.
3. Match study spans to reading spans by overlap, not exact string equality.
4. Join matched identities to `reverse_lectionary_index.jsonl` placement rows.
5. Enrich placement rows with Synaxarium bridge fields only when the bridge row's Coptic day matches the placement day.
6. Derive `collection_type` only when the placement day matches `foundational_reading_collections_69.csv`; otherwise leave it blank.
7. Use `hour_theme` when present. Do not fabricate `homily_ref` or placement-level why fields when the dataset lacks them.

## Output shape

Good artifact set:

- `out/study_lectionary_coverage.csv`, one row per study, matched reading, occasion placement.
- `out/study_coverage_rollup.csv`, one row per study for triage.
- `out/lectionary_gap_no_study.csv`, lectionary OT, NT, and deuterocanon readings with no matching study.
- `out/why_flags.csv`, suspicious rows such as missing occasion label, missing or inferred bridge basis, no 69 collection match, or no source for a Pascha or major-feast link.
- `out/why_source_map.md`, source list only, not commentary.
- `audit_artifacts/study_coverage_recon_report.md`, answers inventory and field-gap questions directly.

## Verification checklist

Before reporting or committing:

- Required CSV columns exist in the requested order.
- Row counts match the report.
- Exact duplicate rows are zero, especially in `lectionary_gap_no_study.csv`.
- Every output `identity_key` exists in both `reading_identity.csv` and `reverse_lectionary_index.jsonl`.
- Coverage `study_slug` values exist in rollup.
- Rollup counts recompute from coverage.
- Gap rows do not overlap parsed study passage spans.
- Authored prose has no task-forbidden terms or punctuation.
- `git status --short` shows only intended artifact/report/log files before committing.

## Report-only triage cuts after coverage artifacts exist

Use this when the requester asks for follow-up cuts from existing coverage artifacts and explicitly says report only.

1. Treat `out/study_lectionary_coverage.csv`, `out/study_coverage_rollup.csv`, `out/why_flags.csv`, and `out/design/reverse_lectionary_index.jsonl` as read-only inputs. Do not regenerate or edit the CSV artifacts unless the user explicitly asks for repair.
2. For why-flag breakdowns, compare flags to coverage rows using the shared identifying fields, not only `identity_key`. A reliable key is `study_slug`, `identity_key`, `matched_reading_ref`, `occasion_id`, `occasion_short_label`, `bridge_basis`, `season`, `service`, `hour`, and `slot`.
3. For Pascha / Holy Week slices, filter coverage on `season == "Pascha / Holy Week"`. When tracing back to reverse-index rows, match on `identity_key`, `display_ref`, Pascha-derived season, and service/slot/hour labels, with a fallback to identity plus display reference when labels differ. Report unmatched coverage rows explicitly.
4. For hour-theme dumps, count both distinct reverse-index rows and coverage-row hits, because one reverse row can support multiple study rows. For OT prophecy and Psalm dumps, filter reverse rows by `slot_type in {prophecy, psalm}` or slot text containing prophecy/psalm, then output distinct `(day_title, service_hour, slot_type, display_ref, hour_theme)` rows.
5. For lectionary-note reconciliation, constrain the downstream documentation package-frontmatter scan to the study slugs represented in `out/study_coverage_rollup.csv`. The live downstream documentation package may have newer studies not represented in the frozen coverage artifacts; report those as outside-scope drift instead of letting them change the expected count.
6. Compare prose `lectionary:` notes with coverage-derived labels by deterministic phrase scan over existing artifact labels only: occasion, season, service, and hour. Bucket each represented note as `agrees`, `extra_in_note`, `missing_from_note`, or both. Count studies with joined occasions and no `lectionary:` note from rollup slugs with `occasion_count > 0`.
7. For report-only cuts, still run content-rule verification, file-exists checks, and `git status --short` before committing. Commit exactly the report files requested, one commit per file when asked.

## Audit discipline

Run an independent audit, preferably via a leaf subagent, before final report. Ask it to verify columns, counts, joins, duplicate rows, and prose-rule compliance. If the audit finds hygiene issues, fix them and rerun verification before commits.

## Commit discipline

When the brief says one commit per artifact, commit each generated artifact separately. Include the execution-log update as its own commit after the artifact/report commits.
