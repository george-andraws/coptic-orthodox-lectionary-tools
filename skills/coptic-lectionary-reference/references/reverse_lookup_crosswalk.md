# Reverse-lookup crosswalk

Use the repository's `out/data/reverse_lookup_crosswalk.csv` or `.jsonl` for published reverse-lookup rows. `build_lectionary_crosswalk.py` is the generating implementation. Follow `RUNBOOK.md` before rebuilding; do not infer occasion assignments from thematic similarity.

For an isolated repository-only rebuild, set `LECTIONARY_DISABLE_VAULT_PUBLISH=1` before running any build script. The generator supports `LECTIONARY_WORK_OUT_DATA` and `LECTIONARY_CROSSWALK_OUT` for explicit output locations. Without the disable flag, legacy repository scripts may attempt maintainer-specific vault publishing; never rely on those defaults on another machine.

For Psalm-numbering and normalization details, load `lectionary-design-layer-orchestration-and-psalm-crosswalk.md` and `lookup-normalization-and-bundle-routing.md` in this reference directory. Preserve source provenance, source and display numbering, reading slots, and distinct service occurrences. A reverse-index hit is a lookup lead, not independent evidence of current liturgical practice.
