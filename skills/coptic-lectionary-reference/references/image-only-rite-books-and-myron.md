# Image-only rite books and Myron extraction notes

Use this when a Coptic rite book is authoritative but not text-extractable.

## Durable workflow
1. Try direct text extraction first.
   - `pypdf`
   - `PyMuPDF`
2. If extraction returns little or no text, treat the PDF as image-only.
3. Render the suspect pages to images.
4. Use macOS Vision OCR on the rendered pages.
5. Do not trust OCR alone for scripture references in Arabic.
6. Visually verify the specific pages that contain the reading table.
7. Normalize references conservatively:
   - if the printed quote makes Psalm renumbering obvious, normalize to modern numbering and note the source numbering
   - if not, preserve the printed numbering and say so in notes
8. Store the result as structured rows by:
   - `service_family`
   - `service_variant`
   - `section`
   - `reading_type`
   - `raw_ref`
   - `source_title`
   - `source_url`
   - `source_page`
   - `notes`
9. Rebuild both:
   - curated special-service table
   - passage index / reverse crosswalk
10. Verify both lookup directions:
   - service -> readings
   - passage -> service hits

## Myron consecration source recovered in this session
Source:
- `https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf`

Recovery method:
- image-only PDF
- local page rendering
- macOS Vision OCR
- visual verification of pages 34-37

Recovered family:
- `myron_consecration`

Recovered variants:
- `consecration_day`
- `first_week_day_1`
- `first_week_day_2`
- `first_week_day_3`

Recovered row count:
- 31 rows

## Pentecost prostration rule from this session
The three Sagda / Prostration services should be modeled under one canonical family:
- `pentecost_prostration`

Canonical variants:
- `first_prostration`
- `second_prostration`
- `third_prostration`

Do not keep stale duplicate alias families if a unified canonical family already exists.

## Documentation rule
When a new special-service family is resolved:
- update the curated dataset
- rebuild the crosswalk
- update the downstream documentation package reference table
- update the missing-tracker note so it stops claiming the family is unresolved

## Remaining open question after this session
- whether `church_consecration_special_prayer` has a distinct reading set separate from the main church-consecration rite
