"""Verify actual tarball bytes and an isolated, offline installed consumer."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'packages/lectionary-data'
TARBALL = AUDIT / 'andraws-lectionary-data-1.3.1.tgz'
expected_files = {str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob('*') if p.is_file()}
packed_hashes = {}
with tarfile.open(TARBALL, 'r:gz') as archive:
    members = [m for m in archive.getmembers() if not m.isdir()]
    assert all(m.isfile() and m.name.startswith('package/') for m in members)
    names = [m.name[len('package/'):] for m in members]
    assert len(names) == len(set(names))
    assert set(names) == expected_files
    for member, name in zip(members, names):
        stream = archive.extractfile(member)
        assert stream is not None, name
        data = stream.read()
        assert data == (PACKAGE / name).read_bytes(), name
        packed_hashes[name] = hashlib.sha256(data).hexdigest()

node_script = r'''
const assert = require('node:assert/strict');
const fs = require('node:fs');
const api = require('@andraws/lectionary-data');
const manifest = require('@andraws/lectionary-data/package.json');
assert.equal(manifest.version, '1.3.1');
const refs = ['Exod 4:19-6:13', 'Joel 2:21-27', 'Isa 9:9-10:4', 'Job 12:1-14:22'];
const targetDates = ['2026-03-04', '2027-03-24', '2028-03-08'];
for (const date of targetDates) {
  const rows = JSON.parse(fs.readFileSync(api.dailyYearPath(Number(date.slice(0,4))), 'utf8'))[date];
  const matins = rows.filter(r => r.service_section === 'Matins');
  assert.deepEqual(matins.slice(0,4).map(r=>r.display_ref), refs);
  assert.deepEqual(matins.map(r=>r.slot_type), ['prophecy','prophecy','prophecy','prophecy','psalm','gospel']);
  assert.deepEqual(rows.map(r=>r.reading_order), [1,2,3,4,5,6,7,8,9,10,11]);
  assert.ok(matins.slice(0,4).every(r=>api.isCurrentReading(r)));
  assert.equal(JSON.parse(matins[1].spans_json)[0].verse_end, 27);
}
const reverse=fs.readFileSync(api.occasionIndexPath,'utf8').trim().split('\n').map(JSON.parse);
const prophecies=reverse.filter(r=>r.occasion==='Wednesday of the third week of Great Lent' && r.slot_type==='prophecy');
assert.equal(prophecies.length,4);
assert.deepEqual(prophecies.sort((a,b)=>a.slot_order-b.slot_order).map(r=>r.display_ref),refs);
assert.equal(api.synaxariumMeta.day_count,366);
assert.equal(api.synaxariumMeta.total_commemorations,868);
assert.equal(api.synaxariumForCopticDay('tout',1).commemorations.length,5);
assert.deepEqual(api.gregorianToCoptic(2026,9,11),{year:1743,monthSlug:'tout',day:1});
assert.deepEqual(api.gregorianToCoptic(2027,9,11),{year:1743,monthSlug:'nasie',day:6});
console.log(JSON.stringify({version:manifest.version,target_dates:targetDates,ordered_references:refs,reverse_prophecy_rows:prophecies.length,synaxarium_days:366,synaxarium_commemorations:868,calendar_smoke:'pass',status:'pass'}));
'''
with tempfile.TemporaryDirectory(prefix='lectionary-packed-consumer-', dir=os.environ['TMPDIR']) as directory:
    install = subprocess.run(['npm', 'install', '--prefix', directory, '--offline', '--ignore-scripts', '--no-package-lock', '--no-audit', '--no-fund', str(TARBALL)], text=True, capture_output=True)
    (AUDIT / 'packed-offline-install.log').write_text(install.stdout + install.stderr)
    assert install.returncode == 0, install.stdout + install.stderr
    installed = Path(directory) / 'node_modules/@andraws/lectionary-data'
    for name, expected_hash in packed_hashes.items():
        assert hashlib.sha256((installed / name).read_bytes()).hexdigest() == expected_hash, name
    consumer = subprocess.run(['node', '-e', node_script], cwd=directory, capture_output=True, text=True)
    (AUDIT / 'packed-consumer.log').write_text(consumer.stdout + consumer.stderr)
    assert consumer.returncode == 0, consumer.stdout + consumer.stderr
    result = json.loads(consumer.stdout)

remaining_gaps = {}
for year in (2026, 2027, 2028):
    days = json.loads((PACKAGE / f'data/daily/lectionary-{year}.json').read_text())
    labelled = {date: rows for date, rows in days.items() if any(re.match(r'^(Monday|Tuesday|Wednesday|Thursday|Friday) of the .* week of Great Lent$', row.get('occasion', ''), re.I) for row in rows)}
    missing = [date for date, rows in labelled.items() if not any(row.get('slot_type') == 'prophecy' for row in rows)]
    remaining_gaps[str(year)] = {'labelled_lent_weekdays': len(labelled), 'without_prophecy_rows': len(missing), 'dates_without_prophecy_rows': missing}
result.update({'tarball':str(TARBALL), 'sha256':hashlib.sha256(TARBALL.read_bytes()).hexdigest(), 'bytes':TARBALL.stat().st_size, 'packed_file_count':len(packed_hashes), 'packed_file_sha256':packed_hashes, 'offline_install':'pass', 'installed_bytes_match_tarball':True, 'remaining_lent_coverage_gaps':remaining_gaps})
(AUDIT / 'packed-candidate-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
