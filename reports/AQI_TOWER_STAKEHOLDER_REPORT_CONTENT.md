# AQI Tower — Stakeholder Report: Full Content

*Text version of all report content. For claim traceability see AQI_TOWER_STAKEHOLDER_REPORT_SOURCES.md.*

---

## Page 1 — Cover

**AQI TOWER**
A Structured Engineering Exploration

Clean air for Indian homes — a journey through simulation, validation, and the gap between them.

*2024–2026 · Phase 18 Complete · Physical prototype pending*

---

## Page 2 — Opening Statement

**What this report is**

This document records the engineering exploration behind AQI Tower: an attempt to design a high-performance indoor air-quality tower for Indian conditions.

Nothing in this report is fabricated. Nothing is presented as proven that has not been measured. Every number carries a source classification.

The project started with a question: *can a compact, high-flow, multi-stage air purifier be designed rigorously using modern simulation tools — before committing to a physical prototype?*

The honest answer is: partly. Simulation accelerated the exploration and eliminated several bad ideas early. But the gap between a convincing simulation and a validated physical device is large — and this report is honest about exactly where that gap sits.

---

## Page 3 — The Problem: Air Quality in India

India has some of the highest indoor PM2.5 exposure levels in the world. Cooking smoke, traffic penetration, and seasonal burning events create indoor concentrations that WHO guidelines class as hazardous.

**Why it matters:**

- WHO PM2.5 24-hour guideline: 15 µg/m³
- India average indoor: often 5–10× that during peak events
- Formaldehyde (HCHO): released from furniture, flooring, paints; cumulative indoor exposure risk
- Commercial air purifiers: often low airflow, high cost, or poor India-specific sizing

**Why existing solutions fall short for many households:**

High-performance purifiers are expensive. Budget units often underperform on airflow. No device designed specifically for Indian room sizes (30–60 m²), Indian pollution profiles (PM2.5 + HCHO), or Indian power constraints.

---

## Page 4 — The Original Idea

The AQI Tower concept: a tall, floor-standing unit optimised for high-volume airflow through a multi-stage filtration stack — designed to push the boundary of what a carefully-engineered, cost-conscious device can achieve.

**Filtration stages conceived:**
1. G4/M5 washable pre-filter (coarse dust, HEPA life extension)
2. Activated carbon bed (formaldehyde and VOC adsorption)
3. H13 HEPA filter (fine particles ≥99.95% at MPPS)

**Design targets:**
- High CADR (Clean Air Delivery Rate) — exact target to be validated
- KVO 250 centrifugal fan (Systemair) — shortlisted from fan-curve analysis
- Tower form factor: tall, narrow, floor-standing — maximises filter face area

---

## Page 5 — Methodology: How We Worked

The project used a phase-gated structured methodology:

1. **Concept** — requirements, architecture, form factor decisions
2. **Fan selection** — digitised manufacturer curves, identified operating envelope
3. **CFD setup** — OpenFOAM mesh, boundary conditions, solver choice
4. **Geometry optimisation** — 5 major geometry variants, 10+ CFD cases
5. **Filter integration** — HEPA pressure model, bypass discovery and fix
6. **Particle tracking** — Lagrangian DPM, 4 particle sizes, 224 seed points
7. **Gas phase scoping** — formaldehyde research target, media selection, bench-test rig design
8. **Feasibility reviews** — water spray stage review (Phase 18: NO-GO)

Every phase produced documented decisions, evidence-graded claims, and identified blockers before moving on.

---

## Page 6 — The Role of AI

AI (Claude Sonnet) was used throughout as an engineering co-pilot. It did not make engineering decisions — the team made those. It accelerated structured exploration.

**What AI did:**
- Translated engineering requirements into OpenFOAM configuration files
- Generated Python analysis and post-processing scripts
- Extracted fan-curve data from manufacturer PDFs using vector-path analysis
- Identified questions and decision branches the team had not yet considered
- Compared alternatives with structured decision matrices
- Built the interactive 3D engineering viewer (Three.js T1–T3)
- Documented every assumption, limitation, and evidence classification

**What AI did not do:**
- Run physical experiments
- Validate simulations against measurements
- Fabricate data or invent vendor information
- Override engineering judgement on safety or feasibility decisions

---

## Page 7 — The Toolchain

**OpenFOAM** — open-source CFD solver. All airflow simulations run locally. All case files in repository.

**FreeCAD** — parametric 3D CAD model. Exported to STL for meshing. GEO_C is the current best geometry.

**snappyHexMesh** — OpenFOAM mesher. Hexahedral-dominant mesh with surface refinement. All mesh files in repository.

**Python** — analysis and automation scripting. Data processing, Darcy–Forchheimer fitting, particle tracking, visualisation scripts, export pipelines.

**Three.js** — browser-based 3D visualisation. Powers the interactive engineering viewer (T1–T3) displaying geometry, particles, and CFD scalar fields in any web browser.

**Playwright** — headless Chromium. Renders this HTML report to PDF.

---

## Page 8 — CAD: Building the Tower Geometry

The physical tower geometry was modelled parametrically in FreeCAD. The model is not a final manufacturing design — it is a simulation-ready geometry that captures the key internal flow features.

**Key geometry features:**
- Inlet plenum (base) — draws air through the filter stages
- Riser duct — channels filtered air upward
- Fan housing — contains the KVO 250 centrifugal fan
- Outlet — exhausts clean air at height

The parametric model allows geometry changes (tower dimensions, riser width, outlet height) to feed directly into new CFD cases without manual re-meshing.

---

## Page 9 — Airflow: The First Lesson

The first CFD case (V00) revealed an immediate structural problem: the riser geometry created a large recirculation zone. Air was reversing direction in part of the duct, reducing effective flow and increasing pressure losses.

**V01 baseline metrics** [SIMULATION ONLY]:
- Riser reverse-flow fraction: 23.12%
- Tower total pressure loss: 17.33 Pa
- This meant significant energy was being wasted moving air backwards

This was not a failure — it was information. The simulation told us exactly where to redesign.

---

## Page 10 — Geometry Optimisation

Over several phases, five major geometry variants (V00 through GEO_C) were tested in CFD. Each addressed the weaknesses identified in the previous case.

**GEO_C — current best geometry** [SIMULATION ONLY]:

| Metric | Value | vs V01 |
|--------|-------|--------|
| Simulated airflow | 1,496 m³/h | +12% |
| Riser pressure loss | ~7 Pa | −60% |
| Reverse flow | eliminated | from 23% |

GEO_C is described as "current best" — not "final" or "validated." It is the geometry that will be physically built and tested if the project advances to prototype phase.

---

## Page 11 — GEO_C Results and Fan Integration

**Simulated operating point — GEO_C** [SIMULATION ONLY]:
- Airflow: 1,496.055 m³/h
- Fan head: 3.5 Pa (at simulated operating point)

**KVO 250 fan** [MANUFACTURER DATA]:
- Shutoff pressure: ~688 Pa ± 20 Pa (digitised from Systemair catalogue)
- Rated flow: manufacturer curve only — no independent lab validation
- Motor: EC motor, speed-controlled

The fan was selected by matching its characteristic curve against the simulated system resistance. The actual operating point will shift once a physical prototype is tested — fan curves have manufacturing tolerances, and CFD system resistance is approximate.

---

## Page 12 — The HEPA Filter

**Freudenberg H13 HEPA** [MANUFACTURER DATA]:
- Filtration efficiency: ≥99.95% at MPPS (Most Penetrating Particle Size, ~0.3 µm)
- Classification: EN 1822
- Rated ΔP: 300 Pa at 2.84 m/s face velocity (single manufacturer data point)
- Gross face area: 593 × 593 mm

**Critical gap — whole-system vs. filter-level efficiency:**
The 99.95% figure is the filter element efficiency under controlled test conditions. Whole-system PM2.5 efficiency depends on:
- Bypass seal quality (air finding paths around the filter)
- Real face velocity (different from rated test velocity)
- Filter loading state

None of these have been physically measured. The filter element efficiency cannot be directly applied to the whole system.

---

## Page 13 — HEPA Face Velocity in Context

**Simulated face velocity — CASE_M_SEALED** [SIMULATION ONLY]:
- Mean: 1.0525 m/s
- The Freudenberg 300 Pa rated point is at 2.84 m/s — 2.7× higher than the simulated velocity

**Why this matters:**
At lower face velocities, filter pressure drop decreases (favourably for airflow) but the rated efficiency test conditions no longer apply directly. EN 1822 testing is done at a specific velocity. Actual efficiency at 1.05 m/s must be independently measured.

The simulated HEPA ΔP at CASE_M_SEALED is 111.181 Pa (mean, area-weighted) — consistent with the lower face velocity. This number has not been confirmed by measurement.

---

## Page 14 — The Bypass Discovery

During simulation, a critical flaw was discovered: without deliberate bypass sealing, a large fraction of air was finding paths around the HEPA filter entirely.

**CASE_M — without bypass seal** [SIMULATION ONLY]:
- Bypass fraction: 45.05% — nearly half the air bypassed the HEPA entirely

This meant that even with a 99.95%-efficient filter element, the whole-system efficiency could be far lower. A physical device with this bypass would be near-useless for PM2.5 capture.

**Fix implemented in simulation:**
A bypass-sealing baffle ("bypassSeal") was added to the CFD model. This brought the modelled bypass fraction to effectively zero (9.997×10⁻¹⁰).

**Important caveat:** Closing bypass in simulation ≠ closing bypass in a physical housing. Real bypass seals require physical testing to verify. No physical seal has been built or measured.

---

## Page 15 — Sealed Case Results

**CASE_M_SEALED — with bypass baffle** [SIMULATION ONLY — PARTIAL NON-CONVERGED]:

| Parameter | Value | Source |
|-----------|-------|--------|
| Total airflow | 1,332.205 m³/h | bypass_analysis_sealed.json |
| HEPA ΔP (mean) | 111.181 Pa | bypass_analysis_sealed.json |
| HEPA face velocity (mean) | 1.0525 m/s | bypass_analysis_sealed.json |
| Bypass fraction | 9.997×10⁻¹⁰ | bypass_analysis_sealed.json |

The RANS solver ran for 5,000 iterations. Residuals stabilised for the quantities of interest (integrated flow, pressure drop). The simulation is classified as "PARTIAL NON-CONVERGED" because not all residuals met tight convergence criteria, though the integral quantities were stable.

---

## Page 16 — Particle Tracking

**Phase 12B — Lagrangian particle tracking** [SIMULATION ONLY]:

224 seed points were released at the inlet for four particle sizes. Results show the fraction of particles that arrived at the filter face — not the fraction captured.

| Size | Released | Arrived at filter | Arrived % | Wall deposit % |
|------|----------|-------------------|-----------|----------------|
| 0.3 µm | 224 | 139 | 62.1% | ~37.9% |
| 1 µm | 224 | 139 | 62.1% | ~37.9% |
| 2.5 µm | 224 | 139 | 62.1% | ~37.9% |
| 10 µm | 224 | 137 | 61.2% | ~38.8% |

**Why similar across sizes:** At these flow velocities, larger particles have slightly more inertial deposition on walls. The dominant factor is the flow geometry, not Stokes number.

---

## Page 17 — Filter Arrival ≠ Filter Capture

⚠️ **THIS WARNING IS MANDATORY IN ALL CONTEXTS**

The 62.1% figure means 62.1% of simulated seed particles followed streamlines that reached the filter face. It does NOT mean:

- 62.1% of real particles are captured
- The device has 62.1% CADR efficiency
- Particles not reaching the filter are captured elsewhere

**What "arrival" actually means:**
A particle-tracking trajectory ended at the filter surface. The simulation does not model:
- Actual filtration physics (Brownian motion, interception, impaction, diffusion)
- Filter loading or clogging
- Particle bounce-off, re-entrainment, or depth filtration
- Electrostatic effects

The HEPA filter (99.95% element efficiency) captures particles that reach it. The fraction that reaches it in a real physical device is unknown. CADR validation requires physical measurement.

---

## Page 18 — The Gas-Phase Challenge

PM2.5 is the first problem. Formaldehyde (HCHO) is the second.

Formaldehyde is a Group 1 carcinogen (IARC). It off-gasses from furniture, flooring, paints, and adhesives — it is a persistent indoor pollutant, invisible and odourless at typical concentrations, but dangerous at cumulative exposures.

**Why formaldehyde is hard to remove:**
- Molecular gas — not captured by HEPA filtration
- Requires chemical adsorption or catalytic destruction
- Activated carbon works but capacity is limited and humidity-dependent
- Breakthrough (saturation) must be measured experimentally

**AQI Tower gas-phase plan:**
Selected activated carbon (OVC 4×8, Calgon Carbon) as a non-impregnated research control. Formaldehyde-specific impregnated carbon (FORMASORB or equivalent) as secondary comparison. A full bench-test protocol has been designed (Phases 14–17) but no experiment has been run.

---

## Page 19 — Why Gas-Phase CFD is Blocked

Gas-phase CFD (species transport, adsorption kinetics) requires measured inputs:
- Darcy–Forchheimer coefficients for the carbon bed (measured pressure-drop testing)
- Adsorption equilibrium and kinetic parameters (measured breakthrough data)
- Real HCHO inlet concentrations from a traceable source

None of these have been measured. Building a gas-phase CFD model without measured inputs produces a result that cannot be validated even against itself. The team decided not to run gas-phase CFD until the bench test provides real data.

**This is not a failure — it is correct engineering practice.**

---

## Page 20 — The Bench-Test Experiment Design

A full bench-test protocol was designed to measure carbon-bed breakthrough under controlled conditions. Key design decisions:

**Gas source:** Certified HCHO cylinder (BOC/Linde India) + two mass-flow controllers + static mixer. No open-source generation (no formalin, no hotplate). Institutional chemical-safety approval required.

**Sensors:** Two Sensirion SDP810 differential pressure sensors (₹4,748 each, Tanotis India). Two SFA30 formaldehyde sensors (upstream + downstream, channel-swap calibration).

**Flow control:** Rotameter (₹1,950, Shree Aashapura, IndiaMART). Carbon tube column: 75 mm ID recommended.

**DAQ:** Raspberry Pi 4B + Python CSV logger, 1 s interval.

**DNPH/HPLC reference:** ISO 16000-3:2022 method. Outsourced to NABL/17025-accredited laboratory. No in-house HPLC.

**Status:** Protocol complete. Hardware not yet ordered. Institutional safety approval not yet obtained.

---

## Page 21 — Why the Project is Currently Paused

The project is paused at the boundary between simulation and physical experiment. Blockers are real and legitimate — not engineering hesitation:

1. **Institutional laboratory access** — gas-phase testing requires an exhausted, approved chemical laboratory. Not yet secured.
2. **Carbon procurement** — OVC 4×8 and FORMASORB India availability requires direct quote from Kuraray/Calgon Carbon India. No reply yet.
3. **HCHO cylinder** — BOC/Linde India certified gas cylinder. Not yet ordered.
4. **MFCs** — mass-flow controllers for gas mixing. Imported. Long lead time.
5. **Budget** — experiment cost estimate pending final BOM.

The simulation and design work is complete for this phase. The next action is physical — and that requires resources and approvals that are external to the design team.

---

## Page 22 — Water Spray: The Stage That Was Reviewed and Rejected

Phase 18 was a rigorous feasibility review of adding a water-spray pre-stage to the tower.

**Decision: NO-GO.** Scored 13/100 in a structured decision matrix (Option B, G4/M5 pre-filter: 84/100).

**Why rejected:**
- PM2.5 capture: below Greenfield scrubbing efficiency threshold — simple spray cannot capture sub-micron particles
- Hygiene risk: water recirculation in a breathing-zone device creates Legionella/biofilm risk — independently disqualifying
- Pressure drop: 35–125 Pa penalty reduces fan airflow by 7–23%
- HCHO removal: negligible (<0.1% per pass for simple water spray)
- Complexity: 12+ additional components for zero unique benefit

**Recommended replacement:** G4/M5 washable panel pre-filter at inlet. One component. ~25–50 Pa clean ΔP. No water. No hygiene risk. Wide India availability. Achieves the only defensible water-spray function (coarse dust pre-collection) better and simpler.

---

## Page 23 — The Digital Engineering Viewer

A browser-based interactive 3D viewer was built using Vite + Three.js. It displays all engineering data from the project — geometry, particles, and real CFD scalar fields — in any modern web browser. No software installation required.

**Four modes:**
- **T1 — Architecture:** Interactive 3D tower geometry. Click any component. Layer toggles. Exploded view. Status labels (ENGINEERING / SCHEMATIC / PROVISIONAL).
- **T2 — Particle Mode:** Phase 12B tracking results. Filter by size. FILTER ARRIVAL ≠ CAPTURE always visible.
- **T3 — CFD Field:** Real OpenFOAM velocity + pressure scalar planes. Turbo colourmap. SIMULATION ONLY labelled.
- **CFD Summary:** Exact JSON-sourced values (1,332 m³/h, 111 Pa). Provenance panel per case.

The viewer enforces the project's epistemic standards: every claim is labelled by source, convergence status is shown per case, and the viewer makes existing information easier to understand — it does not create new engineering truth.

---

## Page 23b — Engineering Viewer: Live Screenshots

Stills captured from the live Three.js viewer session showing CFD scalar field mode (left) and CFD Summary data panel (right). Video recordings of the full session are available in the repository (GIF/ folder).

---

## Page 24 — Project Status Dashboard

**Developed and documented:**
- Project requirements framework and architecture concepts
- Parametric FreeCAD tower model (GEO_C)
- Real fan data — KVO 250, 6-point curve, 688 Pa shutoff
- HEPA filter research — Freudenberg H13, evidence gaps identified
- Airflow CFD — 10 cases from V00 to CASE_M_SEALED
- Geometry optimisation — GEO_C: 5× pressure reduction vs V01
- Bypass discovery and fix — bypassSeal baffle in simulation
- Phase 12B particle tracking — 4 sizes, 224 seeds, arrival fractions
- Formaldehyde research target confirmed (Phase 14)
- Carbon media selection — OVC 4×8 as research control
- Bench-test rig engineering (Phases 15–17): protocol, BOM, scripts
- Water spray reviewed and rejected (Phase 18) — G4/M5 recommended
- Interactive 3D engineering viewer (Three.js T1–T3)
- Procurement research — India vendor routes, confirmed prices

**Not yet done (physical validation pending):**
- Physical prototype built or tested
- CADR measured
- PM2.5 removal efficiency measured
- Formaldehyde breakthrough experiment run
- Bypass seal physically verified
- Fan operating point physically confirmed
- Carbon bed pressure drop measured

---

## Page 25 — Eight Lessons from Eighteen Phases

1. **Simulate to eliminate, not to validate.** CFD eliminated bad geometry variants early. But no simulation replaces a physical measurement.

2. **Bypass is the hidden failure mode.** In simulation, 45% of air bypassed the HEPA without a seal. This would have been invisible in a naive prototype test.

3. **Data must be graded, not just cited.** Manufacturer data, simulation results, and measured data are not the same quality of evidence.

4. **AI accelerates structured exploration.** It does not replace engineering judgment, physical testing, or expert review.

5. **Gas-phase is a different problem.** Particle removal (CFD + HEPA) and formaldehyde removal (adsorption + breakthrough) require different methods and different experiments.

6. **Procurement is a real constraint in India.** Several critical inputs require direct vendor quotes not available online. This is a legitimate blocker, not a planning failure.

7. **The gap between simulation and hardware is large.** GEO_C is the best geometry we know — in simulation. The real device may behave differently.

8. **"Reviewed and rejected" is a result.** Phase 18 produced a documented NO-GO on water spray. This is engineering progress, not failure.

---

## Page 26 — Where Expert Review Must Enter

The following areas require domain expert review before any claim can be made to external stakeholders:

- **CFD convergence and mesh quality:** an independent CFD engineer should review residual plots, mesh metrics, and boundary condition choices
- **HEPA system efficiency:** a filter engineer should confirm what the EN 1822 element rating implies at the actual face velocity and system configuration
- **HCHO adsorption modelling:** a chemical engineer with activated carbon / VOC expertise should review the proposed experimental protocol and projected results
- **Bench-test safety:** a laboratory safety officer at the host institution must approve the HCHO gas-handling protocol before any gas is introduced
- **DNPH/HPLC validation:** the reference analytical laboratory must confirm their method meets ISO 16000-3:2022

No claim in this report should be treated as the final word on any of these topics.

---

## Page 27 — Questions a Mentor Should Ask

A technically competent external reviewer would reasonably ask:

1. Why is CASE_M_SEALED classified as "PARTIAL NON-CONVERGED"? What residuals did not converge, and by how much?
2. How sensitive is the 1,332 m³/h result to mesh resolution? Was a grid-independence study done?
3. The H13 filter is rated at 2.84 m/s; you're simulating 1.05 m/s. What does EN 1822 predict at 1.05 m/s?
4. The bypass fraction of 9.997×10⁻¹⁰ is effectively zero — is this physical or an artefact of the boundary condition?
5. OVC 4×8 is a non-impregnated control carbon. What HCHO breakthrough time do you predict, and what is the basis of that estimate?
6. How will you account for temperature and RH variation (25–30°C, 50–70% RH) in the breakthrough experiment?
7. What is the institutional chemical-safety approval process at the target laboratory, and what is the realistic timeline?

These questions are not answered yet. They define the agenda for the next phase.

---

## Page 28 — Roadmap: What Comes Next

**Immediate next steps (Phase 19 — pending approval):**

1. Send RFQs: Kuraray India + Chemet India (OVC 4×8), Caliber (FORMASORB), BOC/Linde India (HCHO cylinder)
2. Order confirmed instruments: SDP810 × 2 (Tanotis, ₹4,748 each), Rotameter (₹1,950)
3. Identify and approach NABL/17025-accredited HPLC laboratory
4. Secure institutional laboratory safety approval
5. Build Raspberry Pi DAQ rig — Python logger, test with clean air

**Phase 20 — Clean-air pressure-drop testing:**

Measure carbon-bed ΔP at target velocities. Fit Darcy–Forchheimer model. These are the inputs for gas-phase CFD.

**Phase 21 — HCHO breakthrough experiment:**

Run the protocol designed in Phases 14–17. Primary metric: t10 breakthrough time at three EBCT levels and three concentrations.

**Phase 22+ — Physical prototype:**

Only after gas-phase characterisation. Integrate all validated components. Physical CADR measurement.

---

## Page 29 — Technology Maturity Assessment

| Stage | Maturity | Evidence type |
|-------|----------|---------------|
| Tower geometry (GEO_C) | High (simulation) | CFD, parametric CAD |
| Fan selection (KVO 250) | Medium-High | Manufacturer curve + CFD match |
| HEPA filter specification | Medium | EN 1822 cert + manufacturer data |
| Bypass seal concept | Medium (simulation only) | CFD — not physically tested |
| Particle tracking | Medium (sim screening) | Lagrangian DPM — not filter capture |
| Carbon bed spec (OVC 4×8) | Low-Medium | Manufacturer data only |
| HCHO breakthrough prediction | Very Low | No measured data |
| Whole-system CADR | None | Not measured |
| Physical prototype | None | No prototype built |

---

## Page 30 — The Value of This Work

The AQI Tower project has produced:

- A documented engineering design process, traceable to sources
- A parametric CAD model and CFD-validated geometry (GEO_C)
- Identification and simulation-level fix of a critical bypass flaw
- A complete bench-test protocol for formaldehyde characterisation
- A procurement research base for India availability and pricing
- A rigorous NO-GO decision on water spray — with documentation
- An interactive 3D engineering viewer with enforced epistemic labelling
- 18 phases of structured engineering documentation

This is not a finished product. It is a structured foundation — the kind that reduces wasted effort in physical prototyping, identifies failure modes early, and provides a basis for expert review.

---

## Page 31 — Claims We Do Not Make

The following claims are explicitly **not made** in this report, and must not be inferred:

- ❌ AQI Tower has a validated CADR
- ❌ AQI Tower removes PM2.5 at any specified efficiency
- ❌ AQI Tower removes formaldehyde at any specified efficiency
- ❌ The simulated airflow (1,332 m³/h) is the real-world operating airflow
- ❌ The simulated pressure drop (111 Pa) is the real-world filter pressure drop
- ❌ 62.1% particle arrival equals 62.1% particle capture
- ❌ CFD bypass ≈0% proves the physical housing is sealed
- ❌ H13 ≥99.95% element efficiency equals whole-system PM2.5 efficiency
- ❌ The carbon bed will remove formaldehyde at any specified rate
- ❌ Water spray was considered for final design
- ❌ Any physical prototype has been built, tested, or measured

---

## Page 32 — Key Numbers Summary

All numbers carry their evidence classification.

| Number | Value | Classification |
|--------|-------|----------------|
| Simulated airflow (CASE_M_SEALED) | 1,332.205 m³/h | SIMULATION ONLY |
| Simulated HEPA ΔP | 111.181 Pa | SIMULATION ONLY |
| Simulated HEPA face velocity | 1.0525 m/s | SIMULATION ONLY |
| Bypass before seal | 45.05% | SIMULATION ONLY |
| Bypass after seal | ~0% | SIMULATION ONLY |
| 0.3 µm particle arrival fraction | 62.1% (139/224) | SIMULATION — NOT CAPTURE |
| GEO_C simulated airflow | 1,496.055 m³/h | SIMULATION ONLY |
| KVO 250 shutoff pressure | ~688 Pa ± 20 Pa | MANUFACTURER DATA |
| H13 HEPA efficiency (MPPS) | ≥99.95% | MANUFACTURER DATA / EN 1822 |
| HEPA rated ΔP | 300 Pa at 2.84 m/s | MANUFACTURER DATA (single point) |
| HEPA gross face area | 593 × 593 mm | CAD GEOMETRY |
| SDP810 sensor price | ₹4,748 / unit | CONFIRMED QUOTE (Tanotis, 2026-09-07) |
| Rotameter price | ₹1,950 | CONFIRMED QUOTE (Shree Aashapura, 2026-09-07) |
| Water spray decision | NO-GO | PHASE 18 DECISION |

---

## Page 33 — Closing Vision

Clean air should not be a luxury. The goal of this project is a device that is:

- **Effective:** measurably reduces PM2.5 and formaldehyde in a real Indian home
- **Honest:** every claim grounded in physical measurement
- **Affordable:** designed with India cost and supply chains in mind
- **Open:** documented so others can learn from both the progress and the gaps

The simulation work is done. The design framework is in place. The next chapter requires physical hardware, an institutional laboratory, and patient, careful experimentation.

That next chapter has not started yet. This report is the end of the first one.

---

## Page 34 — Technical Appendix

**Source files (in repository):**

| File | Contents |
|------|----------|
| `results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json` | GEO_C airflow, pressure, fan head |
| `results/GEOMETRY_OPTIMIZATION/comparison_metrics.json` | All geometry variant metrics |
| `results/FILTER_H13/bypass_analysis_sealed.json` | CASE_M_SEALED filter, bypass, face velocity |
| `results/PARTICLE_CFD/particle_arrival_fractions.json` | Particle arrival by size |
| `data/fans/README.md` | KVO 250 fan data and curve |
| `data/filters/HEPA_EFFICIENCY_EVIDENCE.md` | H13 HEPA evidence chain |
| `docs/PHASE18_WATER_SPRAY_FEASIBILITY.md` | Water spray analysis |
| `docs/PHASE18_WATER_SPRAY_DECISION_MATRIX.md` | Decision matrix (84 vs 13 pts) |
| `docs/PHASE14_FORMALDEHYDE_TARGET.md` | Formaldehyde target rationale |
| `docs/PHASE15_TEST_RIG_ENGINEERING_SPEC.md` | Bench-test rig specification |
| `docs/PHASE15_BOM.md` | Bill of materials |
| `docs/PHASE15_DATA_ACQUISITION_SPEC.md` | DAQ specification |

**CFD case register:**

| Case | Status | Notes |
|------|--------|-------|
| V00 | PARTIAL | Initial baseline — riser recirculation identified |
| V01 | CONVERGED | Baseline metrics; 23.12% reverse flow |
| GEO_B | CONVERGED | Improved geometry |
| GEO_C | CONVERGED | Best geometry; 1,496 m³/h simulated |
| GEO_C_CONFIRM | CONVERGED | Confirmation run |
| CASE_M | PARTIAL | With HEPA model; 45% bypass discovered |
| CASE_M_SEALED | PARTIAL NON-CONVERGED | Bypass sealed; 1,332 m³/h; used as primary result |

*Evidence classification system used throughout: MEASURED · SIMULATED · MANUFACTURER DATA · RESEARCH EVIDENCE · ENGINEERING INFERENCE · PROVISIONAL · FUTURE WORK*
