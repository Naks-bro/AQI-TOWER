# AQI Tower

AQI Tower is a student-led project to develop and computationally investigate a tower-type air-purification system before any physical fabrication. The working concept is a vertical machine with driven airflow, multiple filtration stages, biomass-derived adsorption, and eventual sensing and monitoring. These are hypotheses to investigate, not a final design.

**Phase 18 engineering decision:** The initially proposed water-spray stage has been evaluated and rejected on technical grounds (NO-GO). It is replaced by a G4/M5 washable panel pre-filter. See `docs/PHASE18_WATER_SPRAY_FEASIBILITY.md` and `docs/PHASE18_WATER_SPRAY_DECISION_MATRIX.md`.

## Current Project Phase

**PHASE 19 COMPLETE — G4/M5 PRE-FILTER SPECIFICATION — RFQ REQUIRED BEFORE FINAL PRODUCT FREEZE.**
**PHASE 18 COMPLETE — WATER-SPRAY STAGE FEASIBILITY — DECISION: NO-GO.**
**PHASE 17B — PROCUREMENT UNBLOCK — RFQ READY — NO ITEMS ORDERED YET.**
**PHASE 17A EXPERIMENT: BLOCKED — HARDWARE NOT YET AVAILABLE.**
**GAS-PHASE CFD: BLOCKED — NO MEASURED INPUTS YET. HCHO TESTING: DEFERRED (requires institutional safety approval).**

Phase 19 converted the Phase 18 G4/M5 recommendation into a technical specification, procurement package, and pressure-drop analysis. No experiment was performed. No CFD was run. No CAD was changed. No existing results were modified.

Phase 18 evaluated whether the proposed water-spray stage is technically justified. The decision is NO-GO. The stage is replaced by a G4/M5 washable panel pre-filter. No experiment was performed. No CFD was run. No CAD was changed. No existing results were modified.

Phase 17B researches and documents actionable procurement routes for all Phase 17A hardware blockers. No items have been ordered.

Phase 17A produces no fake data. Fabricating experimental results is explicitly prohibited.

### Phase 18 record

**PHASE 18 COMPLETE — WATER-SPRAY STAGE FEASIBILITY — DECISION: NO-GO — DATE: 2026-09-07.**

Phase 18 is a research-only engineering go/no-go review of the proposed water-spray pre-treatment stage. No CFD was run, no CAD was changed, no existing results were modified.

Key Phase 18 findings:

- **PM2.5 irrelevant:** Simple spray cannot capture PM2.5. The Greenfield gap (0.1–2 µm) means inertial impaction and diffusion are both ineffective at this scale and energy input. Expected efficiency < 3% for 0.3–2.5 µm particles.
- **Hygiene risk is disqualifying:** Recirculating warm water with aerosol generation (Legionella, biofilm, mold) in a device delivering air to a breathing zone violates the device's fundamental purpose. ASHRAE 188 and CIBSE TM13 requirements are not feasible for a student prototype.
- **Coarse function fully replaced:** The only defensible function — coarse pre-collection — is achieved more safely and efficiently by a dry G4/M5 washable panel pre-filter.
- **Pressure drop penalty:** 35–125 Pa additional resistance reduces airflow by 7–23% on an already constrained KVO 250 fan.
- **HCHO removal negligible:** < 0.1% per pass at project concentrations. Not a substitute for the activated carbon stage.
- **Complexity unjustified:** 12+ additional components for zero unique, irreplaceable function.
- **Decision matrix:** Option B (G4/M5 pre-filter) scores 84/100; Option A (water spray) scores 13/100. The 71-point gap is insensitive to weighting changes.
- **Recommended treatment sequence:** Inlet → [G4/M5 washable pre-filter] → [Activated carbon bed] → [H13 HEPA] → Clean riser → KVO 250 fan → Outlet
- **CFD unchanged:** GEO_C and CASE_M_SEALED remain valid; pre-filter ΔP can be added analytically when the product is selected.

See [docs/PHASE18_WATER_SPRAY_FEASIBILITY.md](docs/PHASE18_WATER_SPRAY_FEASIBILITY.md) and [docs/PHASE18_WATER_SPRAY_DECISION_MATRIX.md](docs/PHASE18_WATER_SPRAY_DECISION_MATRIX.md).

### Phase 19 record

**PHASE 19 COMPLETE — G4/M5 PRE-FILTER SPECIFICATION AND INTEGRATION — DATE: 2026-09-07.**

Phase 19 converted the Phase 18 recommendation into a technically defensible, procurable, mechanically integrable pre-filter stage. No CFD run, no CAD change, no experiment.

Key Phase 19 outputs:

- **Selected class:** G4 (EN 779:2012 / ISO Coarse ≥ 60%). Sufficient HEPA protection at lower ΔP than M5; M5 available as upgrade from same supplier.
- **Selected size:** 592 × 592 × 48 mm (matches HEPA footprint; face velocity 1.06 m/s = HEPA face velocity).
- **Clean ΔP estimate:** ~21–30 Pa at 1.06 m/s [engineering estimate — RFQ required for confirmed value].
- **System impact (clean G4):** Q drops from 1332 to ~1300 m³/h (~2.4% reduction from baseline). Remaining fan margin for carbon bed: ~57–67 Pa.
- **Maintenance trigger:** 80 Pa ΔP across pre-filter (SDP810-500Pa sensor, upstream/downstream static taps).
- **Integration:** slide-in cassette at inlet face; EPDM gasket seal; snap retention; no tools required.
- **Preferred supplier:** Freudenberg India (existing Phase 12A contact) + simultaneous backup RFQ to Camfil India.
- **Procurement status:** RFQ REQUIRED — T-01 (filter panel × 2), T-02 (cassette frame), T-04 (tower DP sensor).
- **CFD rerun:** NOT REQUIRED (< 3% flow change; within RANS uncertainty; analytical fan-curve intersection is adequate).

See [docs/PHASE19_PREFILTER_SPECIFICATION.md](docs/PHASE19_PREFILTER_SPECIFICATION.md), [docs/PHASE19_PREFILTER_DECISION_MATRIX.md](docs/PHASE19_PREFILTER_DECISION_MATRIX.md), and updated [docs/PRESSURE_DROP_BUDGET.md](docs/PRESSURE_DROP_BUDGET.md).

Phase 17B outputs (procurement unblock):

- **OVC 4×8 media:** Three verified India contact routes — (1) Kuraray India kuraray.com/in-en/contact-us/, (2) Kuraray Environmental Solutions carbon-solutions.kuraray.com, (3) Chemet India info@chemetindia.com +91 22 6680 2222 (confirmed Calgon Carbon distributor). Jacobi Carbons India (infoin@jacobi.net) identified as fallback non-OVC source. Price: REQUIRES QUOTE from all routes.
- **SDP810-500Pa:** Confirmed listing at Tanotis India; price **₹4,748.73 incl. taxes** (2026-09-07); "Add to cart" available.
- **Rotameter A (0–100 L/min):** Confirmed at Shree Aashapura Mumbai IndiaMART; price **₹1,950** (2026-09-07).
- **Testo 510:** Confirmed IndiaMART listings **₹9,999–₹12,197** (two India vendors, 2026-09-07); borrow from physics/civil lab first.
- **Acrylic column:** Requires custom 75 mm ID order (standard 75 mm OD ≈ 69 mm ID — wrong); fabrication spec in tracker; cost REQUIRES QUOTE (~₹600–1,500 tube + ₹1,000–3,000 machining).
- **FORMASORB:** Same Kuraray/Chemet routes as OVC 4×8; classified BUY LATER / QUOTE NOW; RFQ letter ready in PHASE17B_OVC4X8_RFQ.md.
- **Ready-to-send RFQ letters:** Two letters (OVC 4×8 and FORMASORB) in `docs/PHASE17B_OVC4X8_RFQ.md`; one alternative letter for Jacobi India if OVC 4×8 is unavailable.
- **Column fabrication spec:** Full dimensioned specification (75 mm ID, 300 mm length, machined end caps, O-ring grooves, pressure taps, screen seats, bed-depth scale, HCHO limitation notice) in `docs/PHASE17B_PROCUREMENT_TRACKER.md` Section 4.
- **Full tracker:** 17 P0 items, 3 P1 items, 7 P2 items, 8 P3 items with status, price, and next action in `docs/PHASE17B_PROCUREMENT_TRACKER.md`.
- **Verified buy-now minimum:** ₹6,698.73 confirmed (SDP810 + Rotameter A); total P0 estimated ~₹11,153 + media quote + column/machining quote.
- **Primary blocker:** OVC 4×8 lot availability and price — must be resolved before any other procurement decision is final.

See [docs/PHASE17B_PROCUREMENT_TRACKER.md](docs/PHASE17B_PROCUREMENT_TRACKER.md) and [docs/PHASE17B_OVC4X8_RFQ.md](docs/PHASE17B_OVC4X8_RFQ.md).

### Prior Phase 17A record (hardware blocked — planning complete)

Phase 17A planning outputs:

- **Pre-experiment checklist:** 17 items; all PENDING (hardware not in hand).
- **Instrument record template:** ready to complete on procurement.
- **Data template:** `results/PRESSURE_DROP_PHASE17A/RAW_DATA_TEMPLATE.csv` — correct headers; no data rows.
- **Analysis script:** `scripts/analysis/phase17a_analysis.py` — full Python pipeline; reads RAW_DATA.csv; applies validity flags; computes fixture-corrected ΔP; fits Darcy–Forchheimer (a and b) with non-negativity constraint; reports R², residuals, 95% CI; generates three figures; writes `DARCY_FORCHHEIMER_FIT.json`; handles empty-CSV gracefully.
- **Analysis method:** `results/PRESSURE_DROP_PHASE17A/PRESSURE_DROP_ANALYSIS.md` — validity categories (VALID / VALID_FLAGGED / INVALID), Stage A–D procedure, Darcy–Forchheimer fitting, OpenFOAM translation formulae.
- **Fit JSON template:** `results/PRESSURE_DROP_PHASE17A/DARCY_FORCHHEIMER_FIT_TEMPLATE.json` — schema with all nulls; overwritten by script when data are available.
- **Results document:** `docs/PHASE17A_PRESSURE_DROP_RESULTS.md` — full acceptance criteria, QC table, OpenFOAM translation table, all values NOT MEASURED, final decision table.
- **No fake data.** All ΔP fields, coefficients, and R² values are null or NOT MEASURED until physical experiment is performed.

See [docs/PHASE17A_PRESSURE_DROP_RESULTS.md](docs/PHASE17A_PRESSURE_DROP_RESULTS.md).

### Prior Phase 16 record

**PHASE 16 COMPLETE — PROCUREMENT-READY CLEAN-AIR PRESSURE-DROP SYSTEM.**

Phase 16 converted the Phase 15 engineering specification into a procurement-ready, build-ready clean-air pressure-drop test system. No experiment was performed. No CFD was run. No CAD was changed. HCHO testing is deferred to Phase 17B+.

Key Phase 16 outputs:

- **Phase 15 calculations independently audited:** all values confirmed correct; one rounding difference of 0.14 L/min at 0.80 m/s (not significant); new finding: Ergun estimate ~586 Pa at 104 mm bed, 1.05 m/s (marginally exceeds 500 Pa primary sensor range; backup wide-range instrument added).
- **Instruments selected:** Sensirion SDP810-500Pa (primary DP, I²C, 1 Pa resolution); Testo 510 0–10,000 Pa (secondary/check); Rotameter A 0–100 L/min ₹1,950 (baseline conditions); Rotameter B 0–300 L/min REQUIRES QUOTE (high-velocity conditions); SHT40 breakout T/RH sensor; Sensirion SHT40 ×2.
- **Column material decision:** acrylic 75 mm ID for Phase 16 clean-air only; SS316 or borosilicate glass required when HCHO breakthrough testing begins (Phase 17B+).
- **Rig flow schematic defined:** vertical column, bottom-to-top flow, pressure taps at each end, rotameter downstream (clean side).
- **Clean-air data schema defined:** 14 mandatory fields; post-processing only for corrected ΔP and Darcy–Forchheimer coefficients.
- **Test matrix defined:** Stage A (empty rig baseline) + Stages B/C/D (26/52/104 mm beds), five velocity points each, three independently repacked replicates per depth.
- **Stop criteria, QC thresholds, and replicate rejection criteria defined.**
- **Darcy–Forchheimer fitting procedure specified:** from measurements only; no invented or literature coefficients.
- **Procurement tables:** BUY NOW (clean-air items, ~₹11,550 Tier 1 minimum / ~₹35,000 Tier 2 recommended); BUY LATER (HCHO items — not until Phase 17B approval); OUTSOURCE (column machining, external HPLC).
- **Build order: 15 numbered steps** with per-step acceptance checks.
- **Critical procurement blockers:** OVC 4×8 India availability and lot quote; column machining lead time; SDP810 India stock confirmation; Rotameter B quote.

See [docs/PHASE16_INSTRUMENT_SELECTION.md](docs/PHASE16_INSTRUMENT_SELECTION.md), [docs/PHASE16_PROCUREMENT_PLAN.md](docs/PHASE16_PROCUREMENT_PLAN.md), and [docs/PHASE16_CLEAN_AIR_TEST_PROTOCOL.md](docs/PHASE16_CLEAN_AIR_TEST_PROTOCOL.md).

### Prior Phase 15 record

**PHASE 15 COMPLETE — TEST-RIG ENGINEERING SPECIFICATION.**

Phase 15 converted the Phase 14 experimental requirements into a buildable, procurement-ready engineering package for the packed-bed bench test. No experiment was performed. No CFD was run. No CAD was changed.

Key Phase 15 outputs:

- **Column diameter selected:** 75 mm ID recommended (wall-effect ratio 15.8×; flows 35–278 L/min across the full Phase 14 velocity matrix). 50 mm is the minimum viable alternative.
- **Column and flow matrix tabulated:** exact Q (L/min), EBCT (s), and bed volume (mL) for all Phase 14 combinations of U_s (0.13–1.05 m/s) and bed depth (26, 52, 104 mm).
- **SFA30 documentation verified:** current v1.3 datasheet (January 2025) confirmed. ±20 ppb accuracy floor means the SFA30 cannot alone validate C/C0 ≤ 0.10 at the 50 µg/m³ inlet. DNPH–HPLC reference method is mandatory.
- **DNPH / HPLC workflow defined:** ISO 16000-3:2022 cartridge sampling with outsourced analysis; institutional laboratory collaboration recommended before purchasing cartridges.
- **HCHO generation specification:** Architecture A (certified gas cylinder + two calibrated MFCs + static mixer + exhaust scrubber) defined as the recommended approach. All cylinder/MFC items require quotes; institutional safety approval required before any purchase.
- **Pressure and flow measurement architectures defined:** 0–500 Pa DP sensor (≤1 Pa resolution), rotameter for pressure-drop tests, MFC for breakthrough tests.
- **Media containment, sealing, sampling ports, transport-delay, and safety boundary all defined.**
- **Synchronized data schema and Raspberry Pi CSV logger architecture defined.**
- **BOM produced:** all items classified (VERIFIED PRODUCT / CANDIDATE PRODUCT / GENERIC REQUIREMENT / REQUIRES QUOTE / UNKNOWN); cost tiers established.
- **Critical procurement blockers identified:** institutional safety approval, OVC 4×8 / FORMASORB India availability, certified HCHO cylinder, MFCs, and external HPLC laboratory.

See [docs/PHASE15_TEST_RIG_ENGINEERING_SPEC.md](docs/PHASE15_TEST_RIG_ENGINEERING_SPEC.md), [docs/PHASE15_BOM.md](docs/PHASE15_BOM.md), and [docs/PHASE15_DATA_ACQUISITION_SPEC.md](docs/PHASE15_DATA_ACQUISITION_SPEC.md).

### Prior Phase 14 record

**PHASE 14 COMPLETE — FORMALDEHYDE GAS-PHASE TARGET FROZEN.**

Phase 14 independently compared formaldehyde, benzene, toluene, acetone, ethanol, and generic TVOC. Formaldehyde ranked first in the documented weighted decision matrix and is now the single target gas for the carbon-stage research program.

Key Phase 14 decisions:

- **Target gas:** formaldehyde, HCHO / CH₂O, CAS 50-00-0.
- **Baseline challenge:** 100 µg/m³ (about 81.3 ppb at 25 °C and 1 atm); comparison points 50 and 200 µg/m³.
- **Baseline environment:** 25 ± 2 °C and 50 ± 5% RH; high-humidity stresses are defined separately.
- **Primary breakthrough metric:** `t10`, the elapsed time and treated bed volumes to sustained, time-aligned `C/C0 ≥ 0.10`, confirmed by a reference method.
- **Material decision B:** Calgon Carbon OVC 4×8 remains the non-impregnated research control, while a traceable formaldehyde-specific impregnated carbon such as FORMASORB is the secondary comparison.
- **Measurement:** synchronized upstream/downstream dedicated HCHO sensors for the continuous curve, with DNPH–HPLC as the concentration reference. The low-cost sensors are not sufficient alone for early low-outlet validation.
- **Safety:** intentional HCHO generation is restricted to a closed, exhausted, institutionally approved laboratory system. No improvised hotplate, formalin, polymer, furniture, or occupied-room challenge is permitted.
- **No performance claim:** no formaldehyde removal efficiency, adsorption capacity, breakthrough time, bed life, gas CADR, or porous-media coefficient has been measured.

See [docs/PHASE14_FORMALDEHYDE_TARGET.md](docs/PHASE14_FORMALDEHYDE_TARGET.md).

### Prior Phase 13 record

Phase 13 defined the proposed carbon stage as a gas-phase adsorption stage rather than a generic AQI or particulate filter. It selected Calgon Carbon OVC 4×8 as a primary research candidate before the gas target was known, documented FORMASORB as a conditional HCHO specialist, and recorded the missing pressure and adsorption data. Phase 14 supersedes only the earlier **TARGET GAS — NOT YET DEFINED** status; the Phase 13 evidence limitations remain in force.

See [docs/BIOCHAR_MATERIAL_SELECTION.md](docs/BIOCHAR_MATERIAL_SELECTION.md), [docs/BIOCHAR_EXPERIMENT_PLAN.md](docs/BIOCHAR_EXPERIMENT_PLAN.md), and [docs/BIOCHAR_CFD_PLAN.md](docs/BIOCHAR_CFD_PLAN.md).

### Prior Phase 12B record

**PHASE 12B COMPLETE — CONSERVATIVE PARTICLE TRACKING.**

Phase 12B tracked four assumed particle sizes through the frozen `CASE_M_SEALED` timestep-5000 velocity field. The airflow CFD, geometry, fan, bypass seal, and HEPA pressure-drop model were not changed or rerun.

Key Phase 12B findings:
- **FILTER ARRIVAL FRACTION:** 62.1% for 0.3, 1, and 2.5 µm; 61.2% for 10 µm.
- **WALL DEPOSITION FRACTION:** 37.9% for 0.3, 1, and 2.5 µm; 38.8% for 10 µm. These totals include both filter-frame contacts and other wall contacts; the source results retain those subcategories.
- **OUTLET ESCAPE FRACTION:** 0% in the conservative terminal accounting. This is a result of the sealed flow topology and the upstream filter-arrival gate, not proof of particle capture.
- **Particle accounting:** exact for every size (224 injected = filter arrival + wall deposition + outlet escape + other).
- **Model scope:** one-way, dilute equilibrium-slip paths with gravity; nearest-neighbour velocity lookup and first-order Euler stepping. The figures show airflow streamlines and tracked particle terminal positions, not stored full particle path histories.
- **FILTER ARRIVAL ≠ FILTER CAPTURE.** No filter capture probability was applied. Product-specific η(d_p) remains unavailable, so no filtration-efficiency, PM2.5-removal, CADR, or AQI-reduction claim is made.

See [docs/PARTICLE_CFD_V12B.md](docs/PARTICLE_CFD_V12B.md) and [results/PARTICLE_CFD/PARTICLE_TRACKING_RESULTS.md](results/PARTICLE_CFD/PARTICLE_TRACKING_RESULTS.md).

### Prior Phase 12A record

**Phase 12A — Freudenberg technical data acquisition — COMPLETE.**

Phase 12A searched all available public sources for fractional efficiency, MPPS, and multi-point pressure-drop data for the Freudenberg SF13-B-0593x0593x292 H13 HEPA filter. No CFD was run or modified.

Key Phase 12A findings:
- **Fractional efficiency curve η(d_p): NOT PUBLICLY AVAILABLE.** No efficiency vs particle size data found in any public source, including manufacturer product pages, downloads centre, or product catalog.
- **MPPS particle diameter: NOT AVAILABLE** as product-specific data. Generic glass fibre range is 0.1–0.25 µm (literature).
- **Multi-point ΔP curve: NOT AVAILABLE.** Only the single rated point (300 Pa at 2.84 m/s) is publicly listed.
- **ISO 29463 class confirmed: ISO 35 H** (equivalent to H13 EN 1822). New data point from Freudenberg US product page.
- **EN 1822 test certificate confirmed to accompany each unit.** This certificate contains the actual fractional efficiency data and MPPS — it must be obtained on purchase.
- **Freudenberg India contact established:** Pune HQ +91 20 67633600, email info@freudenberg-filter.com. Draft data request letter written.

See [docs/FREUDENBERG_DATA_REQUEST.md](docs/FREUDENBERG_DATA_REQUEST.md), [docs/FREUDENBERG_DATA_GAPS.md](docs/FREUDENBERG_DATA_GAPS.md).

### Prior Phase 11 record

**Phase 11 — HEPA efficiency evidence audit + CADR methodology — COMPLETE.**

Phase 11 audited all available HEPA filtration-efficiency information, defined a rigorous CADR methodology, and planned the future particle CFD study. No CFD was run or modified.

Key Phase 11 findings:
- **H13 classification confirmed** (EN 1822, ≥99.95% at MPPS) from Freudenberg product page. This is the only confirmed efficiency data point.
- **Particle-size-specific efficiency data: NOT AVAILABLE** for this product. No efficiency curve, no MPPS value, no data at PM2.5 or PM10 sizes.
- **Efficiency at AQI Tower face velocity (1.05 m/s): NOT AVAILABLE.** The EN 1822 test is at 2.84 m/s.
- **FINAL CADR = NOT ESTABLISHED.** A conditional theoretical estimate (~1331 m³/h at MPPS) is defined but explicitly labelled THEORETICAL / CONDITIONAL — NOT MEASURED.
- **CADR claim hierarchy (Levels 0–4)** defined in `docs/CADR_METHODOLOGY.md`. Current position: Level 0–1.
- **Future particle CFD plan** defined in `docs/PARTICLE_CFD_PLAN.md`. Not yet run.

See [docs/CADR_METHODOLOGY.md](docs/CADR_METHODOLOGY.md), [data/filters/HEPA_EFFICIENCY_EVIDENCE.md](data/filters/HEPA_EFFICIENCY_EVIDENCE.md), [docs/PARTICLE_CFD_PLAN.md](docs/PARTICLE_CFD_PLAN.md).

### Prior Phase 10B record

**Phase 10B — HEPA H13 filter bypass sealed — COMPLETE.**

Phase 10A diagnosed the 38–48% filter bypass (Phase 9) as an unintended open connection at z = 0.850 m between the dirty plenum and the CLEAN_RISER (x = 0.260–0.305 m overlap zone). Phase 10B sealed this gap with a wall baffle and reran CASE_M. Bypass dropped from 45% to ~0%. The corrected operating point is **Q ≈ 1332 m³/h, fan head ≈ 115 Pa, filter ΔP = 111 Pa** — much closer to the Phase 6D analytical budget (Q ≈ 1300 m³/h, ΔP ≈ 133 Pa). CADR estimation is now gated only by filter efficiency data (not yet available). See [results/FILTER_H13_COMPARISON.md](results/FILTER_H13_COMPARISON.md) and [docs/FILTER_BYPASS_FIX.md](docs/FILTER_BYPASS_FIX.md).

### Prior Phase 9 record

**Phase 9 — HEPA H13 filter resistance CFD — PARTIAL COMPLETE — FILTER BYPASS DISCOVERED.**

Three sensitivity cases (CASE_L / CASE_M / CASE_H) were run on the GEO_C tower geometry with a porous-baffle representation of the Freudenberg SF13-B H13 HEPA filter, driven by the KVO 250 6-point fan curve. The filter model is calibrated to the single available manufacturer data point (300 Pa at 2.84 m/s, clean). All three cases ran 5000 iterations; all are PARTIAL — NON-CONVERGED (same RANS limit as V00/GEO_C); integrated quantities are stable.

Key Phase 9 findings:
- **H13 filter is the dominant system resistance.** Fan operating head increases 13–19× from the empty-tower baseline (3.50 → 45–68 Pa) for CASE_L → CASE_H. Airflow drops only 4–6% (1496 → 1402–1435 m³/h) because the KVO 250 operates on a flat fan curve near free delivery.
- **Filter bypass discovered: 38–48% of airflow bypasses the filter face.** Bypass fraction increases with filter resistance — a physically real flow path around the filter. Effective filtration fraction: 52–62% of total Q. Resolved in Phase 10B. See [FILTER_H13_COMPARISON.md](results/FILTER_H13_COMPARISON.md).
- **Porous-baffle relaxation = 0.005 required** for stable filter ΔP behaviour. Default (0.2) produced oscillatory filter ΔP per iteration. This setting must be preserved for all future filter-stage CFD.
- **CFD result vs. budget:** CFD gives Q ≈ 1412 m³/h at 61 Pa (CASE_M unsealed), compared to the Phase 6D analytical estimate of Q ≈ 1300 m³/h at 133 Pa. The difference was primarily driven by the bypass path reducing effective system resistance.

See [results/FILTER_H13_COMPARISON.md](results/FILTER_H13_COMPARISON.md) and [docs/FILTER_H13_MODEL.md](docs/FILTER_H13_MODEL.md).

### Prior Phase 8 record

**Phase 8 — Airflow geometry optimization — COMPLETE.**

Three new parametric empty-tower geometries were tested with the unchanged six-point KVO 250 terminal-suction model and comparable 20 mm all-hexahedral meshes. GEO_C is the **PROMISING / BEST CURRENT GEOMETRY**: it converged in 926 iterations and a fresh confirmation reproduced the result exactly. Relative to V01, GEO_C reduces simulated empty-path total-pressure loss from 17.33 to 3.50 Pa, peak speed from 6.53 to 5.62 m/s, full-riser reverse-flow indicator from 23.12% to 15.88%, and riser-entry CoV from 1.087 to 0.234.

GEO_A is **PROMISING BUT UNCERTAIN** because its improved airflow field remains non-converged. GEO_B is **REJECTED** because recirculation/low-speed metrics worsen despite convergence. See [Phase 8 comparison](results/GEOMETRY_OPTIMIZATION_COMPARISON.md) and [setup/diagnosis](docs/GEOMETRY_OPTIMIZATION.md). V00 and V01 are preserved. No filters, particles, water, solar, or final product geometry were added.

### Prior Phase 6D record

Phase 5 (V00, empty tower, placeholder 1 m/s inlet) is complete at the PARTIAL — NON-CONVERGED level. The best V00 solution (SIMPLEC, iteration 6000) showed ~33 Pa empty-tower pressure drop at Q = 1,512 m³/h.

Phase 6B conducted real manufacturer research on five fan candidates. Phase 6C verified three manufacturer PDFs directly and obtained the first real HEPA H13 filter data point. Phase 6D extracted a full numeric fan curve for the KVO 250 from the PDF using PyMuPDF vector path extraction. Key findings:

- **G2E140 thermal-limit claim corrected (Phase 6C):** The "50 Pa maximum back pressure" from Phase 6B was a misinterpretation. The manufacturer document specifies a MINIMUM test back pressure (not a maximum operating limit). The G2E140 cannot be rejected on thermal grounds; remains Tier 3 pending performance datasheet.
- **Systemair KVO 250 — Evidence A — 6-point fan curve — CFD READY (Phase 6D):** Manufacturer catalog confirmed (Phase 6C). All specs confirmed. Fan curve: 2 confirmed numeric + 4 graph-digitized points via PyMuPDF Bezier extraction. **Shutoff head CORRECTED: ~688 Pa ±20 Pa** (Phase 6C rough estimate was ~850 Pa — outside the stated uncertainty range). CFD STATUS: CFD READY WITH GRAPH-DIGITIZATION UNCERTAINTY.
- **First filter data (Phase 6C):** Freudenberg SF13-B H13 HEPA, 593×593×292 mm, 300 Pa initial ΔP at 2.84 m/s. Single point only.
- **Preliminary operating estimate (KVO 250 + one clean HEPA):** Q ≈ 1300 m³/h at ΔP ≈ 133 Pa — rough orientation figure, unchanged by Phase 6D shutoff correction (operating point lies in confirmed curve region).
- **V01_fan placeholder is archived.** Phase 7 used a terminal suction boundary with the actual curve; no baffle or CAD change was needed.
- **No final fan selected.** The empty-tower numerical operating point is available; the final purifier operating point remains unknown.

See [docs/FAN_SELECTION.md](docs/FAN_SELECTION.md), [docs/FAN_DATA_GAPS.md](docs/FAN_DATA_GAPS.md), [docs/FAN_CURVE_AUDIT.md](docs/FAN_CURVE_AUDIT.md), and [docs/PRESSURE_DROP_BUDGET.md](docs/PRESSURE_DROP_BUDGET.md).

## Repository Purpose

The repository is intended to keep the work reproducible and understandable for a student team with computer science and biotechnology backgrounds. Engineering decisions should be documented in accessible language and progressively validated instead of treating the current concept as correct.

## Current Software Status

Last updated: 2026-09-07 (Phase 17B procurement unblock complete — RFQ letters ready; OVC 4×8 routes identified; SDP810 and Rotameter A prices confirmed; column fabrication spec written; no CFD, CAD change, or experiment performed).

- **DETECTED:** Windows 11, FreeCAD 1.1.3, Python, Git, Node.js, npm, WSL 2 with Ubuntu, Visual Studio Code, CMake, GCC, and Clang.
- **INSTALLED (Phase 5):** OpenFOAM Foundation 14 (Ubuntu package), ParaView 5.11.2 with python3-paraview — both in WSL Ubuntu.
- **NOT INSTALLED:** CfdOF workbench, Three.js project package.
- **FACT:** FreeCAD was installed on `D:` with explicit approval during Phase 4.

See [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) for detected versions and hardware details.

## Repository Layout

| Location | Current content |
| --- | --- |
| `docs/` | Environment, project overview, CAD V00, CFD V00 documentation |
| `requirements/` | Engineering requirements, requirements matrix, assumptions |
| `cad/parametric/` | `AQI_Tower_ConceptA_V00.FCStd` — parametric FreeCAD model (Phase 4) |
| `cfd/V00/` | OpenFOAM case: mesh, boundary conditions, all timestep fields (0–9000), solver logs |
| `scripts/simulation/` | `run_cfd_v00.sh`, `run_cfd_v00_continue.sh`, `analyze_cfd_v00.py` |
| `results/CFD_V00/` | `metrics.json`, `residuals.csv`, `residual_history.png`, `velocity_streamlines.png`, `pressure_section.png` |
| `results/CFD_V00_RESULTS.md` | Full V00 CFD results record |
| `results/CFD_V01_FAN_RESULTS.md` | Actual KVO 250 result, partial convergence, pressure definitions and comparison |
| `results/CFD_V01_FAN/` | Five figures, final metrics, residual history and independent verification |
| `cfd/V01_fan/` | Real KVO 250 curve-driven case; final fields at iteration 4000; archived placeholder |
| `cad/parametric/AQI_Tower_ConceptA_GEO_A/B/C.FCStd` | Native parametric Phase 8 design experiments; all dimensions labelled as non-requirements |
| `cfd/GEO_A/`, `cfd/GEO_B/`, `cfd/GEO_C/` | Three empty-tower geometry trials using the unchanged KVO 250 model |
| `cfd/GEO_C_CONFIRM/` | One fresh, identical GEO_C confirmation run |
| `results/GEOMETRY_OPTIMIZATION_COMPARISON.md` | Phase 8 results, pressure/airflow/recirculation comparison, classifications, and filter-readiness gate |
| `results/GEOMETRY_OPTIMIZATION/` | Actual metrics, field/residual figures, baseline diagnosis, comparison data, and verification |
| `docs/GEOMETRY_OPTIMIZATION.md` | Pre-run diagnosis, hypotheses, controlled trial plan, actual outcome, and reproduction workflow |
| `docs/FAN_SELECTION.md` | Fan comparison table, architecture options, Phase 6B/6C candidate assessments |
| `docs/FAN_DATA_GAPS.md` | Gap analysis, scenario analysis, next-action priority list (Phase 6C) |
| `docs/FAN_CURVE_AUDIT.md` | Per-candidate fan curve source, points, uncertainty, CFD readiness audit |
| `docs/PRESSURE_DROP_BUDGET.md` | System resistance framework; first filter data; preliminary operating point |
| `data/fans/README.md` | Minimum datasheet requirements; current candidate status |
| `data/fans/*.json` | Structured fan data records (5 candidates, updated Phase 6C) |
| `data/filters/README.md` | Minimum filter datasheet requirements |
| `data/filters/freudenberg_SF13B_593x593x292.json` | HEPA H13 filter data (Freudenberg, Phase 6C); Phase 12A: ISO 29463 class, India contacts, gap summary added |
| `docs/FREUDENBERG_DATA_REQUEST.md` | Phase 12A: data status, all sources searched, contact routes, draft inquiry letter for fractional efficiency data |
| `docs/FREUDENBERG_DATA_GAPS.md` | Phase 12A: gap impact table, CADR level readiness, particle CFD readiness, recommended actions |
| `scripts/simulation/run_cfd_v01_fan.sh` | Run script for V01_fan |
| `cfd/FILTER_H13/CASE_L/`, `CASE_M/`, `CASE_H/` | Phase 9 HEPA H13 porous-baffle cases; 5000-iteration runs; filter_implementation.json per case |
| `results/FILTER_H13_COMPARISON.md` | Phase 9 primary results: fan operating point, filter ΔP, bypass fraction, impact classification |
| `docs/FILTER_H13_MODEL.md` | Filter model methodology, Darcy derivation, bypass finding, convergence notes |
| `results/FILTER_H13/` | Phase 10A/10B visualizations: velocity/pressure slice, filter face maps, bypass streamlines, residual histories, 3-case comparison, before/after bypass figures, bypass_analysis.json, bypass_analysis_sealed.json |
| `docs/FILTER_BYPASS_DIAGNOSIS.md` | Phase 10A bypass diagnosis: geometric mechanism, evidence, per-case data, confidence, recommended fix |
| `docs/FILTER_BYPASS_FIX.md` | Phase 10B: fix implementation (bypassSeal baffle), verification (bypass~0%), updated operating point |
| `cfd/FILTER_H13/CASE_M_SEALED/` | Phase 10B bypass-sealed case; 5000-iteration run; all timesteps |
| `scripts/simulation/phase10a_visualize.py` | pvpython script that generated all Phase 10A figures |
| `scripts/simulation/prepare_case_m_sealed.py` | Pure Python: copies CASE_M and adds bypassSeal baffle to createBafflesDict |
| `scripts/simulation/phase10b_visualize.py` | pvpython script: generates Phase 10B before/after figures and bypass_analysis_sealed.json |
| `data/filters/HEPA_EFFICIENCY_EVIDENCE.md` | Phase 11: full evidence audit — H13 confirmed, particle-size data NOT AVAILABLE, CADR not established |
| `docs/CADR_METHODOLOGY.md` | Phase 11: CADR concept, claim hierarchy (Levels 0–4), system factors, conditional theoretical estimate |
| `docs/PARTICLE_CFD_PLAN.md` | Phase 11: Lagrangian particle CFD plan — scope, inputs required, open questions, sequence |
| `docs/PARTICLE_CFD_V12B.md` | Phase 12B: audited particle model, exact accounting, interpretation, limitations, and future η(d_p) hook |
| `scripts/simulation/phase12b_particle_tracking.py` | Phase 12B equilibrium-slip particle path integration and technical figure generator |
| `results/PARTICLE_CFD/` | Phase 12B machine-readable results, audited results record, four endpoint/streamline figures, and summary figure |
| `data/filters/biochar_candidates.json` | Phase 13 machine-readable candidate properties, evidence, gaps, and research selection |
| `docs/BIOCHAR_MATERIAL_SELECTION.md` | Phase 13 material distinctions, candidate comparison, adsorption evidence, pressure-loss evidence, and selection |
| `docs/BIOCHAR_EXPERIMENT_PLAN.md` | Future pressure-drop, adsorption, breakthrough, and humidity bench-test plan; no experiment performed |
| `docs/BIOCHAR_CFD_PLAN.md` | Future measured-data-driven porous-media framework; no coefficients and no CFD case created |
| `docs/PHASE14_FORMALDEHYDE_TARGET.md` | Frozen HCHO target, weighted pollutant selection, concentration/EBCT/measurement/safety requirements, material decision, experiments, and CFD data gates |
| `docs/PHASE15_TEST_RIG_ENGINEERING_SPEC.md` | Phase 15: column geometry analysis, diameter selection (75 mm), flow/EBCT/bed-volume tables, media containment, pressure and flow measurement, HCHO generation requirements, SFA30 current documentation, DNPH/HPLC workflow, sealing, safety boundary, acceptance criteria |
| `docs/PHASE15_BOM.md` | Phase 15: full procurement table by category; VERIFIED / CANDIDATE / GENERIC / REQUIRES QUOTE / UNKNOWN classification; three cost tiers; critical procurement blockers |
| `docs/PHASE15_DATA_ACQUISITION_SPEC.md` | Phase 15: synchronized data schema, Raspberry Pi CSV logger architecture, calibration requirements, C/C0 post-processing procedure, DNPH chain-of-custody record |
| `docs/PHASE16_INSTRUMENT_SELECTION.md` | Phase 16: Phase 15 calculation audit, column material selection, DP/flow/T-RH instrument selection, tubing/fittings/screens, ASCII flow schematic, clean-air data schema, acceptance criteria |
| `docs/PHASE16_PROCUREMENT_PLAN.md` | Phase 16: BUY NOW / BUY LATER / OUTSOURCE tables with India prices; three budget tiers (₹11,550 / ₹35,000 / ₹65,000); 15-step build order; procurement timeline |
| `docs/PHASE16_CLEAN_AIR_TEST_PROTOCOL.md` | Phase 16: Stage A–D test procedure, velocity sequence, pre-test checklist, replicate protocol, stop criteria, QC thresholds, Darcy–Forchheimer fitting procedure, data retention |
| `docs/PHASE17A_PRESSURE_DROP_RESULTS.md` | Phase 17A: BLOCKED status; pre-conditions checklist; NOT MEASURED data tables; OpenFOAM translation table; acceptance criteria; resume instructions |
| `docs/PHASE17B_OVC4X8_RFQ.md` | Phase 17B: ready-to-send RFQ letters for OVC 4×8 (Routes 1–4) and FORMASORB; what to record on receipt |
| `docs/PHASE17B_PROCUREMENT_TRACKER.md` | Phase 17B: full item tracker (17 P0, 3 P1, 7 P2, 8 P3 items); verified India prices; column fabrication spec (75 mm ID acrylic, end caps, O-rings, taps) |
| `results/PRESSURE_DROP_PHASE17A/RAW_DATA_TEMPLATE.csv` | Phase 17A: header-only CSV template; all data fields present; no measurement rows |
| `results/PRESSURE_DROP_PHASE17A/PRESSURE_DROP_ANALYSIS.md` | Phase 17A: data validity rules (VALID/FLAGGED/INVALID), fixture correction procedure, Darcy–Forchheimer fitting steps, Ergun comparison rules, OpenFOAM translation formulae |
| `results/PRESSURE_DROP_PHASE17A/DARCY_FORCHHEIMER_FIT_TEMPLATE.json` | Phase 17A: coefficient output schema; all values null; overwritten by analysis script on experiment completion |
| `scripts/analysis/phase17a_analysis.py` | Phase 17A: full Python analysis pipeline — validity flags, fixture correction, replicate statistics, Darcy–Forchheimer fit, plots, JSON output |
| `memory/project_status.md` | Concise current project state for future continuation |
| `reports/` | CAD preview and figure QA notes |
| `threejs/` | Not yet populated |
