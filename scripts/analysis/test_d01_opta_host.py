"""Compile/run actual C++ core and .ino with host-only GPIO shim. No installation."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
F=ROOT/'firmware/d01_opta_review'
compiler=shutil.which('g++')
if not compiler:
    raise SystemExit('Host C++ compiler NOT INSTALLED. No target-board compilation or installation attempted.')
with tempfile.TemporaryDirectory(prefix='aqi-opta-host-') as temp:
    exe=Path(temp)/'control_test.exe'
    result=subprocess.run([compiler,'-std=c++17','-Wall','-Wextra','-Werror','-pedantic',
                           '-I',str(F/'test_support'),str(F/'test_control.cpp'),'-o',str(exe)],capture_output=True,text=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    run=subprocess.run([str(exe)],capture_output=True,text=True,check=True)
    record=json.loads(run.stdout)
record.update(status='HOST SYNTHETIC TESTS PASS / NOT BOARD COMPILED OR SAFETY IMPLEMENTATION',
              compiler_version=subprocess.run([compiler,'--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],
              source_sha256={str(p.relative_to(F)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(F.rglob('*')) if p.is_file() and p.suffix in ('.h','.cpp','.ino')})
(ROOT/'reports/prototype_d01/electrical_package/OPTA_HOST_CHECKS.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,indent=2))
