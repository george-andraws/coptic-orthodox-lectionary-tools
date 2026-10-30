# Combined 1.3.8 validation

## Final tested source

All Mark, 1 Timothy and Luke feature and integration writers were stopped before final acceptance. Production-code fingerprints remained unchanged throughout the final Python and Node replays. Retained source fixtures, policies and historical complete-output pins were not refreshed from candidate output.

## Full suites

- Complete Python collection: **1,251 tests in 97 modules**.
- Complete replay, partitioned by whole module into three disjoint shards: **1,235 passed, 16 skipped, 6,183 subtests passed**. All three commands exited zero. All collected nodes were accounted for; no changed frozen files.
- The 16 skips predate this follow-up and were retained rather than introduced to make this release pass.
- Complete Node inventory: **23 files, 112 tests passed**, zero failures, skips or cancellations. Command exit zero; code and Node-test fingerprints unchanged.
- Existing consumer plus compatibility changes, before the dependency upgrade: **2,521 site tests passed**, TypeScript check exited zero, and all **7,658** current projected rows passed the real span, slot and package-row validators.

Python was run in the isolated dependency environment:

```sh
uv run --python 3.11 --with beautifulsoup4 --with requests --with convertdate --with pytest python -m pytest tests
```

The complete replay used three processes with disjoint module lists, unique temporary roots, disabled shared pytest caches, verbose logs and JUnit output. Collection and grouped-node coverage were checked independently. This changes scheduling only, not assertions or production authentication. Node ran under the same environment so its spawned Python interpreters had the required dependencies.

## Failed-run disposition

The first full Python run exited one with 15 failed, 1,202 passed, 16 skipped, 20 setup errors and 6,167 passed subtests. The first full Node run exited one with 109 passed and three failed. Original run logs were retained outside the source checkout. The two committed Mark transition-log copies have trailing blank-line whitespace normalized only; original byte-for-byte copies remain with the release verification artifacts.

The failures were test-domain mismatches after the intentional successor changes:

1. Historical calendar, materialization and R4 corruption tests read mutable successor output while retaining predecessor oracles. They now bind exact authenticated 1.3.7 input and policy, with the existing 1.3.6 control kept on its original lane. No mutation body, valid vector, expected diagnostic or rejection catch was relaxed. Four corrected modules passed 158 tests and 105 subtests before the full replay.
2. Mark-only complete-array tests compared an intermediate Mark view with the final public representation. They now compare full final arrays and authenticate the inverse before applying the unchanged Mark predecessor-table oracle. All 74 Mark tests passed before the full replay.
3. The ordinary service-order test lacked the two L1 holds and three approved LK9 annotation changes. Exact new deltas are asserted separately; historical complete-order hashes remain unchanged.
4. The Psalmody test parsed the old JSON provenance cell rather than its new explicit evidence envelope. It still checks every original source body and now checks transport shape and short public provenance.
5. The bounded Jonah reader fixture omitted the five eve dates required by the new whole-eve coverage gate. It now includes hash-authenticated predecessor eve tables. Real repair hooks and no-SQLite/no-filesystem-write audits remain enabled; a negative control proves omission still refuses before output.

These corrections changed test fixtures and assertions only, not production data, policies or source qualifications. The final complete replays above supersede the failed runs as acceptance evidence.

## Real artifact gates

After the final full suites, the real package builder, strict file-set integrity validator and cached-source comparator each exited zero. Every year had zero comparison mismatches. The candidate contains **12,282 reverse rows** and **4,078 / 4,069 / 4,087 daily appointments** for 2026 / 2027 / 2028, retaining all 1,096 civil dates.

Independent artifact checks verified the exact L1/L2/L9 removals, all supported pending-equivalence appointments, raw provenance and reference preservation, the three bounded LK9 daily annotation changes, and unchanged API/calendar/Synaxarium/license bytes. Frozen-boundary counterprobes rejected forged L1 occurrence booleans and types, source-title rebinding and compound composite reactivation.

The dirty candidate truthfully records its precommit source state. It is not the publication artifact. Release procedure requires one source commit, a fresh clean clone of that commit, naturally generated `source_tree_dirty: false`, matching reviewed data/runtime bytes, strict gates, exact tarball installation and registry readback. Publication status is verified separately; this source receipt does not fabricate a registry upload or a self-referential final commit hash.
