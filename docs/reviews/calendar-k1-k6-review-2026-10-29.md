# Calendar keys and display labels: K1-K6

## Scope and baseline

Implemented an additive runtime review module and isolated regression tests. No shared builder, release script, raw source dataset, catalog, Synaxarium, or site file was edited by this worker. No commit, push, or publication was performed.

The authenticated published baseline is `@andraws/lectionary-data` 1.3.6, with 12,206 reverse rows. Its tarball SHA-512 was recomputed and equals:

```
sha512-FD4T8t3ETBZLaWX359BnLBqglKmV1UeoX2j0MGxiJ3g4aRsqANGErVqnB+M7sCKjXV0/Z2zH8ItUJgS2ZtFAag==
```

Counts include retained inactive witnesses unless explicitly stated otherwise. Source classification uses the retained crosswalk table and exact passage-index ordinal, not the visual shape of the calendar label. All 6,039 Katameros baseline reverse rows resolve to their retained source tuples.

## Reproduction and outcomes

| ID | Published 1.3.6 finding | Implemented outcome |
| --- | --- | --- |
| K1 | All 4,525 source-qualified `AnnualReadings` reverse rows lack the normalized date field. | Fixed dates use Synaxarium slug keys. Original month spellings and raw keys remain unchanged. |
| K2 | 404 source-qualified annual-Sunday reverse rows represent 544 dated-independent source rows. There are 382 single literal month/ordinal keys, three single generic fifth-Sunday keys, and 19 multiple-key rows. The requested count of 361 does not reproduce. | `annual_sunday` is separate from `coptic_date_key`. Sunday rows never receive a fixed-date key. SQLite pseudo-month 14 becomes `any-month-5`, not a date. |
| K3 | Exactly 5,519 of 6,039 Katameros reverse rows have empty `day_titles`. | No saint or commemoration fields are added. All 366 distinct generated fixed-date keys exist in the unchanged Synaxarium. |
| K4 | Exactly 83 reverse rows have the Entry-into-Egypt collision suffix, corresponding to 125 presentation witnesses. | Only `display_label` loses the suffix. A genuine stand-alone Entry feast label is unchanged. |
| K5 | The 99 generic Great Lent reverse rows correspond to 167 dated ordinary-source witnesses on 12 Coptic dates. Of those 99 rows, 26 collapse more than one fixed date. Ten St Mary's Fast reverse rows correspond to 160 witnesses, all on Mesra 1. | Great Lent receives 128 date-specific metadata views; St Mary's Fast receives ten. Every selected date has retained numeric-date and/or Gregorian-locator evidence. No real affected ordinary row requires a hold. The no-evidence path is tested and stays inactive with `calendar_review_status=seasonal_label_unresolved`. |
| K5, Nineveh qualification | The 26 named Nineveh reverse rows are eight source-qualified movable-cycle rows and 18 no-service archive rows. There are zero generic ordinary-source rows with that title. | The alleged fixed-date defect does not reproduce for this cohort. No fixed dates or new holds are imposed on either the qualified cycle or its inactive archive. |
| K6 | The legacy Theophany term appears on 31 reverse rows, not 42. The legacy Nativity Fast term appears anywhere on 63 reverse rows, including 22 `occasion` values. | Normalized display labels use Theophany, Paramoun of the Theophany, and Nativity Fast. No raw source field is renamed. |

The complete presentation projection preserves all 67,884 input rows and all existing field values. It gives 43,201 rows fixed-date metadata and validates their 366 distinct date keys against the catalog. This is a source-layer result, not a new design membership contract.

## Runtime API and parent integration hook

The parent-selected lane runs after npm `canonicalizeOccurrences`, outside the unchanged historical design corpus guard:

```python
from calendar_review_repairs import load_runtime_review

calendar = load_runtime_review(ROOT)
reverse_rows = calendar.apply_reverse_rows(payload['rows'])
daily_days = calendar.apply_daily_year(payload['days'])
```

`apply_reverse_rows` accepts published-like reverse rows. `apply_daily_year` accepts a complete `{ISO-date: reading-array}` year and binds each reading to that trusted outer date. The parent's `scripts/apply_review_repairs.py` already calls these exact APIs in its reverse and daily branches. Calendar metadata must run before sibling coordinate or composite repairs, because its source qualifier deliberately rejects altered identities.

`load_runtime_review(ROOT)` caches one read-only source model per process. A direct probe replaced `sqlite3.connect` with a rejecting function: loading succeeded, made zero SQLite connections, and a second call returned the same model instance. No per-reading database queries or network calls are needed.

The normalized fields are:

- `coptic_date_key`
- `annual_sunday`
- `display_label`
- `calendar_review_status`

Runtime views also carry `calendar_review_source_locators` and `calendar_review_calendar_keys`, identifying the exact selected retained witnesses. These are reading metadata, not catalog additions. A collapsed raw row containing several calendar contexts receives separate metadata views. All original fields, including the representative raw locator, remain unchanged; the added locator list identifies the evidence for each selected context rather than falsely treating the representative locator as evidence for every date.

Do not replace `occasion`, `calendar_keys`, `day_titles`, `source_title`, `source_locator`, provenance, source disclosures, or original lifecycle fields with the normalized values. Do not feed the new metadata views back through the legacy canonicalization fingerprint. The runtime APIs accept their own output idempotently.

## Exercised runtime results

| Projection | Input | Output | Preservation |
| --- | --- | --- | --- |
| Published-like reverse | 12,206 rows | 12,327 metadata views | Every original raw row retained unchanged, with 121 extra context views; replay identical. |
| Daily 2026 | 365 dates, 4,097 readings | 365 dates, 4,097 readings | All original fields and physical reading order unchanged. |
| Daily 2027 | 365 dates, 4,088 readings | 365 dates, 4,088 readings | All original fields and physical reading order unchanged. |
| Daily 2028 | 366 dates, 4,103 readings | 366 dates, 4,103 readings | All original fields and physical reading order unchanged. |

The reverse result contains 7,892 fixed-date views and 1,036 annual-Sunday views. These populations are disjoint. There are zero unresolved real-source holds in this cohort, zero invalid Synaxarium keys, and zero prohibited legacy terms or collision suffixes in display labels. Kiahk 23 retains both conflicting Matins Gospel witnesses; this module does not decide R2.

## Verification

The same six K1-K6 behavioral contracts were run against the published baseline and then the projection:

```sh
LECTIONARY_CALENDAR_BASELINE=/absolute/path/to/authenticated/package \
CALENDAR_REVIEW_MODE=baseline \
uv run --no-project --python 3.11 --with convertdate python \
  -m unittest discover -s tests -p test_calendar_review_repairs.py -v

LECTIONARY_CALENDAR_BASELINE=/absolute/path/to/authenticated/package \
uv run --no-project --python 3.11 --with convertdate python \
  -m unittest discover -s tests -p test_calendar_review_repairs.py -v
```

RED: 25 tests discovered, six expected K1-K6 failures, ten projection-only skips. GREEN: 25 tests passed, zero skips. The suite covers all three complete daily years, the entire published reverse array, original-field preservation, source family/kind rebinding, wrong reference/identity/slot/locator/title/context, wrong outer date, normalized-field and evidence mutations, contradictory date evidence, missing catalog keys, no-date holds, movable Nineveh noninterference, distinct multi-date contexts, and idempotent replay.

The local `python3` resolves to Python 3.9.6 despite the inherited toolchain note. Python 3.11.15 was used through `uv`; `convertdate` was supplied in an isolated tool environment. No repository dependency file was changed.

`py_compile` passed. Parent package assembly, combined sibling repairs, tarball verification, and release acceptance remain the parent's responsibility. This worker's passing projection is not a claim that a package was rebuilt or released.

Machine-readable counts, source fingerprints, the compact source projection, and full RED/GREEN logs are in the task evidence directory:

```
/Users/ga/workspace/lectionary-fixes-20261029/calendar-evidence.json
/Users/ga/workspace/lectionary-fixes-20261029/calendar-projection.jsonl
/Users/ga/workspace/lectionary-fixes-20261029/calendar-red-final.log
/Users/ga/workspace/lectionary-fixes-20261029/calendar-green.log
```
