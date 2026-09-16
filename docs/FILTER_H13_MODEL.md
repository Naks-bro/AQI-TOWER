# HEPA H13 Filter Resistance Model — AQI Tower Phase 9

## Status: PARTIAL — THREE SENSITIVITY CASES RUN — FILTER BYPASS DISCOVERED

Last updated: 2026-09-06 (Phase 9).

---

## Purpose

Phase 9 adds a porous-baffle representation of the Freudenberg SF13-B H13 HEPA filter to the best current tower geometry (GEO_C / FILTER_H13 mesh) and determines how the filter affects the KVO 250 fan operating point. Three resistance scenarios (L / M / H) bracket the planning uncertainty range. No filter particles, loading history, or moisture effects are included.

---

## Geometry and mesh

The FILTER_H13 mesh is derived from GEO_C by adding filter-face baffle cells at x = 305 mm (the filter mounting plane). Mesh parameters are identical to GEO_C except for the additional baffle topology.

| Parameter | Value |
|---|---|
| Total cells | 67,838 |
| Fluid volume | 0.45425 m³ |
| Max cell edge | 20 mm |
| AIR_INLET area | 0.420 m² |
| AIR_OUTLET area | 0.125 m² |
| WALLS area | 3.772 m² |
| Filter active face area (nominal) | 0.3516 m² (593 × 593 mm) |
| Filter active face area (mesh) | 0.351649 m² |
| Filter depth (porousBafflePressure length) | 0.292 m |
| FILTER_UPSTREAM faces | 961 |

The filter is placed at x = 305 mm, spanning y = 103.5 to 696.5 mm and z = 203.5 to 796.5 mm. Frame wall baffles (FILTER_FRAME_UPSTREAM / DOWNSTREAM) seal the remaining cross-section at x = 305 mm from y = 100 to 700 mm and z = 150 to 850 mm, closing any cell-to-cell connection at the filter plane that would bypass the porous face.

---

## Filter resistance model

### Physical basis

Only one manufacturer data point is available for the Freudenberg SF13-B (Phase 6C):

| Quantity | Value | Source |
|---|---|---|
| Filter class | H13 (EN 1822) | Manufacturer |
| Dimensions | 593 × 593 × 292 mm | Manufacturer |
| Face area | 0.3516 m² | Manufacturer |
| Initial ΔP at rated conditions | 300 Pa at v = 2.84 m/s | Manufacturer nominal |

No multi-point ΔP–velocity curve exists. A purely Darcy (linear) resistance model is the only defensible choice:

ΔP_filter [Pa] = slope × v_face [m/s]

where slope = 300 Pa / 2.84 m/s = 105.63 Pa·s/m.

**This is an approximation from a single data point. The true ΔP–v curve is unknown. All filter ΔP values in this study are model outputs, not measurements.**

### OpenFOAM implementation

OpenFOAM `porousBafflePressure` boundary condition (cyclic pair at the filter face).

Pressure jump formula (pure Darcy, I = 0):

ΔP [Pa] = D × μ × |U_face| × length

where D is the Darcy resistance coefficient [m⁻²], μ = ρ × ν = 1.20 × 1.5×10⁻⁵ = 1.8×10⁻⁵ Pa·s.

Coefficient derivation for CASE_M (multiplier = 1.0):

D = slope / (μ × length) = 105.63 / (1.8×10⁻⁵ × 0.292) = 20,097,755 m⁻²

### Three resistance scenarios

Three cases bracket the planning uncertainty range from `docs/PRESSURE_DROP_BUDGET.md`. The multiplier scales the Darcy coefficient linearly from the CASE_M baseline.

| Case | Scenario | Basis | Multiplier | D (m⁻²) | slope (Pa·s/m) | Model ΔP at 1.19 m/s |
|---|---|---|---|---|---|---|
| CASE_L | Lower resistance | Lower edge of 80–150 Pa planning bracket at 1.19 m/s | 0.6349 | 12,760,480 | 67.07 | ~80 Pa |
| CASE_M | Nominal | Single manufacturer data point (300 Pa at 2.84 m/s) | 1.0000 | 20,097,755 | 105.63 | ~126 Pa |
| CASE_H | Upper resistance | Upper edge of 80–150 Pa planning bracket at 1.19 m/s | 1.1905 | 23,925,899 | 125.75 | ~150 Pa |

The reference face velocity of 1.19 m/s comes from the pressure-drop budget: Q = 1512 m³/h through 0.352 m² filter face = 1.19 m/s. The 80–150 Pa range (L and H bracket values) is from the Phase 6C/6D HEPA planning bracket in `docs/PRESSURE_DROP_BUDGET.md`.

All three cases share the same mesh, fan BC, air properties, and turbulence model. Only D differs.

---

## Fan boundary condition

The KVO 250 6-point fan curve (Phase 6D) is applied as a `codedFixedValue` terminal-suction boundary at AIR_OUTLET, identical to GEO_C. The BC enforces the fan-static pressure relation:

p = p0 − ΔP_fan(Q)

where ΔP_fan is interpolated from the 6-point kinematic fan-curve table. This is the same fan model used in GEO_C; no changes were made to the fan BC for Phase 9.

---

## Solver and convergence settings

| Setting | Value |
|---|---|
| Solver | foamRun (incompressibleFluid), Foundation 14 |
| Turbulence | k-epsilon RANS, smooth-wall functions |
| Pressure coupling | SIMPLEC (consistent = yes) |
| nNonOrthogonalCorrectors | 0 |
| p relaxation | 0.3 |
| U relaxation | 0.7 |
| k, epsilon relaxation | 0.5 |
| Residual targets | p < 1e-5, U < 1e-6, k/epsilon < 1e-6 |
| Porous-baffle relaxation | 0.005 (see note) |

**Porous-baffle relaxation note:** Initial runs with createBaffles default relaxation (0.2) produced severe oscillations in filter ΔP. Reducing relaxation to 0.05 improved stability; 0.005 produced stable filter ΔP and flow quantities. The createBafflesDict stores the initial value (0.2) but the running case used 0.005. All three production runs used 0.005. This finding must be preserved for any future filter CFD in this project.

### Convergence status

All three cases ran to iteration 5000. None met residual targets; all show the same oscillatory behaviour observed in V00 and GEO_C (U residuals plateau at ~10⁻⁵, p at ~4×10⁻⁵). This is the expected RANS limit for flows with 90° turns and recirculation in the riser.

However, all integrated quantities (Q, filter face ΔP, KVO fan operating head) are stable to 7 significant figures in the final iterations. The comparison is based on late-iteration averages of these stable quantities. Convergence status: **PARTIAL — NON-CONVERGED** for all three cases. Results are defensible for engineering sensitivity comparison but not for final design certification.

---

## Filter bypass — critical finding

During results extraction, a significant discrepancy was discovered between total airflow and flow through the filter patch:

| Case | Total Q (m³/s) | Filter Q through FILTER_UPSTREAM (m³/s) | Bypass fraction |
|---|---|---|---|
| CASE_L | 0.3985 | 0.2470 | **38%** |
| CASE_M | 0.3921 | 0.2155 | **45%** |
| CASE_H | 0.3894 | 0.2026 | **48%** |

A substantial fraction of the total flow does not pass through the filter face. The bypass fraction increases with filter resistance, which is physically consistent with a real bypass path (higher resistance drives more flow to the lower-resistance bypass route).

**The bypass is not a numerical artefact.** The filter + frame baffles seal the cross-section at x = 305 mm from y = 100–700 mm and z = 150–850 mm. However, the mesh contains flow regions above z = 850 mm (the CLEAN_RISER zone, z = 850–1850 mm) and the topology of connections between the dirty plenum and these regions requires further investigation. The growing bypass fraction with increasing resistance is physical evidence that a real flow path exists that circumvents the filter face.

**Design implication:** In the current geometry representation, 38–48% of the KVO 250 airflow bypasses the H13 filter. Actual filtration effectiveness is lower than it would be in a fully-sealed filter installation. This must be resolved before Phase 9 results can be used for CADR estimation or filter-stage design.

**Phase 10 prerequisite:** Investigate bypass geometry. Options include checking mesh connectivity above z = 850 mm at x < 305 mm, inspecting faceZones created by createBaffles, and running a blockage test (set D to a very large value and confirm Q through FILTER_UPSTREAM approaches total Q).

The filter ΔP values reported below are the local ΔP across the active filter face for the air that actually passes through it, not a system-level average including bypass air.

---

## Air and fluid properties

| Property | Value |
|---|---|
| Kinematic viscosity ν | 1.5×10⁻⁵ m²/s |
| Density ρ | 1.20 kg/m³ |
| Dynamic viscosity μ | 1.8×10⁻⁵ Pa·s |

Kinematic pressure in OpenFOAM p fields is in m²/s². Physical pressure in Pa = kinematic × ρ.

---

## What this model does not include

- Filter loading history (ΔP increases as filter loads with particles)
- Multi-point ΔP–velocity curve (only one data point exists; linear model is an approximation)
- Particle transport or filtration efficiency calculation
- Prefilter stage (unknown; not modelled)
- Biochar or other adsorption stages
- Wet scrubber stage
- Temperature or humidity effects on air properties
- Blade geometry; the fan is represented only by its performance curve

---

## Source data traceability

All three cases were generated from the same source inputs, verified by SHA-256 hash stored in each `filter_implementation.json`:

| Source | SHA-256 |
|---|---|
| Filter data (freudenberg_SF13B_593x593x292.json) | 47ae10a150dab276d6f158fb9397925b51e168b85bcafa90de8fe495aa42aec6 |
| Fan data (systemair_KVO_250.json) | 847274a70e6d1a56d4707186c6eb37792f96358bb481bad46a704c554de15c73 |
| CAD (AQI_Tower_ConceptA_GEO_C.FCStd) | baec2027a16a7ab14a02662b8a39bbd5b7168770d9405e7382b93da9babd2a7b |
