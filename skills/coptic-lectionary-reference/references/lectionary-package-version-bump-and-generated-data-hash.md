# Lectionary package version bump and generated data hash guard

Use this when preparing `@andraws/lectionary-data` for a version bump without publishing.

## Durable lesson

The package version is not owned only by `packages/lectionary-data/package.json`. The package builder also owns it through `scripts/build_npm_package.mjs`:

```js
const VERSION = 'x.y.z';
```

If only `packages/lectionary-data/package.json` is edited, `node scripts/build_npm_package.mjs` can rewrite it back to the builder constant.

## Required sequence for version-only bumps

1. Check current package metadata and data checksum before changing anything:
   - `packages/lectionary-data/package.json`
   - `packages/lectionary-data/meta.json`
   - `sha256sum packages/lectionary-data/data/reverse_lectionary_index.jsonl`
2. Bump both:
   - `packages/lectionary-data/package.json` version
   - `scripts/build_npm_package.mjs` `VERSION` constant
3. Commit the version-source changes first if `meta.json.source_repo_commit` is expected to point at the committed package-generation source.
4. Run `node scripts/build_npm_package.mjs`.
5. Compare generated package data against the pre-bump checksum before committing generated files.

## Critical pitfall

A version bump can change data bytes even when row counts and keys are unchanged. In this package, package `VERSION` must not be allowed to rewrite historical `removal_effective_version` values on existing removed/provenance-only rows. Rebuilding after a version bump can otherwise change every such row, e.g. `1.1.6 -> 1.1.7`, which changes `data/reverse_lectionary_index.jsonl` SHA-256 while preserving row count and keys.

When the requester explicitly requires the reverse-index SHA to remain unchanged, stop if the checksum differs. Report the changed field and row count instead of committing generated files or proceeding to `npm pack` / publish.

## Durable fix pattern: removal-effective-version baseline

For future version bumps, preserve historical removed-row versions through a builder-owned baseline file under `scripts/package_baselines/`, not through package `VERSION`.

Required pattern:

1. Harvest projection-removed rows from the last published tarball, not from the current worktree package payload.
2. Store a baseline JSON under `scripts/package_baselines/` so it is outside package `files` and does not ship to consumers.
3. Key baseline entries by `identity_key` first, but do not assume `identity_key` is globally unique. If duplicated, disambiguate by `(identity_key, removal_context_key)`.
4. During `scripts/build_npm_package.mjs`, every newly projected removed row must resolve against the baseline.
5. On hit, copy the baseline `removal_effective_version`.
6. On miss, fail the build with a listing of `identity_key`, `occasion`, `slot`, and `removal_context_key`. Never default a miss to package `VERSION` unless the requester explicitly approves a new-removal release branch.
7. Keep package `VERSION` for `package.json`, `meta.json`, and README metadata only.

Verification after implementing this pattern:

- Run `node --check scripts/build_npm_package.mjs`.
- Run `node scripts/build_npm_package.mjs`.
- Hash `packages/lectionary-data/data/reverse_lectionary_index.jsonl` and compare to the required target hash.
- Count projection-removed rows and their `removal_effective_version` distribution.
- Check `meta.projection_rules.removal_effective_version_baseline_miss_count` is `0`.
- Run `npm pack --dry-run --json ./packages/lectionary-data` and confirm `data/reverse_lectionary_index.jsonl` is included while `scripts/package_baselines/` is not.
- Confirm the npm registry does not already contain the target package version before telling the maintainer it is ready for his publish review.

Useful focused diff probe:

```python
from pathlib import Path
import collections, hashlib, json, subprocess
root = Path('$REPO_ROOT')
idx = root / 'packages/lectionary-data/data/reverse_lectionary_index.jsonl'
head_bytes = subprocess.check_output(['git', 'show', 'HEAD:packages/lectionary-data/data/reverse_lectionary_index.jsonl'], cwd=root)

def rows_from_bytes(raw):
    return [json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
def rows_from_file(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
def key(row):
    return tuple(row.get(f, '') for f in ('occasion', 'service_section', 'service_hour', 'slot', 'identity_key'))

before = rows_from_bytes(head_bytes)
after = rows_from_file(idx)
before_by = {key(row): row for row in before}
after_by = {key(row): row for row in after}
changed_fields = collections.Counter()
for k in set(before_by) & set(after_by):
    b, a = before_by[k], after_by[k]
    for field in set(b) | set(a):
        if b.get(field) != a.get(field):
            changed_fields[field] += 1
print({
    'head_sha256': hashlib.sha256(head_bytes).hexdigest(),
    'worktree_sha256': hashlib.sha256(idx.read_bytes()).hexdigest(),
    'rows_before': len(before),
    'rows_after': len(after),
    'keys_added': len(set(after_by) - set(before_by)),
    'keys_removed': len(set(before_by) - set(after_by)),
    'changed_fields': dict(changed_fields),
})
```

## Focused ad-hoc verification when system asks for fresh evidence

If code was edited in `build_design_deliverables.py` or `scripts/build_npm_package.mjs` and the runtime says no canonical test/lint/build was detected, create a temporary focused verifier under the requested OS temp root using `tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', dir=<requested-root>, delete=False)`, run it, then remove it when possible. Report this explicitly as **ad-hoc focused verification, not full suite green**.

For lectionary package scalar/version fixes, the temp verifier should check at minimum:

- `python3 -m py_compile build_design_deliverables.py`.
- `node --check scripts/build_npm_package.mjs`.
- Package and `meta.json` versions equal the intended release.
- `packages/lectionary-data/data/reverse_lectionary_index.jsonl` SHA-256 equals the newly established target and differs from the previous release hash when a data correction is expected.
- `source_family` and `source_kind` contain zero `" || "` joins in both `out/design/reverse_lectionary_index.jsonl` and package index.
- Any explicitly named regression rows are present and have family/kind from the same `source_disclosure` entry while retaining all disclosure families.
- Projection-removed rows remain at the expected historical `removal_effective_version` distribution and `meta.projection_rules.removal_effective_version_baseline_miss_count == 0`.
- `npm pack --dry-run --json ./packages/lectionary-data` includes `data/reverse_lectionary_index.jsonl` and excludes `scripts/package_baselines/` JSON.
- `npm view @andraws/lectionary-data@<version> version` confirms the target version is absent before handoff.

This temp verifier is a supplement to the package integrity verifier, not a replacement for a full canonical suite if the requester asks for suite-green evidence.

## Collapsed reverse-index scalar rule

When collapsing multi-source rows in `build_design_deliverables.py`, do not use display joins for atomic source fields. `source_disclosure` is the multi-attestation record; top-level scalar fields should identify one winning source consistently.

Recommended source-family precedence for Pascha/Coptic Reader collapsed rows:

1. `coptic_reader`
2. `holy_pascha`
3. `holy_pascha_curated_day_hour`
4. any other non-Katameros family
5. Katameros-derived families/kinds

`source_kind` must come from the same winning disclosure entry as `source_family`. Prefer `source_edition`, `source_title`, `source_locator`, and matching row `provenance` from that same winning source unless the requester explicitly asks for a display-joined field. Add/keep a guard that fails the reverse-index build if atomic scalar fields such as `source_family` or `source_kind` contain `" || "` on any row.

## Publish rule

Never run `npm publish` unless the requester explicitly authorizes publish. For this package, the maintainer usually runs npm publish himself.
