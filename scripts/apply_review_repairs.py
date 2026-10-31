#!/usr/bin/env python3
"""Source-owned runtime review projection, after the legacy design contract.

The design corpus and its historical membership ledger remain unchanged. This
bounded release lane preserves witnesses and authenticates new appointments at
both the reverse and date-output boundaries. It never writes source inputs.
"""
from __future__ import annotations

import json
import copy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import calendar_review_repairs as calendar_review
import holy_week_review_repairs as holy_week
import kiahk23_review_repairs as kiahk23
import resolver_review_repairs as resolver_review
import mark_followup_repairs as mark_followup
import metadata_followup_repairs as metadata
import composite_followup_repairs as composite
import evidence_followup_repairs as evidence
import annual_occasion_repairs as annual_occasion


def finish_daily(days):
    days = metadata.repair_daily(days)
    for date, rows in days.items():
        days[date], _ = evidence.repair_psalm_annotations(rows)
        days[date] = composite.compact_public_rows(days[date])
    return days


def finish_reverse(rows):
    rows, events = composite.merge_remaining_composites(rows)
    rows = metadata.repair_rows(rows)
    rows, counts = evidence.repair_rows(rows)
    return {'rows': composite.compact_public_rows(rows), 'events': events,
            'evidence_counts': counts}


def _preserve_archived_witnesses(rows, daily_by_year):
    """Restore pinned LK5 occurrence bytes after descriptive annotation.

    Annotation rewrites occurs_in_shipped_years from current daily output. A
    Reader correction may remove the archived passage from daily files. That
    must not rewrite the pinned witness. Any other field drift still reaches
    the composite check.
    """
    owned = {'occurs_in_shipped_years', 'displaced_by', 'occurs_outside_paschal_seasons', 'occurrence_scope'}
    expected_by_key = {composite._key(item): item for group in composite._witness_groups() for item in group}
    projected = []
    for row in rows:
        annotated = resolver_review.annotate_calendar_occurrence(row, daily_by_year)
        expected = expected_by_key.get(composite._key(annotated))
        if expected is None:
            projected.append(_keep_authenticated_occurrence(annotated))
            continue
        if json.dumps(annotated, sort_keys=True) == json.dumps(expected, sort_keys=True):
            projected.append(annotated)
            continue
        left = json.loads(json.dumps(annotated, sort_keys=True))
        right = json.loads(json.dumps(expected, sort_keys=True))
        changed = {key for key in set(left) | set(right) if left.get(key) != right.get(key)}
        projected.append(copy.deepcopy(expected) if changed <= owned else annotated)
    return projected


_PREDECESSOR_OCCURRENCE = None


def _predecessor_occurrence_index():
    global _PREDECESSOR_OCCURRENCE
    if _PREDECESSOR_OCCURRENCE is None:
        _PREDECESSOR_OCCURRENCE = {metadata._signature(item): item for item in metadata.baseline()['reverse_rows']}
    return _PREDECESSOR_OCCURRENCE


def _keep_authenticated_occurrence(row):
    """Keep a predecessor occurrence bit the metadata inverse still owns.

    A weekday Reader correction can remove a shared display reference from daily
    files. Occurrence annotation then clears occurs_in_shipped_years on an
    untouched Sunday row. That is not an authorized metadata change. L1 rows
    and removed rows keep the later layer's value.
    """
    if row.get('removed_marker'):
        return row
    original = _predecessor_occurrence_index().get(metadata._signature(row))
    if original is None or mark_followup.rule(original) == 'L1':
        return row
    if row.get('occurs_in_shipped_years') == original.get('occurs_in_shipped_years'):
        return row
    restored = dict(row)
    restored['occurs_in_shipped_years'] = original.get('occurs_in_shipped_years')
    return restored


def labels(rows):
    return [dict(row, display_label=calendar_review.display_label(
        row.get('display_occasion') or row.get('display_label') or row.get('occasion', '')))
        for row in rows]


def project(mode, payload):
    if mode == 'reverse':
        # Calendar metadata is qualified against untouched source identities.
        rows = calendar_review.load_runtime_review(ROOT).apply_reverse_rows(payload['rows'])
        rows = holy_week.repair_reverse_rows(rows)
        rows = kiahk23.repair_reverse_rows(rows)
        rows, events = resolver_review.repair_reverse_rows(rows)
        rows = annual_occasion.repair_reverse_rows(mark_followup.repair_rows(labels(rows)))
        return {'rows': rows, 'events': events}
    if mode == 'daily':
        year = payload['year']
        days = calendar_review.load_runtime_review(ROOT).apply_daily_year(payload['days'])
        days = holy_week.repair_daily_year(year, days, payload['reverse_rows'])
        days = kiahk23.repair_daily(days, payload['reverse_rows'])
        events = []
        for date, rows in days.items():
            projected, changes = resolver_review.repair_daily_rows(date, rows)
            days[date] = labels(projected)
            events.extend(changes)
        days = mark_followup.repair_daily(days)
        coverage = mark_followup.validate_eve_coverage(days, year)
        events.extend(dict(id='L3', **entry) for entry in coverage if entry['coverage'] == 'held_missing_reader')
        mark_followup.validate_day_hour_sets(days)
        return {'days': annual_occasion.repair_daily(finish_daily(days)), 'events': events}
    if mode == 'occurrence':
        return finish_reverse(_preserve_archived_witnesses(payload['rows'], payload['daily_by_year']))
    raise ValueError('Unknown review projection mode: ' + str(mode))


def main():
    payload = json.load(sys.stdin)
    result = project(payload.pop('mode'), payload)
    json.dump(result, sys.stdout, ensure_ascii=False, separators=(',', ':'))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
