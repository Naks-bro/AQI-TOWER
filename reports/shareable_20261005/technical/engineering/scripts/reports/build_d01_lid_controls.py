"""Two-page E04 lid layout and ordinary-input schematic from checked CAD evidence."""
from pathlib import Path
import csv,json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/electrical_package/control_module'
d=json.loads((O/'LID_CONTROL_CHECKS.json').read_text())
assert not d['release'] and d['native_tower_unchanged'] and d['objects']==18
c=canvas.Canvas(str(O/'D01_E04_LID_CONTROLS_REVIEW.pdf'),pagesize=(842,595),invariant=1)
c.setTitle('D01 E04 proposed lid controls and ordinary input circuit')
navy=HexColor('#153d4c')
sty=ParagraphStyle('body',fontName='Helvetica',fontSize=9,leading=12,textColor=navy)
def label(t,x,y,size=9):
 c.setFillColor(navy);c.setFont('Helvetica',size);c.drawString(x,y,t)
def para(t,x,y,w):
 p=Paragraph(t,sty);_,h=p.wrap(w,500);assert y-h>42;p.drawOn(c,x,y-h);return y-h-8
def header(t,n):
 c.setFillColor(navy);c.rect(0,522,842,73,fill=1,stroke=0)
 c.setFillColor(HexColor('#79e1cc'));c.setFont('Helvetica-Bold',9);c.drawString(30,572,'AQI TOWER / D01 R03M / E04 LID CONTROLS / 5 OCTOBER 2026')
 c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',20);c.drawString(30,544,t)
 c.setFillColor(HexColor('#ac2947'));c.setFont('Helvetica-Bold',8);c.drawString(30,23,'PROPOSED / NO DRILLING, WIRING OR ENERGIZATION RELEASE');c.drawRightString(812,23,str(n))
def table(rows,widths,x,y):
 t=Table([[Paragraph(str(v),sty) for v in row] for row in rows],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e1efee')),('GRID',(0,0),(-1,-1),.4,HexColor('#b7ced2')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
 _,h=t.wrap(sum(widths),500);assert y-h>42;t.drawOn(c,x,y-h);return y-h-9
def dim(x,y,xx,yy,t):
 c.setStrokeColor(navy);c.line(x,y,xx,yy)
 if y==yy:
  c.line(x,y-4,x,y+4);c.line(xx,y-4,xx,y+4);label(t,(x+xx)/2-10,y+6,8)
 else:
  c.line(x-4,y,x+4,y);c.line(xx-4,yy,xx+4,yy);label(t,x+5,(y+yy)/2,8)
header('A closed lid with three clearly labelled controls',1)
cx,cy,s=255,331,1.35
c.setStrokeColor(navy);c.setFillColor(HexColor('#eff5f6'));c.roundRect(cx-150*s,cy-100*s,300*s,200*s,8,stroke=1,fill=1)
for b in d['buttons']:
 x=cx+b['centre_mm'][0]*s
 c.setStrokeColor(HexColor(b['color']));c.setFillColor(HexColor(b['color']));c.circle(x,cy,14.5*s,stroke=1,fill=1)
 label(b['name'],x-17,cy-37,10)
 c.setDash(3,3);c.rect(x-20*s,cy-20*s,40*s,40*s,stroke=1,fill=0);c.setDash()
 label(str(b['centre_mm'][0]),x-10,cy+40,8)
dim(cx-150*s,cy+112*s,cx+150*s,cy+112*s,'300 mm')
dim(cx-160*s,cy-100*s,cx-160*s,cy+100*s,'200')
dim(cx-15*s,cy-60*s,cx+45*s,cy-60*s,'60')
dim(cx+45*s,cy-60*s,cx+105*s,cy-60*s,'60')
label('Datum: box centre X/Y; proposed row Y=0; not a drilling template',45,174,8)
label('Dashed squares: ASSUMED 40 x 40 rear envelopes',45,158,8)
y=para('<b>Verified OEM mounting instruction:</b> BRU46063 page2 specifies22.3mm hole with +0.4/-0 tolerance;1-6mm panel range for these ordinary heads. Same-row minimum30mm; proposed60mm pitch exceeds this. Labels and installed accessories must still fit.',487,491,325)
y=para('<b>Detected in the private box STEP:</b> lid thickness4.0mm at all three proposed centres. It lies within the head mounting range. This does not establish delivered thickness, retention or ingress protection after drilling.',487,y,325)
y=para('<b>Assumed, not measured:</b> rear stack40x40x55mm below inner lid plus20mm wire-tail depth. All reservations clear the24 OEM box solids and three existing component bodies. Smallest combined reservation/body gap6.03mm.',487,y,325)
y=para('<b>Conflict found:</b> STOP/RESET wire-tail reservations overlap the hub and speed-controller <i>assumed service spaces</i>. No solid body clash, but cable routing/connector access is NOT closed. Keep these overlap results for review; do not claim full assembled fit.',487,y,325)
para('<b>Speed setting:</b> retain the unmodified internal NA-FC1 for now. Disconnect the external source before access; set speed, then close the lid before operation. Live adjustable external knob mounting is NOT designed. Ordinary STOP is not isolation.',487,y,325)
y=table([['Control','Candidate head / collar / contact','Centre X/Y mm','Function'],
 *[[b['name'],b['head']+' / ZB5AZ009 / '+b['contact'],str(b['centre_mm']),b['contact_type']+' spring-return'] for b in d['buttons']]], [85,325,125,245],30,136)
c.showPage();header('Ordinary input circuit - not a safety circuit',2)
label('PROPOSED PROTECTED +12 V CONTROL BRANCH - PROTECTION / TERMINALS UNSELECTED',35,491,10)
c.setStrokeColor(navy);c.line(65,458,65,308)
for i,b in enumerate(d['buttons']):
 y=445-i*60;c.line(65,y,190,y);c.circle(190,y,2,stroke=1,fill=0);c.circle(230,y,2,stroke=1,fill=0)
 if b['contact_type']=='NO':c.line(191,y,226,y+14)
 else:c.line(191,y,231,y);c.line(214,y-7,220,y+7)
 c.line(231,y,450,y);c.rect(450,y-18,310,36,stroke=1,fill=0)
 label(b['name']+' / '+b['contact_type'],270,y+10,9)
 label('Opta '+b['terminal']+' = '+b['firmware_pin']+' (DIGITAL INPUT)',463,y-3,11)
 label('Contact screw IDs intentionally omitted - not verified',35,288,8)
y=table([['Input state','Ordinary software interpretation'],
 ['START NO pressed / I1 HIGH','Request RUN only when existing logic permits. Held START cannot auto-restart.'],
 ['STOP NC healthy / I2 HIGH','Pressing STOP opens contact; LOW requests stop. This is NOT protective isolation.'],
 ['RESET NO pressed / I3 HIGH','Clear ordinary latched fault only when logic allows; does NOT itself start fans.'],
 ['Common / additional inputs','Opta negative shares reviewed source0V. I4 bench permit / I5 source present remain E02 references; not protective inputs.'],
 ],[205,575],30,270)
y=para('<b>OEM electrical facts:</b> Opta digital input0-24V, HIGH minimum6.6V, LOW maximum4.46V, impedance8.9kOhm,1.12mA at10V.12V/8.9kOhm =1.348mA is a nominal resistance screen only, not guaranteed current. Gold-flashed ZBE1016(NO) / ZBE1026(NC) are manufacturer-designated low-power contacts. Their numerical minimum switching range at our conditions remains UNKNOWN.',30,y,780)
y=para('<b>Bench-only status:</b> default sketch leaves every relay OFF; this circuit cannot yet operate the fans. No protective PR1 selected, no fan-power contact assignment, no fuses or wire sizes released. Verify contact minimum rating, terminal IDs, retention, source/branch protection, actual cables, service loop, heat and isolation before any dummy-load commissioning.',30,y,780)
para('<b>Primary sources checked5 Oct2026:</b> Schneider BRU46063 page2; Harmony catalogue DIA5ED2121213EN low-power contact table; Arduino Opta collective datasheet input specification. Full links in LID_CONTROL_CHECKS.json / README. OEM drawings/models are private research references, not redistributed. Physical prototypes0; unchanged R03M geometry.',30,y,780)
c.save()
with (O/'LID_CONTROL_PARTS.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Function','Head','Collar','Contact','Contact_type','Opta_terminal','Firmware_pin','Status'])
 for b in d['buttons']:w.writerow([b['name'],b['head'],b['collar'],b['contact'],b['contact_type'],b['terminal'],b['firmware_pin'],'CANDIDATE; low-current minimum and assembled rear fit unverified'])
doc=pdfium.PdfDocument(str(O/'D01_E04_LID_CONTROLS_REVIEW.pdf'));assert len(doc)==2
for i in range(2):doc[i].render(scale=1.4).to_pil().save(O/'previews'/f'E04_{i+1}.png')
print('E04 two-page drawing and candidate parts schedule written.')
