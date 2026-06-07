#!/usr/bin/env bash
set -euo pipefail
cd /Users/georgeandraws/workspace/coptic-lectionary-research
Q="python3 out/scripts/query_lectionary.py"
{
echo '## HELP FLAGS'
$Q --help | sed -n '1,120p'
echo
for cmd in \
  "$Q --pascha-day Monday --hour 'First Hour' --limit 20" \
  "$Q --pascha-day Monday --hour 'Ninth Hour' --limit 20" \
  "$Q --pascha-day Tuesday --hour 'Ninth Hour' --limit 20" \
  "$Q --pascha-day Wednesday --hour 'Ninth Hour' --limit 20" \
  "$Q --pascha-day 'Great Thursday' --hour 'Ninth Hour' --limit 20" \
  "$Q --pascha-day 'Great Thursday' --hour 'Liturgy of Blessing of the Water' --limit 20" \
  "$Q --pascha-day 'Good Friday' --hour 'Third Hour' --limit 20" \
  "$Q --passage 'Isaiah 53' --include-crosswalk --limit 12" \
  "$Q --passage 'Isa 53' --include-crosswalk --limit 12" \
  "$Q --passage 'Isa 52:13-53:12' --include-crosswalk --limit 12" \
  "$Q --passage 'Wisdom 1:1-9' --include-crosswalk --limit 12" \
  "$Q --passage 'Wisdom 7:24-30' --include-crosswalk --limit 12" \
  "$Q --passage 'Wisdom 2:12-22' --include-crosswalk --limit 12" \
  "$Q --passage 'Lamentations 3:1-66' --include-crosswalk --limit 12" \
  "$Q --passage 'John 2' --include-crosswalk --limit 20" \
  "$Q --passage 'Isa 5' --include-crosswalk --limit 20" \
  "$Q --cycle-passage '40.5' --limit 10" \
  "$Q --passage '4 Maccabees 1:1-12' --include-crosswalk --limit 10" \
  "$Q --source-text 'Wisdom 7:24-30' --limit 10" \
  "$Q --source-text 'Psalm 62:7,6' --limit 10" \
  "$Q --special-service wedding --limit 10"; do
  echo
  echo '## COMMAND:' "$cmd"
  eval "$cmd"
done
} > audit_artifacts/final_regression_query_outputs_2026-06-06.txt
python3 - <<'PY'
import csv,json,re,subprocess,sys
from pathlib import Path
root=Path('/Users/georgeandraws/workspace/coptic-lectionary-research')
qout=(root/'audit_artifacts/final_regression_query_outputs_2026-06-06.txt').read_text()
checks={
 'monday_first_genesis': 'Monday | First Hour | OT1 | Gen 1:1-31; Gen 2:1-3' in qout,
 'monday_ninth_genesis': 'Monday | Ninth Hour | OT1 | Gen 2:15-25; Gen 3:1-24' in qout,
 'tuesday_ninth_genesis': 'Tuesday | Ninth Hour | OT1 | Gen 6:5-9:7' in qout,
 'wednesday_ninth_genesis': 'Wednesday | Ninth Hour | OT1 | Gen 24:1-9' in qout,
 'great_thursday_ninth_genesis_22': 'Great Thursday | Ninth Hour | OT1 | Gen 22:1-19' in qout,
 'great_thursday_ninth_genesis_14': 'Great Thursday | Ninth Hour | OT3 | Gen 14:17-20' in qout,
 'great_thursday_water_genesis_18': 'Great Thursday | Liturgy of Blessing of the Water | OT1 | Gen 18:1-23' in qout,
 'good_friday_third_genesis_48': 'Good Friday | Third Hour | OT1 | Gen 48:1-19' in qout,
 'isaiah_53_good_friday': 'Good Friday | Sixth Hour | OT2 | Isa 53:7-12' in qout,
 'isa_52_53_great_thursday': 'Great Thursday | Eleventh Hour | OT1 | Isa 52:13-53:12' in qout,
 'wisdom_1': 'Monday | Sixth Hour' in qout and 'Wis 1:1-9' in qout,
 'wisdom_7': 'Wednesday Eve | Eleventh Hour' in qout and 'Wis 7:24-30' in qout,
 'wisdom_2': 'Good Friday | First Hour' in qout and 'Wis 2:12-22' in qout,
 'lamentations_3': 'Good Friday | Twelfth Hour' in qout and 'Lam 3:1-66' in qout,
 'numeric_40_5': 'Matt 5:1-16' in qout,
 'source_text_flag_help': '--source-text' in qout,
 'special_service_flag_help': '--special-service' in qout,
}
# False positive sections: get command blocks
def block(cmdfrag):
    marker='## COMMAND: '+cmdfrag
    i=qout.find(marker)
    if i<0: return ''
    j=qout.find('\n## COMMAND:', i+1)
    return qout[i:] if j<0 else qout[i:j]
john2=block("python3 out/scripts/query_lectionary.py --passage 'John 2'")
isa5=block("python3 out/scripts/query_lectionary.py --passage 'Isa 5'")
checks['john2_no_john20_21_1john2']=not re.search(r'\b(Jn|John)\s*20\b|\b(Jn|John)\s*21\b|\b1\s*John\s*2\b|\b1Jn\s*2\b', john2)
checks['isa5_no_isa50_52_53_58']=not re.search(r'\bIsa\s*(50|52|53|58)\b|\bIsaiah\s*(50|52|53|58)\b', isa5)
# Counts/schema
count_summary={}
for name in ['reverse_lookup_crosswalk.csv','reverse_lookup_summary.csv','bible_chapter_lectionary_index.csv','bible_chapter_lectionary_occurrences.csv','pascha_source_text_index.csv','pascha_day_hour_index.csv']:
    p=root/'out/data'/name
    with p.open(newline='',encoding='utf-8') as f:
        r=csv.DictReader(f)
        rows=sum(1 for _ in r)
        count_summary[name]={'rows':rows,'schema':r.fieldnames}
checks['reverse_crosswalk_count']=count_summary['reverse_lookup_crosswalk.csv']['rows']==66504
checks['chapter_index_count']=count_summary['bible_chapter_lectionary_index.csv']['rows']==1351
checks['chapter_occurrence_count']=count_summary['bible_chapter_lectionary_occurrences.csv']['rows']==71315
checks['pascha_source_text_count']=count_summary['pascha_source_text_index.csv']['rows']==277
required_crosswalk_fields={'source_kind','source_family','source_table','source_file','service','day','hour','reading_slot','source_ref','raw_ref','normalized_ref','normalized_segment','book','chapter','verse_start','verse_end','provenance_url'}
checks['crosswalk_fields_present']=required_crosswalk_fields.issubset(set(count_summary['reverse_lookup_crosswalk.csv']['schema']))
# Changed files expected snippets
expectations={
 '033 - Jeremiah/Jeremiah 7 - Temple sermon.md':['John 2:13-17, is indexed for Pascha Monday Sixth Hour','not the temple-cleansing Gospel'],
 '033 - Jeremiah/Jeremiah 8 - Refused repentance and no balm in Gilead.md':['Jeremiah 8:17-9:6 is verified in the rebuilt local Coptic Pascha index for Great Thursday Eve First Hour'],
 '025 - Psalms/Psalm 62 (LXX 61) - My Soul Is Subject to God Alone.md':['Thursday Eve Eleventh Hour','source-text row'],
 '025 - Psalms/Psalm 122 (LXX 121) - I Was Glad When They Said to Me.md':['Psalm 122:4 at Holy Monday Sixth Hour'],
 '030 - Wisdom of Solomon/Wisdom of Solomon - Overview.md':['rebuilt local Coptic lectionary package'],
 '030 - Wisdom of Solomon/Audits/Wisdom of Solomon Series Plan.md':['rebuilt lectionary package now verifies Wisdom 2:12-22 and Wisdom 7:24-30'],
}
base=Path('/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Biblical Explanations/Kings Bible Study Project')
file_checks={}
for rel,subs in expectations.items():
    txt=(base/rel).read_text(encoding='utf-8')
    file_checks[rel]=all(s in txt for s in subs)
checks['changed_files_expected_snippets']=all(file_checks.values())
# stale scan
stale=json.loads((root/'audit_artifacts/final_bible_study_stale_claim_scan_2026-06-06.json').read_text())
checks['stale_critical_zero']=stale['summary']['stale_jer_8_wed_eve']==0 and stale['summary']['stale_ps122_tuesday_sixth']==0 and stale['summary']['stale_ps62_wed_eleven']==0 and stale['summary']['stale_wisdom_query_gap']==0
out={'checks':checks,'count_summary':count_summary,'changed_file_snippet_checks':file_checks,'stale_scan_summary':stale['summary'],'query_output_path':str(root/'audit_artifacts/final_regression_query_outputs_2026-06-06.txt')}
(root/'audit_artifacts/final_verification_summary_2026-06-06.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
failed=[k for k,v in checks.items() if not v]
if failed:
    raise SystemExit('FAILED: '+', '.join(failed))
PY
