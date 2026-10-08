"""Independent read-only source audit. No producer verifier/contract imports."""
import base64, calendar, copy, datetime as dt, hashlib, json, re
from pathlib import Path
ROOT = Path('/Users/ga/workspace/lectionary-comprehensive-audit-2026-10-07')
P = ROOT / 'lent-source-completion-04'
O = ROOT / 'lent-psalm-gospel-independent-review-04'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def save(n,a): (O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
def check(v,msg):
    if not v: raise AssertionError(msg)
HASHES=load(P/'HASHES.json')
check(sha((P/'FINAL-RECEIPT.json').read_bytes())=='c4248755cba79f12d76803d932e25d09bd38a7fc7f71359744e1d2d9c2b80001','frozen receipt')
hashledger=[]
for name,h in HASHES.items():
    actual=sha((P/name).read_bytes());check(actual==h,'packet hash '+name)
    hashledger.append({'path':str(P/name),'sha256':actual,'matches':True})
for f in load(P/'evidence-manifest.json'):
    actual=sha(Path(f['path']).read_bytes());check(actual==f['sha256'],'evidence '+f['path'])
    hashledger.append({'path':f['path'],'sha256':actual,'matches':True})
inputs=load(P/'source-input-hashes.json')
for f in inputs:
    check(sha(Path(f['path']).read_bytes())==f['sha256'],'protected source input '+f['path'])
save('protected-source-input-ledger.json',inputs)
C=load(P/'candidate-oracle.json'); OLD=load(P/'accepted-evidence-reuse-ledger.json')
PG=[r for r in C if r['slot']=='Psalm and Gospel']; OLDPG=[r for r in OLD if r['slot']=='Psalm and Gospel']
HEAD=re.compile(r'^\s*(Psalms|Matthew|Mark|Luke|John)\s+\d+(?:\s*:\s*\d+)?[\d\s,:;\-–]*$')
SCRIPT=re.compile('[\u0600-\u06ff\u2c80-\u2cff]')
months=['Thoout','Paope','Hathor','Koiahk','Tobe','Meshir','Paremhotep','Parmoute','Pashons','Paone','Epep','Mesore','Nesi']
def pascha(y):
    a=y%4;b=y%7;c=y%19;d=(19*c+15)%30;e=(2*a+4*b-d+34)%7
    n=d+e+114
    return dt.date(y,n//31,n%31+1)+dt.timedelta(days=13)
def coptic(date):
    y=date.year;start=dt.date(y,9,12 if calendar.isleap(y+1) else 11)
    if date<start:
        y-=1;start=dt.date(y,9,12 if calendar.isleap(y+1) else 11)
    n=(date-start).days
    return {'year':y-283,'month':n//30+1,'month_name':months[n//30],'day':n%30+1}
def scan(text):
    return [(i+1,l) for i,l in enumerate(text.splitlines()) if HEAD.fullmatch(l)]
def verses(text):
    return [l for l in text.splitlines() if re.match(r'^\d+\s',l) and not SCRIPT.search(l)]
contextledger=[];headledger=[];bodyledger=[];reuseledger=[]
def verify(r,body=None,candidate=True):
    b=Path(r['text_path']).read_bytes() if body is None else body
    check(sha(b)==r['text_sha256']==r['whole_rendered_body_sha256'],'full-body-hash')
    text=b.decode();heads=scan(text);check([l for _,l in heads]==r['raw_reference_lines'],'literal-headings')
    check([l for l in text.splitlines() if re.match(r'^\s*(?:[1-4] )?[A-Z][A-Za-z ]+ \d+[\d\s,:;\-–]*$',l)]==[l for _,l in heads],'broad-literal-heading-scan')
    check(len(heads)==2 and heads[0][1].lstrip().startswith('Psalms') and not heads[1][1].lstrip().startswith('Psalms'),'Psalm-Gospel-order')
    check('Matins Psalm' in text and 'Matins Gospel' in text,'service-body-labels')
    check(r['service']=='Matins' and r['slot']=='Psalm and Gospel' and r['navigation']==['Readings','Matins','Psalm and Gospel'],'navigation')
    blocks=r['ordered_source_blocks'];check(len(blocks)==2,'block-count');lines=text.splitlines(keepends=True)
    for j,((line,heading),block) in enumerate(zip(heads,blocks)):
        check(block['source_order']==j+1 and block['source_line']==line and block['raw_reference_line']==heading,'block-heading-order')
        check(block['source_byte_offset']==len(''.join(lines[:line-1]).encode()),'byte-offset')
        check(base64.b64decode(block['raw_line_utf8_base64'])==lines[line-1].encode(),'literal-base64')
        begin=block['body_envelope_first_line'];end=block['body_envelope_last_line']
        envelope=''.join(lines[begin-1:end])
        check(envelope==block['body_envelope_literal'] and sha(envelope.encode())==block['body_envelope_sha256'],'body-envelope')
        check(begin==line and end==(heads[j+1][0]-1 if j+1<len(heads) else len(lines)),'envelope-endpoint')
    date=dt.date.fromisoformat(r['civil_date']);civil=date.strftime('%A, %B ')+str(date.day)+date.strftime(', %Y')
    check(r['weekday']==date.strftime('%A') and civil in r['actual_home_line'],'civil-date')
    check(r['actual_home_line']==r['context'].splitlines()[0] and r['actual_occasion'] in r['actual_home_line'],'actual-occasion')
    check((date-pascha(date.year)).days==r['pascha_offset_days'],'offset')
    check(coptic(date)==r['numeric_coptic_calendar_crosscheck'],'numeric-Coptic')
    cp=coptic(date);numeric=f"{cp['month_name']} {cp['day']}, {cp['year']}"
    if r['civil_date']=='2026-02-15':
        check(numeric in (P/'presentation-panel/selected-date-panel.txt').read_text(),'Presentation numeric panel')
    else: check(numeric in r['actual_home_line'],'observed-Coptic')
    if candidate:
        ctx=next(Path(f['path']) for f in r['context_files'] if f['path'].endswith('context.txt'))
        check(ctx.read_text()==r['context'],'primary-home')
        menu=(ctx.parent.parent/'Matins-menu.txt').read_text().splitlines()
        check(menu[:3]==['Back','Prophecies','Psalm and Gospel'] and (len(menu)==3 or menu[3]=='Commemorations'),'Matins-menu')
        check('Matins' in (ctx.parent.parent/'Readings-menu.txt').read_text().splitlines(),'Readings-menu')
        images=r['reference_screenshots'];check([x['raw_ref'] for x in images]==[l for _,l in heads],'image-order')
        for image in images: check(sha(Path(image['path']).read_bytes())==image['sha256'],'ready-image-hash')
        check(r['state']=='producer_candidate_pending_independent_acceptance' and r['evidence_state']==r['state'],'false-qualification')
        check(r['source_numbering']=='literal_reader_edition_unmapped' and r['numbering']=='literal source; no conversion','false-Psalm-conversion')
    check('original captured civil date/occasion/service only' in r['qualification_scope'],'scope')
    return heads,verses(''.join(lines[heads[1][0]:])),cp
for r in PG:
    heads,v,cp=verify(r)
    m=re.search(r'(\d+)\s*:\s*(\d+)-(?:([0-9]+):)?(\d+)$',heads[1][1]);check(m is not None,'Gospel range shape')
    nums=[int(x.split()[0]) for x in v];start=int(m[2]);end=int(m[4])
    expected=([39]+list(range(1,13))) if m[3] else list(range(start,end+1))
    omitted=[]
    if r['civil_date']=='2026-02-28': omitted=[44,46];expected=[n for n in expected if n not in omitted]
    check(nums==expected,'Gospel-verse-order '+r['civil_date'])
    special={'2026-03-19':'John12:36 source ends before departure/hiding clause; partial canonical verse; do not expand', '2027-04-08':'Luke9:43 ends after things which Jesus did, before He said to His disciples; partial canonical verse; do not expand', '2026-02-28':'Mark9 source English numbered verses 44 and 46 absent; preserve actual body, do not fill', '2026-02-27':'Matthew15:39 then chapter16 verses1-12; preserve reset'}
    contextledger.append({'civil_date':r['civil_date'],'occasion_key':r['occasion_key'],'actual_home_line':r['actual_home_line'],'Coptic':cp,'offset':r['pascha_offset_days'],'navigation':r['navigation'],'primary_context_files':r['context_files'],'verified':True,'visual_home_sheet':f"contexts-ready-{(next(i for i,x in enumerate(sorted(set(y['civil_date'] for y in C))) if x==r['civil_date']))//8:02}.jpg"})
    headledger.append({'civil_date':r['civil_date'],'headings':[{'line':i,'raw':l,'precolon_whitespace':bool(re.search(r'\s+:',l)),'leading_tab':l.startswith('\t'),'composite':bool(re.search('[,;]|:\\d+.*:',l))} for i,l in heads],'literal_preserved':True})
    bodyledger.append({'civil_date':r['civil_date'],'full_body_sha256':r['text_sha256'],'blocks_verified':2,'English_Gospel_verse_numbers':nums,'first_verse':v[0],'last_verse':v[-1],'English_Gospel_lines':v,'source_omitted_numbered_verses':omitted,'boundary_note':special.get(r['civil_date'],'source endpoint/body preserved; no independent edition-equivalence claim'),'canonical_psalm_approved':False})
# Rehash and authenticate all 33 reuse rows against their ORIGINAL accepted manifests.
for r in OLD:
    check(sha(Path(r['text_path']).read_bytes())==r['text_sha256'],'old-body')
    origin=Path(r['origin_manifest']);obj=([json.loads(l) for l in origin.read_text().splitlines() if l.strip()] if origin.suffix=='.jsonl' else load(origin))
    check(isinstance(obj,list),'original accepted manifest shape')
    flat=[]
    for x in obj:
        flat.append(x)
        flat.extend(x.get('documents',[]))
        flat.extend(x.get('readings',[]))
    matches=[x for x in flat if (x.get('text_path') or x.get('textPath') or x.get('documentPath'))==r['text_path'] and (x.get('text_sha256') or x.get('whole_rendered_body_sha256') or x.get('textSha256') or x.get('documentSha256'))==r['text_sha256']]
    check(matches,'original acceptance binding '+r['civil_date'])
    if r['slot']=='Psalm and Gospel':
        oldheads,oldverses,oldcp=verify(r,candidate=False)
        headledger.append({'civil_date':r['civil_date'],'reuse':True,'headings':[{'line':i,'raw':l,'precolon_whitespace':bool(re.search(r'\s+:',l)),'leading_tab':l.startswith('\t')} for i,l in oldheads],'literal_preserved':True})
        bodyledger.append({'civil_date':r['civil_date'],'reuse':True,'full_body_sha256':r['text_sha256'],'blocks_verified':2,'English_Gospel_lines':oldverses,'English_Gospel_verse_numbers':[int(l.split()[0]) for l in oldverses],'first_verse':oldverses[0],'last_verse':oldverses[-1],'canonical_psalm_approved':False})
    reuseledger.append({'civil_date':r['civil_date'],'occasion_key':r['occasion_key'],'slot':r['slot'],'text_path':r['text_path'],'sha256':r['text_sha256'],'original_manifest':str(origin),'original_manifest_sha256':sha(origin.read_bytes()),'exact_original_acceptance_bindings':len(matches),'scope':'original dated only; no Prophecies acceptance added by this reviewer'})
# Each fresh PG body agrees EXACTLY with existing archive bytes, not a new wording claim.
bodyreuse=[]
for r in load(P/'exact-fresh-body-hash-reuse-ledger.json'):
    if r['slot']!='Psalm and Gospel':continue
    for oldpath in r['exact_existing_body_paths']:check(sha(Path(oldpath).read_bytes())==r['fresh_body_sha256'],'old archive exact bytes')
    bodyreuse.append(r)
coverage=load(P/'finite-coverage-map.json')['coverage'];check(len(coverage)==116,'116 contexts')
keys={(x['key']['actual_occasion_key'],x['key']['child']) for x in coverage};check(len(keys)==116,'duplicate inventory key')
oldkeys={(r['occasion_key'],r['slot']) for r in OLD};newkeys={(r['occasion_key'],r['slot']) for r in C}
check(len(OLD)==33 and len(oldkeys)==32 and len(newkeys-oldkeys)==84 and oldkeys|newkeys==keys,'33/32/84 conservation')
pgkeys={r['occasion_key'] for r in PG};oldpgkeys={r['occasion_key'] for r in OLDPG};check(len(PG)==55 and len(pgkeys-oldpgkeys)==53 and len(pgkeys|oldpgkeys)==58,'55/53/58 PG accounting')
# Body equality is never appointment identity.
groups={}
for r in PG+OLDPG: groups.setdefault(r['text_sha256'],[]).append({'date':r['civil_date'],'key':r['occasion_key']})
samebody=[{'sha256':h,'appointments':rows} for h,rows in groups.items() if len({x['key'] for x in rows})>1]
check(any({'GreatFast@-13','GreatFast@-9'}<={x['key'] for x in g['appointments']} for g in samebody),'distinct last Monday/Friday')
conservation={'all_reused_documents':33,'reused_unique_child_keys':32,'PG_candidates':55,'PG_new_distinct_frontier':53,'PG_existing_keys':5,'PG_duplicate_date_witnesses':[r['civil_date'] for r in PG if r['occasion_key'] in oldpgkeys],'PG_union_occasions':58,'full_inventory_child_keys':116,'same_body_distinct_appointments':samebody,'no_prophecies_PG_retained':[x['key']['actual_occasion_key'] for x in coverage if x['key']['child']=='Prophecies' and 'explicit_no_prophecies_rubric' in x['source_states']],'collision_scope':'Cross2026-03-19 distinct from ordinary fifth Thursday2027-04-08; Presentation2026-02-15 distinct from preFastSunday2027-03-07; Annunciation2027-04-07 distinct from actual LastFriday2028-04-07'}
check(len(conservation['no_prophecies_PG_retained'])==19,'19 non-prophecy companions')
menus=[]
for r in load(P/'source-service-inventory.json'):
    date=r['civil_date'];directory=P/'jonah-service-inventory'/date
    readings=(directory/'Readings-menu.txt').read_text();liturgy=(directory/'Liturgy-menu.txt').read_text();rubric=(directory/'Vespers-rubric.txt').read_text()
    check(all(x in readings.splitlines() for x in ['Vespers','Matins','Liturgy']),'Jonah menu')
    check(all(x in liturgy.splitlines() for x in ['Pauline Epistle','Catholic Epistle','Praxis','Psalm and Gospel']),'Jonah Liturgy inventory')
    check(rubric.startswith('Vespers and Vesper Praises are not prayed during Jonah\'s Fast'),'explicit no Vespers')
    for f in r['files']:check(sha(Path(f['path']).read_bytes())==f['sha256'],'inventory file')
    menus.append({'date':date,'occasion':r['actual_occasion'],'Readings_menu':readings,'Liturgy_menu':liturgy,'Vespers_rubric':rubric,'accepted_scope':'observed dated menu inventory and explicit no-Vespers; NOT uncaptured Liturgy assignments','files':r['files']})
check(len(menus)==4,'four Jonah menus')
# Real serialized row counterprobes; all must fail the independent verifier.
probes=[]
def probe(name,mutate,body=None):
    r=copy.deepcopy(PG[0]);mutate(r)
    try:verify(r,body=body)
    except AssertionError as e:probes.append({'name':name,'rejected':True,'reason':str(e)});return
    raise AssertionError('mutation survived '+name)
probe('wrong civil context',lambda r:r.update(civil_date='2026-02-03'))
probe('wrong actual feast',lambda r:r.update(actual_occasion='Annunciation'))
probe('full body hash',lambda r:r.update(text_sha256='0'*64))
probe('literal heading dropped',lambda r:r['raw_reference_lines'].pop())
probe('heading tab removed',lambda r:r['raw_reference_lines'].__setitem__(0,r['raw_reference_lines'][0].lstrip()))
probe('heading reorder',lambda r:r['raw_reference_lines'].reverse())
probe('ordered blocks reversed',lambda r:r['ordered_source_blocks'].reverse())
probe('source envelope endpoint shortened',lambda r:r['ordered_source_blocks'][1].update(body_envelope_last_line=r['ordered_source_blocks'][1]['body_envelope_last_line']-1))
probe('ready image omitted',lambda r:r['reference_screenshots'].pop())
probe('image order reversed',lambda r:r['reference_screenshots'].reverse())
probe('false qualification',lambda r:r.update(state='accepted_independent'))
probe('false Psalm canonicalization',lambda r:r.update(source_numbering='mt_nkjv'))
probe('body endpoint truncation',lambda r:None,Path(PG[0]['text_path']).read_bytes()[:-100])
# Count, scope and conservation counterprobes deliberately corrupt accepted identity lists.
for name,corrupt,predicate in [
 ('duplicate dated witness',PG+[PG[0]],lambda rows:len({(r['civil_date'],r['slot']) for r in rows})==len(rows)),
 ('false all-year qualification',dict(scope='all dates',recurrence=True),lambda x:x['scope']=='original dated only' and not x['recurrence']),
 ('no-prophecies erases PG',{r['occasion_key'] for r in PG+OLDPG}-set(conservation['no_prophecies_PG_retained']),lambda x:len(x)==58),
 ('samebody dedup loses appointments',{r['text_sha256']:r for r in PG+OLDPG}.values(),lambda x:len({r['occasion_key'] for r in x})==58)]:
    check(not predicate(corrupt),'counterprobe survived '+name);probes.append({'name':name,'rejected':True,'reason':'independent conservation/scope contract'})
parserforms=['\tPsalms 29 :10-11','\tPsalms 99: 1-2','\tPsalms 54:1, 26:11','\tPsalms 119','\tMatthew 15:39-16:12']
check([l for _,l in scan('\n'.join(parserforms))]==parserforms,'literal forms chapter-only/composite/precolon/tab')
check(verses('6 “English.\n7 (Parenthesis English.)\n8 «العربية\n9 Ⲡⲓ')==['6 “English.','7 (Parenthesis English.)'],'punctuation/script verse parser')
save('parser-form-counterchecks.json',{'positive_literal_forms':parserforms,'all_preserved':True,'chapter_only_in_actual_PG':[],'chapter_only_note':'none observed in these 60 source documents; synthetic parser support is not source evidence'})
for n,a in [('per-context-ledger.json',contextledger),('headings-ledger.json',headledger),('body-ledger.json',bodyledger),('old-qualified-reuse-ledger.json',reuseledger),('sourcehash-ledger.json',hashledger),('bodyhash-reuse-ledger.json',bodyreuse),('conservation-ledger.json',conservation),('corruption-ledger.json',probes),('Jonah-source-inventory-ledger.json',menus)]:save(n,a)
accepted=[]
for r in PG:
    x=copy.deepcopy(r);x.update(state='accepted_dated_source_PG_only',evidence_state='independently_accepted_dated_source_PG_only',independent_review='lent-psalm-gospel-independent-review-04',recurrence_approved=False,canonical_coordinates_approved=False,production_activation_approved=False,qualification_scope='exact captured civil date / actual occasion / Matins Psalm and Gospel only',duplicate_qualified_key_witness=r['occasion_key'] in oldpgkeys);accepted.append(x)
(O/'accepted-dated-oracle.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in accepted))
summary={'accepted_candidate_PG_documents':55,'new_distinct_PG_contexts':53,'duplicate_date_witnesses':2,'retained_old_PG_documents':5,'PG_union_occasions':58,'literal_candidate_headings':110,'ready_PG_images':110,'packet_hash_checks':len(HASHES),'primary_evidence_checks':len(load(P/'evidence-manifest.json')),'all_hash_checks':len(hashledger),'independent_counterprobes_rejected':len(probes),'canonical_Psalm_approval':False,'recurrence_approval':False,'production_activation':False}
save('summary.json',summary)
print(json.dumps(summary,indent=2))
