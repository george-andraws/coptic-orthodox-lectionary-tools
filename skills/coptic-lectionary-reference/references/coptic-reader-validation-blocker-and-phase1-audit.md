# Coptic Reader validation blocker and Phase 1 audit pattern

Use this reference when the requester asks to validate the local lectionary dataset specifically against Coptic Reader, especially when the task says not to improvise a new extraction method.

## Durable lesson

Do not treat the local lectionary builder's existing sources as Coptic Reader unless the repo actually documents a Coptic Reader access path. In the observed builder repo, the live sources were:

- `sources/katameros-api/Core/KatamerosDatabase.db` for annual/Sunday/Great Lent/Pentecost cycle tables.
- `copticchurch.net/readings?...` cached/scraped daily pages for date-resolved readings.
- downloaded/extracted Katameros/Pascha text, especially St. Mary Ottawa Holy Pascha text, for Holy Week source text.
- curated Python rows for special-service and Agpeya data.

Live repo and git-history searches found no Coptic Reader ingestion/access code or notes for terms like `Coptic Reader`, `CopticReader`, `copticreader`, `main.dart.js`, `documentPath`, `AssetManifest`, or `reader.coptic`.

## Required stop condition

If the requester asks for Coptic Reader as ground truth and also says not to improvise extraction, then:

1. Inventory the repo and document exact paths/counts.
2. Search live files and git history for the original Coptic Reader access mechanism.
3. If no repo-backed mechanism is found, stop before fresh extraction, duplicate analysis, or Coptic Reader comparison.
4. Write a blocker report only, explicitly saying the original access path is not reproducible from the repo.
5. Do not modify dataset files.

A useful report location pattern is:

```text
audit_artifacts/phase1_coptic_reader_validation_blocker_YYYY-MM-DD.md
```

Commit only the markdown report when the user asked for one commit per phase and the report is the Phase 1 deliverable. Before committing, run a staged-path guard so generated data stays untouched, for example check that no staged paths match `^(out|sources|cache)/|\.csv$|\.jsonl$|\.db$|\.sqlite$`.

## Inventory facts from the observed repo shape

Common paths to report:

- Main builder: `build_lectionary_reference.py`
- Crosswalk builder: `build_lectionary_crosswalk.py`
- Chapter occurrence builder: `build_bible_chapter_lectionary_index.py`
- Pascha source-text builder: `build_pascha_source_text_index.py`
- Query helper source: `query_lectionary.py`
- Packaged query helper: `out/scripts/query_lectionary.py`
- Verifier: `verify_lectionary_queries.py`
- Reverse crosswalk: `out/data/reverse_lookup_crosswalk.csv`
- Chapter occurrence CSV: `out/data/bible_chapter_lectionary_occurrences.csv`
- Pascha day/hour CSV: `out/data/pascha_day_hour_index.csv`
- Durable/fallback Pascha day/hour CSV: `out2/pascha_day_hour_index.csv`
- Pascha source text CSV: `out/data/pascha_source_text_index.csv`
- Source SQLite DB: `sources/katameros-api/Core/KatamerosDatabase.db`
- Packaged DB copy: `out/sources/KatamerosDatabase.sqlite`

If there is no conventional `tests/`, `test*.py`, `*_test.py`, `pytest.ini`, or `pyproject.toml`, say so plainly and identify `verify_lectionary_queries.py` as a verifier rather than pretending it is a full test suite.

## Holy Week schema observation to carry forward

The Pascha day/hour CSV shape is:

```text
day,hour,source,order,slot,refs
```

That is not the ordinary Liturgy-only structure. It models Holy Week by day/hour plus Pascha slot. Do not flatten Pascha into ordinary `Pauline / Catholicon / Praxis / Psalm / Gospel` assumptions when auditing schema or root cause.
