"""Frozen predecessor + real CSV/design -> npm, without a candidate-mode bypass."""
import hashlib
import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest
import build_design_deliverables as design
import bright_saturday_composite_supplements as bright
import psalmody_source_supplements as psalmody
from test_bright_composite_projection_integration import (
    raw_rows, csv_transport, HELD_KEYS, HISTORICAL_KEYS,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/fixtures/bright-published-1.3.5.json'
SHA = '9a8344c0c9087d5e48e635a62630a5dfb3da15382a870743eb36745171e3da0a'


def baseline():
    data = FIXTURE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == SHA
    f = json.loads(data)
    assert f['source']['member_sha256'] == '6c7060c0f4102475bf753cbe52dc63ba66d70af4a8edf0914269432b244a0941'
    assert f['source']['selected_rows'] == len(f['rows']) == 47
    assert f['source']['selector'] == "source_family == 'bright_saturday' OR occasion == 'Bright Saturday'"
    return f['rows']


def payload():
    raw = [r for r in raw_rows() if r['source_kind'] == bright.SOURCE_KIND or r['superseded_reason'] == bright.HOLD]
    p = csv_transport(design.build_reverse_presentation(raw)[0])
    def exact_eight(rows):
        assert len(rows) == 8
        assert {design.occasion_index_key(r) for r in rows} == HELD_KEYS | HISTORICAL_KEYS
    with patch.object(design, 'verify_reverse_index_contract', side_effect=exact_eight):
        reverse = design.build_reverse_lectionary_index(p, transport_mode='presentation')[0]
    # The legacy aliases share the invalid numeric identities too: no activation.
    retired = {k[-1] for k in HISTORICAL_KEYS}
    legacy = [r for r in baseline() if r['identity_key'] not in retired]
    opening = [r for r in psalmody.load_psalmody_source_rows() if r['calendar_key'] == 'Bright Saturday']
    opening = design.build_reverse_presentation(opening)[0]
    assert len(opening) == 1
    # Only the corpus-wide membership gate is isolated: eight literal composite
    # keys plus the independently pinned Psalm 151 opening identity.
    def with_opening(rows):
        composite = [r for r in rows if r['source_kind'] != 'psalmody_source_supplement']
        exact_eight(composite)
        extras = [r for r in rows if r['source_kind'] == 'psalmody_source_supplement']
        assert len(extras) == 1
        assert design.occasion_index_key(extras[0]) == ('Bright Saturday', 'Midnight Praises', '', 'Psalm151', 'rid_803a7b6de46806e9e2d7')
    with patch.object(design, 'verify_reverse_index_contract', side_effect=with_opening):
        opening_reverse = design.build_reverse_lectionary_index(p + opening, transport_mode='presentation')[0]
    opening_reverse = [r for r in opening_reverse if r['source_kind'] == 'psalmody_source_supplement']
    daily = design.build_daily_year_files(p + opening, transport_mode='presentation')
    return {'reverse': reverse, 'legacy': legacy, 'opening': opening_reverse, 'daily': daily}


def test_real_bright_csv_design_npm_coexistence():
    result = subprocess.run(['node', str(ROOT / 'tests/npm_bright_composite_coexistence.test.cjs'), '--pipeline'],
        input=json.dumps(payload()), text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_historical_fixture_is_independent_of_mutable_package(monkeypatch):
    original = Path.read_bytes
    def read(path):
        if path.is_relative_to(ROOT / 'packages'):
            raise AssertionError('mutable output is not historical evidence')
        return original(path)
    monkeypatch.setattr(Path, 'read_bytes', read)
    assert len(baseline()) == 47


def test_fixture_hash_rejects_drift(tmp_path, monkeypatch):
    damaged = tmp_path / 'damaged.json'
    damaged.write_bytes(FIXTURE.read_bytes() + b'\n')
    monkeypatch.setitem(baseline.__globals__, 'FIXTURE', damaged)
    with pytest.raises(AssertionError):
        baseline()
