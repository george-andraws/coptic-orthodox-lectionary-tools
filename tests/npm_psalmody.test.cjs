const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const pkg = path.join(root, 'packages/lectionary-data');
const rows = fs.readFileSync(path.join(pkg, 'data/reverse_lectionary_index.jsonl'), 'utf8')
  .trim().split('\n').map(JSON.parse);
const current = row => !row.removed_marker && row.active !== false &&
  ['current_confirmed_coptic_reader', 'current_public_or_local_reference'].includes(row.current_status);
const psalmody = rows.filter(row => current(row) && row.source_kind === 'psalmody_source_supplement');

test('package contains precisely twelve source-qualified Psalmody chapter occurrences', () => {
  const expected = [
    ['Bright Saturday', 'Ps 151'],
    ...['Church Consecration (Part 1)', 'Preparation of the Holy Myron'].flatMap(occasion =>
      [151, 148, 149, 150].map(chapter => [occasion, `Ps ${chapter}`])),
    ...[148, 149, 150].map(chapter => ['Pentecost Prostration Praises', `Ps ${chapter}`]),
  ];
  // Compare declared source stages below, without guessing a stage from a rite
  // label: those are independent fields in the authenticated source manifest.
  const manifest = JSON.parse(fs.readFileSync(path.join(root,
    'sources/coptic-reader/psalmody-qualified-2026-10-25/source-manifest.json')));
  const occasions = { bright_saturday: 'Bright Saturday', church_consecration_part1: 'Church Consecration (Part 1)',
    myron_preparation: 'Preparation of the Holy Myron', pentecost_prostration_praises: 'Pentecost Prostration Praises' };
  const exact = manifest.records.map(r => [occasions[r.rite], r.rite === 'bright_saturday' ? 'Midnight Praises' : r.stage, `Ps ${r.chapter}`]);
  assert.deepEqual(psalmody.map(r => [r.occasion, r.canonical_lxx_ref]).sort(), expected.sort());
  assert.deepEqual(psalmody.map(r => [r.occasion, r.service_section, r.canonical_lxx_ref]).sort(), exact.sort());
  for (const row of psalmody) {
    assert.equal(row.canonical_mt_ref, '');
    const [span] = JSON.parse(row.spans_json);
    assert.equal(span.book, 'Ps');
    assert.equal(span.chapter_start, span.chapter_end);
    assert.equal(span.verse_start, null);
    assert.equal(span.verse_end, null);
    assert.match(row.source_locator, /sha256=[a-f0-9]{64}/);
    assert.ok(JSON.parse(row.source_disclosure).length);
    assert.equal(row.provenance_format, 'lectionary_provenance_v1');
    assert.ok(row.provenance.length <= 300);
    const transport = JSON.parse(row.provenance_evidence_json);
    assert.equal(transport.schema, row.provenance_format);
    assert.deepEqual(Object.keys(transport).sort(), ['legacy_provenance', 'schema']);
    assert.ok(JSON.parse(transport.legacy_provenance).body_literal);
  }
});

test('each shipped Bright Saturday opens Midnight Praises with source-only Psalm 151', () => {
  for (const [year, date] of [[2026, '2026-04-11'], [2027, '2027-05-01'], [2028, '2028-04-15']]) {
    const daily = JSON.parse(fs.readFileSync(path.join(pkg, `data/daily/lectionary-${year}.json`)));
    const praises = daily[date].filter(r => r.service_section === 'Midnight Praises');
    assert.ok(praises.length > 1);
    assert.equal(praises[0].canonical_lxx_ref, 'Ps 151');
    assert.equal(praises[0].canonical_mt_ref, '');
    assert.equal(praises.filter(r => r.source_kind === 'psalmody_source_supplement').length, 1);
    assert.ok(praises.every(r => r.slot !== 'FourthHoos'), 'do not transplant another service’s Fourth Hoos');
  }
});

test('special-service Psalmody does not become an ordinary daily recurrence', () => {
  for (const year of [2026, 2027, 2028]) {
    const daily = JSON.parse(fs.readFileSync(path.join(pkg, `data/daily/lectionary-${year}.json`)));
    for (const [date, readings] of Object.entries(daily)) {
      const additions = readings.filter(r => r.source_kind === 'psalmody_source_supplement');
      for (const row of additions) {
        assert.equal(row.source_family, 'bright_saturday', date);
        assert.equal(row.slot, 'Psalm151', date);
        assert.equal(row.occasion, 'Bright Saturday', date);
      }
    }
  }
});
