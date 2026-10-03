"""One R03M mechanical detail pass on saved R02G. PROPOSED, not strength release."""
import json,hashlib,math,csv
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2];B=R/'reports/prototype_d01/r02_guards';O=R/'reports/prototype_d01/mechanical_package';O.mkdir(exist_ok=True)
base=B/'D01_R02G_ASSEMBLY.FCStd';sha=hashlib.sha256(base.read_bytes()).hexdigest()
src=A.openDocument(str(base));doc=A.newDocument('D01_R03M');V=A.Vector
meta={m['name']:m for m in json.loads((B/'cad_mesh.json').read_text())};records=[];schedule=[]
def cyl(r,h,z=0):return Part.makeCylinder(r,h,V(0,0,z))
def wash(d=4):
    od,t,bore=(12,1,4.3) if d==4 else (15,1.2,5.3)
    return cyl(od/2,t).cut(cyl(bore/2,t+2,-1))
def nut(d=4):
    rr=(7 if d==4 else 8)/math.sqrt(3)
    pts=[V(rr*math.cos(i*math.pi/3),rr*math.sin(i*math.pi/3),0) for i in range(6)]
    return Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(V(0,0,5)).cut(cyl(d/2,7,-1))
def orient(shape,p,axis=(0,0,1)):
    sh=shape.copy();sh.Placement=A.Placement(V(*p),A.Rotation(V(0,0,1),V(*axis)));return sh
def add(name,sh,kind='hardware',note='Proposed fastener envelope; grade, torque and locking engagement unreleased',color='#9aaebb',explode=None):
    o=doc.addObject('PartDesign::Feature',name);o.Shape=sh
    o.addProperty('App::PropertyString','ReleaseStatus');o.ReleaseStatus=note
    records.append(dict(obj=o,name=name,kind=kind,note=note,color=color,explode=explode or [0,0,0]));return o
skip=('H01_Stud','H02_Fan_bolt','H06_End','H07_Seat','G01_','G02_','G03_')
for old in src.Objects:
    if old.Name.startswith(skip):continue
    m=meta[old.Name];add(old.Name,old.Shape.copy(),**{k:m[k] for k in ('kind','note','color','explode')})
# Two fabricated guard subassemblies: preserve envelope, make joining route explicit.
for tag in ('Outer','Inner'):
    parts=[]
    for old in src.Objects:
        if old.Name.startswith((f'G01_{tag}',f'G02_{tag}',f'G03_{tag}')):
            sh=old.Shape.copy()
            # Welding alternative uses undrilled lap interfaces; no blind rivets.
            if old.Name.startswith(f'G02_{tag}_skirt_') and old.Name[-1] in '01':
                x=115 if old.Name[-1]=='0' else 434;zz=590 if tag=='Outer' else 560
                ys=(110,130,230,250) if tag=='Outer' else (50,70,290,310)
                for y in ys:sh=sh.fuse(Part.makeCylinder(1.75,1,V(x,y,zz),V(1,0,0)))
            if old.Name.startswith(f'G03_{tag}_'):
                bb=sh.BoundBox;x=113 if '_L_' in old.Name else 435;zz=590 if tag=='Outer' else 560
                for y in (bb.YMin+10,bb.YMin+30):sh=sh.fuse(Part.makeCylinder(1.75,2,V(x,y,zz),V(1,0,0)))
            parts.append(sh)
    merged=parts[0].multiFuse(parts[1:]).removeSplitter()
    assert len(merged.Solids)==1,(tag,len(merged.Solids))
    add('G10_'+tag+'_fabricated_guard',merged,'guard','PROPOSED welded steel sheet/angle assembly. Face perimeter, four vertical corners and four bracket laps joined. Weld process/size/distortion/strength not released; no rivet holes. Perforations not modeled.',explode=[0,0,140 if tag=='Outer' else -100])
# Shorter M5 rods: outer reducer clamps stay in position, unnecessary projections removed.
studs=[(20,z) for z in (55,305,555)]+[(530,z) for z in (55,305,555)]+[(275,50),(275,560)]
for rear in (False,True):
    for i,(x,z) in enumerate(studs):
        end=19 if x==275 else 39;seat=9 if x==275 else 29;prefix=f'K01_{"Rear" if rear else "Front"}_{i}'
        def at(shape,y):
            sh=orient(shape,(x,y,z),(0,1,0))
            return sh.mirror(V(0,180,0),V(0,1,0)) if rear else sh
        add(prefix+'_stud',at(cyl(2.5,end+21),-21),note=f'Proposed M5x{end+21} rod; replaces old projecting stud. End treatment/retention pending.')
        for label,y in [('outer',-13.2),('inner',seat)]:add(prefix+'_'+label+'_washer',at(wash(5),y))
        for label,y in [('outer',-18.2),('inner',seat+1.2)]:add(prefix+'_'+label+'_nut',at(nut(5),y))
schedule.append(dict(item='M5 reducer studs',qty=16,spec='12 x60 mm;4 x40 mm;32 nuts8AFx5;32 washers15ODx1.2 (bore5.3 assumed)',status='PROPOSED; external thread projection2.8mm; inner3.8mm'))
# Hard spacers stop plates closing below the current nominal gasket gaps.
for rear in (False,True):
    for i,(x,z) in enumerate(studs):
        sh=orient(cyl(5,3).cut(cyl(2.75,5,-1)),(x,-3,z),(0,1,0))
        if rear:sh=sh.mirror(V(0,180,0),V(0,1,0))
        add(f'K03_Outer_stop_{rear}_{i}',sh,note='Proposed OD10/ID5.5 x3 spacer fixes outer installed seal gap. Gasket free thickness/force unverified; NOT a compression specification.')
    for i,(x,z) in enumerate([(x,z) for x in (80,470) for z in (150,460)]):
        sh=orient(cyl(3.25,36).cut(cyl(2.25,38,-1)),(x,-55,z),(0,1,0))
        if rear:sh=sh.mirror(V(0,180,0),V(0,1,0))
        add(f'K04_Inner_stop_{rear}_{i}',sh,note='Proposed OD6.5/ID4.5 x36 sleeve between fixed nut and retainer. Assumed40mm filter +3mm installed seal; adjust only after actual filter/gasket verification.')
schedule.append(dict(item='Seal compression limiters',qty=24,spec='16 outer OD10/ID5.5 x3;8 inner OD6.5/ID4.5 x36',status='ASSUMED nominal gaps; force/tolerance/actual filter thickness unknown'))
# Fan stack:50 mm under-head screw with actual nut/washer envelopes.
for old in src.Objects:
    if not old.Name.startswith('H02_Fan_bolt'):continue
    b=old.Shape.BoundBox;x=(b.XMin+b.XMax)/2;y=(b.YMin+b.YMax)/2;n=old.Name.replace('H02','K02')
    add(n+'_screw',orient(cyl(2,50).fuse(cyl(3.5,4,50)),(x,y,559)))
    add(n+'_top_washer',orient(wash(),(x,y,608)))
    add(n+'_bottom_washer',orient(wash(),(x,y,570)))
    add(n+'_nut',orient(nut(),(x,y,565)))
schedule.append(dict(item='Fan fastenings',qty=16,spec='M4x50 cap screw;32 washers12ODx1;16 nuts7AFx5',status='PROPOSED;6mm nominal thread projection; fan corner bearing strength unknown'))
# Existing through cabinet joints, now with washers and locknuts.
for old in src.Objects:
    if not old.Name.startswith(('H06_End','H07_Seat')):continue
    b=old.Shape.BoundBox;n=old.Name.replace('H06','K06').replace('H07','K07')
    if old.Name.startswith('H06'):
        right='_True_' in old.Name;p=(551 if right else -1,(b.YMin+b.YMax)/2,(b.ZMin+b.ZMax)/2);axis=(-1,0,0) if right else (1,0,0)
    else:
        rear='_True_' in old.Name;p=((b.XMin+b.XMax)/2,361 if rear else -1,(b.ZMin+b.ZMax)/2);axis=(0,-1,0) if rear else (0,1,0)
    # Under-head face at external washer;29mm wood stack +two1mm washers.
    add(n+'_screw',orient(cyl(2,40).fuse(cyl(3.5,4,-4)),p,axis))
    add(n+'_outer_washer',orient(wash(),p,axis))
    pp=tuple(p[i]+30*axis[i] for i in range(3));add(n+'_inner_washer',orient(wash(),pp,axis))
    pp=tuple(p[i]+31*axis[i] for i in range(3));add(n+'_nut',orient(nut(),pp,axis))
schedule.append(dict(item='Cabinet through joints',qty=32,spec='M4x40 cap screws;64 washers12ODx1;32 nuts7AFx5',status='PROPOSED;4mm nominal thread projection; wood bearing/edge and clamp load not approved'))
# Model heads/washers for existing wood screw cores; retain core-only thread simplification.
for old in src.Objects:
    if not old.Name.startswith('H10_') or old.Name.startswith(('H10_Service','H10_Outer','H10_Inner')):continue
    if not (old.Name.startswith('H10_True_') or old.Name.startswith('H10_False_')):continue
    b=old.Shape.BoundBox;x=(b.XMin+b.XMax)/2;y=(b.YMin+b.YMax)/2;top='True' in old.Name
    z=580 if top else 19
    add('K10_washer_'+old.Name,orient(wash(),(x,y,z)))
    add('K10_head_'+old.Name,orient(cyl(3.5,4),(x,y,581 if top else 15)),note='Head envelope for retained core-only wood screw. Full screw/thread geometry and end-grain withdrawal capacity remain unverified.')
# Existing cores end at head bearing interface after washer added: extend core across washer only.
    doc.getObject(old.Name).Shape=orient(cyl(1.2,20 if top else 25),(x,y,561 if top else 19))
    if top:
        for r in records:
            if r['name'].startswith('M07_'):r['obj'].Shape=r['obj'].Shape.cut(orient(cyl(1.25,10),(x,y,561)))
    next(r for r in records if r['name']==old.Name)['note']=f'Proposed4x{20 if top else 25} wood screw, core-only envelope. Pilot/core are not actual threads. Head/washer separate; end-grain withdrawal and torque unverified.'
schedule.append(dict(item='Top/base wood screws',qty=8,spec='4 top4x20;4 base4x25;8 washers;head7dia x4 envelope',status='Core only; thread/pilot, wood grade and end-grain withdrawal must be verified; never lift by lid'))
# Positive foot retention: generic drilled foot, recessed underside screw head.
for old in src.Objects:
    if not old.Name.startswith('M08_Foot'):continue
    b=old.Shape.BoundBox;x=(b.XMin+b.XMax)/2;y=(b.YMin+b.YMax)/2
    obj=doc.getObject(old.Name);obj.Shape=obj.Shape.cut(orient(cyl(2.25,22,-1),(x,y,0))).cut(orient(cyl(6,9),(x,y,0)))
    doc.getObject('M01_Base').Shape=doc.getObject('M01_Base').Shape.cut(orient(cyl(2.25,11),(x,y,19)))
    add('K08_'+old.Name+'_screw',orient(cyl(2,30,8).fuse(cyl(3.5,4,4)),(x,y,0)))
    add('K08_'+old.Name+'_lower_washer',orient(wash(),(x,y,8)))
    add('K08_'+old.Name+'_upper_washer',orient(wash(),(x,y,29)))
    add('K08_'+old.Name+'_nut',orient(nut(),(x,y,30)))
    next(r for r in records if r['name']==old.Name)['note']='Proposed30x30x20 foot,4.5 through bore and12dia x9 underside recess. Exact foot material/load/compression/tear capacity unselected.'
schedule.append(dict(item='Foot retention',qty=4,spec='M4x30 cap screw;8 washers12ODx1;4 nuts7AFx5;4 feet with12dia x9 recess',status='PROPOSED; head4mm above floor;3mm nominal thread projection; foot material strength unknown'))
doc.recompute();clashes=[];pairs=0;excluded=0
for i,a in enumerate(records):
    for b in records[i+1:]:
        if 'reservation' in (a['kind'],b['kind']):excluded+=1;continue
        pairs+=1
        if not a['obj'].Shape.BoundBox.intersect(b['obj'].Shape.BoundBox):continue
        v=a['obj'].Shape.common(b['obj'].Shape).Volume
        if v>.05:clashes.append([a['name'],b['name'],v])
checks=dict(source_sha256=sha,source_unchanged=hashlib.sha256(base.read_bytes()).hexdigest()==sha,objects=len(records),checked_pairs=pairs,excluded_reservation_pairs=excluded,clashes_mm3=clashes,valid=all(r['obj'].Shape.isValid() for r in records),guard_subassemblies_single_solid=True,
    exclusions='Reservation pairs only. Welds/threads/perforations and tolerances not geometrically modeled. No strength, weld quality, finger-access, sealing or electrical release.')
(O/'checks.json').write_text(json.dumps(checks,indent=2));assert checks['valid'] and checks['source_unchanged'] and not clashes,checks
doc.saveAs(str(O/'D01_R03M_ASSEMBLY.FCStd'));Part.export([r['obj'] for r in records],str(O/'D01_R03M_ASSEMBLY.step'))
ed=A.newDocument('D01_R03M_EXPLODED')
for r in records:
    n=r['name'];rear='Rear' in n
    if n.startswith('G10_'):r['explode']=[0,0,240 if 'Outer' in n else -140]
    elif n.startswith(('F02_','K02_')):r['explode']=[0,0,110]
    elif n.startswith('S02_'):r['explode']=[0,0,75]
    elif n=='M06_Fan_plate':r['explode']=[0,0,40]
    elif n.startswith(('M08_','K08_')):r['explode']=[0,0,-110]
    elif n.startswith('K01_'):r['explode']=[0,130 if rear else -130,0]
    elif n.startswith('K03_'):r['explode']=[0,100 if '_True_' in n else -100,0]
    elif n.startswith('K04_'):r['explode']=[0,260 if '_True_' in n else -260,0]
    elif n.startswith('K06_'):r['explode']=[120 if '_True_' in n else -120,0,0]
    elif n.startswith('K07_'):r['explode']=[0,70 if '_True_' in n else -70,0]
    elif n.startswith(('A01_','A05_','A06_','H10_Outer_fixed','H10_Inner_fixed','H11_Outer_fixed','H11_Inner_fixed')):r['explode']=[0,130 if rear else -130,0]
    elif n.startswith('A02_'):r['explode']=[0,160 if rear else -160,0]
    elif n.startswith('A03_'):r['explode']=[0,210 if rear else -210,0]
    elif n.startswith(('A04_','H10_Service','H11_Service')):r['explode']=[0,260 if rear else -260,0]
    o=ed.addObject('PartDesign::Feature',r['name']);sh=r['obj'].Shape.copy();sh.translate(V(*r['explode']));o.Shape=sh
ed.recompute();ed.saveAs(str(O/'D01_R03M_EXPLODED.FCStd'))
mesh=[];inventory=[]
for r in records:
    sh=r['obj'].Shape;vs,ts=sh.tessellate(1.5);b=sh.BoundBox
    mesh.append({k:r[k] for k in ('name','kind','color','explode','note')}|dict(vertices=[[v.x,v.y,v.z] for v in vs],triangles=[list(t) for t in ts]))
    centres=[sum(getattr(s.CenterOfMass,k)*s.Volume for s in sh.Solids)/sh.Volume for k in 'xyz']
    inventory.append(dict(id=r['name'],kind=r['kind'],x_mm=b.XLength,y_mm=b.YLength,z_mm=b.ZLength,volume_mm3=sh.Volume,centre_mm=centres,note=r['note']))
(O/'cad_mesh.json').write_text(json.dumps(mesh));(O/'part_inventory.json').write_text(json.dumps(inventory,indent=2));(O/'fasteners.json').write_text(json.dumps(schedule,indent=2))
step=Part.read(str(O/'D01_R03M_ASSEMBLY.step'));re=A.openDocument(str(O/'D01_R03M_ASSEMBLY.FCStd'))
checks.update(STEP_valid=step.isValid(),STEP_volume_matches=math.isclose(step.Volume,sum(r['obj'].Shape.Volume for r in records),rel_tol=1e-7),native_reopen_objects=len(re.Objects))
assert checks['STEP_valid'] and checks['STEP_volume_matches'] and len(re.Objects)==len(records)
(O/'checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
