# Filter Data Requirements

## Purpose

This directory holds structured data records for filtration components being evaluated for the AQI Tower. Filter data drives the system resistance curve — without at least one confirmed filter ΔP relationship, the operating point of any fan cannot be calculated.

## Why this exists

The AQI Tower system resistance is dominated by filter pressure drop, not by duct losses. The V00 CFD empty-tower result (~33 Pa at 1512 m³/h) is a minor term. Even a single clean H13 HEPA filter adds 80–300+ Pa depending on face velocity. Without real filter data, fan selection is speculation.

## Minimum required data fields

Every filter record must include the following before it can be used in any calculation. Mark missing fields MISSING — do not estimate them.

| Field | Symbol | Unit | Notes |
|---|---|---|---|
| Filter class / grade | — | — | EN 1822: E10–U17; ISO 29463; MERV; or equivalent |
| Dimensions (face) | W × H | mm | The flow-facing area |
| Depth | D | mm | Media pack depth |
| Rated face velocity | v_rated | m/s | Manufacturer's stated test velocity |
| Rated airflow | Q_rated | m³/h | Must be consistent with face area × face velocity |
| Initial pressure drop at rated conditions | ΔP_initial | Pa | Clean filter, sourced from manufacturer |
| Pressure drop vs. face velocity — table or curve | ΔP(v) | Pa vs m/s | At least 3 points preferred; single point acceptable if noted |
| Terminal pressure drop (replacement criterion) | ΔP_terminal | Pa | At end of service life; if stated |
| Frame material | — | — | Galvanized steel / aluminium / plastic |
| Media type | — | — | Glass fibre / synthetic; MiniPleat / deep-pleat / flat |
| Manufacturer and part number | — | — | Exact article number or model |
| Source URL or document reference | — | — | Must be a real, retrievable manufacturer source |

## Evidence levels (same as for fans)

| Level | Meaning |
|---|---|
| A | Official manufacturer datasheet with ΔP curve (multiple v points) directly obtained |
| B | Official manufacturer product page with nominal ΔP and rated conditions; single point only |
| C | Distributor or secondary source with partial data |
| D | Literature estimate only; no product-specific data |

## How filter ΔP enters the system curve

For turbulent-regime filter media (typical HEPA, prefilter):

- ΔP scales approximately **linearly** with face velocity: ΔP ∝ v. This is the viscous-dominated Darcy regime.
- Face velocity at the AQI Tower operating point: v = Q_operating / A_filter (m/s), where A_filter is the net filter face area (m²).
- Single-point linear scaling from a rated condition: ΔP_filter(Q) ≈ ΔP_rated × (Q / Q_rated), where Q_rated = v_rated × A_filter × 3600 m³/h.
- This scaling is valid only for a **clean** filter. Loaded filters may show different behaviour. If possible, use a multi-point curve.

**IMPORTANT:** This linear scaling from a single rated point is an approximation. Always note the assumed scaling when using it. It must not be cited as a measured ΔP for the AQI Tower — it is an extrapolation.

## Current status (Phase 6C, 2026-09-05)

| Product | File | Evidence | ΔP data | Status |
|---|---|---|---|---|
| Freudenberg SF13-B-0593x0593x292 (H13, galvanized steel) | `freudenberg_SF13B_593x593x292.json` | B | 300 Pa at 2.84 m/s (nominal, one point) | FIRST REAL DATA POINT — single point only |

No filter has reached Evidence Level A (full ΔP vs. v curve). The single Freudenberg data point is the first real manufacturer filter data in this project.

## Needed next actions

1. **Get full ΔP curve for the Freudenberg SF13-B (or equivalent H13 product).** Contact Freudenberg Filtration Technologies or obtain a technical datasheet with ΔP at 3+ face velocities.
2. **Determine the actual filter face area for the AQI Tower.** The tower cross-section from the FreeCAD model (Phase 4) sets the available filter area. If the filter must be smaller than the cross-section, a transition frame is needed.
3. **Obtain prefilter (G4/F7/M5 class) ΔP data.** A coarse prefilter stage will protect the HEPA from rapid loading. Its ΔP at tower operating conditions is currently entirely unknown.
4. **Obtain any data on biochar packed-bed ΔP** (Ergun equation parameters: particle diameter, void fraction, bed depth).
