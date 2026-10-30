const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const packageRoot = process.env.LECTIONARY_PACKAGE_UNDER_TEST || path.resolve(__dirname, '../packages/lectionary-data');
const api = require(packageRoot);
const reverse = fs.readFileSync(api.occasionIndexPath, 'utf8').trim().split('\n').map(JSON.parse);
const daily = Object.fromEntries(api.shippedYears.map(year => [year, JSON.parse(fs.readFileSync(api.dailyYearPath(year), 'utf8'))]));
const current = rows => rows.filter(api.isCurrentReading);
const one = (rows, predicate) => {
  const hits = rows.filter(predicate);
  assert.equal(hits.length, 1, 'exactly one matching appointment');
  return hits[0];
};

test('K1-K3 fixed-date and Sunday metadata are separate and join the catalog', () => {
  const fixed = one(reverse, r => r.identity_key === 'rid_6d8d52b6341b8e102fb7' && r.source_family === 'katameros_cycle' && r.calendar_keys === 'Kiyahk 23');
  assert.equal(fixed.coptic_date_key, 'kiahk-23');
  assert.ok(!fixed.annual_sunday);
  const sundays = reverse.filter(r => r.source_family === 'katameros_cycle' && r.calendar_keys === 'Bashans 3' && r.canonical_mt_ref === 'Lk 10:25-37');
  assert.equal(sundays.length, 1);
  assert.equal(sundays[0].annual_sunday, 'bashans-3');
  assert.ok(!sundays[0].coptic_date_key);
  const catalog = JSON.parse(fs.readFileSync(api.synaxariumPath, 'utf8'));
  for (const row of reverse) {
    if (row.coptic_date_key) assert.ok(Object.hasOwn(catalog, row.coptic_date_key), row.coptic_date_key);
    assert.ok(!(row.coptic_date_key && row.annual_sunday));
  }
});

test('K4-K6 display labels normalize terminology without overwriting retained source labels', () => {
  let checked = 0;
  for (const row of [...reverse, ...Object.values(daily).flatMap(days => Object.values(days).flat())]) {
    assert.equal(typeof row.display_label, 'string');
    assert.doesNotMatch(row.display_label, /Epiphany|Christmas Fast|and the Feast of Entry into Egypt/i);
    checked++;
  }
  assert.ok(checked > 1000);
  assert.ok(reverse.some(r => /Epiphany/.test(r.occasion)), 'original source occasion remains available');
});

test('R2 fixed-day Kiahk23 uses the whole Reader table, never the Sunday table', () => {
  const expected = ['Jn 7:40-53', 'Matt 12:1-8', 'Heb 11:32-40', 'James 5:7-13', 'Acts 2:22-36', 'Matt 22:35-46'];
  for (const date of ['2026-01-01', '2027-01-01']) {
    const rows = daily[date.slice(0, 4)][date];
    assert.equal(rows.length, 9, `${date}: default daily output excludes archived witnesses`);
    assert.ok(rows.every(api.isCurrentReading), `${date}: every daily row is current without filtering`);
    assert.deepEqual(rows.map(r => r.reading_order), [1, 2, 3, 4, 5, 6, 7, 8, 9]);
    assert.deepEqual(rows.map(r => [r.service_section, r.slot]), [
      ['Vespers', 'Psalm'], ['Vespers', 'Gospel'],
      ['Matins', 'Psalm'], ['Matins', 'Gospel'],
      ['Liturgy', 'Pauline Epistle'], ['Liturgy', 'Catholic Epistle'],
      ['Liturgy', 'Acts of the Apostles'], ['Liturgy', 'Psalm'], ['Liturgy', 'Gospel'],
    ]);
    assert.deepEqual(rows.filter(r => r.slot_type !== 'psalm').map(r => r.canonical_mt_ref), expected);
    assert.ok(rows.every(r => r.coptic_date_key === 'kiahk-23'));
    const psalms = rows.filter(r => r.slot_type === 'psalm');
    assert.equal(psalms.length, 3);
    for (const row of psalms) {
      assert.equal(row.current_status, 'pending_psalm_equivalence_unresolved');
      assert.equal(row.canonical_mt_ref, '');
      assert.equal(row.canonical_lxx_ref, '');
      assert.deepEqual(JSON.parse(row.spans_json), [], 'do not infer canonical Psalm coordinates');
    }
  }
  const sunday = current(daily[2028]['2028-01-02']);
  assert.equal(one(sunday, r => r.service_section === 'Matins' && r.slot_type === 'gospel').canonical_mt_ref, 'Mark 3:28-35');
  assert.equal(one(sunday, r => r.service_section === 'Liturgy' && r.slot_type === 'gospel').canonical_mt_ref, 'Lk 1:57-80');
  const old = one(reverse, r => r.identity_key === 'rid_90f9856d0b9722750c38' && r.calendar_keys === 'Kiahk 23');
  assert.equal(api.isCurrentReading(old), false, 'retain old source as inactive evidence');
});

test('R1 Reader Last-Friday Matins wins in every shipped year', () => {
  for (const date of ['2026-04-03', '2027-04-23', '2028-04-07']) {
    const gospel = one(current(daily[date.slice(0, 4)][date]), r => r.service_section === 'Matins' && r.slot_type === 'gospel');
    assert.equal(gospel.canonical_mt_ref, 'Lk 16:19-31');
  }
});

test('H1-H4 and H6 exclude known copies and add authenticated civil-eve appointments', () => {
  for (const [palm, tuesday, friday] of [
    ['2026-04-05', '2026-04-07', '2026-04-10'],
    ['2027-04-25', '2027-04-27', '2027-04-30'],
    ['2028-04-09', '2028-04-11', '2028-04-14'],
  ]) {
    const year = palm.slice(0, 4);
    const eve = current(daily[year][palm]).filter(r => r.pascha_service === 'eve_of_monday');
    assert.ok(eve.some(r => r.canonical_mt_ref === 'Lk 9:18-22'));
    assert.ok(eve.some(r => r.canonical_mt_ref === 'Matt 17:19-23'));
    const tuesdayEve = current(daily[year][tuesday]).filter(r => r.pascha_service === 'eve_of_wednesday');
    assert.ok(tuesdayEve.some(r => r.canonical_mt_ref === 'Matt 22:1-14'));
    assert.ok(!tuesdayEve.some(r => r.canonical_mt_ref === 'Lk 13:23-30'));
    const sixth = current(daily[year][friday]).filter(r => r.service_hour === 'Sixth Hour' && r.slot_type === 'gospel');
    const john = sixth.filter(r => r.canonical_mt_ref.startsWith('Jn '));
    assert.equal(john.length, 1);
    assert.equal(john[0].canonical_mt_ref, 'Jn 19:13-27');
    assert.ok(sixth.some(r => r.canonical_mt_ref.startsWith('Matt ')));
    assert.ok(sixth.some(r => r.canonical_mt_ref.startsWith('Mark ')));
    assert.ok(sixth.some(r => r.canonical_mt_ref.startsWith('Lk ')));
  }
  assert.ok(!current(reverse).some(r => r.source_family === 'holy_pascha_curated_day_hour' && r.identity_key === 'rid_af6bf4bf6c1d0b812cd2'));
});

test('R3 every normalized fixed/Sunday row has occurrence and displacement metadata', () => {
  const rows = reverse.filter(r => r.coptic_date_key || r.annual_sunday);
  assert.ok(rows.length > 1000);
  for (const row of rows) {
    assert.equal(typeof row.occurs_in_shipped_years, 'boolean');
    assert.ok(Array.isArray(row.displaced_by));
  }
});

test('R4 chapter fragments remain one ordered Acts appointment', () => {
  const acts = current(daily[2026]['2026-04-02']).filter(r => r.service_section === 'Liturgy' && r.slot_type === 'praxis');
  assert.equal(acts.length, 1);
  assert.deepEqual(JSON.parse(acts[0].spans_json).map(s => [s.book, s.chapter_start, s.verse_start, s.chapter_end, s.verse_end]), [
    ['Acts', 25, 23, 25, 27], ['Acts', 26, 1, 26, 6],
  ]);
});

test('R6 impossible Daniel1:1-42 survives as evidence, not current numeric Daniel1', () => {
  const bel = current(reverse).filter(r => /Bel 1:1-42/.test(r.display_ref));
  assert.ok(bel.length > 0);
  for (const row of bel) assert.equal(JSON.parse(row.spans_json)[0].book, 'Bel');
  assert.ok(!current(reverse).some(r => r.display_ref === 'Dan 1:1-42'));
});
