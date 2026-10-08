"""Reviewer-owned source-only checks. No producer imports or runtime activation."""
import json, hashlib, re, base64, copy, datetime as dt
from pathlib import Path
D=Path(__file__).resolve().parent
R=D.parent/'lent-source-completion-04'
def load(n): return json.loads((R/n).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(b): return hashlib.sha256(b).hexdigest()
def save(n,d): (D/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
REF=re.compile(r'\s*(?:[1-4]\s+)?[A-Za-z][A-Za-z ]+\s+\d+(?:\s*:\s*\d+)?[\d\s,:;–—\-]*\s*')
C=[x for x in load('candidate-oracle.json') if x['slot']=='Prophecies']
O=[x for x in load('accepted-evidence-reuse-ledger.json') if x['slot']=='Prophecies']
ALL=C+O
PIN={x['text_path']:copy.deepcopy(x) for x in ALL}
REJECTED={p for x in load('ready-image-repair-ledger.json') if x['slot']=='Prophecies' for p in x['rejected_initial_image_paths']}
def pascha(y):
 a=y%4;b=y%7;c=y%19;d=(19*c+15)%30;e=(2*a+4*b-d+34)%7
 # Julian computus expressed by same numeric Gregorian date plus calendar difference.
 return dt.date(y,(d+e+114)//31,(d+e+114)%31+1)+dt.timedelta(days=y//100-y//400-2)
def files(e):
 f=e.get('context_files',[])
 if isinstance(f,dict): return [{'path':p,'sha256':h} for p,h in f.items()]
 return [{'path':x} if isinstance(x,str) else x for x in f]
def validate(e,body=None):
 assert e['slot']=='Prophecies' and e['service']=='Matins','wrong service/child'
 p=PIN[e['text_path']]
 for k in ['civil_date','actual_occasion','occasion_key','weekday','pascha_offset_days','navigation','semantic_state','context','actual_home_line']:
  assert e.get(k)==p.get(k),'wrong pinned context '+k
 assert e['navigation']==['Readings','Matins','Prophecies']
 assert e['actual_occasion'] in e['actual_home_line']
 date=dt.date.fromisoformat(e['civil_date']);assert date.strftime('%A')==e['weekday']
 assert (date-pascha(date.year)).days==e['pascha_offset_days']
 assert int(e['occasion_key'].split('@')[1])==e['pascha_offset_days']
 civil=date.strftime('%A, %B ')+str(date.day)+date.strftime(', %Y');assert civil in e['context']
 cp=e['numeric_coptic_calendar_crosscheck']
 rd=103605+365*(cp['year']-1)+cp['year']//4+30*(cp['month']-1)+cp['day']-1
 assert rd==date.toordinal(),'wrong computed Coptic date'
 if 'Presentation of the Lord Christ' in e['context']:
  panel=(R/'presentation-panel/selected-date-panel.txt').read_text();assert 'February 15, 2026' in panel and 'Meshir 8, 1742' in panel
 else: assert f"{cp['month_name']} {cp['day']}, {cp['year']}" in e['context']
 b=Path(e['text_path']).read_bytes() if body is None else body
 assert digest(b)==e['text_sha256']==e['whole_rendered_body_sha256']==p['text_sha256'],'wrong entire body or rewritten immutable binding'
 t=b.decode('utf-8');lines=t.splitlines(keepends=True)
 heads=[(i,l.rstrip('\n')) for i,l in enumerate(lines) if REF.fullmatch(l.rstrip('\n'))]
 assert [l for i,l in heads]==e['raw_reference_lines'],'omitted/reordered literal headings'
 assert len(heads)==len(e['ordered_source_blocks'])
 for j,((i,l),s) in enumerate(zip(heads,e['ordered_source_blocks'])):
  end=heads[j+1][0] if j+1<len(heads) else len(lines);env=''.join(lines[i:end])
  assert s['source_order']==j+1 and s['raw_reference_line']==l
  assert s['source_line']==i+1 and s['source_byte_offset']==len(''.join(lines[:i]).encode())
  assert base64.b64decode(s['raw_line_utf8_base64'])==lines[i].encode()
  assert s['body_envelope_first_line']==i+1 and s['body_envelope_last_line']==end
  assert s['body_envelope_literal']==env and s['body_envelope_sha256']==digest(env.encode())
  assert 'A reading from' in env and 'Glory be to the Holy Trinity' in env,'incomplete source block'
 if not heads:
  assert t=='Prophecies\nالنبوآت\nNo prophecies are read on this day.'
  assert e['semantic_state']=='explicit_no_prophecies_rubric'
 else: assert e['semantic_state']=='assigned_scripture_table'
 if e['text_path'] in {x['text_path'] for x in C}:
  assert e['state']=='producer_candidate_pending_independent_acceptance' and not e.get('source_qualified',False)
  assert e['evidence_state']=='producer_candidate_pending_independent_acceptance'
  screenshots=e['reference_screenshots'];assert len(screenshots)==max(1,len(heads))
  for j,s in enumerate(screenshots):
   assert s['path'] not in REJECTED and s==p['reference_screenshots'][j],'unapproved/loading/substituted image'
   assert sha(s['path'])==s['sha256']
   if heads: assert s['raw_ref']==heads[j][1]
  capture_dir=Path(e['origin_manifest']).parent
  for name,required in [('Readings-menu.txt','Matins'),('Matins-menu.txt','Prophecies')]:
   assert required in (capture_dir/name).read_text()
  for f in files(e):
   if Path(f['path']).name=='context.txt':assert Path(f['path']).read_text()==e['context']
 return True

def inventory(a):
 assert len(a)==59
 keys=[(e['occasion_key'],e['weekday'],e['service'],e['slot']) for e in a]
 assert len(set(keys))==58
 repeats=[k for k,v in __import__('collections').Counter(keys).items() if v>1]
 assert repeats==[('GreatFast@-47','Tuesday','Matins','Prophecies')]
 a1=[e for e in a if e['civil_date']=='2026-02-24'][0];a2=[e for e in a if e['civil_date']=='2028-02-29'][0]
 assert a1['text_sha256']==a2['text_sha256']
 unique={k:e for k,e in zip(keys,a)}
 assert sum(bool(e['raw_reference_lines']) for e in unique.values())==39
 assert sum(not e['raw_reference_lines'] for e in unique.values())==19
 expected={f'GreatFast@{off}' for off in range(-55,-6)}|{'BeforeFast@-57','BeforeFast@-56','JonahFast@-69','JonahFast@-68','JonahFast@-67','JonahPassover@-66'}
 assert expected <= {e['occasion_key'] for e in a} and len(expected)==55
 assert {e['occasion_key'] for e in a}-expected=={'Presentation@-56','Cross@-24','Annunciation@-25'}
 laz=[e for e in a if e['occasion_key']=='GreatFast@-8'][0]
 assert laz['raw_reference_lines']==['\tGenesis 49:1-28','\tIsaiah 40:9-31','\tZephaniah 3:14-20','\tZechariah 9:9-15']
 return True

def main():
 assert sha(R/'FINAL-RECEIPT.json')=='c4248755cba79f12d76803d932e25d09bd38a7fc7f71359744e1d2d9c2b80001'
 H=load('HASHES.json')
 for p,h in H.items():assert sha(R/p)==h,p
 M=load('evidence-manifest.json')
 for f in M:assert sha(f['path'])==f['sha256'],f['path']
 inputs=load('source-input-hashes.json')
 for f in inputs:assert sha(f['path'])==f['sha256'],f['path']
 for e in ALL:validate(e)
 inventory(ALL)
 reuse=[x for x in load('exact-fresh-body-hash-reuse-ledger.json') if x['slot']=='Prophecies']
 n=0
 for x in reuse:
  assert x['old_capture_state']=='old image qualification unchanged; exact fresh body hash corroboration only'
  for p in x['exact_existing_body_paths']:assert sha(p)==x['fresh_body_sha256'];n+=1
 seeds=load('finite-coverage-map.json')['source_seed_lane'];assert len(seeds)==52 and len({s['seed_key'] for s in seeds})==52
 import csv
 csv_path=next(f['path'] for f in inputs if f['path'].endswith('katameros_cycle_readings.csv'))
 with open(csv_path,newline='') as stream: raw=[r for r in csv.DictReader(stream) if r['source_table']=='GreatLentReadings']
 assert len(raw)==419 and len({r['day_key'] for r in raw})==52
 for s in seeds:
  original=[r for r in raw if r['day_key']==s['seed_key']]
  assert original==s['raw_rows'],'seed source-row mismatch'
 coverage=load('finite-coverage-map.json')['coverage']
 assert len(coverage)==116 and len({(c['key']['actual_occasion_key'],c['key']['weekday'],c['key']['service'],c['key']['child']) for c in coverage})==116
 grouped={}
 for c in coverage:grouped.setdefault(c['key']['actual_occasion_key'],set()).add(c['key']['child'])
 assert len(grouped)==58 and all(v=={'Prophecies','Psalm and Gospel'} for v in grouped.values())
 assert {c['key']['actual_occasion_key'] for c in coverage if c['key']['child']=='Prophecies'}=={e['occasion_key'] for e in ALL}
 s49=next(s for s in seeds if s['seed_key']=='week 49 day_of_week 3');s4=next(s for s in seeds if s['seed_key']=='week 4 day_of_week 3')
 sig=lambda s:[(r['reading_slot'],r['raw_ref']) for r in s['raw_rows']]
 assert sig(s49)==sig(s4) and s49['source_key']==s4['source_key']=='GreatFast@-32'
 assert len({s['source_key'] for s in seeds})==51
 cal=load('supported-2020-2035-calendar-inventory.json');assert len(cal)==880
 assert sum(bool(c['fixed_feast_collision_candidate']) for c in cal)==34
 for row in cal:
  d=dt.date.fromisoformat(row['civil_date']);assert dt.date.fromisoformat(row['pascha_date'])==pascha(d.year)
  assert (d-pascha(d.year)).days==row['pascha_offset_days'] and d.strftime('%A')==row['weekday']
  c=row['numeric_coptic_date_computed'];assert d.toordinal()==103605+365*(c['year']-1)+c['year']//4+30*(c['month']-1)+c['day']-1
  assert 'precedence NOT asserted' in row['scope']
 target=next(e for e in C if len(e['raw_reference_lines'])>=3)
 probes=[]
 def probe(name,fn):
  try:fn()
  except (AssertionError,KeyError):probes.append({'name':name,'rejected':True})
  else:raise AssertionError('mutation escaped '+name)
 def change(e,k,v):z=copy.deepcopy(e);z[k]=v;validate(z)
 for k,v in [('civil_date','2026-04-01'),('service','Liturgy'),('navigation',['Readings','Liturgy','Prophecies']),('actual_occasion','Annunciation'),('occasion_key','GreatFast@-24'),('pascha_offset_days',-24),('weekday','Sunday'),('semantic_state','explicit_no_prophecies_rubric'),('source_qualified',True)]:probe('wrong_'+k,lambda k=k,v=v:change(target,k,v))
 probe('removed_heading',lambda:change(target,'raw_reference_lines',target['raw_reference_lines'][:-1]))
 probe('reordered_headings',lambda:change(target,'raw_reference_lines',list(reversed(target['raw_reference_lines']))))
 probe('omitted_prophecy_block',lambda:change(target,'ordered_source_blocks',target['ordered_source_blocks'][:-1]))
 probe('reordered_blocks',lambda:change(target,'ordered_source_blocks',list(reversed(target['ordered_source_blocks']))))
 probe('removed_document',lambda:inventory(ALL[:-1]))
 probe('duplicate_alias_as_appointment',lambda:inventory(ALL+[copy.deepcopy(target)]))
 probe('omitted_ready_image',lambda:change(target,'reference_screenshots',target['reference_screenshots'][:-1]))
 z=copy.deepcopy(target);z['reference_screenshots'][0]['path']=next(iter(REJECTED));probe('promoted_old_loading_image',lambda:validate(z))
 z=copy.deepcopy(target);z['ordered_source_blocks'][0]['source_byte_offset']+=1;probe('wrong_utf8_offset',lambda:validate(z))
 probe('truncated_entire_body',lambda:validate(target,Path(target['text_path']).read_bytes()[:-20]))
 rubric=next(e for e in C if not e['raw_reference_lines']);probe('blank_false_absence',lambda:validate(rubric,b'Prophecies\n'))
 # Consistently rehash a false absence: pinned source/body contract must still reject.
 z=copy.deepcopy(target);z.update(raw_reference_lines=[],ordered_source_blocks=[],semantic_state='explicit_no_prophecies_rubric',text_sha256=rubric['text_sha256'],whole_rendered_body_sha256=rubric['text_sha256'])
 probe('forged_consistently_rehashed_false_absence',lambda:validate(z,Path(rubric['text_path']).read_bytes()))
 z=copy.deepcopy(target);z['ordered_source_blocks'][0]['body_envelope_literal']=z['ordered_source_blocks'][0]['body_envelope_literal'][:-10];probe('truncated_body_envelope',lambda:validate(z))
 result={'verdict':'PASS_SOURCE_ONLY','new_candidate_documents':len(C),'old_original_scope_documents':len(O),'distinct_occasion_keys':58,'assigned_tables':39,'explicit_absence_tables':19,'new_headings':sum(len(e['raw_reference_lines']) for e in C),'new_ready_images':sum(len(e['reference_screenshots']) for e in C),'packet_artifacts_rehashed':len(H),'evidence_files_rehashed':len(M),'source_inputs_rehashed':len(inputs),'old_body_match_bindings':n,'supported_computed_candidates':len(cal),'collision_candidates':34,'mutations':probes,'runtime_tests_or_builds_run':False,'production_files_changed':False,'canonical_coordinates_accepted':False,'recurrence_accepted':False,'activation_accepted':False}
 save('verification-results.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
