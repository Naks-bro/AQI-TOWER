# HEPA H13 Filter Resistance Study — Phase 9 + 10B Results

**SIMULATION — KVO 250 / GEO_C TOWER / HEPA H13 POROUS BAFFLE**  
**PARTIAL — NON-CONVERGED — ENGINEERING SENSITIVITY ONLY**  
**Filter ΔP model: APPROXIMATION FROM SINGLE MANUFACTURER DATA POINT**

Last updated: 2026-09-06 (Phase 10B — bypass sealed, CASE_M_SEALED added).

---

## Evidence boundary

This study uses three OpenFOAM simulations (CASE_L, CASE_M, CASE_H) on the GEO_C tower geometry with a porous-baffle representation of the Freudenberg SF13-B H13 HEPA filter. The porous model is calibrated to one manufacturer data point (300 Pa at 2.84 m/s face velocity, clean filter). All three cases are PARTIAL — NON-CONVERGED. Integrated quantities are stable; residuals plateau at ~10⁻⁵ (same limitation as V00/GEO_C).

The comparison baseline is the GEO_C empty-tower result (Phase 8, CONVERGED at iteration 926).

A filter bypass of 38–48% was discovered during results extraction (see §5). All filter ΔP values are for the 52–62% of flow that actually passes through the filter face.

No particles, filter loading, prefilter, biochar stage, wet scrubber, or thermal effects are included.

---

## 1. Primary results table

### 1.1 Fan operating point

| Metric | GEO_C empty | CASE_L | CASE_M | CASE_H |
|---|---:|---:|---:|---:|
| Total airflow Q (m³/h) | **1496.05** | **1434.5** | **1411.7** | **1401.7** |
| Total airflow Q (m³/s) | 0.4156 | 0.3985 | 0.3921 | 0.3894 |
| Fan-static-equiv. head (Pa) | **3.50** | **45.38** | **60.92** | **67.70** |
| Head increase from empty (Pa) | — | +41.88 | +57.42 | +64.20 |
| Head increase factor (×) | — | 13.0× | 17.4× | 19.3× |
| Q change from empty (%) | — | −4.1% | −5.6% | −6.3% |

GEO_C empty: Phase 8 CONVERGED result. CASE_L/M/H: Phase 9 PARTIAL — NON-CONVERGED; late-iteration stable values.

**Key result:** A single clean H13 HEPA filter increases the fan operating head by 13–19× relative to the empty tower. Airflow decreases by only 4–6% because the KVO 250 fan curve is very flat near free-delivery — the fan absorbs the large resistance increase with little Q reduction.

### 1.2 Filter face conditions

| Metric | CASE_L | CASE_M | CASE_H |
|---|---:|---:|---:|
| Flow through filter face (m³/s) | 0.2470 | 0.2155 | 0.2026 |
| Flow through filter face (m³/h) | 889.2 | 775.8 | 729.4 |
| Filter face velocity (m/s) | 0.702 | 0.613 | 0.576 |
| Filter face ΔP (Pa) | 47.1 | 64.73 | 72.5 |
| Model check: slope × v_face (Pa) | 67.07 × 0.702 = 47.1 ✓ | 105.63 × 0.613 = 64.7 ✓ | 125.75 × 0.576 = 72.4 ✓ |

Filter face ΔP is the local pressure drop across the active filter face for the air that passes through it. It is computed from the kinematic pressure difference (FILTER_UPSTREAM − FILTER_DOWNSTREAM) × ρ.

### 1.3 Resistance scenario definitions

| Case | Scenario | D (m⁻²) | slope (Pa·s/m) | Model ΔP at 1.19 m/s |
|---|---|---:|---:|---:|
| CASE_L | Lower bracket edge | 12,760,480 | 67.07 | ~80 Pa |
| CASE_M | Single-point calibrated | 20,097,755 | 105.63 | ~126 Pa |
| CASE_H | Upper bracket edge | 23,925,899 | 125.75 | ~150 Pa |

Reference face velocity 1.19 m/s = Q(1512 m³/h) / A_face(0.352 m²). Source bracket: Phase 6C/6D planning bracket.

---

## 2. Filter bypass — critical finding

| Case | Total Q (m³/s) | Filter Q (m³/s) | Bypass Q (m³/s) | Bypass fraction |
|---|---:|---:|---:|---:|
| CASE_L | 0.3985 | 0.2470 | 0.1515 | **38%** |
| CASE_M | 0.3921 | 0.2155 | 0.1766 | **45%** |
| CASE_H | 0.3894 | 0.2026 | 0.1868 | **48%** |

38–48% of total airflow bypasses the filter face patch and is **not filtered**. The bypass fraction increases with filter resistance, confirming a real flow path around the filter rather than a numerical artefact.

The filter + frame baffles at x = 305 mm seal the y = 100–700 mm, z = 150–850 mm cross-section. The bypass path is associated with the flow volume above z = 850 mm (the CLEAN_RISER zone). The topology of connections between the dirty plenum and the riser above the filter plane requires geometry investigation before Phase 10 modelling.

**Design consequence:** In the current geometry representation, effective filtration treats only 52–62% of the total airflow. Actual CADR (Clean Air Delivery Rate) and filtration efficiency cannot be estimated from these results without resolving the bypass path.

---

## 3. Convergence summary

| Case | Final iteration | Residuals met | Late-Q range | Status |
|---|---:|---|---:|---|
| GEO_C empty | 926 | Yes | < 0.001% | CONVERGED |
| CASE_L | 5000 | No (p~4e-5, U~1e-5) | Stable to 7 sig. fig. | PARTIAL — NON-CONVERGED |
| CASE_M | 5000 | No (p~4e-5, U~8-10e-6) | Stable to 7 sig. fig. | PARTIAL — NON-CONVERGED |
| CASE_H | 5000 | No (p~4e-5, U~1e-5) | Stable to 7 sig. fig. | PARTIAL — NON-CONVERGED |

Porous-baffle relaxation = 0.005 was required to achieve stable (though non-converged) filter ΔP behaviour. Higher values (0.2, 0.05) produced oscillatory filter ΔP with iteration. See `docs/FILTER_H13_MODEL.md` for details.

The non-convergence mechanism is identical to V00 and GEO_C: RANS cannot resolve the quasi-periodic recirculation at the 90° turn into the riser. Integrated quantities (Q, filter ΔP, fan head) are stable regardless of residual state; the comparison is valid for engineering sensitivity at this stage.

---

## 4. Model self-consistency check

The filter face ΔP should equal the Darcy model prediction at the computed face velocity:

| Case | D × μ × v × L (Pa) | Measured ΔP (Pa) | Agreement |
|---|---:|---:|---|
| CASE_L | 12,760,480 × 1.8e-5 × 0.702 × 0.292 = 47.1 | 47.1 | ✓ |
| CASE_M | 20,097,755 × 1.8e-5 × 0.613 × 0.292 = 64.8 | 64.73 | ✓ |
| CASE_H | 23,925,899 × 1.8e-5 × 0.576 × 0.292 = 72.4 | 72.5 | ✓ |

Model is self-consistent. The filter BC is correctly implemented.

---

## 5. H13 filter impact classification

### On the fan operating point
**IMPACT: HIGH**

A single clean H13 filter is the dominant system resistance in this tower:
- Fan head increases 13–19× from the empty-tower baseline (3.5 Pa → 45–68 Pa)
- Q decreases by only 4–6% because the KVO 250 operates near free delivery on a flat fan curve
- The operating head (45–68 Pa) remains well within the KVO 250 confirmed-curve range (confirmed points at Q=914 m³/h/388 Pa and Q=1501 m³/h/0 Pa)

Adding further filter stages (prefilter, biochar) will push head higher and Q lower. The KVO 250 has headroom before entering the graph-digitized section of its curve.

### On airflow (Q)
**IMPACT: MODERATE**

Q drops 4–6% from empty-tower (1496 → 1402–1435 m³/h). The fan's flat curve prevents large Q loss despite the large head increase.

### On filtration effectiveness
**IMPACT: CRITICAL CONCERN — BYPASS UNRESOLVED**

38–48% flow bypass means only 52–62% of air passes through the H13 filter in the current geometry. This is a critical design finding. No CADR estimate is possible until the bypass path is understood and either sealed or accepted as a design feature.

### On model confidence
**CONFIDENCE: LOW**

- Filter model rests on one manufacturer data point; linear extrapolation is unvalidated
- Non-converged RANS cannot fully resolve the turn/riser recirculation
- Filter bypass mechanism is not yet identified
- No particle, loading, or multi-stage effects included

Results are suitable for phase screening and identifying the dominant resistance but not for final design decisions.

---

## 6. Comparison with pressure-drop budget estimates

The Phase 6D/7 budget estimated Q ≈ 1300 m³/h at ΔP ≈ 133 Pa for KVO 250 + one clean HEPA (analytical intersection). Phase 9 CFD gives:

| Source | Q (m³/h) | Fan head (Pa) |
|---|---:|---:|
| Budget (Phase 6D analytical) | ~1300 | ~133 |
| CASE_M CFD (Phase 9) | 1412 | 61 |

The CFD gives higher Q and lower fan head than the analytical estimate. The main reasons:
1. The analytical budget assumed the full Q passes through the filter (no bypass). In CFD, 45% bypasses, so the effective system resistance is lower.
2. The analytical budget used the total Q through the filter face area. With bypass, the effective filter face velocity is lower (0.613 vs ~1.19 m/s), giving lower ΔP.

If the bypass were sealed (full flow through filter), the CFD result would move toward higher head and lower Q, likely closer to the budget estimate. The budget estimate remains the better conservative planning figure until bypass is resolved.

---

## 7. Phase 10B — Bypass sealed (CASE_M_SEALED)

Phase 10B added a wall baffle at z = 0.850 m, x = 0.260–0.305 m (the unintended bypass gap) and reran CASE_M with the sealed geometry. Full details in `docs/FILTER_BYPASS_FIX.md`.

### 7.1 Corrected CASE_M operating point

| Quantity | CASE_M (unsealed) | CASE_M_SEALED | Change |
|---|---:|---:|---|
| Total Q (m³/h) | 1412 | **1332** | −80 (−5.7%) |
| Q through filter (m³/h) | 776 | **1332** | +557 (+72%) |
| Bypass fraction | **45.1%** | **~0%** | −45 ppt |
| Filter face velocity (m/s) | 0.613 | **1.053** | +72% |
| Filter ΔP (Pa) | 64.7 | **111.2** | +46.5 Pa |
| Fan operating head (Pa) | ~61 | **~115** | +54 Pa (+89%) |
| Filter face CoV | 0.100 | 0.100 | unchanged |

**Verification (Phase 10B target): bypass < 2% — PASS (actual: ~0%, = 1×10⁻⁹).**

### 7.2 Updated comparison with pressure-drop budget

| Source | Q (m³/h) | Fan head (Pa) |
|---|---:|---:|
| Budget (Phase 6D analytical) | ~1300 | ~133 |
| CASE_M CFD unsealed (Phase 9) | 1412 | 61 |
| **CASE_M_SEALED CFD (Phase 10B)** | **1332** | **~115** |

The sealed CASE_M result is much closer to the Phase 6D budget (Q ≈ 1300 m³/h, ΔP ≈ 133 Pa). The remaining differences are:
- Bypass is now zero, so all flow goes through the filter
- Fan head ~115 Pa (sealed) vs budget ~133 Pa — the CFD gives a somewhat lower effective resistance, likely because the 1D analytical budget assumed uniform face velocity and did not account for viscous turn losses being taken by the fan
- Q is 1332 vs budget 1300 — within ±3%, consistent with analytical uncertainty

The sealed CFD result validates the Phase 6D budget as a reasonable conservative planning figure.

### 7.3 H13 impact classification — updated for sealed geometry

On the fan operating point: **HIGH** (confirmed). Fan head increases ~33× from empty tower (3.5 → 115 Pa). Q decreases 11% from empty (1496 → 1332 m³/h). The flat fan curve absorbs a large head increase but cannot fully maintain flow.

On filtration effectiveness: **RESOLVED**. With bypass sealed, effective filtration fraction = ~100% of Q_total. CADR estimation is now gated only by filter efficiency data (not yet available beyond H13 ≥ 99.95% at ≥ 0.3 µm).

Model confidence: **LOW** (unchanged). Single-point Darcy model; non-converged RANS. Suitable for phase screening.

---

## 8. Next steps (Phase 11+)

1. **CADR estimate.** Sealed CASE_M gives corrected filter face velocity (1.053 m/s). Need: full filter efficiency curve vs particle size for a preliminary CADR range.
2. **Add bypass seal to FreeCAD model.** Sheet-metal cap at z = 0.850 m between filter frame and inner riser wall (x = 0.260–0.305 m).
3. **CASE_L_SEALED / CASE_H_SEALED** (optional). Low-priority; sealed CASE_M is the primary result.

---

## 9. Files produced in Phase 9 + 10A + 10B

| File | Contents |
|---|---|
| `cfd/FILTER_H13/CASE_L/` | Full OpenFOAM case; 5000-iteration run; filter_implementation.json |
| `cfd/FILTER_H13/CASE_M/` | Full OpenFOAM case; 5000-iteration run; filter_implementation.json |
| `cfd/FILTER_H13/CASE_H/` | Full OpenFOAM case; 5000-iteration run; filter_implementation.json |
| `cfd/FILTER_H13/CASE_M_SEALED/` | Phase 10B bypass-sealed case; 5000-iteration run; all timesteps |
| `docs/FILTER_H13_MODEL.md` | Filter model methodology, Darcy derivation, bypass finding, convergence notes |
| `docs/FILTER_BYPASS_DIAGNOSIS.md` | Phase 10A bypass diagnosis: geometric mechanism, evidence, confidence |
| `docs/FILTER_BYPASS_FIX.md` | Phase 10B: fix implementation, verification, updated operating point |
| `results/FILTER_H13/bypass_analysis.json` | Phase 10A: bypass fractions for CASE_L/M/H |
| `results/FILTER_H13/bypass_analysis_sealed.json` | Phase 10B: bypass for CASE_M_SEALED + before/after comparison |
| `results/FILTER_H13/bypass_before_after_CASE_M.png` | Side-by-side: filter face velocities + residual histories |
| `results/FILTER_H13/filter_face_bypass_CASE_M_SEALED.png` | Filter face velocity distribution, sealed case |
| `results/FILTER_H13/bypass_streamlines_CASE_M_SEALED.png` | Streamlines at y ≈ 0.4 m mid-plane, sealed case |
| `scripts/simulation/prepare_case_m_sealed.py` | Setup script: copies and modifies CASE_M → CASE_M_SEALED |
| `scripts/simulation/phase10b_visualize.py` | Generates all Phase 10B figures and bypass_analysis_sealed.json |
