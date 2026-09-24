# Special-service extraction and integration notes

Use this reference when extending the maintainer's local Coptic lectionary package beyond the ordinary annual Katameros and Pascha datasets.

## What was recovered successfully
Direct Saint Bishoy service-book downloads were usable for exact-table extraction:

- Service-books index: `https://saintbishoy.ca/service-books/`
- Baptism: `https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf`
- Wedding/Crowning: `https://saintbishoy.ca/wp-content/uploads/Rites_Wedding_Ceremony.pdf`
- Unction of the Sick: `https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf`
- Funeral readings: `https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf`

## Durable extraction pattern
1. Prefer explicit rite books over app UI scraping when a service-family table is missing.
2. Download the rite PDF directly and extract the text locally.
3. Build a curated row set with these columns at minimum:
   - `service_family`
   - `service_variant`
   - `section`
   - `reading_type`
   - `raw_ref`
   - `source_title`
   - `source_url`
   - `source_page`
   - `notes`
4. Build a normalized passage index from the curated rows using the shared passage-normalization helpers.
5. Publish both files into local `out/data/` and the downstream documentation package lectionary reference folder.
6. Feed the normalized special-service passage index into `reverse_lookup_crosswalk.csv` as `source_kind=special_service`.
7. Regenerate the query helper and verify both:
   - direct rite lookup
   - passage lookup with `--include-crosswalk`

## Builder and helper additions that should persist
- Add a dedicated builder step before reverse-crosswalk generation so special-service data is not a manual sidecar.
- Keep a direct helper mode for rite-family lookup, e.g. `--special-service wedding`.
- Preserve `--include-crosswalk` as the opt-in broad reverse-lookup mode. Do not merge special-service rows into ordinary passage output by default.

## Curated coverage captured in this pass
### Wedding / Crowning
- Main rite:
  - `Ephesians 5:22-6:3`
  - `Psalm 19:5; Psalm 128:3`
  - `Matthew 19:1-6`

### Baptism
- Mother absolution, male child:
  - `Hebrews 1:8-12`
  - `Psalm 32:1-2`
  - `Luke 2:21-35`
- Mother absolution, female child:
  - `1 Corinthians 7:12-14`
  - `Psalm 45:9; Psalm 45:13`
  - `Luke 10:38-42`
- Sanctification of baptismal water:
  - `Titus 2:11-3:7`
  - `1 John 5:5-20`
  - `Acts 8:26-39`
  - `Psalm 32:1-2`
  - `John 3:1-21`

### Unction of the Sick
All seven prayers were recoverable from the rite book and should be treated as exact tables, not inferred summaries.

### Funeral
Recovered major variants:
- men main
- women main
- women during delivery
- male children
- female children
- third day / memorials
- Passion Week burial-site overrides for several variants

## Verification cases that proved the integration
Direct rite lookup:
- `python3 out/scripts/query_lectionary.py --special-service wedding`
- `python3 out/scripts/query_lectionary.py --special-service women_delivery`

Reverse-crosswalk checks:
- `python3 out/scripts/query_lectionary.py --passage "1 Kings 17:17-24" --include-crosswalk`
- `python3 out/scripts/query_lectionary.py --passage "1 Thessalonians 4:13-18" --include-crosswalk`
- `python3 out/scripts/query_lectionary.py --passage "John 16:20-23" --include-crosswalk`

## Remaining gaps after this pass
Still not curated from explicit rite books in this workflow:
- Myron Consecration
- Altar Consecration
- Church Consecration special prayer
- Home Blessing
- Liturgy of the Waters
- First Prostration
- Second Prostration
- Cornerstone prayer

## Guardrails
- Do not treat the ordinary annual index as sufficient for sacramental, funerary, consecratory, or ordination-related services.
- Do not treat app route discovery alone as authoritative if an explicit rite PDF is available.
- When a Passion Week burial-site override is given and the rite says Psalm/Gospel are read "as before," preserve the explicit override as a separate row and keep a note rather than inventing a flattened combined table.
- Prefer class-level curated datasets over one-off session notes when the user wants future Bible-study generation to reuse the data.
