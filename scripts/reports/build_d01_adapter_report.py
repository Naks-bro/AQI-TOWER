"""Render saved R02 CAD and make dimensioned review sheets, not fabrication approval."""
import ast,json,math,csv
from pathlib import Path
import numpy as np
from PIL import Image,ImageColor
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/r02_adapter'
M=json.loads((O/'cad_mesh.json').read_text());GUARD_RIM_MM=10
fn=next(n for n in ast.parse((R/'scripts/reports/build_d01_delivery.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='render')
exec(compile(ast.Module(body=[fn],type_ignores=[]),'shared_renderer','exec'),globals())
render()
panels=json.loads((O/'panels.json').read_text());audit=json.loads((O/'checks.json').read_text())
assert audit['STEP_volume_matches'] and not audit['clashes_mm3']
out=O/'panel_dxf_REVIEW_ONLY';out.mkdir(exist_ok=True)
for panel in panels:
    a=['0','SECTION','2','HEADER','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES']
    for x,y,w,h in [(0,0,panel['w'],panel['h']),panel['opening']]:
        corners=[(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]
        for (ax,ay),(bx,by) in zip(corners,corners[1:]):a+=list(map(str,['0','LINE','8','OUTLINE','10',ax,'20',ay,'30',0,'11',bx,'21',by,'31',0]))
    for x,y,r in panel['holes']:a+=list(map(str,['0','CIRCLE','8','DRILL','10',x,'20',y,'30',0,'40',r]))
    a+=['0','ENDSEC','0','EOF'];(out/(panel['name']+'.dxf')).write_text('\n'.join(a)+'\n')
c=canvas.Canvas(str(O/'D01_R02_ADAPTER_DRAWINGS.pdf'),pagesize=(1191,842))
def text(x,y,s,size=12,col='#203848'):
    c.setFillColor(HexColor(col));c.setFont('Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,width,size=12):
    for line in simpleSplit(s,'Helvetica',size,width):text(x,y,line,size);y-=17
    return y-12
def header(title,n):
    text(35,807,'AQI TOWER / D01-R02 / EXPERIMENTAL REMOVABLE FILTER CASSETTE',11,'#008b7f')
    text(35,772,title,25)
    text(35,22,'03 OCT 2026 | REVIEW ONLY - NOT FOR CUTTING, PROCUREMENT OR ENERGIZING | Physical prototypes: 0',10)
    text(1140,22,str(n),10)
header('One cabinet, interchangeable filter modules',1)
c.drawImage(str(O/'D01_ASSEMBLY.png'),35,95,width=700,height=571)
y=710
for title,body in [('What changed','Two reducing plates adapt the same R01 cabinet to the published370 x290 x40 mm STARKVIND envelope. Existing cabinet, fans, guards and outer seals are retained.'),
('Sealing route','Cabinet -> original495.3/475.3 mm gasket -> reducing plate -> assumed370/350 by290/270 mm gasket -> filter. Seal all new mounting feedthroughs; no unsealed screw holes into the plenum.'),
('Positive support','Two proposed bent ledges per filter carry weight separately from clamping friction. Four M4 studs retain each removable frame. Final heads/nuts, bracket bends and strength remain unselected.'),
('Digital checks',f"{audit['objects']} valid objects; {audit['new_pair_checks']} new-part pair checks without positive-volume clashes. Native reopen and STEP volume checks pass. Original R01 hash unchanged."),
('Do not transfer old airflow','Smaller openings and a different filter invalidate earlier flow estimates. Pressure curve, bypass, installed flow and particle removal remain unmeasured. OEM permits intended use only in STARKVIND appliances; this custom use is experimental.')]:
    text(760,y,title,15);y=para(760,y-25,body,390)
c.showPage();header('Reducer and retainer / proposed panel geometry',2)
for i,p in enumerate(panels):
    x0=65+i*570;y0=310;scale=.6
    c.setStrokeColor(HexColor('#203848'));c.setLineWidth(.8)
    c.rect(x0,y0,p['w']*scale,p['h']*scale)
    x,y,w,h=p['opening'];c.rect(x0+x*scale,y0+y*scale,w*scale,h*scale)
    for x,y,r in p['holes']:c.circle(x0+x*scale,y0+y*scale,r*scale)
    text(x0,696,p['name']+' / quantity2 / thickness9 mm',15)
    text(x0,670,f"Outside {p['w']} x{p['h']} mm; opening350 x270 mm",12)
    text(x0,280,'Datum: lower-left outside face. All coordinates in mm.',11)
    text(x0,255,'Opening lower-left: '+str(p['opening'][:2]),11)
    groups={}
    for x,y,r in p['holes']:groups.setdefault(r,[]).append(f'({x:g},{y:g})')
    yy=232
    for radius,coords in groups.items():yy=para(x0,yy,f'Dia{2*radius:g}: '+', '.join(coords),495,10)
    para(x0,yy,'Rear module mirrored physically. DXFs supplied for geometry review only. Hole sizes are proposals, not selected fastener tolerances.',495,10)
para(35,90,'Front section (global y, mm): cabinet0; old gasket -3..0; reducer -12..-3; new gasket -15..-12; filter -55..-15; retainer -64..-55. Rear is mirrored about y180. New gasket border and frame contact remain assumptions.',1100,11)
c.save()
pdf=pdfium.PdfDocument(O/'D01_R02_ADAPTER_DRAWINGS.pdf');assert len(pdf)==2
for i,page in enumerate(pdf):page.render(scale=1).to_pil().save(O/f'sheet-{i+1}.png')
with (O/'ADAPTER_DELTA_BOM.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['item','quantity','basis','status'])
    w.writerows([['Reducing plate',2,'550x550x9;350x270 opening','PROPOSED'],['STARKVIND104.633.30',2,'370x290x40 published envelope','EXPERIMENTAL NOT SELECTED FOR PURCHASE'],['Filter gasket',2,'370x290 outer;350x270 inner;3 installed','LANDING/COMPRESSION UNKNOWN'],['Retaining frame',2,'410x330x9;350x270 opening','PROPOSED'],['M4x70 studs',8,'shaft envelope','NUTS/WASHERS/RETENTION UNSELECTED'],['Bent support ledges',4,'30wide;43shelf;20downstand;2thick','BEND/GRADE/STRENGTH UNKNOWN'],['M4x20 support bolts',4,'shaft envelope','HEAD/NUT UNSELECTED'],['Feedthrough sealing washers',12,'10OD/4ID/1 installed envelopes','EXACT PRODUCT/COMPRESSION UNKNOWN']])
print('CAD render, two PDF sheets, two DXFs and delta BOM generated.')
