"""Two-page D01 source comparison; no new CAD or construction release."""
import csv, hashlib, json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
import pypdfium2 as pdfium

R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/component_validation'
D=json.loads((O/'pressure_comparison.json').read_text())
c=canvas.Canvas(str(O/'D01_COMPONENT_CHECK.pdf'),pagesize=(842,595))
c.setTitle('D01 - Component evidence and filter pressure allowance')
def text(x,y,s,size=11,color='#243746'):
    c.setFillColor(HexColor(color));c.setFont('Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,width=748,size=11):
    for line in simpleSplit(s,'Helvetica',size,width):text(x,y,line,size);y-=16
    return y-8
def header(title,number):
    c.setFillColor(HexColor('#132D3B'));c.rect(0,505,842,90,fill=1,stroke=0)
    text(36,556,'AQI TOWER / D01 / COMPONENT EVIDENCE',11,'#6FDAC3')
    text(36,524,title,22,'#FFFFFF')
    text(36,20,'03 OCT 2026 | R01 geometry unchanged | REVIEW ONLY | Physical prototypes: 0',9)
    text(790,20,str(number),10)

header('Real fan data. Honest uncertainty.',1)
para(36,480,'We obtained 14 manufacturer data points. They differ from the brochure, so both calculations stay visible. Filters, guard losses and installed airflow are still unmeasured.')
# Vector chart: four parallel fans; pressure not multiplied by four.
x0,y0,w,h=65,195,475,205
for pa in range(0,51,10):
    y=y0+pa/50*h;c.setStrokeColor(HexColor('#DDE4E8'));c.line(x0,y,x0+w,y);text(40,y-3,str(pa),9)
for q in range(0,751,150):text(x0+q/750*w-7,y0-18,str(q),9)
text(65,415,'Available fan static pressure / Pa',10)
text(220,158,'Total flow through four fans / m3/h',10)
rows=list(csv.DictReader((O/'curve_comparison.csv').open()))
for key,col in [('brochure_Pa','#D98032'),('numeric_Pa','#008E85')]:
    c.setStrokeColor(HexColor(col));c.setLineWidth(2)
    path=c.beginPath()
    for i,r in enumerate(rows):
        x=x0+float(r['total_flow_m3h'])/750*w;y=y0+float(r[key])/50*h
        (path.moveTo if i==0 else path.lineTo)(x,y)
    c.drawPath(path)
text(570,399,'OEM numeric data',12,'#008E85');text(570,379,'2800 rpm; 14 points',10)
text(570,346,'Earlier brochure reading',12,'#D98032');text(570,326,'Approximate digitization',10)
text(570,291,'Same assumed filter cases:',11)
text(570,268,'Filter reference*   Old     Numeric',10)
for i,ref in enumerate((5,10,20)):
    a=D['scenarios'][i]['total_flow_m3h'];b=D['scenarios'][i+3]['total_flow_m3h']
    text(570,245-22*i,f'{ref:2} Pa                  {a:.0f}       {b:.0f}',11)
text(570,173,'Flows in m3/h; NOT measured.',10)
para(36,125,'*Each parallel filter path is assumed to lose 5, 10 or 20 Pa at 400 m3/h total (200 through each filter). All R01 guard, plenum and installation allowances are retained.',size=10)
para(36,78,'Do not replace the old claim with a bigger number. OEM endpoint differences and supplied revision remain unresolved. Neither curve predicts CADR, HEPA performance or an outdoor bubble.',size=10)
c.showPage()
header('What filter can this assembly tolerate?',2)
para(36,480,'This table turns the airflow model into a useful component-screening requirement. The pressure remaining for each filter is the fan pressure minus all modeled non-filter losses.')
for x,s in zip((42,174,317,480,642),('Total m3/h','Each filter m3/h','Other losses / Pa','Filter Pa: brochure','Filter Pa: numeric')):text(x,413,s,10)
for i,r in enumerate(D['filter_headroom']):
    y=386-i*27
    vals=[r['total_flow_m3h'],r['each_filter_flow_m3h'],r['assumed_nonfilter_loss_Pa'],r['brochure_filter_headroom_Pa'],r['numeric_filter_headroom_Pa']]
    for x,v in zip((42,174,317,480,642),vals):text(x,y,f'{v:.1f}',12)
y=para(36,267,'Decision: compare candidate filters at 150 and 175 m3/h per element. At 300 m3/h total, about 14.5 Pa remains for the filter. At 400 total, the assumed non-filter losses already exceed both fan curves. These balance limits are not validated safety margins.')
y=para(36,y,'Candidate, not selected: Camfil AQ13 407051002 is an OEM-listed nominal 20x20x2 inch filter. The current sheet does not establish the actual frame dimensions or low-flow resistance needed here. India contact route found; exact local stock, price and delivery UNKNOWN.')
y=para(36,y,'Existing S&P 990303 remains a dimensional reference only. Before cutting seats, confirm an obtainable filter, actual frame/seal dimensions and its clean/loading pressure curve. Mechanical, guards, electrical restart protection and physical commissioning remain unreleased.')
para(36,y,'Sources: ARCTIC support.arctic.de/p14-max/docs; ARCTIC specification PDF; Camfil AQ13 2025 product sheet and official India contact locator. Full clickable links, SKU discrepancy, hashes, numeric data and reproduction steps accompany this PDF in README.md.',size=9)
c.save()
pdf=pdfium.PdfDocument(O/'D01_COMPONENT_CHECK.pdf')
assert len(pdf)==2
for i,page in enumerate(pdf):page.render(scale=1.4).to_pil().save(O/f'page-{i+1}.png')
names=['ARCTIC_P14_Max_PQ_CFD.xlsx','ARCTIC_P14_Max_PQ_20240919.pdf','ARCTIC_P14_Max_Spec.pdf','Camfil_AQ13_2025.pdf']
files=[R/'data/prototype_d01/sources'/n for n in names]
files += [p for p in O.iterdir() if p.is_file() and p.name!='MANIFEST.json']
(O/'MANIFEST.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
print('Two PDF pages rendered; source and output hashes saved.')
