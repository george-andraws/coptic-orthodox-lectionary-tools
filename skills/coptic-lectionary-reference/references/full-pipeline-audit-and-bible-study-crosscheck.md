# Full lectionary pipeline audit + Bible-study cross-check pattern

Use this reference when the requester asks for an end-to-end local lectionary audit, rebuild, publication, and Bible-study guide cross-check.

## Durable workflow

1. Establish a baseline artifact before changes:
   - repo status, file list, mtimes, sizes, checksums, row counts
   - key scripts, curated data, generated outputs, published downstream documentation package copies
2. Inventory the pipeline and write a source-of-truth map:
   - raw/provenance layer
   - curated normalized source layer
   - generated index layer
   - query helper layer
   - downstream documentation package publication layer
3. Verify the actual query helper contract with `python3 out/scripts/query_lectionary.py --help` before using flags. Do not assume `--include-crosswalk` exists.
4. For Holy Week/Pascha problems, verify direct day/hour rows and extracted Pascha source-text rows first, then reverse crosswalk, then chapter index.
5. Prefer upstream fixes and full rebuilds. Do not hand-patch generated CSV/JSON unless that file is genuinely the curated source layer.
6. Rebuild, then publish only after verification passes.
7. Produce both human-readable and machine-readable manifests with changed scripts, curated/source files, generated artifacts, published files, row counts, checksums, schema changes, affected passages/services, reasons, and verification commands.
8. Cross-check Bible-study guides from the manifest's affected passages plus a general pass over existing lectionary claims.
9. Update guide prose/frontmatter only when the rebuilt local data clearly supports the correction. If a placement is ambiguous or missing, write an audit/revision note instead of inventing a placement.
10. Final response must cite real verification outputs, not just report that checks passed.

## Practical command lessons from the 2026-06-06 audit

- Broad Python `os.walk` over downstream documentation store folders can time out. Use ripgrep-backed `search_files` / targeted file reads for large downstream documentation package scans.
- Exact Holy Week regression queries should include day + hour + expected slot, not just passage lookup.
- Keep false-positive guards for chapter-style passage matching:
  - `John 2` must not match `John 20`, `John 21`, or `1 John 2`.
  - `Isa 5` must not match `Isa 50`, `Isa 52`, `Isa 53`, or `Isa 58`.
  - Numeric shorthand like `40.5` and multi-word/deuterocanonical books like `4 Maccabees 1:1-12` should be tested if the package intentionally supports them.
- If rebuilt data shows no row deltas, the useful change may still be a verifier/script hardening. Manifest that explicitly rather than overstating data changes.

## Scope pitfall

Do not fix downstream documentation links during this class of task unless the requester explicitly asks for link repair. Broken-link checks are verification only. If a check reveals broken links, report them as findings or remaining work, but do not rewrite links as part of a lectionary data/script audit.

## Known 2026-06-06 result shape

The 2026-06-06 pass found the corrected Pascha Genesis rows already present in the local baseline, rebuilt without row deltas, and hardened `verify_lectionary_queries.py` with permanent Pascha Genesis regression coverage. The local package remained partial because `pascha_source_text_index.csv` had 277 rows but 4 unparsed source-text rows. Treat that as a source-recovery gap, not something to fill from memory.
