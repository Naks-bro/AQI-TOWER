"""One current-review package: actual CAD-derived panels, inventory and pressure budget."""
import json,csv,hashlib,zipfile
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
import pypdfium2 as pdfium
from PIL import Image
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/current_handoff';G=R/'reports/prototype_d01/r02_guards'
a=json.loads((O/'assembly_audit.json').read_text());panels=json.loads((O/'current_panels.json').read_text())
p=json.loads((O/'CURRENT_PRESSURE_BUDGET.json').read_text());rows=[r for r in p['rows'] if r['assumed_reducer_K']==1]
gates=[
['M','Mechanical closure','OPEN','Our remaining design: complete guard seams/rivets, cabinet/fan/M5 fastening stacks, seal compression and cable enclosure detail; review loads, tipping and access. Actual material/part fit and assembly inspection must follow.'],
['E','Electrical closure','OPEN','Our remaining design: selected protective isolation/restart arrangement and exact connector/cable layout. Qualified review and physical commissioning required. Present Noctua speed-control chain is NOT restart protection.'],
['P','Performance evidence','OPEN','Exact filter pressure/seal evidence is missing. Determine clean/loaded resistance and assembled flow; then run controlled indoor trials. Internet research or further CAD cannot substitute for measurements when public data are absent.']]
with (O/'BUILD_GATES.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['id','gate','status','required_work']);w.writerows(gates)
noncad=[
['FAN',4,'ARCTIC P14 Max','OEM family reference','Delivered revision/SKU, current/startup and compatibility not released'],
['FILTER',2,'IKEA STARKVIND104.633.30','OEM envelope370x290x40','Custom use experimental, OEM STARKVIND-only; resistance/landing unknown; no HEPA/MERV claim'],
['POWER',1,'Noctua NV-PS1 and included NA-AC10','OEM reference12V2A','India plug/availability and installed startup/protection unverified'],
['SPEED',1,'Noctua NA-FC1','OEM reference manual PWM','Does not implement restart inhibit'],
['HUB',1,'Noctua NA-FH1','OEM reference4-pin input;4 outputs used','SATA unused; cable and protection review pending'],
['PROTECTION','TBD','Isolation, stop/restart and protective access hardware','UNSELECTED','Safety design incomplete; no invented terminal assignment'],
['SEALS','TBD','Joint sealant, perimeter/fan/penetration seals','ASSUMED envelopes only','Products, compression, aging and leakage not selected/tested'],
['GUARD_JOIN','TBD','Guard corner/face joints and bracket rivets','UNMODELED/UNRELEASED','Rivet grip/heads, seams and capacity need completion'],
['HARDWARE','TBD','Remaining cabinet/fan/M5 nuts, washers and retained ends','PARTLY MODELED','Do not mistake all shaft envelopes for complete installed fasteners'],
['ENCLOSURE',1,'External control housing, glands and strain relief','RESERVATION ONLY','Part/layout, thermal and ingress details unresolved'],
['TEST',1,'Airflow/pressure/power/noise and indoor particle trial equipment/service','NOT OBTAINED','Buy/rent or paid operator; no college lab assumed'],
['REVIEW',1,'Scoped mechanical and electrical review/commissioning','NOT ENGAGED','ENTC friend not assumed; qualified physical work required']]
with (O/'COMPONENT_AND_MISSING_ITEMS.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['id','qty','item','evidence','release_gap']);w.writerows(noncad)
c=canvas.Canvas(str(O/'AQI_D01_CURRENT_REVIEW_PACKAGE.pdf'),pagesize=(842,595));page=0
def text(x,y,s,size=11,color='#243746'):
    c.setFillColor(HexColor(color));c.setFont('Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,w,size=11):
    for line in simpleSplit(s,'Helvetica',size,w):text(x,y,line,size);y-=size*1.4
    return y-12
def start(title):
    global page
    if page:c.showPage()
    page+=1;text(30,568,'AQI TOWER / CURRENT R02G ASSEMBLY / 03 OCT 2026',10,'#008579')
    text(30,536,title,22)
    text(30,18,'REVIEW ONLY - NOT A BUILD/BUY/ENERGIZATION RELEASE | Physical prototypes: 0',9)
    text(794,18,str(page),9)
start('One prototype. One current handoff.')
c.drawImage(str(G/'D01_ASSEMBLY.png'),20,82,width=475,height=388)
y=486
for s in ['Purpose: build our own small indoor particle-filtering demonstrator before attempting a large outdoor tower.',
 'This package consolidates the latest assembly, matching panel geometry, all CAD objects, component gaps and a current pressure budget. It does not restart the design.',
 'What exists:245 valid CAD objects,10 panel drawings extracted from the saved assembly and29,116 checked part pairs without modeled collisions.',
 'What does not exist: a built or tested machine, a verified airflow rating, or a construction-ready safety release.',
 'The honest endpoint: mechanical and electrical closure allow construction; commissioning and measured results allow demonstration. Three gates remain, not an endless sequence of cosmetic revisions.']:
    y=para(510,y,s,295)
start('Current pressure budget: what the fans can tolerate')
y=para(30,492,'This is a conditional calculation, NOT predicted airflow. Four fans share flow; each of the two filters carries half the total. Filter resistance is unknown and is not filled in with an invented curve.',780)
headers=['Total m3/h','Each filter','Fan Pa','Other losses Pa','Filter allowance Pa']
xs=[35,185,335,470,645]
for x,h in zip(xs,headers):text(x,y,h,11,'#008579')
y-=27
for r in rows:
    for x,v in zip(xs,[r['total_m3h'],r['each_filter_m3h'],r['fan_available_Pa'],r['nonfilter_total_Pa'],r['filter_allowance_Pa']]):text(x,y,f'{v:.2f}')
    y-=28
y=para(30,y-10,'At300 m3/h total, the assumed losses leave14.61 Pa for ONE filter path at150 m3/h. A filter needs to stay below the allowance with a justified margin to support that target. At400 m3/h, these assumptions leave no pressure for filters. Neither is a measured result.',780)
y=para(30,y,'Included: plenum, both guards, installation allowance and a new reducer-path allowance. Assumed K=1 is shown; CSV also includes0.5 and2. Guard open area0.036 m2 each; reducer opening0.0945 m2 per parallel path. Full2800 rpm, equal sharing, no bypass and all loss coefficients are unverified.',780)
para(30,y,'OEM numeric fan curve and brochure disagree; this table uses the numeric source without averaging. Existing historical flow predictions are not reused as the current filter result. Eight arithmetic checks pass; source and input hashes are recorded.',780)
start('Power and controls: exact boundary of current work')
labels=['OEM external\n12 V supply','NA-AC10\nconnector','NA-FC1\nspeed control','NA-FH1 hub\n4-pin input','4 x P14 Max\nparallel outputs']
for i,label in enumerate(labels):
    x=30+i*160;c.setStrokeColor(HexColor('#008579'));c.rect(x,391,140,70)
    for j,line in enumerate(label.split('\n')):text(x+9,435-j*17,line,11)
    if i<4:c.line(x+140,426,x+160,426)
y=para(30,357,'FUNCTIONAL OEM REFERENCE CHAIN ONLY. No wire colours, terminal assignments or protective-circuit ratings are inferred. SATA hub input remains unused. A speed knob or zero-speed command is not service isolation.',780)
y=para(30,y,'Nominal fan load:4 x0.35 A =1.4 A, or16.8 W at12 V; supply reference2 A/24 W. The nominal difference is not a startup/current/protection approval. Controller overhead, cable losses, startup, delivered revision and fan behavior remain unverified.',780)
y=para(30,y,'MISSING PROTECTIVE FUNCTION: the pictured chain does not implement the existing manual-restart/protective-access requirements. Their reviewed hardware arrangement, isolation method, cable restraint and enclosure must be completed before energization. The laptop is for logging, not safety control.',780)
para(30,y,'Physical checks must cover the approved protection/connector arrangement, abnormal and power-restoration behavior, fan run-down, guards, strain relief and applicable electrical tests. Do not perform improvised live-fault tests. Optional ENTC help is not assumed.',780)
start('Finite critical path and funding request')
y=490
for gid,name,status,body in gates:
    text(30,y,gid+' / '+name+' - '+status,14,'#008579');y=para(30,y-25,body,780)
y=para(30,y,'Digital work: finish the identified mechanical/electrical interfaces and recheck one assembly. External work: authorized sample procurement, fabrication, qualified review and commissioning, then measured trials. These dependencies may overlap; delivery/workshop dates and total funding are UNKNOWN.',780)
para(30,y,'Funding request: staged support for verified parts/samples, panel and guard fabrication, scoped safety review, assembly and rented/paid measurement. First success criterion is a safely commissioned guarded assembly with recorded flow, pressure and power; then repeatable indoor particle trials. No guaranteed completion date, cost, cleaning percentage or outdoor radius is claimed.',780)
start('Build review map: do not combine old revisions')
y=490
for s in ['CURRENT: D01_R02G_ASSEMBLY.FCStd and STEP are the assembly authority. Ten flat-panel drawings on the following pages come from actual current CAD faces; their area x thickness was checked against solid volume.',
 'DRAWINGS: each face is shown in global-axis orientation with its local lower-left datum. Circles are identified by local coordinates. DXF units are mm. These are geometric review outputs, not kerf-compensated or tolerance/strength-approved cutting files.',
 'PARTS: CAD_PART_INVENTORY.csv lists every current modeled object. COMPONENT_AND_MISSING_ITEMS.csv adds OEM references, unmodeled hardware, seals, controls and services. A CAD object is not necessarily a purchased part; do not order245 items from that number.',
 'UNCHANGED LIMITS: excluded from collision checks are reservation envelopes and guard-to-guard seams. Filter pleats and guard perforations in renders are visual annotations. Physical sealing, real material properties, forces, reach and stability remain unverified.',
 'SOURCES: IKEA STARKVIND104.633.30 is an experimental custom-fit envelope, not an OEM-approved purifier application. No HEPA/MERV class is assigned to this assembly. ARCTIC numeric curve and Noctua power-chain references are linked in README; do not distribute their OEM documents as our licensed design.',
 'NO-LAB ROUTE: funded local cutting/assembly and qualified commissioning, with bought/rented instruments or a paid measurement service. No college workshop or optional friend is on the critical path. Physical prototypes remain0.']:
    y=para(30,y,s,780)
for p1 in panels:
    start(p1['id']+' / current CAD face')
    sc=min(365/p1['w'],350/p1['h']);x0,y0=55,100
    c.setStrokeColor(HexColor('#294b5c'));c.setLineWidth(.55)
    circles=[]
    for e in p1['edges']:
        if e['type']=='circle':
            u,v=e['center'];c.circle(x0+u*sc,y0+v*sc,e['radius']*sc);circles.append((u,v,2*e['radius']))
        else:c.line(x0+e['a'][0]*sc,y0+e['a'][1]*sc,x0+e['b'][0]*sc,y0+e['b'][1]*sc)
    text(x0,y0-22,f"Width {p1['w']:.2f} mm; height {p1['h']:.2f} mm; thickness {p1['t']:.2f} mm",10)
    y=para(450,491,f"Quantity1. Local axes {p1['axes']}; origin at lower-left of projected CAD bounding box. Same-name DXF supplied. Opposite-side parts are separate drawings, not assumed identical.",355)
    y=para(450,y,'Circle centres and diameters (mm):',355)
    if not circles:y=para(450,y,'None. See outline/openings in DXF.',355)
    for j,(u,v,d) in enumerate(sorted(circles,key=lambda p:(p[2],p[0],p[1]))):
        text(450+(j%2)*180,y,f'({u:.2f}, {v:.2f}) dia {d:.2f}',8)
        if j%2==1:y-=14
    if len(circles)%2:y-=14
    assert y>70,(p1['id'],y)
    para(450,60,'Nominal geometry only. Material, tolerances, seams and strength NOT released.',355,9)
c.save();pdf=pdfium.PdfDocument(O/'AQI_D01_CURRENT_REVIEW_PACKAGE.pdf')
for i,page_obj in enumerate(pdf):page_obj.render(scale=1).to_pil().save(O/f'page-{i+1:02d}.png')
for first in range(0,len(pdf),3):
    contact=Image.new('RGB',(842,595*min(3,len(pdf)-first)),'white')
    for j in range(min(3,len(pdf)-first)):contact.paste(Image.open(O/f'page-{first+j+1:02d}.png'),(0,j*595))
    contact.save(O/f'inspection-{first//3+1}.png')
print(f'Generated {len(pdf)} pages, gates and component/missing-item registers.')
