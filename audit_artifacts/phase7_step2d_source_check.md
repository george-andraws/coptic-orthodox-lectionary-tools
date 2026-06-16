# Phase 7 Step 2d Source Check

## Tool note

A Grok 4.3 research worker was launched for this step but timed out before producing an artifact. The source checks below were performed by Codex through direct terminal HTTP pulls and local PDF/text extraction. Step 8 remains the independent Grok audit gate for the produced edits.

## Verdict table

| Item | Verdict | Source basis | Read from source vs inferred |
| --- | --- | --- | --- |
| Coptic Encyclopedia byline | Confirmed. The CCDL API lists creator as `Basilios, Archbishop; Coquin, René-Georges`. | CCDL API item 1199, `creato` field. | Read from source. |
| Youssef Abuqti wording | ACCOT states the Abuqti calculation was developed by Ptolemy al-Farmawi during Pope Demetrius and was attributed to the patriarch. The article treats this as traditional attribution. | ACCOT, `The Arrangement of the Church Lectionary`. | Source states the claim directly; `traditional attribution` is cautious article framing. |
| Youssef 15 weeks or 107 days | Confirmed. ACCOT gives `(15 weeks or 107 days)`. | ACCOT, `The Arrangement of the Church Lectionary`. | Read from source. |
| Arithmetic check | 15 x 7 = 105. | Python calculation in this run. | Computed. |
| Zanetti series and year | Not cleanly confirmed. Open Library says series 33, 1985. The Coptic Encyclopedia PDF bibliography says series 31, 1988. | Open Library OL2304712M JSON and Coptic Encyclopedia `Lectionary` PDF text. | Read from source, conflict unresolved. |
| Burmester page span 83 to 137 | Not confirmed in accessible source pulls. | Crossref, Open Library, Internet Archive, repo local search did not confirm the article record or page span. | Unresolved. |

## Evidence excerpts

- CCDL API item 1199: title `Lectionary`, publication `The Coptic encyclopedia, volume 5`, entry reference `CE:1435a-1437b`, creator `Basilios, Archbishop; Coquin, René-Georges`.
- ACCOT Youssef page: `to the feast of the Descent of the Holy Spirit (15 weeks or 107 days)`.
- ACCOT Youssef page: `there is a long astronomical calculation known as the Abuqti calculation. This calculation was developed in the third century AD by the Egyptian astronomer Ptolemy al-Farmawi ... during the time of Pope Demetrius the Vinedresser ... This calculation was attributed to the patriarch and thus became known as hisab al-karma`.
- Open Library OL2304712M JSON: title `Les lectionnaires coptes annuels`, subtitle `Basse-Egypte`, series `Publications de l'Institut orientaliste de Louvain`, `33`, publish date `1985`, publisher `Université catholique de Louvain, Institut orientaliste`.
- Coptic Encyclopedia `Lectionary` PDF bibliography: `Zanetti, Ugo. Les Lectionnaires coptes annuels, Basse Egypte. Publications de l'Institut orientaliste de Louvain 31. Louvain-la-Neuve, 1988.`

## Open items

- Confirm Burmester's exact article page span from a catalog record, article scan, or BSAC volume scan before adding pages 83 to 137.
- Resolve the Zanetti series/year conflict before adding a series number or year to the article source list.
