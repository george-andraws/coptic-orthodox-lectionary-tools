# Structured passage matching and build-pipeline hardening

## Book/type semantic integrity

- Validate each emitted biblical passage against its reading slot; correct string matching alone cannot prevent upstream Gospel references from being indexed as Catholic Epistles. Require Gospel books for Gospel slots, the seven Catholic Epistles for Catholic slots, Pauline books for Pauline slots, Acts for Praxis, and Psalms for Psalm slots.
- Preserve raw erroneous references and attach an independently sourced correction before normalization. Reject malformed double numeric book prefixes instead of salvaging an inner regex match; `62.43.4:15-21` must not silently become Gospel John.
- Keep service grouping separate from passage type. A Palm Sunday Gospel group can contain Psalms; classify the individual Psalm as Psalm while retaining its enclosing first/fourth Gospel service section and the source's Psalm numbering.
- Audit every downstream representation after these repairs: split cycle/date passage indexes, crosswalk, design reverse index, npm reverse/daily files, website primary search, and legacy fallback shards/index. Report overlapping materialization counts separately, not as an additive total.
- Inspect legacy schema explicitly: the website compact index stores reading type in `hour`, not `slot_type`. A validator that checks only package fields can silently miss every fallback defect.


Use this when maintaining the local Coptic lectionary package after adding reverse crosswalk, Pascha day/hour support, or new passage indexes.

## Durable lessons from this session

### 1) Do not use substring passage matching for structured Bible references
Loose containment causes false positives.

Examples that must stay blocked:
- `John 2` matching `John 20`, `John 21`, or `1Jn 2`
- `Isa 5` matching `Isa 50`, `Isa 52`, `Isa 53`, or `Isa 58`

Preferred approach:
- normalize the book name first
- parse both query and candidate into structured spans
- require exact normalized book equality
- compare chapter/verse overlap numerically
- only use plain text containment for true non-structured numeric shorthand cases such as `40.5`

### 2) Use the shared normalization module everywhere
If build-time and query-time logic drift, lookup quality degrades fast.

Keep `passage_normalization.py` as the single source of truth for:
- book-name normalization
- structured passage parsing
- cross-chapter/open-ended cleanup
- overlap matching
- helper/runtime matching

Any change to passage parsing should flow through:
- `build_lectionary_reference.py`
- `build_lectionary_crosswalk.py`
- generated `out/scripts/query_lectionary.py`
- copied `out/scripts/passage_normalization.py`

### 3) Do not index malformed open-ended refs as searchable passages
Bad examples that should not appear in normal searchable fields:
- `2Pet 1:19—`
- `Acts 6:1—`
- `Mark 14:-3-9`
- `Mark 14:-39`

Preferred handling:
- clean `:-` artifacts before parsing
- when the source is a same-book chained reference like `Isa 52:13— & Isa 53:12`, combine it into a bounded span if possible
- otherwise exclude the malformed open-ended fragment from the searchable passage index and reverse crosswalk
- preserve ugly source text only in provenance/raw display fields, not canonical searchable fields

### 3b) Holy Pascha source text has malformed cross-chapter shorthand that should parse, not be preserved as unparsed
St. Mary Ottawa Holy Pascha source-text extraction can produce cross-chapter shorthand that looks malformed but is recoverable from context:
- `Zephaniah 1:14-2:1-2` → `Zeph 1:14-2:2`
- `Genesis 1:1-2:1-3` → `Gen 1:1-2:3`
- `Isaiah 55:1-13-56:1` → `Isa 55:1-56:1`
- `Zechariah 12:11-14:1-3, 6-9` → `Zech 12:11-14:3,14:6-9`

Preferred handling:
- repair in the shared `passage_normalization.py` parser, not by hand-editing generated CSVs
- keep `raw_ref` exactly as extracted for provenance
- assert `pascha_source_text_index.csv` has zero unparsed rows after rebuild
- add verifier checks for each repaired canonical ref so the source-text index and reverse crosswalk stay trustworthy

### 4) Text cycle lookups and numeric shorthand should use different paths
For `--cycle-passage`:
- structured text queries like `Matt 5:1` should use `katameros_cycle_passage_index.csv`
- numeric shorthand like `40.5` should continue to use the legacy normalized/raw cycle reading path

This keeps the classic shorthand behavior without reintroducing substring leaks.

### 5) Crosswalk build must consume local fresh data first
`build_lectionary_crosswalk.py` should read from local `out/data`, not the published downstream documentation package copy, so rebuilds are deterministic and do not depend on stale published artifacts.

### 6) Keep crosswalk inclusion explicit for ordinary passage queries
Safer default:
- `--passage` prefers date-resolved hits first
- only fall back to reverse crosswalk when no date-resolved hits exist
- use `--include-crosswalk` when you intentionally want broader appended results

This keeps ordinary lookup output focused while still making broader reverse lookup available on demand.

### 7) Make the top-level build own the pipeline
Preferred pipeline order:
1. build reference data locally
2. copy Pascha / Bright Saturday datasets into local `out/data`
3. build reverse crosswalk from local data
4. copy support modules and generate helper
5. run a repeatable verification script
6. only then rely on published artifacts

### 8) Keep a repeatable verification script in the project
A project-level verification script should cover:
- false-positive prevention (`John 2`, `Isa 5`)
- known-good lookups (`Isaiah 53`, `Isa 53`, `Matt 5:1`, `40.5`)
- Pascha day/hour lookup
- artifact existence after clean build
- malformed searchable ref count in normal indexes

Session implementation used `verify_lectionary_queries.py` for this role.
