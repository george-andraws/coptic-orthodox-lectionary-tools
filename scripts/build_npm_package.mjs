#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { mkdir, readFile, writeFile, copyFile, stat } from 'node:fs/promises';
import { createInterface } from 'node:readline';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');

const PACKAGE_NAME = '@andraws/lectionary-data';
const VERSION = '1.3.6';
const SCHEMA_VERSION = '1.2.0';
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
const REMOVAL_EFFECTIVE_VERSION_BASELINE = path.join(
  REPO_ROOT,
  'scripts',
  'package_baselines',
  'removal_effective_versions_1.1.6.json',
);
const SOURCE_CORRECTIONS = path.join(REPO_ROOT, 'sources', 'lectionary_corrections.json');

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
  const first = new Date(0);
  first.setUTCHours(0, 0, 0, 0);
  first.setUTCFullYear(year, 0, 1);
  for (let date = first; date.getUTCFullYear() === year; date.setUTCDate(date.getUTCDate() + 1)) {
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
  ['vespers', 1],
  ['matins', 2],
  ['midnightpraises', 3],
  ['firsthour', 10],
  ['1sthour', 10],
  ['thirdhour', 20],
  ['3rdhour', 20],
  ['sixthhour', 30],
  ['6thhour', 30],
  ['ninthhour', 40],
  ['9thhour', 40],
  ['liturgyofblessingofthewater', 45],
  ['eleventhhour', 50],
  ['11thhour', 50],
  ['twelfthhour', 60],
  ['12thhour', 60],
  ['liturgy', 99],
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
  const key = String(serviceSection || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  return SERVICE_ORDER.get(key) ?? 999;
}

function existingNumericOrder(value) {
  if (value === null || value === undefined || typeof value === 'boolean' || (typeof value === 'string' && value.trim() === '')) return null;
  const numeric = Number(value);
  return Number.isInteger(numeric) && numeric > 0 ? numeric : null;
}

function slotOrder(slot, serviceSection) {
  if (serviceSection === 'Liturgy') return LITURGY_SLOT_ORDER.get(slot) ?? 99;
  if (serviceSection === 'Vespers' || serviceSection === 'Matins') return PSALM_GOSPEL_SLOT_ORDER.get(slot) ?? 99;
  return LITURGY_SLOT_ORDER.get(slot) ?? PSALM_GOSPEL_SLOT_ORDER.get(slot) ?? 99;
}

const SOURCE_PRIORITY = new Map([
  ['coptic_reader_verified_calendar_boundary', 0],
  ['coptic_reader_verified_supplement', 0],
  ['coptic_reader_verified_sunday_policy', 0],
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

function parseReferenceShape(value) {
  const text = String(value || '').replace(/\([^)]*\)/g, '').trim();
  const match = text.match(/^\s*([1-3]?\s*[A-Za-z]+)\s+(\d+):(\d+)\s*-\s*(\d+)(?::(\d+))?\s*$/);
  if (!match) return null;
  return {
    book: match[1].toLowerCase().replace(/\s+/g, ''),
    startChapter: Number(match[2]),
    startVerse: Number(match[3]),
    endChapter: Number(match[4]),
    endVerse: match[5] === undefined ? null : Number(match[5]),
  };
}

function shorthandChapterVariant(left, right) {
  const leftShape = parseReferenceShape(left.canonical_mt_ref || left.display_ref);
  const rightShape = parseReferenceShape(right.canonical_mt_ref || right.display_ref);
  if (!leftShape || !rightShape) return false;
  if (leftShape.book !== rightShape.book) return false;
  if (leftShape.startChapter !== rightShape.startChapter || leftShape.startVerse !== rightShape.startVerse) return false;
  const leftShorthand = leftShape.endVerse === null;
  const rightShorthand = rightShape.endVerse === null;
  if (leftShorthand === rightShorthand) return false;
  const shorthand = leftShorthand ? leftShape : rightShape;
  const expanded = leftShorthand ? rightShape : leftShape;
  return shorthand.endChapter === expanded.endChapter && expanded.endVerse !== null;
}

function passageOverlapOrShorthandVariant(left, right) {
  return spansOverlap(left, right) || shorthandChapterVariant(left, right);
}

function projectionGroupKey(row, context) {
  return [context, normalizedService(row.service_section), normalizeContextText(row.service_hour), normalizedSlotType(row)].join('|');
}

function isProjectionRemovedRow(row) {
  return row?.active === false || String(row?.status || '').toLowerCase() === 'removed';
}

async function loadRemovalEffectiveVersionBaseline() {
  const body = await readFile(REMOVAL_EFFECTIVE_VERSION_BASELINE, 'utf8');
  const baseline = JSON.parse(body);
  const correctionOverlay = JSON.parse(await readFile(SOURCE_CORRECTIONS, 'utf8'));
  for (const entry of correctionOverlay.projection_removal_effective_versions || []) {
    const entries = baseline.entries_by_identity_key[entry.identity_key] || [];
    if (entries.some((existing) => existing.removal_context_key === entry.removal_context_key)) {
      throw new Error(`Duplicate source-correction removal baseline for identity_key=${entry.identity_key}`);
    }
    baseline.entries_by_identity_key[entry.identity_key] = [...entries, entry];
  }
  const allEntries = Object.values(baseline.entries_by_identity_key).flat();
  baseline.entry_count = allEntries.length;
  baseline.distinct_identity_key_count = Object.keys(baseline.entries_by_identity_key).length;
  baseline.source_version = `${baseline.source_version}+source-corrections-${VERSION}`;
  const entriesByIdentityKey = baseline.entries_by_identity_key || {};
  for (const [identityKey, entries] of Object.entries(entriesByIdentityKey)) {
    if (!Array.isArray(entries) || entries.length === 0) {
      throw new Error(`Invalid removal effective-version baseline for identity_key=${identityKey}`);
    }
    for (const entry of entries) {
      if (!entry.removal_effective_version) {
        throw new Error(`Missing removal_effective_version in baseline for identity_key=${identityKey}`);
      }
      if (!entry.removal_context_key) {
        throw new Error(`Missing removal_context_key in baseline for identity_key=${identityKey}`);
      }
    }
  }
  return baseline;
}

function resolveRemovalEffectiveVersion(row, suppression, baseline) {
  const identityKey = String(row.identity_key || '');
  const contextKey = String(suppression.context_key || '');
  const entries = baseline.entries_by_identity_key?.[identityKey] || [];
  if (entries.length === 0) {
    return { value: '', reason: 'identity_key not found in baseline' };
  }
  if (entries.length === 1) {
    return { value: entries[0].removal_effective_version, reason: 'matched unique identity_key' };
  }
  const exact = entries.find((entry) => entry.removal_context_key === contextKey);
  if (exact) {
    return { value: exact.removal_effective_version, reason: 'matched identity_key and removal_context_key' };
  }
  return { value: '', reason: 'duplicated identity_key requires exact removal_context_key baseline match' };
}

function removalBaselineMiss(row, suppression, reason) {
  return normalizeObjectStrings({
    identity_key: row.identity_key || '',
    occasion: row.occasion || '',
    service_section: row.service_section || '',
    service_hour: row.service_hour || '',
    slot: row.slot || '',
    removal_context_key: suppression.context_key || '',
    display_ref: row.display_ref || '',
    reason,
  });
}

function formatRemovalBaselineMisses(misses) {
  const rows = misses.map((miss) => [
    `identity_key=${miss.identity_key}`,
    `occasion=${miss.occasion}`,
    `service_section=${miss.service_section}`,
    `service_hour=${miss.service_hour}`,
    `slot=${miss.slot}`,
    `removal_context_key=${miss.removal_context_key}`,
  ].join(' | '));
  return [
    `Removal effective-version baseline miss for ${misses.length} projection-removed row(s).`,
    'Every projection-removed row must resolve to scripts/package_baselines/removal_effective_versions_1.1.6.json; refusing to default to package VERSION.',
    ...rows,
  ].join('\n');
}

function annotateRemovedProjectionRow(row, suppression, baseline, baselineMisses) {
  const resolved = resolveRemovalEffectiveVersion(row, suppression, baseline);
  if (!resolved.value) {
    baselineMisses.push(removalBaselineMiss(row, suppression, resolved.reason));
    return row;
  }
  const consumerNote = 'Retained for provenance only because a higher-priority date-resolved source supplies the active reading for this context. Ignore this row by default in active lookups.';
  return normalizeObjectStrings({
    ...row,
    active: false,
    status: 'removed',
    removed_marker: row.removed_marker || 'removed_by_source_priority_projection',
    removal_reason: 'lower_priority_overlap_with_date_resolved_source',
    removal_context_key: suppression.context_key,
    removal_effective_version: resolved.value,
    preferred_source_family: suppression.preferred_source_family,
    preferred_source_kind: suppression.preferred_source_kind,
    preferred_source_locator: suppression.preferred_source_locator,
    preferred_identity_key: suppression.preferred_identity_key,
    preferred_display_ref: suppression.preferred_display_ref,
    retained_for: 'provenance_only',
    consumer_note: consumerNote,
  });
}

function suppressLowerPriorityPassageVariants(rows, removalEffectiveVersionBaseline) {
  const groups = new Map();
  for (const [index, row] of rows.entries()) {
    if (String(row.removed_marker || '').trim()) continue;
    // Retain historical witnesses, but never let them compete with current
    // appointments for source priority or suppress qualified current fragments.
    if (!isCurrentReading(row)) continue;
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
        if (!passageOverlapOrShorthandVariant(left.row, right.row) || !passageVariant(left.row, right.row)) continue;
        const preferred = priority(left.row) < priority(right.row) ? left : right;
        const lower = preferred === left ? right : left;
        if (!suppressed.has(lower.index)) {
          suppressed.set(lower.index, {
            context_key: contextKey,
            preferred_source_family: preferred.row.source_family || '',
            preferred_source_kind: preferred.row.source_kind || '',
            preferred_source_locator: preferred.row.source_locator || '',
            preferred_identity_key: preferred.row.identity_key || '',
            preferred_display_ref: preferred.row.display_ref || '',
            suppressed_source_family: lower.row.source_family || '',
            suppressed_display_ref: lower.row.display_ref || '',
            suppressed_identity_key: lower.row.identity_key || '',
          });
        }
      }
    }
  }

  const baselineMisses = [];
  const outputRows = rows.map((row, index) => {
    const suppression = suppressed.get(index);
    return suppression ? annotateRemovedProjectionRow(row, suppression, removalEffectiveVersionBaseline, baselineMisses) : row;
  });

  if (baselineMisses.length > 0) {
    throw new Error(formatRemovalBaselineMisses(baselineMisses));
  }

  return {
    rows: outputRows,
    activeRows: outputRows.filter((row) => !isProjectionRemovedRow(row)),
    suppressions: [...suppressed.values()],
    baseline_miss_count: baselineMisses.length,
  };
}

// Canonical consumer appointments are a projection, not a rewrite of witnesses.
// Do not feed these aliases into the legacy overlap projection/removal baseline.
function canonicalOccasion(value) {
  const aliases = { Tout: 'Tut', Hator: 'Hatur', Hatoor: 'Hatur', Kiahk: 'Kiyahk', Kiak: 'Kiyahk', Toba: 'Tubah', Amshir: 'Meshir', Bashans: 'Bashons', Paona: 'Baunah', Baba: 'Babah', Baramoudah: 'Barmuda', 'Al-Nasi': 'Nesi' };
  let text = String(value || '');
  for (const [alias, name] of Object.entries(aliases)) text = text.replace(new RegExp(`\\b${alias}\\b`, 'gi'), name);
  text = text.replace(/^(?:the\s+)?(first|second|third|fourth|fifth) Sunday of /i, (_, ordinal) => `${ordinal[0].toUpperCase()}${ordinal.slice(1).toLowerCase()} Sunday of `);
  // UK Midlands Sundays general remarks 4: the four Kiyahk lessons can
  // start on the last Sunday of Hatur. These are service-table aliases,
  // not permission to assign an uncaptured civil date or change the calendar.
  text = text.replace(/^(first|second|third|fourth) Sunday of Christmas Fast$/i, (_, ordinal) => `${ordinal[0].toUpperCase()}${ordinal.slice(1).toLowerCase()} Sunday of Kiyahk`);
  if (text === 'Wednesday') text = 'Wednesday of Holy Pascha';
  return text;
}

function qualifiedCanonicalSource(row) {
  return (row.source_family === 'katameros_cycle' && row.source_kind === 'katameros_cycle')
    || (['ordinary_date_resolved', 'coptic_reader_verified_supplement', 'coptic_reader_verified_sunday_policy', 'coptic_reader_verified_calendar_boundary'].includes(row.source_family) && row.source_kind === 'copticchurch_date')
    || (row.source_family === 'holy_pascha_curated_day_hour' && row.source_kind === 'pascha_day_hour')
    || (row.source_family === 'coptic_reader' && row.source_kind === 'coptic_reader_fixture');
}

function canonicalContexts(row) {
  if (row.source_family !== 'katameros_cycle' || row.source_kind !== 'katameros_cycle') return [{ key: canonicalOccasion(row.occasion).toLowerCase(), raw: row.calendar_keys || '' }];
  return String(row.calendar_keys || '').split(' || ').map(raw => {
    let label = raw;
    const annualSunday = row.occasion === 'annual Sundays by Coptic month/week';
    const sunday = raw.match(/^(.+) ([1-5])$/);
    const seasonal = raw.match(/^week (\d+) day_of_week ([0-6])$/);
    if (annualSunday && sunday) label = `${ORDINALS.get(Number(sunday[2]))} Sunday of ${sunday[1]}`;
    else if (seasonal && Number(seasonal[1]) > 0 && Number(seasonal[1]) <= 8) {
      const season = row.occasion.includes('Holy Fifty') ? 'the Holy Fifty Days' : 'Great Lent';
      label = `${WEEKDAYS[Number(seasonal[2])]} of the ${ORDINALS.get(Number(seasonal[1]))} week of ${season}`;
    }
    return { key: canonicalOccasion(label).toLowerCase(), raw };
  });
}

function canonicalService(row) {
  // GetFromRef in the retained SQLite implementation places Prophecy in Matins.
  if (row.source_family === 'katameros_cycle' && row.source_kind === 'katameros_cycle' && row.service_section === 'prophecy' && row.occasion.includes('Great Lent')) return 'matins';
  return normalizedService(row.service_section);
}

function sourceSelectorMatches(row, selector) {
  return Object.entries(selector).every(([key, value]) => String(key === 'calendar_keys' ? (row.source_calendar_keys || row[key] || '') : (row[key] ?? '')) === String(value));
}

function validateCanonicalRemovalVersion(value) {
  if (typeof value !== 'string' || !/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?![\s\S])/.test(value)
    || !value.split('.').every(part => Number.isSafeInteger(Number(part)))) {
    throw new Error('Invalid canonical removal effective version');
  }
  return value;
}

function retainCanonicalSupersession(row, preferred, context, reason, removalEffectiveVersion = '1.3.3') {
  validateCanonicalRemovalVersion(removalEffectiveVersion);
  return { ...row, active: false, status: 'removed',
    removed_marker: 'superseded_by_canonical_occurrence_projection',
    removal_reason: reason, removal_context_key: context, removal_effective_version: removalEffectiveVersion,
    preferred_source_family: preferred.source_family, preferred_source_kind: preferred.source_kind,
    preferred_source_locator: preferred.source_locator, preferred_identity_key: preferred.identity_key,
    preferred_display_ref: preferred.display_ref, retained_for: 'provenance_only',
    consumer_note: 'Retained for provenance only; the same source-qualified appointment is represented by the preferred current row. Ignore this row by default in active lookups. This does not change Scripture coordinates or activate held witnesses.' };
}

function canonicalizeOccurrences(inputRows, policy) {
  // Explicit epochs belong to reviewed new rules, never to the current builder
  // VERSION. Validate before replay too; omitted legacy/sentinel epochs stay put.
  for (const rule of policy.supersessions || []) {
    if (Object.hasOwn(rule, 'removal_effective_version')) validateCanonicalRemovalVersion(rule.removal_effective_version);
  }
  // Bind every source/context/disclosure/order cell before any suppression. The
  // reviewed output is accepted only for explicit idempotent replay; a new
  // source table requires renewed review, not best-effort selector matching.
  const fingerprint = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
  const inputFingerprint = fingerprint(inputRows);
  if (inputFingerprint === policy.projection_output_sha256) {
    return { rows: inputRows.map(row => ({ ...row })), dispositions: [], sentinel_additions: 0 };
  }
  if (inputFingerprint !== policy.projection_input_sha256) {
    throw new Error(`Canonical occurrence input fingerprint drift: ${inputFingerprint}`);
  }
  for (const rule of policy.supersessions || []) {
    for (const selector of [rule.lower, rule.preferred]) {
      const matches = inputRows.filter(row => isCurrentReading(row) && sourceSelectorMatches(row, selector));
      if (matches.length !== 1) throw new Error('Canonical occurrence selector must identify one authenticated current row');
    }
  }
  let rows = inputRows.map(row => ({ ...row }));
  const dispositions = [];
  const preserveAlternate = (preferred, lower) => {
    // Sunday disclosure has an authenticated one-envelope contract. Keep it
    // untouched, and retain other witnesses in this separate explicit field.
    const items = JSON.parse(preferred.alternate_source_disclosure || '[]');
    const seen = new Set(items.map(item => JSON.stringify(item)));
    for (const item of JSON.parse(lower.source_disclosure || '[]')) {
      const key = JSON.stringify(item);
      if (!seen.has(key)) { items.push(item); seen.add(key); }
    }
    preferred.alternate_source_disclosure = JSON.stringify(items);
  };
  const excludeContext = (index, preferred, context, reason, removalEffectiveVersion = '1.3.3') => {
    const row = rows[index];
    const rawKeys = String(row.calendar_keys || '').split(' || ');
    if (row.source_family === 'katameros_cycle' && !rawKeys.includes(context)) return;
    const remaining = rawKeys.filter(key => key !== context);
    preserveAlternate(preferred, row);
    dispositions.push({ identity_key: row.identity_key, source_locator: row.source_locator, context, reason, preferred_identity_key: preferred.identity_key });
    if (row.source_family === 'katameros_cycle' && remaining.length && remaining.length < rawKeys.length) {
      row.source_calendar_keys ||= row.calendar_keys;
      row.calendar_keys = remaining.join(' || ');
      row.source_day_titles ||= row.day_titles;
      row.day_titles = '';
      row.superseded_calendar_keys = [...new Set([...(row.superseded_calendar_keys || []), context])];
    } else rows[index] = retainCanonicalSupersession(row, preferred, context, reason, removalEffectiveVersion);
  };
  // Explicit complete-source-slot split/endpoint decisions, never overlap alone.
  for (const rule of policy.supersessions || []) {
    const lowerIndex = rows.findIndex(row => isCurrentReading(row) && sourceSelectorMatches(row, rule.lower));
    const preferred = rows.find(row => isCurrentReading(row) && sourceSelectorMatches(row, rule.preferred));
    if (lowerIndex < 0 || !preferred || !qualifiedCanonicalSource(preferred)) continue;
    excludeContext(lowerIndex, preferred, rule.calendar_key, rule.reason, rule.removal_effective_version);
  }
  // Week 99 is a real preparation boundary, not a recurring 99th Lent week.
  // Week 49 is an unreachable SQLite duplicate; retain its raw context only.
  const sentinelAdditions = [];
  for (const row of rows) {
    if (!isCurrentReading(row) || row.source_family !== 'katameros_cycle' || row.source_kind !== 'katameros_cycle') continue;
    const keys = String(row.calendar_keys || '').split(' || ');
    const retained = [];
    for (const key of keys) {
      if (key === policy.nonrecurring_sentinel) {
        row.source_calendar_keys ||= row.calendar_keys;
        row.nonrecurring_source_calendar_keys = [key];
      } else if (policy.sentinel_rules?.[key]) {
        const label = policy.sentinel_rules[key];
        const clone = { ...row, source_occasion: row.occasion, source_calendar_keys: row.calendar_keys, occasion: label, calendar_keys: label, occasion_kind: 'specific' };
        const locator = policy.sentinel_sources?.[[key, row.slot, row.canonical_mt_ref].join('|')];
        if (!locator) throw new Error(`Missing source-qualified preparation sentinel: ${key} ${row.slot} ${row.display_ref}`);
        clone.source_locator = locator;
        clone.collapsed_row_count = '1';
        clone.source_disclosure = JSON.stringify(JSON.parse(row.source_disclosure).map(item => ({ ...item, source_locator: locator })));
        sentinelAdditions.push(clone);
      } else retained.push(key);
    }
    if (retained.length !== keys.length) {
      row.source_calendar_keys ||= row.calendar_keys;
      if (retained.length) {
        row.calendar_keys = retained.join(' || ');
        row.source_day_titles ||= row.day_titles;
        row.day_titles = '';
      }
      else {
        const clone = sentinelAdditions[sentinelAdditions.length - 1];
        Object.assign(row, retainCanonicalSupersession(row, clone || row, row.calendar_keys, 'source_sentinel_represented_as_named_preparation'));
      }
    }
  }
  rows.push(...sentinelAdditions);
  // Apply display aliases only to supported CURRENT sources. Inactive originals
  // and authenticated Sunday labels/envelopes remain byte-for-byte untouched.
  for (const row of rows) {
    if (!isCurrentReading(row) || !qualifiedCanonicalSource(row) || row.source_family === 'coptic_reader_verified_sunday_policy') continue;
    const label = canonicalOccasion(row.occasion);
    if (label !== row.occasion) { row.source_occasion ||= row.occasion; row.occasion = label; }
  }
  const groups = new Map();
  for (const [index, row] of rows.entries()) {
    if (!isCurrentReading(row) || !qualifiedCanonicalSource(row)) continue;
    for (const context of canonicalContexts(row)) {
      const key = [context.key, canonicalService(row), row.service_hour || '', row.slot_type || '', row.canonical_mt_ref || '', row.canonical_lxx_ref || '', row.reading_name || ''].join('|');
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push({ index, context });
    }
  }
  const rank = row => row.source_family === 'coptic_reader' && row.source_kind === 'coptic_reader_fixture' ? -1 : priority(row);
  for (const [key, members] of groups) {
    if (members.length < 2) continue;
    members.sort((a, b) => rank(rows[a.index]) - rank(rows[b.index]) || a.index - b.index);
    const preferred = rows[members[0].index];
    for (const member of members.slice(1)) {
      const lower = rows[member.index];
      if (!isCurrentReading(lower)) continue;
      // A repeated source reading in two prophecy ordinals is not an alias.
      if (lower.slot_type === 'prophecy' && lower.source_family === preferred.source_family && lower.slot_order !== preferred.slot_order) continue;
      excludeContext(member.index, preferred, member.context.raw, 'exact_canonical_appointment_alias');
    }
  }
  if (fingerprint(rows) !== policy.projection_output_sha256) {
    throw new Error(`Canonical occurrence output fingerprint drift: ${fingerprint(rows)}`);
  }
  return { rows, dispositions, sentinel_additions: sentinelAdditions.length };
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
  const removalEffectiveVersionBaseline = await loadRemovalEffectiveVersionBaseline();
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
  const projected = suppressLowerPriorityPassageVariants(disambiguated.rows, removalEffectiveVersionBaseline);
  const policy = JSON.parse(await readFile(path.join(REPO_ROOT, 'sources/canonical-occurrence-policy.json'), 'utf8'));
  for (const [file, expected] of Object.entries(policy.source_fingerprints)) {
    const actual = createHash('sha256').update(await readFile(path.join(REPO_ROOT, file))).digest('hex');
    if (actual !== expected) throw new Error(`Canonical occurrence source fingerprint drift: ${file}`);
  }
  const canonical = canonicalizeOccurrences(projected.rows, policy);
  await writeFile(OCCASION_DEST, `${canonical.rows.map((row) => JSON.stringify(row)).join('\n')}\n`, 'utf8');
  return {
    rows: canonical.rows,
    activeRows: canonical.rows.filter(isCurrentReading),
    source_rows: parsedRows.length,
    output_rows: canonical.rows.length,
    active_rows: canonical.rows.filter(row => !isProjectionRemovedRow(row)).length,
    canonical_occurrence_projection: {
      policy: 'sources/canonical-occurrence-policy.json',
      disposition_count: canonical.dispositions.length,
      sentinel_additions: canonical.sentinel_additions,
      dispositions_by_reason: Object.fromEntries([...new Set(canonical.dispositions.map(item => item.reason))].map(reason => [reason, canonical.dispositions.filter(item => item.reason === reason).length])),
    },
    removed_rows_included: canonical.rows.filter(isProjectionRemovedRow).length,
    lower_priority_passage_variants_suppressed: projected.suppressions.length,
    lower_priority_passage_variants_retained_as_removed: projected.suppressions.length,
    removal_effective_version_baseline: {
      source_version: removalEffectiveVersionBaseline.source_version,
      entry_count: removalEffectiveVersionBaseline.entry_count,
      distinct_identity_key_count: removalEffectiveVersionBaseline.distinct_identity_key_count,
      duplicate_identity_key_count: removalEffectiveVersionBaseline.duplicate_identity_key_count,
    },
    removal_effective_version_baseline_miss_count: projected.baseline_miss_count,
    weekday_specific_contexts_disambiguated: disambiguated.disambiguated,
    legacy_month_spellings_normalized: ['Kiak -> Kiahk', 'Baba -> Babah'],
    suppressed_examples: projected.suppressions.slice(0, 20),
  };
}

const PASCHA_DAY_OFFSETS = new Map([
  ['Hosanna Sunday', -7],
  ['Monday', -6],
  ['Tuesday', -5],
  ['Wednesday', -4],
  ['Great Thursday', -3],
  ['Good Friday', -2],
  ['Bright Saturday', -1],
]);

const PASCHA_DAILY_OCCASIONS = new Map([
  ['Hosanna Sunday', new Set(['Hosanna Sunday'])],
  ['Monday', new Set(['Monday Eve', 'Monday'])],
  ['Tuesday', new Set(['Tuesday Eve', 'Tuesday'])],
  ['Wednesday', new Set(['Wednesday Eve', 'Wednesday', 'Wednesday of Holy Pascha'])],
  ['Great Thursday', new Set(['Great Thursday Eve', 'Great Thursday'])],
  ['Good Friday', new Set(['Good Friday'])],
  ['Bright Saturday', new Set(['Bright Saturday'])],
]);

function paschaDateForDay(year, dayName) {
  const pascha = new Date(`${julianPaschaGregorian(year)}T00:00:00Z`);
  const offset = PASCHA_DAY_OFFSETS.get(dayName);
  if (offset === undefined) throw new Error(`Unsupported Pascha day: ${dayName}`);
  pascha.setUTCDate(pascha.getUTCDate() + offset);
  return dateToIso(pascha);
}

function isBrightSaturdayServiceRow(row) {
  return row.source_family === 'bright_saturday' && String(row.calendar_keys || '').startsWith('Bright Saturday');
}

function isQualifiedCovenantRow(row) {
  const section = row.service_section;
  if (row.source_family !== 'coptic_reader_qualified_pascha_hour' || row.source_kind !== 'coptic_reader_qualified_pascha_hour'
    || row.service_hour !== section || row.occasion !== (section === 'Liturgy' ? 'the Covenant Thursday' : 'Great Thursday')
    || !['Liturgy', 'Liturgy of Blessing of the Water'].includes(section)) return false;
  return JSON.parse(row.source_disclosure || '[]').some(source =>
    String(source.source_locator || '').startsWith('sources/coptic-reader/covenant-thursday-qualified-2026-10-25/')
    && source.covenant_thursday_source?.length > 0
    && source.covenant_thursday_source.every(q => q.runtime_activation_approved === false
      && q.old_receipts_grant_activation === false && q.fresh_app_verification === false));
}

function rowsForPaschaDailyDate(projectedRows, dayName) {
  const occasions = PASCHA_DAILY_OCCASIONS.get(dayName) || new Set();
  return projectedRows.filter((row) => {
    if (!isCurrentReading(row)) return false;
    if (dayName === 'Great Thursday' && isQualifiedCovenantRow(row)) return true;
    if (dayName === 'Bright Saturday' && isBrightSaturdayServiceRow(row)) return true;
    const retainedWednesdayFixture = dayName === 'Wednesday'
      && row.occasion === 'Wednesday of Holy Pascha'
      && row.source_family === 'coptic_reader'
      && row.source_kind === 'coptic_reader_fixture';
    return (row.source_family === 'holy_pascha_curated_day_hour' || retainedWednesdayFixture || row.source_family === 'coptic_reader_qualified_pascha_hour')
      && occasions.has(String(row.occasion || ''));
  });
}

// Source authentication is performed by design before serialization. Requalify
// that hash-bound held contract here; friendly source names alone grant nothing.
function isQualifiedBrightComposite(row) {
  if (row.source_family !== 'bright_saturday' || row.source_kind !== 'bright_saturday_qualified_composite'
    || row.occasion !== 'Bright Saturday' || !['Matins', '6th Hour', 'Liturgy'].includes(row.service_section)
    || row.service_hour !== '' || row.slot !== 'Psalm' || row.current_status !== 'pending_psalm_equivalence_unresolved'
    || row.canonical_mt_ref !== '' || row.canonical_lxx_ref !== '' || row.spans_json !== '[]'
    || row.removed_marker || row.active === false) return false;
  const identities = {
    rid_d58dc513121900158fc9: ['Matins', '28', '2'],
    rid_16e3ff8ccefe525d98e0: ['Matins', '28', '3'],
    rid_969f73205a3c4d8ceef6: ['6th Hour', '32', '2'],
    rid_5be18395526b0ff8b009: ['Liturgy', '39', '2'],
  };
  const expected = identities[row.identity_key];
  if (!expected || expected.join('|') !== [row.service_section, row.source_order, row.source_token_order].join('|')) return false;
  const ordinal = value => (typeof value === 'string' && /^[1-9]\d*$/.test(value))
    || (typeof value === 'number' && Number.isSafeInteger(value) && value > 0);
  if (!ordinal(row.source_order) || !ordinal(row.source_token_order)) return false;
  try {
    const sources = JSON.parse(row.source_disclosure || '[]');
    return Array.isArray(sources) && sources.some(source => source.source_family === row.source_family
      && source.source_kind === row.source_kind && Array.isArray(source.bright_composite_source)
      && source.bright_composite_source.length === 1 && source.bright_composite_source.every(q =>
        q.contract_sha256 === '6365f62b235fcf3b0b41a7d96d11096de01a7cf93107c87943155a5aea5bc5a0'
        && q.contract_path === 'sources/user-corrections/bright-saturday-composites-2026-10-25.json'
        && q.fresh_app_verification === false && q.canonical_coordinate_status === 'held_no_exact_cross_edition_counterpart'
        && q.canonical_mt_ref === '' && q.canonical_lxx_ref === '' && q.service_section === row.service_section
        && JSON.stringify(JSON.parse(row.provenance || 'null')) === JSON.stringify(q)
        && String(row.source_order) === q.source_order && String(row.source_token_order) === q.source_token_order
        && row.source_locator === source.source_locator && row.source_locator.startsWith(q.source_path + ':')
        && row.source_locator.includes('sha256=' + q.document.sha256)
        && row.source_locator.includes('body_sha256=' + q.document.body_sha256)
        && row.display_ref === q.source_selection_ref + ' (Reader selection; canonical coordinates held)'));
  } catch { return false; }
}

// Design authenticates this retained Wednesday appointment. Recover its typed
// token ordinal from the disclosure, not array position or numeric Psalm order.
function qualifiedJonahFragmentOrder(row, date) {
  if (!['2026-02-04', '2027-02-24', '2028-02-09'].includes(date)
    || row.source_family !== 'jonah_fast_source_qualified' || row.source_kind !== 'jonah_fast_date_supplement'
    || row.occasion !== "Wednesday of Ninevah's Fast" || !['Matins', 'Liturgy'].includes(row.service_section)
    || row.service_hour !== '' || row.slot !== 'Psalm' || !isCurrentReading(row)) return null;
  const positiveInteger = value => (typeof value === 'number' && Number.isSafeInteger(value) && value > 0)
    || (typeof value === 'string' && /^[1-9]\d*(?![\s\S])/.test(value) && Number.isSafeInteger(Number(value)));
  const matins = row.service_section === 'Matins';
  const sourceOrder = matins ? 2 : 7;
  const printed = matins ? 'Psalms 102:12, 11' : 'Psalms 31:1, 6';
  const sourcePath = `sources/coptic-reader/jonah-qualified-2026-10-25/2026-02-04/${row.service_section}/Psalm_and_Gospel.txt`;
  const documentHash = matins ? '1cdebbea8e1fc17c6c0d8e7f045a4a3d75309af44b8e76adc8e1d5c59e99bb93' : '283c31bbaef53f2cf5d35f0a030258c2cfc99e999631e96dd676bc7d2d1ba047';
  const bodyHash = matins ? 'b8c7623bd9ed89d16bd95fdfa0173034e4fafe05aa66d32373b33acddc54ede8' : 'e2f7536930eef20fbef970ffb9216cb40afba794afda5dfb1f2f443049637a07';
  const locator = `${sourcePath}:line 7; sha256=${documentHash}; body_sha256=${bodyHash}; selected=2026-02-04; printed_ref=${printed}`;
  if (row.source_locator !== locator) return null;
  try {
    const sources = JSON.parse(row.source_disclosure || '[]');
    if (!Array.isArray(sources)) return null;
    const matches = sources.filter(s => s.source_family === row.source_family && s.source_kind === row.source_kind
      && s.source_locator === locator).flatMap(s => Array.isArray(s.consumer_source_transport) ? s.consumer_source_transport : [])
      .filter(t => t.jonah_source?.gregorian_date === date);
    if (matches.length !== 1) return null;
    const {jonah_source: q, token_order: token} = matches[0];
    if (!positiveInteger(q.source_order) || q.source_order !== sourceOrder || !positiveInteger(token) || ![1, 2].includes(token)
      || q.source_family !== row.source_family || q.source_kind !== row.source_kind
      || q.day_title !== row.occasion || q.service_section !== row.service_section || q.reading_type !== row.slot
      || q.jonah_contract_sha256 !== 'e0175a66f98ab0c8dc3c5bda2917e82e5a490fe97cf00c59b732af7475225726'
      || q.runtime_activation_approved !== true || q.source_verified_date !== '2026-02-04'
      || q.source_evidence !== sourcePath || q.source_heading_line !== 7
      || q.source_full_document_sha256 !== documentHash || q.jonah_source_body_sha256 !== bodyHash
      || q.printed_ref !== printed || (matins && q.normalized_ref !== 'Ps 103:13 & Ps 103:12')
      || row.canonical_mt_ref !== (matins ? ['Ps 103:13', 'Ps 103:12'] : ['Ps 32:1', 'Ps 32:5'])[token - 1]
      || row.canonical_lxx_ref !== (matins ? ['Ps 102:13', 'Ps 102:12'] : ['Ps 31:1', 'Ps 31:5'])[token - 1]) return null;
    for (const [field, expected] of [['source_order', sourceOrder], ['source_token_order', token]]) {
      if (Object.hasOwn(row, field) && (!positiveInteger(row[field]) || Number(row[field]) !== expected)) return null;
    }
    return {source_order: sourceOrder, source_token_order: token};
  } catch { return null; }
}

function dailyRowFromReverse(row, dayName, date = '') {
  const occasion = isBrightSaturdayServiceRow(row) ? 'Bright Saturday' : row.occasion;
  const jonahOrder = qualifiedJonahFragmentOrder(row, date);
  const serviceHour = isQualifiedBrightComposite(row) || jonahOrder ? '' : row.service_hour || row.service_section || '';
  return normalizeObjectStrings({
    occasion,
    service_section: row.service_section || '',
    service_hour: serviceHour,
    slot: row.slot || '',
    display_ref: row.display_ref || '',
    identity_key: row.identity_key || '',
    reading_type: row.reading_type || 'scripture',
    ...(row.reading_name ? { reading_name: row.reading_name } : {}),
    slot_type: row.slot_type || slotType(row.slot),
    slot_order: existingNumericOrder(row.slot_order),
    service_order: existingNumericOrder(row.service_order) ?? serviceOrder(serviceHour || row.service_section),
    source_group_key: row.source_group_key || [row.source_kind || '', row.source_row_id || '', row.source_occasion || row.occasion || '', serviceHour, row.slot || ''].join('|'),
    current_status: row.current_status || '',
    active: row.active,
    status: row.status || '',
    superseded_by_ref: row.superseded_by_ref || '',
    superseded_reason: row.superseded_reason || '',
    removed_marker: row.removed_marker || '',
    canonical_mt_ref: row.canonical_mt_ref || '',
    canonical_lxx_ref: row.canonical_lxx_ref || '',
    spans_json: row.spans_json || '[]',
    source_family: row.source_family || '',
    source_kind: row.source_kind || '',
    source_locator: row.source_locator || '',
    source_disclosure: row.source_disclosure || '[]',
    source_disclosure_count: row.source_disclosure_count || '0',
    ...(isQualifiedCovenantRow(row) || isQualifiedBrightComposite(row) ? {source_order: row.source_order, source_token_order: row.source_token_order} : {}),
    ...(jonahOrder || {}),
    ...(isQualifiedBrightComposite(row) ? {provenance: row.provenance} : {}),
    hour_theme: row.hour_theme || '',
    structural_day: dayName,
  });
}

function canonicalBrightSaturdaySlot(slot) {
  const key = String(slot || '').trim().toLowerCase();
  return BRIGHT_SATURDAY_SLOT_ALIASES.get(key) || key;
}

function brightSaturdayStatusRank(row) {
  return row.current_status === 'current_public_or_local_reference' ? 0 : 1;
}

function preferBrightSaturdayRow(current, candidate) {
  const currentExplicit = BRIGHT_SATURDAY_SLOT_ALIASES.has(String(current.slot || '').trim().toLowerCase()) ? 0 : 1;
  const candidateExplicit = BRIGHT_SATURDAY_SLOT_ALIASES.has(String(candidate.slot || '').trim().toLowerCase()) ? 0 : 1;
  if (candidateExplicit !== currentExplicit) return candidateExplicit > currentExplicit ? candidate : current;
  if (brightSaturdayStatusRank(candidate) !== brightSaturdayStatusRank(current)) {
    return brightSaturdayStatusRank(candidate) < brightSaturdayStatusRank(current) ? candidate : current;
  }
  return current;
}

function mergeSourceDisclosure(winner, other) {
  const parse = (value) => {
    try {
      const parsed = JSON.parse(value || '[]');
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  };
  const seen = new Set();
  const merged = [];
  for (const item of [...parse(winner.source_disclosure), ...parse(other.source_disclosure)]) {
    const key = JSON.stringify(item);
    if (seen.has(key)) continue;
    seen.add(key);
    merged.push(item);
  }
  return {
    ...winner,
    source_disclosure: JSON.stringify(merged),
    source_disclosure_count: String(merged.length),
  };
}

const BRIGHT_SATURDAY_SLOT_ALIASES = new Map([
  ['pauline', 'pauline epistle'],
  ['catholic', 'catholic epistle'],
  ['acts', 'praxis'],
  ['prayer of jeremiah', 'praise of the prophet jeremiah'],
]);

function dedupeDailyRows(rows) {
  const seen = new Map();
  const out = [];
  const appointmentKey = row => [row.occasion, row.service_section, row.service_hour, row.slot, row.identity_key].join('|');
  const covenantKeys = new Set(rows.filter(isQualifiedCovenantRow).map(appointmentKey));
  for (const row of rows) {
    // These two source labels describe the same Wednesday Day appointment.
    // Keep Eve separate and retain the exact current Reader row when available;
    // the other attestation remains unchanged in the reverse provenance index.
    const wednesdayDay = row.structural_day === 'Wednesday'
      && ['Wednesday', 'Wednesday of Holy Pascha'].includes(row.occasion);
    const brightSaturday = row.occasion === 'Bright Saturday' || row.structural_day === 'Bright Saturday';
    const slotKey = brightSaturday ? canonicalBrightSaturdaySlot(row.slot) : (row.slot || '');
    const covenantJoin = covenantKeys.has(appointmentKey(row));
    const key = covenantJoin ? appointmentKey(row) : wednesdayDay
      ? ['Wednesday Day', row.service_section || '', row.service_hour || '', row.slot_type || '', row.slot_order ?? '', row.identity_key || '', row.display_ref || ''].join('|')
      : [row.occasion || '', row.service_section || '', row.service_hour || '', slotKey, row.identity_key || '', row.display_ref || ''].join('|');
    if (seen.has(key)) {
      const index = seen.get(key);
      if (covenantJoin) {
        const winner = isQualifiedCovenantRow(out[index]) ? out[index] : row;
        out[index] = mergeSourceDisclosure(winner, winner === row ? out[index] : row);
      } else if (wednesdayDay && row.source_family === 'coptic_reader' && row.source_kind === 'coptic_reader_fixture') {
        out[index] = row;
      } else if (brightSaturday) {
        const winner = preferBrightSaturdayRow(out[index], row);
        const loser = winner === out[index] ? row : out[index];
        out[index] = mergeSourceDisclosure(winner, loser);
      }
      continue;
    }
    seen.set(key, out.length);
    out.push(row);
  }
  return out;
}

function addMissingStructuralDailyRows(sorted, year, projectedRows) {
  const additions = [];
  for (const dayName of PASCHA_DAILY_OCCASIONS.keys()) {
    const date = paschaDateForDay(year, dayName);
    const existingRows = sorted[date] || [];
    const annunciationCollision = sorted[date]?.some((row) => /annunciation/i.test(String(row.occasion || row.day_title || '')));
    const rows = rowsForPaschaDailyDate(projectedRows, dayName).map((row) => dailyRowFromReverse(row, dayName));
    if (!rows.length) continue;
    if (annunciationCollision) {
      const sourceRule = 'UK Midlands Katameros Days p.22 rule 13: Annunciation yields during the non-repeatable Lord events window';
      sorted[date] = sortDailyReadings(dedupeDailyRows(rows.map((row) => ({ ...row, correction_reason: sourceRule }))), date);
    } else {
      // A nonempty date may still omit structural hours or one source family.
      // Hosanna hours supplement, rather than replace, ordinary Palm services.
      sorted[date] = sortDailyReadings(dedupeDailyRows([...existingRows, ...rows]), date);
    }
    additions.push({ date, day: dayName, reading_count: sorted[date].length });
  }
  return additions;
}

function sortDailyReadings(readings, date = '') {
  const boundarySource = 'sources/coptic-reader/last-friday-2028-04-07-2026-10-07/verified-table.json';
  // This authenticated whole-table replacement has one supplied sequence,
  // not independent prophecy and Psalm/Gospel slot-order families. Keep this
  // projection confined to the captured collision; it grants no recurrence.
  const completeBoundary = date === '2028-04-07' && readings.length === 11 && readings.every((reading, index) =>
    isCurrentReading(reading)
    && reading.source_kind === 'copticchurch_date'
    && reading.source_family === 'coptic_reader_verified_calendar_boundary'
    && reading.source_file === boundarySource
    && reading.source_row_id === `boundary:${boundarySource}:2028-04-07:${index + 1}`
    && reading.occasion === 'Friday of the seventh week of Great Lent'
    && !reading.service_hour
    && reading.service_section === (index < 6 ? 'Matins' : 'Liturgy'));
  if (completeBoundary) {
    return readings.map((reading, index) => ({
      ...reading,
      reading_order: index + 1,
      service_order: serviceOrder(reading.service_section),
      slot_type: reading.slot_type || slotType(reading.slot),
      slot_order: index < 6 ? index + 1 : index - 5,
    }));
  }
  const enriched = readings.filter(isCurrentReading).map((reading) => ({
    ...reading,
    service_order: existingNumericOrder(reading.service_order) ?? serviceOrder(reading.service_section),
    slot_type: reading.slot_type || slotType(reading.slot),
    slot_order: existingNumericOrder(reading.slot_order) ?? slotOrder(reading.slot, reading.service_section),
  }));
  // The cached Palm Liturgy h5 prints this complete appointment, including
  // the interspersed Psalm. This is not a general Gospel/book ordering rule.
  const palmRefs = ['Matt 21:1-17', 'Mark 11:1-11', 'Lk 19:29-48', 'Jn 12:12-19'];
  const palmRow = row => row.source_kind === 'copticchurch_date'
    && row.source_family === 'ordinary_date_resolved' && row.occasion === 'Palm Sunday'
    && row.service_section === 'Liturgy' && !row.service_hour && row.slot_type === 'gospel';
  const palmRows = enriched.filter(palmRow);
  const year = Number(date.slice(0, 4));
  const completePalm = [2026, 2027, 2028].includes(year)
    && date === paschaDateForDay(year, 'Hosanna Sunday') && palmRows.length === 4
    && palmRefs.every(ref => palmRows.filter(row => row.canonical_mt_ref === ref).length === 1);
  const brightDate = !date || ([2026, 2027, 2028].includes(year)
    && date === paschaDateForDay(year, 'Bright Saturday'));
  const brightPraises = row => brightDate && row.source_family === 'bright_saturday'
    && row.occasion === 'Bright Saturday' && row.service_section === 'Midnight Praises'
    && row.service_hour === 'Midnight Praises';
  const brightCsvRow = row => brightPraises(row) && row.source_kind === 'bright_saturday_service_order'
    ? /^out\/data\/bright_saturday_service_order\.csv:row ([1-9]\d*);/.exec(row.source_locator || '') : null;
  const openingPsalm = row => brightPraises(row) && row.source_kind === 'psalmody_source_supplement'
    && row.slot === 'Psalm151' && row.canonical_lxx_ref === 'Ps 151' && !row.canonical_mt_ref
    && String(row.source_locator || '').startsWith('sources/coptic-reader/psalmody-qualified-2026-10-25/bright-saturday-midnight-praises.full.txt:');
  const brightPhysicalRow = row => brightDate && row.source_family === 'bright_saturday'
    && row.occasion === 'Bright Saturday'
    && (!row.service_hour || row.service_hour === row.service_section)
    && ['Matins', '3rd Hour', '6th Hour', '9th Hour', 'Liturgy'].includes(row.service_section)
    && row.source_kind === 'bright_saturday_service_order'
    ? /^out\/data\/bright_saturday_service_order\.csv:row ([1-9]\d*);/.exec(row.source_locator || '') : null;
  const brightContext = row => brightDate && row.occasion === 'Bright Saturday'
    && (brightPhysicalRow(row) || isQualifiedBrightComposite(row));
  const stagedFamilies = new Set(['ordinary_date_resolved', 'katameros_cycle', 'coptic_reader_verified_supplement',
    'holy_pascha_curated_day_hour', 'coptic_reader', 'coptic_reader_qualified_pascha_hour', 'bright_saturday', 'jonah_fast_source_qualified']);
  const stages = { prophecy: 0, pauline: 1, catholicon: 2, praxis: 3, psalm: 4, gospel: 5 };
  const orderKey = row => {
    const csvRow = brightCsvRow(row);
    const opening = openingPsalm(row);
    const praises = csvRow || opening;
    const jonahOrder = qualifiedJonahFragmentOrder(row, date);
    const role = /^Prophecy(?:\b|$)/i.test(row.slot || '') ? 'prophecy' : row.slot_type;
    const stage = stagedFamilies.has(row.source_family) && row.service_section !== 'Midnight Praises'
      ? (stages[role] ?? 99) : 99;
    return [
      praises ? 0 : row.service_order,
      praises ? 0 : serviceOrder(row.service_hour || row.service_section),
      row.service_section || '', brightContext(row) ? row.service_section : row.service_hour || '', row.occasion || '',
      stage, opening ? 0 : 1, csvRow ? Number(csvRow[1]) : 0,
      completePalm && palmRow(row) ? palmRefs.indexOf(row.canonical_mt_ref) : 0,
      brightPhysicalRow(row) ? Number(brightPhysicalRow(row)[1]) : brightContext(row) ? Number(row.source_order) : 0,
      brightContext(row) ? Number(row.source_token_order || 0) : 0,
      row.slot_order,
      isQualifiedCovenantRow(row) ? Number(row.source_token_order) : 0,
      jonahOrder?.source_order || 0,
      jonahOrder?.source_token_order || 0,
    ];
  };
  // Independent per-row keys make this a total order (no pair-dependent stage
  // comparisons). Supplied fragment order is the final, stable tie breaker.
  const keys = new Map(enriched.map(row => [row, orderKey(row)]));
  enriched.sort((a, b) => {
    const ka = keys.get(a);
    const kb = keys.get(b);
    for (let i = 0; i < ka.length; i += 1) {
      if (ka[i] < kb[i]) return -1;
      if (ka[i] > kb[i]) return 1;
    }
    return 0;
  });
  return enriched.map((reading, index) => {
    const { reading_order: _previousOrder, ...fields } = reading;
    return { reading_order: index + 1, ...fields };
  });
}

function buildStructuralDateResolver(dailyInfos) {
  const missingDatesByYear = {};
  const structuralRowsByYear = {};
  for (const info of dailyInfos) {
    missingDatesByYear[String(info.year)] = info.missing_dates.map(classifyStructuralMissingDate);
    structuralRowsByYear[String(info.year)] = info.structural_daily_additions || [];
  }
  return {
    schema: 'julian_pascha_structural_daily_v2',
    coverage: 'complete_daily_with_date_resolved_structural_rows',
    exported_function: 'classifyDate(date)',
    date_key_format: 'YYYY-MM-DD',
    shipped_years: SHIPPED_YEARS,
    missing_dates_by_year: missingDatesByYear,
    structural_daily_additions_by_year: structuralRowsByYear,
    contract: 'All shipped civil dates have daily JSON keys. Holy Week and Bright Saturday structural rows fill missing public-cache dates; the verified Annunciation collision is replaced under the documented exception rule rather than unioned.',
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

async function readDailyInfo(year, projectedRows) {
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
    sorted[date] = sortDailyReadings(readings.map((reading) => normalizeObjectStrings(reading)), date);
  }

  const structuralDailyAdditions = addMissingStructuralDailyRows(sorted, year, projectedRows);

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
    structural_daily_additions: structuralDailyAdditions,
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

function isCurrentReading(row) {
  if (!row || typeof row !== 'object' || Array.isArray(row) || row.active === false || row.status === 'removed') return false;
  if (/^(superseded\b|removed\b|removed_|omitted\b)|\bremoved in\b|\bsource omitted\b/i.test(String(row.removed_marker || '').trim())) return false;
  const status = String(row.current_status || row.status || '').trim().toLowerCase();
  if (!status) return true;
  if (status === 'removed' || status.startsWith('superseded') || status === 'historical_candidate_removed' || status === 'historical_witness') return false;
  if (['current', 'current_public_or_local_reference', 'current_working_source_not_coptic_reader_checked', 'current_confirmed_coptic_reader', 'current_confirmed_by_fixture_equivalence', 'pending_psalm_equivalence_unresolved'].includes(status)) return true;
  throw new RangeError('Unknown explicit reading status: ' + status);
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
  const month = Number(date.slice(5, 7));
  const day = Number(date.slice(8, 10));
  if (year === 0) throw new RangeError('date must use Gregorian year 0001 or later.');
  const parsed = new Date(0);
  parsed.setUTCHours(0, 0, 0, 0);
  parsed.setUTCFullYear(year, month - 1, day);
  if (parsed.getUTCFullYear() !== year || parsed.getUTCMonth() + 1 !== month || parsed.getUTCDate() !== day) {
    throw new RangeError('date must be a real Gregorian calendar date.');
  }
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

function isRemovedReading(row) {
  return Boolean(row && (row.active === false || String(row.status || '').toLowerCase() === 'removed'));
}

function isActiveReading(row) {
  return !isRemovedReading(row);
}

${isCurrentReading.toString()}

module.exports = {
  occasionIndexPath,
  dailyDir,
  dailyYearPath,
  classifyDate,
  isRemovedReading,
  isActiveReading,
  isCurrentReading,
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
- \`index.js\`: CommonJS exports for stable resolved paths, package metadata, and date classification.
- \`meta.json\`: package provenance, schema version, counts, shipped years, structural daily materialization summary, and schema notes. In \`daily_files\`, \`rows\` is retained as the legacy date-count field; use \`date_count\` and \`reading_count\` for explicit counts.

## Usage

\`\`\`js
const lectionaryData = require('${PACKAGE_NAME}');

console.log(lectionaryData.occasionIndexPath);
console.log(lectionaryData.dailyYearPath(2026));
console.log(lectionaryData.shippedYears);
console.log(lectionaryData.meta.source_repo_commit);
console.log(lectionaryData.classifyDate('2026-04-10'));
console.log(lectionaryData.isCurrentReading({ display_ref: 'Jn 1:1-17' }));
\`\`\`

## Exports

- \`occasionIndexPath\`: absolute path to \`data/reverse_lectionary_index.jsonl\`.
- \`dailyDir\`: absolute path to \`data/daily\`.
- \`dailyYearPath(year)\`: returns the absolute path for a shipped daily lectionary JSON file.
- \`classifyDate(date)\`: classifies a shipped ISO date as present in daily JSON or as a documented structural-only Holy Week/Bright Saturday gap.
- \`isRemovedReading(row)\`: returns true for rows marked \`active: false\` or \`status: "removed"\`.
- \`isActiveReading(row)\`: backwards-compatible convenience negation of \`isRemovedReading(row)\`; it does not exclude every historical or superseded state.
- \`isCurrentReading(row)\`: returns true only for unmarked legacy rows or supported current-status values; removal markers, superseded rows, and historical witnesses are false.
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

Rows that were removed from active lookup by source-priority projection include additional fields:

- \`active: false\`
- \`status: "removed"\`
- \`removal_reason\`
- \`removal_context_key\`
- \`preferred_source_family\`
- \`preferred_display_ref\`
- \`preferred_identity_key\`
- \`consumer_note\`
- \`retained_for: "provenance_only"\`

Default consumers should filter with \`isCurrentReading(row)\`. \`isActiveReading(row)\` retains its narrower backwards-compatible meaning and is appropriate only when historical/source-marked rows are intentionally included.

### Dual-numbering display references

\`display_ref\` is the human-facing reference. Psalm references use Masoretic Text numbering as the primary display form with Septuagint numbering inline when available. Consumers that need machine normalization should use \`canonical_mt_ref\`, \`canonical_lxx_ref\`, and \`spans_json\` instead of parsing \`display_ref\`.

### Removed markers

\`removed_marker\` carries source-derived removal or omission markers where they exist. Consumers should preserve this value and should not treat marked readings as active without checking the field.

## Daily file schema

Each daily file is a JSON object keyed by ISO date, for example \`2026-04-12\`. Each value is an array of readings for that date.

Shipped years: ${meta.shipped_years.join(', ')}.

Each daily reading includes a unique \`reading_order\` within that date. The package writes daily arrays sorted by \`reading_order\`, using deterministic service and slot ordering: Vespers, Matins, then Liturgy; within those services, Psalm/Gospel for Vespers and Matins, and Pauline, Catholic, Acts, Psalm, Gospel for Liturgy. \`slot_order\` may repeat for split Psalm verses or readings that share one liturgical slot; use \`reading_order\` when a unique date-local order is required.

In \`meta.daily_files\`, \`rows\` is retained as a legacy alias for \`date_count\`. Use \`date_count\` for the number of ISO date keys and \`reading_count\` for the total number of readings across those dates.

## Structural Holy Week / Bright Saturday daily rows

The package date-resolves Holy Week and Bright Saturday structural rows into the shipped daily files when the public copticchurch.net daily cache does not provide rows for that civil date, and replaces a verified Annunciation collision under the documented exception rule. As a result, every shipped civil date in ${meta.shipped_years.join(', ')} has a daily JSON key.

\`meta.structural_date_resolver.structural_daily_additions_by_year\` lists the civil dates filled from structural Pascha/Bright Saturday rows. \`classifyDate(date)\` returns \`hasDailyReadings: true\` for every shipped civil date that has a daily key.

## Source-priority projection

The package projects the raw reverse index into a consumer-safe runtime index. When a copticchurch.net date-resolved row and a lower-priority local cycle row overlap the same normalized consumer occasion, service, service hour, and slot type but disagree on the passage span, the lower-priority variant is retained as inactive provenance rather than used as an active lookup row.

Inactive projection rows are marked with \`active: false\`, \`status: "removed"\`, \`removed_marker: "removed_by_source_priority_projection"\`, a \`consumer_note\`, and preferred-reading fields such as \`preferred_source_family\`, \`preferred_display_ref\`, and \`preferred_identity_key\`. Use \`isCurrentReading(row)\` for default current-reading lookups.

For fixed-date rows with a Sunday-specific counterpart, generic rows are disambiguated as non-Sunday contexts rather than silently duplicated.

Projection counts and examples are recorded in \`meta.projection_rules\`.

## Span and Psalm numbering contract

\`spans_json\` contains machine-readable canonical spans when the reading can be represented as biblical book/chapter/verse ranges. It may be an empty array for named non-standard readings supplied by Coptic Reader fixtures, such as \`Memoirs of Job\`; in that case use \`reading_type\`, \`reading_name\`, and \`display_ref\`.

Psalm \`display_ref\` values may include inline dual numbering, for example \`Ps 105:14-15 (LXX Ps 104:14-15)\`. Consumers should not parse \`display_ref\` for machine matching. Use \`canonical_mt_ref\`, \`canonical_lxx_ref\`, and \`spans_json\`.

## Known limitation

Structural-only occasions outside the shipped civil-year daily scope, such as some special services, remain available through \`reverse_lectionary_index.jsonl\`. Holy Week and Bright Saturday rows for shipped civil dates are included in daily files.

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
        active: 'Optional. False only for rows retained as inactive provenance after source-priority projection. Missing means active for backwards compatibility.',
        status: 'Optional. Set to removed for rows retained as inactive provenance after source-priority projection.',
        removal_reason: 'Optional. Reason an inactive provenance row is excluded from active lookup.',
        removal_context_key: 'Optional. Normalized consumer context/service/hour/slot key that triggered source-priority removal.',
        preferred_source_family: 'Optional. Source family of the active preferred row for an inactive provenance row.',
        preferred_display_ref: 'Optional. Display reference of the active preferred row for an inactive provenance row.',
        preferred_identity_key: 'Optional. Identity key of the active preferred row for an inactive provenance row.',
        consumer_note: 'Optional. User-facing explanation for inactive provenance rows.',
        retained_for: 'Optional. Set to provenance_only for inactive rows kept for auditability.',
      },
      daily_file_shape: 'Each daily JSON file maps ISO dates to an array of readings sorted by reading_order. Each reading includes reading_order, service_order, slot_type, and slot_order; slot_order may repeat within split Psalm/reading fragments, while reading_order is unique per date.',
      structural_date_resolver: 'meta.structural_date_resolver documents Holy Week/Bright Saturday structural rows that were date-resolved into shipped daily files. All shipped civil dates are expected to have daily JSON keys.',
      psalm_dual_numbering: 'Psalm display_ref may include inline LXX numbering in parentheses. Use canonical_mt_ref, canonical_lxx_ref, and spans_json for machine matching.',
      canonicalization_notes: 'canonicalization_note values are source/provenance hints, not date or service resolvers.',
      multi_source_family: 'The same identity_key may appear across multiple source_family values and distinct occasions; this is expected attestation breadth, not a duplicate by itself.',
      source_priority_projection: 'When current copticchurch.net date-resolved rows overlap lower-priority cycle rows for the same normalized consumer context/service/hour/slot but disagree on passage span, the npm package marks the lower-priority variant as active:false/status:removed and retains it for provenance. Active consumers should filter with isActiveReading(row). See meta.projection_rules for counts and examples.',
      coptic_month_spellings: 'Runtime package labels normalize Kiak to Kiahk and Baba to Babah.',
      weekday_specific_disambiguation: 'When a Sunday-specific fixed-date row has a generic sibling with the same reading identity, the generic sibling is labeled as a non-Sunday context to avoid consumer duplicate grouping.',
      known_limitation: 'Structural-only occasions outside the shipped civil-year daily scope remain available through reverse_lectionary_index.jsonl. Holy Week and Bright Saturday rows for shipped civil dates are date-resolved into daily files.',
    },
  };
}

async function main() {
  const sourceRepoCommit = readGitHead();
  const sourceTreeDirty = readGitDirty();

  // The 1.3 release owns the catalog/calendar runtime. This readings builder
  // must not replace it with the legacy 1.2 templates or delete its assets.
  const existingPackage = JSON.parse(await readFile(path.join(PACKAGE_DIR, 'package.json'), 'utf8'));
  const existingMeta = JSON.parse(await readFile(path.join(PACKAGE_DIR, 'meta.json'), 'utf8'));
  if (existingPackage.name !== PACKAGE_NAME || !existingMeta.synaxarium || !['1.3.0', '1.3.1', '1.3.2', '1.3.5', VERSION].includes(existingPackage.version)) {
    throw new Error('Current 1.3 catalog/calendar package is a prerequisite; refusing destructive legacy rebuild.');
  }
  for (const file of ['index.js', 'calendar.js', 'README.md', 'LICENSE', 'data/synaxarium/synaxarium.json']) {
    await stat(path.join(PACKAGE_DIR, file));
  }
  await mkdir(DAILY_DIR, { recursive: true });

  const reverseProjection = await projectReverseIndex();
  const { rows: _projectedRows, activeRows: activeProjectedRows, ...projectionRules } = reverseProjection;
  const occasionIndexRows = projectionRules.output_rows;
  const dailyInfos = [];

  for (const year of SHIPPED_YEARS) {
    dailyInfos.push(await readDailyInfo(year, activeProjectedRows));
  }
  const dailyFiles = dailyInfos.map(({ missing_dates, structural_daily_additions, pascha_date, ...info }) => info);
  const structuralDateResolver = buildStructuralDateResolver(dailyInfos);

  const freshMeta = metaJson(sourceRepoCommit, sourceTreeDirty, occasionIndexRows, dailyFiles, structuralDateResolver, projectionRules);
  const meta = { ...existingMeta, ...freshMeta, schema_notes: { ...existingMeta.schema_notes, ...freshMeta.schema_notes } };

  await writeFile(path.join(PACKAGE_DIR, 'package.json'), `${JSON.stringify({ ...existingPackage, version: VERSION }, null, 2)}\n`, 'utf8');
  await writeFile(path.join(PACKAGE_DIR, 'meta.json'), `${JSON.stringify(meta, null, 2)}\n`, 'utf8');

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
