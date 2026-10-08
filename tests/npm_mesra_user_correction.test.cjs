const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');

// Surgical helper execution: no main(), package writes or artifact regeneration.
function projectionHelpers() {
  const source = fs.readFileSync(path.join(root, 'scripts/build_npm_package.mjs'), 'utf8');
  const start = source.indexOf('const SERVICE_ORDER =');
  const end = source.indexOf('function disambiguateWeekdaySpecificRows(');
  assert.ok(start > 0 && end > start);
  return vm.runInNewContext(source.slice(start, end) + '\n({ suppressLowerPriorityPassageVariants });');
}

test('George Mesra 19 correction keeps James 1:12-21 active through actual npm projection', () => {
  const policy = JSON.parse(fs.readFileSync(path.join(root, 'sources/lectionary_corrections.json')));
  assert.equal(policy.projection_removal_effective_versions.filter(r =>
    r.identity_key === 'rid_663541d046c596982394' && r.removal_context_key === 'mesra 19|liturgy||catholicon').length, 0);
  const script = `import json,datetime as dt
import build_lectionary_reference as core
import build_design_deliverables as design
_,table=core.parse_copticchurch_html((core.WORK/'cache/copticchurch_html/2023-08-25.html').read_text(),dt.date(2023,8,25))
row=next(r for r in core.build_date_passage_index(table) if r['reading_type']=='Catholic Epistle')
public=dict(design.identity_for(row['matched_ref'],'copticchurch_date'),occasion=row['day_title'],service_section=row['service_section'],service_hour='',slot=row['reading_type'],source_kind='copticchurch_date',source_family='ordinary_date_resolved',current_status='current_working_source_not_coptic_reader_checked')
cycle=dict(design.identity_for('James 1:12-21','katameros_cycle'),occasion='Mesra 19',service_section='liturgy_catholic',service_hour='',slot='liturgy_catholic',source_kind='katameros_cycle',source_family='annual_fixed',current_status='current_public_or_local_reference')
print(json.dumps([public,cycle]))`;
  const rows = JSON.parse(execFileSync(process.env.PYTHON || 'python3', ['-B', '-c', script], {
    cwd: root, encoding: 'utf8', env: { ...process.env, PYTHONDONTWRITEBYTECODE:'1', LECTIONARY_DISABLE_VAULT_PUBLISH:'1' },
  }));
  assert.equal(rows[0].display_ref, 'James 1:12-21');
  assert.equal(rows[0].identity_key, rows[1].identity_key);
  const result = projectionHelpers().suppressLowerPriorityPassageVariants(rows, new Map());
  assert.equal(result.activeRows.length, 2, 'same corrected identity has no conflicting endpoint to suppress');
  assert.equal(result.suppressions.length, 0);
  assert.ok(result.activeRows.every(r => r.display_ref === 'James 1:12-21'));
});
