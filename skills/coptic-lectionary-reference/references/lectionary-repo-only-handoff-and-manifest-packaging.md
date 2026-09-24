# Repo-only handoff and manifest packaging for lectionary-data runs

Use this when the requester explicitly restricts work to `coptic-lectionary-research` / lectionary-data only and says he will push to `coptic-corpus` himself.

## Scope boundary

- Work only in the lectionary-data repo.
- Produce push-ready handoff files under `out/handoff/`.
- Never claim a site push or site verification happened if `coptic-corpus` was not accessible.
- The final report should say clearly that the maintainer pushes to `coptic-corpus` himself.

## Article presentation pass rules

When the active lectionary article is already substantively correct and the task is presentation/readiness only:

1. Do not rewrite sourced claims.
2. Move inline `Source:` / `Sources:` trailers into notes or endnotes so the article stops reading like generator apparatus.
3. Set `publish: false` unless the requester explicitly approves publication in the current task.
4. Add a visible top-of-body draft note such as `DRAFT, pending deacon review` only while the article remains on review hold.
5. Verify the active article still states the 69 verdict as `INFERRED_LIKELY_SAME_SET`, roster unverified.

If the maintainer later approves publication:
- Change the article through `build_design_deliverables.py`, not just the generated markdown.
- Set root and handoff article frontmatter to `publish: true` and remove the draft warning.
- Update `verify_design_deliverables.py` so regeneration enforces the approved state.
- Update `out/handoff/HANDOFF.md` and `out/handoff/site_integration_spec.md` so they no longer tell the maintainer to keep the article unpublished.
- Regenerate, copy the refreshed article to `out/handoff/`, run verification, and commit as one logical publish-readiness change.

## Change-manifest workflow

When the requester asks for a manifest of lectionary data changes across the repo history:

1. Pick and record a baseline commit before the relevant re-key/data phase.
2. Tag it if helpful, for example `lectionary-baseline`.
3. Build the manifest from git history, not memory.
4. Emit two layers:
   - a grouped review manifest at `out/design/lectionary_change_manifest.csv`
   - an exact row-level archive at `out/design/lectionary_change_manifest.raw.csv.gz`
5. Also emit:
   - `out/design/affected_passages.csv`
   - `out/design/lectionary_change_manifest.md`
6. Cross-check the manifest against the execution log by commit hash.
7. Exclude the manifest outputs themselves from future manifest scans so the tool does not recurse on its own artifacts.

Why the two-layer pattern matters:
- exact row-level CSV deltas can become too large for practical review or push,
- a grouped CSV stays reviewable,
- a deterministic gzip archive preserves full auditability.

## Handoff package shape

Package the site-facing deliverables under `out/handoff/` with:
- `HANDOFF.md` as the index,
- the publish-candidate article,
- the main CSV datasets the maintainer will import,
- the site integration spec,
- the grouped manifest,
- the raw manifest gzip,
- the affected-passages index,
- `open_questions_for_george.md`.

`HANDOFF.md` should tell the maintainer:
- what to push,
- what each file is for,
- import order,
- guardrails to preserve.

## Guardrails to preserve in the handoff

- keep the article unpublished until deacon review, unless the requester explicitly approves publication in the current task; after approval, make all generated handoff/spec wording say `publish: true` and remove stale draft warnings,
- keep `removed_marker` visible for historical Pascha rows,
- accept both MT and LXX Psalm numbering in search and map both to `identity_key`,
- do not over-claim the 69 identity,
- treat Synaxarium bridge rows as discovery links, not direct proper-reading proof.

## npm package handoff for lectionary data

When preparing `packages/lectionary-data`:
- Keep package identity centralized in `scripts/build_npm_package.mjs`; do not hand-edit generated package files as the only source of truth.
- Current locked package identity is `@andraws/lectionary-data` at version `1.0.0` with SPDX license `CC-BY-4.0` unless the maintainer changes it.
- For non-data packaging changes, keep `meta.json.source_repo_commit` pinned to the approved data provenance commit rather than deriving it from the current packaging commit.
- Build with `node scripts/build_npm_package.mjs`, then validate with `npm pack --json` from `packages/lectionary-data`.
- Validate the tarball file set, package.json license, README license text, LICENSE presence, meta license/provenance, JSON/JSONL parsing, 8,005 index rows, and file size limits before telling the maintainer to publish.
- Do not run `npm publish` unless the requester explicitly authorizes publishing in the current task and npm auth has been verified with `npm whoami`.

## Independent audit and artifact hygiene

If a an independent reviewer/Hermes CLI audit writes chain-of-thought or scratch text into an artifact file, overwrite the artifact with the clean final audit only before committing it.

If the audit finds a real log/manifest mismatch, fix the underlying log or artifact and then regenerate the dependent summary instead of just documenting the inconsistency.

## Push-failure handling

If `git push` fails because GitHub rejects historical blobs over the 100 MB hard limit:

- report the failure plainly,
- record that the work is committed locally,
- identify the offending history class if visible,
- do not rewrite history, migrate to LFS, or do branch surgery unless the requester explicitly asks for that repo-wide operation.

This is a repo-history issue, not a reason to under-report completed local work.

If the requester explicitly authorizes history cleanup:
- Use a narrow path-only rewrite for the retired artifact, for example `git filter-repo --path <retired-path> --invert-paths`, then verify the path has zero history hits and no reachable blob exceeds the host limit.
- Remember that `git filter-repo` removes the `origin` remote by design; restore the remote URL before pushing.
- Try a safe normal push after verifying the rewritten local `HEAD`; if the remote can fast-forward or otherwise accepts it, no force push is needed. If a force push is required, use `--force-with-lease` against the verified remote hash and expect Hermes or the user to require explicit approval.
