const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');

test('readings rebuild preserves 1.3 catalog, UTC calendar, APIs and metadata', () => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'lectionary-builder-'));
  const destination = path.join(fixture, 'packages/lectionary-data');
  const original = path.join(root, 'packages/lectionary-data');
  try {
    for (const directory of ['scripts/package_baselines', 'sources', 'out/design/daily']) {
      fs.mkdirSync(path.join(fixture, directory), { recursive: true });
    }
    fs.cpSync(original, destination, { recursive: true });
    for (const file of ['scripts/package_baselines/removal_effective_versions_1.1.6.json', 'sources/lectionary_corrections.json', 'out/design/reverse_lectionary_index.jsonl']) {
      fs.copyFileSync(path.join(root, file), path.join(fixture, file));
    }
    const policyFile = 'sources/canonical-occurrence-policy.json';
    fs.copyFileSync(path.join(root, policyFile), path.join(fixture, policyFile));
    const policy = JSON.parse(fs.readFileSync(path.join(root, policyFile)));
    for (const file of Object.keys(policy.source_fingerprints)) {
      fs.mkdirSync(path.dirname(path.join(fixture, file)), { recursive: true });
      fs.copyFileSync(path.join(root, file), path.join(fixture, file));
    }
    for (const year of [2026, 2027, 2028]) {
      const file = `out/design/daily/lectionary-${year}.json`;
      fs.copyFileSync(path.join(root, file), path.join(fixture, file));
    }
    fs.copyFileSync(process.env.LECTIONARY_BUILDER_UNDER_TEST || path.join(root, 'scripts/build_npm_package.mjs'), path.join(fixture, 'scripts/build_npm_package.mjs'));
    execFileSync('git', ['init', '-q'], { cwd: fixture });
    execFileSync('git', ['-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-qm', 'fixture'], { cwd: fixture });
    const beforeMeta = JSON.parse(fs.readFileSync(path.join(destination, 'meta.json')));
    execFileSync(process.execPath, [path.join(fixture, 'scripts/build_npm_package.mjs')], { cwd: fixture, stdio: 'pipe' });
    for (const file of ['calendar.js', 'index.js', 'README.md', 'LICENSE', 'data/synaxarium/synaxarium.json']) {
      assert.deepEqual(fs.readFileSync(path.join(destination, file)), fs.readFileSync(path.join(original, file)), `preserved ${file}`);
    }
    const meta = JSON.parse(fs.readFileSync(path.join(destination, 'meta.json')));
    assert.deepEqual(meta.synaxarium, beforeMeta.synaxarium);
    assert.equal(meta.schemaVersion, beforeMeta.schemaVersion);
    const manifest = JSON.parse(fs.readFileSync(path.join(destination, 'package.json')));
    assert.equal(manifest.version, '1.3.5');
    assert.deepEqual(manifest.files, JSON.parse(fs.readFileSync(path.join(original, 'package.json'))).files);
    const api = require(destination);
    assert.equal(api.synaxariumMeta.day_count, 366);
    assert.equal(api.synaxariumMeta.total_commemorations, 868);
    for (const key of Object.keys(require(original))) assert.ok(key in api, key);
    assert.equal(api.gregorianToCoptic(2026, 9, 11).monthSlug, 'tout');
    const reverseBeforeRejectedBuild = fs.readFileSync(path.join(destination, 'data/reverse_lectionary_index.jsonl'));
    const evidenceFile = path.join(fixture, 'out/data/katameros_cycle_passage_index.csv');
    const originalEvidence = fs.readFileSync(evidenceFile);
    fs.appendFileSync(evidenceFile, 'corrupted evidence');
    assert.throws(() => execFileSync(process.execPath, [path.join(fixture, 'scripts/build_npm_package.mjs')], { cwd: fixture, stdio: 'pipe' }), /source fingerprint drift/);
    assert.deepEqual(fs.readFileSync(path.join(destination, 'data/reverse_lectionary_index.jsonl')), reverseBeforeRejectedBuild);
    fs.writeFileSync(evidenceFile, originalEvidence);
    fs.writeFileSync(path.join(destination, 'package.json'), JSON.stringify({ ...manifest, version: '1.4.0' }));
    assert.throws(() => execFileSync(process.execPath, [path.join(fixture, 'scripts/build_npm_package.mjs')], { cwd: fixture, stdio: 'pipe' }), /refusing destructive legacy rebuild/);
    assert.deepEqual(fs.readFileSync(path.join(destination, 'data/reverse_lectionary_index.jsonl')), reverseBeforeRejectedBuild);
  } finally {
    fs.rmSync(fixture, { recursive: true, force: true });
  }
});
