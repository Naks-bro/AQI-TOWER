"""Close E04 assumed service-volume conflicts without shrinking reservations.
E05 is the same enclosure: hub rotated90deg, controller moved, lid row Y55.
Actual cable bends/retention/protection remain unverified. No fabrication release.
"""
from pathlib import Path
import hashlib,json,csv
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/electrical_package/control_module'
data=json.loads((O/'LID_CONTROL_CHECKS.json').read_text())
oem_path=R/'tmp/control_oem/step/1554XA2GY.stp'
oem=Part.read(str(oem_path));assert len(oem.Solids)==24
assert hashlib.sha256(oem_path.read_bytes()).hexdigest()==data['OEM_box_sha256']
doc=A.openDocument(str(O/'D01_E04_LID_CONTROL_ENVELOPES.FCStd'))
assert len(doc.Objects)==18
V=A.Vector
for name in ('H1_NA_FH1','H1_CONNECTOR_SPACE_ASSUMED'):
 shape=doc.getObject(name).Shape.copy();shape.rotate(V(0,0,0),V(0,0,1),90);shape.translate(V(-37,-90,0))
 doc.getObject(name).Shape=shape
for name in ('SC1_NA_FC1','SC1_CONNECTOR_SPACE_ASSUMED'):
 shape=doc.getObject(name).Shape.copy();shape.translate(V(28,-90,0));doc.getObject(name).Shape=shape
shell=Part.makeBox(300,200,120.08,V(-150,-100,-70.08)).cut(Part.makeBox(290,190,111,V(-145,-95,-65)))
checks=[]
keeps=['CTRL1_WIRE_SPACE_ASSUMED','H1_CONNECTOR_SPACE_ASSUMED','SC1_CONNECTOR_SPACE_ASSUMED']
for b in data['buttons']:
 x=b['centre_mm'][0];b['centre_mm'][1]=55
 levels=sorted(v.Point.z for e in oem.Solids[1].common(Part.makeLine(V(x,55,-20),V(x,55,60))).Edges for v in e.Vertexes)
 assert len(levels)==2 and all(abs(a-z)<.01 for a,z in zip(levels,[46,50]))
 b['lid_surface_levels_mm']=levels
 for suffix in ('FACE_PROXY','REAR_ASSUMED','WIRE_TAIL_ASSUMED'):
  obj=doc.getObject(b['name']+'_'+suffix);shape=obj.Shape.copy();shape.translate(V(0,55,0));obj.Shape=shape
  if suffix!='FACE_PROXY':checks.append(obj.Name)
 b['rear_assumed_bounds_mm'][1]+=55;b['rear_assumed_bounds_mm'][4]+=55
 b['wire_tail_assumed_bounds_mm'][1]+=55;b['wire_tail_assumed_bounds_mm'][4]+=55
 combined=doc.getObject(b['name']+'_REAR_ASSUMED').Shape.fuse(doc.getObject(b['name']+'_WIRE_TAIL_ASSUMED').Shape)
 b['assumed_service_overlap_mm3']={n:combined.common(doc.getObject(n).Shape).Volume for n in keeps}
 b['minimum_body_gaps_mm']={n:combined.distToShape(doc.getObject(n).Shape)[0] for n in ('CTRL1_OPTA_LITE','H1_NA_FH1','SC1_NA_FC1')}
 assert all(v>.01 for v in b['minimum_body_gaps_mm'].values())
 assert all(v<.01 for v in b['assumed_service_overlap_mm3'].values())
 shell=shell.cut(Part.makeCylinder(11.15,10,V(x,55,45)))
doc.getObject('CB1_SIMPLIFIED_ENVELOPE').Shape=shell
checks+=keeps+['CTRL1_OPTA_LITE','H1_NA_FH1','SC1_NA_FC1']
actual=[]
for name in checks:
 shape=doc.getObject(name).Shape
 hits=[dict(solid=i,volume_mm3=shape.common(s).Volume) for i,s in enumerate(oem.Solids) if i!=3 and shape.common(s).Volume>.01]
 assert not hits,(name,hits)
 actual.append(dict(object=name,hits=hits))
service_pairs=[]
for i,n in enumerate(keeps):
 for m in keeps[i+1:]:
  a,b=doc.getObject(n).Shape,doc.getObject(m).Shape
  v=a.common(b).Volume;assert v<.01
  service_pairs.append(dict(objects=[n,m],overlap_mm3=v,gap_mm=a.distToShape(b)[0]))
assert len(service_pairs)==3
assert len({tuple(row['objects']) for row in service_pairs})==3
assert all(row['objects'][0]!=row['objects'][1] for row in service_pairs)
body_names=['CTRL1_OPTA_LITE','H1_NA_FH1','SC1_NA_FC1']
for i,n in enumerate(body_names):
 for m in body_names[i+1:]:assert doc.getObject(n).Shape.common(doc.getObject(m).Shape).Volume<.01
doc.recompute();doc.saveAs(str(O/'D01_E05_CURRENT_CONTROL_LAYOUT.FCStd'))
Part.export(list(doc.Objects),str(O/'D01_E05_CURRENT_CONTROL_LAYOUT.step'))
step=O/'D01_E05_CURRENT_CONTROL_LAYOUT.step';step.write_text('\n'.join(x.rstrip() for x in step.read_text().splitlines())+'\n')
placements=[]
for obj in doc.Objects:
 box=obj.Shape.BoundBox
 placements.append(dict(name=obj.Name,bounds_mm=[box.XMin,box.YMin,box.ZMin,box.XMax,box.YMax,box.ZMax],status=obj.EvidenceStatus))
A.closeDocument(doc.Name)
check=A.openDocument(str(O/'D01_E05_CURRENT_CONTROL_LAYOUT.FCStd'))
assert len(check.Objects)==18 and all(o.Shape.isValid() for o in check.Objects)
A.closeDocument(check.Name);assert len(Part.read(str(step)).Solids)==18
tower=R/'reports/prototype_d01/mechanical_package/D01_R03M_ASSEMBLY.FCStd'
assert hashlib.sha256(tower.read_bytes()).hexdigest()==data['native_tower_sha256']
data.update(revision='E05',status='ASSUMED SERVICE-VOLUME CONFLICTS CLOSED / ACTUAL WIRING AND BUILD RELEASE OPEN',
 actual_box_checks=actual,service_pair_checks=service_pairs,placements=placements,
 changes={'hub':'Rotate90 degrees about Z; translate X-37,Y-90 from E03',
 'controller':'Translate X+28,Y-90 from E03','buttons':'Row Y55 instead of0; X unchanged'},
 digital_routing_conflict_closed=True,actual_routing_verified=False)
data['limitations'][1]='All unchanged assumed service/wire-tail reservations now mutually clear; actual lead bends/connectors still unknown'
data['sources']['current_contacts']='https://download.se.com/files?p_Doc_Ref=0100CT2401-SEC-19'
data['sources']['current_contacts_page']='19-42; dated22 July2026; tables19.98/19.99; no numeric minimum switching range supplied'
(O/'CURRENT_CONTROL_CHECKS.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
with (O/'CURRENT_CONTROL_PLACEMENT.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Object','Xmin','Ymin','Zmin','Xmax','Ymax','Zmax','Status'])
 for p in placements:w.writerow([p['name'],*p['bounds_mm'],p['status']])
print('PASS:18 reopened CAD objects/STEP solids;12 reservations/bodies clear23 nonpanel box solids each; unchanged reservations mutually clear; native tower unchanged.')
