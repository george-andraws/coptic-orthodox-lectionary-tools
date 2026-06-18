#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { createReadStream } from 'node:fs';
import { mkdir, readFile, rm, writeFile, copyFile, stat } from 'node:fs/promises';
import { createInterface } from 'node:readline';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');

const PACKAGE_NAME = '@andraws/lectionary-data';
const VERSION = '1.0.1';
const SOURCE_REPO_COMMIT = '6cc3295cad4d35ca93e7f72b1cf190a67dd4ab7e';
const LICENSE_ID = 'CC-BY-4.0';
const COPYRIGHT_HOLDER = 'George Andraws, Light and Logos (andraws.net)';
const ATTRIBUTION = 'Coptic lectionary data from Light and Logos (andraws.net), licensed under CC BY 4.0.';
const REPOSITORY_URL = 'git+https://github.com/george-andraws/coptic-orthodox-lectionary-tools.git';
const SHIPPED_YEARS = [2026, 2027, 2028];

const HANDOFF_DIR = path.join(REPO_ROOT, 'out', 'handoff');
const PACKAGE_DIR = path.join(REPO_ROOT, 'packages', 'lectionary-data');
const DATA_DIR = path.join(PACKAGE_DIR, 'data');
const DAILY_DIR = path.join(DATA_DIR, 'daily');

const OCCASION_SOURCE = path.join(HANDOFF_DIR, 'reverse_lectionary_index.jsonl');
const OCCASION_DEST = path.join(DATA_DIR, 'reverse_lectionary_index.jsonl');

function readGitHead() {
  return execFileSync('git', ['rev-parse', 'HEAD'], {
    cwd: REPO_ROOT,
    encoding: 'utf8',
  }).trim();
}

async function countJsonlRows(filePath) {
  let rows = 0;
  const lineReader = createInterface({
    input: createReadStream(filePath, { encoding: 'utf8' }),
    crlfDelay: Infinity,
  });

  for await (const line of lineReader) {
    if (line.trim()) rows += 1;
  }

  return rows;
}

async function readDailyInfo(year) {
  const source = path.join(HANDOFF_DIR, 'daily', `lectionary-${year}.json`);
  const destination = path.join(DAILY_DIR, `lectionary-${year}.json`);
  const body = await readFile(source, 'utf8');
  const parsed = JSON.parse(body);

  if (!parsed || Array.isArray(parsed) || typeof parsed !== 'object') {
    throw new Error(`${source} must be a JSON object keyed by ISO date.`);
  }

  for (const [date, readings] of Object.entries(parsed)) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      throw new Error(`${source} has a non ISO date key: ${date}`);
    }
    if (!Array.isArray(readings)) {
      throw new Error(`${source} date ${date} must map to an array of readings.`);
    }
  }

  await copyFile(source, destination);
  const stats = await stat(destination);

  return {
    year,
    rows: Object.keys(parsed).length,
    bytes: stats.size,
  };
}

function packageJson() {
  return {
    name: PACKAGE_NAME,
    version: VERSION,
    description: 'Coptic Orthodox reverse-lectionary occasion index and date-resolved daily readings.',
    license: LICENSE_ID,
    repository: {
      type: 'git',
      url: REPOSITORY_URL,
    },
    main: 'index.js',
    files: ['index.js', 'meta.json', 'README.md', 'LICENSE', 'data/'],
    publishConfig: {
      access: 'public',
    },
    dependencies: {},
  };
}

function indexJs() {
  return `'use strict';

const path = require('node:path');
const meta = require('./meta.json');

const packageRoot = __dirname;
const occasionIndexPath = path.resolve(packageRoot, 'data', 'reverse_lectionary_index.jsonl');
const dailyDir = path.resolve(packageRoot, 'data', 'daily');
const shippedYears = Object.freeze([...meta.shipped_years]);

function dailyYearPath(year) {
  const numericYear = Number(year);
  if (!Number.isInteger(numericYear)) {
    throw new TypeError('year must be an integer year.');
  }
  if (!shippedYears.includes(numericYear)) {
    throw new RangeError(\`No lectionary daily file is shipped for year \${numericYear}.\`);
  }
  return path.resolve(dailyDir, \`lectionary-\${numericYear}.json\`);
}

module.exports = {
  occasionIndexPath,
  dailyDir,
  dailyYearPath,
  shippedYears,
  meta,
};
`;
}

function licenseText() {
  return `Coptic Orthodox Reverse-Lectionary Data
Copyright (c) 2026 ${COPYRIGHT_HOLDER}

This work is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to share and adapt this material for any purpose, including commercially, as long as you
give appropriate credit, provide a link to the license, and indicate if changes were made.

License deed: https://creativecommons.org/licenses/by/4.0/
Legal code: https://creativecommons.org/licenses/by/4.0/legalcode

Required attribution:
${ATTRIBUTION}

Scope: The lectionary readings and their liturgical assignments are the tradition of the Coptic
Orthodox Church. This license applies to the compilation, structure, encoding, identity keys, and
editorial curation in this dataset, not to the underlying tradition.
`;
}

function readme(meta) {
  return `# ${PACKAGE_NAME}

Coptic Orthodox reverse-lectionary occasion index and date-resolved daily readings packaged for npm consumers.

## What this package contains

- \`data/reverse_lectionary_index.jsonl\`: one JSON object per line for reverse lookup by lectionary occasion and reading identity.
- \`data/daily/lectionary-2026.json\`, \`lectionary-2027.json\`, and \`lectionary-2028.json\`: date-resolved readings keyed by ISO date.
- \`index.js\`: CommonJS exports for stable resolved paths and package metadata.
- \`meta.json\`: package provenance, counts, shipped years, and schema notes.

## Usage

\`\`\`js
const lectionaryData = require('${PACKAGE_NAME}');

console.log(lectionaryData.occasionIndexPath);
console.log(lectionaryData.dailyYearPath(2026));
console.log(lectionaryData.shippedYears);
console.log(lectionaryData.meta.source_repo_commit);
\`\`\`

## Exports

- \`occasionIndexPath\`: absolute path to \`data/reverse_lectionary_index.jsonl\`.
- \`dailyDir\`: absolute path to \`data/daily\`.
- \`dailyYearPath(year)\`: returns the absolute path for a shipped daily lectionary JSON file.
- \`shippedYears\`: frozen array of shipped daily years.
- \`meta\`: parsed \`meta.json\`.

## Occasion index schema

Each line in \`data/reverse_lectionary_index.jsonl\` is a JSON object. The published field set is:

- \`occasion\`
- \`service_section\`
- \`service_hour\`
- \`slot\`
- \`identity_key\`
- \`display_ref\`
- \`canonical_mt_ref\`
- \`canonical_lxx_ref\`
- \`spans_json\`
- \`removed_marker\`
- \`hour_theme\`
- \`source_disclosure\`
- \`attestation_year_min\`
- \`attestation_year_max\`

### Dual-numbering display references

\`display_ref\` is the human-facing reference. Psalm references use Masoretic Text numbering as the primary display form with Septuagint numbering inline when available. Consumers that need machine normalization should use \`canonical_mt_ref\`, \`canonical_lxx_ref\`, and \`spans_json\` instead of parsing \`display_ref\`.

### Removed markers

\`removed_marker\` carries source-derived removal or omission markers where they exist. Consumers should preserve this value and should not treat marked readings as active without checking the field.

## Daily file schema

Each daily file is a JSON object keyed by ISO date, for example \`2026-04-12\`. Each value is an array of readings for that date.

Shipped years: ${meta.shipped_years.join(', ')}.

## Known limitation

Structural-only occasions without a \`gregorian_date\` are not present in the daily files yet. This includes Bright Saturday and special services.

## Provenance

- Package version: ${meta.version}
- Source repo commit: ${meta.source_repo_commit}
- Generated at: ${meta.generated_at}
- Occasion index rows: ${meta.occasion_index_rows}

## License

This package is licensed under ${LICENSE_ID}.

Required attribution:
${ATTRIBUTION}

License deed: https://creativecommons.org/licenses/by/4.0/

Scope: The lectionary readings and their liturgical assignments are the tradition of the Coptic Orthodox Church. This license applies to the compilation, structure, encoding, identity keys, and editorial curation in this dataset, not to the underlying tradition.
`;
}

function metaJson(sourceRepoCommit, occasionIndexRows, dailyFiles) {
  return {
    package_name: PACKAGE_NAME,
    version: VERSION,
    license: LICENSE_ID,
    source_repo_commit: sourceRepoCommit,
    generated_at: new Date().toISOString(),
    occasion_index_rows: occasionIndexRows,
    daily_files: dailyFiles,
    shipped_years: SHIPPED_YEARS,
    schema_notes: {
      occasion_index_fields: {
        occasion: 'Lectionary occasion label.',
        service_section: 'Service section for the reading when present.',
        service_hour: 'Service hour for the reading when present.',
        slot: 'Reading slot within the service context.',
        identity_key: 'Stable reading identity key used for reverse lookup.',
        display_ref: 'Human-facing reference, using MT primary with LXX inline where applicable.',
        canonical_mt_ref: 'Canonical Masoretic Text reference when available.',
        canonical_lxx_ref: 'Canonical Septuagint reference when available.',
        spans_json: 'Serialized span metadata for machine consumers.',
        removed_marker: 'Source-derived removal or omission marker when present.',
        hour_theme: 'Theme label attached to the service hour when present.',
        source_disclosure: 'Disclosure of source coverage or source-derived status.',
        attestation_year_min: 'Minimum attested year in the packaged source data.',
        attestation_year_max: 'Maximum attested year in the packaged source data.',
      },
      daily_file_shape: 'Each daily JSON file maps ISO dates to an array of readings.',
      known_limitation: 'Structural-only occasions without a gregorian_date, including Bright Saturday and special services, are not in the daily files yet.',
    },
  };
}

async function main() {
  const sourceRepoCommit = SOURCE_REPO_COMMIT;

  await rm(PACKAGE_DIR, { recursive: true, force: true });
  await mkdir(DAILY_DIR, { recursive: true });

  await copyFile(OCCASION_SOURCE, OCCASION_DEST);
  const occasionIndexRows = await countJsonlRows(OCCASION_DEST);
  const dailyFiles = [];

  for (const year of SHIPPED_YEARS) {
    dailyFiles.push(await readDailyInfo(year));
  }

  const meta = metaJson(sourceRepoCommit, occasionIndexRows, dailyFiles);

  await writeFile(path.join(PACKAGE_DIR, 'package.json'), `${JSON.stringify(packageJson(), null, 2)}\n`, 'utf8');
  await writeFile(path.join(PACKAGE_DIR, 'index.js'), indexJs(), 'utf8');
  await writeFile(path.join(PACKAGE_DIR, 'meta.json'), `${JSON.stringify(meta, null, 2)}\n`, 'utf8');
  await writeFile(path.join(PACKAGE_DIR, 'README.md'), readme(meta), 'utf8');
  await writeFile(path.join(PACKAGE_DIR, 'LICENSE'), licenseText(), 'utf8');

  const packageStats = await stat(OCCASION_DEST);
  console.log(JSON.stringify({
    package_name: PACKAGE_NAME,
    version: VERSION,
    source_repo_commit: sourceRepoCommit,
    occasion_index_rows: occasionIndexRows,
    occasion_index_bytes: packageStats.size,
    daily_files: dailyFiles,
    package_dir: path.relative(REPO_ROOT, PACKAGE_DIR),
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
