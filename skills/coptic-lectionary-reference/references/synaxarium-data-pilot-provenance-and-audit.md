# Synaxarium data pilot provenance and audit pattern

Use this when the requester asks to build or validate Synaxarium title data for `@andraws/lectionary-data`, especially before scaling beyond a pilot.

## Provenance gate

Before any data generation, resolve the package source repo:

- Local folder `$REPO_ROOT` may be a stale local name.
- Canonical GitHub repo verified in the Phase A pilot: `https://github.com/george-andraws/coptic-orthodox-lectionary-tools`.
- `npm view @andraws/lectionary-data --json` should be checked against `registry.npmjs.org`; in the 2026-06-28 pilot, version `1.1.8` had repository `git+https://github.com/george-andraws/coptic-orthodox-lectionary-tools.git`.
- Capture raw command transcripts in the artifact folder, not just summarized observations.

## Source-family rules

Treat source families as the unit of attestation:

- `copticchurch_net_family`: CopticChurch.net Synaxarium plus coptic.io Synaxarium data. coptic.io states CopticChurch.net as its Synaxarium source and its canonical JSON entries carry CopticChurch URLs. If any coptic.io title diverges from the live CopticChurch page, reclassify that claim before final attestation.
- `st_takla_family`: St-Takla.org English Coptic Synaxarium month/day pages. This is a separate modern edition family.
- `st_george_chicago_seed`: randogoth/coptic-synaxarium JSON, moved to Codeberg with `synaxarium_coptic.json`. Use as seed and discrepancy evidence only. Do not count it as authority. Its README says “Free to use” but no formal license file was found, so the maintainer and Fr. Boulos should approve any retained seed use.

Carry this caveat forward: modern Synaxaria descend from the medieval compilation attributed to Michael, bishop of Atrib and Malij. Cross-family agreement proves modern edition agreement on inclusion, wording, or order, not historical independence. Use coarse buckets: `consensus`, `single-family`, `disputed`.

## Access patterns

CopticChurch.net:

- All-days list: `https://www.copticchurch.net/synaxarium/all/en`
- Per-day pages: `https://www.copticchurch.net/synaxarium/{monthNumber}_{day}.html?lang=en`
- coptic.io structured data: `https://raw.githubusercontent.com/abanobmikaeel/coptic.io/main/packages/data/src/en/synaxarium/canonical.json`
- Month spellings observed: `Tout, Baba, Hator, Kiahk, Toba, Amshir, Baramhat, Baramouda, Bashans, Paona, Epep, Mesra, Nasie`.

St-Takla month indexes:

- `01-tout.html`, `04-kiahk.html`, `05-toba.html`, `06-amshir.html`, `07-baramhat.html`, `10-beona.html`, `11-abib.html`, `13-nasie.html`
- Real entry links live under a month subfolder such as `/synaxarium/06-amsheer/05-amshir-bishay.html`. Filter out navigation links and day landing links before treating link text as a claim.
- When extracting one St-Takla day from a month index, require both the target day number and the expected month-folder slug, for example `/06-amsheer/30-amshir...`. Same-number cross-month navigation links such as Baramouda 30 can otherwise pollute raw claims.
- Month spellings vary: `Tute/Toot/Tout`, `Tubah/Touba/Topa/Toba`, `Amshir/Amcheer/Meshir`, `Paona/Baona`, `Abib/Epep`, `Nasie/El-Nasi`, etc.

randogoth seed:

- GitHub mirror exposes mainly README and is archived.
- Codeberg API showed `synaxarium_coptic.json` at `https://codeberg.org/randogoth/coptic-synaxarium/raw/branch/master/synaxarium_coptic.json`.

## Pilot artifact pattern

For gateable pilot work, create an artifact folder under `audit_artifacts/`, not package data. Recommended files:

- `source_recon.md`
- `source_recon_raw_evidence.txt`
- `schema_proposal.md`
- `pilot.json`
- `collision_report.md`
- `methodology_note.md`
- `gate_report.md`
- independent audit output and rerun audit output

`pilot.json` should include clean records plus wrapper sections:

- `rawClaims`: exact source titles, family, URL, retrieved timestamp, authority flag.
- `pilotFlags`: all inferred fields, disagreements, transliteration variants, leap-only flags.
- `liveSourceChecks`: sanity checks against live pages.
- `collisionSummary`: normalized duplicate scan.

Keep seed claims in `sources` for traceability, but exclude `st_george_chicago_seed` from record `sourceFamilies` and consensus counts.

## Schema and validation lessons

- Records need opaque immutable ids. Do not encode contested facts in ids.
- `displayGroupId` can include a title slug for render grouping, but downstream code must not use it as the stable join key. Use `id`.
- `members` was useful in the pilot for named pairs and counted collectives. Formalize its sub-field schema before a full build.
- `searchAliases` are for search expansion only. Do not merge identities because of transliteration variants.
- Every inferred `type` and `rank` should get a `pilotFlags` entry. If a source says “Commemoration” and the schema lacks a `commemoration` type, flag the assigned type for the maintainer and Fr. Boulos.
- Nasie 6 must be `validInCommonYear=false`, `validInLeapYear=true`.
- Do not renumber raw claim IDs after cleanup if audit output has already referenced them. A numbering gap is acceptable when no record is missing a claim.
- On full-year reruns, clear generated adjudication brief files before writing the current set. Otherwise stale brief files from a prior over-broad run can survive even when the index is current.
- Keep the grouping type classifier and final record type classifier aligned. If `type_prefix()` treats a word such as `feast` as a type trigger, `infer_type()` should use the same trigger, or the review file can show mismatched type-dispute behavior.
- For adjudication triage, do not classify Ascetic versus Monk as a plain transliteration/display variant. Move it to people-level review unless a human ruling confirms same identity.
- For patriarch records, ordinal and patriarchal-number conflicts are people-level disputes, not display variants. Shared tokens such as patriarch, Alexandria, and pope can cause false similarity matches.
- Source spelling warnings such as CopticChurch `Carpentar` need notes in whichever tier the record lands, not only Tier 3.

## Known pilot stress examples

- `amshir-9`: CopticChurch family lists Severus and James. St-Takla plus seed list Barsauma and Paul. Treat as disputed inclusion.
- `tout-1`: CopticChurch plus seed say Bartholomew martyrdom. St-Takla link text said departure. Treat as disputed title/type.
- `paona-5`: Bshay/Ebsoy/Ebshoy variant. Keep variants in `searchAliases`, not as merged identity proof.
- `amshir-26`: Zadok and 128 companions tests counted collective modeling.
- `nasie-6`: leap-only day.

## Independent audit pattern

Respect the rule that the producer model does not audit its own artifact. If Claude Code CLI is installed but not logged in, do not call that a permanent tool failure. Use configured Hermes one-shot with an alternate provider/model, for example Anthropic Sonnet, and restrict toolsets to file reads:

```bash
hermes -z "$(cat audit_prompt.txt)" --provider anthropic -m claude-sonnet-4.6 -t file --safe-mode --ignore-rules
```

Run at most two audit passes. Apply concrete fixes, rerun once, record remaining blockers and non-blocking issues, then stop at the gate. Do not scale to 366 days or publish before the maintainer approves the pilot method.
