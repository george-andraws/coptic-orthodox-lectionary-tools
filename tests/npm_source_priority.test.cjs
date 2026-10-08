const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

test('explicit authenticated Reader families outrank public working sources in npm projection', () => {
  // Evaluate the actual trusted constant, not a duplicate test priority table.
  const source = fs.readFileSync(path.join(__dirname, '../scripts/build_npm_package.mjs'), 'utf8');
  const literal = source.match(/const SOURCE_PRIORITY = new Map\(([\s\S]*?)\);/)[1];
  const priority = vm.runInNewContext(`new Map(${literal})`);
  for (const family of ['coptic_reader_verified_calendar_boundary', 'coptic_reader_verified_supplement', 'coptic_reader_verified_sunday_policy']) {
    assert.ok((priority.get(family) ?? 100) < priority.get('ordinary_date_resolved'), family);
  }
  assert.equal(priority.get('unverified_coptic_reader_label'), undefined);
});
