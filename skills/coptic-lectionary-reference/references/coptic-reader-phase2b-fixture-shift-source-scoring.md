# Coptic Reader Phase 2b Fixture, Eve/Day Shift, and Source Scoring

Use this reference when validating Holy Pascha / Wednesday readings against the maintainer-provided Coptic Reader ground truth.

## Locked fixture pattern

When the requester provides Coptic Reader readings manually or from screenshots, create a locked fixture rather than treating the text as ephemeral chat context.

Recommended path shape:

```text
tests/fixtures/pascha_<day>_<eve-or-day>_coptic_reader.json
```

For Wednesday Day, the fixture created in the repo was:

```text
tests/fixtures/pascha_wednesday_day_coptic_reader.json
```

Fixture conventions:

- Include `locked: true`.
- Record source as `Coptic Reader app`, provided by the maintainer.
- Scope explicitly: season/day/eve-or-day.
- Include Scripture readings only. Liturgical/homiletic items are context unless the requester says to model them.
- Preserve uncertainty flags such as screenshot cutoffs.
- Preserve shown references exactly even when they look odd, e.g. `Proverbs 1:11-35` shown by Coptic Reader despite standard Proverbs 1 ending at verse 33.
- Preserve named non-versed readings such as `Memoirs of Job`; do not invent verse ranges.

## Canonical key before diffing

Before comparing any Pascha source, map all labels onto one key:

```text
pascha:<day>:<eve_or_day>:<hour>
```

Examples:

```text
pascha:wednesday:day:first_hour
pascha:wednesday:day:third_hour
pascha:wednesday:eve:eleventh_hour
```

Mapping rules used successfully:

- Stored dataset `day=Wednesday` -> `pascha:wednesday:day:<hour>`.
- Stored dataset `day=Wednesday Eve` -> `pascha:wednesday:eve:<hour>`.
- St. Mary source-text index uses the same day/hour mapping as stored rows.
- Live Katameros API `First Hour`, `Third Hour`, etc. on a Pascha Wednesday date -> `pascha:wednesday:day:<hour>`.
- Live Katameros API sections like `First Hour Eve of Pascha Thursday` are after Wednesday Day. Map separately, e.g. `pascha:wednesday:eve_after_day:<hour>`, and do not use them as Tuesday-evening/Wednesday-Eve comparator without explicit intent.

Treat mismatch counts computed before canonical mapping as unreliable.

## Wednesday Day Phase 2b findings

Against the maintainer's Coptic Reader Wednesday Day fixture:

| Source | Matches | Rate |
|---|---:|---:|
| Stored `pascha_day_hour_index.csv` | 21/26 | 80.77% |
| St. Mary `pascha_source_text_index.csv` | 15/26 | 57.69% |
| Live Katameros API 2025/2026 | 14/26 | 53.85% |

The Eve/Day shift did **not** explain Wednesday Day:

- Stored Wednesday Day vs fixture: 21/26.
- Stored Wednesday Eve re-keyed against Day fixture: 0/26.
- Missing fixture items not fixed by Eve/Day shift: `Ps 50:6`, `Ps 32:10`, `Memoirs of Job`, `Ps 40:6-8`, `Ps 68:17`.

Therefore, for Wednesday Day, do not frame the issue as a simple off-by-one Eve/Day relabeling. It is genuine content/reference mismatch in specific rows.

## Katameros nuance

Do not collapse live Katameros API and local Katameros SQLite into one source.

Observed in Phase 2b:

- Live API `https://api.katameros.app/readings/gregorian/16-04-2025?languageId=2` and `08-04-2026` returned `title: Pascha Wednesday` with Pascha hour sections and OT prophecies.
- Local `sources/katameros-api/Core/KatamerosDatabase.db` had no Pascha/Holy Week tables; it contained annual/Sunday/Great Lent/Pentecost tables plus metadata/Bible text.

Use conclusions:

- Live Katameros API can be a secondary comparator for Pascha hour-days, but Coptic Reader fixture remains controlling when the maintainer declares it authoritative.
- Local Katameros SQLite is not usable for Pascha hour-days.
- Stored rows marked `api` are partly consistency checks against live Katameros-like source behavior, not fully independent evidence.

## Great Lent Id=46 vs Id=53 re-check

Phase 2a removed `GreatLentReadings.Id=53` and kept `Id=46`. The valid concern was that `Id=53` was a composite, not a pure duplicate:

- `Id=46`: Matins Psalm `Ps 63:1`.
- `Id=53`: Matins Psalm `Ps 63:1 + Ps 64:2-4`.

Best external check performed later:

- Live Katameros API for Thursday of the 7th week of Great Lent, 2025-04-10 and 2026-04-02, returned Matins Psalm `Ps 63:1` and did not include `Ps 64:2-4`.

So the Phase 2a choice is supported, but future duplicate reviews must still treat differing composite references as conflicts requiring external source validation, not silent duplicates.

## Existing verifier pitfall

Current `verify_lectionary_queries.py` Pascha checks can pass while conflicting with Coptic Reader fixture truth. In particular, audit/rewrite before using as correctness evidence:

- `assert_wednesday_pascha_day_hour_corrections()`
- `assert_pascha_source_text_dedupe_invariants()`
- `assert_required_pascha_genesis_rows()`
- relevant Pascha portions of `assert_known_good()`

Do not cite current verifier passing as proof that Wednesday Day matches Coptic Reader until these are rewritten around locked fixture expectations.
