"""Read-only R03M guard/access geometry. Not a reach or strength certification."""
from pathlib import Path
import hashlib,json
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/mechanical_package'
path=O/'D01_R03M_ASSEMBLY.FCStd';before=hashlib.sha256(path.read_bytes()).hexdigest()
doc=A.openDocument(str(path));V=A.Vector
def obj(n):
    o=doc.getObject(n);assert o is not None,n;return o
def bounds(sh):
    b=sh.BoundBox;return dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
outer=obj('G10_Outer_fabricated_guard').Shape;inner=obj('G10_Inner_fabricated_guard').Shape
plate=obj('M06_Fan_plate').Shape
fans=[obj(f'F02_P14_Max_{i}').Shape for i in range(1,5)]
# Design face elevations checked against actual coplanar planar face geometry.
def horizontal_faces(sh):
    out=[]
    for f in sh.Faces:
        b=f.BoundBox
        if b.ZLength<1e-6 and f.Area>10000:out.append({'z_mm':b.ZMin,'area_mm2':f.Area})
    return out
of=horizontal_faces(outer);inf=horizontal_faces(inner)
assert any(abs(f['z_mm']-630)<1e-6 for f in of)
assert any(abs(f['z_mm']-531)<1e-6 for f in inf)
rows=[]
for i,fan in enumerate(fans,1):
    b=bounds(fan)
    rows.append(dict(fan=i,bounds_mm=b,upper_face_to_fan_envelope_mm=630-b['zmax'],
        lower_face_to_fan_envelope_mm=b['zmin']-531,
        note='Fan body envelope, NOT blade position or certified reach distance'))
reservations=[o for o in doc.Objects if o.Name.startswith('E02_Cable_corridor')]
crossings=[]
for ob in reservations:
    for name,guard in [('outer',outer),('inner',inner)]:
        vol=ob.Shape.common(guard).Volume
        if vol>1e-6:crossings.append(dict(corridor=ob.Name,guard=name,positive_intersection_mm3=vol))
data=dict(status='ACCESS REVIEW ONLY - NO SAFE-REACH PASS',source_sha256=before,
  source_unchanged=hashlib.sha256(path.read_bytes()).hexdigest()==before,
  face_evidence={'outer':of,'inner':inf},fan_clearances=rows,
  guard_plate_minimum_distances_mm={'outer':outer.distToShape(plate)[0],'inner':inner.distToShape(plate)[0]},
  distance_warning='Minimum contact/distance somewhere does not prove perimeter closure; welds, deflection, tolerances and attachment not qualified.',
  cable_corridor_guard_intersections=crossings,
  cable_corridor_bounds_mm={o.Name:bounds(o.Shape) for o in reservations},
  cable_guard_distances_mm={o.Name:o.Shape.distToShape(outer)[0] for o in reservations},
  perforation_warning='CAD faces are solid envelopes; actual proposed perforations live in guard_pattern.json. Never use these solid faces to claim finger-probe exclusion.',
  service_boundary='Filter removal does not intentionally remove either fan guard. Removing a guard or top assembly exposes a different hazard state; isolated servicing only.',
  physical_tests=0)
assert data['source_unchanged'];assert len(rows)==4
(O/'GUARD_ACCESS_AUDIT.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(data,indent=2));A.closeDocument(doc.Name)
