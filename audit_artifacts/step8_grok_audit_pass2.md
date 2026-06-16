# Step 8 Grok Audit Pass 2

## Summary

I inspected only `/Users/georgeandraws/workspace/coptic-lectionary-research`. I did not edit, commit, or push.

The substantive Step 8 corrections look good: stale bridge prose was fixed in the article/spec/site spec, schema/header parity is now enforced, the 69 collection has per-row `membership_verdict=CONFIRMED_SAME_SET`, open questions now separate `removed_marker` rows from other candidate-removed rows, and verification passes.

One required repo-state issue remains: `05-LECTIONARY-DESIGN.md` exists locally, but it is still untracked according to `git status --short`. If this is committed as-is without adding that file, the repo-local locked brief will still be missing from the tracked repository.

## Required revisions

1. Severity: required  
   Location: repo root, `05-LECTIONARY-DESIGN.md`  
   Finding: The repo-local locked brief now exists, but it is not tracked yet. This only partially resolves pass 1 finding 1.  
   Evidence: `git status --short` returned:
   - `?? 05-LECTIONARY-DESIGN.md`

   The file itself is readable and contains the locked decision brief, including Section 2 “Locked decisions” at lines 115-130. But because it is untracked, it will not be present in the committed repo unless explicitly added.  
   Suggested revision: Add `05-LECTIONARY-DESIGN.md` to the Step 8 commit. If the intent is to preserve audit traceability too, also add `audit_artifacts/step8_grok_audit_pass1.md`, which is likewise untracked.

## Advisable revisions or open questions

1. Severity: advisable  
   Location: `audit_artifacts/lectionary_execution_log.md` lines 90, 98-99, 195-203  
   Finding: The execution log still contains historical Phase 6 wording saying the bridge was strengthened as “medium-confidence collection-type discovery links” and that all 4,688 bridge rows had `basis=collection-type` and `confidence=medium`. Step 7 later records the corrected distribution, but there is still no explicit note saying the earlier Phase 6 distribution is historical and superseded.  
   Evidence:
   - Lines 98-99 still report all 4,688 bridge rows as `collection-type` / `medium`.
   - Lines 195-203 correctly report Step 7 after-distribution as `explicit=789`, `collection-type=3899`, `high=789`, `medium=3899`.
   - I did not find the pass 1 suggested note: “Earlier Phase 6 counts/distributions are historical and superseded by Step 7 for bridge basis/confidence.”
   Suggested revision: Add one sentence under Step 7, for example:  
   `Earlier Phase 6 bridge basis/confidence counts are historical and are superseded by this Step 7 distribution.`

2. Severity: advisable / open question  
   Location: `out/design/temporal_classification.csv`, `audit_artifacts/open_questions_for_george.md` lines 40-55  
   Finding: The `removed_marker` implementation remains prose-pattern based rather than a single enum token. This is acceptable if intentional, and the open question is now properly preserved.  
   Evidence:
   - There are 9 rows with `removed_marker`, representing 6 distinct marker strings.
   - The markers are scoped only to George’s named removed-reading families.
   - The Wisdom candidate-removed rows are now separately listed without implying they are part of George’s removed-marker list.
   Suggested revision: No immediate data change required. Keep the enum-vs-prose decision open for George unless Codex chooses to normalize now with a separate `removed_marker_note`.

## Checks that passed

- `git status --short` ran successfully. Current changes are uncommitted, and `05-LECTIONARY-DESIGN.md` is present but untracked.
- `python3 -m py_compile build_design_deliverables.py verify_design_deliverables.py scripts/build_phase6_deck.py` passed.
- `python3 build_design_deliverables.py` passed and regenerated the design summary.
- `python3 verify_design_deliverables.py` passed with: `design deliverables verified`.
- `git diff --check` passed.
- Generated prose scan over the target files found no em dashes and none of the banned words checked: `delve`, `multifaceted`, `additionally`, `landscape`, `underscore`, `foster`, `interplay`.
- Article bridge wording is no longer stale:
  - `coptic-lectionary-and-synaxarium.md` lines 102-107 now says 69-covered rows are `explicit` / `high`, outside-69 rows remain `collection-type` / `medium`, and neither is direct proof for every named commemoration.
  - Teacher note at lines 141-142 carries the same caveat.
- `lectionary_spec.md` bridge section is no longer stale or incomplete:
  - Lines 217-229 list the actual emitted bridge columns.
  - Line 231 documents `explicit/high` for 69-covered rows and `collection-type/medium` outside the 69.
- Schema/output header parity is now enforced:
  - `verify_design_deliverables.py` lines 143-166 compare actual CSV headers to schema table contracts.
  - Independent header parity check found no mismatches for emitted CSVs listed in `out/design/lectionary_schema.json`.
- `out/design/synaxarium_reading_bridge.csv` distribution is correct:
  - 4,688 rows total.
  - `basis`: `collection-type=3899`, `explicit=789`.
  - `confidence`: `medium=3899`, `high=789`.
- `out/design/foundational_reading_collections_69.csv` has 69 rows and now includes per-row `membership_verdict=CONFIRMED_SAME_SET`.
- `out/design/lectionary_schema.json` includes the 69 collection verdict and expanded table contracts.
- `audit_artifacts/open_questions_for_george.md` now separates:
  - rows with `removed_marker` populated by George’s list,
  - other old-edition-only candidate-removed rows needing review.
- `site_integration_spec.md` now includes both foundational 69 files in the copy list:
  - `out/design/foundational_reading_collections_69.csv`
  - `out/design/foundational_reading_collections_69.jsonl`
- Source/provenance/disclosure outputs remain present and verified, including `source_registry.csv`, `passage_source_disclosure.csv/jsonl`, source editions, locators, URLs, and citations.
