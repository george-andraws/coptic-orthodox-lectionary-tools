const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = process.env.CANDIDATE_PACKAGE_DIR || path.resolve(__dirname, '../packages/lectionary-data');
const api = require(root);
const rows = fs.readFileSync(path.join(root, 'data/reverse_lectionary_index.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
const current = rows.filter(api.isCurrentReading);
const daily = JSON.parse(fs.readFileSync(path.join(root, 'data/daily/lectionary-2026.json'), 'utf8'));

test('Coptic Reader Monday Eve Sixth Hour keeps LXX 28 as MT 29, not MT 28', () => {
  const psalms = current.filter(r => r.occasion === 'Monday Eve' && r.service_hour === 'Sixth Hour' && r.slot_type === 'psalm');
  assert.ok(psalms.length > 0);
  for (const row of psalms) {
    assert.equal(row.canonical_mt_ref, 'Ps 29:1-2');
    assert.equal(row.canonical_lxx_ref, 'Ps 28:1-2');
  }
  const emitted = daily['2026-04-06'].filter(r => r.occasion === 'Monday Eve' && r.service_hour === 'Sixth Hour' && r.slot_type === 'psalm');
  assert.ok(emitted.length > 0);
  assert.ok(emitted.every(r => r.display_ref.startsWith('Ps 29:1-2')));
});

test('remaining authoritative Psalm readings retain text-aligned MT coordinates and source order', () => {
  const daily = JSON.parse(fs.readFileSync(api.dailyYearPath(2026), 'utf8'));
  const expectations = [
    ['2026-01-04','Matins', [[96,11,96,13]]],
    ['2026-02-18','Liturgy', [[25,20,25,20],[25,16,25,16]]],
    ['2026-02-19','Liturgy', [[118,14,118,14],[118,18,118,18]]],
    ['2026-03-15','Matins', [[31,24,31,24],[31,23,31,23]]],
    ['2026-03-22','Matins', [[102,1,102,2],[102,12,102,12]]],
    ['2026-07-31','Vespers', [[68,35,68,35],[68,3,68,3]]],
    ['2026-09-13','Liturgy', [[31,23,31,23],[31,19,31,19]]],
  ];
  for (const [date,section,expected] of expectations) {
    const rows = daily[date].filter(r=>api.isCurrentReading(r)&&r.service_section===section&&r.slot_type==='psalm');
    const actual = rows.flatMap(r=>JSON.parse(r.spans_json)).map(s=>[s.chapter_start,s.verse_start,s.chapter_end,s.verse_end]);
    assert.deepEqual(actual,expected,date+' '+section);
  }
});

test('Good Friday Sixth Hour preserves the authoritative composite in text order', () => {
  const daily = JSON.parse(fs.readFileSync(api.dailyYearPath(2026), 'utf8'));
  const rows = daily['2026-04-10'].filter(r=>api.isCurrentReading(r)&&r.service_hour==='Sixth Hour'&&r.slot_type==='psalm');
  const actual = rows.flatMap(r=>JSON.parse(r.spans_json)).map(s=>[s.chapter_start,s.verse_start,s.chapter_end,s.verse_end]);
  assert.deepEqual(actual,[[38,21,38,22],[22,16,22,18],[22,7,22,8]]);
});

test('Jonah Fast has no current Vespers in the three materialized fast days', () => {
  const daily = JSON.parse(fs.readFileSync(api.dailyYearPath(2026), 'utf8'));
  for (const date of ['2026-02-02','2026-02-03','2026-02-04']) {
    assert.ok(daily[date].length>0);
    assert.equal(daily[date].filter(r=>api.isCurrentReading(r)&&r.service_section==='Vespers').length,0,date);
  }
});

test('Coptic Reader source corrections are occasion-specific', () => {
  const cases = [
    ['Abib 7', 'Gospel', 'Mark 9:33-41'],
    ['Amshir 2', 'Gospel', 'Mark 9:33-41'],
    ['Fast of Nineveh', 'Gospel', 'Matt 12:35-45'],
    ['The first Sunday of Tout', 'Pauline Epistle', '1Tim 1:12-19'],
  ];
  for (const [occasion, slot, expected] of cases) {
    assert.ok(current.some(r => r.occasion === occasion && r.slot === slot && r.display_ref === expected), `${occasion}/${slot}: missing ${expected}`);
  }
  assert.equal(current.filter(r => ['Matt 9:33-41', '1Tim 1:12-27', '1Pet 3:25-4:6'].includes(r.display_ref)).length, 0);
  assert.ok(current.some(r => r.display_ref === '1Pet 3:15-4:6'));
});

