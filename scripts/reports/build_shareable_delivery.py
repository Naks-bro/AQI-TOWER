"""Two audience bundles from existing R03M/IH02 evidence, not a release.
Requires ReportLab, Pillow, openpyxl, pypdf, pypdfium2; use bundled runtime.
"""
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line, String
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium

R = Path(__file__).resolve().parents[2]
O = R/'reports/shareable_20261005'
V = O/'visuals'
IH = R/'reports/prototype_d01/internal_handoff_20261005'
M = R/'reports/prototype_d01/mechanical_package'
S = O/'stakeholder'
T = O/'technical'
for d in (S,T,O/'qa'):
    d.mkdir(parents=True,exist_ok=True)
mesh = json.loads((M/'cad_mesh.json').read_text())
sys.path.insert(0,str(R/'scripts/analysis'))
from d01_validation import pressure_rows
pressure = pressure_rows()
batch_summary=R/'reports/prototype_d01/batch_summary'
batch_summary.mkdir(exist_ok=True)
(batch_summary/'CURRENT_PRESSURE_BUDGET.json').write_text(json.dumps(pressure,indent=2)+'\n',encoding='utf-8')
central = next(x for x in pressure['rows'] if x['total_m3h']==300 and x['reducer_K']==1)
assert abs(central['filter_allowance_Pa']-14.316071817116585)<1e-8
assert len(mesh)==493
assert hashlib.sha256((M/'D01_R03M_ASSEMBLY.FCStd').read_bytes()).hexdigest()=='fb28a31315968509dcdbbb2caac8c6d69c84ecb94a35ccd75937a5d9ecaa33a6'

# Self-contained offline viewer; actual mesh coordinates rounded only for display.
display_mesh=[{k:p[k] for k in ('name','kind','explode','note','triangles')} |
              {'vertices':[[round(x,3) for x in v] for v in p['vertices']]} for p in mesh]
html=(R/'threejs/presentation.template.html').read_text(encoding='utf-8')
html=html.replace('__CAD_DATA__',json.dumps(display_mesh,separators=(',',':')).replace('</','<\\/'))
html=html.replace('__VIEWER_CODE__',(V/'viewer.js').read_text(encoding='utf-8'))
(O/'AQI_TOWER_3D_REVIEW.html').write_text(html,encoding='utf-8')
shutil.copy2(R/'threejs/node_modules/three/LICENSE',O/'THREE_JS_LICENSE.txt')

fontpath=Path('C:/Windows/Fonts/arial.ttf')
font=ImageFont.truetype(str(fontpath),14)
for directory,output,label in [('frames','assembly_exploded.gif','CAD assembly explanation | R03M | NOT build-approved'),
                              ('air_frames','illustrative_airflow.gif','ILLUSTRATIVE AIR PATHS | NOT CFD or measured performance')]:
    frames=[]
    for path in sorted((V/directory).glob('*.png')):
        im=PILImage.open(path).convert('RGB')
        draw=ImageDraw.Draw(im)
        draw.rectangle((0,0,im.width,40),fill='#173d49')
        draw.text((12,11),label,fill='white',font=font)
        frames.append(im)
    assert len(frames)==24, f'Incomplete Blender render: {directory}'
    frames[0].save(V/output,save_all=True,append_images=frames[1:],duration=167,loop=0)

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyAQI',fontName='Helvetica',fontSize=11,leading=16,spaceAfter=10,textColor=HexColor('#263d48')))
styles.add(ParagraphStyle(name='SmallAQI',fontName='Helvetica',fontSize=9,leading=12,spaceAfter=8,textColor=HexColor('#536b73')))
styles['Title'].fontSize=30;styles['Title'].leading=35;styles['Title'].textColor=HexColor('#174b58')
styles['Heading1'].fontSize=21;styles['Heading1'].leading=26;styles['Heading1'].textColor=HexColor('#174b58')
styles['Heading2'].fontSize=13;styles['Heading2'].leading=17;styles['Heading2'].textColor=HexColor('#174b58')
def p(t,small=False):return Paragraph(t,styles['SmallAQI' if small else 'BodyAQI'])
def h(t):return Paragraph(t,styles['Heading1'])
def sub(t):return Paragraph(t,styles['Heading2'])
def picture(path,width=460):
    im=PILImage.open(path)
    return Image(str(path),width=width,height=width*im.height/im.width)
def table(header,rows,widths):
    tab=Table([[p(escape(str(x)),True) for x in row] for row in [header]+rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#d8eceb')),('GRID',(0,0),(-1,-1),.4,HexColor('#d1dcdf')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f1f6f7')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return tab
def footer(c,d):
    c.setFillColor(HexColor('#174b58'));c.rect(0,0,595,31,fill=True,stroke=False)
    c.setFillColor(white);c.setFont('Helvetica',8)
    c.drawString(36,12,'AQI Tower | 5 October 2026 | Digital review only | Physical prototypes 0')
    c.drawRightString(557,12,str(d.page))
def pdf(name,story):
    SimpleDocTemplate(str(name),pagesize=(595,842),leftMargin=38,rightMargin=38,topMargin=34,bottomMargin=46).build(story,onFirstPage=footer,onLaterPages=footer)
def bubbles():
    d=Drawing(515,165)
    for i in range(3):
        x=93+i*164
        d.add(Circle(x,90,61,fillColor=HexColor('#e8f5f1'),strokeColor=HexColor('#69aaa4'),strokeDashArray=[4,4]))
        d.add(Rect(x-12,62,24,58,fillColor=HexColor('#246f7a'),strokeColor=None))
        d.add(String(x,43,'Future tower',textAnchor='middle',fontSize=10,fillColor=HexColor('#174b58')))
        if i<2:d.add(Line(x+65,90,x+98,90,strokeColor=HexColor('#69aaa4'),strokeWidth=2))
    d.add(String(257,8,'Concept only. No measured radius, spacing or guaranteed protected zone.',textAnchor='middle',fontSize=9))
    return d

six=[('Vision for 2026','Build and safely test one indoor prototype. Use those results to decide whether a larger outdoor tower is worth developing.'),
     ('Work completed','An integrated CAD model, mechanical drawings, an electrical reference plan, calculations and physical-test instructions are ready for review. No physical unit has been built.'),
     ('Key decisions','Start with particle filtration indoors. Use a custom housing with two parallel filters and four fans. Keep water, gas-filter media and solar outside this first build.'),
     ('Unresolved challenges','Actual filter resistance, sealing, guard strength, cabinet stability and electrical protection still need closure. Outdoor coverage is unknown.'),
     ('Support requirements','Fund exact parts after approval, qualified design review, local fabrication, safe assembly and rented or paid measurement services. We do not assume a college lab.'),
     ('Plan for upcoming month','Assign reviewers, resolve supplier inputs, agree test targets and collect quotes. Release and build only after approval. Choose a final project name. Dates depend on responses and workshop capacity.')]
stake=[Paragraph('AQI Tower',styles['Title']),p('Prototype development and funding review'),
       p('We are preparing a small air-cleaning prototype. We need support to finish the engineering review, build it safely and measure whether it works.'),picture(V/'assembly.png',470),
       p('Actual CAD-derived rendering, not a physical product photo. Purple parts reserve control-box and cable space. Guard openings are not represented accurately.',True),
       p('<b>Current position:</b> digital design exists; construction and performance are not yet approved. AQI Tower is a working name.'),PageBreak(),
       h('Report 1 Executive Summary'),p('A short update for the college, NGO and funding team.')]
for title,body in six:stake += [sub(title),p(body)]
stake += [PageBreak(),h('Report 2 Comprehensive Report'),sub('Vision for 2026'),p(six[0][1]),
          sub('Project idea and the clean air bubble'),p('The long-term idea is a larger outdoor cylindrical tower. Each tower would aim to improve air near people. Several towers might form a chain of local cleaner-air zones.'),bubbles(),
          p('A bubble is a simple way to explain the goal. It is not a sealed dome or a proven clean-air boundary. Outdoor wind mixes air continuously, so we cannot promise a bubble size or cleaning percentage.'),
          p('The current prototype is a small rectangular indoor unit, not the final outdoor tower. Keeping the first build simple helps us inspect, transport, measure and repair it.'),
          sub('Where it may be used later'),p('Potential sites include sheltered waiting areas and other managed public locations. No site has been selected. Fully outdoor use needs separate heat, rain, dust, corrosion, anchoring and vandal-resistance design.'),PageBreak(),
          h('How the prototype works'),picture(V/'cutaway.png',415),
          table(['Part','Simple explanation'],[['Two filters','Air enters through two opposite filter branches. They work side by side, not in sequence.'],['Four fans','Pull air into a shared chamber and discharge it through the top.'],['Cabinet seals and guards','Keep the parts supported, limit leaks and restrict access to moving fans. These details still need approval.']],[135,384]),
          p('Cutaway view removes panels and guards for explanation. Never operate an unguarded unit. Colours identify parts; they do not show measured pollution, flow speed or efficiency.',True),PageBreak(),
          h('Work completed'),picture(V/'exploded.png',390),
          p('The current model coordinates the cabinet, filters, seals, fan plate, guards and proposed hardware. A parallel engineering review has added filter-fit tolerance checks, joint-load calculations, power and wiring screens, and an updated parts register. These calculations help find problems before we buy or build.'),
          sub('What the computer work tells us'),p('We can check nominal fit and explore pressure losses. We cannot yet state actual airflow, cleaning efficiency, noise, power or filter lifetime. The fan and filter must work together under load.'),
          sub('Important evidence boundary'),p('Earlier coloured CFD studies belong to a different large-tower geometry. They were partial or nonconverged and do not validate this prototype. The new animation explains assembly and the intended air path; it is not a new CFD result.'),PageBreak(),
          h('Key decisions and unresolved challenges'),sub('Key decisions'),p(six[2][1]),
          table(['Question','Current answer'],[['Has a tower been physically tested?','No. Physical prototypes built: 0.'],['Are parts and wiring released?','No. The integrated design is for review only.'],['Will it remove gases?','Not demonstrated. The first scope is particle filtration.'],['Does it have a verified HEPA rating?','No whole-device HEPA classification.'],['How large is the outdoor bubble?','Unknown. Outdoor benefit and spacing need field measurements.'],['Are costs and dates confirmed?','No. Quotes, supply times and fabrication capacity are still unknown.']],[235,284]),
          p('The main missing work is component evidence, mechanical and electrical approval, then construction and controlled measurements. Another attractive model does not close those items.'),PageBreak(),
          h('Support requirements and upcoming month'),sub('Support requirements'),p(six[4][1]),
          table(['Funding stage','What funding should enable'],[['Review first','Resolve guard, structure, filter seal and electrical protection with named reviewers.'],['Build after release','Purchase approved parts and outsource the required cabinet and guard fabrication.'],['Measure after commissioning','Rent suitable instruments or commission a test service; record airflow, pressure, particles, noise and power.']],[150,369]),
          sub('Plan for upcoming month'),p(six[5][1]),
          sub('The next measurable milestone'),p('A review-approved prototype assembly followed by a safe first run with recorded airflow and pressure. A later controlled room test should compare background particle decay with purifier-on trials.'),
          p('Supplier responses, fabrication, delivery, qualified commissioning and physical testing are separate tasks. No completion date or performance percentage is promised.'),
          p('Use STAKEHOLDER_FUNDING.xlsx for staged funding discussions. Meetings content is omitted as requested; no meeting count has been invented.',True)]
room_page=[PageBreak(),h('Room size, time and what we target'),
    p('The prototype is about 0.631 m high in the current display envelope. The viewer places a simple 1.70 m person beside it for scale. This is not an average Indian height or a picture of a tested installation.'),
    sub('The first target: airborne particles'),p('We aim to reduce airborne dust and fine smoke particles, including PM2.5 and PM10. The actual capture and room reduction need measurements. Smoke gases, CO2, carbon monoxide, odours/VOCs and bacteria/virus control are not established. Particle filtration does not replace ventilation or removing pollution sources.'),
    sub('Why a bigger room takes longer'),p('A room contains a volume of air: floor area multiplied by ceiling height. More air takes longer to clean at the same particle-cleaned air rate. The interactive viewer lets you change the area, height, assumed clean-air rate and elapsed time.'),
    table(['Example only','Ideal time to 90% fewer particles'],[['25 m2 room, 2.8 m ceiling, assumed150 m3/h clean air','64.5 minutes'],['50 m2 room, same ceiling and assumed clean-air rate','128.9 minutes']],[310,209]),
    p('These examples are NOT prototype ratings or safe-occupancy times. They assume perfect mixing, no new particles and no outdoor influx. Open windows, people, cooking, leaks and uneven mixing change the result.'),
    sub('A useful engineering requirement'),p('For the example25 m2 room to reach90% reduction in30 minutes, the ideal model needs322.4 m3/h of particle-cleaned air. Even perfect capture at the assumed300 m3/h airflow screening point cannot meet that target: its ideal minimum is32.2 minutes. That airflow has not been measured. We must agree a realistic room/target before claiming success.'),
    p('Sources checked5 October2026: EPA Guide to Air Cleaners in the Home (epa.gov/indoor-air-quality-iaq/guide-air-cleaners-home), and CDC Appendix B Air (cdc.gov/infection-control/hcp/environmental-control/appendix-b-air.html). The latter supplies the ideal decay equation/mixing limitations, not a medical approval for our prototype.',True)]
stake += room_page
pdf(S/'AQI_TOWER_STAKEHOLDER_REPORT.pdf',stake)

tech=[Paragraph('AQI Tower Engineering Handoff',styles['Title']),p('Current D01 R03M integration with IH02 evidence'),picture(V/'exploded.png',420),
      p('<b>NOT FOR FABRICATION OR ENERGIZATION.</b> Authoritative manufacturing geometry remains the FreeCAD R03M study; Blender and browser meshes are display derivatives.'),
      p('The following review pages lead into the unchanged 41-page IH02 engineering reference. Return named decisions with evidence in TECHNICAL_REVIEW.xlsx. Do not mix legacy large-tower mains/HEPA assumptions with this 12 V indoor demonstrator.'),PageBreak(),
      h('Current pressure and geometry'),
      table(['Quantity','Current screen or evidence'],[['Total flow','300 m3/h assumed, not measured'],['Parallel branches','4 fans at 75 m3/h each; 2 filters at 150 m3/h each'],['OEM fan head','27.63 Pa at stated curve condition'],['Nonfilter loss','13.31 Pa under K1 reducer scenario'],['Remaining filter head','14.32 Pa per parallel filter branch'],['CAD inventory','493 source objects; tessellated display derived from saved R03M'],['Display bounding envelope','595 x 504 x 631 mm including reservations and projecting hardware; not a fabrication specification']],[175,344]),
      p('The two parallel filters do not add their pressure drops in series. Clean/loaded filter curves, installed/static fan curve compatibility, loss coefficients and branch equality remain unresolved. This screen is not an operating-point prediction.'),
      sub('Colour and animation interpretation'),p('Teal identifies cabinet/guards, amber filters, dark blue fan envelopes, purple reserved control space. Motion shows part separation or hand-authored air paths, not velocity, turbulence, deposition or removal. Guard faces remain solid tessellations, not the proposed perforation geometry.'),PageBreak(),
      h('Review responsibilities and construction path'),
      table(['Discipline','Closure required'],[['Mechanical','Guard strength/reach, seams and attachments; cabinet joints and stability; real filter tolerance, gasket compression, safe service access and whole mass/CG.'],['Electrical','Hazard allocation, independent protective functions, actual DC switching/isolation/protection, wire/connector ratings, cable restraints and enclosure. No guessed terminal assignments.'],['OEM-dependent','Exact fan/extension connector and clamping dimensions; delivered filter/frame properties. Sent enquiries are pending.'],['Commissioning and test','Confirm premises and targets; review assembly, isolation/restart and abnormal behaviour before collecting measured performance.']],[115,404]),
      sub('Critical path'),p('Exact component evidence and accepted targets -> mechanical/electrical review -> revision-specific fabrication release -> supplier delivery and fabrication -> assembly and qualified commissioning -> airflow/pressure and controlled particle tests. These dependencies are not completion dates.'),
      sub('Outdoor boundary'),p('Current fan temperature limits, enclosure and materials do not establish suitability for Indian outdoor heat or public misuse. Weather protection, tamper-resistant service access, anchoring and wind-dependent performance require a separate qualified design and approved site.'),
      sub('Files to use'),p('Native CAD, STEP, 15 DXFs, current tools, measurement templates and source registers are in engineering/. TECHNICAL_REVIEW.xlsx combines parts, release, pressure and hardware sheets. The Blender file is for presentation only.'),PageBreak(),
      h('Historical CFD evidence'),picture(R/'results/FILTER_H13/central_velocity_pressure_CASE_M.png',505),
      p('Existing Phase 9 CASE_M plot: KVO 250 + GEO_C + H13 approximation from a single manufacturer data point. Colours show calculated speed and gauge pressure for that historical case, not R03M performance.'),
      p('GEO_C is an earlier air-path geometry trial. It is not the current manufacturing assembly. Historical CFD is partial/nonconverged; the later numerical bypass seal is not a proven physical seal. No new R03M CFD has been run for this delivery.'),
      p('For the current prototype, use the pressure screen and obtain measured filter/installed-flow evidence. The following IH02 appendices are preserved unchanged.')]
tech += [PageBreak(),h('Room duty and validation tools'),
    p('Digital supplement. T01 remains OPEN: actual premises, accepted targets and instruments are not selected. The viewer calculates scenarios, not D01 CADR. First scope remains airborne particles; no gas, medical or outdoor coverage claims.'),
    sub('Mass balance and performance requirement'),p('Volume V = area x ceiling height. Ideal particle concentration ratio = exp(-CADR x t / (60 x V)); time in minutes = -60 x V x ln(1-reduction) / CADR. CADR is size-dependent effective particle-cleaned flow, not fan free-air flow or the300 m3/h pressure-screen assumption. Source/influx, settling, ventilation and nonuniform mixing are excluded.'),
    table(['Illustrative room at2.8 m height','90% in30 min requires CADR','Ideal90% time at assumed150 m3/h'],[['10 m2 /28 m3','128.9 m3/h','25.8 min'],['25 m2 /70 m3','322.4 m3/h','64.5 min'],['50 m2 /140 m3','644.7 m3/h','128.9 min']],[180,169,170]),
    p('For a filtration-only mass balance, effective clean-air delivery cannot exceed actual installed airflow at100% capture. The25 m2 example needs more than the assumed300 m3/h screening flow. This is a conditional feasibility limit, not proof of delivered airflow. Accept room/target only after measured duty is known.'),
    sub('Tools carried forward'),p('engineering/scripts/analysis/indoor_decay.py and its8 synthetic tests are now included. This existing single-pair off/on fit estimates conditional additional particle-cleaned flow only if its assumptions are explicitly declared. It is not certified CADR; repeatability and uncertainty remain unevaluated. Preserve calibration, source/background, ventilation state, timing and measured room volume. Use the existing recorder schema, not the older PARTICLE_TIMESERIES_BLANK.csv interchange format.'),
    p('A new room-scenario workbook tab and ROOM_MODEL_BASIS.md explain inputs, limitations and sources. The interactive person and room are visual references, not a modeled occupied ventilation field. No guard, electrical or structural approval has been granted by this supplement.'),
    p('Primary references checked5 October2026: EPA Guide to Air Cleaners in the Home; CDC Appendix B Air. See ROOM_MODEL_BASIS.md for exact links and applicability limits.',True)]
pdf(T/'REVIEW_INTRO.pdf',tech)
writer=PdfWriter()
for path in (R/'reports/prototype_d01/electrical_package/control_module/D01_CURRENT_BUILD_DECISION.pdf',
             R/'reports/prototype_d01/electrical_package/control_module/D01_E05_LID_CONTROLS_REVIEW.pdf',
             R/'reports/prototype_d01/electrical_package/AQI_D01_OPTA_BENCH_REVIEW.pdf',
             T/'REVIEW_INTRO.pdf',IH/'03_ENGINEERING_DRAWINGS_AND_REVIEW.pdf',R/'reports/prototype_d01/electrical_package/AQI_D01_POWER_AND_WIRING_SUPPLEMENT.pdf'):
    writer.append(str(path))
with (T/'AQI_TOWER_TECHNICAL_HANDOFF.pdf').open('wb') as f:writer.write(f)

def readcsv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.reader(f))
def sheet(wb,name,rows):
    ws=wb.create_sheet(name)
    for row in rows:ws.append(row)
    ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
    for cell in ws[1]:cell.fill=PatternFill('solid',fgColor='174B58');cell.font=Font(color='FFFFFF',bold=True)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment=Alignment(vertical='top',wrap_text=True)
            if cell.row%2==0:cell.fill=PatternFill('solid',fgColor='EEF5F5')
        ws.row_dimensions[row[0].row].height=48
    for i,col in enumerate(ws.columns,1):
        ws.column_dimensions[get_column_letter(i)].width=min(55,max(14,max(len(str(c.value or '')) for c in col[:20])*.65))
    # Wrapped descriptions must remain readable, including long review holds.
    import math
    for row in ws.iter_rows(min_row=2):
        lines=max(sum(max(1,math.ceil(len(line)/(ws.column_dimensions[cell.column_letter].width*.9))) for line in str(cell.value or '').split('\n')) for cell in row)
        ws.row_dimensions[row[0].row].height=max(36,lines*15+8)
    ws.sheet_properties.pageSetUpPr.fitToPage=True
    ws.page_setup.orientation='landscape';ws.page_setup.paperSize=ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth=1;ws.page_setup.fitToHeight=0;ws.print_title_rows='1:1'
    return ws
milestones=[['Milestone','Current state','Evidence needed','Timing'],['Engineering review','Open','Named mechanical/electrical decisions and linked evidence','Dependent on reviewers and OEM inputs'],['Construction release','Not released','Frozen components, drawings and electrical schedule','After review'],['First safe run','Not done','Signed inspection/commissioning and measured airflow/pressure','After delivery, fabrication and assembly'],['Indoor performance','Not done','Controlled repeated trials and raw logs','After safe run'],['Outdoor pilot','Separate future scope','Site permission, weather/public-safety design and wind-dependent tests','Not scheduled']]
claims=[['Claim','Evidence status','Permitted wording'],['Physical prototype','0 built','We have prepared the digital design for review.'],['Flow and cleaning','Unmeasured','The calculations are conditional; tests are planned.'],['Outdoor bubble','Unproven','The chain of zones is a research concept.'],['Costs and stock','Unquoted','Funding will be based on verified quotes.'],['Final name','Not selected','AQI Tower is the working name.']]
for technical,path in [(False,S/'STAKEHOLDER_FUNDING.xlsx'),(True,T/'TECHNICAL_REVIEW.xlsx')]:
    wb=Workbook();wb.remove(wb.active)
    sheet(wb,'Read me',[['Topic','Meaning'],['Revision','D01 R03M / E05 / current parallel batch / 5 October 2026'],['Status','Review only. Not order, fabrication or energization authorization.'],['Current parts','Funding quotes and Current combined parts use28 current references; other parts/release tabs are historical snapshots. Verify quote unit/kit basis before entering quantity.'],['Prices','Blank means UNKNOWN; no prices have been invented.'],['Evidence','CAD/digital checks are not physical results.'],['Team','College/NGO funding; no college lab assumed; qualified physical services still needed.']])
    sheet(wb,'Milestones',milestones)
    sheet(wb,'Claims',claims)
    roomrows=[['ASSUMED area m2','ASSUMED height m','ASSUMED CADR m3/h','Target fraction reduced','Volume m3','Ideal target minutes','Required CADR for30 min','Status']]
    for n,area in enumerate([10,25,50,100],2):
        valid=f'AND(ISNUMBER(A{n}),A{n}>0,ISNUMBER(B{n}),B{n}>0,ISNUMBER(C{n}),C{n}>=0,ISNUMBER(D{n}),D{n}>0,D{n}<1)'
        roomrows.append([area,2.8,150,.9,f'=IF({valid},A{n}*B{n},"INVALID INPUT")',f'=IF({valid},IF(C{n}>0,-60*E{n}*LN(1-D{n})/C{n},"NO MODELED CLEANING"),"INVALID INPUT")',f'=IF({valid},-2*E{n}*LN(1-D{n}),"INVALID INPUT")','Illustrative only; no measured D01 CADR'])
    roomws=sheet(wb,'Room scenarios',roomrows)
    for col,low,high in [('A',.1,10000),('B',.1,100),('C',0,100000),('D',.000001,.999999)]:
        rule=DataValidation(type='decimal',operator='between',formula1=low,formula2=high,allow_blank=False)
        rule.errorTitle='Invalid scenario';rule.error='Use a positive area/height, nonnegative CADR, and a reduction fraction strictly between0 and1.';rule.showErrorMessage=True;rule.errorStyle='stop';roomws.add_data_validation(rule);rule.add(f'{col}2:{col}5')
    for row in roomws.iter_rows(min_row=2):row[3].number_format='0%'
    # Current quote sheet, not a mutation of the preserved IH02 quotation template.
    parts=list(csv.DictReader((R/'reports/prototype_d01/batch_review/CURRENT_COMBINED_PARTS_REGISTER.csv').open(encoding='utf-8-sig',newline='')))
    rows=[['ID','Item','Quantity_basis','Vendor_or_service','Quote_date','Unit_cost_INR','Tax_INR','Delivery_INR','Lead_time','Scope_and_exclusions','Release_ID','Approval']]
    for item in parts:
        rows.append([item['ID'],item['Exact_product_or_geometry'],item['Quantity_basis'],'','','','','','',
                     item['Not_released_or_unknown']+'; quantities are proposals, verify kit/unit basis before quotation',
                     '', 'UNQUOTED / NOT ORDER AUTHORIZATION'])
    rows[0]+=['Quoted_line_total_INR']
    for n,row in enumerate(rows[1:],2):
        row += [f'=IF(AND(ISNUMBER(C{n}),ISNUMBER(F{n}),ISNUMBER(G{n}),ISNUMBER(H{n})),C{n}*F{n}+SUM(G{n}:H{n}),"UNQUOTED")']
        try:row[2]=float(row[2])
        except ValueError:pass
    sheet(wb,'Funding quotes',rows)
    if technical:
        sheet(wb,'Current combined parts',readcsv(R/'reports/prototype_d01/batch_review/CURRENT_COMBINED_PARTS_REGISTER.csv'))
        sheet(wb,'Current release gates',readcsv(R/'reports/prototype_d01/electrical_package/control_module/CURRENT_RELEASE_GATES.csv'))
        sheet(wb,'Control module placement',readcsv(R/'reports/prototype_d01/electrical_package/control_module/CURRENT_CONTROL_PLACEMENT.csv'))
        for name,file in [('Release decisions','REVIEW_AND_RELEASE_REGISTER.csv'),('Parts register','COMBINED_PARTS_REGISTER.csv')]:sheet(wb,name,readcsv(IH/file))
        keys=list(pressure['rows'][0]);sheet(wb,'Pressure screening',[keys]+[[row[k] for k in keys] for row in pressure['rows']])
        sheet(wb,'Pressure assumptions',[['Field','Value'],['Status',pressure['status']],['Assumptions',pressure['assumptions']],['Filter data','No measured clean or loaded curve; allowance is not actual loss']])
        sheet(wb,'Fasteners',readcsv(M/'FASTENER_SCHEDULE.csv'))
        sheet(wb,'Display dimensions',[['CAD object','Kind','X mm','Y mm','Z mm','Limit']]+[[p['name'],p['kind']]+[round(max(v[i] for v in p['vertices'])-min(v[i] for v in p['vertices']),3) for i in range(3)]+['Mesh bounding box; no tolerance or manufacturing release'] for p in mesh])
    wb.save(path)
    check=load_workbook(path);assert check['Read me']['B2'].value.startswith('D01')

for dest in (S,T):
    (dest/'visuals').mkdir(exist_ok=True)
    for name in ('assembly.png','exploded.png','cutaway.png','assembly_exploded.gif','illustrative_airflow.gif','human_scale.png','room_scenario.png'):
        shutil.copy2(V/name,dest/'visuals'/name)
    shutil.copy2(O/'AQI_TOWER_3D_REVIEW.html',dest/'AQI_TOWER_3D_REVIEW.html')
    shutil.copy2(O/'THREE_JS_LICENSE.txt',dest/'THREE_JS_LICENSE.txt')
shutil.copytree(IH/'engineering',T/'engineering',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for name in ('d01_mass_stability.py','test_d01_mass_stability.py'):
    shutil.copy2(R/'scripts/analysis'/name,T/'engineering/scripts/analysis'/name)
for name in ('MASS_STABILITY_REVIEW.md','mass_stability_review.json','part_inventory.json','cad_mesh.json'):
    shutil.copy2(M/name,T/'engineering/reports/prototype_d01/mechanical_package'/name)
(T/'engineering/reports/prototype_d01/mechanical_package/panel_DXF_REVIEW_ONLY').mkdir(parents=True,exist_ok=True)
shutil.copy2(M/'panel_DXF_REVIEW_ONLY/G_FACE.dxf',T/'engineering/reports/prototype_d01/mechanical_package/panel_DXF_REVIEW_ONLY/G_FACE.dxf')
shutil.copy2(M/'MASS_STABILITY_REVIEW.md',T/'MASS_STABILITY_REVIEW.md')
for name in ('d01_electrical_closure.py','test_d01_electrical_closure.py'):
    shutil.copy2(R/'scripts/analysis'/name,T/'engineering/scripts/analysis'/name)
for name in ('AQI_D01_POWER_AND_WIRING_SUPPLEMENT.pdf','POWER_COORDINATION.json','E01_RATED_PARTS.csv'):
    shutil.copy2(R/'reports/prototype_d01/electrical_package'/name,T/'engineering/reports/prototype_d01/electrical_package'/name)
shutil.copy2(R/'reports/prototype_d01/electrical_package/AQI_D01_POWER_AND_WIRING_SUPPLEMENT.pdf',T/'AQI_D01_POWER_AND_WIRING_SUPPLEMENT.pdf')
shutil.copytree(R/'firmware/d01_opta_review',T/'engineering/firmware/d01_opta_review',dirs_exist_ok=True)
shutil.copytree(R/'firmware/tests/d01_opta',T/'engineering/firmware/tests/d01_opta',dirs_exist_ok=True)
# Remove only superseded generated host-test copies, now preserved in firmware/tests.
for stale in ('test_control.cpp','test_support/Arduino.h'):
    target=T/'engineering/firmware/d01_opta_review'/stale
    if target.is_file(): target.unlink()
for name in ('test_d01_opta_host.py','compile_d01_opta.py'):
    shutil.copy2(R/'scripts/analysis'/name,T/'engineering/scripts/analysis'/name)
for name in ('AQI_D01_OPTA_BENCH_REVIEW.pdf','OPTA_INTEGRATION_SCREEN.json','OPTA_HOST_CHECKS.json','OPTA_BOARD_BUILD.json'):
    shutil.copy2(R/'reports/prototype_d01/electrical_package'/name,T/'engineering/reports/prototype_d01/electrical_package'/name)
shutil.copy2(R/'reports/prototype_d01/electrical_package/AQI_D01_OPTA_BENCH_REVIEW.pdf',T/'AQI_D01_OPTA_BENCH_REVIEW.pdf')
shutil.copytree(R/'reports/prototype_d01/electrical_package/control_module',T/'engineering/reports/prototype_d01/electrical_package/control_module',dirs_exist_ok=True,ignore=shutil.ignore_patterns('previews','*.FCBak','__pycache__','*.pyc'))
for relative in ('reports/prototype_d01/mechanical_package/batch_closure',
                 'reports/prototype_d01/electrical_package/batch_closure',
                 'reports/prototype_d01/batch_review','reports/prototype_d01/batch_summary'):
    shutil.copytree(R/relative,T/'engineering'/relative,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc','previews'))
for relative in ('reports/prototype_d01/component_validation/OEM_P14_Max_points.csv',
                 'reports/prototype_d01/component_validation/README.md',
                 'reports/prototype_d01/mechanical_package/README.md',
                 'docs/build/NO_LAB_BUILD_ROUTE.md',
                 'reports/prototype_d01/mechanical_package/guard_pattern.json',
                 'reports/prototype_d01/mechanical_package/cad_mesh.json',
                 'reports/prototype_d01/mechanical_package/part_inventory.json',
                 'reports/prototype_d01/mechanical_package/fasteners.json'):
    target=T/'engineering'/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(R/relative,target)
for name in ('d01_mechanical_release_batch.py','test_d01_mechanical_release_batch.py',
             'd01_electrical_release_batch.py','test_d01_electrical_release_batch.py'):
    shutil.copy2(R/'scripts/analysis'/name,T/'engineering/scripts/analysis'/name)
(T/'engineering/scripts/maintenance').mkdir(exist_ok=True)
for name in ('run_d01_release_batch.py','check_d01_handoff_consistency.py'):
    shutil.copy2(R/'scripts/maintenance'/name,T/'engineering/scripts/maintenance'/name)
shutil.copy2(R/'reports/prototype_d01/batch_review/CURRENT_COMBINED_PARTS_REGISTER.csv',T/'CURRENT_COMBINED_PARTS_REGISTER.csv')
# Only generated delivery duplicates; project sources/local backups stay untouched.
packaged_root=(T/'engineering').resolve()
for path in packaged_root.rglob('*'):
    if path.is_file() and (path.suffix.lower() in ('.pyc','.fcbak') or '__pycache__' in path.parts):
        assert path.resolve().is_relative_to(packaged_root)
        path.unlink()
shutil.copy2(R/'reports/prototype_d01/electrical_package/control_module/D01_E03_DIMENSIONED_CONTROL_LAYOUT.pdf',T/'D01_E03_DIMENSIONED_CONTROL_LAYOUT.pdf')
shutil.copy2(R/'reports/prototype_d01/electrical_package/control_module/D01_E04_LID_CONTROLS_REVIEW.pdf',T/'D01_E04_LID_CONTROLS_REVIEW.pdf')
for name in ('D01_E05_LID_CONTROLS_REVIEW.pdf','D01_CURRENT_BUILD_DECISION.pdf','CURRENT_RELEASE_GATES.csv'):
    shutil.copy2(R/'reports/prototype_d01/electrical_package/control_module'/name,T/name)
for folder in ('geometry','reports'):
    (T/'engineering/scripts'/folder).mkdir(parents=True,exist_ok=True)
shutil.copy2(R/'scripts/geometry/layout_d01_control_module.py',T/'engineering/scripts/geometry/layout_d01_control_module.py')
shutil.copy2(R/'scripts/reports/build_d01_control_layout.py',T/'engineering/scripts/reports/build_d01_control_layout.py')
shutil.copy2(R/'scripts/geometry/layout_d01_lid_controls.py',T/'engineering/scripts/geometry/layout_d01_lid_controls.py')
shutil.copy2(R/'scripts/reports/build_d01_lid_controls.py',T/'engineering/scripts/reports/build_d01_lid_controls.py')
shutil.copy2(R/'scripts/geometry/close_d01_control_layout.py',T/'engineering/scripts/geometry/close_d01_control_layout.py')
shutil.copy2(R/'scripts/reports/build_d01_closeout.py',T/'engineering/scripts/reports/build_d01_closeout.py')
for name in ('indoor_decay.py','test_indoor_decay.py','test_measurement_recording.py'):
    shutil.copy2(R/'scripts/analysis'/name,T/'engineering/scripts/analysis'/name)
(T/'engineering/scripts/monitoring').mkdir(parents=True,exist_ok=True)
shutil.copy2(R/'scripts/monitoring/record_measurements.py',T/'engineering/scripts/monitoring/record_measurements.py')
(T/'engineering/data/monitoring').mkdir(parents=True,exist_ok=True)
for name in ('decay_plan_TEMPLATE.json','run_metadata_TEMPLATE.json'):
    shutil.copy2(R/'data/monitoring'/name,T/'engineering/data/monitoring'/name)
(T/'ROOM_MODEL_BASIS.md').write_text('''# Indoor particle room model - 5 October 2026

ASSUMPTIONS: well-mixed closed room, constant size-specific particle-clean-air delivery, no ongoing source/outdoor influx; natural deposition and ventilation excluded. Scene person1.70 m is a scale marker only. Room is drawn square from adjustable floor area; height is independently adjustable. These are not measured premises or an occupied-room simulation. Default25 m2,2.8 m,150 m3/h CADR are examples; D01 CADR is UNKNOWN.

V=area*height; concentration ratio=exp(-CADR*t_minutes/(60*V)); target time=-60*V*ln(1-reduction)/CADR. At zero CADR the modeled fraction stays1 and target time is unavailable. Exactly100% removal is not reached in finite ideal time. The plot shows relative particles, not AQI or disease risk.

Example25 m2/2.8 m/150 m3/h:90% in64.472 min. Double volume doubles time; double clean-air rate halves it. To reach90% in30 min,70 m3 requires322.362 m3/h CADR. If filtration airflow were300 m3/h and capture perfect, minimum ideal time would be32.236 min; both actual airflow and capture remain unmeasured. User-entered rates above300 do not describe that300 m3/h screening point.

Targets: airborne dust and fine smoke particles, with PM2.5/PM10 trial measurements proposed. No whole-device HEPA, gases/CO2/CO/VOCs/odours, bacteria/virus control, medical protection or outdoor coverage established. Filtration supplements source control and ventilation; no intentional ozone, ionizer or UV stage is added.

Sources checked5 October2026:
- EPA https://www.epa.gov/indoor-air-quality-iaq/guide-air-cleaners-home : CADR is particle-specific, room volume matters, gas removal is distinct, filtration does not replace ventilation/source control. EPA does not certify D01.
- CDC https://www.cdc.gov/infection-control/hcp/environmental-control/appendix-b-air.html : ideal exponential purge equation and no-source/perfect-mixing limits. We adapt Q to effective particle clean-air delivery; this is NOT healthcare clearance advice or certification.

Existing research analysis: engineering/scripts/analysis/indoor_decay.py. It consumes recorder CSV fields timestamp_utc,stage,run_id,evidence_kind,channel,instrument_id,value,unit,calibration_reference. A plan specifies actual run/channel/instrument, indoor environment, room_volume_m3 and measured/assumed basis, usable_pm_floor_ug_m3 and floor evidence, off/on time windows and explicit assumption declarations. Run its --help and eight synthetic tests; never turn a synthetic fixture into physical evidence. This analysis does not subtract an asymptotic background, evaluate repeatability or produce confidence intervals. Use expert-designed real trials after safe commissioning; do not generate smoke or contaminants for a stakeholder demo.

Remaining engineering release register is unchanged: source data, guard/structure/seals, rated circuit/enclosure, commissioning and physical trials remain OPEN. This supplement closes the room-scenario software task, not those approvals.
''',encoding='utf-8')
shutil.copy2(T/'ROOM_MODEL_BASIS.md',S/'ROOM_MODEL_BASIS.md')
shutil.copy2(V/'AQI_R03M_REVIEW.blend',T/'AQI_R03M_REVIEW.blend')
(T/'BLENDER_VIEW_GUIDE.md').write_text('''# Blender presentation guide

Open AQI_R03M_REVIEW.blend. Use the active/latest scene named AQI R03M Review Presentation (currently .001); other pre-existing scenes were preserved, not overwritten.

Frame 1: assembled. Frames 30-36: exploded. Frame 48: assembled again. Camera zoom is animated to keep exploded parts inside the view. Space/play controls animate the assembly; render the camera for final lighting.

493 source parts are actual CAD tessellations, in metres for display. Five studio objects and 32 illustrative air markers bring the latest scene to 530 objects. The source CAD remains authoritative; Blender mesh dimensions do not establish fabrication tolerances. Guards remain solid envelopes.

Air markers are hidden from render by default. The supplied air GIF was rendered from a temporary cutaway with CAD animations cleared, cabinet/guard panels hidden and air markers enabled. These paths are hand-authored, NOT CFD. The source file remains the assembly animation. Use the provided GIF or offline viewer for the ready-to-share airflow explanation.

Sources: scripts/visualization/build_blender_review.py and render_blender_review.py. The latter renders a temporary background copy and does not save over the source scene. No paid assets or copied product model are used.
''',encoding='utf-8')
(T/'historical_cfd').mkdir(exist_ok=True)
shutil.copy2(R/'results/FILTER_H13/central_velocity_pressure_CASE_M.png',T/'historical_cfd/PHASE9_CASE_M_NOT_R03M.png')
shutil.copy2(batch_summary/'CURRENT_PRESSURE_BUDGET.json',T/'CURRENT_PRESSURE_BUDGET.json')
for name in ('TOOL_USAGE.md','FILTER_CURVE_BLANK.csv'):
    shutil.copy2(IH/name,T/name)
with (T/'TOOL_USAGE.md').open('a',encoding='utf-8') as f:
    f.write('''

## Room particle analysis supplement

From engineering/:

```
python -m unittest discover -s scripts/analysis -p test_indoor_decay.py -v
python -m unittest discover -s scripts/analysis -p test_measurement_recording.py -v
python scripts/monitoring/record_measurements.py --help
python scripts/analysis/indoor_decay.py --help
```

Copy the data/monitoring templates to new filenames and fill actual run/instrument/room/window metadata. Unfilled templates are intentionally invalid and must not be used as results. The importer converts actual JSONL records into a new CSV; it does not connect to sensors. Use that recorder CSV with indoor_decay.py, not the older particle-timeseries template. Both tools refuse to overwrite an existing evidence file. Read ROOM_MODEL_BASIS.md before interpretation; calibrated repeated trials remain necessary. No smoke/contaminant generation is authorized.
''')
(S/'START_HERE.md').write_text('''# AQI Tower stakeholder bundle

Read AQI_TOWER_STAKEHOLDER_REPORT.pdf first. It separates Report 1 Executive Summary from Report 2 Comprehensive Report. Meetings content is omitted as requested; final project name is still needed.

Open AQI_TOWER_3D_REVIEW.html directly in a WebGL-capable browser. No server or internet is required. Simple view explains the device; Technical view shows the conditional pressure and release holds. Use GIFs in visuals/ for messaging/slides.

STAKEHOLDER_FUNDING.xlsx is the quote and milestone workbook. Prices, stock and completion dates are unknown. Line totals require numeric quantity, unit price, total-line tax and total-line delivery; explicitly enter zero only if the quote confirms zero. Do not treat a quoted line or a rendering as construction approval.

Physical prototypes built: 0. Air animation is illustrative, NOT CFD. Outdoor bubbles are unproven. R03M guards remain solid CAD envelopes; purple objects reserve space. No purchase or contact is performed by this package.
''',encoding='utf-8')
(T/'START_HERE.md').write_text('''# AQI Tower technical bundle

MULTI-AGENT BATCH: CURRENT_COMBINED_PARTS_REGISTER.csv / workbook Current combined parts supersedes historical IH02 procurement navigation, without releasing any line for purchase. Mechanical and electrical batch_closure folders contain executable tolerance/load/voltage/protection screens and their tests. From engineering/ run python scripts/maintenance/run_d01_release_batch.py --calculations-only. Root verification also audits package consistency. Read the concrete batch results at engineering/reports/prototype_d01/batch_summary/. Current pressure inputs now have exact root-byte provenance; historicalIH02 unchanged. All calculations are conditional, not physical qualification.

CURRENT HANDOFF: read pages1–6 of AQI_TOWER_TECHNICAL_HANDOFF.pdf first. Current build decision, E05 lid/control fit and preserved E02 ordinary-input reference are now inside ONE56-page PDF. The earlier50-page review follows as historical reference. E05 replaces E04's conflicted placement: unchanged assumed cable/service volumes now clear each other and the private exact box. See CURRENT_RELEASE_GATES.csv and workbook Current release gates tab. E03/E04 remain historical fit studies. Actual supports, connector/button stack, low-current contact numeric limits, protective functions/circuit and physical tests remain OPEN. Not construction release; no fans operated.

Latest E04: D01_E04_LID_CONTROLS_REVIEW.pdf provides proposed closed-lid START/STOP/RESET locations and ordinary input schematic. Editable 18-object proxy CAD, candidate parts and LID_CONTROL_CHECKS.json are in engineering/reports/prototype_d01/electrical_package/control_module/. OEM local lid thickness4mm and mounting-range compatibility checked; assumed rear/wire-tail reservations clear bodies but overlap hub/controller assumed service spaces. Actual button stack, contact minimum switching ratings, wiring and protection remain unverified. Speed control is an isolated preset proposal only; no powered open-box adjustment. NOT a drilling, wiring or energization release. Native tower unchanged; physical0. Sources/reproduction in module README.

New E03: D01_E03_DIMENSIONED_CONTROL_LAYOUT.pdf and engineering/reports/prototype_d01/electrical_package/control_module/ contain original editable external-module envelope CAD and placements. Three bodies and three ASSUMED service spaces clear the private exact Hammond STEP; no physical fit or release. Closed-lid NA-FC1 access, supports, protection, actual cables and heat remain unresolved. Source STEP not redistributed; download source instructions and hashes in module README/FIT_CHECKS.json. Native R03M unchanged.

AQI_TOWER_TECHNICAL_HANDOFF.pdf now has56 pages: two current decision pages, two E05 layout pages, two preserved E02 bench pages, earlier five-page introduction, preserved41-page IH02 reference and four-page E01 supplement. Room-model software and exploratory decay tool included; read ROOM_MODEL_BASIS.md. Record actual decisions in TECHNICAL_REVIEW.xlsx. Not for fabrication, ordering or energization.

The last four pages provide the current power path, fan pin-function reference, catalogue-load and conditional wire-drop calculation, and exact remaining protection gaps. From engineering/ run python scripts/analysis/d01_electrical_closure.py and python scripts/analysis/test_d01_electrical_closure.py. Ten synthetic tests, not physical commissioning. PR1 protection, actual wires/fuses/enclosure and manual-restart implementation are still UNSELECTED; do not bridge this open design.

New separate E02 candidate: AQI_D01_OPTA_BENCH_REVIEW.pdf and engineering/firmware/d01_opta_review/. Implemented ordinary C++ START/STOP/RESET logic for proposed Opta Lite; all relay outputs disabled by default.1,041 host assertions,1,024 one-step cases. Run python scripts/analysis/test_d01_opta_host.py with existing g++ from engineering/. Default sketch also target-compiled with official Opta core4.6.0 / CLI1.5.1; Opta build evidence is engineering/reports/prototype_d01/electrical_package/OPTA_BOARD_BUILD.json. compile_d01_opta.py requires the separately installed isolated toolchain, never installs/uploads. Toolchain/binaries excluded from this ZIP. Not safety-rated, no hardware tested, no fan connection release. External enclosure and real fuse screens do not establish coordination. Firmware README names exact OEM sources and remaining protection gaps; existing project safety requirements unchanged.

Latest separate mechanical supplement: MASS_STABILITY_REVIEW.md. Corrected partial mass and directional static tipping arithmetic, NOT whole-device mass or safety approval. From engineering/ run python scripts/analysis/d01_mass_stability.py and python scripts/analysis/test_d01_mass_stability.py. Original mechanical PDFs and IH02 are preserved snapshots.

Authoritative assembly: engineering/reports/prototype_d01/mechanical_package/D01_R03M_ASSEMBLY.FCStd. STEP, exploded CAD, harness reservation derivative and 15 review DXFs accompany it. Blender and the offline viewer are tessellated presentation derivatives, not manufacturing models or CFD validation.

Run tools from engineering/ using TOOL_USAGE.md. The current pressure budget and blank filter curve are supplied. Supply actual measured data and calibration/source evidence; do not substitute animation dots for results.

Outstanding: exact filter resistance/tolerances, guard/structure/seal release, cable dimensions, hazard/protection/rated electrical enclosure, premises/targets, quotes, fabrication, commissioning and physical tests. OEM technical replies remain pending in reviewed records.

No lab assumed. No physical prototype built. Outdoor heat, rain, vandal resistance, site anchoring and measurable benefit remain separate future engineering.
''',encoding='utf-8')

# Evidence-based GitHub coverage inventory: omit regenerable bulk and credentials.
ignored=subprocess.run(['git','ls-files','--others','--ignored','--exclude-standard'],cwd=R,capture_output=True,text=True,check=True).stdout.splitlines()
groups={}
for name in ignored:
    path=R/name
    inaccessible=False
    try:
        if not path.is_file():continue
        size=path.stat().st_size
    except OSError:
        size=0
        inaccessible=True
    if name.startswith('reports/shareable_20261005/') or name.endswith('.blend1'):category='Reproducible presentation QA frames and Blender save backup'
    elif name.startswith('threejs/node_modules/') or '__pycache__' in name:category='Dependencies and caches'
    elif name.startswith('cfd/'):category='Generated raw solver fields meshes logs'
    elif name.startswith('GIF/'):category='Historical viewer recordings retained locally'
    elif name.startswith('tmp/') or name.endswith('.FCBak'):category='Scratch and recoverable CAD backups'
    elif name.endswith('.zip'):category='Redundant historical ZIP exports; source folders tracked'
    else:category='Other ignored local output; see existing ignore policy'
    counts=groups.setdefault(category,[0,0,0]);counts[0]+=1;counts[1]+=size;counts[2]+=int(inaccessible)
with (O/'GITHUB_COVERAGE.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['Retained_local_category','File_count','Readable_bytes_subtotal','Inaccessible_size_count','Reason']);w.writerows([[k,*v,'Not silently deleted or claimed uploaded; inaccessible WSL links excluded from byte subtotal'] for k,v in sorted(groups.items())])
(O/'README.md').write_text('''# Shareable AQI Tower delivery

5 October 2026. Two audiences, one unchanged engineering basis: D01 R03M / IH02.

- stakeholder/: 8-page plain-language Executive Summary and Comprehensive Report, room-scenario/funding workbook, offline dual-mode viewer and GIFs.
- technical/: one56-page review: current build decisions/E05 control layout/E02 bench reference first, preserved earlier50-page evidence afterwards; workbook, authoritative CAD/STEP/DXFs, current tools and editable Blender presentation. Current release gates and control placement are included. Not construction release.
- The viewer now includes a1.70 m scale person, adjustable square room, area/height/assumed-CADR/time sliders and an ideal particle-decay chart. Default clean-air rate is an example, not a D01 rating. ROOM_MODEL_BASIS.md gives sources and limits.
- visuals/: actual CAD-derived renders and annotated GIFs. Colour identifies parts; air motion is illustrative, not CFD.
- GITHUB_COVERAGE.csv: excluded generated/dependency/history categories retained locally. GitHub is not an exact mirror of raw solver time folders or dependencies.

Extract either ZIP before opening its HTML. WebGL is required for 3D; PDFs and GIFs remain usable without it. The viewer is offline and includes the Three.js MIT licence. Source build tools are scripts/visualization/ and scripts/reports/build_shareable_delivery.py.

No new physical results or build approval. Exact component/filter data, mechanical/electrical release, quotations, site, fabrication and safe commissioning remain outstanding. No fabricated price or completion date. Final device name not selected.
''',encoding='utf-8')
for dest,name in [(S,'AQI_TOWER_STAKEHOLDER_BUNDLE.zip'),(T,'AQI_TOWER_TECHNICAL_BUNDLE.zip')]:
    files=[f for f in dest.rglob('*') if f.is_file() and f.name!='MANIFEST.json']
    manifest={str(f.relative_to(dest)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    (dest/'MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    with zipfile.ZipFile(O/name,'w',zipfile.ZIP_DEFLATED) as z:
        for f in dest.rglob('*'):
            if f.is_file():z.write(f,f.relative_to(dest))
    with zipfile.ZipFile(O/name) as z:
        assert all(hashlib.sha256(z.read(n)).hexdigest()==sha for n,sha in manifest.items())

# Render every new PDF page for inspection; preserved appendices unchanged.
for path in (S/'AQI_TOWER_STAKEHOLDER_REPORT.pdf',T/'REVIEW_INTRO.pdf'):
    doc=pdfium.PdfDocument(str(path))
    for i in range(len(doc)):
        doc[i].render(scale=1.5).to_pil().save(O/'qa'/f'{path.stem}_{i+1}.png')
    print(path.name,'pages',len(doc))
print('Technical combined pages',len(PdfReader(T/'AQI_TOWER_TECHNICAL_HANDOFF.pdf').pages))
print('Shareable bundles built; assertions and ZIP manifests pass.')
