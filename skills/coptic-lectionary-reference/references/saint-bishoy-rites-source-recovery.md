# Saint Bishoy rite-source recovery notes

## Durable recovery pattern
Use this when special-service reading tables are still missing after the ordinary lectionary package and known Coptic Reader routes have been checked.

1. Start with the Saint Bishoy deacons-corner rites page:
   - `https://saintbishoy.ca/deacons-corner/church-rites-hymns-for-seasons-and-services/`
2. If a rite family is not linked there, query the WordPress media API directly:
   - `https://saintbishoy.ca/wp-json/wp/v2/media?search=<term>&per_page=50`
3. Good search terms for hidden rite assets:
   - `prostration`
   - `consecration`
   - `myron`
   - `corner`
   - `stone`
   - `chrism`
   - `muron`
   - rite-family English names
4. Download candidate PDFs from each media item's `source_url`.
5. Extract full text locally and capture the printed Pauline / Catholic / Acts / Psalm / Gospel blocks, not just the table-of-contents overview.
6. Publish into the curated local files:
   - `special_service_readings_curated.csv`
   - `special_service_passage_index.csv`
7. Rebuild the reverse crosswalk and verify both:
   - direct rite lookup: `--special-service ...`
   - reverse lookup: `--passage ... --include-crosswalk`

## Recovered source URLs from this session
### Publicly linked on Saint Bishoy
- Baptism: `https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf`
- Wedding / Crowning: `https://saintbishoy.ca/wp-content/uploads/Rites_Wedding_Ceremony.pdf`
- Unction: `https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf`
- Funeral: `https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf`
- Home Blessing: `https://saintbishoy.ca/wp-content/uploads/Rites_Blessing_Houses.pdf`
- Epiphany Laqan / Waters: `https://saintbishoy.ca/wp-content/uploads/Rites_Laqan_Epiphany.pdf`
- Consecration of Churches, Altars and Vessels: `https://saintbishoy.ca/wp-content/uploads/Rites_Book-2_Consecration.pdf`

### Found through WordPress media API
- Pentecost prostrations: `https://saintbishoy.ca/wp-content/uploads/Rites_Prostration_Sagda.pdf`
- Lent / Jonah prostrations: `https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations_Lent_Jonah.pdf`

## Families recovered into the curated dataset
- Wedding / Crowning
- Baptism
- Unction of the Sick
- Funeral major variants
- Home Blessing
- Liturgy of the Waters / Epiphany Laqan
- Church Consecration
- Altar Consecration
- First Prostration
- Second Prostration

## Counts after this pass
- `special_service_readings_curated.csv`: 79 rows
- `special_service_passage_index.csv`: 92 rows

## Still unresolved after this pass
- Myron Consecration
- Cornerstone prayer
- Whether Church Consecration Special Prayer has a distinct reading set beyond the main church-consecration rite

## Interpretation note
The Pentecost prostration book contains both overview summaries and full printed reading pages. Use the overview to locate sections, but treat the printed Psalm / Gospel / Pauline pages as the canonical reading table to store.