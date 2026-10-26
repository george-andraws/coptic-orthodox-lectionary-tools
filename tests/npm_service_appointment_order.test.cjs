const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const text = fs.readFileSync(path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
const { sortDailyReadings } = vm.runInNewContext(text.slice(text.indexOf('function dateToIso('), text.indexOf('async function main()')) + '\n({sortDailyReadings});');
const daily = Object.fromEntries([2026, 2027, 2028].map(y => [y, JSON.parse(fs.readFileSync(path.join(root, `packages/lectionary-data/data/daily/lectionary-${y}.json`)))]));
const role = row => /^Prophecy(?:\b|$)/i.test(row.slot || '') ? 'prophecy' : row.slot_type;
const stages = { prophecy: 0, pauline: 1, catholicon: 2, praxis: 3, psalm: 4, gospel: 5 };
const comparable = row => ['ordinary_date_resolved', 'katameros_cycle', 'coptic_reader_verified_supplement',
  'holy_pascha_curated_day_hour', 'coptic_reader', 'coptic_reader_qualified_pascha_hour', 'bright_saturday', 'jonah_fast_source_qualified'].includes(row.source_family)
  && row.service_section !== 'Midnight Praises';

test('new Jonah supplement family preserves prophecy, Psalm and Gospel service stages', () => {
  // Declared integration contract fixture, not a claim about the still-old package.
  const rows = ['psalm', 'gospel', 'prophecy'].map(type => ({
    occasion: 'Fast of Nineveh', service_section: 'Matins', service_hour: '',
    slot: type === 'prophecy' ? 'OT1' : type, slot_type: type, slot_order: 1,
    source_family: 'jonah_fast_source_qualified', source_kind: 'jonah_fast_date_supplement',
  }));
  assert.deepEqual(Array.from(sortDailyReadings(rows, '2026-02-02'), r => r.slot_type),
    ['prophecy', 'psalm', 'gospel']);
});

test('complete shipped service groups retain prophecy, epistle, Psalm and Gospel stage order', () => {
  const failures = [];
  for (const year of [2026, 2027, 2028]) for (const [date, original] of Object.entries(daily[year])) {
    const sorted = sortDailyReadings(original, date);
    assert.equal(sorted.length, original.length, date);
    const fullRow = row => JSON.stringify(Object.fromEntries(Object.entries(row)
      .filter(([key]) => key !== 'reading_order').sort(([a], [b]) => a.localeCompare(b))));
    assert.deepEqual(Array.from(sorted, fullRow).sort(), original.map(fullRow).sort(), date);
    assert.deepEqual(Array.from(sorted, r => r.reading_order), original.map((_, i) => i + 1));
    assert.deepEqual(JSON.parse(JSON.stringify(sortDailyReadings(sorted, date))), JSON.parse(JSON.stringify(sorted)), date);
    const groups = new Map();
    for (const row of sorted.filter(comparable)) {
      const key = [row.occasion, row.service_section, row.service_hour || ''].join('|');
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(row);
    }
    for (const [key, rows] of groups) {
      let previous = -1;
      for (const row of rows) {
        const stage = stages[role(row)];
        if (stage === undefined) continue;
        if (stage < previous) { failures.push(`${date}|${key}|${row.display_ref}`); break; }
        previous = stage;
      }
    }
  }
  assert.deepEqual(failures, []);
});

test('Palm Sunday four source Gospels retain Matthew, Mark, Luke and John order', () => {
  for (const [year, date] of [[2026, '2026-04-05'], [2027, '2027-04-25'], [2028, '2028-04-09']]) {
    const rows = sortDailyReadings(daily[year][date], date).filter(r => r.occasion === 'Palm Sunday' && r.service_section === 'Liturgy' && r.slot_type === 'gospel');
    assert.deepEqual(Array.from(rows, r => r.canonical_mt_ref), ['Matt 21:1-17', 'Mark 11:1-11', 'Lk 19:29-48', 'Jn 12:12-19']);
  }
});

const palmGospels = daily[2026]['2026-04-05'].filter(r => r.occasion === 'Palm Sunday' && r.service_section === 'Liturgy' && r.slot_type === 'gospel');
const refs = rows => Array.from(rows, r => r.canonical_mt_ref);

test('Palm sequence is confined to the complete current source appointment on trusted dates', () => {
  for (const mutation of [{ source_kind: 'other' }, { source_family: 'other' },
    { occasion: 'Palm Sunday Eve' }, { service_section: 'Matins' }, { service_hour: 'First Hour' }]) {
    const input = palmGospels.map(r => ({ ...r, ...mutation }));
    assert.deepEqual(refs(sortDailyReadings(input, '2026-04-05')), refs(input), JSON.stringify(mutation));
  }
  for (const date of ['', '2026-04-04', '2026-04-06', '2029-04-01']) {
    assert.deepEqual(refs(sortDailyReadings(palmGospels, date)), refs(palmGospels), date);
  }
  for (const mutation of [{ active: false }, { current_status: 'historical_witness' }, { removed_marker: 'superseded by repair' }]) {
    const input = palmGospels.map((r, i) => i === 3 ? { ...r, ...mutation } : r);
    assert.deepEqual(refs(sortDailyReadings(input, '2026-04-05')), refs(input.slice(0, 3)));
  }
  assert.deepEqual(refs(sortDailyReadings(palmGospels.slice(0, 3), '2026-04-05')), refs(palmGospels.slice(0, 3)));
});

test('adjacent numeric prophecies retain OT2 before OT10, fragments and separate Eve/day groups', () => {
  const base = daily[2026]['2026-04-06'][0];
  const input = ['Monday', 'Monday Eve'].flatMap(occasion => [
    { slot: 'Gospel', slot_type: 'gospel', slot_order: 1 },
    { slot: 'OT10', slot_type: 'prophecy', slot_order: 10 },
    { slot: 'Psalm', slot_type: 'psalm', slot_order: 1 },
    { slot: 'OT2', slot_type: 'prophecy', slot_order: 2 },
    { slot: 'OT2', slot_type: 'prophecy', slot_order: 2, display_ref: 'second supplied fragment' },
  ].map(r => ({ ...base, ...r, occasion })));
  const sorted = sortDailyReadings(input, '2026-04-06');
  for (const occasion of ['Monday', 'Monday Eve']) {
    const rows = sorted.filter(r => r.occasion === occasion);
    assert.deepEqual(Array.from(rows, r => r.slot), ['OT2', 'OT2', 'OT10', 'Psalm', 'Gospel']);
    assert.equal(rows[1].display_ref, 'second supplied fragment');
    const positions = Array.from(sorted, (r, i) => r.occasion === occasion ? i : -1).filter(i => i >= 0);
    assert.equal(positions.at(-1) - positions[0], rows.length - 1);
  }
});

test('Bright physical row order does not leak into other sources, occasions or dates', () => {
  // Immutable published witness, deliberately descending physical source order.
  // Equal fallback slot order makes the unqualified dispatch retain this exact
  // shuffle, rather than accidentally agreeing with the canonical source order.
  const legacy = JSON.parse(fs.readFileSync(path.join(root, 'tests/fixtures/bright-published-1.3.5.json')));
  const ordinal = r => Number(/:row (\d+);/.exec(r.source_locator)[1]);
  const praises = legacy.rows.filter(r => r.service_section === 'Midnight Praises')
    .map(r => ({ ...r, occasion: 'Bright Saturday', service_hour: 'Midnight Praises', slot_order: 99 }))
    .sort((a, b) => ordinal(b) - ordinal(a));
  assert.equal(praises.length, 22);
  const canonical = [...praises].sort((a, b) => ordinal(a) - ordinal(b));
  const baseline = input => refs(sortDailyReadings(input, '2026-04-10'));
  assert.deepEqual(baseline(praises), refs(praises), 'wrong-date dispatch must retain the deliberate shuffle');
  assert.notDeepEqual(refs(praises), refs(canonical), 'fixture must distinguish physical dispatch');
  for (const mutation of [{ source_kind: 'other' }, { source_family: 'other' },
    { occasion: 'Bright Saturday Eve' }, { service_section: 'Other Service', service_hour: 'Other Service' },
    { source_locator: 'other.csv:row 1; source_ref=untrusted' }]) {
    const input = praises.map(r => ({ ...r, ...mutation }));
    assert.deepEqual(refs(sortDailyReadings(input, '2026-04-11')), baseline(input));
  }
  assert.deepEqual(refs(sortDailyReadings(praises, '2026-04-11')), refs(canonical), 'qualified dispatch uses source ordinals');
  assert.deepEqual(refs(sortDailyReadings(praises, '2026-04-11')).sort(), refs(praises).sort(), 'no canticle loss');
});

test('Bright Saturday praises precede Matins and retain the printed canticle sequence', () => {
  for (const [year, date] of [[2026, '2026-04-11'], [2027, '2027-05-01'], [2028, '2028-04-15']]) {
    const sorted = sortDailyReadings(daily[year][date], date);
    const praises = sorted.filter(r => r.service_section === 'Midnight Praises');
    assert.equal(sorted[0].service_section, 'Midnight Praises');
    // The old package has these canticles; a qualified Psalm 151 opening is
    // independent and must not weaken this complete retained sequence.
    const existing = praises.filter(r => r.source_kind === 'bright_saturday_service_order');
    assert.deepEqual(Array.from(existing, r => r.canonical_mt_ref), [
      'Deut 32:1-42', '1Sam 2:1-11', 'Hab 3:2-19', 'Jonah 2:2-10', 'Isa 38:10-20', 'PrMan 1:1-15',
      'Isa 26:9-20', 'Isa 25:1-12', 'Isa 26:1-9', 'Lam 5:16-22', 'Bar 2:11-16', '1Kgs 18:36-39',
      '1Chr 29:10-13', '1Kgs 8:22-30', 'Dan 9:4-19', 'Dan 3:1-23', 'Dan 3:25-51', 'Dan 3:91-97',
      'Lk 1:46-55', 'Lk 1:68-79', 'Lk 2:29-32', 'Sus 1:1-64',
    ]);
  }
});
