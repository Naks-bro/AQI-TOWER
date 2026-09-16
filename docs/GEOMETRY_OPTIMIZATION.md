# AQI Tower — Phase 8 Geometry Optimization

## Scope and evidence boundary

Phase 8 tests empty-tower airflow geometry only. It preserves V00 and V01 and does not add filter resistance, porous media, particles, water, solar, fan blades, or final-product dimensions. Every new dimension is a **DESIGN EXPERIMENT PARAMETER — NOT PRODUCT REQUIREMENT**.

The numerical evidence comes from the saved V01 iteration-4000 field. V01 is **PARTIAL / NON-CONVERGED**: its bulk flow and fan-law closure are stable, but its pressure and velocity initial residuals do not meet the existing criteria. Consequently, the field can support controlled relative screening, not a final performance claim.

## Baseline V01 diagnosis — completed before geometry selection

### DETECTED geometry facts

- The lower cross-flow area is 0.420 m².
- The actual shared opening into the riser is only 0.090 m²: X=0.320–0.500 m and Y=0.150–0.650 m.
- The full vertical riser area is 0.185 m². Flow therefore contracts by 4.67:1 from the lower path into the opening, turns 90°, and immediately expands by 2.06:1 into the riser.
- The side outlet ends at Z=1.850 m while the riser continues to Z=2.000 m, leaving a 150 mm blind cap above the outlet.

### DETECTED field facts

Using the existing V01 definitions, 23.116% of CLEAN_RISER volume has Uz < -0.05 m/s and 5.947% of CLEAN_PLENUM volume has Ux < -0.05 m/s. The total volume below 0.1 m/s is 2.038%.

Downward flow begins in the first saved cell layer above the riser entrance (cell centre Z=0.8599 m). The first 50 mm band has 25.82% reverse-flow volume, rising to about 30% in the next bands. The peak-speed cell is 6.531 m/s at approximately (0.490, 0.580, 0.959) m, directly above the restricted opening. Reverse-flow volume also rises above the outlet and exceeds 48% in each of the last three 50 mm bands near the blind cap.

### DIAGNOSED CAUSE

**ENGINEERING INTERPRETATION:** The spatial coincidence of the high-speed jet and reverse flow with the restricted opening, abrupt 90° turn, immediate expansion, and blind cap supports a geometry-driven separation diagnosis. These are the most direct geometric causes visible in the saved solution.

**UNKNOWN:** V01 alone does not prove a unique physical cause or the time-dependent vortex structure. Standard k-epsilon, the first-pass mesh, wall-function spread, and incomplete steady residual convergence remain possible contributors to the quantitative magnitude.

Diagnostic evidence:

- `results/GEOMETRY_OPTIMIZATION/v01_diagnosis.json`
- `results/GEOMETRY_OPTIMIZATION/v01_turn_vector_diagnosis.png`
- `results/GEOMETRY_OPTIMIZATION/v01_riser_reverse_by_height.png`

## Controlled trial plan — documented before running CFD

All cases retain the same inlet, three empty stage locations, KVO 250 six-point curve, terminal suction convention, fan orientation, air properties, turbulence model, discretization, solver family, residual criteria, nominal 20 mm maximum cell edge, and outlet face size/orientation. Differences below are deliberate geometry experiments.

### GEO_A — stepped outer turning chamber

**Hypothesis:** Opening the blocked outer side beneath the riser and approximating a rising turning surface with two coarse steps will reduce the concentrated entry jet and separation without adding a vane.

**DESIGN EXPERIMENT PARAMETERS — NOT PRODUCT REQUIREMENTS:** Add a 90 mm long chamber segment from X=500–590 mm with base Z=450 mm, then a 100 mm segment from X=590–690 mm with base Z=650 mm. Both extend to Z=850 mm and span Y=150–650 mm. The original riser X range and blind cap remain unchanged.

**Possible disadvantage:** The step corners can create smaller local separations, consume enclosure volume, and form cleaning ledges. This is a CFD-friendly approximation of a gradual turn, not a fabrication recommendation.

### GEO_B — increased riser-entry overlap

**Hypothesis:** Moving the riser inner wall 60 mm toward the upstream side increases the shared entry area from 0.090 to 0.120 m² and the riser area from 0.185 to 0.215 m², reducing contraction severity and average riser velocity.

**DESIGN EXPERIMENT PARAMETERS — NOT PRODUCT REQUIREMENTS:** Clean-riser inner X changes from 320 to 260 mm; outer X remains 690 mm. No turning chamber is added and the blind cap remains.

**Possible disadvantage:** The larger riser overlaps the upper faces of the last empty treatment-stage regions. Future physical cassettes and service access may conflict with this space; Phase 8 does not resolve that packaging issue.

### GEO_C — combined entry cleanup plus blind-cap removal

**Hypothesis:** Combining the GEO_A turning chamber and GEO_B increased overlap should address the entry jet, while ending the riser at the outlet top removes the diagnosed blind volume above the side outlet.

**DESIGN EXPERIMENT PARAMETERS — NOT PRODUCT REQUIREMENTS:** Use the GEO_A two-step chamber, set the riser inner X to 260 mm, and set riser top Z to 1850 mm instead of 2000 mm. The outlet remains X=690–700 mm, Y=150–650 mm, Z=1600–1850 mm with the same fan orientation and area.

**Possible disadvantage:** This trial changes three related features at once, so it cannot isolate their individual contributions. It also reduces upper packaging volume and may conflict with future acoustic treatment or service access.

## Fair-comparison rules

- Generate each mesh from its own native parametric CAD file; no reused V01 mesh.
- Use the same 20 mm maximum cell edge and exact axis-aligned CAD partitioning. Cell counts may differ because fluid volumes differ; cell size and topology quality must remain comparable.
- Run the same initial 3000-iteration setup. If all three retain the same bounded residual cycle, apply the same single 1000-iteration tighter-linear-solve diagnostic to all three.
- Use conservative inlet/outlet `phi` for flow and mass balance.
- Use V01 thresholds unchanged: riser reverse Uz < -0.05 m/s, clean-plenum reverse Ux < -0.05 m/s, and low speed |U| < 0.1 m/s.
- Report the full CLEAN_RISER reverse fraction and an additional common window Z=0.850–1.850 m so removal of GEO_C's blind cap is not allowed to hide entry behaviour.
- Use identical section locations where they remain inside all geometries, including riser entry Z=0.860 m and mid-riser Z=1.200 m.
- Do not describe a case as converged unless every existing criterion is met.

## Results and decision

### Actual outcome

All three meshes pass the full OpenFOAM topology/geometry check and use 61,395–64,630 all-hexahedral cells at the same 20 mm maximum edge. GEO_B converged in 1,505 iterations and GEO_C in 926. GEO_A remained in a residual cycle after 3,000 iterations and one bounded 1,000-iteration tighter-linear-solve diagnostic; it is **PARTIAL / NON-CONVERGED**.

| Metric | V01 | GEO_A | GEO_B | GEO_C |
| --- | ---: | ---: | ---: | ---: |
| Flow, m³/h | 1475.74 | 1492.26 | 1486.02 | 1496.05 |
| Total-pressure loss, Pa | 17.326 | 6.079 | 10.328 | 3.500 |
| Peak speed, m/s | 6.531 | 5.776 | 5.735 | 5.620 |
| Full-riser reverse volume, % | 23.116 | 17.294 | 25.265 | 15.882 |
| Common-window reverse volume, % | 19.174 | 12.536 | 21.429 | 15.882 |
| Riser-entry CoV | 1.087 | 0.222 | 0.951 | 0.234 |
| STAGE_03 CoV | 0.772 | 0.583 | 0.740 | 0.591 |
| Low-speed volume, % | 2.038 | 1.537 | 2.379 | 1.630 |

### Decision

- **GEO_A — PROMISING BUT UNCERTAIN:** strongest distribution metrics, but residual criteria fail.
- **GEO_B — REJECTED:** convergence is good, but recirculation and low-speed volume worsen relative to V01.
- **GEO_C — PROMISING / BEST CURRENT GEOMETRY:** converged, lowest loss and peak speed, improved stage/riser-entry uniformity, reduced recirculation, and no blind cap.

One fresh GEO_C confirmation simulation used the same CAD, regenerated identical mesh, unchanged KVO curve and byte-matched solver dictionaries. It converged again at iteration 926 and reproduced all reported key metrics exactly. That establishes deterministic repeatability, not physical validation.

The complete comparison, pressure definitions, convergence table, classifications and conditional filter-readiness gate are in `results/GEOMETRY_OPTIMIZATION_COMPARISON.md`.

### Reproduction

1. Generate CAD with `scripts/geometry/create_phase8_geometry_variants.py` using FreeCAD 1.1.3.
2. Prepare CFD cases with `scripts/simulation/prepare_phase8_geometry_cases.py` using FreeCAD's Python.
3. Run one case through `scripts/simulation/run_phase8_geometry_case.sh CASE_NAME` in WSL Ubuntu/OpenFOAM 14.
4. Use `continue_phase8_geometry_case.sh` only for the documented bounded diagnostic when residual criteria fail.
5. Extract fields with ParaView `pvpython` and `analyze_phase8_geometry.py CASE_NAME`.
6. Regenerate the comparison with `compare_phase8_geometry.py` and run `verify_phase8_geometry.py`.

No reproduction step is permission to overwrite V00, V01, or an existing solved case.
