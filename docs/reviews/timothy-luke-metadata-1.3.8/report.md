# Timothy and Luke metadata review, 1.3.8

## Scope and baseline

This fragment covers T-L1, T-L2, T-L3, T-L4, T-L7 and LK1, LK2, LK3, LK4, LK8 only. It does not own the shared builder, existing release membership contract, root release documents, T-L5, composite repairs, special-service evidence repairs or Psalm annotations.

The parent froze npm latest at authenticated published 1.3.7. Before any implementation edit, this worker verified the registry SHA-512 integrity of the retained tarball and all 11 extracted file hashes from `authentication.json`. The source fixture retains those exact authentication values. It is not a candidate oracle or a refreshed whole-corpus membership policy.

- Reverse index: 12,330 rows before and after this metadata layer.
- This layer changes metadata on 6,409 rows, never membership, reading coordinates, source titles, source locators, raw calendar keys, source disclosures, inactive history or lifecycle status.
- Complete exact source-qualified row identities, baseline physical line and field deltas are in `source-qualified-row-deltas.json.gz`. Its SHA-256 is `2099463b22b5079f0197f2f647a8285ada00b55f0316d1da9aca3ad8dd39d73d`.
- `scope.json` contains source authentication, scope counts, named identities and seven confirmation appointments. `endpoint-conflicts.json` contains every reported exact date, service, slot, reference and witness locator.

## Findings and disposition

| ID | Reproduced | Disposition and exact scope |
|---|---|---|
| T-L1 | Yes | Every row with a nonempty removal marker now explicitly reports `occurs_in_shipped_years: false`. Of 4,509 removed witnesses, 2,326 reported true, 1,256 already reported false and 927 had no field. There are 3,253 field changes, zero true claims afterward. No status is changed. |
| T-L2 | Yes | 25 Hatour 24 metadata views receive the catalog's exact title, `The Commemoration of the Twenty-Four Presbyters`, in the display label and a date-only commemoration title list. All three catalog titles are retained in catalog order. The raw source label stays intact. This joins a calendar date to a catalog, not a reading to a saint or a reason for its selection. Split reading history is untouched. |
| T-L3 | Yes | All 1,090 rows containing bare cycle keys receive source-qualified `normalized_season` and `normalized_calendar_keys`. The cited 220 current single-key rows are 156 Great Lent and 64 Holy Fifty. One further current Holy Fifty row collapses two raw keys and is counted separately. Raw keys remain unchanged. |
| T-L4 | Yes | K1 already supplies fixed-date and Sunday keys, but K6 had not unified month spellings. Normalized display labels now use the LK2 recommendation. Hatour, from the later Luke prompt, supersedes the earlier Hator recommendation. |
| T-L7 | Yes, with one source correction | Exactly seven low-priority `confirm, no change expected` appointments are listed in the check-sheet fragment. Six have actual copticchurch.net locators. Great Thursday's Water Liturgy already uses retained Reader evidence in 1.3.7 and has no copticchurch.net witness in that package's reverse or daily arrays. Its actual selected-date, body-hash and line locator is preserved rather than fabricating a copticchurch URL. No status promotion occurs. |
| LK1 | Yes | Both Abib 26 three-Gospel sets are flagged, six reverse rows total. Neither set is selected or held. The three already shipped copticchurch Gospels remain in 2027-08-02, with flags only. The Synaxarium's commemoration names establish date co-display, not reading-selection intent. |
| LK2 | Yes | 5,478 reverse display labels change across this combined normalization, including cycle labels and Hatour 24 labels. Each month token uses Tout, Baba, Hatour, Kiahk, Toba, Amshir, Baramhat, Baramouda, Bashans, Paona, Abib, Mesra or Nasie. Annual Sundays derive their month and ordinal from the authenticated normalized Sunday key. Initial `The fourth Sunday of` becomes `Fourth Sunday of`. Q-LK2 remains unanswered; the explicit recommended spelling is used. |
| LK3 | Yes | All 592 Great Lent family and 498 Holy Fifty family views gain usable labels. Feasts and preparation sentinels are named rather than interpreted as ordinary numeric weeks. Two already inactive Exodus witnesses under source week 49 remain unresolved and explicitly say so. There is no invented forty-ninth liturgical week, no new hold and no activation. |
| LK4 | Yes, with an inactive-witness correction | Both named endpoint pairs are flagged, four reverse witnesses. Tout 8's Katameros Matthew 23:13-36 witness is already inactive in authenticated 1.3.7. It is preserved and is not falsely counted as a second current appointment. The report-only current comparison identifies 31 context/service/slot/start groups, 365 exact dated groups and 365 distinct dated slots. No endpoints change. |
| LK8 | Yes | Exactly 145 generated Holy Week overlay views have empty `attestation_years`, `attestation_year_min` and `attestation_year_max`. Their former synthetic year is explicitly labeled `synthetic_overlay_years`, not promoted into a full shipped range. Genuine dated observations, retained selected dates and source disclosures remain unchanged. No status changes. |

The prompt's 507 occurrence claims and 705 bare month-key copies are not repeated as measured totals. The authenticated 1.3.7 artifact has 3,919 canonical-occurrence supersessions, 2,275 with true occurrence claims. A literal `Month 1-5` selector across those supersessions yields 806 views, 576 true, including actual fixed-day views as well as Sunday copies. The repair applies the broader, explicit requested removal-marker rule and reports its exact 4,509-row population separately.

### Named identity checks

- T-L1: `rid_1cb21a9e546625f8b503`, raw `Tut 1`, 1 Timothy 1:12-19; `rid_2ba106e64365ef933085`, raw `Babah 4`, 1 Timothy 6:3-21; `rid_62f86c38e99a8b80724a`, raw `Abib 3`, 1 Timothy 6:3-16. Each stays superseded and now explicitly does not occur.
- T-L3: source `week 6 day_of_week 4`, `rid_539d72ebd85c4b03eaf1`, becomes Thursday of the sixth week of Great Lent; the same raw key with `rid_f7ab1aa9ada78662622d` becomes Feast of the Ascension in `holy_fifty`. These are distinct normalized contexts, not one day.
- LK1 copticchurch: Liturgy `rid_84ed6fb31aac63feec5f`, Matthew 23:13-26; Matins `rid_90f9856d0b9722750c38`, Matthew 17:1-9; Vespers `rid_875283c8a2bfb534d4ab`, Luke 11:37-51.
- LK1 Katameros: Liturgy `rid_9b9fb26c186e72003e9c`, Matthew 2:13-23; Matins `rid_37424e94554789b41fc3`, Matthew 12:15-23; Vespers `rid_d2857a5170e70b6bb682`, Matthew 4:12-17.
- All named LK4, T-L7 and unresolved week-49 source-qualified identities and locators are in `scope.json` and the check-sheet fragment.

## Weekday and sentinel evidence

The retained Katameros source implementation `Core/Repositories/ReadingsRepository.cs`, lines 23-41, queries the database using `System.DateTime.DayOfWeek` cast to integer. This is Sunday zero, not Python's Monday-zero convention. The hash-pinned source passage table independently corroborates Sunday zero at Palm Sunday and Thursday four at the Ascension. Source weeks 99/0 and 99/6 name Preparation Sunday and Saturday; Holy Fifty week 0/day 0 names the Resurrection. Palm Sunday, Lazarus Saturday, Thomas Sunday, the Ascension and Pentecost use feast labels.

The source's Holy Fifty week 7/day 1 contains an old Entrance into Egypt name. K4 already rejected treating that movable cycle day as the fixed feast. This layer retains the ordinary Holy Fifty weekday label instead of reintroducing the old collision defect.

Some published source locators retain ordinals from an earlier source projection. Their literal bytes are authenticated against the published fixture. Source-table corroboration joins table, raw key and slot rather than applying that old ordinal to a different CSV. No locator is rewritten.

## LK4 counting contract

This is a report-only inventory of different-source current appointments with the same normalized context, service, hour, slot type, book and canonical MT start but different canonical MT endpoints. A group is counted once rather than once per pair. Only single-span, usable canonical MT selections are compared. Source-only unresolved-coordinate rows, inactive history and multi-span composites are not misrepresented as endpoint differences. No LXX source-frame numeric fields are treated as canonical MT coordinates.

Exact dates come from retained copticchurch locators across the 2020-2035 source cache. These are observed source-date pointers, not inferred recurrence and not new Reader attestations. A retained date list is not a promise that both source witnesses shipped together on that day. The full report includes Fourth Sunday of Mesra Vespers for all 16 retained source years. Tout 8's inactive witness is separately disclosed and preserved.

## Daily results and acceptance limits

| Year | Published 1.3.7 reading rows | Metadata-only result | Metadata rows changed | Mark then metadata result |
|---|---:|---:|---:|---:|
| 2026 | 4,088 | 4,088 | 950 | 4,078 |
| 2027 | 4,079 | 4,079 | 893 | 4,069 |
| 2028 | 4,096 | 4,096 | 949 | 4,087 |

The metadata-only 2027-08-02 service retains all 11 readings, the same physical order, references, statuses and source cells. Its three copticchurch Gospel rows gain LK1 flags. Metadata does not turn the alternative Katameros table into that date's daily table.

The combined Mark then metadata reverse result has 12,334 rows, matching Mark's four retained review candidates and adding no metadata appointments. Tests prove exact metadata inversion back to every Mark daily array, then invoke Mark's unchanged complete-table comparator and source qualifiers. Deletion, addition, reordering, endpoint and lifecycle corruption still fail Mark's exact guard. Metadata restoration does not rewrite the independent Mark oracle from a new candidate.

These are module and bounded caller results, not a full candidate build, npm tarball acceptance, clean-checkout acceptance, publication or site acceptance. The parent owns all integration hooks and final combined acceptance after writers freeze.

## Verification

- System `python3 -m pytest` was unavailable because that interpreter lacks pytest. No test expectation was changed for that environment issue. Execution used `uv run --python 3.11 --with pytest python -m pytest`.
- Initial RED: `tests/test_metadata_followup_repairs.py -k removed_rows_never_claim_occurrence` failed on the real removed-row occurrence assertion against a no-op implementation. One earlier harness attempt incorrectly used Mark's bounded fixture, not the full predecessor; that fixture-selection error was corrected before the meaningful RED run.
- GREEN: `uv run --python 3.11 --with pytest python -m pytest -q tests/test_metadata_followup_repairs.py tests/test_metadata_followup_controls.py tests/test_metadata_followup_restoration.py --tb=short --maxfail=2`: 42 passed, exit 0, 125.03 seconds.
- A process-local mutation disabling `repair_rows` killed all five selected behavior controls: removal occurrence, seasonal key qualification, month/title normalization, generated attestation fields and LK1 flags. The disabled function was confined to that process and no source file was changed.
- `python3 scripts/report_metadata_followup.py` executed the complete predecessor metadata projection, whole-row checks and endpoint inventory and emitted the report fragments.

No shared existing file, generated package output, commit, npm publication, push or site operation is owned or performed by this worker.
