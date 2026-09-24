---
name: coptic-lectionary-reference
description: Look up and explain Coptic Orthodox lectionary usage, readings, Synaxarium/commemoration references, feast/day placement, and source confidence. Supporting skill for Bible-study and lesson workflows, not a primary authoring skill unless the user asks specifically for lectionary information.
category: note-taking
---

Data-engineering, validation, package, and release references live in `references/lectionary-data-ops-registry.md`.
Do not load that registry for ordinary Bible-study lectionary lookup. Load it only for lectionary data/package/repo work.

# Coptic Orthodox Lectionary Reference Skill

## Lectionary and Synaxarium support lane

This skill owns lookup and interpretation of Coptic lectionary usage, readings, feast/day placement, Synaxarium/commemoration references, and source confidence. It supports Bible-study and lesson workflows but does not author the final Bible-study guide or lesson unless the requester asks specifically for lectionary/Synaxarium information.

Report confidence explicitly:
- confirmed
- likely
- uncertain
- absent evidence

When evidence is absent, say so plainly. Do not infer a reading, date, commemoration, saint entry, or feast placement from thematic fit alone.

For lessons and book overviews involving saints, prophets, biblical authors, martyrs, or feasts, provide commemoration findings or absence wording for the primary content skill to include. When a passage has a verified lectionary placement, also explain the spiritual logic of the placement in reader-facing language; do not merely list a day, service, or row number. When a commemorated saint, named Sunday, or feast is tied to the passage, return that name so the study can use it. When evidence is absent, give scoped absence language that can be used in a guide without sounding like a tool report.


For repository data work, use a layered lookup. For ordinary calendar questions, check the date-resolved index and then the reverse crosswalk. For Holy Week / Pascha questions, check extracted Pascha source text and direct day/hour data first, then the reverse crosswalk, then the generated chapter index. Do not call a passage absent until Pascha / Bright Saturday structured data and source text have been checked. Use `references/local-lectionary-data-stack.md` for the dataset map and `references/pascha-source-text-first-verification.md` for the source-text-first Holy Week rule.

Use this skill whenever a task involves:
- identifying what is read on a Coptic Orthodox day
- finding which days a passage appears on
- explaining why a passage is assigned to a feast, fast, memorial, or Holy Week hour
- naming a commemorated saint, feast, or liturgical day tied to a Bible-study passage
- handling Psalm numbering correctly in Coptic lectionary work
- generating Bible studies that need liturgical placement accuracy

## Accessing the Coptic Reader app

For any request to browse, access, or extract Coptic Reader readings, load `references/coptic-reader-accessible-web-verification.md` first. This is the proven primary access workflow, not encrypted-bundle exploration:

- Open `https://copticreader.org/app/` in an isolated browser and enable Flutter accessibility with `document.querySelector('flt-semantics-placeholder')?.click()`.
- Verify the selected civil date and Coptic occasion after confirming the date picker.
- Navigate ordinary readings through Readings > Liturgy; navigate Pascha through Special > Pascha > day/eve > hour.
- Wait for a nonempty same-origin reading iframe, then extract `document.querySelector('iframe').contentDocument.body.innerText`.
- Preserve the printed references and save occasion/hour context with the reading evidence. Do not blindly convert Psalm numbering. No decryption is needed for this rendered-text route.

## Core source of truth

Coptic Reader is the current-practice authority when a scoped, auditable capture conflicts with another source. Preserve its printed references and numbering convention alongside normalized references and source provenance. A context-qualified Monday Eve Sixth Hour fixture confirms Psalm 28:1–2 (LXX; MT Psalm 29:1–2) and Mark 10:32–34; do not mistake the Psalm numbering difference for a source disagreement.

Treat this repository as the primary workflow source. Set `$REPO_ROOT` to its checkout. Use the generated data in `out/data/`, the tracked query helper, and the included references directory. For dataset structure, special services, Coptic Reader verification, and rite-book recovery, load the named `references/` files in this skill rather than assuming an external documentation store exists.

Use the tracked root query helper when possible:
- `query_lectionary.py`
- When invoking passage lookup from a shell or script, pass the passage as one quoted value, e.g. `python3 query_lectionary.py --passage "4 Maccabees 1:1-12" --limit 20`. If a wrapper builds the command, ensure `--passage` is the option name and the whole reference is a single argument; otherwise multi-word book names like `4 Maccabees` can be misparsed before the lectionary data is actually queried.
- If `$REPO_ROOT/query_lectionary.py` fails with a stale relative data path such as `$REPO_ROOT/out/data/copticchurch_passage_index_2020_2035.csv`, use the generated helper instead: `$REPO_ROOT/out/scripts/query_lectionary.py`, run with `workdir=$REPO_ROOT/out`.

## What the skill is for

The lectionary package is built for two-way lookup:

1. **Day -> readings**
2. **Passage -> days / occurrences**

It also includes a special Pascha/Holy Week structure organized by **day and hour**, not just by date.

## Psalm numbering rule

Coptic liturgical Psalm usage is LXX/Septuagint in principle, but the maintainer's local lectionary data and external comparators may store **English/NKJV/Masoretic-looking Psalm references**. Do not assume every stored Pascha or Katameros row is already LXX.

Rule:
- keep every source citation as written and label its convention when known (`lxx_liturgical`, `mt_nkjv`, or `mixed_bilingual`)
- before any Psalm diff or source score, determine the convention of each source and normalize all Psalm refs to one canonical convention
- recommend canonical storage as LXX/liturgical, but preserve `source_ref`, `source_convention`, `canonical_lxx_ref`, `canonicalization_confidence`, and `canonicalization_note`
- if helpful, show MT/NKJV equivalence in parentheses, e.g. `Psalm 50 (MT Psalm 51)`
- do not silently renumber Psalms to Protestant/NKJV style, and do not silently force NKJV-looking stored refs into LXX without reporting the conversion
- do not assume verse boundaries are identical between traditions; superscriptions/titles can shift verses as well as chapters
- do not apply a flat minus-one Psalm offset; use the explicit seam map in `references/pascha-psalm-numbering-and-sus-source-probe.md` for Psalms 9/10, 113-116, 146/147, and 151
- for exact Psalm work, prefer the local Psalm note and LXX-based text over a simple chapter-shifted NKJV lookup
- for Psalms Bible-study work that titles notes by NKJV number with LXX in parentheses, query both the expected LXX/Coptic number and the printed/English number preserved in local crosswalk rows before assigning lectionary usage; Psalm 19 and Psalms 20-22 are known examples where local rows preserve printed/English citations while the Brenton chapter is shifted
- when searching Psalms in lectionary CSVs, avoid broad raw-text matching because `19.` can be the Psalms book code; prefer structured `passage`, `source_ref`, `normalized_ref`, and `normalized_segment` fields, and confirm Agpeya combined-list matches before claiming an hour placement
- when Bible explanation work depends on a Psalm, apply the project's exegesis workflow with the Psalm-numbering rules above

## Day-type significance rule

Do not treat lectionary readings as just calendar assignments. The Church uses them to interpret the day.

Use the companion note `Lectionary Day Types and Reading Significance.md` to classify the day when relevant:
- feast of the Lord
- paramoun / preparation day
- Holy Week / Pascha hour
- Great Lent
- Holy Fifty Days / Pentecost season
- memorial / saint-linked / martyr-linked / hierarchical commemoration

If the local lectionary title and the Synaxarium context matter, do not guess the commemorative type from the passage alone.

## Holy Week / Pascha rule

Treat Holy Week/Pascha as a separate structure.

Use day/hour granularity when needed:
- Hosanna Sunday
- Monday through Wednesday of Holy Week
- Great Thursday
- Good Friday
- Bright Saturday

Do not flatten Pascha into ordinary annual readings.

For Holy Pascha explanations, use a vetted patristic companion source where available, but still verify exact day/hour reading boundaries against repository data and primary Pascha source texts.

For Holy Week / Pascha reverse lookup, source text and direct day/hour rows control over generated chapter indexes. The chapter index is downstream of the Pascha CSV and can inherit CSV mistakes, so use it as verification output, not as the first or final authority when the question is specifically about Pascha. If source text, `pascha_day_hour_index.csv`, reverse crosswalk, and chapter index disagree, fix the upstream Pascha data and regenerate downstream outputs before updating Bible-study guide prose or frontmatter.

For Bright Saturday and other Pascha services, consult the Coptic Reader audit note before assuming the ordinary Katameros is complete:
- `references/coptic-reader-service-audit.md`
- `references/special-services-source-map.md`

## Preferred workflow

When a question asks what is read on a date or why a reading appears:

1. Check the repository's generated data and relevant source note.
2. Use `query_lectionary.py` or the stored data if the answer is already indexed.
3. For Psalm work, check the Psalm numbering note.
4. When searching by passage, try both the full-name and shorthand forms before concluding the passage is absent, e.g. `John 20` and `Jn 20`, `Psalm 51` and `Ps 51`.
5. If a passage still returns no rows, check the reverse lookup crosswalk or summary before calling it a script failure. Treat it as a likely data-gap question unless the passage clearly exists elsewhere in the local package.
6. For direct Coptic Reader validation, first use the accessible rendered web UI workflow in `references/coptic-reader-accessible-web-verification.md`; its same-origin reading iframe provides visible source text without decrypting assets. If that route fails, use the bundle-first/runtime-asset route in `references/coptic-reader-bundle-and-query-verification-2026-05-19.md` and `references/coptic-reader-phase1-validation-and-runtime-assets.md` before trying to scrape the Flutter UI directly. For a validation pass, search repository history for an established access method; inspect generated/encrypted asset manifests only to document endpoint shape unless the requester approves building a comparator pipeline.
4. For feast / memorial / commemorative meaning, check the day-type note.
5. If the question is about a saint, martyr, pope, bishop, or other memorial day and the local data only gives a title, use the day title plus Synaxarium context rather than inventing a category.
6. For Bright Saturday and sacramental services, consult the Coptic Reader service audit notes first, then look for the underlying service page or bundle route before deciding the material is unavailable.
7. For Bright Saturday and other rite-specific services, check the special-services source map before treating the ordinary Katameros as complete.
8. If the service is sacramental, consecratory, funerary, or ordination-related, assume the ordinary annual index is insufficient until a rite-specific source confirms the readings.
9. When a service PDF is found, record both the rite and the exact reading table, then add a reverse-lookup stub if the passage appears in multiple services.
10. When the lookup script is being verified, test both directions: date -> readings and passage -> date/occurrence. Use normalized shorthand query forms from the data first, then extend the matcher only if needed.
11. For Coptic Reader bundle work, treat `main.dart.js` as a route map. Search for service-family names, then look for `documentPath`, `documentTitle`, `menuHierarchyIds`, and `historyDocumentPaths` metadata before trying browser navigation.
12. If direct curl is blocked, use a browser-context fetch on the bundle; that has been a reliable fallback for route discovery.
13. Treat bundle discovery as provisional until a page-level reading table or explicit service PDF confirms the readings.
14. If a user asks for future Bible-study placement or reverse lookup, prefer the normalized local crosswalk files and only fall back to raw prose notes when the data file lacks the form you need.
15. When a passage lookup confirms a special-service placement for an existing Bible-study note, do not stop at answering the lookup. If the user asks to update the note, propagate the placement into frontmatter, liturgical explanation, teacher notes, and source notes; remove any prior "verify before asserting" language; verify with the currently supported `query_lectionary.py` options plus the normalized crosswalk/source files directly. Do not use the stale `--include-crosswalk` flag unless `--help` shows the local helper supports it. Flag existing audio as stale when the source Markdown changes.
15. If special-service tables are missing, prefer explicit rite-book PDFs before more app-bundle archaeology. The durable path is: recover the rite PDF, extract the exact reading table, publish curated CSV + passage-index files, then feed them into the reverse crosswalk as `source_kind=special_service`.
16. When you add a new service family, verify both direct rite lookup and reverse-crosswalk lookup before considering the dataset usable.
17. For Saint Bishoy-hosted rite books, prefer the deacons-corner rites page first, then query the WordPress media API at `https://saintbishoy.ca/wp-json/wp/v2/media?search=<term>&per_page=50` when expected PDFs are not linked publicly. This surfaced hidden assets such as `Rites_Prostration_Sagda.pdf` and `Rites_Prostrations_Lent_Jonah.pdf`.
18. Treat WordPress media discovery as a class-level recovery tool, not a one-off hack: search with rite-family terms like `prostration`, `consecration`, `myron`, `corner`, `stone`, `chrism`, and `muron`, then download any matching PDFs directly from `source_url`.
19. When a recovered rite book gives an overview list plus printed page-level readings, use the overview only to orient the sections; store the actual printed Pauline/Psalm/Gospel blocks as the canonical table.
20. For consecration-family work, inspect the rite-book table of contents before deeper extraction. If the section exposes Psalms / Pauline / Gospel blocks, treat it as a real reading-table target. If it only exposes prayers, blessings, absolutions, litanies, or procession material, do not keep calling it a missing reading-table gap unless later pages prove otherwise.
21. Before starting fresh recovery work on "missing" special services, compare the tracker note against the live `special_service_readings_curated.csv` families. Fix tracker drift first so you do not research a family that is already covered.
22. Keep canonical family naming in the curated dataset. For Pentecost prostrations, use one class-level family `pentecost_prostration` with explicit variants `first_prostration`, `second_prostration`, and `third_prostration`; remove stale legacy aliases instead of publishing both names.
23. When Coptic Reader screenshots reveal a feast-specific Laqan table, preserve the existing class-level family and add a distinct feast variant rather than merging it into Epiphany or a generic waters rite. Archive the screenshots, update the source generator, rebuild downstream indexes and design deliverables, and verify both direct-service and reverse-passage lookup. If publishing the npm package, also follow the clean-provenance, tarball-install, registry-install, and stash-restoration release steps in `references/coptic-reader-feast-specific-laqan-ingestion.md`.

## Accuracy guardrails

- Do not guess lectionary placement from memory.
- During lectionary pipeline audits, do not repair downstream documentation links unless the requester explicitly includes link repair in scope. Run broken-link checks as verification and report findings, but do not rewrite links just because a check found them.
- When maintaining Coptic Orthodox Lessons notes, preserve existing `lectionary` frontmatter strings on chapter guides and do not fabricate a placement to fill metadata. If the local index does not support a passage occurrence, omit or leave the field unchanged and report the uncertainty.
- If deriving `passages` for Psalm study-guide frontmatter, use the note's `psalm_nkjv` value as the NKJV/Masoretic source and preserve `psalm_lxx` for crosswalks. If split/merged numbering looks irregular, flag it rather than guessing.
- Do not mix MT and LXX Psalm numbering in the same line without labeling both.
- Do not assume a passage has only one liturgical use.
- Do not assume every memorial day is labeled cleanly in the scraped data.
- Do not assume the ordinary annual Katameros contains all readings for Bright Saturday, baptisms, weddings, ordinations, or unction of the sick.
- Do not conflate the crowning Gospel with the Wedding at Cana miracle; crowning commonly uses Matthew 19:1-6 unless a source explicitly says otherwise.
- If the exact commemorative identity is unclear, say so and suggest checking the Synaxarium or the local title.
- If a special-service source is only partially recovered, mark it as partial instead of filling gaps from inference.

## When to apply this skill during Bible explanation work

If a Bible-study or passage explanation asks where the passage is read, why it is read, or what liturgical day it belongs to, this skill should be consulted before writing the answer.

Use it alongside the project's passage-exegesis workflow whenever a passage explanation needs liturgical placement accuracy.

## Practical output standard

When answering a lectionary question, give:
- the day or passage lookup result
- the liturgical context
- any Psalm numbering clarification if relevant
- any caution if the day type is only partially supported by local metadata
- for special services, the rite name plus the recovered reading table, or an explicit gap note if only part of the service is sourced

Be direct. Prefer exact references over broad summaries.

## Special-services gap tracking

If the task moves beyond the ordinary annual lectionary, maintain a temporary gap list in the source map note rather than mentally filling missing readings from familiarity. Treat the gap list as part of the deliverable until the rite-specific source is recovered.
