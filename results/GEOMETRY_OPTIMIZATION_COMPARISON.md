# AQI Tower — Phase 8 Geometry Optimization Comparison

**SIMULATION — KVO 250 / EMPTY TOWER**  
**All new dimensions: DESIGN EXPERIMENT PARAMETER — NOT PRODUCT REQUIREMENT**  
**Decision: GEO_C is the best current geometry; classification PROMISING.**

## Evidence boundary

This comparison uses actual saved OpenFOAM fields. No filters, porous resistance, particles, water, solar, fan blades, or final-product details are present. V00 and V01 are preserved. V01 and GEO_A are partial/non-converged; GEO_B, GEO_C, and the one GEO_C confirmation meet the existing residual criteria. Stable flow does not substitute for residual convergence.

## Baseline flow problem

DETECTED geometry forces the 0.420 m² lower path through a 0.090 m² opening, turns it 90°, then expands it into a 0.185 m² riser. This is a 4.67:1 contraction followed immediately by a 2.06:1 expansion. The riser also contains a 150 mm blind cap above the side outlet.

The saved V01 field shows reverse Uz starting in the first cell layer above the entrance at Z=0.8599 m. The first 50 mm band contains 25.82% reverse-flow volume. The 6.531 m/s peak occurs at approximately (0.490, 0.580, 0.959) m above the restricted opening, and the blind-cap bands exceed 48% reverse flow. This supports—but does not uniquely prove—a geometry-driven separation diagnosis.

## Geometries tested

| Case | Intervention | Trial parameters | Main disadvantage |
| --- | --- | --- | --- |
| GEO_A | Two-step outer turning chamber | X=500–590 mm from Z=450–850 mm; X=590–690 mm from Z=650–850 mm; riser otherwise V01 | Step corners/cleaning ledges; blind cap retained |
| GEO_B | Larger entry/riser overlap only | Riser inner wall X=320→260 mm; entry 0.090→0.120 m²; riser 0.185→0.215 m² | Encroaches over last stage zone; sharp outer turn and cap retained |
| GEO_C | GEO_A + GEO_B + cap removal | Two-step chamber; riser inner X=260 mm; riser top Z=2000→1850 mm | Multiple changes cannot be individually attributed; less upper packaging space |

Every value in this table is a **DESIGN EXPERIMENT PARAMETER — NOT PRODUCT REQUIREMENT**.

## Mesh comparison

| Case | Fluid volume m³ | Cells | Max edge mm | Max non-orthogonality | Max skewness | Max aspect ratio | Check |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| V01 | 0.42400 | 57,645 | 20 | 0° | ~3.05e-13 | 2 | Mesh OK |
| GEO_A | 0.45200 | 61,395 | 20 | 0° | 3.04e-13 | 2 | Mesh OK |
| GEO_B | 0.45850 | 64,630 | 20 | 0° | 3.05e-13 | 2 | Mesh OK |
| GEO_C | 0.45425 | 63,780 | 20 | 0° | 3.04e-13 | 2 | Mesh OK |
| GEO_C confirmation | 0.45425 | 63,780 | 20 | 0° | 3.04e-13 | 2 | Mesh OK |

Cell counts differ only because the tested fluid volumes differ. Cell edge, schemes, solver, air properties, turbulence model, KVO curve, fan orientation, outlet area, and initial conditions are controlled.

## Primary CFD results

| Metric | V01 | GEO_A | GEO_B | GEO_C |
| --- | ---: | ---: | ---: | ---: |
| Operating flow, m³/h | 1475.74 | 1492.26 | 1486.02 | **1496.05** |
| Fan-static-equivalent / total-pressure loss, Pa | 17.326 | 6.079 | 10.328 | **3.500** |
| Inlet–outlet static-pressure difference, Pa | 32.461 | 20.422 | 25.128 | **18.810** |
| Peak cell speed, m/s | 6.531 | 5.776 | 5.735 | **5.620** |
| Volume-mean speed, m/s | 1.743 | 1.591 | 1.584 | **1.544** |
| Full CLEAN_RISER reverse volume, % | 23.116 | 17.294 | 25.265 | **15.882** |
| Common riser Z=0.85–1.85 m reverse volume, % | 19.174 | **12.536** | 21.429 | 15.882 |
| CLEAN_PLENUM reverse volume, % | 5.947 | **4.825** | 6.152 | 4.875 |
| Low-speed total volume, %, speed<0.1 m/s | 2.038 | **1.537** | 2.379 | 1.630 |

GEO_C versus V01: operating flow +1.38%, total-pressure loss -79.80%, static difference -42.05%, peak speed -13.95%, full-riser reverse volume -31.30%, and low-speed volume -20.01%. The operating points remain close to free delivery because this is still an empty tower.

## Velocity uniformity

CoV is the area-weighted standard deviation divided by the magnitude of mean normal velocity. Lower is more uniform. No approved product acceptance limit exists.

| Section CoV | V01 | GEO_A | GEO_B | GEO_C |
| --- | ---: | ---: | ---: | ---: |
| STAGE_01 | 0.421 | **0.338** | 0.457 | 0.368 |
| STAGE_02 | 0.580 | **0.456** | 0.658 | 0.511 |
| STAGE_03 | 0.772 | **0.583** | 0.740 | 0.591 |
| Riser entry, Z=0.86 m | 1.087 | **0.222** | 0.951 | 0.234 |
| Riser mid, Z=1.20 m | 0.924 | **0.713** | 0.925 | 0.761 |
| Outlet midplane | 0.393 | **0.390** | 0.392 | 0.416 |

Riser-entry reverse area falls from 31.22% in V01 to 0% in GEO_A and GEO_C; GEO_B retains 26.16%. STAGE_03 reverse area falls from 2.06% in V01 to 1.68% in GEO_A/GEO_C; GEO_B remains 2.06%. Section quantities use cell values on a geometric cut and are not used for conservation.

## Pressure interpretation

The fan-static-equivalent value equals the flux-weighted total-pressure loss because inlet total pressure is approximately ambient in this terminal-suction model. It is not the inlet-minus-outlet static difference. GEO_C's 3.500 Pa total-pressure loss and 18.810 Pa static difference are both reported so the pressure definitions are not mixed.

## Convergence and quality status

| Case | Final iteration | Residual criteria | Mass imbalance | Late-Q range | Fan closure error | Status |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| V01 | 4000 | Not met | 6.84e-8% | 0.000651% | 0.00250 Pa | PARTIAL / NON-CONVERGED |
| GEO_A | 4000 | Not met after one bounded diagnostic | 4.42e-8% | 0.000209% | -0.000035 Pa | PARTIAL / NON-CONVERGED |
| GEO_B | 1505 | Met | 1.09e-5% | 0.00000282% | -0.000022 Pa | CONVERGED |
| GEO_C | 926 | Met | 7.40e-6% | 0.0000614% | -0.000046 Pa | CONVERGED |
| GEO_C confirmation | 926 | Met | 7.40e-6% | 0.0000614% | -0.000046 Pa | CONVERGED |

GEO_A retains a strong residual cycle: final initial residuals are p=4.54e-4, Ux=5.16e-5, Uy=3.58e-4, Uz=4.19e-5, k=4.15e-5, epsilon=4.08e-5. Its integrated quantities are stable, but it is not promoted to converged.

## Engineering classification

### GEO_A — PROMISING BUT UNCERTAIN

It gives the best common-window recirculation and section-uniformity results and materially lowers pressure loss, but its large steady residual cycle remains after the one allowed numerical diagnostic. Its relative pattern is useful; its precision and robustness are uncertain.

### GEO_B — REJECTED

It converges and lowers loss, but the enlarged overlap alone increases full/common-riser reverse volume, clean-plenum reverse volume, and low-speed volume versus V01. It leaves a highly uneven riser entry and creates a future stage-packaging conflict without sufficient aerodynamic benefit.

### GEO_C — PROMISING

It converges, has the lowest pressure loss and peak speed, eliminates reverse area at the riser-entry section, improves all three empty-stage CoVs versus V01, reduces full-riser recirculation, and removes the blind cap. The remaining 15.88% riser reverse indicator and 0.761 mid-riser CoV are material limitations, so this is not a final geometry or product approval.

## Best current geometry

**GEO_C is the best current geometry.** GEO_A is slightly better in common-window reverse flow and most section CoVs, but its non-convergence prevents a stronger numerical decision. GEO_C combines a confirmed residual solution with the lowest empty-path loss and broad improvements over V01.

## Confirmation run

One fresh GEO_C confirmation case was regenerated from the same native CAD and byte-matched dictionaries. It again converged at iteration 926. Key metrics—including Q, both pressure measures, peak/mean speed, riser reverse flow, entry/STAGE_03 CoV, and low-speed volume—match the original GEO_C result exactly. This confirms deterministic reconstruction/repeatability, not physical accuracy.

## Can filter modelling begin?

**YES, CONDITIONALLY—for a controlled, source-backed filter-resistance study using GEO_C only.** GEO_C clears the current numerical geometry gate and is confirmed repeatable. It is not approved as a final tower: no mesh-independence study, transient comparison, approved uniformity/recirculation limit, physical airflow validation, or real adapter model exists. Any next-phase filter case must preserve this empty GEO_C result as its geometry-control reference and must use sourced resistance data rather than invented pressure loss.

## Evidence files

- `results/GEOMETRY_OPTIMIZATION/comparison_metrics.json`
- `results/GEOMETRY_OPTIMIZATION/phase8_geometry_comparison.png`
- `results/GEOMETRY_OPTIMIZATION/verification.json`
- `results/GEOMETRY_OPTIMIZATION/GEO_*/metrics.json`
- `results/GEOMETRY_OPTIMIZATION/GEO_*/central_velocity_pressure.png`
- `results/GEOMETRY_OPTIMIZATION/GEO_*/residual_history.png`
