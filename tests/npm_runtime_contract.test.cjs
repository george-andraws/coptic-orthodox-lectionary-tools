'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const packageRoot = process.env.LECTIONARY_PACKAGE_UNDER_TEST || path.resolve(__dirname, '../packages/lectionary-data');
const api = require(packageRoot);
const months = ['tout', 'baba', 'hatour', 'kiahk', 'toba', 'amshir', 'baramhat',
  'baramouda', 'bashans', 'paona', 'abib', 'mesra', 'nasie'];

test('calendar matches the independent ICU oracle through a complete Gregorian century cycle', () => {
  const formatter = new Intl.DateTimeFormat('en-u-ca-coptic', {
    timeZone: 'UTC', year: 'numeric', month: 'numeric', day: 'numeric',
  });
  let count = 0;
  for (const date = new Date('1900-01-01T00:00:00Z'); date.getUTCFullYear() < 2300; date.setUTCDate(date.getUTCDate() + 1)) {
    const parts = Object.fromEntries(formatter.formatToParts(date).map(part => [part.type, part.value]));
    assert.deepEqual(api.gregorianToCoptic(date.getUTCFullYear(), date.getUTCMonth() + 1, date.getUTCDate()), {
      year: Number(parts.year), monthSlug: months[Number(parts.month) - 1], day: Number(parts.day),
    }, date.toISOString().slice(0, 10));
    count++;
  }
  assert.equal(count, 146097);
});

test('calendar rejects invalid component types and out-of-range boundaries with the documented error classes', () => {
  for (const component of [undefined, null, true, '2026', NaN, Infinity, 1.5]) {
    for (const position of [0, 1, 2]) {
      const args = [2026, 1, 1];
      args[position] = component;
      assert.throws(() => api.gregorianToCoptic(...args), TypeError);
    }
  }
  for (const args of [[0, 1, 1], [10000, 1, 1], [2026, 13, 1], [2026, 1, 0], [2026, 1, 32]]) {
    assert.throws(() => api.gregorianToCoptic(...args), RangeError);
  }
});

test('date classification and paths agree with every shipped civil day, including leap day', () => {
  assert.ok(Object.isFrozen(api.shippedYears));
  for (const year of api.shippedYears) {
    const dailyPath = api.dailyYearPath(year);
    assert.equal(dailyPath, path.join(packageRoot, 'data/daily', `lectionary-${year}.json`));
    assert.equal(api.dailyYearPath(String(year)), dailyPath);
    const days = JSON.parse(fs.readFileSync(dailyPath, 'utf8'));
    const expected = [];
    for (const date = new Date(`${year}-01-01T00:00:00Z`); date.getUTCFullYear() === year; date.setUTCDate(date.getUTCDate() + 1)) {
      const iso = date.toISOString().slice(0, 10);
      expected.push(iso);
      assert.deepEqual(api.classifyDate(iso), {
        date: iso, year, shippedYear: true, hasDailyReadings: true,
        classification: 'daily_file_present', dailyPath,
      });
    }
    assert.deepEqual(Object.keys(days).sort(), expected);
  }
  for (const value of [undefined, null, 20260101, new Date(), '2026-1-01', '2026-01-01\n']) {
    assert.throws(() => api.classifyDate(value), TypeError);
  }
  for (const value of ['0000-01-01', '2026-00-01', '2026-01-00', '2026-02-29', '2100-02-29']) {
    assert.throws(() => api.classifyDate(value), RangeError);
  }
  assert.deepEqual(api.classifyDate('2000-02-29'), {
    date: '2000-02-29', year: 2000, shippedYear: false, hasDailyReadings: false,
    classification: 'unshipped_year', dailyPath: null,
  });
  for (const value of [NaN, Infinity, 'not-a-year', 2026.5]) {
    assert.throws(() => api.dailyYearPath(value), TypeError);
  }
  assert.throws(() => api.dailyYearPath(2000), RangeError);
});

test('every public Synaxarium day is deeply frozen and rejects invalid lookups', () => {
  assert.deepEqual(api.frozenMonthSlugs, months);
  assert.ok(Object.isFrozen(api.frozenMonthSlugs));
  assert.ok(Object.isFrozen(api.synaxariumMeta));
  let dayCount = 0;
  let titleCount = 0;
  for (const month of months) {
    for (let day = 1; day <= (month === 'nasie' ? 6 : 30); day++) {
      const value = api.synaxariumForCopticDay(month, day);
      assert.ok(Object.isFrozen(value), `${month}-${day}`);
      assert.ok(Object.isFrozen(value.commemorations));
      for (const record of value.commemorations) assert.ok(Object.isFrozen(record));
      assert.equal(value.validInCommonYear, month !== 'nasie' || day !== 6);
      assert.equal(value.validInLeapYear, true);
      dayCount++;
      titleCount += value.commemorations.length;
    }
  }
  assert.equal(dayCount, 366);
  assert.equal(titleCount, 868);
  for (const month of [undefined, null, '', 'Tout', 'hator', 'epep', '../tout']) {
    assert.throws(() => api.synaxariumForCopticDay(month, 1), RangeError);
  }
  for (const day of [undefined, null, true, '1', 0, -1, 1.5, NaN, Infinity, 31]) {
    assert.throws(() => api.synaxariumForCopticDay('tout', day), RangeError);
  }
  assert.throws(() => api.synaxariumForCopticDay('nasie', 7), RangeError);
});

test('legacy active helpers retain their documented narrower meaning than current readings', () => {
  for (const [row, removed, current] of [
    [{ display_ref: 'Jn 1:1-5' }, false, true],
    [{ active: false }, true, false],
    [{ status: 'removed' }, true, false],
    [{ current_status: 'historical_witness' }, false, false],
    [{ current_status: 'historical_candidate_removed' }, false, false],
    [{ removed_marker: 'removed_by_source' }, false, false],
    [{ current_status: 'pending_psalm_equivalence_unresolved' }, false, true],
  ]) {
    const before = structuredClone(row);
    assert.equal(api.isRemovedReading(row), removed);
    assert.equal(api.isActiveReading(row), !removed);
    assert.equal(api.isCurrentReading(row), current);
    assert.deepEqual(row, before, 'lifecycle predicates must not modify source records');
  }
});
