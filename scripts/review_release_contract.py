"""Fail-closed, source-owned exceptions for the generic release validator.

False/('', '') means unowned; a recognized but malformed review row raises
ValueError. These helpers never infer approval from candidate metadata.
"""
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import calendar_review_repairs as calendar
import holy_week_review_repairs as holy
import kiahk23_review_repairs as r2

ROOT = Path(__file__).resolve().parents[1]
DESIGN_SOURCE = 'out/design/reverse_lectionary_index.jsonl'
DESIGN_SHA256 = '3473d858301159573118dd8df25522a95c412e19a8a78bc22a3d483a6f7dd0fc'
IDENTITY_FIELDS = ('identity_key', 'display_ref', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json')
CALENDAR_FIELDS = calendar.FIELDS + ('calendar_review_source_locators', 'calendar_review_calendar_keys')
STABLE_FIELDS = ('source_family', 'source_kind', 'source_locator', 'occasion', 'service_section',
                 'service_hour', 'slot', 'calendar_keys', 'day_titles')


def validate_public_followup_rows(rows):
    """Public cosmetics are independent of source/evidence authentication."""
    for row in rows:
        text = row.get('provenance', '')
        if (type(text) is not str or len(text) > 300 or text.lstrip().startswith(('{', '['))
                or '_review_original_row' in json.dumps(row, ensure_ascii=False)):
            raise ValueError('LK6 invalid public provenance presentation')


def followup_reverse_view(rows, *, previous_layer='mark', require_all_targets=True):
    import composite_followup_repairs as composite
    import metadata_followup_repairs as metadata
    import evidence_followup_repairs as evidence
    validate_public_followup_rows(rows)
    rows = composite.restore_public_rows(rows)
    rows = evidence.restore_rows_for_comparison(rows, require_all_targets=require_all_targets)
    rows = metadata.restore_rows_for_comparison(rows, previous_layer=previous_layer, annotated=True)
    return composite.legacy_validation_rows(rows)


def followup_daily_view(days, *, previous_layer='mark'):
    import composite_followup_repairs as composite
    import metadata_followup_repairs as metadata
    import evidence_followup_repairs as evidence
    output = {}
    for date, rows in days.items():
        validate_public_followup_rows(rows)
        rows = composite.restore_public_rows(rows)
        rows = evidence.restore_rows_for_comparison(rows, date=date)
        output[date] = metadata.restore_rows_for_comparison(rows, date=date, previous_layer=previous_layer)
    return output


@lru_cache(maxsize=1)
def _r2_rows():
    plan = r2.authenticate_plan()
    return [r2._new_row(appointment, plan) for appointment in plan['appointments']]


def _r2_owned(row):
    if r2._recognized(row):
        return True
    # Identity survives compound stripping of family/evidence/coordinate markers.
    # Numeric identities are shared elsewhere, so retain their service context.
    for expected in _r2_rows():
        if row.get('identity_key') == expected['identity_key'] and (
                not expected['canonical_mt_ref'] or
                row.get('occasion') in r2.LABELS and
                all(row.get(f, '') == expected[f] for f in ('service_section', 'slot'))):
            return True
    return False


def source_owned_empty_coordinates(row, date_key=None):
    """True only for qualified R2 source-only Psalms; qualify numeric R2 too.

    Pass the trusted outer ISO date for daily rows; never derive it from row data.
    Other pre-existing source-only families remain the validator's responsibility.
    """
    if not _r2_owned(row):
        return False
    r2.qualify_row(row, civil_date=date_key)
    return row['slot'] == 'Psalm' and not row['canonical_mt_ref'] and json.loads(row['spans_json']) == []


def _check_expected(row, expected):
    for field, value in expected.items():
        if row.get(field) != value or type(row.get(field)) is not type(value):
            raise ValueError('review inactive witness drift: ' + field)
    for field in ('source_file', 'source_row_id', 'source_ref', 'source_url',
                  'gregorian_date', 'coptic_date', 'holy_week_review_evidence',
                  'kiahk23_retirement', 'superseded_by_ref'):
        if field not in expected and row.get(field):
            raise ValueError('review inactive unexpected source/approval field: ' + field)
    # Extra lifecycle fields must not reactivate an otherwise authentic witness.
    for field, default in (('active', False), ('status', 'removed')):
        if field in row and row[field] != expected.get(field, default):
            raise ValueError('review inactive lifecycle drift: ' + field)


def _matches_owned(row, expected):
    return (row.get('source_locator') == expected.get('source_locator') or
            row.get('identity_key') == expected.get('identity_key') and
            all(row.get(f, '') == expected.get(f, '') for f in ('occasion', 'service_section', 'service_hour', 'slot')))


@lru_cache(maxsize=1)
def _holy_holds(payload):
    # The byte-keyed cache cannot hide on-disk source drift; callers reread/hash.
    originals = [json.loads(line) for line in payload.decode().splitlines()]
    candidates = [r for r in originals if r.get('source_family') == holy.LEGACY and
                  (r.get('occasion') == 'Tuesday Eve' or
                   (r.get('occasion'), r.get('service_hour'), r.get('canonical_mt_ref')) in {
                       ('Good Friday', 'Sixth Hour', 'Jn 19:1-12'),
                       ('Wednesday Eve', 'First Hour', 'Jer 43:5-11')})]
    return [next(r for r in holy.repair_reverse_rows([original])
                 if r.get('source_locator') == original['source_locator']) for original in candidates]


def review_inactive_qualified(row):
    """Authenticate exact R2 retirements and H1/H4/H6 holds, not all inactivity."""
    import mark_followup_repairs as followup
    if followup.inactive_qualified(row):
        return True
    r2.authenticate_plan()
    legacy = json.loads(r2._read(r2.SOURCE + '/repair-approval/legacy-published-1.3.6.json'))['reverse_rows']
    retired = [r2._retire(original) for original in legacy]
    matches = [r for r in retired if _matches_owned(row, r)]
    if matches or row.get('kiahk23_retirement') or row.get('removed_marker') == 'removed_by_kiahk23_review':
        exact = [r for r in matches if all(row.get(f) == r.get(f) for f in STABLE_FIELDS)]
        if len(exact) != 1:
            raise ValueError('review Kiahk23 retirement source/context rebound')
        _check_expected(row, exact[0])
        qualified_calendar_context(row)
        return True
    # Recognize the malformed hold even after its explicit hold note is stripped.
    possible = (row.get('current_status') == holy.HOLD or
                str(row.get('holy_week_review_note', '')).startswith(('H1:', 'H4:', 'H6:')) or
                row.get('source_family') == holy.LEGACY or
                str(row.get('source_locator', '')).startswith('out/data/pascha_day_hour_index.csv:row '))
    if not possible:
        return False
    path = ROOT / DESIGN_SOURCE
    payload = path.read_bytes()
    if path.is_symlink() or hashlib.sha256(payload).hexdigest() != DESIGN_SHA256:
        raise ValueError('review Holy Week original source authentication failed')
    holds = _holy_holds(payload)
    # Reauthenticate retained capture documents even when the projection is cached.
    for key in holy._manifest()['documents']:
        holy.authenticate_document(key)
    matches = [r for r in holds if _matches_owned(row, r)]
    if not matches and row.get('current_status') != holy.HOLD and not str(row.get('holy_week_review_note', '')).startswith(('H1:', 'H4:', 'H6:')):
        return False
    exact = [r for r in matches if all(row.get(f) == r.get(f) for f in STABLE_FIELDS)]
    if len(exact) != 1:
        raise ValueError('review Holy Week hold source/context rebound')
    _check_expected(row, exact[0])
    for field in ('coptic_date_key', 'annual_sunday', 'calendar_review_status'):
        if row.get(field, ''):
            raise ValueError('review Holy Week unexpected calendar context')
    if row.get('display_label', exact[0]['display_occasion']) != exact[0]['display_occasion']:
        raise ValueError('review Holy Week display context drift')
    return True


def _originals(row):
    """Unwrap only source-preserved coordinate changes; calendar stays original."""
    if row.get('composite_fragments_json'):
        fragments = json.loads(row['composite_fragments_json'])
        originals = [f['_review_original_row'] for f in fragments]
        if len(originals) < 2:
            raise ValueError('calendar composite original fragments missing')
        base = originals[0]
    elif row.get('resolver_review_disclosure'):
        disclosure = json.loads(row['resolver_review_disclosure'])
        base = disclosure.get('original', row)
        # R1 reverse superseded_source belongs to the old witness, not the
        # already-correct Reader source carrying the same recurrence disclosure.
        if 'superseded_source' in disclosure and row.get('source_family') == 'ordinary_date_resolved':
            base = disclosure['superseded_source']
        originals = [base]
    else:
        return [row]
    if any(row.get(f, '') != base.get(f, '') for f in STABLE_FIELDS):
        raise ValueError('calendar transformed source/context rebound')
    return originals


def qualified_calendar_context(row):
    """Return authenticated (fixed-date slug, annual-Sunday slug) for deduping.

    All normalized fields/evidence must agree with their original source view.
    Unscoped rows cannot manufacture a context to evade duplicate detection.
    This does not approve transformed numeric coordinates (other gates do that).
    """
    if _r2_owned(row):
        r2.qualify_row(row)
        if any(row.get(f) for f in ('annual_sunday', 'calendar_review_status',
                                   'calendar_review_source_locators', 'calendar_review_calendar_keys')):
            raise ValueError('calendar Kiahk23 unexpected normalized context')
        if row.get('display_label', row['occasion']) != row['occasion']:
            raise ValueError('calendar Kiahk23 display metadata drift')
        return ('kiahk-23', '')
    try:
        originals = _originals(row)
        import mark_followup_repairs as followup
        index = {followup.key(r): r for r in followup.originals()}
        restored = []
        for original in originals:
            predecessor = index.get(followup.key(original))
            if predecessor and original.get('display_label') != predecessor.get('display_label'):
                followup._qualify(original, predecessor, projected=True)
                original = dict(original, display_label=predecessor['display_label'])
            restored.append(original)
        originals = restored
        runtime = calendar.load_runtime_review(ROOT)
        projected = runtime.apply_reverse_rows(originals)
        pair = (originals[0].get('source_family'), originals[0].get('source_kind'))
        scoped = pair in (*calendar.DATED_SOURCES, calendar.KATAMEROS)
        if not scoped:
            if any(row.get(f) for f in ('coptic_date_key', 'annual_sunday',
                                       'calendar_review_source_locators', 'calendar_review_calendar_keys')):
                raise ValueError('calendar unscoped normalized context')
            return ('', '')
        contexts = {tuple(r.get(f, '') for f in calendar.FIELDS) for r in projected}
        if len(contexts) != 1:
            raise ValueError('calendar source context is ambiguous')
        for field in CALENDAR_FIELDS:
            if row.get(field, '') != projected[0].get(field, ''):
                if field == 'display_label' and row.get(field) == followup.display_label(projected[0]):
                    continue
                raise ValueError('calendar review normalized metadata/evidence drift: ' + field)
        return (projected[0]['coptic_date_key'], projected[0]['annual_sunday'])
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError('calendar review original source malformed') from exc
