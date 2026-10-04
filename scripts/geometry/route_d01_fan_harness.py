"""Integrated harness routing reservations; no connector, clamp or guard-cut approval."""
from pathlib import Path
import json,hashlib,math
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2];B=R/'reports/prototype_d01/mechanical_package';O=B/'harness_detail';O.mkdir(exist_ok=True)
source=B/'D01_R03M_ASSEMBLY.FCStd';sha=hashlib.sha256(source.read_bytes()).hexdigest()
src=A.openDocument(str(source));doc=A.newDocument('D01_R03M_Harness_Study');V=A.Vector
meta={r['name']:r for r in json.loads((B/'cad_mesh.json').read_text())}
for old in src.Objects:
    ob=doc.addObject('PartDesign::Feature',old.Name);ob.Shape=old.Shape.copy()
    ob.addProperty('App::PropertyString','ReleaseStatus');ob.ReleaseStatus='Inherited R03M review-only geometry'
routes=[];checks=[];tubes=[]
for i,(x,y,z) in enumerate([(269,178,590),(419,178,594),(269,182,598),(419,182,602)],1):
    # Starts are proposed emergence locations OUTSIDE fan bodies, not verified OEM exits.
    pts=[(x,y,z),(427,y,z),(427,180,z),(433,180,z)]
    solids=[]
    for a,b in zip(pts,pts[1:]):
        delta=V(*b)-V(*a);solids.append(Part.makeCylinder(1.5,delta.Length,V(*a),delta.normalize()))
    tube=solids[0].multiFuse(solids[1:]);hits=[]
    tubes.append(tube)
    for old in src.Objects:
        if meta[old.Name]['kind']=='reservation':continue
        vol=tube.common(old.Shape).Volume
        if vol>.01:hits.append({'part':old.Name,'intersection_mm3':vol})
    obj=doc.addObject('PartDesign::Feature',f'R_Harness_{i}_ASSUMED_3mm');obj.Shape=tube
    obj.addProperty('App::PropertyString','ReleaseStatus');obj.ReleaseStatus='ASSUMED3mm routing envelope; not cable specification. Sharp elbows not manufacturable bend definition.'
    length=sum((V(*b)-V(*a)).Length for a,b in zip(pts,pts[1:]))
    # Includes the unmodeled protected crossing from433 to435 and external reservation legs.
    route_to_box=length+2+130+(z-490)
    routes.append(dict(fan=i,proposed_points_mm=pts,internal_polyline_mm=length,
       length_to_box_reference_mm=route_to_box,assumed_service_and_bend_allowance_mm=50,
       screening_required_length_mm=route_to_box+50,
       difference_vs_400mm_lead_mm=400-route_to_box-50,clashes=hits))
    checks.append(not hits)
doc.recompute();assert all(checks),routes
pair_volumes=[tubes[i].common(tubes[j]).Volume for i in range(4) for j in range(i+1,4)]
assert all(v<.01 for v in pair_volumes)
out=O/'D01_R03M_HARNESS_REVIEW.FCStd';doc.saveAs(str(out));A.closeDocument(doc.Name)
reopened=A.openDocument(str(out));assert len(reopened.Objects)==len(src.Objects)+4
assert all(o.Shape.isValid() for o in reopened.Objects)
A.closeDocument(reopened.Name);A.closeDocument(src.Name)
data=dict(source_sha256=sha,source_unchanged=hashlib.sha256(source.read_bytes()).hexdigest()==sha,
 status='ROUTING RESERVATION ONLY - NO FABRICATION OR WIRING RELEASE',
 routes=routes,all_internal_envelopes_clear=all(checks),route_pair_intersection_volumes_mm3=pair_volumes,assumed_cable_envelope_diameter_mm=3,
 boundary='Each tube stops atx433 INSIDE guard; guard inner face startsx434. No cutout, through-guard connector, gland, cable anchor or external bend modeled.',
 unknowns=['Actual OEM cable emergence/orientation','Actual lead jacket/individual-wire/sleeve section and connector envelope','Bend radius and retention','Exact split grommet/harness compatibility','Closed guard entry and side enclosure mounting'],
 note='All493 source objects preserved; added4 routing reservations. Connector insertion, pullout, clamps, curved bends, per-wire separation and guard removal not validated.')
assert data['source_unchanged'];(O/'ROUTING_CHECKS.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print(json.dumps(data,indent=2))
