# Phase 12B — Conservative Particle Tracking Results

**Date:** 2026-09-06
**Phase:** 12B
**Status:** COMPLETE — conservative equilibrium-slip particle path integration through the frozen CASE_M_SEALED velocity field

---

## Flow Field Used

| Parameter | Value |
|---|---|
| Case | CASE_M_SEALED (Phase 10B) |
| Timestep | 5000 (final) |
| Phase | 10B |
| Status | PARTIAL NON-CONVERGED (same RANS limit as all GEO_C cases) |
| Q_total | 1332.2 m³/h |
| Filter face velocity (mean) | 1.053 m/s |
| Filter ΔP | 111.2 Pa |
| Bypass fraction | ~0% (9.997×10⁻¹⁰, numerical noise) |

---

## Particle Model

| Property | Value |
|---|---|
| Type | One-way coupled, non-reacting, dilute equilibrium-slip particle paths |
| Particle density | 1200 kg/m³ (single assumed representative aerosol density; composition-specific density was not modelled) |
| Drag/tracking model | Particle velocity = local frozen-air velocity + Cunningham-corrected Stokes terminal-settling velocity in −z; no time-resolved particle-momentum equation |
| Gravity | 9.81 m/s² in −z direction (GEO_C coordinate system) |
| Velocity interpolation | Nearest-neighbour (KDTree on 67,838 cell centres) |
| Integration method | Euler, dt = 0.004 s, max_time = 6.0 s |
| Injection plane | x = 0.010 m, uniform grid in active flow region |
| N seeds | 224 (from 324 candidates; 100 rejected by WALL_DIST_THR = 0.014 m) |

### Particle Classification

- **FILTER_ARRIVAL**: particle reached x > 0.290 m within active filter face area (y ∈ [0.1035, 0.6965], z ∈ [0.2035, 0.7965])
- **FRAME_DEPOSIT**: particle reached x > 0.290 m but outside active filter face area (hit filter frame or casing wall near filter)
- **WALL_DEPOSIT**: nearest-cell KDTree distance exceeded 0.014 m threshold (particle left active flow domain)
- **RECIRCULATION**: particle still in domain at max_time = 6.0 s (no particles reached this state)

There is no independent `OUTLET_ESCAPE` event in the script. In this sealed topology, a downstream path crosses the filter-arrival gate first. The reported OUTLET ESCAPE FRACTION of 0% is therefore derived from geometry and complete terminal accounting, not from a separate far-outlet collector.

**CRITICAL INTERPRETATION:** FILTER ARRIVAL ≠ FILTER CAPTURE. The filter capture probability η(d_p) is NOT available for this product (Freudenberg SF13-B H13). No capture probability was applied. FILTER_ARRIVAL records the fraction of particles that reached the filter face — not the fraction that would be removed from the air.

---

## Particle Sizes Tracked

| Size label | d_p (µm) | Cunningham Cc | τ_p (µs) | v_settle (mm/s) | Stokes number |
|---|---|---|---|---|---|
| 0.3 µm | 0.3 | 1.568 | 0.523 | 0.00513 | 5.23 × 10⁻⁶ |
| 1 µm | 1.0 | 1.166 | 4.318 | 0.0424 | 4.32 × 10⁻⁵ |
| 2.5 µm | 2.5 | 1.066 | 24.684 | 0.242 | 2.47 × 10⁻⁴ |
| 10 µm | 10.0 | 1.017 | 376.516 | 3.694 | 3.77 × 10⁻³ |

All Stokes numbers are << 1. Particles follow airflow streamlines; only gravity drift is size-dependent.

---

## Arrival Fractions — All Particle Sizes

| Size | N total | N filter arrival | N frame deposit | N wall deposit | N recirculation |
|---|---|---|---|---|---|
| 0.3 µm | 224 | 139 | 14 | 71 | 0 |
| 1 µm | 224 | 139 | 14 | 71 | 0 |
| 2.5 µm | 224 | 139 | 14 | 71 | 0 |
| 10 µm | 224 | 137 | 17 | 70 | 0 |

| Size | Filter arrival fraction | Frame deposit fraction | Wall deposit fraction | Recirculation fraction |
|---|---|---|---|---|
| 0.3 µm | **62.1%** | 6.25% | 31.7% | 0.0% |
| 1 µm | **62.1%** | 6.25% | 31.7% | 0.0% |
| 2.5 µm | **62.1%** | 6.25% | 31.7% | 0.0% |
| 10 µm | **61.2%** | 7.59% | 31.2% | 0.0% |

For the required conservation audit, filter-frame contacts are included in the total WALL DEPOSITION FRACTION while remaining visible as a subcategory above:

| Size | FILTER ARRIVAL | WALL DEPOSITION (frame + other wall) | OUTLET ESCAPE | Other (max-time) | Accounted / injected | Balance |
|---|---:|---:|---:|---:|---:|---:|
| 0.3 µm | 139 (62.05%) | 85 (37.95%) | 0 (0%) | 0 (0%) | 224 / 224 | 0 |
| 1 µm | 139 (62.05%) | 85 (37.95%) | 0 (0%) | 0 (0%) | 224 / 224 | 0 |
| 2.5 µm | 139 (62.05%) | 85 (37.95%) | 0 (0%) | 0 (0%) | 224 / 224 | 0 |
| 10 µm | 137 (61.16%) | 87 (38.84%) | 0 (0%) | 0 (0%) | 224 / 224 | 0 |

The integer balance is exact for all four sizes. Fractions sum to 1.0 before display rounding.

---

## Key Findings

### 1. Nearly identical arrival fractions across all size classes

FILTER ARRIVAL FRACTIONS are 62.1% (0.3–2.5 µm) and 61.2% (10 µm). The 0.89 percentage-point difference is two particles out of 224; one particle is 0.446 percentage points. The run contains no seed-density or timestep sensitivity study, so this difference is reported as unresolved at the present numerical resolution rather than as measured size selectivity. At the stated 3.0 m/s characteristic velocity, terminal settling spans 0.00017%–0.123% of flow speed; at 0.5 m/s, the 10 µm value is 0.739%.

### 2. Arrival fraction controlled by flow topology, not particle physics

At this resolution, the approximately 62% FILTER ARRIVAL FRACTION is dominated by the GEO_C mean-flow topology and the injection/wall-classification method. The four tracked sizes remain tightly coupled to the airflow because all Stokes numbers are much less than 1.

### 3. No outlet escape

The derived OUTLET ESCAPE FRACTION is 0%. All particles were classified as FILTER_ARRIVAL, FRAME_DEPOSIT, or WALL_DEPOSIT before any downstream outlet could be reached. Because the script has no separate outlet-crossing event, this verifies the terminal accounting and sealed topology but is not an independent outlet-plane measurement.

### 4. 37.9–38.8% total wall deposition

The required WALL DEPOSITION FRACTION is 37.95% for 0.3–2.5 µm and 38.84% for 10 µm when filter-frame contacts are included. The original subcategories are 31.25–31.70% other-wall contacts and 6.25–7.59% filter-frame contacts. These are terminal contacts in a simplified model; sticking, rebound, and resuspension were not modelled.

### 5. Frame deposits increase slightly with particle size

Frame contacts increased from 6.25% (0.3–2.5 µm) to 7.59% (10 µm). Greater 10 µm gravitational settling is a physically plausible contributor, but the two-particle difference cannot be separated from the coarse seed grid, nearest-cell interpolation, wall threshold, or timestep without sensitivity runs.

### 6. No recirculation (no stagnant particles)

All 224 particles reached a terminal state within 6.0 s. No particle remained in the `RECIRCULATION`/max-time category for this seed grid; this does not prove the absence of smaller or unsampled recirculation regions.

---

## Stokes Number Analysis

For all four tracked particle sizes, St = τ_p × U_char / L_char << 1 (U_char = 3.0 m/s, L_char = 0.30 m).

| Size | St | Physical interpretation |
|---|---|---|
| 0.3 µm | 5.2 × 10⁻⁶ | Effectively a passive tracer |
| 1 µm | 4.3 × 10⁻⁵ | Effectively a passive tracer |
| 2.5 µm | 2.5 × 10⁻⁴ | Effectively a passive tracer |
| 10 µm | 3.8 × 10⁻³ | Still strongly airflow-coupled; settling is the largest of the four sizes but remains small relative to the stated characteristic flow speed |

Size-dependent trajectory differences are negligible for this flow configuration. The dominant effect controlling filter arrival is flow path topology, not particle inertia.

---

## Limitations

1. **No filter capture efficiency applied.** η(d_p) is not publicly available for the Freudenberg SF13-B (Phase 12A finding). FILTER ARRIVAL ≠ FILTER CAPTURE.

2. **Nearest-neighbour velocity interpolation.** No spatial gradient correction applied; adequate for St << 1 but slightly coarser than trilinear interpolation for strongly curved streamlines.

3. **Euler integration.** First-order accurate; adequate for small dt = 0.004 s and slowly varying flow fields.

4. **Uniform area-style grid seeding (not mass-flow-weighted).** The valid seed set is selected by distance to an internal cell centre. A mass-flow-weighted inlet release could produce a higher or lower FILTER ARRIVAL FRACTION; its direction and magnitude are UNKNOWN until calculated.

5. **Frozen steady-state RANS field.** Turbulent dispersion is not modelled. Real particles experience fluctuations around the mean path, and their effect on these fractions is UNKNOWN.

6. **PARTIAL NON-CONVERGED flow field.** CASE_M_SEALED ran 5000 iterations at the same RANS residual plateau as all GEO_C cases. Integrated quantities (Q, ΔP, bypass) are stable and cross-checked, but local-velocity uncertainty remains. The field is accepted only for conservative flow-path screening.

7. **Gravity direction.** Gravity is applied as −z (downward) in GEO_C coordinates. The actual installed orientation of the tower is not yet confirmed in the CAD model. If the tower is installed differently, the gravity direction relative to the mesh must be rechecked.

8. **Equilibrium-slip approximation.** The script sets particle velocity equal to local frozen-air velocity plus terminal settling. It does not solve the transient particle-momentum equation, so “Stokes + Cunningham” describes the settling/relaxation calculation rather than a time-resolved drag integration.

9. **Wall-contact proxy.** WALL_DEPOSIT is triggered when distance from the nearest cell centre exceeds 0.014 m. This is not an exact face-intersection or sticking model and may be sensitive near mesh edges and corners.

10. **Endpoint figures.** The four files named `trajectory_*.png` contain airflow streamlines and tracked particle terminal positions for a mid-plane band. Full individual particle path histories were not stored.

---

## Files

| File | Description |
|---|---|
| `particle_arrival_fractions.json` | Complete numerical results: physics parameters, per-size fractions, summary |
| `trajectory_0p3um.png` | 0.3 µm terminal-outcome points over frozen-field speed and airflow streamlines |
| `trajectory_1um.png` | 1 µm terminal-outcome points over frozen-field speed and airflow streamlines |
| `trajectory_2p5um.png` | 2.5 µm terminal-outcome points over frozen-field speed and airflow streamlines |
| `trajectory_10um.png` | 10 µm terminal-outcome points over frozen-field speed and airflow streamlines |
| `particle_summary.png` | Destination-fraction comparison plus Stokes-number and settling-velocity context |
| `PARTICLE_TRACKING_RESULTS.md` | This file |

Supporting files:
- `scripts/simulation/phase12b_particle_tracking.py` — pvpython script that produced all results
- `docs/PARTICLE_CFD_V12B.md` — methodology documentation

---

## Future η(d_p) hook

The per-size FILTER ARRIVAL FRACTIONS and counts can later be paired with a verified product-specific η(d_p) function. No such function is created or assumed here, and Phase 12B does not calculate filter capture, removal, CADR, or AQI reduction.
