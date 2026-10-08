"""Scoped integration ledger: actual helpers, isolated outputs, full-date preservation."""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
import calendar_resolution as calendar
import build_lectionary_reference as reference
from build_lectionary_crosswalk import apply_pascha_curated_ref_correction

OUT = ROOT / 'audit_artifacts/calendar-boundary-integration'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source = (ROOT / 'calendar_resolution.py').read_text()
# Recover exact pre-task bytes, checking against the pre-edit recorded hash.
before = source[:source.index('def load_last_friday_boundary')] + source[source.index('def resolve_current_date_rows'):]
before = before.replace('import hashlib\nimport json\nfrom pathlib import Path\n', '')
before = before.replace('\nfrom passage_normalization import canonicalize_text_ref\n\nWORK = Path(__file__).resolve().parent\nLAST_FRIDAY_TITLE = "Friday of the seventh week of Great Lent"\nBOUNDARY_SOURCE = "Coptic Reader verified calendar boundary"\n', '')
before = before.replace('Overlay documented Holy Week and verified Last Friday feast collisions.', 'Overlay only documented Annunciation/Holy Week collisions.')
before = before.replace('        if (date_value - julian_pascha_gregorian(date_value.year)).days == -9:\n            resolved.extend(last_friday_collision_rows(date_value, date_rows))\n            continue\n', '')
before = before.replace("({'Matins': '0', 'Liturgy': '1'}[row['service_section']] if row.get('source') == BOUNDARY_SOURCE else row.get(\"service_section\", \"\"))", 'row.get("service_section", "")')
before = before.replace('(f"{int(row[\'source_order\']):02d}" if row.get(\'source\') == BOUNDARY_SOURCE else str(row.get("source_order", "")))', 'str(row.get("source_order", ""))')
expected = json.loads((OUT / 'before-hashes.json').read_text())['calendar_resolution.py']
assert hashlib.sha256(before.encode()).hexdigest() == expected, 'Pre-task reconstruction must be byte-identical'
(OUT / 'calendar_resolution.before.py').write_text(before)
module = types.ModuleType('before_calendar')
exec(before, module.__dict__)
with (ROOT / 'out/data/copticchurch_date_readings_2020_2035.csv').open() as handle:
    raw_rows = list(csv.DictReader(handle))
with (ROOT / 'out/data/pascha_day_hour_index.csv').open() as handle:
    pascha_rows = list(csv.DictReader(handle))
corrected = []
for row in pascha_rows:
    item = apply_pascha_curated_ref_correction(row)
    if item.get('_raw_refs'):
        item['raw_refs'] = item.get('raw_refs') or item['_raw_refs']
        item['correction_source'] = item.get('correction_source') or item.get('_ref_correction_note', '')
    corrected.append(item)
baseline = module.resolve_current_date_rows(raw_rows, corrected)
current = calendar.resolve_current_date_rows(raw_rows, corrected)
def group(rows):
    days = {}
    for row in rows:
        days.setdefault(row['gregorian_date'], []).append(row)
    return days
old, new = group(baseline), group(current)
changed = [date for date in sorted(set(old) | set(new)) if old.get(date) != new.get(date)]
assert changed == ['2023-04-07', '2028-04-07'], changed
for date in changed:
    (OUT / f'before-{date}.json').write_text(json.dumps(old[date], indent=2) + '\n')
    (OUT / f'after-{date}.json').write_text(json.dumps(new[date], indent=2) + '\n')
(OUT / 'before-table.json').write_text(json.dumps(old['2028-04-07'], indent=2) + '\n')
(OUT / 'after-table.json').write_text(json.dumps(new['2028-04-07'], indent=2) + '\n')
# Exercise the ACTUAL sidecar helper on a temp directory, not a full parent builder.
canaries = {'2026-04-07', '2027-04-07', '2028-04-06', '2028-04-07', '2028-04-08', '2026-04-03'}
with tempfile.TemporaryDirectory() as directory:
    temp = Path(directory)
    reference.write_csv(temp / 'copticchurch_date_readings_2020_2035.csv', [r for r in raw_rows if r['gregorian_date'] in canaries])
    shutil.copyfile(ROOT / 'out/data/pascha_day_hour_index.csv', temp / 'pascha_day_hour_index.csv')
    with patch.object(reference, 'DATA', temp):
        isolated_rows, isolated_index = reference.build_current_date_sidecars()
    assert group(isolated_rows)['2028-04-07'] == new['2028-04-07']
    assert len(group(isolated_rows)['2026-04-07']) == 38
    assert len(group(isolated_rows)['2027-04-07']) == 9
    assert len([r for r in isolated_index if r['gregorian_date'] == '2028-04-07']) == 11
    (OUT / 'isolated-helper-output.json').write_text(json.dumps({'dates': sorted(canaries), 'row_counts': {d: len(r) for d, r in group(isolated_rows).items()}, 'files': {p.name: sha(p) for p in temp.iterdir() if p.is_file()}}, indent=2) + '\n')
ledger = {'source_scope': 'calendar boundary and source passage helper only', 'baseline_source_sha256': expected,
          'compared_civil_dates': len(old), 'unchanged_civil_dates': len(old) - len(changed), 'changed_dates': changed,
          'raw_source_count': len(raw_rows), 'current_source_before_count': len(baseline), 'current_source_after_count': len(current),
          'target_before_count': len(old['2028-04-07']), 'target_after_count': len(new['2028-04-07']),
          'boundary_collision_counts': {d: {'before': len(old[d]), 'after': len(new[d])} for d in changed},
          'recurrence_disclosure': '2023-04-07 has the same exact Annunciation AND Last-Friday -9 collision; applies the 2028 verified recurring context, not a fresh 2023 capture',
          'suppressed_service': 'Vespers', 'missing_matins_prophecies_restored': 4,
          'raw_removed_context': {'date': '2028-04-07', 'occasion': 'Annunciation', 'reason': 'superseded by independently captured Last Friday complete table; preserve historical source rows'},
          'recurring_prophecy_scope': 'exact Last Friday -9 AND Annunciation feast collision; no noncollision enrichment',
          'isolated_actual_helper': 'build_current_date_sidecars', 'unrun': ['full builders', 'design/site', 'npm install/pack/publish', 'deploy', 'vault', 'commits'],
          'parent_followup': ['recognize boundary source provenance in crosswalk/design', 'preserve raw Annunciation as context-qualified superseded history', 'full serialized rebuild and release gates remain held']}
(OUT / 'ledger.json').write_text(json.dumps(ledger, indent=2) + '\n')
# Surrounding source tests run with temp output isolation (existing index helper writes reports).
selected = ['test_recurs_in_supported_years_at_only_verified_movable_context', 'test_source_boundary_and_current_date_helper_order', 'test_primary_fingerprint_and_printed_reference_drift_fail_closed', 'test_no_adjacent_or_other_week_or_wrong_title_enrichment', 'test_context_qualified_cycle_correction_retains_raw_api']
loader = unittest.TestLoader()
suite = loader.loadTestsFromName('test_lent_annunciation_boundary')
for name in selected:
    suite.addTests(loader.loadTestsFromName('test_lent_matins_prophecies.LentMatinsProphecies.' + name))
with tempfile.TemporaryDirectory() as directory, patch.object(reference, 'DATA', Path(directory)):
    result = unittest.TextTestRunner(verbosity=2).run(suite)
assert result.wasSuccessful()
print(json.dumps(ledger, indent=2))
