"""Independent saved-primary evidence reviewer; writes only its review directory."""
import json, hashlib, re, copy, datetime
from pathlib import Path
ROOT=Path('/Users/ga/workspace/lectionary-comprehensive-audit-2026-10-07')
P=ROOT/'annual129-recovery-03'
OUT=ROOT/'annual129-independent-review-03'
sha=lambda b:hashlib.sha256(b).hexdigest()
def readj(path): return json.loads(Path(path).read_text())
def rows(path):return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
def emit(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def jlines(name,rs):
    (OUT/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs))
def require(ok,msg):
    if not ok:raise ValueError(msg)
def coptic(date):
    d=datetime.date.fromisoformat(date); y,m,day=d.year,d.month,d.day
    a=(14-m)//12; yy=y+4800-a; mm=m+12*a-3
    jd=day+(153*mm+2)//5+365*yy+yy//4-yy//100+yy//400-32045
    cy=(4*(jd-1825030)+1463)//1461
    start=1825030+365*(cy-1)+cy//4
    offset=jd-start
    return [offset//30+1,offset%30+1,cy],d.strftime('%A')
ART=readj(P/'artifact-hashes.json'); EXT=readj(P/'external-evidence-hashes.json')
protected={str(P/k):v for k,v in ART.items()};protected.update(EXT)
protected[str(P/'FINAL-RECEIPT.json')]='56969d6ba50b5e8869c4c25f7778a240a5fe7b33f6f19dc4cd3b127063ca8f7f'
protected[str(P/'artifact-hashes.json')]=sha((P/'artifact-hashes.json').read_bytes())
protected[str(ROOT/'fresh-annual-continuation-02/tables.jsonl')]=sha((ROOT/'fresh-annual-continuation-02/tables.jsonl').read_bytes())
checks=[]
for path,h in protected.items():
    actual=sha(Path(path).read_bytes()); require(actual==h,'binding '+path)
    checks.append({'path':path,'expected':h,'observed':actual,'pass':True})
C=rows(P/'source-candidate.jsonl')[0]; T=rows(P/'tables.jsonl')[0]
OLD=rows(ROOT/'fresh-annual-remaining-dated/tables.jsonl')
seed=next(x for x in readj(ROOT/'fresh-annual-remaining-dated/context-plan.json') if x['id']=='AnnualReadings-129')
original=next(x for x in OLD if x['id']=='AnnualReadings-129')
require(C['originalSeed']==seed==readj(P/'original-seed.json'),'original seed preservation')
require(C['originalCapture']==original,'original capture/aliases preservation')
require(len(OLD)==220,'original 220')
require(original['date']=='2026-01-17' and original['homeContext'].startswith('Selected Season Theophany Paramoun Tobe 9, 1742 Saturday, January 17, 2026'),'Paramoun context')
DOCS=['Vespers','Matins-Prophecies','Matins-Psalm and Gospel','Liturgy-Pauline Epistle','Liturgy-Catholic Epistle','Liturgy-Praxis','Liturgy-Psalm and Gospel']
REFS=['Psalms 111:1','Matthew 25:14-23','Psalms 131:1,7','Luke 6:17-23','Hebrews 11:17-31','James 1:12-21','Acts 19:11-20','Psalms 1:1,2','Matthew 4:23-5:16']
RUNS={1:list(range(14,24)),3:list(range(17,24)),4:list(range(17,32)),5:list(range(12,22)),6:list(range(11,21)),8:list(range(23,26))+list(range(1,17))}
heading=re.compile(r'^\s*((?:[1-4] )?[A-Za-z][A-Za-z ]+\d+\s*:\s*[\d,:; -]+)\s*$')
navfolder=P/'AnnualReadings-129/6ec4bf38-ef24-48ff-ab78-9c7550da226d'
for name,expect in [('Readings',['Back','Vespers','Matins','Liturgy','Antiphonary']),('Matins',['Back','Prophecies','Psalm and Gospel']),('Liturgy',['Back','Pauline Epistle','Catholic Epistle','Praxis','Synaxarion','Psalm and Gospel'])]:
    require((navfolder/(name+'-menu.txt')).read_text().splitlines()==expect,'navigation '+name)
# Oracle is raw captured text plus explicit user requirements, never producer verdict flags.
def verify(c,body_override=None):
    require(c['date']=='2024-01-18','bounded date')
    require(c['homeLine']=='Selected Season Standard Tobe 9, 1740 Thursday, January 18, 2024','actual context')
    require(c['actualOccasion']=='Standard' and c['coptic']==[5,9,1740],'occasion/coptic')
    require(len(c['documents'])==7,'seven documents')
    require([d['label'] for d in c['documents']]==DOCS,'document order')
    require(c['originalSeed']==seed and c['originalCapture']==original,'history conservation')
    require(not c.get('releaseReady',False) and not c.get('recurringAcceptance',False),'false promotion')
    result=[];found=[];bodies=[]
    for di,d in enumerate(c['documents']):
        raw=(body_override or {}).get(d['textPath'],Path(d['textPath']).read_bytes()); text=raw.decode()
        require(sha(raw)==d['textSha256'],'body hash')
        require(d['sourceProbe'] and d['reusedImmutableEvidence'],'fresh rendered hash reuse')
        require(d['originalTableId']==('AnnualReadings-37' if di==1 else 'AnnualReadings-57'),'reuse origin')
        require(d['date']=='2024-01-18' and d['url']=='https://copticreader.org/app/#/document','dated doc')
        for im,h in [(d['screenshotPath'],d['screenshotSha256'])]+[(x['path'],x['sha256']) for x in d['referenceScreenshots']]:
            require(Path(im).is_file() and sha(Path(im).read_bytes())==h,'missing/corrupt image')
        hits=[];offset=0
        for li,line in enumerate(text.splitlines(keepends=True)):
            mt=heading.fullmatch(line.rstrip('\n'))
            if mt:hits.append((li,offset,mt.group(1),line.rstrip('\n')))
            offset+=len(line.encode())
        require([h[2] for h in hits]==d['printedReferences'],'literal doc refs')
        for hi,(li,start,ref,literal) in enumerate(hits):
            end=hits[hi+1][1] if hi+1<len(hits) else len(raw)
            block=raw[start:end].decode(); ordinal=len(found)
            found.append(ref); r=c['readings'][ordinal]
            require((r['printedReference'],r['documentOrder'],r['headingOrder'],r['sourceAppointmentOrdinal'],r['headingLine'])==(ref,di,hi,ordinal,li+1),'heading order/book')
            require(r['byteStart']==start and r['byteEnd']==end and r['literalHeadingLine']==literal,'boundary locator')
            require(r['blockLiteral']==block and r['blockSha256']==sha(block.encode()),'complete block')
            nums=[]; english=[]
            for line in block.splitlines():
                m=re.match(r'^\s*(\d+)\s+(.+)$',line)
                if m and re.search('[A-Za-z]',m[2]) and not re.search('[\u0600-\u06ff\u2c80-\u2cff]',m[2]):
                    nums.append(int(m[1]));english.append(line)
            if ordinal in RUNS: require(nums==RUNS[ordinal],'complete numbered endpoint/body')
            else:require(r['canonicalPsalmStatus']=='PENDING_EDITION_TEXT_QUALIFICATION','Psalm coordinate promotion')
            result.append({'ordinal':ordinal,'documentOrder':di,'headingOrder':hi,'reference':ref,'line':li,'byteStart':start,'byteEnd':end,'blockSha256':sha(block.encode()),'englishVerseNumbers':nums,'englishVerseLines':english,'pass':True,'canonicalPsalmStatus':r['canonicalPsalmStatus']})
        if di==1:require(text=='Prophecies\nالنبوآت\nNo prophecies are read on this day.','explicit no prophecies')
        bodies.append(d['label']+'\n'+text)
    require(found==REFS and len(c['readings'])==9,'nine ordered headings')
    whole=sha('\n'.join(bodies).encode());require(whole==c['tableTextSha256']==T['tableTextSha256']=='826366fd244494e1214ea9182814b273aae666f35a68038fee1725390b4781bf','whole table')
    return result
require(C['documents']==T['documents'],'candidate/table document conservation')
for d in C['documents']:
    require(d in rows(P/'evidence.jsonl'),'fresh evidence witness equality')
    origin=next(x for x in rows(d['originManifest']) if x['id']==d['originalTableId'])
    od=next(x for x in origin['documents'] if x['label']==d['label'])
    for field in ['textSha256','screenshotSha256','printedReferences']:
        require(d[field]==od[field],'old immutable witness '+field)
    def absolute(v):
        path=Path(v); return str(path if path.is_absolute() else Path(d['originManifest']).parent/path)
    for field in ['textPath','screenshotPath']:
        require(d[field]==absolute(od[field]),'old immutable path alias '+field)
    require(d['referenceScreenshots']==[dict(x,path=absolute(x['path'])) for x in od['referenceScreenshots']],'old reference aliases')
boundaries=verify(C)
context=[]
for q in rows(P/'primary-date-probe-verdicts.jsonl'):
    computed,weekday=coptic(q['date']);require(computed==q['coptic'],'independent Coptic epoch')
    folder=Path(q['evidenceDirectory']); home=(folder/'home-selected.txt').read_text().splitlines()[0]
    require(home==q['homeLine'] and (' '+weekday+', ') in home,'weekday home')
    require(home.startswith('Selected Season Standard Tobe 9,'),'Standard probe')
    require(q['selectedDatePanelRow'] in (folder/'date-panel-selected.txt').read_text(),'selected panel')
    context.append({'date':q['date'],'coptic':computed,'weekday':weekday,'homeLine':home,'scope':'complete dated table' if q['date']=='2024-01-18' else 'context only; seven documents NOT authenticated','verdict':'ACCEPT_CONTEXT','folder':str(folder)})
require(coptic('2026-01-17')==([5,9,1742],'Saturday'),'canary independent calendar')
mutations=[]
def mutant(name,fn,body=None):
    m=copy.deepcopy(C);fn(m)
    try:verify(m,body)
    except (ValueError,FileNotFoundError,KeyError,IndexError) as ex:mutations.append({'mutation':name,'killed':True,'reason':str(ex)})
    else:raise ValueError('SURVIVED '+name)
mutant('context_Paramoun_ordinary_nine_shape',lambda m:m.update(homeLine=original['homeContext'].splitlines()[0],actualOccasion='Theophany Paramoun'))
mutant('book_Hebrews_to_Romans',lambda m:m['readings'][4].update(printedReference='Romans 11:17-31'))
mutant('reading_order',lambda m:m['readings'].__setitem__(slice(4,6),list(reversed(m['readings'][4:6]))))
mutant('body_block_truncation',lambda m:m['readings'][1].update(blockLiteral=m['readings'][1]['blockLiteral'][:-50]))
mutant('endpoint_truncation',lambda m:m['readings'][8].update(printedReference='Matthew 4:23-5:15'))
mutant('missing_image',lambda m:m['documents'][0].update(screenshotPath=str(OUT/'nonexistent.png')))
mutant('false_recurring_promotion',lambda m:m.update(recurringAcceptance=True))
mutant('false_release_promotion',lambda m:m.update(releaseReady=True))
mutant('Psalm_false_coordinate_promotion',lambda m:m['readings'][0].update(canonicalPsalmStatus='QUALIFIED_MT'))
mutant('2023_context_only_as_complete',lambda m:m.update(date='2023-01-17'))
path=C['documents'][0]['textPath'];mutant('raw_body_corruption',lambda m:None,{path:Path(path).read_bytes()[:-1]})
OUT.mkdir(exist_ok=True)
jlines('source-boundary-order-verdicts.jsonl',boundaries)
jlines('context-verdicts.jsonl',context)
jlines('guard-mutation-verdicts.jsonl',mutations)
jlines('source-hash-verdicts.jsonl',checks)
emit('accepted-dated-oracle.json',{'id':'AnnualReadings-129','acceptedDate':'2024-01-18','coptic':[5,9,1740],'weekday':'Thursday','occasion':'Standard','printedReferences':REFS,'documents':C['documents'],'readings':C['readings'],'tableTextSha256':C['tableTextSha256'],'independentAcceptance':True,'acceptanceScope':'exact dated saved rendered-hash witness only','recurringAcceptance':False,'releaseReady':False,'parentManifestUpdated':False,'originalSeed':seed,'originalCapture':original,'contextOnlyDate':'2023-01-17'})
visual=rows(P/'visual-evidence-manifest.jsonl')
require(len(visual)==11 and len({x['sha256'] for x in visual})==11,'eleven unique images')
jlines('visual-verdicts.jsonl',[dict(x,independentVisualVerdict='READY; literal headings/rubric visually inspected on hash-bound contact sheet; reused image not fresh dated screenshot') for x in visual])
emit('conservation-verdicts.json',{'original220Retained':len(OLD),'originalSeedAllFieldsEqual':True,'originalParamounAllDocumentAndImageAliasesEqual':True,'originalParamounNineReferenceShapeRetainedNotAnnualQualification':True,'protectedBindings':len(protected),'bodyReusesAnnual57':6,'rubricReuseAnnual37':1,'freshDuplicateBodyCopies':0,'scope':'Protected candidate artifacts and external original bindings; no edits outside review directory'})
emit('remaining-gates.json',{'annual180':{'scope':'observed 2020-2035 only','greatFast':15,'preFastSaturday':1,'state':'unresolved generic annual date; seed retained','universalAbsence':False,'outsideBounds':'unobserved, not ruled out'},'sourcePsalmQualification':'literal coordinates only; edition and full-text fragment qualification held','calendar':'recurrence, exception and precedence need separately authorized qualified resolver and production guards','sourceIntegration':'parent manifest and source/core/consumer integration not performed or approved','releaseReady':False})
for path,h in protected.items():require(sha(Path(path).read_bytes())==h,'closing conservation '+path)
print(json.dumps({'result':'ACCEPT_2024_DATED_SOURCE_ONLY','artifactBindings':len(ART),'externalBindings':len(EXT),'headings':len(boundaries),'nonPsalmBoundaries':len(RUNS),'mutationsKilled':len(mutations),'contextOnly2023':True,'protectedBindingsUnchanged':len(protected)},indent=2))
