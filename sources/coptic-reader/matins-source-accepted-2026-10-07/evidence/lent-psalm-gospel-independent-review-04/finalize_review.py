"""Freeze reviewer artifacts after independent audit and visual inspection."""
import datetime,hashlib,json
from pathlib import Path
O=Path(__file__).resolve().parent;P=O.parent/'lent-source-completion-04'
def h(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=json.loads((O/'visual-index.json').read_text())
fallback=[1,3,5,11,15,17,23,33,39,41,43,53,57,59,65,89,103]
rows=[]
for i,r in enumerate(a):
    assert h(r['path'])==r['sha256']
    rows.append(dict(r,index=i,inspected_full_sheet=f'pg-visual-{i//12:02}.jpg',literal_top_crop_sheet=f'header-crops-{i//28:02}.jpg',Gospel_full_column_fallback=(f'Gospel-fallback-{fallback.index(i)//3:02}.jpg' if i in fallback else None),ready=True,loading_overlay=False,literal_reference_matches=True,whitespace_authentication='literal raw text bytes; pixels not used to infer tab or space width'))
visual={'method':'independent native vision inspection; all 110 candidate reference images; full-sheet inspection followed by literal crops and 17 full-English-column fallback panels','candidate_reference_images':rows,'producer_home_sheets_inspected':[{'path':str(P/f'contexts-ready-{i:02}.jpg'),'sha256':h(P/f'contexts-ready-{i:02}.jpg')} for i in range(8)],'producer_home_panel_count':57,'Presentation_numeric_panel':{'path':str(P/'presentation-panel/selected-date-panel.png'),'sha256':h(P/'presentation-panel/selected-date-panel.png'),'numeric_observed':'Meshir 8,1742; February15,2026'},'old_PG_home_inspection_sheets':['old-pg-visual-00.jpg','old-pg-visual-01.jpg'],'Jonah_menu_rubric_inspection_sheet':'jonah-menu-visual.jpg','Jonah_dates':['2026-02-02','2026-02-03','2026-02-04','2026-02-05'],'scope':'rendered portions authenticate readiness/headings; whole bodies authenticated by independent hash and source-block audits'}
save('visual-ledger.json',visual)
summary=json.loads((O/'summary.json').read_text())
accepted=[json.loads(l) for l in (O/'accepted-dated-oracle.jsonl').read_text().splitlines()]
assert len(accepted)==55 and len({(r['civil_date'],r['slot']) for r in accepted})==55
assert sum(r['duplicate_qualified_key_witness'] for r in accepted)==2
assert all(not r['recurrence_approved'] and not r['canonical_coordinates_approved'] and not r['production_activation_approved'] for r in accepted)
# Final read-back of every input binding, after all owned writes.
for name,value in json.loads((P/'HASHES.json').read_text()).items():assert h(P/name)==value,name
for r in json.loads((P/'evidence-manifest.json').read_text()):assert h(r['path'])==r['sha256'],r['path']
for r in json.loads((P/'source-input-hashes.json').read_text()):assert h(r['path'])==r['sha256'],r['path']
assert h(P/'FINAL-RECEIPT.json')=='c4248755cba79f12d76803d932e25d09bd38a7fc7f71359744e1d2d9c2b80001'
artifacts={str(x.relative_to(O)):h(x) for x in sorted(O.rglob('*')) if x.is_file() and x.name not in ['HASHES.json','FINAL-RECEIPT.json']}
save('HASHES.json',artifacts)
receipt={'schema':'lectionary.independent-dated-PG-review.v1','reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'accept_55_candidate_Matins_PG_documents_at_original_dated_scope_only','summary':summary,'input_receipt_file_sha256':h(P/'FINAL-RECEIPT.json'),'input_hash_manifest_sha256':h(P/'HASHES.json'),'artifact_count':len(artifacts),'artifact_hash_manifest':'HASHES.json','artifact_hash_manifest_sha256':h(O/'HASHES.json'),'accepted_oracle_sha256':h(O/'accepted-dated-oracle.jsonl'),'REPORT_sha256':h(O/'REPORT.md'),'reviewer_code_sha256':h(O/'independent_review.py'),'visual_ledger_sha256':h(O/'visual-ledger.json'),'production_activation_approved':False,'canonical_coordinates_approved':False,'recurrence_approved':False,'Prophecies_candidate_approval':False,'Jonah_scope':'four dated menu/no-Vespers witnesses only; no uncaptured Liturgy appointments','remaining':['canonical Psalm/English-edition and fragment coordinates','uncaptured all-year recurrence/collision applicability','uncaptured Jonah Liturgy bodies','separate independent Prophecies review'],'writes_scope':str(O),'source_inputs_preserved':True}
receipt['receipt_payload_sha256']=hashlib.sha256(json.dumps(receipt,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
save('FINAL-RECEIPT.json',receipt)
# Verify every emitted artifact from disk, including all accepted serialized rows.
for name,value in json.loads((O/'HASHES.json').read_text()).items():assert h(O/name)==value,name
read=json.loads((O/'FINAL-RECEIPT.json').read_text());expected=read.pop('receipt_payload_sha256');assert hashlib.sha256(json.dumps(read,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==expected
print(json.dumps({'summary':summary,'artifact_count':len(artifacts),'final_receipt_sha256':h(O/'FINAL-RECEIPT.json'),'final_all_input_and_output_hashes_verified':True},indent=2))
