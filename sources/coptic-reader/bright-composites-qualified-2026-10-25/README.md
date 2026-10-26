# Bright Saturday composite qualification — retained evidence, canonical hold

No fresh Reader retrieval or independent current-practice confirmation was performed. The package-first baseline/gap is the parent's authenticated `@andraws/lectionary-data@1.3.5` review. Original capture receipts are copied unchanged as `original-captures.json`; original sources and prior approval flags are not edited. October 25 is a retention label, not a capture timestamp. Selected context is Joyous Saturday, April 11, 2026. Capture time and app version remain unknown.

## Interpretation

- Matins prints `Psalm 88:4-5; 44:23,26; 126:2-3`. The body has Awake/Arise/help/redeem clauses, **not 44:24–25**. Legacy `44:23-26` survives as an inactive numeric witness. The source-only corrected selection is `Ps 44:23,44:26`.
- Matins `126:2-3` prints and contains the mouth/joy, tongue/exultation, nations and great-things clauses. This is the Reader's selected wording, not a newly certified NKJV or Brenton verse counterpart.
- Sixth Hour prints `Psalm 130:1; 142:7`. `142:7` contains only “Bring my soul out of prison, that I may give thanks to Your name, O Lord.” The righteous-surround-me continuation is absent; claiming the full target-edition verse would overstate coverage.
- Liturgy of the Word prints `Psalms 82:8` and “Arise, O God, judge the earth; For You shall inherit all nations.” This is the authenticated selected clause, not an independent comparison with a target Bible edition.

All four get explicit source-only identities. **Canonical MT/LXX refs remain empty and spans_json is []**: this bounded retained pack does not establish exact cross-edition counterparts. Generic Psalm numbering is unchanged. These are qualified holds, not approval to amend the canonical occurrence ledger or activate numeric searches.

## Evidence bounds

Full captures, their screenshots, selected-home/picker and Saturday/Pascha menus are portable here. The pinned correction contract authenticates all 15 assets and selected heading/body clauses on each call.

|Document|SHA-256|Heading|Body bounds (1-based)|Selected English|
|---|---|---|---|---|
|saturday--matins.txt|eb373a8c80ae9fcb658c1726c38a1815281a078217a5d61e1bb305b08cedbb7f|1663|1664–1694|1671 (44), 1674 (126)|
|saturday--third-and-sixth-hours.txt|36637b897d93e0405d35dec4e92430935f60262aad955560ca85681b13840b01|336|337–367|347 (142)|
|saturday--liturgy-of-the-word.txt|78570c0a89319493c6a1bade8fd41fbe64cf3c80b145deaf817ab8156b80df8f|432|433–459|435 (82)|

## Literal key proposal (not ledger edits)

Suppress these four newly exposed generic keys; they were absent from the prior 1.3.5 baseline, so this is **not** a request to remove four existing baseline appointments:

```json
["6TH HOUR","6th Hour","","Psalm","rid_f8f64afe999bed4ad0e1"]
["MATINS / RAISING OF INCENSE","Matins","","Psalm","rid_01f32bd787164f059e93"]
["MATINS / RAISING OF INCENSE","Matins","","Psalm","rid_cf1a402c8a2d11ef55de"]
["ST. BASIL LITURGY – LITURGY OF THE WORD","Liturgy","","Psalm","rid_c6e5abb3b44d8783f05f"]
```

Proposed source-only held identities in existing Bright Saturday service context (not generic numeric additions):

```json
["Bright Saturday","Matins","","Psalm","rid_d58dc513121900158fc9"]
["Bright Saturday","Matins","","Psalm","rid_16e3ff8ccefe525d98e0"]
["Bright Saturday","6th Hour","","Psalm","rid_969f73205a3c4d8ceef6"]
["Bright Saturday","Liturgy","","Psalm","rid_5be18395526b0ff8b009"]
```

## Integration contract

`build_lectionary_crosswalk.project_bright_rows` is the real raw-creation entry used by main. It authenticates exact source/service/slot/reference rows, retains four legacy rows with `superseded_reason=bright_composite_edition_context_hold`, and adds four string-valued authenticated source selections. No global generated output was rebuilt.

Parent-owned design daily/reverse hooks are still required: dispatch exact kind `bright_saturday_qualified_composite`, call `qualify_bright_composite_row(raw)` before projection, then `bright_composite_identity_for(raw)` instead of the generic identity builder. Carry returned metadata through provenance/disclosure. After passage-CSV transport call `authenticate_bright_composite_identity(raw, identity)`; do not widen status or numeric-index allowlists based on family/kind alone. Legacy hold rows must stay inactive. Source-only identity acceptance must remain separate from canonical numeric activation.

APIs re-read pinned contract/captures each call; malformed/scalar/context/lifecycle drift and missing/corrupt/symlinked evidence fail closed. No design hook, package build, ledger amendment, commit, publication or deployment is claimed.
