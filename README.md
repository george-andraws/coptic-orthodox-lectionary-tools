# Coptic Lectionary Research Package

Local reference package for Coptic Orthodox lectionary research and study generation.

## Main build

Run from this directory:

```bash
python3 build_lectionary_reference.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py
```

The main generated package lives under `out/`:

- `out/data/` - generated CSV/JSONL data
- `out/scripts/query_lectionary.py` - query helper copied from tracked `query_lectionary.py`
- `out/scripts/passage_normalization.py` - copied from tracked `passage_normalization.py`

Pascha and Bright Saturday artifacts are treated as required package inputs. The main builder prefers canonical copies in `out/data/` and falls back to legacy side-output directories (`out2/`, `out_bright/`) when needed.

## Malformed source refs

Some copticchurch.net source rows contain malformed raw refs such as `Mk 14:-39`. These are repaired for indexing, but not silently: repaired rows are reported in `out/data/source_ref_repair_report.csv` and carry warning metadata in `copticchurch_passage_index_2020_2035.csv`.

## Synaxarium

`build_synaxarium_index.py` is intentionally separate from the lectionary build. It produces a St-Takla Synaxarium source map under `out_synaxarium/`; it is not currently part of `BUILD_SUMMARY.json` or `query_lectionary.py`.

## Bible chapter index

The build also generates a chapter-level index from the reverse passage crosswalk:

- `out/data/bible_chapter_lectionary_index.csv` - one row per supported Bible chapter, including unread chapters
- `out/data/bible_chapter_lectionary_occurrences.csv` - detailed occurrence rows for chapter coverage

Query example:

```bash
python3 out/scripts/query_lectionary.py --chapter "John 2"
```
