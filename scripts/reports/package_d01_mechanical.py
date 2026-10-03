"""Bundle authored mechanical review outputs with integrity checks, not OEM downloads."""
import json,hashlib,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/mechanical_package'
cad=O/'D01_R03M_ASSEMBLY.FCStd';sha=hashlib.sha256(cad.read_bytes()).hexdigest()
for name in ('service_checks.json','assembly_audit.json'):
    assert json.loads((O/name).read_text())['source_sha256']==sha,name
checks=json.loads((O/'checks.json').read_text());assert checks['STEP_valid'] and not checks['clashes_mm3']
files=[f for f in O.rglob('*') if f.is_file() and f.suffix in ('.FCStd','.step','.pdf','.json','.csv','.dxf','.md') and f.name!='MANIFEST.json']
files += [R/s for s in ['scripts/geometry/build_d01_mechanical_package.py','scripts/geometry/audit_d01_current.py','scripts/geometry/check_d01_mechanical_service.py','scripts/analysis/d01_mechanical_screen.py','scripts/reports/build_d01_mechanical_report.py','scripts/reports/package_d01_mechanical.py']]
files += [R/s for s in ['scripts/reports/build_d01_delivery.py','reports/prototype_d01/r02_guards/D01_R02G_ASSEMBLY.FCStd','reports/prototype_d01/r02_guards/cad_mesh.json']]
files += [O/'D01_ASSEMBLY.png',O/'D01_EXPLODED.png']
manifest=[dict(path=f.relative_to(R).as_posix(),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(files)]
(O/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(O/'AQI_D01_MECHANICAL_PACKAGE.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files+[O/'MANIFEST.json']:z.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(O/'AQI_D01_MECHANICAL_PACKAGE.zip') as z:
    assert z.testzip() is None
    for m in manifest:assert hashlib.sha256(z.read(m['path'])).hexdigest()==m['sha256']
print('Verified mechanical ZIP:',len(manifest),'files; current native/audit/service hashes match.')
