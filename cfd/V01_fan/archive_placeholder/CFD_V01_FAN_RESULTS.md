# CFD V01_fan Results — Fan-driven flow, placeholder pressure rise

## Status: NOT YET RUN — PLACEHOLDER DOCUMENT

This document is a placeholder. The V01_fan case has been prepared (case structure, boundary conditions, solver settings) but has not been executed. Results cannot be reported until the case is run and residuals are inspected.

## What this case will show (when run)

V01_fan imposes a PLACEHOLDER total pressure rise of 300 Pa (250 m²/s² kinematic) at AIR_INLET to represent an idealised fan. The outlet is at p = 0 gauge. The solver finds the velocity field and flow rate that satisfies continuity and momentum given that pressure boundary condition.

The expected outcome is a lower flow rate than V00 (which imposed Q = 1,512 m³/h unconditionally). At 300 Pa driving pressure against the empty-tower resistance that scaled as ~33 Pa at 1,512 m³/h, the approximate Q estimate by scaling:

  Q_V01 ≈ 1512 × sqrt(300 / 33) ≈ 1512 × 3.01 ≈ 4,560 m³/h (rough estimate)

Wait — this estimate is non-physical: if 33 Pa at 1,512 m³/h scales as Q², then 300 Pa would correspond to Q ≈ 1512 × sqrt(300/33) ≈ 4,560 m³/h. But that would require the fan to deliver 300 Pa at a higher flow rate than V00, which contradicts the fact that real fans deliver less ΔP at higher Q. This illustrates why a fixed totalPressure BC is not equivalent to a real fan curve — it can drive flows beyond the physical fan's capability.

**This estimate should not be treated as a design prediction.** It confirms only that the case structure is reasonable for demonstrating a pressure-driven flow. With a real fan curve (decreasing ΔP at higher Q), the actual operating Q would be much lower than this naive estimate.

If the empty-tower resistance at the real operating Q is R(Q) Pa, and the fan delivers exactly 300 Pa at that Q (which a real fan does not — it delivers less at higher Q), then R(Q) = 300 Pa gives Q as above. The totalPressure BC imposes 300 Pa regardless of Q, so the solver will find the Q where system resistance = 300 Pa at inlet.

Correct interpretation: V01_fan will show the empty-tower flow field when a driving head of 300 Pa is available. It is not a prediction of any real fan's operating point.

## Results table (to be filled after run)

| Metric | V00 (imposed 1 m/s) | V01_fan (placeholder 300 Pa) | Notes |
|---|---|---|---|
| Convergence status | PARTIAL — NON-CONVERGED | NOT YET RUN | |
| Best iteration | 6000 (SIMPLEC) | — | |
| p residual (best) | 3.8e-5 | — | Target 1e-5 |
| Ux residual (best) | 3.6e-6 | — | Target 1e-6 |
| Inlet Q (m³/h) | 1512 (imposed) | — | |
| Inlet mean velocity (m/s) | 1.0 (imposed) | — | |
| Static pressure at inlet (Pa) | ~33 Pa above outlet | — | |
| Max speed (m/s) | 6.65 | — | |
| Volume mean speed (m/s) | 1.84 | — | |
| Riser reverse-flow fraction | ~24% | — | |
| Mass imbalance (%) | 0.00045% | — | |
| Fan ΔP (Pa) | N/A (velocity BC) | 300 PLACEHOLDER | |

## Limitations that will remain after running V01_fan

1. **No real fan data.** The 300 Pa driving pressure is not derived from any fan product. Results cannot be used for fan selection.
2. **No filter stages.** The tower is still empty. Real operating Q will be substantially lower than V01_fan predicts because filter ΔP is not modelled.
3. **Fixed pressure BC vs. real fan curve.** The `totalPressure` BC imposes a flat operating line, not a real falling fan curve. True operating point analysis requires the `fan` baffle BC with a real curve.
4. **Same convergence limitation as V00.** The quasi-periodic recirculation at 90° turns will likely persist. Document residual level achieved.
5. **CADR is still UNKNOWN.** No filtration efficiency, particle capture, or air quality improvement is modelled or can be inferred.

## How to update this document

After running V01_fan:
1. Replace all "NOT YET RUN" and "—" entries with actual values from the solver log and postProcessing output.
2. Note the convergence status: CONVERGED / PARTIAL — NON-CONVERGED.
3. Compare with V00 results to identify the effect of pressure-driven vs. velocity-driven BCs.
4. If a real fan curve is then available, run V02_fan (with the fan baffle BC) and add a new results document.

Last updated: 2026-09-05.
