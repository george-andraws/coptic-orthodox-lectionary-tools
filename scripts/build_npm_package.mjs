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
const VERSION = '1.1.4';
const SCHEMA_VERSION = '1.1.0';
const LICENSE_ID = 'CC-BY-4.0';
const COPYRIGHT_HOLDER = 'George Andraws, Light and Logos (andraws.net)';
const ATTRIBUTION = 'Coptic lectionary data from Light and Logos (andraws.net), licensed under CC BY 4.0.';
const REPOSITORY_URL = 'git+https://github.com/george-andraws/coptic-orthodox-lectionary-tools.git';
const SHIPPED_YEARS = [2026, 2027, 2028];

const DESIGN_DIR = path.join(REPO_ROOT, 'out', 'design');
const PACKAGE_DIR = path.join(REPO_ROOT, 'packages', 'lectionary-data');
const DATA_DIR = path.join(PACKAGE_DIR, 'data');
const DAILY_DIR = path.join(DATA_DIR, 'daily');

const OCCASION_SOURCE = path.join(DESIGN_DIR, 'reverse_lectionary_index.jsonl');
const OCCASION_DEST = path.join(DATA_DIR, 'reverse_lectionary_index.jsonl');

function readGitHead() {
  return execFileSync('git', ['rev-parse', 'HEAD'], {
    cwd: REPO_ROOT,
    encoding: 'utf8',
  }).trim();
}

function readGitDirty() {
  return execFileSync('git', ['status', '--porcelain'], {
    cwd: REPO_ROOT,
    encoding: 'utf8',
  }).trim().length > 0;
}

function dateToIso(date) {
  return date.toISOString().slice(0, 10);
}

function allDatesForYear(year) {
  const out = [];
  for (let date = new Date(Date.UTC(year, 0, 1)); date.getUTCFullYear() === year; date.setUTCDate(date.getUTCDate() + 1)) {
    out.push(dateToIso(date));
  }
  return out;
}

function julianPaschaGregorian(year) {
  const a = year % 4;
  const b = year % 7;
  const c = year % 19;
  const d = (19 * c + 15) % 30;
  const e = (2 * a + 4 * b - d + 34) % 7;
  const month = Math.floor((d + e + 114) / 31);
  const day = ((d + e + 114) % 31) + 1;
  const julianDate = new Date(Date.UTC(year, month - 1, day));
  julianDate.setUTCDate(julianDate.getUTCDate() + 13);
  return dateToIso(julianDate);
}

function classifyStructuralMissingDate(date) {
  return {
    date,
    classification: 'holy_week_structural_only_not_in_daily',
    expected_source: 'pascha_or_bright_saturday_structural_rows',
    severity: 'known_gap',
    next_action: 'use reverse_lectionary_index.jsonl for Pascha/Bright Saturday structural rows until daily date resolution is added',
  };
}

const SERVICE_ORDER = new Map([
  ['Vespers', 1],
  ['Matins', 2],
  ['Liturgy', 3],
]);

const LITURGY_SLOT_ORDER = new Map([
  ['Pauline Epistle', 1],
  ['Catholic Epistle', 2],
  ['Acts of the Apostles', 3],
  ['Praxis', 3],
  ['Psalm', 4],
  ['Gospel', 5],
]);

const PSALM_GOSPEL_SLOT_ORDER = new Map([
  ['Psalm', 1],
  ['Gospel', 2],
]);

function slotType(slot) {
  const compact = String(slot || '').toLowerCase().replace(/[^a-z]/g, '');
  if (compact.includes('psalm')) return 'psalm';
  if (compact.includes('gospel')) return 'gospel';
  if (compact.includes('pauline')) return 'pauline';
  if (compact.includes('catholic') || compact.includes('catholicon')) return 'catholicon';
  if (compact.includes('acts') || compact.includes('praxis')) return 'praxis';
  if (compact.includes('prophecy') || compact.startsWith('ot')) return 'prophecy';
  return 'source_label_preserved';
}

function serviceOrder(serviceSection) {
  return SERVICE_ORDER.get(serviceSection) ?? 99;
}

function slotOrder(slot, serviceSection) {
  if (serviceSection === 'Liturgy') return LITURGY_SLOT_ORDER.get(slot) ?? 99;
  if (serviceSection === 'Vespers' || serviceSection === 'Matins') return PSALM_GOSPEL_SLOT_ORDER.get(slot) ?? 99;
  return LITURGY_SLOT_ORDER.get(slot) ?? PSALM_GOSPEL_SLOT_ORDER.get(slot) ?? 99;
}

const SOURCE_PRIORITY = new Map([
  ['ordinary_date_resolved', 10],
  ['coptic_reader_fixture', 20],
  ['holy_pascha_curated_day_hour', 30],
  ['holy_pascha', 40],
  ['katameros_cycle', 90],
]);
const WEEKDAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
const ORDINALS = new Map([
  [1, 'first'],
  [2, 'second'],
  [3, 'third'],
  [4, 'fourth'],
  [5, 'fifth'],
  [6, 'sixth'],
  [7, 'seventh'],
  [8, 'eighth'],
]);

function normalizeLegacyMonthSpellings(text) {
  return String(text)
    .replace(/\bKiak\b/g, 'Kiahk')
    .replace(/\bBaba\b/g, 'Babah');
}

function normalizeObjectStrings(value) {
  if (typeof value === 'string') return normalizeLegacyMonthSpellings(value);
  if (Array.isArray(value)) return value.map(normalizeObjectStrings);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([key, entry]) => [key, normalizeObjectStrings(entry)]));
  }
  return value;
}

function normalizeContextText(value) {
  return normalizeLegacyMonthSpellings(String(value || ''))
    .replace(/<br\s*\/?\s*>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace('/Pentecost', '')
    .replace(/[(),]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}

function normalizedService(value) {
  const compact = String(value || '').toLowerCase().replace(/[^a-z]/g, '');
  if (compact.includes('vespers')) return 'vespers';
  if (compact.includes('matins')) return 'matins';
  if (compact.includes('liturgy')) return 'liturgy';
  return normalizeContextText(value);
}

function normalizedSlotType(row) {
  if (row.slot_type) return normalizeContextText(row.slot_type);
  return slotType(row.slot);
}

function priority(row) {
  return SOURCE_PRIORITY.get(String(row.source_family || '')) ?? 100;
}

function mappedCycleContexts(row) {
  const contexts = new Set();
  if (row.source_family !== 'katameros_cycle') return contexts;
  const occasion = String(row.occasion || '');
  const calendarKeys = String(row.calendar_keys || '');
  for (const match of calendarKeys.matchAll(/week\s+(\d+)\s+day_of_week\s+(\d+)/g)) {
    const week = Number(match[1]);
    const day = Number(match[2]);
    const ordinal = ORDINALS.get(week);
    const weekday = WEEKDAYS[day];
    if (!ordinal || !weekday) continue;
    if (occasion.includes('Holy Fifty')) {
      contexts.add(normalizeContextText(`${weekday} of the ${ordinal} week of the holy fifty days`));
    } else if (occasion.includes('Great Lent')) {
      contexts.add(normalizeContextText(`${weekday} of the ${ordinal} week of great lent`));
    }
  }
  return contexts;
}

function consumerContexts(row) {
  const contexts = mappedCycleContexts(row);
  for (const field of ['occasion', 'calendar_keys', 'day_titles']) {
    for (const part of String(row[field] || '').split(/\s*(?:;|\|\|)\s*/)) {
      const normalized = normalizeContextText(part);
      if (normalized && !['holy fifty days cycle', 'holy fifty days', 'great lent jonah nineveh cycle'].includes(normalized)) {
        contexts.add(normalized);
      }
    }
  }
  return contexts;
}

function parseSpans(row) {
  try {
    const parsed = JSON.parse(row.spans_json || '[]');
    return Array.isArray(parsed) ? parsed.filter((span) => span && typeof span === 'object') : [];
  } catch {
    return [];
  }
}

function spanInterval(span) {
  const book = String(span.book || '').toLowerCase();
  const chapterStart = Number(span.chapter_start);
  const chapterEnd = Number(span.chapter_end || span.chapter_start);
  const verseStart = Number(span.verse_start || 0);
  const verseEnd = Number(span.verse_end || verseStart);
  if (!book || !Number.isFinite(chapterStart) || !Number.isFinite(chapterEnd) || !Number.isFinite(verseStart) || !Number.isFinite(verseEnd)) {
    return null;
  }
  return { book, start: chapterStart * 1000 + verseStart, end: chapterEnd * 1000 + verseEnd };
}

function spansOverlap(left, right) {
  const leftIntervals = parseSpans(left).map(spanInterval).filter(Boolean);
  const rightIntervals = parseSpans(right).map(spanInterval).filter(Boolean);
  return leftIntervals.some((a) => rightIntervals.some((b) => a.book === b.book && a.start <= b.end && b.start <= a.end));
}

function passageVariant(left, right) {
  const leftRef = normalizeContextText(left.canonical_mt_ref || left.display_ref);
  const rightRef = normalizeContextText(right.canonical_mt_ref || right.display_ref);
  return Boolean(leftRef && rightRef && leftRef !== rightRef);
}

function projectionGroupKey(row, context) {
  return [context, normalizedService(row.service_section), normalizeContextText(row.service_hour), normalizedSlotType(row)].join('|');
}

function suppressLowerPriorityPassageVariants(rows) {
  const groups = new Map();
  for (const [index, row] of rows.entries()) {
    if (String(row.removed_marker || '').trim()) continue;
    if (String(row.current_status || '').toLowerCase().startsWith('superseded')) continue;
    for (const context of consumerContexts(row)) {
      const key = projectionGroupKey(row, context);
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push({ index, row });
    }
  }

  const suppressed = new Map();
  for (const [contextKey, members] of groups.entries()) {
    for (let leftIndex = 0; leftIndex < members.length; leftIndex += 1) {
      for (let rightIndex = leftIndex + 1; rightIndex < members.length; rightIndex += 1) {
        const left = members[leftIndex];
        const right = members[rightIndex];
        if (priority(left.row) === priority(right.row)) continue;
        if (!spansOverlap(left.row, right.row) || !passageVariant(left.row, right.row)) continue;
        const preferred = priority(left.row) < priority(right.row) ? left : right;
        const lower = preferred === left ? right : left;
        if (!suppressed.has(lower.index)) {
          suppressed.set(lower.index, {
            context_key: contextKey,
            preferred_source_family: preferred.row.source_family || '',
            preferred_display_ref: preferred.row.display_ref || '',
            suppressed_source_family: lower.row.source_family || '',
            suppressed_display_ref: lower.row.display_ref || '',
            suppressed_identity_key: lower.row.identity_key || '',
          });
        }
      }
    }
  }

  return {
    rows: rows.filter((_row, index) => !suppressed.has(index)),
    suppressions: [...suppressed.values()],
  };
}

function disambiguateWeekdaySpecificRows(rows) {
  const sundaySpecific = new Set();
  for (const row of rows) {
    const occasion = String(row.occasion || '');
    if (occasion.startsWith('Sunday, ')) {
      const base = occasion.slice('Sunday, '.length);
      sundaySpecific.add([base, row.source_family || '', row.identity_key || '', row.service_section || '', row.slot_type || '', row.display_ref || ''].join('|'));
    }
  }

  let disambiguated = 0;
  const updated = rows.map((row) => {
    const key = [row.occasion || '', row.source_family || '', row.identity_key || '', row.service_section || '', row.slot_type || '', row.display_ref || ''].join('|');
    if (!sundaySpecific.has(key)) return row;
    const replacement = `Non-Sunday ${row.occasion}`;
    const next = { ...row };
    for (const field of ['occasion', 'calendar_keys', 'day_titles']) {
      if (next[field] === row.occasion) next[field] = replacement;
    }
    disambiguated += 1;
    return next;
  });
  return { rows: updated, disambiguated };
}

async function projectReverseIndex() {
  const body = await readFile(OCCASION_SOURCE, 'utf8');
  const parsedRows = body
    .split(/\r?\n/)
    .filter((line) => line.trim())
    .map((line, index) => {
      try {
        return normalizeObjectStrings(JSON.parse(line));
      } catch (error) {
        throw new Error(`${OCCASION_SOURCE} line ${index + 1}: ${error.message}`);
      }
    });

  const disambiguated = disambiguateWeekdaySpecificRows(parsedRows);
  const projected = suppressLowerPriorityPassageVariants(disambiguated.rows);
  await writeFile(OCCASION_DEST, `${projected.rows.map((row) => JSON.stringify(row)).join('\n')}\n`, 'utf8');
  return {
    source_rows: parsedRows.length,
    output_rows: projected.rows.length,
    lower_priority_passage_variants_suppressed: projected.suppressions.length,
    weekday_specific_contexts_disambiguated: disambiguated.disambiguated,
    legacy_month_spellings_normalized: ['Kiak -> Kiahk', 'Baba -> Babah'],
    suppressed_examples: projected.suppressions.slice(0, 20),
  };
}

function sortDailyReadings(readings) {
  const enriched = readings.map((reading) => ({
    ...reading,
    service_order: serviceOrder(reading.service_section),
    slot_type: slotType(reading.slot),
    slot_order: slotOrder(reading.slot, reading.service_section),
  }));
  enriched.sort((a, b) => {
    const keysA = [a.service_order, a.service_section || '', a.service_hour || '', a.slot_order, a.slot || '', a.display_ref || '', a.identity_key || ''];
    const keysB = [b.service_order, b.service_section || '', b.service_hour || '', b.slot_order, b.slot || '', b.display_ref || '', b.identity_key || ''];
    return keysA < keysB ? -1 : keysA > keysB ? 1 : 0;
  });
  return enriched.map((reading, index) => ({
    reading_order: index + 1,
    ...reading,
  }));
}

function buildStructuralDateResolver(dailyInfos) {
  const missingDatesByYear = {};
  for (const info of dailyInfos) {
    missingDatesByYear[String(info.year)] = info.missing_dates.map(classifyStructuralMissingDate);
  }
  return {
    schema: 'julian_pascha_structural_gap_v1',
    coverage: 'partial_daily_with_structural_date_resolver',
    exported_function: 'classifyDate(date)',
    date_key_format: 'YYYY-MM-DD',
    shipped_years: SHIPPED_YEARS,
    missing_dates_by_year: missingDatesByYear,
    contract: 'If classifyDate(date).hasDailyReadings is false and classification is holy_week_structural_only_not_in_daily, use reverse_lectionary_index.jsonl for Pascha/Bright Saturday structural rows. Do not treat the daily file omission as data loss.',
    pascha_computus: 'Julian/Coptic Pascha converted to Gregorian with 13-day offset for the shipped range.',
  };
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
  const source = path.join(DESIGN_DIR, 'daily', `lectionary-${year}.json`);
  const destination = path.join(DAILY_DIR, `lectionary-${year}.json`);
  const body = await readFile(source, 'utf8');
  const parsed = JSON.parse(body);

  if (!parsed || Array.isArray(parsed) || typeof parsed !== 'object') {
    throw new Error(`${source} must be a JSON object keyed by ISO date.`);
  }

  const sorted = {};
  for (const date of Object.keys(parsed).sort()) {
    const readings = parsed[date];
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      throw new Error(`${source} has a non ISO date key: ${date}`);
    }
    if (!Array.isArray(readings)) {
      throw new Error(`${source} date ${date} must map to an array of readings.`);
    }
    sorted[date] = sortDailyReadings(readings.map((reading) => normalizeObjectStrings(reading)));
  }

  await writeFile(destination, `${JSON.stringify(sorted, null, 2)}\n`, 'utf8');
  const stats = await stat(destination);

  const presentDates = new Set(Object.keys(sorted));
  const missingDates = allDatesForYear(year).filter((date) => !presentDates.has(date));
  const dateCount = Object.keys(sorted).length;
  const readingCount = Object.values(sorted).reduce((total, readings) => total + readings.length, 0);

  return {
    year,
    rows: dateCount,
    date_count: dateCount,
    reading_count: readingCount,
    bytes: stats.size,
    missing_dates: missingDates,
    pascha_date: julianPaschaGregorian(year),
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
const structuralDateResolver = Object.freeze(meta.structural_date_resolver || {});

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

function classifyDate(date) {
  if (typeof date !== 'string' || !/^\\d{4}-\\d{2}-\\d{2}$/.test(date)) {
    throw new TypeError('date must be an ISO YYYY-MM-DD string.');
  }
  const year = Number(date.slice(0, 4));
  if (!shippedYears.includes(year)) {
    return {
      date,
      year,
      shippedYear: false,
      hasDailyReadings: false,
      classification: 'unshipped_year',
      dailyPath: null,
    };
  }
  const missing = (((meta.structural_date_resolver || {}).missing_dates_by_year || {})[String(year)] || []).find((entry) => entry.date === date);
  if (missing) {
    return {
      ...missing,
      year,
      shippedYear: true,
      hasDailyReadings: false,
      dailyPath: dailyYearPath(year),
    };
  }
  return {
    date,
    year,
    shippedYear: true,
    hasDailyReadings: true,
    classification: 'daily_file_present',
    dailyPath: dailyYearPath(year),
  };
}

module.exports = {
  occasionIndexPath,
  dailyDir,
  dailyYearPath,
  classifyDate,
  structuralDateResolver,
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
- \`index.js\`: CommonJS exports for stable resolved paths, package metadata, and structural date classification.
- \`meta.json\`: package provenance, schema version, counts, shipped years, structural date resolver contract, and schema notes. In \`daily_files\`, \`rows\` is retained as the legacy date-count field; use \`date_count\` and \`reading_count\` for explicit counts.

## Usage

\`\`\`js
const lectionaryData = require('${PACKAGE_NAME}');

console.log(lectionaryData.occasionIndexPath);
console.log(lectionaryData.dailyYearPath(2026));
console.log(lectionaryData.shippedYears);
console.log(lectionaryData.meta.source_repo_commit);
console.log(lectionaryData.classifyDate('2026-04-10'));
\`\`\`

## Exports

- \`occasionIndexPath\`: absolute path to \`data/reverse_lectionary_index.jsonl\`.
- \`dailyDir\`: absolute path to \`data/daily\`.
- \`dailyYearPath(year)\`: returns the absolute path for a shipped daily lectionary JSON file.
- \`classifyDate(date)\`: classifies a shipped ISO date as present in daily JSON or as a documented structural-only Holy Week/Bright Saturday gap.
- \`structuralDateResolver\`: resolver metadata copied from \`meta.structural_date_resolver\`.
- \`shippedYears\`: frozen array of shipped daily years.
- \`meta\`: parsed \`meta.json\`.

## Occasion index schema

Each line in \`data/reverse_lectionary_index.jsonl\` is a JSON object. The published field set is:

- \`occasion\`
- \`service_section\`
- \`service_hour\`
- \`slot\`
- \`slot_type\`
- \`slot_order\`
- \`occasion_kind\`
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

Each daily reading includes a unique \`reading_order\` within that date. The package writes daily arrays sorted by \`reading_order\`, using deterministic service and slot ordering: Vespers, Matins, then Liturgy; within those services, Psalm/Gospel for Vespers and Matins, and Pauline, Catholic, Acts, Psalm, Gospel for Liturgy. \`slot_order\` may repeat for split Psalm verses or readings that share one liturgical slot; use \`reading_order\` when a unique date-local order is required.

In \`meta.daily_files\`, \`rows\` is retained as a legacy alias for \`date_count\`. Use \`date_count\` for the number of ISO date keys and \`reading_count\` for the total number of readings across those dates.

## Structural date resolver

The daily files intentionally omit some Holy Week / Bright Saturday dates whose readings live as structural Pascha rows in \`reverse_lectionary_index.jsonl\`. These omissions are enumerated in \`meta.structural_date_resolver.missing_dates_by_year\` and exposed through \`classifyDate(date)\`.

For example, \`classifyDate('2026-04-10')\` returns \`hasDailyReadings: false\` with classification \`holy_week_structural_only_not_in_daily\`; consumers should use the reverse index for those structural rows instead of treating the date as data loss.

## Source-priority projection

The package projects the raw reverse index into a consumer-safe runtime index. When a copticchurch.net date-resolved row and a lower-priority local cycle row overlap the same normalized consumer occasion, service, service hour, and slot type but disagree on the passage span, the lower-priority variant is omitted from the npm package. This keeps current-practice rows authoritative while retaining non-conflicting local witnesses.

For fixed-date rows with a Sunday-specific counterpart, generic rows are disambiguated as non-Sunday contexts rather than silently duplicated.

Projection counts and examples are recorded in \`meta.projection_rules\`.

## Span and Psalm numbering contract

\`spans_json\` contains machine-readable canonical spans when the reading can be represented as biblical book/chapter/verse ranges. It may be an empty array for named non-standard readings supplied by Coptic Reader fixtures, such as \`Memoirs of Job\`; in that case use \`reading_type\`, \`reading_name\`, and \`display_ref\`.

Psalm \`display_ref\` values may include inline dual numbering, for example \`Ps 105:14-15 (LXX Ps 104:14-15)\`. Consumers should not parse \`display_ref\` for machine matching. Use \`canonical_mt_ref\`, \`canonical_lxx_ref\`, and \`spans_json\`.

## Known limitation

Structural-only occasions without a \`gregorian_date\` are not present in the daily files yet. This includes Bright Saturday and special services. Known shipped-year Holy Week / Bright Saturday daily omissions are not silent gaps; they are listed in \`meta.structural_date_resolver\` and classified by \`classifyDate(date)\`.

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

function metaJson(sourceRepoCommit, sourceTreeDirty, occasionIndexRows, dailyFiles, structuralDateResolver, projectionRules) {
  return {
    package_name: PACKAGE_NAME,
    version: VERSION,
    schemaVersion: SCHEMA_VERSION,
    schema_version: SCHEMA_VERSION,
    license: LICENSE_ID,
    source_repo_commit: sourceRepoCommit,
    source_tree_dirty: sourceTreeDirty,
    generated_at: new Date().toISOString(),
    occasion_index_rows: occasionIndexRows,
    daily_files: dailyFiles,
    shipped_years: SHIPPED_YEARS,
    structural_date_resolver: structuralDateResolver,
    projection_rules: projectionRules,
    schema_notes: {
      occasion_index_fields: {
        occasion: 'Lectionary occasion label.',
        service_section: 'Service section for the reading when present.',
        service_hour: 'Service hour for the reading when present.',
        slot: 'Original reading slot label from the source pipeline, preserved for provenance.',
        slot_type: 'Normalized slot category, such as prophecy, psalm, gospel, pauline, catholicon, or praxis.',
        slot_order: 'Source-backed reading order within the service hour and normalized slot family when determinable; null only for preserved unmapped source labels.',
        occasion_kind: 'Occasion classification: specific for dated/named occasions, cycle for generic cycle or rule labels.',
        identity_key: 'Stable reading identity key used for reverse lookup.',
        display_ref: 'Human-facing reference, using MT primary with LXX inline where applicable.',
        canonical_mt_ref: 'Canonical Masoretic Text reference when available.',
        canonical_lxx_ref: 'Canonical Septuagint reference when available.',
        spans_json: 'Serialized span metadata for machine consumers. Empty array is allowed for named non-standard readings that cannot be represented as biblical chapter/verse spans, such as Memoirs of Job.',
        removed_marker: 'Source-derived removal or omission marker when present.',
        hour_theme: 'Theme label attached to the service hour when present.',
        source_disclosure: 'Disclosure of source coverage or source-derived status.',
        attestation_year_min: 'Minimum attested year in the packaged source data.',
        attestation_year_max: 'Maximum attested year in the packaged source data.',
      },
      daily_file_shape: 'Each daily JSON file maps ISO dates to an array of readings sorted by reading_order. Each reading includes reading_order, service_order, slot_type, and slot_order; slot_order may repeat within split Psalm/reading fragments, while reading_order is unique per date.',
      structural_date_resolver: 'meta.structural_date_resolver lists shipped-year dates intentionally omitted from daily files because they are structural Holy Week/Bright Saturday rows resolved through reverse_lectionary_index.jsonl.',
      psalm_dual_numbering: 'Psalm display_ref may include inline LXX numbering in parentheses. Use canonical_mt_ref, canonical_lxx_ref, and spans_json for machine matching.',
      canonicalization_notes: 'canonicalization_note values are source/provenance hints, not date or service resolvers.',
      multi_source_family: 'The same identity_key may appear across multiple source_family values and distinct occasions; this is expected attestation breadth, not a duplicate by itself.',
      source_priority_projection: 'When current copticchurch.net date-resolved rows overlap lower-priority cycle rows for the same normalized consumer context/service/hour/slot but disagree on passage span, the npm package omits the lower-priority variant. See meta.projection_rules for counts and examples.',
      coptic_month_spellings: 'Runtime package labels normalize Kiak to Kiahk and Baba to Babah.',
      weekday_specific_disambiguation: 'When a Sunday-specific fixed-date row has a generic sibling with the same reading identity, the generic sibling is labeled as a non-Sunday context to avoid consumer duplicate grouping.',
      known_limitation: 'Structural-only occasions without a gregorian_date, including Bright Saturday and special services, are not in the daily files yet.',
    },
  };
}

async function main() {
  const sourceRepoCommit = readGitHead();
  const sourceTreeDirty = readGitDirty();

  await rm(PACKAGE_DIR, { recursive: true, force: true });
  await mkdir(DAILY_DIR, { recursive: true });

  const projectionRules = await projectReverseIndex();
  const occasionIndexRows = projectionRules.output_rows;
  const dailyInfos = [];

  for (const year of SHIPPED_YEARS) {
    dailyInfos.push(await readDailyInfo(year));
  }
  const dailyFiles = dailyInfos.map(({ missing_dates, pascha_date, ...info }) => info);
  const structuralDateResolver = buildStructuralDateResolver(dailyInfos);

  const meta = metaJson(sourceRepoCommit, sourceTreeDirty, occasionIndexRows, dailyFiles, structuralDateResolver, projectionRules);

  await writeFile(path.join(PACKAGE_DIR, 'package.json'), `${JSON.stringify(packageJson(), null, 2)}\n`, 'utf8');
  await writeFile(path.join(PACKAGE_DIR, 'index.js'), indexJs(), 'utf8');
  await writeFile(path.join(PACKAGE_DIR, 'meta.json'), `${JSON.stringify(meta, null, 2)}\n`, 'utf8');
  await writeFile(path.join(PACKAGE_DIR, 'README.md'), readme(meta), 'utf8');
  await writeFile(path.join(PACKAGE_DIR, 'LICENSE'), licenseText(), 'utf8');

  const packageStats = await stat(OCCASION_DEST);
  console.log(JSON.stringify({
    package_name: PACKAGE_NAME,
    version: VERSION,
    schemaVersion: SCHEMA_VERSION,
    source_repo_commit: sourceRepoCommit,
    source_tree_dirty: sourceTreeDirty,
    occasion_index_rows: occasionIndexRows,
    occasion_index_bytes: packageStats.size,
    daily_files: dailyFiles,
    projection_rules: projectionRules,
    package_dir: path.relative(REPO_ROOT, PACKAGE_DIR),
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
