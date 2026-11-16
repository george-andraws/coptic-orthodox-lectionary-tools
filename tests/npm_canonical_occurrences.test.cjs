const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { gunzipSync } = require('node:zlib');
const { createHash } = require('node:crypto');
const root = path.resolve(__dirname, '..');
const api = require('../packages/lectionary-data');
const source = fs.readFileSync(process.env.LECTIONARY_BUILDER_UNDER_TEST || path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
// Frozen 1.3.2 -> 1.3.3 regression oracle, copied byte-for-byte from
// b5602df6bcca68b9f5fafb05597dbcc31280a409. Current release policy/data have
// separate review gates; never refresh these fingerprints from builder output.
const policyBytes = fs.readFileSync(path.join(root, 'tests/fixtures/canonical-occurrences-policy-1.3.3.json'));
assert.equal(createHash('sha256').update(policyBytes).digest('hex'), 'a3617c001647cfab6aec6e8c917c3254078e6fb06bbf436e01b0c4430e4b864c', 'Historical canonical policy bytes must retain their reviewed lineage');
const policy = JSON.parse(policyBytes);
assert.equal(policy.projection_input_sha256, '693afa1d6cfa0484a03e202148e896adea33f84d1e38d448466f4333bddb26d9');
assert.equal(policy.projection_output_sha256, '9e438d08ede32f5d92cd3724944571910b81ce38e6a60641e04967902e05144a');
const helpers = vm.runInNewContext(source.slice(source.indexOf('function dateToIso('), source.indexOf('async function main()')) + '\n({ project: typeof canonicalizeOccurrences === "function" ? canonicalizeOccurrences : rows => ({ rows }), normalizeContextText, isCurrentReading, retainCanonicalSupersession });', { createHash });
const bytes = fs.readFileSync(path.join(root, 'tests/fixtures/canonical-occurrences-input-1.3.2.jsonl.gz'));
assert.equal(createHash('sha256').update(bytes).digest('hex'), '1b9dce4a4d9fbb623f19adac7ff72443fb7fe129da6830304d2a51542c9f2587');
const before = gunzipSync(bytes).toString('utf8').trim().split('\n').map(JSON.parse);
const first = helpers.project(before, policy);
const rows = first.rows;
const current = input => input.filter(api.isCurrentReading);
const find = (ref, occasion) => current(rows).filter(r => r.canonical_mt_ref === ref && (!occasion || r.occasion === occasion));
const hash = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');

test('first projection from authenticated 1.3.2 inputs reproduces the independently reviewed complete output', () => {
  assert.equal(first.sentinel_additions, 20);
  assert(first.dispositions.length > 0);
  assert.equal(hash(rows), policy.projection_output_sha256);
  assert.equal(hash(rows), '9e438d08ede32f5d92cd3724944571910b81ce38e6a60641e04967902e05144a');
});

test('canonical output replay is a separate idempotent operation', () => {
  assert.equal(hash(helpers.project(rows, policy).rows), hash(rows));
});

test('Wednesday Ninth Hour has one source-confirmed Psalm and one Proverbs appointment', () => {
  assert.equal(find('Ps 41:5-6', 'Wednesday').length, 0);
  assert.equal(find('Ps 41:5-7', 'Wednesday of Holy Pascha').length, 1);
  assert.equal(find('Prov 1:11-35', 'Wednesday').length, 0);
  assert.equal(find('Prov 1:11-35', 'Wednesday of Holy Pascha').length, 1);
});

test('Amshir Sunday and fixed Baunah aliases have a single canonical current representative', () => {
  assert.equal(find('Heb 3:1-4:2').filter(r => /(?:Amshir|Meshir)/.test(r.occasion)).length, 1);
  for (const ref of ['Heb 3:1-19', 'Heb 4:1-2']) assert.equal(find(ref).filter(r => r.calendar_keys.includes('Amshir 3')).length, 0);
  assert.equal(find('Lk 1:57-80').filter(r => /(?:Paona|Baunah) 30/.test(r.occasion)).length, 1);
});

test('same Lent prophecy source slots exclude old Numbers splits and duplicate Proverbs', () => {
  for (const ref of ['Num 10:35-36', 'Num 11:1-35']) assert.equal(find(ref).filter(r => r.calendar_keys.includes('week 5 day_of_week 2')).length, 0);
  assert.equal(find('Prov 1:20-33').filter(r => r.calendar_keys.includes('week 3 day_of_week 1')).length, 0);
  assert.equal(find('Num 10:35-11:35', 'Tuesday of the fifth week of Great Lent').length, 1);
});

test('every authentic preparation sentinel is named, with ordinary contexts retained', () => {
  assert.equal(current(rows).filter(r => /week (?:99|49)\b/.test(r.calendar_keys)).length, 0);
  assert.equal(find('Ps 95:1-2', 'Preparation Saturday').length, 1);
  assert.ok(find('Lk 13:1-5').some(r => r.calendar_keys.includes('week 6 day_of_week 1') || r.occasion === 'Monday of the sixth week of Great Lent'));
});

test('Mesra 7 duplicates collapse without erasing distinct services or inactive evidence', () => {
  assert.equal(find('Acts 7:2-7', 'Mesra 7').length, 1);
  const outputBytes = new Set(rows.map(r => JSON.stringify(r)));
  assert.ok(before.some(r => !api.isCurrentReading(r)), 'Retained inactive source metadata control must not be vacuous');
  for (const r of before.filter(r => !api.isCurrentReading(r))) assert.ok(outputBytes.has(JSON.stringify(r)), r.source_locator);
  assert.ok(current(rows).some(r => r.occasion === 'Wednesday Eve'));
  assert.ok(current(rows).some(r => r.occasion === 'Mesra 7' && r.service_section === 'Matins'));
});

test('policy selector misses, ambiguous selectors and omitted decisions cannot silently pass', () => {
  for (const preferred of [{identity_key:'missing'}, {source_family:'ordinary_date_resolved'}]) {
    const changed = {...policy, supersessions: [{...policy.supersessions[0], preferred}, ...policy.supersessions.slice(1)]};
    assert.throws(() => helpers.project(before, changed), /selector must identify one authenticated current row/);
  }
  assert.throws(() => helpers.project(before, {...policy, supersessions: []}), /Canonical occurrence output fingerprint drift/);
});

test('forged preferred source metadata, missing selectors and moved contexts fail closed before suppression', () => {
  const preferred = before.findIndex(r => r.canonical_mt_ref === 'Num 10:35-11:35' && r.occasion === 'Tuesday of the fifth week of Great Lent' && api.isCurrentReading(r));
  assert(preferred >= 0);
  for (const change of [{source_locator:'forged'}, {source_disclosure:'[]'}, {spans_json:'[]'}, {slot_order:999}, {occasion:'Wednesday Eve'}, {source_kind:'wrong_kind'}, {active:false}]) {
    const input = before.map((r, i) => i === preferred ? {...r, ...change} : r);
    assert.throws(() => helpers.project(input, policy), /Canonical occurrence input fingerprint drift/, JSON.stringify(change));
  }
  assert.throws(() => helpers.project(before.filter((_, i) => i !== preferred), policy), /Canonical occurrence input fingerprint drift/);
  assert.throws(() => helpers.project([...before, {...before[preferred], slot_order:999}], policy), /Canonical occurrence input fingerprint drift/);
});

test('current package isCurrentReading remains compatible with historical and packaged lifecycle rows', () => {
  // Compatibility is about the public lifecycle predicate, NOT equality between
  // the historical full-output oracle and intentionally evolved current data.
  const packaged = fs.readFileSync(api.occasionIndexPath, 'utf8').trim().split('\n').map(JSON.parse);
  assert.ok(packaged.length > 0);
  for (const [label, input] of [['historical input', before], ['historical output', rows], ['current package', packaged]]) {
    assert.deepEqual(input.map(api.isCurrentReading), input.map(helpers.isCurrentReading), label);
  }
  const controls = [
    [null, false], [[], false], [{}, true],
    [{current_status:'current_confirmed_coptic_reader'}, true],
    [{current_status:'current_public_or_local_reference', active:false}, false],
    [{current_status:'current_public_or_local_reference', status:'removed'}, false],
    [{current_status:'current_public_or_local_reference', removed_marker:'superseded by source-qualified appointment'}, false],
    [{current_status:'historical_candidate_removed'}, false],
    [{current_status:'historical_witness'}, false],
  ];
  for (const predicate of [api.isCurrentReading, helpers.isCurrentReading]) {
    for (const [row, expected] of controls) assert.equal(predicate(row), expected, JSON.stringify(row));
    assert.throws(() => predicate({current_status:'unknown_explicit_status'}), /Unknown explicit reading status/);
  }
});

const plain = value => JSON.parse(JSON.stringify(value));

// The historical oracle fixes every byte. The new fixture changes precisely one
// explicit retirement epoch, never derives expected versions from VERSION.
const changedPolicy = value => ({...policy, supersessions: policy.supersessions.map((r, i) => i === 0 ? {...r, removal_effective_version: value} : r)});
const row = {identity_key: 'old', source_locator: 'original', provenance: '{"held":true}'};
const preferred = {identity_key: 'new', source_family: 'qualified', source_kind: 'dated', source_locator: 'retained', display_ref: 'source'};

test('omitted retirement epoch remains 1.3.3 with every historical output byte unchanged', () => {
  assert.equal(helpers.retainCanonicalSupersession(row, preferred, 'context', 'reason').removal_effective_version, '1.3.3');
  assert.equal(hash(rows), policy.projection_output_sha256);
  assert.equal(hash(helpers.project(rows, policy).rows), policy.projection_output_sha256);
});

test('explicit 1.3.6 epoch changes only the new retirement version', () => {
  const old = plain(helpers.retainCanonicalSupersession(row, preferred, 'context', 'reason'));
  assert.deepEqual(plain(helpers.retainCanonicalSupersession(row, preferred, 'context', 'reason', '1.3.6')), {...old, removal_effective_version: '1.3.6'});
});

test('rule epoch crosses excludeContext into the retired row without changing legacy retirements or sentinels', () => {
  const expected = plain(rows);
  const selected = expected.filter(r => r.identity_key === 'rid_08986158a59ce1cfbbda' && r.removal_context_key === 'Tut 1');
  assert.equal(selected.length, 1);
  assert.equal(selected[0].removal_effective_version, '1.3.3');
  selected[0].removal_effective_version = '1.3.6';
  const newPolicy = {...changedPolicy('1.3.6'), projection_output_sha256: hash(expected)};
  const result = helpers.project(before, newPolicy).rows;
  assert.equal(hash(result), hash(expected));
  assert.deepEqual(plain(result), expected);
  assert.equal(hash(helpers.project(result, newPolicy).rows), hash(expected));
  assert.equal(hash(before), policy.projection_input_sha256, 'inputs are never mutated');
});

test('provided malformed versions fail closed even on idempotent replay', () => {
  for (const value of ['', null, undefined, true, 136, '1.3', 'v1.3.6', '1.3.06', ' 1.3.6', '1.3.6 ', '1.3.6\n', '1.3.6-beta', '1.3.6+build', '1.3.6.0', '9007199254740992.3.6']) {
    assert.throws(() => helpers.project(before, changedPolicy(value)), /Invalid canonical removal effective version/, String(value));
    assert.throws(() => helpers.project(rows, changedPolicy(value)), /Invalid canonical removal effective version/, `replay ${value}`);
    if (value !== undefined) assert.throws(() => helpers.retainCanonicalSupersession(row, preferred, 'context', 'reason', value), /Invalid canonical removal effective version/);
  }
});
