# Phase 3 verification - Pascha Wednesday reverse index deliverable

- Baseline for before counts: `1f04c1a^:out/design/reverse_lectionary_index.jsonl`.
- Current design deliverable: `out/design/reverse_lectionary_index.jsonl`.
- Handoff copy: `out/handoff/reverse_lectionary_index.jsonl`.
- Package copy: `packages/lectionary-data/data/reverse_lectionary_index.jsonl`.

## Query/card counts

- `Psalm 23` query count: before `39`, after `39`. No change expected or observed.
- Pascha Wednesday query count: before `65`, after `47`. This dropped by `18` because exact duplicate A rows collapsed and the First Hour Psalm composite moved into attestation.

## Exact duplicate A collapse

- Category A identity keys checked: `17`.
- Before A row counts by identity had duplicates: `17` identities with two or more rows.
- After A row counts by identity: `17` rows for `17` identities; every A identity has one reverse-index row.
- First Hour Psalm rows now have `source_disclosure_count=3` and retain St. Mary Ottawa, local Pascha, and Coptic Reader attestations.

## B and C preservation

- Category B: before rows `14`, after rows `14`, before identities `9`, after identities `9`, key removed `0`, key added `0`, changed common rows `0`.
- Category C: before rows `25`, after rows `25`, before identities `16`, after identities `16`, key removed `0`, key added `0`, changed common rows `0`.

## Record-count diff by occasion

- `Wednesday`: before `36`, after `18`, delta `-18`.

No other occasion record count changed.

## Label/collision check

- Category A rows with non-Pascha-Wednesday label after rebuild: `0`.
- Remaining bare `Wednesday` rows are B/C routed items or unresolved Psalm/range artifacts; they were intentionally not altered in Phase 1.

## Deliverable hashes

- `out/design/reverse_lectionary_index.jsonl`: `ba6dcec9cdfa7a9497f2f5abd2dc2f014fdc18a8d07f2ea9e02c1ae59dc5d396`
- `out/handoff/reverse_lectionary_index.jsonl`: `ba6dcec9cdfa7a9497f2f5abd2dc2f014fdc18a8d07f2ea9e02c1ae59dc5d396`
- `packages/lectionary-data/data/reverse_lectionary_index.jsonl`: `3e3fa60fb1255153dae5acc1f13adea1f8b98b1ed6f8a08b76ab134a2dca6493`

## Validation commands

- `PYTHONDONTWRITEBYTECODE=1 python3 verify_design_deliverables.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_package_integrity.py --package-dir /Users/georgeandraws/workspace/coptic-lectionary-research/packages/lectionary-data`
- `git diff --check`
