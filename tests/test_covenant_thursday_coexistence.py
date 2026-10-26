"""Literal Covenant join oracle with authenticated published 1.3.5 witnesses."""
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest
import build_design_deliverables as design
import covenant_thursday_source_supplements as covenant
from test_covenant_thursday_projection_integration import raw_csv, TABLE

ROOT = Path(__file__).resolve().parents[1]
# Frozen complete service records from the authenticated predecessor, never the
# mutable package directory that the next release build will replace.
BASELINE = ROOT / 'tests/fixtures/covenant-published-1.3.5.json'
BASELINE_SHA = '3c6850d8b2a6ff4275ee6a2b40a18e6fb216d3b590efde0db3a936b03d8c73f2'


def baseline():
    data = BASELINE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == BASELINE_SHA, 'published 1.3.5 service fixture drift'
    fixture = json.loads(data)
    assert fixture['source']['version'] == '1.3.5'
    assert fixture['source']['member_sha256'] == '6c7060c0f4102475bf753cbe52dc63ba66d70af4a8edf0914269432b244a0941'
    assert len(fixture['rows']) == fixture['source']['selected_rows'] == 54
    return fixture['rows']


def literal_keys():
    keys = set()
    for section, appointments in TABLE.items():
        for slot, printed, mt, lxx in appointments:
            material = 'scripture|' + mt + '|' + lxx if mt else 'scripture_named_excerpt|' + printed
            identity = 'rid_' + hashlib.sha256(material.encode()).hexdigest()[:20]
            keys.add(('the Covenant Thursday' if section == 'Liturgy' else 'Great Thursday', section, section, slot, identity))
    return keys


def projected():
    return design.build_reverse_presentation(raw_csv())[0]


def joined_reverse():
    p = projected()
    old = [r for r in baseline() if design.occasion_index_key(r) in literal_keys()]
    assert len(old) == 5
    def subset(rows):
        assert len(rows) == 16
        assert {design.occasion_index_key(r) for r in rows} == literal_keys()
    with patch.object(design, 'verify_reverse_index_contract', side_effect=subset):
        reverse, disagreements = design.build_reverse_lectionary_index(p + old, transport_mode='presentation')
    return p, old, reverse


def test_structural_baseline_survives_package_rebuild(monkeypatch):
    original_read = Path.read_bytes
    def without_mutable_package(path):
        if path.is_relative_to(ROOT / 'packages'):
            raise FileNotFoundError('rebuilt package output is not historical evidence')
        return original_read(path)
    monkeypatch.setattr(Path, 'read_bytes', without_mutable_package)
    rows = baseline()
    assert len([r for r in rows if design.occasion_index_key(r) in literal_keys()]) == 5
    assert any(r.get('service_hour') == 'First Hour' for r in rows)


def test_frozen_predecessor_fixture_drift_is_rejected(tmp_path, monkeypatch):
    damaged = tmp_path / 'published-predecessor.json'
    damaged.write_bytes(BASELINE.read_bytes() + b'\n')
    monkeypatch.setitem(baseline.__globals__, 'BASELINE', damaged)
    with pytest.raises(AssertionError, match='fixture drift'):
        baseline()


def test_qualified_contexts_join_five_existing_keys_without_promoting_witnesses():
    p, old, reverse = joined_reverse()
    assert {design.occasion_index_key(r) for r in p} == literal_keys()
    assert len(literal_keys() - {design.occasion_index_key(r) for r in old}) == 11
    for original in old:
        row = next(r for r in reverse if design.occasion_index_key(r) == design.occasion_index_key(original))
        assert row['source_kind'] == covenant.SOURCE_KIND
        assert row['current_status'] == 'current_public_or_local_reference'
        disclosures = json.loads(row['source_disclosure'])
        assert any(d.get('covenant_thursday_source') for d in disclosures)
        assert any(w['current_status'] == original['current_status'] and w['removed_marker'] == original['removed_marker']
                   and w.get('source_disclosure') == original['source_disclosure']
                   for d in disclosures for w in d.get('source_witnesses', []))
    assert sum(r['current_status'] == 'current_working_source_not_coptic_reader_checked' for r in old) == 1
    assert sum(r['current_status'].startswith('historical') for r in old) == 4


def test_real_csv_design_npm_structural_coexistence():
    p, old, reverse = joined_reverse()
    daily = design.build_daily_year_files(p, transport_mode='presentation')
    result = subprocess.run(['node', str(ROOT / 'tests/npm_covenant_thursday_coexistence.test.cjs'), '--pipeline'],
        input=json.dumps({'daily': daily, 'reverse': reverse, 'legacy': baseline()}), text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize('field,value', [('occasion', 'Great Friday'), ('service_hour', 'First Hour'),
    ('service_section', 'Matins'), ('source_kind', 'pascha_day_hour'), ('source_family', 'other'),
    ('source_order', '99'), ('source_token_order', '99'), ('identity_key', 'rid_forged'), ('provenance', '{}')])
def test_actual_reverse_and_daily_callers_reject_forged_projection(field, value):
    row = dict(projected()[0], **{field: value})
    with pytest.raises(ValueError):
        design.build_daily_year_files([row], transport_mode='presentation')
    with pytest.raises(ValueError):
        design.build_reverse_lectionary_index([row], transport_mode='presentation')


def test_projection_reauthenticates_evidence_at_reverse_and_daily_callers():
    p = projected()
    with patch.object(covenant, 'load_covenant_thursday_rows', side_effect=ValueError('tampered evidence')):
        with pytest.raises(ValueError, match='tampered evidence'):
            design.build_daily_year_files(p, transport_mode='presentation')
        with pytest.raises(ValueError, match='tampered evidence'):
            design.build_reverse_lectionary_index(p, transport_mode='presentation')
