"""E03 original external-module envelopes checked against a private OEM STEP.

Run with existing FreeCAD bundled Python. Does not modify R03M or redistribute
the downloaded OEM model. Shapes published here are deliberately simple proxies.
"""
from pathlib import Path
import hashlib, json
import FreeCAD as A
import Part

R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/electrical_package/control_module'
O.mkdir(exist_ok=True)
OEM=R/'tmp/control_oem/step/1554XA2GY.stp'
if not OEM.is_file(): raise SystemExit('Download exact Hammond STEP locally first; see source URL in README.')
source=R/'reports/prototype_d01/mechanical_package/D01_R03M_ASSEMBLY.FCStd'
native_hash=hashlib.sha256(source.read_bytes()).hexdigest()
oem=Part.read(str(OEM))
assert len(oem.Solids)==24, 'Unexpected OEM STEP revision; re-review solid identities'
panel=oem.Solids[3]
assert abs(panel.BoundBox.XLength-285)<.01 and abs(panel.BoundBox.YLength-185)<.01
z=panel.BoundBox.ZMax
V=A.Vector
def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,V(x,y,z))
doc=A.newDocument('D01_E03_EXTERNAL_CONTROL_ENVELOPES')
records=[]
def add(name,shape,status,color):
    obj=doc.addObject('PartDesign::Feature',name);obj.Shape=shape
    obj.addProperty('App::PropertyString','EvidenceStatus');obj.EvidenceStatus=status
    records.append(dict(name=name,bounds_mm=[shape.BoundBox.XMin,shape.BoundBox.YMin,shape.BoundBox.ZMin,
                    shape.BoundBox.XMax,shape.BoundBox.YMax,shape.BoundBox.ZMax],status=status,color=color))
    return shape
# Original full-wall proxy omits moulded bosses, recesses, seals and panel contour.
# Precise collision assessment below uses private OEM solids instead.
shell=box(-150,-100,-70.08,300,200,120.08).cut(box(-145,-95,-65,290,190,111))
add('CB1_SIMPLIFIED_ENVELOPE',shell,'ORIGINAL APPROXIMATE SHELL; not Hammond manufacturing geometry','#d7e5e9')
plate=box(-142.5,-92.5,-60,285,185,z+60)
for x in (-122.5,-22.5):plate=plate.cut(Part.makeCylinder(2.25,4,V(x,0,-61)))
add('PL1_SIMPLIFIED_PANEL',plate,'OEM285x185 outline; simplified rectangular proxy, contour/holes omitted except2 proposed4.5mm holes','#aab8c4')
rail=box(-135,-17.5,z,125,35,7.5)
add('DIN1_ENVELOPE',rail,'OEM35x7.5 profile envelope; proposed125mm cut, not full profile or approved attachment','#6b8398')
parts={
 'CTRL1_OPTA_LITE':box(-115,-44.4,z+7.5,70,88.8,61.1),
 'H1_NA_FH1':box(20,-65,z+5,93,43,12.5),
 'SC1_NA_FC1':box(40,25,z+5,48,25,21),
}
for name,s in parts.items():
    add(name,s,'OEM BODY DIMENSIONS / ASSUMED POSITION, ORIENTATION AND MOUNT; no connector geometry',
        {'CTRL1_OPTA_LITE':'#1b8b83','H1_NA_FH1':'#405773','SC1_NA_FC1':'#d49a40'}[name])
# Transparent service/routing reservations are NOT verified cable bend radii.
keeps={
 'CTRL1_WIRE_SPACE_ASSUMED':box(-125,-64.4,z+7.5,90,128.8,61.1),
 'H1_CONNECTOR_SPACE_ASSUMED':box(10,-85,z+5,113,83,27.5),
 'SC1_CONNECTOR_SPACE_ASSUMED':box(30,5,z+5,68,65,36),
}
for name,s in keeps.items():add(name,s,'ASSUMED routing/service volume; actual connectors/clip release and bends unknown','#bf73bd')
collisions=[]
for name,s in parts.items():
    hits=[]
    for i,solid in enumerate(oem.Solids):
        if i==3:continue # mounting panel contact/support assessed separately
        v=s.common(solid).Volume
        if v>.01:hits.append(dict(OEM_solid=i,volume_mm3=v))
    collisions.append(dict(part=name,hits=hits))
keep_hits=[]
for name,s in keeps.items():
    hits=[]
    for i,solid in enumerate(oem.Solids):
        if i==3:continue
        v=s.common(solid).Volume
        if v>.01:hits.append(dict(OEM_solid=i,volume_mm3=v))
    keep_hits.append(dict(reservation=name,hits=hits))
pair_checks=[]
for i,(name,s) in enumerate(parts.items()):
    for other,t in list(parts.items())[i+1:]:
        pair_checks.append(dict(parts=[name,other],overlap_mm3=s.common(t).Volume,distance_mm=s.distToShape(t)[0]))
assert not any(c['hits'] for c in collisions),collisions
assert not any(c['hits'] for c in keep_hits),keep_hits
assert all(p['overlap_mm3']<.01 for p in pair_checks),pair_checks
doc.recompute();doc.saveAs(str(O/'D01_E03_CONTROL_ENVELOPES.FCStd'))
Part.export(list(doc.Objects),str(O/'D01_E03_CONTROL_ENVELOPES.step'))
# Normalize harmless exporter trailing spaces for clean repository diffs.
step_path=O/'D01_E03_CONTROL_ENVELOPES.step'
step_path.write_text('\n'.join(line.rstrip() for line in step_path.read_text().splitlines())+'\n')
A.closeDocument(doc.Name)
check=A.openDocument(str(O/'D01_E03_CONTROL_ENVELOPES.FCStd'))
assert len(check.Objects)==9 and all(o.Shape.isValid() for o in check.Objects)
A.closeDocument(check.Name)
data=dict(status='OEM MODEL BODY-FIT SCREEN / NOT FABRICATION OR WIRING RELEASE',
    native_tower_sha256=native_hash,native_tower_unchanged=hashlib.sha256(source.read_bytes()).hexdigest()==native_hash,
    OEM_STEP_sha256=hashlib.sha256(OEM.read_bytes()).hexdigest(),OEM_STEP_solids=24,
    OEM_STEP_source='https://www.hammfg.com/files/parts/stp/1554XA2GY.zip',
    panel_top_z_mm=z,panel_thickness_in_STEP_mm=panel.BoundBox.ZLength,
    objects=records,body_vs_actual_OEM_checks=collisions,assumed_space_vs_actual_OEM_checks=keep_hits,
    body_pair_checks=pair_checks,proposed_DIN_holes_mm=[[-122.5,0],[-22.5,0]],proposed_hole_diameter_mm=4.5,
    sources={'box':'https://www.hammfg.com/files/parts/pdf/1554XA2GY.pdf',
      'panel':'https://www.hammfg.com/files/parts/pdf/1554XPL.pdf',
      'opta':'https://docs.arduino.cc/resources/datasheets/AFX00001-AFX00002-AFX00003-datasheet.pdf',
      'rail':'https://www.phoenixcontact.com/en-us/products/din-rail-ns-35-75-perf-2000mm-0801733',
      'hub':'https://www.noctua.at/en/products/na-fh1/specifications',
      'speed_controller':'https://www.noctua.at/en/products/na-fc1/specifications'},
    access_date='2026-10-05',
    limitations=['Exact Opta DIN seating plane unknown; back face placed above rail crest conservatively',
      'OEM panel page rounds thickness to2mm; downloadedSTEP1.6256mm, do not select fastener lengths from either alone',
      'Assumed5mm hub/controller carrier lift; no actual carrier/clamps/retention hardware',
      'Cable connectors, bend radii, button backs, glands, PR1/protection, functional earth and heat not modeled',
      'Power adapter remains external; no mains inside proposed box',
      'Closed-box dial/button operation not solved; no lid or wall drilling released',
      'Box remains freestanding off-tower; not a new approved tower mount or stable placement',
      'OEMSTEP kept local; published CAD contains only original simplified envelopes'],
    release=False,physical_tests=0)
(O/'FIT_CHECKS.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:data[k] for k in ('status','panel_top_z_mm','body_vs_actual_OEM_checks','assumed_space_vs_actual_OEM_checks','body_pair_checks','native_tower_unchanged')},indent=2))
