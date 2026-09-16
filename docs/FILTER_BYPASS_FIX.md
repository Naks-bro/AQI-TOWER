# Filter Bypass Fix — AQI Tower Phase 10B

**PHASE 10B — BYPASS SEALED AND VERIFIED**  
**CASE_M_SEALED — 5000 iterations — GEO_C geometry — KVO 250 fan curve**  
**SIMULATION — PARTIAL NON-CONVERGED (same RANS oscillatory limit as all prior cases)**

Last updated: 2026-09-06 (Phase 10B).

---

## What Was Fixed

Phase 10A identified that 45% of system airflow (in CASE_M) bypassed the HEPA filter through an unintended open connection at the dirty-plenum/clean-riser junction (z = 0.850 m, x = 0.260–0.305 m). This document records the fix, verification, and updated operating point.

---

## The Bypass Path (Phase 10A Summary)

The GEO_C geometry creates an overlap zone at z = 0.850 m:

| Region | X range | Z range | Note |
|--------|---------|---------|------|
| INTERSTAGE_02 (dirty) | 0.250–0.290 m | < 0.850 m | dirty-side horizontal duct |
| STAGE_03 dirty side | 0.290–0.305 m | < 0.850 m | dirty side of filter mount |
| CLEAN_RISER | 0.260–0.690 m | > 0.850 m | vertical riser, inner wall at x = 0.260 m |

In the overlap zone x = 0.260–0.305 m, dirty-plenum cells (z < 0.850 m) faced CLEAN_RISER cells (z > 0.850 m) through open internal mesh faces at z = 0.850 m. No wall or baffle existed at this interface. The filter at x = 0.305 m was correctly implemented and had no gaps.

**Bypass path:** dirty plenum (x = 0.260–0.305, z < 0.850) → open horizontal face at z = 0.850 → CLEAN_RISER (x = 0.260–0.305, z > 0.850), bypassing the filter entirely.

---

## The Fix

A `bypassSeal` wall baffle was added to `system/createBafflesDict` using the OpenFOAM `plate` surface type:

```
origin (0.260 0.150 0.850)
span   (0.045 0.500 0.0)
```

This creates two wall patches (`BYPASS_SEAL_DIRTY` and `BYPASS_SEAL_CLEAN`) covering the 75 internal faces at the z = 0.850 m interface in the overlap zone. The baffle is a horizontal plate identical in concept to the sheet-metal cap that would seal this gap in physical fabrication.

### What was NOT changed

- Filter resistance, fan curve, turbulence model, solver settings — unchanged
- CASE_M is preserved unmodified
- CASE_M_SEALED is a new directory, created from CASE_M by `scripts/simulation/prepare_case_m_sealed.py`
- blockMeshDict — unchanged; same 67,838-cell mesh
- The porous-baffle relaxation is 0.005 from the start (CASE_M required a multi-phase restart; CASE_M_SEALED starts tight)

### Implementation details

| Item | Value |
|------|-------|
| Case source | `cfd/FILTER_H13/CASE_M` (copied, not modified) |
| Case destination | `cfd/FILTER_H13/CASE_M_SEALED` |
| Baffle type | `plate` (OpenFOAM createBaffles surface type) |
| Plate origin | (0.260, 0.150, 0.850) m |
| Plate span | (0.045, 0.500, 0.0) m |
| Plate area | 0.045 × 0.500 = 0.0225 m² |
| Faces converted | 75 (BYPASS_SEAL_DIRTY + BYPASS_SEAL_CLEAN) |
| Filter faces | 961 (unchanged, FILTER_UPSTREAM + FILTER_DOWNSTREAM) |
| porous-baffle relaxation | 0.005 (from iteration 1) |
| endTime | 5000 |

---

## CFD Run: CASE_M_SEALED

### Pre-run checks

| Step | Result |
|------|--------|
| blockMesh | OK — 67,838 cells, identical mesh to CASE_M |
| checkMesh | OK — max non-orthogonality 0°, max skewness 3×10⁻¹³ |
| createBaffles | OK — 961 filter + 260 frame + 75 bypass-seal faces converted |

### Solver run

- Solver: `foamRun`, `incompressibleFluid`, steady RANS SIMPLEC, k-epsilon
- Fan curve: KVO 250 6-point codedFixedValue BC at AIR_OUTLET (unchanged)
- Convergence: PARTIAL NON-CONVERGED (same oscillatory RANS limit as all prior GEO_C cases)
- endTime reached: 5000 iterations

---

## Results: Before vs After

| Quantity | CASE_M (unsealed) | CASE_M_SEALED | Change |
|----------|------------------:|--------------|--------|
| Total Q (m³/h) | 1412 | **1332** | −80 m³/h (−5.7%) |
| Q through filter (m³/h) | 776 | **1332** | +557 m³/h (+72%) |
| Bypass fraction | **45.1%** | **~0% (1×10⁻⁹)** | −45 ppt |
| Mean filter face velocity (m/s) | 0.613 | **1.053** | +0.44 m/s (+72%) |
| Filter ΔP (Pa) | 64.7 | **111.2** | +46.5 Pa (+72%) |
| Fan operating head (Pa) | 60.9 | **~115** | +54 Pa (+89%) |
| Fan op. head × filter area CoV | 0.100 | **0.100** | unchanged |

Fan head for CASE_M_SEALED estimated from KVO 250 curve at Q = 1332 m³/h: interpolated between (1200 m³/h, 205 Pa) and (1501 m³/h, 0 Pa) → ~115 Pa.

**Target verification: PASS — bypass fraction < 2% (actual: ~0%).**

### Model self-consistency check (CASE_M_SEALED)

| Check | Value |
|-------|-------|
| D × μ × v × L = 20,097,755 × 1.8×10⁻⁵ × 1.053 × 0.292 | 111.2 Pa |
| Measured filter ΔP (FILTER_UPSTREAM − FILTER_DOWNSTREAM) × ρ | 111.2 Pa |
| Agreement | ✓ |

Filter velocity CoV = 0.100 (unchanged from CASE_M) — the uniform velocity distribution across the filter face is preserved after sealing.

---

## Convergence Note

All GEO_C cases (Phases 7–10) reach the same oscillatory RANS limit at the 90° turn from horizontal duct to vertical riser. Residuals do not reach the convergence tolerances (p < 1×10⁻⁵, U/k/ε < 1×10⁻⁶) but integrated quantities (Q, filter ΔP, fan head) are stable to better than 1% over the final 500 iterations. Results are classified PARTIAL NON-CONVERGED throughout this project.

---

## Figures Generated (Phase 10B)

| File | Contents |
|------|----------|
| `results/FILTER_H13/filter_face_bypass_CASE_M_SEALED.png` | Filter face velocity distribution, sealed case |
| `results/FILTER_H13/bypass_streamlines_CASE_M_SEALED.png` | Streamlines at y ≈ 0.4 m mid-plane, sealed case |
| `results/FILTER_H13/bypass_before_after_CASE_M.png` | Side-by-side: CASE_M vs CASE_M_SEALED — filter face velocities + residual histories |
| `results/FILTER_H13/bypass_analysis_sealed.json` | Machine-readable sealed bypass data + comparison with CASE_M |

Generated by `scripts/simulation/phase10b_visualize.py`.

---

## What Is Still Unknown

1. **CADR estimate remains unavailable.** CASE_M_SEALED gives the corrected filter face velocity, but CADR requires: filter efficiency curve vs particle size (not available beyond H13 ≥ 99.95% for ≥ 0.3 µm), actual loaded-filter resistance, and a realistic particle source model.

2. **Physical fabrication gap.** In a real device, sealing the bypass requires a sheet-metal cap or gasket between the filter mounting frame (x = 0.305 m) and the inner riser wall (x = 0.260 m) at z = 0.850 m. This structural detail is not yet in the CAD model.

3. **CASE_L_SEALED / CASE_H_SEALED.** Only CASE_M was re-run with the seal. The sealed operating point for the L and H resistance scenarios is not yet computed. Given that the bypass path is fully blocked, the sealed L/H results will converge to Q_total / FILTER_AREA ≈ similar face velocities to the sealed CASE_M, scaled by the fan curve response.

4. **Non-convergence root cause.** The oscillatory RANS limit at the 90° turn has not been resolved. This would require geometry smoothing (curved transition) or a different turbulence model. Out of scope for Phase 10B.

---

## Recommended Next Step

**Phase 11 — Post-processing and CADR framework.**

With the bypass sealed, CASE_M_SEALED provides a corrected airflow field. The next priorities are:

1. Obtain a full filter efficiency curve for the Freudenberg SF13-B at the operating face velocity.
2. Estimate a preliminary CADR from the corrected filter flow rate and the ≥ 99.95% H13 efficiency.
3. Evaluate prefilter (G4/M5) addition for loaded-filter lifetime extension, if a particulate loading model is pursued.
4. Add the bypass seal geometry to the FreeCAD model for fabrication documentation.
