# Covenant Thursday bounded retained-source supplement

## Scope and status

This new source pack qualifies **retained** complete Coptic Reader documents for
Great Thursday's Liturgy of the Word and Liturgy of Blessing of the Water only.
The selected civil date was **2026-04-09**, occasion **Covenant Thursday**. No fresh
app inspection or retrieval occurred. Current qualification is
`source_qualified_retained_within_bounded_scope`, not a fresh-current-app claim.

The package-first exception is the authenticated `@andraws/lectionary-data@1.3.5`
audit finding: missing Word group and Genesis-only Waters projection on
2026-04-09, 2027-04-29 and 2028-04-13. Those dates are package gap findings, not
three independent primary captures. The current user's bounded authorization is
retained separately in `bounded-user-authorization.json` and
`sources/user-corrections/covenant-thursday-2026-10-25.json`.

`old-review-receipt.json` is copied without alteration. Its `consumer_eligible`
and `release_approval` remain false and `runtime_contract_acceptance` remains
pending. It does not retrospectively authorize this new contract or activation.

## Appointment table

- Word: Pauline 1 Corinthians 11:23-34; one composite Psalm appointment printed
  `Psalms 22:5;40:9`; Gospel Matthew 26:20-29. Catholic, Praxis and Synaxarion are
  explicitly not read (complete Word document, line 77).
- Waters: Genesis 18:1-23; Proverbs 9:1-11; `Exodus from 14, 15`;
  `Joshua from 1, 3`; Isaiah 4:2-4; Isaiah 55:1-56:1; Ezekiel 36:25-29;
  Ezekiel 47:1-9; Pauline 1 Timothy 4:9-5:10; assigned Psalm printed
  `Psalms 51:7, 10`; Gospel John 13:1-17.
- Prescribed Psalm 50 and Psalm 150 prayers remain in the full Waters source
  text but are **not extra appointed lessons** in this helper.
- Exodus and Joshua are short, unversified named excerpts, **not whole chapters**.
  Preserve their literal headings and chapter hints without inventing verse spans,
  continuous chapter ranges or chapter-completeness claims.

## Edition-coordinate distinction

The literal Word Psalm body selects the table clause and bread/betrayal clause.
Its covering MT/NKJV coordinates are Ps 23:5 and Ps 41:9; Brenton's displayed
coordinates are Ps 22:5 and Ps 40:10. The first does not include the anointing/cup
clauses; the second does not include all the familiar-friend/trust opening.
The assigned Waters Psalm body selects hyssop/washing and clean-heart/renewal:
MT/NKJV Ps 51:7 and Ps 51:10; Brenton displayed Ps 50:9 and Ps 50:12.
These are selected-clause correspondences, **not full-verse or translation
identity**. The pinned retained normalization records and their complete Bible
witness files are separate from the complete Reader transcripts and original
printed references. Do not apply a flat minus-one Psalm conversion.

## Parent integration API

`load_covenant_thursday_rows() -> list[dict]` exports **16 raw crosswalk-shaped
string-valued rows**, comprising **14 appointments** (Word 3, Waters 11).
The two Psalm fragments share `source_file`, `source_row_id`, `source_order` and
`reading_slot`; only `source_token_order` and the coordinate fields differ.
Order is numeric, explicitly 1..3 / 1..11 within each service, with token order
1..2 for the two composite Psalms. `source_file` is repository-relative and names
the **complete portable Reader transcript**, not a derived fragment file.

`qualify_covenant_thursday_row(row)` must receive the original raw row before
presentation reshaping. It reauthenticates every evidence file and exact raw
field, returning fresh parsed provenance metadata or raising `ValueError`.
Metadata binds full capture and body hashes/literals, ordinals, printed and
normalized references, slot, selected date/navigation, edition witnesses and
current state. A path/family/kind alone is never qualifying evidence. No cache
or caller-controlled provenance is trusted.

Named Exodus/Joshua rows retain the literal heading in `passage` and have empty
`normalized_ref`, `normalized_segment`, chapter and verse coordinates. Metadata
contains `coordinate_status=verse_unaddressable_named_excerpt`, `book_hint`,
`chapter_hints`, `chapter_complete=false`, and an explicit disclosure. Parent
presentation must preserve these as named excerpts, not parse chapter hints into
spans or drop them for lack of a numeric passage identity.

`service_day` and `day_title` are exactly `Great Thursday`. Word section/hour are
`Liturgy`. Waters section/hour preserve the exact existing legacy CSV label
`Liturgy of Blessing of the Water`. Source family and kind are both
`coptic_reader_qualified_pascha_hour`; this does not itself activate rows.

No activation hook, global registry, historical ledger, generated output, package
or Git change is included. The parent owns structural annual recurrence at
Julian Pascha minus three days, integration, service replacement/retention policy,
materialization, release gates, and publication. The Thursday Sixth Hour
source-book dispute is explicitly outside this contract.

## Verification

RED: `python3 -m unittest discover -s tests -p test_covenant_thursday_source_supplements.py -v`
failed all five tests with `bounded Covenant Thursday helper is missing` before
production implementation. GREEN: the same command passed five tests, covering
the complete exact appointment table, named-excerpt no-span behavior, raw-field
and provenance forgeries, every evidence-file mutation and portable source-root
readback, full body/context authentication and historical nonapproval retention.
