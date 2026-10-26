"""Exact retained Reader oracle; no generic Psalm-coordinate activation."""
import csv
import io
import json
from pathlib import Path
import shutil
import tempfile
from unittest.mock import patch

import pytest
import build_lectionary_crosswalk as crosswalk

ORACLE = [('Matins', 'Ps 44:23,44:26'), ('Matins', 'Ps 126:2-3'),
          ('6th Hour', 'Ps 142:7'), ('Liturgy', 'Ps 82:8')]


def api():
    import bright_saturday_composite_supplements as supplement
    return supplement


def source_rows():
    return crosswalk.read_csv(crosswalk.BRIGHT_CSV)


def test_real_projection_adds_four_qualified_selections_and_preserves_history():
    fn = getattr(crosswalk, 'project_bright_rows', None)
    assert fn is not None, 'Bright source qualification is not wired into real raw projection'
    rows = fn(source_rows(), crosswalk.BRIGHT_CSV)
    selected = [r for r in rows if r['source_kind'] == api().SOURCE_KIND]
    assert [(r['service_section'], r['passage']) for r in selected] == ORACLE
    legacy = [r for r in rows if r.get('superseded_reason') == api().HOLD]
    assert len(legacy) == 4
    assert any(r['passage'] == 'Ps 44:23-26' and '44:23-26' in r['raw_ref'] for r in legacy)
    for row in selected:
        q = api().qualify_bright_composite_row(row)
        identity = api().bright_composite_identity_for(row)
        assert q['fresh_app_verification'] is False
        assert q['canonical_coordinate_status'] == 'held_no_exact_cross_edition_counterpart'
        assert identity['canonical_mt_ref'] == identity['canonical_lxx_ref'] == ''
        assert json.loads(identity['spans_json']) == []
    # No source syntax rewrite changes unrelated controls or source ordering.
    assert any(r['passage'] == 'Matt 27:62-66' and not r['superseded_reason'] for r in rows)
    from psalmody_source_supplements import load_psalmody_source_rows
    psalmody = load_psalmody_source_rows()
    assert api().qualify_bright_composite_row(psalmody[0]) is None
    assert load_psalmody_source_rows() == psalmody


def test_exact_source_selection_excludes_44_24_and_25():
    rows = api().load_bright_composite_rows()
    row = rows[0]
    from passage_normalization import parse_passage
    assert [(p.verse_start, p.verse_end) for p in parse_passage(row['passage']).parts] == [(23, 23), (26, 26)]
    q = api().qualify_bright_composite_row(row)
    assert 'Awake, why do You sleep' in q['body_literal']
    assert q['printed_ref'] == 'Psalm 88:4-5; 44:23,26; 126:2-3'
    assert q['legacy_ref'] == 'Ps 44:23-26'


def test_raw_and_passage_csv_roundtrip_reauthenticates(tmp_path):
    rows = api().load_bright_composite_rows()
    raw = tmp_path / 'raw.csv'
    crosswalk.write_csv(raw, rows, crosswalk.FIELDS)
    reread = crosswalk.read_csv(raw)
    assert reread == rows
    for row in reread:
        assert api().qualify_bright_composite_row(row)
        identity = api().bright_composite_identity_for(row)
        path = tmp_path / 'passage.csv'
        crosswalk.write_csv(path, [identity], list(identity))
        projected = crosswalk.read_csv(path)[0]
        assert api().authenticate_bright_composite_identity(row, projected) == identity


@pytest.mark.parametrize('field,value', [('service_day','Good Friday'), ('service_section','3rd Hour'),
    ('source_family','ordinary_date_resolved'), ('source_kind','pascha_day_hour'),
    ('source_order',True), ('source_order',1), ('source_token_order','1.0'),
    ('passage','Ps 44:23-26'), ('removed_marker','x'), ('candidate_only',False)])
def test_context_and_scalar_tampering_fail_closed(field, value):
    row = api().load_bright_composite_rows()[0]
    row[field] = value
    with pytest.raises(ValueError):
        api().qualify_bright_composite_row(row)


def test_portable_capture_authentication_missing_corrupt_and_symlink(tmp_path):
    mod = api()
    root = tmp_path / 'evidence'
    shutil.copytree(mod.SOURCE_ROOT, root)
    assert len(mod.load_bright_composite_rows(root)) == 4
    target = root / 'saturday--matins.txt'
    data = target.read_bytes()
    target.write_bytes(data + b'changed')
    with pytest.raises(ValueError):
        mod.load_bright_composite_rows(root)
    target.unlink()
    with pytest.raises(ValueError):
        mod.load_bright_composite_rows(root)
    outside = tmp_path / 'outside.txt'
    outside.write_bytes(data)
    target.symlink_to(outside)
    with pytest.raises(ValueError):
        mod.load_bright_composite_rows(root)


def test_authentication_failure_reaches_real_projection():
    mod = api()
    with patch.object(mod, 'load_bright_composite_rows', side_effect=ValueError('evidence unavailable')):
        with pytest.raises(ValueError, match='evidence unavailable'):
            crosswalk.project_bright_rows(source_rows(), crosswalk.BRIGHT_CSV)


@pytest.mark.parametrize('field,value', [('section','OTHER'), ('subsection','3rd Hour'),
                                      ('reading_name','Gospel'), ('reference','Ps 44:23-26')])
def test_real_projection_rejects_source_service_slot_reference_rebinding(field, value):
    rows = source_rows()
    index = int(api().load_bright_composite_rows()[0]['source_order']) - 1
    rows[index] = {**rows[index], field: value}
    with pytest.raises(ValueError):
        crosswalk.project_bright_rows(rows, crosswalk.BRIGHT_CSV)


def test_all_legacy_token_order_and_canticle_rows_remain_in_order():
    source = source_rows()
    rows = crosswalk.project_bright_rows(source, crosswalk.BRIGHT_CSV)
    legacy = [r for r in rows if r['source_kind'] == 'bright_saturday_service_order']
    from passage_normalization import canonicalize_text_ref, extract_text_ref_tokens
    expected = [(str(i), str(j), canonicalize_text_ref(token))
                for i, row in enumerate(source, 1)
                for j, token in enumerate(extract_text_ref_tokens(
                    crosswalk.expand_bright_psalm_shorthand(row['reference'])), 1)]
    assert [(str(r['source_order']), str(r['source_token_order']), r['passage']) for r in legacy] == expected


def test_passage_identity_tamper_is_rejected():
    mod = api()
    row = mod.load_bright_composite_rows()[0]
    identity = mod.bright_composite_identity_for(row)
    identity['canonical_mt_ref'] = 'Ps 44:23-26'
    with pytest.raises(ValueError):
        mod.authenticate_bright_composite_identity(row, identity)
