const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { createHash } = require('node:crypto');
const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const hash = value => createHash('sha256').update(value).digest('hex');
const accepted = JSON.parse(read('tests/fixtures/canonical-successor-1.3.6-relationships.json'));
const renewal = JSON.parse(read('tests/fixtures/canonical-final-renewal-1.3.6-relationships.json'));
const expected = {...accepted, source_contract: renewal.source_contract, source_contract_sha256: renewal.source_contract_sha256};
const source = fs.readFileSync(process.env.LECTIONARY_BUILDER_UNDER_TEST || path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
const helpers = vm.runInNewContext(source.slice(source.indexOf('function dateToIso('), source.indexOf('async function main()')) + '\n({ normalizeObjectStrings, disambiguateWeekdaySpecificRows, suppressLowerPriorityPassageVariants, sourceSelectorMatches, isCurrentReading, canonicalizeOccurrences })', { createHash });
const rows = helpers.disambiguateWeekdaySpecificRows(read('out/design/reverse_lectionary_index.jsonl').trim().split('\n').map(line => helpers.normalizeObjectStrings(JSON.parse(line)))).rows;
const policy = JSON.parse(read('sources/canonical-occurrence-policy.json'));
const baseline = JSON.parse(read('scripts/package_baselines/removal_effective_versions_1.1.6.json'));
for (const entry of JSON.parse(read('sources/lectionary_corrections.json')).projection_removal_effective_versions || []) {
  const existing = baseline.entries_by_identity_key[entry.identity_key] || [];
  assert.ok(!existing.some(item => item.removal_context_key === entry.removal_context_key));
  baseline.entries_by_identity_key[entry.identity_key] = [...existing, entry];
}
const key = row => [row.occasion, row.service_section, row.service_hour || '', row.slot, row.identity_key];
const same = (left, right) => JSON.stringify(left) === JSON.stringify(right);

test('literal successor relationships are bound to the independently approved source contract', () => {
  assert.equal(hash(read(expected.source_contract)), expected.source_contract_sha256);
  const correction = JSON.parse(read(expected.babah_authority));
  assert.equal(correction.context.corrected_ref, '1Cor 16:12-24');
  for (const [file, fingerprint] of Object.entries(correction.source_fingerprints)) assert.equal(hash(read(file)), fingerprint);
  const preferred = rows.filter(row => helpers.sourceSelectorMatches(row, expected.babah_preferred));
  assert.equal(preferred.length, 1);
  assert.equal(helpers.isCurrentReading(preferred[0]), true);
});

test('successor exact Babah selector names the repaired 12-24 appointment, never the obsolete 12-23 identity', () => {
  const rule = policy.supersessions.find(item => item.calendar_key === 'Babah 3' && item.lower.slot === 'liturgy_pauline');
  assert.ok(rule);
  assert.equal(JSON.stringify(rule.preferred), JSON.stringify(expected.babah_preferred));
  assert.deepEqual(rule.complete_preferred_slot_refs, ['1Cor 16:12-24']);
});

test('inactive Covenant composite witnesses cannot suppress current source-qualified Psalm fragments', () => {
  const selected = rows.filter(row => expected.covenant_current_psalms.some(item => same(key(row), item.slice(0, 5))) || (expected.inactive_covenant_composite_ids.includes(row.identity_key) && /Thursday/.test(row.occasion)));
  assert.equal(selected.length, 6);
  for (const row of selected.filter(row => expected.inactive_covenant_composite_ids.includes(row.identity_key))) {
    assert.equal(row.current_status, 'historical_witness');
    assert.equal(helpers.isCurrentReading(row), false);
  }
  // The production projection and real removal baseline are used unchanged.
  // A new removal-baseline entry would hide the lifecycle defect, not repair it.
  const projected = helpers.suppressLowerPriorityPassageVariants(selected, baseline).rows;
  for (const item of expected.covenant_current_psalms) {
    const matches = projected.filter(row => same(key(row), item.slice(0, 5)));
    assert.equal(matches.length, 1);
    assert.equal(matches[0].canonical_mt_ref, item[5]);
    assert.equal(helpers.isCurrentReading(matches[0]), true);
  }
  for (const before of selected.filter(row => !helpers.isCurrentReading(row))) assert.ok(projected.some(row => same(row, before)));
});

test('inactive lifecycle variants are retained verbatim and never become priority competitors', () => {
  const selected = rows.filter(row => expected.covenant_current_psalms.some(item => same(key(row), item.slice(0, 5))) || (expected.inactive_covenant_composite_ids.includes(row.identity_key) && /Thursday/.test(row.occasion)));
  for (const state of [{current_status: 'historical_witness'}, {current_status: 'historical_candidate_removed'}, {current_status: 'superseded_source'}, {current_status: 'current_public_or_local_reference', active: false}, {current_status: 'current_public_or_local_reference', status: 'removed'}]) {
    const input = selected.map(row => expected.inactive_covenant_composite_ids.includes(row.identity_key) ? {...row, ...state} : row);
    const result = helpers.suppressLowerPriorityPassageVariants(input, baseline);
    assert.equal(result.suppressions.length, 0);
    assert.equal(JSON.stringify(result.rows), JSON.stringify(input));
  }
});

test('current priority competition and unknown-status refusal remain enforced', () => {
  const composite = rows.find(row => expected.inactive_covenant_composite_ids.includes(row.identity_key) && /Thursday/.test(row.occasion));
  const fragments = rows.filter(row => expected.covenant_current_psalms.some(item => same(key(row), item.slice(0, 5))));
  assert.throws(() => helpers.suppressLowerPriorityPassageVariants([...fragments, {...composite, current_status: 'current_public_or_local_reference'}], baseline), /Removal effective-version baseline miss/);
  assert.throws(() => helpers.suppressLowerPriorityPassageVariants([{...composite, current_status: 'invented_status'}], baseline), /Unknown explicit reading status/);
});

test('all reviewed current reverse inputs pass the unmodified pre-canonical production lane', () => {
  const projected = helpers.suppressLowerPriorityPassageVariants(rows, baseline).rows;
  assert.equal(projected.length, rows.length);
});

test('all eight Bright states and five old Covenant witness qualifications remain source-bound before npm projection', () => {
  const qualifications = JSON.parse(read(expected.source_contract)).mandatory_qualifications;
  for (const k of qualifications.bright_legacy_inactive_keys) {
    const matches = rows.filter(row => same(key(row), k));
    assert.equal(matches.length, 1);
    assert.equal(helpers.isCurrentReading(matches[0]), false);
    assert.equal(matches[0].superseded_reason, 'bright_composite_edition_context_hold');
    assert.ok(matches[0].superseded_by_ref);
  }
  for (const k of qualifications.bright_source_only_keys) {
    const matches = rows.filter(row => same(key(row), k));
    assert.equal(matches.length, 1);
    for (const field of ['canonical_mt_ref', 'canonical_lxx_ref']) assert.equal(matches[0][field], '');
    assert.equal(matches[0].spans_json, '[]');
    // Current source text is retained, but pending coordinates are not numeric activation.
    assert.equal(matches[0].current_status, 'pending_psalm_equivalence_unresolved');
    assert.equal(matches[0].source_kind, 'bright_saturday_qualified_composite');
  }
  for (const witness of qualifications.covenant_old_witnesses) {
    const matches = rows.filter(row => same(key(row), witness.key));
    assert.equal(matches.length, 1);
    const disclosure = JSON.parse(matches[0].source_disclosure);
    assert.ok(disclosure.some(item => item.source_family === witness.source_family && item.source_kind === witness.source_kind && (item.source_witnesses || []).some(old => old.current_status === witness.current_status)));
  }
});

// Expected membership is the independently approved literal SOURCE/PLAN ledger,
// not a snapshot of canonicalizeOccurrences output. Preservation assertions below
// compare source cells directly and exercise first projection, not only replay.
const input = helpers.suppressLowerPriorityPassageVariants(rows, baseline).rows;
const contract = JSON.parse(read(expected.source_contract));
const digest = value => hash(JSON.stringify(value));
function assertRelationships(result) {
  assert.equal(result.length, input.length + 20, '20 authenticated preparation origins, no other additions');
  const mutable = new Set(['occasion', 'source_occasion', 'calendar_keys', 'source_calendar_keys', 'day_titles', 'source_day_titles', 'superseded_calendar_keys', 'nonrecurring_source_calendar_keys', 'alternate_source_disclosure', 'active', 'status', 'removed_marker', 'removal_reason', 'removal_context_key', 'removal_effective_version', 'preferred_source_family', 'preferred_source_kind', 'preferred_source_locator', 'preferred_identity_key', 'preferred_display_ref', 'retained_for', 'consumer_note']);
  for (const [i, before] of input.entries()) {
    const after = result[i];
    // Physical source order, coordinates, source envelopes, provenance, public
    // slot labels and all non-projection metadata are invariant at this stage.
    for (const field of Object.keys(before)) if (!mutable.has(field)) assert.equal(JSON.stringify(after[field]), JSON.stringify(before[field]), `${i} ${field}`);
    if (!helpers.isCurrentReading(before)) assert.equal(JSON.stringify(after), JSON.stringify(before), `inactive witness ${i}`);
    // Newly qualified families are outside legacy canonical alias competition.
    if (['bright_saturday_qualified_composite', 'jonah_fast_date_supplement', 'psalmody_source_supplement', 'coptic_reader_qualified_pascha_hour'].includes(before.source_kind)) assert.equal(JSON.stringify(after), JSON.stringify(before), `qualified source ${i}`);
  }
  for (const rule of policy.supersessions) {
    const lowerIndex = input.findIndex(row => helpers.isCurrentReading(row) && helpers.sourceSelectorMatches(row, rule.lower));
    const after = result[lowerIndex];
    assert.ok(!helpers.isCurrentReading(after) || !String(after.calendar_keys).split(' || ').includes(rule.calendar_key), `lower context ${rule.calendar_key}`);
    const preferredIndex = input.findIndex(row => helpers.isCurrentReading(row) && helpers.sourceSelectorMatches(row, rule.preferred));
    assert.equal(helpers.isCurrentReading(result[preferredIndex]), true, `preferred ${rule.calendar_key}`);
  }
  const sentinels = result.slice(input.length);
  assert.equal(sentinels.length, Object.keys(policy.sentinel_sources).length);
  for (const [selector, locator] of Object.entries(policy.sentinel_sources)) {
    const [calendar, slot, ref] = selector.split('|');
    const matches = sentinels.filter(row => row.occasion === policy.sentinel_rules[calendar] && row.slot === slot && row.canonical_mt_ref === ref && row.source_locator === locator);
    assert.equal(matches.length, 1, selector);
    const origin = input.find(row => row.identity_key === matches[0].identity_key && String(row.calendar_keys).split(' || ').includes(calendar));
    assert.ok(origin);
    for (const field of ['canonical_mt_ref', 'canonical_lxx_ref', 'spans_json', 'slot_order', 'source_family', 'source_kind']) assert.equal(matches[0][field], origin[field]);
  }
}

test('whole real pre-canonical input matches literal approved membership and all 1192 exact selectors', () => {
  // The ledger owns literal design-source keys before the production lane's
  // documented Baba/Babah, Kiak/Kiahk and Non-Sunday presentation aliases.
  const raw = read('out/design/reverse_lectionary_index.jsonl').trim().split('\n').map(JSON.parse);
  const actual = raw.map(row => JSON.stringify(key(row))).sort();
  assert.equal(input.length, raw.length);
  assert.equal(new Set(actual).size, actual.length);
  assert.deepEqual(actual, contract.intended_keys.map(k => JSON.stringify(k)).sort());
  assert.equal(policy.supersessions.length, 596);
  assert.equal(digest(policy.supersessions.slice(0, 594)), expected.approved_supersessions_sha256, 'all 594 accepted exact rules remain byte-equivalent');
  assert.deepEqual(policy.supersessions.slice(594), renewal.rules, 'only two literal Abib rules with explicit 1.3.6 epochs');
  assert.equal(policy.projection_lineage.version, '1.3.6');
  assert.equal(policy.projection_lineage.policy_sha256, expected.predecessor.policy_sha256);
  assert.equal(policy.projection_lineage.input_sha256, expected.predecessor.input_sha256);
  assert.equal(policy.projection_lineage.output_sha256, expected.predecessor.output_sha256);
  for (const rule of policy.supersessions) for (const selector of [rule.lower, rule.preferred]) assert.equal(input.filter(row => helpers.isCurrentReading(row) && helpers.sourceSelectorMatches(row, selector)).length, 1);
  for (const [file, fingerprint] of Object.entries(expected.source_authorities)) assert.equal(hash(read(file)), fingerprint, file);
  for (const [file, fingerprint] of Object.entries(policy.source_fingerprints)) assert.equal(hash(fs.readFileSync(path.join(root, file))), fingerprint, file);
});

test('first current projection preserves full source metadata, lifecycle, order and exact source-derived relationships', () => {
  const result = helpers.canonicalizeOccurrences(input, policy);
  assert.equal(result.sentinel_additions, 20);
  assertRelationships(result.rows);
  assert.notEqual(digest(input), digest(result.rows));
  assert.equal(digest(result.rows), policy.projection_output_sha256);
  assert.equal(digest(helpers.canonicalizeOccurrences(result.rows, policy).rows), digest(result.rows));
});

test('source-derived first-projection oracle rejects disabled projection independently of output hash', () => {
  assert.throws(() => assertRelationships(input), /20 authenticated preparation origins/);
});

test('current input guard rejects unrelated reference drift, forged nonapproval and a missing row', () => {
  const unrelated = input.findIndex(row => row.source_family === 'special_service_psalmody');
  assert.ok(unrelated >= 0);
  const covenant = input.findIndex(row => row.source_kind === 'coptic_reader_qualified_pascha_hour');
  assert.ok(covenant >= 0);
  const mutations = [
    input.map((row, i) => i === unrelated ? {...row, canonical_mt_ref: 'Ps 1:1'} : row),
    input.map((row, i) => i === covenant ? {...row, source_disclosure: row.source_disclosure.replace(/false/g, 'true')} : row),
    input.filter((_, i) => i !== unrelated),
  ];
  assert.notEqual(digest(mutations[1]), digest(input), 'forged approval mutation must alter real false fields');
  for (const mutated of mutations) assert.throws(() => helpers.canonicalizeOccurrences(mutated, policy), /Canonical occurrence input fingerprint drift/);
  // Rebinding a checksum is not source approval: the independent metadata
  // relationships must also detect post-projection semantic corruption.
  const valid = helpers.canonicalizeOccurrences(input, policy).rows;
  for (const [index, change] of [[unrelated, {canonical_mt_ref: 'Ps 1:1'}], [covenant, {source_disclosure: mutations[1][covenant].source_disclosure}]]) {
    const mutated = valid.map((row, i) => i === index ? {...row, ...change} : row);
    assert.throws(() => assertRelationships(mutated));
  }
  assert.throws(() => assertRelationships(valid.filter((_, i) => i !== unrelated)));
});
