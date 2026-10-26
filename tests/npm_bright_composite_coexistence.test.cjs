const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');
const root = path.resolve(__dirname, '..');
const text = fs.readFileSync(path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
const api = vm.runInNewContext(text.slice(text.indexOf('function dateToIso('), text.indexOf('async function main()')) + '\n({dailyRowFromReverse,sortDailyReadings,addMissingStructuralDailyRows});');
const plain = x => JSON.parse(JSON.stringify(x));
const kind = 'bright_saturday_qualified_composite';
const ids = ['rid_d58dc513121900158fc9', 'rid_16e3ff8ccefe525d98e0', 'rid_969f73205a3c4d8ceef6', 'rid_5be18395526b0ff8b009'];
const expected = {
  Matins: ['Isa 55:2-13', 'Eph 4:1-5', 'Ps 88:4-5', ids[0], ids[1], 'Matt 27:62-66'],
  '6th Hour': ['Isa 50:10-51:8', 'Ps 130:1', ids[2], 'Matt 5:3-12'],
  '9th Hour': ['Isa 45:15-20', 'Jer 31:31-34', 'Ps 41:5,41:10', 'Jn 5:21-30'],
  Liturgy: ['1Cor 15:1-22', '1Pet 1:1-9', 'Acts 3:12-21', 'Ps 3:3,3:5', ids[3], 'Matt 28:1-20'],
};
const canticles = ['Deut 32:1-42','1Sam 2:1-11','Hab 3:2-19','Jonah 2:2-10','Isa 38:10-20','PrMan 1:1-15','Isa 26:9-20','Isa 25:1-12','Isa 26:1-9','Lam 5:16-22','Bar 2:11-16','1Kgs 18:36-39','1Chr 29:10-13','1Kgs 8:22-30','Dan 9:4-19','Dan 3:1-23','Dan 3:25-51','Dan 3:91-97','Lk 1:46-55','Lk 1:68-79','Lk 2:29-32','Sus 1:1-64'];
const key = r => r.source_kind === kind ? r.identity_key : r.canonical_mt_ref;
const multiset = rows => plain(rows).map(r => JSON.stringify(Object.fromEntries(Object.entries(r).filter(([k]) => k !== 'reading_order').sort(([a],[b]) => a.localeCompare(b))))).sort();
function pipeline(input) {
  const held = input.reverse.filter(r => r.source_kind === kind);
  assert.equal(held.length, 4);
  const historical = input.reverse.filter(r => r.source_kind !== kind);
  assert.equal(historical.length, 4);
  assert(historical.every(r => r.current_status === 'historical_candidate_removed' && r.removed_marker.includes('bright_composite_edition_context_hold')));
  for (const row of held) {
    const daily = api.dailyRowFromReverse(row, 'Bright Saturday');
    assert.equal(daily.source_order, row.source_order, 'reverse transport retains source row');
    assert.equal(daily.source_token_order, row.source_token_order, 'reverse transport retains token');
    assert.equal(daily.service_hour, '', 'held rows retain authenticated empty hour');
    assert.equal(daily.source_disclosure, row.source_disclosure);
    assert.equal(daily.provenance, row.provenance, 'held source provenance survives reverse transport');
    for (const mutation of [{source_family:'other'}, {identity_key:'rid_forged'}, {source_kind:'other'}, {occasion:'Good Friday'}, {service_section:'3rd Hour'}, {service_hour:'Matins'}, {canonical_mt_ref:'Ps 44:23-26'}, {spans_json:'[{"book":"Ps"}]'}, {current_status:'current_public_or_local_reference'}, {source_order:true}, {source_token_order:'02'}, {source_locator:'forged'}, {provenance:'{}'}, {source_disclosure:'[]'}]) {
      assert.equal(api.dailyRowFromReverse({...row,...mutation}, 'Bright Saturday').source_token_order, undefined, JSON.stringify(mutation));
    }
    const disclosure = JSON.parse(row.source_disclosure);
    disclosure[0].bright_composite_source[0].fresh_app_verification = true;
    assert.equal(api.dailyRowFromReverse({...row, source_disclosure:JSON.stringify(disclosure)}, 'Bright Saturday').source_token_order, undefined);
  }
  for (const [year,date] of [[2026,'2026-04-11'],[2027,'2027-05-01'],[2028,'2028-04-15']]) {
    const allReverse = [...input.legacy,...input.reverse,...input.opening];
    const structural = {};
    api.addMissingStructuralDailyRows(structural, year, allReverse.slice().reverse());
    const sorted = {[date]: input.daily[year][date].slice().reverse()};
    api.addMissingStructuralDailyRows(sorted, year, allReverse.slice().reverse());
    for (const all of [structural[date], sorted[date]]) {
      assert.equal(all.filter(r => r.source_kind === kind).length, 4, 'already-populated date does not duplicate four held selections');
      assert(!all.some(r => historical.some(h => h.identity_key === r.identity_key)), 'no current numeric legacy activation');
      for (const [section,refs] of Object.entries(expected)) assert.deepEqual(Array.from(all.filter(r => r.service_section === section),key),refs, `${date} ${section}`);
      const praises = all.filter(r => r.service_section === 'Midnight Praises');
      assert.equal(all[0].canonical_lxx_ref, 'Ps 151');
      assert.deepEqual(Array.from(praises.slice(1),r => r.canonical_mt_ref),canticles);
      assert.deepEqual(Array.from(all.filter(r => r.source_kind === kind),r => r.identity_key),ids);
      for (const r of all.filter(r => r.source_kind === kind)) {
        assert.equal(r.current_status,'pending_psalm_equivalence_unresolved');
        assert.equal(r.canonical_mt_ref,''); assert.equal(r.canonical_lxx_ref,''); assert.equal(r.spans_json,'[]');
        const expectedSource = JSON.parse(held.find(h => h.identity_key === r.identity_key).source_disclosure)[0];
        const actualSources = JSON.parse(r.source_disclosure);
        assert(actualSources.some(s => JSON.stringify(s) === JSON.stringify(expectedSource)), 'complete reverse disclosure survives merge');
        for (const source of actualSources) assert.deepEqual(source.bright_composite_source, expectedSource.bright_composite_source);
      }
      assert.deepEqual(multiset(api.sortDailyReadings(all.slice().reverse(),date)),multiset(all), 'all valid fields preserved except order');
    }
    const before = plain(sorted[date]);
    api.addMissingStructuralDailyRows(sorted,year,allReverse);
    assert.deepEqual(plain(sorted[date]),before,'idempotent populated replay');
    const beforeStructural = plain(structural[date]);
    api.addMissingStructuralDailyRows(structural,year,allReverse);
    assert.deepEqual(plain(structural[date]),beforeStructural,'idempotent structural replay');
  }
}
if (process.argv.includes('--pipeline')) pipeline(JSON.parse(fs.readFileSync(0,'utf8')));
else test('Bright real pipeline is invoked by Python integration', () => assert.equal(typeof api.addMissingStructuralDailyRows,'function'));
