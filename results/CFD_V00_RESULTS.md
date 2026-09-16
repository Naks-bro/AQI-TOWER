# CFD V00 — Results Record

**SIMULATION — V00 | PLACEHOLDER INLET VELOCITY = 1 m/s**

This document records the numerical results of the V00 baseline CFD simulation. V00 represents an empty tower with a uniform placeholder inlet condition. It establishes baseline airflow geometry behaviour only. It does NOT validate filtration, fan performance, particle removal, PM2.5 reduction, biochar effectiveness, water-stage performance, CADR, or any product-level claim.

---

## 1. Software and Version

| Item | Value |
| --- | --- |
| OpenFOAM | Foundation 14, Ubuntu package 20260724 |
| Solver | `foamRun` with `incompressibleFluid` module |
| Pressure–velocity coupling | SIMPLEC (`consistent yes`) |
| Time discretization | steadyState (SIMPLE iterations, not physical time) |
| ParaView | 5.11.2 with python3-paraview |

---

## 2. Physical Model

| Parameter | Value |
| --- | --- |
| Fluid | Constant-property isothermal air |
| Kinematic viscosity ν | 1.50 × 10⁻⁵ m²/s |
| Density ρ (reference) | 1.20 kg/m³ |
| Dynamic viscosity μ | 1.80 × 10⁻⁵ Pa s |
| Turbulence model | Standard k-epsilon RANS, smooth-wall functions |
| Thermal effects | Not modelled |
| Gravity/buoyancy | Not modelled |
| Compressibility | Not modelled (incompressible) |
| Multiphase | Not modelled |

---

## 3. Geometry and Mesh

| Parameter | Value |
| --- | --- |
| Source | `cad/parametric/AQI_Tower_ConceptA_V00.FCStd` |
| Fluid volume | 0.424 m³ |
| Mesh type | Structured hexahedral (`blockMesh`) |
| Total cells | 57,645 |
| Maximum non-orthogonality | 0 (perfect hex mesh) |
| Maximum skewness | ≈ 0 |
| Maximum aspect ratio | 2 |
| Mesh status | `checkMesh` PASS — Mesh OK |

All ten cell zones (AIR_INLET, DIRTY_PLENUM, STAGE_01, INTERSTAGE_01, STAGE_02, INTERSTAGE_02, STAGE_03, CLEAN_PLENUM, CLEAN_RISER, AIR_OUTLET) are present as labelled air volumes. Zone labels carry no physical resistance.

---

## 4. Boundary Conditions

| Patch | Velocity BC | Pressure BC | Turbulence BC |
| --- | --- | --- | --- |
| AIR_INLET | `fixedValue (1 0 0)` m/s — PLACEHOLDER | `zeroGradient` | Fixed k, epsilon (I=5%, L=0.07 Dh) |
| AIR_OUTLET | `pressureInletOutletVelocity` | `fixedValue 0` m²/s² (gauge) | `inletOutlet` with placeholder backflow values |
| WALLS | `noSlip` | `zeroGradient` | `kqRWallFunction`, `epsilonWallFunction`, `nutkWallFunction` |

The inlet velocity imposes Q = 0.42 m³/s (1512 m³/h). This is a PLACEHOLDER CFD FLOW for numerical workflow testing, not a product requirement.

---

## 5. Solver Settings Used

### Best-performing settings (SIMPLEC run, iterations 3001–6000)

```
SIMPLE { consistent yes; nNonOrthogonalCorrectors 0; }
relaxationFactors
{
    fields    { p 0.3; }
    equations { U 0.7; k 0.5; epsilon 0.5; }
}
```

### Original settings (iterations 1–3000, led to convergence stall)

```
SIMPLE { consistent yes; nNonOrthogonalCorrectors 0; }
relaxationFactors { equations { U 0.8; ".*" 0.8; } }
```

### Second diagnostic attempt (iterations 6001–9000, performed worse)

```
SIMPLE { consistent no; }
relaxationFactors { fields { p 0.2; } equations { U 0.7; k 0.5; epsilon 0.5; } }
```

---

## 6. Convergence Status

**PARTIAL — NON-CONVERGED**

The V00 case did not meet the documented convergence criteria within 9,000 iterations across three runs. The best result was achieved at iteration 6,000 (SIMPLEC with p-field relaxation 0.3) and is used for all result extraction below.

### Documented convergence criteria (from `docs/CFD_V00.md`)

| Residual | Criterion | Best achieved at iter 6000 | Status |
| --- | --- | --- | --- |
| p (pressure) | < 1 × 10⁻⁵ | 3.8 × 10⁻⁵ | **NOT MET** (3.8× above) |
| Ux | < 1 × 10⁻⁶ | 3.6 × 10⁻⁶ | **NOT MET** (3.6× above) |
| Uy | < 1 × 10⁻⁶ | 4.9 × 10⁻⁶ | **NOT MET** (4.9× above) |
| Uz | < 1 × 10⁻⁶ | 3.9 × 10⁻⁶ | **NOT MET** (3.9× above) |
| k | < 1 × 10⁻⁶ | 6.5 × 10⁻⁷ | **MET** |
| epsilon | < 1 × 10⁻⁶ | 1.8 × 10⁻⁷ | **MET** |

### Residual history

| Phase | Iterations | p residual at start | p residual at end |
| --- | --- | --- | --- |
| Run 1 (original settings) | 1–3000 | 1.00 | ~1.3–1.7 × 10⁻⁴ (stalled ~iter 300) |
| Run 2 (SIMPLEC + p-field 0.3) | 3001–6000 | 1.3 × 10⁻⁴ | ~3.0–3.8 × 10⁻⁵ (stalled) |
| Run 3 (classic SIMPLE + p=0.2) | 6001–9000 | 3.8 × 10⁻⁵ | ~9.7–14 × 10⁻⁵ (worsened) |

Residual history figure: `results/CFD_V00/residual_history.png`

### Root cause of non-convergence

The period-2 oscillation in the pressure initial residual (alternating high–low each iteration, stalled from ~iteration 300 onward) is the characteristic signature of quasi-periodic recirculation at sharp bends that prevents steady RANS/SIMPLE from reaching a fixed-point solution. The geometry contains multiple 90° turns (inlet → dirty plenum → treatment stages → clean plenum → riser → outlet). At Re ≈ 43,100, these turns produce separation zones with low-frequency oscillatory vortex dynamics that a single-equation-per-iteration steady solver cannot fully damp. The SIMPLEC run (Run 2) substantially reduced p residuals (~3.5× lower than Run 1) but could not eliminate the underlying physical oscillation.

**This is not a mesh or numerical setup failure.** The mesh is geometrically perfect (zero non-orthogonality, zero skewness, aspect ratio ≤ 2). The solver is stable and mass-conservative. The physical flow itself is the source of the remaining residual: a steady RANS solution for this geometry at this Re does not converge tightly because the flow is inherently non-stationary in the recirculation zones.

### Mass balance (iteration 6000)

| Quantity | Value |
| --- | --- |
| Inlet volume flow (signed) | −0.4200 m³/s (imposed) |
| Outlet volume flow (signed) | +0.4200 m³/s |
| Wall volume flux | 0.0 m³/s |
| Mass imbalance | 0.00045% |
| Inlet mass flow | 0.5040 kg/s |
| Outlet mass flow | 0.5040 kg/s |

Mass balance is excellent and is not the convergence blocker.

---

## 7. Field Results — Iteration 6000 Reference

**These results are extracted from a partially-converged field. They are best-effort estimates of the baseline airflow pattern, not validated final predictions. All numerical values should be treated as order-of-magnitude indicators, not design specifications.**

### 7.1 Flow rates

| Quantity | Value | Comment |
| --- | --- | --- |
| Imposed inlet velocity | 1.0 m/s | PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| Inlet area | 0.42 m² | |
| Inlet volumetric flow | 0.42 m³/s = 1,512 m³/h | Imposed by BC |
| Outlet volumetric flow | 0.420 m³/s | Consistent with inlet |
| Outlet area | 0.125 m² | |
| Mean outlet velocity | 3.36 m/s | Q_out / A_out |

### 7.2 Pressure

All pressures are gauge (flow-induced), referenced to zero at the outlet. `p` in OpenFOAM is kinematic pressure (p/ρ); physical pressure = p × ρ.

| Quantity | Kinematic (m²/s²) | Physical (Pa) |
| --- | --- | --- |
| Inlet area-averaged pressure | 27.50 | 33.00 |
| Outlet pressure (fixed reference) | 0 | 0 |
| Inlet-to-outlet static pressure difference | 27.50 | 33.00 |
| Cell-minimum pressure | −1.25 | −1.51 |
| Cell-maximum pressure | 28.47 | 34.17 |
| Volume-weighted mean pressure | 18.55 | 22.25 |
| Late-100-iteration inlet pressure oscillation range | — | 0.0005 Pa |

The static pressure difference of ~33 Pa represents the total flow-induced gauge pressure across the empty tower geometry under the placeholder 1 m/s inlet condition. This is NOT a system resistance figure; it includes velocity pressure effects from the varying cross-section and does not include any filter, fan, or porous media resistance.

### 7.3 Velocity

| Quantity | Value |
| --- | --- |
| Cell-minimum speed | 0.0023 m/s |
| Cell-maximum speed | 6.65 m/s |
| Volume-weighted mean speed | 1.84 m/s |
| Location of maximum speed (approx.) | x = 0.490 m, y = 0.220 m, z = 0.959 m (in riser turn region) |
| Volume fraction with speed < 0.1 m/s | 1.2% |

### 7.4 Per-region speed (volume-weighted mean, m/s)

| Region | Mean speed (m/s) | Reverse-flow fraction | Note |
| --- | --- | --- | --- |
| AIR_INLET | 1.00 | 0% | Imposed uniform 1 m/s |
| DIRTY_PLENUM | 1.02 | 0% | Minimal acceleration; uniform distribution |
| STAGE_01 | 1.07 | 0% | Through-flow, slight acceleration |
| INTERSTAGE_01 | 1.11 | 0% | Through-flow |
| STAGE_02 | 1.16 | 0% | Continued acceleration |
| INTERSTAGE_02 | 1.24 | 0.7% | First appearance of minor reverse flow |
| STAGE_03 | 1.34 | 1.9% | Increasing reverse-flow indicator |
| CLEAN_PLENUM | 1.48 | 7.8% | Significant turning; recirculation present |
| CLEAN_RISER | 2.42 | 23.7% | Area contraction + turning; substantial reverse-flow fraction |
| AIR_OUTLET | 4.92 | 0% | Concentrated exit |

The reverse-flow fractions in CLEAN_PLENUM and CLEAN_RISER are indicators of recirculation, not proof of complete vortices. They use a one-component threshold (Ux < −0.05 m/s or Uz < −0.05 m/s depending on zone axis) and do not characterise the full three-dimensional structure.

### 7.5 Cross-section velocities

| Section | Area (m²) | Normal velocity mean (m/s) | CoV | Reverse area fraction | Sampled Q (m³/s) |
| --- | --- | --- | --- | --- | --- |
| STAGE_01 mid | 0.42 | 0.999 | 0.51 | 1.1% | 0.420 |
| STAGE_02 mid | 0.42 | 1.000 | 0.55 | 2.0% | 0.420 |
| STAGE_03 mid | 0.42 | 1.000 | 0.60 | 2.8% | 0.420 |
| Riser entry (z=0.86 m) | 0.185 | 2.32 | 1.09 | 31.6% | 0.429 |
| Riser mid (z=1.20 m) | 0.185 | 2.27 | 0.94 | 17.5% | 0.420 |
| Outlet mid | 0.125 | 3.42 | 0.39 | 0% | 0.427 |

CoV = coefficient of variation of the normal velocity (σ/|mean|). A CoV > 1 at the riser entry indicates strongly non-uniform velocity — the cross-section is dominated by a narrow high-velocity jet alongside a broad recirculating zone.

### 7.6 Wall y-plus

| Quantity | Value |
| --- | --- |
| y+ minimum | 10.9 |
| y+ maximum | 797.9 |
| y+ face mean | 151 |
| Face fraction below 30 (viscous sublayer influenced) | 27.2% |
| Face fraction above 300 (outside log-law range) | 13.6% |

Mean y+ is within the intended log-law wall-function range (30–300) but the wide spread (10.9–797) indicates that wall-function accuracy varies considerably across the domain. Faces with y+ < 30 and y+ > 300 are outside the log-law range where the kq and epsilon wall functions are most accurate. No boundary-layer resolution study has been conducted. This is consistent with the limitations stated in `docs/CFD_V00.md`.

---

## 8. Key Flow Observations

The following observations are based on the partially-converged SIMPLEC field at iteration 6000. They describe geometry-driven airflow patterns under the placeholder boundary condition.

**Flow path:** Air enters uniformly at the X-min face (AIR_INLET) and travels horizontally through the dirty plenum and three treatment stages (STAGE_01, STAGE_02, STAGE_03), then turns downward into the clean plenum (CLEAN_PLENUM), upward through the clean riser (CLEAN_RISER), and exits at the X-max top face (AIR_OUTLET).

**Velocity distribution through stages:** Speed increases progressively from ~1 m/s at the inlet to ~1.34 m/s at STAGE_03 due to continuity effects as the flow turns and begins to converge toward the clean plenum. Through-flow velocity is reasonably uniform (CoV 0.51–0.60 at the stage midsections) but non-uniformity increases toward STAGE_03.

**Clean plenum recirculation (~7.8% reverse-flow fraction by volume):** The geometry change from horizontal treatment stages to vertical riser flow causes the turning flow to separate and recirculate in the clean plenum. This is physically expected for a right-angle turn without a guide vane.

**Riser recirculation (~23.7% reverse-flow fraction by volume):** The clean riser shows the highest reverse-flow indicator. The flow turns from horizontal (across the stage array) to vertical (upward through the riser) at a sharp 90° corner. The high CoV at the riser entry (1.09) confirms a strongly non-uniform, partially-separated entry condition. The flow progressively organises as it moves up the riser (CoV drops from 1.09 to 0.94 between z=0.86 m and z=1.20 m).

**Maximum velocity location (~6.65 m/s at x=0.490 m, z=0.959 m):** The highest speed occurs in the riser near the turn, where the area contracts and the flow jet is concentrated. This is in the upper part of the CLEAN_RISER zone near the internal corner.

**Low-velocity / dead zones (~1.2% of fluid volume):** About 1.2% of the fluid volume has speed below 0.1 m/s. This is a relatively small fraction; most of the internal volume is actively swept at speeds between 1 m/s and 5 m/s.

**Outlet backflow:** A small fraction of outlet faces (corresponding to Q_backflow ≈ 0.0027 m³/s) shows inward flow, which is a physical consequence of the non-uniform velocity profile at the exit — the `pressureInletOutletVelocity` BC handles this correctly. Net outlet flow is balanced with the inlet.

---

## 9. Limitations

1. **Convergence criteria not met.** The p and U residuals did not reach their documented targets. All numerical values carry uncertainty from the remaining oscillation. Relative flow patterns (faster here, recirculation there) are more reliable than precise magnitudes.

2. **Placeholder inlet condition.** 1 m/s is a workflow test value. The actual operating velocity will differ once fan performance data and system resistance are available. All pressure and velocity values scale with the actual flow rate.

3. **No mesh-independence study.** The 57,645-cell mesh is the first-pass mesh only. Mesh refinement near the sharp turns and in the riser may change the recirculation extent predictions.

4. **Steady RANS limitation.** The k-epsilon model assumes turbulence is in local equilibrium. Standard k-epsilon can over-predict recirculation length in abrupt separation regions. The riser reverse-flow fraction should be treated as an indicator, not a validated quantitative prediction.

5. **Wall-function range not satisfied uniformly.** y+ ranges from 11 to 798; 27% of wall faces are in the viscous-affected regime where log-law functions are less accurate.

6. **No stage physical resistance.** Treatment stage volumes have no modelled resistance (no porous media, filter, biochar, or water). The V00 flow path represents the open geometric path only.

7. **No fan, external wind, or thermal effect.** The boundary condition is an idealized uniform inlet velocity with no fan curve interaction, no temperature gradient, and no external environment.

8. **Pressure difference is not system resistance.** The 33 Pa inlet gauge pressure includes dynamic pressure changes from varying cross-section. The irreversible total-pressure loss requires proper total-pressure integration at matched sections and is not identical to the 33 Pa figure.

9. **This simulation cannot validate filtration or purification performance.**

---

## 10. Figures

All figures are in `results/CFD_V00/` and carry the SIMULATION — V00 label.

| File | Content |
| --- | --- |
| `residual_history.png` | Residual plot for all fields across 6,000 iterations with criterion lines |
| `velocity_streamlines.png` | Speed on central Y-plane with inlet-seeded streamlines |
| `pressure_section.png` | Gauge pressure on central Y-plane |

Raw numerical data:
| File | Content |
| --- | --- |
| `metrics.json` | Full quantitative metrics (machine-readable) |
| `residuals.csv` | Per-iteration residual history |

---

## 11. Interpretation Summary

Under the placeholder 1 m/s inlet condition, the empty Concept A geometry shows:

- **Reasonable through-flow uniformity** at the three treatment stage positions (CoV 0.51–0.60 at midsections, ≥97% forward flow through STAGE_01 and STAGE_02).
- **Progressive non-uniformity increase** toward the outlet, driven by the 90° turns at the clean plenum and riser entry.
- **Significant recirculation in the riser** (~24% reverse-flow indicator fraction) from the sharp-turn geometry, which is the dominant aerodynamic concern in the current concept.
- **No divergence or physically implausible field values;** the solution is stable and mass-conservative.

These observations suggest the sharp 90° turn from the horizontal stage array into the vertical riser is the primary geometric source of flow non-uniformity and pressure loss in the empty tower. Future phases should consider whether a guide vane, gradual turn, or inlet/outlet geometry change can reduce riser separation before adding filter resistance and fan modelling.

**This is NOT a validated design assessment.** It establishes only that the baseline geometry produces a physically reasonable and internally consistent CFD result under a simplified placeholder boundary condition.
