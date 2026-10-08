"""One-shot evidence reuse: verify original hashes/context BEFORE copying a fixture."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path('/Users/ga/workspace/lectionary-comprehensive-audit-2026-10-07')
RAW = AUDIT / 'fresh-ordinary'
ID = 'exception-2028-04-07'
DEST = ROOT / 'sources/coptic-reader/last-friday-2028-04-07-2026-10-07'
if DEST.exists():
    raise SystemExit('One-shot evidence reuse refuses to overwrite an existing fixture directory')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
oracle = next(json.loads(x) for x in (AUDIT / 'ordinary-oracle-review/corrected-oracle.jsonl').read_text().splitlines() if json.loads(x)['id'] == ID)
entries = [json.loads(x) for x in (RAW / 'evidence.jsonl').read_text().splitlines() if json.loads(x).get('context') == ID]
contexts = [next(e for e in reversed(entries) if e['label'] == name) for name in ['home-selected', 'picker-selected']]
accepted = contexts + oracle['documents']
ledger = []
for doc in accepted:
    assert doc['date'] == '2028-04-07' and doc['context'] == ID
    for key, hashkey in [('textPath', 'textSha256'), ('screenshotPath', 'screenshotSha256')]:
        path = RAW / doc[key]
        assert sha(path) == doc[hashkey], str(path)
        ledger.append({'file': path.name, 'sha256': sha(path), 'original_path': str(path), 'capture': doc['capturedAt']})
home = (RAW / ID / 'home-selected.txt').read_text()
assert home.startswith('Selected Season Last Friday of Great Fast Paremhotep 29, 1744 Friday, April 7, 2028')
assert oracle['date'] == '2028-04-07' and oracle['homeContext'] == home.strip()
assert len(oracle['orderedAssignedOccurrences']) == 11
for doc in oracle['documents']:
    refs = [line.strip() for line in (RAW / doc['textPath']).read_text().splitlines() if re.fullmatch(r'\t(?:[1-3] )?[A-Za-z ]+ \d+:.*', line)]
    assert refs == doc['printedReferences'], doc['label']
assert 'Vespers and Vesper Praises are not prayed' in (RAW / ID / 'Vespers.txt').read_text()
assert 'weekdays of the Great Fast' in (RAW / ID / 'Vespers.txt').read_text()
# Only copy after every primary evidence assertion succeeds.
DEST.mkdir(parents=True, exist_ok=True)
for item in ledger:
    shutil.copyfile(item['original_path'], DEST / item['file'])
(DEST / 'capture-manifest.json').write_text(json.dumps(accepted, indent=2, ensure_ascii=False) + '\n')
(DEST / 'independent-oracle.json').write_text(json.dumps(oracle, indent=2, ensure_ascii=False) + '\n')
# Actual retrieved canonical verse witnesses, not synthesized API responses.
normalizations = []
for chapter in [32, 98]:
    url = f'https://www.biblegateway.com/passage/?search=Psalm+{chapter}&version=NKJV'
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    passage = soup.select_one('.passage-text')
    assert passage is not None
    for el in passage.select('.crossrefs, .footnotes, .crossreference, .footnote'):
        el.decompose()
    text = passage.get_text(' ', strip=True)
    path = DEST / f'nkjv-psalm-{chapter}.txt'
    path.write_text(text + '\n')
    normalizations.append({'url': url, 'path': path.name, 'sha256': sha(path), 'convention': 'mt_nkjv'})
text32 = (DEST / 'nkjv-psalm-32.txt').read_text()
text98 = (DEST / 'nkjv-psalm-98.txt').read_text()
assert '10' in text32 and 'mercy shall surround him' in text32 and '11' in text32 and 'upright in heart' in text32
assert re.search(r'8 Let the rivers clap their hands; Let the hills be joyful together 9 before the Lord', text98)
normalized = ['Gen 49:33-50:26', 'Prov 11:27-12:22', 'Isa 66:10-24', 'Job 42:7-17', 'Ps 32:10-11', 'Lk 16:19-31', '2Tim 3:1-4:5', 'James 5:7-16', 'Acts 15:1-18', 'Ps 98:8-9', 'Lk 13:31-35']
types = ['Prophecy'] * 4 + ['Psalm', 'Gospel', 'Pauline Epistle', 'Catholic Epistle', 'Acts', 'Psalm', 'Gospel']
readings = []
for i, (occ, norm, reading_type) in enumerate(zip(oracle['orderedAssignedOccurrences'], normalized, types), 1):
    service = occ['slot'].split('-')[0]
    doc = next(d for d in oracle['documents'] if d['label'] == occ['slot'])
    row = dict(service_section=service, reading_type=reading_type, printed_ref=occ['printed_reference'], normalized_ref=norm,
               source_order=i, source_slot=f'OT{i}' if i <= 4 else reading_type,
               evidence=Path(doc['textPath']).name, heading_order=occ['heading_order'])
    if reading_type == 'Psalm':
        row.update(source_convention='coptic_reader_printed_liturgical', canonicalization_confidence='confirmed_text_aligned',
                   canonicalization_note=('Coptic Reader wording corresponds to NKJV Psalm 32:10-11, not printed verses 11-12; wording differs (scourges/sorrows, sinner/wicked).' if i == 5 else 'Coptic Reader excerpt corresponds to NKJV Psalm 98:8b-9; the rivers clause in 8a is not sung. Canonical full-verse coverage is 98:8-9, not a claim that all verse 8 is sung.'),
                   normalization_evidence=f'nkjv-psalm-{32 if i == 5 else 98}.txt')
    readings.append(row)
fixture = dict(schema_version=1, verified_date='2028-04-07', coptic_date='Paremhotep 29, 1744', occasion='Last Friday of Great Fast',
               day_title='Friday of the seventh week of Great Lent', pascha_offset_days=-9, feast_collision='Annunciation',
               coverage_scope='last_friday_annunciation_collision_only', suppressed_service='Vespers',
               recurring_prophecy_context={'day_title': 'Friday of the seventh week of Great Lent', 'pascha_offset_days': -9, 'requires_feast_collision': 'Annunciation', 'source_document': 'Matins-Prophecies.txt'},
               normalization_witnesses=normalizations,
               source_fingerprints={p.name: sha(p) for p in sorted(DEST.iterdir()) if p.is_file()}, readings=readings)
(DEST / 'verified-table.json').write_text(json.dumps(fixture, indent=2, ensure_ascii=False) + '\n')
(ROOT / 'audit_artifacts/calendar-boundary-integration/capture-verification.json').write_text(json.dumps({'status': 'verified_before_fixture_copy', 'selected_date': '2028-04-07', 'coptic_date': fixture['coptic_date'], 'occasion': fixture['occasion'], 'assigned_occurrences': len(readings), 'files': ledger, 'normalization_witnesses': normalizations, 'visual_review': ['home/date/occasion verified', 'ready Prophecies Genesis 49:33-50:26 verified', 'explicit no Vespers rubric verified']}, indent=2) + '\n')
print('Verified', len(ledger), 'original raw/text screenshot hashes;', len(readings), 'ordered readings; two fetched Psalm verse witnesses.')
