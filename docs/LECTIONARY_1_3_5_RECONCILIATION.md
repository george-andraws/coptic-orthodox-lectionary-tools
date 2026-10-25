# Lectionary 1.3.5: published artifact and source reconciliation

Verified October 25, 2026. This is a retrospective reconciliation of an existing npm release, not a new release or a claim that all data issues are resolved.

## Artifact identity and preservation

The registry published `@andraws/lectionary-data@1.3.5` at `2026-10-20T00:21:24.061Z`. The controlling artifact is:

- Tarball: <https://registry.npmjs.org/@andraws/lectionary-data/-/lectionary-data-1.3.5.tgz>
- Integrity: `sha512-L+QbKbbAopEM+plhs0LkaAzP37bKLZPi2Kg+esPvs971hL78mEHdYBYXv04ptQvCdw+zMk0jsJDPYyh2wGgE3Q==`
- Tarball SHA-256: `2bce78f092c318bdf5dc67a0b0bc1e300b668418ca98b0ff7e3742b1f31ae509`
- Tarball size: 2,487,936 bytes; 11 files; 49,724,775 unpacked bytes.

[Per-file hashes, installed comparison and builder replay](receipts/lectionary-1.3.5-artifact.json) record the exact observations. All 11 tar members match the repository's package directory and the canonical site's installed 1.3.5 package. A fresh local `npm pack` is byte-identical to the downloaded registry tarball, including its archive bytes, not merely parsed JSON.

No runtime package member is changed by this reconciliation. In particular, `meta.json` and the stale packed README are retained exactly. Updated repository documentation does not mutate npm's immutable artifact.

## What the source closeout contains

The previous committed package source stopped at 1.3.3. Existing uncommitted source, tests, contracts and generated data supply the already-published 1.3.4/1.3.5 changes:

- Bright Saturday: restore previously blank-reference Susanna, Prayer of Manasseh, second Azariah section, and Matins Isaiah/Ephesians entries; preserve source heading/body distinctions and do not invent an MT equivalent for Psalm 151.
- Bright Saturday daily serialization: collapse same-service Pauline/Catholic/Praxis slot aliases, prefer the explicit current representative, and retain both source disclosures. Distinct service sections stay separate.
- Lamentations: qualify Good Friday Twelfth Hour Lamentations 3:1-66 from the retained Reader hour, retain the conflicting Jonah API/Ottawa witnesses as edition-specific history, add Hosanna Sunday daytime Ninth Hour Lamentations 1:1-4, and use the retained Jeremiah praise heading. Sunday Day is not Monday Eve.
- Joel: retain printed modern-English primary coordinates while representing the Brenton chapter seams, with narrow first/fifth-week Wednesday cycle supplements and no Annunciation substitution. This is not a complete Lent or Jonah's Fast enrichment.
- Laqqan public day titles: name the feast while preserving the machine service-family/variant keys.
- Preserve the reverse-key contract lineage and source-qualified correction policy instead of replacing historical evidence or reissuing earlier review approvals.

The frozen package has 12,211 reverse rows. Daily files contain:

| Year | Civil dates | Reading rows |
| --- | ---: | ---: |
| 2026 | 365 | 4,068 |
| 2027 | 365 | 4,063 |
| 2028 | 366 | 4,072 |

The six changed 2026 dates relative to the committed 1.3.3 snapshot are February 18, March 11, March 18, April 5, April 10 and April 11. There are five corresponding changes in 2027 because the fifth-week Wednesday collides with Annunciation, and six in 2028. Unchanged row totals do not imply unchanged coordinates or disclosures.

## Reproducibility and honest provenance

The published registry `gitHead` and `meta.source_repo_commit` are both `b5602df6bcca68b9f5fafb05597dbcc31280a409`; `meta.source_tree_dirty` is **true**, and `generated_at` is `2026-10-20T00:17:38.514Z`. That commit alone did not contain all published inputs. This closeout makes the previously uncommitted source and generated package snapshot available in Git history; it does not retroactively turn the original publication into a clean-source build.

An isolated replay of `scripts/build_npm_package.mjs`, using the reconciled tracked design daily/reverse files, package baseline and policy-fingerprinted sources, reproduces **10 of 11 members byte-for-byte**, including all reading data, runtime code, manifest, Synaxarium, license and README. The only differing member is regenerated `meta.json`: its source commit and generation timestamp describe the new execution. All other metadata, including counts, is equal. This proves package materialization from these inputs, not a fresh raw-source extraction, complete primary-source audit or ecclesiastical approval.

The generated `out/scripts/passage_normalization.py` was stale relative to its source. The existing `build_lectionary_reference.copy_support_modules()` step refreshes that helper only, without rebuilding reading data or writing the vault. The curated Bright Saturday CSV retains its existing CRLF bytes; its scoped Git attribute treats CR as a line ending, not trailing space. No source bytes were normalized to silence whitespace checks.

## Verification and remaining gates

The completed baseline run used isolated Python 3.11 with `beautifulsoup4`, `requests` and `convertdate`, vault publication disabled and a scratch `TMPDIR`.

| Gate | Observed baseline result |
| --- | --- |
| Registry/package integrity, including tarball | Pass |
| Strict full calendar-date coverage | Pass |
| Source manifest | Pass |
| Synaxarium catalog | Pass |
| Full Python discovery | 339 tests; 14 failures and 1 error; exit 1 |
| Node `*.test.cjs` | 24 reported tests; 22 passed, 2 failed: canonical fixture/policy fingerprint mismatch and spawned system Python lacking `bs4`; exit 1 |
| Legacy Node `.js` release assertions | 16 tests; 14 passed, 2 failed; the identical two failures reproduce on the committed 1.3.3 package and tests |
| Design verifier | Fails its calendar-overlay source-context equality oracle |
| Query verifier | Fails because the chapter inventory lacks the already-parsed `PrMan` book |
| Cached-source comparator | Errors because seasonal coverage assumes every evidence JSON contains `qualified_dates` |

Most Python failures share the overlay oracle's expectation that the now-retired Good Friday Jonah row remain current. The identity-canary failure records the intentional Joel chapter-seam changes against the frozen legacy identities; one comparison failure concerns the qualified Hosanna Sunday supplement. These are recorded findings, not waived release gates. The prior 1.3.3 report's all-clear statements apply only to their recorded scope, not automatically to this source snapshot. The subsequent repair/release task must resolve or explicitly classify each affected check and rerun against its final artifact.

## Retained limitations

- Independent read-only review approved recording the already-shipped source history with these limitations, not releasing another artifact unchanged. It reproduced a newly broken canonical-occurrence regression module: the frozen 1.3.2 fixture still expects its historical policy, but the current policy pins 1.3.5. Preserve that historical fixture/oracle while adding a separately authenticated current replay; do not disable the fingerprint guard.
- The current Bright Saturday CSV has 39 rows, but its paired JSONL and legacy `out_bright` fallbacks retain the earlier 38-row snapshot. The crosswalk consumes the CSV. These paired/fallback projections need reconciliation before a future source rebuild; immutable npm parity does not make them equivalent.
- The cited Bright Saturday/Good Friday/Hosanna retained Reader captures are outside this Git snapshot. Source notes name paths/hashes, but qualification notes are not completely transported into published runtime disclosures. The new release work must preserve and authenticate those captures durably rather than relabel the original artifact as independently source-approved.
- Review counterprobes found a false Wednesday-fixture explanation on the correctly inactive Good Friday Jonah row, and a Joel projection path that can relabel an inactive synthetic source as current and emits empty disclosures. No real newly activated extra appointment was demonstrated in the published snapshot. Both are source-pipeline fixes for the separately authorized follow-up, not changes to 1.3.5 bytes.
- The 1.3.5 artifact is the reconciliation baseline, not proof of complete worship coverage. Tobit daily materialization, Jonah's Fast prophecies and the Psalm 151 / Fourth Hoos indexing gaps remain separate work.
- Two existing Node assertions concern February 18 Psalm-fragment order and a retained Nineveh no-Vespers marker. Do not weaken either merely to make the published snapshot pass. Record freshly observed results separately from historical reports.
- Other source/design/query failures must be classified against their own oracle and baseline, not hidden behind exact npm parity. Exact tarball equality cannot prove that all upstream generated projections are current.
- Broader annual/default Morning activation, Psalm coordinate holds and site-owned Annunciation presentation holds are not cleared by this reconciliation.
- The packed README still says 1.3.0. The root README and this record supply current release status while preserving the immutable package snapshot.
- No npm publication, consumer upgrade, website code change, content sync, deployment, real-phone acceptance or Obsidian write is performed in this task.
