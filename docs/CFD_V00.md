# CFD V00 — Empty Concept A baseline

## Objective

SIMULATION — V00. Determine baseline airflow behaviour through the EMPTY tower. This is not a purification test or a product validation. No fan, filter, porous medium, HEPA, biochar, water, particles, solar, batteries, sensors, outdoor wind, or external dispersion is modelled.

## Geometry and workflow

Source: `cad/parametric/AQI_Tower_ConceptA_V00.FCStd`, generated in Phase 4 by `scripts/geometry/create_conceptA_v00.py`. All dimensions remain MODELLING PLACEHOLDERS — NOT PRODUCT REQUIREMENTS.

The preparation script opens the actual native file with FreeCAD, uses its CFDRegion metadata, verifies each fluid shape is exactly an axis-aligned box, checks zero volumetric overlap, and boolean-fuses the ten regions to require one valid connected solid. The reference TowerEnvelope is excluded. Its SHA-256, bounding boxes, boundary areas, volume and mesh counts are recorded in `cfd/V00/geometry_audit.json`.

The exact union is partitioned at every box coordinate into conformal rectangular blocks. Shared vertices and matching subdivisions make internal interfaces ordinary interior mesh faces, not walls. `blockMesh` generates hexahedra with a maximum edge of 20 mm (some shorter edges at CAD interfaces). This preserves the actual stepped CAD without a lossy STL or duplicate STEP file. The preparation script deliberately rejects non-box future CAD; it must not silently approximate new geometry by bounds.

All ten names are retained as cell zones: AIR_INLET, DIRTY_PLENUM, STAGE_01, INTERSTAGE_01, STAGE_02, INTERSTAGE_02, STAGE_03, CLEAN_PLENUM, CLEAN_RISER, AIR_OUTLET. They all contain the same air; zone labels do not apply physical resistance. Only AIR_INLET, AIR_OUTLET and WALLS are boundary patches.

Coordinates: X follows the lower cross-flow path, Y spans width, Z points upward. CAD millimetres are converted to metres once in blockMesh. All exposed surfaces except the outer inlet/outlet faces are assumed sealed, stationary walls. No leakage or physical wall thickness is modelled. The riser overlaps the lower clean plenum only over part of its footprint and has a cap above the outlet; these are retained, not redesigned.

## Fluid

ASSUMPTION: constant-property, isothermal air near room temperature and atmospheric pressure. Kinematic viscosity nu = 1.50e-5 m²/s; reference density rho = 1.20 kg/m³, giving dynamic viscosity mu = 1.80e-5 Pa s. These are rounded conventional engineering approximations, not measurements of the site. Density is used to convert incompressible kinematic pressure p (m²/s²) to Pa and volume flow to mass flow. Temperature, humidity, buoyancy and gravity/hydrostatic pressure are not solved. Pressure is gauge flow-induced pressure relative to the outlet, not atmospheric absolute pressure.

## PLACEHOLDER CFD FLOW

ASSUMPTION: uniform inlet velocity U = (1, 0, 0) m/s. For the CAD inlet area 0.42 m² this imposes Q = 0.42 m³/s = 1512 m³/h. This normalized input is convenient for checking a workflow and observing turning/contraction effects. It is NOT a product requirement, fan prediction, rated flow, CADR or approved target. The future fan phase must replace the imposed-flow assumption with sourced fan performance data and a justified operating point.

## Flow regime

The 0.6 m × 0.7 m inlet gives hydraulic diameter 4A/perimeter = 0.6462 m. Re = U Dh/nu ≈ 43,100, so a turbulent baseline is reasonable for this placeholder and the sharp bends. The actual regime remains UNKNOWN until a real operating flow and inlet conditions exist. Low-speed incompressible flow is appropriate; anticipated velocities of a few m/s are far below sonic speed. Check actual maximum speed after running.

## Solver choice

OpenFOAM Foundation 14, `foamRun` with the `incompressibleFluid` module and `steadyState` time discretization (steady pressure/velocity iteration, the modern SIMPLE-style workflow). No transient, compressible, thermal or multiphase model is justified in V00. Iteration numbers are not elapsed physical seconds.

## Turbulence model

Standard k-epsilon RANS with smooth-wall functions: a simple, established two-equation baseline for turbulent internal flow. ASSUMPTIONS: inlet turbulence intensity 5%, length scale 0.07 Dh; k = 1.5 (I U)² = 0.00375 m²/s² and epsilon = Cmu^(3/4) k^(3/2)/L with Cmu = 0.09. They are not measured turbulence conditions. Backflow at the outlet uses these same temporary turbulence values.

Limitations: equilibrium wall functions and standard k-epsilon can be inaccurate in strong separation and adverse pressure gradients. This modest first mesh is not a boundary-layer study; report y-plus and flag cells outside a conventional log-layer range. Steady RANS cannot resolve fluctuating vortices or prove the physical flow is steady. No mesh, turbulence, inlet-profile or outlet-location independence is claimed.

## Boundary conditions

| Patch | Velocity | Kinematic pressure | Turbulence |
| --- | --- | --- | --- |
| AIR_INLET, outer X-min face | Fixed (1 0 0) m/s — PLACEHOLDER CFD FLOW | zeroGradient | Fixed k and epsilon as above |
| AIR_OUTLET, outer X-max face | pressureInletOutletVelocity; permits backflow | Fixed 0 m²/s² gauge | inletOutlet k/epsilon with placeholder backflow values |
| WALLS, remaining external union faces | noSlip | zeroGradient | kqRWallFunction, epsilonWallFunction, nutkWallFunction |

The inlet velocity supplies the flow mathematically; no fan exists in the domain. A zero outlet gauge pressure is a reference/ideal discharge condition, not an external-environment calculation. Wall nut uses a smooth-wall function and patch nut is calculated elsewhere.

## Mesh and convergence plan (recorded before the first run)

Run `blockMesh`, then `checkMesh -allTopology -allGeometry`; require one connected mesh, positive volumes, correct boundary areas, valid zone coverage, and no failed checks. Record cell count, skewness, non-orthogonality, aspect ratio and total volume. No mesh-independence claim.

Use bounded convective schemes and under-relaxation. Maximum initial budget: 3000 iterations, writing every 250 iterations and on exit. Requested initial-residual criteria: p < 1e-5 and each velocity component, k and epsilon < 1e-6. Also require inlet/outlet volume imbalance < 0.1% of imposed inlet flow and stable monitored pressure/flow. A solver stopping successfully is not sufficient by itself: inspect residual histories and late-iteration behaviour. If criteria fail, report nonconvergence and retain the evidence.

## Results and quality review plan

Read the actual final fields with ParaView. Integrate patch phi for conservative inlet/outlet volume flow; convert to mass using rho. Report cell-centre speed min/max and volume-weighted mean (wall boundary speed is separately zero), pressure in Pa, area-weighted section averages and normal velocity. Inspect a central Y plane, streamlines, reversed flow, slow regions and fast contractions. Static-pressure difference is not identical to irreversible total-pressure loss when inlet/outlet speeds differ. Preserve this distinction.

Check domain connectivity, CAD/mesh volume, all ten empty cell zones, patch orientation/area, metre units, flow direction, mass closure, residual convergence, and wall-function limitations independently of plotting. Store logs and numerical summaries with the case; report results in `results/CFD_V00_RESULTS.md`. Images must say SIMULATION — V00 and must not imply filtration validation.

## Software source

Official installation instructions: [OpenFOAM Foundation 14 on Ubuntu](https://openfoam.org/download/14-ubuntu/). The Ubuntu Noble package is compatible with Ubuntu 24.04. The installed `incompressibleFluid/pitzDailySteady` tutorial supplies version-matched dictionary conventions, not geometry or boundary values for this tower.

---

## Execution record (Phase 5, 2026-09-05)

Three solver runs were conducted; no run met all documented convergence criteria.

### Run 1 — Original settings (iterations 1–3000)

Settings: SIMPLEC (`consistent yes`), all equation relaxation 0.8, no p field relaxation. The pressure residual stalled at ~1.3–1.7 × 10⁻⁴ from approximately iteration 300 onward, exhibiting a sustained period-2 oscillation (pressure alternating high–low each iteration). Velocity residuals stalled at ~1.5–2.2 × 10⁻⁴. Mass balance was excellent (0.002% imbalance). k bounding occurred only in the first 5 iterations (normal start-up). No divergence.

Root cause: Equation relaxation of 0.8 for all fields with no explicit pressure field damping produced pressure-velocity coupling overshoot in the presence of strong separation at the multiple 90° turns.

### Run 2 — SIMPLEC with p field relaxation (iterations 3001–6000)

Change: Added `fields { p 0.3; }` relaxation; reduced U equation relaxation 0.8 → 0.7 and k/epsilon 0.8 → 0.5. Continued from iteration 3000.

Result: Pressure residual improved substantially (~3.5× lower), settling at ~3.0–3.8 × 10⁻⁵. Velocity residuals dropped to ~2–5 × 10⁻⁶. k and epsilon converged fully. A period-3 oscillation in p/U residuals persisted. This run produced the best achieved solution and is used for result extraction (timestep 6000 fields).

### Run 3 — Classic SIMPLE with tighter p relaxation (iterations 6001–9000)

Change: Switched from SIMPLEC (`consistent yes`) to standard SIMPLE (`consistent no`); changed p field relaxation to 0.2.

Result: Pressure residual worsened to ~9.7–14 × 10⁻⁵ (period-3 oscillation, higher than SIMPLEC). Classic SIMPLE performed worse for this geometry. Fields from timestep 6000 (Run 2) were retained as the reference.

### Convergence conclusion

The V00 case is **PARTIAL — NON-CONVERGED**. The persistent oscillatory residual stall is attributed to quasi-periodic recirculation at the 90° turns in the multi-bend geometry, which a steady-state RANS SIMPLE solver cannot resolve to a fixed point. The geometry, mesh, and physical model are otherwise sound. Full details are in `results/CFD_V00_RESULTS.md`.

Potential remediation for future work: transient RANS (PISO), coarser convergence criteria with documented justification, geometry guide-vane modification to reduce turning separation, or a finer mesh with y+ below 30 everywhere and enhanced wall functions.
