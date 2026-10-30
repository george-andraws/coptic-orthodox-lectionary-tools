# Metadata follow-up integration contract

No existing shared file was edited by this worker. The parent integrates the following APIs.

## Projection order

At package projection, after the existing Mark overlay, call:

```python
import metadata_followup_repairs as metadata
rows = metadata.repair_rows(rows)
metadata.validate_rows(rows)
days = metadata.repair_daily(days)
for readings in days.values():
    metadata.validate_rows(readings)
```

This layer is one-to-one and changes only the declared `CHANGED_FIELDS`. It does not filter daily rows or assign reading order. Keep the existing complete membership guard unchanged. Run the composite and Psalm worker layers after this metadata layer, or undo those layers before invoking this layer's inverse, because their new coordinates or composite identities are not part of the frozen metadata source tuple.

All additive fields must survive any later explicit output field allowlists. Existing source titles, source locators, raw calendar keys and disclosures must not be rebuilt from display labels. Synaxarium titles are date-only co-display; they do not select readings or establish a reading's relationship to a saint.

## Authenticated inverse and existing qualifiers

The parent must not give metadata-enriched rows directly to older exact-row Mark or calendar qualifiers. Do not weaken those qualifiers or replace their expected arrays.

```python
# After undoing any later worker layers, authenticate and remove only metadata.
mark_view = metadata.restore_daily_for_comparison(days, previous_layer='mark')
# This existing guard still authenticates the COMPLETE Mark successor tables.
predecessor_view = mark.restore_predecessor_for_comparison(mark_view, year)
```

For a direct emitted reverse or daily row qualifier:

```python
mark_rows = metadata.restore_rows_for_comparison(rows, date=trusted_date_or_none)
for row in mark_rows:
    mark.qualify_emitted(row, date=trusted_date_or_none)
```

For the old calendar qualifier's exact normalized-label comparison, use the independently selected calendar view:

```python
calendar_rows = metadata.restore_rows_for_comparison(
    rows, date=trusted_date_or_none, previous_layer='calendar')
```

The default `mark` view reconstructs Mark's prior labels from immutable predecessor bytes through Mark's existing display-label API. The `calendar` view instead restores the predecessor's exact pre-Mark calendar label. It never reconstructs either label from a mutable candidate label. All metadata values and field-presence differences must match this layer's source-derived expected projection before restoration is returned. Arbitrary metadata, a changed source tuple, erased flags, substituted seasons or forged display text are rejected. Source status, endpoints, all foreign fields, row order and membership are left untouched for the older guards to authenticate. There is no replacement of missing rows from the fixture.

Run inverse views only when this projection layer has actually been applied. The API does not accept a mutable payload flag as proof of its execution.

## Endpoint and check-sheet APIs

- `endpoint_conflicts(rows)` is report-only and returns exact context, service, slot, canonical start, endpoint variants, retained Gregorian dates and source-qualified witnesses. It does not mutate input or choose a range.
- `timothy_confirmations()` returns exactly seven low-priority confirmations. Six have retained copticchurch URLs; the already Reader-backed Great Thursday Water Liturgy retains its actual Reader evidence locator. No copticchurch witness for that service exists in the frozen package.
- `baseline()` authenticates the frozen full predecessor source fixture. It is not a permission to replace or refresh the independent existing release membership ledger.

## Fixture-copy dependencies

Add these paths to disposable real-builder fixture copying, without disabling source authentication:

- `metadata_followup_repairs.py`
- `sources/metadata-followup-1.3.8/published-1.3.7.json.gz`
- `out/data/katameros_cycle_passage_index.csv`
- `sources/katameros-api/Core/Repositories/ReadingsRepository.cs`

The inverse also needs `mark_followup_repairs.py` and Mark's normal retained fixture/evidence dependencies. The existing fixture helper already owns those Mark dependencies. No network access, SQLite write, credential or package installation is required by the metadata module.

The new source fixture is 3,437,856 compressed bytes, with SHA-256 `6b08ce872a07b2849a8ddc05c8db759648ee50e3b5f6a693df392f81da02c5ba`. Its input package files and registry integrity are listed in `scope.json`. Generated output and candidate oracle files are not fixture dependencies.

## Focused commands

```sh
uv run --python 3.11 --with pytest python -m pytest -q \
  tests/test_metadata_followup_repairs.py \
  tests/test_metadata_followup_controls.py \
  tests/test_metadata_followup_restoration.py
python3 scripts/report_metadata_followup.py
```

The 42 focused tests passed, including exact round trips through Mark's unchanged complete-table guard for all three years. Parent-owned whole-candidate build, final serialized validation, pack/install and publication acceptance remain separate gates.
