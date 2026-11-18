"""Authenticated inverse for the bounded, daily-only Good Friday order repair.

The published predecessor remains the historical oracle. This module does not
rewrite source ordinals or approve reading membership, coordinates or lifecycle.
Only the two complete reviewed permutations may enter older positional inverses.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURE = 'tests/fixtures/good-friday-published-1.3.11.json.gz'
FIXTURE_SHA256 = '54f264bdb981bbc7e8fbbaad9c2554b7bdc28c6a62599c9e3a8025ae7e73f4d3'
TABLES = {
    'Sixth Hour': ('Matt 27:27-45', 'Mark 15:26-33', 'Lk 23:26-44', 'Jn 19:13-27'),
    'Twelfth Hour': ('Matt 27:57-61', 'Mark 15:42-16:1', 'Lk 23:50-56', 'Jn 19:38-42'),
}
SOURCES = (
    ('sources/coptic-reader/holy-week-review-qualified-2026-10-29/friday--6th-hour.txt',
     'aae5386449ddad8f45ca625402bd4ed3ee9c885c10c05e161e69f77e02110c57'),
    ('sources/coptic-reader/pascha-resolution-qualified-2026-10-25/fresh-pascha/friday--12th-hour.txt',
     '9a6bd0b11b67fa6d3cfbe10a99b84a085796b8b3e886ddec4d191ef02dbe2e0e'),
)
DATES = ('2026-04-10', '2027-04-30', '2028-04-14')


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _pinned(relative, expected):
    path = ROOT / relative
    data = path.read_bytes()
    if path.is_symlink() or hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('Good Friday ordering source authentication failed: ' + relative)
    return data


def restore_daily_order(rows, date):
    if date not in DATES:
        return rows
    # Recognize the successor, not arbitrary Friday rows or tiny historical
    # fixture slices. Unrecognized content still reaches all old strict guards.
    has_successor = any(tuple(r.get('canonical_mt_ref') for r in rows
        if r.get('occasion') == 'Good Friday' and r.get('service_section') == hour
        and r.get('slot') == 'Gospel') == refs for hour, refs in TABLES.items())
    if not has_successor:
        return rows
    for relative, digest in SOURCES:
        _pinned(relative, digest)
    frozen = json.loads(gzip.decompress(_pinned(FIXTURE, FIXTURE_SHA256)))
    before = frozen['daily'][date]
    expected = copy.deepcopy(before)
    for hour, refs in TABLES.items():
        positions = [i for i, row in enumerate(before)
                     if row['service_section'] == hour and row['slot'] == 'Gospel']
        if len(positions) != 4:
            raise ValueError('Good Friday predecessor quartet incomplete')
        for i, ref in zip(positions, refs):
            matches = [r for r in before if r['service_section'] == hour and r['canonical_mt_ref'] == ref]
            if len(matches) != 1:
                raise ValueError('Good Friday predecessor source selection ambiguous')
            expected[i] = copy.deepcopy(matches[0])
    for i, row in enumerate(expected):
        row['reading_order'] = i + 1
    # Exact full-cell comparison includes unknown fields, all companions, source
    # disclosures, original slot ordinals, strict scalar types and history flags.
    # Never return frozen rows until every candidate cell is authenticated.
    if _json(rows) != _json(expected):
        raise ValueError('Good Friday ordering full-day source/context/cell drift')
    return copy.deepcopy(before)
