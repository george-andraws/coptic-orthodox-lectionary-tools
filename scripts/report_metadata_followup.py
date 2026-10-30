#!/usr/bin/env python3
"""Emit the bounded metadata audit fragments without rebuilding the package."""
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import metadata_followup_repairs as m


def main():
    destination = ROOT / 'docs/reviews/timothy-luke-metadata-1.3.8'
    destination.mkdir(parents=True, exist_ok=True)
    frozen = m.baseline()
    rows = frozen['reverse_rows']
    projected = m.repair_rows(rows)
    m.validate_rows(projected)
    inventory = m.endpoint_conflicts(rows)
    confirmations = m.timothy_confirmations()
    deltas = []
    fields = Counter()
    for position, (before, after) in enumerate(zip(rows, projected), 1):
        changed = {k: {'before_present': k in before, 'before': before.get(k),
                       'after_present': k in after, 'after': after.get(k)}
                   for k in set(before) | set(after)
                   if before.get(k) != after.get(k) or (k in before) != (k in after)}
        if changed:
            fields.update(changed.keys())
            deltas.append(dict(baseline_line=position,
                               source={k: before.get(k, '') for k in m.SOURCE_FIELDS}, changes=changed))
    daily = {}
    for year, days in frozen['daily'].items():
        after = m.repair_daily(days)
        daily[year] = dict(before=sum(map(len, days.values())), after=sum(map(len, after.values())),
                           changed=sum(old != new for date, readings in days.items()
                                       for old, new in zip(readings, after[date])))
    def witness(row):
        return {k: row.get(k, '') for k in ('identity_key', 'source_family', 'source_kind',
            'source_locator', 'source_title', 'calendar_keys', 'day_titles', 'service_section',
            'service_hour', 'slot', 'display_ref', 'current_status', 'removed_marker')}
    scope = dict(baseline_authentication=frozen['authentication'],
                 fixture_sha256=m.FIXTURE_SHA256, retained_source_hashes=m.SOURCE_HASHES,
                 reverse_before=len(rows), reverse_after=len(projected), changed_rows=len(deltas),
                 changed_fields=dict(fields), daily=daily,
                 removed_rows=sum(bool(r.get('removed_marker')) for r in rows),
                 removed_true_before=sum(bool(r.get('removed_marker')) and r.get('occurs_in_shipped_years') is True for r in rows),
                 removed_true_after=sum(bool(r.get('removed_marker')) and r.get('occurs_in_shipped_years') is True for r in projected),
                 cycle_rows_by_season=dict(Counter(r['normalized_season'] for r in projected if m.bare_cycle_keys(r))),
                 single_key_current_by_season=dict(Counter(r['normalized_season'] for r in projected if len(m.bare_cycle_keys(r)) == 1 and m.is_current(r))),
                 multikey_current_by_season=dict(Counter(r['normalized_season'] for r in projected if len(m.bare_cycle_keys(r)) > 1 and m.is_current(r))),
                 lk1_witnesses=[witness(r) for r in projected if m.LK1_FLAG in r.get('metadata_review_flags', [])],
                 lk4_named_witnesses=[witness(r) for r in projected if m._lk4(r)],
                 unresolved_cycle_witnesses=[witness(r) for r in projected if r.get('cycle_label_status') == 'unresolved_source_week_49'],
                 endpoint_context_service_slot_start_groups=len(inventory),
                 endpoint_dated_start_groups=sum(len(r['dates']) for r in inventory),
                 endpoint_distinct_dated_slots=len({(date, r['service'], r['hour'], r['slot']) for r in inventory for date in r['dates']}),
                 timothy_confirmations=confirmations)
    for name, obj in [('scope.json', scope), ('endpoint-conflicts.json', inventory)]:
        (destination / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + '\n')
    data = gzip.compress(json.dumps(deltas, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode(), mtime=0)
    (destination / 'source-qualified-row-deltas.json.gz').write_bytes(data)
    lines = ['# Timothy and Luke metadata check-sheet fragment', '',
             'No status promotion, endpoint choice or new Reader verification is recorded.', '',
             '## T-L7: confirm, no change expected', '',
             'Exactly seven appointment confirmations, all low priority. Six retain their copticchurch.net locator. '
             'The Great Thursday Water Liturgy is already backed by retained Reader source evidence in 1.3.7; '
             'the package has no copticchurch.net witness for that service. Its actual locator is retained instead of inventing one.', '',
             '| Identity | Reading | Occasion and service | Source locator |', '|---|---|---|---|']
    lines += [f"| `{r['identity_key']}` | {r['display_ref']} | {m.normalize_month_words(r['occasion'])}, {r['service_section']} | `{r['source_locator']}` |" for r in confirmations]
    lines += ['', '## LK1: Abib 26, do not choose', '',
              'Both three-Gospel sets are flagged. Calendar co-display does not say why a reading was selected for a saint.', '',
              '| Source family | Raw day wording | Service | Reading | Identity and locator |', '|---|---|---|---|---|']
    lines += [f"| {r['source_family']} | {r['day_titles'] or r['calendar_keys']} | {r['service_section']} | {r['display_ref']} | `{r['identity_key']}`; `{r['source_locator']}` |" for r in scope['lk1_witnesses']]
    lines += ['', '## LK4: preserve both printed ranges', '',
              'Fourth Sunday of Mesra, Vespers: Luke 17:20-36 versus 17:20-37. '
              'Tout 8, Liturgy: Matthew 23:13-26 versus 23:13-36. The latter Katameros witness is already inactive. '
              'Both named pairs receive flags without lifecycle or coordinate changes.', '',
              f"Report-only current inventory: {len(inventory)} context/service/slot/start groups, "
              f"{scope['endpoint_dated_start_groups']} dated groups and {scope['endpoint_distinct_dated_slots']} distinct dated slots. "
              'Each exact date and source tuple is retained in endpoint-conflicts.json. '
              'The next table lists the complete inventory, not only the two examples.', '',
              '| Context | Service and slot | Canonical MT variants | Retained dates |', '|---|---|---|---|']
    lines += [f"| {r['context']} | {r['service']} {r['hour']}, {r['slot']} | {' / '.join(r['references'])} | {', '.join(r['dates'])} |" for r in inventory]
    lines += ['', '## LK3: unresolved source sentinel', '',
              'The two inactive Exodus witnesses under source week 49 remain inactive. '
              'Their label discloses the unresolved source week instead of inventing a forty-ninth liturgical week.', '']
    (destination / 'check-sheet-fragment.md').write_text('\n'.join(lines))
    print(json.dumps({k: scope[k] for k in ('reverse_before', 'reverse_after', 'changed_rows', 'changed_fields',
          'daily', 'removed_rows', 'removed_true_before', 'removed_true_after', 'cycle_rows_by_season',
          'single_key_current_by_season', 'multikey_current_by_season',
          'endpoint_context_service_slot_start_groups', 'endpoint_dated_start_groups')}, indent=2))
    print('row-deltas sha256=' + hashlib.sha256(data).hexdigest())


if __name__ == '__main__':
    main()
