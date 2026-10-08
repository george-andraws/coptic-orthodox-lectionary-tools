# Special source continuation — bounded evidence snapshot

**Completeness: NOT CLAIMED.** Actual menu children, not the stale prior queue, control this inventory. Captured routing menus are not assigned-reading tables.

## Outcome
- 24 unresolved leaf contexts attempted; 24 successful full-document captures; zero failed children. Two additional menu-only probes (Unction and Funeral) succeeded.
- 49 valid complete documents reused without altering their raw bytes; 73 complete rendered documents now available.
- Prior frozen helper SHA256: `82e81beb51d87e12e03bd09c67536a35d934ba393969118b0f2ba55f1563ffaf`.
- Isolated copied helper SHA256: `406e0aa7a8672e2508853189eb5085830f1c61fe962693533b7260a59f436f82`; node syntax check passed and before/after child hash checks passed. Only output-root replacement made. No edits during child runs.
- Foreground batches, maximum three separately launched headless browsers. All child processes awaited; no background recovery job remains owned by this continuation.

## Finite menu inventory
94 actual child contexts: 11 verified routing menus, 73 complete rendered documents, 9 unresolved contexts, and the unexpanded Pascha frontier delegated to a different lane. The 83 leaf-or-frontier count is **not** a claim of 83 known leaves: Veneration and Pascha remain unexpanded frontiers. Expanded known menu leaves are 81: 73 captured and 8 still unresolved.

Priority families are now captured at every currently observed leaf: Consecrations (including all 10 Ordinations and both Myron stages), seven Unction prayers, 14 Funeral variants, three Lakkan variants. Source spelling is retained as `Lakkan`; it is not silently renamed. `Women During Delivery` is the actual Funeral menu label. Exact saved source menu labels control.

## Oracle and scope
333 assigned printed reading blocks, 66 prescribed Psalm-prayer blocks, 3 prescribed canticle references, and 1 interpretation-heading citation (not counted as an additional assigned reading). 65 incidental or rubric reference occurrences are separate. 48 documents expose assigned printed reading blocks; 1 exposes prescribed Psalm-prayer blocks only; 24 expose no printed assigned-reference blocks in the complete rendered document. These negatives are scoped to the rendered document, **not** assertions that the rite universally has no assigned Scripture. External linked documents, ordinary liturgy dependencies, and reading-slot prose without printed references are not invented.

The oracle retains exact raw heading, printed reference, document order, source lines and context, date/occasion navigation, raw text and image paths/hashes, helper hash, and reused/new distinction. Psalm numbering is not converted. Full raw documents preserve prayers/rubrics and incidental quotations. 13 assigned printed blocks lack a dedicated reference screenshot (older evidence or headings not matched by the frozen screenshot helper); service/end screenshots and full raw text remain available. This is an explicit evidence limitation, not hidden completeness.

Visual spot-check: Unction First Prayer screenshot shows James 5:10-20 and rendered trilingual reading; its Home context shows Standard, Thoout 27, 1743, Wednesday October 7, 2026. Other screenshots are hash-verified, not all manually inspected.

## Remaining queue
- Crowning: Crowning Prayer; Engagement Prayer; Liturgy of the Word (Weddings); Second Marriage Prayer.
- Prostration: First Prostration; Praises; Second Prostration; Third Prostration.
- Veneration: unexpanded source-menu frontier; document-versus-menu is unknown until navigated.
- Pascha: unexpanded frontier outside this special-service lane; no completeness inferred.

## Files and verification
`inventory.json`, `coverage.json`, `family-coverage.json`, `remaining-queue.json`, `document-dispositions.json`, `assigned-scripture-oracle.json`, `oracle-summary.json`, `incidental-and-rubric-references.json`, `acceptance-checks.json`, `seed-captures.jsonl`, `frozen-helper.json`, plus `verified/` raw documents, screenshots, manifests and child logs. `continue.py` and `extract_oracle.py` are standalone continuation utilities.

Node syntax check exit 0. Four foreground capture batches exit 0. Extraction/acceptance assertions exit 0: unique contexts, raw text hashes, context screenshots, en-dash and prefixed Pauline references, and exclusion of Priest inline quotations from assigned readings. No site sync/build/test/install/deploy, production/vault edits, commits, or original capture-helper modifications.

To resume, authorize a new bound and use another checkpointed continuation; do not rerun the current `batch` mode expecting more work because its hard 24-context budget has been consumed.
