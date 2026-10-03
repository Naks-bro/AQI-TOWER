"""Create a review sheet from R02H CAD and its checked fastening dimensions."""
import ast,json,math,csv
from pathlib import Path
import numpy as np
from PIL import Image,ImageColor
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/r02_adapter/hardware_detail'
M=json.loads((O/'cad_mesh.json').read_text());GUARD_RIM_MM=10
fn=next(n for n in ast.parse((R/'scripts/reports/build_d01_delivery.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='render')
exec(compile(ast.Module(body=[fn],type_ignores=[]),'shared_renderer','exec'),globals())
if not (O/'D01_ASSEMBLY.png').exists():render()
a=json.loads((O/'checks.json').read_text())
c=canvas.Canvas(str(O/'D01_R02H_FASTENING_SERVICE.pdf'),pagesize=(1191,842))
def text(x,y,s,size=12):
    c.setFillColor(HexColor('#203848'));c.setFont('Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,w=470):
    for line in simpleSplit(s,'Helvetica',12,w):text(x,y,line);y-=17
    return y-12
text(35,808,'AQI TOWER / D01-R02H / 03 OCT 2026 / REVIEW ONLY',12)
text(35,770,'Filter fastening and removal: now included in the CAD',25)
c.drawImage(str(O/'D01_ASSEMBLY.png'),25,225,width=650,height=530)
y=716
for s in [f"DETECTED: {a['objects']} valid CAD objects; {a['pair_checks']} changed-part pair checks with no modeled clashes. Native reopen and STEP volume checks pass.",
 'CHANGED: eight 70 mm rod envelopes replaced with proposed M4 x80 studs. Four ledge screws now have25 mm under-head length and modeled cap heads. Added28 nuts and32 metal backing washers.',
 'SERVICE CHECK: after removing the four service nuts, washers and retainer on each side, the filter has a nominal200 mm straight outward travel without collision. Isolate power and wait for fans to stop before access; protective access controls remain unresolved.',
 'ASSUMPTIONS: nut7 mm across flats x5 high; washer12 OD x4.3 ID x1; installed sealing washer1 mm. Gasket compression, filter border, tool/hand access and manufacturing tolerances are not verified.',
 'NOT RELEASED: this check does not establish strength, leak tightness, protection from moving fans or restart safety. Inherited M5 hardware remains incomplete. Indoor experimental use only; physical prototypes:0.']:
    y=para(700,y,s,450)
text(35,218,'FRONT STUD STACK / global y coordinates (mm); rear mirrored about y=180',13)
items=[(-72,-70,'tip'),(-70,-65,'service nut'),(-65,-64,'washer'),(-64,-55,'retainer'),(-19,-14,'fixed nut'),(-14,-13,'washer'),(-13,-12,'seal'),(-12,-3,'adapter'),(-3,-2,'washer'),(-2,3,'inner nut'),(3,8,'tip')]
# Dimensional strip: ring/filter space is intentionally open at the corner stud.
for i,(lo,hi,label) in enumerate(items):
    x=55+(lo+72)*12;w=(hi-lo)*12
    c.setFillColor(HexColor('#beddd8' if i%2 else '#dce5ec'));c.rect(x,143,w,24,fill=1)
    c.setStrokeColor(HexColor('#687d88'));c.line(x+w/2,143,x+w/2,126-(i%2)*35)
    c.saveState();c.translate(x+w/2,120-(i%2)*35);c.rotate(35)
    c.setFillColor(HexColor('#203848'));c.setFont('Helvetica',8)
    c.drawRightString(0,0,label+' '+str(lo)+'..'+str(hi));c.restoreState()
text(35,47,'Nominal thread projection: service2 mm / inner5 mm / ledge6 mm. Two-pitch1.4 mm comparison is an assumption, not a release criterion.',10)
text(35,25,'Original R02 preserved. Sources and reproducible commands: README.md beside this sheet. No prices, availability or physical results claimed.',10)
c.save();p=pdfium.PdfDocument(O/'D01_R02H_FASTENING_SERVICE.pdf');p[0].render(scale=1).to_pil().save(O/'sheet-1.png')
with (O/'HARDWARE_DELTA_BOM.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['item','quantity','status']);w.writerows([
    ['M4x80 studs replacing M4x70',8,'PROPOSED; grade/end treatment unknown'],
    ['M4x25 cap screws replacing M4x20 shafts',4,'DIMENSIONAL REFERENCE ONLY'],
    ['M4 nylon locking nuts 7AF x5',28,'DIMENSIONAL REFERENCE ONLY; reuse limits unknown'],
    ['M4 large washers 12OD x1; assumed4.3ID',32,'PROPOSED; material unselected'],
    ['Existing sealing washers 10OD/4ID/1 installed',12,'RETAINED; product/compression unknown']])
print('Generated checked CAD render, review PDF and hardware delta BOM.')
