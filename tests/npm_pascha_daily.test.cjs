const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const api = require('../packages/lectionary-data');
const reverse = fs.readFileSync(api.occasionIndexPath, 'utf8').trim().split('\n').map(JSON.parse);

// Execute the real helpers without invoking main or regenerating package files.
function helpers() {
  const source = fs.readFileSync(process.env.LECTIONARY_BUILDER_UNDER_TEST || path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
  const start = source.indexOf('function dateToIso(');
  const end = source.indexOf('async function main()');
  assert.ok(start > 0 && end > start);
  return vm.runInNewContext(source.slice(start, end) + '\n({ rowsForPaschaDailyDate, addMissingStructuralDailyRows, dailyRowFromReverse, dedupeDailyRows });');
}

const readerWednesday = reverse.filter(row => row.source_family === 'coptic_reader'
  && row.occasion === 'Wednesday of Holy Pascha' && api.isCurrentReading(row));

function key(row) {
  return [row.occasion, row.service_hour, row.slot, row.identity_key, row.display_ref].join('|');
}

test('Pascha Wednesday admits every current Reader fixture row without restoring inactive history', () => {
  const { rowsForPaschaDailyDate } = helpers();
  assert.equal(readerWednesday.length, 21, 'preserved current fixture projection');
  const selected = rowsForPaschaDailyDate(reverse, 'Wednesday');
  for (const expected of readerWednesday) assert.ok(selected.some(row => key(row) === key(expected)), expected.source_locator);
  assert.ok(selected.every(api.isCurrentReading));
  assert.ok(selected.every(row => ['Wednesday', 'Wednesday Eve', 'Wednesday of Holy Pascha'].includes(row.occasion)));
  for (const day of ['Monday', 'Tuesday', 'Great Thursday', 'Good Friday', 'Bright Saturday']) {
    assert.equal(rowsForPaschaDailyDate(readerWednesday, day).length, 0, day);
  }
  const invalid = [
    ...readerWednesday.map(row => ({ ...row, active: false })),
    ...readerWednesday.map(row => ({ ...row, current_status: 'historical_witness' })),
    ...readerWednesday.map(row => ({ ...row, source_family: 'unverified_reader' })),
    ...readerWednesday.map(row => ({ ...row, source_kind: 'ordinary_date' })),
    ...readerWednesday.map(row => ({ ...row, occasion: 'Wednesday of Great Lent' })),
  ];
  assert.equal(rowsForPaschaDailyDate(invalid, 'Wednesday').length, 0);
});

test('partial structural daily inputs are completed and repeat materialization is idempotent', () => {
  const { rowsForPaschaDailyDate, addMissingStructuralDailyRows, dailyRowFromReverse } = helpers();
  const selected = rowsForPaschaDailyDate(reverse, 'Wednesday');
  const existing = dailyRowFromReverse(selected[0], 'Wednesday');
  existing.reading_order = 999;
  const daily = { '2026-04-08': [existing] };
  addMissingStructuralDailyRows(daily, 2026, reverse);
  assert.equal(daily['2026-04-08'].length, 39);
  assert.equal(new Set(daily['2026-04-08'].map(key)).size, 39);
  assert.deepEqual(Array.from(daily['2026-04-08'], row => row.reading_order), Array.from({ length: 39 }, (_, index) => index + 1));
  const before = JSON.stringify(daily);
  addMissingStructuralDailyRows(daily, 2026, reverse);
  assert.equal(JSON.stringify(daily), before);
});

test('Annunciation collision replaces rather than merges the ordinary feast rows', () => {
  const { addMissingStructuralDailyRows } = helpers();
  const daily = { '2026-04-07': [{ occasion: 'The Annunciation Feast', display_ref: 'synthetic collision anchor' }] };
  addMissingStructuralDailyRows(daily, 2026, reverse);
  const rows = daily['2026-04-07'];
  assert.equal(rows.length, 38);
  assert.ok(rows.every(row => ['Tuesday', 'Tuesday Eve'].includes(row.occasion)));
  assert.ok(rows.every(row => /Annunciation yields/.test(row.correction_reason)));
  const before = JSON.stringify(daily);
  addMissingStructuralDailyRows(daily, 2026, reverse);
  assert.equal(JSON.stringify(daily), before);
});

test('Wednesday alias dedupe prefers Reader regardless of input order and never merges Eve', () => {
  const { dailyRowFromReverse, dedupeDailyRows } = helpers();
  const reader = dailyRowFromReverse(readerWednesday.find(row => row.display_ref === 'Prov 1:11-35'), 'Wednesday');
  const rawReverse = fs.readFileSync(path.join(root, 'out/design/reverse_lectionary_index.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
  const curated = dailyRowFromReverse(rawReverse.find(row => row.occasion === 'Wednesday' && row.display_ref === 'Prov 1:11-35'), 'Wednesday');
  const eve = { ...reader, occasion: 'Wednesday Eve' };
  for (const input of [[curated, reader, eve], [reader, curated, eve]]) {
    const rows = dedupeDailyRows(input);
    assert.equal(rows.length, 2);
    assert.equal(rows[0].source_family, 'coptic_reader');
    assert.equal(rows[0].source_disclosure, reader.source_disclosure);
    assert.equal(rows[1].occasion, 'Wednesday Eve');
  }
  assert.equal(dedupeDailyRows([reader, { ...reader, service_hour: 'First Hour', service_section: 'First Hour' }]).length, 2);
});

for (const [year, date] of [[2026, '2026-04-05'], [2027, '2027-04-25'], [2028, '2028-04-09']]) {
  test(`Hosanna ${date} appends only current Pascha hours to the ordinary Palm Sunday services`, () => {
    const rows = JSON.parse(fs.readFileSync(api.dailyYearPath(year), 'utf8'))[date];
    const structural = rows.filter(row => row.structural_day === 'Hosanna Sunday');
    assert.equal(structural.length, 5);
    assert.deepEqual(new Set(structural.map(row => row.identity_key)), new Set([
      'rid_d9f544171faf5b8bf1b4', 'rid_febdbadd9aea980d2dbb',
      'rid_f334b150887bd2f1bff5', 'rid_3f05adb088ea4fb9b1e9',
      'rid_6f2b1cdfaffff2641d58',
    ]));
    assert.equal(rows.filter(row => !row.structural_day).length, 16, 'ordinary Palm services retained');
    assert.ok(rows.every(api.isCurrentReading));
    assert.equal(rows.length, 21);
    const lamentations = structural.find(row => row.identity_key === 'rid_6f2b1cdfaffff2641d58');
    assert.equal(lamentations.service_hour, 'Ninth Hour');
    assert.equal(lamentations.display_ref, 'Lam 1:1-4');
    assert.equal(lamentations.current_status, 'current_confirmed_coptic_reader');
  });
}

for (const [year, date] of [[2026, '2026-04-08'], [2027, '2027-04-28'], [2028, '2028-04-12']]) {
  test(`packaged ${date} preserves Reader readings and all five daytime hour categories`, () => {
    const rows = JSON.parse(fs.readFileSync(api.dailyYearPath(year), 'utf8'))[date];
    const daytime = rows.filter(row => !row.occasion.endsWith(' Eve'));
    for (const expected of readerWednesday) {
      const actual = daytime.find(row => key(row) === key(expected));
      assert.ok(actual, expected.source_locator);
      for (const field of ['source_family', 'source_kind', 'source_locator', 'source_disclosure', 'spans_json', 'current_status', 'canonical_mt_ref', 'canonical_lxx_ref']) {
        assert.equal(actual[field], expected[field], `${date}: ${field}`);
      }
    }
    for (const hour of ['First Hour', 'Third Hour', 'Sixth Hour', 'Ninth Hour', 'Eleventh Hour']) {
      for (const type of ['prophecy', 'psalm', 'gospel']) {
        assert.ok(daytime.some(row => row.service_hour === hour && row.slot_type === type), `${date}: ${hour} ${type}`);
      }
    }
    const job = daytime.find(row => row.display_ref === 'Memoirs of Job');
    assert.ok(job, 'named Sixth Hour reading retained');
    assert.equal(job.reading_name, 'Memoirs of Job');
    assert.equal(job.reading_type, 'named-reading');
    assert.deepEqual(JSON.parse(job.spans_json), [], 'do not invent Job verse coordinates');
    assert.ok(rows.some(row => row.occasion === 'Wednesday Eve'), 'eve readings retained');
    const proverbs = daytime.filter(row => row.service_hour === 'Ninth Hour' && row.display_ref === 'Prov 1:11-35');
    assert.equal(proverbs.length, 1, 'Wednesday aliases must not duplicate the same appointment');
    assert.equal(proverbs[0].source_family, 'coptic_reader', 'retain the current Reader representative');
    assert.ok(rows.every(api.isCurrentReading));
    assert.equal(new Set(rows.map(key)).size, rows.length, 'no exact duplicated occurrences');
    assert.deepEqual(rows.map(row => row.reading_order), rows.map((_, index) => index + 1));
  });
}

test('Bright Saturday liturgy aliases collapse to one explicit slot and keep both disclosures', () => {
  const { dedupeDailyRows } = helpers();
  const disclosure = (label) => JSON.stringify([{ source: label }]);
  const pair = (shortSlot, explicitSlot, displayRef, identity) => ([
    {
      occasion: 'Bright Saturday',
      service_section: 'Liturgy',
      service_hour: 'Liturgy',
      slot: shortSlot,
      identity_key: identity,
      display_ref: displayRef,
      current_status: 'current_working_source_not_coptic_reader_checked',
      source_disclosure: disclosure('pascha'),
    },
    {
      occasion: 'Bright Saturday',
      service_section: 'Liturgy',
      service_hour: 'Liturgy',
      slot: explicitSlot,
      identity_key: identity,
      display_ref: displayRef,
      current_status: 'current_public_or_local_reference',
      source_disclosure: disclosure('service-order'),
    },
  ]);
  const rows = dedupeDailyRows([
    ...pair('Pauline', 'Pauline Epistle', '1Cor 15:1-22', 'pauline'),
    ...pair('Catholic', 'Catholic Epistle', '1Pet 1:1-9', 'catholic').reverse(),
    ...pair('Acts', 'Praxis', 'Acts 3:12-21', 'praxis'),
    {
      occasion: 'Bright Saturday',
      service_section: 'Liturgy',
      service_hour: 'Liturgy',
      slot: 'Gospel',
      identity_key: 'gospel',
      display_ref: 'Matt 28:1-20',
      current_status: 'current_working_source_not_coptic_reader_checked',
      source_disclosure: disclosure('pascha-gospel'),
    },
    {
      occasion: 'Bright Saturday',
      service_section: 'Liturgy',
      service_hour: 'Liturgy',
      slot: 'Gospel',
      identity_key: 'gospel',
      display_ref: 'Matt 28:1-20',
      current_status: 'current_public_or_local_reference',
      source_disclosure: disclosure('service-order-gospel'),
    },
    {
      occasion: 'Bright Saturday',
      service_section: 'Matins',
      service_hour: 'Matins',
      slot: 'Pauline Epistle',
      identity_key: 'matins-pauline',
      display_ref: 'Eph 4:1-5',
      current_status: 'current_public_or_local_reference',
      source_disclosure: disclosure('matins'),
    },
  ]);
  assert.equal(JSON.stringify(rows.map(row => [row.slot, row.display_ref, row.service_hour])), JSON.stringify([
    ['Pauline Epistle', '1Cor 15:1-22', 'Liturgy'],
    ['Catholic Epistle', '1Pet 1:1-9', 'Liturgy'],
    ['Praxis', 'Acts 3:12-21', 'Liturgy'],
    ['Gospel', 'Matt 28:1-20', 'Liturgy'],
    ['Pauline Epistle', 'Eph 4:1-5', 'Matins'],
  ]));
  for (const row of rows.filter(item => item.service_hour === 'Liturgy')) {
    assert.equal(row.current_status, 'current_public_or_local_reference');
    assert.equal(JSON.parse(row.source_disclosure).length, 2);
  }
});
