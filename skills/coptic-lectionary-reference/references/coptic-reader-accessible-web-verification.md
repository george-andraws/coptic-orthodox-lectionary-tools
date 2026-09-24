# Coptic Reader accessible web verification

Use the public app UI for authoritative, context-qualified source checks before attempting encrypted asset extraction.

1. Navigate https://copticreader.org/app/ in an isolated browser. Let Flutter initialize and dismiss release notes.
2. Enable accessibility with `document.querySelector('flt-semantics-placeholder')?.click()`. This exposes menu/date controls in the accessibility tree and DOM.
3. Select the date through the home Selected Season/Church Season button, then the exact Select Date/Time row (not its enclosing Calendar button). Switch the picker to Calendar if it uses scroll wheels. Use month arrows and year dropdown as needed.
4. Read back the exact selected day in the picker before OK. Allow Flutter transitions to complete before subsequent clicks. A condition that merely finds the date anywhere in the calendar is insufficient, because all displayed days match before selection. Verify the home screen's complete date, season, and Coptic date after OK, and save a context screenshot.
5. Navigate Readings > Liturgy > Pauline Epistle / Catholic Epistle / Psalm and Gospel. Menus expose role=button accessible names; coordinate clicks from CDP DOM.getBoxModel work. Avoid nested enclosing buttons with concatenated child text when selecting DOM targets.
6. Rendered reading documents live in a same-origin iframe on `#/document`. Extract visible text using `document.querySelector('iframe').contentDocument.body.innerText`. Do not infer absence from an empty top-level body. No decryption or script-secret extraction is needed.
7. Save actual rendered text and a screenshot showing the reference, plus the preceding date-context screenshot. Append each verified reading to a JSON evidence manifest with date, occasion, service, slot, printed reference, numbering convention, app version, and evidence paths; aggregate/dedupe in code.
8. Use an exact-context correction fixture. The same corrupt raw citation can have DIFFERENT corrections in different occasions. Preserve immutable raw citations and source hashes; never blanket-replace a book or range based on one verified date.

## Source and navigation safeguards

- Treat Coptic Reader Psalm verse numbers as edition-qualified liturgical versification, not merely LXX chapter numbers with MT verse numbers. Match the actual text to a primary canonical Bible source before assigning MT verse coordinates; preserve printed references unchanged. Printed Psalm30:28,26 aligns to MT31:24,23 by text, so chapter-only conversion is wrong.
- Reconcile all companion fragments of an affected Psalm and assert their emitted order without sorting. Fixing only an impossible fragment can leave a numerically valid but wrong companion chapter or duplicate composite.
- For Pascha hours, use Special > Pascha > named day > named hour and capture the document heading. General Readings is not the Pascha service directory.
- Prefer Selected Season to open date controls across responsive layouts. Assert both the home screen civil date and Coptic occasion; civil-date success alone does not validate a guessed Coptic date.
- Poll for a nonempty reading iframe; its route can appear before its content loads. Keep CDP promises below the IPC timeout and retry state checks instead of one long wait.
- Distinguish an explicit no-service rubric from a missing reading. A no-Vespers rubric during Jonah's Fast is not permission to substitute a Marian Vespers Gospel.

## Synaxarion exception-review gate

- Use Readings > Liturgy > Synaxarion after verifying the selected date. The same-origin iframe returns full readable English and Arabic Synaxarion text; do not conclude the source is inaccessible because the top-level body is empty or a first coordinate click failed.
- Treat Flutter semantics availability and animation completion as separate checks. New menu/date labels can appear before hit targets finish moving. Verify the resulting menu and date before extraction, and reject a stale civil date or wrong printed Coptic heading instead of saving it.
- Preserve the printed month names, including Paope, Meshir and Epep. A heading validator may compare hyphenated versus space-separated ordinal words, but must not rewrite captured text.
- Preserve the stateful official document URL exactly as observed, usually `https://copticreader.org/app/#/document`. It does not encode a selected day. When a task has a strict per-day citation gate, disclose this and obtain approval for official URL plus day, navigation instructions, and saved date-context/text evidence rather than inventing a deep link. the maintainer has accepted that format for the gated Synaxarium exception review.
- Keep Coptic Reader current-practice evidence separate from historical adjudication. Stage type or spelling display proposals only; retain people-level, numeral/ordinal, descriptor and collective-membership ambiguities for a human. A Thecla departure claim combined with a Thecla-and-Mouji martyrdom claim is not safely a type-only dispute merely because an earlier queue labeled it that way.
- For a bounded exception-only pass, extract full pages only for required exception days and source-access gate samples. Preserve IDs, append each successful day to a JSONL manifest, verify requested counts in code, and use byte-preservation checks rather than re-verifying consensus content.

## Family comparison safeguards

- Search the full purified catalog before proposing absence, and search every source claim and stored alias, not only the family record's display title. Preserve event distinctions, since a departure, birth and relic transfer naming one person are not automatically the same commemoration.
- Separate rejected search candidates from supported proposed associations. Rejected fuzzy hits must not remove a spine heading from the new-to-corpus bucket.
- Require actual membership evidence for grouping differences. Multiple unrelated headings on one day do not imply a group, and shared title boilerplate does not support a spelling proposal.
- Keep exact normalized equality separate from boosted similarity scores. A high fuzzy score must never become an exact match or hide a substantive type conflict.
- For the maintainer's six-bucket family comparison, bucket 2 may include spelling or type differences with separate subcounts, per his approved clarification. Preserve every family claim so one agreeing source cannot hide another source's type disagreement.

## Resumable full-year Synaxarion capture

- Reuse prior verified raw pages and context screenshots when the maintainer authorizes it. Preserve original civil dates, provenance, and raw bytes; do not relabel older captures as the new mapping year. Deduplicate by Coptic day and report reused versus new evidence.
- Retain the working browser session. If a readable iframe remains but Flutter navigation has no semantics, bring the app page to the foreground with CDP, re-enable accessible controls, and inspect the actual resulting menu before reloading. Background rendering can leave navigation unresponsive; an empty top-level body alone is not a failed source.
- Select the home Selected Season button by its accessible name instead of a fixed y coordinate. Its position varies with the occasion text. Preserve ordinary Readings > Liturgy > Synaxarion navigation and verify every resulting page.
- On Sundays and feast/season days, the home occasion may replace the numeric Coptic date. the maintainer approved home civil date and occasion plus the selected-date panel's numeric Coptic date plus the exact Synaxarion heading, with saved evidence. Do not confuse the liturgical occasion with the fixed calendar-day field.
- For single-year purification, select the union of imported days and the target year's movable-cycle date interval using captured app occasion boundaries. Add requested canaries explicitly. Preserve a pre-change index, catalog, raw files and hash manifest; capture into a separate directory first. Replace only selected days after validating scope, update source dates in the catalog without changing titles or IDs, and prove all untargeted raw files unchanged. Record document availability separately from liturgical prescription or suppression.
- In independent capture audits, require explicit unresolved grouping-review flags for collective headings, not merely false merge/split fields. Use conservative lexical candidate tagging with an inference label, retain false positives for review, and do not infer identity equivalence. A no-gap failure log must be zero bytes when the maintainer requires it literally empty; keep historical failures and status explanations in separate files.
- Limit browser batches to about 12 missing days. The outer tool can time out before a requested 1800-second timeout; write the index after each accepted day and checkpoint months against the full plan, not just the batch subset.
- Preserve capitalization and source typos in raw headings. Case and hyphen differences may be compared without rewriting text. Any lexical ordinal typo needs a narrowly scoped, flagged inference supported by the Arabic heading and numeric app date, not a general fuzzy-match bypass.

Current-reference text and screenshot extraction is a public rendered-UI workflow. Do not dump full iframe srcdoc scripts or browser storage; only reading text and necessary context are evidence. Avoid simultaneous browser-harness navigation by multiple workers; use one owner or genuinely isolated Playwright/browser instances.
