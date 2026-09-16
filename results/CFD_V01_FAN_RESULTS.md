# V01 — KVO 250 fan / empty tower results

**SIMULATION — V01 / SYSTEMAIR KVO 250 / EMPTY TOWER**  
**GRAPH-DIGITIZED FAN CURVE — UNCERTAINTY APPLIES**  
**Status: ACTUAL CFD RUN COMPLETED — PARTIAL / NON-CONVERGED.**

## Objective

Find the operating flow of the supplied real KVO 250 characteristic coupled to the existing empty Concept A tower. This is a simplified numerical prediction, not a physical measurement or final purifier operating point. No filters or other Phase 8 physics were added.

## Fan

One Systemair KVO 250, article 2027, nominal 230 V / 50 Hz and 2480 rpm. Classification: **PROMISING WITH GEOMETRY ISSUES**, conditional on the simplified empty-tower assumptions. No final fan selected.

## Fan Curve Source

Input: `data/fans/systemair_KVO_250.json`, preserved unchanged. SHA-256:
`847274a70e6d1a56d4707186c6eb37792f96358bb481bad46a704c554de15c73`.

The project Phase 6D audit identifies a Systemair manufacturer catalog, hosted at [the dataset's catalog source](https://planetaklimata.com.ua/instr/Systemair/Systemair_Fans_KVO_Data_sheet_Eng.pdf). Phase 7 used the supplied audited dataset without redigitizing or silently changing it.

## Fan Curve Data

| Q m³/s | Computed m³/h | Fan static Pa | Source confidence |
| --- | ---: | ---: | --- |
| 0 | 0 | 688 | Graph-digitized ±20 Pa |
| 0.1042 | 375.12 | 640 | Graph-digitized ±20 Pa |
| 0.2083 | 749.88 | 480 | Graph-digitized ±15 Pa |
| 0.254 | 914.4 | 388 | Confirmed numeric source |
| 0.3333 | 1199.88 | 205 | Graph-digitized ±15 Pa |
| 0.417 | 1501.2 | 0 | Confirmed numeric source |

Interpolation is linear in the supplied m³/s coordinates. Confirmed numeric does not mean a measurement has zero uncertainty. No speed/density correction or polynomial fitting was applied. The six values, including the corrected 688 Pa shutoff value, remain intact.

## Fan Representation

A curve-driven terminal suction boundary uses OpenFOAM `codedFixedValue`. It calculates current Q from the sum of outlet face fluxes, interpolates Ps(Q), and applies a uniform suction static pressure:

`p_kinematic = -Ps(Q)/1.20 - sum(phi*|U|²/2)/sum(phi)`.

The fan discharges at zero-gauge static pressure outside the CFD domain. By the fan-static definition (discharge static minus suction total), the upstream flux-weighted total pressure is -Ps. The kinetic correction is essential: directly subtracting fan static pressure from outlet static pressure would be a different model. See the derivation and source-code checks in `docs/CFD_V01_FAN.md`; pressure definitions follow [AMCA](https://www.amca.org/educate/articles-and-technical-papers/amca-inmotion-articles/straightening-out-fan-curves.html).

This is a lumped performance boundary, not a blade, rotor, swirl, or local fan-wake model. The applied scalar head has numerical relaxation 0.1 once per steady iteration; its final curve closure is independently checked below. Endpoint clamping is permitted only for startup protection; the final operating point is inside the source range.

## Fan Location

The existing AIR_OUTLET at X=0.700 m is the upstream fan suction plane, pulling air along +X after the clean riser. It is 0.500 × 0.250 m = 0.125 m². The actual fan's 250 mm circular connection is 0.049087 m²; these areas are not equated.

An ideal zero-total-pressure-loss adapter is assumed, not designed or meshed. Real transition loss, inlet distortion and fan installation effects can materially change the operating point. Free discharge is a pressure reference, not an external airflow simulation.

## Geometry

The original native FreeCAD model is unchanged. CAD SHA-256:
`1bac8a8a7f5bd57b1aa2770b1b02a1653f8fbd21281d9bb256868cf0712424ce`.

Fluid volume: 0.424 m³. All ten cell zones remain empty fluid. The reference envelope is not a fluid domain. No new fan-zone geometry is needed for the terminal representation.

## Mesh

| Check | Result |
| --- | --- |
| V00 cells / V01 cells | 57,645 / 57,645 |
| Mesh changes | None; original mesh files copied byte-for-byte and hash-verified |
| Type | All hexahedra; 10–20 mm edges |
| Connected regions | One |
| Cell zones / boundary patches | Ten / three |
| Max non-orthogonality | 0° |
| Max skewness | 3.05e-13 |
| Max aspect ratio | 2 |
| Total volume from checkMesh | 0.424 m³ |
| checkMesh -allTopology -allGeometry | Mesh OK |

VTK rereads volume as 0.423999985 m³ due to coordinate precision; this is not a geometry change. No mesh-independence or boundary-layer study was performed.

## Boundary Conditions

| Patch | Pressure | Velocity |
| --- | --- | --- |
| AIR_INLET | totalPressure, ambient p0=0 | pressureInletOutletVelocity; no imposed flow |
| AIR_OUTLET | Actual KVO 250 suction law | pressureInletOutletVelocity |
| WALLS | zeroGradient | noSlip |

Air nu=1.50e-5 m²/s, reference rho=1.20 kg/m³. Standard k-epsilon, inherited smooth-wall functions and assumed inlet k=0.00375 m²/s², epsilon=0.000834 m²/s³. Initial velocity guesses do not prescribe final Q. Thermal, buoyant, compressible and multiphase effects are absent.

## Solver

OpenFOAM Foundation 14 (Ubuntu package 20260724), foamRun/incompressibleFluid, steadyState, SIMPLEC. ParaView 5.11.2 for actual field reading and images. No software was installed during this continuation task.

The old unrun 300 Pa case and notes were archived in `cfd/V01_fan/archive_placeholder/`; they are not the source of these results.

## Convergence

**PARTIAL — NON-CONVERGED after 4000 steady iterations.** An iteration number is not physical elapsed time.

1. Iterations 1–3000: V00-best relaxation (p 0.3, U 0.7, k/epsilon 0.5), bounded linearUpwind U, limitedLinear turbulence. Linear tolerance 1e-8, relative tolerance 0.05. Stable small residual cycle.
2. Iterations 3001–4000: one numerical diagnostic; linear tolerance tightened to 1e-10, relative tolerance zero. No physics, curve, mesh, relaxation or discretization change. Continuity improved by roughly four orders of magnitude; the outer residual cycle persisted. No further tuning was attempted.

| Equation | Final initial residual | Required | Met? |
| --- | ---: | ---: | --- |
| p | 2.837e-5 | <1e-5 | No |
| Ux | 2.713e-6 | <1e-6 | No |
| Uy | 5.137e-6 | <1e-6 | No |
| Uz | 3.181e-6 | <1e-6 | No |
| k | 6.420e-7 | <1e-6 | Yes |
| epsilon | 1.878e-7 | <1e-6 | Yes |

Final linear solver residuals are below 1e-10; they must not be substituted for the initial equation residuals above to claim nonlinear convergence.

Final continuity: local sum 2.055e-9, global -6.557e-10, cumulative -1.680e-8 for the continuation. Conservative inlet/outlet imbalance is 6.84e-8% of inlet Q. Late-100-iteration sampled outlet Q ranges from 0.409924417 to 0.409927084 m³/s (0.000651% range). Inlet pressure range is approximately 5.8e-7 Pa over that sampled window. These show stable integrated quantities, not physical validation.

**Diagnosis:** Tighter inner solves did not eliminate the outer iteration cycle, so inner linear accuracy is not its sole cause. Nonlinear pressure/velocity/turbulence coupling, limiters, outlet backflow and separated flow remain plausible contributors. A period-2/3 iteration cycle does not prove a physical transient vortex. No transient or mesh study was run to establish that cause.

**Execution errors retained:** Two compilation-only errors were fixed before the first solve. Run 1 saved complete iteration-3000 fields and printed End, then crashed during coded-boundary destruction. The continuation preloaded the compiled library to retain its lifetime and exited cleanly with code 0 after iteration 4000. These errors are not hidden as successful exits. The saved final fields were reopened successfully in ParaView.

## Operating Point

**Numerical operating point: Q = 0.409927 m³/s = 1475.74 m³/h; fan-static head ≈17.33 Pa.**

The unmodified curve at final Q gives 17.3232 Pa. Independently integrated suction total pressure gives a fan-static-equivalent head of 17.3257 Pa; mismatch 0.00250 Pa (<0.1 Pa criterion). The point lies on the last segment, between 0.3333 m³/s at 205 Pa and 0.417 m³/s at 0 Pa, close to free delivery. This is an empty-tower simulated operating point, not a measured or final purifier operating point.

The dotted Q² line in the fan figure is only a resistance guide through this one simulated point. It is NOT an independently calculated multi-flow system-curve sweep.

## Airflow

| Quantity | m³/s | m³/h |
| --- | ---: | ---: |
| Inlet, inward magnitude | 0.4099270839 | 1475.737502 |
| Outlet, net outward | 0.4099270836 | 1475.737501 |
| Walls | 0 | 0 |

Mass flow is approximately 0.491913 kg/s at rho=1.20. Outlet reverse flux magnitude is 0.002635 m³/s, about 0.64% of net discharge; the net conservative flux, not only forward flux, is used in operating-point calculations.

## Pressure

All values are flow-induced gauge pressures; atmospheric/hydrostatic pressure is excluded.

| Quantity | Pa |
| --- | ---: |
| Inlet area-mean static | -0.63310 |
| Tower outlet/fan suction static | -33.09455 |
| Tower inlet-minus-outlet static difference | 32.46145 |
| Inlet flux-weighted total | Approximately 0 |
| Outlet/suction flux-weighted total | -17.32565 |
| Tower flux-weighted total-pressure loss | 17.32565 |
| Cell minimum / maximum | -34.51447 / -0.05159 |
| Volume-weighted mean static | -11.47568 |

The 32.46 Pa static difference is not the 17.33 Pa fan-static operating head. The outlet flow carries considerably more kinetic energy than the inlet flow. A suction fan also shifts tower gauge pressure below ambient; negative pressure is expected, not reversed flow by itself.

No component-by-component loss allocation is claimed. The fields place major acceleration and pressure changes around the turn into the riser.

## Velocity

| Quantity | m/s |
| --- | ---: |
| Minimum cell-centre speed | 0.00748 |
| Maximum cell-centre speed | 6.53134 |
| Volume-weighted mean speed | 1.74347 |
| Inlet area-mean normal speed, Q/A | 0.97602 |
| Outlet net mean normal speed, Q/A | 3.27942 |
| No-slip wall boundary speed | 0 |

Peak-speed cell is near (X,Y,Z)=(0.490,0.580,0.959) m, in the riser-turn jet. Max speed is comfortably in the low-Mach regime for the incompressible approximation. The metrics are cell-centre values; point-interpolated plots can smooth extrema.

## Recirculation / Flow Distribution

- **Riser:** 23.12% of its volume has Uz < -0.05 m/s. A high-speed upward jet coexists with substantial downward-moving regions.
- **Clean plenum:** 5.95% of its volume has Ux < -0.05 m/s.
- **Slow regions:** 2.04% of the total volume has speed <0.1 m/s. This is a chosen diagnostic threshold, not a residence-time or contamination criterion.
- **Sharp turn:** Riser-entry normal-velocity CoV ≈1.087 and reverse section area ≈31.22%; a strongly uneven entry remains.
- **Stage distribution:** STAGE_03 normal-velocity CoV ≈0.772. The central stage image shows greater flow near its upper part and slow lower portions. There is no filter in that section.
- **Fan disturbances:** Changed suction/inlet boundary conditions alter the field, but blade wakes and swirl are explicitly unmodelled. No physical fan-induced local wake is claimed.

Reverse component fractions are indicators, not a proof of closed vortex topology. Inlet-seeded streamlines show through-flow paths, not every closed recirculation region.

| Section | Area m² | Mean normal m/s | CoV | Reverse area |
| --- | ---: | ---: | ---: | ---: |
| STAGE_01 centre | 0.420 | 0.9760 | 0.4207 | 0% |
| STAGE_02 centre | 0.420 | 0.9762 | 0.5804 | 0.159% |
| STAGE_03 centre | 0.420 | 0.9756 | 0.7724 | 2.063% |
| Riser z=0.86 m | 0.185 | 2.2701 | 1.0868 | 31.222% |
| Riser z=1.20 m | 0.185 | 2.2156 | 0.9241 | 15.827% |
| Outlet-volume midplane | 0.125 | 3.3362 | 0.3925 | 0% |

Section statistics use piecewise cell values on VTK cuts, NOT conservative face phi. At the abrupt riser entry their sampled Q differs from conservative Q by about 2.45%; the outlet midplane differs by about 1.73%. These sampling/discretization limitations are not disguised as mass leaks. All conservation claims use boundary phi.

## V00 vs V01

V00 values below use its saved `results/CFD_V00/metrics.json` at iteration 6000. V00 data/files and interpretation remain preserved.

| Metric | V00: imposed 1 m/s | V01: KVO 250 suction |
| --- | ---: | ---: |
| Flow m³/h | 1512 | 1475.74 (2.40% lower) |
| Tower static difference Pa | 32.998 | 32.461 |
| Maximum cell speed m/s | 6.6532 | 6.5313 |
| Volume mean speed m/s | 1.8442 | 1.7435 |
| Riser reverse-volume indicator | 23.72% | 23.12% |
| Clean-plenum reverse-volume indicator | 7.82% | 5.95% |
| Slow total volume (<0.1 m/s) | 1.21% | 2.04% |
| STAGE_01 / 02 / 03 normal CoV | 0.135 / 0.355 / 0.595 | 0.421 / 0.580 / 0.772 |
| Residual convergence | Partial, not converged | Partial, not converged |

The flow rate changes modestly, while lower-stage distribution changes more because a uniform imposed inlet has been replaced by a pressure-driven inlet. This is not a controlled one-variable fan comparison. Riser geometry concerns persist.

**Inherited record discrepancy:** V00's narrative table lists STAGE_01/02 CoVs near 0.51/0.55, but its saved numerical metrics give 0.135/0.355. This report uses the numerical values and flags the discrepancy; it does not rewrite V00. Its narrative causal claim of proven physical unsteadiness is also not established by a steady-iteration residual cycle alone.

## Uncertainty

Four of six source knots carry graph-digitization uncertainty. Linear weighting of the recorded ±15 Pa uncertainty at Q=0.3333 toward the nominal zero-pressure endpoint gives about ±1.27 Pa at this final Q **from that digitized knot alone**. This is not a complete uncertainty interval: endpoint measurement tolerance, curve interpolation between sparse knots, installation effects, turbulence, mesh and residual errors are additional and unquantified. Do not publish 1475.74 as a precision-guaranteed specification.

## Limitations

1. Filters are absent. HEPA/filter, prefilter, biochar and water-stage pressure losses at this operating flow remain unknown. Existing single-point filter research was not applied.
2. Both V00 and V01 fail the full residual criteria; stable bulk flow and excellent mass balance do not make either fully converged.
3. The six-point graph-digitized curve has uncertainty; its last segment is sparse.
4. The real 250 mm fan connection/adapter and installation effects are absent. A loss-free terminal connection is optimistic, not a fabrication solution.
5. Standard k-epsilon and smooth-wall functions on one coarse mesh are unvalidated for separated flow. y+ ranges 8.92–792.09; 28.78% of wall faces lie below 30 and 14.59% above 300.
6. No blade wake, swirl, fan stability map, electrical power, acoustic, thermal or mechanical assessment is made.
7. No final CAD validation, mesh-independence study or physical test exists.
8. V01 establishes neither final CADR, AQI reduction, filtration efficiency nor final fan selection.

## Engineering Interpretation

**PROMISING WITH GEOMETRY ISSUES.** The supplied fan characteristic can drive the modelled empty path at a stable bulk operating point close to the V00 placeholder flow. Significant riser reverse flow and uneven stage velocities remain; this run does not show that the tower purifies air or that the fan is adequate with real treatment losses.

Phase 8 data collection and planning can be considered after review, but adding resistance requires appropriate stage pressure-loss data and explicit acceptance of the current numerical/installation limitations. No Phase 8 simulation or optimization was started.

## Figures

All five exported figures were visually inspected; labels carry the required simulation, fan, empty-tower and curve-uncertainty warnings. The visualization skill prompted clearer units, non-colour residual distinctions and moving headers clear of the geometry.

| File in results/CFD_V01_FAN/ | Content |
| --- | --- |
| velocity_streamlines.png | Central speed magnitude, through-flow streamlines and useful Y=0.4 m section |
| pressure_section.png | Central gauge pressure |
| stage03_cross_section.png | Signed normal velocity through empty STAGE_03 |
| fan_curve_operating_point.png | Original curve, digitization bars and actual CFD point |
| residual_history.png | All 4000 actual iterations and unchanged residual thresholds |

ParaView state: `V01_inspection.pvsm`. Machine-readable evidence: `metrics.json`, `residuals.csv`, `verification.json`. Images are actual field visualizations, not illustrative tower renders.

## Files / Reproducibility / Quality Check

- Setup and derivation: `docs/CFD_V01_FAN.md`.
- Active case: `cfd/V01_fan/`; final fields at `4000/`.
- Logs: `logs/foamRun_kvo.log`, `logs/foamRun_kvo_continue.log`, `logs/checkMesh_kvo.log`, `logs/analysis.log`; setup error logs preserved.
- Source-generated boundary and provenance: `0/p`, `constant/kvo250_static_curve_Pa`, `fan_implementation.json`.
- Scripts: `prepare_kvo250_v01.py`, `run_kvo250_v01.sh`, `continue_kvo250_v01.sh`, `analyze_kvo250_v01.py`, `verify_kvo250_v01.py`.
- The old run entry point delegates to the protected real-fan script, not the obsolete 300 Pa case.

Independent read-only checks of the case pass: unchanged fan JSON, unchanged CAD, identical mesh files, single connected domain, correct volume/cell count, ten empty zones, no fixed inlet velocity, positive in-range flow, mass closure, fan pressure conversion and clean final log. Every logged fan interpolation value agrees with an independent source-table calculation within 1.3e-7 Pa. The residual-target check explicitly fails and remains visible in `verification.json`.
