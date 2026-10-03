"""Render actual D01 CAD tessellation and build an engineering PDF. No image AI.
Use Codex bundled Python (Pillow, ReportLab, pypdfium2); no installations.
"""
import json, math, csv, hashlib, zipfile, sys
import numpy as np
from pathlib import Path
from PIL import Image,ImageDraw,ImageColor
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
import pypdfium2 as pdfium

R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01'
C=json.loads((R/'cad/parametric/d01_r00.json').read_text())
M=json.loads((O/'cad_mesh.json').read_text());D=json.loads((O/'panel_geometry.json').read_text());P=json.loads((O/'pressure_results.json').read_text())
pdfmetrics.registerFont(TTFont('UI','C:/Windows/Fonts/segoeui.ttf'));pdfmetrics.registerFont(TTFont('UIB','C:/Windows/Fonts/segoeuib.ttf'))
INK='#203848';TEAL='#007e79';MUTED='#536875';PALE='#edf3f4';AMBER='#91601c'

def render(exploded=False):
    polygons=[];allpoints=[]
    def proj(p):
        x,y,z=p
        return (.7071*x+.7071*y,-.35355*x+.35355*y+.866*z,.61237*x-.61237*y+.5*z)
    for item in M:
        off=item['explode'] if exploded else (0,0,0)
        vv=[tuple(p[i]+off[i] for i in range(3)) for p in item['vertices']]
        pp=[proj(p) for p in vv];allpoints+=pp
        col=ImageColor.getrgb(item['color'])
        for tri in item['triangles']:
            pts=[vv[i] for i in tri];ps=[pp[i] for i in tri]
            a=[pts[1][i]-pts[0][i] for i in range(3)];b=[pts[2][i]-pts[0][i] for i in range(3)]
            n=(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]);norm=math.sqrt(sum(v*v for v in n)) or 1
            shade=.74+.26*abs((n[0]*.4-n[1]*.3+n[2]*.866)/norm)
            cc=tuple(int(v*shade) for v in col)
            if item['kind']=='guard':cc=tuple(int(v*.3+245*.7) for v in cc)
            polygons.append((sum(p[2] for p in ps)/3,ps,cc,item['kind'],pts,abs(n[2]/norm)>.99))
        # Pleat markings are visual annotation on OEM envelope, not modeled media geometry.
        if item['kind']=='filter':
            xs=[p[0] for p in vv];ys=[p[1] for p in vv];zs=[p[2] for p in vv]
            y=min(ys)-.1
            for j in range(1,38):
                x=min(xs)+j*(max(xs)-min(xs))/38
                q=[proj((x,y,min(zs)+10)),proj((x+1.8,y,min(zs)+10)),proj((x+1.8,y,max(zs)-10)),proj((x,y,max(zs)-10))]
                polygons.append((sum(p[2] for p in q)/4,q,(178,169,145),'pleat',None,False))
    xmin=min(p[0] for p in allpoints);xmax=max(p[0] for p in allpoints);ymin=min(p[1] for p in allpoints);ymax=max(p[1] for p in allpoints)
    w,h=1900,1550;s=min((w-160)/(xmax-xmin),(h-140)/(ymax-ymin))
    def xy(p):return ((p[0]-(xmin+xmax)/2)*s+w/2,h/2-(p[1]-(ymin+ymax)/2)*s)
    pixels=np.full((h,w,3),[244,247,247],dtype=np.uint8);depth=np.full((h,w),-np.inf,dtype=np.float32)
    for dep,ps,col,kind,world,horizontal in polygons:
        for k in range(1,len(ps)-1):
            ids=[0,k,k+1];t=[ps[i] for i in ids];q=[xy(p) for p in t]
            x0=max(0,int(math.floor(min(p[0] for p in q))));x1=min(w,int(math.ceil(max(p[0] for p in q)))+1)
            y0=max(0,int(math.floor(min(p[1] for p in q))));y1=min(h,int(math.ceil(max(p[1] for p in q)))+1)
            if x1<=x0 or y1<=y0:continue
            (ax,ay),(bx,by),(cx,cy)=q;den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
            if abs(den)<1e-8:continue
            yy,xx=np.mgrid[y0:y1,x0:x1];xx=xx+.5;yy=yy+.5
            aa=((by-cy)*(xx-cx)+(cx-bx)*(yy-cy))/den
            bb=((cy-ay)*(xx-cx)+(ax-cx)*(yy-cy))/den;cc=1-aa-bb
            zz=aa*t[0][2]+bb*t[1][2]+cc*t[2][2]
            mask=(aa>=-1e-7)&(bb>=-1e-7)&(cc>=-1e-7)&(zz>depth[y0:y1,x0:x1])
            if kind=='guard' and horizontal and world:
                wx=aa*world[ids[0]][0]+bb*world[ids[1]][0]+cc*world[ids[2]][0]
                wy=aa*world[ids[0]][1]+bb*world[ids[1]][1]+cc*world[ids[2]][1]
                row=np.rint(wy/(6*.8660254));hx=((wx-(row%2)*3+3)%6)-3;hy=wy-row*(6*.8660254)
                holes=(hx*hx+hy*hy)<4
                rim=globals().get('GUARD_RIM_MM',0)
                if rim:holes &= (wx>=115+rim)&(wx<=435-rim)&(wy>=20+rim)&(wy<=340-rim)
                mask &= ~holes
            depth[y0:y1,x0:x1][mask]=zz[mask];pixels[y0:y1,x0:x1][mask]=col
    im=Image.fromarray(pixels)
    out=O/('D01_EXPLODED.png' if exploded else 'D01_ASSEMBLY.png');im.save(out)
    return out

render();render(True)
pdf=canvas.Canvas(str(O/'AQI_D01_ENGINEERING_PACKAGE.pdf'),pagesize=A4)
pdf.setTitle('AQI Tower D01 prototype engineering package R00');pdf.setAuthor('AQI-TOWER project')
page=0;pw,ph=A4
def text(x,y,s,size=10,bold=False,color=INK):
    pdf.setFillColor(HexColor(color));pdf.setFont('UIB' if bold else 'UI',size);pdf.drawString(x,y,s)
def para(s,x,y,w,size=10,color=INK):
    st=ParagraphStyle('x',fontName='UI',fontSize=size,leading=size*1.4,textColor=HexColor(color))
    p=Paragraph(s,st);_,h=p.wrap(w,9999);p.drawOn(pdf,x,y-h);return y-h-10
def start(title,subtitle='',size=A4):
    global page,pw,ph
    if page:pdf.showPage()
    page+=1;pw,ph=size;pdf.setPageSize(size)
    pdf.setFillColor(white);pdf.rect(0,0,pw,ph,fill=1,stroke=0)
    text(38,ph-32,'AQI TOWER  /  D01-R00  /  03 OCT 2026',9,True,TEAL)
    text(38,ph-65,title,23,True)
    if subtitle:para(subtitle,38,ph-81,pw-76,10,MUTED)
    pdf.setStrokeColor(HexColor('#ced9df'));pdf.line(38,35,pw-38,35)
    text(38,21,'ENGINEERING PROPOSAL  |  Not released for fabrication or energizing',8,color=AMBER)
    text(pw-60,21,str(page),8)
def table(rows,widths,x,y,fs=9):
    style=ParagraphStyle('cell',fontName='UI',fontSize=fs,leading=fs*1.25)
    cells=[[Paragraph(str(v),style) for v in row] for row in rows]
    t=Table(cells,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#dcebea')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,HexColor('#d0dade')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f5f7f8')])]))
    w,h=t.wrap(9999,9999);assert y-h>43,(page,y,h);t.drawOn(pdf,x,y-h);return y-h-14
def arrow(x,y,X,Y,color=TEAL):
    pdf.setStrokeColor(HexColor(color));pdf.setFillColor(HexColor(color));pdf.setLineWidth(1.5);pdf.line(x,y,X,Y)
    ang=math.atan2(Y-y,X-x);p=pdf.beginPath();p.moveTo(X,Y);p.lineTo(X-8*math.cos(ang-.4),Y-8*math.sin(ang-.4));p.lineTo(X-8*math.cos(ang+.4),Y-8*math.sin(ang+.4));p.close();pdf.drawPath(p,fill=1,stroke=0)
def dim(x,y,X,Y,label):
    pdf.setStrokeColor(HexColor(MUTED));pdf.setLineWidth(.5);pdf.line(x,y,X,Y)
    if abs(y-Y)<.1:
        for a in (x,X):pdf.line(a,y-4,a,y+4)
        text((x+X)/2-pdfmetrics.stringWidth(label,'UI',8)/2,y+5,label,8)
    else:
        for a in (y,Y):pdf.line(x-4,a,x+4,a)
        pdf.saveState();pdf.translate(x-6,(y+Y)/2);pdf.rotate(90);text(-pdfmetrics.stringWidth(label,'UI',8)/2,0,label,8);pdf.restoreState()
def panel(d,x,y,s):
    pdf.setLineWidth(.7);pdf.setStrokeColor(HexColor(INK));pdf.setFillColor(HexColor(PALE));pdf.rect(x,y,d['w']*s,d['h']*s,fill=1)
    for a,b,w,h in d['rects']:pdf.setFillColor(white);pdf.rect(x+a*s,y+b*s,w*s,h*s,fill=1)
    for a,b,r in d['circles']:pdf.setFillColor(white);pdf.circle(x+a*s,y+b*s,r*s,fill=1)
    dim(x,y-15,x+d['w']*s,y-15,f"{d['w']:g}");dim(x-15,y,x-15,y+d['h']*s,f"{d['h']:g}")
    text(x,y+d['h']*s+15,d['name'].replace('_',' ')+f"  /  qty {d['qty']}  /  t={d['thick']:g}",10,True)

start('A prototype we can manufacture','An indoor particle-filtering demonstrator, built around our own housing, seals, controls and test method.')
pdf.drawImage(str(O/'D01_ASSEMBLY.png'),38,280,width=519,height=424)
y=para('Two large filter panels pull particles out of incoming air. Four small fans move that air upward. A sealed, serviceable box lets us measure whether the assembly actually works.',38,271,519,12)
y=table([['Proposed build','What exists now'],['550 mm wide cabinet; 631 mm overall height; about 473 mm filter-to-filter depth. External controls add 40 mm to width.','Native CAD, exported STEP, dimensioned panel drawings, pressure calculations and a connector-level electrical plan.'],['First goal: a measured indoor result, not a large outdoor claim.','Physical prototypes built: 0. No parts ordered. No physical results.']],[259,260],38,y,10)
para('RECOMMENDATION: fund one small demonstrator before the full cylindrical tower. The final outdoor goal remains; this is not a replacement claim or a purchased purifier presented as our invention.',38,y,519,10)

start('What changed and why','The immediate work is one assembly, not another cosmetic tower branch.')
y=table([['Usable previous work','Reason it is not a build release'],['Airflow / filter studies, FreeCAD scripts and pressure-budget logic.','Historical 1,332 m3/h CFD was partial/nonconverged; it does not validate this new assembly.'],['Measurement recorder and indoor decay-analysis scripts.','Synthetic software tests only. No instruments or measured air-cleaning result.'],['Cylindrical packaging and structural studies.','Heavy casing, unresolved fan duty, real filter fit and closure details stalled integration.']],[250,269],38,ph-125,10)
y=para('<b>The faster route.</b> Flat cut panels replace curved fabrication for this demonstrator. An external OEM power supply avoids designing an exposed mains power cabinet. The two filters share airflow in parallel, reducing the resistance each fan must overcome.',38,y,519,11)
y=para('<b>What D01 can validate.</b> Assembly method, replaceable seals, delivered airflow, electrical consumption, noise and repeatable indoor particle-decay measurements. MERV13 filters are NOT HEPA; D01 does not prove the old H13 stage, gas removal, water stage, outdoor bubble size or tower spacing.',38,y,519,11)
y=para('<b>Funding request.</b> Obtain quotations for the BOM, panel cutting, guard fabrication, assembly review, rental or paid airflow/pressure/power/noise measurement, and particle monitors. Total cost, freight, taxes and lead times are UNKNOWN. No guessed purchase total is presented.',38,y,519,11)
y=table([['Critical path','Owner / dependency'],['1. Resolve exact fan revision and obtainable filter; confirm sizes and filter curve.','Digital selection update + vendor evidence. No contact made.'],['2. Complete guard attachments, joints, seal and control safety review; issue R01 release.','Our drawings + paid mechanical/electrical review. No college lab assumed.'],['3. Purchase, cut panels, assemble and inspect.','User authorization; supplier delivery and fabricator schedule unknown.'],['4. Commission and run repeatable indoor trials.','Qualified physical checks + rented/bought instruments.'],['Next measurable milestone','One guarded, leak-checked operating assembly with measured total flow, watts and recorded test conditions.']],[260,259],38,y,9)
para('Digital engineering can proceed now. Delivery, fabrication and testing cannot be assigned honest completion dates until suppliers and services confirm them. No outdoor scale-up is on this release path.',38,y,519,10)

start('M00 General arrangement','Dimensions in mm. Proposed geometry; views not to scale. Guards are sheet envelopes, not certified perforation geometry.',landscape(A3))
# orthographic views from model bounding boxes, deliberate simplification with consistent datum.
def front(x,y,s):
    pdf.setFillColor(HexColor(PALE));pdf.setStrokeColor(HexColor(INK));pdf.rect(x,y+20*s,550*s,560*s,fill=1)
    pdf.setFillColor(HexColor('#eee5d4'));pdf.rect(x+27.35*s,y+57.35*s,495.3*s,495.3*s,fill=1)
    pdf.setFillColor(HexColor(TEAL));pdf.rect(x,y+30*s,550*s,550*s,fill=0)
    for j in range(1,32):pdf.setStrokeColor(HexColor('#c8bea7'));pdf.line(x+(27.35+j*495.3/32)*s,y+58*s,x+(27.35+j*495.3/32)*s,y+552*s)
    pdf.setStrokeColor(HexColor(INK));pdf.rect(x+115*s,y+580*s,320*s,51*s)
    for a in (25,495):pdf.rect(x+a*s,y,30*s,20*s)
    for a,b in [(20,z) for z in (55,305,555)]+[(530,z) for z in (55,305,555)]+[(275,50),(275,560)]:pdf.circle(x+a*s,y+b*s,2.75*s)
    dim(x,y-24,x+550*s,y-24,'550 cabinet');dim(x-25,y,x-25,y+631*s,'631 overall')
front(90,265,.63);text(90,695,'FRONT  /  air enters through filter',12,True)
x=530;y=265;s=.63
pdf.setStrokeColor(HexColor(INK));pdf.setFillColor(HexColor(PALE));pdf.rect(x,y+20*s,360*s,560*s,fill=1)
for a in (-56.45,360):pdf.setFillColor(HexColor('#eee5d4'));pdf.rect(x+a*s,y+57.35*s,56.45*s,495.3*s,fill=1)
pdf.setFillColor(HexColor('#d5e0e5'));pdf.rect(x+20*s,y+580*s,320*s,51*s,fill=1)
dim(x-56.45*s,y-24,x+416.45*s,y-24,'472.90 excluding stud ends');text(510,695,'SIDE  /  filters remove outward',12,True)
arrow(x-65,y+180,x-10,y+180);arrow(x+360*s+65,y+180,x+360*s+10,y+180);arrow(x+180*s,y+631*s+10,x+180*s,y+631*s+52)
pdf.drawImage(str(O/'D01_ASSEMBLY.png'),830,250,width=315,height=257)
para('Service: allow at least 150 mm clear space outside each retainer (proposal). Unplug and verify all fans stopped before tool-removing retainers. Fixed inner guard must remain in place even when a filter is removed.',830,650,310,11)
para('Cabinet datum: x=0 left, y=0 front seat, z=0 floor. Rear seat ends at y=360. Front filter y=-47.45 to -3; rear y=363 to407.45. Fan outlets point upward.',830,545,310,10)
table([['Interface','Nominal geometry / evidence'],['Filter support and seal','495.3 square x44.45 deep OEM envelope; 470 square intake; 12.65 mm support overlap/edge. 10 mm seal width needs actual frame landing check.'],['Fan plate','Four140 square fans; centres(200,105),(350,105),(200,255),(350,255); 125 square mounting pitch from OEM.'],['Service clamping','550 square retainer,475 opening,8 M5 studs per face; shelf supports filter weight. Foam4mm free to3mm installed is an assumption.'],['Structure','9mm plywood proposal with20x20 internal corner cleats and non-slip feet. Not a certified load or stability design.']],[170,880],65,205,10)

start('M00 Exploded assembly','Same CAD parts translated for assembly explanation. The exploded view is not another design option.',landscape(A3))
pdf.drawImage(str(O/'D01_EXPLODED.png'),40,100,width=785,height=640)
y=700
for title,body in [('1  Fan cassette','Four P14 Max envelopes, gaskets and through-bolts sit on a drilled top plate. Outer guard encloses rotating parts.'),('2  Cabinet','Base, two end panels and two aperture seats join against internal cleats. Seal every fixed seam; gasket the removable top.'),('3  Filter service','Each filter sits on its shelf, against a continuous gasket. A removable retainer spreads clamping around the paper frame.'),('4  Protection','A tool-fixed inner guard stops access to fan blades through a removed filter. Guard perforations and attachment strength still require detailed review.'),('5  External controls','Control enclosure is a space reservation only. Power supply stays external; cable route, gland and actual mounting need completion.')]:
    text(855,y,title,13,True,TEAL);y=para(body,855,y-15,290,11)-18
para('CAD simplifications: fan rotor is illustrative; filters are envelopes; guard sheets do not contain their perforation holes. Nuts, washers, cleat screws and guard flanges are not fully modeled. These exclusions prevent an honest fabrication release today.',855,y,290,10,AMBER)

start('M01 to M04 Panel drawings','All dimensions mm. DXFs are 1:1 review geometry, without kerf compensation. Do not scale the PDF to cut parts.',landscape(A3))
panel(D[0],90,435,.50);panel(D[1],455,390,.49);panel(D[2],775,390,.49)
panel(D[3],90,80,.49)
y=345
y=para('<b>Hole coordinates for M03 seat</b><br/>Datum lower left of532 x542 panel. Aperture lower left(31,41),470 x470.<br/>8 holes dia5.5: x=11 or521 at z=26,276,526; plus(266,21),(266,531).',430,y,320,11)
y=para('<b>Hole coordinates for M04 retainer</b><br/>Datum lower left of550 x550 panel. Aperture lower left(37.5,37.5),475 x475.<br/>8 holes dia5.5: x=20 or530 at z=25,275,525; plus(275,20),(275,530). Minimum centre-to-edge distance20mm on retainer. Use flat washers; verify bending and plywood bearing.',430,y,320,11)
para('<b>Proposed material and joints</b><br/>9mm sealed plywood,20x20 timber cleats. Pilot-drill; screw into cleats rather than panel edges. Adhesive/sealant must be compatible, fully cured and suitable for indoor exposure. Target panel dimensions +/-0.5mm and squareness within1mm are proposed, not achieved tolerances.<br/><br/>The retainer was widened to550mm to fix weak edge ligaments found during review. M5x100 studs now reach through the corner cleats. Cleat screw pitch, pull-out capacity, guard brackets and retainer stiffness still require completion.',785,345,345,11,AMBER)
panel(next(d for d in D if d['name']=='M05_SHELF'),455,100,.8)
para('Two ledges per filter: x30 to265 and285 to520. A20mm centre gap clears the lower clamp stud. Top surface at z57.35. Match-drill corner-cleat stud holes from the seat; short centre studs do not pass through cleats.',690,142,440,10)

start('M06 Fan plate and S01 filter seal','OEM fan dimensions establish the pattern. Filter sealing and clamping require physical fit confirmation.',landscape(A3))
fp=next(d for d in D if d['name']=='M06_FAN_PLATE');panel(fp,85,335,.85)
para('Fan centres from lower-left datum:<br/>(200,105), (350,105), (200,255), (350,255).<br/>Each fan: aperture dia134.2; four dia4.5 holes at centre +/-62.5 in x/y. Fan body140 x140 x27. Verify the delivered revision with the OEM1:1 template.',600,705,500,12)
para('Proposed mounting: M4x50 through-bolts, flat washers and locknuts,16 sets. Do not over-compress the fan frame. A1mm installed fan gasket is assumed. Seal around the cable entry; do not trap cables in the rotor or plate joint.',600,570,500,12)
text(65,265,'Filter edge section  /  schematic, not to scale',14,True)
for x,w,col,label in [(85,45,PALE,'Seat 9'),(130,20,INK,'Seal 3'),(150,180,'#eee5d4','Filter 44.45'),(330,45,TEAL,'Retainer 9')]:
    pdf.setFillColor(HexColor(col));pdf.rect(x,155,w,70,fill=1,stroke=0);text(x,117 if label=='Seal 3' else 135,label,10)
arrow(480,190,390,190);para('Clamp force comes from retained studs/fasteners. Do not use fan suction as the seal.<br/>Shelf takes gravity load. No adhesive on replaceable media.',490,233,295,11)
para('Seal landing: proposed10mm wide closed-cell foam around the495.3mm frame; butt joint sealed or use a continuous ring. Free4mm / installed3mm is only a starting compression assumption. Verify manufacturer force data, flatness, frame width and bypass before specifying torque or stops.',805,250,325,11)
para('Guard proposal: two320 x320 perforated faces,4mm holes on6mm triangular pitch (~40% open), with solid skirts. CAD shows sheet envelopes. Inner face z530, outer face z630. Final flanges, fixing holes, edge safety, blade clearance and finger-probe assessment must be detailed before release.',65,90,1060,10,AMBER)

start('E01 Power and control','Connector-level preliminary schematic. OEM preterminated cables only; no custom mains wiring.',landscape(A4))
nodes=[(38,'Site supply','Qualified socket / plug check'),(195,'NV-PS1','12V / 2A / 24W'),(352,'NA-FC1','Manual PWM setting'),(509,'NA-FH1','4-pin INPUT; SATA unused'),(666,'4 x P14 Max','4-pin fan OUTPUTS')]
for x,title,sub in nodes:
    pdf.setFillColor(HexColor(PALE));pdf.roundRect(x,ph-220,137,70,7,fill=1,stroke=0);text(x+8,ph-172,title,12,True);para(sub,x+8,ph-182,121,9)
for j in range(4):arrow(nodes[j][0]+137,ph-185,nodes[j+1][0]-4,ph-185)
text(193,ph-244,'NV-PS1 -> included NA-AC10 -> NA-FC1 input -> NA-FH1 PWM input -> ports1-4',10)
y=table([['Verified OEM basis','Design implication / unresolved check'],['NV-PS1:12V,2A,24W; external ClassII adapter. OEM supports FC1/FH1 combination.','Keep supply closed and outside cabinet. Supplied EU/US/UK plugs do not establish compatibility with the actual Indian socket.'],['NA-FH1:24W via4-pin input; eight outputs. NA-FC1 total current limit3A.','Use only4 fans. No SATA feed, no motherboard, no double powering. Route cables outside blade paths with strain relief.'],['Fan nominal current4 x0.35A=1.4A; nominal fan load16.8W.','7.2W margin before controller/hub losses and startup. Not a measured maximum or proven start-current budget.'],['Keyed OEM4-pin connectors; fan drawing identifies ground/power/tach/PWM.','No bare-terminal assignment or connector orientation invented. Confirm delivered manuals and third-party PWM compatibility before energizing.']],[365,400],38,ph-265,10)
para('<b>RELEASE GAP:</b> This chain may restart when power returns. It DOES NOT implement the existing tower manual-restart/interlock requirement. Do not silently waive that requirement. Before supervised testing, a qualified reviewer must either implement a rated restart-inhibit arrangement or explicitly approve a guarded bench-only exception with unplug-before-service controls. No unattended use. Speed=0 is not isolation.',38,y,765,11,AMBER)

start('The pressure budget','Screening scenarios at maximum fan speed. These are calculations, not a measured airflow rating.')
sys.path.insert(0,str(R/'scripts/analysis'));import d01_pressure as calc
gx,gy,gw,gh=70,455,455,205
for q in range(0,701,100):
    x=gx+q/700*gw;pdf.setStrokeColor(HexColor('#e1e8eb'));pdf.line(x,gy,x,gy+gh);text(x-8,gy-16,str(q),8)
for v in range(0,61,10):
    y=gy+v/60*gh;pdf.line(gx,y,gx+gw,y);text(gx-25,y-3,str(v),8)
def curve(f,col):
    pdf.setStrokeColor(HexColor(col));pdf.setLineWidth(2);p=pdf.beginPath()
    for j,q in enumerate(range(0,646,5)):
        if f(q)>60:break
        x=gx+q/700*gw;y=gy+f(q)/60*gh
        if j==0:p.moveTo(x,y)
        else:p.lineTo(x,y)
    pdf.drawPath(p)
curve(calc.fan,INK)
for p,col in [(5,'#50a89d'),(10,TEAL),(20,'#b07737')]:curve(lambda q:sum(calc.budget(q,p).values()),col)
text(70,680,'Pressure Pa',10);text(230,421,'Total airflow m3/h',10)
text(75,403,'Dark: fan  |  green:5Pa  |  teal:10Pa  |  brown:20Pa filter cases',9)
rows=[['At each calculated operating point','Low clean','Middle clean','Loaded case']]
for label,key in [('Flow m3/h','flow_m3h'),('Fan pressure Pa','fan_Pa')]:rows.append([label]+[f'{s[key]:.1f}' for s in P['scenarios']])
for label,key in [('Filter path Pa','filter_path'),('Intake/plenum Pa','intake_and_plenum'),('Inner guard Pa','inner_guard'),('Outer guard Pa','outer_guard'),('Installation reserve Pa','installation_reserve')]:rows.append([label]+[f"{s['budget_Pa'][key]:.2f}" for s in P['scenarios']])
y=table(rows,[235,94,94,96],38,383,9)
y=para('Four fans share the flow; their pressures do not add. Two filters each see half the flow; their pressure drops do not add. Assumed filter loss is5/10/20Pa at total400m3/h, scaling linearly. Other losses use K x rho x v^2 /2. Exact filter curve and installed guard losses remain UNKNOWN.',38,y,519,10)
para('The fan curve is visually digitized from the OEM chart. The +/-2Pa sensitivity gives about +/-11m3/h, but this is NOT a total uncertainty bound. The installation reserve is an allowance, not a verified static/total-pressure conversion. No CADR or cleaning percentage follows from these numbers.',38,y,519,10,AMBER)

BOM=[
('F01','2','S&P MERV13 990303 reference','495.3x495.3x44.45mm OEM','Dimensions verified; India availability and resistance curve UNKNOWN; not HEPA'),
('F02','4','ARCTIC P14 Max','140x140x27;125mm pitch;12V0.35A','OEM verified; SKU/color revision conflict. Checked India listings out of stock'),
('E01','1','Noctua NV-PS1 + included NA-AC10','12V2A24W external supply','OEM verified; India stock, plug compatibility and price UNKNOWN'),
('E02','1','Noctua NA-FC1','Manual PWM,3A maximum total','OEM verified; third-party fan behavior / current / availability to confirm'),
('E03','1','Noctua NA-FH1','24W via4-pin input','OEM verified; use4 outputs only; included input cable'),
('M01-06','12','Cut9mm plywood panels','Base1,end2,seat2,retainer2,shelf4,top1','Proposed; drawings/DXF supplied; material, joints and clamp strength unreleased'),
('M07','4','20x20 cleats,542mm long','Corner joinery support','Proposed; screw schedule and load review outstanding'),
('S01','~4m','10mm wide closed-cell foam','4mm free /3mm installed proposal','Exact product, force-compression, frame landing and leakage unknown'),
('S02','4','140mm fan gaskets','1mm installed proposal','Exact material / apertures / compression unknown'),
('H01','16 sets','12 M5x100 +4 M5x80 studs/nuts/washers','6 long side /2 short centre studs per face','Proposed; short centre studs avoid inner guard. Thread engagement / retention review needed'),
('H02','16 sets','M4x50 bolts/washers/locknuts','Fan mounting','Proposed; actual stack and rotor clearance to verify'),
('G01-02','2 cages','Perforated guards + solid skirts','320x320 faces; outer50 / inner41 high','4mm holes6mm triangular pitch proposal; attachment and reach review open'),
('M08','4','Non-slip feet','30x30x20 envelopes','Exact product / attachment / tip and slide checks unknown'),
('E04','1 set','Control enclosure/cable fittings','Reserved140x100x40 external space','Unselected; actual components and wiring layout not detailed'),
('H03','1 lot','Cleat screws, guard brackets, seam sealant, top gasket','Shop detail pending','NOT omitted from cost; quantities and products unresolved'),
('T01','1 service','Airflow / pressure / watt / sound measurement','Rent or hire equipped operator','No college lab assumed; quote and instrument suitability needed'),
('T02','2','Logging particle monitors + temp/RH','Co-locate before trials','Exact kit / calibration or comparison plan / quote pending'),
('R01','1 service','Mechanical + electrical review / commissioning','Defined in final page','Scope-specific paid service; no named engineer assumed')]
with (O/'D01_BOM.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['ID','quantity','product_or_item','basis','status']);w.writerows(BOM)
start('Parts and funding schedule','Exact OEM references are separated from proposed fabrication items. All prices and delivery dates remain unquoted.',landscape(A3))
table([['ID','Qty','Product / fabrication item','Technical basis','Status before purchase']]+BOM,[60,45,265,250,490],38,ph-120,9)

start('Assembly and physical trial','Work to the released revision only. This R00 supports design review and quotation, not immediate cutting.')
y=ph-120
for title,body in [
('1  Receive and measure','Check actual fan identity/pitch, filter size and edge frame, power accessories and manuals. Measure with calipers; record photos and serials. If they differ, update the CAD rather than force fitting.'),
('2  Make the cabinet','After joint/guard review: cut, deburr and seal panel edges. Square base/end/seat panels on cleats. Pilot-drill and attach the supports. Keep adhesive away from filter media; allow full specified cure.'),
('3  Fit the service parts','Install filter shelves and continuous gaskets. Seat filters with arrows inward. Fit retainers and retained fasteners, tighten evenly without crushing frames. Fit the gasketed removable fan plate and four outward-blowing fans.'),
('4  Fit and check guards and controls','Secure inner and outer guards with tool-required fasteners; verify no reachable blades, loose edges or blade contact. Mount controls and secure cables. Qualified person resolves restart behavior, socket/adapter, protection and startup current before energizing.'),
('5  Commission without pollutant generation','In a clean supervised room, measure cold start/current, all fan rotation, low/high settings, power-loss response and at least30min high-speed temperature/noise behavior. Stop on rubbing, smell, instability, loose guards or abnormal heating. This trial is not a thermal safety certification.'),
('6  Measure airflow and seals','Use a calibrated low-pressure instrument (roughly0-100Pa) and a competent low-loss flow hood/traverse method. A restrictive hood changes these low-pressure fans: document its correction/backpressure. Check all seams and compare with temporarily taped perimeter seams. A significant flow/particle change requires sealing repair; no visual seal claim alone.'),
('7  Run matched indoor trials','Record room volume, doors/windows, background conditions, monitor locations, fan setting, watts and filter pressure. Co-locate two monitors first. Run at least3 matched fan-off/fan-on decay pairs with comparable starting conditions, no occupants/pollutant sources and documented ventilation. Do not generate smoke, burn incense or handle test dust casually. If ambient particles are too low, book a controlled test service.'),
('8  Report what actually happened','Preserve raw files; use existing recorder/decay analysis with uncertainty and natural-decay comparison. Report measured flow, power, noise, repeatability and particle response. A low-cost PM sensor cannot certify MERV/HEPA efficiency. Negative or inconclusive results are valid results.')]:
    text(38,y,title,12,True,TEAL);y=para(body,38,y-17,519,10)-5
assert y>40,y

start('Evidence and the release boundary','What was checked, what is still missing, and what the next revision must close.')
y=table([['Evidence class','Current result'],['DETECTED digital checks','73 valid CAD objects; 435 enclosure/filter/support pairs and 1,280 fastener-to-part pairs have no positive-volume clashes. Nine arithmetic tests pass. Not strength, leakage or safety certification.'],['DETECTED and corrected','Retainer widened to 550 mm; minimum bolt edge distance 20 mm. Side studs reach cleats; shorter centre studs clear guard. Shelf split clears bottom stud. Guard flanges/joints and cleat fastening remain incomplete.'],['VERIFIED OEM facts','Fan envelope/pitch, filter reference dimensions and power/control product ratings have source links below. No exact procurement set is released.'],['ASSUMPTIONS','Panel/cleat material, seals/compression, guard loss, filter pressure scenarios and flow sharing. Hardware masses and structural capacity incomplete.'],['UNKNOWN physical results','Airflow, sealing, efficiency, CADR, noise, startup current, stability, surface temperatures, outdoor benefit. Physical prototypes: 0.']],[155,364],38,ph-122,10)
y=para('<b>Qualified review has a specific job:</b> check panel/cleat joints, retainer bending and edge distances, shelf loads, actual mass/centre of gravity, tip/slide resistance, guard reach/deflection and cable restraint. Electrical review checks the OEM chain, actual plug/socket, startup budget, automatic-restart gap and safe isolation. Commissioning verifies these on the built unit. This is not a request to redesign everything from scratch.',38,y,519,10)
y=para('<b>Public build precedent:</b> Tempest Brisa provides DXF/SVG construction files under CC0 1.0. One DXF and its licence are archived in data/prototype_d01/sources. The D01 enclosure is newly generated, not a rebranded Brisa or Dyson model. No upstream CADR result is inherited and no patentability claim is made.',38,y,519,10)
sources=[('ARCTIC drawing and mounting template','https://support.arctic.de/p14-max'),('ARCTIC specification and pressure chart','https://www.arctic.de/media/8a/18/01/1710507321/Spec_Sheet_P14_Max_EN.pdf'),('S&P MERV13 dimensional submittal','https://www.solerpalau-usa.com/documents/Submittal/trc-merv.pdf'),('Noctua power chain','https://www.noctua.at/en/products/nv-ps1'),('Noctua hub ratings','https://www.noctua.at/en/products/na-fh1/specifications'),('Noctua controller current limit','https://www.noctua.at/en/support/faqs/how-many-fans-can-i-connect-to-the-na-fc1-controller'),('Brisa source and CC0 licence','https://github.com/obife29/Tempest-Brisa-Open-Source'),('India listing checked: out of stock','https://mdcomputers.in/product/arctic-p14-max-140mm-case-fan-acfan00287a')]
text(38,y,'Sources checked 03 October 2026',11,True);y-=20
for label,url in sources:
    text(38,y,label,9,color=TEAL);pdf.linkURL(url,(38,y-2,555,y+11),relative=0);y-=18
para('Clickable source titles. OEM files are reference material, not open-source manufacturing licences. Availability can change; no supplier has confirmed stock, suitability, a quote or a date to this project.',38,y-3,519,9)
pdf.save()

qa=O/'qa';qa.mkdir(exist_ok=True)
doc=pdfium.PdfDocument(str(O/'AQI_D01_ENGINEERING_PACKAGE.pdf'))
for i in range(len(doc)):doc[i].render(scale=1.35).to_pil().save(qa/f'page-{i+1:02}.png')
print(json.dumps({'pdf_pages':len(doc),'pdf_bytes':(O/'AQI_D01_ENGINEERING_PACKAGE.pdf').stat().st_size,'rendered_pages':len(list(qa.glob('page-*.png')))}))
