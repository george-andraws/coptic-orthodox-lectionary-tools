const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const text = fs.readFileSync(path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
const api = vm.runInNewContext(text.slice(text.indexOf('function dateToIso('), text.indexOf('async function main()')) + '\n({sortDailyReadings,dailyRowFromReverse,addMissingStructuralDailyRows,readDailyInfo});');
const plain = x => JSON.parse(JSON.stringify(x));
const dates = [[2026, '2026-02-04'], [2027, '2027-02-24'], [2028, '2028-02-09']];
const expected = ['Jonah 3:1-4:11', 'Ps 103:13', 'Ps 103:12', 'Matt 11:25-30', 'Eph 2:1-22', '1Jn 2:12-17', 'Acts 15:12-20', 'Ps 32:1', 'Ps 32:5', 'Matt 15:32-16:4'];
const orderFields = new Set(['reading_order', 'service_order', 'slot_order', 'slot_type', 'source_order', 'source_token_order']);
const multiset = rows => plain(rows).map(r => JSON.stringify(Object.fromEntries(Object.entries(r).filter(([k]) => !orderFields.has(k)).sort(([a], [b]) => a.localeCompare(b))))).sort();
const refs = rows => Array.from(rows, r => r.canonical_mt_ref);
const read = year => JSON.parse(fs.readFileSync(path.join(root, `out/design/daily/lectionary-${year}.json`)));
const psalms = rows => rows.filter(r => r.service_section === 'Matins' && r.slot === 'Psalm');
const mutateTransport = (row, fn) => {
  const sources = JSON.parse(row.source_disclosure);
  for (const s of sources) for (const t of s.consumer_source_transport || []) fn(t, s);
  return {...row, source_disclosure: JSON.stringify(sources)};
};

test('literal source contract establishes father-pities before east/west, not numeric Psalm order', () => {
  const contract = JSON.parse(fs.readFileSync(path.join(root, 'sources/coptic-reader/jonah-qualified-2026-10-25/source-contract.json')));
  const appointment = contract.days.find(d => d.date === '2026-02-04').appointments[1];
  assert.equal(appointment.printed_ref, 'Psalms 102:12, 11');
  assert.equal(appointment.normalized_ref, 'Ps 103:13 & Ps 103:12');
  assert.equal(appointment.order, 2);
});

for (const [year, date] of dates) test(`${date} real design materialization retains source token order and complete metadata`, () => {
  const original = read(year)[date];
  for (const input of [original, original.slice().reverse(), [...original.slice(4), ...original.slice(0, 4)]]) {
    const sorted = api.sortDailyReadings(plain(input), date);
    assert.deepEqual(refs(sorted), expected);
    assert.deepEqual(multiset(sorted), multiset(original), 'complete metadata/row multiset except declared order fields');
    assert.deepEqual(psalms(plain(sorted)).map(r => {
      const transport = JSON.parse(r.source_disclosure)[0].consumer_source_transport.find(t => t.jonah_source.gregorian_date === date);
      return [transport.jonah_source.source_order, transport.token_order];
    }), [[2, 1], [2, 2]], 'positive source ordinals survive in the unchanged disclosure');
    assert.deepEqual(plain(api.sortDailyReadings(plain(sorted).reverse(), date)), plain(sorted), 'JSON replay and shuffled populated path');
    const merged = {[date]: plain(sorted)};
    api.addMissingStructuralDailyRows(merged, year, []);
    assert.deepEqual(plain(merged[date]), plain(sorted), 'Pascha structural merge must not reinterpret Jonah');
  }
});

test('reverse-to-daily transport retains qualified ordinals and structural-only dispatch does not invent Jonah dates', () => {
  const reverse = fs.readFileSync(path.join(root, 'out/design/reverse_lectionary_index.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
  const selected = reverse.filter(r => r.source_family === 'jonah_fast_source_qualified' && r.occasion === "Wednesday of Ninevah's Fast" && r.service_section === 'Matins' && r.slot === 'Psalm');
  assert.equal(selected.length, 2);
  for (const [year, date] of dates) {
    const daily = selected.slice().reverse().map(r => api.dailyRowFromReverse(r, '', date));
    const sorted = api.sortDailyReadings(plain(daily), date);
    assert.deepEqual(refs(sorted), ['Ps 103:13', 'Ps 103:12']);
    assert.deepEqual(Array.from(sorted, r => [r.source_order, r.source_token_order]), [[2, 1], [2, 2]]);
    for (const r of sorted) assert.equal(r.source_disclosure, selected.find(s => s.identity_key === r.identity_key).source_disclosure);
    const structural = {};
    api.addMissingStructuralDailyRows(structural, year, selected);
    assert.equal(structural[date], undefined, 'Jonah is date-resolved design input, not a Pascha structural source');
  }
});

test('actual daily reader writes the corrected sequence only to disposable in-memory output', async () => {
  const bodies = new Map();
  // A bounded real date keeps unrelated R1 SQLite recurrence lookup outside
  // this Jonah test. The actual repair bridge remains enabled, never stubbed.
  const ctx = {path, REPO_ROOT: root, execFileSync: (command, args, options) => {
    assert.equal(command, 'python3');
    const guard = `import sys,runpy,os
 def audit(event,args):
  if event == 'sqlite3.connect': raise RuntimeError('SQLite forbidden in Jonah child')
  if event == 'open' and ((isinstance(args[1],str) and any(c in args[1] for c in 'wax+')) or (isinstance(args[2],int) and args[2] & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))): raise RuntimeError('write forbidden in Jonah child')
 sys.addaudithook(audit)
 runpy.run_path(sys.argv[1],run_name='__main__')`.replace(/^ /gm, '');
    return execFileSync(command, ['-B', '-c', guard, ...args], {...options, timeout: 60000, env: {...process.env, PYTHONDONTWRITEBYTECODE: '1'}});
  }, DESIGN_DIR: 'design', DAILY_DIR: 'daily', readFile: async p => {
    const year = Number(path.basename(p).match(/\d{4}/)[0]);
    const date = dates.find(([y]) => y === year)[1];
    return JSON.stringify({[date]: read(year)[date]});
  }, writeFile: async (p, body) => bodies.set(p, body), stat: async p => ({size: Buffer.byteLength(bodies.get(p))})};
  const reader = vm.runInNewContext(text.slice(text.indexOf('function dateToIso('), text.indexOf('async function main()')) + '\nreadDailyInfo;', ctx);
  for (const [year, date] of dates) {
    await reader(year, [], []);
    assert.deepEqual(refs(JSON.parse(bodies.get(`daily/lectionary-${year}.json`))[date]), expected);
    const rows = JSON.parse(bodies.get(`daily/lectionary-${year}.json`))[date];
    assert.ok(rows.every(r => Object.hasOwn(r, 'display_label')), 'real review hook executed');
  }
});

test('unqualified context, forged source metadata and non-positive/non-integer ordinals do not gain source ordering', () => {
  const source = psalms(read(2026)['2026-02-04']).sort((a, b) => a.canonical_mt_ref.localeCompare(b.canonical_mt_ref));
  assert.deepEqual(refs(source), ['Ps 103:12', 'Ps 103:13']);
  for (const change of [{source_family: 'other'}, {source_kind: 'other'}, {service_section: 'Liturgy'}, {service_hour: 'Matins'}, {occasion: 'Fast of Nineveh'}, {slot: 'Gospel'}, {source_locator: 'forged'}, {source_disclosure: '[]'}, {source_disclosure: '{'}]) {
    const input = source.map(r => ({...r, ...change}));
    assert.deepEqual(refs(api.sortDailyReadings(input, '2026-02-04')), refs(input), JSON.stringify(change));
  }
  for (const date of ['', '2026-02-03', '2026-02-05', '2029-01-31']) assert.deepEqual(refs(api.sortDailyReadings(source, date)), refs(source), date);
  for (const field of ['source_order', 'source_token_order']) for (const value of [true, false, 0, -1, 1.5, '02', '1.0', '', null, 9007199254740992]) {
    const input = source.map(r => ({...r, [field]: value}));
    assert.deepEqual(refs(api.sortDailyReadings(input, '2026-02-04')), refs(input), `${field}=${value}`);
  }
  for (const change of [t => {t.token_order = true;}, t => {t.token_order = 3;}, t => {t.jonah_source.source_order = 9;}, t => {t.jonah_source.gregorian_date = '2026-02-05';}, t => {t.jonah_source.service_section = 'Liturgy';}, t => {t.jonah_source.jonah_contract_sha256 = 'forged';}, t => {t.jonah_source.runtime_activation_approved = 'true';}, t => {t.jonah_source.jonah_source_body_sha256 = 'forged';}, (t, s) => {s.source_kind = 'other';}]) {
    const input = source.map(r => mutateTransport(r, change));
    assert.deepEqual(refs(api.sortDailyReadings(input, '2026-02-04')), refs(input));
  }
});
