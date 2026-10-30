# Changelog

## 1.3.8

Bounded follow-up against authenticated published 1.3.7. No printed witness is promoted, no Synaxarium entry or raw source field is changed.

- **L1:** Hold the malformed Mesra 7 dated Vespers Mark 14:39 witness. The saved heading is `Mk 14:-39` with whole-chapter text, not evidence for a silent repair to 3-9. Preserve the separate cycle witness.
- **L2:** Hold exactly four Tuesday day-hour Gospels and the two Third Hour prophecies; preserve Monday and Tuesday Sixth Hour. Document all five Tuesday hours and the retained Reader Third Hour conflict without adding replacements.
- **L3:** Add four inactive printed Third/Ninth Hour candidates alongside unchanged historical witnesses. Account explicitly for all five hours of every Pascha eve, with Reader gaps distinguished from current hours. Record the actual printed Eleventh Hour without activating it.
- **L4:** Normalize every Pascha display label using source-qualified Coptic eve identities; unify Palm/Hosanna and both Bright Saturday families while preserving raw labels and civil dates.
- **L5:** Normalize 30 Kiyank display labels and 19 Ninevah display labels to Kiahk and Nineveh. The source retains 60 Kiyank tokens in 30 records.
- **L6:** Flag both Hator 11 Vespers Gospel witnesses as conflicting, without selecting either or linking readings to commemorations. Keep Q-L1 unanswered.
- **L7:** Add the requested `unverified_service_book` evidence annotation to six undated appointments, retaining their existing saved Reader evidence and statuses. Document the inactive printed Myron Mark 16 lead as chapter 16 entirely.
- **L8:** Preserve Tout 23 readings unchanged. Add the Marian-day-set question to the check sheet and leave Q-L2 unanswered.
- **L9:** Exclude exactly three stale unresolved Wednesday Pascha Psalm occurrences per year, preserving their status in the reverse archive. Keep all accepted source-only and numeric-source-coordinate Psalm holds current under exact date/source/disclosure allowances. The public current-reading predicate is unchanged.
- **L10:** Supply all 21 requested service/hour source comparisons, including historical, printed and retained Reader wordings, without a new current-status sweep.

### 1 Timothy follow-up

- **T-L1:** Every removed witness explicitly reports `occurs_in_shipped_years: false`. Correct 2,326 true claims and add the previously missing false field where needed, without deleting historical evidence.
- **T-L2:** Use the exact Twenty-Four Presbyters Synaxarium title in normalized Hatour 24 display metadata, with date-only catalog co-display and unchanged raw source titles.
- **T-L3:** Qualify all 1,090 bare seasonal-cycle views by season and normalized calendar key. Current single-key rows comprise 156 Great Lent and 64 Holy Fifty views; a two-key Holy Fifty view is disclosed separately.
- **T-L4:** Normalize month spellings using the later LK2 recommendation, including Hatour rather than the earlier Hator recommendation. Preserve raw keys.
- **T-L5:** Document the distinct guaranteed reverse-index and daily-row schemas. `day_titles` remains optional in daily rows rather than receiving a fabricated value.
- **T-L6:** Attach authenticated retained evidence to the requested rite occurrences and preserve their actual service names. Identify the same Covenant Thursday Lakkan Pauline without deleting a witness or claiming whole-table equality. Captured evidence is not falsely described as absent.
- **T-L7:** Add exactly seven low-priority confirmation appointments. Preserve six real copticchurch locators and the already Reader-backed Water Liturgy locator rather than inventing a seventh copticchurch source.

### Luke follow-up

- **LK1:** Flag both three-Gospel Abib 26 source tables. Choose neither and preserve the existing daily appointments.
- **LK2:** Normalize reader-facing month names to the thirteen catalog spellings and annual-Sunday capitalization, without rewriting source labels. Q-LK2 remains unanswered; its recommended default is used.
- **LK3:** Replace generic cycle headings with source-qualified weekdays, weeks and actual feast names. Disclose the two inactive unresolved source-week-49 witnesses instead of inventing liturgical weeks.
- **LK4:** Preserve endpoint variants and add a report-only inventory of 31 current comparison groups across 365 retained dated slots. Tout 8's longer Katameros witness is already inactive.
- **LK5:** Merge all 52 remaining authenticated inactive source-cell pairs into ordered composite appointments. Retain all 104 original witnesses and their retirement metadata in the fragment records.
- **LK6:** Keep public provenance plain text, at most 300 characters, and move structured evidence to explicit reversible JSON cells. Public fragment records use `original_source_row`; no `_review_original_row` token remains in daily output. Decoding does not replace source authentication.
- **LK7:** Qualify 34 captured Special occurrences with portable Reader evidence and the established authority tier. Keep 11 Agpeya/Palm printed-book occurrences unverified, with named editions and check-sheet entries. Existing statuses remain unchanged.
- **LK8:** Empty 145 synthetic Pascha overlay attestation triples rather than inventing a full range of attestations. Preserve their former synthetic years separately and retain genuine source observations and disclosures. No status changes.
- **LK9:** Correct four source-qualified MT-to-LXX annotation views. Preserve held/non-MT coordinates and authenticated edition exceptions rather than applying a blanket offset.

See [full report and tables](docs/LECTIONARY_1_3_8_RELEASE.md), [Reader check sheet](coptic-reader-check-sheet.md) and [open questions](open_questions_for_george.md). Dirty candidate provenance remains truthful during integration. The final package must be rebuilt from the single committed source in a fresh clean checkout before any publication.

## 1.3.7

Source-backed corrections to the authenticated published 1.3.6 baseline. This release does not update the consuming website or the Synaxarium catalog.

### Holy Week

- **H1:** Remove the copied current Tuesday-night appointments from daily output and retain them as explicit inactive Reader-review holds. Add the authenticated First and Sixth Hour selections; leave uncaptured hours on the check sheet.
- **H2:** Add the authenticated Third and Eleventh Hours of the Eve of Monday on Palm Sunday's civil evening. Other hours remain source-recovery gaps.
- **H3:** Add explicit Pascha service and civil-evening metadata without changing raw source labels.
- **H4:** Hold the Good Friday Sixth Hour John 19:1-12 copy and supply the authenticated John 19:13-27 appointment, with source-defined Gospel order.
- **H5:** Flag, but do not delete, the Great Thursday Third/Ninth Hour Matthew 26:17-19 repetition. Third Hour remains to check.
- **H6:** Hold the Jeremiah 43:5-11 book-code witness and add Reader's Ezekiel 43:5-11 for the Eve of Thursday First Hour.
- **H7:** Preserve Galatians 3:1-6 as historical: the retained complete Reader Eleventh Hour has no Pauline. Confirm the Sixth Hour Galatians 6:14-18 witness; retain the Isaiah 19 question.
- **H8:** Qualify 53 existing non-Psalm appointments from retained Reader evidence and hold the 17 identified erroneous appointments. The remaining 177 working appointments are not represented as newly verified.

### Calendar keys and labels

- **K1-K3:** Add source-qualified fixed Coptic date keys and separate annual-Sunday ordinals. Join only by date to the unchanged catalog; no reading-to-saint fields are added.
- **K4:** Remove the Entry-into-Egypt collision suffix only from the display label.
- **K5:** Recover dates for the actual generic ordinary-source cohorts. Preserve movable Nineveh contexts and inactive no-service witnesses instead of inventing fixed dates.
- **K6:** Normalize reader-facing Theophany and Nativity Fast terminology while retaining original source labels.

### Resolver and reading model

- **R1:** Project the source-qualified Last Friday of Great Lent Matins Gospel, Luke 16:19-31, in place of the conflicting ordinary-source reference.
- **R2:** Use the complete authenticated nine-selection weekday Kiahk 23 table. Matins is Matthew 12:1-8. Exclude Sunday and overriding-occasion contexts. Preserve prior witnesses inactive. Keep three printed Psalm selections source-only, without inferred canonical coordinates. Fresh Reader Matins on Sunday January 2, 2028 is Mark 3:28-35.
- **R3:** Add actual shipped-year occurrence metadata and descriptive seasonal-overlap metadata across the disclosed full computus cycle. These fields are not a feast-precedence rule or a universal absence claim.
- **R4:** Combine the reviewed same-source chapter fragments into one ordered appointment, retaining every fragment and locator in the disclosure.
- **R5:** Record the Amshir 10 catalog question on the check sheet. No Synaxarium title is invented or added.
- **R6:** Identify the Bel selection in Reader Daniel 14 source coordinates. Do not assert unverified Brenton or MT equivalence.
- **R7:** Introduce this changelog and a release report with exact-artifact acceptance requirements.

### Study feedback

- **C1-C2:** The reported wording is absent from the current named canonical guides, so no edits apply.
- **C3:** Preserve the already-qualified 2 Timothy Overview line. Seasonal overlap alone is not authenticated evidence for deleting the annual assignment.

See [release scope and limitations](docs/LECTIONARY_1_3_7_RELEASE.md) and [Reader checks](coptic-reader-check-sheet.md). Source evidence, tests and held questions remain separate from release acceptance. Earlier npm artifacts are immutable.
