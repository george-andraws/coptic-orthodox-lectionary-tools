# Coptic Orthodox Lectionary Tools

Source pipelines, validation tools and the published `@andraws/lectionary-data` runtime package for Coptic Orthodox reading lookup and date-based Synaxarium display.

## Current runtime release

**`@andraws/lectionary-data@1.3.11` is the verified published runtime release.** It adds bounded Brenton covering annotations, Theophany/Apostles Waters daily groups, bounded working-cycle first-Lent-Monday materialization with the printed Exodus difference disclosed, retained Bright Saturday supplements including chapter-range Revelation and source-only Distribution, and the bounded Joseph 2027 and Amshir 7 2028 supplements. These are not fresh Reader attestations or authority promotions. Synaxarium remains 366 Coptic days and 868 titles.

Read the [package corrections](packages/lectionary-data/README.md), [changelog](CHANGELOG.md), and [1.3.11 receipt](docs/releases/lectionary-data-1.3.11.json). The [1.3.10 release](docs/LECTIONARY_1_3_10_RELEASE.md) and its [receipt](docs/releases/lectionary-data-1.3.10.json) remain immutable historical evidence.

- [Package API and schema](packages/lectionary-data/README.md)
- [Current Synaxarium contract and release workflow](docs/SYNAXARIUM_RELEASE.md)
- [Broader lectionary validation plan](docs/LECTIONARY_VALIDATION_PLAN.md)
- [Previous canonical-appointment release](docs/LECTIONARY_1_3_3_RELEASE.md)

The consuming site is `george-andraws/coptic-corpus`, built locally from `/Users/ga/code/coptic-corpus/stgeorge-lessons`. It pins the published version exactly and displays Synaxarium after Praxis using one shared date service. This does not create a saint-to-reading relationship.

The repository has distinct layers: research/capture material, generated reference data under `out/`, and the npm runtime under `packages/lectionary-data`. Do not confuse research Synaxarium bridges with the public titles catalog. Older execution briefs and generated internal specs are historical records, not the current npm contract.

The runtime builder applies ordered source-owned review repairs after the unchanged design/canonicalization guard and structural daily fill. The 1.3.10 final stages apply the Deuteronomy/display repairs, then the qualified Good Friday history and daily exclusion. Run it in the declared Python dependency environment:

```bash
uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate \
  python -c 'import subprocess; subprocess.run(["node", "scripts/build_npm_package.mjs"], check=True)'
```

For future releases, freeze source writers, prefer a clean source checkout, run the full Python and declared Node inventories with the dependency environment on subprocess PATH, validate the exact packed archive and compare registry bytes after authorized publication. The 1.3.11 archive records clean source at `ec7d4f1`; its metadata commit does not change reading bytes. The 1.3.10 receipt still records that release's dirty source truthfully. Consumer upgrades require separate authorization and real parser/validator checks for both source-only empty coordinates and numeric coordinate holds. The 1.3.10 site upgrade completed those checks; the 1.3.11 site generation and tests remain outstanding.

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
