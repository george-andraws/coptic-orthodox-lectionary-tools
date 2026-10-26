const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const stages = { 'Pauline Epistle': 0, 'Catholic Epistle': 1, 'Acts of the Apostles': 2, Psalm: 3, Gospel: 4 };
const services = { Vespers: 0, Matins: 1, Liturgy: 2 };
const ordinary = r => r.source_kind === 'copticchurch_date' && r.source_family === 'ordinary_date_resolved' && !r.service_hour;

test('npm daily preserves ordinary service-stage and supplied companion-fragment order', () => {
  let checked = 0;
  for (const year of [2026, 2027, 2028]) {
    const design = JSON.parse(fs.readFileSync(path.join(root, `out/design/daily/lectionary-${year}.json`), 'utf8'));
    const shipped = JSON.parse(fs.readFileSync(path.join(root, `packages/lectionary-data/data/daily/lectionary-${year}.json`), 'utf8'));
    for (const [date, rows] of Object.entries(design)) {
      const expected = rows.filter(ordinary);
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
      const actual = shipped[date].filter(ordinary);
      const group = r => r.source_group_key.replace(/\bKiak\b/g, 'Kiahk').replace(/\bBaba\b/g, 'Babah');
      assert.deepEqual(actual.map(r => [r.identity_key, r.display_ref, group(r)]), expected.map(r => [r.identity_key, r.display_ref, group(r)]), date);
      const order = actual.map(r => services[r.service_section] * 10 + stages[r.slot]);
      assert.deepEqual(order, [...order].sort((a, b) => a - b), date);
      checked++;
    }
  }
  assert.ok(checked > 900, 'ordinary date assertions must execute across all shipped years');
});
