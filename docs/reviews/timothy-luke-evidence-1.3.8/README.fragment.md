# T-L6, LK7 and LK9 integration fragment

This is a source-owned follow-up module, not a regenerated or released package. No builder, root README, release contract, comparator or generated package file was edited by this worker.

## Python APIs

```python
import evidence_followup_repairs as evidence

# Reverse: call after ordinary review projections, before final serialization.
# This returns (fresh_rows, counts), not just a list.
reverse_rows, counts = evidence.repair_rows(reverse_rows)

# Final serialized readback: authenticate emitted evidence AND exact 45-target
# membership. Keep all existing source, lifecycle and corpus validators too.
evidence.validate_rows(reverse_rows, require_all_targets=True)

# Daily: only LK9 applies. Keep the ordinary schema and source qualifications.
for date, readings in days.items():
    days[date], psalm_counts = evidence.repair_psalm_annotations(readings)
    evidence.validate_psalm_annotations(days[date])
```

Separate APIs: `repair_evidence_rows(rows, *, root=None)`, `validate_evidence_rows(rows, *, root=None, require_all_targets=False)`, `repair_psalm_annotations(rows)`, `validate_psalm_annotations(rows)` and `frame_qualified_lxx(mt_ref)`. The last function accepts an already-qualified MT reference; callers must not feed source-frame coordinates to it directly. Use the row-level repair to enforce that prerequisite.

Preserve these additional reverse fields through explicit output allowlists: `evidence_status`, `evidence_json`, `psalm_annotation_review_json`. The first two are also bound into each original `source_disclosure` entry under `evidence_followup`. Existing disclosure fields and source titles, locators, editions, calendar keys, coordinate numbers, selections, statuses and occurrence identifiers are preserved. No new occurrence is created and no witness is deleted.

LK9 changes annotation and its explanation, not retained occurrence IDs. Daily and reverse callers must both run the annotation hook so their coordinate metadata agrees. New identity-key policy is outside this bounded repair.

## Compatibility with Mark follow-up

A real read-only probe against the finished `mark_followup_repairs.py` found:

- Zero intersections between this worker's 49 changed reverse rows and `mark_followup.rule`.
- `mark_followup.qualify_emitted` returned false for all 49, without a refusal.
- None of this worker's three affected daily dates is among Mark's 36 pinned complete-date groups.
- The six Mark L7 rows are not in this 45-row target ledger and are untouched, including their Mark-owned `unverified_service_book` metadata.

No reversible adapter is needed for that Mark contract as frozen. Do not strip or relax Mark guards. Other existing generic validators can reject LK9's corrected annotation because they still expect the generic chapter-only proposal. Parent may validate an untouched internal view before this additive projection, but must separately validate final emitted rows with this module. Do not derive predecessor expectations by repairing candidate data. The authenticated predecessor ledger and retained source packs remain the oracle.

## Dependencies and verification

The new module requires its pinned `baseline-targets.json` plus existing retained Special and Covenant Thursday source packs, their current source-qualified modules, `build_design_deliverables.py`, and `passage_normalization.py`. Disposable builder fixtures must copy these genuine dependencies. The Oil of Gladness context also authenticates `source-classification-verdicts.json`; an old unclassified record alone is not the rubric oracle.

```sh
uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate --with pytest python -m pytest tests/test_evidence_followup_repairs.py -q
```

Parent owns final shared-hook integration, strict output allowlists, full frozen-candidate suites, package rebuild, artifact verification, commit and publication. Nothing here authorizes regeneration, npm, site changes or publication by this worker.
