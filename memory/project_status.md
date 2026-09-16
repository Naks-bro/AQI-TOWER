# AQI-TOWER Project Status

Last updated: 2026-09-07

## Current phase

**PHASE 19 COMPLETE — G4/M5 PRE-FILTER SPECIFICATION — RFQ REQUIRED.**
**PHASE 18 COMPLETE — WATER-SPRAY STAGE: NO-GO.**
**PHASE 17B: RFQ READY — OVC 4×8 routes confirmed; SDP810 ₹4,748 Tanotis; Rotameter A ₹1,950 confirmed — no items ordered.**
**PHASE 17A EXPERIMENT: BLOCKED — HARDWARE NOT YET AVAILABLE.**
**GAS-PHASE CFD: BLOCKED — NO MEASURED INPUTS YET.**

No experiment has been performed. No CFD was run. No CAD was changed. No previous result was modified.

## Phase 19 key decisions

- **Selected pre-filter class: G4** (EN 779:2012 / ISO Coarse ≥ 60%). G4 preferred over M5: sufficient HEPA protection, lower ΔP, better fan margin for carbon bed.
- **Filter dimensions: 592 × 592 × 48 mm** (matches HEPA face; face velocity 1.057 m/s = same as HEPA).
- **Clean ΔP: ~21–30 Pa** at 1.057 m/s [engineering estimate — pending manufacturer RFQ].
- **Maintenance trigger: 80 Pa** (SDP810-500Pa sensor across pre-filter, upstream/downstream static taps).
- **System Q with clean G4: ~1300 m³/h** (~2.4% reduction from 1332 m³/h baseline). Fan head ~137 Pa. Remaining margin for carbon bed: ~57–67 Pa.
- **Preferred supplier: Freudenberg India** (existing Phase 12A contact: info@freudenberg-filter.com) + simultaneous backup RFQ to Camfil India (info.in@camfil.com).
- **Integration: slide-in cassette** at inlet face; EPDM gasket; no tools for filter removal/replacement.
- **CFD: NO RERUN REQUIRED.** < 3% flow change is within RANS uncertainty; analytical fan-curve intersection is adequate.
- **Procurement status: RFQ REQUIRED** — T-01 (filter × 2), T-02 (cassette frame ~₹500–2,000), T-04 (tower DP sensor ₹4,748.73 confirmed Tanotis).
- **CAD update: deferred to next CAD phase** — inlet cassette frame and pre-filter zone dimensions defined in spec.
- **Files created/updated:** docs/PHASE19_PREFILTER_SPECIFICATION.md, docs/PHASE19_PREFILTER_DECISION_MATRIX.md, docs/PRESSURE_DROP_BUDGET.md (Phase 19 section added), docs/PHASE17B_PROCUREMENT_TRACKER.md (Phase 19 tower items added).

## Phase 18 key decisions

- **Water-spray stage: NO-GO.** Simple spray cannot capture PM2.5 (Greenfield gap); hygiene risk (Legionella/biofilm in a breathing-zone device) is independently disqualifying; pressure drop 35–125 Pa would reduce Q by 7–23%; HCHO removal is negligible (<0.1% per pass); complexity adds 12+ components for zero unique benefit.
- **Recommended replacement: G4/M5 washable panel pre-filter** at inlet (upstream of carbon bed and H13 HEPA). Achieves the only defensible water-spray function (coarse pre-collection/HEPA life extension) with 1 component, ~25–50 Pa clean ΔP, no water, no hygiene risk, and wide India availability.
- **Decision matrix winner: Option B** (G4/M5 pre-filter, 84/100 pts) vs. Option A (water spray, 13/100 pts). Gap of 71 pts is insensitive to weighting choices.
- **Recommended new treatment sequence:** Inlet → [G4/M5 washable pre-filter] → [Activated carbon bed] → [H13 HEPA] → Clean riser → KVO 250 fan → Outlet
- **CFD unchanged:** GEO_C and CASE_M_SEALED results remain valid. Pre-filter ΔP can be added analytically when product is selected; no new CFD run required.
- **Three.js T1–T3 viewer: COMPLETE.** All modes operational (ARCHITECTURE, PARTICLE, CFD SUMMARY, CFD FIELD). Real CFD scalar planes exported and displayed. Build: 518 kB clean.
- **Files created:** docs/PHASE18_WATER_SPRAY_FEASIBILITY.md, docs/PHASE18_WATER_SPRAY_DECISION_MATRIX.md

## Phase 15 key decisions

- **Recommended column diameter:** 75 mm ID (wall-effect ratio 15.8×; ID/d_max for OVC 4×8).
- **Baseline condition (75 mm, 26 mm bed, 0.26 m/s):** Q = 68.9 L/min; EBCT = 0.100 s; bed volume = 114.9 mL.
- **Pressure sensor required:** 0–500 Pa differential, ≤1 Pa resolution.
- **HCHO generation:** Architecture A — certified gas cylinder + two MFCs + static mixer; institutional laboratory only.
- **SFA30 verified:** v1.3 datasheet January 2025; range 0–1000 ppb; ±20 ppb or ±20% accuracy at reference conditions; LOD < 20 ppb; India price observed ~₹7,099/unit (E Control Devices). Two modules required + one spare.
- **DNPH/HPLC reference:** ISO 16000-3:2022; outsourced to NABL/17025-accredited laboratory; no in-house HPLC.
- **DAQ:** Raspberry Pi 4B + Python CSV logger; 1 s log interval; all mandatory fields defined in schema.
- **Critical blockers:** institutional safety approval, OVC 4×8/FORMASORB India availability (REQUIRES QUOTE from Kuraray/Calgon Carbon India), certified HCHO cylinder (BOC/Linde India), MFCs (imported), external HPLC laboratory confirmation.
- **Files created:** docs/PHASE15_TEST_RIG_ENGINEERING_SPEC.md, docs/PHASE15_BOM.md, docs/PHASE15_DATA_ACQUISITION_SPEC.md.

## Phase 14 frozen decisions (still in force)

## Phase 14 frozen decisions (still in force)

- **Target gas:** Formaldehyde (HCHO / CH₂O), CAS 50-00-0.
- **Baseline media:** Calgon Carbon OVC 4×8 as a non-impregnated research control, not a proven final medium.
- **Secondary comparison:** Calgon Carbon FORMASORB or an equivalent traceable formaldehyde-specific impregnated carbon, conditional on exact-grade data, SDS, and procurement.
- **Test concentrations:** 50, 100, and 200 µg/m³; baseline 100 µg/m³ (about 81.3 ppb at 25 °C and 1 atm).
- **Baseline environment:** 25 ± 2 °C, 50 ± 5% RH.
- **Stress conditions:** 25 ± 2 °C / 70 ± 5% RH and 30 ± 2 °C / 70 ± 5% RH.
- **Bench EBCT levels:** 0.05, 0.10, and 0.20 s; baseline 0.10 s. These are experiment levels, not a final bed depth.
- **Primary breakthrough metric:** `t10`, elapsed time and treated bed volumes to sustained, time-aligned `C/C0 ≥ 0.10`, confirmed by the reference method.
- **Continuous measurement:** synchronized upstream/downstream dedicated HCHO sensors, with co-location, channel swapping, and transport-delay correction.
- **Reference measurement:** paired DNPH cartridges with HPLC/UV analysis under a validated laboratory method.
- **Safety boundary:** HCHO generation only in a closed, exhausted, institutionally approved laboratory using a controlled traceable source. No open hotplate/formalin/polymer/furniture or occupied-room challenge.

Full rationale: [Phase 14 formaldehyde target](../docs/PHASE14_FORMALDEHYDE_TARGET.md).

## Current validated project context

- **Geometry:** GEO_C is promising/best current, not final.
- **Airflow:** Phase 10B `CASE_M_SEALED` gives approximately 1332.2 m³/h, 115 Pa fan head, and 111.2 Pa H13 model pressure drop; the RANS result is partial/non-converged but integrated quantities were stable.
- **HEPA face:** 593 × 593 mm gross area; approximately 1.053 m/s at the Phase 10B flow.
- **Bypass:** the Phase 10B numerical bypass seal reduced the modelled bypass to approximately zero. A physical housing has not been tested.
- **Particle study:** Phase 12B is conservative equilibrium-slip arrival screening, not filter-capture or CADR validation.
- **Carbon evidence:** OVC 4×8 has a manufacturer pressure graph only within its published velocity range and no HCHO breakthrough data. FORMASORB is HCHO-specific by manufacturer application but also lacks matched quantitative breakthrough and pressure data.

## Explicit unknowns

- Actual HCHO removal efficiency, dynamic adsorption capacity, breakthrough time, bed life, and gas-phase CADR.
- Final carbon-bed area, depth, mass, packing, placement, seals, and allowable pressure budget.
- Measured pressure curve and fitted Darcy/Forchheimer coefficients.
- Measured HCHO breakthrough curves, humidity dependence, kinetic/mass-transfer parameters, and equilibrium model parameters.
- Exact India material availability, price, MOQ, SDS, disposal/reactivation route, laboratory access, reference analysis, and institutional safety approval.

## Next authorized work

Only after a new phase is approved: prepare the controlled bench test, obtain traceable media/instruments, secure institutional chemical-safety review and analytical-laboratory support, then perform clean-air pressure-drop testing before any HCHO breakthrough test. Do not start gas-phase CFD until measured inputs exist.
