"""Authenticate retained Reader evidence for three already-decided Pascha repairs.

``authenticate_pascha_evidence(key) -> dict`` accepts ONLY the exact strings
``good_friday_twelfth``, ``hosanna_sunday_day_ninth``, ``bright_saturday_matins``.
It rereads the hash-pinned manifest, full document and every associated companion
on every call and raises ValueError on missing, altered or rebound evidence.
The returned fresh dictionary contains repository-relative ``path``, ``sha256``,
``locator``, literal ``readings`` with one-based line bounds, ``selected_context``,
``navigation``, ``service_day``, ``service_hour`` and ``qualification_notes``.

This is an evidence guard, NOT an appointment loader or row-identity validator.
Callers must bind their own exact source/kind/day/hour/reference allowlists and
carry the qualification through provenance and public disclosure. No mutable
caller root, source path, reference or metadata is accepted. Original absolute
capture paths are provenance labels only: they are never opened. No live app,
external archive, package upgrade, canonicalization or source approval is implied.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath


_ROOT = Path(__file__).resolve().parent
_SOURCE = 'sources/coptic-reader/pascha-resolution-qualified-2026-10-25'
MANIFEST_SHA256 = '5e9db07bd940ba9fbdf0a94b72543e93c1db013bedc2695a461b33e7d308573f'
_KEYS = ('good_friday_twelfth', 'hosanna_sunday_day_ninth', 'bright_saturday_matins')


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _read_relative(relative):
    """Reject escapes and symlinks, including identical-byte external targets."""
    if type(relative) is not str or not relative or '\\' in relative:
        raise ValueError('Pascha evidence path is not a literal repository-relative path')
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or str(path) != relative:
        raise ValueError('Pascha evidence path escape or normalization')
    target = _ROOT
    for part in path.parts:
        # Enumerating literal names also rejects case rebinding on macOS.
        if part not in {entry.name for entry in target.iterdir()}:
            raise ValueError('Pascha evidence literal path missing: ' + relative)
        target = target / part
        if target.is_symlink():
            raise ValueError('Pascha evidence symlink path rejected: ' + relative)
    if not target.resolve().is_relative_to(_ROOT) or not target.is_file():
        raise ValueError('Pascha evidence path escapes repository or is not a file')
    return target.read_bytes()


def _asset(record):
    relative = record['file']
    raw = _read_relative(_SOURCE + '/' + relative)
    if len(raw) != record['bytes'] or _sha(raw) != record['sha256']:
        raise ValueError('Pascha evidence full capture/companion authentication failed: ' + relative)
    return raw


def authenticate_pascha_evidence(key) -> dict:
    """Return authenticated local-source metadata; reject unknown keys or drift.

    ``path`` and companion ``path`` are repository-relative. ``locator`` includes
    the full-capture SHA-256 and reading line bounds. ``capture_time`` and
    ``app_version`` remain None: selected dates/live-clock labels do not establish
    either. Authentication grants no new appointment or activation permission.
    """
    if type(key) is not str or key not in _KEYS:
        raise ValueError('Unknown Pascha evidence key (exact allowlist required)')
    try:
        raw = _read_relative(_SOURCE + '/source-manifest.json')
        if _sha(raw) != MANIFEST_SHA256:
            raise ValueError('Pascha evidence manifest authentication failed')
        manifest = json.loads(raw)
        if (manifest['schema'] != 'retained_pascha_resolution_evidence_v1'
                or set(manifest['documents']) != set(_KEYS)
                or manifest['fresh_app_verification'] is not False
                or manifest['new_appointment_approval'] is not False
                or manifest['retention_label_is_capture_date'] is not False
                or manifest['app_version'] is not None or manifest['capture_time'] is not None):
            raise ValueError('Pascha evidence scope/qualification drift')
        document = manifest['documents'][key]
        lines = _asset(document).decode('utf-8').splitlines()
        if (document['full_rendered_text'] is not True
                or len(lines) != document['line_count']
                or lines[0] != document['document_title']):
            raise ValueError('Pascha evidence document title/completeness drift')
        for reading in document['readings']:
            heading = reading['heading_line']
            first = reading['body_first_line']
            last = reading['body_last_line']
            if not 1 <= heading < first <= last <= len(lines):
                raise ValueError('Pascha evidence reading bounds invalid')
            body = '\n'.join(lines[first - 1:last]).encode('utf-8')
            if (lines[heading - 1] != reading['heading_exact']
                    or lines[first - 1] != reading['body_opening_exact']
                    or lines[last - 1] != reading['body_closing_exact']
                    or _sha(body) != reading['body_sha256']):
                raise ValueError('Pascha evidence literal reading/context rebinding')
        companions = []
        for companion in document['companions']:
            data = _asset(companion)
            if 'line_count' in companion:
                context = data.decode('utf-8').splitlines()
                if (len(context) != companion['line_count']
                        or context[0] != companion['first_line_exact']):
                    raise ValueError('Pascha evidence companion context truncation')
            companions.append({**companion, 'path': _SOURCE + '/' + companion['file']})
        if key == 'good_friday_twelfth' and 'jonah' in '\n'.join(lines).casefold():
            raise ValueError('Pascha Good Friday scoped Jonah absence contradicted')
        path = _SOURCE + '/' + document['file']
        ranges = ','.join(str(r['heading_line']) + '-' + str(r['body_last_line'])
                          for r in document['readings'])
        return {**document, 'key': key, 'path': path,
                'locator': path + ':lines ' + ranges + '; sha256=' + document['sha256'],
                'manifest_path': _SOURCE + '/source-manifest.json',
                'manifest_sha256': MANIFEST_SHA256, 'companions': companions,
                'source_url': manifest['source_url'], 'app_version': None,
                'capture_time': None, 'fresh_app_verification': False,
                'new_appointment_approval': False}
    except (OSError, KeyError, IndexError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('Pascha evidence missing or malformed') from exc
