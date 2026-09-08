"""Validate the public catalog against the frozen audited-source fingerprint fixture."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = 'tout baba hatour kiahk toba amshir baramhat baramouda bashans paona abib mesra nasie'.split()
RECORD_FIELDS = {'id', 'title', 'type', 'rank', 'displayOrder', 'displayGroupId'}
DAY_FIELDS = {'commemorations', 'validInCommonYear', 'validInLeapYear'}

def validate_synaxarium_integrity(package_dir):
    failures = []
    def fail(reason, **details): failures.append(dict(reason=reason, **details))
    try:
        data = json.loads((Path(package_dir) / 'data/synaxarium/synaxarium.json').read_text())
        expected = json.loads((ROOT / 'tests/fixtures/synaxarium-1743.json').read_text())['days']
    except (OSError, ValueError, KeyError) as exc:
        return {'status': 'fail', 'failures': [{'reason': 'unreadable_catalog_or_source_fixture', 'error': str(exc)}]}
    keys = {f'{m}-{d}' for m in SLUGS for d in range(1, 7 if m == 'nasie' else 31)}
    if not isinstance(data, dict):
        return {'status': 'fail', 'failures': [{'reason': 'catalog_not_object'}]}
    if set(data) != keys: fail('missing_or_invalid_days', missing=sorted(keys-set(data)), extra=sorted(set(data)-keys))
    if set(expected) != keys: fail('invalid_source_fixture')
    ids = set()
    count = 0
    for key, value in data.items():
        if not isinstance(value, dict) or set(value) != DAY_FIELDS:
            fail('invalid_day_fields', day=key)
            continue
        if value['validInCommonYear'] is not (key != 'nasie-6') or value['validInLeapYear'] is not True:
            fail('invalid_year_validity', day=key)
        rows = value['commemorations']
        if not isinstance(rows, list):
            fail('commemorations_not_array', day=key)
            continue
        count += len(rows)
        reference = expected.get(key, {})
        if len(rows) != reference.get('count'): fail('source_day_count_mismatch', day=key)
        digest = hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        if digest != reference.get('sha256'): fail('source_projection_mismatch', day=key)
        for ordinal, row in enumerate(rows, 1):
            if not isinstance(row, dict) or set(row) != RECORD_FIELDS:
                fail('invalid_record_fields', day=key, ordinal=ordinal)
                continue
            identity = row['id']
            if not isinstance(identity, str) or not identity:
                fail('invalid_id', day=key)
            elif identity in ids:
                fail('duplicate_id', day=key, id=identity)
            else:
                ids.add(identity)
            if not isinstance(row['title'], str) or not row['title'].strip(): fail('invalid_title', day=key)
            if not isinstance(row['type'], str) or row['type'] not in {'departure', 'martyrdom', 'feast', 'commemoration'}: fail('invalid_type', day=key)
            if type(row['rank']) is not int or type(row['displayOrder']) is not int or row['rank'] != ordinal or row['displayOrder'] != ordinal:
                fail('invalid_display_priority', day=key)
            if row['displayGroupId'] is not None: fail('unaudited_grouping', day=key)
    if count != 868: fail('total_not_868', actual=count)
    return {'status': 'fail' if failures else 'pass', 'day_count': len(data), 'total_commemorations': count, 'unique_ids': len(ids), 'failures': failures}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package-dir', type=Path, default=ROOT / 'packages/lectionary-data')
    result = validate_synaxarium_integrity(parser.parse_args().package_dir)
    print(json.dumps(result, indent=2))
    return int(result['status'] != 'pass')

if __name__ == '__main__':
    raise SystemExit(main())
