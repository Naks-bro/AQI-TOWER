"""R01 detail sheets, generated from the same revised assembly; retain R00 report."""
import json,math,ast,csv,hashlib,zipfile
from pathlib import Path
import numpy as np
from PIL import Image,ImageColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,white
from reportlab.lib.pagesizes import A4,landscape,A3
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2];B=R/'reports/prototype_d01';O=B/'r01'
M=json.loads((O/'cad_mesh.json').read_text());GUARD_RIM_MM=10
# Reuse precisely the existing renderer function without executing its R00 report builder.
tree=ast.parse((R/'scripts/reports/build_d01_delivery.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='render')
exec(compile(ast.Module(body=[fn],type_ignores=[]),'d01_shared_renderer','exec'),globals())
render()
pdfmetrics.registerFont(TTFont('UI','C:/Windows/Fonts/segoeui.ttf'));pdfmetrics.registerFont(TTFont('UIB','C:/Windows/Fonts/segoeuib.ttf'))
pdf=canvas.Canvas(str(O/'D01_R01_CONSTRUCTION_DETAILS.pdf'),pagesize=landscape(A3));pdf.setTitle('D01 R01 construction details')
INK='#203848';TEAL='#007e79';AMBER='#91601c';PALE='#edf3f4';page=0;pw,ph=landscape(A3)
def txt(x,y,t,size=11,b=False,col=INK):pdf.setFillColor(HexColor(col));pdf.setFont('UIB' if b else 'UI',size);pdf.drawString(x,y,t)
def par(t,x,y,w,size=11,col=INK):
    a=Paragraph(t,ParagraphStyle('p',fontName='UI',fontSize=size,leading=size*1.4,textColor=HexColor(col)));_,h=a.wrap(w,9999);a.drawOn(pdf,x,y-h);return y-h-14
def start(title,sub=''):
    global page
    if page:pdf.showPage()
    page+=1;txt(38,ph-30,'AQI TOWER  /  D01-R01  /  SAME ASSEMBLY, CONSTRUCTION DETAIL REVISION',9,True,TEAL)
    txt(38,ph-65,title,24,True);par(sub,38,ph-85,pw-76,11)
    txt(38,22,'DESIGN REVIEW ONLY - NOT RELEASED FOR CUTTING, PURCHASE OR ENERGIZING',9,col=AMBER);txt(pw-65,22,str(page),9)
def table(rows,widths,x,y,size=10):
    ps=ParagraphStyle('c',fontName='UI',fontSize=size,leading=size*1.3)
    t=Table([[Paragraph(str(v),ps) for v in row] for row in rows],colWidths=widths)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#dcebea')),('GRID',(0,0),(-1,-1),.4,HexColor('#d0dade')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]));_,h=t.wrap(9999,9999);assert y-h>45;t.drawOn(pdf,x,y-h);return y-h-18
def rect(x,y,w,h,fill=PALE):pdf.setFillColor(HexColor(fill));pdf.setStrokeColor(HexColor(INK));pdf.setLineWidth(.6);pdf.rect(x,y,w,h,fill=1)
def dim(x,y,X,Y,label):
    pdf.setStrokeColor(HexColor(INK));pdf.setLineWidth(.5);pdf.line(x,y,X,Y)
    if y==Y:
        for xx in (x,X):pdf.line(xx,y-4,xx,y+4)
        txt((x+X)/2-18,y+6,label,9)
    else:
        for yy in (y,Y):pdf.line(x-4,yy,x+4,yy)
        pdf.saveState();pdf.translate(x-8,(y+Y)/2);pdf.rotate(90);txt(-10,0,label,9);pdf.restoreState()
start('The prototype now has attachment details','R01 continues D01. It preserves the fan/filter arrangement and adds joints, support hardware and a cable-routing reservation.')
pdf.drawImage(str(O/'D01_ASSEMBLY.png'),38,100,width=670,height=547)
y=690
for title,body in [('Guard attachment','Eight angle brackets and four shared through-bolts connect both guards to the fan plate. Rivet-hole patterns are drilled in the actual CAD.'),('Cabinet joints','Thirty-two M4 through-bolt locations connect the end and filter-seat panels to the corner cleats. Top/base retention uses eight proposed timber screws.'),('Filter support','Eight metal angles support the four ledges. Shelf hardware is kept below the filter seating surface; flush screw-head detailing remains required.'),('Cable routing','An external route is reserved from the right guard wall to the control box. It is not an approved cable-gland hole or completed electrical circuit.')]:
    txt(755,y,title,15,True,TEAL);y=par(body,755,y-20,380,12)-17
par('CHECKED: 163 valid objects and zero nominal overlaps in 12,675 tested pairs. Reservations and inherited guard seams are excluded. These checks do not establish strength, finger protection, sealing or physical performance.',755,y,380,11,AMBER)
start('G03 Guard bracket and bolt section','Dimensions mm. Proposed angle material/grade, rivet grip and exact fasteners remain unselected. All dimensions are nominal.')
# Enlarged x-z section through left guard mount; y=60. Real coordinates mapped consistently.
sx,sz,scale=95,550,6;ox,oy=110,225
def section(x,z,w,h,col=PALE):rect(ox+(x-sx)*scale,oy+(z-sz)*scale,w*scale,h*scale,col)
section(95,571,55,9);section(95,580,20,2,'#93adb8');section(113,582,2,18,'#93adb8')
section(95,569,20,2,'#93adb8');section(113,551,2,18,'#93adb8');section(115,580,1,50,'#b7c9cc');section(115,530,1,41,'#b7c9cc')
section(103,558.6,4,25,'#406273');section(101.5,583.6,7,4,'#406273')
section(100.5,582,9,1.6,'#b3bdc4');section(100.5,567,9,1.6,'#b3bdc4');section(101,563.8,8,3.2,'#406273')
txt(475,oy+26*scale,'Fan plate z571-580',12,True);txt(285,oy+59*scale,'Outer guard wall',11);txt(285,oy-6*scale,'Inner guard wall',11)
dim(ox,oy-60,ox+120,oy-60,'20');dim(ox-25,oy+30*scale,ox-25,oy+50*scale,'20')
y=700
y=table([['Feature','Dimension / location'],['Each bracket','20 x20 x2 equal angle;40 long. Eight pieces. Nominal sharp corner; actual root fillet must fit.'],['Guard bolt pattern','Four dia4.5 holes through fan plate: x105/445 and y60/300. M4x25 proposed with two washers and a locknut.'],['Bracket foot hole','10 from free transverse edge;20 from length end. Hole dia4.5.'],['Skirt rivets','Two dia3.5 holes per bracket:10 and30 from length end. Outer z590; inner z560. Sixteen proposed3.2 rivets; grip stack3mm nominal.'],['Guard face','320 square with10 solid rim;300 square perforated field.4mm holes /6mm triangular pitch proposal. No holes cut into CAD sheet envelope.'],['Cage seams','Continuous closed joints of face-to-skirt and skirt corners, by shop-approved process for selected metal. No loose edges. Actual weld/formed joint design not released.']],[120,415],615,y,11)
par('The lower washer has0.4mm nominal take-up in this envelope. Select the real washers and locknut, then verify engagement and tool clearance. The shared bolts mean removing the top guard can loosen the lower guard: support both and isolate power before service. No independent-access safety claim.',615,y,535,11,AMBER)
start('J01 Cabinet drilling and retention','Assembly coordinates: x from left; y from front seat; z from floor. No holes may be located by scaling this PDF.')
schedule=json.loads((O/'fastener_schedule.json').read_text())
rows=[['Joint','Count / proposed hardware','Coordinates and assembly detail']]
for s in schedule[2:4]+schedule[5:6]:rows.append([s['group'],str(s['quantity'])+' / '+s['size'],s['locations']+'<br/>'+s['note']])
y=table(rows,[210,300,595],38,ph-125,12)
# Front panel hole map, includes new joints as green dots and old clamp holes gray.
xx,yy,sc=95,110,.62;rect(xx,yy,532*sc,542*sc);rect(xx+31*sc,yy+41*sc,470*sc,470*sc,'#ffffff')
for x in (11,521):
    for z in (126,226,326,426):pdf.setFillColor(HexColor(TEAL));pdf.circle(xx+x*sc,yy+z*sc,3,fill=1)
for x,z in [(a,b) for a in (11,521) for b in (26,276,526)]+[(266,21),(266,531)]:pdf.setFillColor(HexColor('#7e8990'));pdf.circle(xx+x*sc,yy+z*sc,2.75*sc,fill=1)
txt(xx,yy+542*sc+18,'Seat panel - green = new cabinet joints',12,True);dim(xx,yy-20,xx+532*sc,yy-20,'532')
y=415
y=par('<b>Assembly order</b><br/>Dry-fit the base, panels and cleats square. Drill the through-joints using the panel datums; deburr and protect the edges. Fit washers and locking nuts on the internal side. Confirm the cabinet diagonals before tightening.',530,y,610,12)
y=par('<b>Top and bottom</b><br/>Top screws4 x20 and base screws4 x25 are layout proposals, not a verified timber connection. Pilot diameter, screw type and end-grain holding strength must follow the selected wood and fastener data. No handles or lifting points are released: support the base when moving.',530,y,610,12)
par('<b>Sealing</b><br/>Use compatible cured sealant on permanent seams. Proposed removable top seam uses externally applied, removable foil HVAC tape; product and adhesion are unverified. No new top gasket thickness is inserted silently into the CAD. Seal all penetrations and physically check for bypass.',530,y,610,12,AMBER)
start('M09 Filter ledge support','Each filter rests on two235mm ledges. Two metal angles support each ledge: eight brackets total.')
rect(95,390,450,55,'#d5dfdf');rect(325,390,20,55,'#ffffff')
for x in (130,235,375,480):rect(x,350,45,40,'#94aeb9')
txt(100,470,'Front ledge layout - schematic',15,True);txt(298,365,'20 gap',10);dim(95,500,325,500,'235');dim(345,500,545,500,'235')
y=690
y=table([['Feature','Coordinates / dimensions'],['Bracket','25 x25 x2 equal angle,30 long. Four per filter. Nominal sharp bend; actual extrusion root fillet and edge condition must fit.'],['Bracket x positions','Segments60-90,200-230,320-350,460-490. Fastener centres75,215,335,475.'],['Seat attachment','M4x20 proposal; dia4.5 at z37. Front and rear seat holes correspond. Washers/nut retention to be detailed.'],['Ledge attachment','M3x20 proposal through dia3.5 at y-15 (front) or375 (rear), at the four x centres. Head must be flush at/below z57.35.'],['Load path','Filter frame -> plywood ledge -> angle -> seat bolt/panel -> cabinet/base. Do not rely on filter clamping friction to carry weight.']],[145,425],600,y,12)
par('Do not blindly countersink thin plywood: match the actual head, verify remaining material and check that the filter sits flat. The clamp studs, shelf fasteners and guard mounts were checked together in the same CAD.',600,y,570,12,AMBER)
load=json.loads((O/'load_screening.json').read_text())
table([['Conditional load arithmetic - NOT a structural pass','Result'],['Guard bracket example:50N on one bracket,10mm arm;40mm wide x2mm strip. sigma = F L / (b t^2 /6).','18.75 MPa nominal'],['Shelf example:assumed2kg filter x2 handling factor, all load on one bracket,25mm arm;30mm wide x2mm strip.','49.05 MPa nominal'],['Missing before a strength judgement','Actual material allowable, bend/holes, connection bearing/pull-out, load distribution, guard flexure and abuse cases. These assumed loads are not compliance tests.']],[750,355],38,270,11)
start('E02 Cable route and revised pressure','The electrical architecture is unchanged. This sheet reserves a route; it does not release a gland, wiring or restart protection.')
rect(70,455,330,110);txt(90,530,'Four fans inside guarded top',15,True)
pdf.setStrokeColor(HexColor('#b28b3c'));pdf.setLineWidth(5);pdf.line(400,510,535,510);pdf.line(535,510,535,395)
rect(495,310,150,85,'#d7ece6');txt(507,345,'Control reservation',12,True);txt(415,532,'130mm',10);txt(547,440,'105mm',10)
par('Amber route: proposed12mm-diameter corridor. No12mm guard hole is authorized. Select a closed-entry gland/connector and cable restraint that preserve the guard. OEM fan leads may need extensions after internal routing and service loops are measured.',70,280,550,12,AMBER)
y=700
y=par('<b>Actual work still needed</b><br/>Confirm the third-party fan/controller chain, cable reach, connector retention, enclosure mounting and actual socket/plug arrangement. The control chain still lacks the required manual restart after power restoration. No safety function is assigned to the laptop or monitoring code.',700,y,440,12)
pressure=json.loads((O/'pressure_results.json').read_text())
y=table([['Guard change','R01 assumption'],['Perforated field','300 x300mm inside a320mm face'],['Free area per face','0.036m2 assuming40% field porosity'],['Whole-face open fraction','35.15625%, previously40%'],['Calculated flows, low / middle / loaded', ' / '.join(f"{s['flow_m3h']:.1f}" for s in pressure['scenarios'])+' m3/h']],[200,250],700,y,11)
par('These are screening scenarios, not measured ratings. The new guard border raises the calculated resistance; R00 airflow numbers no longer apply unchanged. Exact filter curve, guard loss coefficient and installation effects remain unknown. No CADR or outdoor coverage follows.',700,y,440,12,AMBER)
par('<b>Release boundary</b><br/>Detailed geometry now exists for the attachments. Exact products/materials, joint strength, guard manufacture/reach, seal compression/leakage, mass/stability, cable entry and restart protection still need closure. Physical prototypes built:0. No supplier contacted, purchase or installation made.',38,150,1105,12)
pdf.save()
qa=O/'qa';qa.mkdir(exist_ok=True);p=pdfium.PdfDocument(str(O/'D01_R01_CONSTRUCTION_DETAILS.pdf'))
for i in range(len(p)):p[i].render(scale=1.1).to_pil().save(qa/f'page-{i+1}.png')
with (O/'FASTENERS_R01.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(schedule[0]));w.writeheader();w.writerows(schedule)
with (B/'D01_BOM.csv').open(encoding='utf-8-sig',newline='') as f:bom=list(csv.DictReader(f))
for row in bom:
    if row['ID']=='G01-02':row['Technical basis' if 'Technical basis' in row else 'basis']='320 square faces;10mm solid rim,300 square perforated field; external50/inner41 skirt height'
    if row['ID']=='H03':row.update(product_or_item='Remaining seam sealant, top seam tape and small fittings',basis='Detailed fastenings now separately itemized below',status='Exact sealant/tape/fittings unselected; do not double-count R01 fasteners')
for ident,qty,item,basis in [
('G03','8','20x20x2 angle segments,40mm long','Guard brackets; material/fillet to confirm'),
('H03A','4 sets','M4x25 bolts +8 washers +4 locknuts','Guard through-clamps; washer/nut envelopes only'),
('H03B','16','Nominal3.2mm rivets','Grip for3mm stack; exact product/head retention unknown'),
('H06-07','32 sets','M4x40 bolts +64 washers +32 locknuts','Cabinet through-joints; strength/bearing unverified'),
('M09','8','25x25x2 angle segments,30mm long','Filter ledge supports; material/fillet unknown'),
('H08','8 sets','M4x20 bolts +16 washers +8 locknuts','Shelf-angle to seat; actual stack to verify'),
('H09','8 sets','M3x20 flush screws +8 washers +8 locknuts','Ledge to angle; actual countersink/head geometry unresolved'),
('H10','8','4 top4x20 and4 base4x25 timber screws','Layout only; exact screw/pilot/end-grain capacity unresolved')]:
    bom.append(dict(ID=ident,quantity=qty,product_or_item=item,basis=basis,status='PROPOSED - NOT RELEASED OR ORDERED'))
with (O/'BOM_R01.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(bom[0]));w.writeheader();w.writerows(bom)
files=[p for p in O.iterdir() if p.is_file() and p.suffix.lower() in ('.md','.pdf','.fcstd','.step','.png','.json','.csv') and p.name!='MANIFEST.json']+list((O/'panel_dxf_REVIEW_ONLY').glob('*.dxf'))
files += [R/s for s in ['scripts/geometry/detail_d01_r01.py','scripts/analysis/d01_r01_checks.py','scripts/analysis/d01_pressure.py','scripts/reports/build_d01_r01.py','scripts/reports/build_d01_delivery.py','cad/parametric/d01_r00.json']]
files += [B/s for s in ['D01_ASSEMBLY.FCStd','cad_mesh.json','panel_geometry.json','D01_BOM.csv','README.md','AQI_D01_ENGINEERING_PACKAGE.pdf']]
manifest={'revision':'D01-R01','release':'REVIEW ONLY','files':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
(O/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(R/'reports/AQI_D01_R01_REVIEW_PACKAGE.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files+[O/'MANIFEST.json']:z.write(p,p.relative_to(R))
print(json.dumps({'pages':page,'pdf':str(O/'D01_R01_CONSTRUCTION_DETAILS.pdf')}))
