"""Public evidence is a pinned factual receipt, not absent archived source bytes."""
import hashlib
import json
from pathlib import Path

import holy_week_continuation as hw

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SHA = '10d981e8fa068a4b49a7227f62955a3a26f1efbc785f514cb274277fc5434443'


def test_public_receipts_exclude_full_service_and_private_review():
    source = ROOT / hw.SOURCE
    assert not (source / 'thursday-eve-eleventh.txt').exists()
    assert not (source / 'independent-source-plan.md').exists()
    receipt = json.loads((source / 'capture-receipt.json').read_text())
    assert receipt['evidence_kind'] == 'factual_capture_receipt'
    assert receipt['archived_capture']['sha256'] == ARCHIVE_SHA
    assert receipt['archived_capture']['publicly_distributed'] is False
    assert receipt['archived_capture']['bytes'] == 76017
    assert receipt['archived_capture']['lines'] == 749
    assert [r['printed_reference'] for r in receipt['readings']] == ['Jeremiah 8:4-10', 'Psalm 61:4,1', 'John 12:44-50']
    assert [r['heading_line'] for r in receipt['readings']] == [12, 110, 124]
    assert receipt['capture_selected_year'] is None
    for p in source.iterdir():
        assert p.name in {'capture-receipt.json', 'source-plan-receipt.json'}
        raw = p.read_bytes()
        assert len(raw) < 10000
        assert b'/Users/' not in raw and b'session' not in raw
        assert hashlib.sha256(raw).hexdigest() == hw.PINS[str(p.relative_to(ROOT))]
    review = json.loads((source / 'source-plan-receipt.json').read_text())
    assert review['original_report_sha256'] == '19bd78cf20bbcf0f1f4397bdb8a444b6ce093f44c78ed1f4484e2317a198a80f'
    assert review['new_independent_review'] is False
    assert review['release_acceptance'] is False


def test_public_proof_authenticates_receipt_not_unavailable_archive():
    rows = hw.project_daily(hw.predecessor()['daily']['2026-04-08'], '2026-04-08')
    row = next(r for r in rows if r.get('identity_key') == hw.NEW_ID)
    proof = json.loads(row[hw.MARKER])
    assert proof['source_path'] == hw.SOURCE + 'capture-receipt.json'
    assert proof['source_sha256'] != ARCHIVE_SHA
    assert proof['evidence_kind'] == 'factual_capture_receipt'
    assert proof['archived_source_sha256'] == ARCHIVE_SHA
    assert proof['archived_source_publicly_distributed'] is False
    assert '#/readings/2' in row['source_locator']
    assert 'archived heading line 124' in row['source_locator']
    assert proof['capture_selected_year'] is None
    assert proof['fresh_app_verification'] is False
