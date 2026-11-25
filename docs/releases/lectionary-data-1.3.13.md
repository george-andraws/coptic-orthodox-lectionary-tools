# Lectionary data 1.3.13 — source-qualified Jeremiah follow-up

This successor to the authenticated `@andraws/lectionary-data@1.3.12` artifact implements the explicitly selected Coptic Reader priority for the evidenced current-appointment conflicts below. Registry publication, consumer installation and site deployment are separate operations; this source document does not attest that they occurred. The repository's current-published-release statement remains on the registry-authenticated predecessor until publication is read back.

## Source decisions and complete PK ledger disposition

| Review item | Implemented disposition |
|---|---|
| PK-1 | Preserve the existing structured current Eve/day identities and civil dates. No global renaming or day shift; Good/Great Friday wording is not an identity correction. |
| PK-2 | Correct the working Katameros book transcriptions `Jer 12:1-14` to `Exod 12:1-14` and `Isa 3:5-12` to `Lev 23:5-12`, retaining their raw strings. Reader establishes current Good Friday Eleventh-Hour Exodus 12:1-14, not an additional current Leviticus appointment. Preserve both corrected API witnesses separately inactive and the erroneous originals as inactive audit history. Leave the genuine Ninth-Hour Jeremiah reading unchanged. |
| PK-3 | Reader's Eve-of-Great-Friday Ninth Hour prints Jeremiah 9:7-11. Its bounded five-unit counterpart is named English Brenton Jeremiah 9:6-10; this is not a general Jeremiah numbering map. Preserve API literal `24.9:6-10` as its own inactive variant. Correct only the Ottawa p. 511 historical witness's service from `eve_of_thursday` to `eve_of_friday`; do not relabel all Eve rows. |
| PK-4 | Preserve the already inactive Tuesday Third-Hour candidate, the existing Holy Monday appointment, and the separation between inactive mislabeled Jeremiah and current Ezekiel 43:5-11. Jeremiah 8's verse-10 endpoint at the actual Eve-of-Great-Thursday Eleventh Hour remains on hold; Ottawa p. 365 ends at printed 8:9. No new endpoint or appointment is inferred. |
| PK-5 | No new precedence rule. Bashans 24/June 1, 2026 has Entrance-into-Egypt readings after Pentecost; 2027/2028 differ through seasonal displacement. Preserve the package's descriptive potential-overlap metadata rather than asserting all-three-year suppression. |
| PK-6 | Correct working `Exod 7:2-15` to API Jeremiah 7:2-15 and `Wis 12:13-13:1` to Sirach 12:13-13:1, preserving raw refs and source qualification. Current Great Thursday Sixth Hour follows Reader's Jeremiah 7:1-15 and Sirach 12:13-13:1. The API's 7:2 start is a separately labeled inactive witness, not silently equated with Reader's 7:1. Keep Ottawa's printed Sirach 23:7-14 and historical lifecycle, disclosing that its body corresponds to Sirach 12:13-13:1; do not move this witness to Wednesday. |
| PK-7 | Preserve Bright Saturday Ninth-Hour MT `Ps 41:5,41:10`. Add only named English Brenton covering loci `Ps 40:6; Ps 40:11`, while retaining liturgical source order `Psalm 41:10, 5` / Brenton `Ps 40:11; Ps 40:6` separately. This is neither generic LXX whole-verse equivalence nor a blanket Psalm offset. |

## Evidence and rights boundaries

`sources/jeremiah-followup-1.3.13/source-facts.json` contains a factual projection of retained rendered-source captures, their context, printed references and archive identifiers. Full Reader service bodies are not newly distributed in this source layer or the npm artifact. A digest identifying a privately retained body does not authenticate an absent public body. Public rebuilds authenticate the factual receipt, unchanged corroborating witnesses, source-local API constructors and the published predecessor. Retained observations and recurring named-service materialization are not fresh app attestations for all shipped years. Earlier review nonactivation decisions remain historical records, not retrospectively edited approvals.

## Public and producer contracts

- Package version `1.3.13`; reading schema remains `1.2.0`. Existing exports, `index.js`, `calendar.js`, license and the 366-day/868-title Synaxarium catalog are unchanged.
- The existing source-qualified correction overlay authenticates the old row's source cell before replacement, preserves raw references and emits both CSV and JSONL representations in source order. Missing, empty, forged and ambiguous source/context inputs fail closed.
- The npm builder applies the Jeremiah outer layer **after** the established Good Friday ordering. The deliberately historical `release` intermediate mode remains 1.3.12; the separately named `jeremiah` stage produces this successor.
- Default daily arrays contain only current appointments with complete physical ordering and consecutive `reading_order`. Reverse output keeps inactive original working witnesses, corrected API variants and separately qualified Ottawa printed witnesses. No inactive witness fills a current appointment.
- `jeremiah_followup_json` and `source_disclosure[].jeremiah_followup` are additive evidence cells on affected daily/reverse rows. The Bright Saturday named-edition annotation also uses `edition_psalm_covering_json`. Consumers must transport those cells without treating historical evidence as a second current appointment.
- The complete successor reverse corpus has 12,308 rows, including four new inactive API witnesses and four Reader-current rows. Its authenticated inverse restores all 12,300 predecessor rows, exact order, multiplicity and values before older guards run. Five former working witnesses are held inactive. The current-reading reverse population is 7,663, distinct from the legacy projection-active count.
- Daily current-reading counts are 4,101 (2026), 4,092 (2027), 4,119 (2028). The one-row-per-year decrease is the unsupported Good Friday Leviticus companion, not deleted history. The inverse restores the predecessor's 4,102/4,093/4,120 counts. Other changes replace or annotate appointments, not remove unrelated companions.

## Regression and reproducibility boundaries

Literal Reader expectations, real source-function CSV/JSONL export controls, source/authentication failures, complete forward/replay/inverse checks, lifecycle/context/coordinate/order mutations and boolean/float-for-integer predecessor probes live in `tests/test_jeremiah_followup.py` and `tests/test_jeremiah_followup_contract.py`. The complete authenticated predecessor fixture is outside mutable package outputs. Its SHA-256 is `51459e51f14f3a6593acd3c43e45ce0db6d35e0fd61b73afaeadfa334a6e16a6`.

Historical policy, count, source-fingerprint and order assertions retain their historical domains. Current successor output is authenticated and reversed before applying those oracles; known intermediate 1.3.12 composition is explicitly routed as that version. New earlier authentication refusals do not weaken older generic guard tests. The final run evidence distinguishes the preserved diagnostic RED, focused repairs, renewed complete Python gate, reused byte-matched complete Node gate and exact-archive acceptance; their actual logs/receipts are separate from this source narrative.

Supported mixed Python suite and prepared-input rebuild commands, from repository root:

```sh
TMPDIR="$HOME/.hermes/cache/scratch" \
LECTIONARY_CALENDAR_BASELINE=/absolute/authenticated-1.3.6/package \
uv run --python 3.11 --with beautifulsoup4 --with requests \
  --with convertdate --with pytest python -m pytest tests -v --tb=short -r fE

PYTHONHASHSEED=0 uv run --python 3.11 --with beautifulsoup4 --with requests \
  --with convertdate --with pytest node scripts/build_npm_package.mjs
```

The historical calendar baseline is the authenticated actual 1.3.6 npm artifact, never the successor. Both `.test.cjs` and `test_*.js` Node suites must run with spawned Python in the same dependency environment. Exact tarball qualification includes its full member inventory, strict extracted-package integrity, an isolated offline installation and both exported lookup directions. Package materialization from the prepared source snapshot does not claim a fresh raw-source recapture.

For clean-source provenance, the source/tests/behavioral package are committed first. Rebuilding from that clean commit may change only execution provenance in `meta.json`; a separate metadata-only commit can follow. The archive receipt records its exact source commit, final repository commit, SHA-256/SHA-512 integrity and all member hashes. A frozen archive, not a mutable package directory, is the separately authorized publication input. No push, npm publication or site mutation is part of this producer handoff.
