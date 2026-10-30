# Parent adjudication of the independent Mark component review

This is component-level diagnostic evidence, not combined-release approval. The independent review's original hashes and observations remain immutable in the parent review packet outside the source checkout.

- **N1, pending allowance scope:** retained as an explicit composition requirement. `validate_pending_reading` authenticates the bounded date/reference/disclosure allowance, not every source-family field. The real serialized-output verifier must still run the source-family/disclosure validators. The docstring now states that precondition. Reverse-only source fields are not fabricated on daily rows.
- **N2, inactive eve hours:** fixed in the coverage helper itself. A row with an explicit inactive lifecycle or removal marker cannot satisfy current-hour coverage. Existing missing-Reader hour disclosures remain unchanged.

## Regression evidence

New `tests/test_mark_eve_lifecycle.py` starts with the complete authenticated 2026 source projection. Before the fix, its valid control passed and all four targeted negatives failed because no rejection occurred: `active: false`, `status: removed`, `current_status: historical_witness`, and a supersession marker. After the fix, the entire new group and dedicated Mark group passed:

```sh
uv run --python 3.11 --with pytest --with convertdate python -m pytest -q tests/test_mark_eve_lifecycle.py tests/test_mark_followup_repairs.py
```

Observed result: **74 passed**, exit 0. The independent review already verified all 309 expected L10 source-table entries across the 21 requested sections and the separate historical Wednesday Eve Eleventh Hour evidence. This parent change does not add current readings or alter the reported daily membership delta.
