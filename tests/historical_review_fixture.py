"""Authenticated 1.3.7 inputs for predecessor-domain contract tests only.

Successor public transport and whole-corpus membership belong to the separate
follow-up integration/release gates, not to these bounded historical fixtures.
"""
import copy
import hashlib
import json
from pathlib import Path

import metadata_followup_repairs as metadata

ROOT = Path(__file__).resolve().parents[1]
POLICY_SHA256 = '8fb0f6e9da2ec1a9c55513e8dfda3fbea9d38d698ebb57e2c5fd622905d791c1'


def published_1_3_7():
    """Do not let a mutation test modify the authenticated loader's cache."""
    frozen = metadata.baseline()
    assert frozen['authentication']['version'] == '1.3.7'
    return copy.deepcopy(frozen)


def historical_policy():
    data = (ROOT / 'sources/lectionary_corrections.json').read_bytes()
    assert hashlib.sha256(data).hexdigest() == POLICY_SHA256
    return json.loads(data)


def immutable_runtime_asset(relative, authentication):
    """Reuse current runtime only while it is byte-identical to the predecessor."""
    data = (ROOT / 'packages/lectionary-data' / relative).read_bytes()
    assert hashlib.sha256(data).hexdigest() == authentication['files']['package/' + relative]
    return data
