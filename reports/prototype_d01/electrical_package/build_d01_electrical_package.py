"""Generate the bounded D01 E00 electrical review, not fabrication wiring."""
from pathlib import Path
import csv, hashlib, importlib.util, json, zipfile
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'reports/prototype_d01/electrical_package'
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('control', ROOT/'scripts/analysis/d01_control_acceptance.py')
import sys
control = importlib.util.module_from_spec(spec); sys.modules['control'] = control; spec.loader.exec_module(control)
checks = control.tests()
sources = [
 ('S1','ARCTIC P14 Max black','https://www.arctic.de/en/P14-Max-Black/ACFAN00287A'),
 ('S2','NV-PS1 specifications','https://www.noctua.at/en/products/nv-ps1/specifications'),
 ('S3','NA-FC1 specifications','https://www.noctua.at/en/products/na-fc1/specifications'),
 ('S4','NA-FH1 specifications','https://www.noctua.at/en/products/na-fh1/specifications'),
 ('S5','NA-FH1 manual','https://cdn.noctua.at/media/noctua_na_fh1_manual_spot_en.pdf?download=true'),
 ('S6','NV-PS1 manual','https://cdn.noctua.at/media/noctua_nv_ps1_manual_en_web.pdf?download=true'),
 ('S7','NA-FH1 features','https://www.noctua.at/en/products/na-fh1/features')]
budget = {'basis':'Nominal arithmetic, not measured startup or coordinated protection',
 'voltage_V':12, 'fan_count':4, 'fan_current_A':0.35,
 'fan_total_A':4*0.35, 'fan_total_W':12*4*0.35,
 'supply_limit_A':2, 'hub_input_limit_W':24,
 'nominal_difference_A':2-4*0.35, 'auxiliary_load_A':'UNKNOWN',
 'startup_sensitivity':[{'assumed_multiplier':k,'fan_only_A':1.4*k,
 'difference_to_2A':2-1.4*k} for k in (1,1.25,1.5,2)],
 'voltage_drop_example':{'assumptions':'Copper rho 0.0175 ohm mm2/m at reference temperature; 1 m one-way; 0.5 mm2; 1.4 A. NOT cable selection.',
 'drop_V':2*1*0.0175/0.5*1.4}}
assert abs(budget['fan_total_W']-16.8)<1e-9
assert abs(budget['nominal_difference_A']-.6)<1e-9
assert abs(budget['voltage_drop_example']['drop_V']-.098)<1e-9
checks['arithmetic_checks']=3
def js(name, data): (OUT/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
js('checks.json',checks); js('power_budget.json',budget)
js('sources.json',{'accessed':'2026-10-04','sources':[dict(zip(('id','title','url'),s)) for s in sources],
 'scope':'Manufacturer descriptions only; no India stock, price, whole-device compliance or delivered-unit verification claimed.'})
interfaces = [
 ['J01','Site outlet -> NV-PS1','OEM mains plug','Site socket / upstream protection / India conformity unresolved; no bare-mains modification'],
 ['J02','NV-PS1 -> NA-AC10','OEM barrel connection','5.5 / 2.1 mm; use supplied keyed adapter, do not infer polarity from size'],
 ['J03','NA-AC10 -> NA-FC1 input','OEM 4-pin connection','Review reference chain; protective switching insertion not yet selected'],
 ['J04','NA-FC1 output -> NA-FH1 input','OEM 4-pin / NA-EC1','24 W path limit; no SATA supply'],
 ['J05-08','NA-FH1 ports 1-4 -> fans F1-F4','OEM keyed 4-pin','One fan per port; four independent labels; exact cable routing and extensions unresolved'],
 ['J09','Protective module -> fan power permission','UNSELECTED','DC load breaking, latched inhibit, monitored recovery and failure response require rated design'],
 ['J10','Logger -> instruments only','Separate domain','No USB connection to hub / fan power; no GPIO safety or fan supply'],
 ['J11','Service isolation -> all energy sources','UNSELECTED','Prevent reconnection; stopped impeller / dark lamp not proof of isolation']]
bom = [
 ['F1-F4','4','ARCTIC P14 Max black ACFAN00287A','REFERENCE','12 V / 0.35 A each; exact delivered revision still verify; S1'],
 ['PS1','1','Noctua NV-PS1 incl. NA-AC10','REFERENCE','12 V / 2 A / 24 W; external Class II adapter; S2/S6'],
 ['SC1','1','Noctua NA-FC1','REFERENCE','3 A / 36 W maximum; NOT protective stop; S3'],
 ['H1','1','Noctua NA-FH1 incl. NA-EC1','REFERENCE','24 W on selected input; self-resetting fuse; S4/S5'],
 ['PR1','1 assembly','Independent protective control and isolation','UNSELECTED','Not replaced by PWM controller, hobby relay or this Python model'],
 ['CB1','1','Insulating / protected low-voltage enclosure','UNSELECTED','140 x 100 x 40 CAD reservation only; mount and ventilation to resolve'],
 ['W1','as needed','OEM compatible extensions / strain relief','UNSELECTED','Length, temperature, voltage drop, retention and guard entry required'],
 ['PB','set','START / STOP / RESET and indicators','UNSELECTED','Ratings and protective architecture must be selected together']]
def csvout(name, header, rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)
csvout('INTERFACES.csv',['ID','Endpoints','Connection','Release limitation'],interfaces)
csvout('BOM.csv',['ID','Quantity','Item','Status','Basis'],bom)
c=canvas.Canvas(str(OUT/'AQI_D01_ELECTRICAL_REVIEW.pdf'),pagesize=(595,842))
c.setTitle('AQI D01 - Electrical and controls review E00')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=16,textColor=HexColor('#203747'))
page=0;y=0
def para(text):
    global y
    p=Paragraph(text,style);w,h=p.wrap(503,700)
    assert y-h>62, (page,text[:50],y,h)
    p.drawOn(c,46,y-h);y-=h+13
def new(title,subtitle):
    global page,y
    if page:c.showPage()
    page+=1
    c.setFillColor(HexColor('#102d3c'));c.rect(0,726,595,116,fill=1,stroke=0)
    c.setFillColor(HexColor('#70dec5'));c.setFont('Helvetica-Bold',10);c.drawString(46,801,'AQI TOWER / D01 / E00 / 04 OCT 2026')
    c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',21);c.drawString(46,765,title)
    c.setFillColor(HexColor('#203747'));c.setFont('Helvetica',10);c.drawString(46,706,subtitle)
    c.setFont('Helvetica-Bold',8);c.drawString(46,32,'REVIEW ONLY - NOT RELEASED FOR WIRING OR ENERGIZING')
    c.drawRightString(548,32,str(page));y=675
new('Powering the first prototype','Package 2: one electrical review for the existing R03M assembly')
para('<b>Decision:</b> retain four 12 V fans and an external OEM power adapter as the reference route. Keep mains wiring outside the cabinet. Use local speed adjustment; no app or custom power PCB is needed for the first experiment.')
para('<b>What this closes:</b> the OEM connection reference, nominal load calculation, named interfaces, enclosure fit screen, restart acceptance model and fault-test specification are now in one reproducible package.')
para('<b>What it does not close:</b> the rated protective stop/restart circuit. The OEM chain can run fans, but does not itself satisfy our manual-restart requirement. It is not an approved wiring diagram.')
para('<b>DETECTED:</b> four fans total 1.40 A / 16.8 W nominal. The adapter and selected hub input are limited to 2 A / 24 W. The difference is 0.60 A before controller/hub consumption, startup and tolerances; it is not proven spare capacity.')
para('<b>RECOMMENDATION:</b> retain the external adapter, fixed guards and separate protective module approach. Do not add a 24 V safety relay merely to fill a BOM: a separate control supply can remain alive while the 12 V supply trips and recovers.')
para('<b>Physical prototypes: 0.</b> No components purchased, no electrical tests performed. This indoor demonstrator does not prove outdoor cleaning radius, heat tolerance or vandal resistance.')
new('E01 / power connection reference','Block-level architecture; lines are interfaces, not conductor or terminal instructions')
def box(x,y,w,h,text,amber=False):
    c.setFillColor(HexColor('#fff0da' if amber else '#e2f3ef'));c.setStrokeColor(HexColor('#bd7c22' if amber else '#267b72'));c.roundRect(x,y,w,h,5,fill=1,stroke=1)
    p=Paragraph(text,ParagraphStyle('box',parent=style,fontSize=10,leading=13));_,hh=p.wrap(w-18,h);p.drawOn(c,x+9,y+(h-hh)/2)
def arrow(x,y,x2,y2):
    c.setStrokeColor(HexColor('#203747'));c.line(x,y,x2,y2);c.line(x2,y2,x2-4,y2+6);c.line(x2,y2,x2+4,y2+6)
for yy,txt in [(613,'SITE OUTLET / service isolation: installation review OPEN'),(532,'PS1: external NV-PS1 / supplied NA-AC10'),(451,'PR1: protective switching + restart inhibit / UNSELECTED'),(370,'SC1: NA-FC1 manual speed controller'),(289,'H1: NA-FH1 4-pin INPUT / SATA NOT CONNECTED'),(208,'F1 + F2 + F3 + F4 / separate hub outputs 1-4')]:
    box(66,yy,463,51,txt,yy in (613,451))
    if yy>208:arrow(297,yy,297,yy-30)
y=186
para('PR1 is a <b>proposed insertion boundary</b>, not a verified inline product or terminal assignment. Its sensing, switching, fault response and connection harness are still unselected. The unmodified OEM reference chain omits PR1 and therefore is NOT our released system.')
para('Logger/instruments remain electrically separate. No SATA, motherboard, USB fan-power source or remote-start path is part of this reference.')
new('E05 / load and rating screen','Calculated from published nominal values; no startup waveform or physical test')
para('<b>Fan load:</b> 4 x 0.35 A = 1.40 A; 12 V x 1.40 A = 16.8 W. NA-FC1 rating is 3 A / 36 W, but it does not raise the 24 W supply/hub-path ceiling. [S1-S4]')
para('<b>Startup sensitivity, not predicted inrush:</b><br/>1.00 x nominal: 1.40 A; difference to 2 A = +0.60 A.<br/>1.25 x: 1.75 A; difference = +0.25 A.<br/>1.50 x: 2.10 A; difference = -0.10 A.<br/>2.00 x: 2.80 A; difference = -0.80 A.<br/>All exclude auxiliary current. Startup approval remains OPEN.')
para('<b>Cable calculation example only:</b> with assumed copper resistivity 0.0175 ohm mm2/m, 1 m one-way length, 0.5 mm2 conductors and 1.4 A, loop drop is 0.098 V before connectors. This does NOT select cable size: actual length, insulation, temperature, fault protection and terminations remain unknown.')
para('<b>Protection is not sized from 1.4 A alone.</b> Supply short-circuit behavior, switching DC capability, contact welding, branch cable withstand and protection coordination must be established together. No invented fuse, breaker or wire rating is issued.')
para('<b>Temperature:</b> NV-PS1 is specified 0-40 C; the fan has the same project ceiling. Ambient rating is not allowance for a hotter closed enclosure. Keep the adapter external; verify actual worst-case internal temperatures. No India outdoor approval follows.')
para('<b>Class II adapter:</b> do not add an improvised earth connection to it. Whole-assembly bonding and installation protection need review; its component class does not certify the cabinet. Plug types C/A/G supplied are not proof of suitability for the actual Indian outlet. [S2]')
new('E02 / restart and failure behavior','An executable requirements model is supplied - NOT controller firmware')
para('<b>Required sequence:</b> power restored -> OFF; release START -> fresh START -> RUN REQUESTED. Fault -> TRIPPED; restore verified permissives -> release and press RESET -> OFF; release and press START -> RUN REQUESTED. STOP always wins.')
para('<b>Important finding 1:</b> NA-FH1 uses self-resetting input protection. Its manual instructs disconnecting all power for one minute to reset after a trip. That is not a latched protective-stop guarantee. Recovery must not create an unintended run condition. [S5]')
para('<b>Important finding 2:</b> the upstream RPM signal comes from output 1 only. Four status LEDs are not four independent protective feedback channels. One healthy fan cannot prove all four are operating. [S5/S7]')
para('<b>Important finding 3:</b> a separate 24 V control supply may stay powered when the 12 V fan supply fails. A held run contact could then restart fans on recovery. Monitor the relevant power domain; also resolve downstream hub/fan recovery, which upstream voltage monitoring alone cannot detect.')
para('<b>Model checks:</b> '+str(len(checks['named_checks']))+' named sequences and '+str(checks['exhaustive_one_step_cases'])+' one-step combinations pass. Missing permissive, held START/RESET, power restoration, STOP priority and trip reset are covered. Ideal inputs only: no sensor, contact, timer, diagnostic coverage or safety integrity is proven.')
para('<b>Selection hold:</b> no complete rated PR1 architecture has been established. A basic hold-in relay, PWM zero setting, hub fuse, fan RPM LED or Python test cannot close this gate. Determine required protective reliability and access/run-down measures before assigning terminal numbers.')
new('E03 / E04: cabinet interfaces','Existing mechanical CAD is preserved; no unverified holes or enclosure added')
para('<b>OEM dimensions:</b> hub 93 x 43 x 12.5 mm; controller 48 x 25 x 21 mm. The CAD reservation is 140 x 100 x 40 mm, not selected internal enclosure space. Controller + hub can only be screened geometrically; connectors, bend radii, cover, retention and thermal clearances are not included. [S3/S4]')
para('<b>Placement recommendation:</b> keep only low-voltage OEM speed/hub parts in the side enclosure. Keep adapter and the eventual protective assembly external. Do not assume a relay panel fits in the reservation or hang its mass on an unreviewed cabinet joint.')
para('<b>Mechanical handoff:</b> reservation x=550..590, y=110..250, z=390..490 mm. Reserved cable corridor runs (435,180,595) to (565,180,595) to (565,180,490). Coordinates use R03M CAD axes; this is space allocation, not a drilled feed-through.')
para('<b>Guard crossing remains OPEN:</b> actual entry needs retention, edge protection and a reach-safe closure. Do not drill a generic hole in the guard. Obtain routed lengths and connector envelopes before choosing extensions. The included hub input cable is 300 mm; the reserved external route alone uses about 235 mm. [S7]')
para('<b>Interface schedule:</b> J01 site supply; J02 OEM barrel adapter; J03 controller input; J04 hub input; J05-08 four fan leads; J09 protective permission; J10 independent logger; J11 service isolation. The accompanying CSV records each endpoint and its remaining limitation. No pin numbers inferred from cable colors.')
para('<b>Parts status:</b> four named OEM products are reference candidates, not procurement release. Protective module, enclosure, switches, extensions, strain relief and isolation are unresolved. No prices or India stock invented; see BOM.csv.')
new('E06 / physical acceptance and release','All physical cases below are NOT EXECUTED')
para('<b>Before power:</b> confirm delivered product/manual revisions and source suitability; inspect guards, cable retention, polarity and terminations; complete applicable insulation, bonding and protection tests using qualified procedures. Do not improvise test voltages from this pack.')
para('<b>Controlled operating tests:</b> no motion on power application; deliberate start/stop; held START during restoration; simultaneous START/STOP; RESET without START; held RESET on fault recovery; interruption of fan power with control power remaining. Record actual run-down before considering any access release.')
para('<b>Fault review / safe simulation:</b> resolve hub self-reset, individual fan fault/recovery, missing PWM command, loss of protective input and switched-contact failure. Do not short live circuits, block blades, defeat guards or damage fans to simulate faults. Approved methods may use documents and isolated test fixtures.')
para('<b>Measurements:</b> capture four-fan startup and steady current, controller/hub auxiliary load, fan-terminal voltage, supply recovery and enclosure temperature at the intended environment. RPM/PM readings do not certify safe standstill or filter sealing.')
para('<b>Finite release blockers:</b><br/>1. Rated PR1 protective implementation including downstream recovery and access/run-down.<br/>2. Cable/enclosure/guard-entry detail and product/interface compatibility.<br/>3. Site supply review, applicable safety classification and qualified commissioning evidence.<br/>Mechanical strength/seal/guard holds and actual filter/airflow evidence remain separate gates.')
para('<b>Critical path:</b> protective design and interface closure -> qualified design review -> authorized purchasing/fabrication -> inspected assembly -> controlled commissioning -> indoor airflow/particle test. Supplier delivery, review availability and physical results are unknown, so no completion date is invented.')
new('Evidence and reproducibility','Sources checked 4 October 2026; manufacturer content remains owned by its publisher')
for sid,title,url in sources:
    para(f'<b>{sid} - {title}</b><br/><link href="{url}" color="#087c70">{url}</link>')
para('Run scripts/analysis/d01_control_acceptance.py for the abstract checks. Run scripts/reports/build_d01_electrical_package.py to reproduce calculations, schedules, report and bundle. Checks do not certify hardware. Historical 230 V fan wiring is not applicable to D01.')
c.save()
readme='''# D01 electrical review E00 - 4 October 2026

Open **AQI_D01_ELECTRICAL_REVIEW.pdf**. This is the consolidated package 2 review for R03M, NOT released wiring or energization instructions.

Includes: OEM power-reference schematic; nominal and startup-sensitivity arithmetic; interface CSV; reference/unresolved BOM; enclosure/cable integration constraints; restart requirements with executable abstract tests; physical commissioning cases and three explicit electrical release blockers.

The protective module remains UNSELECTED. Hardware implementation, conductor/fuse ratings, terminal assignments, protective reliability and physical commissioning are not complete. Model PASS does not change this status. All physical tests NOT EXECUTED; prototypes 0.

The hub self-resetting protection and single upstream RPM channel prevent claiming this OEM chain is an independent four-fan protective system. Keep SATA unused and logger independent. No purchases, installations, supplier messages or publication performed.

Reproduce from repository root using Python with ReportLab:
`python scripts/analysis/d01_control_acceptance.py`
`python scripts/reports/build_d01_electrical_package.py`

Next meaningful work: finish rated protection/interface engineering and the actual filter/flow validation package, not another cosmetic CAD branch. Outdoor/public deployment remains unqualified.
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')
for source in (ROOT/'scripts/analysis/d01_control_acceptance.py',Path(__file__)):
    (OUT/source.name).write_bytes(source.read_bytes())
files=[p for p in OUT.iterdir() if p.is_file() and p.suffix not in ('.zip',) and p.name!='MANIFEST.json']
js('MANIFEST.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
with zipfile.ZipFile(OUT/'AQI_D01_ELECTRICAL_REVIEW.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files+[OUT/'MANIFEST.json']:z.write(p,p.name)
print(json.dumps({'pages':page,'checks':checks,'output':str(OUT)},indent=2))
