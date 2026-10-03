"""R03M straight filter removal checks; does not approve powered access."""
import json,hashlib
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/mechanical_package';path=O/'D01_R03M_ASSEMBLY.FCStd'
sha=hashlib.sha256(path.read_bytes()).hexdigest();doc=A.openDocument(str(path));V=A.Vector
meta={m['name']:m for m in json.loads((O/'cad_mesh.json').read_text())};results=[]
for rear in (False,True):
    suffix='_Rear' if rear else '_Front';sweep=Part.makeBox(370,240,290,V(90,-255,160))
    if rear:sweep=sweep.mirror(V(0,180,0),V(0,1,0))
    hits=[]
    for ob in doc.Objects:
        if meta[ob.Name]['kind']=='reservation':continue
        if ob.Name.endswith(suffix) and ob.Name.startswith(('A03_','A04_','H10_Service','H11_Service')):continue
        vol=sweep.common(ob.Shape).Volume
        if vol>.05:hits.append([ob.Name,vol])
    results.append(dict(side=suffix[1:],filter_outward_travel_mm=200,clashes_mm3=hits))
audit=dict(source_sha256=sha,source_unchanged=hashlib.sha256(path.read_bytes()).hexdigest()==sha,filter_sweeps=results,
    limits='Retainer and service nuts/washers removed first. Hand/tool and retainer trajectories, weld beads, manufacturing variation and actual filter deformation unverified. No powered access.')
assert audit['source_unchanged'] and not any(s['clashes_mm3'] for s in results)
(O/'service_checks.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
