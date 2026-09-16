# AQI Tower

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

## Current status

**Engineering status last updated:** 7 September 2026  
**Repository onboarding updated:** 16 September 2026

- Phase 19 is complete: a G4 washable pre-filter is the current recommended pre-filter, pending supplier RFQ data.
- The water-spray stage was evaluated and rejected. It is not part of the current treatment path.
- The best current digital airflow geometry is `GEO_C`; it is not a final product design.
- The sealed HEPA simulation case predicts about 1,332 m3/h airflow, but the CFD is not physical proof.
- The pressure-drop experiment is blocked because the required hardware has not been procured.
- Gas-phase CFD is blocked until measured carbon pressure-drop and adsorption data exist.
- No complete physical AQI Tower prototype has been built or validated.
- The official device/project name is still to be selected. **AQI Tower is the working name.**

For the complete status, decisions, blockers, and next authorized work, read [memory/project_status.md](memory/project_status.md).

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

