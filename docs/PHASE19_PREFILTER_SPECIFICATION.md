# AQI Tower Phase 19 — G4/M5 Pre-filter Specification and Integration

**PHASE 19 STATUS: COMPLETE**
**Date: 2026-09-07**
**Research and specification phase. No CFD run. No CAD modified. No experiment performed.**

---

## Evidence Quality Tags

- **[MFR]** MANUFACTURER — published product data or specification
- **[STD]** STANDARD — ISO, EN, ASHRAE, or equivalent
- **[REF]** TEXTBOOK / ENGINEERING REFERENCE
- **[PROJ]** PROJECT VALUE — established from project files
- **[CALC]** PROJECT CALCULATION — derived from project data
- **[EST]** ENGINEERING ESTIMATE — from reference data; uncertainty stated
- **[RFQ]** REQUIRES QUOTE — value must be confirmed with manufacturer before procurement

---

## 1. Prior Project State Review

The following values are established from existing project files and must not be overridden without explicit identification of the conflict.

### 1.1 Airflow baseline (CASE_M_SEALED, Phase 10B)

**[PROJ]** All values are PARTIAL NON-CONVERGED RANS screening estimates. See `docs/FILTER_BYPASS_FIX.md`.

| Quantity | Value | Source |
|---|---|---|
| Total volumetric flow rate Q | 1332.2 m³/h = **0.3701 m³/s** | `results/FILTER_H13/bypass_analysis_sealed.json` |
| Fan head at operating Q | ~**115 Pa** | Interpolated KVO 250 curve at 1332 m³/h |
| HEPA filter ΔP (clean, single-point model) | **111.2 Pa** | CASE_M_SEALED phase 10B |
| Bypass fraction (sealed) | ~0% (9.997×10⁻¹⁰) | CASE_M_SEALED |
| Mean HEPA face velocity | **1.053 m/s** | CASE_M_SEALED |
| Empty tower + duct losses (residual) | **~3.8 Pa** | = 115 − 111.2 Pa, at 1332 m³/h **[CALC]** |

Note on residual duct losses: the Phase 6D document (V01, empty tower) reported 17.33 Pa total-pressure loss at 1476 m³/h. The V00 result of 33 Pa was a static-pressure difference, not total loss. The 3.8 Pa residual from CASE_M_SEALED balance is the more physically relevant figure at the actual operating point and is used in all Phase 19 calculations. **[CALC, PROJ]**

### 1.2 HEPA filter geometry

**[MFR, PROJ]** From `docs/PRESSURE_DROP_BUDGET.md` K2 and `threejs/data/towerConfig.js`:

| Quantity | Value |
|---|---|
| Product | Freudenberg SF13-B-0593×0593×292 |
| Nominal face dimensions | 593 × 593 mm |
| Nominal depth | 292 mm |
| Face area | 0.593 × 0.593 = **0.3516 m²** |
| Filter class | H13 (EN 1822); ≥99.95% at MPPS |
| Rated ΔP (manufacturer, clean) | 300 Pa at 2.84 m/s (single point) |
| CFD ΔP (clean, at project operating point) | 111.2 Pa at 1.053 m/s (single-point calibrated) |

### 1.3 KVO 250 fan curve (Phase 6D, confirmed points)

**[MFR]** From `docs/PRESSURE_DROP_BUDGET.md` K3:

| Q (m³/h) | ΔP_fan (Pa) | Confidence |
|---|---|---|
| 914 | 388 | CONFIRMED (acoustic table, catalog p.37) |
| 1200 | 205 | GRAPH-DIGITIZED (±15 Pa) |
| 1501 | 0 | CONFIRMED (free delivery, catalog p.34) |

Fan curve segment used for Phase 19 calculations (1200–1501 m³/h, linear interpolation):

**ΔP_fan(Q) = 205 − 0.6811 × (Q − 1200) [Pa; Q in m³/h]** **[CALC]**

### 1.4 Tower geometry — inlet face

**[PROJ]** From `docs/PRESSURE_DROP_BUDGET.md` K1 (velocity BC):

The V00/V01 CFD inlet boundary condition covered an area of **0.420 m²**, derived from: Q = 1512 m³/h at 1 m/s → A = 1512/3600 = 0.420 m². This is the reference inlet face area for all face-velocity calculations.

The dirty plenum outer dimensions (from `threejs/data/towerConfig.js`) span: CAD y = [0, 0.800 m] × CAD z = [0, 0.850 m] = 0.680 m² total face, of which the actual flow inlet covers 0.420 m². The discrepancy reflects internal structure (frame, mounting flanges) not explicitly modelled in this phase. The exact inlet opening geometry requires verification against the FreeCAD CAD model before ordering filter hardware.

### 1.5 Tower physical zones — pre-filter location

**[PROJ]** From `threejs/data/towerConfig.js`:

| Zone | CAD x range | CAD z range | Notes |
|---|---|---|---|
| Inlet face | x = 0 | — | Inlet boundary |
| Water stage placeholder (REMOVED) | x ≈ 0.013–0.068 m | z = 0.204–0.797 m | 55 mm depth; 593×593 face; Phase 18 NO-GO; to be replaced |
| Carbon stage placeholder | x ≈ 0.073–0.128 m | z = 0.204–0.797 m | 55 mm depth; 593×593 face; schematic only |
| H13 HEPA filter | x = 0.130–0.422 m | z = 0.204–0.797 m | 292 mm depth; 593×593 face |

The pre-filter physically replaces the water stage in the x = 0.013–0.068 m zone. Available depth before the carbon stage = 130 mm. A standard 50 mm panel pre-filter fits with 63 mm clearance for mounting frame, gaskets, and airspace.

### 1.6 Phase 18 final decision

**Phase 18 decision: NO-GO for water spray.** Approved replacement: dry G4/M5 washable panel pre-filter at the inlet. No CFD rerun needed unless the pre-filter geometry generates aerodynamic reasons to revisit flow distribution. Phase 18 baseline estimate: 25–50 Pa clean ΔP. **[PROJ]**

---

## 2. Pre-filter Design Requirements

### 2.1 Mandatory requirements

| ID | Requirement | Basis |
|---|---|---|
| R-M-01 | Filter class ≥ G4 per EN 779:2012 or equivalent ISO Coarse 60%+ per ISO 16890:2016 | Phase 18 NO-GO decision; HEPA life protection from coarse particles |
| R-M-02 | Washable or cleanable media (synthetic fibre preferred) | Prototype serviceability; no recurring cost for replacement in early testing |
| R-M-03 | Dry operation — no water, liquid, or biocide | Phase 18 constraint |
| R-M-04 | Nominal face dimensions 590–595 mm × 590–595 mm OR custom-cut equivalent to cover the 593×593 mm HEPA footprint | Face velocity match; see §3 |
| R-M-05 | Nominal depth ≤ 50 mm (to fit in available x = 0–0.068 m zone with clearance) | Geometry constraint **[PROJ]** |
| R-M-06 | Clean ΔP ≤ 70 Pa at face velocity 1.05 m/s | Fan headroom; see §7 |
| R-M-07 | Available in India or procurable without critical import risk | Prototype procurement constraint |
| R-M-08 | Compatible with upstream dry operation (no moisture sensitivity) | Dry system |
| R-M-09 | Temperature rating ≥ 40°C (ambient outdoor Indian summer conditions) | Project environment |

### 2.2 Preferred requirements

| ID | Requirement | Basis |
|---|---|---|
| R-P-01 | Manufacturer datasheet with published ΔP vs. face velocity at ≥ 2 velocity points | Reliable pressure-drop budgeting |
| R-P-02 | Final/recommended change ΔP ≥ 80 Pa (longer service interval) | Prototype convenience |
| R-P-03 | Cardboard, galvanised steel, or aluminium frame (not disposable paper) | Durability for reuse after washing |
| R-P-04 | Existing supplier relationship (Freudenberg preferred as Phase 12A India contact established) | Procurement simplification |
| R-P-05 | Standard EU size 592 × 592 mm (matches HEPA footprint with 1 mm clearance) | Off-shelf availability |

### 2.3 Nice-to-have requirements

| ID | Requirement | Basis |
|---|---|---|
| R-N-01 | Dust holding capacity ≥ 150 g/m² (EN 779) | Longer service interval |
| R-N-02 | Fire classification UL 900 or equivalent (if testing environment has local regulations) | Safety planning |
| R-N-03 | M5 class option available from same supplier (easy upgrade path) | Future upgrade |
| R-N-04 | Unit cost < ₹3,000 per filter | Prototype budget |

---

## 3. Face Velocity Calculation

### 3.1 Reference flow

From CASE_M_SEALED: Q = 1332.2 m³/h = **0.3701 m³/s** **[PROJ]**

This is the flow in the baseline configuration (no pre-filter). The pre-filter face velocity will change slightly with the pre-filter installed; see §7.

### 3.2 Option A — CFD inlet BC area (upper-bound velocity reference)

**[PROJ]** The CFD inlet boundary condition area is 0.420 m² (from PRESSURE_DROP_BUDGET K1).

| Parameter | Value |
|---|---|
| Filter face area | 0.420 m² |
| Face velocity at Q = 1332.2 m³/h | 0.3701 / 0.420 = **0.881 m/s** |
| Face velocity in m/min | **52.8 m/min** |

This represents the entire inlet opening including structural frame; the filter media would have a slightly higher velocity than this if the frame covers part of the opening.

### 3.3 Option B — Pre-filter sized to HEPA footprint (recommended)

**[CALC]** The HEPA filter face is 593 × 593 mm = 0.3516 m². A pre-filter sized to the same footprint (592 × 592 mm standard, or 593 × 593 mm custom) gives:

| Parameter | Value |
|---|---|
| Filter face dimensions | 592 × 592 mm (standard) |
| Filter face area | 0.592² = 0.3504 m² |
| Face velocity at Q = 1332.2 m³/h | 0.3701 / 0.3504 = **1.057 m/s** |
| Face velocity in m/min | **63.4 m/min** |

**This face velocity (1.057 m/s) is effectively identical to the HEPA face velocity (1.053 m/s), which is physically expected and consistent: any flow that reaches the HEPA face must first pass through a co-located pre-filter of the same area.**

Option B (592 × 592 mm) is the recommended sizing because:
1. It matches the HEPA footprint exactly — co-location is natural and geometric
2. Standard HVAC pre-filter sizes include 592 × 592 mm specifically because pre-filters are routinely paired with HEPA filters of the same face dimensions
3. The same mounting frame geometry can potentially be reused or adapted
4. A single face-velocity figure applies to both the pre-filter and HEPA for all operating-point calculations

### 3.4 Summary

| Sizing option | Face area | Face velocity | Recommended? |
|---|---|---|---|
| A — CFD inlet BC area | 0.420 m² | 0.88 m/s | Reference only; actual opening requires CAD verification |
| **B — HEPA-matched 592×592 mm** | **0.350 m²** | **1.06 m/s** | **YES — preferred for mounting simplicity and operating-point consistency** |

**CAD verification action required:** Before ordering hardware, verify the exact inlet opening geometry against the FreeCAD GEO_C model. Confirm that a 592 × 592 mm filter panel can be seated at the inlet face without clearance conflict. If the actual opening differs from the HEPA footprint, adjust the filter order accordingly.

---

## 4. Filter Classification Reference

Both EN 779:2012 (legacy) and ISO 16890:2016 (current) classification systems are used in India and by international suppliers. This section maps the relevant classes to avoid confusion.

### 4.1 Relevant grades

| EN 779 class | ISO 16890 equivalent | Efficiency at MPPS (test aerosol) | Primary removal target |
|---|---|---|---|
| G4 | ISO Coarse ≥ 60% | ≥ 60% gravimetric efficiency (0.4 µm DEHS) | PM10 and coarse particles; negligible PM2.5 |
| M5 | ISO ePM10 ≥ 50% | ≥ 50% fractional at PM10 | PM10 + partial PM2.5 (~30–40% EN 779) |
| M6 | ISO ePM10 ≥ 70% | ≥ 70% fractional at PM10 | Better PM2.5 capture (~40–55%) |
| F7 | ISO ePM1 ≥ 50% | ≥ 50% at PM1 (0.3–1 µm) | Significant PM2.5 and PM1 |

**[STD: EN 779:2012 Particulate Air Filters for General Ventilation; ISO 16890-1:2016 Air Filters for General Ventilation]**

### 4.2 Notes for procurement

EN 779:2012 was officially withdrawn and replaced by ISO 16890:2016. However, many Indian suppliers continue to quote EN 779 G4/M5 designations, and manufacturers supply equivalence tables. Either designation is acceptable for procurement; confirm which standard the supplied test certificate references.

---

## 5. Candidate Products

Five candidate product families are identified. Specification values are from manufacturer product pages, catalogs, and published technical data where available. Values labelled [EST] are engineering estimates from literature reference ranges; they must not be used as design values without manufacturer confirmation.

**Important note:** No manufacturer prices for pre-filters have been independently verified for India as of 2026-09-07. All price figures are estimates **[EST]** requiring confirmation.

---

### Candidate 1 — Camfil Cam-Flo G4 (or equivalent coarse pre-filter)

**[MFR: Camfil AB, camfil.com/en-IN; India manufacturing presence confirmed]**

| Parameter | Value | Source |
|---|---|---|
| Manufacturer | Camfil India Pvt Ltd | MFR |
| Product family | Cam-Flo / Cam30 series (G4 coarse) | MFR |
| Filter class | G4 (EN 779:2012) / ISO Coarse 60%+ | MFR |
| Media | Synthetic fibre (polyester / polypropylene) | MFR |
| Standard EU sizes available | 287×287, 592×490, 592×592, 610×610 mm | MFR (standard EU catalogue) |
| Target size for this project | **592 × 592 × 48 mm** | — |
| Depth | 48 mm (standard flat panel) | MFR |
| Frame | Cardboard (disposable); galvanised steel option for washable | MFR |
| Washable? | Cardboard frame: No. Galvanised steel frame version: Yes | MFR |
| Rated airflow | Typically 1800–3600 m³/h per module at 2.5 m/s nominal (for 592×592) | EST |
| Initial ΔP at 2.5 m/s face velocity | ~50–60 Pa | EST — requires MFR datasheet |
| Initial ΔP at 1.06 m/s face velocity | ~21–25 Pa | EST — linear scaling from 2.5 m/s reference **[CALC]** |
| Recommended final ΔP | Typically 250 Pa (disposable) | EST |
| Dust holding capacity | ~100–150 g/m² for EN 779 G4 at rated velocity | EST |
| Temperature limit | ≥ 60°C continuous (typical synthetic media) | EST |
| India availability | YES — Camfil India operates manufacturing in India | MFR |
| Approximate India price | ~₹800–2,000 per 592×592×48 filter | EST — requires RFQ |
| RFQ contact | info.in@camfil.com; camfil.com/en-IN | MFR |
| Datasheet | Available from camfil.com product catalogue; request EN 779 or ISO 16890 test certificate | — |

**Key gap:** washable version requires galvanised steel frame (Cam-Flo variants). Confirm frame material when requesting quote. Cardboard-frame Cam30 is disposable only.

---

### Candidate 2 — Freudenberg Viledon G4 coarse filter

**[MFR: Freudenberg Filtration Technologies SE, viledon.com; India: Pune +91 20 67633600, info@freudenberg-filter.com — Phase 12A contact already established]**

| Parameter | Value | Source |
|---|---|---|
| Manufacturer | Freudenberg Filtration Technologies | MFR |
| Product family | Viledon brand — F35G (G4) or equivalent coarse pre-filter | MFR |
| Filter class | G4 (EN 779) / ISO Coarse | MFR |
| Media | Viledon synthetic fibre (polypropylene/polyester blend) | MFR |
| Standard EU sizes | 592×490, 592×592, and others — standard EU HVAC sizes | MFR |
| Target size | **592 × 592 × 48–96 mm** | — |
| Frame | Cardboard, galvanised steel, or rigid plastic depending on product variant | MFR |
| Washable? | Metal-frame variants: Yes; cardboard: No | MFR |
| Initial ΔP at 2.5 m/s | ~45–55 Pa (estimated from G4 class data) | EST |
| Initial ΔP at 1.06 m/s | ~19–23 Pa | EST — [CALC] |
| India availability | YES — Pune HQ; India contact confirmed Phase 12A | MFR |
| Approximate India price | ~₹700–1,800 per unit | EST — requires RFQ |
| RFQ contact | info@freudenberg-filter.com; +91 20 67633600 | MFR (Phase 12A) |

**Advantage:** Existing supplier relationship from Phase 12A. Combined HEPA + pre-filter enquiry reduces administrative overhead.

---

### Candidate 3 — AAF (American Air Filter / Daikin) G4/M5 panel filter

**[MFR: AAF International / AAF India; aafilters.com; India distribution via AAF India, multiple regions]**

| Parameter | Value | Source |
|---|---|---|
| Manufacturer | AAF International (Daikin Industries subsidiary) | MFR |
| India brand | AAF India | MFR |
| Product family | Sabre-Cell / AstroCell flat panel coarse filter family | MFR |
| Filter class | G4 or M5 (EN 779) / ISO equivalent | MFR |
| Media | Synthetic progressive density fibre | MFR |
| Standard sizes | EU standard sizes including 592×592 mm | MFR |
| Depth | 48–96 mm depending on model | MFR |
| Frame | Galvanised steel (reusable/washable frames available) | MFR |
| Washable? | Galvanised steel frame models: Yes | MFR |
| Initial ΔP at 2.5 m/s | ~50–70 Pa (G4); ~70–100 Pa (M5) | EST |
| Initial ΔP at 1.06 m/s | ~21–30 Pa (G4); ~30–42 Pa (M5) | EST — [CALC] |
| India availability | YES — AAF India distributes through regional offices | MFR |
| Approximate India price | ~₹900–2,500 per unit | EST — requires RFQ |
| RFQ contact | AAF India — contact via aafilters.com/en-IN or local HVAC distributor | MFR |

---

### Candidate 4 — Mann+Hummel G4 industrial air filter

**[MFR: Mann+Hummel GmbH; mann-hummel.com; India: Mann+Hummel Purolator Filters India Ltd, Noida, Uttar Pradesh]**

| Parameter | Value | Source |
|---|---|---|
| Manufacturer | Mann+Hummel India (industrial filtration division) | MFR |
| Product family | FiLCON / equivalent G4 HVAC coarse panel filter | MFR |
| Filter class | G4 (EN 779) or ISO Coarse | MFR |
| Media | Synthetic fibre | MFR |
| Standard sizes | EU-standard and custom HVAC sizes | MFR |
| Depth | 48–96 mm | MFR |
| Frame | Galvanised steel or cardboard | MFR |
| Washable? | Metal frame: Yes | MFR |
| Initial ΔP at 2.5 m/s | ~50–60 Pa | EST |
| Initial ΔP at 1.06 m/s | ~21–25 Pa | EST — [CALC] |
| India availability | YES — India manufacturing confirmed (Noida); HVAC products distributed nationally | MFR |
| Approximate India price | ~₹700–2,000 per unit | EST — requires RFQ |
| RFQ contact | Mann+Hummel India, Noida; contact via mann-hummel.com or IndiaMART | MFR |

---

### Candidate 5 — Generic G4 washable panel filter (IndiaMART HVAC category)

**[MFR: multiple Indian HVAC filter manufacturers — IndiaMART platform]**

Multiple Indian manufacturers supply washable G4 panel filters on IndiaMART. Specific brands include Filtration Group India, Air-Con Filtration, Servigroup, and others. These products vary in quality and testing certification.

| Parameter | Value | Source |
|---|---|---|
| Manufacturer | Multiple Indian HVAC filter manufacturers | IndiaMART |
| Filter class | G4 (EN 779) — self-certified; some carry EN 779 test certificates | MFR varies |
| Media | Synthetic fibre (polypropylene) | MFR varies |
| Standard sizes | 592×592, 610×610, 490×490 and custom sizes | MFR varies |
| Depth | 48–96 mm | MFR varies |
| Frame | Galvanised steel or aluminium (washable) | MFR varies |
| Washable? | Yes — primary selling point for Indian market | MFR varies |
| Initial ΔP | Not always published; ~50–70 Pa at 2.5 m/s estimated | EST — highly uncertain |
| India availability | YES — widely available, usually fast delivery | — |
| Approximate India price | **~₹400–1,500** per 592×592 unit | EST — confirm on IndiaMART |
| RFQ contact | Multiple; search IndiaMART for "G4 washable air filter 592×592" | — |

**Risk:** Test certificate quality varies. Some products may be G4-labelled without EN 779 or ISO 16890 certification. Always request the test certificate from the manufacturer. Priority: confirm EN 779 or ISO 16890 test evidence before purchase.

---

## 6. G4 vs M5 Comparison for This System

### 6.1 Primary function

The pre-filter's primary function is HEPA life extension by capturing coarse particles before they reach the H13 HEPA face. The HEPA (≥99.95% at MPPS, H13) already captures PM2.5 at high efficiency. The pre-filter does not need to address PM2.5 — the HEPA does this.

### 6.2 Coarse particle capture

| Size range | G4 capture | M5 capture | PM source (India urban outdoor) |
|---|---|---|---|
| > 10 µm (coarse dust, pollen, mineral) | > 80% | > 85% | Dominant HEPA loading fraction in India |
| 2.5–10 µm | ~30–50% (EN 779 test) | ~60–80% | Moderate HEPA loader |
| 1–2.5 µm | ~10–25% | ~40–55% | Minor; HEPA handles this |
| 0.3–1 µm (PM1) | ~5–15% | ~25–45% | HEPA handles this; irrelevant to pre-filter role |

**[EST from EN 779:2012 gravimetric efficiency classes and ISO 16890 ePM fraction data]**

### 6.3 HEPA protection

For HEPA life extension in a polluted Indian outdoor environment (PM10 ≈ 100–300 µg/m³ at major cities), the dominant HEPA loading fraction is particles > 5 µm (mineral dust, road dust, pollen). Both G4 and M5 capture > 80% of this fraction. The incremental benefit of M5 over G4 for the coarse loading scenario is modest.

### 6.4 Pressure drop impact

| Grade | Estimated clean ΔP at 1.06 m/s | Impact on system Q |
|---|---|---|
| G4 | **~21–30 Pa** [EST] | Q drops ~2.3–3.0% from baseline |
| M5 | **~35–50 Pa** [EST] | Q drops ~3.5–4.8% from baseline |

Full system analysis in §7.

### 6.5 Service interval and washability

- G4 filters load more quickly (lower capture efficiency → more pass-through) but are equally washable.
- M5 filters capture more mass per pass → faster ΔP increase → more frequent washing, but longer interval per unit particle mass captured per pass (more captured = filter loads faster locally).
- Net service interval is environment-dependent. For a highly polluted site (PM10 > 200 µg/m³), monthly washing is likely regardless of G4 or M5 selection.

### 6.6 Recommendation

**G4 is the recommended grade for the prototype.** Reasoning:

1. **Sufficient HEPA protection:** G4 removes > 80% of the coarse fraction that drives HEPA loading. The incremental HEPA-life benefit of M5 over G4 does not justify the higher ΔP penalty at this prototype stage.
2. **Lower pressure drop:** G4 adds ~21–30 Pa vs M5's ~35–50 Pa at the operating face velocity. Preserving fan margin is important because the activated carbon bed (Phase 14/15) will add further unquantified resistance (estimated 20–80 Pa from PRESSURE_DROP_BUDGET).
3. **Washability:** G4 washable panels are more widely available in India at lower cost.
4. **Upgrade path:** Switching from G4 to M5 is trivial — same dimensions, same mounting. The prototype can be run with G4 to establish service intervals, then upgraded to M5 if coarse-particle HEPA loading remains problematic after testing.

**M5 is appropriate if:**
- Service interval data from G4 operation shows HEPA is still loading faster than desired
- PM10 at the installation site is particularly high (> 300 µg/m³ mean)
- The activated carbon bed ΔP turns out to be at the low end of estimates (< 30 Pa), leaving more fan headroom

---

## 7. Pressure Drop Analysis and System Operating Point

### 7.1 Baseline (no pre-filter, CASE_M_SEALED)

**[PROJ, CALC]**

| Component | ΔP at Q = 1332 m³/h |
|---|---|
| Empty tower + duct + turning losses | 3.8 Pa |
| H13 HEPA (clean, single-point model) | 111.2 Pa |
| Activated carbon bed | UNKNOWN — not yet measured |
| Pre-filter | 0 Pa (absent) |
| **Total** | **115 Pa** |
| Fan head (KVO 250 at 1332 m³/h) | **115 Pa ✓** |

### 7.2 System curve equation (extended for pre-filter)

**[CALC]** Extending the CASE_M_SEALED baseline:

```
ΔP_sys(Q) = 3.8 × (Q/1332)² + [111.2 + ΔP_pf] × (Q/1332)   [Pa; Q in m³/h]
```

where:
- `3.8 × (Q/1332)²` — duct losses (quadratic with Q, from CASE_M_SEALED balance)
- `111.2 × (Q/1332)` — HEPA ΔP (approximately linear with Q using single-point calibration)
- `ΔP_pf × (Q/1332)` — pre-filter ΔP (approximately linear with Q for fibrous media) where ΔP_pf is the clean pre-filter ΔP at Q = 1332 m³/h reference point

**Activated carbon bed excluded:** not yet measured. Its ΔP will shift the operating point further when the Phase 14/15 experimental data become available.

Fan curve (1200–1501 m³/h segment):
```
ΔP_fan(Q) = 205 − 0.6811 × (Q − 1200)   [Pa; Q in m³/h]
```

### 7.3 Operating point intersection — analytical solution

Setting ΔP_sys = ΔP_fan and solving as a quadratic in u = Q/1332: **[CALC]**

```
3.8u² + (1018.7 + ΔP_pf) × u − 1022.3 = 0

u = [−(1018.7 + ΔP_pf) + √((1018.7 + ΔP_pf)² + 15,539)] / 7.6

Q_new = u × 1332   [m³/h]
```

Derivation: 1022.3 = 205 + 0.6811 × 1200; 15,539 = 4 × 3.8 × 1022.3. See full derivation in Phase 19 working notes.

### 7.4 Scenarios

**[CALC]** All values ±5% due to model uncertainty (single-point HEPA calibration, simplified duct-loss scaling).

| Scenario | ΔP_pf at Q = 1332 (Pa) | Q_new (m³/h) | Fan head (Pa) | Q reduction | HEPA face v |
|---|---|---|---|---|---|
| Baseline (no pre-filter) | 0 | 1332 | 115 | 0% | 1.053 m/s |
| Clean G4 — low estimate | 25 | **~1300** | ~137 | **~2.4%** | ~1.028 m/s |
| Clean G4 — high estimate / M5 low | 45 | **~1276** | ~154 | **~4.2%** | ~1.009 m/s |
| Loaded G4 — maintenance trigger | 100 | **~1215** | ~198 | **~8.8%** | ~0.961 m/s |

Note: the loaded-filter scenario at 100 Pa assumes the pre-filter is at the maintenance/replacement threshold. At 9% airflow reduction, CADR is proportionally reduced. The trigger should be set well below the point where CADR impact becomes unacceptable to the project's application requirements (not yet defined — see REQUIREMENTS.md §3.2).

### 7.5 Remaining fan margin

At Q = 1300 m³/h (clean G4, ~25 Pa scenario), fan head ≈ 137 Pa. The KVO 250's shutoff head is 688 Pa (Phase 6D). The system is operating well within the fan's capability. The remaining margin before adding the carbon bed ΔP:

- Fan can deliver up to ~195 Pa at 1200 m³/h (confirmed curve segment)
- Carbon bed is estimated 20–80 Pa (PRESSURE_DROP_BUDGET, unverified)
- Added pressure budget available above current 137 Pa: 195 − 137 = **58 Pa** before Q drops below 1200 m³/h

If the carbon bed ΔP is at the low estimate (20 Pa), system remains comfortable. At 80 Pa, system resistance at 1200 m³/h would approach the 205 Pa fan capacity — tight but still within the fan curve confirmed region. This reinforces the recommendation to prefer G4 over M5 for the pre-filter (lower ΔP reserves more headroom for the carbon bed).

---

## 8. Mechanical Integration

### 8.1 Filter location

The pre-filter occupies the zone previously assigned to the water-stage placeholder: CAD x ≈ 0.013–0.068 m. The inlet face of the filter is at approximately x = 0.013 m (leaving a 13 mm buffer from the tower inlet face for frame and gasket). The downstream face of the filter clears the upstream face of the carbon stage at x = 0.073 m, leaving approximately 5–13 mm of clearance (adequate for airspace).

The filter panel is mounted at the tower's inlet face in the y-z plane (592 × 592 mm face). It seals across the 593 × 593 mm HEPA footprint zone of the dirty plenum cross-section.

### 8.2 Recommended mounting concept — slide-in cassette

**[PROJ, CALC]** A slide-in cassette arrangement is recommended for the prototype:

1. **Outer frame:** A sheet-metal or 3D-printed frame (approximately 620 × 620 mm outer face, 592 × 592 mm clear opening) is fixed to the tower inlet face at x = 0. The frame is recessed 13 mm from the outer face to provide a stop for the filter panel. Material: galvanised steel sheet (0.8–1.2 mm); or acrylic for visibility.

2. **Filter panel:** Standard 592 × 592 × 48 mm G4 panel slides into the cassette from one side (e.g., from the y = 0 side for access). The slide path has 2 mm clearance per side.

3. **Sealing:** Closed-cell foam gasket (EPDM, 10 mm wide × 6 mm deep) around the perimeter of the frame opening. The filter panel compresses the gasket when fully seated. This prevents bypass air around the filter edges.

4. **Retention:** Snap-in wire clip or spring-loaded latch holds the filter in the seated position. No tools required for removal.

5. **Drainage / drying:** After washing, the filter panel is re-installed dry. The cassette frame has a drainage slot (5 mm gap) at the bottom edge if the filter is accidentally installed wet; this prevents water accumulation.

6. **Bypass sealing:** The frame must cover the full 593 × 593 mm HEPA footprint plus 15–20 mm perimeter on all sides to prevent edge bypass. Any gap between the frame and the tower wall is sealed with foam tape. This is equivalent to the bypassSeal baffle concept already used for the HEPA (Phase 10B) — no gap between dirty plenum and clean path should exist.

7. **Access:** The filter slides out from the front (inlet face) of the tower. No dismantling of internal components required. Target removal time: < 2 minutes.

### 8.3 Orientation

The filter panel is vertical (face normal = CAD x direction). Gravity acts downward (CAD z direction). The synthetic fibre media does not require any particular orientation preference. No special drain orientation is required.

### 8.4 Required structural additions (not yet in CAD)

| Item | Description | Estimated dimensions | Material |
|---|---|---|---|
| Inlet cassette frame | Outer frame with filter stop and gasket seat | 620 × 620 × 30 mm | Galvanised steel or acrylic |
| EPDM foam gasket | Perimeter seal between filter panel and frame | 4 × perimeter strip, 10 mm × 6 mm | EPDM closed-cell foam |
| Wire retention clip | Holds filter panel in seated position | — | SS316 or carbon steel |
| Frame-to-wall seal tape | Prevents edge bypass at frame-wall interface | — | Self-adhesive foam tape |

### 8.5 CAD modification status

**CAD modification is NOT performed in this phase.** Phase 19 provides dimensions and design requirements sufficient for a later CAD update phase. When the CAD is updated:
- Add the cassette frame at CAD x = 0 face
- Replace WATER_STAGE placeholder with PRE_FILTER zone (x = 0.013–0.063 m, 50 mm depth)
- Add sealing annotation at perimeter
- Verify the 592 × 592 mm filter panel clears all structural elements with ≥ 2 mm tolerance

---

## 9. Differential Pressure Monitoring

### 9.1 Purpose

Phase 18 recommended repurposing the DP sensor to monitor pre-filter loading. This section defines the monitoring specification properly.

### 9.2 Pressure tap locations

| Tap | Location | CAD x | Notes |
|---|---|---|---|
| Upstream tap | Dirty plenum, immediately upstream of pre-filter face | x = 0.005 m | Static wall tap; avoid jet from inlet |
| Downstream tap | Dirty plenum, between pre-filter and carbon stage | x = 0.070 m | After filter, before carbon stage |

Both taps are drilled through the tower wall into the dirty plenum. The differential pressure between these two taps is the pre-filter ΔP. The static taps should be 4–6 mm diameter smooth-bored holes, perpendicular to the wall, without burrs. **[REF: ISO 5167, ASHRAE Handbook Fundamentals Ch. 36 — static pressure tap design]**

### 9.3 Expected ΔP range

| Condition | Expected ΔP | Notes |
|---|---|---|
| Filter newly installed (clean) | ~21–30 Pa | G4 at 1.06 m/s [EST] |
| Partially loaded | 30–70 Pa | Rising over weeks/months |
| Maintenance trigger | ~80–100 Pa | Set conservatively below 3× clean |
| Replacement threshold | 100+ Pa | Approaching loaded limit |

### 9.4 Sensor selection

**[PROJ]** The Phase 16/17A rig already specifies the Sensirion SDP810-500Pa (range ±500 Pa, 1 Pa resolution). This sensor is adequate for monitoring the 20–100 Pa range of the pre-filter.

However, for the tower installation (separate from the bench rig), a lower-range sensor provides better resolution at the clean-filter end (~20 Pa):

| Option | Range | Resolution | India availability | Notes |
|---|---|---|---|---|
| Sensirion SDP810-500Pa | ±500 Pa | 1 Pa | Tanotis: ₹4,748.73 confirmed | Already specified for bench rig; covers pre-filter range |
| Sensirion SDP31-125Pa | ±125 Pa | ~0.5 Pa | Not confirmed for India; check Tanotis, Robu.in | Better resolution at clean ΔP end; preferred for tower |
| Testo 510 (handheld) | 0–10,000 Pa | 1 Pa | IndiaMART ₹9,999–12,197 confirmed | Borrow from lab for commissioning checks; not for continuous monitoring |

**Recommendation:** Use the SDP810-500Pa for the tower pre-filter monitoring (same part as bench rig, simplifies procurement). If the SDP31-125Pa becomes available, it is preferable for dedicated long-term pre-filter DP monitoring due to better resolution at clean-filter conditions.

**This is a NEW sensor item** (separate from Phase 17A bench rig M-02). It should be added to the tower procurement list as a separate line item.

### 9.5 Alarm threshold

**[PROJ, EST]** Recommended alarm trigger: **ΔP > 80 Pa** for cleaning notification. This is approximately 3× the expected clean ΔP (25 Pa) and provides notice before the system reaches the maintenance threshold. The exact value should be calibrated after the first cleaning cycle once actual clean ΔP is measured.

### 9.6 Sensor status

**REQUIRES RESOLUTION** — The tower pre-filter DP sensor is a new hardware item not included in Phase 16/17B procurement records. It should be added to the tower BOM as a Phase 19 procurement item. The SDP810-500Pa is confirmed available at ₹4,748.73 (Tanotis); ordering a second unit for the tower is the simplest path.

---

## 10. Maintenance Plan

### 10.1 Visual inspection

Monthly or at any DP alarm event:
1. Check filter for visible dust cake, tears, or media collapse
2. Check gasket condition — look for compression set or cracking
3. Check frame for deformation or corrosion
4. Record DP reading and filter appearance in the project data log

### 10.2 Differential pressure check

At every planned inspection (monthly minimum in polluted outdoor environments):
1. Read pre-filter DP from SDP810 via Raspberry Pi log
2. Compare to baseline DP established at first installation
3. If DP > 80 Pa: initiate cleaning
4. If DP > 100 Pa: cleaning is overdue; check for airflow reduction in system

### 10.3 Cleaning (washable G4 panel)

**[MFR guidance where available; EST otherwise — confirm with selected manufacturer]**

1. Remove filter panel from cassette (slide out toward inlet face)
2. Tap gently to dislodge dry dust cake (outdoors)
3. Rinse with clean water — back-flush recommended (water from downstream face through upstream face)
4. If soiled: dilute neutral detergent (pH 6–8); rinse thoroughly
5. Shake off excess water; allow to air dry COMPLETELY (minimum 2 hours at ambient temperature)
6. **Do NOT reinstall wet.** Wet filter medium in a warm dirty plenum promotes mold growth.
7. Re-inspect after drying; check for media tears
8. Reinstall dry filter; record date in data log; note ΔP at reinstall

**Provisional cleaning interval:** monthly, or when ΔP exceeds 80 Pa (whichever occurs first). Adjust based on actual ΔP rise rate observed after first installation. In very high PM10 environments (> 200 µg/m³), expect weekly cleaning.

### 10.4 Replacement

Replace filter panel (not whole cassette) when:
- Media is torn, collapsed, or permanently deformed
- DP returns to > 60 Pa immediately after washing (media retention exhausted)
- Gasket at filter perimeter fails — replace gasket separately if available
- Filter has completed 12 wash cycles (provisional — adjust from data)

**Provisional replacement interval:** annually for a moderately polluted site (PM10 ~150 µg/m³). Earlier replacement expected at highly polluted sites. Track replacement timing and reason in project data log.

---

## 11. Procurement Recommendation

### 11.1 Preferred product

**Freudenberg Viledon G4 washable panel filter — 592 × 592 × 48 mm or closest standard size**

Rationale:
- Existing supplier relationship (Phase 12A India contact: info@freudenberg-filter.com, +91 20 67633600, Pune)
- Single supplier for both H13 HEPA (SF13-B) and G4 pre-filter reduces enquiry overhead
- Freudenberg is a well-documented industrial filtration manufacturer with traceable test certificates
- Standard EU size 592 × 592 is within their catalogue range

Status: **RFQ REQUIRED** — price, lead time, and availability not yet confirmed.

### 11.2 Backup product

**Camfil G4 washable panel filter (Cam-Flo or equivalent) — 592 × 592 × 48 mm**

Rationale:
- India manufacturing confirmed
- Standard HVAC pre-filter range with EN 779 certification
- Contact: info.in@camfil.com

Status: **RFQ REQUIRED**.

### 11.3 Local / custom alternative

**Generic Indian HVAC washable G4 panel (IndiaMART)**

If Freudenberg and Camfil lead times or costs are prohibitive:
- Search IndiaMART for "washable G4 filter 592×592" or "G4 pre-filter HVAC"
- Verify EN 779 or ISO 16890 test certificate before purchase
- Request datasheet with ΔP vs. face velocity (minimum 2 data points)
- Approximate cost: ₹400–1,500

Status: **CANDIDATE — test certificate verification required before commitment**.

### 11.4 Prototype quantity

For Phase 19/20 commissioning:
- **2 filter panels** (1 in service, 1 available immediately for swap during washing)
- **1 cassette frame** (permanently installed)
- **1 gasket set** (spare EPDM foam tape roll)

### 11.5 RFQ specification

The following specification should be sent to Freudenberg (preferred) and Camfil (backup):

---

**PRE-FILTER RFQ SPECIFICATION — AQI TOWER PHASE 19**

Product type: Coarse pre-filter panel for HVAC air purifier application  
Filter class: G4 per EN 779:2012 or ISO Coarse ≥ 60% per ISO 16890:2016  
Nominal face dimensions: **592 × 592 mm** (or closest standard size; custom 593 × 593 mm acceptable)  
Filter depth: **48 mm** preferred (50 mm acceptable; 96 mm if 48 mm is unavailable in this class)  
Media type: Synthetic fibre (polyester or polypropylene); no glass fibre  
Frame: **Galvanised steel** or aluminium (must be washable — not cardboard)  
Washability: Must survive minimum 12 wash cycles with neutral detergent without media degradation  
Quantity: **2 units** plus 1 spare (total 3)  
Required datasheet data:
- Initial ΔP at minimum **two face velocity points** (e.g., 1.0 m/s and 2.5 m/s)
- Final/recommended change ΔP  
- EN 779:2012 or ISO 16890:2016 test certificate reference  
- Dust holding capacity (g/m²)  
- Temperature limit  
Application face velocity: ~1.05 m/s  
Delivery: India (Pune / Mumbai preferred; national shipping acceptable)  
Required: Price per unit, MOQ, lead time, test certificate copy

---

---

## 12. Final Engineering Decision

### 12.1 Selected specification (provisional — pending RFQ)

**PROVISIONAL SPECIFICATION — RFQ REQUIRED BEFORE FINAL PRODUCT FREEZE**

| Parameter | Selected value |
|---|---|
| Filter class | **G4** (EN 779:2012) or ISO Coarse ≥ 60% (ISO 16890:2016) |
| Nominal face dimensions | **592 × 592 mm** |
| Depth | **48 mm** |
| Media | Synthetic fibre (polyester or polypropylene) — no glass fibre |
| Frame | **Galvanised steel** (washable) |
| Face velocity (at CASE_M_SEALED baseline Q) | **1.057 m/s** |
| Clean ΔP estimate | **~21–30 Pa** at 1.057 m/s [EST] |
| Maintenance ΔP trigger | **80 Pa** (provisional) |
| Predicted Q with clean filter | **~1300–1310 m³/h** (~2–2.5% reduction from 1332) |
| Integration method | Slide-in cassette at inlet face; EPDM gasket; snap clip retention |
| DP monitoring | SDP810-500Pa (same family as bench rig M-02); upstream and downstream wall taps |
| CAD modification | Required in next CAD phase — frame, filter zone, sealing annotation |
| CFD rerun | **NO RERUN REQUIRED** — ΔP is added analytically; flow impact is < 3% (within RANS uncertainty) |
| Procurement status | RFQ required — preferred supplier: Freudenberg; backup: Camfil |

### 12.2 What is still unknown / open risks

| Item | Risk | Mitigation |
|---|---|---|
| Actual clean ΔP from manufacturer | EST range 21–30 Pa may be too wide for precise system budgeting | Send RFQ to Freudenberg and Camfil; request ΔP vs. velocity datasheet |
| Exact inlet opening dimensions | Phase 19 brief says "~420 × 420 mm" (0.176 m²); CFD BC suggests 0.420 m² (0.420 m²); actual requires CAD verification | Open FreeCAD GEO_C model; measure inlet face opening before ordering |
| Service interval in India conditions | Provisional 1-month estimate may be too long for PM10 > 200 µg/m³ | Instrument the pre-filter DP; track ΔP rise rate from commissioning |
| Carbon bed ΔP | Still unmeasured; estimated 20–80 Pa (PRESSURE_DROP_BUDGET) | Phase 17A experiment once hardware available |
| Cassette frame fabrication | No fabrication quote obtained | Include in Phase 19 RFQ or address in CAD phase |
| Pre-filter tower DP sensor | New item not in current procurement tracker | Add to tower BOM as Phase 19 item (SDP810-500Pa, ₹4,748.73 confirmed) |

### 12.3 CFD status

**CFD RERUN: NOT REQUIRED.** Rationale:
- Pre-filter adds approximately linear ΔP to the system; this is captured analytically using the fan curve intersection method (§7)
- The flow impact is ~2–3% of Q, which is smaller than the RANS uncertainty in CASE_M_SEALED (classified PARTIAL NON-CONVERGED)
- The pre-filter is co-located with the existing inlet face; it does not create new geometric complexity in the flow domain
- The system curve update in §7 provides an adequate engineering estimate

A new CFD run would only be warranted if: (a) the actual pre-filter geometry or its position creates a significant flow obstruction (e.g., blockage ratio > 15%) that changes the dirty-plenum velocity distribution approaching the HEPA; (b) the actual pre-filter ΔP is substantially higher than estimated (> 100 Pa clean); or (c) a new tower geometry version is developed.

---

## References

1. EN 779:2012 Particulate Air Filters for General Ventilation — Determination of the Filtration Performance. CEN.
2. ISO 16890-1:2016 Air Filters for General Ventilation — Part 1: Technical specifications, requirements and classification system based upon particulate matter efficiency (ePM). ISO.
3. ASHRAE Handbook Fundamentals (2021) Chapter 32 — Air Cleaners. ASHRAE.
4. Systemair KVO 250 Product Catalog — 6-point fan curve (Phase 6D). Confirmed points: 914 m³/h/388 Pa, 1501 m³/h/0 Pa.
5. Freudenberg Filtration Technologies — SF13-B-0593×0593×292 H13 HEPA product data. India contact: info@freudenberg-filter.com.
6. `docs/PRESSURE_DROP_BUDGET.md` — Phase 6D fan curve; HEPA single-point data; inlet BC area 0.420 m².
7. `docs/FILTER_BYPASS_FIX.md` — CASE_M_SEALED results: Q = 1332 m³/h, fan head 115 Pa, HEPA ΔP 111.2 Pa.
8. `docs/PHASE18_WATER_SPRAY_FEASIBILITY.md` — Phase 18 NO-GO decision; G4/M5 pre-filter approved replacement.
9. `threejs/data/towerConfig.js` — GEO_C zone geometry, HEPA face dimensions, carbon stage zone dimensions.
10. `docs/GEOMETRY_OPTIMIZATION.md` — V01 inlet cross-flow area 0.420 m² reference.
