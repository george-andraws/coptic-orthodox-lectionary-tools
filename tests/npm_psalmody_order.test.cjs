const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
const { sortDailyReadings } = vm.runInNewContext(source.slice(source.indexOf('function dateToIso('), source.indexOf('async function main()')) + '\n({sortDailyReadings});');
const retained = JSON.parse(fs.readFileSync(path.join(root, 'packages/lectionary-data/data/daily/lectionary-2026.json')))['2026-04-11']
  .filter(r => r.source_kind !== 'psalmody_source_supplement');
const opening = {
  occasion: 'Bright Saturday', structural_day: 'Bright Saturday', service_section: 'Midnight Praises', service_hour: 'Midnight Praises',
  source_kind: 'psalmody_source_supplement', source_family: 'bright_saturday',
  slot: 'Psalm151', slot_type: 'source_label_preserved', slot_order: 1,
  current_status: 'current_confirmed_coptic_reader', removed_marker: '',
  canonical_mt_ref: '', canonical_lxx_ref: 'Ps 151', display_ref: 'Ps 151 (Reader Psalmody; LXX/source chapter only)',
  source_locator: 'sources/coptic-reader/psalmody-qualified-2026-10-25/bright-saturday-midnight-praises.full.txt:lines 5-43; sha256=3c858d0729c37fc420e08fb362967edf59d4316855d92840b9f4b4be4ede2d45',
};

test('qualified opening Psalm precedes, rather than interleaves with, Bright Saturday canticles', () => {
  const before = sortDailyReadings(retained);
  const after = sortDailyReadings([...retained, opening]);
  assert.equal(after.filter(r => r.service_section === 'Midnight Praises')[0].canonical_lxx_ref, 'Ps 151');
  const stripOrder = r => { const { reading_order, ...rest } = r; return rest; };
  assert.deepEqual(after.filter(r => r.source_kind !== 'psalmody_source_supplement').map(stripOrder), before.map(stripOrder));
  assert.equal(new Set(after.map(r => r.reading_order)).size, after.length);
});

test('inactive witnesses remain excluded from the opening-order projection', () => {
  for (const mutation of [{ active: false }, { current_status: 'historical_witness' },
    { removed_marker: 'superseded by source-qualified repair' }]) {
    assert.ok(!sortDailyReadings([...retained, { ...opening, ...mutation }])
      .some(r => r.source_kind === 'psalmody_source_supplement'));
  }
});
