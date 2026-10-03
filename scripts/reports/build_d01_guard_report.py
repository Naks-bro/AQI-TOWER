"""R02G guard mounting review drawing from the integrated CAD revision."""
import ast,json,math,csv
from pathlib import Path
import numpy as np
from PIL import Image,ImageColor
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/r02_guards'
M=json.loads((O/'cad_mesh.json').read_text());GUARD_RIM_MM=10
fn=next(n for n in ast.parse((R/'scripts/reports/build_d01_delivery.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='render')
exec(compile(ast.Module(body=[fn],type_ignores=[]),'shared_renderer','exec'),globals())
if not (O/'D01_ASSEMBLY.png').exists():render()
a=json.loads((O/'checks.json').read_text())
c=canvas.Canvas(str(O/'D01_R02G_GUARD_MOUNTINGS.pdf'),pagesize=(1191,842))
def text(x,y,s,size=12):
    c.setFillColor(HexColor('#203848'));c.setFont('Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,w):
    for line in simpleSplit(s,'Helvetica',12,w):text(x,y,line);y-=18
    return y-14
def start(title,num):
    text(35,809,'AQI TOWER / D01-R02G / 03 OCT 2026 / PROPOSED DETAIL',12)
    text(35,772,title,25)
    text(35,23,'REVIEW ONLY - NOT FOR FABRICATION OR ENERGIZING | Physical prototypes: 0 | No outdoor/public approval',10)
    text(1140,23,str(num),10)
start('Two guards. Separate fastenings.',1)
c.drawImage(str(O/'D01_ASSEMBLY.png'),25,105,width=690,height=563)
y=711
for s in ['WHY CHANGE: the previous four shared bolts retained both guards. R02G gives the upper and lower guards four separate bolts each, so removing one set does not release the other mounting.',
 'WHAT CHANGED: upper brackets moved along the sides; four extra holes added to the fan plate. Upper side-skirt rivet holes move with their brackets. Inner brackets retain their earlier positions.',
 f"DIGITAL CHECKS: {a['objects']} valid parts; {a['pair_checks']} checked changed-part pairs without clashes. Sixteen assumed driver/socket envelope checks clear. Native reopen and STEP volume checks pass.",
 'WHAT THIS DOES NOT PROVE: actual tools and hand access, sheet/rivet strength, finger protection, vibration resistance, captive fasteners, sealed cable entry or safe isolation. Guards remain proposed sheet envelopes, not certified products.',
 'NEXT CONSTRUCTION GATE: complete guard seams/rivets, remaining cabinet hardware and protective access/isolation details; verify actual filter resistance and sealing. No powered demonstration until the complete assembly passes physical review.']:
    y=para(745,y,s,400)
c.showPage();start('Mounting coordinates and bolt stacks / millimetres',2)
text(55,749,'TOP VIEW: fan plate 550 x 360 x 9',12)
x0,y0,s=55,360,1.05
c.setStrokeColor(HexColor('#526a7a'));c.rect(x0,y0,550*s,360*s)
# Guard outline; only guard mounting holes shown, not complete plate cutting drawing.
c.rect(x0+115*s,y0+20*s,320*s,320*s)
for tag,ys,color in [('INNER',(60,300),'#21877c'),('OUTER',(120,240),'#ac612c')]:
    c.setStrokeColor(HexColor(color))
    for x in (105,445):
        for y in ys:c.circle(x0+x*s,y0+y*s,4,fill=0)
    text(55,327 if tag=='INNER' else 304,f'{tag}: x105 / 445; y'+ ' / '.join(map(str,ys))+'; hole diameter4.5',12)
text(55,278,'Origin: plate front-left corner. Dimensions are global x,y.',11)
text(55,256,'Guard-only view: retain all other R01 plate holes/apertures.',11)
y=714
for s1 in ['OUTER GUARD: angle y100..140 and220..260, x95..115 /435..455, base z580..582. Screw head z583..587;20 mm shaft z563..583. Top washer582..583; bottom washer570..571; nut565..570.',
 'INNER GUARD: angle y40..80 and280..320, same x positions, base z569..571. Screw head581..585;20 mm shaft561..581. Top washer580..581; bottom washer568..569; nut563..568.',
 'BOTH: M4 x20 proposed screw; head7 diameter x4 high, nut7 across flats x5 high; washers12 OD x1 with assumed4.3 ID. Nominal thread projection2 mm. No torque/grade release.',
 'OUTER SKIRT: new blank, diameter3.5 rivet holes at y110/130/230/250, z590 on both side skirts. OMIT prior y50/70/290/310 holes. Existing bracket holes travel with the brackets; no new bracket shape.',
 'TOOL ASSUMPTIONS: straight driver shaft4 mm diameter,100 mm long above each screw; nut socket12 mm outside diameter,25 mm length below washer. Handles, hands, insertion route and tolerances excluded.']:
    y=para(690,y,s1,460)
para(55,193,'ASSEMBLY ORDER: prepare revised plate/skirt blanks; join guard skirts and brackets using reviewed fasteners; independently secure inner guard, then outer guard. Verify both retain their mountings when the other set is removed, with power isolated. This is a review sequence, not authorization to energize.',1080)
para(55,106,'Source dimensions: Accu SSC-M4-20-A4-R360 cap screw; HNN-M4-A4 nut; Easyfix large M4 washer. Links and limitations in README. No product stock, coating selection, service life or safety certification is asserted.',1080)
c.save();pdf=pdfium.PdfDocument(O/'D01_R02G_GUARD_MOUNTINGS.pdf')
for i,p in enumerate(pdf):p.render(scale=1).to_pil().save(O/f'sheet-{i+1}.png')
with (O/'GUARD_DELTA_BOM.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['item','qty','revision_action','release']);w.writerows([
    ['M4x20 cap screw',8,'Replace4 shared M4x25 envelopes','DIMENSIONAL PROPOSAL'],
    ['7AF x5 M4 locknut',8,'Replace4 cylindrical nut envelopes','GRADE/REUSE UNKNOWN'],
    ['12OD x1 M4 washer',16,'Replace8 earlier washer envelopes','4.3ID ASSUMED'],
    ['Outer guard angle40 long',4,'Relocate y100/220 starts','ROOT RADIUS/STRENGTH UNKNOWN'],
    ['Outer side skirt',2,'New rivet hole pattern','SEAMS/RIVETS NOT RELEASED'],
    ['Fan plate',1,'Add4 dia4.5 holes at x105/445 y120/240','STRENGTH/SEAL UNKNOWN']])
print('Two review sheets, actual CAD render and delta BOM generated.')
