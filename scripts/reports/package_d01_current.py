"""Hash and bundle current authored review outputs, without OEM source downloads."""
import hashlib,json,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/current_handoff';G=R/'reports/prototype_d01/r02_guards'
files=[f for f in O.rglob('*') if f.is_file() and f.suffix in ('.md','.pdf','.csv','.json','.dxf') and f.name!='MANIFEST.json']
files += [G/n for n in ['D01_R02G_ASSEMBLY.FCStd','D01_R02G_ASSEMBLY.step','D01_R02G_GUARD_MOUNTINGS.pdf','cad_mesh.json','checks.json','README.md']]
files += [R/p for p in ['scripts/geometry/audit_d01_current.py','scripts/analysis/d01_current_pressure_budget.py','scripts/reports/build_d01_current_handoff.py','scripts/reports/package_d01_current.py','reports/prototype_d01/component_validation/OEM_P14_Max_points.csv']]
assert len(files)==len(set(files)) and all(f.exists() for f in files)
manifest=[dict(path=f.relative_to(R).as_posix(),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(files)]
(O/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(O/'AQI_D01_CURRENT_REVIEW_HANDOFF.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files+[O/'MANIFEST.json']:z.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(O/'AQI_D01_CURRENT_REVIEW_HANDOFF.zip') as z:
    assert z.testzip() is None
    for m in manifest:assert hashlib.sha256(z.read(m['path'])).hexdigest()==m['sha256']
print(f'Verified {len(manifest)} file hashes in review ZIP; original CAD unchanged.')
