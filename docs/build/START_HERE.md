# From digital study to a real tower

**Latest assembly / package1:** [R03M mechanical package](../../reports/prototype_d01/mechanical_package/README.md). One batch covers fastener stacks, joined guards, foot retention, seal stops, CAD/exploded view, drawings and assembly sequence.493 objects and119,805 checked pairs clear. Do not mix old rod lengths/base/guard blank patterns with this revision. Mechanical materials/strength/seal/access holds remain; package2 controls/enclosure interface unresolved. Review only.

**START WITH THE CONSOLIDATED HANDOFF:** [current D01 review package](../../reports/prototype_d01/current_handoff/README.md).15-page PDF and bundled current assembly,10 CAD-extracted panel DXFs, inventory and explicit missing items.29,116 whole-assembly checked pairs clear;774 excluded. Current conditional pressure allowance14.61Pa/filter at300m3/h total under stated assumptions, NOT actual flow. Mechanical/electrical/performance gates remain OPEN. This replaces navigation between delta-only deliveries; historical material follows.

**Current assembly:** [R02G independent guard mountings](../../reports/prototype_d01/r02_guards/README.md). Separates four shared bolts into four per guard.245 valid objects;8,641 changed-part pair checks and16 assumed tool checks clear. Revised plate/skirt drilling and hardware drawing supplied. Guard seams/rivets, strength, reach protection, electrical isolation/restart and filter evidence remain unresolved. Review only.

**Current hardware detail:** [R02H fastening/service revision](../../reports/prototype_d01/r02_adapter/hardware_detail/README.md).229 valid objects;13,644 changed-part pair checks and two200 mm filter sweeps clear. Adapter nuts/washers/heads now modeled. Tool access, inherited M5/guards, seal/strength and electrical gates remain open. No construction release.

**Latest integrated CAD:** [R02 removable filter adapter](../../reports/prototype_d01/r02_adapter/README.md).169 objects,5,310 new-part pair checks clear, native/STEP checks pass. Review-only cassette on the existing cabinet; new sealing/support features and dimensioned drawings provided. DO NOT use R01 airflow predictions for this different filter. No construction/energization release.

**Current user direction: internet-only sourcing preparation; no supplier-chasing task for the user.** [Online alternatives and actual interface comparison](../../reports/prototype_d01/component_validation/D01_ONLINE_FILTER_OPTIONS.pdf) now supersedes the inquiry-sending workflow below. IKEA/Smart Air options need sealed adapters and pressure validation; Filtrete import offers are costly and inconsistent. Inquiry gasket490/470mm was erroneous; saved CAD uses495.3/475.3mm. No purchase/fabrication release.

**Filter decision needs external data:** [prepared technical inquiry](../../reports/prototype_d01/component_validation/FILTER_INQUIRY_UNSENT.md), not sent. Exact dimensions and per-filter low-flow resistance are requested; returned-data checker has ten passing synthetic tests. No obtainable drop-in filter is approved yet. Sending or ordering requires explicit user authorization.

**Deployment boundary:** [India heat, robustness and size review](INDIA_DEPLOYMENT_BASIS.md). D01 is not suitable for unattended public/outdoor use. Keep supervised indoor prototype closure on the critical path; outdoor heat/weather/tamper protection require a separately qualified assembly and actual host site. Five added calculation checks completed, not safety certification.

**Latest component evidence:** [D01 fan-data comparison and filter allowance](../../reports/prototype_d01/component_validation/README.md). OEM numeric curve archived, source discrepancies retained; nine checks pass. R01 CAD unchanged. Approximately14.5Pa filter allowance at300m3/h total is a provisional selection screen, not tested performance. Exact obtainable filter and safety details still block construction release.

**D01 continuation:** [R01 construction detail package](../../reports/prototype_d01/r01/README.md) now updates the same assembly with guard brackets, cabinet joints, shelf supports and cable routing. R01 drilling files and revised pressure assumptions supersede corresponding R00 details for review, not for fabrication release.

**Latest 3 October recommendation:** [D01 integrated indoor demonstrator](../../reports/prototype_d01/README.md) now supplies one CAD assembly, drawings, BOM and calculation package. It proposes a smaller 12 V/MERV13 first build to unblock physical learning; it does not validate or release the full-size HEPA plan below. Physical prototypes remain0. Read its explicit component, mechanical and restart-control gaps before treating any drawing as a construction instruction.

Updated: 3 October 2026. Status: preliminary planning, NOT released for fabrication.

## The decision

Build one full-size particulate-filtering prototype first, test it indoors, then investigate outdoor operation. The final goal remains an outdoor tower network. An indoor test is a controlled stepping stone, not proof of outdoor coverage.

User clarification: previous small-device work was digital, not a physical test. No physical tower measurements are available in the reviewed records. College/NGO support is funding only: no college lab assumed. Pune, Hyderabad or Mumbai are possible locations; actual premises/room and outdoor site remain UNKNOWN. Budget should be reasonable; no fixed ceiling or deadline was supplied. An ENTC reviewer is optional/unconfirmed; the assistant still prepares the design and software.

The first build path is **guarded intake -> removable coarse prefilter -> sealed HEPA cassette -> clean-air plenum -> fan -> guarded outlet**. Reserve space for a removable gas-filter module, but do not fit an uncharacterized carbon bed or claim gas cleaning in the first demonstration. This is a RECOMMENDATION to speed particulate validation; the research concept with carbon remains in the historical records. No water stage, ionizer or ozone generator. Grid power first; solar after measuring consumption.

## What already exists and what does not

| Item | Evidence/status | What must happen next |
|---|---|---|
| GEO_C airflow layout | DETECTED: digital geometry optimization | Convert into a physical assembly; GEO_C is not a construction drawing |
| Sealed HEPA airflow | DETECTED: about 1,332 m3/h in `results/FILTER_H13/bypass_analysis_sealed.json` | Partial/nonconverged CFD; verify actual airflow and bypass |
| Physical filter size | DETECTED: candidate HEPA 593 x 593 x 292 mm | Old `docs/CAD_V00.md` has 30 mm stage placeholders; rebuild packaging |
| Seal | DETECTED: CFD boundary closes a bypass path | Draw gasket, clamping frame and door; boundary condition does not prove leak-tightness |
| Fan | DETECTED: historical KVO 250/KVO 250 L data, 250 mm port, 301 W, 20 kg | Confirm exact SKU, current curve, envelope, wiring and availability with OEM |
| Physical test | NOT DONE in reviewed records; confirmed digital-only by user | Obtain instruments and conduct controlled tests |
| Mechanical structure | Missing fabrication drawings, mass/stability calculations | Mentor/fabricator review before release |
| Electrical system | Missing rated wiring, protection and terminal drawings | Electrical engineer review and qualified assembly |
| Procurement | Historical lab BOM is not a tower BOM | Use the new preliminary tower parts list |
| Outdoor bubble | UNKNOWN | Measure breathing-height effects under wind; no guaranteed radius |

Also: `cad/parametric/v00.json` describes a different small envelope from CAD_V00. Do not treat all historical models as one physical machine. Phase 19 and pressure-budget records use differing prefilter loading thresholds; set the maintenance limit from supplier data and measured operating flow, not an inherited 80/100 Pa number.

## Calculations that change the build decision

Run `python scripts/analysis/build_screening.py`. Its generated output is `results/build_screening.json`. These are screening calculations, not a fresh CFD run or measured performance.

- A 250 mm connection carrying 1,300 m3/h has about 7.36 m/s velocity and 32.5 Pa dynamic pressure (density assumed 1.2 kg/m3). Bends, guards and transitions can matter: an assumed loss coefficient of 1 adds about 32.5 Pa. Do not trust the historical 3.8 Pa residual as the whole new tower's loss.
- At 1,300 m3/h, the historical fan curve is already nearly consumed by the modeled clean HEPA/prefilter combination. The earlier claim of 57–67 Pa spare carbon margin must not be used at that same flow. Available head must be compared with ALL losses at the SAME target flow.
- An illustrative carbon contact time of 0.1 seconds would require about 36 litres of bed volume at 1,300 m3/h. This says nothing about gas removal or bed pressure drop; those require material-specific data.
- If whole-device efficiency were 90%, an illustrative 1,300 m3/h flow gives 1,170 m3/h effective clean-air flow. At an assumed 5 air changes/hour and 3 m ceiling, that corresponds to 78 m2 in an ideally mixed enclosed room. Neither the efficiency nor that area is a tested rating.
- Wind at 1 m/s through an illustrative 10 m wide x 2 m high outdoor section carries 72,000 m3/h. Comparing this with 1,300 m3/h shows why an indoor result cannot establish a large outdoor bubble. This is a scale comparison, NOT a predicted cleaning percentage.

The current fan is a benchmark candidate, not a commitment for the larger final tower. Request competing fan curves at a defined loaded-system duty point. More free-air flow alone is not enough.

## Read the build package

Fan decision input: [copyable selection brief and three-flow duty comparison](FAN_SELECTION_BRIEF_R00.md), with [response sheet](FAN_SUPPLIER_RESPONSE_R00.csv). Screening only; actual room/filter/OEM installation inputs remain required. Not sent or order-ready.

Electrical development: [core operating sequence](CORE_CONTROL_SEQUENCE.md), [functional schematic](CORE_ELECTRICAL_FUNCTIONS.svg) and [interface register](CORE_ELECTRICAL_INTERFACES.csv). Preliminary requirements and fifteen unexecuted witness cases; exact fan, supply and rated wiring still open.

Current execution basis: [build without a college lab](NO_LAB_BUILD_ROUTE.md), [funded work packages](FUNDED_WORK_PACKAGES.csv) and [optional ENTC review handout](OPTIONAL_ENTC_REVIEW.md). Buy/rent equipment and hire scoped physical services; no dependency on a college lab or the optional friend. Core-first/cladding-later is a recommendation, not an architecture release.

Equipment preparation: [buy/rent indoor instrument kit](INDOOR_INSTRUMENT_KIT.md) and [revised request sheet](INDOOR_INSTRUMENT_REQUEST_NO_LAB.csv). Official sensor/flow-instrument references checked; addresses, measurement ranges and conceptual pressure-tap mapping documented. Actual devices/calibration/interfaces still UNKNOWN; no order or wiring release. Previous college-based CSV is superseded.

Analysis preparation: [single-pair indoor particle-decay tool](INDOOR_DECAY_ANALYSIS.md). Works with recorded CSV and explicit windows/assumptions; synthetic tests only. No confidence interval or physical performance result; requires reviewer assessment and repeated trials before interpretation.

Monitoring preparation: [offline measurement recorder and first-trial data format](MEASUREMENT_RECORDING.md), metadata template and eight synthetic tests. It does not connect sensors or control the fan; no data collected. This independent software task proceeds while closure/component data and engineering review remain outstanding.

Action package: [HEPA closure review request and acceptance sequence](M05_CLOSURE_REVIEW_PACKAGE.md), with [supplier/reviewer response sheet](M05_SUPPLIER_RESPONSE.csv). Prepared, not sent. Obtain component-specific closing-force/gasket data and mechanical review before a new closure CAD branch; keep other build gates separate.

Newest evidence: [OEM hatch hardware and gasket check](M05_HARDWARE_GASKET_REVIEW.md). Real cutouts exceed the assumed rim; gasket compression force cannot be inferred from door pressure. No replacement latch or seal selected. Review closure/catch and gasket data before another fabrication-detail branch.

Newest service detail: [M05 removable HEPA hatch](M05_HEPA_SERVICE_HATCH.md), [visual layout](M05_HEPA_SERVICE_HATCH.html) and separate CAD. Widened-opening/casing examples are now a new fit branch, not approved dimensions. Flange/gasket/cover geometry and generic hardware locations added; real mechanisms, drop retention, compression and stiffness remain unknown.

Latest decision sheet: [weight and service-access sensitivities](M03_WEIGHT_SERVICE_DECISION.md). Outer casing dominates modeled weight; casing-only aluminium scenario saves 61.76 kg in a density calculation. Current 1 mm service gap is not robust to assumed allowances; door/seal hardware needs a real envelope. No material/dimension release or CAD revision is implied.

Newest fit option: [continuous frame around independent inner filter housing](M03_INDEPENDENT_HOUSING.md); 36 valid solids, zero nominal clashes, tight service margins recorded, weight not optimized. For the overall task rather than just CAD, use [six remaining build gates](BUILD_REMAINING.md). We are not yet fabrication-ready.

Latest calculation: [plate load-transfer and connection review](M02_PLATE_LOAD_REVIEW.md). Read-only partial material loads, equal-stiffness reaction sensitivities and six tests; no actual plate-strength approval. Segmented posts remain an unselected option. Next compare continuous supports around a separately sealed inner filter housing; avoid treating the appearance casing as the only possible pressure boundary.

Latest interface branch: [segmented capped posts at intact filter plates](M02_M03_SEGMENTED_INTERFACE.md), with [visual explanation](M02_M03_SEGMENTED_INTERFACE.html) and combined fit CAD. Zero checked nominal clashes; plates now lie in the support load path and require review. No structural or leakage approval; earlier continuous-frame findings remain historical evidence.

Newest fit check: [M02 frame routing and interface register](M02_FRAME_INTERFACES.md), [visual layout](M02_FRAME_LAYOUT.html) and separate FreeCAD/STEP. Eight unresolved post/plate clashes are explicitly recorded; no bulkhead holes cut or structural sections selected. Fan mounting, sealed support boundary and actual base still require design/review.

Latest mechanical finding: [M02 weight, support and stability screening](M02_WEIGHT_STABILITY.md). Partial CAD material inventory is 135.6 kg in the assumed steel scenario, not total tower weight. Actual component masses, frame/base, CG and support polygon are missing; compare lighter casing options with independent supports before fabrication. No structural PASS is claimed.

Latest physical detail: [M04 hollow transition/outlet study and pressure-basis check](AIRPATH_AND_PRESSURE_BASIS.md). Separate CAD generated; component loss coefficients remain assumptions. Short inlet/outlet lengths need OEM acceptance; no new performance claim or fabrication release.

Latest calculation step: [Fan-duty comparison and R02 candidate envelope branch](FAN_DUTY_DECISION.md). New OEM-backed comparison candidate improves modeled flow but does not satisfy every assumed loaded scenario; it is NOT selected. R02 height increase is an option study, not final dimensions.

Latest: [R01 cassette/intake development](CASSETTE_INTAKE_R01.md) adds eight intake apertures, illustrative gasket/seat/retainer interfaces and a lifted service sweep. [Supplier release questions](SUPPLIER_RELEASE_QUESTIONS.md) identify exact missing fan/filter data. R01 remains preliminary and unguarded; no OEM fan substitution or fabrication release.

Next step delivered: [Preliminary parametric 3D packaging CAD R00](PACKAGING_CAD_R00.md), native FreeCAD/STEP files and executed fit checks. Fan is still generic; intake/guards, seals and structure remain incomplete. This is not the former GEO_C air volume or a fabrication release.

New: [Visual schematic pack R00](SCHEMATICS.html) and [schematic register/packaging assumptions](SCHEMATIC_REGISTER.md). Includes tower section, pressure-tap airflow schematic and electrical/control functions; not released construction drawings.

User additionally requests a Dyson HushJet-inspired cylindrical option and government-project research. See [Cylindrical options and researched component families](CYLINDRICAL_OPTIONS.md). Rectangular GEO_C is no longer assumed to be the final physical shape; compare packaging alternatives before freezing CAD.

1. [Mechanical and filter plan](MECHANICAL_FILTER_PLAN.md): arrangement, seals, manufacturing and drawing checklist.
2. [Electrical and monitoring plan](ELECTRICAL_PLAN.md): safe system architecture and missing ratings.
3. [Preliminary tower BOM](TOWER_BOM.csv): candidate purchases; not order-ready.
4. [Build and test sequence](BUILD_AND_TEST.md): go/no-go checks and outdoor progression.
5. [Stakeholder brief](STAKEHOLDER_BRIEF.md): plain-language support request.
6. [Sources and tools](SOURCES_AND_TOOLS.md): official references and tooling choices.

## Immediate release blockers

Before cutting sheet metal: approve intended room/site, required measured airflow, noise target, exact fan/filter dimensional drawings, loaded pressure budget, enclosure mass/stability, and mechanical assembly drawings. Before energizing: approve protection, wiring, earthing, guarding and commissioning tests. A reasonable budget is not a substitute for these decisions.

No purchases, installation, new CFD, final CAD or electrical certification are implied by this planning package.
