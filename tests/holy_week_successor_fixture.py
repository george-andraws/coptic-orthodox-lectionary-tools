"""Trusted-version test adapter; preserve original 1.3.11 historical oracles.

Undo the authenticated outer successor and its preceding ordering-only delta
before invoking historical positional fixtures. Never choose a policy by markers
or observed coordinates, and never refresh a predecessor fingerprint.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def current_version():
    package = ROOT / 'packages/lectionary-data'
    version = json.loads((package/'package.json').read_text())['version']
    assert json.loads((package/'meta.json').read_text())['version'] == version
    assert version in ('1.3.10', '1.3.11', '1.3.12')
    return version


def reverse_1_3_11(rows):
    if current_version() == '1.3.12':
        import holy_week_continuation as continuation
        continuation.verify_membership(rows)
        return continuation.restore_reverse(rows)
    return rows


def daily_1_3_11(rows, date):
    if current_version() == '1.3.12':
        import holy_week_continuation as continuation
        rows = continuation.restore_daily(rows, date)
    from good_friday_order_review import restore_daily_order
    return restore_daily_order(rows, date)
