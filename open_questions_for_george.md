# Open questions for George

Retained source and editorial questions from the supplied briefs. George's latest request authorizes the combined package update, confident commit/push and npm publication after validation. The earlier Mark request also authorizes a local consumer pin and lectionary rebuild. No site push or deployment is implied. Unanswered questions below remain open; implemented defaults are not presented as George's answers.

- **Q1.** Display names for the Pascha eves: the Coptic form ("Eve of Tuesday," recommended) or the civil form ("Monday night")?
  - The additive package metadata exposes an unambiguous Coptic service identifier and label while retaining both raw source conventions. No website presentation is changed.
- **Q2.** "Epiphany" and "Christmas Fast": normalize in a package display-label field (recommended) or leave the package raw and fix at render time?
  - The requested additive display-label field is supplied. Raw source labels remain unchanged; consumer presentation is not changed.
- **Q3.** Kiahk 23 Matins Gospel: Matt 12:1-8 or Matt 17:1-9, after the Coptic Reader check.
  - Resolved by George's specific investigation request: Reader's weekday table gives Matthew 12:1-8. Its actual Sunday January 2, 2028 Matins gives Mark 3:28-35. The old ordinary-source Matthew 17 table is not explained by that Sunday substitution.
- **Q4.** Displaced feasts (R3): drop them from authoring entirely (recommended), or show them once as "assigned in the annual Katameros"?
  - Still an editorial decision. Seasonal overlap does not by itself establish suppression or universal non-occurrence. No canonical annual-assignment claim was deleted solely from the three shipped years.
- **Q5.** May a row be promoted on printed Pascha-book evidence alone (Gal 3:1-6, Gal 6:14-18, Isa 19:19-25), or only with Coptic Reader evidence (recommended, per 05 locked decision 4)?
  - No exception to the existing Reader-evidence rule was assumed. Galatians 3 remains historical, Galatians 6 has actual retained Reader confirmation, and the Isaiah question remains on the check sheet.

## L1-L10 follow-up questions

- **Q-L1.** Hator 11 Vespers Gospel: Matthew 10:24-33 or Mark 14:3-9?
  - Unanswered. Both source-qualified witnesses carry conflict metadata. No choice or commemoration-specific assignment is inferred.
- **Q-L2.** Is Tout 23's Marian day set intended, or a copy of Tout 21?
  - Unanswered. No reading, span, status or Synaxarium catalog entry is changed.
- **Q-L3.** Should the Tuesday of Pascha day hours stay out of Daily Readings until Coptic Reader confirms them? (Recommended in the brief: yes.)
  - Unanswered. The six explicitly reported suspect appointments are held as instructed; the other Tuesday appointments are not silently removed. Saved Reader Third Hour evidence and conflicting source endpoints are recorded on the check sheet, without adding replacements or settling the broader policy question.

## Combined 1 Timothy and Luke questions

## Metadata and source questions

These questions are retained without answers.

- **Q-T2.** Should superseded provenance rows stay in the consumer-facing reverse index at all, or move to a separate provenance file? This implementation retains every historical witness, including originals inside ordered composite fragments, and explicitly marks removed witnesses as not occurring.
- **Q-LK1.** Abib 26: does Coptic Reader read St. Joseph's Gospels, including Matthew 2:13-23 at the Liturgy, or the prophets' set, including Matthew 23:13-26? Both complete three-Gospel sets remain flagged. Neither is chosen or promoted.
- **Q-LK2.** One month spelling in display labels: the Synaxarium catalog's recommended spelling, or another? Pending an answer, this implementation follows the later Luke recommendation: Tout, Baba, Hatour, Kiahk, Toba, Amshir, Baramhat, Baramouda, Bashans, Paona, Abib, Mesra, Nasie. Hatour supersedes the earlier T-L4 recommendation of Hator.

## Retained source limitations, not answered by inference

- T-L7 requested a copticchurch locator for every confirmation, but the authenticated 1.3.7 Great Thursday Water Liturgy already has a retained Reader source locator and no copticchurch witness for that service. The check sheet keeps all seven appointments and discloses that source difference.
- Two already inactive Exodus witnesses use source week 49. Their labels disclose the unresolved source week. No normal liturgical week, new appointment or current-practice approval is inferred.
- Tout 8's Katameros Matthew 23:13-36 endpoint witness is already inactive in the frozen package. Its unresolved endpoint difference remains on the check sheet, outside the two-current-row conflict total.


## Service evidence policy and edition questions

- **Q-LK3, retained unanswered:** Do Coptic Reader Special captures count as Coptic Reader evidence for rite rows? The current implementation follows the specific authorization to attach authenticated retained captures and the established `current_authority` tier, while preserving every existing current status. This does not answer the broader policy question.
- **Q-TL6-EDITION:** The retained Saint Bishoy Agpeya and Palm Sunday PDF witnesses identify the books, but this review did not establish their revision or publication date. Which precise print editions should be named when those 11 source rows receive fresh Reader checks?

No reading, service assignment or Psalm offset has been supplied from memory. There is no unresolved numeric disagreement after the bounded LK9 repair. The generic chapter-only proposal for MT Psalm 41:9 remains different from its qualified retained Brenton locus, and that qualified mapping is preserved rather than treated as an error.
