"""Record pre-existing historical-index rebuild drift before restoring it."""
import ast
import collections
import csv
import io
import json
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
relative = 'out/data/copticchurch_passage_index_2020_2035.csv'
old = list(csv.DictReader(io.StringIO(subprocess.check_output(['git', 'show', 'HEAD:'+relative], cwd=ROOT, text=True))))
with (ROOT/relative).open() as stream:
    current = [row for row in csv.DictReader(stream) if row['source'] != 'Coptic Reader verified recurring supplement']
normalize = lambda row: json.dumps({k:v for k,v in row.items() if v not in ('', None)}, sort_keys=True)
a, b = collections.Counter(map(normalize, old)), collections.Counter(map(normalize, current))
head_source = subprocess.check_output(['git','show','HEAD:build_lectionary_reference.py'], cwd=ROOT, text=True)
new_source = (ROOT/'build_lectionary_reference.py').read_text()
function = lambda source: ast.dump(next(node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == 'build_date_passage_index'))
assert function(head_source) == function(new_source)
receipt = {'classification':'pre-existing stale legacy raw passage snapshot, not a current helper/package regression', 'builder_function_unchanged_from_HEAD':True, 'baseline_rows':len(old), 'regenerated_existing_rows':len(current), 'old_rows_not_equal':sum((a-b).values()), 'regenerated_rows_not_equal':sum((b-a).values()), 'examples_old':[json.loads(x) for x in list(a-b)[:3]], 'examples_regenerated':[json.loads(x) for x in list(b-a)[:3]], 'disposition':'Restore both unqualified legacy passage-index snapshots byte-for-byte to HEAD. Current-date sidecars, date helpers, crosswalk, chapter indexes and package carry all 64 supplemented readings. Do not promote unrelated historical-source corrections in this bounded task.'}
(HERE/'legacy-snapshot-drift.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
