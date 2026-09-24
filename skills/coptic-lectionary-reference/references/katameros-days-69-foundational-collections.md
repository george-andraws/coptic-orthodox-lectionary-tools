# Katameros of the Days: extracting the 69 foundational collections

Use when the requester asks about F.N. Youssef's 69 `al-qira'at al-asasiyya` / foundational readings, the second volume of the Yearly Katameros, or the weekday/feast collection list.

## Durable finding

The UKMID/Ottawa PDF `Katameros_Days.pdf` exposes a clean table of contents that reconciles exactly to Youssef's count:

- Source URL tried successfully: `https://ukmidcopts.org/pdf/Katameros_Days.pdf`
- Title: `Katameros of the Days: Readings for Week Days and Feasts`
- TOC pages: PDF pages 23-26 in the extracted PDF page numbering
- TOC result: 69 dated reading-section entries
- Unique printed reading pages: 69
- Inferred date entries: 0

Do not reproduce reading bodies. Extract only TOC/date/section-heading metadata unless the requester explicitly asks for source-text verification.

## Extraction pattern

1. Download the PDF to scratch space, not into the repo unless the task asks for artifacts:

```bash
mkdir -p /tmp/coptic-lectionary-sources
python3 - <<'PY'
from pathlib import Path
from urllib.request import Request, urlopen
url='https://ukmidcopts.org/pdf/Katameros_Days.pdf'
out=Path('/tmp/coptic-lectionary-sources/Katameros_Days.pdf')
req=Request(url, headers={'User-Agent':'Mozilla/5.0'})
with urlopen(req, timeout=120) as r:
    out.write_bytes(r.read())
print(out, out.stat().st_size)
PY
```

2. Use `pypdf` or another installed PDF library to inspect the first 30 pages and confirm the title/front matter.

3. Parse the TOC dated entries with month/day/page regex. The TOC entry form is `day month printed_page`, after removing control characters such as `\x1f`.

4. To extract English headings, do not rely on a single PDF-page offset because printed page and PDF page offsets can shift. Cache each PDF page's extracted text once, scan for uppercase dated heading lines such as `8TH DAY OF TUT`, then collect title lines until `Vespers`.

5. Keep both raw and normalized title fields if the list will become data. The PDF contains typos/OCR-like spellings (`Relice`, `Commemeration`, inconsistent capitalization). The report may normalize obvious spelling, but data should preserve source text.

## Candidate 69 list source shape

The TOC dates in order are:

1. 1 Tut
2. 2 Tut
3. 8 Tut
4. 16 Tut
5. 17 Tut
6. 18 Tut
7. 19 Tut
8. 21 Tut
9. 26 Tut
10. 12 Babah
11. 14 Babah
12. 22 Babah
13. 27 Babah
14. 8 Hatur
15. 9 Hatur
16. 12 Hatur
17. 15 Hatur
18. 17 Hatur
19. 22 Hatur
20. 24 Hatur
21. 25 Hatur
22. 27 Hatur
23. 28 Hatur
24. 29 Hatur
25. 22 Kiyahk
26. 28 Kiyahk
27. 29 Kiyahk
28. 30 Kiyahk
29. 1 Tubah
30. 3 Tubah
31. 4 Tubah
32. 6 Tubah
33. 10 Tubah
34. 11 Tubah
35. 12 Tubah
36. 13 Tubah
37. 22 Tubah
38. 26 Tubah
39. 30 Tubah
40. 2 Amshir
41. 13 Baramhat
42. 29 Baramhat
43. 23 Baramudah
44. 27 Baramudah
45. 30 Baramudah
46. 1 Bashans
47. 10 Bashans
48. 20 Bashans
49. 24 Bashans
50. 26 Bashans
51. 2 Baunah
52. 16 Baunah
53. 30 Baunah
54. 3 Abib
55. 5 Abib
56. 20 Abib
57. 3 Misra
58. 13 Misra
59. 17 Misra
60. 25 Misra
61. 26 Misra
62. 28 Misra
63. 29 Misra
64. 30 Misra
65. 1 Al-Nasi
66. 2 Al-Nasi
67. 3 Al-Nasi
68. 4 Al-Nasi
69. 6 Al-Nasi

## Cross-check notes

- St. Bishoy Deacons' Corner exposes 13 monthly `Katameros_Days_Readings_*.pdf` files through its WordPress media API. Use `https://saintbishoy.ca/wp-json/wp/v2/media?search=Katameros%20Days&per_page=50` and read `source_url` values.
- Those PDFs are useful for month-level cross-checks and reading-table recovery, but the Ottawa/UKMID PDF TOC is cleaner for the 69 collection list.
- If ACCOT/Youssef page requests return HTTP 406 in Python, retry with `curl -L --compressed` and browser-like `User-Agent`/`Accept` headers. Capture this as a fetch pattern, not as a claim that the site is unavailable.

## Youssef audit anchor facts

When auditing article/spec wording against Fouad Naguib Youssef, check for these facts explicitly:

- two calendars: Coptic calendar plus Hebrew calendar
- Resurrection date follows the Hebrew calendar/Paschal rule, with Abuqti calculation / `hisab al-karma`, Ptolemy al-Farmawi, and Pope Demetrius the Vinedresser
- three seasons: sowing/Father/Incarnation; harvest/Son/Redemption; flooding/Holy Spirit/Church
- movable middle season: Saturday before Great Lent to Pentecost, 15 weeks / 107 days
- Sunday program overrides weekday program; weekday readings follow the Synaxarium
- Sunday program: four Sundays per month, two-month/eight-Sunday programs, fifth-Sunday 29/30 rules
- seven Major Feasts, seven Minor Feasts, and two Feasts of the Cross contribute to the yearly program
- 69 foundational readings are organized by commemoration type and collected in volume 2 of the Yearly Katameros
