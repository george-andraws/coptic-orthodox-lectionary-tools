# Study coverage independent audit

Generated: 2026-06-19 13:34:34 PDT

Scope: audited only the generated study coverage artifacts in this repository. No vault content was read or edited, and no commit was made.

## Files audited

- `out/study_lectionary_coverage.csv`
- `out/study_coverage_rollup.csv`
- `out/lectionary_gap_no_study.csv`
- `out/why_flags.csv`
- `out/why_source_map.md`
- `audit_artifacts/study_coverage_recon_report.md`

## Result

No blocking issue found. The artifacts satisfy the brief as report and build outputs: they do not edit Bible study notes, they use the existing final lectionary data, and the prose artifacts do not add thematic commentary.

## Column and row checks

All CSVs have the expected columns, in the expected order, with no missing or extra columns.

| Artifact | Rows | Exact duplicate rows | Notes |
|---|---:|---:|---|
| `study_lectionary_coverage.csv` | 6,541 | 0 | Matches recon report. |
| `study_coverage_rollup.csv` | 843 | 0 | Matches parsed study count in recon report. |
| `lectionary_gap_no_study.csv` | 3,016 | 0 | Duplicates removed after the first audit finding. |
| `why_flags.csv` | 8,207 | 0 | Matches recon report. |

Required identifying fields were populated in all rows checked. Critical blank counts were zero for study slug, book, chapter, passage or reading ref, identity key, occasion label, season, service, slot, bridge basis, status, and attesting edition where those fields exist.

## Join sanity checks

- Every `study_slug` in `study_lectionary_coverage.csv` exists in `study_coverage_rollup.csv`.
- Coverage has 414 unique study slugs with rows. Rollup has 414 studies with `occasion_count > 0` and 429 with `occasion_count = 0`.
- Rollup `occasion_count` equals the distinct `occasion_id` count per study, not the raw coverage row count. This is consistent.
- Rollup `max_occurrence_count`, `distinct_collection_types`, `distinct_seasons`, and `has_removed_historical` matched recomputed values.
- Every identity key in coverage, gap, and why flags exists in `out/design/reading_identity.csv` and `out/design/reverse_lectionary_index.jsonl`.
- Every `why_flags.csv` row maps back to a coverage row on the shared fields checked, and every why flag source locator is tied to the same identity key in the reverse index.
- Parsed study passage spans and reading identity spans showed no non-overlap in coverage rows that use ordinary chapter or verse syntax.
- Gap rows showed no overlap with any parsed study passage span, supporting the no-study gap intent.

## Suspicious blanks and caveats

These are visible, but documented by the recon report and not blockers:

- `homily_ref` is blank in all 6,541 coverage rows. The recon report states the lectionary data does not carry a populated placement-level homily or why-link field.
- `collection_type` is blank in 5,988 coverage rows. This aligns with the bridge model where only some rows map to the 69 collection vocabulary.
- `confidence` is blank in 3,248 coverage rows, exactly the rows with `bridge_basis = missing`.
- `hour` is blank in most coverage and gap rows. This is expected for non-hour-shaped services.
- `hour_theme` is blank in 3,473 coverage rows. It exists only where the source data carries an hour theme.
- `lectionary_gap_no_study.csv` initially contained 7 exact duplicate rows. They were removed after this audit finding, leaving 3,016 rows and 0 exact duplicates.

## Distribution spot checks

Coverage season distribution:

| Season | Rows |
|---|---:|
| Annual / fixed or ordinary cycle | 4,718 |
| Great Lent | 625 |
| Holy Fifty Days | 532 |
| Pascha / Holy Week | 440 |
| Agpeya | 140 |
| Special service | 86 |

Coverage bridge basis distribution:

| Bridge basis | Rows |
|---|---:|
| missing | 3,248 |
| collection-type | 2,767 |
| explicit | 526 |

Why flag reason distribution:

| Reason | Rows |
|---|---:|
| no 69 collection_type match | 4,165 |
| missing or inferred bridge_basis | 3,248 |
| no source for link | 794 |

## Prose and brief compliance

- `out/why_source_map.md` and `audit_artifacts/study_coverage_recon_report.md` contain no em dash characters.
- Those prose files did not contain any of the seven disallowed terms named in Section 0.8 of the brief.
- `why_source_map.md` is a source map and flagging rule, not reading-to-occasion commentary.
- The recon report explicitly states that no Bible-study note, lectionary source row, or thematic commentary was changed or authored.

## Blockers

None.

## Advisory follow-up

The 7 exact duplicate rows in `out/lectionary_gap_no_study.csv` were removed after the audit finding. No follow-up blocker remains.
