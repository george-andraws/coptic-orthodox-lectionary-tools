"""Bounded local verification runner; never publishes artifacts."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
label, *command = sys.argv[1:]
env = dict(os.environ, LECTIONARY_DISABLE_VAULT_PUBLISH='1', TMPDIR=str(Path.home() / '.hermes/cache/scratch'))
start = time.time()
result = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
log = HERE / f'{label}.log'
log.write_text(result.stdout)
receipt_path = HERE / 'commands.json'
receipts = json.loads(receipt_path.read_text()) if receipt_path.exists() else []
receipts.append(dict(label=label, command=command, cwd=str(ROOT), env_overrides={key: env[key] for key in ['LECTIONARY_DISABLE_VAULT_PUBLISH', 'TMPDIR', 'LECTIONARY_BUILDER_UNDER_TEST'] if key in env}, exit_code=result.returncode, duration_seconds=round(time.time()-start, 3), log=str(log.relative_to(ROOT))))
receipt_path.write_text(json.dumps(receipts, indent=2) + '\n')
print(result.stdout[-8000:])
print(f'RECEIPT {label}: exit={result.returncode}', flush=True)
sys.exit(result.returncode)
