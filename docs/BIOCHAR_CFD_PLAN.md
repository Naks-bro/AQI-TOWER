# AQI Tower Phase 13 — Future Biochar CFD Plan

**PLAN ONLY — NO CFD CASE CREATED OR RUN**  
**No porous resistance or adsorption coefficient is assumed**

> **Phase 14 update:** Formaldehyde (HCHO) is now the frozen target gas. Gas-phase adsorption CFD remains **BLOCKED** until the pressure-drop and breakthrough inputs specified in [`PHASE14_FORMALDEHYDE_TARGET.md`](PHASE14_FORMALDEHYDE_TARGET.md) are measured. The future minimum sequence is measured Darcy–Forchheimer resistance, passive-scalar transport without adsorption, then a finite-capacity empirical source/sink calibrated to replicated breakthrough data. A constant first-order sink may describe only a validated clean-bed/early-time regime and must not be used to predict saturation or bed life.

## Objective

Define how a future, exact carbon medium could be introduced into the AQI Tower airflow model after measured pressure-loss data exist. This plan does not select final geometry, bed depth, placement, or adsorption performance.

## Recommended Representation

Use a **finite porous-media zone** for the carbon bed rather than treating it as another HEPA baffle. A packed bed has volume, residence time, distributed resistance, and potential flow maldistribution.

The coefficient framework must follow the measured pressure curve:

- **Darcy resistance:** use only if `ΔP/L` is linear with superficial velocity across the full operating range.
- **Darcy–Forchheimer resistance:** use if the measured curve requires both linear and quadratic velocity terms:

  `ΔP/L = a U_s + b U_s²`

- **Packed-bed/Ergun correlation:** use as a consistency check only when measured particle diameter, void fraction, particle shape/sphericity, fluid properties, and packing state exist. It is not a substitute for tower-range measurements.

No values for `a`, `b`, permeability, inertial resistance, void fraction, or adsorption kinetics are created in Phase 13.

## Model-Selection Gate

| Available evidence | Allowed future model | Not allowed |
|---|---|---|
| One pressure point | Screening bracket only; no calibrated nonlinear model | Claiming a unique Darcy/Forchheimer coefficient pair |
| Multi-point ΔP–velocity data, one bed depth | Empirical resistance fit at that packing/depth | Extrapolation beyond measured velocity |
| Multi-point data at several depths and packing states | Validated Darcy or Darcy–Forchheimer porous zone | Ignoring settling or fixture-loss uncertainty |
| Particle diameter + void fraction + shape + measured curve | Ergun comparison and coefficient cross-check | Using nominal mesh size as a spherical particle diameter without evidence |
| Breakthrough curves at matched conditions | Separate future species/adsorption model may be evaluated | Turning static adsorption capacity into a guaranteed removal boundary |

## Required Inputs

### Material and bed

- exact manufacturer/grade/lot;
- media distinction: GAC, pellet, raw biochar, activated biochar, or impregnated medium;
- particle-size distribution and particle shape;
- loose and settled bulk density;
- bed void fraction if measurable;
- selected bed depth, face area, mass, support screens, and packing procedure.

### Pressure loss

- empty-fixture-corrected ΔP at multiple superficial velocities;
- temperature, pressure, RH, and air properties;
- repeats and uncertainty;
- data covering the intended tower operating range;
- fitted equation plus validation residuals.

### Adsorption, only for a later transport model

- named gas or mixture;
- inlet concentration, temperature, and RH;
- upstream/downstream time series;
- flow, EBCT, bed geometry, and dry media mass;
- breakthrough and saturation definitions;
- repeatability, competitive adsorption, and regeneration history where applicable.

## Future Airflow-CFD Workflow

1. Preserve `CASE_M_SEALED` as the current HEPA-only reference.
2. Create a new future case rather than editing Phase 10B results.
3. Add a porous volume only after an approved bed envelope exists; do not alter CAD in this phase.
4. Map the measured `ΔP/L` relation to the OpenFOAM porous formulation with unit checks.
5. Run an isolated straight-bed validation case first and compare simulated pressure loss with held-out bench points.
6. Only after validation, add the porous zone to the tower and recompute the KVO 250 operating point.
7. Check mass balance, pressure drop by stage, face-velocity distribution, bypass, and fan-curve intersection.
8. Keep gas adsorption absent from the airflow model unless matched breakthrough/kinetic data support a separate species model.

## Adsorption-Modelling Boundary

A pressure-only porous zone answers the hydraulic question: how much resistance and flow redistribution does the bed create? It does **not** predict pollutant capture.

A later gas-transport model would need advection/diffusion plus a validated adsorption relation and possibly intraparticle mass-transfer kinetics. The correct formulation depends on the named gas, concentration range, humidity, temperature, and media chemistry. No universal “biochar efficiency” boundary condition is scientifically valid.

## Verification Requirements

- Pressure loss matches independent bench points within a predeclared tolerance.
- Resistance units and superficial/interstitial velocity definitions are documented.
- Simulated bed face velocity remains inside the measured range.
- Mesh sensitivity is checked across the porous region.
- Upstream and downstream pressure taps are located consistently with the experiment.
- The HEPA and biochar pressure drops remain separately reported.
- Any future adsorption model reproduces at least one held-out breakthrough curve before tower-level interpretation.

## Current Readiness

**BIOCHAR CFD READINESS: PARTIALLY READY.**

The OVC 4x8 manufacturer graph establishes that real pressure-loss data exist, but it is not tabulated and does not cover the existing 1.053 m/s HEPA-face velocity. The exact target gas, bed geometry, India-supplied media lot, bulk density/void fraction, tower-range pressure curve, and breakthrough data remain missing.

Therefore:

- no OpenFOAM files are created;
- no porous coefficients are estimated;
- no fan operating point is recalculated; and
- no adsorption or removal result is claimed.
