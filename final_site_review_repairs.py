"""Bounded source-adopted Lent/Bright successor with authenticated inverse.

The independent proposal and exact multiplicity sets precede generated output.
Historical corpus contracts are unchanged: this inverse recovers their input.
Source adoption is not implementation, consumer, or release acceptance.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE='sources/site-review-1.3.11/'
PLAN_SHA256='44980c79098f42939c8583c9eccebd39939b06bbe77e71b92c0fb4782add5995'
MARKER='final_site_review_json'


def _json(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))


def _read(path,digest):
    p=ROOT/path
    raw=p.read_bytes()
    if p.is_symlink() or not p.resolve().is_relative_to(ROOT.resolve()) or hashlib.sha256(raw).hexdigest()!=digest:
        raise ValueError('final site review source authentication failed: '+path)
    return raw


def plan():
    return json.loads(_read(SOURCE+'adopted-source-plan.json',PLAN_SHA256))


@lru_cache(maxsize=1)
def _decode(raw):
    return json.loads(gzip.decompress(raw))


def predecessor():
    return _decode(_read(SOURCE+'adopted-predecessor.json.gz',plan()['predecessor_fixture_sha256']))


def authenticate_sources():
    p=plan()
    for path,digest in p['source_files'].items():
        _read(path,digest)
    return p


def verify_successor_membership(rows, *, stage='cumulative'):
    """Use the adopted independent multiset, never derive an oracle from output."""
    from collections import Counter
    if stage=='base':
        raw=_read(SOURCE+'approved-successor-context-keyset.json.gz',
                  '0a00f913b6d56239a8fccccf01092084786813f886a0a0c3686864d94ea0f26b')
        approved=json.loads(gzip.decompress(raw))
    elif stage=='cumulative':
        approved=_supplement_json(supplement_inputs()['membership'])
    else:
        raise ValueError('final site review unknown membership stage')
    actual=Counter(tuple(r.get(f,'')for f in approved.get('fields',approved.get('key_fields')))for r in rows)
    expected=Counter({tuple(r['key']):r['multiplicity']for r in approved['multiset']})
    if actual!=expected:
        raise ValueError('final site review independent successor membership/multiplicity mismatch')
    return {'row_count':sum(actual.values()),'distinct_keys':len(actual)}


def _proof(kind):
    return {'version':'1.3.11','source_plan_sha256':PLAN_SHA256,'kind':kind,
            'fresh_app_verification':False,'authority_status_promoted':False}


def _disclose(row,proof):
    row[MARKER]=_json(proof)
    sources=json.loads(row['source_disclosure'])
    for source in sources:
        source['final_site_review']=proof
    row['source_disclosure']=_json(sources)
    return row


def _new_reverse():
    p=authenticate_sources()
    result=[]
    for a in p['bright']['additions']:
        row=copy.deepcopy(predecessor()['bright_template'])
        ref=a['reference']; chapter=15 if a.get('chapter_only') else 5
        row.update(identity_key=a['identity_key'],occasion=a['occasion'],calendar_keys=a['calendar_keys'],
                   service_section=a['service'],slot=a['slot'],slot_type=a.get('transport_slot_type',a['slot_type']),
                   source_kind=a['source_kind'],canonical_mt_ref=ref,canonical_lxx_ref=ref,display_ref=ref,
                   source_locator=a['body_source']+':'+str(a['heading_line'])+'; source_ref='+ref,
                   source_title='Bright Saturday source-derived supplement from retained Coptic Reader',
                   source_edition='Retained English service; no fresh app visit or exact cross-edition equivalence claim',
                   provenance='Retained Coptic Reader source-derived Bright Saturday supplement',
                   display_label='Bright Saturday — '+a['service'],hour_theme='')
        span={'book':'Exod' if a.get('chapter_only') else '1Cor','chapter_start':chapter,'chapter_end':chapter,
              'verse_start':None if a.get('chapter_only') else 7,'verse_end':None if a.get('chapter_only') else 13,
              'source_ref':ref,'source_convention':'modern_english_reference',
              'canonical_mt_ref':ref,'canonical_lxx_ref':ref,'confidence':'source_qualified',
              'validation_basis':'Chapter-scope canticle index; no verse endpoints or whole-chapter claim' if a.get('chapter_only') else 'Retained printed heading and complete numbered English body, verses 7-13'}
        row['spans_json']=json.dumps([span],ensure_ascii=False,sort_keys=True)
        source={k:row[k]for k in ('source_family','source_kind','source_edition','source_title','source_locator')}
        proof=dict(_proof('bright_missing_appointment'),source_path=a['body_source'],
                   source_sha256=p['source_files'][a['body_source']],heading_line=a['heading_line'],
                   chapter_only=a.get('chapter_only',False),source_slot_role=a['slot_type'],
                   transport_qualification=a.get('transport_qualification','Existing Pauline slot type'),
                   scope=a.get('scope','Complete retained 1 Corinthians 5:7-13 selection'))
        row['source_disclosure']=_json([source])
        result.append(_disclose(row,proof))
    return result


def _daily_new(row,order):
    row=copy.deepcopy(row)
    row.update(service_order=10 if row['service_section']=='Midnight Praises' else 30,
               slot_order=2 if row['service_section']=='Midnight Praises' else 3,
               reading_order=order,source_group_key='final_site_review|'+row['identity_key'])
    return row


def _lent_rows(date,before):
    p=authenticate_sources()
    old=predecessor()['lent_reverse']
    selected=old[5:] if date=='2026-02-16' else old
    additions=[]
    slots={'pauline':'Pauline Epistle','catholicon':'Catholic Epistle','praxis':'Acts of the Apostles','psalm':'Psalm','gospel':'Gospel','prophecy':'OT'}
    for r in selected:
        row=copy.deepcopy(r)
        service='Matins' if r in old[:5] else 'Liturgy'
        ordinal=old.index(r)+1
        row.update(service_section=service,slot=slots[r['slot_type']],service_order=30 if service=='Matins' else 50,
                   slot_order=ordinal,source_group_key='working_cycle_first_lent_monday|'+row['identity_key'])
        source='sources/katameros-api/Core/KatamerosDatabase.db'
        proof=dict(_proof('bounded_working_cycle_first_lent_monday'),date=date,
                   source_path=source,source_sha256=p['source_files'][source],source_ordinal=ordinal,
                   recurrence_basis=p['lent']['recurrence_basis'],
                   printed_exodus_qualification=p['lent']['printed_exodus_difference'],
                   exact_printed_copy_claimed=False,reader_recurrence_approved=False)
        additions.append(_disclose(row,proof))
    kept=[copy.deepcopy(r) for r in before if r['service_section']=='Vespers' or date=='2026-02-16' and r['service_section']=='Matins']
    return kept+additions


def _daily_expected(date):
    import site_review_repairs as earlier
    p=plan()
    before=copy.deepcopy(predecessor()['daily'][date])
    after=copy.deepcopy(before)
    for join in p['additional_daily_annotation_joins']:
        if join['date']!=date:
            continue
        indices=[i for i,r in enumerate(after)if r==join['original']]
        if len(indices)!=1:
            raise ValueError('final site review ambiguous bounded daily source join')
        i=indices[0]
        row=earlier._annotate(after[i],join['proof'])
        proof=dict(_proof('bounded_daily_annotation_own_representation'),date=date,
                   source_join_basis=join['join_basis'],original_reverse_context=join['original_reverse'])
        after[i]=_disclose(row,proof)
    if date in p['lent']['dates']:
        after=_lent_rows(date,before)
    elif date in p['bright']['dates']:
        additions=[_daily_new(r,0)for r in _new_reverse()]
        # Early Agpeya Pauline precedes the later incense prophecy/Pauline.
        eph=next(r for r in after if r['service_section']=='Matins' and r['canonical_mt_ref']=='Eph 4:1-5')
        after.remove(eph)
        pos=next(i for i,r in enumerate(after)if r['service_section']=='Matins')
        after.insert(pos,eph)
        pos=next(i for i,r in enumerate(after)if r['service_section']=='Matins' and r['slot_type']=='psalm')
        after.insert(pos,additions[0])
        pos=next(i for i,r in enumerate(after)if r['service_section']=='Midnight Praises')+1
        after.insert(pos,additions[1])
        ps3=next(r for r in after if r['service_section']=='Liturgy' and r['identity_key']=='rid_6c9303917ae652573ee4')
        ps3['display_ref']='Ps 3:5,3 (Brenton covering locus Ps 3:4,6; source selection order)'
        ps3['source_selection_order_json']=_json({'selected_verse_order':[5,3],
            'source_path':'sources/coptic-reader/bright-composites-qualified-2026-10-25/saturday--liturgy-of-the-word.txt',
            'source_sha256':p['source_files']['sources/coptic-reader/bright-composites-qualified-2026-10-25/saturday--liturgy-of-the-word.txt'],
            'qualification':'Selected-body presentation order only; canonical covering membership unchanged; no whole-verse equivalence claim'})
        collapse=p['bright']['psalm82_daily_display_collapse']
        numeric=next(r for r in after if r['identity_key']==collapse['remove_numeric_id'] and r['service_section']=='Liturgy')
        held=next(r for r in after if r['identity_key']==collapse['keep_source_only_id'] and r['service_section']=='Liturgy')
        after.remove(numeric)
        sources=json.loads(held['source_disclosure'])
        sources.extend(json.loads(numeric['source_disclosure']))
        held['source_disclosure']=_json(sources)
        held['source_disclosure_count']=str(len(sources))
        held['coexisting_numeric_witness_json']=_json({'original_daily_witness':numeric,
            'qualification':'Retained provenance, not a second displayed selection or a coordinate approval; reverse historical witness preserved'})
        _disclose(held,dict(_proof('bounded_bright_psalm82_source_only_display_collapse'),date=date,
            canonical_coordinates_approved=False,displayed_source_selection_count=1,reverse_history_preserved=True))
    for i,row in enumerate(after,1):
        row['reading_order']=i
    return before,after


def _same(rows,expected):
    if len(rows)!=len(expected) or any(_json(r)!=_json(e)for r,e in zip(rows,expected)):
        raise ValueError('final site review complete source/context/coordinate/order mismatch')


def _recognizer():
    known=plan()['bright']['additions']
    def recognized(row):
        context=any(row.get('identity_key')==a['identity_key'] and
                    row.get('occasion')==a['occasion'] and row.get('service_section')==a['service'] for a in known)
        return context or MARKER in row or 'final_site_review' in row.get('source_disclosure','')
    return recognized


def project_base_rows(rows,*,date=None):
    recognized=_recognizer()
    if date is None:
        added=_new_reverse()
        if any(recognized(r)for r in rows):
            return project_base_rows(restore_base_rows(rows))
        return copy.deepcopy(rows)+added
    if date not in predecessor()['daily']:
        if any(recognized(r)for r in rows):
            raise ValueError('final site review wrong daily date')
        return copy.deepcopy(rows)
    before,after=_daily_expected(date)
    if any(MARKER in r for r in rows):
        _same(rows,after)
        return after
    _same(rows,before)
    return after


def restore_base_rows(rows,*,date=None):
    recognized=_recognizer()
    if date is None:
        expected=_new_reverse()
        added=[r for r in rows if recognized(r)]
        _same(added,expected)
        return [copy.deepcopy(r)for r in rows if not recognized(r)]
    if date not in predecessor()['daily']:
        if any(recognized(r)for r in rows):
            raise ValueError('final site review wrong daily date')
        return copy.deepcopy(rows)
    before,after=_daily_expected(date)
    _same(rows,after)
    return before


# A bounded supplement to this same late-owned layer. Original plans, inputs
# and historical membership sets remain immutable and explicitly stage-scoped.
SUPPLEMENT_INPUT_SHA256='31bf270d75d521cff306b8fc68067f8971173ebc02cb119db2ac6be2a5f2c024'
SUPPLEMENT_MARKER='site_review_supplement_json'
SUPPLEMENT_IDS=frozenset({'rid_5ec1f5c5b847553e2bfb','rid_34a83ab69dcba0a6fd3b',
    'rid_ca4b57d664d6ae9fe6fc','rid_753be171aee9fe41026f',
    'rid_8685f027ac3abc3243e1','rid_7b2fb603c3595c6509f6'})
SUPPLEMENT_DATES=frozenset({'2026-04-11','2027-05-01','2028-04-15','2027-08-02','2028-02-15'})


def supplement_inputs():
    return json.loads(_read(SOURCE+'supplement/inputs.json',SUPPLEMENT_INPUT_SHA256))


def _supplement_raw(record):
    raw=gzip.decompress(_read(record['path'],record['gzip_sha256']))
    if len(raw)!=record['bytes'] or hashlib.sha256(raw).hexdigest()!=record['sha256']:
        raise ValueError('final site review supplement raw source authentication failed')
    return raw


def _supplement_json(record):
    return json.loads(_supplement_raw(record))


def supplement_plan():
    return _supplement_json(supplement_inputs()['approval'])


def authenticate_supplement_sources():
    inputs=supplement_inputs()
    # Re-read/hash every immutable source; no cached approval verdict can hide
    # changed on-disk inputs. Content duplicates share one portable CAS member.
    checked=set()
    for record in inputs['files'].values():
        if record['path'] not in checked:
            _supplement_raw(record)
            checked.add(record['path'])
    return _supplement_json(inputs['approval'])


def _supplement_proof(kind,**fields):
    return dict(version='1.3.11',kind=kind,input_manifest_sha256=SUPPLEMENT_INPUT_SHA256,
                source_plan_sha256=supplement_inputs()['approval']['sha256'],
                fresh_app_verification=False,authority_status_promoted=False,**fields)


def _supplement_disclose(row,proof):
    row[SUPPLEMENT_MARKER]=_json(proof)
    sources=json.loads(row['source_disclosure'])
    for source in sources:
        source['site_review_supplement']=proof
    row['source_disclosure']=_json(sources)
    row['source_disclosure_count']=str(len(sources))
    return row


def _supplement_new_reverse():
    p=authenticate_supplement_sources();inputs=supplement_inputs()
    additions=p['bright_saturday']['approved_additions']+p['joseph_2027']['additional_source_only_psalm_witnesses']
    result=[]
    for a in additions:
        row=copy.deepcopy(predecessor()['bright_template'])
        row.update(dict(zip(p['key_fields'],a['tuple'])))
        source=inputs['files'][a['source_path']]
        printed=a['printed_reference']
        is_hold=not a['spans'];joseph=a['tuple'][1]=='ordinary_date_resolved'
        slot_type='psalm' if is_hold else 'gospel' if a['tuple'][7]=='Gospel' else 'source_label_preserved'
        selected=(a.get('selected_english') or p['bright_saturday']['distribution_psalm']['selected_english']) if is_hold else ''
        row.update(canonical_lxx_ref=a['canonical_lxx_ref'],spans_json=_json(a['spans']),
            display_ref=printed if is_hold else a['canonical_mt_ref'],
            slot_type=slot_type,slot_order=1,reading_type='scripture',reading_name='',
            authority_tier=a['authority_tier'],current_status=a['current_status'],removed_marker='',
            day_titles=p['joseph_2027']['context']['commemoration'] if joseph else 'Bright Saturday',
            source_title='Retained dated Joseph selection' if joseph else 'Retained Bright Saturday supplement',
            source_edition='Retained Coptic Reader source; printed selection and original clock separately qualified',
            source_locator=source['path']+'; raw_sha256='+source['sha256']+'; printed_ref='+_json(printed),
            provenance='Retained Reader body; independently source-approved bounded working projection',
            display_label='St. Joseph the Carpenter — '+row['service_section'] if joseph else 'Bright Saturday — '+row['service_section'],
            hour_theme='',attestation_years='',attestation_year_min='',attestation_year_max='')
        proof=_supplement_proof('source_only_psalm_selection' if is_hold else 'retained_bright_appointment',
            approved_key=a['tuple'],eligible_dates=a['eligible_dates'],printed_reference=printed,
            source_path=source['path'],source_raw_sha256=source['sha256'],
            qualification=a['qualification'],canonical_coordinates_approved=not is_hold,
            original_context=p['joseph_2027']['context'] if joseph else p['bright_saturday']['source_context'])
        if is_hold:
            row['source_selected_english']=selected
            row['source_only_selection_json']=_json(dict(proof,selected_english=selected,
                canonical_mt_ref='',canonical_lxx_ref='',spans=[],mapping_approval=False))
        row['source_disclosure']=_json([{k:row[k]for k in('source_family','source_kind','source_title','source_locator','source_edition')}])
        result.append(_supplement_disclose(row,proof))
    return result


def _supplement_recognized(row):
    owned_identity=(row.get('identity_key') in SUPPLEMENT_IDS and
        (row.get('identity_key')!='rid_ca4b57d664d6ae9fe6fc' or
         row.get('service_section')=='Distribution' or
         row.get('source_kind')=='bright_saturday_retained_supplement'))
    return (owned_identity or SUPPLEMENT_MARKER in row
            or 'site_review_supplement' in row.get('source_disclosure',''))


def _supplement_expected_daily(date):
    import site_review_repairs as earlier
    p=supplement_plan();inputs=supplement_inputs()
    selectors=_supplement_json(inputs['selectors'])
    added=_supplement_new_reverse()
    if date in p['bright_saturday']['eligible_dates']:
        before=project_base_rows(predecessor()['daily'][date],date=date)
        after=copy.deepcopy(before)
        rev,psalm,gospel=copy.deepcopy(added[:3])
        for row,order,slot_order in ((rev,35,1),(psalm,60,1),(gospel,60,2)):
            row.update(service_order=order,slot_order=slot_order,source_group_key='supplement|'+row['identity_key'])
        # Retained menu: Third/Sixth Hours, Revelation, then Ninth Hour.
        pos=next(i for i,r in enumerate(after)if r['service_section']=='9th Hour')
        after.insert(pos,rev)
        after.extend([psalm,gospel])
    else:
        before=project_base_rows(earlier.project_rows(selectors['predecessor_daily'][date],date=date),date=date)
        joseph=date=='2027-08-02'
        target=p['joseph_2027'] if joseph else p['amshir7_2028']
        descriptions=target['complete_expected_order']
        cycle=selectors['joseph_cycle' if joseph else 'amshir_cycle']
        checks=_supplement_json(inputs['body_checks'])
        source_docs=[{k:v for k,v in d.items()if k!='numbered_english_body'}for d in checks if d['target']==('Joseph' if joseph else 'Amshir')]
        after=[]
        for ordinal,d in enumerate(descriptions,1):
            found=[r for r in added if r['identity_key']==d['tuple'][0]]
            if found:
                row=copy.deepcopy(found[0])
            else:
                matches=[r for r in cycle if tuple(r.get(f,'')for f in p['key_fields'])==tuple(d['tuple'])]
                if len(matches)!=1:
                    raise ValueError('final site review supplement cycle selector ambiguity')
                row=copy.deepcopy(matches[0])
                row.update(service_section=d['target_service'],slot=d.get('target_slot',
                    {'psalm':'Psalm','gospel':'Gospel','pauline':'Pauline Epistle','catholicon':'Catholic Epistle','praxis':'Acts of the Apostles'}[row['slot_type']]))
            row.update(service_order={'Vespers':10,'Matins':30,'Liturgy':50}[row['service_section']],
                       slot_order=ordinal,source_group_key='supplement|'+row['identity_key'])
            proof=_supplement_proof('bounded_joseph_2027' if joseph else 'bounded_amshir_2028_working_cycle',
                date=date,approved_selector=d['tuple'],source_ordinal=ordinal,
                retained_context=target['context'] if joseph else target['retained_reader_context'],
                exact_2028_reader_confirmation=False,all_year_reader_recurrence_approved=False,
                qualification=target['projection'],source_documents=source_docs,
                psalm_attribution_limits=target.get('psalm_attribution_limits',[target['psalm_semantics']] if joseph else []))
            after.append(_supplement_disclose(row,proof))
    for i,row in enumerate(after,1):
        row['reading_order']=i
    return before,after


def _supplement_restore(rows,*,date=None):
    if date is None:
        expected=_supplement_new_reverse()
        owned=[r for r in rows if _supplement_recognized(r)]
        _same(owned,expected)
        return [copy.deepcopy(r)for r in rows if not _supplement_recognized(r)]
    if date not in SUPPLEMENT_DATES:
        if any(_supplement_recognized(r)for r in rows):
            raise ValueError('final site review supplement wrong daily date')
        return copy.deepcopy(rows)
    before,expected=_supplement_expected_daily(date)
    _same(rows,expected)
    return before


def project_rows(rows,*,date=None):
    if any(_supplement_recognized(r)for r in rows):
        restored=_supplement_restore(rows,date=date)
        return project_rows(restored,date=date)
    base=project_base_rows(rows,date=date)
    if date is None:
        return base+_supplement_new_reverse()
    if date not in SUPPLEMENT_DATES:
        return base
    before,after=_supplement_expected_daily(date)
    _same(base,before)
    return after


def restore_rows(rows,*,date=None):
    return restore_base_rows(_supplement_restore(rows,date=date),date=date)


def source_owned_supplement_empty_coordinates(row,*,date=None):
    if row.get('identity_key') not in SUPPLEMENT_IDS-{'rid_5ec1f5c5b847553e2bfb','rid_ca4b57d664d6ae9fe6fc'}:
        return False
    expected=_supplement_new_reverse() if date is None else _supplement_expected_daily(date)[1] if date in SUPPLEMENT_DATES else []
    found=[r for r in expected if r['identity_key']==row.get('identity_key')]
    if len(found)!=1:
        raise ValueError('final site review supplement wrong source-only date/context')
    _same([row],found)
    return not row['canonical_mt_ref'] and not row['canonical_lxx_ref'] and row['spans_json']=='[]'
