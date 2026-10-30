# Coptic Orthodox Lectionary Tools

Source pipelines, validation tools and the published `@andraws/lectionary-data` runtime package for Coptic Orthodox reading lookup and date-based Synaxarium display.

## Current runtime release

**Version 1.3.7 is the current release candidate; 1.3.6 is the authenticated published baseline.** The candidate corrects the complete weekday Kiahk 23 table, source-confirmed Holy Week errors and Last Friday Matins; it adds separate fixed-date/Sunday metadata and reviewed composite appointments. Unresolved selections and uncaptured hours stay qualified or held. Calendar and Synaxarium bytes are unchanged: 366 Coptic days, 868 titles and the same pure calendar converter. Publication remains gated on exact-artifact acceptance.

Read [1.3.7 scope, source evidence and limitations](docs/LECTIONARY_1_3_7_RELEASE.md), the [changelog](CHANGELOG.md) and [Reader check sheet](coptic-reader-check-sheet.md). Earlier npm artifacts are immutable. The [1.3.5 reconciliation](docs/LECTIONARY_1_3_5_RECONCILIATION.md) remains historical evidence, not the candidate's source authority.

- [Package API and schema](packages/lectionary-data/README.md)
- [Current Synaxarium contract and release workflow](docs/SYNAXARIUM_RELEASE.md)
- [Broader lectionary validation plan](docs/LECTIONARY_VALIDATION_PLAN.md)
- [Previous canonical-appointment release](docs/LECTIONARY_1_3_3_RELEASE.md)

The consuming site is `george-andraws/coptic-corpus`, built locally from `/Users/ga/code/coptic-corpus/stgeorge-lessons`. It pins the published version exactly and displays Synaxarium after Praxis using one shared date service. This does not create a saint-to-reading relationship.

The repository has distinct layers: research/capture material, generated reference data under `out/`, and the npm runtime under `packages/lectionary-data`. Do not confuse research Synaxarium bridges with the public titles catalog. Older execution briefs and generated internal specs are historical records, not the current npm contract.

The 1.3.7 runtime builder applies source-owned review repairs after the unchanged design/canonicalization guard and after structural daily fill. Run it in the declared Python dependency environment:

```bash
uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate \
  python -c 'import subprocess; subprocess.run(["node", "scripts/build_npm_package.mjs"], check=True)'
```

Freeze all source writers before final acceptance. Rebuild from a clean checkout, run the full Python and declared Node test inventories with the dependency environment on subprocess PATH, validate the exact packed tarball and compare registry bytes after authorized publication. Do not install this candidate in the site as part of a package-only task. Its three new source-only Kiahk Psalm selections require a bounded consumer-validator qualification when a site upgrade is separately authorized.

## Research-layer build

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

The production catalog is built by `scripts/build_synaxarium.py` from the audited `synaxarium_from_coptic_reader.jsonl` and `coptic_reader_index.json` files, then checked by `scripts/validate_synaxarium.py` and the existing package-integrity gate. See the [current release workflow](docs/SYNAXARIUM_RELEASE.md).

`build_synaxarium_index.py` is a separate legacy research tool producing a St-Takla source map under `out_synaxarium/`. It is not the source of the published Coptic Reader catalog and is not integrated into `BUILD_SUMMARY.json` or `query_lectionary.py`. Preserve its evidence separately; do not ship its raw text, review metadata or bridge records as public catalog fields.

## Bible chapter index

The build also generates a chapter-level index from the reverse passage crosswalk:

- `out/data/bible_chapter_lectionary_index.csv` - one row per supported Bible chapter, including unread chapters
- `out/data/bible_chapter_lectionary_occurrences.csv` - detailed occurrence rows for chapter coverage

Query example:

```bash
python3 out/scripts/query_lectionary.py --chapter "John 2"
```
