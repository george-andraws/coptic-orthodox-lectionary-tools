const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.resolve(__dirname, '..', 'packages', 'lectionary-data');
const readme = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
const reverse = fs.readFileSync(path.join(root, 'data', 'reverse_lectionary_index.jsonl'), 'utf8')
  .trim().split('\n').map(JSON.parse);

function documentedFields(section) {
  const match = readme.match(new RegExp('<!-- ' + section + '-guaranteed-fields -->\\s*```json\\s*([\\s\\S]*?)\\s*```'));
  assert.ok(match, `T-L5: missing documented ${section} guaranteed field list`);
  const fields = JSON.parse(match[1]);
  assert.ok(Array.isArray(fields) && fields.length > 0);
  assert.equal(new Set(fields).size, fields.length);
  return fields;
}

test('T-L5: reverse field guarantees hold for every published row', () => {
  const fields = documentedFields('reverse');
  assert.ok(fields.includes('day_titles'));
  for (const [index, row] of reverse.entries()) {
    for (const field of fields) assert.ok(Object.hasOwn(row, field), `reverse row ${index}: ${field}`);
  }
});

test('T-L5: daily field guarantees hold without promising day_titles', () => {
  const fields = documentedFields('daily');
  assert.ok(!fields.includes('day_titles'));
  for (const year of [2026, 2027, 2028]) {
    const days = JSON.parse(fs.readFileSync(path.join(root, 'data', 'daily', `lectionary-${year}.json`), 'utf8'));
    for (const [date, rows] of Object.entries(days)) {
      for (const row of rows) {
        for (const field of fields) assert.ok(Object.hasOwn(row, field), `${date}: ${row.identity_key}: ${field}`);
      }
    }
  }
  assert.match(readme, /day_titles.*not guaranteed in daily rows/);
});
