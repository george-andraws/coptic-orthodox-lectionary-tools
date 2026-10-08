# Calendar-boundary integration report

## Outcome and scope

Implemented an upstream complete-table replacement for **Annunciation AND Last Friday (Pascha offset -9)**. The independently captured 2028-04-07 table restores four ordered Matins prophecies, the Matins Psalm/Gospel, all five Liturgy readings, and the explicit absence of Vespers. Raw source readings are copied, never edited or relabeled by the resolver.

The represented source calendar contains the same collision on **2023-04-07**. The recurring exact-context rule correctly changes both collision dates, retaining `verified_date=2028-04-07`; it does not invent a fresh 2023 capture. All **5,750 other represented dates** remain exactly equal to the byte-bound pre-task resolver baseline. This is preservation of the 5,752 dates actually represented by the cached source, not an assertion of complete civil-calendar coverage.

The prophecy context is explicitly separate in `verified-table.json` (`recurring_prophecy_context`, requires Annunciation collision). Existing generic `recurring_date_supplements` and their guards are untouched. No newly staged Lent supplement batch was integrated. Noncollision Last Fridays are intentionally unchanged.

## Evidence and Psalm handling

- Verified **18 original text/screenshot hashes** against original capture manifests **before fixture creation**. Verified civil date, Paremhotep 29, 1744, Last Friday of Great Fast, all seven document services, and ordered printed references. Reviewed the home/context, first Prophecy and no-Vespers screenshots visually.
- Exact source headings are preserved, including `Psalms 31:11-12` and `Psalms 97:8`.
- Retrieved and saved actual NKJV Psalm 32 and 98 text witnesses from Bible Gateway, with URL and SHA-256. Matins text aligns to **MT Psalm 32:10-11**, not printed verse numbers 11-12. Liturgy aligns to **MT Psalm 98:8b-9**; machine full-verse coverage is `Ps 98:8-9`, with explicit disclosure that verse 8a's rivers clause is not sung. No blanket chapter-plus-one or unchanged-verse normalization was used.
- Canonicalization notes/confidence and printed references survive the actual passage-index helper. No Psalm normalization blocker remains for these two verified excerpts.

## Verification

- `RED.log`: observed original wrong Annunciation table fail the independent complete-table regression (9 wrong rows versus 11 Last-Friday rows).
- `uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate python audit_artifacts/calendar-boundary-integration/verify_scoped.py`: **11 tests passed**, including the six new boundary tests and five existing source/supplement compatibility tests. Saved in `scoped-verification.log`.
- Corruption coverage: omitted, reordered, truncated, duplicate, wrong date/occasion/service/offset, wrong suppression and source-hash drift; fixture mutations update the outer fixture hash to prove semantic guards, not merely checksum detection. Mixed/overlapping seasonal and feast inputs fail closed.
- Actual `build_current_date_sidecars()` exercised on isolated TEMP copies of six canary dates. 2026-04-07 retains **38 corrected Pascha source rows**; 2027-04-07 retains **9 Annunciation rows**; 2028-04-07 yields **11 exact Last-Friday rows**. No parent builder was run.
- Full in-memory resolver comparison: **50,564 → 50,568** rows, only 2023-04-07 and 2028-04-07 changed, **9 → 11** each. Saved before/after tables and `ledger.json`.
- Compiled all three owned Python files successfully; scoped `git diff --check` passed.

The initial trial used the uncorrected Pascha source fragments (42 rows). This was a test-layer mismatch, not a changed calendar result: the preserved actual helper applies the existing continuous-reference corrections and returns 38. The test now follows that real helper path.

## Changed files

- `calendar_resolution.py`: source-bound whole-table overlay, complete evidence and semantic guards, exact source order, no generic season-window extrapolation.
- `build_lectionary_reference.py`: preserve boundary-specific Psalm normalization metadata through the passage helper.
- `sources/lectionary_corrections.json`: separate `calendar_boundary_tables` rule and bound fixture hash; existing supplement data unchanged.
- `tests/test_lent_annunciation_boundary.py`: independent complete oracle, recurrence/idempotency, canaries and corruption tests.
- `sources/coptic-reader/last-friday-2028-04-07-2026-10-07/`: 23 fixture/provenance files.
- `audit_artifacts/calendar-boundary-integration/`: logs, exact reconstructed pre-task resolver validated against its recorded hash, capture verification, isolated-helper output, ledger, source hash manifests and this report.

## Parent integration gates remain held

No generated production files, design/site builders or tests, npm installs/packs/publication, deployment, vault files or commits were performed. This is an upstream source/calendar result, **not a completed package/site release**.

Parent must serialize the later supplement merge, recognize `Coptic Reader verified calendar boundary` / `source_boundary_overlay` as ordinary source-backed provenance (not Pascha or the Wednesday-only supplement source), preserve the two displaced Annunciation contexts as qualified superseded raw history, transport OT1–OT4 order and Psalm excerpt notes, and run the complete pipeline/release gates. The broader UK Midlands exception-window table remains unimplemented outside verified contexts.

## Final source hashes

Bound exact final source/fixture bytes are recorded in `final-hashes.json` (self-excluded):

- `calendar_resolution.py`: `bcbd7229527491d1b043193d5dd34bca7e599eb27b0fb579cff20ff62c383417`
- `build_lectionary_reference.py`: `105c7f2b2fa49e9ea2f97da56e1e779ca44a6360865be3572d5f344b05b88443`
- `sources/lectionary_corrections.json`: `92cb0edf28179fefeef8fd88e851adbd9ddfe4be1fcef375766c0a131193b9ed`
- `tests/test_lent_annunciation_boundary.py`: `146c6856b5e8fe1302330b6c2506feb2a26bdfdf584440727d0bdc193f657681`
- `verified-table.json`: `f3b3bffbf99bf1a972f5c1abc2b2a4e7504774ae67a8111e1d9358011cd8deb4`
