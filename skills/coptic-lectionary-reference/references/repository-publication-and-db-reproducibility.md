# Lectionary repository publication and DB reproducibility

Session pattern: when publishing the maintainer's local Coptic lectionary package to GitHub, do not assume SQLite files are disposable just because they look like generated/cache artifacts.

## Durable finding

The generated query helper can answer lookups from committed CSV/JSONL outputs without the SQLite database:

```bash
python3 out/scripts/query_lectionary.py --date 2032-04-07
python3 out/scripts/query_lectionary.py --passage "John 2" --include-crosswalk
```

But a full local rebuild requires the Katameros SQLite database:

```text
sources/katameros-api/Core/KatamerosDatabase.db
```

`build_lectionary_reference.py` sets:

```python
DB = SRC / 'katameros-api' / 'Core' / 'KatamerosDatabase.db'
```

and uses `sqlite3.connect(DB)` in `load_books()` / cycle export code. Without the real DB, the rebuild path fails or can accidentally create an empty SQLite file.

The generated package also publishes an identical copy at:

```text
out/sources/KatamerosDatabase.sqlite
```

That file is useful for packaged source/provenance completeness and should be included when the repository goal is "clone and run immediately."

## Git ignore rule for public repo

Do include:

```text
sources/katameros-api/Core/KatamerosDatabase.db
out/sources/KatamerosDatabase.sqlite
```

Do not include transient SQLite sidecars:

```text
*.db-shm
*.db-wal
*.sqlite-shm
*.sqlite-wal
```

Recommended `.gitignore` shape:

```gitignore
# Python bytecode/cache
__pycache__/
*.py[cod]
*.pyo

# SQLite transient sidecar files
*.sqlite-*
*.db-*

# Include required SQLite source/package databases for reproducible local rebuilds
!sources/katameros-api/Core/KatamerosDatabase.db
!out/sources/KatamerosDatabase.sqlite
```

## Verification commands

Before claiming the repo is reproducible:

```bash
sqlite3 sources/katameros-api/Core/KatamerosDatabase.db 'pragma integrity_check; select count(*) from Books;'
sqlite3 out/sources/KatamerosDatabase.sqlite 'pragma integrity_check; select count(*) from Books;'
PYTHONDONTWRITEBYTECODE=1 python3 verify_lectionary_queries.py
python3 - <<'PY'
import build_lectionary_reference as b
books = b.load_books()
print('db_path', b.DB)
print('book_count', len(books))
PY
```

Expected durable values from the current dataset:

```text
integrity_check: ok
Books count: 73
DB sha256: 19fe28dffc81007001049c2b07ce124400e28648bbb0cfd358528fca8252ff9e
```

## Pitfall

Testing "what happens if the DB is absent" by moving the DB away and importing/running code that calls `sqlite3.connect(DB)` may create a new empty DB file at the original path. If you do this, restore the real DB from a known-good copy before staging/committing. Verify with `pragma integrity_check`, table count, and sha256 before pushing.
