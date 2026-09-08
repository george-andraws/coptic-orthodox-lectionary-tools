"""Project audited 1743 titles. Private source captures never enter the npm package."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = 'tout baba hatour kiahk toba amshir baramhat baramouda bashans paona abib mesra nasie'.split()
ALIASES = {'hator': 'hatour', 'epep': 'abib'}

def normalized(key):
    month, day = key.split('-')
    return f'{ALIASES.get(month, month)}-{day}'

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def project(catalog, index):
    data = {f'{m}-{d}': {'commemorations': [], 'validInCommonYear': not (m == 'nasie' and d == 6), 'validInLeapYear': True}
            for m in SLUGS for d in range(1, 7 if m == 'nasie' else 31)}
    for record in catalog:
        key = normalized(record['coptic_day'])
        ordinal = record['ordinal_in_capture']
        data[key]['commemorations'].append(dict(id=record['opaque_id'], title=record['canonical_display_title'], type=record['type'], rank=ordinal, displayOrder=ordinal, displayGroupId=None))
    assert len(index) == 366 and len(catalog) == 868
    assert len({r['opaque_id'] for r in catalog}) == 868
    evidence = {}
    for source_key, captured in index.items():
        key = normalized(source_key)
        rows = data[key]['commemorations']
        rows.sort(key=lambda r: r['displayOrder'])
        assert [r['title'] for r in rows] == captured['commemoration_headings'], key
        assert [r['displayOrder'] for r in rows] == list(range(1, len(rows) + 1)), key
        assert captured['coptic_year'] == 1743 and captured['target_year_verified'] is True
        evidence[key] = {'count': len(rows), 'sha256': fingerprint(data[key]), 'civil_date': captured['civil_date']}
    return data, evidence

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_dir', type=Path)
    args = parser.parse_args()
    catalog_path = args.source_dir / 'synaxarium_from_coptic_reader.jsonl'
    index_path = args.source_dir / 'coptic_reader_index.json'
    data, days = project([json.loads(line) for line in catalog_path.read_text().splitlines()], json.loads(index_path.read_text()))
    output = ROOT / 'packages/lectionary-data/data/synaxarium/synaxarium.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    fixture = ROOT / 'tests/fixtures/synaxarium-1743.json'
    fixture.parent.mkdir(parents=True, exist_ok=True)
    fixture.write_text(json.dumps({'catalog_sha256': hashlib.sha256(catalog_path.read_bytes()).hexdigest(), 'index_sha256': hashlib.sha256(index_path.read_bytes()).hexdigest(), 'days': days}, indent=2) + '\n')
    print(json.dumps({'days': len(days), 'commemorations': sum(d['count'] for d in days.values())}))

if __name__ == '__main__':
    main()
