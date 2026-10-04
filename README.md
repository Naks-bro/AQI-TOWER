# AQI Tower

## Latest engineering deliverable — D01 indoor demonstrator

**Guard bending continuation:** [calculation and engineering limits](reports/prototype_d01/mechanical_package/GUARD_ACCESS_DECISION.md), with36 assumed solid-strip scenarios and28 arithmetic checks. Actual perforations/supports prevent these from being treated as guard approval. Quantified thickness/span and mass trade-offs; no new CAD branch or unverified material release.

**Current update (4 October):** ARCTIC and Noctua technical enquiries are sent; Noctua ticket **220175**. See [enquiry record](docs/build/OEM_CABLE_ENQUIRIES.md); no technical replies or parts ordered. [Airflow analyzer](scripts/analysis/d01_validation.py) now requires independent measurement-plane area, valid timezones and consistent calibration, and records the source CSV hash. **23 synthetic/arithmetic checks pass**, no physical test. Use the repository script; the V00 PDF/ZIP's older analyzer is superseded. See [usage and limitations](reports/prototype_d01/validation_package/README.md).

**Current harness blocker:** exact cable/connector dimensions are not established by the reviewed current OEM drawings. [Evidence](reports/prototype_d01/mechanical_package/harness_detail/README.md). Guard stays uncut; authorized OEM enquiries have now been submitted and replies are pending. This does not resolve the separate electrical, guard-strength or performance gates.

**Harness route study (4 October): [integrated routing CAD and findings](reports/prototype_d01/mechanical_package/harness_detail/README.md).** Four assumed3 mm internal routes clear the493-object R03M assembly and each other;497-object study reopened valid. Provisional long leads448/456 mm exceed listed400 mm, so300 mm extensions are candidates. Actual fan lead emergence, connector section, split-entry insert and restraints remain unknown; guard remains uncut. This is partial interface progress, NOT a completed harness or protected entry.

**Guard/access audit (4 October): [hazard-to-protection decision](reports/prototype_d01/mechanical_package/GUARD_ACCESS_DECISION.md).** Read-only native CAD confirms22/50 mm upper/lower face-to-fan-body separations (NOT safety distances). Cable reservation is tangent outside the guard, not a crossing: actual fan harness/feed-through is missing. Fixed independent guards plus isolated servicing proposed for review; no existing restart requirement waived. Guard strength/reach and physical isolation remain unresolved; source CAD unchanged.

**Protective-control selection screen (4 October): [three real relay candidates and decision](reports/prototype_d01/electrical_package/PROTECTIVE_SELECTION_DECISION.md).** Eight reproducible checks cover supply loading, enclosure orientation and two restart counterexamples. No drop-in selected: X9P leaves only0.2 W before auxiliaries; X5 monitored restart not established; s4 requires24 V and additional design. A hazard-to-protection review must justify the restart architecture rather than accumulating unselected relays. Existing restart requirements remain in force; no build release.

**Package 3 validation V00 (4 October): [validation package](reports/prototype_d01/validation_package/README.md).** Five-page procedure, three blank measurement CSV sheets, strict airflow arithmetic tool and R03M pressure screen. Actual proposed guard open area reduces the conditional K1 filter allowance to **14.32 Pa per filter at assumed 300 m3/h total**, superseding the older 14.61 Pa value for R03M. Fifteen synthetic/arithmetic checks pass; all physical runs remain NOT EXECUTED. Mechanical, electrical and validation review packages now exist; this is not construction approval. Remaining work is rated protective/structural/interface closure, qualified review and physical evidence—not more presentation branches.

**Package 2 electrical review E00 (4 October): [one electrical package](reports/prototype_d01/electrical_package/README.md).** Seven-page power-reference schematic, verified OEM ratings/manual links, nominal/startup sensitivity, interface/BOM schedules and enclosure integration constraints. Four fans total 1.4 A nominal against a 2 A supply; startup and auxiliary current remain unverified. Fourteen abstract sequence checks and 1,024 one-step cases pass; these are NOT hardware safety tests. Rated protective stop/restart implementation, cable/guard-entry details and commissioning remain OPEN. Mechanical R03M CAD unchanged; no wiring/energization release.

**Package1 mechanical batch: [R03M mechanical package](reports/prototype_d01/mechanical_package/README.md).** Integrated/exploded CAD, complete proposed cabinet/fan/M5 stacks, shorter rods, positive foot fixings, seal stops and joined guard fabrication route.493 valid objects;119,805 pair checks clear excluding reservations only; filter sweeps and native/STEP checks pass. Matching panel and guard drawings, inventory, assembly sequence and load/seal sensitivities are included. Material/weld strength, actual seal fit and physical guarding/stability holds remain; NOT a construction release. Control enclosure/glands stay a package2 interface.

**READ FIRST: [One current review handoff](reports/prototype_d01/current_handoff/README.md).**15-page consolidated PDF, current integrated CAD bundle,10 flat-panel drawings/DXFs extracted from that CAD,245-object inventory, missing-item register and current-geometry pressure allowance. Whole-assembly audit:29,116 checked pairs clear,774 excluded;8 pressure checks pass. Three closure packages remain mechanical/electrical/performance. NOT construction-ready; no more interpretation of delta-only PDFs is required for the current review. Earlier links below are historical detail evidence.

**Current assembly: [R02G independent guard mountings](reports/prototype_d01/r02_guards/README.md).**245 valid CAD objects; upper and lower guards now have separate four-bolt attachments.8,641 changed-part pair checks and16 assumed tool-envelope checks clear; native/STEP checks pass. Two-sheet drawing and delta BOM included. Guard seams/rivets, strength, access/isolation and remaining construction gates are not released.

**Current detail revision: [R02H fastening and filter service](reports/prototype_d01/r02_adapter/hardware_detail/README.md).** Same assembly,229 valid CAD objects; full proposed adapter nut/washer stacks and ledge bolt heads.13,644 changed-part pair checks and both200 mm nominal filter withdrawal sweeps clear; native/STEP checks pass. Drawing sheet and hardware delta BOM included. No strength, tool-access, sealing or safety release; previous CAD preserved.

**Latest CAD: [R02 removable experimental filter adapter](reports/prototype_d01/r02_adapter/README.md).** Integrated169-object assembly, two dimensioned sheets, STEP, two review DXFs and delta BOM.5,310 new-part pair checks and native/STEP checks pass. Retains the R01 cabinet, but changes filter modules; old airflow predictions do not transfer. OEM STARKVIND-only intended use, custom seal/structure and electrical release remain unresolved. No physical build or purchase.

**Internet-only continuation:** [online filter options and dimensioned comparison](reports/prototype_d01/component_validation/D01_ONLINE_FILTER_OPTIONS.pdf) checks official IKEA/Smart Air India alternatives and expensive Filtrete import listings. User is not being asked to contact suppliers. No drop-in selection or performance approval yet. Corrected an inquiry-document error: actual CAD gasket495.3/475.3mm, not490/470mm. Five fit-screen arithmetic checks pass; original CAD preserved.

Filter closure: [ready-to-send technical inquiry](reports/prototype_d01/component_validation/FILTER_INQUIRY_UNSENT.md) now includes exact interface dimensions and per-filter duty points. Added a returned-curve checker with ten passing synthetic tests, no extrapolation and no automatic purchase approval. Public catalogues have not established a pressure-qualified, obtainable drop-in filter; supplier response is needed. Inquiry NOT SENT.

Deployment decision: [India heat, public-use robustness and size](docs/build/INDIA_DEPLOYMENT_BASIS.md). D01 remains a supervised indoor prototype proposal, not an outdoor/public unit. Verified fan ceiling40 C; added weather-guard loss and cylinder-size sensitivities pass five arithmetic checks. Outdoor protection/anchors/materials remain unselected; do not simply wrap D01 in a metal cylinder.

Latest evidence check: [OEM fan comparison and filter pressure allowance](reports/prototype_d01/component_validation/README.md), with a two-page PDF and nine passing calculation checks. Numeric OEM data predict 371/344/299 m3/h under the same assumed filter cases; historical R01 predicts 359/337/298. Manufacturer source discrepancies remain explicit. At 300 total, roughly14.5 Pa remains per filter;400 total is unsupported under current loss assumptions. These are calculations, not measured performance or purchase approval. R01 CAD remains current.

Latest continuation: [R01 construction drawings and revised assembly](reports/prototype_d01/r01/README.md) adds guard brackets, cabinet joints, filter-ledge supports and cable routing. **Still review-only**, with updated pressure screening; do not combine R00 drilling files with R01.

3 October 2026: [Open the integrated CAD/drawing/BOM/test package](reports/prototype_d01/README.md) or [read the 11-page engineering PDF](reports/prototype_d01/AQI_D01_ENGINEERING_PACKAGE.pdf). This is a proposed custom 12 V, four-fan, two-MERV13-filter demonstrator before the larger cylindrical tower. Native assembly/exploded CAD, STEP, panel DXFs and reproducible pressure calculations are supplied. It is **not HEPA, not a physical prototype and not released for fabrication or energizing**. Exact obtainable components, guard/joint details, seals and restart protection remain open. Historical full-size plans below remain evidence, not released construction instructions.

> Working project name. The final device/project name has not yet been selected.

AQI Tower is an evidence-first engineering project exploring a tower-shaped air-cleaning system. The aim is to study the idea with requirements, CAD, airflow simulation, filter data, and controlled physical tests before making product-performance claims.

This repository is the shared source of truth for the project. It contains the decisions, models, simulation setup, scripts, curated results, reports, and onboarding guidance needed to continue the work responsibly.

## Start here

If you are new to the project, follow this order:

1. Read this README.
2. Read [Project Overview](docs/PROJECT_OVERVIEW.md).
3. Read the current status in [Project Status](memory/project_status.md).
4. Review the engineering requirements in [Requirements](requirements/REQUIREMENTS.md) and [Requirements Matrix](requirements/REQUIREMENTS_MATRIX.md).
5. Open only the folder related to your task using the repository map below.
6. Before changing anything, read the latest document for that phase and check its stated assumptions and unknowns.

## Paper and team handbook

- [AQI Tower System Map](docs/paper/AQI_TOWER_SYSTEM_MAP.html): project specifications, the four software layers (geometry, simulation, visualization, data and decisions) with their files, dependencies and tech stack. Open it in a browser.
- [Conference paper draft](docs/paper/AQI_Tower_IEEE_Paper.docx) ([PDF](docs/paper/AQI_Tower_IEEE_Paper.pdf)): IEEE A4 format. Author names, college and funding body are still placeholders.
- [Reference material](docs/paper/REFERENCES.md): the paper's citations with DOIs, the source documents archived in this repository, and the main external sources used in the engineering documents.

## Current status

Ready to present: [six-page prototype stakeholder PDF](reports/prototype_delivery/AQI_TOWER_PROTOTYPE_STAKEHOLDER_BRIEF.pdf) and [offline clickable explainer](reports/prototype_delivery/PROTOTYPE_DEMO.html). Includes project evidence, original diagrams, public construction references and an optional clearly labelled reference-appliance demo route. Six PDF pages visually checked; browser interaction/mobile checks passed. These are presentation deliverables, not physical hardware or new performance evidence.

Build-start priority: [three pre-construction gates and conditional time allowance](docs/build/BUILD_REMAINING.md). Focus on actual component replies, premises and qualified workshop/review quotes rather than more generic CAD branches. A 4–8-week coordination allowance starts only after usable OEM inputs and service/parts availability; it is not a booked delivery estimate and excludes unknown delays/outdoor work.

Latest fan step: [supplier selection brief R00](docs/build/FAN_SELECTION_BRIEF_R00.md) and [response sheet](docs/build/FAN_SUPPLIER_RESPONSE_R00.csv). Recomputed three-flow clean/loaded scenarios; neither current fan is confirmed adequate at the provisional loaded duty. Request prepared, not sent; no fan selected or ordered.

Latest electrical step: [core start/stop and fault plan](docs/build/CORE_CONTROL_SEQUENCE.md), [functional schematic](docs/build/CORE_ELECTRICAL_FUNCTIONS.svg) and eleven-interface register. No automatic restart proposed; laptop monitoring remains outside protection. Fifteen commissioning cases prepared, none executed. Not a rated wiring design or permission to energize.

Current build route: [no college lab required](docs/build/NO_LAB_BUILD_ROUTE.md). College/NGO provide funding only; buy/rent instruments and hire scoped fabrication/testing services. The assistant still prepares the digital design; [ENTC review](docs/build/OPTIONAL_ENTC_REVIEW.md) is optional/unconfirmed, not a delivery dependency. Pune/Hyderabad/Mumbai are possible locations. Use [funded work packages](docs/build/FUNDED_WORK_PACKAGES.csv) for itemized quotes, not assumed prices.

Latest equipment step: [indoor instrument kit and placement plan](docs/build/INDOOR_INSTRUMENT_KIT.md), [revised no-lab equipment request sheet](docs/build/INDOOR_INSTRUMENT_REQUEST_NO_LAB.csv) and updated monitoring BOM. Earlier college-based CSV is superseded. No equipment obtained or physical data collected; exact kits and acquisition routes remain unselected.

Newest analysis software: [exploratory indoor off/on decay comparison](docs/build/INDOOR_DECAY_ANALYSIS.md), explicit-window plan template and eight synthetic tests. Withholds a conditional estimate without declared assumptions; rejects mixed evidence and outdoor use. No physical data, uncertainty/certified rating or release implied.

Newest software: [indoor measurement recorder](docs/build/MEASUREMENT_RECORDING.md) imports instrument/manual readings into traceable CSV with explicit physical/synthetic labels. Eight synthetic unit tests; no live sensor connection, fan control, physical readings or performance claims. No new dependencies.

Build planning updated 3 October 2026: [HEPA closure supplier/workshop review package](docs/build/M05_CLOSURE_REVIEW_PACKAGE.md) includes a copyable request, option comparison, load/tolerance worksheet and [response sheet](docs/build/M05_SUPPLIER_RESPONSE.csv). No request sent, hardware selected or drawings released; supplier data and mechanical review are now the next hatch-design input.

Latest closure check: [real latch drawings and gasket-force screening](docs/build/M05_HARDWARE_GASKET_REVIEW.md). Reviewed hardware cannot replace M05's small location blocks unchanged; reference gasket force illustrates why door pressure alone cannot size latches. Six new arithmetic tests; no hardware selected or CAD/fabrication release.

For a plain-language answer to what is still left, read [How much remains? Six build gates](docs/build/BUILD_REMAINING.md). We are in design development, not fabrication-ready; OEM data, mechanical/electrical reviews and physical validation remain essential.

**Engineering/build planning updated:** 3 October 2026

The current priority is transition to a physical prototype. Start with the [Build planning package](docs/build/START_HERE.md): mechanical/filter planning, electrical architecture, preliminary tower BOM, reproducible screening calculations and test gates. These documents are **not released fabrication or wiring drawings**.

User direction: first test indoors; final goal fully outdoors. Earlier small-device testing was clarified as digital-only. A particulate-only first build is recommended so optional gas research does not block core validation. Budget is to remain reasonable; the exact ceiling, deadline, site and performance targets are not fixed.

Also compare [cylindrical/HushJet-inspired options](docs/build/CYLINDRICAL_OPTIONS.md), including verified government-trial lessons and OEM component families. No final shape or exact new component SKU has been selected.

[Visual schematics R00](docs/build/SCHEMATICS.html) show a round-shell/panel-filter packaging study, airflow instrumentation and electrical/control functions. Read the [drawing register](docs/build/SCHEMATIC_REGISTER.md) for assumptions and release gaps. These are not final CAD or wire-by-wire schematics.

[Parametric packaging CAD R00](docs/build/PACKAGING_CAD_R00.md) now provides a new native FreeCAD/STEP fit study with filter envelopes, assumed service openings, bulkheads and clearly labeled fan/electrical/base allowances. Executed checks cover geometry validity, nominal overlaps, assumed HEPA removal path and parameter propagation—not structure, sealing, real fan fit or airflow performance.

Latest fit revision: [R01 cassette/intake study](docs/build/CASSETTE_INTAKE_R01.md), with intake apertures and illustrative HEPA seat/gasket/retainer. [Draft supplier questions](docs/build/SUPPLIER_RELEASE_QUESTIONS.md) define missing OEM data; none sent. Guards, rated supports, exact fan and seal/clamp approval remain unresolved.

Latest duty study: [Fan comparison and R02 candidate packaging](docs/build/FAN_DUTY_DECISION.md) compares the historical KVO curve with visually digitized official S&P TD-2000/315 SILENT ECOWATT data. Stronger candidate is not a purchase selection; restrictive loaded scenario still falls below the illustrative 1,200 m3/h goal. R02 accommodates its drawing-based bounding envelope, not detailed OEM CAD.

Latest air-path detail: [M04 transition/outlet geometry and pressure accounting](docs/build/AIRPATH_AND_PRESSURE_BASIS.md), with separate hollow CAD parts and five-test loss sensitivity script. Static/total pressure, exit energy and installed fan effects must be reconciled; previous fan comparisons remain unvalidated scenarios. Room dimensions and outdoor pilot setting requested from team.

Latest mechanical check: [M02 weight/support/stability screening](docs/build/M02_WEIGHT_STABILITY.md). Read-only CAD-volume inventory gives about 135.6 kg for an all-steel scenario versus 46.6 kg for aluminium on the same study geometry, before fan, filters, frame/base and electrics. Neither material is approved; complete weight/CG and structural/stability release remain UNKNOWN. Compare independently supported frame/lightweight casing options before buying sheet metal.

New [M02 frame-routing CAD and mounting interfaces](docs/build/M02_FRAME_INTERFACES.md), with [visual layout](docs/build/M02_FRAME_LAYOUT.html): twenty valid assumed tube routes clear checked component envelopes and the assumed HEPA service sweep, but intersect both existing filter plates at eight locations. Pressure-boundary and hollow-post bypass paths must be resolved. Base/feet and structural sizing remain unknown; not an integrated assembly or fabrication release.

Latest branch: [M02/M03 segmented closed-post interface](docs/build/M02_M03_SEGMENTED_INTERFACE.md) and [illustration](docs/build/M02_M03_SEGMENTED_INTERFACE.html). Twenty-eight route solids and a combined 41-solid fit snapshot remove the eight nominal clashes without perforating the plates. Sixteen cap/plate contacts verified; real joints, structural load transfer and airtightness remain unapproved. Earlier CAD preserved; this is an option study, not a complete build assembly.

Latest load review: [plate loads and connection decision](docs/build/M02_PLATE_LOAD_REVIEW.md). Partial modeled material plus the unselected fan gives 49.33 kg above the HEPA plane, not an actual support load or total weight. Eccentric/lateral examples demonstrate why resting contact is insufficient as a connection design. Do not freeze segmented posts; compare a continuous frame surrounding a separately sealed inner cassette. No structural PASS or plate sizing claimed.

Latest fit candidate: [independent inner filter housing with continuous surrounding frame](docs/build/M03_INDEPENDENT_HOUSING.md). Thirty-six valid solids and zero nominal clashes; three assumed service sweeps clear. Side gap 6 mm and retainer opening margin 1 mm per side are NOT manufacturing-approved. All-steel partial material sum 191.27 kg excludes actual fan/filters/base/hardware; no weight optimization, assembly-seal proof or architecture freeze yet.

Latest decision check: [weight and service-access comparison](docs/build/M03_WEIGHT_SERVICE_DECISION.md). Changing cosmetic-casing density only to assumed aluminium gives a 129.52 kg partial material scenario, not approved or complete weight. Hypothetical tolerance allowances eliminate the existing 1 mm service gap; wider opening/door hardware may require a larger casing. Example dimensions are NOT changes to the CAD or manufacturing specifications.

Newest separate branch: [M05 removable HEPA hatch](docs/build/M05_HEPA_SERVICE_HATCH.md) and [layout illustration](docs/build/M05_HEPA_SERVICE_HATCH.html). Models a flange, gasket space, cover and generic latch/handle locations with assumed 980 mm casing, 700 mm outer access and 645 mm inner opening. Forty-eight valid solids, no modeled clashes and assumed cover/filter service paths clear. Actual mechanisms, compression, panel retention and strength remain unresolved; earlier CAD untouched.

- Phase 19 is complete: a G4 washable pre-filter is the current recommended pre-filter, pending supplier RFQ data.
- The water-spray stage was evaluated and rejected. It is not part of the current treatment path.
- The best current digital airflow geometry is `GEO_C`; it is not a final product design.
- The sealed HEPA simulation case predicts about 1,332 m3/h airflow, but the CFD is not physical proof.
- The pressure-drop experiment is blocked because the required hardware has not been procured.
- Gas-phase CFD is blocked until measured carbon pressure-drop and adsorption data exist.
- No complete physical AQI Tower prototype has been built or validated.
- The official device/project name is still to be selected. **AQI Tower is the working name.**

For the complete status, decisions, blockers, and next authorized work, read [memory/project_status.md](memory/project_status.md).

Historical phase conclusions remain below; build-stage qualifications in the new package take precedence for procurement and physical release. In particular, old CAD filter placeholders do not fit the actual HEPA depth, and the claimed carbon pressure margin is not established at 1,300 m3/h.

## Current system concept

The current proposed air path is:

```text
Polluted air
    -> G4 washable pre-filter
    -> activated-carbon research stage
    -> H13 HEPA filter candidate
    -> clean-air riser
    -> KVO 250 fan
    -> outlet
```

This sequence is a research direction, not a final product specification. Sensors, energy integration, outdoor coverage, and a multi-tower “bubble” network remain future work.

## Important evidence rule

Always distinguish these clearly:

- **FACT / DETECTED:** directly observed or verified.
- **SIMULATION RESULT:** produced by a documented model; not physical proof.
- **RECOMMENDATION:** a proposed next action or candidate choice.
- **UNKNOWN / NOT MEASURED:** information that still requires evidence.

Do not claim a clean-air radius, coverage area, CADR, particle-removal percentage, gas-removal percentage, or filter life unless it has been measured using an approved method.

## Repository map

| Folder | What it contains | Use it for |
| --- | --- | --- |
| `docs/` | Phase reports, engineering decisions, methods, specifications, and environment records | Understanding why decisions were made |
| `requirements/` | Requirements, assumptions, and the requirements matrix | Checking what the design must achieve |
| `cad/parametric/` | FreeCAD models and model metadata | Editing or reviewing the tower geometry |
| `cfd/` | Reproducible OpenFOAM case inputs | Preparing or rerunning approved airflow studies |
| `scripts/geometry/` | FreeCAD/Python geometry scripts | Rebuilding or checking parametric geometry |
| `scripts/simulation/` | CFD preparation, execution, analysis, and visualization scripts | Reproducing approved simulations |
| `scripts/analysis/` | Physical-test data analysis scripts | Processing measured experiment data |
| `data/` | Structured fan, filter, and material evidence | Keeping source data separate from assumptions |
| `results/` | Curated result files, figures, tables, and result summaries | Reviewing findings without keeping every raw solver file |
| `reports/` | Stakeholder reports and report-generation material | Communicating progress to non-technical audiences |
| `output/` | Current exported deliverables | Sharing finished reports |
| `threejs/` | Interactive Three.js engineering viewer | Viewing the concept and selected result summaries in a browser |
| `memory/` | Concise continuation status | Quickly understanding the latest project state |

Generated CFD time steps, meshes, logs, temporary files, videos, build outputs, and `node_modules` are intentionally excluded from Git. They can be recreated from the tracked source files and scripts.

## Tools and what each one is for

| Tool | Purpose in this project | Current reference environment |
| --- | --- | --- |
| Git and GitHub | Version control, collaboration, review, and project history | Git on Windows; GitHub repository |
| FreeCAD | Parametric tower geometry and CAD review | FreeCAD 1.1.3 |
| OpenFOAM | Airflow and pressure-loss simulation | OpenFOAM Foundation 14 in Ubuntu/WSL 2 |
| ParaView | CFD field inspection and engineering figures | ParaView 5.11.2 in Ubuntu/WSL 2 |
| Python | Geometry automation, data processing, analysis, and figures | Python 3.13.1 on Windows; 3.12.3 in Ubuntu |
| Node.js and npm | Three.js viewer development | Node.js v24.19.0 and npm 11.9.0 on Windows |
| Three.js and Vite | Browser-based engineering visualization | Defined in `threejs/package.json` |

The full machine and software record is in [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md).

## Basic setup

### 1. Clone the repository

```bash
git clone https://github.com/Naks-bro/AQI-TOWER.git
cd AQI-TOWER
```

### 2. Documentation-only work

Markdown files can be edited in any text editor. Use clear language, keep assumptions visible, and link every technical claim to its detailed source file.

### 3. Three.js viewer

```bash
cd threejs
npm install
npm run dev
```

Do not commit `node_modules/` or `dist/`.

### 4. CAD work

Open the relevant `.FCStd` file in `cad/parametric/` with FreeCAD. Preserve the existing versions; create a clearly named new version for an approved design change.

### 5. CFD work

CFD is run in Ubuntu/WSL using OpenFOAM 14. Source the OpenFOAM environment before running an approved script:

```bash
source /opt/openfoam14/etc/bashrc
```

Use the scripts in `scripts/simulation/` and the corresponding phase document. Do not run a new CFD case simply because a case folder exists. Generated time directories, meshes, logs, and post-processing outputs should remain local; publish only curated results in `results/`.

### 6. Physical-test analysis

The Phase 17A analysis entry point is `scripts/analysis/phase17a_analysis.py`. It must use measured data only. Never add invented rows to the raw-data templates.

## How to contribute

1. Pull the latest `main` branch.
2. Create a short branch for one clear task.
3. Make the smallest complete change.
4. Run the relevant check, script, build, or visual review.
5. Update the detailed phase document and curated results when applicable.
6. Update this README if the current status, tools, repository map, key decisions, blockers, or next step changed.
7. Add a short entry to [CHANGELOG.md](CHANGELOG.md).
8. Commit with a clear message and open a pull request.

Example branch names:

```text
docs/update-onboarding
cad/prefilter-cassette
cfd/new-approved-case
analysis/pressure-drop-results
```

## README update rule

The README is a current entry point, not a full lab notebook. Update it whenever one of these changes:

| Change | README action |
| --- | --- |
| A phase starts or finishes | Update **Current status** and link the detailed phase document |
| A major decision changes | Update **Current system concept** or the relevant status bullet |
| A blocker is resolved or created | Update **Current status** |
| A tool or required version changes | Update **Tools** and `docs/ENVIRONMENT.md` |
| A folder or primary workflow changes | Update **Repository map** or **Basic setup** |
| A measured result replaces an estimate | Clearly change the evidence label and link the result record |
| Only small internal details changed | Update the detailed document and `CHANGELOG.md`; the README may remain unchanged |

Every pull request must either update the README or explicitly state why the README is not affected.

## Safety and honesty boundaries

- Do not perform formaldehyde testing outside a qualified, exhausted, institutionally approved laboratory.
- Do not purchase parts or freeze a final design without the required review and authorization.
- Do not overwrite previous simulation or experimental evidence.
- Do not present CFD, CAD, supplier claims, or theoretical calculations as physical product performance.
- Do not commit credentials, private supplier correspondence, personal data, or machine-generated bulk files.

## Key documents

- [Project status](memory/project_status.md)
- [Project overview](docs/PROJECT_OVERVIEW.md)
- [Environment](docs/ENVIRONMENT.md)
- [Requirements](requirements/REQUIREMENTS.md)
- [Concept design](docs/CONCEPT_DESIGN.md)
- [Geometry optimization](docs/GEOMETRY_OPTIMIZATION.md)
- [HEPA bypass fix](docs/FILTER_BYPASS_FIX.md)
- [Particle CFD record](docs/PARTICLE_CFD_V12B.md)
- [Formaldehyde target](docs/PHASE14_FORMALDEHYDE_TARGET.md)
- [Pre-filter specification](docs/PHASE19_PREFILTER_SPECIFICATION.md)
- [Detailed historical README](docs/PROJECT_HISTORY.md)

## Immediate next steps

1. Select the official project/device name.
2. Send the pre-filter and carbon-media RFQs.
3. Obtain expert review of the current CAD, fan, filters, seals, and test plan.
4. Procure or borrow the approved clean-air pressure-drop test equipment.
5. Perform controlled component tests before any final product claim or gas-phase CFD.
