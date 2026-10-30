# Timothy and Luke evidence follow-up, 1.3.8 candidate

## Outcome and scope

Implemented NEW `evidence_followup_repairs.py` and its tests, plus this review directory only. Shared builders, root documentation, other workers' modules and generated package outputs were not edited. No npm, site, commit, push, fresh external retrieval or release operation was performed.

The oracle is authenticated published `@andraws/lectionary-data@1.3.7`, not mutable candidate output. All 11 baseline member hashes match `baseline/authentication.json`. Its reverse SHA256 is `4b785a5c626eaf4809f74738bfb3be05d7c8d0ae095b51bf98e72cad55559bf9`. `baseline-targets.json` freezes literal predecessor rows and exact retained source contexts; its pinned hash is `de51c94fa1c988a1d5e40f5ef2b8f4cebb84de5051dd05fa3031d978f1e14bbe`.

Read-only projection over all 12,330 published reverse rows leaves 12,330 rows. Exactly **49 rows change**: 45 evidence metadata rows and four separate Psalm annotations. No current status, removal marker, source title, locator, edition, raw calendar key, occurrence ID, appointed selection or numeric source coordinate changes. First projection and idempotent replay both passed.

## T-L6: reproduced, retained captures qualify all 12 occurrences

- **Pre-sanctified Chrism:** `rid_5fc19001c7a8830daa5a`, 1 Timothy 2:11-3:7, `myron_consecration / consecrations_oil_pre_sanctified_chrism / third_liturgy_liturgy_of_the_word`. Source navigation explicitly names **Pre-sanctified Chrism**. It is not relabeled as every Myron service. Retained heading is line 810 in `aba4ce45-7734-4586-910e-d72d7575a879-4.txt`, SHA256 `c1e9685173143193db89e0ad82b740666e5b868de151d5525fcbf65feeeb28a2`.
- **Reception of New Priest:** 1 Timothy 5:17-6:2 `rid_e475dd1bbf8b05b45910` and John 1:1-17 `rid_ab056b3f3f04f22996b0`. Same retained document, lines 640 and 880, SHA256 `7e04a9c9babe3ae8d19badd4c060ac5cdef027b01536fc75a023969423901d30`.
- **Funeral of Deacons:** eight occurrences, six Psalm fragments plus 1 Corinthians 15:23-38 and John 12:20-26. The exact Reader document and existing retained Psalm normalization records support their distinct labels and covering MT loci. They are not inferred from a general funeral label.
- **Covenant Thursday Lakkan:** undated 1 Timothy 4:9-5:10 `rid_5cd67675f32c75db9167`. The selected Special/Lakkan/Covenant Thursday document and selected Pascha/Thursday/Thursday Day/Liturgy of the Waters document have the identical service title **The Liturgy of Blessing of the Water of Great Thursday** and identical complete Pauline body. Both full-document hashes, paths, heading lines, the exact body hash and qualified contract are carried in the added evidence. **One same-service metadata marker, no deletion.** The undated index has different coverage from the dated complete table, including named Exodus/Joshua excerpts, so entire-table equality is explicitly false.

The later specific instruction to use qualified retained Reader evidence governs: these 12 rows are not falsely reported as uncaptured service books. All receive retained evidence and `current_authority`, with current statuses unchanged.

## LK7: reproduced, source-qualified treatment

The 33 listed Luke occurrences divide into **22 captured Special rows** and **11 printed-book rows**. Together with T-L6, 34 rows receive `current_authority`, the established Reader tier in the design source rules. These have 35 capture attestations across 23 documents because the combined monk-priest / monk occurrence retains both contexts.

Qualification checks the pinned manifest and records, actual full-document SHA256, selected record, exact navigation, heading, line, section, source context and target occurrence. Oil of Gladness also authenticates the assigned-reading classification verdict and its actual rubric lines; its original unclassified record is not silently taken as sufficient. Evidence is portable and repeated inside `source_disclosure`. No current-status promotion occurs.

**11 printed rows remain `working_local_source` and receive `unverified_service_book`:** five Agpeya Luke Gospels and six Palm Sunday procession Luke Gospels. The named editions are Fr. Jacob Nadian's Saint Bishoy Agpeya book and Palm Sunday procession/general funeral book; revision/date was not established. Retained local PDF hashes are:

- `web_special_service_sources/agpeya_book.pdf`: `653617a2011348ff9a14fc9cce94ce481bcc94dfa27f498cea341b66292b8b3f`.
- `web_special_service_sources/palm_sunday_procession.pdf`: `9ab41765a004fd4ad4aa86faf93271fcb7ac78b07b25ce498fec07b04eb12b1d`.

Their printed source is not converted into Reader provenance from passage resemblance. The check-sheet fragment lists each exact identity, hour/station, reference, edition and original locator. This is a scoped acceptance limit, not an assertion of capture absence across all repository evidence.

## LK9: reproduced, four annotations corrected

Recomputed every Psalm row through frame-qualified handling, not a global MT-to-LXX equality rule. Of 5,054 Psalm rows, 5,017 have declared MT coordinates that agree with their parsed coordinate frame. Thirty-one source-only/held rows and six non-MT/held-frame rows remain unchanged. No numeric frame mismatch was found in the authenticated baseline.

The generic current helper `build_design_deliverables.psalm_lxx_ref` intentionally returns a chapter-only, medium-confidence proposal for Psalm 51. Its output alone does **not** establish superscription offsets. The authenticated Covenant Thursday source contract and retained Brenton/NKJV Bible witnesses qualify the covering loci MT 51:7 -> LXX 50:9 and MT 51:10 -> LXX 50:12. Only those supported mappings supplement the existing converter. This is not a new +2 rule for other Psalms, source labels or editions.

Exact changes:

| Source context | MT | Before LXX | After LXX |
|---|---|---|---|
| Katameros cycle, `week 6 day_of_week 6`, `vespers_psalm` | Ps 51:10 | Ps 50:10 | Ps 50:12 |
| copticchurch, Saturday of sixth week of Holy Fifty, Vespers | Ps 51:10 | Ps 50:10 | Ps 50:12 |
| Waters, `apostles_feast_laqan || lakkan_covenant_thursday`, main readings | Ps 51:10 | Ps 50:10 | Ps 50:12 |
| Same combined raw Waters context | Ps 51:7 | Ps 50:7 | Ps 50:9 |

The source-owned Great Thursday Liturgy annotation MT Ps 41:9 / LXX Ps 40:10 is preserved. The generic proposal Ps 40:9 is less qualified, not a reason to overwrite it. That is one `qualified_mapping_preserved`, not an unresolved source conflict. The final baseline has zero unresolved disagreements under these rules. Unknown future medium-confidence disagreements are held report-only, without supplying offsets, changing status or overwriting source coordinates.

Read-only daily projection changes one annotation in each year: **2026-05-23, 2027-06-12, 2028-05-27**. Counts remain **4088 / 4079 / 4096**, respectively. These are this module's isolated deltas, not predictions of combined pending 1.3.8 totals. No daily or reverse output file was regenerated.

## Tests and controls

Targeted tests exercise exact membership, idempotency, immutable source fields, disclosure preservation, hash tampering through the actual repair caller, wrong family/kind/service/slot/reference, inactive and malformed lifecycle flags, copied evidence, missing emitted evidence, Lakkan's authenticated same-service relation, source-coordinate versus MT coordinates, held/source-only exceptions, qualified Psalm superscriptions and unresolved proposals.

RED proof was observed for three equivalent targeted mutants: disabled evidence transformation, removed hash verification and dropped Psalm superscription qualification. Each produced one intended assertion failure; all three mutants were killed. An initial preimplementation collection also failed for the absent new module, but that setup failure is not the behavioral RED claim. The final new test inventory has 16 tests. The final targeted-plus-surrounding command passed **41 tests and 205 subtests**, exit 0, in 53.25 seconds. `git diff --check` also returned exit 0. No em dash or trailing-space prose was found in the new Python or Markdown files.

A surrounding diagnostic command ran only the new tests and existing Covenant Thursday source/projection plus Special context tests, not the full release pipeline:

```sh
uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate --with pytest python -m pytest tests/test_evidence_followup_repairs.py tests/test_covenant_thursday_source_supplements.py tests/test_covenant_thursday_projection_integration.py tests/test_special_context_projection.py -q
```

A read-only probe of finished Mark guards found zero intersections with the 49 changed rows, zero `qualify_emitted` recognitions/refusals among them, and no intersection between LK9's three daily dates and Mark's 36 authenticated complete-date groups. The six Mark L7 rows remain untouched. No compatibility adapter or weakened guard is needed for that frozen contract.

## Limits and integration

System Python lacked `convertdate`; the established uv Python 3.11 environment resolved the import and executed real tests. No other functional blocker was found. Source qualification is retained evidence, not fresh app verification, recurring-use approval, release approval or current-status activation. Q-LK3 remains unanswered.

See `README.fragment.md` for APIs, output fields and dependency copying. Parent must wire the hooks and final emitted-row validation, then freeze all writers before complete package and release acceptance. Generic historical validators should see their authenticated internal view where necessary, while the emitted evidence is separately validated. Do not refresh candidate rows into the predecessor oracle. Root README/T-L5 and shared builder/validator work remain parent-owned.
