const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const api = require(process.env.LECTIONARY_PACKAGE_UNDER_TEST || path.resolve(__dirname, '../packages/lectionary-data'));
const reverse = fs.readFileSync(api.occasionIndexPath, 'utf8').trim().split('\n').map(JSON.parse);
const days = Object.fromEntries(api.shippedYears.map(y => [y, JSON.parse(fs.readFileSync(api.dailyYearPath(y), 'utf8'))]));
const badTuesday = new Set(['Jn 11:12-24', 'Mark 11:11-19', 'Matt 21:23-27', 'Jn 8:51-59', 'Isa 5:20-30', 'Jer 9:12-19']);

test('L1 malformed Mesra source is held, never silently corrected from a different witness', () => {
  for (const date of ['2026-08-13', '2027-08-13']) {
    assert.ok(!days[date.slice(0, 4)][date].some(r => r.display_ref === 'Mark 14:39'));
  }
  const held = reverse.find(r => r.identity_key === 'rid_24a3269b0d1a1fb0412d' && r.occasion === 'Mesra 7');
  assert.equal(held.current_status, 'pending_coptic_reader_review');
  assert.equal(api.isCurrentReading(held), false);
  assert.equal(held.display_ref, 'Mark 14:39');
  assert.match(held.source_locator, /source_ref=Mark 14:39$/);
});

test('L2 copied Tuesday day-hour appointments are archived and absent in every year', () => {
  for (const date of ['2026-04-07', '2027-04-27', '2028-04-11']) {
    const rows = days[date.slice(0, 4)][date];
    assert.ok(!rows.some(r => r.pascha_service === 'tuesday' && badTuesday.has(r.canonical_mt_ref)));
    assert.ok(rows.some(r => r.pascha_service === 'tuesday' && r.canonical_mt_ref === 'Jn 8:12-20'), 'unreported Sixth Hour is not silently retired');
    assert.ok(rows.some(r => r.pascha_service === 'eve_of_wednesday' && r.canonical_mt_ref === 'Matt 22:1-14'));
  }
  const held = reverse.filter(r => r.source_family === 'holy_pascha_curated_day_hour' && r.occasion === 'Tuesday' && badTuesday.has(r.canonical_mt_ref));
  assert.equal(held.length, 6);
  assert.ok(held.every(r => r.current_status === 'pending_coptic_reader_review' && !api.isCurrentReading(r)));
});

test('L3 printed Third and Ninth Hours are explicit inactive candidates, never a fabricated Eleventh Hour', () => {
  const rows = reverse.filter(r => r.source_family === 'holy_pascha' && r.occasion === 'Wednesday Eve' && ['Matt 24:36-51', 'Amos 5:18-27', 'Matt 23:29-36', 'Hos 9:14-10:2'].includes(r.canonical_mt_ref));
  assert.equal(rows.length, 8, 'four historical sources plus four explicit candidates');
  const candidates = rows.filter(r => r.current_status === 'pending_coptic_reader_review');
  assert.equal(candidates.length, 4);
  assert.ok(candidates.every(r => r.active === false && !api.isCurrentReading(r)));
  assert.equal(rows.filter(r => r.current_status === 'historical_witness').length, 4);
  assert.deepEqual(candidates.filter(r => r.slot === 'Gospel').map(r => [r.service_hour, r.canonical_mt_ref]).sort(), [['Ninth Hour', 'Matt 23:29-36'], ['Third Hour', 'Matt 24:36-51']]);
});

test('L4-L5 display labels are normalized without changing raw source titles', () => {
  const rows = [...reverse, ...Object.values(days).flatMap(d => Object.values(d).flat())];
  for (const r of rows) {
    assert.doesNotMatch(r.display_label, /Kiyank|Ninevah/);
    if (r.pascha_service === 'eve_of_tuesday') assert.equal(r.display_label, 'Eve of Tuesday');
    if (r.pascha_service === 'eve_of_friday') assert.equal(r.display_label, 'Eve of Good Friday');
    if (['Hosanna Sunday', 'Palm Sunday'].includes(r.occasion)) assert.equal(r.display_label, 'Palm Sunday');
    if (r.occasion === 'Bright Saturday') assert.equal(r.display_label, 'Bright Saturday');
  }
  assert.ok(reverse.some(r => /Kiyank/.test(r.day_titles)));
});

test('L6 preserves both Hator 11 Vespers witnesses with an explicit conflict', () => {
  const rows = reverse.filter(r => r.coptic_date_key === 'hatour-11' && /vespers/i.test(r.service_section) && /gospel/i.test(r.slot));
  assert.equal(rows.length, 2);
  assert.deepEqual(rows.map(r => r.canonical_mt_ref).sort(), ['Mark 14:3-9', 'Matt 10:24-33']);
  assert.ok(rows.every(r => r.evidence_status === 'conflicting_vespers_sources' && r.mark_followup_note.startsWith('L6:')));
});

test('L7 retains all six undated appointments with service-book evidence qualification', () => {
  const rows = reverse.filter(r => r.evidence_status === 'unverified_service_book' && r.mark_followup_note?.startsWith('L7:'));
  assert.equal(rows.length, 6);
  assert.ok(rows.every(r => r.source_kind === 'special_service'));
  assert.ok(rows.some(r => r.source_family === 'myron_consecration' && r.canonical_mt_ref === 'Mark 16:1-20'));
});

test('L9 legacy unresolved Pascha Psalms stay archived, accepted source-only Psalms remain current', () => {
  for (const year of api.shippedYears) {
    const rows = Object.values(days[year]).flat();
    assert.ok(!rows.some(r => r.source_family === 'holy_pascha_curated_day_hour' && r.current_status === 'pending_psalm_equivalence_unresolved'));
    assert.ok(rows.some(r => r.source_family === 'bright_saturday' && r.current_status === 'pending_psalm_equivalence_unresolved'));
    assert.ok(rows.every(api.isCurrentReading));
    for (const rr of Object.values(days[year])) assert.deepEqual(rr.map(r => r.reading_order), rr.map((_, i) => i + 1));
  }
  const held = reverse.filter(r => r.source_family === 'holy_pascha_curated_day_hour' && r.current_status === 'pending_psalm_equivalence_unresolved' && !r.removed_marker);
  assert.equal(held.length, 3);
  assert.ok(held.every(r => r.active === false && !api.isCurrentReading(r)));
});
