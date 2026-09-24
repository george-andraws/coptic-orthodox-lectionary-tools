# Consecrations book and remaining-gap audit

Use this with `coptic-lectionary-reference` when special-service work reaches consecration families or when the tracker note and the live dataset disagree.

## Durable findings from this session

### 1. Use the consecrations book table of contents to decide whether a supposed missing table is real
The PDF at:
- `https://copticbook.wordpress.com/wp-content/uploads/2023/06/consecrations-ar-en-cop.pdf`

was good enough to answer two different questions:
- extract the explicit Cornerstone reading table
- test whether the Church Consecration "special prayer" should still be treated as a missing reading table

Practical rule:
- inspect the table of contents first
- if a section lists Psalms / Pauline / Gospel / Reading of the Gospel blocks, treat it as a real reading-table target
- if the section only lists prayers, blessings, absolutions, litanies, procession material, or a short blessing, do not keep treating it as an unresolved reading-table gap unless later pages prove otherwise

This prevents wasting time on pseudo-gaps created by tracker drift.

### 2. Cornerstone prayer is now explicit and local
Recovered from the consecrations book:
- Old Testament: `Genesis 28:10-31`
- Pauline: `Hebrews 9:1-10`
- Psalm: `Psalm 127:1; Psalm 122:1-2`
- Gospel: `Luke 9:28-35`

Canonical local family:
- `cornerstone_prayer`

### 3. Pentecost prostrations should live under one canonical family
Do not keep parallel legacy aliases like `first_sagda`, `second_sagda`, or `third_sagda` if the curated dataset already uses a class-level family.

Canonical family used now:
- `pentecost_prostration`

Canonical variants:
- `first_prostration`
- `second_prostration`
- `third_prostration`

If older alias rows exist in the same builder, delete them rather than carrying both names forward.

### 4. Re-audit the tracker note against the live CSV before trusting the gap list
The tracker note lagged behind the actual curated dataset. Before doing fresh research, compare the note's "missing" claims against the current `special_service_readings_curated.csv` families. If the CSV already covers the family, fix the note first.

## Remaining real gaps after this pass
At the end of this session, the only unresolved items were:
- Myron Consecration
- whether the Church Consecration special-prayer path has any distinct reading table beyond the main church-consecration rite

Treat everything else as covered unless a later audit proves otherwise.
