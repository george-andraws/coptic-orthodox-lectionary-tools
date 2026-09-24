# Autonomous lectionary design runs: audit and finalization patterns

Use this reference for the maintainer's long-running lectionary-data repo work when the task involves generated article/spec/schema outputs, bridge logic, audit loops, and final execution reports.

## Durable workflow lessons

1. **Commit one logical step at a time, but audit the integrated result.** After a later step changes meaning, scan every generated artifact that might still describe the older state: article, spec, site handoff, open questions, deck outline/PPTX, execution log, and verifier expectations.
2. **Do not trust generated prose just because data changed correctly.** In the 69 bridge upgrade, data moved from all `collection-type/medium` to `explicit/high` for 69-covered rows, but stale prose remained in the article, spec, deck, and older log sections until audited.
3. **When post-audit fixes touch reviewable artifacts, rerun the independent audit if still within the allowed pass count.** A final an independent reviewer pass caught whether later deck/log/open-question fixes had introduced or left contradictions.
4. **Generated output contracts need header parity, not only required-field spot checks.** Add verifier checks comparing `csv.DictReader(...).fieldnames` to schema table contracts for every emitted CSV. This prevents schema drift where outputs gain fields but schema remains partial.
5. **If the locked brief is outside the repo, add a tracked repo-local copy or tracked reference.** Repo-only audits cannot verify locked decisions from a WebUI attachment path.
6. **Distinguish model semantics from review residue.** For `removed_marker`, keep maintainer-named removed-reading families separate from other `historical_candidate_removed` rows. If marker format is unresolved, record it as an open decision instead of silently changing model shape.
7. **Final log commits should be log-only where possible.** Regenerating binary decks can create nondeterministic PPTX diffs. If the deck was already committed and a final verification reruns it without content intent, revert the nondeterministic binary rewrite before the final log commit.

## Step 7 bridge upgrade checks

Record distributions before and after:

- Before: `basis=collection-type: 4688`, `confidence=medium: 4688`.
- After: `basis=explicit: 789`, `basis=collection-type: 3899`, `confidence=high: 789`, `confidence=medium: 3899`.

Also report:

- 58 foundational days produced bridge rows and were upgraded.
- 11 foundational days had no emitted bridge rows.
- Outside the 69, rows remain uniformly `collection-type/medium` unless a later source gives stronger evidence.

## Independent audit routing pattern

When the producer is Codex and the brief requires an independent reviewer audit:

```bash
Use an independently routed reviewer with a bounded prompt and retain only the final audit artifact.
```

Save each audit pass under `audit_artifacts/`, and tell the auditor explicitly:

- inspect repo only,
- do not edit,
- do not commit,
- return concrete required/advisable revisions,
- audit against locked decisions, source registry, generated outputs, and content rules.

## Continuation-pass gates and source blockers

When the maintainer starts a continuation pass from an attached brief and asks to verify the committed repo copy:

1. Read the repo-local brief and attached brief, compare content, and print the requested first lines or marker checks before editing.
2. Verify `git rev-parse --short HEAD` and `git status --short` before any change. If the brief names an allowed dirty file, treat any other dirty path as a stop condition.
3. If a step says sources are externally confirmed but also says to stop on unsourceable claims, do not silently rely on memory or broad internet familiarity for new article prose. Try the required source route, then a direct network fallback or repo-local source notes. If named-source text cannot be inspected and the claim is broader than the accessible evidence, stop and report the exact unsupported portion.
4. For Pascha shared-date wording, distinguish a worked same-date example from a general rule. A dated example can support that year only; it does not by itself prove that Coptic Pascha always falls on the same Sunday as Eastern Orthodox Pascha.
5. If a research subprocess cannot access web tools, save the partial research artifact uncommitted only if useful, and report that it is not a source confirmation. Do not commit partial source-check artifacts unless the step asks for them or they become part of the audit record.

## Finalization checklist

Before final response:

1. Replace all `pending this commit` placeholders with actual hashes.
2. Run compile, build, verifier, deck generator if deck artifacts are in scope, and `git diff --check`.
3. Check `git status --short`; only the known allowed untracked files should remain.
4. Extract the current open-questions file verbatim enough for the report.
5. Include every commit hash and one-line purpose.
6. Include bridge basis/confidence distribution before and after.
7. Include final open questions and any remaining known untracked file.
