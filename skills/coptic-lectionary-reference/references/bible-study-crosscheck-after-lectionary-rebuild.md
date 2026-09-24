# Bible-study cross-check after a lectionary rebuild

Use this when the requester asks to update Bible-study guides after repairing or rebuilding the local lectionary package.

## Durable workflow

1. **Do not broaden scope into link repair.** If broken-link checks are requested, treat them as verification/reporting only unless the requester explicitly asks to fix links.
2. **Capture query evidence first.** For each repaired placement, run the currently supported local query helper flags from `--help`, then save the exact output under the lectionary repo `audit_artifacts/` before editing guides.
3. **Patch only guides with overlapping passages.** Build the affected guide list from added/removed/modified rows and normalized passage spans. Do not sweep unrelated Bible-study notes.
4. **Update reader-facing sections cleanly.** Replace stale absence language such as "no exact indexed occurrence" only where the rebuilt data now supports a placement. Keep the guide body free of tool/process language like parser, script, command, pipeline, helper output, row counts, or local paths.
5. **Update provenance/source-map notes.** If a book-level `Resources Used - <Book>.md` exists, update the affected source-map bullets so they do not contradict the guide.
6. **Mark downstream artifacts stale when tracked.** If the guide frontmatter or status table tracks Google Docs/audio/MP3, mark them stale after Markdown changes. For notes with existing audio links in frontmatter but no formal audio field, add a scoped `downstream_artifacts: stale-after-<date>-lectionary-update` marker rather than changing the audio URL.
7. **Verify after edits.** Run query regression, expected-text scans over touched files, stale-wording scans for superseded absence phrases, and a process-marker scan over guide bodies. Record results in an audit artifact and append the impact report/daily log.

## 2026-06-06 precedent

A Holy Pascha cross-chapter parser repair changed effective support for these guide updates:

- `Zephaniah 1:14-2:2` -> Monday Eve, Third Hour, source text raw `Zephaniah 1:14-2:1-2`.
- `Isaiah 55:1-56:1` -> Great Thursday, Liturgy of Blessing of the Water, source text raw `Isaiah 55:1-13-56:1`.
- `Zechariah 12:11-14:3,14:6-9` -> Great Thursday, Eleventh Hour, source text raw `Zechariah 12:11-14:1-3, 6-9`.
- `Zechariah 14:6-11` -> Good Friday, Ninth Hour.

The guide edits were limited to Zephaniah 1, Zephaniah 2, Isaiah 55, Isaiah 56-57, Zechariah 12, Zechariah 13, and Zechariah 14, plus `Resources Used - Isaiah.md`, the lectionary impact report, and the daily log.

## Output standard

Final response should list exact guide paths changed, what lectionary status changed, where evidence was saved, and the verification result. Do not say broadly that "some files changed."