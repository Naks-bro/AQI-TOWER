"""R02G: separate inner/outer guard mountings on the saved R02H assembly."""
import json,hashlib,math
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2];B=R/'reports/prototype_d01/r02_adapter/hardware_detail'
O=R/'reports/prototype_d01/r02_guards';O.mkdir(exist_ok=True)
base=B/'D01_R02H_ASSEMBLY.FCStd';digest=hashlib.sha256(base.read_bytes()).hexdigest()
src=A.openDocument(str(base));doc=A.newDocument('D01_R02G');V=A.Vector
meta={m['name']:m for m in json.loads((B/'cad_mesh.json').read_text())};records=[];changed=set();removed=[]
def cyl(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z))
def washer(x,y,z):return cyl(x,y,z,6,1).cut(cyl(x,y,z-1,2.15,3))
def nut(x,y,z):
    rr=7/math.sqrt(3);pts=[V(x+rr*math.cos(i*math.pi/3),y+rr*math.sin(i*math.pi/3),z) for i in range(6)]
    return Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(V(0,0,5)).cut(cyl(x,y,z-1,2,7))
def add(name,shape,m=None):
    if m is None:m=dict(name=name,kind='hardware',color='#9aadb9',explode=[0,0,0],note='Proposed M4 hardware envelope, not approved grade/torque; threads/socket omitted');changed.add(name)
    o=doc.addObject('PartDesign::Feature',name);o.Shape=shape
    o.addProperty('App::PropertyString','ReleaseStatus');o.ReleaseStatus=m['note']
    records.append(dict(obj=o,**{k:m[k] for k in ('name','kind','color','explode','note')}))
for old in src.Objects:
    name=old.Name
    if name.startswith(('H03_Guard','H04_Guard','H05_Guard')):removed.append(name);continue
    sh=old.Shape.copy();m=meta[name].copy()
    if name=='M06_Fan_plate':
        # Retain inner holes y60/300; add separate outer holes y120/240.
        for x in (105,445):
            for y in (120,240):sh=sh.cut(cyl(x,y,570,2.25,11))
        changed.add(name);m['note']='R02G guard holes x105/445, y60/120/240/300. Separate inner/outer fixings. Other R01 holes retained.'
    if name.startswith('G03_Outer_'):
        yy=int(name.rsplit('_',1)[1]);sh.translate(V(0,60 if yy==40 else -60,0))
        changed.add(name);m['note']='Outer bracket relocated to y100..140 or220..260. Part name retains historical identifier; use R02G coordinates.'
    if name in ('G02_Outer_skirt_0','G02_Outer_skirt_1'):
        xx=115 if name.endswith('_0') else 434
        # New manufacturing revision: old rivet holes omitted, not a field patch instruction.
        for yy in (50,70,290,310):sh=sh.fuse(Part.makeCylinder(1.75,1,V(xx,yy,590),V(1,0,0)))
        for yy in (110,130,230,250):sh=sh.cut(Part.makeCylinder(1.75,4,V(xx-1,yy,590),V(1,0,0)))
        sh=sh.removeSplitter();changed.add(name);m['note']='R02G new skirt blank: rivet holes y110/130/230/250 at z590. Old y50/70/290/310 drilling NOT used.'
    add(name,sh,m)
mounts=[]
for tag,ys,headbase,lowerwasher in [('Outer',(120,240),583,570),('Inner',(60,300),581,568)]:
    for x in (105,445):
        for y in ys:
            stem=f'J01_{tag}_{x}_{y}'
            add(stem+'_Screw',cyl(x,y,headbase-20,2,20).fuse(cyl(x,y,headbase,3.5,4)))
            add(stem+'_Upper_washer',washer(x,y,headbase-1))
            add(stem+'_Lower_washer',washer(x,y,lowerwasher))
            add(stem+'_Nut',nut(x,y,lowerwasher-5))
            mounts.append(dict(tag=tag,x=x,y=y,headbase=headbase,lowerwasher=lowerwasher,prefix=stem))
doc.recompute();clashes=[];pairs=0
for i,a in enumerate(records):
    for b in records[i+1:]:
        if not ({a['name'],b['name']}&changed) or 'reservation' in (a['kind'],b['kind']):continue
        if a['kind']==b['kind']=='guard':continue
        pairs+=1;vol=a['obj'].Shape.common(b['obj'].Shape).Volume
        if vol>.05:clashes.append([a['name'],b['name'],vol])
# ASSUMED tool envelopes, not actual purchased tools. Test installed geometry.
toolchecks=[]
for m in mounts:
    x,y,h,l=m['x'],m['y'],m['headbase'],m['lowerwasher']
    for label,shape in [('driver',cyl(x,y,h+4,2,100)),('nut_socket',cyl(x,y,l-25,6,25).cut(cyl(x,y,l-6,4.3,7)))]:
        hits=[]
        for r in records:
            if r['kind']=='reservation' or r['name'].startswith(m['prefix']):continue
            vol=shape.common(r['obj'].Shape).Volume
            if vol>.05:hits.append([r['name'],vol])
        toolchecks.append(dict(mount=m['prefix'],tool=label,clashes_mm3=hits))
audit=dict(source_sha256=digest,source_unchanged=hashlib.sha256(base.read_bytes()).hexdigest()==digest,
    objects=len(records),changed_objects=len(changed),removed_shared_hardware=removed,pair_checks=pairs,clashes_mm3=clashes,
    tool_checks=toolchecks,valid=all(r['obj'].Shape.isValid() for r in records),
    thread_projection_mm=2,independent_mounts=dict(inner=4,outer=4),
    exclusions='Unchanged pairs; reservations; inherited guard seams. Tool envelopes exclude hands, handles, insertion manoeuvres and tolerances. Rivets, corner seams, strength, reach protection, captive retention, cable entry and isolation/restart unresolved. No safety release.')
(O/'checks.json').write_text(json.dumps(audit,indent=2))
assert audit['valid'] and audit['source_unchanged'] and not clashes and not any(t['clashes_mm3'] for t in toolchecks),audit
doc.saveAs(str(O/'D01_R02G_ASSEMBLY.FCStd'));Part.export([r['obj'] for r in records],str(O/'D01_R02G_ASSEMBLY.step'))
mesh=[]
for r in records:
    vs,ts=r['obj'].Shape.tessellate(1.5)
    mesh.append({k:r[k] for k in ('name','kind','color','explode','note')}|dict(vertices=[[v.x,v.y,v.z] for v in vs],triangles=[list(t) for t in ts]))
(O/'cad_mesh.json').write_text(json.dumps(mesh));(O/'mounts.json').write_text(json.dumps(mounts,indent=2))
step=Part.read(str(O/'D01_R02G_ASSEMBLY.step'));reopened=A.openDocument(str(O/'D01_R02G_ASSEMBLY.FCStd'))
audit.update(STEP_valid=step.isValid(),STEP_volume_matches=math.isclose(step.Volume,sum(r['obj'].Shape.Volume for r in records),rel_tol=1e-7),native_reopen_objects=len(reopened.Objects))
assert audit['STEP_valid'] and audit['STEP_volume_matches'] and audit['native_reopen_objects']==len(records)
(O/'checks.json').write_text(json.dumps(audit,indent=2));print(json.dumps({k:v for k,v in audit.items() if k not in ('removed_shared_hardware','tool_checks')},indent=2))
