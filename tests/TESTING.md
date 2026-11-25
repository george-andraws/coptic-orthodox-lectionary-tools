# Python release testing and bounded performance review

The repository has mixed `unittest.TestCase` and pytest functions/fixtures/parameterization. Use pytest for the complete Python inventory; unittest discovery alone is not equivalent. The existing `npm run test:python` remains the two-worker CI flow in `package.json`. This follow-up does not change producer code, package data, authenticated source pins, runtime exports, timeouts or publication.

## Serial fail-fast historical compatibility lane

For an expensive serial release acceptance, use the same full pytest command with `--historical-first -x`:

```sh
TMPDIR=/your/owned/scratch \
LECTIONARY_CALENDAR_BASELINE=/absolute/authenticated-1.3.6/package \
uv run --python 3.11 --with-requirements requirements-test.txt \
  python -m pytest tests --historical-first -x -v --tb=short \
  --durations=30 --junitxml=/your/owned/results/full-python.xml
```

The original calendar baseline is the authenticated real npm **1.3.6** package, never the current artifact. `tests/conftest.py` moves the five existing formerly stale source-fixture/historical-version/serialized-output controls to the front, cheap to expensive. They still execute **once**, followed by every other selected test. `-x` stops on the first failure; omit `-x` for a diagnostic run that continues. No separate preflight invocation, cached verdict, skip or repeated historical lane is involved. The option rejects incomplete selection and parallel scheduling rather than claiming that a loadfile scheduler preserves this serial order. Without the option, normal collection order and CI concurrency are unchanged.

Preflight collection separately before a long run:

```sh
uv run --python 3.11 --with-requirements requirements-test.txt \
  python -m pytest tests --historical-first --collect-only -q
```

Read the actual terminal exit, summary, complete counts, warnings and input-preservation result. Collection is not execution. Keep logs, JUnit and immediate failure reports outside the source tree. A short-lived worker should return READY with the exact frozen input bindings and let its parent launch/own a long notified final run; do not leave an untransferred child process that will be killed on worker exit.

## Why the Sunday corruption matrices use two levels

Profiling the unchanged release checkout identified repeated complete Mark/release/Holy Week/Jonah materialization inside three Sunday-only corruption matrices. Their immutable class inputs were already parsed once. The expensive repetition was unrelated prerequisite reconstruction, not the local corruption logic.

The revised matrices authenticate their complete current-version prerequisites through the actual production `followup_daily_view(..., version='1.3.13')` and Mark inverse **once per test**, then send every independent mutation through the actual `contextual_counters` boundary in its declared historical comparison domain. Each invocation still decodes its CSV and JSON, authenticates the Sunday witnesses, checks actual source/body/service/reference/order/lifecycle/flags and compares complete dated Sunday sequences. Nothing replaces a guard, source loader or oracle with mocked success; no authentication/comparison verdict is cached. The narrower helper requires Sunday-specific refusals rather than allowing an unrelated missing prerequisite to bless a mutation.

All original ten Sunday test identities and mutation loops remain. Full current file/version checks, cleaned-Psalm refusals, all selected shipped Sunday table multiplicities, immutable manifest/oracle/body/SQLite drift, policy-fingerprint drift, symmetric wrong-date/source errors, calendar-boundary order and nonzero CLI behavior remain on the original unmodified file caller. An additional file-caller test retains real source-service, package-type and duplicate corruption integration. This is a bounded test-layer optimization, not permission to replace full package/corpus acceptance with a subset.

## Measurement contract

Compare the same affected module, inputs, interpreter/dependency lock, single worker, process priority and profiling mode before and after. Use fresh Python processes to include cold imports/setup. Call that application-cold, not OS-cold: do not claim filesystem caches were dropped unless they actually were. Preserve per-test durations, JUnit identities/subtests, function-call profiles, real child exits and the complete before/after input hashes. Report matrix-only and full affected-module timing separately; do not extrapolate a measured module speedup into an unexecuted full-suite result.

The source-independent review receipts also compare the original mutation control-flow ASTs after substituting only the intended refusal-helper name; the original constants, operations, order and loops must match. The full suite still runs on the final frozen source with the authentic historical baseline. No package rebuild, npm version bump, publication or site file change is necessary for a test-only follow-up.
