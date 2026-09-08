'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const pkg = require('../packages/lectionary-data');

test('calendar is UTC-stable at Coptic new year and leap day', () => {
  for (const tz of ['UTC', 'America/Los_Angeles', 'Pacific/Kiritimati']) {
    const script = `const p=require('./packages/lectionary-data'); console.log(JSON.stringify([p.gregorianToCoptic(2026,9,11),p.gregorianToCoptic(2027,9,11),p.gregorianToCoptic(2027,9,12)]));`;
    const actual = JSON.parse(execFileSync(process.execPath, ['-e', script], { cwd: require('node:path').resolve(__dirname, '..'), env: { ...process.env, TZ: tz } }));
    assert.deepEqual(actual, [
      { year: 1743, monthSlug: 'tout', day: 1 },
      { year: 1743, monthSlug: 'nasie', day: 6 },
      { year: 1744, monthSlug: 'tout', day: 1 },
    ], tz);
  }
});

test('calendar supports years outside shipped readings, early years and century boundaries', () => {
  for (const year of [1, 99, 284, 1900, 2000, 2100, 2400, 9999]) {
    const date = new Date(0);
    date.setUTCFullYear(year, 2, 1);
    date.setUTCHours(12, 0, 0, 0);
    const parts = new Intl.DateTimeFormat('en-u-ca-coptic', { timeZone: 'UTC', year: 'numeric', month: 'numeric', day: 'numeric', era: 'short' }).formatToParts(date);
    const get = type => parts.find(p => p.type === type).value;
    const expectedYear = year < 284 || (year === 284) ? 1 - Number(get('year')) : Number(get('year'));
    assert.equal(pkg.gregorianToCoptic(year, 3, 1).year, expectedYear);
    assert.equal(pkg.gregorianToCoptic(year, 3, 1).day, Number(get('day')));
  }
  for (const args of [[1900,2,29], [2100,2,29], [2026,4,31], [0,1,1], [2026,0,1], [2026,1,1.5]]) {
    assert.throws(() => pkg.gregorianToCoptic(...args));
  }
  assert.doesNotThrow(() => pkg.gregorianToCoptic(2000,2,29));
});

test('public catalog preserves titles, order and immutable day validity', () => {
  const day = pkg.synaxariumForCopticDay('tout', 1);
  assert.equal(day.commemorations.length, 5);
  assert.equal(day.commemorations[0].title, 'Feast of El-Nayrouz (Beginning of the New Coptic Year)');
  assert.equal(day.commemorations[0].id, '2092d164-a560-599e-97be-57c87a600c6f');
  assert.deepEqual(day.commemorations.map(c => c.rank), [1,2,3,4,5]);
  assert.equal(pkg.synaxariumForCopticDay('nasie', 6).validInCommonYear, false);
  assert.equal(pkg.synaxariumForCopticDay('nasie', 6).validInLeapYear, true);
  assert.throws(() => { day.commemorations[0].title = 'changed'; });
  assert.throws(() => pkg.synaxariumForCopticDay('hator', 1));
  assert.throws(() => pkg.synaxariumForCopticDay('tout', 31));
  assert.equal(pkg.synaxariumMeta.day_count, 366);
  assert.equal(pkg.synaxariumMeta.total_commemorations, 868);
});
