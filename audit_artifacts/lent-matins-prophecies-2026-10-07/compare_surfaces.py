"""Compare complete generated surfaces with HEAD; fail on out-of-scope changes."""
import collections
import csv
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from calendar_resolution import julian_pascha_gregorian
HERE = Path(__file__).resolve().parent
TITLE = 'Wednesday of the third week of Great Lent'
TARGETS = {(julian_pascha_gregorian(year)-dt.timedelta(days=39)).isoformat() for year in range(2020, 2036)}
REFS = ['Exod 4:19-6:13', 'Joel 2:21-27', 'Isa 9:9-10:4', 'Job 12:1-14:22']

def old_bytes(relative):
    return subprocess.check_output(['git', 'show', 'HEAD:' + relative], cwd=ROOT)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def normalized(row):
    return {key: value for key, value in row.items() if value not in ('', None)}

def row_counter(rows):
    return collections.Counter(json.dumps(normalized(row), sort_keys=True, ensure_ascii=False) for row in rows)

receipt = {'baseline_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'source_capture_not_fresh_replay': True, 'target_dates': sorted(TARGETS)}
overlay = json.loads((ROOT/'sources/lectionary_corrections.json').read_text())
receipt['source_fingerprints'] = {key: value for key, value in overlay['source_fingerprints'].items() if 'lent-week3-wednesday' in key}
for key, expected in receipt['source_fingerprints'].items():
    assert sha((ROOT/key).read_bytes()) == expected, key

preserved = ['packages/lectionary-data/index.js', 'packages/lectionary-data/calendar.js', 'packages/lectionary-data/README.md', 'packages/lectionary-data/LICENSE', 'packages/lectionary-data/data/synaxarium/synaxarium.json', 'sources/katameros-api/Core/KatamerosDatabase.db', 'out/data/pascha_day_hour_index.csv', 'out/data/pascha_day_hour_index.jsonl', 'lectionary_spec.md', 'site_integration_spec.md', 'out/design/todays_readings_current_practice.csv', 'out/design/todays_readings_current_practice.jsonl', 'out/data/copticchurch_passage_index_2020_2035.csv', 'out/data/copticchurch_passage_index_2020_2035.jsonl']
receipt['preserved_bytes'] = {}
for relative in preserved:
    old = old_bytes(relative)
    new = (ROOT/relative).read_bytes()
    assert old == new, relative
    receipt['preserved_bytes'][relative] = {'sha256': sha(new), 'bytes': len(new)}

receipt['daily'] = {}
for directory, years in [('out/design/daily', range(2020, 2036)), ('packages/lectionary-data/data/daily', [2026, 2027, 2028])]:
    for year in years:
        relative = f'{directory}/lectionary-{year}.json'
        old = old_bytes(relative)
        new = (ROOT/relative).read_bytes()
        a, b = json.loads(old), json.loads(new)
        assert a.keys() == b.keys(), relative
        changed = sorted(date for date in a if a[date] != b[date])
        target = (julian_pascha_gregorian(year)-dt.timedelta(days=39)).isoformat()
        assert changed == [target], (relative, changed)
        props = [r for r in b[target] if r['source_family'] == 'coptic_reader_verified_supplement']
        assert [r['display_ref'] for r in props] == REFS
        assert [r['slot_order'] for r in props] == [1, 2, 3, 4]
        unaffected_target = [{k:v for k,v in r.items() if k != 'reading_order'} for r in b[target] if r['source_family'] != 'coptic_reader_verified_supplement']
        assert unaffected_target == [{k:v for k,v in r.items() if k != 'reading_order'} for r in a[target]], relative
        # Compare literal pretty-printed non-target date blocks, not only JSON equality.
        pattern = rb'(?ms)^  "(\d{4}-\d{2}-\d{2})": \[\n.*?^  \](?:,)?\n'
        ablocks = {m.group(1).decode():m.group(0) for m in re.finditer(pattern, old)}
        bblocks = {m.group(1).decode():m.group(0) for m in re.finditer(pattern, new)}
        assert len(ablocks) == len(a) and len(bblocks) == len(b), relative
        non_target = sorted(set(a)-{target})
        assert all(ablocks[d] == bblocks[d] for d in non_target), relative
        receipt['daily'][relative] = {'changed_dates': changed, 'old_target_readings': len(a[target]), 'new_target_readings': len(b[target]), 'non_target_dates_byte_equal': len(non_target), 'non_target_blocks_sha256': sha(b''.join(bblocks[d] for d in non_target)), 'target_original_readings_semantically_equal_except_reading_order': True}

receipt['source_date_surfaces'] = {}
# The legacy unqualified passage snapshot is deliberately not promoted: its
# unchanged builder also reapplies older corrections absent from that snapshot.
# Current helpers/design/package use the verified current-date sidecar instead.
for filename in ['copticchurch_date_readings_2020_2035.csv', 'copticchurch_date_readings_current_2020_2035.csv', 'copticchurch_passage_index_current_2020_2035.csv']:
    relative = 'out/data/'+filename
    a = list(csv.DictReader(io.StringIO(old_bytes(relative).decode())))
    b = list(csv.DictReader((ROOT/relative).open()))
    added = [row for row in b if row['source'] == 'Coptic Reader verified recurring supplement']
    assert len(added) == 64, relative
    assert {row['gregorian_date'] for row in added} == TARGETS
    # Ignore absent-vs-empty metadata only; all existing references/provenance must match.
    existing = [row for row in b if row['source'] != 'Coptic Reader verified recurring supplement']
    assert row_counter(a) == row_counter(existing), relative
    for date in TARGETS:
        rows = [r for r in added if r['gregorian_date'] == date]
        field = 'normalized_ref' if 'normalized_ref' in rows[0] else 'matched_ref'
        assert [r[field] for r in rows] == REFS, (relative, date)
    receipt['source_date_surfaces'][relative] = {'old_rows': len(a), 'new_rows': len(b), 'added_sourced_prophecies': len(added), 'all_existing_rows_semantically_equal_ignoring_absent_vs_empty_metadata': True}

# Reverse index has exactly four new context rows and one cycle Joel endpoint replacement.
relative = 'packages/lectionary-data/data/reverse_lectionary_index.jsonl'
a = [json.loads(line) for line in old_bytes(relative).splitlines()]
b = [json.loads(line) for line in (ROOT/relative).read_bytes().splitlines()]
added = row_counter(b)-row_counter(a)
removed = row_counter(a)-row_counter(b)
assert sum(added.values()) == 5 and sum(removed.values()) == 1
new_rows = [json.loads(row) for row in added]
old_rows = [json.loads(row) for row in removed]
assert old_rows[0]['display_ref'] == 'Joel 2:21-26'
assert all(row['occasion'] == TITLE or (row['display_ref'] == 'Joel 2:21-27' and row['source_kind'] == 'katameros_cycle') for row in new_rows)
receipt['reverse_delta'] = {'old_rows': len(a), 'new_rows': len(b), 'added': new_rows, 'replaced_old': old_rows, 'unchanged_rows': len(a)-1}

relative = 'out/data/bible_chapter_lectionary_occurrences.csv'
a = list(csv.DictReader(io.StringIO(old_bytes(relative).decode())))
b = list(csv.DictReader((ROOT/relative).open()))
added = row_counter(b)-row_counter(a)
removed = row_counter(a)-row_counter(b)
added_rows = [json.loads(row) for row in added]
removed_rows = [json.loads(row) for row in removed]
assert len(b)-len(a) == 144
assert sum(added.values()) == 145 and sum(removed.values()) == 1
assert all(row.get('gregorian_date') in TARGETS or row.get('passage') == 'Joel 2:21-27' for row in added_rows)
assert removed_rows[0]['passage'] == 'Joel 2:21-26'
for date in TARGETS:
    rows = [r for r in added_rows if r.get('gregorian_date') == date]
    assert len(rows) == 9
    exodus5 = [r for r in rows if r['book_abbrev'] == 'Exod' and r['chapter'] == '5']
    assert len(exodus5) == 1
receipt['chapter_delta'] = {'old_rows':len(a), 'new_rows':len(b), 'new_date_chapter_occurrences':144, 'cycle_joel_rows_replaced':1, 'exodus5_verified_on_all_16_target_dates': True}

receipt['package_meta'] = json.loads((ROOT/'packages/lectionary-data/meta.json').read_text())
receipt['changed_files'] = subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
receipt['status'] = 'pass'
(HERE/'comparisons.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({key:value for key,value in receipt.items() if key not in {'package_meta','changed_files','daily','source_fingerprints','preserved_bytes'}}, indent=2, ensure_ascii=False))
print('COMPLETE NON-TARGET COMPARISONS PASS')
