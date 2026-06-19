# Why Source Map

Scope: source list only. No reading-to-occasion commentary is authored here.

## Registry sources that can support why-link research

| Source | Coverage | Full text reachable |
|---|---|---|
| F.N. Youssef, The Arrangement of the Church Lectionary | Coptic calendar logic, seasons, Synaxarium basis, and 69 foundational readings | reachable: ACCOT web page |
| St. Mary Ottawa / UKMID, Katameros of the Days | Weekday and feast dated collections, annual day table, and 69 TOC witness | reachable: hosted PDF |
| St. Mary Ottawa, Holy Pascha eBook | Pascha day and hour readings in printed witness | reachable when local/PDF copy is present |
| Coptic Reader app fixture supplied by George | Current-practice Pascha Wednesday Day fixture only | reachable locally as fixture data |
| St-Takla English Coptic Synaxarium | Daily commemoration titles and source context | reachable: web day pages |
| Coptic Encyclopedia, Lectionary | Structure and historical framing of lectionary books | reachable: CCDL download |
| O.H.E. Burmester, The Coptic-Greek-Arabic Holy Week Lectionary from Scetis | Historical Holy Week reading witness and older Pascha layer | limited: citation/local source needed for full text |
| Ugo Zanetti, Les lectionnaires coptes annuels: Basse-Egypte | Annual Coptic lectionary scholarship | limited: bibliographic/local access |

## Source registry rows reviewed

| source_key | title | edition | confidence | notes |
|---|---|---|---|---|
| coptic_reader_fixture_wednesday_day | Coptic Reader app, Pascha Wednesday Day fixture supplied by George | manual Coptic Reader fixture supplied by George, 2026-06-15 | confirmed_for_wednesday_day_only | Manual fixture from screenshots. Coptic Reader governs current practice where captured. |
| coptic_encyclopedia_lectionary | Coptic Encyclopedia, Lectionary entry, Claremont CCDL | Claremont CCDL item 1199 | confirmed | Defines the lectionary as four books and explains historical development and calendar value. |
| fn_youssef_arrangement | Fouad Naguib Youssef, The Arrangement of the Church Lectionary, ACCOT | ACCOT web article accessed 2026-06-16 | confirmed_for_principles | Explains calendar logic, Sunday cycle, and the relation of daily readings to the Synaxarium. |
| ugo_zanetti_annual_lectionaries | Ugo Zanetti, Les lectionnaires coptes annuels, Basse-Egypte | Publications de l'Institut Orientaliste de Louvain 33, Louvain-la-Neuve, 1985, xxiv + 383 p. | bibliographic_confirmed_content_not_fully_ingested | Standard scholarly study cited by the Coptic Encyclopedia for annual lectionaries. |
| st_mary_ottawa_days | St. Mary Ottawa / UKMID Katameros of the Days, Readings for Week Days and Feasts | first edition, Christmas 1714 A.M., 1998 A.D. | confirmed_local_extraction_and_step1_audit | First edition, Christmas 1714 A.M., 1998 A.D. Source for the 69 dated entries used as bridge taxonomy; alignment with Youssef's 69 foundational reading collections is inferred, not roster-verified. |
| katameros_api_sqlite | pierresaid Katameros API SQLite source bundled in repo | local repo snapshot of pierresaid Katameros API SQLite database | confirmed_local | Main local structured source for annual, Sunday, Great Lent, and Holy Fifty cycle tables. |
| copticchurch_date_resolved | copticchurch.net date-resolved readings cache, 2020 to 2035 | local cache covering 2020 to 2035 | confirmed_local_cache | Date-resolved public readings used by the existing local package. |
| st_mary_ottawa_pascha | St. Mary Ottawa Holy Pascha extracted text | Lent 1734 A.M., 2018 A.D. eBook extracted text | confirmed_local_extraction_with_known_parser_caveats | Useful historical witness. Not current authority when it disagrees with Coptic Reader. |
| st_takla_synaxarium | St-Takla English Coptic Synaxarium day index | St-Takla English web index accessed 2026-06-16 | confirmed_index_not_full_text_ingestion | Used to store day commemorations and source URLs. Full text should be opened when exact wording matters. |
| special_service | Special-service readings extracted in the local package | local package snapshot | confirmed_local | Local structured special-service rows retained with source labels and provenance. |
| agpeya | Agpeya readings extracted in the local package | local package snapshot | confirmed_local | Local structured Agpeya rows retained with source labels and provenance. |
| bright_saturday_service_order | Bright Saturday service-order readings extracted in the local package | local package snapshot | confirmed_local | Local structured Bright Saturday rows retained with source labels and provenance. |

## Open no-source flagging rule

Rows in `out/why_flags.csv` use `reason = "no source for link"` when the coverage row is Pascha or a likely major feast and no placement-level homily or why-link source field is present in the dataset.
## Reachability check from this run

| Source | URL | Status | Content type | Probe bytes |
|---|---|---:|---|---:|
| ACCOT F.N. Youssef article | https://accot.stcyrils.edu.au/fny-read1/ | 200 | text/html; charset=UTF-8 | 256 |
| UKMID Katameros Days PDF | https://ukmidcopts.org/pdf/Katameros_Days.pdf | 200 | application/pdf | 256 |
| UKMID Katameros Sundays PDF | https://ukmidcopts.org/pdf/Katameros_Sundays.pdf | 200 | application/pdf | 256 |
| Coptic Encyclopedia Lectionary entry | https://ccdl.claremont.edu/digital/api/collection/cce/id/1199/download | 200 | application/pdf | 256 |
| St. Bishoy Katameros page | https://saintbishoy.ca/deacons-corner/katameros/ | 200 | text/html; charset=UTF-8 | 256 |

Web search note: live `web_search` was unavailable in this Hermes environment because Firecrawl or portal credits were not configured. No unverified new web sources were added.
