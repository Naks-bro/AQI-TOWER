"""Four-page E01 power/interface drawing supplement; no energization release."""
import csv
import importlib.util
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'reports/prototype_d01/electrical_package'
spec=importlib.util.spec_from_file_location('power',ROOT/'scripts/analysis/d01_electrical_closure.py')
power=importlib.util.module_from_spec(spec)
spec.loader.exec_module(power)
data=power.build()
(OUT/'POWER_COORDINATION.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
W,H=842,595
c=canvas.Canvas(str(OUT/'AQI_D01_POWER_AND_WIRING_SUPPLEMENT.pdf'),pagesize=(W,H),invariant=1)
c.setTitle('AQI D01 R03M power and wiring review E01')
navy=HexColor('#153d4c');teal=HexColor('#087e83');amber=HexColor('#ac6407');red=HexColor('#ac2947')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=14,textColor=navy)
small=ParagraphStyle('small',parent=style,fontSize=8.5,leading=11)
page=0


def text(s,x,y,width=750,smalltext=False):
    p=Paragraph(s,small if smalltext else style)
    _,h=p.wrap(width,480)
    assert y-h>42,(page,s[:40],y,h)
    p.drawOn(c,x,y-h)
    return y-h-9


def new(title,sub):
    global page
    if page:c.showPage()
    page+=1
    c.setFillColor(navy);c.rect(0,H-91,W,91,fill=1,stroke=0)
    c.setFillColor(HexColor('#6ce0cb'));c.setFont('Helvetica-Bold',9);c.drawString(36,H-26,'AQI TOWER / D01 R03M / E01 SUPPLEMENT / 5 OCTOBER 2026')
    c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',21);c.drawString(36,H-57,title)
    c.setFont('Helvetica',9);c.drawString(36,H-76,sub)
    c.setFillColor(red);c.setFont('Helvetica-Bold',8);c.drawString(36,24,'REVIEW DRAWING ONLY — NOT RELEASED FOR ORDERING, WIRING OR ENERGIZATION')
    c.drawRightString(W-36,24,str(page))


def box(x,y,w,h,label,openpart=False):
    c.setFillColor(HexColor('#fff0dc' if openpart else '#e5f4f0'))
    c.setStrokeColor(amber if openpart else teal)
    c.roundRect(x,y,w,h,5,fill=1,stroke=1)
    p=Paragraph(label,small);_,height=p.wrap(w-16,h-8)
    assert height<h-8
    p.drawOn(c,x+8,y+(h-height)/2)


def link(x1,y1,x2,y2,color=teal,dashed=False):
    c.setStrokeColor(color);c.setLineWidth(1.5);c.setDash(4,3) if dashed else c.setDash()
    c.line(x1,y1,x2,y2);c.setDash()


def table(headers,rows,widths,y):
    cells=[[Paragraph(str(v),small) for v in row] for row in [headers]+rows]
    t=Table(cells,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#d5ece8')),('GRID',(0,0),(-1,-1),.4,HexColor('#b6ccd0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    _,height=t.wrap(770,480)
    assert y-height>45,(page,height,y)
    t.drawOn(c,36,y-height)
    return y-height-14


new('One power path, four fan branches','OEM reference connectors are named; amber functions are unselected. No bridge across PR1 is permitted.')
box(36,391,135,72,'<b>PS1 / NV-PS1</b><br/>External Class II adapter<br/>12 V / 2 A / 24 W')
box(197,391,101,72,'<b>J02 / NA-AC10</b><br/>OEM supplied<br/>barrel-to-4-pin')
box(324,383,169,88,'<b>PR1 / OPEN DESIGN</b><br/>Service isolation + run permission + restart inhibition<br/>No rated circuit selected',True)
box(519,391,118,72,'<b>SC1 / NA-FC1</b><br/>Speed control only<br/>3 A maximum')
box(664,391,142,72,'<b>H1 / NA-FH1</b><br/>4-pin input: 24 W<br/>SATA NOT USED')
for x1,x2 in [(171,197),(298,324),(493,519),(637,664)]:link(x1,427,x2,427,dashed=x1 in (298,493))
text('Site mains stays outside the prototype cabinet. Actual socket, upstream protection and plug suitability require site review. Keep OEM adapter unmodified.',36,370,770)
for i in range(4):
    x=36+i*198
    box(x,226,175,66,f'<b>F{i+1} / P14 Max</b><br/>ACFAN00287A<br/>12 V; published current 0.35 A')
    link(735,391,735,325)
    link(x+87.5,325,735,325)
    link(x+87.5,325,x+87.5,292)
    c.setFillColor(teal);c.setFont('Helvetica',8);c.drawString(x+92,304,f'H1 port {i+1}')
y=text('<b>OEM interfaces:</b> SC1 output to H1 4-pin input using compatible OEM cable; H1 ports1–4 to individual fans. Lines represent connector-level power/control bundles, NOT conductor routing or plug orientation. PR1 insertion would require a designed compatible harness; no OEM cable should be cut to implement this sketch.',36,207,770)
y=text('<b>Only F1 RPM is forwarded upstream.</b> Other port LEDs are local indications, not independent safety outputs. Do not tie tach outputs together. A lamp or zero PWM does not prove isolation or standstill.',36,y,770)
text('<b>Release hold:</b> the pictured OEM chain alone does not implement the required STOP / deliberate RESET / fresh START behavior. PR1, cable entry, enclosure, conductor protection and all physical connections remain unreleased.',36,y,770)

new('Load and thermal constraints','Catalogue limits are verified. Startup multipliers and auxiliary loads below are illustrative assumptions.')
y=table(['Path item','Published limit / value','Engineering interpretation'],[
    ['Four P14 Max fans','4 x 0.35 A = 1.40 A; 16.8 W at12 V','Published fan current; not measured startup or guaranteed maximum draw'],
    ['NV-PS1 external adapter','12 V; 2 A /24 W','Governs current together with selected hub input'],
    ['NA-FC1 speed controller','3 A /36 W maximum','Rating is NOT its own consumption; auxiliary load unknown'],
    ['NA-FH1 selected input','24 W via4-pin; 2 A at12 V','54 W SATA rating does NOT apply to this path'],
    ['Temperature','Fans0–40 C; adapter0–40 C; hub-40–60 C','Controller/enclosure environment unresolved. Not whole-device outdoor approval'],
], [145,235,390],479)
y=table(['Assumed fan-current multiplier','Assumed auxiliary load','Total demand','Difference to2 A'],[
    [f'{k:.2f}x',f'{a:.2f} A',f"{power.demand(k,a)['total_A']:.2f} A",f"{power.demand(k,a)['arithmetic_margin_A']:+.2f} A"]
    for k,a in [(1,0),(1,.1),(1.25,.1),(1.5,0),(2,0)]
], [235,185,175,175],y)
y=text('<b>Consequence:</b> with0.10 A assumed auxiliary load, the arithmetic fan-current multiplier ceiling is1.357x. Actual startup magnitude/duration is UNKNOWN. Exceeding a continuous catalogue limit does not predict the actual trip timing. Conversely, positive arithmetic margin is not a safety pass.',36,y,770)
text('<b>Do not simply install a stronger adapter:</b> a5 A adapter feeding the same2 A hub path still leaves2.8 A hypothetical fan demand above the hub limit. A changed power architecture requires new connectors, protection and recovery analysis. Do not parallel adapters or connect SATA in this design.',36,y,770)

new('Fan pin functions and wiring limits','OEM pin function reference only. Connector view, colour mapping and the physical terminal schedule are NOT released.')
y=table(['P14 Max pin','OEM function','Design restriction'],[
    ['1','Ground (-)','Signal/power return is not protective earth. Do not infer connector view or wire colour.'],
    ['2','Power (+)','12 V reference. Rated switching and conductor protection unselected.'],
    ['3','Tachometer output','Do not connect multiple tach outputs together or assume a safe-standstill signal.'],
    ['4','PWM control','Speed command only; no claimed protective stop or service isolation.'],
], [105,200,465],479)
y=text('<b>Voltage-drop calculation:</b> deltaV = I x2L x rho/A. At assumed copper rho20=0.0175 ohm mm2/m, one-way1 m,0.5 mm2 and1.4 A: deltaV=0.098 V. At40 C with assumed alpha0.00393/K:0.106 V. These are examples, NOT the OEM cable gauge or a selected wire.',36,y,770)
y=table(['Coordination input','Current status','Needed to release'],[
    ['Fan terminal voltage','Allowed running range UNKNOWN','Do not use published3.9 V startup voltage as allowed running minimum'],
    ['Wire / connectors','Actual conductor gauge, contact rating, resistance UNKNOWN','OEM evidence plus routing, temperature, retention and measured terminal voltage'],
    ['Fuse / protection','Hub auto-reset fuse; time-current / current-limit curves UNKNOWN','Coordinate fault energy with weakest conductor/contact and rated DC device; no arbitrary2 A fuse'],
    ['Switching / enclosure','PR1 and enclosure UNSELECTED','Actual DC load/inrush ratings, compatible harness, cooling and service/isolation arrangement'],
], [155,290,325],y)
text('<b>Keep the logger independent:</b> no GPIO, USB or laptop feed into the fan-power or protective path. OEM PSU Class II does not decide the complete prototype protection class or whether any conductive parts require bonding; assess the actual assembly.',36,y,770)

new('Protection coverage and release evidence','Digital work defines the gap; it does not fabricate a protective relay or claim physical commissioning.')
y=table(['Event / hazard','OEM chain evidence','Remaining implementation'],[
    ['Mains lost / restored','No manual-start latch demonstrated','Fresh start / held-start rejection not implemented'],
    ['Hub overload recovers','Input fuse auto-resets','Recovery coverage must be resolved without defeating OEM protection'],
    ['Fan2 /3 /4 fails','Local LEDs; only fan1 RPM forwarded','No independent four-fan protective monitoring claimed'],
    ['Service / guard removal','No rated isolation assembly selected','Prevent reconnection; verify run-down and inaccessible impellers'],
    ['PWM/monitoring failure','No stopped-state guarantee','Risk allocation, loss-of-signal test and separate physical protection'],
], [165,265,340],479)
y=text('<b>Scope to close, not a generic review:</b> (1) determine actual reachable hazards and accept protection/restart requirements; (2) select rated PR1, all supply sensing and DC switching together; (3) establish wire/connector and protection coordination from measured/OEM current/time data; (4) integrate enclosure, protected entries and service isolation; (5) witness actual power restoration, held START, reset, fault recovery and safe-access cases. Existing restart rules are unchanged.',36,y,770)
y=text('<b>Deliverables included:</b> POWER_COORDINATION.json has20 load and36 wire-drop scenarios; scripts/analysis/d01_electrical_closure.py reproduces them. Ten analytic/synthetic tests check arithmetic and that no synthetic result grants energization. Physical prototypes/tests remain0. No component purchases, live fault tests or invented India stock/prices.',36,y,770)
y=text('<b>Primary references checked5 October2026:</b> ARCTIC P14 Max specification sheet; Noctua NV-PS1 / NA-FC1 / NA-FH1 specifications and NV-PS1 overview; NA-FH1 features. Exact links are in POWER_COORDINATION.json. HSE maintenance guidance is used only for isolation principles, not Indian law or device compliance.',36,y,770)
text('<b>Recommendation:</b> retain the supervised indoor OEM-chain reference. Do not energize this incomplete circuit or bypass PR1. A qualified reviewer must resolve the specific physical/electrical decisions above; the assistant supplies the calculations and drawing evidence, not a false safety approval.',36,y,770)
c.save()

csvrows=[
    ['PS1','1','Noctua NV-PS1 + supplied NA-AC10','VERIFIED OEM REFERENCE','12V/2A/24W; external unmodified; actual India plug/conformity unresolved'],
    ['SC1','1','Noctua NA-FC1','VERIFIED OEM REFERENCE','3A limit; speed control only; consumption unknown'],
    ['H1','1','Noctua NA-FH1 + NA-EC1','VERIFIED OEM REFERENCE','24W four-pin input; SATA not used'],
    ['F1-F4','4','ARCTIC P14 Max ACFAN00287A','VERIFIED OEM REFERENCE','0.35A published current; startup profile unknown'],
    ['PR1','1 assembly','Isolation / switching / restart protective chain','UNSELECTED','Actual hazards, sensing, held-start behavior, DC ratings and qualified review'],
    ['W1','as required','Cables / entries / protection','UNSELECTED','OEM gauge/contact data, actual routes, fault-current/time, restraints and guard entry'],
    ['CB1','1','Control enclosure and mountings','UNSELECTED','140x100x40 CAD reservation is not a finished enclosure'],
]
with (OUT/'E01_RATED_PARTS.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['ID','Quantity','Part','Evidence status','Release hold']);w.writerows(csvrows)
doc=pdfium.PdfDocument(str(OUT/'AQI_D01_POWER_AND_WIRING_SUPPLEMENT.pdf'))
assert len(doc)==4
(OUT/'previews').mkdir(exist_ok=True)
for i in range(len(doc)):
    doc[i].render(scale=1.5).to_pil().save(OUT/'previews'/f'E01_power_{i+1}.png')
print('Built4-page E01 supplement with7-row rated/reference register; no construction release.')
