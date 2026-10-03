"""Read-only, whole-assembly audit and panel extraction from current saved CAD.

Creates one consistent review handoff without regenerating historical revisions.
"""
import json,csv,hashlib,math,argparse
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--source-dir',default='reports/prototype_d01/r02_guards');parser.add_argument('--output-dir',default='reports/prototype_d01/current_handoff');parser.add_argument('--cad-file',default='D01_R02G_ASSEMBLY.FCStd');args=parser.parse_args()
B=R/args.source_dir;O=R/args.output_dir;O.mkdir(exist_ok=True)
source=B/args.cad_file;sha=hashlib.sha256(source.read_bytes()).hexdigest()
doc=A.openDocument(str(source));meta={m['name']:m for m in json.loads((B/'cad_mesh.json').read_text())}
items=[];panels=[]
for obj in doc.Objects:
    m=meta[obj.Name];s=obj.Shape;b=s.BoundBox
    items.append(dict(id=obj.Name,kind=m['kind'],qty=1,x_mm=b.XLength,y_mm=b.YLength,z_mm=b.ZLength,
        volume_mm3=s.Volume,status='RESERVATION - NOT A PART' if m['kind']=='reservation' else 'REVIEW ONLY',note=m['note']))
    if m['kind']!='panel':continue
    # Only actual flat panels: current panel parts have one uniform thin dimension.
    axis=min(range(3),key=lambda k:[b.XLength,b.YLength,b.ZLength][k]);basis=[i for i in range(3) if i!=axis]
    candidates=[]
    for face in s.Faces:
        n=face.normalAt(0,0);v=[n.x,n.y,n.z]
        if v[axis]>.99999:candidates.append(face)
    if not candidates:raise ValueError('No outward planar face: '+obj.Name)
    face=max(candidates,key=lambda f:f.Area);mins=[b.XMin,b.YMin,b.ZMin]
    def uv(v):return [getattr(v,'xyz'[i])-mins[i] for i in basis]
    edges=[]
    for e in face.Edges:
        if isinstance(e.Curve,Part.Circle):
            if abs(e.Length-2*math.pi*e.Curve.Radius)>1e-5:raise ValueError('Partial circle not supported')
            edges.append(dict(type='circle',center=uv(e.Curve.Center),radius=e.Curve.Radius))
        else:
            pts=e.discretize(Number=2)
            if abs(e.Length-(pts[1]-pts[0]).Length)>1e-5:raise ValueError('Nonlinear edge not supported')
            edges.append(dict(type='line',a=uv(pts[0]),b=uv(pts[1])))
    dims=[b.XLength,b.YLength,b.ZLength]
    panels.append(dict(id=obj.Name,w=dims[basis[0]],h=dims[basis[1]],t=dims[axis],
        axes=''.join('xyz'[i] for i in basis),edges=edges,face_area_mm2=face.Area,
        thickness_area_volume_check=math.isclose(face.Area*dims[axis],s.Volume,rel_tol=1e-7)))
    assert panels[-1]['thickness_area_volume_check'],obj.Name
pairs=0;clashes=[];excluded=0
for i,a in enumerate(doc.Objects):
    for b in doc.Objects[i+1:]:
        ka,kb=meta[a.Name]['kind'],meta[b.Name]['kind']
        if 'reservation' in (ka,kb) or ka==kb=='guard':excluded+=1;continue
        pairs+=1
        # Bounding boxes only skip impossible pairs; overlap candidates use exact BRep.
        if not a.Shape.BoundBox.intersect(b.Shape.BoundBox):continue
        v=a.Shape.common(b.Shape).Volume
        if v>.05:clashes.append(dict(a=a.Name,b=b.Name,volume_mm3=v))
audit=dict(source=str(source.relative_to(R)),source_sha256=sha,objects=len(items),panels=len(panels),
    full_pair_checks=pairs,excluded_pairs=excluded,clashes_mm3=clashes,valid=all(o.Shape.isValid() for o in doc.Objects),
    source_unchanged=hashlib.sha256(source.read_bytes()).hexdigest()==sha,
    exclusions='Reservation envelopes and all guard-to-guard pairs (inherited seams). Nominal fit only; no tolerance/load/reach/leak/electrical release.',
    inventory_note='CAD object count is not purchased-product count. Reserved controls are not physically modeled; missing hardware/services are separately listed.')
assert audit['valid'] and audit['source_unchanged'] and not clashes,audit
(O/'assembly_audit.json').write_text(json.dumps(audit,indent=2));(O/'current_panels.json').write_text(json.dumps(panels,indent=2))
with (O/'CAD_PART_INVENTORY.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
dxf=O/'panel_DXF_REVIEW_ONLY';dxf.mkdir(exist_ok=True)
for p in panels:
    a=['0','SECTION','2','HEADER','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES']
    for e in p['edges']:
        if e['type']=='circle':a+=list(map(str,['0','CIRCLE','8','CAD_FACE','10',e['center'][0],'20',e['center'][1],'30',0,'40',e['radius']]))
        else:a+=list(map(str,['0','LINE','8','CAD_FACE','10',e['a'][0],'20',e['a'][1],'30',0,'11',e['b'][0],'21',e['b'][1],'31',0]))
    a+=['0','ENDSEC','0','EOF'];(dxf/(p['id']+'.dxf')).write_text('\n'.join(a)+'\n')
print(json.dumps(audit,indent=2))
