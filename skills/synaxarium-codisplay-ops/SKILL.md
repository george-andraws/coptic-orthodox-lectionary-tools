---
name: synaxarium-codisplay-ops
description: "Use when shipping synaxarium co-display releases."
---

# Synaxarium co-display releases

## Scope

Extend existing `@andraws/lectionary-data` in this repository, not a separate package. The optional consuming site is `george-andraws/coptic-corpus`; inspect its own checkout and instructions before making consumer changes. Do not assume a workspace change appears in another checkout. Preserve pre-existing work, use an isolated branch/worktree, and remove only approved rebuildable outputs. Build from a requester-supplied, audited source directory containing `synaxarium_from_coptic_reader.jsonl` and `coptic_reader_index.json`; do not use pre-purification copies or publish raw captures.

Keep commemorations separate from reading selection. No reading-to-saint link or explanatory reason. Preserve exact titles and opaque ids. Map source hator to public hatour and epep to abib explicitly. The audited catalog has 366 days, 868 records; Nasie 6 is leap-only. Capture ordinal is display priority, not liturgical precedence. Null grouping avoids unaudited merges/splits.

## Documentation sources

Read site `docs/lectionary-and-synaxarium.md` for the current UI/runtime contract and SETUP.md for owner operations. Read package `docs/SYNAXARIUM_RELEASE.md` and the package README for the public schema and release workflow. Treat the old 05-LECTIONARY-DESIGN.md, lectionary_spec.md and 1.2.0 release notes as historical/internal context, not current model routing or catalog schema instructions. Site docs/ is ignored for new files, so intentionally stage new maintained guides explicitly and verify they appear in the commit. Updating a package README in source does not mutate an immutable published npm artifact; do not republish during a docs-only task.

## Validation

Use exact field allowlists at day and record levels. Keep captures and source fingerprint fixtures outside npm files. Validate exact day keys, per-day source counts, ids, titles, order, types and year flags. Test same-total record transfers, substituted days, private day fields, duplicate ids and malformed rows.

Reuse package calendar.js in clients, no second converter. Never add a timezone-dependent offset to force source agreement. Verify UTC/western/eastern zones, Nasie 6/new year, Gregorian centuries, all source-index dates and independent convertdate samples.

## Runtime and compact UX

Order: date service with package calendar, readings, synaxarium with public catalog. Use one LL_dateService snapshot per nav/render cycle. Test clock changes and reject stale reading responses after day changes with a gated browser response, not sleeps.

Show each civil/Coptic date once in the readings heading, for example Daily Readings, Sept 8, 2026 | Nasie 3, 1742 AM. Keep the two dates on one line on mobile, allowing the title to wrap above them. Collapse the date input under Choose date, retain compact Previous/Today/Next controls. Remove stacked Civil date/Coptic date panels and repeated fixed-date occasion headings, but retain named feasts/cycles.

Render a distinct Synaxarium list entry after the first Praxis on both Daily Readings and homepage, with every canonical title visible. If no Praxis is present, place it after available readings. Preserve independence from reading selection; no reason or saint-to-reading relationship. Do not recreate the old separate homepage commemorations section.

Replace the homepage From the library promotion with Today in the Church, using existing season context and a compact synaxarium preview. Preserve Continue reading alongside it. The card must work for new or paused visitors without fetching the journey manifest. Use equal 50/50 desktop card widths with matched titles and subtitles, aligned to the hero and lower grid; stack on mobile. Remove the journey wrapper's horizontal padding and bottom border rather than compensating with offset margins. Show every commemoration in slightly smaller text, no collapsed preview or +N more. Do not display the old independence disclaimer, while keeping the underlying data independent. Empty catalogs stay quiet. On Daily Readings, place a small contextual Reverse Lectionary link to /lectionary between the date navigation and results; test the resolved destination because Quartz rewrites href values to relative paths. Keep generated homepage/readings markup and sync-content templates aligned. Test date navigation, no-Praxis fallback, all titles, missing catalog, mobile line wrapping, paused/new journey states and stale fetches.

## Release gates

- Fresh site: npm ci, npm run install-plugins, npm test, npm run build, npx tsc --noEmit. Missing plugin setup can cause an oversized unsharded contentIndex and missing .quartz/plugins types. Fix prerequisites, not checks.
- Package tests may need isolated Python 3.11 with beautifulsoup4, requests and convertdate. Use uv rather than system installs.
- Inspect actual npm pack and metadata after npm version minor. Keep existing reading provenance distinct from new catalog data.
- npm may accept an upload before registry processing completes. Do not republish. Confirm npm view version and dist.integrity, install exact published version, compare installed bytes to the audited tarball.
- Stop on publication failure when required. Do not work around auth without authorization.
- Verify clean-checkout gates and emitted homepage bundle, including all catalog ids and no private catalog fields.
- Leave a named local branch and one clean site commit. Check detached HEAD and ahead-of-main count before giving a push command. Do not push or wrangler deploy when reserved for the maintainer.
- Real-phone acceptance remains separate: plain andraws.net homepage without cache query during local evening, dates match between blocks, saints match live Coptic Reader.

## Model routing

Follow current user direction. Do not assume delegate_task inherits the parent model or claim identity from prompt text; inspect actual routing metadata. Skip separation when the user waives it.
