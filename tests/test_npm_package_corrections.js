'use strict'
const test = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const dir = path.resolve(__dirname, '../packages/lectionary-data')
const api = require(dir)
const daily = JSON.parse(fs.readFileSync(api.dailyYearPath(2026)))
const reverse = fs.readFileSync(api.occasionIndexPath, 'utf8').trim().split('\n').map(JSON.parse)

test('legacy removed/active contract is unchanged; current is explicit', () => {
  assert.equal(api.isActiveReading({current_status:'historical_witness'}), true)
  assert.equal(api.isRemovedReading({active:false}), true)
  assert.equal(api.isActiveReading(null), true) // legacy negation, deliberately unchanged
  for (const row of [null, [], {active:false}, {status:'removed'}, {removed_marker:'source omitted'}, {current_status:'historical_witness'}, {current_status:'historical_candidate_removed'}, {current_status:'superseded_by_composite'}]) assert.equal(api.isCurrentReading(row), false, JSON.stringify(row))
  for (const current_status of ['', 'current_public_or_local_reference', 'current_working_source_not_coptic_reader_checked', 'current_confirmed_coptic_reader', 'current_confirmed_by_fixture_equivalence', 'pending_psalm_equivalence_unresolved']) assert.equal(api.isCurrentReading({current_status}), true, current_status)
  assert.throws(() => api.isCurrentReading({current_status:'invented_state'}), RangeError)
  assert.throws(() => api.isCurrentReading({current_status:'current_invented_state'}), RangeError)
})

test('Gregorian validation rejects impossible dates and preserves unsupported-year behavior', () => {
  for (const d of ['2026-02-29','2026-04-31','2026-13-01','0000-01-01']) assert.throws(()=>api.classifyDate(d), RangeError)
  assert.throws(()=>api.classifyDate('2026-1-01'), TypeError)
  assert.equal(api.classifyDate('2028-02-29').hasDailyReadings, true)
  for (const d of ['0040-01-01','1999-01-01']) assert.equal(api.classifyDate(d).classification, 'unshipped_year')
})

test('all shipped dates contain current rows only, with numeric order and forward-preserved spans', () => {
  for (const year of api.shippedYears) {
    const days = JSON.parse(fs.readFileSync(api.dailyYearPath(year)))
    assert.equal(Object.keys(days).length, year === 2028 ? 366 : 365)
    for (const [date, rows] of Object.entries(days)) {
      assert(rows.length > 0, date)
      rows.forEach((r,i) => {
        assert.equal(api.isCurrentReading(r), true, `${date}: ${r.display_ref}`)
        assert.equal(r.reading_order, i+1)
        assert.equal(typeof r.slot_order, 'number')
        assert.equal(typeof r.service_order, 'number')
        assert.equal(typeof r.spans_json, 'string', `${date}: forward spans ${r.display_ref}`)
      })
    }
  }
})

test('Annunciation collision gives Tuesday/Eve only and retains undated annual reverse evidence', () => {
  const rows = daily['2026-04-07']
  assert(rows.some(r=>r.occasion==='Tuesday'))
  assert(rows.some(r=>r.occasion==='Tuesday Eve'))
  assert(rows.every(r=>!r.occasion.includes('Annunciation')))
  assert(reverse.some(r=>r.occasion.includes('Annunciation')))
})

test('source-specific Monday/Tuesday Eve Gospels remain distinct', () => {
  for (const [date,occasion,reference] of [['2026-04-06','Monday Eve','Mark 10:32-34'],['2026-04-07','Tuesday Eve','Lk 21:34-38']]) {
    const rows = daily[date].filter(r=>r.occasion===occasion&&r.service_hour==='Sixth Hour'&&r.slot_type==='gospel')
    assert.deepEqual(rows.map(r=>r.display_ref), [reference])
  }
  assert(!reverse.some(r=>api.isCurrentReading(r)&&r.display_ref==='Jn 21:34-38'))
})

test('Monday current composite replaces split Genesis fragments', () => {
  const rows = daily['2026-04-06'].filter(r=>r.occasion==='Monday'&&r.service_hour==='First Hour'&&r.slot==='OT1')
  assert.deepEqual(rows.map(r=>r.display_ref), ['Gen 1:1-2:3'])
})

test('Good Friday emits OT1 through OT10 in actual numeric order without sorting the assertion', () => {
  const rows = daily['2026-04-10'].filter(r=>r.occasion==='Good Friday'&&r.service_hour==='First Hour'&&r.slot_type==='prophecy')
  assert.deepEqual(rows.map(r=>r.slot), ['OT1','OT2','OT3','OT4','OT5','OT6','OT7','OT8','OT9','OT10'])
  assert.deepEqual(rows.map(r=>r.slot_order), [1,2,3,4,5,6,7,8,9,10])
  assert(rows.every(r=>typeof r.source_group_key==='string'&&r.source_group_key.length>0))
  assert.deepEqual(rows.map(r=>r.display_ref).slice(-2), ['Mic 1:16-2:3','Mic 7:1-8'])
})

test('calendar overlay preserves the approved current Job composite', () => {
  const rows=daily['2026-04-07'].filter(r=>r.occasion==='Tuesday'&&r.service_hour==='First Hour'&&r.slot==='OT2')
  assert.deepEqual(rows.map(r=>r.display_ref), ['Job 23:2-24:25'])
})

test('blank source orders fall back to the documented ordinary-service order, never zero', () => {
  const rows=daily['2026-01-01']
  assert.deepEqual(rows.filter(r=>r.service_section==='Vespers').map(r=>r.slot), ['Psalm','Gospel'])
  assert.deepEqual(rows.filter(r=>r.service_section==='Liturgy').map(r=>r.slot), ['Pauline Epistle','Catholic Epistle','Acts of the Apostles','Psalm','Gospel'])
  assert(rows.every(r=>r.service_order>0&&r.slot_order>0))
})

test('reverse slot order is typed and retains named non-scripture readings', () => {
  assert(reverse.some(r=>r.slot==='OT10'))
  for (const r of reverse) if(r.slot_order!==null) assert.equal(typeof r.slot_order,'number')
  assert(reverse.some(r=>r.reading_type==='named-reading'&&r.display_ref==='Memoirs of Job'))
})

test('remaining Coptic Reader corrections preserve exact context and Psalm companions', () => {
  const current = reverse.filter(api.isCurrentReading)
  const expected = [
    ['fourth Sunday of Christmas Fast','Catholic Epistle','1Jn 2:24-3:3'],
    ['Wednesday of the fourth week of Great Lent','Pauline Epistle','Eph 4:17-32'],
    ['Mesra 26','Pauline Epistle','Rom 8:14-27'],
    ['Mesra 5','Gospel','Matt 4:23-5:16'],
    ['Kiahk 3','Gospel','Lk 10:38-42'],
    ["Mesra 16 (St Mary's Feast)",'Gospel','Lk 10:38-42'],
    ['Toba 21','Gospel','Lk 10:38-42'],
    ['The first Sunday of Tout','Psalm','Ps 31:23'],
    ['The first Sunday of Tout','Psalm','Ps 31:19'],
    ['Sunday of the fourth week of Great Lent','Psalm','Ps 31:24'],
    ['Sunday of the fourth week of Great Lent','Psalm','Ps 31:23'],
    ['Sunday of the fifth week of Great Lent','Psalm','Ps 102:1-2'],
    ['Sunday of the fifth week of Great Lent','Psalm','Ps 102:12'],
    ['Thursday of the first week of Great Lent','Psalm','Ps 118:14'],
    ['Thursday of the first week of Great Lent','Psalm','Ps 118:18'],
  ]
  for (const [occasion, slot, ref] of expected) {
    assert(current.some(row => row.occasion === occasion && row.slot === slot && row.display_ref.startsWith(ref)), `${occasion}/${slot}/${ref}`)
  }
  const noVespers = reverse.filter(row => row.occasion === 'Fast of Nineveh' && row.service_section === 'Vespers' && row.display_ref === 'Lk 10:38-52')
  assert(noVespers.length > 0)
  assert(noVespers.every(row => !api.isCurrentReading(row) && row.removed_marker === 'removed_by_coptic_reader_no_service'))
})
