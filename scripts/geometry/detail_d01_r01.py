"""Detail the existing D01 assembly, preserving R00. Nominal geometry, not a safety release."""
import json,hashlib,math
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2];B=R/'reports/prototype_d01';O=B/'r01';O.mkdir(exist_ok=True)
V=A.Vector
base=B/'D01_ASSEMBLY.FCStd';basehash=hashlib.sha256(base.read_bytes()).hexdigest()
src=A.openDocument(str(base));doc=A.newDocument('D01_R01')
meta={m['name']:m for m in json.loads((B/'cad_mesh.json').read_text())};records=[]
for old in src.Objects:
    if not hasattr(old,'Shape'):continue
    ob=doc.addObject('PartDesign::Feature',old.Name);ob.Shape=old.Shape.copy();ob.Label=old.Label
    ob.addProperty('App::PropertyString','ReleaseStatus');ob.ReleaseStatus=old.ReleaseStatus
    m=meta[old.Name];records.append(dict(obj=ob,name=old.Name,kind=m['kind'],color=m['color'],explode=m['explode'],note=m['note']))
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def cyl(r,length,p,axis):return Part.makeCylinder(r,length,V(*p),V(*axis))
def add(name,shape,kind='detail',color='#8ea6b4',note='Proposed detail; no strength or safety approval'):
    ob=doc.addObject('PartDesign::Feature',name);ob.Shape=shape;ob.Label=name.replace('_',' ')
    ob.addProperty('App::PropertyString','ReleaseStatus');ob.ReleaseStatus=note
    records.append(dict(obj=ob,name=name,kind=kind,color=color,explode=[0,0,0],note=note));return ob
def cut(name,r,length,p,axis):
    ob=doc.getObject(name);ob.Shape=ob.Shape.cut(cyl(r,length,p,axis))
schedule=[]
def sched(group,count,size,where,note):schedule.append(dict(group=group,quantity=count,size=size,locations=where,note=note))
# Eight 20x20x2 equal-angle segments,40mm long. Four bolts clamp guard feet to plate.
for side in ('L','R'):
    left=side=='L';ax=95 if left else 435;ux=113 if left else 435;bx=105 if left else 445
    skirt='0' if left else '1'
    for yy in (40,280):
        for inner in (False,True):
            tag='Inner' if inner else 'Outer';hz=569 if inner else 580;vz=551 if inner else 582
            sh=box(ax,yy,hz,20,40,2).fuse(box(ux,yy,vz,2,40,18))
            sh=sh.cut(cyl(2.25,5,(bx,yy+20,hz-1),(0,0,1)))
            rz=560 if inner else 590
            # Two dia3.5 rivet holes each attach the upright to solid guard skirt.
            for ry in (yy+10,yy+30):
                sh=sh.cut(cyl(1.75,6,(112 if left else 433,ry,rz),(1,0,0)))
                cut('G02_'+tag+'_skirt_'+skirt,1.75,6,(112 if left else 433,ry,rz),(1,0,0))
            add(f'G03_{tag}_{side}_{yy}',sh,note='20x20x2 angle segment40mm; nominal sharp inner corner, actual extrusion root radius must be checked. Two dia3.5 rivet holes; one dia4.5 base hole.')
        cut('M06_Fan_plate',2.25,12,(bx,yy+20,570),(0,0,1))
        sh=cyl(2,25,(bx,yy+20,558.6),(0,0,1)).fuse(cyl(3.5,4,(bx,yy+20,583.6),(0,0,1)))
        add(f'H03_Guard_bolt_{side}_{yy}',sh,'hardware',note='M4x25 shaft/head envelope; non-countersunk head. Locknut and flat washers shown separately; not an exact product CAD.')
        for zz in (567,582):add(f'H04_Guard_washer_{side}_{yy}_{zz}',cyl(4.5,1.6,(bx,yy+20,zz),(0,0,1)).cut(cyl(2.15,2,(bx,yy+20,zz-.2),(0,0,1))),'hardware')
        # Lower washer top568.6 leaves0.4mm nominal assembly take-up to angle569.
        add(f'H05_Guard_nut_{side}_{yy}',cyl(4,3.2,(bx,yy+20,563.8),(0,0,1)).cut(cyl(2,4,(bx,yy+20,563.4),(0,0,1))),'hardware',note='Nut cylindrical clearance envelope only; wrench space and actual locknut height to verify.')
sched('Guard through-bolts',4,'M4x25 +8 washers +4 locknuts','x105/445; y60/300','Upper and lower angles share bolts. Opening either guard requires isolation; no interlock implemented.')
sched('Guard angle rivets',16,'3.2mm nominal, grip must cover3mm','Each angle: ylocal10/30; outer z590, inner z560','Eight brackets x2; exact rivet/grip/head retention unselected. Drill dia3.5 proposal.')
# Through-bolt cabinet joints: drills and shaft/head envelopes, not strength selection.
for right in (False,True):
    name='M02_Right' if right else 'M02_Left';xstart=509 if right else -1
    for yy in (19,341):
        for zz in (105,205,405,505):
            cut(name,2.25,42,(xstart,yy,zz),(1,0,0))
            cut('M07_Cleat_'+('521' if right else '9')+'_'+('9' if yy==19 else '331'),2.25,42,(xstart,yy,zz),(1,0,0))
            shaft=cyl(2,40,(510 if right else 0,yy,zz),(1,0,0))
            head=cyl(3.5,4,(550 if right else -4,yy,zz),(1,0,0))
            add(f'H06_End_{right}_{yy}_{zz}',shaft.fuse(head),'hardware')
for rear in (False,True):
    for xx in (20,530):
        for zz in (155,255,355,455):
            ys=319 if rear else -1
            cut('M03_Seat_'+('Rear' if rear else 'Front'),2.25,42,(xx,ys,zz),(0,1,0))
            cut('M07_Cleat_'+('9' if xx==20 else '521')+'_'+('331' if rear else '9'),2.25,42,(xx,ys,zz),(0,1,0))
            shaft=cyl(2,40,(xx,320 if rear else 0,zz),(0,1,0));head=cyl(3.5,4,(xx,360 if rear else -4,zz),(0,1,0))
            add(f'H07_Seat_{rear}_{xx}_{zz}',shaft.fuse(head),'hardware')
sched('End-to-cleat through joints',16,'M4x40 +washers/locknuts','Each end: y19/341; z105/205/405/505','End local datum y0,z29: vertical coordinates76/176/376/476. Drill dia4.5 through panel and cleat.')
sched('Seat-to-cleat through joints',16,'M4x40 +washers/locknuts','Each seat: x20/530; z155/255/355/455','Seat local datum x9,z29: x11/521,z126/226/326/426. Avoid filter clamp holes.')
# Positive shelf support: eight angle segments. Upper screw head must sit flush below filter.
for rear in (False,True):
    tag='Rear' if rear else 'Front'
    for xx in (60,200,320,460):
        sy=360 if rear else -25;vy=360 if rear else -2
        sh=box(xx,sy,46.35,30,25,2).fuse(box(xx,vy,23.35,30,2,23))
        by=375 if rear else -15
        sh=sh.cut(cyl(1.75,4,(xx+15,by,45.35),(0,0,1)))
        sh=sh.cut(cyl(2.25,5,(xx+15,359 if rear else -3,37),(0,1,0)))
        add(f'M09_Shelf_angle_{tag}_{xx}',sh,note='30mm length of25x25x2 angle. Nominal sharp corner; actual root fillet and flush screw seat need fit check.')
        cut('M03_Seat_'+tag,2.25,13,(xx+15,350 if rear else -3,37),(0,1,0))
        cut('M05_Filter_shelf_'+tag,1.75,13,(xx+15,by,45.35),(0,0,1))
        add(f'H08_Shelf_seat_bolt_{tag}_{xx}',cyl(2,20,(xx+15,344 if rear else -2,37),(0,1,0)),'hardware',note='M4x20 shaft envelope; washers/locknut/head not shown, must remain outside media.')
        add(f'H09_Shelf_flush_screw_{tag}_{xx}',cyl(1.5,20,(xx+15,by,37.35),(0,0,1)),'hardware',note='M3x20 shaft; countersunk head/recess not modeled. Final head flush at or below z57.35; do not load filter onto protruding hardware.')
sched('Shelf support',8,'25x25x2 angle,30 long; M4x20 to seat; M3x20 flush to ledge','x75/215/335/475; seat z37; ledge y-15/375','Countersink per actual head, not before product selection. Eight ledge screws and eight seat bolts.')
# Base/top screws are local timber fixings, not invented threaded inserts.
for top in (False,True):
    for xx in (19,531):
        for yy in (19,341):
            zz=560 if top else 20;length=20 if top else 25;panel='M06_Fan_plate' if top else 'M01_Base'
            cut(panel,2.25,length+2,(xx,yy,zz-1),(0,0,1))
            cleat=f'M07_Cleat_{9 if xx==19 else 521}_{9 if yy==19 else 331}'
            # Actual pilot diameter depends on selected timber/screw;2.5mm envelope only.
            cut(cleat,1.25,length,(xx,yy,zz),(0,0,1))
            add(f'H10_{top}_{xx}_{yy}',cyl(1.2,length,(xx,yy,zz),(0,0,1)),'hardware',note='Pilot/wood-screw core envelope only; external thread/head not modeled. Timber end-grain holding capacity unknown; carry by base, not lid.')
sched('Top and base retention',8,'4 top wood screws4x20;4 base4x25','x19/531; y19/341','Pilot diameter per actual wood/screw. Proposed seam: external removable foil HVAC tape after dry fit; exact tape unknown. Not a lifting structure.')
# Cable guide is ONLY a reservation. Do not drill generic holes through a safety guard.
route=[(435,180,595),(565,180,595),(565,180,490)]
for k,(a,b) in enumerate(zip(route,route[1:])):
    vec=V(*b)-V(*a);add(f'E02_Cable_corridor_{k}',Part.makeCylinder(6,vec.Length,V(*a),vec.normalize()),'reservation','#daac5b','12mm corridor is NOT a drilled gland hole. Select closed-entry gland/connector and restraint; preserve guard access protection.')
sched('Cable route',4,'4-pin fan extensions, length to be selected','Fan perimeter -> right guard side -> external control reservation','External leg235mm; internal leads/connector service loops additional. OEM400mm leads may not reach. No gland cutout or connector pin orientation invented.')
doc.recompute()
assert all(r['obj'].Shape.isValid() for r in records)
doc.saveAs(str(O/'D01_R01_ASSEMBLY.FCStd'));Part.export([r['obj'] for r in records],str(O/'D01_R01_ASSEMBLY.step'))
mesh=[]
for r in records:
    vs,ts=r['obj'].Shape.tessellate(1.5);mesh.append({k:r[k] for k in ('name','kind','color','explode','note')}|{'vertices':[[v.x,v.y,v.z] for v in vs],'triangles':[list(t) for t in ts]})
(O/'cad_mesh.json').write_text(json.dumps(mesh))
(O/'fastener_schedule.json').write_text(json.dumps(schedule,indent=2))
# Revise the same panel set with the new holes. Each shelf has its own local datum.
panels=json.loads((B/'panel_geometry.json').read_text());outpanels=[]
for p in panels:
    p=dict(p);p['circles']=list(p['circles'])
    if p['name']=='M01_BASE':p['circles'] += [(x,y,2.25) for x in (19,531) for y in (19,341)]
    if p['name']=='M02_END':p['circles'] += [(y,z-29,2.25) for y in (19,341) for z in (105,205,405,505)]
    if p['name']=='M03_SEAT':p['circles'] += [(x-9,z-29,2.25) for x in (20,530) for z in (155,255,355,455)]+[(x-9,8,2.25) for x in (75,215,335,475)]
    if p['name']=='M06_FAN_PLATE':p['circles'] += [(x,y,2.25) for x in (105,445) for y in (60,300)]+[(x,y,2.25) for x in (19,531) for y in (19,341)]
    if p['name']=='M05_SHELF':
        for rear in (False,True):
            for right in (False,True):
                q=dict(p);q['name']='M05_'+('REAR' if rear else 'FRONT')+'_'+('RIGHT' if right else 'LEFT');q['qty']=1
                q['circles']=[(x,15 if rear else 32.45,1.75) for x in ((50,190) if right else (45,185))]
                q['note']='Dia3.5 through only; countersink not included. Match actual flush head; no protrusion above filter seat.';outpanels.append(q)
        continue
    p['note']='R01 REVIEW ONLY. '+p['note'];outpanels.append(p)
(O/'panel_geometry.json').write_text(json.dumps(outpanels,indent=2))
folder=O/'panel_dxf_REVIEW_ONLY';folder.mkdir(exist_ok=True)
for p in outpanels:
    a=['0','SECTION','2','HEADER','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES']
    for x,y,w,h in [(0,0,p['w'],p['h'])]+[tuple(r) for r in p['rects']]:
        for (ax,ay),(bx,by) in [((x,y),(x+w,y)),((x+w,y),(x+w,y+h)),((x+w,y+h),(x,y+h)),((x,y+h),(x,y))]:a += list(map(str,['0','LINE','8','OUTLINE','10',ax,'20',ay,'30',0,'11',bx,'21',by,'31',0]))
    for x,y,r in p['circles']:a+=list(map(str,['0','CIRCLE','8','DRILL','10',x,'20',y,'30',0,'40',r]))
    a+=['0','ENDSEC','0','EOF'];(folder/(p['name']+'.dxf')).write_text('\n'.join(a)+'\n')
# Full modeled-part check except explicit reservation envelopes and guard seams inherited from R00.
checks=0;clashes=[];excluded=[]
for n,a in enumerate(records):
    if a['kind']=='reservation':continue
    for b in records[n+1:]:
        if b['kind']=='reservation':continue
        if a['kind']==b['kind']=='guard':continue
        checks+=1
        v=a['obj'].Shape.common(b['obj'].Shape).Volume
        if v>.05:clashes.append([a['name'],b['name'],round(v,4)])
audit={'revision':'D01-R01','base_sha256':basehash,'base_unchanged':hashlib.sha256(base.read_bytes()).hexdigest()==basehash,'objects':len(records),'all_shapes_valid':all(r['obj'].Shape.isValid() for r in records),'checked_pairs':checks,'clashes_mm3':clashes,'excluded':'Reservations and inherited guard-to-guard seams. Threads, many heads/nuts, actual perforations and bend fillets not modeled. Not a safety/strength/airflow check.'}
step=Part.read(str(O/'D01_R01_ASSEMBLY.step'));total=sum(r['obj'].Shape.Volume for r in records)
reopened=A.openDocument(str(O/'D01_R01_ASSEMBLY.FCStd'))
audit['STEP_valid']=step.isValid();audit['STEP_volume_matches']=math.isclose(step.Volume,total,rel_tol=1e-7)
audit['native_reopen_count']=len([o for o in reopened.Objects if hasattr(o,'Shape')]);audit['panel_DXF_count']=len(outpanels)
assert audit['base_unchanged'] and audit['all_shapes_valid'] and audit['STEP_valid'] and audit['STEP_volume_matches'] and not clashes
(O/'checks.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
