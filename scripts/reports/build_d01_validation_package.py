"""Generate R03M validation package; leave all physical result fields blank."""
import csv,hashlib,importlib.util,json,zipfile
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
R=Path(__file__).resolve().parents[2];O=R/'reports/prototype_d01/validation_package';O.mkdir(parents=True,exist_ok=True)
s=importlib.util.spec_from_file_location('v',R/'scripts/analysis/d01_validation.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
data=v.pressure_rows();tests=v.selftest()
def js(name,obj):(O/name).write_text(json.dumps(obj,indent=2),encoding='utf-8')
def csvfile(name,fields,rows):
    with (O/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
js('R03M_PRESSURE_BUDGET.json',data);js('checks.json',tests)
csvfile('R03M_PRESSURE_BUDGET.csv',list(data['rows'][0]),data['rows'])
fields=['run_id','cell_id','instrument_id','calibration_ref','method_ref','assembly_revision','timestamp','evidence','quality','cell_area_m2','normal_velocity_ms','velocity_error_bound_ms']
csvfile('AIRFLOW_BLANK.csv',fields,[dict(cell_id=str(i),assembly_revision='R03M',evidence='NOT_MEASURED') for i in range(1,10)])
csvfile('RUN_LOG_BLANK.csv',['run_id','date','operator','reviewer','assembly_revision','filter_part_revision','fan_setting','room_volume_m3','temperature_C','humidity_percent','ambient_pressure_Pa','flow_m3h','filter_left_dp_Pa','filter_right_dp_Pa','input_W','noise_dBA','instrument_refs','method_ref','anomalies','status'],[dict(assembly_revision='R03M',status='NOT_EXECUTED')])
csvfile('PARTICLE_TIMESERIES_BLANK.csv',['run_id','mode_off_on','timestamp','elapsed_seconds','sensor_id','location','PM25_ug_m3','temperature_C','humidity_percent','windows_doors_hvac','quality_note'],[])
rows=[r for r in data['rows'] if r['reducer_K']==1]
c=canvas.Canvas(str(O/'AQI_D01_VALIDATION_PACKAGE.pdf'),pagesize=(595,842));c.setTitle('AQI D01 validation package V00')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=16,textColor=HexColor('#203747'));page=0;y=0
def para(text):
    global y
    p=Paragraph(text,style);_,h=p.wrap(503,700);assert y-h>65;p.drawOn(c,46,y-h);y-=h+14
def new(title):
    global page,y
    if page:c.showPage()
    page+=1;c.setFillColor(HexColor('#102d3c'));c.rect(0,735,595,107,fill=1,stroke=0);c.setFillColor(HexColor('#70dec5'));c.setFont('Helvetica-Bold',10);c.drawString(46,805,'AQI TOWER / D01 / VALIDATION V00 / 04 OCT 2026');c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',22);c.drawString(46,765,title);c.setFillColor(HexColor('#203747'));c.setFont('Helvetica-Bold',8);c.drawString(46,32,'NO PHYSICAL RESULTS - TESTING ONLY AFTER MECHANICAL / ELECTRICAL RELEASE');c.drawRightString(550,32,str(page));y=708
new('What the prototype must prove')
para('<b>First milestone:</b> one safely assembled indoor unit with recorded airflow, filter pressure loss, electrical power, temperature and repeatable particle trends. Not a full outdoor tower and not a certified HEPA air cleaner.')
para('<b>This delivery:</b> current R03M pressure screen, blank measurement workbook (three CSV sheets), a strict airflow calculator, synthetic regression tests and one physical test sequence. No fabricated results fill the empty fields.')
para('<b>Important correction:</b> both guard patterns now use 0.0354623 m2 open area each, not the earlier 0.036 m2. With the same assumed loss coefficient, each guard loss increases by about 3.06%. This does not verify the loss coefficient or actual guard resistance.')
para('<b>Our project:</b> a custom cabinet, seals, service arrangement, guarded four-fan assembly and measured system integration. Buying OEM fans/filters is normal; it does not make the system a proven product or a patentable invention.')
para('<b>Stop condition:</b> do not energize the review-only assembly to collect these data. Mechanical strength/guard/seal review and the rated protective electrical design remain open. The test workbook is ready; the hardware is not yet released.')
para('<b>Evidence labels:</b> OEM = published component data; ASSUMED = modeling choice; CALCULATED = arithmetic from stated inputs; MEASURED = physical record with method/instrument evidence. At present, physical prototypes and physical test runs both equal zero.')
new('Updated pressure budget')
para('<b>Calculated, not measured:</b> four fans in parallel add flow, not pressure. Two filter paths each carry half the total flow only under the equal-sharing assumption. Filter pressures must not be added as if the two paths were in series.')
para('<b>Central assumed reducer K = 1:</b><br/>'+ '<br/>'.join(f"Total {r['total_m3h']} m3/h / each filter {r['per_filter_m3h']:.0f}: fan {r['fan_Pa']:.2f} Pa; other losses {r['nonfilter_Pa']:.2f} Pa; filter allowance <b>{r['filter_allowance_Pa']:.2f} Pa</b>." for r in rows))
para('<b>Meaning:</b> the filter must fit inside the remaining pressure allowance at that same flow in this model. Negative allowance means the assumed non-filter losses already exceed the curve pressure. Positive allowance is NOT proof that the actual filter fits.')
para('<b>Model assumptions:</b> OEM numeric curve at full 2800 rpm; density 1.2 kg/m3; 134.2 mm fan apertures; 350 x 270 mm opening per filter. Guard K1.5 each, plenum K1.5 and installation K1 on their stated velocity references. Reducer K0.5/1/2 sensitivities are included in the CSV.')
para('<b>Still unknown:</b> actual installed fan curve, clean/loaded filter curve, guard K, bypass, uneven flow sharing and outlet recirculation. Reducer and plenum losses may overlap. Static pressure compatibility remains unresolved. These are not guaranteed bounds or a new CFD validation.')
para('<b>Decision:</b> keep 300 m3/h as a provisional investigation point, not a product claim. Do not increase the power supply or fan speed beyond OEM limits to force that result. Change the design if actual flow/pressure evidence demands it.')
new('Measure flow before claiming cleaning')
para('<b>1. Identify the exact assembly.</b> Record CAD revision, delivered fan/filter identities, seals, guards, speed setting, room conditions and instrument/calibration references. Photograph the complete guarded configuration. Keep raw records unchanged.')
para('<b>2. Use a reviewed flow method.</b> Prefer a suitable calibrated capture arrangement or an engineered duct traverse. A handheld reading at one outlet point multiplied by gross area is not a valid total flow measurement. Swirl, nonuniform velocity and both guard layers matter.')
para('<b>Fixture warning:</b> a hood or duct can restrict this low-pressure fan system. Record fixture resistance and use a method validated for the installed configuration; do not call a loaded-fixture flow the unrestricted device flow without justification. Fixture dimensions and correction are not yet selected.')
para('<b>3. Record area-weighted cells.</b> AIRFLOW_BLANK.csv contains empty placeholders, not an approved nine-point traverse. For an accepted normal-velocity map, Q = 3600 x sum(cell area x mean normal velocity). Cells must cover the chosen plane once without overlap; the reviewer determines sampling and averaging.')
para('<b>4. Quantify error.</b> The calculator reports only a conservative velocity-error contribution, 3600 x sum(area x velocity error bound). Area, temporal drift, probe alignment, fixture loading/leakage and spatial sampling require a separate full uncertainty budget. It does not manufacture a confidence interval.')
para('<b>5. Record pressure and power.</b> Measure each filter-path pressure drop separately using reviewed static tap positions. Do not drill before sealing/reach review. Record total electrical input with a suitable rated instrument; 16.8 W nominal fan load is not measured wall power.')
new('Particle trial: useful, not certification')
para('<b>Prepare a controlled room.</b> Record room dimensions, sensor positions, ventilation/HVAC, doors/windows and occupancy. Compare sensors together beforehand; document their response, limitations and detection floor. Keep locations and room conditions comparable across runs.')
para('<b>Do not generate smoke or dust yourself.</b> No incense, combustion, powders or deliberate pollutant release in an occupied room. A formal challenge-aerosol test belongs with an equipped competent service. If ambient particles are too low or unstable, mark the trial inconclusive.')
para('<b>Suggested engineering trial:</b> paired device-OFF baseline and device-ON observation windows, repeated under comparable conditions, using naturally present particles. Log raw PM, temperature and humidity; do not choose only the best-looking interval. Duration must provide adequate signal while conditions remain stable; no invented universal duration.')
para('<b>Analysis boundary:</b> a PM decrease may reflect settling, ventilation, changed sources or sensor humidity response. A simple before/after percentage is not device efficiency. Blank particle data are supplied, but no automatic CADR calculator is issued before the room method and uncertainty are defined.')
para('<b>What can be reported:</b> dated observations, run conditions, measured flow/power, particle trends and limitations. Formal CADR needs a validated method; HEPA-level efficiency needs appropriate filter/installed-leak evidence. Airflow alone proves neither.')
para('<b>No outdoor bubble claim:</b> indoor results cannot establish a public-space radius or tower spacing. Heat, weather, wind, public access, stability and maintenance are separate design and test problems. Carbon/gas removal is outside this particulate trial.')
new('Acceptance, tools and handoff')
para('<b>Before testing:</b> rated protective design and qualified commissioning; guard/access/strength/seal closure; calibrated instruments and a reviewed test method. Funding-only support means rent instruments or commission an equipped service; no college lab is assumed.')
para('<b>Instrument functions, not purchase orders:</b> total-flow measurement suitable for low-pressure fans; differential pressure measurement resolving expected small losses; rated input-power measurement; temperature/humidity logging; comparable particle monitors; noise meter if reporting noise. Exact ranges/accuracy and availability must match the approved method.')
para('<b>Acceptance rules:</b> safety faults mean STOP. Missing method, invalid calibration, leaks, sensor saturation, unstable room conditions or insufficient particle signal mean INVALID/INCONCLUSIVE, not PASS. Flow below a project target requires design review; the 300 m3/h investigation point is not a safety or certification threshold.')
para('<b>Reproducible tools:</b> run scripts/analysis/d01_validation.py for synthetic tests. With accepted physical data: add --airflow-csv FILE --plane-area-m2 AREA --output NEW_FILE.json. AREA is the independently established full measurement plane, not automatically guard hole area. Cell-area sums, timezone-qualified timestamps and calibration consistency are checked; equal area sums do not prove non-overlapping spatial coverage. Source CSV hash is recorded. Existing output files are not overwritten. Blank templates, NaN, missing evidence, duplicate cells and mixed runs are rejected.')
para(f"<b>Checks completed:</b> {tests['passed']} synthetic/arithmetic checks. Input hashes link the pressure screen to the OEM CSV and current guard pattern. No physical measurements or tests performed; no purchases, installation or supplier messages.")
para('<b>Three packages now exist, not three approvals:</b> mechanical R03M; electrical E00; validation V00. Remaining critical path is actual protective/structural/interface closure, qualified review, authorized build, commissioning and measured performance. More PDFs cannot substitute for those steps.')
para('<b>Sources:</b> archived ARCTIC numeric workbook (source URL/hash in JSON); R03M guard_pattern.json; <link href="https://www.epa.gov/indoor-air-quality-iaq/guide-air-cleaners-home" color="#087c70">EPA Guide to Air Cleaners</link> and <link href="https://www.epa.gov/emergencies-iaq/diy-air-cleaners" color="#087c70">EPA DIY Air Cleaners</link>, checked 4 October 2026. EPA guidance is not approval of D01. Test procedures here are proposed project methods, not copied certification standards.')
c.save()
js('sources.json',{'accessed':'2026-10-04','fan_workbook':'https://support.arctic.de/products/p14-max/techdocs/P14%20Max%20-%20PQ%20Curve%20for%20CFD.XLSX','fan_evidence':'Previously archived numeric data, not redownloaded this turn','guidance':['https://www.epa.gov/indoor-air-quality-iaq/guide-air-cleaners-home','https://www.epa.gov/emergencies-iaq/diy-air-cleaners']})
(O/'README.md').write_text('''# D01 validation V00

Read AQI_D01_VALIDATION_PACKAGE.pdf. Five-page consolidated validation pack for mechanical R03M and electrical E00. NOT permission to energize. All physical records are blank / NOT EXECUTED.

R03M_PRESSURE_BUDGET uses actual proposed guard hole area, keeping loss coefficients explicitly assumed. It replaces the older 0.036 m2 guard-area screen for this revision only; no operating flow is established.

The CSV workbook consists of AIRFLOW_BLANK, RUN_LOG_BLANK and PARTICLE_TIMESERIES_BLANK. Copy templates into a new dated run folder; never replace raw observations. Cell count/layout must follow an approved measurement method. No automatic CADR/HEPA/outdoor claim.

From repository root:
`python scripts/analysis/d01_validation.py`
`python scripts/analysis/d01_validation.py --airflow-csv PATH --plane-area-m2 AREA --output NEW_PATH.json`
`python scripts/reports/build_d01_validation_package.py`

The analyzer validates arithmetic inputs, not their truth or calibration. Velocity-only error is not a full uncertainty budget. Physical review and commissioning remain required. Sources and input hashes accompany the pack.
''',encoding='utf-8')
for p in (R/'scripts/analysis/d01_validation.py',Path(__file__)):(O/p.name).write_bytes(p.read_bytes())
files=[p for p in O.iterdir() if p.is_file() and p.suffix!='.zip' and p.name!='MANIFEST.json']
js('MANIFEST.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
with zipfile.ZipFile(O/'AQI_D01_VALIDATION_PACKAGE.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files+[O/'MANIFEST.json']:z.write(p,p.name)
print(json.dumps({'pages':page,'tests':tests,'central_rows':rows},indent=2))
