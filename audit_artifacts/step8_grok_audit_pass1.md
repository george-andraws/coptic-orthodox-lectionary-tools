# Step 8 Grok Audit Pass 1

## Summary
- I inspected only `/Users/georgeandraws/workspace/coptic-lectionary-research`.
- I did not edit, commit, or push.
- I verified the repo state, reviewed the Step 2 through Step 7 changed artifacts, ran the verifier, inspected generated CSV/JSON outputs, and checked consistency against the acceptance criteria.
- Main concerns:
  - The repo-scoped `05-LECTIONARY-DESIGN.md` file is absent, so I could not directly audit against the locked decision source requested in the prompt.
  - The Step 7 bridge upgrade is correctly reflected in data and site spec, but stale prose remains in the article and internal spec saying the bridge is uniformly `collection-type` / `medium`.
  - The schema/spec under-document actual emitted columns for some outputs, especially `synaxarium_reading_bridge` and `passage_source_disclosure`.
  - The verifier passes, but it does not catch those documentation/schema drift issues.

## Required revisions

1. Severity: blocker  
   Location: repo root, missing file `05-LECTIONARY-DESIGN.md`; execution log line 122  
   Finding: The requested locked decision file is not present in the repo.  
   Evidence: `read_file` returned “File not found” for `/Users/georgeandraws/workspace/coptic-lectionary-research/05-LECTIONARY-DESIGN.md`. The execution log says the repo copy was absent and George supplied `/Users/georgeandraws/.hermes/webui/attachments/ec88b422f574/05-LECTIONARY-DESIGN-2-1.md` as a substitute. That substitute is outside the repo, and this audit was explicitly repo-only.  
   Suggested revision: Add the locked design brief, or a tracked repo-local copy/reference of the locked decisions, to this repo. At minimum, add a tracked `05-LECTIONARY-DESIGN.md` or `audit_artifacts/locked_design_brief_reference.md` containing the exact locked decisions used for Steps 2 through 7. Without that, future repo-only audits cannot independently verify criterion 1.

2. Severity: required  
   Location: `coptic-lectionary-and-synaxarium.md` lines 102-107 and 141-142; generator source `build_design_deliverables.py` lines 1529-1531 and 1566-1567  
   Finding: The article’s Synaxarium bridge prose is stale after Step 7. It still says the bridge links fixed Coptic days with `collection-type` basis and `medium` confidence, which contradicts the generated Step 7 data where 789 rows are now `basis=explicit` and `confidence=high`.  
   Evidence:
   - Article line 106: “the Synaxarium bridge ... with `collection-type` basis and `medium` confidence.”
   - Article line 142: “The bridge is medium-confidence collection-type evidence...”
   - Actual data check: `synaxarium_reading_bridge.csv` distribution is `explicit: 789`, `collection-type: 3899`; confidence `high: 789`, `medium: 3899`.
   Suggested revision: Update article prose to say:
   - Days enumerated in the Ottawa/UKMID 69 foundational-reading collection are marked `basis=explicit` and `confidence=high` for the source-row bridge.
   - Outside those 69 days, bridge rows remain `basis=collection-type` and `confidence=medium`.
   - Even explicit 69 rows are not direct proof that each reading is a proper reading for every named commemoration.

3. Severity: required  
   Location: `lectionary_spec.md` lines 215-226; generator source `build_design_deliverables.py` lines 1787-1793  
   Finding: The internal spec’s Synaxarium bridge section is stale and incomplete. It says the bridge uses `collection-type` basis for primary day commemorations, but Step 7 upgraded the 69-covered rows to explicit/high. It also omits emitted columns such as `coptic_day_key`, `commemoration_title`, `commemoration_type`, `display_ref`, and `note`.  
   Evidence:
   - `lectionary_spec.md` line 226: “The bridge uses `collection-type` basis...”
   - Actual CSV header: `commem_id,coptic_day_key,commemoration_title,commemoration_type,reading_identity_key,display_ref,slot,basis,confidence,citation,note`.
   Suggested revision: Replace the bridge field list with the actual emitted columns and revise the prose to match Step 7:
   - 69-covered days: `explicit` / `high`
   - outside 69: `collection-type` / `medium`
   - repeated groups are catalog rows, not resolved daily service schedules.

4. Severity: required  
   Location: `out/design/lectionary_schema.json` lines 1574-1580 and 1592-1606  
   Finding: The schema table definitions are not complete representations of emitted outputs. The verifier only checks a subset, so the mismatch passes.  
   Evidence:
   - Schema `synaxarium_reading_bridge` lists only `commem_id`, `reading_identity_key`, `slot`, `basis`, `confidence`, `citation`.
   - Actual `synaxarium_reading_bridge.csv` includes `coptic_day_key`, `commemoration_title`, `commemoration_type`, `display_ref`, and `note`.
   - Schema `passage_source_disclosure` omits `canonical_mt_ref`, `canonical_lxx_ref`, `day_title`, and `service_hour`.
   - Actual `passage_source_disclosure.csv` includes those fields.
   Suggested revision: Update `out/design/lectionary_schema.json` so each table entry exactly matches the emitted CSV headers, or explicitly define “required minimum fields” separately from “full emitted fields.” The current schema reads like a table contract but is only partial.

5. Severity: required  
   Location: `verify_design_deliverables.py` lines 119-136, 260-268, 338-364  
   Finding: The verifier is meaningful for row counts, vocabularies, provenance blanks, and bridge distribution, but it does not enforce schema/output header parity. This allowed the schema drift above.  
   Evidence: `python3 verify_design_deliverables.py` returned `design deliverables verified`, despite schema table definitions missing fields that are present in generated CSVs.  
   Suggested revision: Add a verifier check that, for each generated CSV listed in the schema, compares `csv.DictReader(...).fieldnames` against `schema["tables"][table]`. If exact parity is not desired, rename the schema section to `required_fields` and add a separate `emitted_fields` contract.

6. Severity: required  
   Location: `audit_artifacts/open_questions_for_george.md` lines 25-28 and 40-52  
   Finding: The open questions blur two different concepts: `historical_candidate_removed` status versus populated `removed_marker`. Wisdom 1:20-2:15 and Wisdom 3:12-24 are listed as candidate removed readings, but they do not receive `removed_marker`, correctly, because George’s removed-marker list did not include them.  
   Evidence:
   - Open questions lines 42-43 list Wisdom rows under “Candidate removed readings needing current-authority confirmation.”
   - Data check: those Wisdom rows have `current_status=historical_candidate_removed` but blank `removed_marker`.
   - Acceptance criterion 5 restricts `removed_marker` to Isaiah 48:1-6, Isaiah 59:1-17, Zechariah 11:11-14, extra Proverbs, and Job 27-28.
   Suggested revision: Split the section into:
   - “Rows with `removed_marker` populated by George’s list”
   - “Other old-edition-only candidate-removed rows needing review”
   This avoids implying the Wisdom rows are part of George’s specific removed-marker list.

7. Severity: advisable  
   Location: `build_design_deliverables.py` lines 301-310; generated outputs with `removed_marker`  
   Finding: `removed_marker` values are consistent in shape and single-string, but not a single controlled token. They embed passage-specific citations directly in the marker. That is usable, but “uniform” in the acceptance criteria could be interpreted as a controlled marker value plus separate provenance fields.  
   Evidence: Six distinct marker strings are emitted, all beginning with “(removed, attested St. Mary Ottawa Holy Pascha...” and ending with “absent from Coptic Reader Wednesday Day fixture supplied by George)”.  
   Suggested revision: Consider separating:
   - `removed_marker = removed_from_current_fixture`
   - `removed_marker_note` or existing provenance fields for source page/line/current comparator
   If keeping the current prose marker, explicitly document that “uniform” means uniform prose pattern, not one shared enum value.

8. Severity: advisable  
   Location: `out/design/foundational_reading_collections_69.csv`; `out/design/lectionary_schema.json` lines 197-216 and 1608-1624  
   Finding: The 69 foundational collection is well represented, but the CSV does not carry the explicit `CONFIRMED_SAME_SET` verdict token as a row field. The schema-level vocabulary has `verdict_token`, but the per-row CSV has only `membership_status`.  
   Evidence:
   - CSV fields include `membership_status`, `membership_basis`, `verification_status`.
   - Schema `controlled_vocabularies.collection_types_69.verdict_token` is `CONFIRMED_SAME_SET`.
   Suggested revision: Add `membership_verdict` or `verdict_token` to each row in `foundational_reading_collections_69.csv/jsonl`, set to `CONFIRMED_SAME_SET`, while retaining `membership_status`.

9. Severity: advisable  
   Location: `audit_artifacts/lectionary_execution_log.md` lines 98-99 and 195-203  
   Finding: The execution log contains older Phase 6 row counts and bridge distributions before Step 7, then later Step 7 corrected distributions. This is historically accurate, but easy to misread during handoff.  
   Evidence:
   - Lines 98-99 report Phase 6 counts and all bridge rows `collection-type` / `medium`.
   - Lines 197-199 correctly report Step 7 before/after distributions.
   Suggested revision: Add one short note after Step 7 saying “Earlier Phase 6 counts/distributions are historical and superseded by Step 7 for bridge basis/confidence.” This will prevent stale interpretation.

10. Severity: advisable  
    Location: `site_integration_spec.md` lines 7-33  
    Finding: The copy list omits `out/design/foundational_reading_collections_69.csv/jsonl`, even though the site behavior now depends on the 69 collection for bridge basis explanation and controlled vocabulary.  
    Evidence:
    - Copy list includes schema, reverse presentation, source registry, bridge, etc.
    - It does not include `out/design/foundational_reading_collections_69.csv` or `.jsonl`.
    Suggested revision: Add both foundational-reading collection files to the site copy list, unless the site will consume the embedded schema copy only.

## Checks that passed

- `git status --short` showed no tracked file edits from this audit. One unrelated untracked file exists: `audit_artifacts/phase2b_sus_source_psalm_numbering_2026-06-15.md`.
- `python3 verify_design_deliverables.py` completed successfully with output: `design deliverables verified`.
- Content-rule scan over the target generated prose files found no em dashes and none of the banned words: `delve`, `multifaceted`, `additionally`, `landscape`, `underscore`, `foster`, `interplay`.
- Step 2 Pascha computation wording is appropriately qualified. Article lines 55-57 clarify that “follows the Hebrew calendar” means the Church’s Paschal computation through the Nicene/Alexandrian mode, not consulting the present-day Hebrew calendar.
- Step 2 NKJV correction passed. Article line 158 says “Scripture references follow NKJV versification.” It does not claim NKJV text is reproduced.
- Step 2 69 identity wording is appropriately caveated. Article line 77 states the Ottawa/UKMID identification is inferred from source identity, volume placement, function, and count, and that the consulted Youssef page does not give a date-by-date roster.
- Documentation-history section is not merely a reformatted sources list. Article lines 39-51 explain printed Katameros witnesses, public documentation layers, scholarly structural sources, Burmester as historical witness, Coptic Reader fixture scope, and Bible-text anchors.
- Foundational-reading collection output exists and has 69 rows. CSV fields include provenance, source, edition, locator, membership status, membership basis, and verification status.
- `source_registry.csv` includes `st_mary_ottawa_days` with edition “first edition, Christmas 1714 A.M., 1998 A.D.” and locator “UKMID PDF TOC pages 23 to 26 plus printed section page.”
- `removed_marker` is populated only on the expected Pascha removed-marker passage family:
  - Isaiah 48:1-6
  - Isaiah 59:1-17
  - Zechariah 11:11-14
  - Proverbs 1:10-33
  - Proverbs 4:4-27,5:1-4 / Proverbs 4:4-5:4
  - Job 27:16-28:2 / Job 27:16-20 / Job 28:1-2
- Historical readings were not deleted. They remain in presentation, attestation, temporal classification, residue, and source-disclosure outputs.
- Citable provenance is carried in the main placement and disclosure outputs. `reverse_lectionary_presentation.csv` and `passage_source_disclosure.csv` have zero blank `source_title`, `source_edition`, or `source_locator` fields.
- Pascha attestation rows carry aggregated source provenance via `source_titles`, `source_editions`, and `source_locators`; no blank values were found in those fields.
- `passage_source_disclosure.csv` has 66,381 rows, matching `reverse_lectionary_presentation.csv`, so the source-disclosure layer is additive rather than a replacement.
- Step 7 data upgrade is correct in generated output:
  - Bridge basis: `explicit=789`, `collection-type=3899`
  - Bridge confidence: `high=789`, `medium=3899`
  - Explicit bridge rows outside the 69: 0
  - Explicit bridge rows missing Ottawa citation: 0
  - Collection-type rows with non-medium confidence: 0
- `site_integration_spec.md` lines 53-59 correctly explain the Step 7 bridge behavior for site rendering.
- `open_questions_for_george.md` lines 93-112 correctly records the outside-69 bridge differentiation flag and the 11 foundational days with no emitted bridge rows.

## Open questions to record for George

- Should the repo include the locked `05-LECTIONARY-DESIGN.md` file, or should audits use a tracked substitute? Current repo-only auditing cannot inspect the source brief directly.
- Should `removed_marker` be a controlled enum-style value with citations in separate fields, or is the current prose marker acceptable as the controlled string pattern?
- Should Wisdom 1:20-2:15 and Wisdom 3:12-24 remain classified as `historical_candidate_removed`, or should they be separated into a different “old local row absent from fixture but not on George’s removed list” category?
- Should `foundational_reading_collections_69.csv/jsonl` carry the explicit `CONFIRMED_SAME_SET` verdict token per row, not only at schema-vocabulary level?
- Should the site copy the standalone `foundational_reading_collections_69.csv/jsonl`, or rely only on the embedded schema vocabulary?
