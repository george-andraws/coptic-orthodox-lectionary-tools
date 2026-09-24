# Pascha source-text-first verification

Use this when a Coptic Orthodox lectionary task involves Holy Week / Pascha readings, especially reverse lookup for a Bible-study guide.

## Failure mode this prevents

A generated reverse lookup or chapter index can look authoritative while inheriting an upstream Pascha table error. In the Genesis audit, the local `pascha_day_hour_index.csv` had duplicated the Monday Ninth Hour Eden/Fall row under Tuesday Ninth Hour and did not surface the Great Thursday water-blessing Genesis 18 row through the generated chapter lookup. The extracted Holy Pascha source text exposed the problem.

## Rule

For Holy Week / Pascha, do not start or end with the generated chapter index alone. Treat the source-text/day-hour layer as controlling when it conflicts with generated artifacts.

Preferred evidence hierarchy for Pascha:

1. Extracted Holy Pascha source text or rite book by exact day/hour/service.
2. `pascha_day_hour_index.csv` direct day/hour rows.
3. `reverse_lookup_crosswalk.csv`.
4. `bible_chapter_lectionary_index.*`.
5. Bible-study guide frontmatter/prose.

If layers disagree, do not choose the generated layer by convenience. Inspect the source text, correct the upstream CSV, regenerate downstream outputs, and then update guide text/frontmatter.

## Required checks for Bible-study lectionary updates

When adding or revising Holy Week / Pascha placement in a Bible-study note:

1. Query the packaged helper from the lectionary package or repo root, not an old copied helper.
2. Run direct day/hour lookup when the service is known, e.g. `--pascha-day "Tuesday" --hour "Ninth Hour"`.
3. Run chapter/passage reverse lookup after the data is regenerated.
4. Search the extracted Pascha source text for the passage or book name if any row is missing, duplicated, or surprising.
5. Compare source-text rows against generated CSV rows for the affected book.
6. If a row is missing or wrong, fix `pascha_day_hour_index.csv` or the builder input first, then regenerate:
   - `pascha_day_hour_index.*`
   - `reverse_lookup_crosswalk.*`
   - `bible_chapter_lectionary_index.*`
   - `bible_chapter_lectionary_occurrences.*`
   - packaged `scripts/query_lectionary.py` and `passage_normalization.py` if helper behavior changed.
7. Copy regenerated artifacts into the downstream documentation package package only after verification.
8. Patch Bible-study guide body, frontmatter `lectionary`, teacher/source notes, and resource index together.
9. Run broken-link checks on the affected Bible-study and Lectionary folders.
10. Record durable source corrections in the daily assistant log and, when appropriate, a small machine-readable JSON provenance note beside the lectionary data.

## Genesis validation rows from the 2026-06-06 correction

These are regression checks for this failure class:

- Monday of Holy Pascha, First Hour, OT1: `Gen 1:1-31; Gen 2:1-3`.
- Monday of Holy Pascha, Ninth Hour, OT1: `Gen 2:15-25; Gen 3:1-24`.
- Tuesday of Holy Pascha, Ninth Hour, OT1: `Gen 6:5-9:7`.
- Wednesday of Holy Pascha, Ninth Hour, OT1: `Gen 24:1-9`.
- Great Thursday, Ninth Hour, OT1: `Gen 22:1-19`.
- Great Thursday, Ninth Hour, OT3: `Gen 14:17-20`.
- Great Thursday, Liturgy of Blessing of the Water, OT1: `Gen 18:1-23`.
- Good Friday, Third Hour, OT1: `Gen 48:1-19`.

At minimum, future Pascha lectionary builds should verify Genesis 1, Genesis 6, Genesis 18, and Genesis 48 from the packaged helper and from the data files directly.