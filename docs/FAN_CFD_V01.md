# CFD V01_fan — Fan-driven flow, placeholder pressure rise

> HISTORICAL / SUPERSEDED in Phase 7. The unrun 300 Pa placeholder is archived under `cfd/V01_fan/archive_placeholder/`. The active V01 now uses the actual KVO 250 six-point curve; see `docs/CFD_V01_FAN.md` and `results/CFD_V01_FAN_RESULTS.md`. Statements below about unavailable fan data and a future V02 describe the older setup, not current status.

## Objective

SIMULATION — V01_fan. Demonstrate a pressure-driven CFD case representing a fan system with a PLACEHOLDER total pressure rise. This is not a fan selection, a fan performance prediction, an operating point calculation, or a filtration validation.

No fan exists in the domain. No filter, particles, water, solar, sensors, or external wind is modelled. The geometry is the same empty tower as V00.

## What V01_fan changes relative to V00

V00 used a fixed inlet velocity of 1 m/s (Q = 1,512 m³/h) as a CFD convenience placeholder. That imposed a specific flow rate regardless of what any real fan could deliver. V01_fan replaces that with a pressure-driven inlet boundary condition:

- AIR_INLET: `totalPressure` with p0 = 250 m²/s² (kinematic) = 300 Pa physical (PLACEHOLDER)
- AIR_OUTLET: `fixedValue p = 0` (reference gauge pressure, unchanged)
- AIR_INLET U: `pressureInletOutletVelocity` (magnitude derived from pressure field)

The solver finds the velocity and pressure field that satisfies continuity and momentum given the imposed total pressure difference. The resulting flow rate Q is determined by the intersection of the imposed total pressure with the empty-tower system resistance — it is not specified a priori.

## Why this is still a placeholder

**Reason 1 — No real fan curve.** No fan product has been selected. No manufacturer datasheet has been obtained. The 300 Pa placeholder was chosen as the midpoint of the indicative system resistance screening range (250–700 Pa, see `docs/PRESSURE_DROP_BUDGET.md`). It does not correspond to any real fan.

**Reason 2 — Flat pressure line vs. real fan curve.** The `totalPressure` BC imposes the same ΔP regardless of flow rate. Real fans deliver less ΔP at higher Q (the fan curve falls from left to right). The V01_fan BC is equivalent to an infinitely stiff pressure source — a conservative overestimate of what any real fan provides at high Q. The true operating point (where a real fan curve crosses the system curve) can only be found with a multi-point fan curve and the fan baffle BC.

**Reason 3 — No filter stages.** Filter pressure drops (prefilter, HEPA, biochar) are entirely unknown and not modelled. Real operating Q through a complete filtration system will be substantially lower than V01_fan predicts.

**Reason 4 — Same geometry limitation.** The empty-tower geometry's convergence problem (quasi-periodic recirculation at 90° turns) persists. V01_fan is subject to the same non-convergence risk as V00.

## Physical model

Identical to V00:
- Constant-property isothermal air: nu = 1.5e-5 m²/s, rho = 1.20 kg/m³
- Incompressible, gauge kinematic pressure
- Standard k-epsilon RANS with smooth-wall functions
- Turbulence inlet: I = 5%, L = 0.07 × 0.6462 m (same ASSUMPTION as V00)
- SIMPLEC solver (consistent yes), inherited fvSolution from V00 best settings

## Fan representation method

V01_fan uses the **totalPressure inlet BC** approach:

The `totalPressure` BC sets p_total = p + 0.5|U|² = p0 at the inlet patch. With the outlet at p = 0 gauge, the total pressure difference across the domain is p0 = 250 m²/s². At the inlet face, the static pressure is p0 − 0.5|U_inlet|². The solver iterates to find U_inlet consistent with the continuity equation and the pressure field.

This is appropriate for a pressure-driven flow demonstration. For a true fan-system operating point:

1. Obtain a real fan curve (at least 5 ΔP vs. Q points).
2. Create an internal baffle at the fan location using `createBaffles`.
3. Apply the `fan` BC to the baffle pair with the curve table.
4. The solver then finds the unique Q where fan ΔP(Q) = system ΔP(Q).

See `cfd/V01_fan/constant/fanProperties` for the fan curve table format.

## Placeholder value justification

| Parameter | Value | Basis |
|---|---|---|
| Fan ΔP (Pa) | 300 Pa PLACEHOLDER | Midpoint of 250–700 Pa screening range |
| Screening range basis | Empty-tower V00 result (~33 Pa) + literature HEPA ΔP (150–250 Pa) | See PRESSURE_DROP_BUDGET.md |
| Kinematic p0 (m²/s²) | 300 / 1.20 = 250 | rho = 1.20 kg/m³ |
| Real fan source | NONE | No datasheet obtained |

## Solver and convergence plan

Same as V00: 3,000 initial iterations, SIMPLEC, writing every 250 iterations. If residuals stall above criteria, document the achieved level and mass imbalance. The same non-convergence risk exists due to the geometry. Do not restart from scratch if stalled; document and proceed.

## Results

See `results/CFD_V01_FAN_RESULTS.md`. Status: NOT YET RUN as of 2026-09-05.

## Next steps after running V01_fan

1. Obtain complete fan curve data for at least one real candidate (see `data/fans/README.md`).
2. Determine at least one filter-stage ΔP (prefilter or HEPA) from a specific product datasheet.
3. Update `docs/PRESSURE_DROP_BUDGET.md` with real values.
4. Run V02_fan with the `fan` baffle BC and a real fan curve to find the actual operating point.
5. Phase 7 (filtration stages as porous media) can only begin after V02_fan establishes a physically justified Q.

## Software source

OpenFOAM Foundation 14, `foamRun` with `incompressibleFluid`, same installation as V00. Run using `scripts/simulation/run_cfd_v01_fan.sh`.

---

Last updated: 2026-09-05.
