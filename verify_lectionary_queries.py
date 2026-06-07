#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import filecmp
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'out'
DATA = OUT / 'data'
SCRIPT = OUT / 'scripts' / 'query_lectionary.py'
REPAIR_REPORT = DATA / 'source_ref_repair_report.csv'
from passage_normalization import extract_text_ref_tokens, parse_passage, passage_matches

SUSPICIOUS_PATTERNS = [
    re.compile(r'\d:.*[—–-]\s*$'),
    re.compile(r':-'),
    re.compile(r'\d:-\d'),
]


def run(cmd: list[str]) -> list[str]:
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True)
    return [line for line in res.stdout.splitlines() if line.strip()]


def assert_no_false_positives():
    john2 = run([sys.executable, str(SCRIPT), '--passage', 'John 2', '--limit', '20'])
    isa5 = run([sys.executable, str(SCRIPT), '--passage', 'Isa 5', '--limit', '20'])
    assert any('Jn 2:1' in line or 'John 2:' in line for line in john2), john2
    assert all('Jn 20' not in line and 'John 20' not in line and 'John 21' not in line and '1Jn 2' not in line and '1John 2' not in line for line in john2), john2
    assert any('Isa 5:' in line or 'Isaiah 5:' in line for line in isa5), isa5
    assert all(not any(bad in line for bad in ['Isa 50', 'Isa 52', 'Isa 53', 'Isa 58']) for line in isa5), isa5
    return {'John 2': john2[:8], 'Isa 5': isa5[:8]}


def assert_required_pascha_genesis_rows():
    checks = {
        'monday_first_hour': run([sys.executable, str(SCRIPT), '--pascha-day', 'Monday', '--hour', 'First Hour', '--limit', '20']),
        'monday_ninth_hour': run([sys.executable, str(SCRIPT), '--pascha-day', 'Monday', '--hour', 'Ninth Hour', '--limit', '20']),
        'tuesday_ninth_hour': run([sys.executable, str(SCRIPT), '--pascha-day', 'Tuesday', '--hour', 'Ninth Hour', '--limit', '20']),
        'wednesday_ninth_hour': run([sys.executable, str(SCRIPT), '--pascha-day', 'Wednesday', '--hour', 'Ninth Hour', '--limit', '20']),
        'great_thursday_ninth_hour': run([sys.executable, str(SCRIPT), '--pascha-day', 'Great Thursday', '--hour', 'Ninth Hour', '--limit', '20']),
        'great_thursday_water': run([sys.executable, str(SCRIPT), '--pascha-day', 'Great Thursday', '--hour', 'Liturgy of Blessing of the Water', '--limit', '20']),
        'good_friday_third_hour': run([sys.executable, str(SCRIPT), '--pascha-day', 'Good Friday', '--hour', 'Third Hour', '--limit', '20']),
        'genesis_18_crosswalk': run([sys.executable, str(SCRIPT), '--passage', 'Genesis 18', '--include-crosswalk', '--limit', '80']),
    }
    assert any('Monday | First Hour | OT1 | Gen 1:1-31; Gen 2:1-3' in line for line in checks['monday_first_hour']), checks['monday_first_hour']
    assert any('Monday | Ninth Hour | OT1 | Gen 2:15-25; Gen 3:1-24' in line for line in checks['monday_ninth_hour']), checks['monday_ninth_hour']
    assert any('Tuesday | Ninth Hour | OT1 | Gen 6:5-9:7' in line for line in checks['tuesday_ninth_hour']), checks['tuesday_ninth_hour']
    assert any('Wednesday | Ninth Hour | OT1 | Gen 24:1-9' in line for line in checks['wednesday_ninth_hour']), checks['wednesday_ninth_hour']
    assert any('Great Thursday | Ninth Hour | OT1 | Gen 22:1-19' in line for line in checks['great_thursday_ninth_hour']), checks['great_thursday_ninth_hour']
    assert any('Great Thursday | Ninth Hour | OT3 | Gen 14:17-20' in line for line in checks['great_thursday_ninth_hour']), checks['great_thursday_ninth_hour']
    assert any('Great Thursday | Liturgy of Blessing of the Water | OT1 | Gen 18:1-23' in line for line in checks['great_thursday_water']), checks['great_thursday_water']
    assert any('Good Friday | Third Hour | OT1 | Gen 48:1-19' in line for line in checks['good_friday_third_hour']), checks['good_friday_third_hour']
    assert any('Great Thursday | Liturgy of Blessing of the Water' in line and 'Gen 18:1-23' in line and 'source=pascha_day_hour' in line for line in checks['genesis_18_crosswalk']), checks['genesis_18_crosswalk']
    assert any('Great Thursday | Liturgy of Blessing of the Water' in line and 'Gen 18:1-23' in line and 'source=pascha_source_text' in line for line in checks['genesis_18_crosswalk']), checks['genesis_18_crosswalk']
    return {k: v[:8] for k, v in checks.items()}


def assert_known_good():
    checks = {
        'isaiah53': run([sys.executable, str(SCRIPT), '--passage', 'Isaiah 53', '--limit', '8']),
        'isa53': run([sys.executable, str(SCRIPT), '--passage', 'Isa 53', '--limit', '8']),
        'cycle_40_5': run([sys.executable, str(SCRIPT), '--cycle-passage', '40.5', '--limit', '8']),
        'cycle_matt_5_1': run([sys.executable, str(SCRIPT), '--cycle-passage', 'Matt 5:1', '--limit', '8']),
        'agpeya_first_hour': run([sys.executable, str(SCRIPT), '--agpeya', 'first hour', '--limit', '8']),
        'pascha_good_friday': run([sys.executable, str(SCRIPT), '--pascha-day', 'Good Friday', '--hour', 'Sixth Hour', '--limit', '8']),
        'pascha_great_thursday': run([sys.executable, str(SCRIPT), '--pascha-day', 'Great Thursday', '--hour', 'Eleventh Hour', '--limit', '8']),
        'pascha_monday_sixth': run([sys.executable, str(SCRIPT), '--pascha-day', 'Monday', '--hour', 'Sixth Hour', '--limit', '8']),
        'pascha_tuesday_sixth': run([sys.executable, str(SCRIPT), '--pascha-day', 'Tuesday', '--hour', 'Sixth Hour', '--limit', '8']),
        'pascha_wednesday_eve_eleventh': run([sys.executable, str(SCRIPT), '--pascha-day', 'Wednesday Eve', '--hour', 'Eleventh Hour', '--limit', '8']),
        'source_text_wisdom_1': run([sys.executable, str(SCRIPT), '--source-text', 'Wisdom 1:1-9', '--limit', '8']),
        'source_text_wisdom_7': run([sys.executable, str(SCRIPT), '--source-text', 'Wisdom 7:24-30', '--limit', '8']),
        'source_text_sirach_4': run([sys.executable, str(SCRIPT), '--source-text', 'Sirach 4:20-5:2', '--limit', '8']),
        'source_text_exodus_32': run([sys.executable, str(SCRIPT), '--source-text', 'Exodus 32:7-15', '--limit', '8']),
        'crosswalk_psalm_62_7': run([sys.executable, str(SCRIPT), '--passage', 'Psalm 62:7', '--include-crosswalk', '--limit', '80']),
        'crosswalk_psalm_18_48': run([sys.executable, str(SCRIPT), '--passage', 'Psalm 18:48', '--include-crosswalk', '--limit', '80']),
        'crosswalk_wisdom_2': run([sys.executable, str(SCRIPT), '--passage', 'Wisdom 2:12-22', '--include-crosswalk', '--limit', '80']),
        'crosswalk_wisdom_7': run([sys.executable, str(SCRIPT), '--passage', 'Wisdom 7:24-30', '--include-crosswalk', '--limit', '80']),
        'chapter_wisdom_7': run([sys.executable, str(SCRIPT), '--chapter', 'Wisdom 7', '--limit', '5']),
        'date_annunciation': run([sys.executable, str(SCRIPT), '--date', '2032-04-07', '--limit', '8']),
        'fallback_cycle_only_default': run([sys.executable, str(SCRIPT), '--passage', '1Cor 10:14-33', '--limit', '8']),
        'fallback_cycle_only_include_crosswalk': run([sys.executable, str(SCRIPT), '--passage', '1Cor 10:14-33', '--include-crosswalk', '--limit', '200']),
        'include_crosswalk': run([sys.executable, str(SCRIPT), '--passage', 'Isaiah 53', '--include-crosswalk', '--limit', '8']),
        'agpeya_crosswalk': run([sys.executable, str(SCRIPT), '--passage', 'John 14:26-15:4', '--include-crosswalk', '--limit', '2000']),
        'palm_procession': run([sys.executable, str(SCRIPT), '--special-service', 'palm sunday procession', '--limit', '80']),
        'palm_vespers': run([sys.executable, str(SCRIPT), '--special-service', 'palm sunday vespers', '--limit', '20']),
        'palm_liturgy': run([sys.executable, str(SCRIPT), '--special-service', 'palm sunday liturgy', '--limit', '80']),
        'palm_station_crosswalk': run([sys.executable, str(SCRIPT), '--passage', 'John 1:43-51', '--include-crosswalk', '--limit', '2000']),
        'chapter_john2': run([sys.executable, str(SCRIPT), '--chapter', 'John 2', '--limit', '5']),
        'chapter_obadiah': run([sys.executable, str(SCRIPT), '--chapter', 'Obadiah 1', '--limit', '5']),
    }
    assert any('Good Friday | Sixth Hour | OT2 | Isa 53:7-12' in line for line in checks['isaiah53']), checks['isaiah53']
    assert any('Good Friday | Sixth Hour | OT2 | Isa 53:7-12' in line for line in checks['isa53']), checks['isa53']
    assert checks['cycle_40_5'], checks['cycle_40_5']
    assert any('Matt 5:1-16' in line or 'Matt 5:1' in line for line in checks['cycle_matt_5_1']), checks['cycle_matt_5_1']
    assert any('First Hour (Prime / Morning Prayer)' in line and 'John 1:1-17' in line for line in checks['agpeya_first_hour']), checks['agpeya_first_hour']
    assert any('Good Friday | Sixth Hour | OT2 | Isa 53:7-12' in line for line in checks['pascha_good_friday']), checks['pascha_good_friday']
    assert any('Great Thursday | Eleventh Hour | OT1 | Isa 52:13-53:12' in line for line in checks['pascha_great_thursday']), checks['pascha_great_thursday']
    assert any('Monday | Sixth Hour | OT2 | Wis 1:1-9' in line for line in checks['pascha_monday_sixth']), checks['pascha_monday_sixth']
    assert any('Tuesday | Sixth Hour | OT1 | Ezek 21:3-13' in line for line in checks['pascha_tuesday_sixth']), checks['pascha_tuesday_sixth']
    assert any('Tuesday | Sixth Hour | OT2 | Sir 4:20-5:2' in line for line in checks['pascha_tuesday_sixth']), checks['pascha_tuesday_sixth']
    assert any('Wednesday Eve | Eleventh Hour | OT1 | Wis 7:24-30' in line for line in checks['pascha_wednesday_eve_eleventh']), checks['pascha_wednesday_eve_eleventh']
    assert any('Monday | Sixth Hour' in line and 'Wis 1:1-9' in line for line in checks['source_text_wisdom_1']), checks['source_text_wisdom_1']
    assert any('Wednesday Eve | Eleventh Hour' in line and 'Wis 7:24-30' in line for line in checks['source_text_wisdom_7']), checks['source_text_wisdom_7']
    assert any('Tuesday | Sixth Hour' in line and 'Sir 4:20-5:2' in line for line in checks['source_text_sirach_4']), checks['source_text_sirach_4']
    assert any('Monday | Sixth Hour' in line and 'Exod 32:7-15' in line for line in checks['source_text_exodus_32']), checks['source_text_exodus_32']
    assert any('Ps 62:7' in line and 'source=pascha_day_hour' in line for line in checks['crosswalk_psalm_62_7']), checks['crosswalk_psalm_62_7']
    assert any('Ps 18:48' in line and 'source=pascha_day_hour' in line for line in checks['crosswalk_psalm_18_48']), checks['crosswalk_psalm_18_48']
    assert any('source=pascha_day_hour' in line or 'source=pascha_source_text' in line for line in checks['crosswalk_wisdom_2']), checks['crosswalk_wisdom_2']
    assert any('source=pascha_day_hour' in line or 'source=pascha_source_text' in line for line in checks['crosswalk_wisdom_7']), checks['crosswalk_wisdom_7']
    assert any('Wis 7' in line and 'read=yes' in line for line in checks['chapter_wisdom_7']), checks['chapter_wisdom_7']
    assert checks['date_annunciation'], checks['date_annunciation']
    assert checks['fallback_cycle_only_default'], checks['fallback_cycle_only_default']
    assert any('source=katameros_cycle' in line for line in checks['fallback_cycle_only_include_crosswalk']), checks['fallback_cycle_only_include_crosswalk']
    assert any('source=pascha_day_hour' in line for line in checks['include_crosswalk']), checks['include_crosswalk']
    assert any('source=agpeya' in line for line in checks['agpeya_crosswalk']), checks['agpeya_crosswalk']
    assert any('procession_station_01_main_sanctuary' in line and 'John 1:43-51' in line for line in checks['palm_procession']), checks['palm_procession']
    assert any('vespers' in line and 'John 12:1-11' in line for line in checks['palm_vespers']), checks['palm_vespers']
    assert any('liturgy_readings' in line and 'Hebrews 9:11-28' in line for line in checks['palm_liturgy']), checks['palm_liturgy']
    assert any('source=special_service' in line and 'procession_station_01_main_sanctuary' in line for line in checks['palm_station_crosswalk']), checks['palm_station_crosswalk']
    assert any('Jn 2' in line and 'read=yes' in line for line in checks['chapter_john2']), checks['chapter_john2']
    assert any('Obad 1' in line for line in checks['chapter_obadiah']), checks['chapter_obadiah']
    return {k: v[:5] for k, v in checks.items()}


def assert_parser_edge_cases():
    assert passage_matches('John 2', 'Jn 20:1-18') is False
    assert passage_matches('John 2', '1Jn 2:1-6') is False
    assert passage_matches('Isa 5', 'Isa 58:1-11') is False
    assert passage_matches('Isa 53', 'Isa 52:13-53:12') is True
    assert parse_passage('Wisdom of Solomon 7:24-30') is not None
    assert parse_passage('Wis 2:12-22') is not None
    assert parse_passage('Sirach 4:20-5:2') is not None
    assert parse_passage('4 Maccabees 1:1-12') is not None
    assert parse_passage('Exod 32:7-15') is not None
    assert parse_passage('Ps 62:7,62:6') is not None
    assert passage_matches('Psalm 62:7', 'Ps 62:7,62:6') is True
    assert passage_matches('Psalm 62:6', 'Ps 62:7,62:6') is True
    assert passage_matches('Psalm 18:48', 'Ps 18:48,18:17') is True
    assert parse_passage('John 3:16--18') is None
    assert parse_passage('Mk 14:-39') is None
    assert parse_passage('John 19:1-') is None
    assert extract_text_ref_tokens('John 19:1- John 19:16') == ['Jn 19:1-16']
    assert extract_text_ref_tokens('Mk 14:-39') == ['Mark 14:39']
    assert extract_text_ref_tokens('Zephaniah 1:14-2:1-2') == ['Zeph 1:14-2:2']
    assert extract_text_ref_tokens('Genesis 1:1-2:1-3') == ['Gen 1:1-2:3']
    assert extract_text_ref_tokens('Isaiah 55:1-13-56:1') == ['Isa 55:1-56:1']
    assert extract_text_ref_tokens('Zechariah 12:11-14:1-3, 6-9') == ['Zech 12:11-14:3,14:6-9']
    return {'status': 'passed'}


def assert_pascha_source_text_fully_parsed():
    rows = list(csv.DictReader((DATA / 'pascha_source_text_index.csv').open(newline='', encoding='utf-8')))
    unparsed = [r for r in rows if r.get('parse_status') != 'parsed' or not r.get('normalized_ref')]
    assert not unparsed, unparsed[:10]
    expected_refs = {
        ('Monday Eve', 'Third Hour', 'Zeph 1:14-2:2'),
        ('Monday', 'First Hour', 'Gen 1:1-2:3'),
        ('Great Thursday', 'Liturgy of Blessing of the Water', 'Isa 55:1-56:1'),
        ('Great Thursday', 'Eleventh Hour', 'Zech 12:11-14:3,14:6-9'),
    }
    actual_refs = {(r.get('day'), r.get('hour'), r.get('normalized_ref')) for r in rows}
    missing = sorted(expected_refs - actual_refs)
    assert not missing, missing
    return {
        'rows': len(rows),
        'parsed_rows': len(rows),
        'unparsed_rows': 0,
        'cross_chapter_repairs_verified': sorted(' | '.join(item) for item in expected_refs),
    }


def assert_four_maccabees_local_absence_documented():
    parsed = parse_passage('4 Maccabees 1:1-12')
    assert parsed is not None and parsed.canonical == '4Macc 1:1-12'
    query_lines = run([sys.executable, str(SCRIPT), '--passage', '4 Maccabees 1:1-12', '--include-crosswalk', '--limit', '10'])
    source_text_lines = run([sys.executable, str(SCRIPT), '--source-text', '4 Maccabees 1:1-12', '--limit', '10'])
    assert query_lines == [], query_lines
    assert source_text_lines == [], source_text_lines
    indexed_hits = []
    for name in [
        'reverse_lookup_crosswalk.csv',
        'pascha_source_text_index.csv',
        'pascha_day_hour_index.csv',
        'katameros_cycle_passage_index.csv',
        'copticchurch_passage_index_2020_2035.csv',
        'special_service_passage_index.csv',
        'agpeya_passage_index.csv',
    ]:
        path = DATA / name
        if not path.exists():
            continue
        rows = list(csv.DictReader(path.open(newline='', encoding='utf-8')))
        hits = [r for r in rows if any(term in ' '.join(str(v) for v in r.values()) for term in ['4Macc', '4 Maccabees'])]
        if hits:
            indexed_hits.append({'file': name, 'hits': len(hits), 'sample': hits[:3]})
    assert not indexed_hits, indexed_hits
    chapter_rows = list(csv.DictReader((DATA / 'bible_chapter_lectionary_index.csv').open(newline='', encoding='utf-8')))
    chapter_one = [r for r in chapter_rows if r.get('book_abbrev') == '4Macc' and r.get('chapter') == '1']
    assert chapter_one and chapter_one[0].get('is_read') == 'no' and chapter_one[0].get('occurrence_count') == '0', chapter_one
    return {
        'parser_canonical': parsed.canonical,
        'query_rows': 0,
        'source_text_rows': 0,
        'indexed_source_hits': 0,
        'chapter_index_status': chapter_one[0],
        'classification': 'verified_absent_from_local_lectionary_sources_not_parser_gap',
    }


def assert_malformed_refs_accounted_for():
    report = {}
    repair_rows = list(csv.DictReader(REPAIR_REPORT.open(newline='', encoding='utf-8'))) if REPAIR_REPORT.exists() else []
    repair_raw_refs = {r.get('raw_ref','') for r in repair_rows}
    assert repair_rows, 'Expected source_ref_repair_report.csv to account for repaired source refs'
    for name in ['copticchurch_date_readings_2020_2035.csv', 'copticchurch_passage_index_2020_2035.csv', 'reverse_lookup_crosswalk.csv']:
        path = DATA / name
        rows = list(csv.DictReader(path.open(newline='', encoding='utf-8')))
        normalized_bad = []
        raw_bad = []
        for row in rows:
            normalized_text = row.get('matched_ref') or row.get('passage') or row.get('normalized_ref') or ''
            raw_text = row.get('raw_ref') or row.get('source_ref') or ''
            if any(p.search(normalized_text) for p in SUSPICIOUS_PATTERNS):
                normalized_bad.append(normalized_text)
            if raw_text and any(p.search(raw_text) for p in SUSPICIOUS_PATTERNS):
                raw_bad.append(raw_text)
        assert not normalized_bad, {'file': name, 'normalized_sample': normalized_bad[:10]}
        unreported = sorted(set(raw_bad) - repair_raw_refs)
        assert not unreported, {'file': name, 'unreported_raw_suspicious_refs': unreported[:10]}
        report[name] = {
            'rows': len(rows),
            'normalized_suspicious_count': 0,
            'raw_suspicious_count': len(raw_bad),
        }
    report['source_ref_repair_report.csv'] = {'rows': len(repair_rows)}
    return report


def assert_artifacts_exist():
    required = [
        DATA / 'copticchurch_date_readings_2020_2035.csv',
        DATA / 'copticchurch_passage_index_2020_2035.csv',
        DATA / 'katameros_cycle_readings.csv',
        DATA / 'katameros_cycle_passage_index.csv',
        DATA / 'reverse_lookup_crosswalk.csv',
        DATA / 'reverse_lookup_summary.csv',
        DATA / 'pascha_day_hour_index.csv',
        DATA / 'pascha_source_text_index.csv',
        DATA / 'bright_saturday_service_order.csv',
        DATA / 'agpeya_hour_readings.csv',
        DATA / 'agpeya_passage_index.csv',
        DATA / 'bible_chapter_lectionary_index.csv',
        DATA / 'bible_chapter_lectionary_occurrences.csv',
        DATA / 'source_ref_repair_report.csv',
        SCRIPT,
    ]
    missing = [str(p) for p in required if not p.exists()]
    assert not missing, missing
    assert filecmp.cmp(ROOT / 'passage_normalization.py', OUT / 'scripts' / 'passage_normalization.py', shallow=False), 'out/scripts/passage_normalization.py drifted from source'
    assert filecmp.cmp(ROOT / 'query_lectionary.py', OUT / 'scripts' / 'query_lectionary.py', shallow=False), 'out/scripts/query_lectionary.py drifted from source'
    return [str(p) for p in required]


def main() -> None:
    summary = {
        'artifacts': assert_artifacts_exist(),
        'false_positive_checks': assert_no_false_positives(),
        'required_pascha_genesis_rows': assert_required_pascha_genesis_rows(),
        'known_good_checks': assert_known_good(),
        'parser_edge_cases': assert_parser_edge_cases(),
        'pascha_source_text_fully_parsed': assert_pascha_source_text_fully_parsed(),
        'four_maccabees_local_absence': assert_four_maccabees_local_absence_documented(),
        'malformed_ref_checks': assert_malformed_refs_accounted_for(),
    }
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
