# Psalms Bible-study lectionary lookup pitfalls

Use this when a Psalms Bible-study note needs Coptic lectionary usage, especially after Psalm 9 where NKJV and LXX numbering are shifted.

## Durable lessons

- Query both numbering layers:
  - Brenton/LXX chapter for the Scripture block and Orthodox/Coptic numbering.
  - Printed/NKJV Psalm references preserved in local lectionary rows, especially in Pascha and date-resolved data.
- Continue from the actual project index, not from conversation memory. When the requester says "next few Psalms," inspect `Psalms Bible Study Index.md` and find the first `Planned` tracker row before drafting.
- Avoid raw-string scans for `Ps 19` / `Psalm 19` across all lectionary files. Raw encoded refs may contain `19.` as the Psalms book code, creating broad false positives.
- Prefer structured fields:
  - `reverse_lookup_crosswalk.csv`: `passage`, `source_ref`, `source_kind`, `liturgical_place`, `service_section`, `reading_type`.
  - `katameros_cycle` data: `normalized_ref` and `normalized_segment`, not `raw_ref` alone.
  - `pascha_day_hour_index.csv`: day/hour + `refs` for Holy Week/Pascha structure.
- Treat Agpeya rows carefully. A combined `canonical_ref` list can print many `matched_ref` values in debug output. Confirm the target Psalm is actually part of that hour before adding it to the note.

## Known examples

- Psalm 20 (NKJV) uses Brenton/LXX Psalm 19, but local rows include printed `Ps 20` for Third Hour, Holy Fifty Days Saturday of the third week, and First Sunday of Abib / Apostle's Feast Vespers.
- Psalm 21 (NKJV) uses Brenton/LXX Psalm 20, with printed `Ps 21` rows for Second Sunday of Tout and many annual fixed-day liturgies.
- Psalm 22 (NKJV) uses Brenton/LXX Psalm 21, but Good Friday/Pascha rows cite printed `Ps 22` for Passion prophecy. Query printed `Ps 22` explicitly before writing its Coptic usage.

## Psalm 56-58 caution case

For NKJV Psalms 56-58, do not blindly assign rows by the visible Psalm number:

- NKJV Psalm 56 = LXX Psalm 55. Local rows that cite `Ps 56:6` around Holy Fifty Days may fit LXX Psalm 56's exaltation refrain more naturally than NKJV Psalm 56. Treat this as a numbering caution unless the source text confirms the NKJV verse.
- NKJV Psalm 57 = LXX Psalm 56. Verified usage can include Agpeya Sixth Hour and Veil Prayer, Great Lent Matins rows, Holy Fifty Days Tuesday/Wednesday of the third week, and annual Baba Matins rows. Include the numbering caveat when a row cites `Ps 56:6` beside Psalm 57 rows.
- NKJV Psalm 58 = LXX Psalm 57. Verified Pascha use includes Great Thursday Eve Sixth Hour, `Ps 58:2` with `Ps 68:21` and the Gethsemane Gospel readings.

## Output rule

When writing the Coptic usage section, say which numbering layer is being used. Example: `The project title is Psalm 22 (LXX 21); local Pascha rows preserve the printed Psalm 22 references.`
