const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {createHash} = require('node:crypto');
const {gunzipSync} = require('node:zlib');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
const api = vm.runInNewContext(source.slice(source.indexOf('function dateToIso('), source.indexOf('async function main()')) + '\n({retainCanonicalSupersession,canonicalizeOccurrences});', {createHash});
const plain = x => JSON.parse(JSON.stringify(x));
const hash = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const policyBytes = fs.readFileSync(path.join(root, 'tests/fixtures/canonical-occurrences-policy-1.3.3.json'));
assert.equal(createHash('sha256').update(policyBytes).digest('hex'), 'a3617c001647cfab6aec6e8c917c3254078e6fb06bbf436e01b0c4430e4b864c');
const policy = JSON.parse(policyBytes);
const input = gunzipSync(fs.readFileSync(path.join(root, 'tests/fixtures/canonical-occurrences-input-1.3.2.jsonl.gz'))).toString('utf8').trim().split('\n').map(JSON.parse);
const original = api.canonicalizeOccurrences(input, policy).rows;
assert.equal(hash(original), '9e438d08ede32f5d92cd3724944571910b81ce38e6a60641e04967902e05144a');

// The historical oracle fixes every byte. The new fixture changes precisely one
// explicit retirement epoch, never derives expected versions from VERSION.
const changedPolicy = value => ({...policy, supersessions: policy.supersessions.map((r, i) => i === 0 ? {...r, removal_effective_version: value} : r)});
const row = {identity_key: 'old', source_locator: 'original', provenance: '{"held":true}'};
const preferred = {identity_key: 'new', source_family: 'qualified', source_kind: 'dated', source_locator: 'retained', display_ref: 'source'};

test('omitted retirement epoch remains 1.3.3 with every historical output byte unchanged', () => {
  assert.equal(api.retainCanonicalSupersession(row, preferred, 'context', 'reason').removal_effective_version, '1.3.3');
  assert.equal(hash(api.canonicalizeOccurrences(input, policy).rows), policy.projection_output_sha256);
  assert.equal(hash(api.canonicalizeOccurrences(original, policy).rows), policy.projection_output_sha256);
});

test('explicit 1.3.6 epoch changes only the new retirement version', () => {
  const old = plain(api.retainCanonicalSupersession(row, preferred, 'context', 'reason'));
  assert.deepEqual(plain(api.retainCanonicalSupersession(row, preferred, 'context', 'reason', '1.3.6')), {...old, removal_effective_version: '1.3.6'});
});

test('rule epoch crosses excludeContext into the retired row without changing legacy retirements or sentinels', () => {
  const expected = plain(original);
  const selected = expected.filter(r => r.identity_key === 'rid_08986158a59ce1cfbbda' && r.removal_context_key === 'Tut 1');
  assert.equal(selected.length, 1);
  assert.equal(selected[0].removal_effective_version, '1.3.3');
  selected[0].removal_effective_version = '1.3.6';
  const newPolicy = {...changedPolicy('1.3.6'), projection_output_sha256: hash(expected)};
  const result = api.canonicalizeOccurrences(input, newPolicy).rows;
  assert.equal(hash(result), hash(expected));
  assert.deepEqual(plain(result), expected);
  assert.equal(hash(api.canonicalizeOccurrences(result, newPolicy).rows), hash(expected));
  assert.equal(hash(input), policy.projection_input_sha256, 'inputs are never mutated');
});

test('provided malformed versions fail closed even on idempotent replay', () => {
  for (const value of ['', null, undefined, true, 136, '1.3', 'v1.3.6', '1.3.06', ' 1.3.6', '1.3.6 ', '1.3.6\n', '1.3.6-beta', '1.3.6+build', '1.3.6.0', '9007199254740992.3.6']) {
    assert.throws(() => api.canonicalizeOccurrences(input, changedPolicy(value)), /Invalid canonical removal effective version/, String(value));
    assert.throws(() => api.canonicalizeOccurrences(original, changedPolicy(value)), /Invalid canonical removal effective version/, `replay ${value}`);
    if (value !== undefined) assert.throws(() => api.retainCanonicalSupersession(row, preferred, 'context', 'reason', value), /Invalid canonical removal effective version/);
  }
});
