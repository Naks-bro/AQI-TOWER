"""Dimensioned E03 layout from checked original control-module proxies."""
import csv,json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/electrical_package/control_module'
d=json.loads((O/'FIT_CHECKS.json').read_text())
assert d['native_tower_unchanged'] and not d['release']
assert not any(x['hits'] for x in d['body_vs_actual_OEM_checks']+d['assumed_space_vs_actual_OEM_checks'])
objs={o['name']:o for o in d['objects']}
pdf=O/'D01_E03_DIMENSIONED_CONTROL_LAYOUT.pdf'
c=canvas.Canvas(str(pdf),pagesize=(842,595),invariant=1)
c.setTitle('D01 E03 external control module dimensioned fit review')
navy=HexColor('#153d4c');teal=HexColor('#148b84');amber=HexColor('#aa651d')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=9,leading=12,textColor=navy)
def para(s,x,y,w):
 p=Paragraph(s,style);_,h=p.wrap(w,520);assert y-h>42;s=p.drawOn(c,x,y-h);return y-h-8
def label(s,x,y,size=9):c.setFillColor(navy);c.setFont('Helvetica',size);c.drawString(x,y,s)
def title(t,page):
 c.setFillColor(navy);c.rect(0,522,842,73,fill=1,stroke=0)
 c.setFillColor(HexColor('#79e1cc'));c.setFont('Helvetica-Bold',9);c.drawString(30,572,'AQI TOWER / D01 R03M / E03 CONTROL MODULE / 5 OCTOBER 2026')
 c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',20);c.drawString(30,544,t)
 c.setFillColor(HexColor('#ac2947'));c.setFont('Helvetica-Bold',8);c.drawString(30,23,'FIT REVIEW ONLY / NO DRILLING, WIRING OR ENERGIZATION RELEASE');c.drawRightString(812,23,str(page))
def dimension(x,y,xx,yy,text):
 c.setStrokeColor(navy);c.setLineWidth(.6);c.line(x,y,xx,yy)
 if abs(y-yy)<.01:
  for a in (x,xx):c.line(a,y-4,a,y+4)
  label(text,(x+xx)/2-13,y+5,8)
 else:
  for a in (y,yy):c.line(x-4,a,x+4,a)
  label(text,x+5,(y+yy)/2,8)
def tab(rows,widths,x,y):
 t=Table([[Paragraph(str(v),style) for v in row] for row in rows],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e1efee')),('GRID',(0,0),(-1,-1),.4,HexColor('#b7ced2')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
 _,h=t.wrap(sum(widths),520);assert y-h>44;t.drawOn(c,x,y-h);return y-h-10
title('External control box: dimensioned body layout',1)
scale=1.45;cx=267;cy=328
def xy(x,y):return cx+x*scale,cy+y*scale
def rect(b,color,fill=True,dashed=False):
 x,y,z,xx,yy,zz=b;c.setStrokeColor(HexColor(color));c.setFillColor(HexColor(color));c.setLineWidth(.8)
 c.setDash(4,3) if dashed else c.setDash()
 if fill:c.setFillAlpha(.15)
 c.rect(*xy(x,y),(xx-x)*scale,(yy-y)*scale,fill=int(fill),stroke=1);c.setFillAlpha(1);c.setDash()
rect([-150,-100,0,150,100,0],'#5d7584',False)
rect([-142.5,-92.5,0,142.5,92.5,0],'#93a7b4',False)
rect(objs['DIN1_ENVELOPE']['bounds_mm'],'#6b8398')
for n in ('CTRL1_WIRE_SPACE_ASSUMED','H1_CONNECTOR_SPACE_ASSUMED','SC1_CONNECTOR_SPACE_ASSUMED'):
 rect(objs[n]['bounds_mm'],'#a263b6',False,True)
for n,name in [('CTRL1_OPTA_LITE','Opta Lite'),('H1_NA_FH1','NA-FH1'),('SC1_NA_FC1','NA-FC1')]:
 o=objs[n];rect(o['bounds_mm'],o['color']);b=o['bounds_mm'];label(name,*xy(b[0]+5,b[1]+(b[4]-b[1])/2),10)
for x,y in d['proposed_DIN_holes_mm']:
 c.setStrokeColor(amber);c.circle(*xy(x,y),2.25*scale,stroke=1,fill=0)
dimension(*xy(-150,112),*xy(150,112),'300')
dimension(*xy(-161,-100),*xy(-161,100),'200')
dimension(*xy(-135,-26),*xy(-10,-26),'125 rail')
label('Datum: enclosure centre; +X right, +Y up; dimensions mm',55,154,9)
label('Purple dashed = ASSUMED service/routing space, not cable specifications',55,137,8)
y=para('<b>Verified sources:</b> Hammond1554XA2GY box; matching1554XPL panel. Opta70 x88.8 x61.1 depth reservation; hub93 x43 x12.5; speed controller48 x25 x21 in the proposed orientation. Components are simplified bodies, not exact connector models.',505,491,300)
y=para('<b>Checked:</b> all3 body envelopes and3 assumed service volumes clear24 solids in the private OEM STEP, excluding intended panel support. Bodies have65 /85 /47 mm pairwise minimum separation. No physical fit result.',505,y,300)
y=para('<b>Design choice:</b> retain existing493-object tower unchanged. Box is a separate, supervised-indoor module; its placement, retention and connection to the tower are not approved. Power adapter stays external. No mains inside this proposed box.',505,y,300)
para('<b>Not yet fitted:</b> PR1, fuses/holders, terminals, cable glands, buttons and their backs, supports, functional earth and complete wiring. A body-fit pass is NOT a complete control-panel fit pass.',505,y,300)
para('<b>Body lower-left X/Y coordinates:</b> Opta -115 /-44.4; hub20 /-65; speed controller40 /25. DIN envelope lower-left -135 /-17.5. Each body dimension and Z coordinate is in PLACEMENT.csv. Coordinates locate proposed envelopes, NOT mounting holes or connectors.',55,117,740)
c.showPage();title('Mounting and depth: explicit next interface',2)
y=tab([['Layer / proposal','Dimension or coordinate','Evidence / release status'],
 ['OEM panel top','STEP Z = -58.3744 mm','OEM panel thickness1.6256 inSTEP; nominal page rounds to2mm'],
 ['DIN support envelope','35 mm wide /7.5 mm high /125 mm proposed cut','Phoenix0801733; actual profile and clips not drawn'],
 ['Opta back / front','7.5 /68.6 mm above panel top','Conservative ASSUMED back plane at rail crest; actual seating unknown'],
 ['Hub / controller carrier','5 mm ASSUMED lift above panel','No actual carrier, clamp, screw or magnetic-only retention approval'],
 ['Proposed rail holes','X -122.5 and -22.5; Y0; diameter4.5 mm','100mm centres; aligned-to-slot cut ASSUMED; NOT drilling release'],
 ['Panel mounting','Use1554XPL matching panel / OEM insert pattern','Do not drill plastic box or transfer part-label locations'],
 ],[165,225,390],30,493)
y=para('<b>Fit limitation:</b> the supplied STEP contains moulded geometry, screws, gasket and a shaped panel. Published CAD intentionally uses an original simplified rectangular panel and shell. It is NOT a substitute for Hammond drawings. Panel contour, existing holes, threads, DIN clip, terminal access and button/connector backs are not manufactured details.',30,y,780)
y=para('<b>Assembly review sequence:</b> inspect exact delivered box/panel/controller; establish actual panel thickness and DIN seating; fix reviewed rail/supports to panel; mechanically retain hub/controller; fit selected protection and terminations; review external source and all entries; check lid/clip/connector access, strain relief, clearances and heat. No energized wiring steps are supplied.',30,y,780)
y=para('<b>Service decision still open:</b> NA-FC1 is inside the box. Its dial and switch are not accessible through a closed lid in this layout. Do not operate with the box open just to reach it. A reviewed access strategy or different control component is needed before use. No arbitrary lid cutouts or thermal vents.',30,y,780)
y=para('<b>Release holds:</b> protective PR1 and fault coordination, real wires/contact gauges, retention and mounting strength, connector bends, heat rise, enclosed controls/access, functional earth, whole-device ingress and placement. The stock IP68 rating does not apply to the completed or drilled module. Physical tests0. All relay commands remain disabled in default firmware.',30,y,780)
para('<b>Sources:</b> exact URLs and OEM STEP hash are in FIT_CHECKS.json. Source PDFs/STEP stay private local references; redistribution permission was not established. Editable FCStd/STEP here contain only original envelope geometry. No purchase, supplier contact, new software installation or tower geometry change.',30,y,780)
c.save()
with (O/'PLACEMENT.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['Name','Xmin','Ymin','Zmin','Xmax','Ymax','Zmax','Evidence'])
 for o in d['objects']:w.writerow([o['name'],*o['bounds_mm'],o['status']])
doc=pdfium.PdfDocument(str(pdf));assert len(doc)==2
(O/'previews').mkdir(exist_ok=True)
for i in range(2):doc[i].render(scale=1.4).to_pil().save(O/'previews'/f'E03_{i+1}.png')
print('E03 dimensioned two-page layout, placements and inspection previews written.')
