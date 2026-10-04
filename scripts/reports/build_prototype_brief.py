"""Build the stakeholder PDF and QA page images; no engineering simulation."""
from pathlib import Path
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports' / 'prototype_delivery'
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / 'AQI_TOWER_PROTOTYPE_STAKEHOLDER_BRIEF.pdf'
for name, file in [('Body','segoeui.ttf'),('Bold','segoeuib.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / file)))
W,H=595.28,841.89
INK=HexColor('#163b46'); TEAL=HexColor('#16796c'); MUTED=HexColor('#526c73')
PALE=HexColor('#edf5f3'); GOLD=HexColor('#bd7a22'); BLUE=HexColor('#4285a8')
c=canvas.Canvas(str(PDF), pagesize=(W,H))
c.setTitle('AQI Tower prototype proposal and progress')
c.setAuthor('AQI Tower project team')
def text(x,y,s,size=11,color=INK,font='Body'):
    c.setFillColor(color); c.setFont(font,size); c.drawString(x,y,s)
def para(s,x,y,width=499,size=11,color=INK):
    p=Paragraph(s,ParagraphStyle('p',fontName='Body',fontSize=size,leading=size*1.45,textColor=color))
    _,h=p.wrap(width,700)
    if y-h<53: raise ValueError(f'Page overflow: {s[:50]}')
    p.drawOn(c,x,y-h); return y-h
def heading(s,y):
    text(48,y,s,15,INK,'Bold'); return y-15
def section(title,body,y):
    y=heading(title,y); y=para(body,48,y-4); return y-23
def start(n,kicker,title,sub):
    c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
    text(48,H-43,'AQI TOWER',11,TEAL,'Bold');text(395,H-43,'3 OCTOBER 2026',9,MUTED)
    text(48,H-80,kicker,10,TEAL,'Bold');text(48,H-116,title,25,INK,'Bold')
    y=para(sub,48,H-136,size=11,color=MUTED)
    text(48,28,'Prototype proposal | Working project name | Not a fabrication release',8,MUTED)
    text(520,28,f'{n} / 6',9,MUTED)
    return y-28
def arrow(x1,y1,x2,y2,color=TEAL):
    c.setStrokeColor(color);c.setFillColor(color);c.setLineWidth(2);c.line(x1,y1,x2,y2)
    a=math.atan2(y2-y1,x2-x1);p=c.beginPath();p.moveTo(x2,y2)
    p.lineTo(x2-9*math.cos(a-.4),y2-9*math.sin(a-.4));p.lineTo(x2-9*math.cos(a+.4),y2-9*math.sin(a+.4));p.close();c.drawPath(p,fill=1,stroke=0)
def tower(x,y,w,h):
    c.setFillColor(PALE);c.setStrokeColor(TEAL);c.setLineWidth(1.5)
    c.roundRect(x,y,w,h,18,fill=1,stroke=1)
    layers=[(.12,.13,'Coarse filter',GOLD),(.30,.22,'HEPA filter',BLUE),(.59,.24,'Fan',TEAL)]
    for f,ht,label,color in layers:
        c.setFillColor(color);c.roundRect(x+12,y+h*f,w-24,h*ht,5,fill=1,stroke=0)
        text(x+20,y+h*f+h*ht/2-4,label,10,white,'Bold')
    arrow(x+w/2,y+h*.88,x+w/2,y+h+24)
    arrow(x-35,y+h*.08,x+10,y+h*.08)
    text(x+8,y+h+36,'Filtered air out',10,TEAL)
    text(x-30,y-20,'Illustrative layout only',9,MUTED)
def link(label,url,y):
    text(48,y,label,10,TEAL,'Bold');c.linkURL(url,(48,y-3,546,y+13),relative=0)
    return y-27

# One-page executive summary, with no meetings page.
y=start(1,'EXECUTIVE SUMMARY','A prototype we can demonstrate','We are asking for support to turn our digital air-cleaning studies into one safely built and measured indoor prototype.')
y=section('Vision for 2026','Build and test one air-cleaning prototype. Use its results to decide whether a larger outdoor tower is worth developing. Outdoor coverage is not proven.',y)
y=section('Work completed','Airflow studies, filter-bypass investigation, cylindrical packaging studies, service-access checks and measurement software. This is digital development; physical prototypes built: <b>0</b>.',y)
y=section('Key decisions','Start with a fan, coarse filter and sealed HEPA filter. Use standard bought parts and a local workshop. Keep solar, water and gas-treatment experiments out of the first demonstration.',y)
y=section('Unresolved challenges','Choose a fan that can handle filter resistance; confirm real parts, seals, supports and safe wiring. Then measure actual airflow, particle reduction, power and noise.',y)
y=section('Support requirements','Fund the first component selection and reviewed build, instruments and paid testing. College and NGO support is financial; no college lab is assumed.',y)
y=section('Plan for the upcoming month','Obtain component and workshop quotations, select a demonstration route, complete reviewed part-specific drawings and arrange assembly/testing. Dates depend on confirmed parts and service availability.',y)
para('<b>Decision requested:</b> support one bounded indoor prototype and its measurements, not an unverified city-scale clean-air claim.',48,y,size=12,color=TEAL)
c.showPage()

y=start(2,'THE PROPOSED PROTOTYPE','How the tower would work','A cylindrical appearance is an option. The first working core must filter air safely before we spend on the finished outer shell.')
tower(85,210,168,350)
for yy,title,body in [(535,'1  Draw room air in','A guard keeps people away from moving parts.'),(456,'2  Catch larger dust','A removable coarse filter protects the next stage.'),(368,'3  Filter fine particles','A HEPA element needs a sealed frame so air cannot go around it.'),(270,'4  Return filtered air','An OEM fan pulls air through the filters. Its actual delivered flow must be measured.')]:
    text(291,yy,title,12,INK,'Bold');para(body,291,yy-14,250,size=10.5)
para('The structure, guards, service hatch and electrical enclosure are part of the prototype, not optional decoration. The drawing shows functions, not final sizes or wiring.',48,158,size=11)
para('<b>What we will measure:</b> airflow, filter pressure, room particle trends, electrical power, noise and installed filter sealing. No virus-removal or health-protection claim is proposed.',48,101,size=10.5)
c.showPage()

y=start(3,'ACTUAL PROJECT PROGRESS','What already exists','The project has digital evidence to show now. It does not yet have measured performance from a physical machine.')
img=ROOT/'reports/stakeholder_report/assets/threejs_3d_view.png'
c.drawImage(str(img),48,415,width=499,height=265,preserveAspectRatio=True,anchor='c')
text(48,399,'Existing project viewer: historical digital geometry and airflow study',9,MUTED)
y=section('Airflow and filters', 'We investigated the air path and a modeled leak around the HEPA filter. A historical simulation predicted about <b>1,332 m3/h</b>; it was partial and not fully converged. This is not a tested tower rating.',365)
y=section('Packaging and maintenance','FreeCAD studies explored a cylinder, actual-depth filter envelopes, supports and a removable service hatch. Nominal fit checks do not establish structural strength or leak-tightness.',y)
y=section('Monitoring and build preparation','Offline recording and analysis tools are available. Functional start/stop plans and supplier questions are prepared. No sensors connected, supplier order or physical commissioning is recorded.',y)
para('<b>GEO_C</b> is simply the internal name of an airflow layout tested on the computer. It is not a product name, a manufactured tower or a safety approval.',48,y,size=10.5,color=TEAL)
c.showPage()

y=start(4,'REAL ONLINE REFERENCES','We can learn from existing designs','We can reuse documented ideas and standard components, while keeping outside results separate from our own evidence.')
# Original explanation of the published multi-filter principle, not a copied OEM graphic.
c.setFillColor(PALE);c.roundRect(48,423,200,226,10,fill=1,stroke=0)
c.setFillColor(BLUE);c.rect(70,444,34,129,fill=1,stroke=0);c.rect(192,444,34,129,fill=1,stroke=0)
c.setFillColor(TEAL);c.roundRect(70,579,156,37,5,fill=1,stroke=0)
text(120,592,'FAN',13,white,'Bold');arrow(148,619,148,641)
arrow(51,504,116,504);arrow(243,504,179,504)
text(83,430,'Multiple filter faces',10,INK)
text(48,402,'Original diagram of a published principle',9,MUTED)
text(275,636,'Public construction precedent',14,INK,'Bold')
para('EPA describes and tested DIY indoor air cleaners with fans and MERV 13 filters, including multi-filter arrangements. These give us a concrete example of fan-and-filter construction. <b>MERV 13 is not HEPA.</b>',275,615,272,size=11)
para('The EPA fan safety guidance is specific to its tested designs and US equipment. It does not approve an arbitrary Indian 230 V fan or our tower. Local compatibility and qualified review remain necessary.',275,488,272,size=10.5)
y=section('Real component references', '<b>S&amp;P TD-SILENT ECOWATT:</b> published fan curves and drawings; our comparison candidate is not selected and is not confirmed adequate at the assumed loaded duty.<br/><br/><b>Sensirion SEK-SPS30:</b> a published particle-sensor evaluation kit candidate for logging. Actual kit, Windows setup, calibration/reference checks and supply remain to be confirmed.',366)
para('Our originality must be assessed separately. Referencing a public design does not make the entire project patentable, nor transfer its test results to our machine.',48,y,size=10.5)
link('EPA public construction and research reference', 'https://www.epa.gov/air-research/research-diy-air-cleaners-reduce-wildfire-smoke-indoors',100)
c.showPage()

y=start(5,'A FASTER SHOWABLE MILESTONE','Demonstrate first and build honestly','Two different routes can help us move. A purchased reference appliance must never be presented as our own completed tower.')
y=section('Route A  A reference demonstration','<b>Optional scope for team approval.</b> Use an unmodified, locally supported commercial indoor purifier beside the project display and particle logging. This demonstrates filtration and our measurement workflow without designing a new mains appliance for the event. A Philips AC3059/65 India product page is one real reference; stock, price and suitability are unconfirmed.',y)
y=section('What Route A delivers','A working reference appliance, instrument setup and recorded demonstration data, if arranged and tested. Label all results with the exact appliance used. This is not our tower prototype, proof of our CAD or an outdoor demonstration.',y)
y=section('Route B  Our custom fan and filter core','Build our guarded, sealed core using OEM parts and a reviewed workshop assembly. It preserves our tower direction, but still needs a selected fan/filter, safe supports/seals and rated electrical design. Current study CAD is not a cutting or wiring instruction.',y)
y=section('Why we cannot order the old fan blindly','At a study flow of 1,300 m3/h, loaded-filter assumptions require about <b>326-413 Pa</b> of static pressure. The S&amp;P comparison chart estimate is about <b>230 Pa</b>. These are unmeasured scenarios, but enough to show that selection needs attention.',y)
y=section('What can be shown immediately','This report, the offline clickable prototype explainer and the existing digital viewer. A non-operating physical appearance mock-up is another optional milestone. None should be labelled a physically validated purifier.',y)
para('<b>Time:</b> no supplier or workshop date is booked. An off-the-shelf reference demo avoids custom fabrication, but delivery and logging still need confirmation. The custom tower has a separate reviewed build schedule.',48,y,size=10.5,color=TEAL)
c.showPage()

y=start(6,'SUPPORT AND NEXT ACTION','What funding will unlock','We need a small, accountable first build stage rather than a promise of a finished outdoor network.')
y=section('Support requirements','Fund component quotations and qualified design review; then approve selected parts, workshop assembly and paid commissioning/testing. Obtain particle monitoring and arrange airflow, power, noise and filter-integrity checks. Costs are <b>UNKNOWN until quoted</b>.',y)
y=section('Plan for the upcoming month','Choose reference demonstration, custom core or both as separately labelled scopes. Confirm a usable indoor room and supply. Obtain fan/filter and service quotes. Revise drawings against real parts, review them and build only the released scope. Record actual results without creating smoke or hazardous pollutant challenges.',y)
y=section('The longer-term outdoor vision','One tower may be investigated as a local cleaner-air zone. Several towers could later form a network. Wind, surrounding pollution and placement must be tested; there is no proven bubble size, cleaning percentage or tower spacing.',y)
# Bubble network illustration is explicitly a hypothesis, not a map.
c.setStrokeColor(TEAL);c.setDash(4,4);c.line(138,320,458,320);c.setDash()
for xx in (138,298,458):
    c.setStrokeColor(TEAL);c.setFillColor(PALE);c.circle(xx,320,68,fill=1,stroke=1)
    c.setFillColor(TEAL);c.roundRect(xx-12,292,24,55,7,fill=1,stroke=0)
text(65,232,'Future local-zone network concept only - circles are not measured coverage',9,MUTED)
text(48,205,'Public references checked 3 October 2026',12,INK,'Bold')
yy=182
for label,url in [('EPA fan-and-filter construction research','https://www.epa.gov/air-research/research-diy-air-cleaners-reduce-wildfire-smoke-indoors'),('Philips AC3059/65 India reference appliance','https://www.philips.co.in/c-p/AC3059_65/series-3000i'),('S&P published fan catalogue - existing local archive','https://statics.solerpalau.com/media/import/documentation/EN_TD-SILENT-ECOWATT.pdf'),('Sensirion SEK-SPS30 sensor kit - earlier OEM check','https://sensirion.com/products/catalog/SEK-SPS30')]: yy=link(label,url,yy)
para('Local evidence: project status, CAD, historical CFD and measurement tools. Fan/kit web refreshes failed; earlier checked references are used. No purchase or supplier commitment is implied.',48,82,size=8.5,color=MUTED)
c.showPage();c.save()
doc=pdfium.PdfDocument(str(PDF))
assert len(doc)==6
for i in range(len(doc)):
    page=doc[i];page.render(scale=1.4).to_pil().save(OUT/f'qa_page_{i+1}.png');page.close()
doc.close()
print(f'Created {PDF} (6 pages) and QA renders')
