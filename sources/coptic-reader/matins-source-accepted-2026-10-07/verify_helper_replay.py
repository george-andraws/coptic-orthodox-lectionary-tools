"""Replay real cached helper dates against raw accepted Matins source evidence.

Usage: python -B verify_helper_replay.py --report-dir PATH --opening-bref PATH
No builders, generated data, vault publication or network operations are used.
"""
import argparse
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
import build_lectionary_reference as current

def sha(data): return hashlib.sha256(data).hexdigest()
def context(r): return {k:copy.deepcopy(r[k]) for k in ('civil_date','occasion_key','actual_occasion','actual_home_line','numeric_coptic_calendar_crosscheck','pascha_offset_days','weekday','service')}

def main():
    p=argparse.ArgumentParser();p.add_argument('--report-dir',type=Path,required=True);p.add_argument('--opening-bref',type=Path,required=True);args=p.parse_args()
    report=args.report_dir;report.mkdir(parents=True,exist_ok=True)
    # Execute frozen code bytes with the original repository resource root.
    # No source file or dirty-tree content is reset.
    import types
    opening=types.ModuleType('opening_bref')
    opening.__file__=str(ROOT/'build_lectionary_reference.py')
    exec(compile(args.opening_bref.read_bytes(), str(args.opening_bref), 'exec'), opening.__dict__)
    for key in ('WORK','SRC','DB','PDFS','OUT','DATA','SOURCES_OUT','SCRIPTS'):
        setattr(opening,key,getattr(current,key))
    fixture=Path(__file__).parent;corpus=json.loads((fixture/'accepted-source-corpus.json').read_bytes());mapping=json.loads((fixture/'path-map.json').read_bytes())
    targets={t['civil_date']:t for t in corpus['complete_exact_dated_Matins_pairs']}
    ledger=[];defaults=[];errors=[];proof=[]
    # All captured complete pairs use the real HTML parser/fetch API, not invented HTML.
    for fp in sorted((ROOT/'cache/copticchurch_html').glob('*.html')):
        date=dt.date.fromisoformat(fp.stem);html=fp.read_text(encoding='utf-8',errors='ignore')
        def parse(module):
            try:return {'result':module.parse_copticchurch_html(html,date)}
            except Exception as e:return {'error':type(e).__name__+': '+str(e)}
        before=parse(opening);after=parse(current)
        if before!=after:errors.append({'date':fp.stem,'error':'Default helper drift'})
        defaults.append({'date':fp.stem,'equal':before==after,'html_sha256':sha(fp.read_bytes()),
                         'result_sha256':sha(json.dumps(after,sort_keys=True).encode()),'baseline_error':before.get('error')})
        if fp.stem not in targets:continue
        records=[x['source_record'] for x in corpus['records'] if x['source_record']['civil_date']==fp.stem]
        prophecy=next(r for r in records if r['slot']=='Prophecies');pg=next(r for r in records if r['slot']=='Psalm and Gospel')
        try:
            meta,rows=current.fetch_date(date,fp.parent,candidate_matins_context=context(pg))
            expected=[]
            # Derive ordered envelopes directly from independent raw source bytes.
            for record in (prophecy,pg):
                raw=(fixture/mapping[record['text_path']]).read_bytes();assert sha(raw)==record['text_sha256']
                lines=raw.decode().splitlines(keepends=True)
                for block in record['ordered_source_blocks']:
                    body=''.join(lines[block['body_envelope_first_line']-1:block['body_envelope_last_line']])
                    assert body==block['body_envelope_literal']
                    expected.append((block['raw_reference_line'].strip(),body))
            matins=[r for r in rows if r['service_section']=='Matins']
            assert [(r['raw_ref'],r['source_body']) for r in matins]==expected
            unaffected=[r for r in rows if r['service_section']!='Matins']
            baseline=before['result'][1]
            assert unaffected==[r for r in baseline if r['service_section']!='Matins']
            index=current.build_date_passage_index(matins,include_candidate_matins=True)
            assert len(index)==len(expected) and all(r['matched_ref']=='' for r in index)
            assert current.build_date_passage_index(matins)==[]
            history=meta['matins_source_projection']['history']
            assert [r['raw_ref'] for r in history]==[r['raw_ref'] for r in baseline if r['service_section']=='Matins']
            entry={'date':fp.stem,'occasion_key':pg['occasion_key'],'actual_home_line':pg['actual_home_line'],
                   'coptic_date':pg['numeric_coptic_calendar_crosscheck'],'source_document_hashes':[r['text_sha256'] for r in records],
                   'expected_source_refs':[ref for ref,body in expected],'emitted_source_refs':[r['raw_ref'] for r in matins],
                   'source_body_hashes':[r['source_body_sha256'] for r in matins],
                   'old_matins_rows':len(history),'candidate_matins_rows':len(matins),
                   'candidate_prophecy_rows':sum(r['reading_type']=='Prophecy' for r in matins),
                   'history_inactive':all(not r['active'] and not r['include_in_current_index'] for r in history),
                   'non_matins_unchanged':True,'default_index_candidate_rows':0,'source_index_candidate_rows':len(index),
                   'canonical_hold':True,'runtime_hold':True,'recurrence_hold':True}
            ledger.append(entry)
            if fp.stem in {'2026-03-04','2028-04-07','2026-02-05'}:
                proof.append({'date':fp.stem,'api':'fetch_date -> parse_copticchurch_html -> project_dated_matins_source -> build_date_passage_index(include_candidate_matins=True)',
                              'rows':index,'retained_history':history})
        except Exception as e:errors.append({'date':fp.stem,'error':type(e).__name__+': '+str(e)})
    summary={'cached_helper_dates':len(defaults),'default_helper_equal_dates':sum(x['equal'] for x in defaults),
             'non_target_helper_dates':sum(x['date'] not in targets for x in defaults),'complete_pairs_expected':59,
             'complete_pairs_replayed':len(ledger),'candidate_source_rows':sum(x['candidate_matins_rows'] for x in ledger),
             'candidate_prophecy_rows':sum(x['candidate_prophecy_rows'] for x in ledger),
             'retained_history_rows':sum(x['old_matins_rows'] for x in ledger),
             'candidate_pg_rows':sum(x['candidate_matins_rows']-x['candidate_prophecy_rows'] for x in ledger),
             'default_baseline_errors':sum(bool(x['baseline_error']) for x in defaults),'errors':errors,
             'partial_2026_04_03_promoted':False,'canonical_approval':False,'recurrence_approval':False,'runtime_activation':False}
    for name,data in [('source-context-reconciliation-ledger.json',ledger),('default-helper-date-comparison.json',defaults),('real-helper-query-proof.json',proof),('verification-results.json',summary)]:
        (report/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(summary,indent=2))
    return 0 if len(ledger)==59 and not errors else 1

if __name__=='__main__':sys.exit(main())
