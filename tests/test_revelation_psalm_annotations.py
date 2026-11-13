"""Bounded Revelation-review Psalm annotation corrections, not a global crosswalk."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

import evidence_followup_repairs as e

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'sources/revelation-review-1.3.10/published-1.3.9-psalm-targets.json'
# Independently compared Bible witnesses, literal expected loci (not converter output).
EXPECTED = {
    'Ps 116:15-16': 'Ps 115:6-7',
    'Ps 88:11-12': 'Ps 87:12-13',
    'Ps 36:9-10': 'Ps 35:10-11',
    'Ps 115:12-13': 'Ps 113:20-21',
    'Ps 115:1-2': 'Ps 113:9-10',
    'Ps 115:16-18': 'Ps 113:24-26',
}


def rows():
    data = FIXTURE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == '7d01fb9820067f0102edab1a1454bcff950f1ed1f74d0566bf1bda185fa7c65b'
    fixture = json.loads(data)
    assert len(fixture['rows']) == 14
    return fixture['rows']


@pytest.mark.parametrize('mt,lxx', EXPECTED.items())
def test_literal_loci_repair_real_published_rows_without_source_changes(mt, lxx):
    before = [r for r in rows() if r['canonical_mt_ref'] == mt]
    after, stats = e.repair_psalm_annotations(before)
    # Three authentic cycle witnesses are already retired in the frozen artifact.
    retired = lambda r: r['source_family'] == 'katameros_cycle' and r['canonical_mt_ref'] in {'Ps 36:9-10','Ps 115:12-13'}
    assert stats['annotations_changed'] == sum(not retired(r) for r in before)
    for old, new in zip(before, after):
        if retired(old):
            assert new == old
            continue
        assert new['canonical_lxx_ref'] == lxx
        assert new['display_ref'] == f'{mt} (LXX {lxx})'
        allowed = {'canonical_lxx_ref', 'display_ref', 'spans_json', 'psalm_annotation_review_json'}
        assert {k:v for k,v in old.items() if k not in allowed} == {k:v for k,v in new.items() if k not in allowed}
        old_span, = json.loads(old['spans_json'])
        new_span, = json.loads(new['spans_json'])
        assert {k:v for k,v in old_span.items() if k not in {'canonical_lxx_ref','validation_basis','confidence'}} == {k:v for k,v in new_span.items() if k not in {'canonical_lxx_ref','validation_basis','confidence'}}
    again, replay = e.repair_psalm_annotations(after)
    assert again == after
    assert replay['annotations_changed'] == 0
    e.validate_psalm_annotations(after)


@pytest.mark.parametrize('field,value', [('active',False),('status','removed'),
    ('current_status','historical_witness'),('current_status','superseded_by_reader'),
    ('removed_marker','superseded by canonical source')])
def test_historical_witnesses_unchanged(field, value):
    row = {**rows()[0],field:value}
    assert e.repair_psalm_annotations([row])[0] == [row]


def test_source_only_and_non_mt_numeric_holds_are_not_mapped():
    original = rows()[0]
    for convention in ('lxx_liturgical_or_fixture_label','existing_numeric_source_coordinates_alignment_held'):
        row = copy.deepcopy(original)
        spans = json.loads(row['spans_json'])
        spans[0]['source_convention'] = convention
        row['spans_json'] = json.dumps(spans)
        assert e.repair_psalm_annotations([row])[0] == [row]
    row = {**original,'canonical_mt_ref':'','canonical_lxx_ref':'','spans_json':'[]',
           'current_status':'pending_psalm_equivalence_unresolved'}
    assert e.repair_psalm_annotations([row])[0] == [row]


def test_neighboring_unreviewed_selection_is_not_inferred_from_offset():
    # The adjacent selection is deliberately not authorized by these six loci.
    assert e.frame_qualified_lxx('Ps 88:10')[0:3] == ('Ps 87:10','chapter_mapped_verse_offset_not_guessed','medium')


def test_new_annotation_inverse_authenticates_delta_and_preserves_foreign_mutations():
    before = rows()
    fixed, _ = e.repair_psalm_annotations(before)
    assert e.restore_rows_for_comparison(fixed) == before
    for field, value in [('canonical_lxx_ref','Ps 115:99'),('display_ref','forged'),
                         ('spans_json','[]'),('source_locator','copied-to-other-context')]:
        bad = copy.deepcopy(fixed)
        bad[0][field] = value
        with pytest.raises(ValueError, match='Psalm annotation'):
            e.restore_rows_for_comparison(bad)
    bad = copy.deepcopy(fixed)
    bad[0]['active'] = False
    # Annotation inverse does not erase lifecycle corruption; downstream guard owns it.
    assert e.restore_rows_for_comparison(bad)[0]['active'] is False


def test_disposable_evidence_tamper_fails_at_real_mapping_boundary(tmp_path, monkeypatch):
    import shutil
    relative = Path('sources/revelation-review-1.3.10')
    shutil.copytree(ROOT / relative, tmp_path / relative)
    monkeypatch.setattr(e, 'ROOT', tmp_path)
    assert e.frame_qualified_lxx('Ps 116:15-16')[0] == 'Ps 115:6-7'
    path = tmp_path / relative / 'Brenton-115.html'
    path.write_bytes(path.read_bytes() + b' altered')
    with pytest.raises(ValueError, match='evidence hash mismatch'):
        e.frame_qualified_lxx('Ps 116:15-16')
