const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const api = require('../packages/lectionary-data');
const refs = ['Exod 4:19-6:13', 'Joel 2:21-27', 'Isa 9:9-10:4', 'Job 12:1-14:22'];
for (const [year, date] of [[2026, '2026-03-04'], [2027, '2027-03-24'], [2028, '2028-03-08']]) {
  test(`official Third-Week Wednesday Matins prophecies lead Psalm/Gospel on ${date}`, () => {
    const day = JSON.parse(fs.readFileSync(api.dailyYearPath(year)))[date];
    const matins = day.filter(row => row.service_section === 'Matins');
    assert.deepEqual(matins.slice(0, 4).map(row => row.display_ref), refs);
    assert.deepEqual(matins.slice(0, 4).map(row => row.slot_order), [1, 2, 3, 4]);
    assert.deepEqual(matins.slice(4).map(row => row.slot_type), ['psalm', 'gospel']);
    assert.deepEqual(day.map(row => row.reading_order), Array.from({ length: 11 }, (_, i) => i + 1));
    for (const row of matins.slice(0, 4)) {
      assert.equal(row.slot_type, 'prophecy');
      assert.equal(row.current_status, 'current_confirmed_coptic_reader');
      assert.equal(row.source_family, 'coptic_reader_verified_supplement');
      assert.match(row.source_file, /^sources\/coptic-reader\/lent-week3-wednesday-2026-10-07\//);
      assert.equal(api.isCurrentReading(row), true);
    }
    const exodus = JSON.parse(matins[0].spans_json)[0];
    assert.deepEqual([exodus.book, exodus.chapter_start, exodus.verse_start, exodus.chapter_end, exodus.verse_end], ['Exod', 4, 19, 6, 13]);
    const joel = JSON.parse(matins[1].spans_json)[0];
    assert.equal(joel.verse_end, 27);
    const reverse = fs.readFileSync(api.occasionIndexPath, 'utf8').trim().split('\n').map(JSON.parse)
      .filter(row => row.occasion === 'Wednesday of the third week of Great Lent' && row.slot_type === 'prophecy');
    assert.equal(reverse.length, 4);
    assert.deepEqual(reverse.sort((a,b) => a.slot_order-b.slot_order).map(row => row.display_ref), refs);
  });
}
