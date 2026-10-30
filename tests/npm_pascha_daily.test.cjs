const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const api = require(process.env.LECTIONARY_PACKAGE_UNDER_TEST || '../packages/lectionary-data');
const reverse = fs.readFileSync(api.occasionIndexPath, 'utf8').trim().split('\n').map(JSON.parse);
const holyFamily = 'coptic_reader_qualified_holy_week_review';
function authenticated(file, expected) {
  const bytes = fs.readFileSync(path.join(root, file));
  assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), expected, file);
  return JSON.parse(bytes);
}
const predecessor = authenticated('tests/fixtures/holy_week_review_1_3_6.json', '8aa845a557e06b3b58a900335a8d5b695727ea934b76065bb2cf6d822762fc02');
const designReverseBytes = fs.readFileSync(path.join(root, 'out/design/reverse_lectionary_index.jsonl'));
assert.equal(crypto.createHash('sha256').update(designReverseBytes).digest('hex'), '3473d858301159573118dd8df25522a95c412e19a8a78bc22a3d483a6f7dd0fc');
// The retained Holy Week fixture contains the two Pascha families only;
// add its unchanged 21-row Wednesday Reader companion from pinned design.
// These five design Psalm witnesses were already removed by source priority
// in 1.3.6 (not new H-review holds). Pin the complete retained tuple set too.
const priorRemoved = new Set(['rid_7727752ced614b97f28b', 'rid_2085cfd33c7ff758f1c4', 'rid_636b325ce818d089c903', 'rid_4af80e7a6f8ba1d41eb7', 'rid_a957214de809fb6c875f']);
const historicalReader = designReverseBytes.toString().trim().split('\n').map(JSON.parse).filter(r => r.source_family === 'coptic_reader' && r.occasion === 'Wednesday of Holy Pascha' && !priorRemoved.has(r.identity_key));
assert.equal(crypto.createHash('sha256').update(JSON.stringify(historicalReader.map(key).sort())).digest('hex'), '0219edc198869803ea59d578c262f4992566b43dc3f1dc1c1b216b43fca6daf3');
const historicalReverse = [...predecessor.reverse_rows, ...historicalReader];
function historicalStructural(date) {
  const days = {};
  helpers().addMissingStructuralDailyRows(days, 2026, historicalReverse);
  const rows = Array.from(days[date]);
  // Complete ordered helper outputs from the 1.3.6 builder + reverse pair at
  // commit 2d38471. A sorter mutation cannot silently refresh this oracle.
  const pins = {'2026-04-07': 'afc2e40f9adeb8c3a867732751a9a807732eee11094068437366e846b9e3d284', '2026-04-08': '9f56c5c0fc9270fe340c7c8127890fe5cae41776525ec43406a35af0b93d1b40'};
  assert.equal(crypto.createHash('sha256').update(JSON.stringify(rows.map(key))).digest('hex'), pins[date], `${date}: complete historical helper order`);
  return rows;
}
function expectedPrefinal(date) {
  const old = historicalStructural(date);
  return old.filter(r => date === '2026-04-07'
    ? r.occasion !== 'Tuesday Eve' // H1: all 15 copied appointments held.
    : r.identity_key !== 'rid_af6bf4bf6c1d0b812cd2'); // H6: Jer -> Ezek source correction is FINAL-stage.
}

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
  assert.equal(historicalStructural('2026-04-08').length, 39, 'authenticated predecessor, before H6 hold');
  const expected = expectedPrefinal('2026-04-08');
  assert.equal(expected.length, 38);
  assert.deepEqual(Array.from(daily['2026-04-08'], key), expected.map(key), 'complete prefinal membership AND order');
  assert.equal(new Set(daily['2026-04-08'].map(key)).size, expected.length);
  assert.deepEqual(Array.from(daily['2026-04-08'], row => row.reading_order), expected.map((_, index) => index + 1));
  const before = JSON.stringify(daily);
  addMissingStructuralDailyRows(daily, 2026, reverse);
  assert.equal(JSON.stringify(daily), before);
});

test('Annunciation collision replaces rather than merges the ordinary feast rows', () => {
  const { addMissingStructuralDailyRows } = helpers();
  const daily = { '2026-04-07': [{ occasion: 'The Annunciation Feast', display_ref: 'synthetic collision anchor' }] };
  addMissingStructuralDailyRows(daily, 2026, reverse);
  const rows = daily['2026-04-07'];
  assert.equal(historicalStructural('2026-04-07').length, 38, 'authenticated predecessor before the 15 copied Eve appointments were held');
  const expected = expectedPrefinal('2026-04-07');
  assert.equal(expected.length, 23);
  assert.deepEqual(Array.from(rows, key), expected.map(key), 'prefinal helper excludes held copies; final repair supplies qualified Eve rows');
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
    const old = predecessor.daily[String(year)][date];
    const ordinary = row => row.source_family === 'ordinary_date_resolved';
    assert.equal(rows.filter(ordinary).length, 16, 'exact ordinary Palm services retained');
    assert.deepEqual(rows.filter(ordinary).map(key), old.filter(ordinary).map(key));
    assert.deepEqual(structural.map(key), old.filter(r => r.structural_day === 'Hosanna Sunday').map(key));
    const additions = rows.filter(r => r.source_family === holyFamily);
    assert.deepEqual(additions.map(r => [r.pascha_service, r.service_hour, r.slot_type, r.canonical_mt_ref]), [
      ['eve_of_monday', 'Third Hour', 'prophecy', 'Zeph 1:14-2:2'],
      ['eve_of_monday', 'Third Hour', 'gospel', 'Lk 9:18-22'],
      ['eve_of_monday', 'Eleventh Hour', 'prophecy', 'Mic 3:1-4'],
      ['eve_of_monday', 'Eleventh Hour', 'gospel', 'Matt 17:19-23'],
    ]);
    const manifest = authenticated('sources/coptic-reader/holy-week-review-qualified-2026-10-29/source-manifest.json', '16737be9590c5df2020e494b4950b1142347887f71a9b91f28b5601d66adf257');
    for (const row of additions) {
      const evidence = JSON.parse(row.holy_week_review_evidence);
      const document = manifest.documents[evidence.document_key];
      const bytes = fs.readFileSync(path.join(root, 'sources/coptic-reader/holy-week-review-qualified-2026-10-29', document.file));
      assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), document.sha256);
      const reading = document.readings.find(r => r.heading_line === evidence.heading_line);
      assert.equal(reading.canonical_mt_ref, row.canonical_mt_ref);
      assert.equal(bytes.toString().split(/\r?\n/)[evidence.heading_line - 1], reading.heading_exact);
      assert.equal(row.pascha_civil_date, date);
    }
    assert.ok(rows.every(api.isCurrentReading));
    assert.equal(rows.length, 25, '16 unchanged ordinary + 5 unchanged structural + 4 authenticated Eve');
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

test('final Holy Week membership and new Reader order match the authenticated source projection, all shipped years', () => {
  const script = `import sys,json,os
def audit(event,args):
    if event == 'sqlite3.connect': raise RuntimeError('SQLite forbidden in source projection')
    if event == 'open' and ((isinstance(args[1],str) and any(c in args[1] for c in 'wax+')) or (isinstance(args[2],int) and args[2] & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))): raise RuntimeError('write forbidden in source projection')
sys.addaudithook(audit)
import holy_week_review_repairs as review
fixture=json.load(sys.stdin)
reverse=review.repair_reverse_rows(fixture['reverse_rows'])
out={year:review.repair_daily_year(int(year),days,reverse) for year,days in fixture['daily'].items()}
json.dump(out,sys.stdout)
`;
  const run = payload => JSON.parse(execFileSync('python3', ['-B', '-c', script], {
    cwd: root, input: JSON.stringify(payload), encoding: 'utf8', maxBuffer: 32 * 1024 * 1024,
    timeout: 60000,
    env: {...process.env, PYTHONDONTWRITEBYTECODE: '1'},
  }));
  const projected = run(predecessor);
  // This is the complete FINAL membership/coordinate oracle, not an ordering
  // oracle made from old final arrays. Structural helper order is asserted
  // above against its own predecessor, while new Reader order is asserted
  // below against the authenticated source projection.
  const project = rows => rows.map(r => [key(r), r.canonical_mt_ref, r.canonical_lxx_ref,
    r.spans_json, r.current_status,
    r.source_family === holyFamily ? r.holy_week_review_evidence : '']).sort((a, b) => a[0].localeCompare(b[0]));
  let dates = 0;
  for (const [year, days] of Object.entries(projected)) {
    const shipped = JSON.parse(fs.readFileSync(api.dailyYearPath(Number(year)), 'utf8'));
    for (const [date, expected] of Object.entries(days)) {
      assert.deepEqual(project(shipped[date]), project(expected), `${date}: complete final source projection, no omitted rows`);
      assert.deepEqual(shipped[date].filter(r => r.source_family === holyFamily).map(key), expected.filter(r => r.source_family === holyFamily).map(key), `${date}: full new Reader source order`);
      assert.ok(shipped[date].every(api.isCurrentReading));
      assert.deepEqual(shipped[date].map(r => r.reading_order), expected.map((_, i) => i + 1));
      dates++;
    }
  }
  assert.equal(dates, 18, 'complete Palm-through-Friday fixtures in all three years');
});

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
