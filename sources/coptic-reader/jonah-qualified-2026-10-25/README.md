# Jonah Fast source-qualified repair — 2026-10-25

## Scope and interface

`jonah_fast_source_supplements.apply_jonah_fast_supplements(date, day_title, rows)` returns a fresh repaired source-row list. The parent must call it inside `parse_copticchurch_html` **after existing corrections/recurring supplements, before constructing metadata and before the generic candidate-Matins opt-in**. No main builder, generated data, package, policy, or old fixture was edited by this patch.

The adapter authenticates `source-contract.json`, every listed portable evidence file, and the separate `sources/user-corrections/jonah-fast-2026-10-25.json` authorization on each qualifying call. The contract and authorization SHA-256 values are pinned in code. The supported scope is exactly 2020–2035 at Pascha offsets -69/-68/-67 under the three literal existing aliases. Computed recurrence is a new narrowly authorized policy, **not additional primary-source attestation**.

Regular dates produce eight current appointments, in source order: Matins Prophecy/Psalm/Gospel, then Liturgy Pauline/Catholic/Acts/Psalm/Gospel. No current Vespers rows are emitted. Monday's conflicting seven old appointment groups are retained as explicit inactive history; the preexisting two inactive Vespers rows are preserved verbatim. Tuesday and Wednesday preserve correct original nonprophecy raw/canonical strings and retain the replaced Psalm rows as inactive history.

The exact 2022-02-15 and 2033-02-15 Presentation exceptions add only the seasonal prophecy, preserve supplied feast companions and their order, retain/suppress Vespers as history, and carry the separately authenticated exact-date collision witnesses in `jonah_collision_witness_json`. A partial collision input does not cause invention of missing feast companions.

## Evidence and authority

- `2026-02-02/`, `2026-02-03/`, `2026-02-04/`: full retained bilingual Matins and Liturgy documents, selected contexts/pickers, capture manifests, reading/service menus, and heading/context screenshots. These are reused captures, not fresh retrieval.
- `2022-02-15/`, `2033-02-15/`: retained Presentation Matins prophecy and Psalm/Gospel children with selected context, menu and capture evidence.
- `original-source-only-records.json` and `original-receipts/`: source-only records and byte-preserved original independent receipts. **Their original false canonical/recurrence/runtime flags remain false.** These receipts do not approve the new adapter.
- `bible/`: public-domain retained KJV/Brenton witnesses, a short previously retained NKJV boundary excerpt, and the new bounded Psalm clause-alignment ledger. Local Brenton XML excerpts preserve actual verse anchors. No live Bible or Reader request was used.
- `input-contexts.json`: frozen actual existing parser inputs for all 48 supported civil dates. This is an input-identity gate, not a Reader reading-table oracle.
- The separate user-correction file records current explicit user authorization. `independent_review_approved` / `independent_runtime_review_approved` remain false. No independent approval is fabricated. Reader app version is unavailable.

## Coordinate adjudication and limits

Keep `printed_ref`, the source edition/body, and `normalized_ref` distinct. The canonical coordinates are **bounded covering parallel loci**, not certification that every word of a modern full verse is read or that Reader is verbatim NKJV/Brenton.

| Appointment | Literal Reader reference | Modern covering coordinates |
|---|---|---|
| Monday prophecy | Jonah 1:1-2:1 | Jonah 1:1-17 |
| Tuesday prophecy | Jonah 2:2-10 | Jonah 2:1-10 |
| Wednesday prophecy | Jonah 3:1-4:11 | Jonah 3:1-4:11 |
| Monday Matins Psalm | Psalms 102:1, 7 | Ps 103:1,8 |
| Monday Liturgy Psalm | Psalms 129:2,4 | Ps 130:2,4 |
| Tuesday Matins Psalm | Psalms 102:13, 8-9 | Ps 103:14-15 & Ps 103:9-10 |
| Tuesday Liturgy Psalm | Psalms 84:2 | Ps 85:2-3 |
| Wednesday Matins Psalm | Psalms 102:12, 11 | Ps 103:13 & Ps 103:12 |
| Wednesday Liturgy Psalm | Psalms 31:1, 6 | existing Psalm 32:1 & Psalm 32:5 retained |

Monday ends with the great fish / three days and nights, not the prayer introduction. Tuesday's first numbered unit contains both modern 2:1 and 2:2. Its mountains/earth wording is redistributed and differs from NKJV's weeds; future restoration, mercy, praise and salvation wording also differ. Brenton's corresponding Tuesday span is 2:2–11, not a flat shift of every Reader label. Wednesday English has forty days at 3:4 whereas Brenton has three. These limits are retained in every affected row's canonicalization note.

The three additional Tuesday/Wednesday Psalm fixes are based on complete clause inspection, not raw numeric label replacement: dust/grass followed by anger/sin; forgiveness followed by wrath; father/children followed by east/west. The correct Wednesday Liturgy Psalm and all other correct companions are preserved.

## Integration obligations

The returned rows contain source edition, printed heading, selected/captured context and time, complete body envelope and hash, full document hash, evidence locator, contract hash, mapping confidence/note, family/kind, and collision witness metadata. Retain those qualifications through date-index/crosswalk/daily/reverse serialization. The current date-index helper only transports its existing allowlisted fields, so adding the parser call alone is **not** final consumer-disclosure verification. Do not drop the covering-locus qualification or present the old receipts as activation approval.

The adapter uses `jonah_source_body_*` names to avoid impersonating the generic held-Matins candidate marker fields. Existing broad candidate guards are unchanged. Do not globally activate held Matins. Default current indexes must exclude the retained history. The real current date-index helper was exercised: the three Jonah prophecies index under their modern covering spans; old Monday 1 Corinthians is absent from the current lane and present only in the explicit inactive lane.

## Actual verification

Before implementation, the source regression failed on all three days with no prophecy; the real parser-integration regression also failed with `0 != 1`. Additional RED–GREEN probes caught partial-Presentation companion invention, erased preexisting Vespers lifecycle/provenance, missing collision disclosure, and the three clause-aligned Psalm coordinate errors.

Latest focused adapter run: **12 tests passed**, including all 48 dates, exact complete appointment lists/order, no Vespers, original/history preservation, partial dates, idempotence, wrong family/kind/date/service/slot/state, duplicate/overlap, replay tampering, source/manifest/body tampering, literal verse-label resets and actual date-index behavior.

The separate `test_parser_integration_is_not_optional` is intentionally **still RED (`0 != 1`) until the parent adds the owned integration call**. No skip/xfail or weakened assertion hides that boundary. No data builds, package writes, staging, commits, publication, deployment, or vault writes were performed.

Run with Python 3.11 and existing dependencies, with `TMPDIR` set to the caller's scratch root, `PYTHONDONTWRITEBYTECODE=1`, and `LECTIONARY_DISABLE_VAULT_PUBLISH=1`:

```sh
uv run --offline --python 3.11 --with beautifulsoup4 --with requests --with convertdate \
  python -m unittest tests.test_jonah_fast_source_supplements -v
```

After parent integration, the full file must pass and the parent must independently verify downstream disclosure, source/service semantic deltas and release artifacts.
