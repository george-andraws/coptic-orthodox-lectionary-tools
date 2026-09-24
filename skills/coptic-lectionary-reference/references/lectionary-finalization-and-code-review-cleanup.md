# Lectionary finalization and code-review cleanup

Use this reference when maintaining the maintainer's local Coptic lectionary package after special-service expansion or code-review feedback.

## Local project

Repo/workspace:

```text
$REPO_ROOT
```

Primary generated package:

```text
out/data/
out/scripts/query_lectionary.py
out/scripts/passage_normalization.py
```

downstream documentation publication target remains the local lectionary reference folder under the maintainer's downstream documentation package.

## Durable lessons from the finalization pass

### 1. Treat malformed raw refs as source defects, not invisible data

The copticchurch.net scrape contains repeatable malformed raw refs such as:

```text
Mk 14:-3-9
Mk 14:-39
```

Do not let these silently normalize into clean-looking refs without metadata. The durable pattern is:

- keep the raw source ref intact
- repair narrowly-known scraper glitches for indexing
- add explicit status/warning fields
- write a repair/quarantine report
- verify normalized/crosswalk outputs are clean while raw defects are accounted for

Implemented fields/files:

```text
copticchurch_date_readings_2020_2035.csv: parse_status, normalization_warning
copticchurch_passage_index_2020_2035.csv: source_ref_status, normalization_warning
out/data/source_ref_repair_report.csv
out/data/source_ref_repair_report.jsonl
```

Verifier should distinguish:

- raw suspicious refs may remain if they are reported
- normalized refs must be clean
- reverse lookup crosswalk must be clean

### 2. Parser guardrails

Direct parsing should reject malformed/open-ended refs rather than creating plausible invalid passage objects.

Regression cases to keep:

```python
assert passage_matches("John 2", "Jn 20:1-18") is False
assert passage_matches("John 2", "1Jn 2:1-6") is False
assert passage_matches("Isa 5", "Isa 58:1-11") is False
assert passage_matches("Isa 53", "Isa 52:13-53:12") is True
assert parse_passage("John 3:16--18") is None
assert parse_passage("Mk 14:-39") is None
assert parse_passage("John 19:1-") is None
assert extract_text_ref_tokens("John 19:1- John 19:16") == ["Jn 19:1-16"]
assert extract_text_ref_tokens("Mk 14:-39") == ["Mark 14:39"]
```

The subtle distinction matters: `parse_passage()` should stay strict, while `extract_text_ref_tokens()` may repair known source glitches for source-index extraction.

### 3. Query usability for reverse lookup

When `--include-crosswalk` is used, do not append crosswalk rows behind date rows where they are hidden by `--limit`. Print separate sections instead:

```text
## date results
...
## reverse crosswalk results
...
```

This makes cycle, Pascha, Agpeya, and special-service occurrences visible even for common passages like John 2.

### 4. Generated query helper should not live only as an embedded string

Keep a tracked source helper:

```text
query_lectionary.py
```

Then copy it into:

```text
out/scripts/query_lectionary.py
```

This mirrors the `passage_normalization.py` pattern and allows direct review/testing before generation.

### 5. Reproducible build scope

Make scripts repo-relative with:

```python
ROOT = Path(__file__).resolve().parent
```

For Pascha/Bright Saturday, prefer canonical `out/data` artifacts and fall back to legacy side-output dirs only when needed:

```text
out/data/pascha_day_hour_index.csv
out/data/bright_saturday_service_order.csv
legacy fallbacks: out2/, out_bright/
```

Guard against same-file copy errors when a canonical source is already in `out/data`.

### 6. Synaxarium is separate unless explicitly brought into the package

Do not automatically fold Synaxarium into the lectionary package. It is a related source map, not part of the main lectionary query helper today.

Current preferred handling:

```text
build_synaxarium_index.py -> out_synaxarium/
```

Document it as separate in `README.md` rather than adding it to `BUILD_SUMMARY` or `query_lectionary.py` unless the requester explicitly asks for Synaxarium queries.

## Final verification recipe

After code-review cleanup or data-structure changes, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile \
  passage_normalization.py query_lectionary.py \
  build_lectionary_reference.py build_lectionary_crosswalk.py \
  build_synaxarium_index.py verify_lectionary_queries.py

python3 build_lectionary_reference.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py

cmp -s query_lectionary.py out/scripts/query_lectionary.py
cmp -s passage_normalization.py out/scripts/passage_normalization.py

test -f out/data/reverse_lookup_crosswalk.csv
test -f out/data/pascha_day_hour_index.csv
test -f out/data/bright_saturday_service_order.csv
test -f out/data/source_ref_repair_report.csv
test -f out/scripts/query_lectionary.py

rg -n ':-|--|[0-9]+:[0-9]+\s*[-–—]\s*$' out/data/*.csv
```

Interpret the suspicious scan carefully:

- Hits in `source_ref_repair_report.csv` are expected.
- Hits in raw fields of copticchurch date/passage CSVs are acceptable only when covered by the repair report.
- Hits in normalized refs or `reverse_lookup_crosswalk.csv` are bugs.

## downstream documentation logging

For substantial lectionary package changes, append a concise entry to:

```text
the project's configured operational log, if one exists
```

Mention what changed, what verification ran, and any remaining intentional caveats.