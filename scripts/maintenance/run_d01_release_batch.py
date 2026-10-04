"""One-command synthetic/calculation batch. Never installs, uploads or energizes.

Run from repository or extracted technical bundle's engineering/ with the existing
Python runtime. --calculations-only skips delivery consistency (ZIPs not inside ZIP).
Results deliberately cannot change build-release or physical-test status.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--calculations-only',action='store_true')
args=parser.parse_args()
names=['test_d01_electrical_closure.py','test_d01_mass_stability.py',
       'test_d01_current_filter_screen.py','test_d01_opta_host.py',
       'test_d01_mechanical_release_batch.py','test_d01_electrical_release_batch.py']
commands=[[sys.executable,str(ROOT/'scripts/analysis'/n)] for n in names]
if not args.calculations_only:
 commands.append([sys.executable,str(ROOT/'scripts/maintenance/check_d01_handoff_consistency.py')])
results=[]
for command in commands:
 script=Path(command[1]);print('Checking '+script.name,flush=True)
 if not script.is_file():raise SystemExit('Missing batch script: '+str(script))
 process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
 record={'script':script.relative_to(ROOT).as_posix(),'returncode':process.returncode,
         'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),
         'stdout':process.stdout,'stderr':process.stderr}
 results.append(record)
 if process.returncode:
  print(process.stdout);print(process.stderr);raise SystemExit(process.returncode)
output=ROOT/'reports/prototype_d01/batch_summary'
output.mkdir(parents=True,exist_ok=True)
data={'status':'SYNTHETIC/CALCULATION BATCH PASS; NOT BUILD OR SAFETY RELEASE',
      'physical_tests':0,'physical_prototypes':0,'construction_release':False,
      'energization_release':False,'calculations_only':args.calculations_only,'commands':results}
if args.calculations_only:
 (output/'BATCH_VERIFICATION.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(f'PASS: {len(results)} verification programs. No physical proof or release inferred.')
