# Phase 12B — Conservative Particle Tracking

**PHASE 12B — CONSERVATIVE PARTICLE TRACKING**  
**FILTER ARRIVAL ≠ FILTER CAPTURE**  
**Status: COMPLETE — audited existing run; airflow CFD and particle tracking were not rerun**

## Objective

Evaluate which injected particle paths reach the upstream face of the sealed H13 stage, contact a wall, or remain otherwise unresolved in the existing frozen airflow field. This is a flow-path screening study. It does not model HEPA capture and does not establish filtration efficiency, particle-removal performance, CADR, or AQI reduction.

## Airflow Field Used

- **DETECTED:** `cfd/FILTER_H13/CASE_M_SEALED`, timestep 5000, Phase 10B.
- **DETECTED:** steady RANS SIMPLEC velocity field with 67,838 cells.
- **DETECTED:** PARTIAL NON-CONVERGED; integrated quantities were previously reported as stable.
- **DETECTED:** Q = 1332.2 m³/h, mean filter-face velocity = 1.053 m/s, filter pressure drop = 111.2 Pa, and bypass fraction ≈ 0%.
- **VERIFIED:** the saved `5000/U` field exists; SHA-256 is `4C06764131005BDE4EE3C5E3CAB5F97AE94E8EB3FCC17BC6C63C04B2B6F3112A` at this audit.
- **FACT:** Phase 12B did not modify or rerun this airflow field.

## Particle Model

The implemented model is one-way coupled, non-reacting, and dilute: particles read the airflow but do not alter it. Particle positions are advanced with first-order Euler steps (`dt = 0.004 s`, maximum time `6.0 s`) using the nearest velocity-cell centre found by a KDTree.

The tracking implementation is an **equilibrium-slip approximation**:

`particle velocity = local frozen-air velocity + terminal-settling velocity in −z`

The terminal-settling velocity is based on Stokes relaxation time with a Cunningham slip correction. The code does not integrate a separate transient particle-momentum equation. This wording corrects the earlier broad “Stokes drag model” label; it does not change the calculation or its numerical results.

## Particle Sizes

| Particle diameter | Cunningham factor | Relaxation time | Terminal settling | Stokes number |
|---:|---:|---:|---:|---:|
| 0.3 µm | 1.568 | 0.523 µs | 0.00513 mm/s | 5.23 × 10⁻⁶ |
| 1 µm | 1.166 | 4.318 µs | 0.0424 mm/s | 4.32 × 10⁻⁵ |
| 2.5 µm | 1.066 | 24.684 µs | 0.242 mm/s | 2.47 × 10⁻⁴ |
| 10 µm | 1.017 | 376.516 µs | 3.694 mm/s | 3.77 × 10⁻³ |

All four Stokes numbers are much less than 1 for the documented characteristic velocity of 3.0 m/s and length of 0.30 m. The equilibrium-slip approximation therefore predicts close following of the mean airflow, with gravity providing the only size-dependent drift.

## Injection Method

- **DETECTED:** nominal injection plane `x = 0.010 m`, just inside the inlet region.
- **DETECTED:** uniform 18 × 18 candidate grid over `y = 0.08–0.82 m` and `z = 0.12–0.88 m`.
- **DETECTED:** candidates whose nearest cell centre was at least 0.014 m away were rejected.
- **DETECTED:** 224 of 324 candidates were retained for each particle size.
- **LIMITATION:** this is not a mass-flow-weighted inlet release. Its bias direction is UNKNOWN without a separate sensitivity calculation.

## Assumptions

- Frozen mean airflow; no transient air-field response.
- One-way dilute coupling; no particle feedback on air.
- Spherical particles with one assumed density, `1200 kg/m³`, for all sizes.
- Gravity is `9.81 m/s²` in the mesh `−z` direction.
- Cunningham-corrected Stokes terminal settling is superimposed on local air velocity.
- No turbulent dispersion, Brownian diffusion, agglomeration, electrostatics, hygroscopic growth, rebound, resuspension, or particle–particle interaction.
- Reaching the active filter gate is FILTER ARRIVAL, never assumed capture.

## Particle Accounting

For the required high-level accounting, filter-frame contacts are included in WALL DEPOSITION FRACTION. The original JSON keeps frame contacts and other wall contacts as separate subcategories.

| Size | FILTER ARRIVAL FRACTION | WALL DEPOSITION FRACTION | OUTLET ESCAPE FRACTION | Other fraction | Accounted / injected | Balance |
|---|---:|---:|---:|---:|---:|---:|
| 0.3 µm | 139/224 = 62.05% | 85/224 = 37.95% | 0/224 = 0% | 0/224 = 0% | 224/224 | 0 |
| 1 µm | 139/224 = 62.05% | 85/224 = 37.95% | 0/224 = 0% | 0/224 = 0% | 224/224 | 0 |
| 2.5 µm | 139/224 = 62.05% | 85/224 = 37.95% | 0/224 = 0% | 0/224 = 0% | 224/224 | 0 |
| 10 µm | 137/224 = 61.16% | 87/224 = 38.84% | 0/224 = 0% | 0/224 = 0% | 224/224 | 0 |

**VERIFIED:** integer conservation is exact for every size. The unrounded fractions sum to 1.0; any displayed percentage mismatch is rounding only.

Raw terminal subcategories:

| Size | Filter arrival | Filter-frame contact | Other-wall contact | Max-time / other |
|---|---:|---:|---:|---:|
| 0.3 µm | 139 | 14 | 71 | 0 |
| 1 µm | 139 | 14 | 71 | 0 |
| 2.5 µm | 139 | 14 | 71 | 0 |
| 10 µm | 137 | 17 | 70 | 0 |

## Filter Arrival Fraction

The highest FILTER ARRIVAL FRACTION is a three-way tie: 0.3, 1, and 2.5 µm each reach 139/224 (62.05%). The 10 µm class reaches 137/224 (61.16%). The two-particle difference is unresolved at the current seed-grid, timestep, interpolation, and wall-threshold resolution; it is not evidence of filter size selectivity.

## Wall Deposition

All sizes have substantial terminal wall contact in this model. The WALL DEPOSITION FRACTION, including the filter frame, is 37.95% for 0.3, 1, and 2.5 µm and 38.84% for 10 µm. These values are contact classifications, not removal efficiency. Sticking, rebound, and later resuspension are UNKNOWN.

## Outlet Escape

The derived OUTLET ESCAPE FRACTION is 0% for all four sizes. The script does not implement a separate far-outlet crossing event: in the sealed topology, a downstream path crosses the upstream filter-arrival gate first, and every injected particle reached one of the existing terminal classes. Therefore the 0% value is a topology/accounting result, not evidence that the HEPA captures arriving particles.

## Trajectory Findings

All four requested files already existed and were visually inspected, so they were not regenerated:

- `trajectory_0p3um.png`
- `trajectory_1um.png`
- `trajectory_2p5um.png`
- `trajectory_10um.png`

They are technical endpoint maps: the white curves are airflow streamlines, while coloured dots are tracked particle terminal positions in a mid-plane band. They do not contain saved full individual particle path histories. The maps show nearly identical outcome patterns for 0.3–2.5 µm and a two-particle shift from filter arrival to frame contact for 10 µm. `particle_summary.png` correctly labels the plotted values as particle arrival fractions rather than filter efficiencies.

## Physical Interpretation

1. **Which particle sizes most often reach the HEPA?** The 0.3, 1, and 2.5 µm classes tie at 62.05% FILTER ARRIVAL FRACTION; 10 µm is slightly lower at 61.16%.
2. **Which particle sizes deposit on walls?** All four. Total WALL DEPOSITION FRACTION is 37.95% for 0.3–2.5 µm and 38.84% for 10 µm when filter-frame contacts are included.
3. **Which particle sizes escape through the outlet?** None in the derived terminal accounting: OUTLET ESCAPE FRACTION is 0% for every size, with the outlet-classification limitation stated above.
4. **Does particle behaviour suggest an important flow-path problem?** It flags a substantial modelled wall/frame-contact pathway because roughly 38% do not reach the active filter gate. That is worth investigating, but its magnitude is not yet a verified design defect because wall contact is detected by a nearest-cell-distance proxy and the inlet release is coarse and not mass-flow-weighted. No open bypass-to-outlet path is indicated.
5. **Is the airflow field suitable for a future particle-capture study?** Yes for conservative screening and method development. A quantitative capture study should retain the sealed topology but address the partial flow-field convergence, inlet weighting, interpolation, wall interaction, turbulent dispersion, and product-specific η(d_p).

## Limitations

1. No product-specific η(d_p); no capture probability is applied.
2. The `1200 kg/m³` particle density is an assumption, not a measured universal PM density.
3. The equilibrium-slip method does not solve transient particle inertia.
4. The frozen RANS field is PARTIAL NON-CONVERGED and contains no transient turbulent fluctuations.
5. Nearest-neighbour velocity lookup and first-order Euler stepping introduce numerical discretization error.
6. The 0.014 m nearest-cell-distance threshold is only a wall-contact proxy, not geometric face intersection.
7. Uniform grid injection is not mass-flow-weighted; its bias is UNKNOWN.
8. With 224 retained seeds, one particle equals 0.446 percentage points; no seed-density or timestep sensitivity run was performed.
9. The model treats each terminal wall contact as deposition but does not simulate sticking, rebound, or resuspension.
10. OUTLET ESCAPE is inferred from event ordering and complete accounting rather than measured by a separate outlet-plane event.
11. Existing figures display airflow streamlines and terminal outcomes, not stored full particle histories.

## Future Integration of η(dp)

The machine-readable output already separates particle diameter and FILTER ARRIVAL FRACTION. It can later be paired with a verified product-specific efficiency function η(d_p) to evaluate capture among particles that arrive at the filter. No η(d_p) function is created, assumed, or applied in Phase 12B.
