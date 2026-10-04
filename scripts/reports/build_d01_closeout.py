"""Current decision front matter: consolidate known evidence, never fake release."""
import json,csv
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/electrical_package/control_module'
d=json.loads((O/'CURRENT_CONTROL_CHECKS.json').read_text())
assert d['digital_routing_conflict_closed'] and not d['release']
styles=getSampleStyleSheet();styles['BodyText'].fontSize=9;styles['BodyText'].leading=12
styles['Title'].textColor=HexColor('#153d4c');styles['Heading2'].textColor=HexColor('#148b84')
def p(s):return Paragraph(s,styles['BodyText'])
def h(s):return Paragraph(s,styles['Heading2'])
def table(rows,widths):
 t=Table([[p(v) for v in row] for row in rows],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e1efee')),('GRID',(0,0),(-1,-1),.4,HexColor('#bdcfd1')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));return t
story=[Paragraph('AQI Tower — consolidated engineering handoff',styles['Title']),p('D01 / R03M mechanical / E05 control-module fit / 5 October 2026'),Spacer(1,10),
 p('<b>Decision:</b> ready to hand to the internal engineering team for a build-release review. NOT ready to order all parts, fabricate unchanged drawings or energize. Physical prototypes built: 0.'),
 h('Use one current design'),p('Four ARCTIC P14 Max ACFAN00287A fans and two proposed IKEA104.633.30 filters in parallel, in the preserved R03M rectangular cabinet. External12V Noctua adapter/controller/hub are the reference power chain. The larger cylindrical outdoor tower is a later project, not this build.'),
 h('What is now closed digitally'),table([['Evidence','What it establishes — and does not establish'],
 ['Mechanical CAD','493 original assembly objects, STEP and15 drawing files retained. Geometry checks do not approve materials, guards, seals or stability.'],
 ['E05 control fit','Same300x200x120mm enclosure. Hub rotated/moved, speed controller moved, buttons at X=-15/45/105,Y=55mm. Unchanged assumed rear/cable reservations now clear each other and OEM box geometry. Actual connectors, button stack and supports are unverified.'],
 ['Software','1,041 host assertions; default Opta target compile/link passed with official core4.6.0. All relay outputs remain disabled. No physical test or protective control implemented.'],
 ['Pressure and power','At assumed300m3/h total, conditional filter allowance14.316Pa each. Four fans catalogue16.8W; plus Opta max2W gives18.8W before hub/controller/auxiliaries/startup. The24W path limit is not a measured margin.'],
 ['Visuals and handoff','Actual CAD renders, Blender, offline viewer, diagrams, parts/review sheets and test tools. Air animation and room slider are explanatory assumptions, not CFD/CADR proof.']], [110,405]),
 h('Control decision'),p('START/STOP/RESET are ordinary inputs. STOP is not emergency stop or isolation. RESET does not start fans. Internal speed adjustment is a disconnected-source preset; close the box before operation. No live knob modification proposed. Current OEM Digest19-42 confirms low-power contacts but gives no numerical minimum switching range.'),
 h('How to read this combined PDF'),p('Pages1–2: current decisions and real release blockers. Pages3–4: E05 layout/input review. Pages5–6: preserved E02 bench-control drawing. Pages7–56: earlier50-page engineering handoff, retained as historical evidence. Where its fit/control or board-build status differs, the E05 check record and current target-build JSON govern; older wiring is not released.'),
 PageBreak(),Paragraph('What must happen before construction',styles['Title']),
 p('These are missing engineering inputs and physical acceptance steps, not items that can be marked complete by generating another document. No build approval has been given.'),
 h('Five remaining release gates'),table([['Gate','Exact deliverable needed / responsible scope'],
 ['1. Guards / structure','Mechanical reviewer and fabricator: guard reach/strength and seams, material grades, joints, feet, whole-device mass/stability and handling. Revised signed detail drawings and unpowered inspection evidence.'],
 ['2. Filters / harness','Exact delivered filter tolerance and gasket/compression evidence; fan/extension lead, connector and clamp geometry. Resolve service retention, bypass seal and protected entries. OEM enquiries already sent; replies pending.'],
 ['3. Rated electrical design','Electrical reviewer: hazard-to-protective-function allocation including restart/recovery; complete selected protection/isolation/switching, startup/fault coordination, actual gauges/terminals/glands, metal-panel treatment, mounts and thermal assessment. Opta software cannot replace this.'],
 ['4. Actual assembly / commissioning','After revision-specific release and authorized procurement: supplier delivery, fabrication, dry-fit inspection, safe qualified assembly, isolation/stop/restart and abnormal/thermal tests. Signed commissioning precedes performance tests.'],
 ['5. Performance / acceptance','Test lead: agreed indoor room/targets, calibrated or paid/rented instruments. Record airflow, pressure, bypass, noise, power, temperatures and controlled PM decay/background. No proven CADR or outdoor bubble radius yet.']], [115,400]),
 h('No-lab construction route'),p('Use a local cabinet/metal fabricator and qualified electrical assembly/test service in Pune, Hyderabad or Mumbai when chosen. College/NGO funding supports those services and approved parts; no college workshop is assumed. Prepare quotations from current drawings clearly marked REVIEW ONLY; production follows signed release, not this PDF.'),
 h('Critical path — no invented dates'),p('Resolve exact component inputs and protective functions → signed mechanical/electrical revision → funding and purchase authorization → delivery/fabrication → unpowered fit and assembly → qualified commissioning → measured performance. Supplier replies and workshop/test capacity control elapsed time; digital compilation alone does not shorten them to a promised date.'),
 h('Funding and technical sheets'),p('STAKEHOLDER_FUNDING.xlsx is for actual quotations and milestone funding. TECHNICAL_REVIEW.xlsx and CURRENT_RELEASE_GATES.csv preserve decisions and closure evidence. Stock, prices and dates are UNKNOWN until confirmed. Only released line items can enter a purchase/build authorization.'),
 p('<b>Unchanged boundary:</b> indoor experimental particle demonstrator. No gas-removal, whole-device HEPA, medical, outdoor heat/rain/tamper or public-clean-air coverage claim. No purchases, supplier messages, hardware flashing or energization performed in this continuation.')]
def footer(c,doc):
 c.setFont('Helvetica',8);c.setFillColor(HexColor('#ac2947'));c.drawString(36,22,'ENGINEERING REVIEW / NOT CONSTRUCTION OR ENERGIZATION RELEASE');c.drawRightString(559,22,str(doc.page))
dest=O/'D01_CURRENT_BUILD_DECISION.pdf'
SimpleDocTemplate(str(dest),topMargin=30,bottomMargin=40,leftMargin=36,rightMargin=36).build(story,onFirstPage=footer,onLaterPages=footer)
pdf=pdfium.PdfDocument(str(dest));assert len(pdf)==2,len(pdf)
for i in range(2):pdf[i].render(scale=1.4).to_pil().save(O/'previews'/f'CLOSEOUT_{i+1}.png')
rows=list(csv.DictReader((R/'reports/prototype_d01/internal_handoff_20261005/REVIEW_AND_RELEASE_REGISTER.csv').open(encoding='utf-8')))
rows.append(dict(ID='D05',Responsible_role_not_assigned_person='Digital preparation',State='CLOSED DIGITAL ONLY',Decision='E04 assumed service-volume collisions',Required_work='Actual dimensions/wiring remain E02 release scope',Closure_evidence='CURRENT_CONTROL_CHECKS.json; unchanged reservations mutually clear',Reviewer_name='',Date='2026-10-05',Disposition='DIGITAL PASS / NO BUILD RELEASE',Evidence_file='CURRENT_CONTROL_CHECKS.json'))
with (O/'CURRENT_RELEASE_GATES.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Two current decision pages and evidence-linked release register written.')
