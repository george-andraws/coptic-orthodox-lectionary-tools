'use strict';

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
    throw new RangeError(`No lectionary daily file is shipped for year ${numericYear}.`);
  }
  return path.resolve(dailyDir, `lectionary-${numericYear}.json`);
}

function classifyDate(date) {
  if (typeof date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(date)) {
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

function isCurrentReading(row) {
  if (!row || typeof row !== 'object' || Array.isArray(row) || row.active === false || row.status === 'removed') return false;
  if (/^(superseded\b|removed\b|removed_|omitted\b)|\bremoved in\b|\bsource omitted\b/i.test(String(row.removed_marker || '').trim())) return false;
  const status = String(row.current_status || row.status || '').trim().toLowerCase();
  if (!status) return true;
  if (status === 'removed' || status.startsWith('superseded') || status === 'historical_candidate_removed' || status === 'historical_witness') return false;
  if (['current', 'current_public_or_local_reference', 'current_working_source_not_coptic_reader_checked', 'current_confirmed_coptic_reader', 'current_confirmed_by_fixture_equivalence', 'pending_psalm_equivalence_unresolved'].includes(status)) return true;
  throw new RangeError('Unknown explicit reading status: ' + status);
}

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
