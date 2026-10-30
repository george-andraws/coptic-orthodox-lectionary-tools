#!/usr/bin/env python3
"""Source-owned runtime review projection, after the legacy design contract.

The design corpus and its historical membership ledger remain unchanged. This
bounded release lane preserves witnesses and authenticates new appointments at
both the reverse and date-output boundaries. It never writes source inputs.
"""
from __future__ import annotations

import json
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
        return {'rows': mark_followup.repair_rows(labels(rows)), 'events': events}
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
        return {'days': finish_daily(days), 'events': events}
    if mode == 'occurrence':
        return finish_reverse([resolver_review.annotate_calendar_occurrence(row, payload['daily_by_year'])
                               for row in payload['rows']])
    raise ValueError('Unknown review projection mode: ' + str(mode))


def main():
    payload = json.load(sys.stdin)
    result = project(payload.pop('mode'), payload)
    json.dump(result, sys.stdout, ensure_ascii=False, separators=(',', ':'))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
