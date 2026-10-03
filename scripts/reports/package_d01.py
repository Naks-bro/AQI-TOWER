"""Package only D01 deliverables and reproducible sources, preserving project paths."""
import json,hashlib,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01'
names=['README.md','AQI_D01_ENGINEERING_PACKAGE.pdf','D01_ASSEMBLY.FCStd','D01_EXPLODED.FCStd','D01_ASSEMBLY.step','D01_ASSEMBLY.png','D01_EXPLODED.png','D01_BOM.csv','geometry_checks.json','reopen_checks.json','pressure_results.json','pressure_curves.csv','panel_geometry.json','cad_mesh.json']
files=[O/n for n in names]+sorted((O/'panel_dxf_REVIEW_ONLY').glob('*.dxf'))
files += [R/p for p in ['cad/parametric/d01_r00.json','scripts/geometry/build_d01.py','scripts/geometry/verify_d01.py','scripts/analysis/d01_pressure.py','scripts/reports/build_d01_delivery.py','scripts/reports/package_d01.py']]
S=R/'data/prototype_d01/sources'
files += [S/n for n in ['ARCTIC_P14_Max_Spec.pdf','ARCTIC_P14_Max_2D_20250124.pdf','ARCTIC_140mm_mounting_template.pdf','SP_MERV13_0303.pdf','Brisa_CC0_reference.dxf','Brisa_LICENSE.txt','Brisa_repository_files.json']]
assert all(p.exists() for p in files)
records=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
(O/'MANIFEST.json').write_text(json.dumps({'revision':'D01-R00','status':'REVIEW ONLY - NOT RELEASED FOR FABRICATION OR ENERGIZING','files':records},indent=2))
zpath=R/'reports/AQI_D01_REVIEW_PACKAGE.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files+[O/'MANIFEST.json']:z.write(p,p.relative_to(R))
with zipfile.ZipFile(zpath) as z:assert z.testzip() is None
print(json.dumps({'zip':str(zpath),'files':len(files)+1,'bytes':zpath.stat().st_size}))
