const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const zlib = require('node:zlib');
const root = path.resolve(__dirname, '..');
const builder = fs.readFileSync(path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
const { sortDailyReadings, addMissingStructuralDailyRows } = vm.runInNewContext(
  builder.slice(builder.indexOf('function dateToIso('), builder.indexOf('async function main()'))
  + '\n({sortDailyReadings,addMissingStructuralDailyRows});');
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const frozenBytes = fs.readFileSync(path.join(root, 'tests/fixtures/good-friday-published-1.3.11.json.gz'));
assert.equal(digest(frozenBytes), '54f264bdb981bbc7e8fbbaad9c2554b7bdc28c6a62599c9e3a8025ae7e73f4d3');
const baseline = JSON.parse(zlib.gunzipSync(frozenBytes));
assert.equal(baseline.tarball_sha256, '2cfd1bd05a721edd4b48323161bedc415ff019107efeff0c10f4f5f75f5772f5');
const plain = value => JSON.parse(JSON.stringify(value));
const refs = rows => Array.from(rows, row => row.canonical_mt_ref);
const gospel = (rows, hour) => rows.filter(r => r.occasion === 'Good Friday' && r.service_section === hour && r.slot === 'Gospel');
const expectedRefs = {
  'Sixth Hour': ['Matt 27:27-45', 'Mark 15:26-33', 'Lk 23:26-44', 'Jn 19:13-27'],
  'Twelfth Hour': ['Matt 27:57-61', 'Mark 15:42-16:1', 'Lk 23:50-56', 'Jn 19:38-42'],
};
const sourceTables = [
  ['sources/coptic-reader/holy-week-review-qualified-2026-10-29/friday--6th-hour.txt',
    'aae5386449ddad8f45ca625402bd4ed3ee9c885c10c05e161e69f77e02110c57',
    'Great Friday (The Sixth Hour)', [499, 592, 635, 711],
    ['Matthew 27:27-45', 'Mark 15:26-33', 'Luke 23:26-44', 'John 19:13-27']],
  ['sources/coptic-reader/pascha-resolution-qualified-2026-10-25/fresh-pascha/friday--12th-hour.txt',
    '9a6bd0b11b67fa6d3cfbe10a99b84a085796b8b3e886ddec4d191ef02dbe2e0e',
    'Great Friday (The Twelfth Hour)', [182, 232, 272, 312],
    ['Matthew 27:57-61', 'Mark 15:42-16:1', 'Luke 23:50-56', 'John 19:38-42']],
];
function expectedDay(rows) {
  const expected = plain(rows);
  for (const [hour, ordered] of Object.entries(expectedRefs)) {
    const selected = gospel(rows, hour);
    assert.equal(selected.length, 4);
    let next = 0;
    for (let i = 0; i < expected.length; i++) {
      if (expected[i].service_section === hour && expected[i].slot === 'Gospel') {
        const reference = ordered[next++];
        expected[i] = plain(selected.find(r => r.canonical_mt_ref === reference));
      }
    }
  }
  return expected.map((r, i) => ({ ...r, reading_order: i + 1 }));
}

test('authenticated whole-hour captures supply literal complete Gospel sequences, not a generic book sort', () => {
  for (const [relative, hash, title, lines, printed] of sourceTables) {
    const bytes = fs.readFileSync(path.join(root, relative));
    assert.equal(digest(bytes), hash);
    const text = bytes.toString('utf8').split('\n');
    assert.equal(text[0].trim(), title);
    assert.deepEqual(lines.map(n => text[n - 1].trim()), printed);
    // Complete English heading census within each retained full document.
    assert.deepEqual(text.map(s => s.trim()).filter(s => /^(Matthew|Mark|Luke|John) \d+:/.test(s)), printed);
  }
});

test('published predecessor keeps its original wrong orders and archived Sixth-Hour John', () => {
  for (const rows of Object.values(baseline.daily)) {
    assert.equal(rows.length, 65);
    assert.deepEqual(refs(gospel(rows, 'Sixth Hour')), ['Matt 27:27-45', 'Lk 23:26-44', 'Mark 15:26-33', 'Jn 19:13-27']);
    assert.deepEqual(refs(gospel(rows, 'Twelfth Hour')), ['Jn 19:38-42', 'Lk 23:50-56', 'Mark 15:42-16:1', 'Matt 27:57-61']);
  }
  const held = baseline.reverse_rows.filter(r => r.service_hour === 'Sixth Hour' && r.canonical_mt_ref === 'Jn 19:1-12');
  assert.equal(held.length, 1);
  assert.equal(held[0].active, false);
  assert.equal(held[0].current_status, 'pending_coptic_reader_review');
});

for (const [date, rows] of Object.entries(baseline.daily)) {
  test(`${date}: complete 65-row day changes only the two approved Gospel permutations`, () => {
    const before = plain(rows);
    const sorted = sortDailyReadings(rows, date);
    assert.deepEqual(plain(sorted), expectedDay(rows));
    assert.deepEqual(plain(sortDailyReadings(sorted, date)), plain(sorted));
    assert.deepEqual(rows, before, 'no mutation of frozen source witnesses');
    assert.equal(gospel(sorted, 'Sixth Hour').some(r => r.canonical_mt_ref === 'Jn 19:1-12'), false);
  });
}

for (const hour of Object.keys(expectedRefs)) {
  const input = gospel(baseline.daily['2026-04-10'], hour);
  test(`${hour}: all 24 input permutations retain the literal supplied sequence`, () => {
    function permutations(xs) { return xs.length ? xs.flatMap((x, i) => permutations(xs.filter((_, n) => n !== i)).map(tail => [x, ...tail])) : [[]]; }
    const variants = permutations(input);
    assert.equal(variants.length, 24);
    for (const rows of variants) assert.deepEqual(refs(sortDailyReadings(rows, '2026-04-10')), expectedRefs[hour]);
  });
  test(`${hour}: wrong dates, nights, source families/kinds, locators and incomplete quartets do not qualify`, () => {
    const legacy = (rows, date) => refs(sortDailyReadings(rows, date));
    for (const date of ['', '2026-04-09', '2026-04-11', '2029-04-06']) {
      assert.deepEqual(legacy(input, date), refs(input), date);
    }
    for (const mutation of [{ source_family: 'other' }, { source_kind: 'other' }, { occasion: 'Good Friday Eve' },
      { service_section: 'First Hour', service_hour: 'First Hour' }, { source_locator: 'other.csv:row 1; source_ref=untrusted' },
      { identity_key: 'other' }, { canonical_mt_ref: 'Jn 19:1-12' }]) {
      // Mutate one witness, not the entire table: no partial repaired quartet.
      const changed = input.map((r, i) => i === 0 ? { ...r, ...mutation } : { ...r });
      assert.deepEqual(legacy(changed, '2026-04-10'), legacy(changed, ''), JSON.stringify(mutation));
    }
    for (const mutation of [{ active: false }, { current_status: 'historical_witness' }, { removed_marker: 'superseded by repair' }]) {
      const changed = input.map((r, i) => i === 0 ? { ...r, ...mutation } : { ...r });
      assert.deepEqual(legacy(changed, '2026-04-10'), legacy(changed, ''), JSON.stringify(mutation));
    }
    for (const rows of [input.slice(1), [...input, input[0]]]) {
      assert.deepEqual(legacy(rows, '2026-04-10'), legacy(rows, ''), 'missing or duplicate Gospel');
    }
  });
}

test('structural fill with an empty or populated Good Friday preserves companions and the corrected order', () => {
  const reverse = baseline.reverse_rows;
  for (const [date, rows] of Object.entries(baseline.daily)) {
    const year = Number(date.slice(0, 4));
    // The real later Holy Week review lane supplies this qualified John row;
    // structural fill itself only owns legacy families. Supply that genuine
    // prerequisite instead of broadening its source-family membership here.
    const supplement = rows.filter(r => r.source_family === 'coptic_reader_qualified_holy_week_review');
    assert.equal(supplement.length, 1);
    for (const seed of [{ [date]: plain(supplement) }, { [date]: plain(rows) }]) {
      addMissingStructuralDailyRows(seed, year, reverse);
      for (const hour of Object.keys(expectedRefs)) assert.deepEqual(refs(gospel(seed[date], hour)), expectedRefs[hour]);
      assert.equal(seed[date].length, 65);
      const first = plain(seed);
      addMissingStructuralDailyRows(seed, year, reverse);
      assert.deepEqual(plain(seed), first);
    }
  }
});
