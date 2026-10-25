# Coptic Orthodox Lectionary Tools

Source pipelines, validation tools and the published `@andraws/lectionary-data` runtime package for Coptic Orthodox reading lookup and date-based Synaxarium display.

## Current runtime release

**Version 1.3.5 is published on npm.** The October 25 reconciliation authenticates all 11 registry tar members against the checked-in runtime snapshot and reproduces its reading data from the reconciled builder inputs. The release includes the earlier canonical-appointment corrections plus bounded Bright Saturday, Lamentations and Joel changes. The CommonJS APIs, calendar runtime and audited Coptic Reader single-year 1743 Synaxarium catalog are preserved: 366 Coptic days, 868 titles, exact public field allowlists and one pure calendar converter.

Read [1.3.5 artifact/source reconciliation and retained limitations](docs/LECTIONARY_1_3_5_RECONCILIATION.md) for exact artifact identity, build provenance, verification results and open findings. This is a retrospective source reconciliation, not a new npm publication or website deployment. The package-directory README is deliberately preserved as shipped, including its stale 1.3.0 version prose; this repository README and the reconciliation record supersede that release-status prose.

- [Package API and schema](packages/lectionary-data/README.md)
- [Current Synaxarium contract and release workflow](docs/SYNAXARIUM_RELEASE.md)
- [Broader lectionary validation plan](docs/LECTIONARY_VALIDATION_PLAN.md)
- [Previous canonical-appointment release](docs/LECTIONARY_1_3_3_RELEASE.md)

The consuming site is `george-andraws/coptic-corpus`, built locally from `/Users/ga/code/coptic-corpus/stgeorge-lessons`. It pins the published version exactly and displays Synaxarium after Praxis using one shared date service. This does not create a saint-to-reading relationship.

The repository has distinct layers: research/capture material, generated reference data under `out/`, and the npm runtime under `packages/lectionary-data`. Do not confuse research Synaxarium bridges with the public titles catalog. Older execution briefs and generated internal specs are historical records, not the current npm contract.

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
