"""Bounded 1.3.7 comparison oracles, never candidate-as-repair-input.

Historical source bytes and published witnesses are authenticated before the
source-owned projection is used. Only exact reviewed additions/retirements are
admitted. Inactive witnesses remain forbidden in the public daily projection.
"""
from __future__ import annotations

from collections import Counter
import copy
import csv
import datetime as dt
import hashlib
import io
import json
from pathlib import Path

import calendar_review_repairs as calendar
import holy_week_review_repairs as holy
import kiahk23_review_repairs as r2
import resolver_review_repairs as resolver

ROOT = Path(__file__).resolve().parents[1]
HOLY_FIXTURE = 'tests/fixtures/holy_week_review_1_3_6.json'
HOLY_SHA256 = '8aa845a557e06b3b58a900335a8d5b695727ea934b76065bb2cf6d822762fc02'
CACHE = 'out/data/copticchurch_passage_index_current_2020_2035.csv'
CACHE_SHA256 = 'd373b55d42f78209a74ee1533884c81c357995333e58e884b76b2d0c14e2b2dd'
SERVICE_ORDER = {'Vespers': 1, 'Matins': 2, 'First Hour': 10, 'Third Hour': 20,
                 'Sixth Hour': 30, 'Ninth Hour': 40, 'Eleventh Hour': 50,
                 'Twelfth Hour': 60, 'Liturgy of Blessing of the Water': 45, 'Liturgy': 99}


def _pinned(relative, digest):
    path = ROOT / relative
    data = path.read_bytes()
    if path.is_symlink() or hashlib.sha256(data).hexdigest() != digest:
        raise ValueError('Review comparison source authentication failed: ' + relative)
    return data


def signature(row):
    return json.dumps({k: v for k, v in row.items() if k != 'reading_order'},
                      ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def source_signature(row):
    # Bind the complete CSV schema as well as literal values, including blank
    # cells. An arbitrary extra field is not an approved source transformation.
    return json.dumps(row, sort_keys=True)


def _appointment(row):
    return tuple(row.get(k, '') for k in ('source_locator', 'identity_key', 'occasion', 'service_section', 'service_hour', 'slot'))


def unscoped_calendar_projection(row):
    """Authenticate the four optional unscoped fields before removing them.

    This is deliberately NOT a generic calendar validator. The caller's exact
    identity/source oracle still rejects every other extra field.
    """
    expected = dict(coptic_date_key='', annual_sunday='', calendar_review_status='',
                    display_label=calendar.display_label(row.get('display_occasion') or row.get('occasion', '')))
    for field, value in expected.items():
        if field in row and (type(row[field]) is not str or row[field] != value):
            raise ValueError('Unscoped calendar metadata drift: ' + field)
    return {k: v for k, v in row.items() if k not in expected}


def _holy_oracle(year):
    frozen = json.loads(_pinned(HOLY_FIXTURE, HOLY_SHA256))
    # Authenticate all full documents on every call, including repeated probes.
    reverse = holy.repair_reverse_rows(frozen['reverse_rows'])
    before = copy.deepcopy(frozen['daily'].get(str(year), {}))
    if not before:
        return {}, {}, reverse
    seed = copy.deepcopy(before)
    for rows in seed.values():
        for row in rows:
            if row.get('structural_day') and row.get('source_family') == holy.LEGACY:
                # npm structural fill consumes the already reviewed reverse
                # witness but transports only its declared daily fields.
                matches = [r for r in reverse if all(r.get(k, '') == row.get(k, '') for k in
                           ('source_locator', 'identity_key', 'occasion', 'service_section', 'service_hour', 'slot'))]
                if len(matches) != 1:
                    raise ValueError('Review comparison structural witness not unique')
                for field in ('current_status', 'source_disclosure'):
                    row[field] = matches[0][field]
    # Only authenticated PREDECESSOR rows enter repair hooks. Never run repair
    # over candidate rows and mistake idempotency for source authentication.
    seed = calendar.load_runtime_review(ROOT).apply_daily_year(seed)
    expected = holy.repair_daily_year(year, seed, reverse)
    for rows in expected.values():
        for row in rows:
            row['display_label'] = calendar.display_label(row.get('display_occasion') or row.get('display_label') or row.get('occasion', ''))
            row['service_order'] = SERVICE_ORDER[row.get('service_hour') or row['service_section']]
    return before, expected, reverse


def _holy_signal(row):
    return (row.get('source_family') == holy.FAMILY or row.get('source_kind') == holy.FAMILY
            or any(field in row for field in holy.CONTEXT_FIELDS + holy.EVIDENCE_FIELDS)
            or holy.SOURCE in str(row.get('source_locator', '')))


RESOLVER_FIXTURE = 'tests/fixtures/resolver_review_runtime_1_3_6.json'
RESOLVER_SHA256 = 'd67211070e397effc37adbcd7a65ecef22b0fee426ac392724d963bf78271a4c'


def _resolver_oracle(year) -> dict[str, tuple[str, dict]]:
    """Project pinned predecessors only; candidate disclosures are never inputs.

    The published daily fixture owns the complete original fragment schema.
    For the two other shipped Thursdays, rebind only its source-address fields
    from the independently approved raw contract. The repair then authenticates
    the literal retained HTML cell, fragment coordinates and Reader recurrence.
    """
    if year not in (2026, 2027, 2028):
        return {}
    frozen = json.loads(_pinned(RESOLVER_FIXTURE, RESOLVER_SHA256))['daily']
    contract = json.loads(_pinned(resolver.RAW_CONTRACT, resolver.RAW_CONTRACT_SHA256))
    seeds, kinds = {}, {}
    for date, rows in frozen.items():
        if date.startswith(f'{year}-') and any(r.get('display_ref') == 'Lk 17:20-37' for r in rows):
            seeds[date] = copy.deepcopy(rows)
            kinds[date] = 'r1'
    date = (resolver.pascha(year) - dt.timedelta(days=10)).isoformat()
    raw = [r for r in contract if r['gregorian_date'] == date
           and r['raw_ref'] == 'Acts 25:23-27  &  Acts 26:1-6']
    refs = ('Acts 25:23-27', 'Acts 26:1-6')
    if [r['passage'] for r in raw] != list(refs):
        raise ValueError('Review comparison raw composite contract incomplete')
    templates = [r for r in frozen['2026-04-02'] if r['display_ref'] in refs]
    fragments = []
    for template, witness in zip(templates, raw):
        row = copy.deepcopy(template)
        row['source_row_id'] = witness['source_row_id']
        row['source_locator'] = (witness['url'] + '; ' + witness['source_file']
            + ':row ' + witness['source_row_id'] + '; source_ref=' + witness['source_ref'])
        row['source_group_key'] = '|'.join((witness['source_kind'], witness['source_row_id'],
                                           witness['calendar_key'], '', witness['reading_type']))
        row['source_disclosure'] = json.dumps([{k: witness[k] for k in
            ('source_kind', 'source_family', 'source_file', 'source_row_id')}], separators=(',', ':'))
        fragments.append(row)
    seeds[date], kinds[date] = fragments, 'r4'
    seeds = calendar.load_runtime_review(ROOT).apply_daily_year(seeds)
    oracle = {}
    for date, rows in seeds.items():
        projected, events = resolver.repair_daily_rows(date, rows)
        kind = kinds[date]
        wanted = [r for r in projected if (r.get('resolver_review_disclosure') if kind == 'r1'
                                         else r.get('composite_fragments_json'))]
        if len(wanted) != 1 or not any(e['id'].lower() == kind for e in events):
            raise ValueError('Review comparison resolver predecessor projection failed')
        oracle[date] = (kind, wanted[0])
    return oracle


def prepare(source_rows, daily, year, *, review_release=False):
    """Return authenticated projection, synthetic source rows and exact audits.

    Review epoch is explicit for package 1.3.7; direct bounded probes can also
    select the lane via its owned markers. The old source/package pair remains
    testable without silently upgrading its historical policy.
    """
    # Public transport decoding is representation-only. Existing exact source
    # table and appointment oracles below still authenticate the decoded rows.
    from composite_followup_repairs import restore_public_rows
    daily = {date: restore_public_rows(rows) for date, rows in daily.items()}
    output = copy.deepcopy(daily)
    additions, retired, dispositions, issues = [], Counter(), [], []

    def issue(date, status):
        issues.append(dict(year=year, status=status, count=1, gregorian_date=date,
                           service_section='', reading_type_or_slot='', normalized_ref=''))

    def audit(date, row, disposition, evidence, digest, *, source=False):
        dispositions.append(dict(year=year, gregorian_date=date,
            occasion=row.get('day_title' if source else 'occasion', ''),
            service_section=row.get('service_section', ''), count=1,
            normalized_ref=row.get('matched_ref' if source else 'display_ref', ''),
            disposition=disposition, evidence=evidence, evidence_sha256=digest))

    # H adds descriptive context to one pre-existing Bright Saturday witness,
    # without granting a new reading/exclusion lane. Authenticate only that
    # metadata here; the unchanged structural comparator still judges the row.
    for date, rows in output.items():
        for row in rows:
            if ((row.get('source_family'), row.get('source_kind'), row.get('occasion')) ==
                    (holy.LEGACY, 'pascha_day_hour', 'Bright Saturday')
                    and any(field in row for field in holy.CONTEXT_FIELDS)):
                try:
                    expected_context = holy.pascha_context(row, date)
                    if any(row.get(k) != v or type(row.get(k)) is not type(v) for k, v in expected_context.items()):
                        raise ValueError('Bright Saturday review context drift')
                except ValueError:
                    issue(date, 'invalid_qualified_holy_week_review_context')
                    continue
                for field in holy.CONTEXT_FIELDS:
                    row.pop(field)

    holy_dates = {date for date, rows in output.items() if any(_holy_signal(r) for r in rows)}
    if review_release or holy_dates:
        before, expected, reverse = _holy_oracle(year)
        if review_release:
            holy_dates.update(set(daily) & set(expected))
        cache = list(csv.DictReader(io.StringIO(_pinned(CACHE, CACHE_SHA256).decode())))
        for date in sorted(holy_dates):
            if date not in expected:
                issue(date, 'invalid_qualified_holy_week_review_context')
                continue
            rows = daily[date]
            wanted = [r for r in expected[date] if r.get('source_family') == holy.FAMILY]
            actual = [r for r in rows if r.get('source_family') == holy.FAMILY or r.get('source_kind') == holy.FAMILY
                      or holy.SOURCE in str(r.get('source_locator', ''))]
            wanted.sort(key=holy._daily_order_key)
            if list(map(signature, actual)) != list(map(signature, wanted)):
                issue(date, 'invalid_qualified_holy_week_review_complete_sequence')
            ordered = [holy._daily_order_key(r) for r in rows if r.get('pascha_service')]
            if ordered != sorted(ordered):
                issue(date, 'invalid_qualified_holy_week_review_service_sequence')
            legacy_expected = [r for r in expected[date] if r.get('source_family') == holy.LEGACY]
            legacy_actual = [r for r in rows if r.get('source_family') == holy.LEGACY]
            if Counter(map(signature, legacy_actual)) != Counter(map(signature, legacy_expected)):
                issue(date, 'invalid_qualified_holy_week_review_legacy_table')
            # Authenticate the retained full source table before issuing any
            # exact retired-witness disposition. No date/family-wide bypass.
            cached = [r for r in cache if r['gregorian_date'] == date]
            supplied = [r for r in source_rows if r.get('gregorian_date') == date]
            if Counter(map(source_signature, supplied)) != Counter(map(source_signature, cached)):
                issue(date, 'invalid_holy_week_review_cached_source_table')
            holds = [r for r in reverse if r.get('current_status') == holy.HOLD]
            available = Counter(map(source_signature, supplied))
            for row in cached:
                matches = [r for r in holds if
                           (r['occasion'], r['service_section'], r['slot'], r['canonical_mt_ref']) ==
                           (row['day_title'], row['service_section'],
                            row.get('source_slot') if row['reading_type'] == 'Prophecy' else row['reading_type'], row['matched_ref'])]
                fingerprint = source_signature(row)
                if len(matches) == 1 and available[fingerprint]:
                    available[fingerprint] -= 1
                    retired[fingerprint] += 1
                    audit(date, row, 'authenticated_holy_week_cached_retirement', HOLY_FIXTURE, HOLY_SHA256, source=True)
            for row in wanted:
                additions.append((date, row))
                evidence = json.loads(row['holy_week_review_evidence'])
                audit(date, row, 'source_qualified_holy_week_review_selection', evidence['path'], evidence['sha256'])
            # Project only exact authenticated legacy views back to the old
            # comparator domain. Changed/extra fields stay failures, not ignored.
            originals = {_appointment(r): r for r in before[date] if r.get('source_family') == holy.LEGACY}
            allowed = {signature(r): r for r in legacy_expected}
            for i, row in enumerate(rows):
                if signature(row) in allowed:
                    output[date][i] = dict(copy.deepcopy(originals[_appointment(row)]), reading_order=row['reading_order'])

    r2_dates = {date for date, rows in daily.items() if any(r2._recognized(r) or r.get('kiahk23_retirement') for r in rows)}
    if review_release:
        r2_dates.update(date for date in daily if r2._date_eligible(date))
    if r2_dates:
        plan = r2.authenticate_plan()
        cache = list(csv.DictReader(io.StringIO(_pinned(CACHE, CACHE_SHA256).decode())))
        for date in sorted(r2_dates):
            if not r2._date_eligible(date):
                issue(date, 'invalid_qualified_kiahk23_review_context')
                continue
            wanted = [dict(r2._new_row(a, plan), gregorian_date=date,
                           weekday=dt.date.fromisoformat(date).strftime('%A'), reading_order=i,
                           display_label='Kiahk 23', service_order=SERVICE_ORDER[a['service_section']])
                      for i, a in enumerate(plan['appointments'], 1)]
            if list(map(signature, daily[date])) != list(map(signature, wanted)):
                issue(date, 'invalid_qualified_kiahk23_review_complete_sequence')
            cached = [r for r in cache if r['gregorian_date'] == date]
            supplied = [r for r in source_rows if r.get('gregorian_date') == date]
            if (not cached or any(r['day_title'] not in {'Kiak 23', 'Kiahk 23', 'Kiyahk 23'} or r.get('service_hour') for r in cached)
                    or Counter(map(source_signature, supplied)) != Counter(map(source_signature, cached))):
                issue(date, 'invalid_kiahk23_review_cached_source_table')
                continue
            for row in cached:
                retired[source_signature(row)] += 1
                audit(date, row, 'authenticated_kiahk23_cached_retirement', r2.PLAN, r2.PLAN_SHA256, source=True)
            for row in wanted:
                additions.append((date, row))
                audit(date, row, 'source_qualified_kiahk23_review_selection', r2.PLAN, r2.PLAN_SHA256)
    # R1 replaces one exact cached predecessor; R4 replaces two complete,
    # ordered fragments with their authenticated appointment on BOTH sides.
    # Bad candidate rows or source tables receive no retirement permission.
    resolver_signal = any(r.get('resolver_review_disclosure') or r.get('composite_fragments_json')
                          for rows in daily.values() for r in rows)
    if review_release or resolver_signal:
        cache = list(csv.DictReader(io.StringIO(_pinned(CACHE, CACHE_SHA256).decode())))
        for date, (kind, wanted) in _resolver_oracle(year).items():
            if date not in daily:
                continue
            def appointment(row, source=False):
                return (row.get('service_section') == wanted['service_section']
                        and row.get('reading_type' if source else 'slot') == wanted['slot'])
            actual = [r for r in daily[date] if appointment(r)]
            valid_package = list(map(signature, actual)) == [signature(wanted)]
            if not valid_package:
                issue(date, 'invalid_qualified_' + kind + '_review_appointment')
            cached = [r for r in cache if r['gregorian_date'] == date and appointment(r, True)]
            supplied = [r for r in source_rows if r.get('gregorian_date') == date and appointment(r, True)]
            valid_source = (len(cached) == (1 if kind == 'r1' else 2)
                            and list(map(source_signature, supplied)) == list(map(source_signature, cached)))
            if not valid_source:
                issue(date, 'invalid_' + kind + '_review_cached_source_table')
            if not (valid_package and valid_source):
                continue
            for row in cached:
                retired[source_signature(row)] += 1
                audit(date, row, 'authenticated_' + kind + '_cached_retirement', CACHE, CACHE_SHA256, source=True)
            additions.append((date, wanted))
            audit(date, wanted, 'source_qualified_' + kind + '_review_selection', RESOLVER_FIXTURE, RESOLVER_SHA256)
    return output, additions, retired, dispositions, issues
