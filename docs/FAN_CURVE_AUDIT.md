# Fan Curve Audit — AQI Tower Phase 6D

## Phase 7 implementation update

The six source points remain unchanged and have now been used in actual V01 CFD. The final Q is 0.409927 m³/s; interpolation gives 17.3232 Pa fan-static head. Independent integration gives 17.3257 Pa (0.00250 Pa mismatch). Status: PARTIAL / NON-CONVERGED, stable integrated quantities. See `results/CFD_V01_FAN_RESULTS.md`.

Corrections to historical workflow guidance below: five points is a project sampling criterion, not an OpenFOAM software minimum. Foundation 14 provides `fanPressure` and `fanPressureJump`, with different pressure/flow conventions; neither requires silently converting volume flow into velocity for its Q-based curve. This task instead uses an explicitly derived terminal suction boundary to preserve the catalog fan-static definition. No baffle area or new mesh is required. The 0.125 m² tower outlet and 0.049087 m² circular fan connection differ; an ideal adapter is assumed, not verified. Numeric anchors have no assigned digitization error, but are not measurements proven to have zero uncertainty. Older V01/V02 readiness notes below are historical.

## Purpose

This document records, per candidate fan, whether a usable aerodynamic fan curve has been obtained, from what source, how many data points are available, what their uncertainty is, and whether the data is sufficient for use in an OpenFOAM fan boundary condition. This audit is the gating record for V02_fan (the first CFD case that will use a real fan curve instead of a placeholder pressure BC).

Last updated: 2026-09-05 (Phase 6D).

---

## OpenFOAM fan BC requirements

The OpenFOAM `fan` boundary condition (internal baffle face, pressure-jump type) requires:

- A complete table of (Q, ΔP_static) pairs in SI units: (m³/s, Pa).
- At minimum 5 points, covering the full operating range from shutoff (Q=0) to free delivery (ΔP=0).
- Points must be at the rated speed and voltage that will be used in the model.
- If the fan speed is variable: curves at the intended operating speed (or two speeds for interpolation).

If fewer than 5 points are available, or if points come from graphical estimation with large uncertainty, the fan BC cannot be used with confidence. The case must remain on the placeholder `totalPressure` BC and be documented as structural/placeholder only.

---

## Audit table

| Candidate | Source document | Model confirmed in document | Fan curve found | Points available | Point sources | Shutoff head (Pa) | Free delivery (m³/h) | Extraction method | Uncertainty | Evidence level | CFD-ready for fan BC |
|---|---|---|---|---|---|---|---|---|---|---|---|
| G2E140-AE77-01 | ebm-papst Operating Instructions (PDF, read Phase 6C) | YES | NO | 0 | N/A | UNKNOWN | ~370 m³/h (distributor) | N/A | N/A | B | NO |
| G2E140-AI28-A5 | None | NO | NO | 0 | N/A | UNKNOWN | ~500 m³/h (distributor) | N/A | N/A | D | NO |
| R2E225-RA92-09 | Mouser specsheet + ebm-papst OI (both PDF, returned binary) | YES (from distributor sources) | NO | 0 | N/A | ~425 Pa (indicative, unconfirmed) | 705 m³/h at 50 Hz | PDF not extractable | N/A | C | NO |
| R2E225-RA92-23 | EquipSpares listing | PARTIAL | NO | 0 | N/A | ~580 Pa (indicative, converted) | ~1300 m³/h | N/A | N/A | C | NO |
| KVO 250 | Systemair KVO catalog (PDF, read Phase 6C; vector-extracted Phase 6D) | YES | YES (table + vector extraction) | **6** | 2 confirmed numeric + 4 graph-digitized (Bezier) | **~688 Pa ±20 Pa** (CORRECTED — was 850 Pa) | 1501 m³/h | PyMuPDF vector path extraction; calibrated Bezier evaluation | Free delivery ±0%; acoustic point ±0%; digitized points ±15–20 Pa | A | **CFD READY WITH GRAPH-DIGITIZATION UNCERTAINTY** |

---

## Candidate-by-candidate detail

### G2E140-AE77-01

**Document read:** ebm-papst Operating Instructions G2E140-AE77-01 (11 pages, PDF). Section 3.2: Nominal Data table — electrical and thermal parameters only. Section 3.3: weight, IP, insulation, motor protection.

**Fan curve:** NOT PRESENT in operating instructions. This document is the installation and safety manual, not the aerodynamic performance datasheet. The aerodynamic performance datasheet is a separate document (not yet obtained).

**Key finding:** The "Min. back pressure" value in Section 3.2 (0 Pa at 50 Hz, 50 Pa at 60 Hz) is the MINIMUM test back pressure used in the factory acceptance test, not a maximum operating limit. The forward-curved thermal risk is at LOW back pressure (free delivery). This fan cannot be rejected on thermal grounds from this document.

**What is needed:** The separate ebm-papst G2E140-AE77-01 PERFORMANCE DATASHEET containing the Q-ΔP fan curve.

**CFD verdict:** NOT CFD-READY. Zero fan curve points.

---

### G2E140-AI28-A5

**Document read:** None. Single distributor listing only.

**Fan curve:** NOT OBTAINED.

**CFD verdict:** NOT CFD-READY. Zero fan curve points.

---

### R2E225-RA92-09

**Documents attempted:**
1. `mouser.com/catalog/specsheets/ebm_papst_R2E225RA9209.pdf` — returned binary content, not parseable.
2. `img.ebmpapst.com/products/manuals/R2E225RA9209-BA-ENU.pdf` — returned binary content, not parseable.

**Fan curve:** NOT OBTAINED. Both PDF sources confirmed to exist but are not text-extractable by the WebFetch tool.

**Data confirmed from distributor sources:** 705 m³/h free delivery at 50 Hz (confirmed from TME and RS Online UK independently). 155W, 2500 RPM at 50 Hz. 225mm×101mm. PA6 glass-fibre impeller, 7 blades, 3.5 µF capacitor, F insulation.

**Max static pressure (425 Pa indicative):** Not confirmed from manufacturer PDF. Remains a secondary source figure.

**What is needed:** A text-readable version of the R2E225-RA92-09 fan curve. Options: contact ebm-papst India directly for a datasheet, or find an HTML product page with embedded performance data.

**CFD verdict:** NOT CFD-READY. Zero confirmed fan curve points.

---

### R2E225-RA92-23

**Documents attempted:** None in Phase 6C.

**Fan curve:** NOT OBTAINED.

**CFD verdict:** NOT CFD-READY. Zero fan curve points.

---

### KVO 250 (best candidate)

**Phase 6C:** Systemair KVO Circular Duct Fan product catalog PDF read directly. Technical data table (catalog page 34) and acoustic data table (catalog page 37) yielded two confirmed numeric operating points. Shutoff head roughly estimated graphically at ~850 Pa ±100 Pa. Three points — insufficient for OpenFOAM fan BC.

**Phase 6D:** PyMuPDF (`page.get_drawings()`) vector extraction performed on catalog page 1 (PDF page 1). The KVO 250L fan curve is a cubic Bezier path, identified by stroke color RGB (0, 0.328, 0.591). Graph axes calibrated from PDF coordinate space: x_left=306.7 pt (Q=0), x_right=479.2 pt (Q=0.9 m³/s); y_bottom=490.6 pt (ΔP=0 Pa), y_top=348.5 pt (ΔP=1200 Pa). Calibration scale factors derived from the acoustic measurement anchor point: Q_scale=0.9941, ΔP_scale=1.0041. Bezier evaluated at dense parameter spacing; 4 intermediate points sampled at round Q values plus the two confirmed endpoints.

**SHUTOFF HEAD CORRECTION:** Phase 6C estimate (~850 Pa ±100 Pa) was a rough graphical read made without access to the actual PDF image. Phase 6D vector extraction yields **~688 Pa ±20 Pa**. The actual value lies well outside the previous uncertainty range — this is a significant correction. All project documents use 688 Pa as the current best estimate for shutoff head.

**Zero-crossing check:** ΔP=0 at Q≈1494 m³/h from the extracted curve (0.5% error vs. confirmed 1501 m³/h). Monotonicity verified: curve is strictly non-increasing throughout the operating range (within ±2 Pa Bezier noise).

**Fan curve points obtained (Phase 6D — 6 points):**

| Q (m³/s) | Q (m³/h) | ΔP_static (Pa) | Uncertainty | Confidence | Source |
|---|---|---|---|---|---|
| 0 | 0 | 688 | ±20 Pa | GRAPH-DIGITIZED | Phase 6D PyMuPDF vector extraction — Bezier at t=0 |
| 0.1042 | 375 | 640 | ±20 Pa | GRAPH-DIGITIZED | Phase 6D PyMuPDF — Bezier at Q≈375 m³/h |
| 0.2083 | 750 | 480 | ±15 Pa | GRAPH-DIGITIZED | Phase 6D PyMuPDF — Bezier at Q≈750 m³/h |
| 0.254 | 914 | 388 | ±0 (anchor) | CONFIRMED NUMERIC SOURCE | Acoustic data table, catalog page 37: KVO 250 + LDC 250-900 |
| 0.3333 | 1200 | 205 | ±15 Pa | GRAPH-DIGITIZED | Phase 6D PyMuPDF — Bezier at Q≈1200 m³/h |
| 0.417 | 1501 | 0 | ±0 | CONFIRMED NUMERIC SOURCE | Technical data table, catalog page 34: maximum airflow |

**CFD verdict: CFD READY WITH GRAPH-DIGITIZATION UNCERTAINTY.** Six points exceed the 5-point minimum. The 4 graph-digitized points carry ±15–20 Pa uncertainty (~3–5% of point value), which is acceptable for a simplified OpenFOAM fan model at this stage of the project. V02_fan may implement the `fan` BC using this 6-point table. Results must be reported with explicit acknowledgment that 4 of 6 points are graph-digitized and carry the stated uncertainty.

---

## CFD readiness summary

| Case | Fan BC type | Status |
|---|---|---|
| V01_fan (existing) | Placeholder `totalPressure` at AIR_INLET, p0=250 m²/s² (300 Pa) | READY TO RUN — structural/placeholder only |
| V02_fan (planned) | Real `fan` BC with KVO 250 6-point curve | **UNBLOCKED** — fan curve data sufficient; baffle face area still needed |

**The V01_fan placeholder case can be run now.** It will demonstrate the flow field with an assumed 300 Pa driving pressure and empty tower geometry. It does NOT represent the real KVO 250 operating point and must not be interpreted as such.

**V02_fan with a real fan BC:** The 6-point KVO 250 fan curve (Phase 6D) meets the minimum data requirement. The remaining blocker is (b) the baffle face area in the tower geometry (from the FreeCAD Phase 4 CAD model) — required to convert OpenFOAM face-integrated volume flow to the physical fan duct diameter. Mesh modifications (createBaffles at fan location) are also needed before V02_fan can run.

---

## Summary of actions needed to proceed

Completed (Phase 6C + 6D):
- ~~Digitize fan curve points from Systemair catalog~~ — Done. 6-point curve extracted via PyMuPDF vector path. CFD-ready.

Remaining blockers for V02_fan:
1. **Confirm the fan baffle face area** in the tower geometry (from the FreeCAD Phase 4 CAD model). The KVO 250 has a 250 mm duct connection diameter → face area = π×(0.125)² = 0.0491 m², but this must be confirmed against the actual CAD geometry to ensure the model connection is consistent.
2. **Implement the `fan` BC** in a new OpenFOAM V02_fan case: add createBaffles step to place the fan face in the mesh, replace totalPressure BC with the `fan` type using the 6-point table from `systemair_KVO_250.json`.

Last updated: 2026-09-05 (Phase 6D).
