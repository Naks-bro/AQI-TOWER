"""Detail saved R02 adapter hardware; nominal fit only, not construction release."""
import json, hashlib, math
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2]; B=R/'reports/prototype_d01/r02_adapter'
O=B/'hardware_detail'; O.mkdir(exist_ok=True)
base=B/'D01_R02_ASSEMBLY.FCStd'; digest=hashlib.sha256(base.read_bytes()).hexdigest()
src=A.openDocument(str(base)); doc=A.newDocument('D01_R02H')
meta={m['name']:m for m in json.loads((B/'cad_mesh.json').read_text())}
V=A.Vector; records=[]; changed=set()
def cyl(x,y,z,r,t):return Part.makeCylinder(r,t,V(x,y,z),V(0,1,0))
def washer(x,y,z):return cyl(x,y,z,6,1).cut(cyl(x,y-1,z,2.15,3))
def nut(x,y,z):
    radius=7/math.sqrt(3)
    pts=[V(x+radius*math.cos(i*math.pi/3),y,z+radius*math.sin(i*math.pi/3)) for i in range(6)]
    return Part.Face(Part.Wire(Part.makePolygon(pts+[pts[0]]).Edges)).extrude(V(0,5,0)).cut(cyl(x,y-1,z,2,7))
def add(name,shape,rear=False,note='Nominal hardware envelope; no threads, torque or strength approval',existing=None):
    if existing is None:
        name+= '_Rear' if rear else '_Front'
        changed.add(name)
        if rear:shape=shape.mirror(V(0,180,0),V(0,1,0))
        m=dict(name=name,kind='hardware',color='#abb9c3',explode=[0,0,0],note=note)
    else:m={k:existing[k] for k in ('name','kind','color','explode','note')}
    obj=doc.addObject('PartDesign::Feature',name);obj.Shape=shape
    obj.addProperty('App::PropertyString','ReleaseStatus');obj.ReleaseStatus=m['note']
    records.append(dict(obj=obj,**m));return obj
for old in src.Objects:
    if old.Name.startswith(('A05_Stud_','A08_Ledge_bolt_')):continue
    add(old.Name,old.Shape.copy(),existing=meta[old.Name])
for rear in (False,True):
    for i,(x,z) in enumerate([(x,z) for x in (80,470) for z in (150,460)]):
        add(f'A05_Stud_{i}',cyl(x,-72,z,2,80),rear,'M4x80 proposed stud envelope; replaces R02 70 mm shaft')
        for label,y in [('Service',-65),('Outer_fixed',-14),('Inner_fixed',-3)]:
            add(f'H10_{label}_washer_{i}',washer(x,y,z),rear)
        for label,y in [('Service',-70),('Outer_fixed',-19),('Inner_fixed',-2)]:
            add(f'H11_{label}_nut_{i}',nut(x,y,z),rear)
    for x in (130,390):
        # Under-head length25; cap head is7 diameter x4 high, socket not represented.
        add(f'A08_Ledge_bolt_{x}',cyl(x+15,-16,148,2,25).fuse(cyl(x+15,-20,148,3.5,4)),rear,'M4x25 nominal cap screw, 7 dia x4 head; socket/threads omitted')
        for label,y in [('Outer',-16),('Inner',-3)]:add(f'H12_{label}_washer_{x}',washer(x+15,y,148),rear)
        add(f'H13_Ledge_nut_{x}',nut(x+15,-2,148),rear)
doc.recompute();clashes=[];count=0
for i,a in enumerate(records):
    for b in records[i+1:]:
        if not ({a['name'],b['name']}&changed) or 'reservation' in (a['kind'],b['kind']):continue
        count+=1
        vol=a['obj'].Shape.common(b['obj'].Shape).Volume
        if vol>.05:clashes.append([a['name'],b['name'],vol])
services=[]
for rear in (False,True):
    suffix='_Rear' if rear else '_Front'
    sweep=Part.makeBox(370,240,290,V(90,-255,160))
    if rear:sweep=sweep.mirror(V(0,180,0),V(0,1,0))
    hits=[]
    for r in records:
        if r['kind']=='reservation':continue
        if r['name'].endswith(suffix) and r['name'].startswith(('A03_','A04_','H10_Service','H11_Service')):continue
        vol=sweep.common(r['obj'].Shape).Volume
        if vol>.05:hits.append([r['name'],vol])
    services.append(dict(side=suffix[1:],travel_mm=200,clashes_mm3=hits))
audit=dict(source_sha256=digest,source_unchanged=hashlib.sha256(base.read_bytes()).hexdigest()==digest,
    objects=len(records),changed_or_added_objects=len(changed),pair_checks=count,clashes_mm3=clashes,
    valid=all(r['obj'].Shape.isValid() for r in records),filter_service=services,
    nominal_thread_projection_mm=dict(service=2,inner_stud=5,ledge=6),
    minimum_assumed_two_pitch_mm=1.4,
    exclusions='Unchanged R02 pairs, reservations, actual threads/socket, tool approach, hand access, tolerances, strength, seal compression, inherited M5 hardware and electrical safety. No release.')
assert audit['source_unchanged'] and audit['valid'] and not clashes and not any(s['clashes_mm3'] for s in services),audit
doc.saveAs(str(O/'D01_R02H_ASSEMBLY.FCStd'));Part.export([r['obj'] for r in records],str(O/'D01_R02H_ASSEMBLY.step'))
mesh=[]
for r in records:
    vs,ts=r['obj'].Shape.tessellate(1.5)
    mesh.append({k:r[k] for k in ('name','kind','color','explode','note')}|dict(vertices=[[v.x,v.y,v.z] for v in vs],triangles=[list(t) for t in ts]))
(O/'cad_mesh.json').write_text(json.dumps(mesh))
reopened=A.openDocument(str(O/'D01_R02H_ASSEMBLY.FCStd'));step=Part.read(str(O/'D01_R02H_ASSEMBLY.step'))
audit.update(native_reopen_objects=len(reopened.Objects),STEP_valid=step.isValid(),STEP_volume_matches=math.isclose(step.Volume,sum(r['obj'].Shape.Volume for r in records),rel_tol=1e-7))
assert audit['STEP_valid'] and audit['STEP_volume_matches'] and audit['native_reopen_objects']==len(records)
(O/'checks.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
