'use strict';

const frozenMonthSlugs = Object.freeze([
  'tout', 'baba', 'hatour', 'kiahk', 'toba', 'amshir', 'baramhat',
  'baramouda', 'bashans', 'paona', 'abib', 'mesra', 'nasie',
]);

// Proleptic Gregorian civil date to Coptic date, using integer Julian day numbers.
// Coptic epoch: Julian 284-08-29, JDN 1825030. Years congruent to 3 mod 4 are leap.
// No clock, local timezone, shipped-year lookup or reading labels are consulted.
function gregorianToCoptic(year, month, day) {
  if (![year, month, day].every(Number.isInteger)) {
    throw new TypeError('Gregorian date components must be integers.');
  }
  if (year < 1 || year > 9999 || month < 1 || month > 12 || day < 1 || day > 31) {
    throw new RangeError('Use a real Gregorian date in years 0001 through 9999.');
  }
  const date = new Date(0);
  date.setUTCHours(0, 0, 0, 0);
  date.setUTCFullYear(year, month - 1, day);
  if (date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) {
    throw new RangeError('Use a real Gregorian date.');
  }
  const jdn = date.getTime() / 86400000 + 2440588;
  const copticYear = Math.floor((4 * (jdn - 1825030) + 1463) / 1461);
  const yearStart = 1825030 + 365 * (copticYear - 1) + Math.floor(copticYear / 4);
  const dayOfYear = jdn - yearStart;
  return {
    year: copticYear,
    monthSlug: frozenMonthSlugs[Math.floor(dayOfYear / 30)],
    day: (dayOfYear % 30) + 1,
  };
}

module.exports = { gregorianToCoptic, frozenMonthSlugs };
