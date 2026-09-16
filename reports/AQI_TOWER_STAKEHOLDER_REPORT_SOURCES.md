# AQI Tower Stakeholder Report — Claim Traceability

Every engineering claim in the report maps to a source file and JSON key or document section below.

---

## Airflow & Pressure — CFD Results

| Claim | Value | Source file | Key / location |
|-------|-------|-------------|----------------|
| GEO_C simulated airflow | 1,496.055 m³/h | `results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json` | `fan.Q_m3_h` |
| GEO_C fan head (operating pt) | 3.500 Pa | `results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json` | `fan.curve_static_Pa` |
| V01 total pressure loss | 17.326 Pa | `results/GEOMETRY_OPTIMIZATION/comparison_metrics.json` | `V01.tower_total_pressure_loss_Pa` |
| V01 riser reverse-flow | 23.12% | `results/GEOMETRY_OPTIMIZATION/comparison_metrics.json` | `V01.riser_reverse_percent` |
| CASE_M_SEALED total airflow | 1,332.205 m³/h | `results/FILTER_H13/bypass_analysis_sealed.json` | `CASE_M_SEALED.total_flow_m3_h` |
| CASE_M_SEALED filter ΔP (mean) | 111.181 Pa | `results/FILTER_H13/bypass_analysis_sealed.json` | `CASE_M_SEALED.filter_delta_P_area_mean_Pa` |
| CASE_M_SEALED face velocity (mean) | 1.0525 m/s | `results/FILTER_H13/bypass_analysis_sealed.json` | `filter_face_velocity_m_s.mean` |
| CASE_M bypass fraction (before) | 45.05% | `results/FILTER_H13/bypass_analysis_sealed.json` | `comparison.CASE_M_bypass_fraction` |
| CASE_M_SEALED bypass fraction | 9.997×10⁻¹⁰ | `results/FILTER_H13/bypass_analysis_sealed.json` | `CASE_M_SEALED.bypass_fraction` |

**Classification: SIMULATION ONLY — not physically measured**

---

## Particle Tracking Results

| Claim | Value | Source file | Key / location |
|-------|-------|-------------|----------------|
| 0.3 µm particles arrived at filter | 139 / 224 (62.1%) | `results/PARTICLE_CFD/particle_arrival_fractions.json` | `results.0p3um.arrived` / `results.0p3um.total` |
| 1 µm particles arrived at filter | 139 / 224 (62.1%) | `results/PARTICLE_CFD/particle_arrival_fractions.json` | `results.1um.arrived` / `results.1um.total` |
| 2.5 µm particles arrived at filter | 139 / 224 (62.1%) | `results/PARTICLE_CFD/particle_arrival_fractions.json` | `results.2p5um.arrived` / `results.2p5um.total` |
| 10 µm particles arrived at filter | 137 / 224 (61.2%) | `results/PARTICLE_CFD/particle_arrival_fractions.json` | `results.10um.arrived` / `results.10um.total` |
| 0.3 µm wall deposit fraction | ~37.9% | `results/PARTICLE_CFD/particle_arrival_fractions.json` | `results.0p3um.wall_deposit_fraction` |
| Seed points (all sizes) | 224 | `results/PARTICLE_CFD/particle_arrival_fractions.json` | `seed_count` |

**Classification: SIMULATION ONLY — FILTER ARRIVAL ≠ FILTER CAPTURE**

*Particle arrival at the filter face in simulation does not imply particle capture. Actual filtration efficiency requires physical measurement.*

---

## Fan Data

| Claim | Value | Source file | Key / location |
|-------|-------|-------------|----------------|
| KVO 250 shutoff pressure | ~688 Pa ± 20 Pa | `data/fans/README.md` + Phase 6D PyMuPDF extraction | Systemair catalogue vector path analysis |
| KVO 250 fan curve | 6-point characteristic | `data/fans/README.md` | Table: Q vs ΔP |

**Classification: MANUFACTURER DATA** — Systemair catalogue. Not independently verified by lab test.

---

## HEPA Filter Data

| Claim | Value | Source file | Key / location |
|-------|-------|-------------|----------------|
| H13 HEPA efficiency (MPPS) | ≥99.95% | `data/filters/HEPA_EFFICIENCY_EVIDENCE.md` | Freudenberg manufacturer page; EN 1822 classification |
| HEPA rated ΔP | 300 Pa at 2.84 m/s | `data/filters/HEPA_EFFICIENCY_EVIDENCE.md` | Freudenberg manufacturer data (single data point) |
| HEPA gross face area | 593 × 593 mm | CAD model (FreeCAD GEO_C) | Filter bay geometry |

**Classification: MANUFACTURER DATA / EN 1822 standard** — element-level efficiency under controlled test conditions. Whole-system efficiency is not the same as element efficiency.

---

## Water Spray Feasibility (Phase 18)

| Claim | Value | Source file | Key / location |
|-------|-------|-------------|----------------|
| Water spray decision | NO-GO | `docs/PHASE18_WATER_SPRAY_FEASIBILITY.md` | Executive decision |
| Water spray score | 13 / 100 | `docs/PHASE18_WATER_SPRAY_DECISION_MATRIX.md` | Option A score |
| G4/M5 pre-filter score | 84 / 100 | `docs/PHASE18_WATER_SPRAY_DECISION_MATRIX.md` | Option B score |
| Water spray ΔP estimate | 35–125 Pa | `docs/PHASE18_WATER_SPRAY_FEASIBILITY.md` | Engineering estimate (not measured) |
| Airflow reduction estimate | 7–23% | `docs/PHASE18_WATER_SPRAY_FEASIBILITY.md` | Engineering estimate from ΔP |
| HCHO removal by spray | <0.1% per pass | `docs/PHASE18_WATER_SPRAY_FEASIBILITY.md` | Research evidence (literature) |

**Classification: PHASE 18 DECISION — documented engineering review and decision matrix**

---

## Procurement Data

| Claim | Value | Source | Date confirmed |
|-------|-------|--------|----------------|
| SDP810 price | ₹4,748 / unit | Tanotis India (online vendor) | 2026-09-07 |
| Rotameter A price | ₹1,950 | Shree Aashapura, IndiaMART | 2026-09-07 |
| OVC 4×8 vendor routes | Kuraray India / Chemet India / Jacobi (fallback) | `memory/project_status.md` | Phase 17B |

**Classification: CONFIRMED QUOTE** — prices confirmed at stated date. Prices subject to change.

---

## Geometry and Design

| Claim | Value | Source | Notes |
|-------|-------|--------|-------|
| GEO_C — "current best geometry" | Simulation validated | CFD case register | Not final; not physically built |
| Treatment sequence (recommended) | Inlet → G4/M5 pre-filter → Carbon bed → H13 HEPA → Riser → KVO 250 → Outlet | Phase 18 decision | Recommended, not validated |
| Carbon bed column ID (recommended) | 75 mm | `docs/PHASE15_TEST_RIG_ENGINEERING_SPEC.md` | Wall-effect ratio 15.8× with OVC 4×8 |
| EBCT levels (bench test) | 0.05, 0.10, 0.20 s | `docs/PHASE14_FORMALDEHYDE_TARGET.md` | Experiment design, not operating targets |
| Test HCHO concentrations | 50, 100, 200 µg/m³ | `docs/PHASE14_FORMALDEHYDE_TARGET.md` | Experiment design |

---

## Evidence Classification System

| Badge | Meaning |
|-------|---------|
| MEASURED | Physically measured value — instrument, protocol, uncertainty stated |
| SIMULATED | Result from CFD or numerical model — no physical validation |
| MANUFACTURER DATA | From vendor datasheet, catalogue, or specifications page |
| RESEARCH EVIDENCE | From peer-reviewed or established technical literature |
| ENGINEERING INFERENCE | Derived from first principles or engineering calculation |
| PROVISIONAL | Working value pending confirmation — may change |
| FUTURE WORK | Not yet determined — requires experiment or additional data |

---

## Claims Explicitly Not Supported

The following are explicitly not claimed and must not be inferred from any value in this report:

| Not claimed | Why |
|-------------|-----|
| Validated CADR | No physical prototype tested; no measurement |
| PM2.5 removal efficiency | No physical measurement |
| HCHO removal efficiency | No experiment run |
| Real-world airflow = 1,332 m³/h | Simulation result; not measured |
| Real-world filter ΔP = 111 Pa | Simulation result; not measured |
| 62.1% = particle capture efficiency | Simulation arrival fraction ≠ capture |
| CFD bypass ≈0% proves physical seal | Simulation boundary condition; physical seal unverified |
| H13 99.95% = whole-system efficiency | Element efficiency ≠ system efficiency |
| Water spray considered for design | Phase 18 decision: NO-GO |
| Physical prototype exists | No prototype has been built |
