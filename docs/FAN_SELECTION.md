# Fan Selection — AQI Tower Phase 6D

## Current Phase 7 decision — supersedes older readiness notes below

**KVO 250: PROMISING WITH GEOMETRY ISSUES; NOT A FINAL FAN.** The real supplied six-point curve was run in V01 with the empty tower. The partially converged numerical operating point is approximately 1476 m³/h at 17.33 Pa fan-static-equivalent head, with 32.46 Pa tower static difference. The riser reverse-flow indicator remains about 23%. Stable integrated Q does not mean full residual convergence. See `results/CFD_V01_FAN_RESULTS.md` and `docs/CFD_V01_FAN.md`.

The old unrun 300 Pa V01 placeholder is archived; no future V02 or baffle is needed to complete this terminal-fan study. Original Phase 6 research below is retained as history; its older availability, readiness and placeholder statements are not current execution status. Filters, real adapter losses and physical validation remain absent.

## Status: PRELIMINARY SCREENING — NO SELECTION MADE — KVO 250 EVIDENCE A — 6-POINT FAN CURVE — CFD READY

This document records the fan selection process for the AQI Tower. No fan has been selected. The Systemair KVO 250 has a 6-point fan curve (2 confirmed numeric + 4 graph-digitized, Phase 6D) and is CFD-ready for V02_fan with acknowledged digitization uncertainty. Shutoff head corrected from ~850 Pa (Phase 6C rough estimate) to ~688 Pa (Phase 6D vector extraction). No other candidate holds a confirmed fan curve.

Last updated: 2026-09-05 (Phase 6D complete).

---

## Fan-system physics

### Fan curve
Static pressure rise delivered by the fan as a function of volumetric flow rate Q. At Q = 0 (blocked outlet), pressure is maximum (shutoff head). At ΔP = 0 (free delivery, no resistance), Q is maximum. Real fan curves fall monotonically between these extremes.

### System curve
Total pressure drop across the tower (duct losses + all filter stages) as a function of Q. For turbulent duct flow, system resistance scales approximately as Q². At Q = 0, ΔP_system = 0.

### Operating point
The unique (Q, ΔP) where the fan curve intersects the system curve. Every component change (adding/replacing a filter, changing fan speed) shifts one or both curves.

### Why 33 Pa is not the fan requirement
The V00 CFD empty-tower result of 33 Pa at Q = 1,512 m³/h (placeholder flow, non-converged) is one additive term in the system curve. Filter stages add 150–700 Pa or more. The actual system total ΔP is entirely unknown until at least one filter-stage ΔP is measured or sourced. A fan capable of only 33–50 Pa would be completely inadequate for a real filtration system.

### Why the 250–700 Pa screening range is preliminary
This range was estimated from published HEPA H13 literature values (150–250 Pa at ~1 m/s face velocity) plus the empty-tower V00 result. It has NOT been confirmed by any product-specific measurement. Three scenarios are tracked: Low (100–200 Pa), Moderate (200–400 Pa), High (400–700 Pa). See `docs/FAN_DATA_GAPS.md` for scenario implications.

---

## Comparison table

| Candidate | Type | Blade | Manufacturer | Model | Voltage | Power (W) | Free-del. Q | Max ΔP (Pa) | Fan curve | Evidence | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ebm-papst G2E140-AE77-01 | Centrifugal, AC | Forward-curved | ebm-papst | G2E140-AE77-01 | 230V AC | 105 (50Hz) | ~370 m³/h | 50 Pa THERMAL LIMIT (UNCONFIRMED) | Not extracted | D | TME, RS Online US, ebmpapst.com manual |
| ebm-papst G2E140-AI28-A5 | Centrifugal, AC | Forward-curved | ebm-papst | G2E140-AI28-A5 | 230V AC | UNKNOWN | ~500 m³/h | UNKNOWN | Not extracted | D | RS Online UK export |
| ebm-papst R2E225-RA92-09 | Centrifugal, AC (RadiCal) | Backward-curved | ebm-papst | R2E225-RA92-09 | 230V AC | 155 (50Hz) | 705 OR 1301 m³/h¹ | ~425 Pa² | Available, not read | C | RS Online UK/US, Mouser |
| ebm-papst R2E225-RA92-23 | Centrifugal, AC (RadiCal) | Backward-curved | ebm-papst | R2E225-RA92-23 | 230V AC | UNKNOWN | ~1300 m³/h | ~580 Pa³ | Available, not read | C | EquipSpares |
| Systemair KVO 250 | Centrifugal duct fan, AC | Backward-curved | Systemair | KVO 250 | UNKNOWN | 301 | 1501 m³/h | UNKNOWN | Available, not read | B | Systemair datasheet summary |

**Notes on table values:**

¹ R2E225-RA92-09 airflow discrepancy: RS Online UK lists 705 m³/h; RS Online US lists 766 CFM = 1301 m³/h for the same model number. Discrepancy unresolved — may reflect different impeller widths, different measurement conditions, or listing error. Do not use either value for sizing without resolving.

² R2E225-RA92-09 max static pressure: 425 Pa stated in a search result summary referencing distributor data. Not directly extracted from manufacturer PDF. TREAT AS INDICATIVE ONLY.

³ R2E225-RA92-23 max static pressure: 2.33 inH₂O × 249.1 Pa/inH₂O = 580 Pa. Converted from EquipSpares listing. Original value: 2.33 inH₂O. TREAT AS INDICATIVE ONLY.

All values should be verified from manufacturer PDF datasheets before engineering use.

---

## Critical finding: G2E140 series — forward-curved blade thermal limit

A maximum back pressure of approximately 50 Pa was cited in search result summaries referencing the G2E140-AE77-01 operating instructions (ebmpapst.com). Forward-curved centrifugal fans have an overloading power characteristic: as system resistance increases and flow decreases, the electrical power drawn by the motor continues to rise, eventually causing thermal overload.

**Implication for this project:** If the AQI Tower system resistance is 250–700 Pa, operating a G2E140 forward-curved fan against this resistance would cause sustained motor overheating and thermal shutdown. The G2E140 series appears to be designed for equipment cooling applications with low back pressure, not for high-resistance filtration systems.

**This finding has NOT been confirmed from a direct read of the manufacturer PDF.** It must be verified before the G2E140 series is formally rejected. The operating instructions PDF is available at `img.ebmpapst.com/products/manuals/G2E140AE7701-BA-ENU.pdf`.

If confirmed: reject all G2E140 candidates.
If refuted: re-evaluate G2E140 against the full fan curve.

---

## Fan architecture options (updated Phase 6B)

The "four fans" concept from Phase 6 was a hypothesis. Phase 6B evaluates it more carefully.

### Option A: Four axial fans in parallel at inlet

**Assessment:** Axial fans typically deliver 50–150 Pa static pressure at useful diameters (200–500 mm). For Scenario L (100–200 Pa system), borderline. For Scenario M or H, insufficient. **Preliminary verdict: UNLIKELY VIABLE for filtration applications.**

### Option B: Centrifugal blowers on suction side (push-through)

**Assessment:** One or more centrifugal fans drawing air through the filter stages. High pressure capability (backward-curved EC/AC). Filter contamination risk (fan impeller exposed to dirty air from inlet side unless placed after filtration). **If placed after filtration (suction side at filter exit):** impeller handles cleaner air. **Preliminary verdict: VIABLE architecture pending fan curve verification.**

### Option C: Push-pull split (fans at both inlet and outlet)

**Assessment:** Two fans at inlet (push) and two at outlet (pull) approximately share the total system ΔP, each seeing roughly half. Reduces requirement per fan. Adds control complexity. **Preliminary verdict: POSSIBLE for Scenario H if single fan cannot cover full ΔP.**

### Option D: Single large centrifugal blower

**Assessment:** One large blower (KVO 315 or equivalent industrial) can deliver 2000+ m³/h and 400–800 Pa. Simpler control. Potential acoustic advantage (lower RPM for same flow). Geometric constraint: 315mm circular duct fan weighs 27 kg and requires duct transitions. **Preliminary verdict: VIABLE if tower geometry permits; needs layout check.**

### Option E: Fans at riser exit (pull-through)

**Assessment:** Fans mounted at or above AIR_OUTLET, pulling air through all stages. Fan impeller handles clean output air. Easier maintenance access. Fan must handle full system ΔP (high pressure requirement). **Preliminary verdict: VIABLE architecture, potentially best for impeller longevity.**

### Updated architecture guidance (NOT a recommendation)

- The number of fans (1, 2, or 4) should be determined by the intersection of the fan curve with the system curve — not assumed in advance.
- Parallel arrangement: at same ΔP, total Q increases approximately as N × Q_single. Parallel fans are appropriate when Q is the limiting factor.
- Series arrangement: at same Q, total ΔP increases approximately as N × ΔP_single. Series fans are appropriate when pressure is the limiting factor and single-fan shutoff head is insufficient.
- The appropriate architecture cannot be determined until system ΔP scenarios are bounded by at least one real filter measurement.

---

## Fan candidates: detailed assessments

### Candidate 1: ebm-papst G2E140-AE77-01

**Type:** Forward-curved centrifugal, AC, single inlet, 230V, 105W (50Hz), 370 m³/h free delivery, IP44

**Why it was initially identified:** Compact EC/AC centrifugal fan series, India distributor found (MS Enterprises, New Delhi). Four units would nominally cover ~1480 m³/h.

**Why it is likely unsuitable:** Forward-curved blade design. Maximum back pressure reported as 50 Pa (unconfirmed from PDF). If confirmed, this fan would experience thermal overload at any operating point in the 250–700 Pa system resistance range. The design is intended for low-resistance equipment cooling, not HVAC filtration.

**Evidence level:** D — secondary sources only, no fan curve.

**Verdict:** Tier 3 — LOW CONFIDENCE / LIKELY REJECTED. Confirm from manufacturer PDF.

### Candidate 2: ebm-papst G2E140-AI28-A5

**Type:** Forward-curved centrifugal, AC, single inlet, 230V, 500 m³/h free delivery

**Assessment:** Higher free-delivery flow than G2E140-AE77-01 but same forward-curved series. Same thermal overload risk assumed. Datasheet not retrieved.

**Evidence level:** D — single distributor listing, no performance data beyond airflow.

**Verdict:** Tier 3 — LOW CONFIDENCE / LIKELY REJECTED.

### Candidate 3: ebm-papst R2E225-RA92-09 (RadiCal backward-curved)

**Type:** Backward-curved RadiCal motorized impeller, AC, single inlet, 230V, 155W (50Hz), 225mm diameter

**Why this is better than G2E140:** Backward-curved (RadiCal®) blades are non-overloading — power draw peaks and then decreases at shutoff. Safe to operate at high back pressure without thermal overload risk. Maximum static pressure ~425 Pa (indicative from distributor data, unconfirmed from manufacturer PDF).

**Key data discrepancy:** Free-delivery airflow listed as either 705 m³/h (RS Online UK) or 1301 m³/h (RS Online US). Unresolved — must be read directly from manufacturer PDF.

**Integration note:** Motorized impeller design — no integral scroll housing. Requires mechanical integration inside the tower.

**Evidence level:** C — distributor data with partial performance numbers.

**Verdict:** Tier 2 — POTENTIALLY SUITABLE. Max static pressure in useful range if confirmed. Needs manufacturer PDF with fan curve.

### Candidate 4: ebm-papst R2E225-RA92-23 (RadiCal backward-curved)

**Type:** Backward-curved RadiCal motorized impeller, AC, 230V, ~1300 m³/h free delivery, ~580 Pa max static pressure

**Why promising:** Higher maximum static pressure than RA92-09 (580 Pa vs 425 Pa indicative). Covers the full Scenario M range and the lower end of Scenario H. Free-delivery flow of 1300 m³/h per unit is substantial — a single or dual unit may suffice for flow.

**Key uncertainty:** Only one distributor source found (EquipSpares). Model number suffix -RA92-23 not confirmed as standard catalog product. Voltage, power at rated conditions not confirmed.

**Evidence level:** C — single distributor source with partial data.

**Verdict:** Tier 2 — POTENTIALLY SUITABLE. Best pressure-capability candidate found so far. Needs manufacturer PDF with fan curve, and confirmation that it is a standard product.

### Candidate 5: Systemair KVO 250 (backward-curved duct fan)

**Type:** Complete circular duct fan, backward-curved, AC external rotor motor, 250mm duct connection, 301W, 1501 m³/h free delivery, 20 kg

**Why promising:** Complete duct-connected unit (no integration housing needed). Large free-delivery flow (1501 m³/h). Backward-curved = non-overloading. Manufacturer (Systemair) has India operations.

**Fan curve status (Phase 6D):** 6 points — 2 confirmed numeric + 4 graph-digitized via PyMuPDF vector path extraction. CFD READY WITH DIGITIZATION UNCERTAINTY. Shutoff head **~688 Pa ±20 Pa** (CORRECTED from Phase 6C estimate of ~850 Pa ±100 Pa). The actual shutoff head is lower than previously estimated, reducing but not eliminating headroom for Scenario M/H operation.

**Evidence level:** A — official Systemair catalog PDF read directly (Phase 6C); fan curve fully digitized (Phase 6D).

**Verdict:** Tier 1 — BEST CANDIDATE — CFD READY. Needs baffle face area from CAD and V02_fan mesh implementation before CFD with real fan BC.

---

## Operating point estimation

**A preliminary estimate is available (VERY LOW confidence).** See `docs/PRESSURE_DROP_BUDGET.md` for derivation.

Preliminary estimate (KVO 250 + empty tower + one clean HEPA, no other stages):  
**Q ≈ 1300 m³/h, ΔP ≈ 133 Pa**

This estimate uses the 6-point KVO 250 fan curve (Phase 6D) and a single-point linear extrapolation of the Freudenberg HEPA ΔP. It excludes prefilter, biochar, wet scrubber, filter loading, and minor losses. The real operating point will be at lower Q and higher ΔP when all stages are included. Do not cite as a design point or CADR claim.

System curve approach when more filter data become available:
1. Build the system curve: ΔP_sys(Q) = ΔP_empty(Q) + ΔP_filters(Q) + …
2. Empty-tower term: ΔP_empty ≈ 33 × (Q/1512)² Pa (rough Q² scaling from V00, non-converged).
3. Each filter term requires manufacturer filter performance data (ΔP vs. face velocity at the tower's filter face area).
4. Plot both curves. Intersection is the operating point.
5. Verify the operating point is on the stable (downward-sloping) portion of the fan curve.

**REMINDER:** The 250–700 Pa screening range is preliminary. Do not cite it as a requirement.

---

## India availability summary

| Candidate | Availability evidence | Distributor/contact |
|---|---|---|
| G2E140-AE77-01 | Partial — ebm-papst India PVT LTD and MS Enterprises New Delhi cited | indiamart.com listing for MS Enterprises |
| G2E140-AI28-A5 | Same distributor assumed | Same |
| R2E225-RA92-09 | Partial — same ebm-papst India channels | Requires direct inquiry for this specific model |
| R2E225-RA92-23 | NOT FOUND in India | Requires direct inquiry |
| Systemair KVO 250 | Partial — Systemair India operates | Requires direct inquiry to Systemair India |

---

## Files created/updated in Phase 6B

| File | Content |
|---|---|
| `docs/FAN_SELECTION.md` | This document — Phase 6B comparison table and assessments |
| `docs/FAN_DATA_GAPS.md` | Detailed gap analysis, scenario analysis, recommended next actions |
| `data/fans/ebmpapst_G2E140_AE77-01.json` | Structured data record: G2E140-AE77-01 |
| `data/fans/ebmpapst_G2E140_AI28-A5.json` | Structured data record: G2E140-AI28-A5 |
| `data/fans/ebmpapst_R2E225_RA92-09.json` | Structured data record: R2E225-RA92-09 |
| `data/fans/ebmpapst_R2E225_RA92-23.json` | Structured data record: R2E225-RA92-23 |
| `data/fans/systemair_KVO_250.json` | Structured data record: Systemair KVO 250 |
| `data/fans/README.md` | Minimum datasheet requirements (unchanged from Phase 6) |

---

## Files created/updated in Phase 6C

| File | Change |
|---|---|
| `docs/FAN_SELECTION.md` | This document — Phase 6C section added, status updated |
| `docs/FAN_CURVE_AUDIT.md` | NEW — per-candidate fan curve source and CFD readiness audit |
| `docs/PRESSURE_DROP_BUDGET.md` | Updated — Known/Unknown/Placeholder/Future sections; preliminary operating point |
| `docs/FAN_DATA_GAPS.md` | Updated — tier classifications revised for Phase 6C findings |
| `data/fans/ebmpapst_G2E140_AE77-01.json` | Evidence D→B; thermal-limit misinterpretation corrected; motor specs confirmed |
| `data/fans/systemair_KVO_250.json` | Evidence B→A; all specs confirmed; fan curve points added |
| `data/fans/ebmpapst_R2E225_RA92-09.json` | Airflow discrepancy resolved; motor specs updated |
| `data/filters/README.md` | NEW — minimum filter datasheet requirements |
| `data/filters/freudenberg_SF13B_593x593x292.json` | NEW — first real HEPA H13 filter data point |

---

## Phase 6C findings

### What was attempted

Three manufacturer PDF sources were targeted for direct reading:
1. ebm-papst G2E140-AE77-01 operating instructions — `img.ebmpapst.com/products/manuals/G2E140AE7701-BA-ENU.pdf` — **READ SUCCESSFULLY**
2. ebm-papst R2E225-RA92-09 operating instructions — `img.ebmpapst.com/products/manuals/R2E225RA9209-BA-ENU.pdf` — **FAILED (binary PDF, not text-extractable)**
3. Systemair KVO 250 catalog — `planetaklimata.com.ua/instr/Systemair/Systemair_Fans_KVO_Data_sheet_Eng.pdf` — **READ SUCCESSFULLY**

HEPA H13 filter data from Freudenberg Filtration Technologies was obtained from their product catalog website.

### Critical correction: G2E140-AE77-01 thermal limit misinterpretation

Phase 6B flagged the G2E140-AE77-01 as "LIKELY UNSUITABLE" due to a "50 Pa maximum back pressure" claim from search result summaries. Phase 6C read the actual manufacturer operating instructions and found:

- Section 3.2 lists "Min. back pressure: 0 Pa (50 Hz) / 50 Pa (60 Hz)"
- This is the **MINIMUM** back pressure of the factory test condition (method "ml" = max load test), **not a maximum operating limit**
- Forward-curved fans are thermally at risk at **LOW** back pressure (free delivery), not high back pressure — the thermal risk is reversed from what was stated in Phase 6B
- The operating instructions contain **no fan curve** — only electrical/thermal nominal data

**Result:** The G2E140-AE77-01 cannot be rejected on thermal grounds from the operating instructions. It remains Tier 3 due to absence of a performance datasheet, not thermal unsuitability. Evidence upgraded D → B.

### KVO 250: Evidence A upgrade and partial fan curve

The Systemair KVO catalog was read directly. Results:

- All electrical/mechanical specs confirmed (230V/50Hz, 301W, 1.33A, 2480 RPM, IP44, 20 kg, F insulation, 7 µF capacitor)
- **Two confirmed fan curve points** from the acoustic data table:
  - (Q = 915 m³/h, ΔP = 388 Pa) — confirmed acoustic measurement operating point
  - (Q = 1501 m³/h, ΔP = 0 Pa) — confirmed free delivery
- **One estimated shutoff point** from the graphical fan curve: ΔP ≈ 850 Pa ±100 Pa at Q = 0

Evidence upgraded B → A. Fan curve is partially known. **3 points are insufficient for the OpenFOAM fan BC (minimum 5 needed).** The V01_fan placeholder case remains the best available CFD option.

### R2E225-RA92-09: fan curve still not obtained

Both attempted PDF sources (Mouser specsheet and ebm-papst operating instructions) returned binary content and could not be parsed. Evidence remains C. The 705 m³/h figure at 50 Hz is confirmed from multiple distributor sources. Fan curve (and shutoff head) are unconfirmed.

### Filter data: first real data point obtained

Freudenberg Filtration Technologies H13 HEPA filter (SF13-B-0593x0593x292, galvanized steel frame, MiniPleat):
- 300 Pa initial ΔP at rated face velocity 2.84 m/s (Q = 3600 m³/h through 593×593 mm face)
- Linear extrapolation to AQI Tower placeholder flow (1512 m³/h → face velocity ~1.19 m/s): ΔP ≈ 126 Pa
- Single point only — no full ΔP-v curve

This is the first real manufacturer filter data in this project. It cannot replace a multi-point curve but provides an order-of-magnitude anchor for HEPA contribution to system resistance.

### Preliminary operating point (ROUGH ORIENTATION ONLY)

With the KVO 250 partial fan curve and the Freudenberg HEPA single-point extrapolation, a preliminary system curve intersection was calculated:

**Q_operating ≈ 1300 m³/h, ΔP_operating ≈ 133 Pa**

This estimate includes: empty tower (33 Pa scaled from V00) + one clean HEPA (linear scaling from Freudenberg data).
This estimate EXCLUDES: prefilter, biochar bed, wet scrubber, filter loading, minor losses, real tower geometry corrections.

Do not cite this as a design point or a CADR claim. It is an orientation figure showing that the KVO 250 operating Q with a real HEPA filter is roughly in the 1000–1400 m³/h range for Scenario L conditions.

### V01_fan CFD readiness

**The V01_fan placeholder case (300 Pa totalPressure BC) is ready to run** — no new fan curve data is required for it. It demonstrates tower flow structure with an assumed driving pressure, not a real fan curve.

**A real fan BC case (V02_fan) requires at minimum 5 KVO 250 fan curve points** — currently 3 are available (2 confirmed + 1 estimated). Two more digitized points from the Systemair catalog graph are needed.

---

## Candidate status after Phase 6D

| Candidate | Evidence | Fan curve | Tier | Status |
|---|---|---|---|---|
| G2E140-AE77-01 | B (upgraded from D in Phase 6C) | NO — performance datasheet not yet obtained | 3 | Re-evaluation pending performance datasheet |
| G2E140-AI28-A5 | D | NO | 3 | Low priority |
| R2E225-RA92-09 | C | NO — PDF unreadable | 2 | Potentially suitable; PDF source needed |
| R2E225-RA92-23 | C | NO | 2 | Potentially suitable; PDF source needed |
| KVO 250 | **A** | **6 POINTS — 2 confirmed + 4 graph-digitized (Phase 6D)** | **1** | **CFD READY WITH DIGITIZATION UNCERTAINTY** |

---

## Files created/updated in Phase 6D

| File | Change |
|---|---|
| `data/fans/systemair_KVO_250.json` | Fan curve expanded to 6 points; shutoff head corrected to 688 Pa; CFD status updated |
| `docs/FAN_CURVE_AUDIT.md` | Phase 6D section added; KVO 250 updated to CFD READY; extraction method documented |
| `docs/PRESSURE_DROP_BUDGET.md` | K3 table updated to 6-point curve; shutoff head corrected; operating point note updated |
| `docs/FAN_DATA_GAPS.md` | KVO 250 updated to CFD READY; Phase 6D completion recorded |
| `docs/FAN_SELECTION.md` | This document — Phase 6D section and status update |
| `README.md` | Phase updated to Phase 6D complete |

---

## What to do next

1. ~~**Digitize 2+ additional KVO 250 fan curve points**~~ — COMPLETED Phase 6D. 6-point curve extracted and documented.
2. **Confirm baffle face area from Phase 4 FreeCAD CAD model** (250mm duct → 0.0491 m² nominal, confirm vs. CAD). Then implement V02_fan `fan` BC using the 6-point table.
3. **Obtain the ebm-papst G2E140-AE77-01 performance datasheet** (separate from operating instructions) to determine shutoff head and re-evaluate or formally reject.
4. **Find a text-readable R2E225-RA92-09 fan curve** — contact ebm-papst India directly, or search for an HTML datasheet source.
5. **Obtain multi-point HEPA ΔP curve** from Freudenberg or equivalent supplier (contact required — no web source found).
6. **Confirm tower filter face area** from Phase 4 FreeCAD CAD model (required to convert Q to face velocity).
7. **Select and obtain prefilter ΔP data** (G4/M5/F7 class).
8. Once at least prefilter + HEPA ΔP data are known: run V02_fan with real fan BC and plot system-curve intersection.
