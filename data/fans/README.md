# Fan Data Requirements

## Purpose

This document defines the minimum data required from a real fan datasheet before that fan can be used in any engineering calculation or CFD model for the AQI Tower project. Nothing in this file is a product selection or a purchase recommendation.

## Why this exists

Phase 5 CFD (V00) established that the empty tower geometry produces approximately 33 Pa of flow-induced pressure loss at a placeholder inlet velocity of 1 m/s (Q = 1,512 m³/h). That number is an indicative data point, NOT the fan requirement. The actual system resistance at any real operating point depends on flow rate (Q²-scaled), the yet-unknown filter pressure drops (HEPA, prefilter, possible biochar stage), and minor losses from geometry that V00 did not model with full accuracy. A fan must be selected against a complete, documented system resistance curve — not against a single CFD number from an empty-tower placeholder run.

## Minimum required datasheet fields

Every candidate fan must provide the following before it is included in any comparison or calculation. If a field is absent, mark it MISSING and do not estimate it.

| Field | Symbol | Unit | Notes |
|---|---|---|---|
| Fan curve: at least 5 (Q, ΔP) points | — | m³/h, Pa | Static pressure rise vs. volumetric flow. Must cover shutoff (Q=0) and free-delivery (ΔP=0). |
| Maximum static pressure (shutoff head) | ΔP_max | Pa | At Q = 0. Must be sourced from the curve or datasheet, not estimated. |
| Maximum free-delivery flow | Q_max | m³/h | At ΔP = 0. |
| Rated operating point | Q_rated, ΔP_rated | m³/h, Pa | Manufacturer's stated duty point. |
| Fan type | — | — | Axial / centrifugal / mixed-flow / cross-flow. |
| Drive type | — | — | AC induction / EC (electronically commutated) / DC brushless / belt-driven. |
| Electrical supply | V_supply | V, Hz | Nominal voltage and frequency (e.g., 230 V / 50 Hz). |
| Input power at rated point | P_in | W | Electrical input. Required to estimate operating cost and power budget. |
| Efficiency at rated point | η | % | Total or static efficiency; note which. |
| Speed at rated point | n | RPM | For scaling and acoustic reference. |
| Frame / housing size | — | mm | Outer envelope: width × depth × height (or diameter). Must fit the tower cross-section. |
| Inlet / outlet duct diameter or dimensions | — | mm | For connection design. |
| Weight | — | kg | Structural load on tower. |
| Noise level | L_w or L_p | dB(A) | At rated point; note reference distance if L_p. |
| IP rating | — | — | Required for water-separation stage proximity. |
| Operating temperature range | T_min, T_max | °C | |
| Manufacturer part number and revision | — | — | Needed to verify the exact datasheet used. |
| Datasheet URL or document reference | — | — | Must be a real, retrievable source. |

## Minimum required for CFD fan BC (V01_fan)

To implement the OpenFOAM `fan` pressure-jump boundary condition the following are additionally required:

- The complete fan curve as a table of (Q, ΔP_static) pairs in SI units (m³/s, Pa), at the specific operating speed.
- If the fan speed is variable (EC motor): the curve at the speed closest to the estimated operating speed, or curves at two speeds for interpolation.
- The face area of the fan inlet or the duct cross-section where the BC will be applied (to convert patch-integrated volume flow to face velocity).

If real fan curve data are not available, the V01_fan case MUST be run with an explicit PLACEHOLDER pressure jump and documented as such. Fan curve data may NOT be invented or estimated from first principles without a physical measurement or manufacturer-provided curve.

## Current status (updated Phase 6D, 2026-09-05)

| Candidate | Data file | Evidence | Fan curve | Max ΔP (Pa) | Status |
|---|---|---|---|---|---|
| EBM-Papst G2E140-AE77-01 | `ebmpapst_G2E140_AE77-01.json` | **B** (upgraded) | NOT in operating instructions — performance datasheet needed | UNKNOWN (thermal-limit claim was misinterpretation) | **Tier 3 — re-evaluation needed** |
| EBM-Papst G2E140-AI28-A5 | `ebmpapst_G2E140_AI28-A5.json` | D | Not extracted | UNKNOWN | Tier 3 — low priority |
| EBM-Papst R2E225-RA92-09 | `ebmpapst_R2E225_RA92-09.json` | C | PDF unreadable (binary) | ~425 Pa indicative | Tier 2 — potentially suitable |
| EBM-Papst R2E225-RA92-23 | `ebmpapst_R2E225_RA92-23.json` | C | Available in PDF, not read | ~580 Pa indicative | Tier 2 — potentially suitable |
| Systemair KVO 250 | `systemair_KVO_250.json` | **A** | **6 points: 2 confirmed + 4 graph-digitized (Phase 6D)** | **~688 Pa ±20 Pa (CORRECTED — was 850 Pa)** | **Tier 1 — CFD READY WITH DIGITIZATION UNCERTAINTY** |

The KVO 250 now meets the minimum data requirements (Evidence Level A with 6 fan curve points). See `docs/FAN_DATA_GAPS.md` and `docs/FAN_CURVE_AUDIT.md` for detail.

## What to do next (priority order, Phase 6D)

1. ~~**Digitize KVO 250 fan curve points**~~ — COMPLETED Phase 6D. 6-point curve extracted via PyMuPDF.
2. **[HIGHEST PRIORITY] Confirm baffle face area** from Phase 4 FreeCAD CAD model, then implement V02_fan with real KVO 250 fan BC.
3. **Obtain ebm-papst G2E140-AE77-01 PERFORMANCE DATASHEET** (separate from operating instructions). Determines whether the G2E140 series has adequate shutoff head for this application.
4. **Find text-readable R2E225-RA92-09 fan curve.** Both PDF sources returned binary. Contact ebm-papst India or use an HTML datasheet source.
5. **Obtain multi-point HEPA ΔP curve** — contact Freudenberg or equivalent for ΔP at 3+ face velocities.
6. **Confirm tower filter face area** from Phase 4 FreeCAD CAD model.

Completed actions (Phase 6C + 6D):
- G2E140-AE77-01 operating instructions read — thermal-limit claim corrected (Phase 6C)
- KVO 250 catalog read — Evidence A, 2 confirmed fan curve points obtained (Phase 6C)
- Airflow discrepancy (R2E225-RA92-09) resolved — 705 m³/h at 50 Hz confirmed (Phase 6C)
- First HEPA H13 filter data obtained (Freudenberg, single point) (Phase 6C)
- KVO 250 fan curve expanded to 6 points via PyMuPDF vector extraction — shutoff head corrected to 688 Pa — CFD READY (Phase 6D)
