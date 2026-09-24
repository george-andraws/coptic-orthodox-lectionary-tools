# Public Hermes skills for Coptic lectionary work

This directory contains portable, repository-owned copies of the lectionary skills maintained with this project. They are documentation and workflow aids; they do not contain credentials, raw Coptic Reader captures, private review artifacts, local machine paths, or deployment state.

## Skill mapping

| Skill | Use for | Included support |
| --- | --- | --- |
| [`coptic-lectionary-reference`](coptic-lectionary-reference/SKILL.md) | Coptic Orthodox date-to-reading and passage-to-occasion lookup, Synaxarium context, Psalm-numbering care, Holy Week/Pascha and special-service source handling | 49 linked research, validation, package, Coptic Reader, and special-service references in `references/` |
| [`synaxarium-codisplay-ops`](synaxarium-codisplay-ops/SKILL.md) | Changes to the existing `@andraws/lectionary-data` Synaxarium catalog and its consumer co-display | The repository package README and `docs/SYNAXARIUM_RELEASE.md` are the public schema and release contract |

## Use in a checkout

1. Clone this repository, check out `main`, and set `REPO_ROOT` to the clone root. The skills use `$REPO_ROOT` as a placeholder. Before any rebuild, export `LECTIONARY_DISABLE_VAULT_PUBLISH=1` to disable legacy maintainer-specific vault output defaults.

   To install in Hermes, copy both complete directories under `skills/` into `${HERMES_HOME:-$HOME/.hermes}/skills/` and start a new session. Keep the repository checkout available for the package scripts, data, runbook, and release instructions.
2. Read the matching `SKILL.md` and only the referenced support file needed for the task.
3. For source-data rebuilds, follow [RUNBOOK.md](../RUNBOOK.md). For runtime package releases, follow [docs/SYNAXARIUM_RELEASE.md](../docs/SYNAXARIUM_RELEASE.md) and [packages/lectionary-data/README.md](../packages/lectionary-data/README.md).
4. Use Coptic Reader rendered UI evidence or a requester-supplied, audited fixture for current-practice claims. Do not infer a reading, commemoration, or saint-to-reading relationship from thematic similarity.

## Dependencies and boundaries

- Base data/query workflow: Python 3 and the tracked repository scripts/data.
- Full test and Synaxarium validation: Python 3.11 with `beautifulsoup4`, `requests`, and `convertdate`; use the documented `uv run` command to avoid modifying a system Python.
- Package tests and tarball checks: Node.js and npm.
- Browser validation: a browser that can access the Coptic Reader rendered UI.
- An audited source directory is required to regenerate the Synaxarium catalog; raw capture files and source fingerprint fixtures are deliberately not distributed as npm package files.
- Consumer-site UI/deployment work belongs in that site's repository and must be verified separately.

## Publication hygiene

The source copies were sanitized for public use. Keep future additions portable: use `$REPO_ROOT` or repository-relative paths, replace personal workflow language with requester/maintainer-neutral language, and do not add private IDs, captures, personal folders, credentials, service tokens, or deployment details.
