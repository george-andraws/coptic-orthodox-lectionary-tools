const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');
const root = path.resolve(__dirname, '..');
const text = fs.readFileSync(path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
const api = vm.runInNewContext(text.slice(text.indexOf('function dateToIso('), text.indexOf('async function main()')) + '\n({addMissingStructuralDailyRows,sortDailyReadings,dedupeDailyRows});');
const plain = x => JSON.parse(JSON.stringify(x));
const waters = 'Liturgy of Blessing of the Water';
const expected = {
  Liturgy: ['1Cor 11:23-34', 'Ps 23:5', 'Ps 41:9', 'Matt 26:20-29'],
  [waters]: ['Gen 18:1-23', 'Prov 9:1-11', '', '', 'Isa 4:2-4', 'Isa 55:1-56:1', 'Ezek 36:25-29', 'Ezek 47:1-9', '1Tim 4:9-5:10', 'Ps 51:7', 'Ps 51:10', 'Jn 13:1-17'],
};
function pipeline(input) {
  for (const [year, date] of [[2026, '2026-04-09'], [2027, '2027-04-29'], [2028, '2028-04-13']]) {
    // Presentation serialization may sort identity/reference keys; source
    // fragment ordinals, not incidental array order, control the appointment.
    const sorted = { [date]: input.daily[year][date].slice().reverse() };
    api.addMissingStructuralDailyRows(sorted, year, [...input.legacy, ...input.reverse]);
    const all = sorted[date];
    const services = all.filter(r => ['Liturgy', waters].includes(r.service_section) && ['the Covenant Thursday', 'Great Thursday'].includes(r.occasion));
    assert.equal(services.length, 16);
    assert.equal(new Set(services.map(r => [r.service_section, r.slot, r.source_group_key].join('|'))).size, 14);
    for (const [section, refs] of Object.entries(expected)) {
      assert.deepEqual(Array.from(services.filter(r => r.service_section === section), r => r.canonical_mt_ref), refs);
    }
    assert.equal(services.filter(r => r.canonical_mt_ref === 'Gen 18:1-23').length, 1);
    assert(services.every(r => r.source_kind === 'coptic_reader_qualified_pascha_hour'));
    for (const row of services.filter(r => ['1Cor 11:23-34', 'Matt 26:20-29', 'Gen 18:1-23', '1Tim 4:9-5:10', 'Jn 13:1-17'].includes(r.canonical_mt_ref))) {
      assert(JSON.parse(row.source_disclosure).some(d => d.source_witnesses?.some(w => w.current_status.startsWith('historical') || w.current_status === 'current_working_source_not_coptic_reader_checked')), 'retained old source lifecycle must survive daily merge');
    }
    assert(all.some(r => r.service_hour === 'First Hour'), 'unrelated existing hours survive');
    const before = JSON.stringify(plain(all));
    api.addMissingStructuralDailyRows(sorted, year, [...input.legacy, ...input.reverse]);
    assert.equal(JSON.stringify(plain(sorted[date])), before, 'structural replay is idempotent');
    const structuralOnly = {};
    api.addMissingStructuralDailyRows(structuralOnly, year, [...input.legacy, ...input.reverse]);
    for (const [section, refs] of Object.entries(expected)) {
      assert.deepEqual(Array.from(structuralOnly[date].filter(r => r.service_section === section && ['the Covenant Thursday', 'Great Thursday'].includes(r.occasion)), r => r.canonical_mt_ref), refs);
    }
    const stripOrder = r => Object.fromEntries(Object.entries(r).filter(([k]) => k !== 'reading_order'));
    const multiset = rows => rows.map(r => JSON.stringify(stripOrder(r))).sort();
    assert.deepEqual(multiset(plain(api.sortDailyReadings(all.slice().reverse(), date))), multiset(plain(all)));
  }
}
if (process.argv.includes('--pipeline')) {
  pipeline(JSON.parse(fs.readFileSync(0, 'utf8')));
} else {
  test('whole-service pipeline is exercised by Python raw CSV/design integration', () => {
    assert.equal(typeof api.addMissingStructuralDailyRows, 'function');
  });
  test('different occasions, hours and services are not broadly collapsed', () => {
    const base = {occasion: 'Great Thursday', service_section: waters, service_hour: waters, slot: 'OT1', identity_key: 'same', display_ref: 'Gen 18:1-23'};
    for (const change of [{occasion: 'Great Thursday Eve'}, {service_hour: 'First Hour'}, {service_section: 'Matins'}]) {
      assert.equal(api.dedupeDailyRows([base, {...base, ...change}]).length, 2);
    }
  });
}
