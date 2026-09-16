# Particle CFD Plan — AQI Tower

**PLAN ONLY — NO PARTICLE CFD HAS BEEN RUN**  
**This document defines scope, inputs, and open questions for a future Lagrangian particle tracking study.**

Last updated: 2026-09-06 (Phase 11).

---

## 1. Purpose

The current CFD model (Phases 7–10) solves only the airflow field (velocity, pressure, turbulence). It does not include particle transport, deposition, or filtration. This document defines what questions the future particle CFD must answer and what inputs are required before it can be run.

The particle CFD is not a substitute for physical testing (Level 3/4 CADR, see `docs/CADR_METHODOLOGY.md`). It will give a numerically predicted particle removal fraction and trajectory distribution, which can guide experiment design and identify internal deposition zones.

---

## 2. Prerequisites

Before particle CFD can be run, the following must be available:

| Prerequisite | Current status | Where to obtain |
|-------------|---------------|-----------------|
| Converged airflow field (CASE_M_SEALED) | Available (Phase 10B, 5000 iters, PARTIAL NON-CONVERGED) | `cfd/FILTER_H13/CASE_M_SEALED/5000/` |
| Filter face efficiency η(d_p) at the operating face velocity | NOT AVAILABLE | Freudenberg test report; or experimental measurement |
| Particle sizes to track | NOT DECIDED | Define from target application and pollutant (see §3) |
| Inlet particle size distribution | NOT DEFINED | Define from target application, ambient conditions |
| Particle density | Assumption needed (ρ_p ≈ 1000–2650 kg/m³ depending on particle type) | Literature or measurement |
| Stokes number check | Required to verify Lagrangian vs Eulerian approach validity | Derived from above + flow field |

---

## 3. Particle Sizes to Track

For the AQI Tower, the relevant particle populations depend on the target pollutant (not yet defined). Suggested representative sizes for the tracking study, spanning PM2.5 and PM10:

| Size class | Diameter | Relevance |
|-----------|----------|-----------|
| Near-MPPS (hardest to capture) | 0.15–0.25 µm | Minimum efficiency point for glass fibre HEPA |
| Fine accumulation mode | 0.3 µm | Commonly cited HEPA test size (old US standard) |
| PM2.5 boundary | 2.5 µm | Upper boundary of fine particles |
| Coarse PM10 | 5–10 µm | Inertia-dominated, high deposition risk in bends |
| Large inertial | 20 µm | Will deposit in bends and inlet plenum |

For each size, the particle relaxation time τ_p = ρ_p d_p² / (18 μ) determines whether Lagrangian tracking or a diffusion-drift model is appropriate:
- τ_p << flow timescale: particles follow streamlines closely (diffusion / very fine particles)
- τ_p comparable or larger: particles have significant inertia (coarse PM)

---

## 4. Questions the Particle CFD Must Answer

| Question | Why it matters |
|----------|---------------|
| What fraction of inlet particles reach the filter face? | Internal deposition in bends, riser, and plenum may remove particles before they reach the filter — this could increase or decrease measured CADR depending on where removed particles count as "captured." |
| What is the residence time distribution of particles in the system? | Long residence time increases diffusion-capture probability for sub-MPPS particles. |
| Are there recirculation zones where particles accumulate? | The 90° turn (dirty plenum → vertical riser) already shows residual recirculation in RANS. Particles may concentrate here and potentially re-enter the airstream. |
| What is the approach angle distribution at the filter face? | Normal incidence maximises filter efficiency; oblique incidence may reduce it. |
| How does internal wall deposition change with particle size? | Large particles deposit in bends; this is a real removal mechanism but not filter capture. |
| Is there any remaining numerical particle bypass around the sealed baffle? | Even with the z=0.850 m bypass sealed, the RANS field has residual near-wall irregularities. A particle tracking run would reveal whether any particles escape the filter in practice. |
| Do particles settle gravitationally in the horizontal duct before reaching the filter? | For particles > ~5 µm, gravitational settling could be significant in horizontal flow sections. |

---

## 5. Approach: Lagrangian Particle Tracking in OpenFOAM

### Solver

OpenFOAM provides `foamRun` with a `Lagrangian` particle cloud, or the dedicated `sprayFoam`/`reactingParcelFoam` solver for particle-laden flows. For passive (non-reacting, non-evaporating) solid aerosol particles, the appropriate solver is:

```
incompressibleFluid with Lagrangian cloud (solidParticle or kinematicCloud)
```

This requires the airflow field to be converged first (steady RANS, CASE_M_SEALED fields at timestep 5000).

### Particle injection

Particles should be injected at the AIR_INLET face with:
- Uniform spatial distribution across the inlet face area
- Inlet air velocity as initial particle velocity (zero slip at injection)
- Number of parcels sufficient for statistical convergence (~10,000–50,000 parcels per size class)

### Boundary conditions for particles

| Boundary | Particle condition |
|----------|--------------------|
| WALLS | Stick (deposit on first contact) or escape — to be decided based on physical model |
| AIR_INLET | Injection source |
| AIR_OUTLET | Escape (particle exits the domain) |
| FILTER_UPSTREAM | Capture with efficiency η(d_p) — requires η as input |
| BYPASS_SEAL_DIRTY/CLEAN | Stick (wall) |

### Filter face particle model

The `porousBafflePressure` BC handles pressure drop but does not model particle capture directly. A custom coded particle interaction or a post-processing capture fraction must be applied at FILTER_UPSTREAM faces. Two approaches:

1. **Simplified approach:** Any particle reaching a FILTER_UPSTREAM face is captured with probability η(d_p). This requires η as input — which is currently unavailable.
2. **Conservative upper bound:** Assume η = 1.0 at the filter face. This gives the maximum possible filter capture fraction from airflow alone (i.e., how many particles reach the filter, ignoring the small ~0.05% penetration at MPPS).
3. **Conservative lower bound:** Track only the airflow delivery efficiency — what fraction of injected particles reaches FILTER_UPSTREAM vs deposits on walls vs exits through the (now sealed) bypass region.

For Phase 12 planning, approach 3 is recommended first, as it does not require product-specific η(d_p) data.

---

## 6. What the Particle CFD Cannot Do

| Limitation | Reason |
|-----------|--------|
| Confirm filter efficiency η(d_p) | η is a material property of the filter medium, determined by the manufacturer test or physical experiment, not by airflow CFD |
| Replace physical measurement | RANS is PARTIAL NON-CONVERGED; particle trajectories in the recirculation zone at the 90° turn will have significant uncertainty |
| Predict filter loading over time | Lagrangian tracking gives single-pass trajectories at a fixed airflow; loaded-filter simulation requires transient coupled simulation |
| Give a certified CADR | CFD results are model predictions; certification requires a physical test (Level 4 in CADR hierarchy) |
| Resolve sub-grid turbulent diffusion for sub-micron particles | The 20 mm mesh cannot resolve turbulent eddies relevant to diffusion capture of 0.1–0.3 µm particles; stochastic dispersion models must be used and validated |

---

## 7. Particle CFD Inputs Required Before Running

| Input | Status | Action required |
|-------|--------|-----------------|
| Airflow field (CASE_M_SEALED) | Available | Load timestep 5000 |
| Particle sizes | Not decided | Define from target application (Phase 12 scope) |
| Particle density ρ_p | Assumption needed | Use ρ_p = 1000–1500 kg/m³ for PM2.5 surrogate initially |
| Filter capture efficiency η(d_p) | NOT AVAILABLE | Request from Freudenberg or defer to physical test |
| Number of parcels | Design decision | Start with 10,000; increase for statistical convergence |
| Inlet particle concentration | Not needed for trajectory study; needed for CADR estimate | Define from target application |
| Gravitational direction | Known (−z in GEO_C coordinates, i.e., downward) | Confirm from geometry |

---

## 8. Outputs Expected from Particle CFD

| Output | How to extract |
|--------|---------------|
| Fraction of particles reaching FILTER_UPSTREAM | Count particle hits at FILTER_UPSTREAM vs total injected |
| Particle deposition map on WALLS | ParaView particle cloud visualization, colored by capture location |
| Residence time distribution | Track time-of-flight from injection to capture/escape |
| Approach angle distribution at filter face | Compute velocity vector angle relative to filter normal at hit location |
| Fraction exiting at AIR_OUTLET (filter penetration) | Count escape events at AIR_OUTLET per size class |
| Fraction depositing on walls before filter | Count WALLS hits per size class |

---

## 9. Relationship to Physical Validation

The particle CFD (Level 2) and physical test (Level 3/4) are complementary, not interchangeable:

- Particle CFD tells us where particles go in the modelled flow field.
- Physical test tells us what efficiency the assembled device actually achieves.
- Ideally, particle CFD predictions should be checked against the physical test results to validate the CFD model. If they agree, the model can then be used to explore design changes without re-testing.

The physical validation plan is defined in `docs/CADR_METHODOLOGY.md` §6.

---

## 10. Recommended Sequence

1. **Phase 11 (current):** Define methodology. No particle CFD yet.
2. **Phase 12A:** Obtain filter efficiency data from Freudenberg (fractional efficiency curve, or at minimum the MPPS value and efficiency at 2–3 particle sizes).
3. **Phase 12B:** Run Lagrangian particle tracking in CASE_M_SEALED airflow field, using approach 3 (wall deposition + filter arrival fraction) without requiring η(d_p).
4. **Phase 12C:** If η(d_p) data is available, add capture efficiency at filter face and compute Level 2 CADR estimate.
5. **Phase 13:** Physical bench test — measure upstream/downstream particle counts at the actual operating flow.
