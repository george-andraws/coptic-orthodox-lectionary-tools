# Exact-dated Matins source candidate (not a release)

Accepted corpus SHA-256: `5f7558115e4743e08febe5e5ecd7f350573c3b80af1d517951db6cc0db9526d2`.
The original 119 records, producer flags, body envelopes and origin strings are
retained byte-for-byte. There are 59 complete exact-dated pairs and one incomplete
2026-04-03 Psalm/Gospel witness. The incomplete date cannot be projected. This
fixture does not authorize recurrence, canonical coordinates or default activation.

## Actual upstream APIs

```python
from build_lectionary_reference import fetch_date, project_dated_matins_source, build_date_passage_index

# Explicit source-only opt-in. context must contain exactly these authenticated
# captured fields, with original values from the accepted source_record:
# civil_date, occasion_key, actual_occasion, actual_home_line,
# numeric_coptic_calendar_crosscheck, pascha_offset_days, weekday, service.
meta, rows = fetch_date(date, html_cache, candidate_matins_context=context)
# Or apply to a real preexisting source table directly:
projection = project_dated_matins_source(rows_from_source, context)
# Source-coordinate search ONLY; matched_ref and canonical_ref remain blank:
held_source_index = build_date_passage_index(rows, include_candidate_matins=True)
# Default canonical index never materializes the candidate:
default_index = build_date_passage_index(rows)
```

The HTML parser and fetch helper do not enable this automatically. The complete
source replacement is in the returned active candidate table. Every original
Matins row remains in `meta['matins_source_projection']['history']` (or the direct
projection's history), explicitly inactive/superseded. Non-target services and
other civil-date rows retain their exact dictionary values and order. No default
package, calendar, catalog, Synaxarium or generated-output builder is changed.

`source_parse_input` is a held Reader-coordinate search string, not an MT/LXX
span. The odd Isaiah heading, Jonah chapter reset and Mark's omitted 44/46 have
source-body-qualified search syntax without changing the raw labels. Composite
Psalms preserve source order and unqualified numbering. Partial clauses and
numbered English source lines remain explicit; no missing verse is interpolated.
`source_body` retains the complete assigned envelope; `source_document_body`
retains the full rendered document. Both hashes, heading UTF-8 offsets, exact
context, navigation and original evidence state are carried with the candidate.

## Integrity and portability

`fingerprints.json` is a code-pinned local integrity trust root, not a publisher
signature. It binds all source/context/screenshot and independent review bytes.
`path-map.json` maps untouched historical origin locators to repository-relative
copies; those personal absolute origin strings are provenance, never filesystem
dependencies. `supplementary-contexts.json` supplies original captured home/picker/
menu evidence for the three legacy exception pairs whose records did not contain
an explicit context_files array. Source records themselves are not rewritten.
The new supplementary context binding is integration evidence, not new recurrence
or canonical approval.

Run `test_upstream_matins.py` with a Python environment containing requests and
BeautifulSoup. `verify_helper_replay.py` compares every available cached HTML date
against the opening BRef code and replays every accepted complete pair through
fetch_date and the actual source index API. `verify_portability_and_mutations.py`
exercises a scratch repository clone with a nonexistent HOME and rejects raw body,
selected-context and independent-review corruption; it also kills a deliberate
whole-table authentication bypass. Reports are written only to the explicit
`--report-dir` argument. No builder/network/vault/package activation is run.

Independent runtime/recurrence and downstream consumer review is still required
before any default promotion. A successful held source search is not a successful
canonical package query or approval of any old edition proposal.
