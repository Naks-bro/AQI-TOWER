"""Reopen native D01, reimport STEP, inspect volumes and drawing interfaces."""
import json,math
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01'
d=A.openDocument(str(O/'D01_ASSEMBLY.FCStd'))
objs=[o for o in d.Objects if hasattr(o,'Shape')]
native_volume=sum(o.Shape.Volume for o in objs)
step=Part.read(str(O/'D01_ASSEMBLY.step'))
e=A.openDocument(str(O/'D01_EXPLODED.FCStd'))
ev=sum(o.Shape.Volume for o in e.Objects if hasattr(o,'Shape'))
g=json.loads((O/'geometry_checks.json').read_text());panels=json.loads((O/'panel_geometry.json').read_text())
ret=next(p for p in panels if p['name']=='M04_RETAINER');plate=next(p for p in panels if p['name']=='M06_FAN_PLATE')
tests={
 'native_73_objects':len(objs)==73,
 'native_all_valid':all(o.Shape.isValid() for o in objs),
 'step_valid':step.isValid(),
 'step_volume_matches':math.isclose(step.Volume,native_volume,rel_tol=1e-7),
 'exploded_volume_matches':math.isclose(ev,native_volume,rel_tol=1e-9),
 'body_checks_clear':not g['positive_volume_clashes_mm3'],
 'hardware_checks_clear':not g['hardware_clashes_mm3'],
 'retainer_edge_centres_at_least20':all(min(x,y,ret['w']-x,ret['h']-y)>=20 for x,y,r in ret['circles']),
 'fan_plate_four_apertures':sum(r>60 for x,y,r in plate['circles'])==4,
 'fan_plate_16_bolt_holes':sum(r<3 for x,y,r in plate['circles'])==16,
 'twelve_plywood_parts':sum(p['qty'] for p in panels if p['thick']==9)==12
}
assert all(tests.values()),tests
result={'tests':tests,'native_volume_mm3':native_volume,'STEP_volume_mm3':step.Volume,'status':'DIGITAL GEOMETRY ONLY; NOT FABRICATION RELEASE'}
(O/'reopen_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
