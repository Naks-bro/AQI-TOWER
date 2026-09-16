# Filter Bypass Diagnosis — AQI Tower Phase 10A

**DIAGNOSIS ONLY — NO GEOMETRY CHANGES MADE**  
**SIMULATION — PHASE 9 FIELDS — CASE_L / CASE_M / CASE_H**  
**Based on saved OpenFOAM fields at iterations 4750 (L/H) and 5000 (M)**

Last updated: 2026-09-06 (Phase 10A).

---

## What Was Visualized

Five figures were generated from the saved Phase 9 OpenFOAM fields using pvpython + matplotlib + scipy:

| File | Contents |
|---|---|
| `results/FILTER_H13/central_velocity_pressure_CASE_M.png` | X-Z central plane (y≈0.4 m), speed + pressure, flow vectors |
| `results/FILTER_H13/bypass_streamlines_CASE_M.png` | X-Z central plane streamlines seeded upstream |
| `results/FILTER_H13/filter_face_bypass_CASE_M.png` | Filter face normal velocity + upstream approach Ux |
| `results/FILTER_H13/residual_history_CASE_M.png` | Residual history from all solver log files |
| `results/FILTER_H13/filter_case_comparison.png` | Filter face velocity maps for all three cases side-by-side |
| `results/FILTER_H13/bypass_analysis.json` | Machine-readable bypass fractions and filter face statistics |

All figures are traceable to the actual saved field files. No CFD data was modified.

---

## Filter Location

**Confirmed from `cfd/FILTER_H13/CASE_M/system/createBafflesDict` and `filter_implementation.json`.**

| Parameter | Value |
|---|---|
| Filter plane | x = 0.305 m |
| Active face Y span | 0.1035 m to 0.6965 m (= 593 mm) |
| Active face Z span | 0.2035 m to 0.7965 m (= 593 mm) |
| Active face area | 0.3516 m² (manufacturer nominal) |
| FILTER_UPSTREAM faces | 961 |
| Frame type | Solid wall baffles sealing y = 0.100–0.103.5 m, 0.696.5–0.700 m (sides) and z = 0.150–0.203.5 m, 0.796.5–0.850 m (top/bottom of filter) |

The filter baffle + frame seal the entire cross-section at x = 0.305 m from y = 100–700 mm and z = 150–850 mm. **The filter face itself is correctly implemented and has no gaps.**

---

## Bypass Path — Evidence

### Quantitative evidence (bypass_analysis.json)

| Case | Total Q (m³/h) | Q through filter (m³/h) | Bypass Q (m³/h) | Bypass fraction |
|---|---:|---:|---:|---:|
| CASE_L | 1434 | 889 | 545 | **38.0%** |
| CASE_M | 1412 | 776 | 636 | **45.1%** |
| CASE_H | 1402 | 729 | 672 | **48.0%** |

Bypass fraction increases monotonically with filter resistance. This is physically consistent with a real bypass path: higher filter resistance redirects more flow to the lower-resistance bypass route.

### Filter face velocity statistics (from bypass_analysis.json)

| Case | Mean v_face (m/s) | Min (m/s) | Max (m/s) | CoV | Reverse area fraction |
|---|---:|---:|---:|---:|---:|
| CASE_L | 0.702 | 0.547 | 0.781 | 0.100 | 0% |
| CASE_M | 0.613 | 0.474 | 0.676 | 0.100 | 0% |
| CASE_H | 0.576 | 0.445 | 0.635 | 0.100 | 0% |

**The filter face itself shows no anomalies.** All flow through the 961-face active area is forward (positive normal direction). The CoV is 0.100 in all three cases — a remarkably stable pattern independent of resistance level. The filter face velocity is well-behaved; the problem is entirely in the fraction of flow that reaches the filter.

### Visual evidence from images

**`bypass_streamlines_CASE_M.png`:**  
Streamlines seeded at x = 0.01 m (far upstream) along the full z range (0.16–0.86 m) show that a significant fraction of the seeded streamlines curve upward (increasing z) before reaching x = 0.305 m and exit the plot at z > 0.85 m without crossing the active filter face. Streamlines seeded at z < 0.20 m or z > 0.80 m are particularly prone to the bypass trajectory.

**`filter_face_bypass_CASE_M.png` (right panel — upstream Ux):**  
Cells at x = 0.25–0.31 m are present at BOTH z < 0.85 m (dirty plenum, positive Ux, approaching filter) AND at z > 0.85 m (clean riser, negative Ux, flow in −x direction in riser). The continuous cell coverage from z ≈ 0.2 m to z ≈ 1.8 m at x = 0.25–0.31 m confirms that the mesh connects these regions at the z = 0.85 m interface.

**`central_velocity_pressure_CASE_M.png`:**  
High-speed cells (>5 m/s, shown bright yellow/green) are concentrated at z = 0.85–0.95 m (the 90° turn from horizontal to vertical). This is the combined bypass + filtered flow accelerating through the turn geometry. Dirty plenum cells (x < 0.305, z < 0.85) show low speed (~0.5–1 m/s), consistent with the wide cross-section of the plenum.

---

## Likely Mechanism

**Classification: OPTION B — Unintended geometry gap at the horizontal–vertical junction.**

### Geometric explanation

The GEO_C tower has:
- **Dirty plenum:** x = 0–0.305 m, z = 0.15–0.85 m (horizontal filter duct, full y width)
- **CLEAN_RISER:** x = 0.26–0.70 m, z = 0.85–1.85 m (vertical riser, inner wall at x = 0.26 m)

At z = 0.85 m (the boundary between horizontal duct and riser), there is an overlap in x:
- Dirty plenum extends to x = 0.305 m (up to the filter face)
- CLEAN_RISER starts at x = 0.26 m (inner wall of riser)
- **Overlap zone: x = 0.26–0.305 m at z = 0.85 m**

In this overlap zone, dirty-plenum cells (z < 0.85 m) are directly connected to CLEAN_RISER cells (z > 0.85 m) through open cell faces at z = 0.85 m. **No wall or baffle was placed at z = 0.85 m between x = 0.26 m and x = 0.305 m on the upstream (dirty) side.**

### Why the filter frame does not seal this path

The filter frame baffles in `createBafflesDict` seal only the x = 0.305 m plane (the filter mounting face). They do not add a horizontal plate at z = 0.85 m. The bypass path goes:

```
dirty plenum (x=0.26–0.305, z<0.85) → open face at z=0.85 → CLEAN_RISER (x=0.26–0.305, z>0.85)
```

This path bypasses the filter at x = 0.305 m entirely.

### Why the bypass fraction increases with resistance

When filter resistance is higher (CASE_H):
- More pressure drop across the filter face
- The bypass path through z = 0.85 m has lower resistance (no porous medium)
- More flow diverts to the lower-resistance bypass route
- Filter face flow (Q_filter) decreases; bypass flow increases

This is exactly the observed behaviour (L=38% → M=45% → H=48%).

### Estimated bypass gap geometry

The suspected bypass gap cross-section:
- x = 0.26 to 0.305 m (width 45 mm)
- y = 0.1035 to 0.6965 m (height 593 mm, full filter width)
- Area ≈ 0.045 × 0.593 ≈ 0.027 m²

At CASE_M bypass flow (0.177 m³/s), the average velocity through this gap would be ≈ 6.5 m/s, consistent with the high-speed region visible at the turn entry in the central plane plot.

---

## CASE L

- Total Q: 1434 m³/h, filter Q: 889 m³/h, bypass: **38.0%**
- Filter face: mean v = 0.702 m/s, CoV = 0.100, no reverse flow
- Filter ΔP: 47.1 Pa (linear model: 67.07 × 0.702 = 47.1 Pa ✓)
- Final iter: 4750 (run interrupted before endTime=5000; integrated quantities stable)

## CASE M

- Total Q: 1412 m³/h, filter Q: 776 m³/h, bypass: **45.1%**
- Filter face: mean v = 0.613 m/s, CoV = 0.100, no reverse flow
- Filter ΔP: 64.7 Pa (linear model: 105.63 × 0.613 = 64.7 Pa ✓)
- Final iter: 5000 (complete run, clean End)
- Fan operating head: 60.92 Pa

## CASE H

- Total Q: 1402 m³/h, filter Q: 729 m³/h, bypass: **48.0%**
- Filter face: mean v = 0.576 m/s, CoV = 0.100, no reverse flow
- Filter ΔP: 72.5 Pa (linear model: 125.75 × 0.576 = 72.4 Pa ✓)
- Final iter: 4750 (run interrupted before endTime=5000; integrated quantities stable)

---

## Confidence

| Claim | Confidence | Basis |
|---|---|---|
| Bypass is real (not a numerical artefact) | **HIGH** | Bypass fraction increases monotonically with resistance — physically correct behaviour for a real bypass path |
| Bypass increases with resistance | **HIGH** | Quantified: L=38%, M=45%, H=48% from stable late-iteration phi values |
| Filter face itself is correctly implemented | **HIGH** | No reverse flow, CoV=0.100, all positive; model self-check passes (ΔP = slope × v to ±0.1 Pa) |
| Bypass located at z=0.85 m junction (x=0.26–0.305 m) | **MEDIUM-HIGH** | Consistent with geometry overlap and visual evidence from streamlines + upstream Ux cells; explicit face-connectivity analysis not performed |
| Bypass gap area ≈ 0.027 m² | **MEDIUM** | Derived from mesh axis nodes; actual effective area may differ due to non-uniform velocity distribution across the gap |

---

## What Is Still Unknown

1. **Exact cell connectivity at z=0.85 m, x=0.26–0.305 m.** A face-by-face connectivity check (e.g. reading `polyMesh/owner` and `polyMesh/neighbour` arrays) would confirm the open path definitively.

2. **Whether the bypass is fully resolvable by adding a wall at z=0.85 m in the overlap zone.** A simple patch at the z=0.85 m interface between x=0.26–0.305 would seal the gap if the hypothesis is correct.

3. **Effect of sealing the bypass on the overall operating point.** With bypass sealed, the effective system resistance increases, Q decreases, and filter face velocity approaches the full-flow value (~1.0–1.1 m/s for Q≈1400 m³/h through 0.3516 m²).

4. **Whether this represents a real fabrication decision or an oversight.** In a physical system, a sheet-metal cap at the top of the filter frame (between inner riser wall and filter mount at x=0.26–0.305 m, z=0.85 m) would seal the bypass.

---

## Recommended Next Step

**Phase 10B: Seal the bypass gap.**

In the blockMeshDict, add a WALL boundary at z = 0.85 m for x = 0.26 m to x = 0.305 m (the overlap zone between dirty plenum and clean riser). Rerun blockMesh + createBaffles + foamRun for CASE_M to verify:
1. Bypass fraction drops to < 2% (numerical leak only)
2. Filter face velocity approaches Q_total / FILTER_AREA ≈ 0.39/0.3516 ≈ 1.11 m/s
3. Operating point shifts to higher fan head and lower Q

Do NOT use Phase 9 results for CADR estimation until the bypass is sealed.
