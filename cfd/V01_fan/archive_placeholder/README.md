# CFD V01_fan — Fan-driven flow, placeholder pressure rise

## Status: CASE STRUCTURE READY — PLACEHOLDER ONLY — DO NOT INTERPRET AS REAL FAN RESULT

## Purpose

This case represents the first step toward fan-driven CFD. The V00 case imposed a fixed inlet velocity of 1 m/s (Q = 1,512 m³/h) as a CFD flow placeholder. V01_fan replaces that with a pressure-driven boundary condition that represents the fan as a total pressure rise at the inlet.

The fan ΔP value is a PLACEHOLDER (300 Pa / 250 m²/s² kinematic). No real fan has been selected. No real fan curve is available. The resulting flow rate from this case represents what an idealised 300 Pa fan would drive through the empty tower — it is still not a product prediction or CADR value.

## What changed from V00

| Feature | V00 | V01_fan |
|---|---|---|
| Inlet BC (p) | `zeroGradient` (p derived) | `totalPressure p0 = 250 m²/s²` (PLACEHOLDER) |
| Inlet BC (U) | `fixedValue (1 0 0)` | `pressureInletOutletVelocity` (derived from p) |
| Outlet BC (p) | `fixedValue 0` | `fixedValue 0` (unchanged) |
| Flow rate Q | Fixed 0.42 m³/s (1,512 m³/h) | Determined by fan ΔP vs system resistance |
| Fan model | None | Pressure-jump at inlet (PLACEHOLDER) |
| Geometry | Empty tower | Empty tower (unchanged) |
| Filters | None | None (still empty — filters NOT modelled) |

## Fan representation: totalPressure inlet BC

The `totalPressure` boundary condition at AIR_INLET sets the total (stagnation) kinematic pressure to p0. The velocity at the inlet is computed by the solver to satisfy continuity. The pressure difference between the inlet total pressure and the outlet static pressure (0 Pa gauge) equals the fan's total-to-static pressure rise.

This is the simplest physically meaningful fan representation for a pressure-driven internal flow case. It requires only a single pressure value, not a full fan curve. It is appropriate for a PLACEHOLDER run but not for final fan selection.

**Limitation:** A fixed p0 BC does not capture the fan curve shape (the relationship between delivered ΔP and Q). A real fan delivers less ΔP at higher Q and more at lower Q. The totalPressure BC imposes a fixed ΔP regardless of Q — it simulates a perfectly flat fan curve, which no real fan has. For a true fan-system operating point analysis, the `fan` baffle BC (with a multi-point fan curve table) must be used.

## Future: internal baffle fan BC

When a real fan curve is available, the preferred approach is:
1. Identify the mesh face location where the fan sits (e.g., between CLEAN_PLENUM and CLEAN_RISER for a pull-through arrangement).
2. Run `createBaffles` to split that interior face into two coupled patch faces.
3. Apply the `fan` BC to one patch with the actual fan curve table in SI units.
4. The solver then finds the true operating point where fan ΔP(Q) = system ΔP(Q).

See `constant/fanProperties` for the fan curve table format.

## Geometry

Identical to V00. Same `blockMeshDict`, same ten cell zones, same AIR_INLET / AIR_OUTLET / WALLS patches. No filter stages, no baffles, no added geometry. Run `blockMesh` in this case directory before `foamRun`.

## How to run (in WSL Ubuntu)

```bash
source /opt/openfoam14/etc/bashrc
cd /mnt/d/DUDE/AQI-TOWER/cfd/V01_fan
blockMesh > logs/blockMesh.log 2>&1
checkMesh -allTopology -allGeometry > logs/checkMesh.log 2>&1
foamRun > logs/foamRun.log 2>&1
```

Check `logs/foamRun.log` for residual history and mass imbalance before interpreting results.

## Convergence expectations

V01_fan uses the same SIMPLEC settings that gave the best V00 result. The same quasi-periodic residual oscillation at the 90° turns may persist — that is a physical characteristic of this geometry at turbulent Re, not a solver error. If p residual stalls above 1e-5, document the achieved level and the mass imbalance, and proceed to result extraction as was done for V00.

## Placeholder justification

The 300 Pa placeholder was chosen as the approximate midpoint of the indicative system resistance screening range (250–700 Pa at a real filtration operating point). It is not derived from any fan product data. The range itself is based on published HEPA filter literature values and the V00 empty-tower result — see `docs/PRESSURE_DROP_BUDGET.md` for the full derivation.

The case MUST be re-run with a real fan curve once one is sourced (see `data/fans/README.md`).

Last updated: 2026-09-05.
