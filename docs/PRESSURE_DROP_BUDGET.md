# Pressure Drop Budget — AQI Tower

## Phase 7 evidence update

The real KVO 250 / empty-tower V01 predicts approximately 1476 m³/h at 17.33 Pa fan-static-equivalent head. Tower inlet-minus-outlet static pressure is 32.46 Pa; the signed flux-weighted total-pressure loss is 17.33 Pa. These measures are not interchangeable. V01 is PARTIAL / NON-CONVERGED, uses an ideal loss-free adapter and includes no filters. See `results/CFD_V01_FAN_RESULTS.md`.

The historical 33 Pa V00 quantity below is an inlet-to-outlet **static difference**, not a measured total-loss system curve. The old one-filter 1300 m³/h estimate is not validated by V01. Its two-point interpolation also omits the newer 1200 m³/h digitized knot; a statement that the estimate is unchanged by the expanded curve has not been established. No filter budget was recalculated or implemented in this phase. Treat the older estimates below as historical rough screening, not active design inputs.

## Status: PARTIAL — PRE-FILTER SPECIFIED — ACTIVATED CARBON BED STILL UNKNOWN

Last updated: 2026-09-07 (Phase 19 pre-filter provisional specification added).

**Phase 19 update:** G4 washable panel pre-filter (592 × 592 × 48 mm) has been specified analytically. Provisional clean ΔP ~21–30 Pa at 1.06 m/s face velocity [EST]. Full system curve updated in Phase 19 section below. No CFD rerun performed; pre-filter ΔP integrated analytically using fan curve intersection method. See `docs/PHASE19_PREFILTER_SPECIFICATION.md` for full analysis.

Phase 6C obtained the first real manufacturer filter pressure-drop data point for this project (Freudenberg H13 HEPA, 300 Pa at 2.84 m/s). The fan data situation improved: the Systemair KVO 250 was upgraded to Evidence A with a partial fan curve (3 points). A preliminary operating-point estimate was made. Phase 6D expanded the KVO 250 fan curve from 3 to 6 points via PyMuPDF vector extraction; the shutoff head was CORRECTED from ~850 Pa to ~688 Pa. The preliminary operating point (Q≈1300 m³/h, ΔP≈133 Pa) is essentially unchanged because the operating point lies in the confirmed region of the curve (between the two confirmed numeric points) and is insensitive to the shutoff head correction. All other filter stages remain entirely unknown.

---

## System resistance concept

A fan operating in a duct system sits at the intersection of two curves:

- **Fan curve:** Static pressure rise delivered by the fan as a function of volumetric flow rate (ΔP decreases as Q increases).
- **System curve:** Total pressure drop demanded by all resistances in the flow path as a function of Q. For turbulent duct flow, system resistance scales approximately as Q² (doubling the flow quadruples the pressure loss). Filter media adds a predominantly linear-with-velocity term.

The **operating point** is the unique (Q, ΔP) pair where the fan curve and the system curve intersect. Adding a filter, loading an existing filter, or changing fan speed shifts one or both curves.

The V00 empty-tower CFD result (33 Pa at 1512 m³/h) is a minor contribution to the total system resistance. Filter stages will dominate.

---

## Known quantities

### K1 — Empty tower duct losses (from V00 CFD)

| Parameter | Value | Confidence | Notes |
|---|---|---|---|
| Total empty-tower ΔP | ~33 Pa | LOW | V00 SIMPLEC iteration 6000, non-converged, placeholder 1 m/s inlet |
| Reference flow | Q = 1512 m³/h (= 1 m/s × 0.42 m² inlet area) | — | Placeholder only; area typo corrected in Phase 7 |
| Scaling estimate | ΔP_empty(Q) ≈ 33 × (Q/1512)² Pa | APPROXIMATE | Valid for turbulent duct regime; not validated by convergence |

### K2 — HEPA H13 filter (Freudenberg SF13-B-0593x0593x292, clean)

| Parameter | Value | Confidence | Notes |
|---|---|---|---|
| Manufacturer | Freudenberg Filtration Technologies | CONFIRMED | Manufacturer product page |
| Article number | SF13-B-0593x0593x292/V12x25-N10N-J27-ACA | CONFIRMED | — |
| Dimensions | 593 × 593 × 292 mm | CONFIRMED | Face area = 0.352 m² |
| Filter class | H13 (EN 1822), ≥99.95% MPPS | CONFIRMED | — |
| Initial ΔP at rated conditions | 300 Pa at v = 2.84 m/s (Q = 3600 m³/h) | CONFIRMED — single point | Manufacturer nominal; clean filter only |
| Scaling to tower flow (1512 m³/h) | v = 1.19 m/s; ΔP ≈ 126 Pa (linear extrapolation) | LOW — one-point extrapolation | See note below |
| Data type | ONE POINT ONLY — no full ΔP-v curve | — | — |

**Extrapolation note:** With only one manufacturer data point, linear scaling ΔP ∝ v is the best available model: ΔP_filter(Q) ≈ 300 × (Q / 3600) Pa (Q in m³/h, filter face area 0.352 m²). At Q = 1512 m³/h: ΔP ≈ 300 × 1512/3600 = 126 Pa. True value could be 80–150 Pa — the linear model is not validated for this filter. This is an approximation for planning purposes only. Do not cite as a measured or design value.

### K3 — Systemair KVO 250 fan curve (Phase 6D — 6 points)

| Q (m³/h) | ΔP_fan (Pa) | Uncertainty | Confidence |
|---|---|---|---|
| 0 | 688 | ±20 Pa | GRAPH-DIGITIZED (Phase 6D PyMuPDF vector extraction) |
| 375 | 640 | ±20 Pa | GRAPH-DIGITIZED |
| 750 | 480 | ±15 Pa | GRAPH-DIGITIZED |
| 914 | 388 | ±0 (anchor) | CONFIRMED (acoustic data table, catalog page 37) |
| 1200 | 205 | ±15 Pa | GRAPH-DIGITIZED |
| 1501 | 0 | ±0 | CONFIRMED (free delivery, catalog page 34) |

Six points; 2 confirmed numeric + 4 graph-digitized. **SHUTOFF HEAD CORRECTED:** Phase 6C estimated ~850 Pa ±100 Pa; Phase 6D vector extraction yields 688 Pa ±20 Pa — outside the previous uncertainty range. See `docs/FAN_CURVE_AUDIT.md` for detail.

---

## Unknown quantities

| Stage | Why unknown | What is needed |
|---|---|---|
| Prefilter (G4/M5/F7 grade) | No product selected; no ΔP data sourced | Identify filter product and obtain ΔP vs. face velocity |
| HEPA ΔP vs. v curve (multi-point) | Only one nominal point obtained (K2 above) | Full ΔP curve from Freudenberg or equivalent |
| Activated carbon / biochar bed | Stage hypothetical; no Ergun parameters (d_p, ε, bed depth) | Define media type, bed geometry; apply Ergun equation |
| Wet scrubber stage | Stage hypothetical; ΔP model not developed | Define stage type; obtain or estimate ΔP |
| External ductwork and connections | None assumed for V01; real connections not defined | Define from tower geometry when known |
| Tower filter face area (actual) | FreeCAD model cross-section not verified in this phase | Measure from Phase 4 CAD model |

---

## Placeholder quantities (used only for orientation — not design values)

| Item | Placeholder value | Basis | Status |
|---|---|---|---|
| Empty tower ΔP | 33 Pa at Q=1512 m³/h | V00 CFD (non-converged) | PLACEHOLDER |
| HEPA H13 ΔP at tower flow | ~126 Pa at Q=1512 m³/h | Single-point linear extrapolation (K2) | PLACEHOLDER EXTRAPOLATION |
| Total system (empty tower + one clean HEPA, no other stages) | ~159 Pa at Q=1512 m³/h | K1 + K2 sum | ROUGH ESTIMATE ONLY |
| Preliminary operating point (KVO 250 + one clean HEPA) | Q ≈ 1300 m³/h, ΔP ≈ 133 Pa | Fan/system curve intersection (6-point fan curve Phase 6D, single-point HEPA); operating point unchanged by shutoff correction since it lies in confirmed curve region | PRELIMINARY — HIGH UNCERTAINTY |

**CRITICAL REMINDER:** The preliminary operating point (Q≈1300 m³/h, ΔP≈133 Pa) is a rough orientation value with multiple compounded uncertainties. It does not include a prefilter, a biochar stage, a wet scrubber, minor losses, or filter loading over time. With additional filter stages and partial filter loading, the real operating point will be at lower Q and higher ΔP. Do not cite the 1300 m³/h figure as a design target or a CADR claim.

---

## Preliminary operating point derivation

**Fan:** Systemair KVO 250 (6-point curve Phase 6D, linear interpolation between confirmed points in operating region)  
**System:** Empty tower (V00) + one Freudenberg SF13-B 593×593 H13 HEPA (clean, linear ΔP scaling)  
**Excluded:** Prefilter, biochar, wet scrubber — all UNKNOWN

System curve: ΔP_sys(Q) = 33×(Q/1512)² + 300×(Q/3600) [Pa, Q in m³/h]  
Fan curve (linear segment, confirmed range): ΔP_fan(Q) = 388 − 0.662×(Q−915) for 915 ≤ Q ≤ 1501 m³/h

Intersection at Q ≈ 1300 m³/h:  
- Fan: 388 − 0.662×(1300−915) = 133 Pa  
- System: 33×(1300/1512)² + 300×1300/3600 = 24.4 + 108.3 = 133 Pa ✓

This intersection is in the confirmed range of the fan curve (between the two confirmed points). The estimate is internally consistent but rests on highly uncertain inputs. Scenario sensitivity:

| Change | Effect on operating point |
|---|---|
| Add prefilter (est. +50–100 Pa at Q=1300) | Q decreases, ΔP increases — may drop to Q≈1100-1200 m³/h |
| Loaded HEPA (×1.5 clean ΔP) | Q decreases further |
| Real HEPA ΔP at 1.19 m/s is quadratic rather than linear (≈53 Pa) | System is lighter; Q increases toward ~1400 m³/h |
| KVO 250 shutoff head corrected to 688 Pa (from Phase 6D) | Negligible effect — operating point (Q≈1300) is in the confirmed curve region between 914 and 1501 m³/h, far from shutoff |
| Add biochar bed (UNKNOWN) | Q decreases, amount unknown |

The range is plausibly 900–1400 m³/h depending on unresolved factors.

---

## System pressure drop components (full list)

### 1. Empty tower duct losses

Status: PARTIAL (K1 above). ΔP_empty(Q) ≈ 33 × (Q/1512)² Pa.

### 2. Pre-filter / coarse filter stage (Phase 19)

**Phase 19 provisional specification:** G4 washable synthetic panel, 592 × 592 × 48 mm, galvanised steel frame. **[PROJ: PHASE19_PREFILTER_SPECIFICATION.md]**

| Parameter | Value | Status |
|---|---|---|
| Filter grade | **G4** (EN 779:2012 / ISO Coarse ≥ 60%) | SPECIFIED (provisional — RFQ pending) |
| Face dimensions | 592 × 592 mm | SPECIFIED (matches HEPA footprint) |
| Face area | 0.592² = **0.3504 m²** | CALCULATED |
| Face velocity at 1332 m³/h | **1.057 m/s** (= HEPA face velocity) | CALCULATED |
| Clean ΔP at 1.057 m/s | **~21–30 Pa** | ESTIMATE — requires manufacturer datasheet |
| Maintenance trigger ΔP | **~80 Pa** | PROVISIONAL |
| Loaded ΔP (maintenance threshold) | **~100 Pa** | PROVISIONAL ESTIMATE |
| Preferred supplier | Freudenberg (existing contact) / Camfil (backup) | PHASE 19 |

Phase 19 operating-point impact: see §Phase 19 addition below.

### 3. HEPA H13 filtration stage

Status: PARTIAL (K2 above). One manufacturer data point. Full curve not yet obtained.

### 4. Activated carbon / biochar bed (experimental)

| Parameter | Value | Status |
|---|---|---|
| Media type | Possibly biochar-derived — hypothesis only | HYPOTHESIS |
| Bed depth | UNKNOWN m | UNKNOWN |
| Ergun parameters (d_p, ε, µ) | UNKNOWN | UNKNOWN |
| ΔP across packed bed | UNKNOWN Pa | UNKNOWN |

### 5. Water-based wet scrubber / separation stage

| Parameter | Value | Status |
|---|---|---|
| Stage type | UNKNOWN | HYPOTHESIS ONLY |
| Pressure drop | UNKNOWN Pa | UNKNOWN |

### 6. External ducting, connections, grilles

Status: Minor losses not modelled. Assumed negligible for V01.

---

## Total system resistance

| Stage | ΔP at operating Q (Pa) |
|---|---|
| Empty tower duct | ~24 Pa at Q=1300 m³/h (scaled from K1) |
| Prefilter | UNKNOWN |
| HEPA H13 (one, clean) | ~108 Pa at Q=1300 m³/h (K2 linear extrapolation) |
| Biochar bed | UNKNOWN |
| Wet scrubber | UNKNOWN |
| Total (stages known) | ~133 Pa — INCOMPLETE |
| Total (all stages) | **UNKNOWN** |

---

## Fan selection screening range (for planning only)

The 250–700 Pa system screening range from Phase 6B was based on literature HEPA values alone. Phase 6C data suggests that a single clean HEPA at tower operating flow (~1300 m³/h) contributes ~108 Pa. A prefilter would add 30–100 Pa. With clean filters only, the total may fall in the 150–250 Pa range (Scenario L–M boundary). Loading over time and additional stages (biochar) could push toward Scenario M (200–400 Pa) or higher.

**The KVO 250 (shutoff ~688 Pa CORRECTED, operating ~388 Pa at 914 m³/h confirmed) appears capable of covering Scenario L and M. Scenario H (400–700 Pa) would require the operating point to be verified against the fully-loaded system curve; the corrected 688 Pa shutoff leaves less headroom than the previous 850 Pa estimate suggested.**

This analysis is preliminary. It must not be cited as a confirmed system requirement.

---

---

## Phase 19 addition — Updated system budget with G4 pre-filter

**Date: 2026-09-07. Source: PHASE19_PREFILTER_SPECIFICATION.md §7.**

### Baseline (CASE_M_SEALED, no pre-filter)

| Component | ΔP at Q = 1332 m³/h | Status |
|---|---|---|
| Empty tower + duct losses | ~3.8 Pa | CALCULATED from CASE_M_SEALED balance |
| H13 HEPA (clean) | 111.2 Pa | CFD (single-point calibrated) |
| G4 pre-filter | 0 Pa | Absent in baseline |
| Activated carbon bed | UNKNOWN | Not yet measured |
| **Total (known stages)** | **~115 Pa** | MATCHES fan head at 1332 m³/h ✓ |

### With G4 pre-filter (provisional)

System curve equation (pre-filter + HEPA + duct):
```
ΔP_sys(Q) = 3.8×(Q/1332)² + [111.2 + ΔP_pf]×(Q/1332)   [Pa; Q in m³/h]
```

Fan curve (1200–1501 m³/h segment):
```
ΔP_fan(Q) = 205 − 0.6811×(Q − 1200)   [Pa; Q in m³/h]
```

| Scenario | ΔP_pf (Pa) | Q_new (m³/h) | Fan head (Pa) | Q vs. baseline |
|---|---|---|---|---|
| Baseline (no pre-filter) | 0 | 1332 | 115 | 0% |
| Clean G4 — low estimate | 25 | **~1300** | ~137 | **−2.4%** |
| Clean G4 — high estimate | 45 | **~1276** | ~155 | **−4.2%** |
| Loaded G4 — maintenance trigger | 100 | **~1215** | ~198 | **−8.8%** |

**Activated carbon bed (Phase 14/15):** not yet included. When measured, its ΔP is added as an additional term `ΔP_carbon×(Q/Q_ref)` in the system curve equation above. The fan's remaining pressure margin at Q = 1300 m³/h is approximately (205 − 137) = 68 Pa before Q drops below 1200 m³/h — this is the budget available for the carbon bed.

### Total system ΔP summary (Phase 19 estimate)

| Component | ΔP at Q ≈ 1300 m³/h (clean G4 scenario) |
|---|---|
| Empty tower + duct losses | ~3.6 Pa [CALC] |
| G4 pre-filter (clean) | **~24–29 Pa** [EST] |
| H13 HEPA (clean) | ~108–111 Pa [CALC] |
| Activated carbon bed | **UNKNOWN** (est. 20–80 Pa — not measured) |
| **Total (pre-filter + HEPA only)** | **~136–143 Pa** |
| Fan head at 1300 m³/h | ~138 Pa [CALC] |
| Fan margin remaining (for carbon bed) | **~57–67 Pa** [CALC] |

---

## Future work required to close this budget

1. **Obtain G4 pre-filter datasheet** (Freudenberg / Camfil RFQ) with ΔP at ≥ 2 face velocity points to replace the [EST] values above.
2. **Verify inlet opening geometry** from FreeCAD GEO_C model to confirm the 592 × 592 mm filter sizing assumption.
3. **Phase 17A experiment:** measure activated carbon bed ΔP (Darcy–Forchheimer fit) — this is the largest remaining unknown in the system resistance budget.
4. Obtain multi-point HEPA ΔP curve from Freudenberg (at minimum 3 face velocity values) to replace the single-point linear extrapolation.
5. Once carbon bed ΔP is measured: plot complete system curve (pre-filter + HEPA + carbon) against KVO 250 fan curve to confirm operating point.
