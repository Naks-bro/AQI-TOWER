"""E02 actual-terminal ordinary-control bench drawing; not tower protective release."""
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
import pypdfium2 as pdfium

R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/electrical_package'
checks=json.loads((O/'OPTA_HOST_CHECKS.json').read_text())
assert checks['host_assertions']==1041 and not checks['target_board_compiled']
opta_A=2/12
candidate=dict(status='ORDINARY-CONTROL BENCH CANDIDATE ONLY / NO PROTECTIVE OR WIRING RELEASE',
    accessed='2026-10-05',controller=dict(part='Arduino Opta Lite AFX00003',max_W_at12V=2,
    envelope_screen_mm=[70,88.8,61.1],depth_basis='56.8mm body plus4.3mm projection from OEM drawing; orientation/rail/clearance not released'),
    enclosure=dict(part='Hammond1554XA2GY',outside_mm=[300,200,120],OEM_max_PCB_mm=[285,174],
                   warning='Max PCB dimensions are NOT a guaranteed DIN workspace. No approved holes, rail, mount, heat or whole-box ingress qualification.'),
    power=dict(controller_A=opta_A,fan_plus_controller_A=1.4+opta_A,
               remaining_to_supply2A=2-1.4-opta_A,remaining_to_fuse_typical40C_1_7A=1.7-1.4-opta_A,
               assumptions='Published fan current and maximum controller consumption. Hub/controller input circuits, wiring and startup remain excluded.'),
    fuse_candidate=dict(part='Littelfuse0297002.WXNV',rated_A=2,rated_DC_V=32,interrupt_A_at32V=1000,
        typical_recommended_load_A_at20C=1.9,typical_recommended_load_A_at40C=1.7,
        opening_windows_s={'110_percent':[360000,None],'135_percent':[.75,600],'200_percent':[.15,5]},
        status='SCREENED / NOT SELECTED',warning='Actual source/hub limiting and recovery curves, weakest wiring, holder and temperature unknown. Cannot claim fuse coordination or guaranteed clearing.'),
    terminal_mapping={'I1':'A0 START_NO','I2':'A1 STOP_NC','I3':'A2 RESET_NO','I4':'A3 BENCH_PERMIT','I5':'A4 unswitched12V DIGITAL only','Output1_pair':'D0 bench lamp only; default disabled'},
    sources={'opta_datasheet':'https://docs.arduino.cc/resources/datasheets/AFX00001-AFX00002-AFX00003-datasheet.pdf',
        'opta_pinout':'https://docs.arduino.cc/resources/pinouts/AFX00001-AFX00002-AFX00003-full-pinout.pdf',
        'enclosure':'https://www.hammfg.com/part/1554XA2GY',
        'fuse':'https://www.littelfuse.com/assetdocs/littelfuse-datasheet-297-mini32v?assetguid=42c9dd21-a88e-4328-8e67-2f832444faf1'},
    release=dict(board_compiled=False,physical_test=False,protective_controller=False,fuse_selected=False,
                 enclosure_released=False,fan_output_connection_released=False))
assert abs(candidate['power']['fan_plus_controller_A']-47/30)<1e-12
assert candidate['power']['remaining_to_fuse_typical40C_1_7A'] < .134
(O/'OPTA_INTEGRATION_SCREEN.json').write_text(json.dumps(candidate,indent=2)+'\n',encoding='utf-8')
c=canvas.Canvas(str(O/'AQI_D01_OPTA_BENCH_REVIEW.pdf'),pagesize=(842,595),invariant=1)
c.setTitle('AQI D01 E02 ordinary control bench candidate')
navy=HexColor('#153d4c');teal=HexColor('#087e83');amber=HexColor('#ac6407');red=HexColor('#ac2947')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=14,textColor=navy)
small=ParagraphStyle('small',parent=style,fontSize=8.5,leading=11)

def text(s,x,y,w=770):
    p=Paragraph(s,style);_,h=p.wrap(w,480);assert y-h>42,(s[:30],y,h);p.drawOn(c,x,y-h);return y-h-9
def title(s,sub,n):
    c.setFillColor(navy);c.rect(0,504,842,91,fill=1,stroke=0)
    c.setFillColor(HexColor('#6ce0cb'));c.setFont('Helvetica-Bold',9);c.drawString(36,569,'AQI TOWER / D01 R03M / E02 BENCH CANDIDATE / 5 OCTOBER 2026')
    c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',20);c.drawString(36,539,s)
    c.setFont('Helvetica',9);c.drawString(36,518,sub)
    c.setFillColor(red);c.setFont('Helvetica-Bold',8);c.drawString(36,24,'NOT SAFETY-RATED — NOT RELEASED FOR WIRING, FAN CONNECTION OR ENERGIZATION');c.drawRightString(806,24,str(n))
def line(x,y,xx,yy,color=teal):
    c.setStrokeColor(color);c.setLineWidth(1.3);c.line(x,y,xx,yy)
def label(s,x,y):
    c.setFillColor(navy);c.setFont('Helvetica',9);c.drawString(x,y,s)
def table(headers,rows,widths,y):
    t=Table([[Paragraph(str(v),small) for v in row] for row in [headers]+rows],colWidths=widths)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#d5ece8')),('GRID',(0,0),(-1,-1),.4,HexColor('#b6ccd0')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    _,h=t.wrap(770,480);assert y-h>45;t.drawOn(c,36,y-h);return y-h-10

title('A real controller and implemented local sequence','Terminal reference for a protected dummy-load bench only. PR1 and the tower protective system remain OPEN.',1)
# Original drawing: contact positions conceptual; printed OEM identifiers only.
c.setFillColor(HexColor('#e5f4f0'));c.setStrokeColor(teal);c.roundRect(409,225,210,240,6,fill=1,stroke=1)
label('CTRL1 / Opta Lite AFX00003',427,442)
label('+ supply',429,417);label('- return',429,393)
line(36,422,409,422,red);label('Reviewed, fused12 V bench source (+)',36,439)
line(36,398,409,398);label('0 V return; NOT protective earth',36,376)
for i,(name,y,closed) in enumerate([('START / NO',351,False),('STOP / NC',319,True),('RESET / NO',287,False),('BENCH PERMIT',255,True)]):
    line(66,422,66,y,red);line(66,y,225,y,red);line(260,y,409,y,red)
    line(225,y,260,y+(0 if closed else 11),red)
    label(name,90,y+8);label(f'I{i+1} = A{i}',425,y-3)
line(335,422,335,233,red);line(335,233,409,233,red);label('I5 = A4',425,230)
label('Source present',264,220)
label('DIGITAL only',425,215)
for x,y in [(66,422),(335,422),(66,351),(66,319),(66,287),(66,255)]:
    c.setFillColor(red);c.circle(x,y,2,fill=1,stroke=0)
line(66,422,66,490,red);line(66,490,700,490,red);line(700,490,700,422,red);line(700,422,720,422,red)
label('Output1 pair / D0',652,398)
line(720,422,748,435,red);line(748,422,775,422,red)
line(775,422,775,319,red);c.setStrokeColor(amber);c.circle(775,302,17,stroke=1,fill=0)
line(775,285,775,195);line(775,195,36,195);line(36,195,36,398)
label('Dummy lamp',665,302);label('NOT a fan',665,287)
text('<b>Connection hold:</b> junction dots connect; crossings without dots do not. Contacts and power protection are not approved parts. Output1 is its printed contact pair, not invented COM/NO identifiers. Preserve polarity; compatible protected harness required. No connection to the tower fan chain is released.',36,180)
text('<b>Firmware:</b> all relay commands remain LOW by default. RUN REQUESTED/TRIP/source LEDs show software status only. Inputs I1–I5 are digital.12 V is outside the0–10 V analog range; do not change I5 to analog mode. I4 is a bench test signal, not independent protective permission.',36,122)
c.showPage()

title('Enclosure fit and protection coordination','A concrete external-box candidate; not a fabrication layout, released fuse choice or completed safety circuit.',2)
# Outer enclosure view only; avoids pretending outer dimensions are usable workspace.
c.setStrokeColor(teal);c.setFillColor(HexColor('#f3f8f8'));c.rect(36,248,330,220,fill=1,stroke=1)
label('Hammond1554XA2GY /300 x200 x120 mm',40,477)
for x,y,w,h,s in [(58,307,77,98,'Opta'),(157,325,102,47,'NA-FH1'),(157,389,53,28,'NA-FC1')]:
    c.setStrokeColor(amber);c.setFillColor(HexColor('#fff0dc'));c.rect(x,y,w,h,fill=1,stroke=1);label(s,x+4,y+h/2)
text('Original envelope sketch, not mounting/drilling coordinates. DIN rail, plate, entry, control-button backs and cable bend/retention are omitted. Keep the power adapter external.',44,291,305)
text('<b>Fit finding:</b> Opta front70 x88.8 mm; drawing-derived depth reservation61.1 mm. A40 mm deep CAD box is not a normal DIN fit. Do not reinterpret the stock box IP rating as modified-device weather protection. The new external box is a recommendation; native tower CAD is unchanged.',392,475,413)
text('<b>Power:</b> Opta maximum2 W at12 V adds0.167 A. Fans plus Opta alone total1.567 A /18.8 W. Supply margin0.433 A remains before hub/controller, input circuits and startup. No fan power-budget approval follows.',392,364,413)
y=table(['Real fuse screen','Verified OEM data','Decision / consequence'],[
    ['Littelfuse0297002.WXNV','2 A /32 V DC;1000 A interrupt rating at32 V','SCREENED, not selected. Holder/actual circuit coordination unresolved'],
    ['Typical thermal allowance','1.9 A at20 C;1.7 A at40 C','Fans+Opta leave only0.133 A to40 C allowance before other loads'],
    ['Opening at110% /2.2 A','Minimum360000 s; no maximum given','Not a2 A current limiter or proof of prompt clearing on a limited supply'],
    ['Opening at200% /4 A','0.15–5 s specified window','Actual PSU/hub fault current/time and weakest cable/contact required'],
], [155,275,340],233)
text('<b>Limits:</b> 1,041 host assertions pass, including1,024 one-step cases. Board compilation and all physical tests are NOT DONE. Software, ordinary relays, digital source presence and LEDs do not prove safe access, fault coverage or standstill. Existing restart rules remain unchanged and unresolved for internal fan/hub resets.',36,y)
c.save()
doc=pdfium.PdfDocument(str(O/'AQI_D01_OPTA_BENCH_REVIEW.pdf'));assert len(doc)==2
for i in range(2):doc[i].render(scale=1.5).to_pil().save(O/'previews'/f'E02_opta_{i+1}.png')
print('Two-page E02 bench candidate drawing and exact-source integration screen created; no tower wiring release.')
