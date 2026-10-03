"""Single mechanical package: current CAD, joints, sealing, assembly and review sheets."""
import ast,json,math,csv,hashlib,zipfile
from pathlib import Path
import numpy as np
from PIL import Image,ImageColor
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/mechanical_package';M=json.loads((O/'cad_mesh.json').read_text());GUARD_RIM_MM=10
fn=next(n for n in ast.parse((R/'scripts/reports/build_d01_delivery.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='render')
exec(compile(ast.Module(body=[fn],type_ignores=[]),'shared_renderer','exec'),globals())
if not (O/'D01_ASSEMBLY.png').exists():render()
if not (O/'D01_EXPLODED.png').exists():render(True)
a=json.loads((O/'checks.json').read_text());s=json.loads((O/'mechanical_screen.json').read_text());service=json.loads((O/'service_checks.json').read_text());panels=json.loads((O/'current_panels.json').read_text());fasteners=json.loads((O/'fasteners.json').read_text())
fasteners += [dict(item='Retained adapter M4 hardware',qty=8,spec='8 M4x80 studs;4 M4x25 ledge screws;28 nuts;32 washers',status='R02H geometry retained; sealing washers separate'),dict(item='Independent guard bolts',qty=8,spec='8 M4x20 screws;8 nuts;16 washers',status='R02G mounting stacks retained; welded cage replaces rivets')]
assert not a['clashes_mm3'] and a['STEP_valid'] and a['STEP_volume_matches']
assert service['source_sha256']==hashlib.sha256((O/'D01_R03M_ASSEMBLY.FCStd').read_bytes()).hexdigest()
vv=[v for m in M if m['kind']!='reservation' for v in m['vertices']]
envelope=[max(v[k] for v in vv)-min(v[k] for v in vv) for k in range(3)]
holes=[]
for row in range(58):
    y=12+row*6*math.sqrt(3)/2
    if y>308:continue
    for col in range(51):
        x=12+col*6+(3 if row%2 else 0)
        if x<=308:holes.append((x,y,2))
area=len(holes)*math.pi*4/1e6
guard=dict(outside_mm=[320,320,1],qty=2,hole_diameter_mm=4,pitch_mm=6,minimum_unperforated_border_mm=10,holes=len(holes),hole_area_m2=area,active_area_porosity=area/.09,notes='Proposed actual2D cut pattern.3D sheets remain envelopes; no reach/deflection/weld release. Pressure calculations must use this area if adopted.')
assert all(x-r>=10 and y-r>=10 and x+r<=310 and y+r<=310 for x,y,r in holes)
guard['loss_multiplier_vs_previous_area_at_same_flow_and_K']=(.036/area)**2
guard['minimum_nominal_hole_ligament_mm']=2
(O/'guard_pattern.json').write_text(json.dumps(guard,indent=2))
blanks=[('G_FACE',320,320,2,holes),('G_OUTER_SIDE',320,50,2,[]),('G_OUTER_END',318,50,2,[]),('G_INNER_SIDE',320,40,2,[]),('G_INNER_END',318,40,2,[])]
for name,w,h,qty,hh in blanks:
    dx=['0','SECTION','2','HEADER','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES']
    corners=[(0,0),(w,0),(w,h),(0,h),(0,0)]
    for p,q in zip(corners,corners[1:]):dx+=list(map(str,['0','LINE','8','OUTLINE','10',p[0],'20',p[1],'30',0,'11',q[0],'21',q[1],'31',0]))
    for x,y,r in hh:dx+=list(map(str,['0','CIRCLE','8','HOLES','10',x,'20',y,'30',0,'40',r]))
    dx+=['0','ENDSEC','0','EOF'];(O/'panel_DXF_REVIEW_ONLY'/(name+'.dxf')).write_text('\n'.join(dx)+'\n')
with (O/'FASTENER_SCHEDULE.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(fasteners[0]));w.writeheader();w.writerows(fasteners)
with (O/'GUARD_BLANKS.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['id','width_mm','height_mm','thickness_mm','qty','status'])
    for n,ww,hh,q,holes0 in blanks:w.writerow([n,ww,hh,1,q,'PROPOSED steel; weld/strength/flatness not released'])
c=canvas.Canvas(str(O/'AQI_D01_MECHANICAL_PACKAGE.pdf'),pagesize=(842,595));page=0
def text(x,y,t,size=11,col='#223a48'):
    c.setFillColor(HexColor(col));c.setFont('Helvetica',size);c.drawString(x,y,t)
def para(x,y,t,w=780,size=11):
    for line in simpleSplit(t,'Helvetica',size,w):text(x,y,line,size);y-=size*1.4
    return y-12
def start(title):
    global page
    if page:c.showPage()
    page+=1;text(30,566,'AQI TOWER / PACKAGE 1: MECHANICAL / R03M / 03 OCT 2026',10,'#008579');text(30,534,title,22)
    text(30,18,'ENGINEERING REVIEW - NOT FABRICATION/SAFETY RELEASE | Indoor only | Physical prototypes: 0',9);text(793,18,str(page),9)
start('One mechanical revision, not another design branch')
c.drawImage(str(O/'D01_ASSEMBLY.png'),20,65,width=500,height=408)
y=490
for t in [f"Same cabinet/filter arrangement. Modeled physical envelope {envelope[0]:.0f} x{envelope[1]:.0f} x{envelope[2]:.0f} mm; excludes control/cable reservations.",
 'Added: complete proposed fan/cabinet/M5 stacks, shorter rods, positive foot bolts, seal-gap stops, and joined guard subassemblies.',
 f"{a['objects']} valid objects; {a['checked_pairs']:,} pair checks clear. Only reservation pairs excluded. STEP/native checks and both200 mm filter-removal sweeps pass.",
 'Still conditional: actual material and weld strength, filter/gasket fit, bearing/preload, stability, guarding tests and electrical enclosure interface. These are not physical PASS results.']:
    y=para(535,y,t,275)
start('Exploded assembly / same modeled parts')
c.drawImage(str(O/'D01_EXPLODED.png'),40,65,width=535,height=437)
para(595,477,'Exploded positions explain grouping; they are not a verified removal trajectory. The complete assembly and exploded native files use the same part identities. Hardware remains schematic: no real threads or weld beads.',210)
para(595,309,'Assemble cabinet and reducer mountings before installing the fan plate/inner guard. Top centre M5 nuts are close to the internal guard: do not assume a socket fits after the guard is installed.',210)
start('Fabrication: two joined guard assemblies')
# Joint map: face and skirt elevation, with welded corner/face labels.
c.setStrokeColor(HexColor('#008579'));c.rect(45,190,300,300)
for x,y,r in holes:c.circle(45+x*300/320,190+y*300/320,r*300/320)
text(45,165,'W1: continuous face-to-skirt perimeter joint',11)
y=490
for t in ['PROPOSED route: fabricated steel guards with joined face, four corner seams and welded mounting-angle laps. This replaces loose sheets/rivets; independent guard-to-plate bolts remain.',
 'Blanks: face320 x320 x1 (quantity2); outer sides320 x50 x1 (2), ends318 x50 x1 (2); inner sides320 x40 x1 (2), ends318 x40 x1 (2). Inner skirt starts at z531, above its1 mm bottom face, eliminating double-counted stock overlap.',
 'W1 joins the face perimeter. W2 joins four vertical corners. W3 joins each mounting-angle lap along its two short edges and top edge. These define joint locations, NOT a released weld size/process. Thin-sheet distortion, toe clearance and capacity require qualified fabrication review.',
 f"Proposed face pattern: {guard['holes']} holes,4 mm diameter,6 mm staggered pitch, at least10 mm solid border. Exact hole area {area:.5f} m2 each.2D DXF supplied;3D face still an envelope. No finger-access approval.",
 'No old rivet holes in the new blanks. Deburr all cut edges; no sharp projections or weld spatter near filters/fans. Material grade/coating and welding procedure are not yet selected.']:
    y=para(380,y,t,425,10)
start('Fastening schedule / installed stacks')
y=490
for r in fasteners:
    if y<100:start('Fastening schedule / continued');y=490
    text(30,y,r['item']+' / quantity '+str(r['qty']),12,'#008579')
    y=para(30,y-18,r['spec']+'. '+r['status'],780,10)
    assert y>42
start('Seal routing and compression stops')
y=490
for t in ['Air path: room -> filter media -> sealed filter border -> reducer -> cabinet plenum -> fan gasket -> fans/outlet. Each bypass joint must be sealed; metal washers and nuts are not air seals.',
 'Outer seal: existing495.3 mm square outside /475.3 inside ring,3 mm installed. Sixteen proposed OD10/ID5.5 x3 mm hard spacers sit outside this ring at the M5 locations. They limit the nominal plate gap; they do not select gasket force.',
 'Filter seal:370 x290 outside /350 x270 inside,3 mm installed. Eight proposed OD6.5/ID4.5 x36 mm sleeves sit between fixed M4 nuts and retainers. With the current nut/washer stack, this gives43 mm from reducer face to retainer:40 mm filter +3 mm gasket.',
 'Tolerance warning: assuming a4 mm free gasket, a39/40/41 mm filter in that fixed gap implies0/25/50% compression. These are illustrations, not measured tolerances. Actual gasket force, filter landing width and thickness must govern final spacer lengths. No tightening torque is invented.',
 'Seal all fixed cabinet edge joints and mounting feedthroughs with compatible selected products. Keep the removable top seam serviceable; do not depend on uncharacterized glue as a structural joint. A continuous perimeter tape/seal route is proposed, product/adhesion/aging unresolved.',
 'Fan seals remain1 mm installed envelopes. Foot and new joint penetrations also need bypass inspection. Leak testing must demonstrate the whole assembled path; a CAD ring and ordinary PM readings do not certify filtration efficiency.']:
    y=para(30,y,t)
start('Supports, weight and stability: what is known')
y=490
for t in ['Filter weight sits on two proposed bent ledges per filter, separate from clamp friction. Each ledge is30 mm wide,43 mm shelf,20 mm downstand,2 mm nominal metal. Bend radius and load capacity remain unverified.',
 'Feet now have positive through fastenings:30 x30 x20 mm proposed blocks;4.5 mm through hole,12 mm diameter x9 mm underside recess. M4x30 screw head is recessed4 mm above floor; two washers and upper nut complete each joint. Actual foot material, tear/compression capacity and friction are unknown.',
 f"Assumed-material CAD subtotal: {s['partial_subtotal_kg']:.2f} kg. It excludes fans, filters, feet, seals and controls. It uses650 kg/m3 panels,600 cleats and7850 metal; these are assumptions. Guard holes are not subtracted from3D mass. This is NOT the device weight or its full centre of gravity.",
 'Static tipping sensitivity assumes a centred whole machine, support polygon x25..525/y15..345 and a push at631 mm height. At hypothetical15 kg whole mass, front/back tipping balance is38.5 N; at20 kg,51.3 N. No safety factor, sliding, impact or public misuse is included.',
 'Consequences: supervised level indoor floor only after stability review; protect against cable pull and handling impacts. Do not lift by the lid, guards or filter retainers. No public/outdoor deployment or invented ballast/anchor selection.']:
    y=para(30,y,t)
start('Assembly sequence / one coherent build route')
y=490
steps=['Review hold points before ordering/cutting: real filter and gasket dimensions, material grades, joint/weld method, fastener/tool access and protective enclosure interface.',
 'Prepare the10 panel blanks and revised guard blanks. The new base adds foot holes. Verify dimensions and hole locations against the current revision only; dry-fit for square and flatness.',
 'Assemble base, side/seat panels and cleats with the proposed through-fastener stacks. Install foot bolts from the recessed underside. Do not crush wood or foot material; torque values await material/joint review.',
 'Install outer gasket,3 mm stops, reducers and short M5 rods. Hold inside nuts before the fan plate/inner guard blocks access. Seal fixed joints and feedthroughs using verified products.',
 'Install ledges, M4 studs/sealing washers/fixed nuts, then verified filter gasket and filter. Fit measured-length stop sleeves, retainers, washers and service nuts evenly. Confirm actual compression, no frame damage and support contact.',
 'Fabricate guards using reviewed joints; independently mount the inner guard to the fan plate. Install fan gaskets and16 fan bolt stacks, then outer guard using its separate four mounts. Ensure clearance after fastening.',
 'Fit the top and complete the reviewed control-enclosure/cable interface from package2. Keep cables clear of impellers, service openings and sharp edges. Do not energize at this stage.',
 'Perform mechanical dry-fit, guard/access, seal, load and stability checks; then qualified electrical commissioning. Physical airflow/filter trials belong to package3.']
for i,t in enumerate(steps,1):y=para(30,y,str(i)+'. '+t,780,10)
start('Release record / exact remaining holds')
y=490
for t in ['DIGITAL CHECKED: assembly shapes, modeled interference, native/STEP export, matching panel faces, proposed full fastener stacks, both filter extraction sweeps, and reproducible mass/tolerance arithmetic. These do not prove physical integrity.',
 'HOLD M1 - Materials and joints: actual panel/cleat/foot/metal properties; wood bearing and end-grain withdrawal, panel/retainer bending, bracket capacity, weld procedure/quality and guard deflection. No load rating is released.',
 'HOLD M2 - Seals and fit: actual filter border/thickness/mass, selected gasket force/deflection and products, final stop lengths, foot and new fastener penetration sealing, filter frame loads and physical leak results.',
 'HOLD M3 - Access and stability: actual tool/hand paths, guard reach/probe tests, loose/captive hardware risk, full weight/CG and tipping/sliding/handling checks. Power must be isolated before access; no running-fan demonstration authorized.',
 'INTERFACE TO PACKAGE2: exact control enclosure, cable glands/restraints and protective isolation/restart system are not specified by this mechanical package. The present exterior box/cable CAD remains a reservation, not a manufactured component.',
 'No purchase, supplier contact, software installation, fabrication or physical test occurred. This is one mechanical review package with substantial detailing completed, NOT a claim that every engineering input or construction release is complete.']:
    y=para(30,y,t)
for p in panels:
    start(p['id']+' / current panel geometry')
    scale=min(360/p['w'],345/p['h']);x0,y0=55,105;c.setStrokeColor(HexColor('#2f4c5b'));c.setLineWidth(.55);circles=[]
    for e in p['edges']:
        if e['type']=='circle':
            u,v=e['center'];c.circle(x0+u*scale,y0+v*scale,e['radius']*scale);circles.append((u,v,e['radius']*2))
        else:c.line(x0+e['a'][0]*scale,y0+e['a'][1]*scale,x0+e['b'][0]*scale,y0+e['b'][1]*scale)
    text(x0,78,f"{p['w']:.2f} x {p['h']:.2f} x {p['t']:.2f} mm / qty1",10)
    y=para(440,490,'Local '+p['axes']+' axes; lower-left datum. Circle list: (x,y), diameter in mm. Same-name DXF supplied. Geometry only, not toleranced cutting approval.',365)
    for j,(u,v,d) in enumerate(sorted(circles,key=lambda x:(x[2],x[0],x[1]))):
        text(440+(j%2)*184,y,f'({u:.2f}, {v:.2f}) dia {d:.2f}',8)
        if j%2:y-=14
    assert y>65,(p['id'],y)
c.save();pdf=pdfium.PdfDocument(O/'AQI_D01_MECHANICAL_PACKAGE.pdf')
for i,p in enumerate(pdf):p.render(scale=1).to_pil().save(O/f'page-{i+1:02d}.png')
for first in range(0,len(pdf),3):
    contact=Image.new('RGB',(842,595*min(3,len(pdf)-first)),'white')
    for j in range(min(3,len(pdf)-first)):contact.paste(Image.open(O/f'page-{first+j+1:02d}.png'),(0,595*j))
    contact.save(O/f'inspection-{first//3+1}.png')
print('Mechanical PDF pages:',len(pdf),'Guard holes per face:',len(holes),'Area m2:',area)
