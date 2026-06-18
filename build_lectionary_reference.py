#!/usr/bin/env python3
"""Build local Coptic Orthodox lectionary reference data from source materials.

Sources used:
- pierresaid/katameros-api SQLite database for annual, Sunday, Great Lent, and Pentecost cycle tables.
- copticchurch.net daily readings pages for date-resolved Gregorian examples.
- Downloaded Katameros PDFs and extracted text are copied beside outputs for Pascha/Holy Week and cross-checking.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

from passage_normalization import (
    canonicalize_text_ref,
    extract_text_ref_tokens,
    iter_numeric_ref_segments,
    normalize_numeric_ref,
    repair_source_ref,
    is_numeric_query,
    passage_matches,
    source_ref_status,
)

WORK = Path(__file__).resolve().parent
SRC = WORK / 'sources'
DB = SRC / 'katameros-api' / 'Core' / 'KatamerosDatabase.db'
PDFS = SRC / 'pdfs'
OUT = WORK / 'out'
DATA = OUT / 'data'
SOURCES_OUT = OUT / 'sources'
SCRIPTS = OUT / 'scripts'
VAULT_PACKAGE = Path('/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference')


def env_flag(name: str) -> bool:
    return os.environ.get(name, '').strip().lower() in {'1', 'true', 'yes', 'on'}


DISABLE_VAULT_PUBLISH = env_flag('LECTIONARY_DISABLE_VAULT_PUBLISH')


def normalize_copticchurch_title(value: str) -> str:
    return (value or '').replace('Fast of Ninevah', 'Fast of Nineveh')


READING_COLUMNS = [
    ('vespers_psalm', 'V_Psalm_Ref'),
    ('vespers_gospel', 'V_Gospel_Ref'),
    ('matins_psalm', 'M_Psalm_Ref'),
    ('matins_gospel', 'M_Gospel_Ref'),
    ('liturgy_pauline', 'P_Gospel_Ref'),
    ('liturgy_catholic', 'C_Gospel_Ref'),
    ('liturgy_acts', 'X_Gospel_Ref'),
    ('liturgy_psalm', 'L_Psalm_Ref'),
    ('liturgy_gospel', 'L_Gospel_Ref'),
]


def correction_key(day_title: str, service_section: str, reading_type: str, raw_ref: str) -> tuple[str, str, str, str]:
    cleaned_ref = repair_source_ref(raw_ref)
    cleaned_ref = re.sub(r'\s+', ' ', cleaned_ref).strip()
    return (
        re.sub(r'\s+', ' ', (day_title or '').strip()).casefold(),
        re.sub(r'\s+', ' ', (service_section or '').strip()).casefold(),
        re.sub(r'\s+', ' ', (reading_type or '').strip()).casefold(),
        cleaned_ref.casefold(),
    )


COPTICCHURCH_SOURCE_CORRECTIONS = {
    correction_key('Saturday of the fourth week of Great Lent', 'Liturgy', 'Psalm', 'Psalm 61:1  &  Psalm 610:5'): {
        'normalized_ref': 'Psalm 61:1,5',
        'normalization_warning': 'source_corrected_from_katameros_api_2026_06_18; live API returned Ps 61:1,5',
    },
    correction_key('Abib 21', 'Matins', 'Gospel', 'Mk 19:9-13'): {
        'normalized_ref': 'Mark 13:9-13',
        'normalization_warning': 'source_corrected_from_katameros_api_2026_06_18; live API returned Mark 13:9-13',
    },
    correction_key('Mesra 23', 'Liturgy', 'Pauline Epistle', 'Rom 8:28:39'): {
        'normalized_ref': 'Rom 8:28-39',
        'normalization_warning': 'source_corrected_from_katameros_api_2026_06_18; live API returned Rom 8:28-39',
    },
    correction_key('Mesra 27', 'Liturgy', 'Pauline Epistle', 'Rom 8:28:39'): {
        'normalized_ref': 'Rom 8:28-39',
        'normalization_warning': 'source_corrected_from_katameros_api_2026_06_18; live API returned Rom 8:28-39',
    },
    correction_key('Mesra 25', 'Liturgy', 'Acts of the Apostles', 'Acts 18:24-  &  Acts 9:1-6'): {
        'normalized_ref': 'Acts 18:24-28; Acts 19:1-6',
        'normalization_warning': 'source_corrected_from_katameros_api_2026_06_18; live API returned Acts 18:24-28 and Acts 19:1-6',
    },
    correction_key('Mesra 29', 'Liturgy', 'Acts of the Apostles', 'Acts 5:34:42'): {
        'normalized_ref': 'Acts 5:34-42',
        'normalization_warning': 'source_corrected_from_katameros_api_2026_06_18; live API returned Acts 5:34-42',
    },
}


def apply_copticchurch_source_correction(row: dict) -> dict:
    key = correction_key(
        row.get('day_title', ''),
        row.get('service_section', ''),
        row.get('reading_type', ''),
        row.get('raw_ref', ''),
    )
    correction = COPTICCHURCH_SOURCE_CORRECTIONS.get(key)
    if not correction:
        return row
    row = dict(row)
    row['normalized_ref'] = correction['normalized_ref']
    row['parse_status'] = 'source_corrected'
    row['normalization_warning'] = correction['normalization_warning']
    return row


def ensure_dirs():
    for p in [OUT, DATA, SOURCES_OUT, SCRIPTS]:
        p.mkdir(parents=True, exist_ok=True)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def load_books() -> Dict[int, str]:
    con = sqlite3.connect(DB)
    rows = con.execute('select Id, Name from Books').fetchall()
    con.close()
    return {int(i): n for i, n in rows}



def export_cycle_tables(books: Dict[int, str]) -> List[dict]:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows_out = []
    table_specs = [
        ('AnnualReadings', 'annual fixed Coptic day'),
        ('SundayReadings', 'annual Sundays by Coptic month/week'),
        ('GreatLentReadings', 'Great Lent/Jonah/Nineveh cycle'),
        ('PentecostReadings', 'Holy Fifty Days/Pentecost cycle'),
    ]
    for table, source_type in table_specs:
        for row in con.execute(f'select * from {table}'):
            base = dict(row)
            if table in ('AnnualReadings','SundayReadings'):
                day_key = f"{base.get('Month_Name')} {base.get('Day')}"
                cycle = table.replace('Readings','')
            else:
                day_key = f"week {base.get('Week')} day_of_week {base.get('DayOfWeek')}"
                cycle = table.replace('Readings','')
            for slot, col in READING_COLUMNS:
                raw = (base.get(col) or '').strip()
                if not raw:
                    continue
                rows_out.append({
                    'source': 'katameros-api sqlite',
                    'source_table': table,
                    'source_type': source_type,
                    'cycle': cycle,
                    'day_key': day_key,
                    'month_number': base.get('Month_Number',''),
                    'month_name': base.get('Month_Name',''),
                    'day': base.get('Day',''),
                    'week': base.get('Week',''),
                    'day_of_week': base.get('DayOfWeek',''),
                    'day_name': base.get('DayName') or '',
                    'season': base.get('Season') or base.get('Seasonal_Tune') or '',
                    'other': base.get('Other') or '',
                    'reading_slot': slot,
                    'raw_ref': raw,
                    'normalized_ref': normalize_numeric_ref(raw, books),
                })
            if table == 'GreatLentReadings' and (base.get('Prophecy') or '').strip():
                raw = base.get('Prophecy').strip()
                rows_out.append({
                    'source': 'katameros-api sqlite',
                    'source_table': table,
                    'source_type': source_type,
                    'cycle': cycle,
                    'day_key': day_key,
                    'month_number': '', 'month_name': '', 'day': '',
                    'week': base.get('Week',''), 'day_of_week': base.get('DayOfWeek',''),
                    'day_name': base.get('DayName') or '',
                    'season': base.get('Seasonal_Tune') or '', 'other': '',
                    'reading_slot': 'prophecy',
                    'raw_ref': raw,
                    'normalized_ref': normalize_numeric_ref(raw, books),
                })
    con.close()
    return rows_out

def write_csv(path: Path, rows: List[dict], fieldnames: Optional[List[str]]=None):
    if not fieldnames:
        keys=[]
        for r in rows:
            for k in r.keys():
                if k not in keys: keys.append(k)
        fieldnames=keys
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader(); w.writerows(rows)

def write_jsonl(path: Path, rows: List[dict]):
    with path.open('w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True)+'\n')

def build_passage_index(cycle_rows: List[dict], books: Dict[int, str]) -> List[dict]:
    out=[]
    for r in cycle_rows:
        for seg in iter_numeric_ref_segments(r.get('raw_ref',''), books) or []:
            out.append({**seg, **{k:r.get(k,'') for k in ['source','source_table','source_type','cycle','day_key','month_number','month_name','day','week','day_of_week','day_name','season','other','reading_slot','raw_ref','normalized_ref']}})
    return out

def parse_copticchurch_html(html: str, date: dt.date) -> Tuple[dict, List[dict]]:
    soup = BeautifulSoup(html, 'html.parser')
    title = normalize_copticchurch_title(soup.title.get_text(' ', strip=True) if soup.title else '')
    content = soup.select_one('.col-lg-9') or soup.body
    headings = content.find_all(['h1','h2','h3','h4','h5']) if content else []
    day_title = ''
    if len(headings) >= 2 and headings[1].name == 'h2':
        day_title = normalize_copticchurch_title(headings[1].get_text(' ', strip=True))
    section = ''
    reading_type = ''
    out=[]
    for h in headings:
        text = normalize_copticchurch_title(h.get_text(' ', strip=True))
        if h.name == 'h2':
            # Ignore day title if first h2, otherwise this is service section/hour.
            if text != day_title:
                section = text
        elif h.name == 'h4':
            reading_type = text
        elif h.name == 'h5' and reading_type:
            ref = text
            if not ref or ref.lower().startswith('readings for'):
                continue
            parse_status, normalization_warning, repaired_ref = source_ref_status(ref)
            row = {
                'source':'copticchurch.net daily scrape',
                'gregorian_date': date.isoformat(),
                'weekday': date.strftime('%A'),
                'day_title': day_title,
                'service_section': section,
                'reading_type': reading_type,
                'raw_ref': ref,
                'normalized_ref': repaired_ref,
                'parse_status': parse_status,
                'normalization_warning': normalization_warning,
                'url': f'https://copticchurch.net/readings?g_year={date.year}&g_month={date.month:02d}&g_day={date.day:02d}'
            }
            out.append(apply_copticchurch_source_correction(row))
    meta={'date':date.isoformat(),'title':title,'day_title':day_title,'reading_count':len(out)}
    return meta,out

def fetch_date(date: dt.date, cache: Path) -> Tuple[dict,List[dict]]:
    fp = cache / f'{date.isoformat()}.html'
    if fp.exists() and fp.stat().st_size > 1000:
        html = fp.read_text(encoding='utf-8', errors='ignore')
    else:
        url=f'https://copticchurch.net/readings?g_year={date.year}&g_month={date.month:02d}&g_day={date.day:02d}'
        r=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Hermes local lectionary cache)'},timeout=20)
        r.raise_for_status()
        html=r.text
        fp.write_text(html,encoding='utf-8')
        time.sleep(0.05)
    return parse_copticchurch_html(html,date)

def scrape_copticchurch(start_year=2020, end_year=2035):
    cache = WORK / 'cache' / 'copticchurch_html'
    cache.mkdir(parents=True, exist_ok=True)
    dates=[]
    d=dt.date(start_year,1,1)
    end=dt.date(end_year,12,31)
    while d<=end:
        dates.append(d); d += dt.timedelta(days=1)
    metas=[]; rows=[]; errors=[]
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs={ex.submit(fetch_date,d,cache):d for d in dates}
        for i,fut in enumerate(as_completed(futs),1):
            d=futs[fut]
            try:
                m,r=fut.result()
                metas.append(m); rows.extend(r)
            except Exception as e:
                errors.append({'date':d.isoformat(),'error':repr(e)})
            if i % 500 == 0:
                print(f'fetched/parsed {i}/{len(dates)}')
    metas.sort(key=lambda x:x['date'])
    rows.sort(key=lambda x:(x['gregorian_date'],x['service_section'],x['reading_type'],x['raw_ref']))
    return metas, rows, errors

def build_date_passage_index(rows: List[dict]) -> List[dict]:
    out=[]
    repaired_report=[]
    for r in rows:
        ref_for_extract = r.get('normalized_ref') or r.get('raw_ref','')
        for token in extract_text_ref_tokens(ref_for_extract):
            out.append({
                'source': r['source'],
                'gregorian_date': r['gregorian_date'],
                'weekday': r['weekday'],
                'day_title': r['day_title'],
                'service_section': r['service_section'],
                'reading_type': r['reading_type'],
                'matched_ref': canonicalize_text_ref(token),
                'raw_ref': r['raw_ref'],
                'source_ref_status': r.get('parse_status','ok'),
                'normalization_warning': r.get('normalization_warning',''),
                'url': r['url'],
            })
        if r.get('parse_status') and r.get('parse_status') != 'ok':
            repaired_report.append({
                'gregorian_date': r.get('gregorian_date',''),
                'day_title': r.get('day_title',''),
                'service_section': r.get('service_section',''),
                'reading_type': r.get('reading_type',''),
                'raw_ref': r.get('raw_ref',''),
                'repaired_ref': r.get('normalized_ref',''),
                'source_ref_status': r.get('parse_status',''),
                'normalization_warning': r.get('normalization_warning',''),
                'url': r.get('url',''),
            })
    if repaired_report:
        write_csv(DATA/'source_ref_repair_report.csv', repaired_report)
        write_jsonl(DATA/'source_ref_repair_report.jsonl', repaired_report)
    return out

def copy_sources():
    # Copy database and PDFs/TXT sources into local source folder.
    shutil.copy2(DB, SOURCES_OUT / 'KatamerosDatabase.sqlite')
    for p in PDFS.glob('*'):
        if p.suffix.lower() in ['.pdf','.txt']:
            shutil.copy2(p, SOURCES_OUT / p.name)
    # Manifest.
    files=[]
    for p in sorted(SOURCES_OUT.iterdir()):
        if p.is_file():
            files.append({'file':p.name,'bytes':p.stat().st_size,'sha256':sha256(p)})
    (SOURCES_OUT/'SOURCE_MANIFEST.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
    return files

def copy_support_modules():
    shutil.copy2(WORK / 'passage_normalization.py', SCRIPTS / 'passage_normalization.py')

def copy_special_datasets():
    required_sources = {
        'pascha_day_hour_index.csv': [DATA / 'pascha_day_hour_index.csv', WORK / 'out2' / 'pascha_day_hour_index.csv'],
        'pascha_day_hour_index.jsonl': [DATA / 'pascha_day_hour_index.jsonl', WORK / 'out2' / 'pascha_day_hour_index.jsonl'],
        'bright_saturday_service_order.csv': [DATA / 'bright_saturday_service_order.csv', WORK / 'out_bright' / 'bright_saturday_service_order.csv'],
        'bright_saturday_service_order.jsonl': [DATA / 'bright_saturday_service_order.jsonl', WORK / 'out_bright' / 'bright_saturday_service_order.jsonl'],
    }
    missing = []
    for name, candidates in required_sources.items():
        existing = next((src for src in candidates if src.exists()), None)
        if existing is None:
            missing.append(name)
            continue
        if existing != DATA / name:
            shutil.copy2(existing, DATA / name)
    if missing:
        raise FileNotFoundError('Missing required Pascha/Bright Saturday artifacts: ' + ', '.join(missing))


def run_special_service_build():
    script = WORK / 'build_special_service_reference.py'
    if script.exists():
        subprocess.run([sys.executable, str(script)], check=True, cwd=str(WORK))


def run_agpeya_build():
    script = WORK / 'build_agpeya_reference.py'
    if script.exists():
        subprocess.run([sys.executable, str(script)], check=True, cwd=str(WORK))


def run_pascha_source_text_build():
    script = WORK / 'build_pascha_source_text_index.py'
    if script.exists():
        subprocess.run([sys.executable, str(script)], check=True, cwd=str(WORK))


def run_crosswalk_build():
    subprocess.run([sys.executable, str(WORK / 'build_lectionary_crosswalk.py')], cwd=WORK, check=True)


def run_chapter_index_build():
    subprocess.run([sys.executable, str(WORK / 'build_bible_chapter_lectionary_index.py')], cwd=WORK, check=True)


def run_verification_examples():
    subprocess.run([sys.executable, str(WORK / 'verify_lectionary_queries.py')], cwd=WORK, check=True)

def write_query_script():
    source = WORK / 'query_lectionary.py'
    if not source.exists():
        raise FileNotFoundError(f'Missing query helper source: {source}')
    target = SCRIPTS / 'query_lectionary.py'
    shutil.copy2(source, target)
    os.chmod(target, 0o755)


def publish_verified_package() -> int:
    """Publish the verified local out/ package to the Obsidian reference package."""
    if DISABLE_VAULT_PUBLISH:
        return 0
    published = 0
    for src_dir_name in ['data', 'scripts', 'sources']:
        src_dir = OUT / src_dir_name
        dst_dir = VAULT_PACKAGE / src_dir_name
        dst_dir.mkdir(parents=True, exist_ok=True)
        if not src_dir.exists():
            continue
        for src in src_dir.iterdir():
            if src.is_file():
                shutil.copy2(src, dst_dir / src.name)
                published += 1
    summary = OUT / 'BUILD_SUMMARY.json'
    if summary.exists():
        VAULT_PACKAGE.mkdir(parents=True, exist_ok=True)
        shutil.copy2(summary, VAULT_PACKAGE / summary.name)
        published += 1
    return published


def main():
    ensure_dirs()
    books=load_books()
    cycle_rows=export_cycle_tables(books)
    write_csv(DATA/'katameros_cycle_readings.csv', cycle_rows)
    write_jsonl(DATA/'katameros_cycle_readings.jsonl', cycle_rows)
    pidx=build_passage_index(cycle_rows, books)
    write_csv(DATA/'katameros_cycle_passage_index.csv', pidx)
    write_jsonl(DATA/'katameros_cycle_passage_index.jsonl', pidx)
    metas, date_rows, errors = scrape_copticchurch(2020, 2035)
    write_csv(DATA/'copticchurch_date_meta_2020_2035.csv', metas)
    write_csv(DATA/'copticchurch_date_readings_2020_2035.csv', date_rows)
    write_jsonl(DATA/'copticchurch_date_readings_2020_2035.jsonl', date_rows)
    didx=build_date_passage_index(date_rows)
    write_csv(DATA/'copticchurch_passage_index_2020_2035.csv', didx)
    write_jsonl(DATA/'copticchurch_passage_index_2020_2035.jsonl', didx)
    (DATA/'copticchurch_scrape_errors.json').write_text(json.dumps(errors,indent=2),encoding='utf-8')
    copy_special_datasets()
    run_pascha_source_text_build()
    run_special_service_build()
    run_agpeya_build()
    run_crosswalk_build()
    run_chapter_index_build()
    source_files=copy_sources()
    copy_support_modules()
    write_query_script()
    run_verification_examples()
    summary={
        'built_at': dt.datetime.now().isoformat(timespec='seconds'),
        'cycle_reading_rows': len(cycle_rows),
        'cycle_passage_segments': len(pidx),
        'date_resolved_years': '2020-2035',
        'date_resolved_days': len(metas),
        'date_resolved_reading_rows': len(date_rows),
        'date_resolved_passage_index_rows': len(didx),
        'date_scrape_errors': len(errors),
        'source_file_count': len(source_files),
    }
    (OUT/'BUILD_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    published_file_count = publish_verified_package()
    summary['published_file_count'] = published_file_count
    summary['published_to'] = str(VAULT_PACKAGE) if not DISABLE_VAULT_PUBLISH else str(OUT)
    (OUT/'BUILD_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    if not DISABLE_VAULT_PUBLISH:
        shutil.copy2(OUT/'BUILD_SUMMARY.json', VAULT_PACKAGE / 'BUILD_SUMMARY.json')
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    main()
