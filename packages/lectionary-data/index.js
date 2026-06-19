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

module.exports = {
  occasionIndexPath,
  dailyDir,
  dailyYearPath,
  classifyDate,
  isRemovedReading,
  isActiveReading,
  structuralDateResolver,
  shippedYears,
  meta,
};
