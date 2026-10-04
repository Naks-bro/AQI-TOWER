"""D01 coherent assembly and 1:1 panel geometry. Run with FreeCAD bundled Python.
CAD envelopes do not certify strength, leakage, finger protection or performance.
Generated output is deliberately marked unreleased. Preserve historical tower CAD.
"""
import json, math, csv
from pathlib import Path
import FreeCAD as A
import Part

ROOT=Path(__file__).resolve().parents[2]
C=json.loads((ROOT/'cad/parametric/d01_r00.json').read_text())
OUT=ROOT/'reports/prototype_d01'
OUT.mkdir(parents=True,exist_ok=True)
V=A.Vector
doc=A.newDocument('AQI_D01_R00')
items=[]; drawings=[]
def box(x,y,z,dx,dy,dz): return Part.makeBox(dx,dy,dz,V(x,y,z))
def add(name,shape,color,kind,explode=(0,0,0),note='PROPOSED GEOMETRY; review required'):
    assert shape.isValid() and shape.Volume>0,name
    o=doc.addObject('PartDesign::Feature',name); o.Shape=shape; o.Label=name.replace('_',' ')
    o.addProperty('App::PropertyString','ReleaseStatus');o.ReleaseStatus=note
    o.addProperty('App::PropertyString','PartType');o.PartType=kind
    items.append(dict(name=name,obj=o,color=color,kind=kind,explode=explode,note=note))
    return o
wood='#b7c9cc';dark='#243c4a';green='#008b7f';filtercol='#eee5d4';seal='#405563';metal='#9aaebb'
def ring_y(x,y,z,w,h,t,inner):
    return box(x,y,z,w,t,h).cut(box(x+(w-inner)/2,y-1,z+(h-inner)/2,inner,t+2,inner))
def ring_z(x,y,z,w,d,t,diam):
    return box(x,y,z,w,d,t).cut(Part.makeCylinder(diam/2,t+2,V(x+w/2,y+d/2,z-1)))
def holes_y(shape,pts,y,t,r):
    for x,z in pts:shape=shape.cut(Part.makeCylinder(r,t+2,V(x,y-1,z),V(0,1,0)))
    return shape
def rectdraw(name,w,h,thick,rects=(),circles=(),qty=1,note=''):
    drawings.append(dict(name=name,w=w,h=h,thick=thick,rects=list(rects),circles=list(circles),qty=qty,note=note))
W=C['cabinet_width'];D=C['cabinet_depth'];T=C['panel_thickness'];Z=C['cabinet_top'];F=C['filter_side'];FD=C['filter_depth'];G=C['installed_filter_gasket'];cz=C['filter_center_z']
bz=C['foot_height'];lo=bz+T;hi=Z-T;H=hi-lo;fx=(W-F)/2;fz=cz-F/2
bolts=[(20,z) for z in (55,305,555)]+[(530,z) for z in (55,305,555)]+[(275,50),(275,560)]
add('M01_Base',box(0,0,bz,W,D,T),wood,'panel',(0,0,-55))
rectdraw('M01_BASE',W,D,T,note='Screw into internal cleats; drill pilots after square dry fit.')
add('M02_Left',box(0,0,lo,T,D,H),wood,'panel',(-100,0,0))
add('M02_Right',box(W-T,0,lo,T,D,H),wood,'panel',(100,0,0))
rectdraw('M02_END',D,H,T,qty=2,note='No cutouts; internal cleats 20x20; screw positions match-drilled.')
for rear in (False,True):
    suffix='Rear' if rear else 'Front';y=D-T if rear else 0;ex=170 if rear else -170
    seat=ring_y(T,y,lo,W-2*T,H,T,C['intake_aperture'])
    # Centre aperture explicitly at z305 (panel centre300 is NOT filter centre).
    seat=box(T,y,lo,W-2*T,T,H).cut(box(40,y-1,70,470,T+2,470))
    seat=holes_y(seat,bolts,y,T,2.75)
    add('M03_Seat_'+suffix,seat,wood,'panel',(0,ex*.35,0))
    gy=D if rear else -G; fy=D+G if rear else -G-FD
    gasket=ring_y(fx,gy,fz,F,F,G,F-2*C['filter_gasket_width'])
    add('S01_Filter_seal_'+suffix,gasket,seal,'seal',(0,ex*.5,0),'ASSUMED 4mm free foam to3mm installed; compression force and frame landing unverified')
    # Filter OEM envelope, not internal pleat CAD.
    add('F01_MERV13_'+suffix,box(fx,fy,fz,F,FD,F),filtercol,'filter',(0,ex,0),'OEM external dimensions only; MERV13 not HEPA; arrow points into cabinet')
    ry=fy+FD if rear else fy-T
    rr=ring_y(0,ry,30,550,550,T,475)
    rr=holes_y(rr,bolts,ry,T,2.75)
    add('M04_Retainer_'+suffix,rr,green,'panel',(0,ex*1.5,0))
    for k,(x,z) in enumerate(bolts):
        # 100mm studs reach through the 20mm corner cleats as well as the seat.
        length=80 if x==275 else 100
        yy=(343 if rear else -63) if x==275 else (325 if rear else -65)
        add('H01_Stud_'+suffix+str(k+1),Part.makeCylinder(2.5,length,V(x,yy,z),V(0,1,0)),metal,'hardware',(0,ex*1.5,0),f'M5x{length} proposed; washers/nuts and retained service hardware required; not strength-rated')
    # Shelf supports filter weight independently of clamping friction.
    shelf_y=D if rear else -G-FD
    add('M05_Filter_shelf_'+suffix,Part.makeCompound([box(30,shelf_y,fz-9,235,FD+G,9),box(285,shelf_y,fz-9,235,FD+G,9)]),wood,'support',(0,ex*.75,0),'Two235mm ledges with20mm central gap to clear lower clamp stud')
rectdraw('M03_SEAT',W-2*T,H,T,rects=[(31,41,470,470)],circles=[(x-T,z-lo,2.75) for x,z in bolts],qty=2,note='Datum lower left viewed from outside; mirror rear physically. Aperture NOT panel-centred vertically.')
rectdraw('M04_RETAINER',550,550,T,rects=[(37.5,37.5,475,475)],circles=[(x,z-30,2.75) for x,z in bolts],qty=2,note='M5 through studs, 8 per face, minimum20mm centre-to-edge on retainer. Tighten evenly; no invented torque or seal-force rating.')
rectdraw('M05_SHELF',235,FD+G,T,qty=4,note='Two per filter; x30..265 and285..520;20mm centre gap clears lower stud. Support angle/cleat review; do not crush paper frame.')
top=box(0,0,hi,W,D,T);topcir=[]
for i,(cx,cy) in enumerate(C['fan_centres']):
    top=top.cut(Part.makeCylinder(C['fan_aperture']/2,T+2,V(cx,cy,hi-1)))
    topcir.append((cx,cy,C['fan_aperture']/2))
    for dx in (-62.5,62.5):
        for dy in (-62.5,62.5):
            top=top.cut(Part.makeCylinder(2.25,T+2,V(cx+dx,cy+dy,hi-1)))
            topcir.append((cx+dx,cy+dy,2.25))
    s=ring_z(cx-70,cy-70,Z,140,140,1,134.2)
    for dx in (-62.5,62.5):
        for dy in (-62.5,62.5):s=s.cut(Part.makeCylinder(2.25,3,V(cx+dx,cy+dy,Z-1)))
    fan=ring_z(cx-70,cy-70,Z+1,140,140,27,130)
    # Hub/blades visual proxies outside precision envelope; not OEM rotor geometry.
    fan=fan.fuse(Part.makeCylinder(22,12,V(cx,cy,Z+8)))
    for ang in range(0,360,60):
        blade=box(cx+15,cy-5,Z+10,47,10,3);blade.rotate(V(cx,cy,0),V(0,0,1),ang);fan=fan.fuse(blade)
    for dx in (-62.5,62.5):
        for dy in (-62.5,62.5):fan=fan.cut(Part.makeCylinder(2.25,30,V(cx+dx,cy+dy,Z)))
    add('S02_Fan_seal_'+str(i+1),s,seal,'seal',(0,0,90))
    add('F02_P14_Max_'+str(i+1),fan,dark,'fan',(0,0,130),'OEM140x140x27,125pitch; simplified rotor, no claimed rotor clearance')
    for j,(dx,dy) in enumerate([(a,b) for a in (-62.5,62.5) for b in (-62.5,62.5)]):
        add('H02_Fan_bolt_'+str(i+1)+'_'+str(j+1),Part.makeCylinder(2,50,V(cx+dx,cy+dy,565)),metal,'hardware',(0,0,140),'M4x50 proposed envelope; actual washers, nuts, seal stack and protrusion to be checked')
add('M06_Fan_plate',top,wood,'panel',(0,0,60))
rectdraw('M06_FAN_PLATE',W,D,T,circles=topcir,note='4 apertures dia134.2; 16 clearance holes dia4.5, 125 square pitch. OEM template confirm before cut. M4 through-bolts proposed; length selected on actual guard/seal stack.')
# Internal corner cleats leave main filter aperture clear.
for x in (9,521):
    for y in (9,331):
        sh=box(x,y,lo,20,20,H)
        sh=holes_y(sh,[(20 if x==9 else 530,z) for z in (55,305,555)],y,20,2.75)
        add('M07_Cleat_'+str(x)+'_'+str(y),sh,wood,'support')
for x in (25,495):
    for y in (15,315):add('M08_Foot_'+str(x)+'_'+str(y),box(x,y,0,30,30,20),dark,'support',(0,0,-70),'Non-slip feet proposed; actual material/attachment and tip test required')
# Tool-fixed guard cages: external and inner. CAD sheet envelopes; perforations specified on drawing, NOT meshed or certified.
for tag,x,y,z,w,d,h,ez in [('Outer',115,20,580,320,320,50,200),('Inner',115,20,530,320,320,41,-70)]:
    basez=z+h if tag=='Outer' else z
    add('G01_'+tag+'_perforated_face',box(x,y,basez,w,d,1),metal,'guard',(0,0,ez),'1mm sheet ENVELOPE ONLY. Proposed4mm holes6mm staggered pitch (~40%open). Deburr, fix, review reach/deflection; not safety certified')
    for n,sh in enumerate([box(x,y,z,1,d,h),box(x+w-1,y,z,1,d,h),box(x+1,y,z,w-2,1,h),box(x+1,y+d-1,z,w-2,1,h)]):
        add('G02_'+tag+'_skirt_'+str(n),sh,metal,'guard',(0,0,ez),'Solid skirt; corner joints and attachment flanges require shop detail')
    rectdraw('G01_'+tag.upper()+'_FACE',w,d,1,note='Perforated purchased sheet; 4mm holes/6mm staggered pitch target. Hole pattern NOT in DXF. Folded/angle-fastened skirts require shop detail.')
# External control mounting envelope, not a selected enclosure. Keep accessible away from exhaust.
add('E01_Control_box_RESERVATION',box(W,110,390,40,140,100),green,'reservation',(90,0,0),'140x100x40 external reservation; exact enclosure, mounting, glands and routing NOT detailed')
doc.recompute()
doc.saveAs(str(OUT/'D01_ASSEMBLY.FCStd'))
Part.export([i['obj'] for i in items],str(OUT/'D01_ASSEMBLY.step'))
mesh=[]
for i in items:
    verts,tris=i['obj'].Shape.tessellate(1.5)
    mesh.append({k:i[k] for k in ('name','color','kind','explode','note')}|{'vertices':[[v.x,v.y,v.z] for v in verts],'triangles':[list(t) for t in tris]})
(OUT/'cad_mesh.json').write_text(json.dumps(mesh))
(OUT/'panel_geometry.json').write_text(json.dumps(drawings,indent=2))
# DXF R12 using LINE/CIRCLE avoids tool-specific dependencies. mm, no kerf offset.
def dxf(d):
    a=['0','SECTION','2','HEADER','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES']
    def line(x,y,X,Y): a.extend(map(str,['0','LINE','8','OUTLINE','10',x,'20',y,'30',0,'11',X,'21',Y,'31',0]))
    def rect(x,y,w,h):
        for p,q in [((x,y),(x+w,y)),((x+w,y),(x+w,y+h)),((x+w,y+h),(x,y+h)),((x,y+h),(x,y))]:line(*p,*q)
    rect(0,0,d['w'],d['h'])
    for r in d['rects']:rect(*r)
    for x,y,r in d['circles']:a.extend(map(str,['0','CIRCLE','8','CUT','10',x,'20',y,'30',0,'40',r]))
    a+=['0','ENDSEC','0','EOF'];return '\n'.join(a)+'\n'
(OUT/'panel_dxf_REVIEW_ONLY').mkdir(exist_ok=True)
for d in drawings:(OUT/'panel_dxf_REVIEW_ONLY'/f"{d['name']}.dxf").write_text(dxf(d))
# Nominal contact/interference audit: excludes OEM internal proxies, studs, guard sheet envelope intersections, reservations.
checked=[i for i in items if i['kind'] in ('panel','support','seal','filter','fan')]
clashes=[]
for n,i in enumerate(checked):
    for j in checked[n+1:]:
        overlap=i['obj'].Shape.common(j['obj'].Shape).Volume
        if overlap>0.05:clashes.append([i['name'],j['name'],round(overlap,3)])
valid=all(i['obj'].Shape.isValid() for i in items)
hardware_clashes=[];hardware_checks=0
for i in [a for a in items if a['kind']=='hardware']:
    for j in [a for a in items if a['kind'] not in ('hardware','reservation')]:
        hardware_checks+=1;v=i['obj'].Shape.common(j['obj'].Shape).Volume
        if v>.05:hardware_clashes.append([i['name'],j['name'],round(v,3)])
audit={'objects':len(items),'all_shapes_valid':valid,'checked_pairs':len(checked)*(len(checked)-1)//2,'positive_volume_clashes_mm3':clashes,'hardware_pairs':hardware_checks,'hardware_clashes_mm3':hardware_clashes,'excluded':'simplified fan internals, guard-to-guard sheet envelope intersections, reservations; nuts/washers absent; no strength/leak/guard certification','panel_dimensions_mm':drawings}
(OUT/'geometry_checks.json').write_text(json.dumps(audit,indent=2))
# Separate exploded native file, same parts, explicit translation, no new design branch.
ed=A.newDocument('AQI_D01_R00_EXPLODED')
for i in items:
    o=ed.addObject('PartDesign::Feature',i['name']);o.Label=i['obj'].Label;sh=i['obj'].Shape.copy();sh.translate(V(*i['explode']));o.Shape=sh
ed.recompute();ed.saveAs(str(OUT/'D01_EXPLODED.FCStd'))
print(json.dumps({k:v for k,v in audit.items() if k!='panel_dimensions_mm'},indent=2))
