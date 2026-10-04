"""Curate a review-only D01 team handoff. Does not release construction or send files."""
import csv, hashlib, importlib.util, io, json, shutil, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
import pypdfium2 as pdfium
from PIL import Image as PILImage, ImageOps, ImageDraw
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String

R=Path(__file__).resolve().parents[2]
O=R/'reports/prototype_d01/internal_handoff_20261005'
M=R/'reports/prototype_d01/mechanical_package'
E=R/'reports/prototype_d01/electrical_package'
V=R/'reports/prototype_d01/validation_package'
O.mkdir(exist_ok=False)

def mod(name):
    s=importlib.util.spec_from_file_location(name,R/f'scripts/analysis/{name}.py')
    m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
v=mod('d01_validation');g=mod('d01_guard_bending');c=mod('d01_control_acceptance')
tests={'airflow':v.selftest(),'guard_arithmetic_checks':g.selftest(),'control':c.tests()}
(O/'DIGITAL_CHECKS.json').write_text(json.dumps(tests,indent=2))
budget=v.pressure_rows()
(O/'CURRENT_PRESSURE_BUDGET.json').write_text(json.dumps(budget,indent=2))
central=next(x for x in budget['rows'] if x['total_m3h']==300 and x['reducer_K']==1)
assert abs(central['filter_allowance_Pa']-14.3161)<.001
assert hashlib.sha256((M/'D01_R03M_ASSEMBLY.FCStd').read_bytes()).hexdigest()=='fb28a31315968509dcdbbb2caac8c6d69c84ecb94a35ccd75937a5d9ecaa33a6'

gates=[
('M01','Mechanical','OPEN INTERNAL','Guard strength and reach','Select material and justified load/probe criteria; assess perforations, welds, side seams and attachments; verify unpowered sample.','Annotated calculation/drawing plus signed inspection result'),
('M02','Mechanical','OPEN INTERNAL','Cabinet joints and stability','Check plywood/cleat grade, bolt bearing, edge distances, wood screw withdrawal, feet, whole mass/CG and cable pull; no lifting by lid.','Approved structural details and stability test record'),
('M03','Mechanical','MIXED INPUT','Filter seal and service','Confirm exact filter frame/tolerance, gasket force/compression, flatness and feedthrough seals; verify safe supported removal.','Revised stops/retainers and fit/leak evidence'),
('M04','Mechanical and electrical','WAITING OEM','Fan harness and protected entry','ARCTIC and Noctua connector/cable dimensions pending; Noctua220175. Complete insert, clamp, bend and retention design when received.','OEM evidence and updated integrated CAD/drawing'),
('E01','Electrical and mechanical','OPEN INTERNAL','Hazard and protective function','Determine applicable requirements; reconcile fixed guards, isolated servicing and present restart requirements before choosing circuitry.','Signed functional allocation and explicit requirement disposition'),
('E02','Electrical','OPEN INTERNAL','Rated circuit and enclosure','Select DC switching/protection/isolation, wire ratings, verified connectors and enclosure; check startup and auxiliary loads. No terminal guesses.','Circuit, cable schedule, ratings and physical layout'),
('E03','Electrical','SITE AND PHYSICAL','Commissioning','Verify site supply and OEM adapter suitability; test isolation, stop/restart, supply recovery, abnormal/thermal behaviour under approved procedures.','Signed commissioning record before performance tests'),
('P01','Mechanical and test lead','PHYSICAL DATA','Filter duty','Obtain exact clean/loaded curve or safe measured pressure/flow points; include all installed losses.','Accepted operating point with margin and replacement rule'),
('T01','Test lead and project lead','TEAM DECISION','Acceptance targets and room','Agree indoor premises, measured flow/noise targets, room volume, instrument methods and PM test plan before trials.','Approved test plan and thresholds'),
('T02','Test lead','AFTER RELEASE','Measured prototype results','Measure airflow, filter losses, bypass, noise, power and room PM with background/control observations.','Raw logs, calibration references and reviewed results'),
('C01','Project lead and engineers','AFTER REVIEW','Procurement and change control','Confirm exact SKUs, quantities, real quotes, lead times and service scopes; authorize only released lines.','Approved BOM and revision-specific purchase/build authorization'),
('O01','Separate future project','OUT OF INDOOR SCOPE','Public outdoor tower','Heat/rain/corrosion/tampering/anchoring and wind-dependent benefit require separate design and field validation.','Separate outdoor release; no bubble radius claimed')]
def csvout(path,header,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)
csvout(O/'REVIEW_AND_RELEASE_REGISTER.csv', ['ID','Responsible_role_not_assigned_person','State','Decision','Required_work','Closure_evidence','Reviewer_name','Date','Disposition','Evidence_file'], [list(x)+['','','OPEN',''] for x in gates])
bom=[
('F1-F4','4','ARCTIC P14 Max ACFAN00287A','Exact OEM reference','Delivered revision and cable details; guard and duty integration','Electrical BOM; OEM sources S1'),
('FL1-FL2','2','IKEA STARKVIND104.633.30 particle filter','Experimental reference only','370x290x40 catalogue envelope; pressure curve/frame/seal tolerances unknown; OEM specifies STARKVIND use only','r02_adapter/README.md'),
('PS1','1','Noctua NV-PS1 with NA-AC10','Exact OEM reference','12V2A24W; startup/auxiliary/site suitability not closed','Electrical BOM S2/S6'),
('SC1','1','Noctua NA-FC1','Exact OEM reference','Speed controller is not protective isolation','Electrical BOM S3'),
('H1','1','Noctua NA-FH1 with NA-EC1','Exact OEM reference','24W selected input; self-reset; only port1 RPM upstream; SATA unused','Electrical BOM S4/S5'),
('EXT','2 candidate leads','NA-EC1 300mm from NA-SEC1 kit','Candidate not selected','Kit contains3 leads; dimensions pending; check total connection count before purchase','Harness README'),
('CAB','1 assembly','R03M panels and cleats','Custom proposed geometry','Grade/joints/strength/finish unreleased; panel inventory is controlling geometry','CAD_PART_INVENTORY.csv and15 DXFs'),
('GUARD','2 assemblies','R03M welded perforated guards','Custom proposed geometry','Strength/reach/weld criteria unreleased;1mm not approved','GUARD_BLANKS.csv; guard_pattern.json'),
('FIX','1 scheduled set','R03M fasteners and compression limiters','Proposed geometry','Use FASTENER_SCHEDULE; do not add inventory quantities again; grade/torque unresolved','FASTENER_SCHEDULE.csv'),
('SEAL','1 design set','Filter/fan/penetration seals','Unselected material','Gasket dimensions are installed envelopes, not a compression specification','CAD inventory; mechanical_screen.json'),
('FEET','4','Retained feet','Proposed geometry','Material/bearing/stability not released','Mechanical package'),
('PR1','1 assembly','Protection and service isolation','UNSELECTED','Not replaced by hub fuse, PWM or software model','Electrical interfaces J09/J11'),
('BOX','1 assembly','Controls enclosure and cable restraints','UNSELECTED','140x100x40 reservation is not selected enclosure or complete fit','Electrical package'),
('TEST','1 service scope','Calibrated airflow/pressure/power/noise/PM measurement','UNSELECTED','Rent or commission test service; no college lab assumed','Validation package'),
('BUILD','1 service scope','Fabrication assembly and qualified review','UNSELECTED','Internal engineers review; outsource workshop work as needed','Review register')]
csvout(O/'COMBINED_PARTS_REGISTER.csv',['ID','Quantity_basis','Item','Evidence_status','Unresolved','Source'],bom)

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body2',fontName='Helvetica',fontSize=10.5,leading=15,spaceAfter=10,textColor=HexColor('#243746')))
styles.add(ParagraphStyle(name='Small2',fontName='Helvetica',fontSize=8.5,leading=11,spaceAfter=6))
styles['Title'].fontSize=27;styles['Title'].leading=32;styles['Title'].textColor=HexColor('#143c44')
styles['Heading1'].fontSize=19;styles['Heading1'].leading=24
def p(text,small=False):return Paragraph(text,styles['Small2' if small else 'Body2'])
def title(text):return Paragraph(text,styles['Title'])
def heading(text):return Paragraph(text,styles['Heading1'])
def table(headers,rows,widths):
    data=[[p(escape(str(x)),True) for x in headers]]+[[p(escape(str(x)),True) for x in r] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#d5e9e6')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f1f5f6')]),('GRID',(0,0),(-1,-1),.4,HexColor('#c4d0d3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    return t
def photo(name,w=370):
    f=M/name;im=PILImage.open(f);return Image(str(f),width=w,height=w*im.height/im.width)
def footer(c,d):
    c.setFillColor(HexColor('#65757b'));c.setFont('Helvetica',8)
    c.drawString(40,24,'AQI TOWER  |  D01 R03M  |  5 October 2026  |  REVIEW ONLY - NOT FOR CONSTRUCTION')
    c.drawRightString(555,24,str(d.page))
def makepdf(name,story):
    SimpleDocTemplate(str(O/name),pagesize=(595,842),leftMargin=40,rightMargin=40,topMargin=38,bottomMargin=46).build(story,onFirstPage=footer,onLaterPages=footer)

def network_diagram():
    d=Drawing(515,115)
    for i in range(3):
        x=92+i*165
        d.add(Circle(x,65,55,fillColor=HexColor('#edf6f3'),strokeColor=HexColor('#74a99a'),strokeDashArray=[3,3]))
        d.add(Rect(x-9,42,18,43,fillColor=HexColor('#257d74'),strokeColor=None))
        d.add(String(x,27,'Future tower',textAnchor='middle',fontSize=9))
        if i<2:
            d.add(Line(x+57,65,x+108,65,strokeColor=HexColor('#658077')))
    d.add(String(257,5,'Concept only: circles do not represent a measured radius or guaranteed coverage',textAnchor='middle',fontSize=8))
    return d

stake=[title('AQI Tower'),p('Indoor prototype and next funding milestone'),
 p('We are developing a fan-and-filter air cleaner. The first physical unit will help us measure how much air it moves, how well the filters work in our housing, and how practical it is to maintain.'),
 photo('D01_ASSEMBLY.png',380),
 p('<b>Actual design rendering, not a photograph.</b> The side box and yellow cable path are reserved space, not completed electrical hardware. Guard perforations are illustrative in the rendering; the native CAD faces remain solid envelopes.',True),
 p('<b>Today:</b> digital assembly and review documents exist. Physical prototypes built: <b>0</b>. This package asks for engineering review and staged funding, not permission to claim a finished product.'),PageBreak(),
 heading('What the first unit will do'),
 p('Air enters through two filters on opposite sides. Four fans draw that air into a shared chamber and discharge it through the top guard. The filters work side by side, not one after another.'),
 table(['Part','Plain explanation'],[['Two removable filters','Catch particles; sealing around their edges is essential. Actual performance in this unit is untested.'],['Four fans','Move air through the resistance of filters and guards. Free-air fan figures are not the finished unit output.'],['Cabinet and guards','Hold the parts together and separate users from moving fans. Strength, access and electrical checks must finish before operation.'],['External power adapter','Proposed12V supply inside the fan system; household mains remains at the external OEM adapter. Electrical review is still required.']],[140,375]),Spacer(1,15),
 p('<b>Why start smaller?</b> It makes the first build easier to inspect, transport and measure. It remains our custom enclosure, filter mounting, integration and testing project. It does not prove that a large outdoor tower will work.'),
 p('<b>Long-term idea:</b> larger towers may create local cleaner-air zones. A chain of zones is a research goal, not a proven network. Wind, weather, nearby pollution and placement will affect results. Bubble size, cleaning percentage and spacing are unknown.'),
 p('No gas-removal, water, solar or outdoor coverage claim is attached to this first particulate prototype. The current experimental replacement filters do not make the assembled device a certified HEPA purifier.'),network_diagram(),PageBreak(),
 heading('What support achieves next'),
 table(['Already prepared','Still needed'],[['Integrated CAD, exploded view, dimensioned panel drawings and hardware schedules','Internal mechanical review of structure, guarding, sealing and service'],['OEM fan data and pressure calculations','Real filter resistance and installed airflow measurements'],['Power-reference schematic and control requirements','Electrical design completion, rated protection and commissioning'],['Blank test sheets and checked analysis software','A supervised indoor location, instruments and an assembled unit']],[255,260]),Spacer(1,12),
 p('<b>Funding request:</b> fund engineering closure first, then released parts and outsourced fabrication, followed by qualified assembly and instrumented testing. Prices, stock and service lead times are not confirmed; the parts register is not a quotation.'),
 p('<b>Measurable next milestone:</b> a reviewed revision with no unresolved safety-critical build holds, followed by one safely commissioned indoor unit and traceable airflow, pressure, power, noise and particle-test records.'),
 p('<b>Timing:</b> internal review can start now. Cable drawings are requested from ARCTIC and Noctua. Supplier responses, workshop availability and rework govern the construction date; no completion date is booked.'),
 p('<b>Team:</b> Nakul Kokate coordinates the project. Mechanical and electrical reviewers can work in parallel using the engineering pack. College and NGO support is funding; no college laboratory is assumed. A final project/device name remains to be agreed.')]
makepdf('01_STAKEHOLDER_BRIEF.pdf',stake)

engineer=[title('D01 Internal Engineering Handoff'),p('Review revision IH02 | Mechanical R03M | Electrical E00 with supplements | 5 October 2026'),
 p('<b>Decision requested:</b> review and resolve the open engineering items in REVIEW_AND_RELEASE_REGISTER.csv. This is a coordinated design-review issue, not a fabrication or energization issue. Manufacturer replies are not the only remaining dependency.'),
 photo('D01_EXPLODED.png',365),p('Exploded view of the actual current assembly. Omitted threads, weld beads and perforations limit what CAD checks establish. Nominal component fits do not establish strength, safety or sealing.',True),
 table(['Evidence class','Meaning'],[['DETECTED','Recorded files or geometry; not physical measurement'],['OEM REFERENCE','Published component data; not approval of our integration'],['ASSUMPTION','Provisional input requiring validation'],['UNKNOWN / OPEN','Do not order, cut or energize the affected interface']],[120,395]),PageBreak(),
 heading('Authoritative files and corrections'),
 p('Use the native R03M assembly as the base. Harness review CAD is a derivative with assumed cable reservations, not a competing machine. The package preserves source-relative paths under engineering/ so scripts can find their inputs.'),
 table(['Use','Controlling source'],[['Mechanical geometry','mechanical_package/D01_R03M_ASSEMBLY.FCStd and STEP;15 DXF files include10 panels plus5 guard blank types'],['Electrical','electrical_package PDF, BOM and interfaces plus protective selection supplement; no completed rated circuit'],['Current pressure','CURRENT_PRESSURE_BUDGET.json generated in this handoff from R03M guard area and archived OEM numeric fan points'],['Current airflow analyzer','engineering/scripts/analysis/d01_validation.py; mandatory --plane-area-m2;23 checks'],['Latest open decisions','REVIEW_AND_RELEASE_REGISTER.csv and guard/harness/protective supplements']],[135,380]),Spacer(1,12),
 p('<b>Superseded assumptions:</b> do not use old Filtrete/MERV13 arrangements, large-tower230V fan wiring, earlier long studs or riveted guard details. D01 currently uses two experimental STARKVIND envelopes and four12V P14 Max fans. No certified whole-device filtration class is assigned.'),
 p('<b>Pressure correction:</b>14.32Pa per filter at an assumed300m3/h total and reducer K1, not the older14.61Pa. This is remaining model headroom, not a measured filter loss or acceptance margin. Old R01 operating-flow predictions do not transfer to STARKVIND.'),
 p('<b>Appendices:</b> earlier mechanical18-page, electrical7-page and validation5-page PDFs are included as labeled reference snapshots after this review section. The current notes and scripts supersede their outdated analyzer command/test count and any older pressure interpretation. No design release is implied.'),PageBreak(),
 heading('Mechanical review disposition'),
 p('DETECTED:493 objects in the base CAD;119805 checked non-reservation pairs with no positive-volume clash in the saved generator audit. The panel audit reports119804 because it also excludes the guard pair. These are stored geometry results; native CAD hash is verified in this handoff.'),
 table(['Interface','Review action'],[['Filters and seals','370x290x40 filter envelopes; frame bearing and thickness tolerances unverified. Assumed39/40/41mm thickness changes nominal4mm gasket compression from0/25/50%. Do not cut spacers from that assumption.'],['Cabinet and supports','Panel/cleat grades and joint capacity not selected. Partial assumed mass12.19kg excludes real fans, filters, controls, feet and seals. Do not call it total mass or approve tipping from it.'],['Guarding','Independent welded guards remain fitted during filter removal.4mm holes/6mm pitch are proposed geometry, not access approval.22/50mm guard-to-body distances are not blade clearance.'],['Fasteners','Use the R03M schedule and modeled inventory together. One schedule row groups8 adapter studs plus4 ledge screws; do not read its qty8 as the whole hardware count. Grade, preload and wood bearing remain open.'],['Service','Two200mm filter withdrawal sweeps passed nominal geometry checks. Hands, tools, retainer handling, sag and manufacturing tolerances still require review.']],[115,400]),Spacer(1,12),
 p('Guard supplement:36 ideal solid-strip cases and28 arithmetic tests explain thickness/span trade-offs only. They do not model the actual2822 holes, plate action, yielding or weld flexibility. A thicker guard or stiffener is not selected. Review loading criteria and unpowered sample assessment.'),PageBreak(),
 heading('Electrical review disposition'),
 p('<b>Reference chain only:</b> OEM NV-PS1 external adapter -> supplied NA-AC10 -> NA-FC1 -> NA-FH1 four-pin input -> four P14 Max fans. SATA stays unused. Instrument logger power remains separate. This is not a terminal-level wiring instruction.'),
 table(['Issue','Required resolution'],[['Power budget','Four fans at0.35A each give1.4A/16.8W nominal.2A/24W path leaves0.6A before controls and startup. A1.5x fan startup scenario alone is2.1A; this is a sensitivity, not a measured surge.'],['Protective behaviour','PWM zero and hub fuse are not isolation. Hub self-reset and port1-only upstream RPM cannot establish independent four-fan safety monitoring.'],['Control candidates','Pilz X5/X9P/s4 screens do not select a protective assembly. X9P leaves0.2W before auxiliaries; s4 needs24V; X5 monitored sequence not established.'],['Enclosure and harness','140x100x40mm is reserved space, not a selected box. Include walls, terminals, bend radii, cooling, glands and access after circuit selection.'],['Review output','Issue rated schematic, interface/terminal and cable schedule, protection coordination, enclosure layout and commissioning procedure. Retain or explicitly revise restart requirements through hazard review.']],[115,400]),Spacer(1,12),
 p('Keep OEM mains adapter intact. No bare-mains design is released. Internal electrical engineer determines applicable Indian requirements, supply/site suitability and required inspection. An external adapter rating does not certify this assembly. No arbitrary fuse size, wire gauge or terminal mapping has been filled in.'),
 p('The14 named control cases and1024 one-step states are software logic checks only. They do not test hardware timing, welded contacts, sensing coverage, DC interruption, thermal behaviour or safety integrity.'),PageBreak(),
 heading('Pressure and measurement basis'),
 p('Four fans operate in parallel: flow adds, pressure does not. Two filter branches operate in parallel: each ideally sees half total flow; their pressure drops are not added. Unequal branch flows remain possible in real construction.'),
 table(['Total m3/h','Each filter m3/h','Fan Pa','Other losses Pa','Filter allowance Pa'],[[x['total_m3h'],x['per_filter_m3h'],f"{x['fan_Pa']:.2f}",f"{x['nonfilter_Pa']:.2f}",f"{x['filter_allowance_Pa']:.2f}"] for x in budget['rows'] if x['reducer_K']==1],[80,105,85,120,125]),Spacer(1,12),
 p('ASSUMPTIONS:2800rpm OEM curve; density1.2kg/m3; equal fan/filter sharing; guard area0.0354623m2 each; guard K1.5 each, plenum K1.5, installation K1 and reducer K1. Full JSON also gives reducer K0.5/2 sensitivity. Coefficients, static/installed compatibility and any double counting remain unverified. Negative headroom means that scenario has no allowance for a positive filter loss.'),
 p('No actual STARKVIND clean/loaded curve has been established. Do not promise300m3/h, CADR, HEPA-level removal or room coverage. Fit and pressure evidence are separate gates.'),
 p('Current airflow tool requires accepted physical rows, unique cells, one run/instrument/method/calibration, ISO timestamps with timezone and independent full-plane area. Equal cell-area sum does not prove correct spatial coverage. Reported error is velocity-only; it excludes area, swirl, fixture effects and time variability.'),
 p('Run from engineering/: <b>python scripts/analysis/d01_validation.py</b>. With real reviewed data: add <b>--airflow-csv FILE --plane-area-m2 AREA --output NEW.json</b>. AREA is the measurement plane, not automatically guard open area. Never alter raw observations to obtain a passing result.'),PageBreak(),
 heading('Review ownership and release gates'),
 table(['IDs','Owner','Closure package'],[['M01-M03','Mechanical engineer','Guard/structure/seal calculations, selected materials/joints, corrected drawings and inspection plan'],['M04','Mechanical + electrical','OEM reply interpretation and protected harness integration'],['E01-E03','Electrical + mechanical','Hazard allocation, rated circuit/enclosure and commissioning evidence'],['P01 / T01-T02','Test lead + project lead','Filter/duty evidence, agreed room/targets, calibrated methods and physical results'],['C01','Project lead + engineers','Real quotes and released revision-specific BOM/build authorization'],['O01','Future outdoor team','Separate public/weather/wind/stability design and field evidence']],[85,145,285]),Spacer(1,15),
 p('Complete the CSV register with reviewer name, disposition, date and linked evidence. A row is not closed by ticking a box: the accepted calculation, drawing or physical result must exist. No reviewers or approvals have been invented.'),
 p('<b>What can happen now:</b> internal drawing/calculation review, applicability/hazard decisions, manufacturability discussions and scoped quotations if separately authorized. These do not require the manufacturer cable reply.'),
 p('<b>Waiting:</b> cable/connector evidence from ARCTIC and Noctua; Noctua ticket220175. Filter/frame/curve data, site selection and actual physical evidence are separate unresolved inputs, not covered by those enquiries.'),
 p('<b>Release boundary:</b> only a signed revised package with closed safety-critical holds can authorize affected fabrication/assembly. Digital work, supplier delivery, workshop fabrication, inspection and physical testing are distinct critical-path activities. No completion date is promised.'),PageBreak(),
 heading('Assembly and verification route'),
 p('<b>Sequence below applies only after component-specific release.</b> Use the mechanical appendix for drawing details; unresolved quantities/ratings must not be guessed on the workshop floor.'),
 table(['Stage','Action and hold point'],[['1 Receive and inspect','Record exact fan/filter/adapter revisions, dimensions and condition. Reject unapproved substitutions; check against released BOM.'],['2 Unpowered dry fit','Inspect cut edges, panel joints, feet, fan mount and guard fit. Keep electronics disconnected. Resolve tolerance clashes before sealing.'],['3 Seals and filters','Fit reviewed ledges, penetration seals, gaskets, stops and retainers in the documented order. Verify compression/flatness and supported service access.'],['4 Guards and wiring','Fit independently retained guards; install released harness restraints and enclosure. Verify cable isolation from moving parts and guarded openings.'],['5 Commission','Qualified electrical/mechanical inspection and approved isolation/stop/restart/thermal checks. Record sign-off before performance operation.'],['6 Measure','Record airflow and pressure at reviewed settings; power and noise; controlled room PM decay/background only under approved method. No improvised smoke, powder or gas challenge.'],['7 Decide','Compare to agreed targets, keep failed results, investigate leakage/low flow/noise. Update design and repeat relevant verification before expansion.']],[110,405]),Spacer(1,12),
 p('Blank CSVs are included. Instrument ranges, calibration and fixture loading must match the approved test method. Consumer PM readings do not certify filter class. Do not infer outdoor radius from an indoor decay test.'),PageBreak(),
 heading('Parts funding and evidence handover'),
 p('COMBINED_PARTS_REGISTER.csv separates exact OEM references, custom geometry and unresolved hardware/services. CAD_PART_INVENTORY.csv is a modeled-object list, not an order list. FASTENER_SCHEDULE.csv groups hardware; do not sum both as additional purchases.'),
 p('Use staged funding: review and engineering closure; then released components/fabrication; then commissioning and calibrated testing. Request actual quotes and lead times against the approved revision. No INR total is asserted without quotations.'),
 p('The ZIP includes selected current native/STEP/exploded files,15 DXFs, current engineering evidence and standalone calculation inputs. No old CAD branches, downloaded manufacturer manuals, email address or conversation records are included. OEM facts must still be checked against delivered parts.'),
 p('Sources are recorded in electrical_package/sources.json, harness_detail/README.md and GUARD_ACCESS_DECISION.md. Principal official sources include ARCTIC P14 Max support, Noctua NV-PS1/NA-FC1/NA-FH1 manuals and IKEA India STARKVIND104.633.30. Archived references are evidence, not current stock or price guarantees.'),
 p('<b>Current filter comparison:</b> scripts/analysis/d01_current_filter_screen.py uses the current R03M budget. Supply per-filter m3/h and Pa with exact part/revision, source, CLEAN or LOADED condition and its conditioning reference. It refuses extrapolation and preserves input hashes. Positive model margin is conditional, not approval. Do not use the earlier R01 offer checker for this design. See TOOL_USAGE.md.'),
 p('The geometric assembly is ours; proprietary purchased parts retain their manufacturers\u2019 rights. This package is for internal review and does not assert patentability or a license to redistribute OEM materials.'),
 p('<b>Handback requested from the team:</b> one annotated review register and one coordinated revision, not parallel incompatible assemblies. Keep changes traceable to R03M and record any accepted change to safety requirements. Do not mark all remaining work complete while these decisions remain open.'),
 p('Annexes follow: mechanical R03M; electrical E00; validation V00. All are reference snapshots and remain review-only. Corrections in this review section take precedence. The complete machine has not been built or tested.')]
makepdf('02_ENGINEERING_REVIEW.pdf',engineer)

# Make explicit separators so no engineer can mistake an appendix for the current review.
appendices=[('A','Mechanical drawings',M/'AQI_D01_MECHANICAL_PACKAGE.pdf'),
            ('B','Electrical review',E/'AQI_D01_ELECTRICAL_REVIEW.pdf'),
            ('C','Validation procedure',V/'AQI_D01_VALIDATION_PACKAGE.pdf')]
merged=pdfium.PdfDocument.new()
doc=pdfium.PdfDocument(str(O/'02_ENGINEERING_REVIEW.pdf'));merged.import_pages(doc);doc.close()
for tag,label,f in appendices:
    cover=io.BytesIO();cc=canvas.Canvas(cover,pagesize=(595,842))
    cc.setFont('Helvetica-Bold',24);cc.drawString(40,740,'Appendix '+tag)
    cc.setFont('Helvetica',20);cc.drawString(40,700,label)
    cc.setFont('Helvetica',11)
    for i,line in enumerate(['Reference snapshot for D01 R03M internal review',
                             'Read the current review section and TOOL_USAGE.md first.',
                             'Current scripts and corrections supersede older analysis instructions.',
                             'Review drawings require release before cutting or wiring.',
                             'No physical performance or safety approval is recorded.']):
        cc.drawString(40,650-i*24,line)
    cc.setFont('Helvetica',9);cc.drawString(40,430,'Source: '+f.name)
    cc.save();cover.seek(0)
    separator=pdfium.PdfDocument(cover);merged.import_pages(separator);separator.close()
    doc=pdfium.PdfDocument(str(f));merged.import_pages(doc);doc.close()
merged.save(str(O/'03_ENGINEERING_DRAWINGS_AND_REVIEW.pdf'));merged.close()

selected=[]
for directory in (M,E):
    for f in directory.rglob('*'):
        if f.is_file() and f.suffix.lower() in ('.fcstd','.step','.dxf','.csv','.json','.md') and f.name not in ('cad_mesh.json','MANIFEST.json','README.md'):
            selected.append(f)
selected += [M/'harness_detail/README.md',R/'reports/prototype_d01/r02_adapter/README.md',E/'sources.json']
selected += [V/n for n in ('AIRFLOW_BLANK.csv','RUN_LOG_BLANK.csv','PARTICLE_TIMESERIES_BLANK.csv','sources.json')]
selected += [R/f'scripts/analysis/{n}.py' for n in ('d01_validation','d01_guard_bending','d01_control_acceptance','d01_current_filter_screen','test_d01_current_filter_screen')]
selected += [R/'reports/prototype_d01/component_validation/OEM_P14_Max_points.csv']
for f in set(selected):
    dest=O/'engineering'/f.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
(O/'START_HERE.md').write_text('''# AQI Tower internal handoff IH02

5 October2026. READY FOR INTERNAL REVIEW ONLY. NOT ready for construction or energization. Source CAD and OEM evidence are the existing4 October revision; supplier replies are still pending in the project records.

Stakeholders: read01_STAKEHOLDER_BRIEF.pdf (3 pages).
Engineers: read03_ENGINEERING_DRAWINGS_AND_REVIEW.pdf, which combines the current review with mechanical, electrical and validation reference appendices.02_ENGINEERING_REVIEW.pdf is the same review section separately for quick navigation.
Return REVIEW_AND_RELEASE_REGISTER.csv with named reviewers and linked closure evidence. Use COMBINED_PARTS_REGISTER.csv for budgeting discussions, not ordering. All costs/stock/lead times unconfirmed.

Authoritative base: engineering/reports/prototype_d01/mechanical_package/D01_R03M_ASSEMBLY.FCStd. STEP and exploded native file accompany it. Harness derivative adds assumed reservations only.15 DXFs are REVIEW ONLY;10 panels plus5 guard blank types. Original drawings remain unchanged.

Current pressure: CURRENT_PRESSURE_BUDGET.json. Current code: engineering/scripts/analysis/d01_validation.py. Run from engineering/; physical CSV requires --plane-area-m2 AREA. Older analyzer commands/counts in V00 appendix are superseded. Do not use legacy R01 filter prediction or large-tower mains plans for this unit.

Use TOOL_USAGE.md for the current filter screen and independent arithmetic checks. Blank source-curve CSV contains no invented measurements. This handoff supersedes IH01 for team circulation; older files remain historical.

Known missing design: released guard/structure/seals, protected harness entry, rated electrical circuit and enclosure. Open inputs: exact filter properties, room/acceptance targets, manufacturing/review services and physical commissioning/performance. OEM cable enquiries sent; replies pending. No supplier response alone closes whole-system release.

No purchasing, fabrication, physical test or external distribution performed by preparation of this handoff. No guarantee of outdoor coverage, filter class or patentability. Physical prototypes0.

MANIFEST.json records every packaged source/output hash. The bundle deliberately excludes old branches, source conversations, personal email and manufacturer PDF redistribution. README links inside preserved supplementary evidence may point to the full project; use this start file for package navigation.
''',encoding='utf-8')
(O/'TOOL_USAGE.md').write_text('''# Running the current tools

Extract the whole ZIP. Open a terminal in engineering/. Python3 is required; these analysis tools use the standard library. No extra engineering program is needed to run the checks. FreeCAD opens FCStd; STEP is supplied for other CAD tools. This is a review package.

```
python scripts/analysis/d01_validation.py
python scripts/analysis/d01_guard_bending.py
python scripts/analysis/d01_control_acceptance.py
python -m unittest discover -s scripts/analysis -p test_d01_current_filter_screen.py -v
```

To compare real OEM or reviewed physical filter data, create a new CSV from FILTER_CURVE_BLANK.csv. Use per-filter flow, not total tower flow. Rows must be sorted, finite and nonnegative. Do not extrapolate. Supply exact evidence and the condition definition:

```
python scripts/analysis/d01_current_filter_screen.py CURVE.csv --part "EXACT PART AND REVISION" --source "DOCUMENT OR TEST RECORD" --evidence OEM --condition CLEAN --condition-ref "SOURCE CLEAN CONDITION" --output NEW_SCREEN.json
```

For measured data use --evidence PHYSICAL; for a loaded curve use --condition LOADED and its actual loading reference. The tool does not verify the truth of labels or the authenticity of a source. Separate clean and loaded runs are needed.15 scenarios use the actual R03M guard open area with assumed loss coefficients. A positive margin does not release purchase or establish actual operating flow.

For accepted physical airflow rows:

```
python scripts/analysis/d01_validation.py --airflow-csv AIRFLOW.csv --plane-area-m2 AREA --output NEW_FLOW.json
```

Replace AREA with the independently established full measurement-plane area in m2. It is not automatically the guard hole area. Velocity-only error is not complete uncertainty. Preserve raw logs and use new output filenames. All bundled test fixtures are synthetic; there are no physical test results.
''',encoding='utf-8')
csvout(O/'FILTER_CURVE_BLANK.csv',['per_filter_flow_m3h','pressure_Pa'],[])
csvout(O/'QUOTE_AND_FUNDING_REGISTER.csv',['ID','Item','Quantity_basis','Vendor_or_service','Quote_date','Unit_cost_INR','Tax_INR','Delivery_INR','Lead_time','Scope_and_exclusions','Release_ID','Approval'],[[r[0],r[2],r[1],'','','','','','','', '','UNQUOTED / NOT ORDER AUTHORIZATION'] for r in bom])

# Render all newly authored pages for inspection; montage is QA only, outside distribution.
qa=O/'qa';qa.mkdir()
for name in ('01_STAKEHOLDER_BRIEF','02_ENGINEERING_REVIEW'):
    doc=pdfium.PdfDocument(str(O/(name+'.pdf')))
    for i in range(len(doc)):
        page=doc[i];im=page.render(scale=1.2).to_pil();im.save(qa/f'{name}_{i+1:02}.png')
    doc.close()
imgs=list(qa.glob('*.png'))
for start in range(0,len(imgs),4):
    sheet=PILImage.new('RGB',(1000,1420),'#d3d9db')
    for k,f in enumerate(imgs[start:start+4]):
        im=PILImage.open(f);im.thumbnail((490,690));sheet.paste(im,((k%2)*500,(k//2)*710))
    sheet.save(qa/f'montage_{start//4}.png')
files=[f for f in O.rglob('*') if f.is_file() and qa not in f.parents]
manifest={str(f.relative_to(O)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(O/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(O/'AQI_TOWER_INTERNAL_HANDOFF_IH02.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files+[O/'MANIFEST.json']:z.write(f,str(f.relative_to(O)))
with zipfile.ZipFile(O/'AQI_TOWER_INTERNAL_HANDOFF_IH02.zip') as z:
    assert z.testzip() is None
    assert all(hashlib.sha256(z.read(n)).hexdigest()==h for n,h in manifest.items())
print(json.dumps({'output':str(O),'packaged_files':len(manifest),'archive_hashes_verified':True,'new_pages':len(imgs),'checks':tests['airflow'],'pressure_at300':central},indent=2))
