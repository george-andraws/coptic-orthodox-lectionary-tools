# Testing the lectionary tools

Run from the repository root with Node.js 22+, npm and uv installed:

```bash
npm test
```

This runs every Python test in `tests/`, followed by every `tests/*.test.cjs`
and `tests/test_*.js` Node test. Python 3.11 and all Python test dependencies
are resolved through the pinned `requirements-test.txt`; the same environment
stays on subprocess PATH when Node tests invoke Python builders. No npm install
is needed. The root manifest is private.

The two inventories can also run independently:

```bash
npm run test:python
npm run test:node
```

`npm test` inside `packages/lectionary-data` runs the full Node inventory,
including the disposable builder and packed archive tests. These commands
require a source checkout, as the published package excludes tests and builders.

Python discovery is restricted to `tests/`, with strict configuration/markers,
skip reasons and the 15 slowest timings displayed. The npm Python command uses
two pytest-xdist processes and `--dist=loadfile`, keeping each file and its
module/class fixtures together. Node retains its default process isolation,
with two files running concurrently. Both phases bound memory use for large
JSON datasets and run sequentially under `npm test`. Run focused checks during
development, then the full suite before committing.

```bash
uv run --python 3.11 --with-requirements requirements-test.txt \
  python -m pytest tests/test_query_contract.py
node --test tests/npm_runtime_contract.test.cjs
```

For Python debugging without workers, use the direct uv command above, or append
`-- -n 0` to `npm run test:python`. Do not use automatic worker counts on these
large corpora without measuring memory first. A full baseline audit is cached
once per worker; each mutation still invokes the real daily validator.

Refresh dependency pins deliberately, and rerun the complete suite afterward:

```bash
uv pip compile --python 3.11 requirements-test.in --output-file requirements-test.txt
```

## Coverage and execution review, November 16, 2026

The review found incomplete default Node discovery, two optional-import skips
that could hide broken regression-test imports, repeated full-corpus projections
and audits, tests of the test's own JSON equality, and a tarball check limited to
one data member. The source-authentication, exact context, order, provenance,
lifecycle and independently frozen historical oracles remain the core checks.

Changes:

- `npm_runtime_contract.test.cjs` compares all 146,097 civil days from 1900 through
  2299 to ICU's independently implemented Coptic calendar, checks invalid types
  and boundary dates, exercises public classification/path lookup on every
  shipped date, and checks deep immutability across all 366 catalog days.
- `npm_calendar_boundary_order.test.cjs` checks the exact archive member set and
  SHA-256/length equality of every packed file. It runs the public runtime and
  timezone tests against the extracted package from outside the checkout.
  Packing uses temporary output/cache directories, disables lifecycle scripts
  and works offline. Its corruption controls clone only the affected day.
- `npm_canonical_occurrences.test.cjs` also owns the retirement-epoch regressions.
  Both use the same authenticated historical input and first projection; the
  changed-policy projection and replay checks still execute production code.
- Two full-corpus JSON-equality self-tests were removed from the final-renewal
  suite. Complete independently expected output/hash assertions and actual
  input-selector/output-policy corruption tests remain.
- The Bright Saturday stdin pipeline now lives in `tests/helpers/` and remains
  exercised by the real Python CSV/design integration. Its former Node test,
  and the Covenant Thursday equivalent, only checked that a function existed.
- `design_validation_fixture.py` shares one complete design baseline audit and
  parsed immutable inputs per Python process. Daily corruption tests rerun
  `verify_daily_rows` with real authentication and exact comparison for every
  mutant. Full schema/source/reverse-index acceptance is still exercised once;
  unrelated whole-corpus checks are no longer repeated inside each daily mutant.
  Tests copy inputs before mutation; source files stay unchanged during a run.
- Calendar-overlay tests share a single full presentation/daily generation while
  retaining the literal Tuesday assertions and all three overlay dates.
- Regression imports in `test_annual_occasion_repairs.py` now fail normally when
  code or dependencies are missing.

Measure the public JavaScript runtime separately from the Python research and
builder layers:

```bash
node --experimental-test-coverage \
  --test-coverage-include='packages/lectionary-data/*.js' --test \
  tests/synaxarium.test.cjs tests/test_authoritative_release.js \
  tests/test_npm_package_corrections.js tests/npm_runtime_contract.test.cjs
```

On Node 22.22.3, adding the new runtime contract tests to the three existing
public-runtime suites increased line coverage from **92.55% to 95.03%** and
branch coverage from **90.00% to 93.67%**. `calendar.js` remains at 100% line and
branch coverage, now with exhaustive cycle comparison. These percentages apply
only to `calendar.js` and `index.js`, not to the full repository. The remaining
uncovered runtime branch handles metadata-declared missing dates; the current
package has complete daily coverage.

Several builder unit tests still slice functions from script text into a VM.
The disposable full-builder test supplies real CLI integration coverage;
removing that source-layout coupling would require a separate builder refactor.

In the measured full Node runs on the same Mac with file concurrency set to two,
elapsed time fell from **251.55 seconds to 178.47 and 185.25 seconds (26–29%)**,
with 115 tests passing in both runs after the changes. This is one baseline and
two validation runs, not a performance guarantee. The original Python profiling
run was stopped after 178 passing tests
and 16 explicit skips at 352.81 seconds; it is not a complete Python baseline.

Final validation passed **all 1,465 Python tests in 1,590.28 seconds (26m30s)**
with two workers and the authenticated historical baseline supplied, with no
skips. The standalone package-integrity CLI also passed with zero failures.
An additional disposable-copy mutation check confirmed that the ICU comparison
rejects an injected one-day conversion error on June 17, 2199, while accepting
the unmodified control. Full Python runtime remains dominated by real corpus
integration checks; use focused commands for quick development feedback.

The historical `CalendarArtifactRegressionTests` class still requires
`LECTIONARY_CALENDAR_BASELINE` pointing to an independently authenticated 1.3.6
package. Its 16 tests are explicitly skipped without that input; do not substitute
the current package or regenerate an expected historical baseline. The other
calendar tests and all current package tests run normally. The suite does not
establish fresh live-source completeness or replace the separate release gates
in [the validation plan](LECTIONARY_VALIDATION_PLAN.md).

For this review, the published 1.3.6 tarball was fetched into a temporary
directory and its SHA-512 integrity matched the frozen baseline receipt in
[the 1.3.7 release record](LECTIONARY_1_3_7_RELEASE.md). All 16 optional calendar
tests then passed, including 21 subtests, in 11.25 seconds. To run them against
an equivalently authenticated local archive extraction:

```bash
LECTIONARY_CALENDAR_BASELINE=/absolute/path/to/extracted/package \
  uv run --python 3.11 --with-requirements requirements-test.txt \
  python -m pytest tests/test_calendar_review_repairs.py::CalendarArtifactRegressionTests
```

## Research behind the changes

- [convertdate's Coptic tests](https://github.com/fitnr/convertdate/blob/master/tests/test_coptic.py)
  use fixed known conversions, leap boundaries and round trips. We retain fixed
  boundary cases and add a full-cycle comparison to an independent implementation;
  a round trip through one implementation alone can preserve a shared defect.
- [date-fns contribution guidance](https://github.com/date-fns/date-fns/blob/main/CONTRIBUTING.md#testing)
  separates function tests from testing the built package in a consuming project.
  The extracted-archive tests apply that distinction without a global npm link.
- [Frictionless data validation](https://framework.frictionlessdata.io/docs/guides/validating-data)
  distinguishes schema/resource/package checks and supports domain-specific
  checks. This supports retaining the lectionary's exact source/context and
  provenance checks alongside structural integrity checks.
- [pytest fixture scopes](https://docs.pytest.org/en/stable/how-to/fixtures.html)
  and [temporary paths](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
  support sharing expensive setup and isolating writable artifacts. The existing
  unittest classes use a small process-local cache rather than a framework rewrite.
- [Node's execution model](https://nodejs.org/api/test.html#test-runner-execution-model)
  documents per-file process isolation and configurable file concurrency. The
  suite keeps isolation instead of using shared-process execution for speed.
- [pytest-xdist distribution](https://pytest-xdist.readthedocs.io/en/stable/distribution.html)
  documents that `loadfile` assigns all tests from one file to the same process.
  This preserves fixture reuse while two workers execute independent files.
- [npm pack](https://docs.npmjs.com/cli/v11/commands/npm-pack/)
  defines the distributed archive; checking its extracted files and running the
  public API there catches packaging faults a checkout-only test can miss.
- [Reproducible Builds](https://reproducible-builds.org/docs/deterministic-build-systems/)
  emphasizes stable inputs/outputs and reduced environmental variance. Dependency
  pins, authenticated fixtures, explicit timezones and byte comparisons apply
  that principle here without replacing provenance checks with snapshots.
