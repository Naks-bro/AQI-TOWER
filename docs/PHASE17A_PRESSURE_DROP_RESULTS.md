# AQI Tower Phase 17A — Clean-Air Pressure-Drop Experiment

**PHASE 17A STATUS: BLOCKED — HARDWARE NOT YET AVAILABLE**
**Date: 2026-09-07**

---

## Why BLOCKED

Phase 17A requires physical measurements on the assembled bench-scale rig. The rig hardware (acrylic column, SDP810-500Pa sensor, Rotameter A, OVC 4×8 media lot) has not yet been procured or assembled. No measurements have been made. No ΔP data exist.

**No experimental values, Darcy–Forchheimer coefficients, or R² values appear in this document. All such fields are explicitly marked as NOT MEASURED.**

When the experiment is complete, this document will be updated with actual measurements. The sections below define exactly what must be recorded and reported.

---

## What Phase 17A Will Produce (Once Executed)

| Output | Location | Current state |
|---|---|---|
| Raw measurement CSV | `results/PRESSURE_DROP_PHASE17A/RAW_DATA.csv` | Template only — no data |
| Analysis method | `results/PRESSURE_DROP_PHASE17A/PRESSURE_DROP_ANALYSIS.md` | Written — ready |
| Fitted coefficients JSON | `results/PRESSURE_DROP_PHASE17A/DARCY_FORCHHEIMER_FIT.json` | Template only — all null |
| Empty-rig fixture plot | `results/PRESSURE_DROP_PHASE17A/stage_A_fixture_dp.png` | Not yet generated |
| ΔP_bed vs U_s plot | `results/PRESSURE_DROP_PHASE17A/dp_bed_vs_velocity.png` | Not yet generated |
| Darcy–Forchheimer plot | `results/PRESSURE_DROP_PHASE17A/darcy_forchheimer_fit.png` | Not yet generated |
| Analysis script | `scripts/analysis/phase17a_analysis.py` | Written — ready to run |

---

## 1. Experiment Pre-Conditions

All of the following must be in hand before the first measurement. This is the gate for starting.

| Pre-condition | Required state | Current state |
|---|---|---|
| OVC 4×8 media lot | Lot certificate; SDS; bulk density; particle size; lot number in hand | NOT RECEIVED — quote pending |
| Acrylic column (75 mm ID, 250 mm) | Fabricated; ID measured = 75 ± 0.5 mm; end caps fitted | NOT FABRICATED |
| SDP810-500Pa | Received; I²C address verified on RPi; zero check = 0 ± 1 Pa | NOT PROCURED |
| Testo 510 (or equivalent secondary) | Available; zero check = 0 ± 1 Pa | NOT CONFIRMED |
| Rotameter A (0–100 L/min) | Calibration check complete; correction factor recorded | NOT PROCURED |
| Compressed air supply | Reaches > 5 kPa at 100 L/min without pressure cycling | NOT CONFIRMED |
| SS316 mesh screens (≤2 mm) | Cut to 75 mm discs; deburring complete | NOT FABRICATED |
| Viton O-rings | Seat without extrusion in column | NOT PROCURED |
| RPi + SHT40 DAQ | CSV logger verified; clock synchronised; all 20 fields logged | NOT CONFIRMED |
| Bubble-leak test passed | All joints ≤5 bubbles/min at 200 Pa supply pressure | NOT YET PERFORMED |
| SDP810 and Testo 510 zero (pre-run) | Both 0 ± 1 Pa with taps open | NOT YET PERFORMED |
| Laboratory balance (0.01 g) | Borrowed or available | NOT CONFIRMED |
| Digital caliper (0.01 mm) | Borrowed or available | NOT CONFIRMED |
| Oven 105 °C (media drying) | Available | NOT CONFIRMED |
| Institutional media-handling sign-off | Even for non-hazardous carbon | NOT OBTAINED |

**Stage A may begin only when all rows in this table read CONFIRMED.**

---

## 2. Instrument Record (to be completed at experiment time)

| Instrument | Model | Serial / ID | Calibration date | Correction factor / notes |
|---|---|---|---|---|
| Primary DP sensor | Sensirion SDP810-500Pa | — | — | — |
| Secondary DP | Testo 510 | — | — | — |
| Flow meter | Rotameter A (0–100 L/min) | — | — | — |
| T/RH sensor | Sensirion SHT40 | — | — | — |
| DAQ | Raspberry Pi 4B | — | — | — |
| Balance | — | — | — | — |
| Caliper | — | — | — | — |

---

## 3. Media Record (to be completed at experiment time)

| Parameter | Value |
|---|---|
| Media name | Calgon Carbon OVC 4×8 |
| Lot number | NOT RECEIVED |
| Supplier | Kuraray / Calgon Carbon India (or distributor) |
| Lot bulk density (from certificate) | NOT RECEIVED kg/m³ |
| Lot particle size range (from certificate or sieve) | NOT RECEIVED mm |
| SDS received | NOT RECEIVED |
| Drying procedure | 105 °C, 2 h; cool in desiccator |
| Packing procedure | 20 tamps on rubber mat; settled depth measured before sealing upper end cap |

---

## 4. Stage A — Empty-Rig Fixture Results

NOT MEASURED.

Fields to be populated after Stage A:

| Step | Target U_s (m/s) | Target Q (L/min) | Measured Q (L/min) | ΔP_fixture mean (Pa) | SD (Pa) | Testo 510 (Pa) | Agreement | Status |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| A1 | 0.13 | 34.5 | — | — | — | — | — | NOT MEASURED |
| A2 | 0.26 | 68.9 | — | — | — | — | — | NOT MEASURED |
| A3 | 0.52 | 137.8 | — | — | — | — | — | NOT MEASURED |
| A4 | 0.80 | 212.1 | — | — | — | — | — | NOT MEASURED |
| A5 | 1.05 | 278.4 | — | — | — | — | — | NOT MEASURED |

Stage A acceptance criteria: ΔP_fixture monotonically increasing with Q; SDP810 and Testo 510 agree within ±3 Pa or ±5%.

---

## 5. Stage B — 26 mm Bed Results

NOT MEASURED.

### 5.1 Replicate summary

| Replicate | Mass (g) | Settled depth (mm) | Bed volume (mL) | Bulk density (kg/m³) | Status |
|---:|---:|---:|---:|---:|---|
| 1 | — | — | — | — | NOT MEASURED |
| 2 | — | — | — | — | NOT MEASURED |
| 3 | — | — | — | — | NOT MEASURED |

### 5.2 ΔP_bed results (fixture-corrected)

| U_s (m/s) | Rep 1 ΔP/L (Pa/m) | Rep 2 ΔP/L (Pa/m) | Rep 3 ΔP/L (Pa/m) | Mean ΔP/L (Pa/m) | CV (%) | QC |
|---:|---:|---:|---:|---:|---:|---|
| 0.13 | — | — | — | — | — | NOT MEASURED |
| 0.26 | — | — | — | — | — | NOT MEASURED |
| 0.52 | — | — | — | — | — | NOT MEASURED |
| 0.80 | — | — | — | — | — | NOT MEASURED |
| 1.05 | — | — | — | — | — | NOT MEASURED |

---

## 6. Stage C — 52 mm Bed Results

NOT MEASURED. (Same table structure as Stage B — to be populated after experiment.)

---

## 7. Stage D — 104 mm Bed Results

NOT MEASURED. (Proceed with Stage D only if: flow source reaches required Q; ΔP remains in instrument range; bed is mechanically stable; see Phase 16 protocol Section 6.1 for SDP810 saturation procedure.)

---

## 8. Darcy–Forchheimer Fit Results

NOT MEASURED.

### 8.1 Per-depth fits

| Bed depth | a (Pa·s/m²) | 95% CI | b (Pa·s²/m³) | 95% CI | R² | n | Velocity range (m/s) | Fit valid |
|---|---:|---:|---:|---:|---:|---:|---|---|
| 26 mm | — | — | — | — | — | — | — | NOT MEASURED |
| 52 mm | — | — | — | — | — | — | — | NOT MEASURED |
| 104 mm | — | — | — | — | — | — | — | NOT MEASURED |

### 8.2 Combined fit (all depths)

| a (Pa·s/m²) | 95% CI | b (Pa·s²/m³) | 95% CI | R² | n | Valid |
|---:|---:|---:|---:|---:|---:|---|
| — | — | — | — | — | — | NOT MEASURED |

### 8.3 Ergun comparison

**ERGUN COMPARISON BLOCKED — REQUIRED INPUT NOT AVAILABLE**

Required inputs not yet in hand:
- Mean particle diameter `d_p` from sieve analysis or traceable lot certificate
- Bed void fraction `ε` from measured bulk density and known particle density

Do not use literature values for `d_p` or `ε` without confirming they match this lot.

---

## 9. OpenFOAM Translation Table

Coefficients will be populated after fitting. The translation formulae and OpenFOAM meaning are defined now; only the numerical values are missing.

| Experimental quantity | Value | Units | OpenFOAM meaning | Verification status |
|---|---|---|---|---|
| Darcy coefficient `a` | NOT MEASURED | Pa·s/m² | `a = μ_air × d` → `d = a/μ` | PENDING |
| Forchheimer coefficient `b` | NOT MEASURED | Pa·s²/m³ | `b = ρ_air × f` → `f = b/ρ` | PENDING |
| OpenFOAM `d` (porous zone) | NOT MEASURED | m⁻² | Darcy permeability term in `DarcyForchheimer` model | PENDING |
| OpenFOAM `f` (porous zone) | NOT MEASURED | m⁻¹ | Forchheimer inertia term in `DarcyForchheimer` model | PENDING |
| μ_air at 25 °C | 1.849 × 10⁻⁵ | Pa·s | Used to convert a → d | FIXED |
| ρ_air at 25 °C | 1.184 | kg/m³ | Used to convert b → f | FIXED |
| Velocity range | 0.13–1.05 | m/s | Range over which fit is valid | PENDING |
| Column ID | 75 mm | — | Column this fit applies to | FIXED |
| Media lot | NOT RECEIVED | — | Lot this fit applies to | PENDING |

**OpenFOAM `DarcyForchheimer` model:** `ΔP/L = μ·d·U + ρ·|U|·f·U`

This translation is a documentation step only. The OpenFOAM case must not be modified with these coefficients until:
1. The fit passes R² ≥ 0.99 and CV ≤ 15% across replicates
2. The coefficients have been reviewed and the validity range documented
3. A new phase is explicitly approved for porous-zone CFD

---

## 10. Data Validity Summary

NOT MEASURED — will be populated by the analysis script.

| Category | Count | Run IDs |
|---|---|---|
| VALID | 0 | — |
| VALID_FLAGGED | 0 | — |
| INVALID | 0 | — |

---

## 11. Quality Control Results

NOT MEASURED.

| QC Check | Criterion | Result |
|---|---|---|
| SDP810 / Testo 510 agreement | ≤ ±3 Pa or ±5% | NOT MEASURED |
| Stage A monotonicity | ΔP increases with Q | NOT MEASURED |
| Within-run CV (ΔP) | ≤ 5% | NOT MEASURED |
| Cross-replicate CV (ΔP/L) | ≤ 15% at every velocity | NOT MEASURED |
| SDP810 zero drift between sessions | ≤ ±1 Pa | NOT MEASURED |
| Darcy–Forchheimer R² | ≥ 0.99 | NOT MEASURED |
| Fit residuals | ≤ 15% at all U_s | NOT MEASURED |
| Settled bed depth tolerance | ±3 mm of target | NOT MEASURED |
| Media fines at downstream screen | None | NOT MEASURED |
| Media movement / fluidization | None | NOT MEASURED |
| Combined vs per-depth fit agreement | a and b within ±20% across depths | NOT MEASURED |

---

## 12. Pre-Experiment Checklist (Final Gate)

Complete all rows before starting Stage A. Do not mark any row CONFIRMED without verifying the actual physical state.

| Item | Required | Status |
|---|---|---|
| OVC 4×8 lot certificate and SDS in hand | YES | PENDING |
| Column ID measured 75 ± 0.5 mm | YES | PENDING |
| End caps fitted; O-rings seated | YES | PENDING |
| Bubble-leak test passed (≤5 bubbles/min at 200 Pa) | YES | PENDING |
| SDP810 zero = 0 ± 1 Pa | YES | PENDING |
| Testo 510 zero = 0 ± 1 Pa (or BORROW confirmed) | YES | PENDING |
| RPi DAQ: CSV with all required fields confirmed on 5-min test run | YES | PENDING |
| Rotameter A calibration check: ≤3% at 3 flow points | YES | PENDING |
| RPi clock NTP-synced or RTC set within 60 s of reference | YES | PENDING |
| Balance (0.01 g) available and tared | YES | PENDING |
| Digital caliper (0.01 mm) available | YES | PENDING |
| Oven (105 °C) available for media drying | YES | PENDING |
| Institutional media-handling sign-off obtained | YES | PENDING |
| Dust mask and nitrile gloves available | YES | PENDING |
| Air supply confirmed ≥5 kPa at 100 L/min without cycling | YES | PENDING |
| Session header template complete for Stage A run file | YES | PENDING |
| Stage A fixture values will be recorded before any packed-bed run | YES | PENDING |

---

## 13. Acceptance Criteria Table

| Requirement | Status |
|---|---|
| Empty-rig baseline measured (Stage A) | NOT MEASURED |
| 26 mm bed measured (Stage B) | NOT MEASURED |
| 52 mm bed measured (Stage C) | NOT MEASURED |
| 104 mm bed measured (Stage D, conditional) | NOT MEASURED |
| Three independent repacks per depth | NOT MEASURED |
| Raw dataset retained (no rows deleted) | NOT MEASURED |
| Fixture correction applied | NOT MEASURED |
| Replicate scatter (CV) reported | NOT MEASURED |
| Pressure-drop curves generated | NOT MEASURED |
| Darcy coefficient `a` fitted from measurements | NOT MEASURED |
| Forchheimer coefficient `b` fitted from measurements | NOT MEASURED |
| Fit residuals checked (≤15%) | NOT MEASURED |
| Data validity classified per Section 10 | NOT MEASURED |
| OpenFOAM translation documented | DONE (values pending) |
| CFD case modified | MUST REMAIN NO — not done |
| HCHO introduced | MUST REMAIN NO — not done |

---

## 14. Phase 17A Decision

**PHASE 17A STATUS: BLOCKED — HARDWARE NOT YET AVAILABLE**

| Decision field | Value |
|---|---|
| Measured empty-column fixture loss | NOT MEASURED |
| Measured 26 mm bed result | NOT MEASURED |
| Measured 52 mm bed result | NOT MEASURED |
| Measured 104 mm bed result | NOT MEASURED |
| Darcy coefficient `a` | NOT MEASURED |
| Forchheimer coefficient `b` | NOT MEASURED |
| Coefficient validity range | NOT MEASURED |
| Primary uncertainty | NOT ASSESSED |
| Next phase | Execute procurement per Phase 16 plan; return to Phase 17A once rig is assembled and media is in hand |

---

## 15. How to Resume This Phase

1. Complete all items in the Pre-Conditions table (Section 1) and Final Checklist (Section 12).
2. Run Stage A (empty column). Populate `RAW_DATA.csv` with the Stage A rows.
3. Run Stage B, C, D. Add rows to the same CSV.
4. Run the analysis script:
   ```
   python scripts/analysis/phase17a_analysis.py \
       --csv results/PRESSURE_DROP_PHASE17A/RAW_DATA.csv \
       --out results/PRESSURE_DROP_PHASE17A/
   ```
5. Review `DARCY_FORCHHEIMER_FIT.json` and the generated plots.
6. Update the tables in Sections 4–13 of this document with the measured values.
7. Update `docs/PHASE17A_PRESSURE_DROP_RESULTS.md` status from BLOCKED to COMPLETE or PARTIAL.
8. Update `README.md` and `memory/project_status.md`.

---

*See also: `docs/PHASE16_CLEAN_AIR_TEST_PROTOCOL.md` for the full stage procedure; `docs/PHASE16_PROCUREMENT_PLAN.md` for the build order; `results/PRESSURE_DROP_PHASE17A/PRESSURE_DROP_ANALYSIS.md` for analysis method details.*
