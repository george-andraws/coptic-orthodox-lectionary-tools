const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {createHash} = require('node:crypto');
const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file));
const json = file => JSON.parse(read(file));
const hash = value => createHash('sha256').update(value).digest('hex');
const digest = value => hash(JSON.stringify(value));
const plain = value => JSON.parse(JSON.stringify(value));
const fixture = json('tests/fixtures/canonical-final-renewal-1.3.6-relationships.json');
const policy = json('sources/canonical-occurrence-policy.json');
const source = fs.readFileSync(process.env.LECTIONARY_BUILDER_UNDER_TEST || path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
const api = vm.runInNewContext(source.slice(source.indexOf('function dateToIso('), source.indexOf('async function main()')) + '\n({normalizeObjectStrings,disambiguateWeekdaySpecificRows,suppressLowerPriorityPassageVariants,sourceSelectorMatches,isCurrentReading,canonicalizeOccurrences});', {createHash});
const raw = read('out/design/reverse_lectionary_index.jsonl').toString().trim().split('\n').map(JSON.parse);
const baseline = json('scripts/package_baselines/removal_effective_versions_1.1.6.json');
for (const entry of json('sources/lectionary_corrections.json').projection_removal_effective_versions || []) baseline.entries_by_identity_key[entry.identity_key] = [...(baseline.entries_by_identity_key[entry.identity_key] || []), entry];
const normalized = api.disambiguateWeekdaySpecificRows(raw.map(api.normalizeObjectStrings)).rows;
const input = plain(api.suppressLowerPriorityPassageVariants(normalized, baseline).rows);
const key = row => JSON.stringify([row.occasion, row.service_section, row.service_hour || '', row.slot, row.identity_key]);
const prior = new Map(fixture.old_relationships.map(item => [JSON.stringify(item.key), item]));
const archive = new Map(fixture.archive.map(row => [key(row), row]));
function independentlyExpected() {
  const result = input.map(row => {
    const accepted = prior.get(key(row));
    if (accepted) {
      assert.equal(digest(row), accepted.source_sha256, 'every predecessor source cell, not only membership');
      return {...row, ...accepted.set};
    }
    assert.deepEqual(row, archive.get(key(row)), 'new row must equal independently source-reconstructed archive');
    return {...row};
  });
  for (const relation of fixture.abib) Object.assign(result[input.findIndex(row => key(row) === JSON.stringify(relation.key))], relation.set);
  const preferred = result[input.findIndex(row => key(row) === JSON.stringify(fixture.preferred.key))];
  // Explicit disclosure preservation precedes the existing display alias stage.
  const occasion = preferred.source_occasion;
  delete preferred.source_occasion;
  preferred.alternate_source_disclosure = fixture.preferred.alternate_source_disclosure;
  preferred.source_occasion = occasion;
  result.push(...plain(fixture.sentinels));
  return result;
}
const expected = independentlyExpected();
const first = api.canonicalizeOccurrences(input, policy);
function assertComplete(rows) { assert.equal(JSON.stringify(rows), JSON.stringify(expected), 'complete row/cell/lifecycle/order/serialization oracle'); }

test('accepted predecessor relationships and source-only archive construct the complete first output and replay', () => {
  assert.equal(input.length, 12186);
  assert.equal(prior.size, 12168);
  assert.equal(archive.size, 18);
  assert.equal(first.sentinel_additions, 20);
  assertComplete(first.rows);
  assertComplete(api.canonicalizeOccurrences(first.rows, policy).rows);
  assert.equal(digest(expected), policy.projection_output_sha256);
  assert.equal(hash(read(fixture.source_contract)), fixture.source_contract_sha256);
  assert.equal(policy.supersessions.length, 596);
  assert.deepEqual(policy.supersessions.slice(594), fixture.rules);
});

test('all 18 immutable histories have zero priority competition and no numeric/current activation', () => {
  const selected = input.filter(row => archive.has(key(row)));
  assert.equal(selected.length, 18);
  assert.equal(api.suppressLowerPriorityPassageVariants(selected, baseline).suppressions.length, 0);
  for (const row of selected) {
    assert.equal(api.isCurrentReading(row), false);
    assert.equal(row.canonical_mt_ref, ''); assert.equal(row.canonical_lxx_ref, ''); assert.equal(row.spans_json, '[]');
    assert.equal(JSON.stringify(first.rows[input.indexOf(row)]), JSON.stringify(row));
  }
  assert.equal(selected.filter(row => row.display_ref === 'Lk 10:38-52').length, 1);
});

test('old retirement epochs and every numeric preparation sentinel are unchanged; only Abib retirements are 1.3.6', () => {
  assert.deepEqual(plain(first.rows.slice(input.length)), fixture.sentinels);
  const retired = first.rows.filter(row => row.removal_effective_version === '1.3.6' && row.removed_marker === 'superseded_by_canonical_occurrence_projection');
  assert.deepEqual(retired.map(row => row.identity_key).sort(), ['rid_02fe8b721c169c9e3435', 'rid_04b5983768df617ca96e']);
  for (const row of first.rows) if (row.removed_marker === 'superseded_by_canonical_occurrence_projection' && !retired.includes(row)) assert.equal(row.removal_effective_version, '1.3.3');
});

test('independent full relationships kill disabled transform, lost disclosures, coordinates, lifecycle and epoch mutations', () => {
  assert.throws(() => assertComplete(input));
  const selected = fixture.abib.map(item => input.findIndex(row => key(row) === JSON.stringify(item.key)));
  for (const i of selected) for (const change of [{active:true}, {removal_effective_version:'1.3.3'}, {removal_context_key:'Abib 3'}, {canonical_mt_ref:'Phil 2:12'}, {canonical_lxx_ref:'Phil 2:1-10'}, {source_disclosure:'[]'}, {slot_order:999}]) {
    const changed = plain(first.rows); Object.assign(changed[i], change); assert.throws(() => assertComplete(changed));
  }
  const preferred = input.findIndex(row => key(row) === JSON.stringify(fixture.preferred.key));
  const changed = plain(first.rows); changed[preferred].alternate_source_disclosure = '[]'; assert.throws(() => assertComplete(changed));
});

test('all three literal Abib selectors reject wrong family/kind/context/coordinates and guarded source drift', () => {
  const selectors = [fixture.rules[0].lower, fixture.rules[1].lower, fixture.rules[0].preferred];
  for (const selector of selectors) {
    const i = input.findIndex(row => api.sourceSelectorMatches(row, selector)); assert.ok(i >= 0);
    for (const field of Object.keys(selector)) {
      const changed = input.map((row, index) => index === i ? {...row, [field]:'wrong-selector-value'} : row);
      assert.equal(api.sourceSelectorMatches(changed[i], selector), false);
      assert.throws(() => api.canonicalizeOccurrences(changed, policy), /Canonical occurrence input fingerprint drift/);
    }
    for (const change of [{active:false}, {current_status:'historical_witness'}, {status:'removed'}, {source_locator:'forged'}, {source_disclosure:'[]'}, {spans_json:'[]'}]) {
      const changed = input.map((row, index) => index === i ? {...row, ...change} : row);
      assert.throws(() => api.canonicalizeOccurrences(changed, policy), /Canonical occurrence input fingerprint drift/);
    }
  }
});


test('archive same-key activation, coordinates, disclosure and order mutants fail independently of rebinding checksums', () => {
  for (const archived of fixture.archive) {
    const i = input.findIndex(row => key(row) === key(archived));
    for (const change of [{current_status:'current_public_or_local_reference', removed_marker:'', active:true}, {canonical_mt_ref:'Lk 10:38-42', spans_json:'[]'}, {source_disclosure:'[]'}, {slot_order:999}]) {
      const changed = plain(first.rows); Object.assign(changed[i], change); assert.throws(() => assertComplete(changed));
    }
  }
});

test('omitting either literal lower decision or backdating a new retirement fails the real final output guard', () => {
  for (const index of [594, 595]) {
    const omitted = {...policy, supersessions:policy.supersessions.filter((_, i) => i !== index)};
    assert.throws(() => api.canonicalizeOccurrences(input, omitted), /Canonical occurrence output fingerprint drift/);
  }
  const backdated = {...policy, supersessions:policy.supersessions.map((rule, i) => i === 594 ? {...rule, removal_effective_version:'1.3.3'} : rule)};
  assert.throws(() => api.canonicalizeOccurrences(input, backdated), /Canonical occurrence output fingerprint drift/);
});
