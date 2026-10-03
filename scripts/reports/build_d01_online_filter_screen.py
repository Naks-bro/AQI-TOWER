"""Dimensioned comparison from R01 basis and public OEM dimensions; no fit release."""
import json, math
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/component_validation'
facts=json.loads((R/'data/prototype_d01/online_filter_screen.json').read_text())
C=json.loads((R/'cad/parametric/d01_r00.json').read_text())
outer=C['filter_side'];inner=outer-2*C['filter_gasket_width'];ap=C['intake_aperture']
checks=dict(gasket_outer_mm=outer,gasket_inner_mm=inner,seat_opening_mm=ap,
    gasket_inner_offset_from_seat_edge_mm=(inner-ap)/2,
    comparisons=[dict(name=n,dimension_basis='OEM published envelope',width_mm=w,height_mm=h,
       centred_uncovered_aperture_each_side_mm=[max(0,(ap-w)/2),max(0,(ap-h)/2)],
       two_filter_gross_area_m2=2*w*h/1e6,
       gross_face_speed_at_total300_m3h=300/3600/(2*w*h/1e6))
       for n,w,h in [('IKEA STARKVIND',370,290),('Smart Air Sqair',264,264)]],
    tests={'gasket_inner475_3':abs(inner-475.3)<1e-8,'seat470':ap==470,
       'starkvind_not_dropin':370<ap and 290<ap,'sqair_not_dropin':264<ap,
       'two_parallel_faces':abs(300/3600/(2*.370*.290)-.388319975)<1e-6})
assert all(checks['tests'].values())
(O/'online_filter_fit_checks.json').write_text(json.dumps(checks,indent=2))
c=canvas.Canvas(str(O/'D01_ONLINE_FILTER_OPTIONS.pdf'),pagesize=(842,595))
def t(x,y,s,size=11,col='#173647'):
    c.setFillColor(HexColor(col));c.setFont('Helvetica',size);c.drawString(x,y,s)
def p(x,y,s,width=750,size=11):
    for line in simpleSplit(s,'Helvetica',size,width):t(x,y,line,size);y-=16
    return y-8
def head(title,n):
    c.setFillColor(HexColor('#173647'));c.rect(0,505,842,90,fill=1,stroke=0)
    t(36,558,'D01 / INTERNET SOURCING / 03 OCT 2026',11,'#78E0C7');t(36,525,title,23,'#FFFFFF')
    t(36,20,'REVIEW ONLY | No purchase, supplier contact or physical performance claim | R01 CAD unchanged',9);t(800,20,str(n),9)
head('Online options without supplier chasing',1)
y=p(36,480,'Public sources give us alternatives, not a finished filter selection. Prefer a sensibly priced, replaceable local component over forcing an expensive import into the current cabinet.')
for title,body in [
    ('IKEA STARKVIND 104.633.30 | Rs 1,090 each displayed',
     'Official India page: 370 x290 x40 mm. Two filters: Rs 2,180 before delivery. Local availability is not confirmed. OEM limits intended use to STARKVIND appliances; custom use is experimental, not endorsed. No published low-flow pressure curve found.'),
    ('Smart Air Sqair replacement | 264 x264 x50 mm',
     'Official India replacement-filter route; current price not verified. Smaller face and greater depth than D01 reference. OEM India/global pages differ in H12/E12 terminology. Not H13, not a drop-in, and appliance CADR cannot transfer to our fans.'),
    ('3M Filtrete MPR1900 | nominal 20 x20 x1 inch',
     'India import listings display Rs 19,801 and Rs 41,464 for four, despite the same stated ASIN. Conflicting actual dimensions and no authenticated exact low-flow curve. Keep as an alternative; do not recommend these costly listings for purchase.')]:
    t(36,y,title,13);y=p(36,y-24,body)
p(36,y-3,'Decision: stop treating supplier correspondence as your task. Continue with an interchangeable filter interface and a measured-flow commissioning route. Missing public data stays unknown; no invented pressure curve, MERV equivalence or guaranteed output.',size=11)
c.showPage();head('Actual interface: why these are not drop-ins',2)
scale=.48;bx,by=60,175
c.setStrokeColor(HexColor('#173647'));c.setLineWidth(1)
c.rect(bx,by,550*scale,550*scale)
for w,h,col in [(outer,outer,'#008E85'),(inner,inner,'#008E85'),(ap,ap,'#D47D30'),(370,290,'#587AB2'),(264,264,'#915AA8')]:
    c.setStrokeColor(HexColor(col));c.rect(bx+(550-w)/2*scale,by+(550-h)/2*scale,w*scale,h*scale)
t(60,465,'Centred envelope comparison / mm',12)
t(350,445,'R01 cabinet opening: 470 x470',12,'#D47D30')
t(350,420,'Actual gasket: 495.3 outside / 475.3 inside',12,'#008E85')
t(350,395,'STARKVIND: 370 x290 x40',12,'#587AB2')
t(350,370,'Sqair: 264 x264 x50',12,'#915AA8')
p(350,340,'The smaller filters leave large open bypass areas. A sealed reducer, matching support and retention are required; placing them behind the old opening is not a working assembly.',width=435)
p(350,252,'Correction: our previous inquiry incorrectly stated a490/470 mm gasket. Reopening the saved R01 CAD confirmed495.3/475.3 mm. The470 mm dimension belongs to the cabinet opening.',width=435)
p(36,134,'The drawing compares dimensions only, not a manufactured gasket landing. Public sources do not yet establish frame-border flatness, clamping force, pressure loss or custom-use suitability. No filter class or performance transfers from another appliance.',size=10)
p(36,80,'Sources: official IKEA India STARKVIND and Smart Air India filter pages; 3M airflow page; observed Desertcart listings; CEC2018 laboratory report. Exact links, dates and limitations: data/prototype_d01/online_filter_screen.json.',size=9)
c.save()
pdf=pdfium.PdfDocument(O/'D01_ONLINE_FILTER_OPTIONS.pdf')
assert len(pdf)==2
for i,page in enumerate(pdf):page.render(scale=1.25).to_pil().save(O/f'online-options-{i+1}.png')
print(json.dumps(checks,indent=2))
