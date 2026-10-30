const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const packageRoot = process.env.LECTIONARY_PACKAGE_UNDER_TEST || path.join(root, 'packages/lectionary-data');
const digest = body => crypto.createHash('sha256').update(body).digest('hex');
const identity = ref => `rid_${digest(`scripture|${ref}|${ref}`).slice(0, 20)}`;
const tuple = r => [r.identity_key, r.display_ref, r.source_group_key.replace(/\bKiak\b/g, 'Kiahk').replace(/\bBaba\b/g, 'Babah')];
// Authenticated pre-review design / published 1.3.6 ordinary projection pairs.
// The output pins were extracted from commit 2d38471, NOT the new candidate.
const historical = {
  2026: ['ab89d0e2d53272c7b0f6d867b1469ab53d7b9f29c54a897e4f146db0072ddc3b', '332cbfe8af768a34af51ed4e785f640ea6073990392863eb6d62f5aa27fe76ac'],
  2027: ['9d5d389fef7f79cb92829e83d49b68244f33836edecc513b2d336751cbca4d76', '8f74b81e1bbe306be8587a457400fc3dff2da9bdea152dc4cf1afcfcef2fa959'],
  2028: ['7859565dbd8c2d51f56e24a10c1861f7a617473333de00f3f2127da43b322420', 'f7013f5339a7799d4ef7bd0411e38843f140c4cf89f895e55ec779d813f6e55a'],
};
function authenticated(file, hash) {
  const body = fs.readFileSync(path.join(root, file));
  assert.equal(digest(body), hash, file);
  return JSON.parse(body);
}
const stages = { 'Pauline Epistle': 0, 'Catholic Epistle': 1, 'Acts of the Apostles': 2, Psalm: 3, Gospel: 4 };
const services = { Vespers: 0, Matins: 1, Liturgy: 2 };
const ordinary = r => r.source_kind === 'copticchurch_date' && r.source_family === 'ordinary_date_resolved' && !r.service_hour;

test('npm daily preserves ordinary service-stage and supplied companion-fragment order', () => {
  let checked = 0;
  let unaffected = 0;
  const changes = {R1: 0, R2: 0, R4: 0};
  const rawContract = authenticated('sources/resolver-review-2026-10-29/raw-fragment-contract.json', 'fa2a7f2ae2a09bbb90a15cbcc5a24b3b07031f6a5d60726ab044ac497b45f61e');
  for (const year of [2026, 2027, 2028]) {
    const design = authenticated(`out/design/daily/lectionary-${year}.json`, historical[year][0]);
    const shipped = JSON.parse(fs.readFileSync(path.join(packageRoot, `data/daily/lectionary-${year}.json`), 'utf8'));
    const predecessorProjection = {};
    for (const [date, rows] of Object.entries(design).sort(([a], [b]) => a.localeCompare(b))) {
      let expected = rows.filter(ordinary);
      if (!expected.length || expected.some(r => !(r.slot in stages) || !(r.service_section in services))) continue;
      // Cached Palm Liturgy h5 explicitly prints Matthew, Mark, Luke, John
      // (2026-04-05.html:278). The source-backed special appointment is tested
      // separately; the generic projection must not demand reverse-store order.
      const palm = expected.map((r, i) => r.occasion === 'Palm Sunday'
        && r.service_section === 'Liturgy' && r.slot === 'Gospel' ? i : -1).filter(i => i >= 0);
      if (palm.length) {
        const sourceRefs = ['Matt 21:1-17', 'Mark 11:1-11', 'Lk 19:29-48', 'Jn 12:12-19'];
        assert.equal(palm.length, 4, date);
        const ordered = sourceRefs.map(ref => {
          const matches = palm.map(i => expected[i]).filter(r => r.canonical_mt_ref === ref);
          assert.equal(matches.length, 1, `${date}: ${ref}`);
          return matches[0];
        });
        palm.forEach((position, i) => { expected[position] = ordered[i]; });
      }
      predecessorProjection[date] = expected.map(tuple);
      const qualified = ref => rawContract.some(raw => raw.source_family === 'ordinary_date_resolved'
        && raw.source_kind === 'copticchurch_date' && raw.gregorian_date === date
        && raw.passage === ref && expected.some(r => r.source_locator === `${raw.url}; ${raw.source_file}:row ${raw.source_row_id}; source_ref=${raw.source_ref}`));
      let changed = false;
      if (['2026-01-01', '2027-01-01'].includes(date)) {
        const plan = authenticated('sources/coptic-reader/kiahk-23-qualified-2026-10-29/repair-approval/repair-plan.json', '2b9e41828da41d2e9519783d5e626304d4ee176071df59e6ee033484b24b0d13');
        assert.equal(expected.length, 11, 'predecessor whole group');
        assert.equal(shipped[date].length, 9, 'R2 replaces the WHOLE proper, not individual disputed slots');
        assert.deepEqual(shipped[date].map(r => [r.service_section, r.slot, r.source_ref]), plan.appointments.map(r => [r.service_section, r.slot, r.printed_ref]));
        assert.ok(shipped[date].every(r => r.source_family === 'coptic_reader_qualified_kiahk23_review'));
        expected = [];
        changed = true; changes.R2++;
      }
      if (['2026-04-03', '2027-04-23'].includes(date)) {
        assert.ok(qualified('Lk 17:20-37'), 'R1 exact retained date/source tuple');
        const capture = fs.readFileSync(path.join(root, 'sources/coptic-reader/matins-source-accepted-2026-10-07/evidence/lent-source-completion-04/attempts/2026-04-03-ready02/Psalm_and_Gospel.txt'));
        assert.equal(digest(capture), '8a1764eb45b2e251e6401c2d5ea5a4b0c0d8c98eb258056877197f94a9983c89');
        assert.ok(capture.toString().includes('\tLuke 16:19-31\n'), 'R1 new reference is retained Reader evidence');
        expected = expected.map(r => r.service_section === 'Matins' && r.slot === 'Gospel'
          ? {...r, identity_key: identity('Lk 16:19-31'), display_ref: 'Lk 16:19-31'} : r);
        changed = true; changes.R1++;
      }
      if (['2026-04-02', '2027-04-22', '2028-04-06'].includes(date)) {
        assert.ok(qualified('Acts 25:23-27') && qualified('Acts 26:1-6'), 'R4 exact two source fragments');
        const fragments = expected.filter(r => r.service_section === 'Liturgy' && r.slot === 'Acts of the Apostles');
        assert.deepEqual(fragments.map(r => r.display_ref), ['Acts 25:23-27', 'Acts 26:1-6']);
        const ref = 'Acts 25:23-27; Acts 26:1-6';
        expected = expected.filter(r => r !== fragments[1]).map(r => r === fragments[0] ? {...r, identity_key: identity(ref), display_ref: ref} : r);
        changed = true; changes.R4++;
      }
      const actual = shipped[date].filter(ordinary);
      assert.deepEqual(actual.map(tuple), expected.map(tuple), date);
      const order = actual.map(r => services[r.service_section] * 10 + stages[r.slot]);
      assert.deepEqual(order, [...order].sort((a, b) => a - b), date);
      checked++;
      if (!changed) unaffected++;
    }
    assert.equal(digest(JSON.stringify(predecessorProjection)), historical[year][1], `${year}: retain complete historical order proof`);
  }
  assert.ok(checked > 900, 'ordinary date assertions must execute across all shipped years');
  assert.ok(unaffected > 900, 'at least 900 unaffected ordinary dates remain exact');
  assert.deepEqual(changes, {R1: 2, R2: 2, R4: 3}, 'all reviewed changes exercised, not skipped');
});
