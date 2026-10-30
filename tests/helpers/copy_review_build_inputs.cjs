'use strict';

const fs = require('node:fs');
const path = require('node:path');

// This fixture runs the real review pipeline, with its production source
// authentication intact. It does not enable a test-only activation mode.
module.exports = function copyReviewBuildInputs(sourceRoot, fixtureRoot) {
  function copy(relative) {
    const destination = path.join(fixtureRoot, relative);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.cpSync(path.join(sourceRoot, relative), destination, { recursive: true });
  }
  for (const name of fs.readdirSync(sourceRoot)) {
    if (name.endsWith('.py')) copy(name);
  }
  for (const name of fs.readdirSync(path.join(sourceRoot, 'sources'), { withFileTypes: true })) {
    if (name.isFile() && name.name.endsWith('.json')) copy(`sources/${name.name}`);
  }
  for (const relative of [
    'scripts/apply_review_repairs.py',
    'out/data/reverse_lookup_crosswalk.csv',
    'out/data/katameros_cycle_passage_index.csv',
    'out/design/reverse_lectionary_presentation.csv',
    'sources/katameros-api/Core/KatamerosDatabase.db',
    'sources/coptic-reader/holy-week-review-qualified-2026-10-29',
    'sources/coptic-reader/kiahk-23-qualified-2026-10-29',
    'sources/coptic-reader/matins-source-accepted-2026-10-07/evidence/lent-source-completion-04/attempts/2026-04-03-ready02',
    'sources/coptic-reader/lent-qualified-2026-10-07/2026-03-13',
    'sources/resolver-review-2026-10-29',
  ]) copy(relative);
  const pins = JSON.parse(fs.readFileSync(path.join(sourceRoot, 'sources/resolver-review-2026-10-29/composite-source-pins.json'), 'utf8'));
  for (const relative of Object.keys(pins)) copy(relative);
};
