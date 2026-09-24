# Pascha Psalm numbering and SUS-source probe

Use this when the requester asks to validate Holy Pascha readings across Coptic Reader, Katameros, St. Mary Ottawa, SUS/St. Pishoy Nashville, or stored repo data, especially when Psalm refs are involved.

## Durable lessons from the Phase 2b Psalm-numbering pass

1. **Do Psalm convention detection before Psalm diffs.** Numeric Psalm mismatches can be convention mismatches, not content mismatches.
2. **Do not assume every Coptic/Pascha source is stored in LXX numbering.** In the local repo, the visible stored Psalm refs in `pascha_day_hour_index.csv`, `pascha_source_text_index.csv`, and Katameros cycle data are mostly English/NKJV/Masoretic-looking, even when the underlying liturgical tradition is LXX.
3. **Bilingual/trilingual books can mix conventions on the same page.** The archived old SUS-path/St. Mark Pascha PDF printed English NKJV/Masoretic headings while Coptic/Arabic labels appeared liturgical/LXX-like. Preserve raw source refs and label the convention.
4. **Coptic Reader fixture Psalm labels can still need screenshot-level verification.** In the Wednesday Day fixture, some Psalm refs looked LXX-like (`Ps 50` vs MT `Ps 51`, `Ps 32` vs MT `Ps 33`, `Ps 40` vs MT `Ps 41`, `Ps 68` vs MT `Ps 69`), but Third/Sixth Hour labels looked MT-like (`Ps 41`, `Ps 83`). Flag instead of forcing a score.
5. **Store canonical Psalm refs with metadata, not by overwriting raw refs.** Recommended fields: `source_ref`, `source_convention`, `canonical_lxx_ref`, `canonicalization_confidence`, `canonicalization_note`.

## Explicit MT/Hebrew ↔ LXX Psalm chapter map

Do not use a flat minus-one offset.

### MT/Hebrew to LXX

| MT/Hebrew Psalm | LXX Psalm |
|---|---|
| `1-8` | same |
| `9-10` | `9` |
| `11-113` | MT minus 1 |
| `114-115` | `113` |
| `116:1-9` | `114` |
| `116:10-19` | `115` |
| `117-146` | MT minus 1 |
| `147:1-11` | `146` |
| `147:12-20` | `147` |
| `148-150` | same |

### LXX to MT/Hebrew

| LXX Psalm | MT/Hebrew Psalm |
|---|---|
| `1-8` | same |
| `9` | `9-10` |
| `10-112` | LXX plus 1 |
| `113` | `114-115` |
| `114-115` | `116`, split by verse range |
| `116-145` | LXX plus 1 |
| `146-147` | `147`, split by verse range |
| `148-150` | same |
| `151` | no Hebrew counterpart |

Verse numbers can also differ because of superscriptions/titles; chapter mapping alone is not enough for authoritative edits.

## Known Wednesday Day examples from the pass

| English/NKJV/MT source ref | Coptic/LXX-looking equivalent in fixture | Note |
|---|---|---|
| `Psalm 51:4` | `Psalm 50:6` | Same text: “That You may be found just when You speak...” |
| `Psalm 33:10` | `Psalm 32:10` | Same text: “The Lord brings the counsel of the nations to nothing...” |
| `Psalm 41:5,7,6` | likely `Psalm 40:6-8` | Needs screenshot-level confirmation for exact fixture label/range. |
| `Psalm 69:17` | `Psalm 68:17` | Standard chapter shift; content aligns. |

## SUS/St. Pishoy Nashville Pascha PDF probe

- The live old URL `https://suscopts.org/stpishoynashville/pascha%20book.pdf` returned `404` during the pass.
- Current SUS/deacons sitemaps and searches did not expose a current live Holy Pascha book PDF.
- Internet Archive had full captures of the old URL. The full 2022 capture was byte-identical to the 2011 capture, but metadata identified it as an old St. Mark / CopticChurch.net Holy Pascha book, not clearly a current SUS/Coptic Reader source.
- The archived PDF states: `Scripture taken from the New King James Version`; no extracted `Septuagint` statement was found.
- Use this archived PDF as a comparator only, not a controlling source for unscreenshotted Holy Week days.

## Re-check conclusions from this pass

- Phase 2a `GreatLentReadings.Id=46` vs `Id=53`: decision unchanged. Live Katameros API supported the shorter Matins Psalm, but the labels are MT/NKJV notation and must be converted before LXX canonical display.
- Hatur 8 `raw_ref=19.68:17,16,17`: dedupe conclusion unchanged. If canonical storage/display becomes LXX, normalize MT `Ps 68` to LXX `Ps 67` chapter-level, with verse-level verification before editing data.
