# Phase 3 Grok Source Ingestion Memo

## Sources Represented

| Source | Authority tier | Role in Phase 3 | Numbering convention |
|---|---:|---|---|
| Coptic Reader app, Pascha Wednesday Day fixture supplied by George | current authority | Current authority for captured Wednesday Day Pascha rows only | LXX liturgical or fixture label, with explicit MT/KJV equivalents where encoded |
| Coptic Encyclopedia, Lectionary entry, Claremont CCDL | scholarly structural | Defines the lectionary structure, four-book model, historical development, and calendar value | Not a row-level readings source |
| Fouad Naguib Youssef, “The Arrangement of the Church Lectionary,” ACCOT | scholarly structural | Explains calendar logic, Sunday cycle, and relation of daily readings to the Synaxarium | Not a row-level readings source |
| Ugo Zanetti, Les lectionnaires coptes annuels, Basse-Egypte | scholarly structural | Bibliographically confirmed scholarly witness cited for annual lectionaries | Content not fully ingested, not a row-level readings source in this packet |
| pierresaid Katameros API SQLite source bundled in repo | working local source | Main local structured source for annual, Sunday, Great Lent, Holy Fifty, and Pascha candidate rows | Mostly MT/NKJV or modern English references, with Psalm equivalence unresolved in flagged cases |
| copticchurch.net date-resolved readings cache, 2020 to 2035 | public current practice reference | Public date-resolved readings used by the existing local package | Modern English reference and MT/NKJV-style reference forms |
| St. Mary Ottawa Holy Pascha extracted text | historical printed witness | Historical Pascha witness retained for comparison, not current authority when it conflicts with Coptic Reader | Mixed extracted printed references, including LXX and MT/KJV Psalm forms needing content validation |
| St-Takla English Coptic Synaxarium day index | Synaxarium source | Day commemoration index and source URL store | Not a row-level lectionary numbering source |
| Special-service readings extracted in the local package | working local source | Local structured special-service rows with source labels and provenance | Modern English reference forms |
| Agpeya readings extracted in the local package | working local source | Local structured Agpeya rows with source labels and provenance | Modern English reference forms |
| Bright Saturday service-order readings extracted in the local package | working local source | Local structured Bright Saturday rows with source labels and provenance | Modern English reference forms |

Represented source counts in the presentation layer:

| Source kind | Rows |
|---|---:|
| copticchurch date-resolved cache | 59,324 |
| Katameros cycle | 6,209 |
| Pascha day-hour rows | 285 |
| Special-service rows | 196 |
| Pascha source-text rows | 153 |
| Agpeya rows | 149 |
| Bright Saturday service-order rows | 36 |
| Coptic Reader Wednesday Day fixture rows | 26 |

Source-key count summary:

| Source | Rows |
|---|---:|
| copticchurch.net date-resolved readings cache | 59,324 |
| Katameros API SQLite | 6,494 |
| Special-service readings | 196 |
| St. Mary Ottawa Pascha | 153 |
| Agpeya readings | 149 |
| Bright Saturday service-order readings | 36 |
| Coptic Reader Wednesday Day fixture | 26 |

Authority classification:

| Category | Sources |
|---|---|
| Current authority | Coptic Reader Wednesday Day fixture, only within captured Wednesday Day scope |
| Public/current-reference | copticchurch.net date-resolved readings cache |
| Local working source | Katameros API SQLite, special-service readings, Agpeya readings, Bright Saturday service-order readings |
| Historical witness | St. Mary Ottawa Holy Pascha extracted text |
| Synaxarium source | St-Takla English Coptic Synaxarium day index |
| Scholarly structural | Coptic Encyclopedia, Fouad Naguib Youssef, Ugo Zanetti |

Confirmed local files in scope:

| File | Status |
|---|---|
| `tests/fixtures/pascha_wednesday_day_coptic_reader.json` | Exists |
| `out/data/pascha_day_hour_index.csv` | Exists |
| `out/data/pascha_source_text_index.csv` | Exists |
| `sources/pdfs/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt` | Exists |
| `sources/katameros-api/Core/KatamerosDatabase.db` | Exists |

## Numbering and Validation

The packet records three presentation numbering convention buckets:

| Numbering convention | Rows |
|---|---:|
| modern English reference | 37,680 |
| MT/NKJV | 28,672 |
| LXX liturgical or fixture label | 26 |

Brenton/KJV Psalm validation posture:

- Psalm identity is not treated as solved by chapter/verse string matching alone.
- Brenton/KJV content anchors are used only for encoded validation examples.
- Coptic Reader Psalm rows are treated as current authority where captured.
- Katameros Psalm rows that appear equivalent but are not content-confirmed remain flagged as `current_psalm_equivalence_unresolved`.
- St. Mary Ottawa Psalm rows remain historical witness rows unless current authority confirms them.
- Exact Psalm identity still requires source-preserving fields and explicit equivalence handling across LXX liturgical numbering and MT/KJV-style references.

Wednesday Day fixture posture:

- 26 Coptic Reader fixture rows are represented.
- 18 rows are shared by Coptic Reader and Katameros API SQLite.
- 7 rows are represented by Coptic Reader fixture only.
- 1 row is shared by Coptic Reader and St. Mary Ottawa.
- Coptic Reader governs current practice for these captured Wednesday Day rows.

Pascha attestation buckets in the packet:

| Bucket | Count |
|---|---:|
| single-source candidate | 260 |
| old-edition only | 152 |
| current confirmed | 26 |
| old-edition only candidate removed | 7 |

Pascha source-combo counts:

| Source combo | Count |
|---|---:|
| Katameros API SQLite only | 267 |
| St. Mary Ottawa only | 152 |
| Coptic Reader fixture plus Katameros API SQLite | 18 |
| Coptic Reader fixture only | 7 |
| Coptic Reader fixture plus St. Mary Ottawa | 1 |

## Caveats

- Coptic Reader is current authority only for the manually supplied Pascha Wednesday Day fixture. It cannot yet be generalized to all Pascha days or hours.
- St. Mary Ottawa Pascha text is useful as a historical printed witness, but it has known extraction and parser caveats.
- Katameros API SQLite and local package rows are working sources, not final current authority when they conflict with the Coptic Reader fixture.
- copticchurch.net is a public current-practice reference, but the packet presents it as a date-resolved cache, not as a Pascha hour authority for the fixture comparison.
- The St-Takla Synaxarium index is confirmed as an index and URL source, not as full-text Synaxarium ingestion.
- Ugo Zanetti is bibliographically confirmed but not fully content-ingested in this packet.
- Psalm equivalence is intentionally conservative. Several Wednesday Day Psalm candidates remain unresolved rather than being forced into agreement.
- Historical candidate rows removed from current confirmation remain visible as removed or historical candidates, not silently discarded.
- The packet confirms that `python3 build_design_deliverables.py` and `python3 verify_design_deliverables.py` passed after identity-key correction, but this memo is not an independent attestation audit.

## Readiness for Attestation

Yes. The ingested and represented source set is sufficient for Codex to compute Phase 3 Pascha attestation, with clear limits.

The packet provides:

- A current-authority Coptic Reader fixture for Pascha Wednesday Day.
- A structured local Katameros source for broad candidate generation.
- A historical printed Pascha witness for comparison.
- Public/current-reference and local working sources for wider context.
- Scholarly structural sources for lectionary framing.
- Synaxarium indexing for commemoration context.
- Explicit authority tiers.
- Explicit source-combo counts.
- Explicit attestation buckets.
- Explicit unresolved Psalm-equivalence statuses.
- Build and verifier pass status after identity-key correction.

Codex can compute Phase 3 Pascha attestation from this set because current authority, local candidates, historical witnesses, and unresolved cases are separated instead of collapsed into one flat source pool.

The correct interpretation is not “all Pascha is fully validated.” The correct interpretation is: “the represented source set is structured enough for Phase 3 attestation computation, while current-authority confirmation is limited to the captured Coptic Reader Wednesday Day fixture.”

## Unresolved Source Gaps

- Full Coptic Reader Pascha coverage beyond Wednesday Day is not ingested in this packet.
- St-Takla Synaxarium full text is not ingested, only the day index and URLs.
- Ugo Zanetti’s content is not fully ingested, only bibliographically confirmed.
- St. Mary Ottawa extraction has known parser caveats and should not override Coptic Reader where they disagree.
- Several Psalm rows remain unresolved pending Brenton/KJV content-anchor validation or equivalent source-level confirmation.
- Katameros-only Pascha rows remain single-source candidates unless confirmed by Coptic Reader, another current authority, or validated equivalence rules.
- Public date-resolved copticchurch.net rows are represented, but they are not a substitute for Pascha day/hour current-authority capture.
- Historical printed witnesses are sufficient for comparison, not sufficient by themselves for current-practice attestation.
