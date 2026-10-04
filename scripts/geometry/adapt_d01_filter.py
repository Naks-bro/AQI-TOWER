"""R02 experimental STARKVIND cassette on the saved R01 cabinet; preserve source.
OEM envelope only. Gasket landing, tolerances, forces and pressure loss unverified.
"""
import json, hashlib, math
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2];B=R/'reports/prototype_d01/r01'
O=R/'reports/prototype_d01/r02_adapter';O.mkdir(exist_ok=True)
base=B/'D01_R01_ASSEMBLY.FCStd';digest=hashlib.sha256(base.read_bytes()).hexdigest()
src=A.openDocument(str(base));doc=A.newDocument('D01_R02_Adapter')
meta={m['name']:m for m in json.loads((B/'cad_mesh.json').read_text())};records=[]
removed=[]
prefixes=('F01_MERV13_','M04_Retainer_','M05_Filter_shelf_','M09_Shelf_angle_','H08_Shelf_seat_bolt_','H09_Shelf_flush_screw_')
for old in src.Objects:
    if not hasattr(old,'Shape'):continue
    if old.Name.startswith(prefixes):removed.append(old.Name);continue
    o=doc.addObject('PartDesign::Feature',old.Name);o.Shape=old.Shape.copy()
    m=meta[old.Name];records.append(dict(obj=o,**{k:m[k] for k in ('name','kind','color','explode','note')}))
V=A.Vector
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def cyl(x,y,z,r,t):return Part.makeCylinder(r,t,V(x,y,z),V(0,1,0))
def ring(x,y,z,w,h,t,iw,ih):return box(x,y,z,w,t,h).cut(box(x+(w-iw)/2,y-1,z+(h-ih)/2,iw,t+2,ih))
def mirror(sh,rear):
    if not rear:return sh
    # Reflect y about cabinet midplane, retaining x/z.
    return sh.mirror(V(0,180,0),V(0,1,0))
def add(name,shape,kind,color,rear=False,offset=0,note='EXPERIMENTAL - NOT RELEASED'):
    name += '_Rear' if rear else '_Front'
    o=doc.addObject('PartDesign::Feature',name);o.Shape=mirror(shape,rear)
    o.addProperty('App::PropertyString','ReleaseStatus');o.ReleaseStatus=note
    records.append(dict(obj=o,name=name,kind=kind,color=color,explode=[0,offset if rear else -offset,0],note=note))
    return o
studs=[(20,z) for z in (55,305,555)]+[(530,z) for z in (55,305,555)]+[(275,50),(275,560)]
newstuds=[(x,z) for x in (80,470) for z in (150,460)]
reliefs=[(x,z) for x in (20,530) for z in (155,255,355,455)]
panels=[]
for rear in (False,True):
    s=ring(0,-12,30,550,550,9,350,270)
    # This centres opening at z305, same as original filter centre.
    for x,z in studs:s=s.cut(cyl(x,-13,z,2.75,11))
    for x,z in newstuds+[(145,148),(405,148)]:s=s.cut(cyl(x,-13,z,2.25,11))
    # Clearance for inherited R01 seat bolt head envelopes, outside perimeter seal.
    for x,z in reliefs:s=s.cut(cyl(x,-13,z,4,11))
    add('A01_Reducer',s,'panel','#008b7f',rear,25,
        '550x550x9; opening350x270. Existing eight M5 studs retain adapter; new M4 feedthroughs require sealed washers. Seal/contact forces and panel stiffness unknown.')
    add('A02_Filter_gasket',ring(90,-15,160,370,290,3,350,270),'seal','#405563',rear,45,
        'ASSUMED10mm flat border,3mm installed gasket. OEM border flatness and compression NOT verified.')
    add('A03_STARKVIND_envelope',box(90,-55,160,370,40,290),'filter','#eee5d4',rear,90,
        'IKEA104.633.30 published370x290x40 envelope. OEM specifies STARKVIND-only; custom use experimental. No MERV/HEPA/airflow claim.')
    ret=ring(70,-64,140,410,330,9,350,270)
    for x,z in newstuds:ret=ret.cut(cyl(x,-65,z,2.25,11))
    add('A04_Retainer',ret,'panel','#4d8999',rear,130,'410x330x9, opening350x270; four M4 studs. Unknown frame strength/contact/torque; head/nut details omitted.')
    for i,(x,z) in enumerate(newstuds):
        add(f'A05_Stud_{i}',cyl(x,-70,z,2,70),'hardware','#9aaebb',rear,0,'M4x70 shaft envelope only; retention nuts/washers unselected.')
        washer=cyl(x,-13,z,5,1).cut(cyl(x,-14,z,2,3))
        add(f'A06_Feedthrough_seal_{i}',washer,'seal','#405563',rear,25,'Assumed installed sealing washer envelope; exact product and compression unverified.')
    for x in (130,390):
        ledge=box(x,-55,158,30,43,2).fuse(box(x,-14,138,30,2,20))
        ledge=ledge.cut(cyl(x+15,-16,148,2.25,5))
        add(f'A07_Ledge_{x}',ledge,'support','#9aaebb',rear,30,'Proposed bent2mm bracket,43mm shelf and20mm downstand,30mm width. Root radius/material/strength not resolved.')
        add(f'A08_Ledge_bolt_{x}',cyl(x+15,-14,148,2,20),'hardware','#9aaebb',rear,0,'M4x20 shaft only; head/nut/lock feature unselected.')
        washer=cyl(x+15,-15,148,5,1).cut(cyl(x+15,-16,148,2,3))
        add(f'A09_Ledge_seal_{x}',washer,'seal','#405563',rear,30,'Seal feedthrough below filter, product unselected; no adhesive-only retention.')
panels=[dict(name='A01_REDUCER',w=550,h=550,t=9,opening=[100,140,350,270],
     holes=[[x,z-30,2.75] for x,z in studs]+[[x,z-30,2.25] for x,z in newstuds+[(145,148),(405,148)]]+[[x,z-30,4] for x,z in reliefs],qty=2),
    dict(name='A04_RETAINER',w=410,h=330,t=9,opening=[30,30,350,270],holes=[[x-70,z-140,2.25] for x,z in newstuds],qty=2)]
doc.recompute();clashes=[];count=0
added=[r for r in records if r['name'].startswith('A0')]
# New-to-existing and new-to-new audit; inherited R01 pairs are unchanged.
for i,a in enumerate(records):
    for b in records[i+1:]:
        if not (a in added or b in added) or 'reservation' in (a['kind'],b['kind']):continue
        count+=1;vol=a['obj'].Shape.common(b['obj'].Shape).Volume
        if vol>.05:clashes.append([a['name'],b['name'],vol])
audit=dict(source_sha256=digest,source_unchanged=hashlib.sha256(base.read_bytes()).hexdigest()==digest,
    removed_objects=removed,objects=len(records),new_objects=len(added),new_pair_checks=count,clashes_mm3=clashes,
    valid=all(r['obj'].Shape.isValid() for r in records),
    exclusions='Inherited R01 pairs; reservation envelopes; nuts/heads/threads, bend radii, real filter frame, physical seals and manufacturing tolerances. No strength/safety release.')
(O/'checks.json').write_text(json.dumps(audit,indent=2))
assert audit['valid'] and audit['source_unchanged'] and not clashes,audit
doc.saveAs(str(O/'D01_R02_ASSEMBLY.FCStd'));Part.export([r['obj'] for r in records],str(O/'D01_R02_ASSEMBLY.step'))
mesh=[]
for r in records:
    vs,ts=r['obj'].Shape.tessellate(1.5)
    mesh.append({k:r[k] for k in ('name','kind','color','explode','note')}|{'vertices':[[v.x,v.y,v.z] for v in vs],'triangles':[list(t) for t in ts]})
(O/'cad_mesh.json').write_text(json.dumps(mesh));(O/'panels.json').write_text(json.dumps(panels,indent=2))
reopened=A.openDocument(str(O/'D01_R02_ASSEMBLY.FCStd'))
step=Part.read(str(O/'D01_R02_ASSEMBLY.step'))
audit['native_reopen_objects']=len(reopened.Objects);audit['STEP_valid']=step.isValid()
audit['STEP_volume_matches']=math.isclose(step.Volume,sum(r['obj'].Shape.Volume for r in records),rel_tol=1e-7)
assert audit['STEP_valid'] and audit['STEP_volume_matches'] and audit['native_reopen_objects']==len(records)
(O/'checks.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
