"""Portable scratch clone plus on-disk corruption and guard-bypass counterproof."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[3]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report-dir',type=Path,required=True);args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='matins-portable-') as temp:
        clone=Path(temp)/'repository';clone.mkdir();home=Path(temp)/'nonexistent-home'
        for name in ['build_lectionary_reference.py','matins_source_projection.py','calendar_resolution.py','reading_context_overlays.py','passage_normalization.py']:
            shutil.copy2(ROOT/name,clone/name)
        fixture=clone/'sources/coptic-reader/matins-source-accepted-2026-10-07'
        # Read-only evidence hardlinks avoid redundant 300 MB scratch copies.
        # Every corruption probe unlinks its clone file before writing it.
        shutil.copytree(Path(__file__).parent,fixture,copy_function=os.link)
        shutil.copy2(ROOT/'sources/lectionary_corrections.json',clone/'sources/lectionary_corrections.json')
        env={**os.environ,'HOME':str(home),'PYTHONDONTWRITEBYTECODE':'1'}
        run=subprocess.run([sys.executable,'-B',str(fixture/'test_upstream_matins.py'),
             'UpstreamMatins.test_59_pairs_complete_raw_order_bodies_history_and_untargeted',
             'UpstreamMatins.test_source_search_omits_unprinted_verses_and_keeps_composite_order',
             'UpstreamMatins.test_projected_table_mutations_rejected_at_real_index_api'],cwd=clone,env=env,capture_output=True,text=True)
        (args.report_dir/'PORTABLE-GREEN.log').write_text(run.stdout+run.stderr)
        probe=clone/'probe.py'
        probe.write_text('''import json
from pathlib import Path
import matins_source_projection as m
f=m.load_dated_matins_fixture()
r=f['corpus']['records'][0]['source_record']
paths=[('body',f['root']/f['path_map'][r['text_path']]),('context',f['root']/f['path_map'][r['context_files'][0]['path']]),('review',f['root']/'evidence/lent-prophecy-independent-review-04/FINAL-RECEIPT.json')]
results=[]
for label,path in paths:
 original=path.read_bytes();path.unlink();path.write_bytes(original[:-1]+b'X')
 try:m.authenticate_dated_matins_fixture(f)
 except ValueError as error:results.append({'mutation':label,'rejected':True,'error':str(error)})
 else:results.append({'mutation':label,'rejected':False})
 path.write_bytes(original)
print(json.dumps(results))
''')
        corrupt=subprocess.run([sys.executable,'-B',str(probe)],cwd=clone,env=env,capture_output=True,text=True)
        (args.report_dir/'RAW-CORRUPTION.log').write_text(corrupt.stdout+corrupt.stderr)
        mutation=clone/'mutant.py'
        mutation.write_text('''import importlib.util,unittest
from pathlib import Path
p=Path('sources/coptic-reader/matins-source-accepted-2026-10-07/test_upstream_matins.py')
spec=importlib.util.spec_from_file_location('matins_tests',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
# Equivalent production fault: remove the whole-table authentication boundary.
module.bref.candidate_matins_index=lambda rows:[{**r,'matched_ref':''} for r in rows]
suite=unittest.TestSuite([module.UpstreamMatins('test_projected_table_mutations_rejected_at_real_index_api')])
result=unittest.TextTestRunner(verbosity=2).run(suite)
print('MUTANT_FAILURES',len(result.failures),'MUTANT_ERRORS',len(result.errors))
raise SystemExit(1 if not result.wasSuccessful() else 0)
''')
        mutant=subprocess.run([sys.executable,'-B',str(mutation)],cwd=clone,env=env,capture_output=True,text=True)
        (args.report_dir/'MUTATION-RED.log').write_text(mutant.stdout+mutant.stderr)
        results=json.loads(corrupt.stdout) if corrupt.returncode==0 else []
        summary={'portable_targeted_tests':3,'portable_green_exit':run.returncode,
                 'fresh_home_created':home.exists(),'original_absolute_paths_required':False,
                 'raw_corruptions':results,'raw_corruption_probe_exit':corrupt.returncode,
                 'guard_bypass_mutant_exit':mutant.returncode,
                 'guard_bypass_mutant_failures_expected':12,
                 'guard_bypass_mutant_observed':'MUTANT_FAILURES 12 MUTANT_ERRORS 0' in mutant.stdout,
                 'no_build_publish_network':True}
        (args.report_dir/'portability-mutation-results.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps(summary,indent=2))
        return 0 if run.returncode==0 and not home.exists() and len(results)==3 and all(r['rejected'] for r in results) and summary['guard_bypass_mutant_observed'] else 1
if __name__=='__main__':sys.exit(main())
