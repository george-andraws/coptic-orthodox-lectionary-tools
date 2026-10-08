const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const sourceFile = 'sources/coptic-reader/last-friday-2028-04-07-2026-10-07/verified-table.json';
const date = '2028-04-07';
const digest = body => crypto.createHash('sha256').update(body).digest('hex');

function oracle() {
  const bytes = fs.readFileSync(path.join(root, sourceFile));
  assert.equal(digest(bytes), 'f3b3bffbf99bf1a972f5c1abc2b2a4e7504774ae67a8111e1d9358011cd8deb4');
  const source = JSON.parse(bytes);
  for (const [file, hash] of Object.entries(source.source_fingerprints)) {
    assert.equal(digest(fs.readFileSync(path.join(root, path.dirname(sourceFile), file))), hash, file);
  }
  assert.equal(source.verified_date, date);
  assert.equal(source.feast_collision, 'Annunciation');
  assert.equal(source.pascha_offset_days, -9);
  assert.equal(source.suppressed_service, 'Vespers');
  assert.equal(source.readings.length, 11);
  assert.deepEqual(source.readings.map(r => r.source_order), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]);
  return source.readings;
}

function verify(body) {
  const expected = oracle();
  const design = JSON.parse(fs.readFileSync(path.join(root, 'out/design/daily/lectionary-2028.json')))[date];
  const rows = JSON.parse(body)[date];
  const tuple = r => [r.service_section, r.slot, r.display_ref.replace(/ \(LXX .*\)$/, '')];
  const sourceTuple = r => [r.service_section, r.source_slot, r.normalized_ref];
  assert.deepEqual(design.map(tuple), expected.map(sourceTuple), 'design must match the complete authenticated table');
  assert.deepEqual(rows.map(tuple), expected.map(sourceTuple), 'consumer must preserve the entire source sequence');
  assert.deepEqual(rows.map(r => r.reading_order), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]);
  assert.deepEqual(rows.map(r => r.service_order), [2, 2, 2, 2, 2, 2, 99, 99, 99, 99, 99]);
  assert.deepEqual(rows.map(r => r.slot_order), [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5]);
  assert.deepEqual(rows.map(r => r.slot_type), ['prophecy', 'prophecy', 'prophecy', 'prophecy', 'psalm', 'gospel', 'pauline', 'catholicon', 'praxis', 'psalm', 'gospel']);
  // Preserve all supplied identity, disclosure, lifecycle and coordinate/hold metadata.
  for (let i = 0; i < rows.length; i++) {
    assert.equal(rows[i].source_file, sourceFile);
    assert.equal(rows[i].source_family, 'coptic_reader_verified_calendar_boundary');
    assert.equal(rows[i].source_row_id, `boundary:${sourceFile}:${date}:${i + 1}`);
    const { reading_order, service_order, slot_order, slot_type, ...actualMetadata } = rows[i];
    const { service_order: ignoredService, slot_order: ignoredOrder, slot_type: ignoredType, ...expectedMetadata } = design[i];
    assert.deepEqual(actualMetadata, expectedMetadata, `metadata at source ordinal ${i + 1}`);
  }
}

test('npm Last-Friday/Annunciation daily retains complete authenticated table and metadata', () => {
  verify(fs.readFileSync(path.join(root, 'packages/lectionary-data/data/daily/lectionary-2028.json')));
});

test('actual npm tarball retains complete Last-Friday/Annunciation table and metadata', () => {
  const destination = fs.mkdtempSync(path.join(os.tmpdir(), 'lectionary-boundary-pack-'));
  try {
    const packed = JSON.parse(execFileSync('npm', ['pack', '--json', '--pack-destination', destination], {
      cwd: path.join(root, 'packages/lectionary-data'), encoding: 'utf8',
    }));
    assert.equal(packed.length, 1);
    const tarball = path.join(destination, packed[0].filename);
    const member = execFileSync('tar', ['-xOf', tarball, 'package/data/daily/lectionary-2028.json'], { maxBuffer: 32 * 1024 * 1024 });
    assert.deepEqual(member, fs.readFileSync(path.join(root, 'packages/lectionary-data/data/daily/lectionary-2028.json')));
    verify(member);
  } finally {
    fs.rmSync(destination, { recursive: true, force: true });
  }
});
