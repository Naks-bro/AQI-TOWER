# Fan Data Gaps — AQI Tower Phase 6D

## Current Phase 7 update

Actual KVO 250 empty-tower V01 has been run: approximately 1476 m³/h at 17.33 Pa fan-static-equivalent head, PARTIAL / NON-CONVERGED. Classification: PROMISING WITH GEOMETRY ISSUES, not final selection. The six-point curve is unchanged. The old V01 placeholder is archived, and no baffle is required for the selected terminal-suction representation. See `docs/CFD_V01_FAN.md` and `results/CFD_V01_FAN_RESULTS.md`.

Remaining gaps: real adapter/installation losses, numerical and mesh validation, target airflow/application approval, filter-stage pressure-loss curves, manufacturer curve uncertainty and physical testing. Original Phase 6 sections below remain historical; statements that no curve or no Evidence A candidate exists are superseded by the later Phase 6D record and this update.

## Status: PHASE 6D COMPLETE — KVO 250 EVIDENCE A — FAN CURVE 6 POINTS (CFD READY) — FIRST FILTER DATA OBTAINED

This document records what was found and what remains missing after the Phase 6B fan data acquisition research (2026-09-05). No candidate has reached Evidence Level A (official manufacturer datasheet with fan curve directly read and verified).

---

## Evidence level definitions

| Level | Meaning |
|---|---|
| A | Official manufacturer datasheet with fan curve directly obtained and verified |
| B | Official manufacturer page or datasheet with substantial performance data but incomplete curve |
| C | Distributor or authorized reseller data with partial performance numbers |
| D | Secondary source only; no fan curve, no complete performance data |

---

## Candidate summary (updated Phase 6C)

| Candidate | Evidence | Free-delivery Q | Max ΔP (Pa) | Fan curve | Suitability | Action required |
|---|---|---|---|---|---|---|
| ebm-papst G2E140-AE77-01 | **B** (upgraded) | ~370 m³/h (distributor) | UNKNOWN (thermal-limit claim was misinterpretation) | NOT in operating instructions — performance datasheet needed | Re-evaluation pending | Obtain performance datasheet (separate from operating instructions) |
| ebm-papst G2E140-AI28-A5 | D | ~500 m³/h | UNKNOWN | Not extracted | LIKELY LOW PRIORITY | Low priority pending G2E140-AE77-01 performance datasheet |
| ebm-papst R2E225-RA92-09 | C | **705 m³/h at 50 Hz (resolved)** | ~425 Pa (indicative, unconfirmed) | PDF unreadable (binary) | Potentially suitable | Find text-readable fan curve source |
| ebm-papst R2E225-RA92-23 | C | ~1300 m³/h | ~580 Pa (indicative, converted from inH₂O) | Not extracted | Potentially suitable | Read manufacturer PDF; verify model is standard |
| Systemair KVO 250 | **A** (upgraded) | **1501 m³/h (confirmed)** | **~688 Pa ±20 Pa (Phase 6D vector extraction — CORRECTED from 850 Pa)** | **6 POINTS — 2 confirmed, 4 graph-digitized** | **TIER 1 — CFD READY WITH DIGITIZATION UNCERTAINTY** | Confirm baffle face area from CAD; implement V02_fan |

---

## Phase 6C finding: G2E140 thermal-limit claim was a misinterpretation

**CORRECTED in Phase 6C.** The operating instructions PDF was read directly. Section 3.2 lists "Min. back pressure: 0 Pa (50 Hz) / 50 Pa (60 Hz)". This is the **MINIMUM** back pressure of the factory test condition (method "ml" = max load test), not a maximum operating limit.

Forward-curved fans are thermally at risk at **LOW** back pressure (free delivery / high airflow), because power consumption rises as back pressure decreases. The thermal protector (TOP) is designed to trip if the motor overloads due to running at high flow with insufficient resistance — the opposite of what Phase 6B assumed.

**Result:** The G2E140-AE77-01 CANNOT be rejected on thermal grounds from the operating instructions alone. The phase 6B "LIKELY UNSUITABLE" verdict was incorrect. The fan remains Tier 3 only because its aerodynamic performance (shutoff head, fan curve) is unknown — that requires a separate performance datasheet not yet obtained.

The operating instructions PDF contains NO aerodynamic fan curve.

---

## What information is available

| Data field | G2E140-AE77-01 | G2E140-AI28-A5 | R2E225-RA92-09 | R2E225-RA92-23 | KVO 250 |
|---|---|---|---|---|---|
| Manufacturer confirmed | YES | YES | YES | YES | YES |
| Model number confirmed | YES | YES | YES | PARTIAL (suffix -L02 unclear) | YES |
| Voltage | 230V AC | 230V AC | 230V AC | 230V AC | UNKNOWN |
| Power (W) | 105/115W | UNKNOWN | 155/210W | UNKNOWN | 301W |
| RPM | 1400/1500 | UNKNOWN | 2500/2600 | 2500 | 2480 |
| Free-delivery flow | ~370 m³/h | ~500 m³/h | 705 or 1301 m³/h (discrepancy) | ~1300 m³/h | 1501 m³/h |
| Max static pressure | 50 Pa (thermal limit, UNCONFIRMED) | UNKNOWN | ~425 Pa (INDICATIVE) | ~580 Pa (INDICATIVE, converted from inH₂O) | UNKNOWN |
| Fan curve (numeric) | NOT EXTRACTED | NOT EXTRACTED | NOT EXTRACTED | NOT EXTRACTED | NOT EXTRACTED |
| Blade type confirmed | Forward-curved | Forward-curved (assumed same series) | Backward-curved (RadiCal) | Backward-curved (RadiCal) | Backward-curved (sizes 200-315) |
| Dimensions | 227×248×130mm (approx) | 247×226×130mm (approx) | 225mm Dia × 99-101mm | 225mm Dia (depth unknown) | 250mm duct connection |
| IP rating | IP44 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Noise (dB(A)) | 59 | UNKNOWN | 69 | UNKNOWN | 52 at 3m |
| Weight | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | 20 kg |
| India availability | Partial (distributor named) | Partial (same distributor) | Partial (distributor named) | UNKNOWN | Partial (Systemair India) |
| Price | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

---

## What information remains missing

### Missing for all candidates
1. **Complete fan curve** (at least 5 (Q, ΔP_static) points, including shutoff and free-delivery) — none retrieved.
2. **Fan curve at rated speed** — required for OpenFOAM fan BC. Without this, V01_fan cannot use a real fan curve.
3. **Confirmed operating point** against the AQI Tower system curve — not calculable without fan curve AND complete system resistance.

### Missing for G2E140 candidates
1. Official confirmation of 50 Pa maximum back pressure from manufacturer PDF.
2. Power, RPM data for G2E140-AI28-A5.
3. Fan curve (aerodynamic, not just the thermal limit).

### Missing for R2E225 candidates
1. Direct read of manufacturer datasheet PDF with fan curve table.
2. Resolution of the 705 m³/h vs 1301 m³/h airflow discrepancy for R2E225-RA92-09.
3. Confirmation that R2E225-RA92-23 is a standard catalog product (not customer-specific variant).
4. Actual voltage, power at rated conditions for R2E225-RA92-23.
5. India stock/availability confirmation.

### Missing for Systemair KVO 250
1. Maximum static pressure (shutoff head) in Pa.
2. Fan curve (fan performance is characterized in Systemair datasheets but was not extracted).
3. Supply voltage confirmation.
4. India availability and pricing.

---

## Candidates ready for CFD (Tier 1)

**KVO 250 — CFD READY (Phase 6D).** The KVO 250 has Evidence A data (manufacturer catalog read directly) and 6 fan curve points (2 confirmed numeric + 4 graph-digitized via PyMuPDF vector extraction). This meets the 5-point minimum for the OpenFOAM `fan` boundary condition. CFD STATUS: CFD READY WITH GRAPH-DIGITIZATION UNCERTAINTY.

**SHUTOFF HEAD CORRECTED (Phase 6D):** Phase 6C estimated ~850 Pa ±100 Pa. Phase 6D PyMuPDF vector extraction yields ~688 Pa ±20 Pa — outside the previous uncertainty range. All documents have been updated.

**Remaining blocker for V02_fan:** Confirm fan baffle face area from the Phase 4 FreeCAD CAD model and implement the `fan` BC (requires createBaffles mesh step). The existing V01_fan case uses a placeholder totalPressure BC (300 Pa) and can be run now.

---

## Tier 1 candidates (CFD-near-ready, needs curve completion)

1. **Systemair KVO 250** — Evidence A. Backward-curved, 1501 m³/h confirmed free delivery, shutoff ~688 Pa (CORRECTED, Phase 6D). **6 fan curve points (2 confirmed + 4 graph-digitized) — CFD READY WITH DIGITIZATION UNCERTAINTY.** Preliminary operating point (one clean HEPA): Q≈1300 m³/h at ~133 Pa. Remaining V02_fan blocker: baffle face area from CAD + createBaffles mesh step.

## Tier 2 candidates (potentially suitable, data incomplete)

These candidates are not disqualified by the available data and warrant further investigation:

1. **ebm-papst R2E225-RA92-09** — Backward-curved RadiCal, ~425 Pa max static pressure (indicative, unconfirmed), 705 m³/h at 50 Hz (confirmed from distributors), 230V AC, 225mm. Fan curve PDF unreadable — alternative text source needed.
2. **ebm-papst R2E225-RA92-23** — Backward-curved RadiCal, ~580 Pa max static pressure (indicative, converted from inH₂O), ~1300 m³/h, 230V AC. Single distributor source — model standard-catalog status not confirmed.

## Tier 3 candidates (re-evaluation needed or low confidence)

1. **ebm-papst G2E140-AE77-01** — Forward-curved, evidence B. The thermal-limit rejection from Phase 6B was incorrect (see Phase 6C finding above). Cannot be formally rejected or accepted without a performance datasheet containing the aerodynamic fan curve. Currently no data on shutoff head. Remains Tier 3 due to data gap, not confirmed unsuitability.
2. **ebm-papst G2E140-AI28-A5** — Forward-curved, evidence D. Low priority until G2E140-AE77-01 performance datasheet is obtained.
3. **Delta Electronics BFB1012 series** — Research found only small electronics-cooling blowers (~65 m³/h, 97×94mm frame). Far too small. REJECTED — insufficient scale.

---

## System resistance scenarios (three-scenario analysis)

Per Phase 6 instructions, we should not assume the 250–700 Pa screening range is correct. Three scenarios:

### Scenario L — Low system resistance (100–200 Pa total)
Would apply if: only one filter stage is used, HEPA is lightly loaded, or filter face area is very large (low face velocity).
Fan implication: A moderate-pressure centrifugal fan suffices. Even the G2E140 might be usable if 50 Pa thermal limit can be exceeded by using a better-suited fan. R2E225 at ~425 Pa would be well-matched and operate efficiently.

### Scenario M — Moderate system resistance (200–400 Pa total)
Would apply if: prefilter + HEPA H13 (standard face velocity, clean condition) + low duct losses.
Fan implication: R2E225-RA92-09 (425 Pa max) may just cover this range at low flow. R2E225-RA92-23 (580 Pa) would provide more headroom. KVO 250 depends on its (unknown) shutoff head.

### Scenario H — High system resistance (400–700 Pa total)
Would apply if: prefilter + loaded HEPA H13 + biochar bed + duct losses accumulate.
Fan implication: R2E225-RA92-09 (425 Pa) may be insufficient. R2E225-RA92-23 (580 Pa) is borderline. KVO 250 (pressure unknown) may or may not cover this. Industrial centrifugal blower with higher shutoff head (e.g., 700–1000 Pa) may be needed. This scenario would likely require a different class of fan (backward-curved blower with external belt drive or large EC impeller) not yet researched.

The scenario analysis shows that:
- If the system lands in Scenario L or M: R2E225 series or KVO 250 may be adequate.
- If the system lands in Scenario H: additional research into higher-pressure blowers is required.
- Scenario cannot be determined without at least one real filter ΔP measurement.

---

## Architecture analysis: number of fans

Per Phase 6 instructions, the "four fans" assumption from the previous phase must not be locked in. The following options were considered:

| Architecture | Suitable fan | Pros | Cons |
|---|---|---|---|
| 1× large centrifugal | KVO 315 or larger industrial | Simpler control, potentially quieter | Single point of failure, geometric constraint, 27 kg |
| 2× medium centrifugal in parallel | R2E225 or KVO 250 | Redundancy, better flow uniformity | Two units in parallel approximately doubles Q at same ΔP — must verify on fan curve |
| 4× small centrifugal in parallel | R2E225 (225mm units) | High redundancy, flexible placement | Four units at 180–300 Pa system ΔP each deliver 325-700 m³/h → 1300-2800 m³/h total (rough, speculative) |
| Series arrangement | Any | Can stack ΔP capability | Not appropriate here — parallel paths to same outlet means series adds no benefit; series means flow passes through both fans which adds complexity and duct length |

**Parallel vs. series note:** In this tower, fans are likely in parallel paths or all acting on the same air stream. True series arrangement (two fans in the same duct) would approximately double ΔP at same Q — useful when system resistance is very high and no single fan can provide enough pressure. This should only be explored if Scenario H is confirmed and single-fan pressure is insufficient.

**Preliminary architecture guidance (NOT a recommendation):**
- 1–2 units of R2E225-RA92-23 or KVO 250 covers Scenario M airflow with one or two units.
- If Scenario H confirmed, neither currently researched candidate is confirmed sufficient, and a different fan class is needed.
- Architecture cannot be locked until fan curves AND at least one filter ΔP are known.

---

## Exact data required before V01 fan CFD with real fan curve

1. Complete (Q, ΔP_static) table — at least 5 points covering shutoff to free delivery — for one fan at rated voltage, rated frequency, rated speed.
2. Confirmation that the table applies to the exact model being used (not a related variant).
3. Duct or baffle face area at the fan location in the tower (to convert volume flow to face velocity in OpenFOAM).
4. Whether the fan operates at fixed speed or variable speed (EC fans); if variable, curve at the intended speed setting.

---

## Recommended next actions (priority order, Phase 6C)

1. ~~**Digitize 2+ KVO 250 fan curve points from Systemair catalog graph.**~~ **COMPLETED Phase 6D.** 6-point curve extracted via PyMuPDF vector path; shutoff head corrected; V02_fan fan BC unblocked (pending CAD baffle face area).
2. **Obtain ebm-papst G2E140-AE77-01 PERFORMANCE DATASHEET** (distinct from operating instructions — the performance datasheet contains the fan curve). Confirm or rule out the G2E140 series for this application.
3. **Find a text-readable R2E225-RA92-09 fan curve.** Both mouser.com and img.ebmpapst.com PDFs are binary and unreadable by web fetch. Options: contact ebm-papst India directly; find an HTML datasheet page; or request the datasheet as a text/Excel file.
4. **Obtain multi-point HEPA ΔP curve.** Contact Freudenberg Filtration Technologies (or equivalent) for a ΔP vs. face velocity table for the SF13-B-0593x0593x292 (or nearest equivalent to the tower filter face area). Phase 6C has one point — a 3-point curve would significantly improve the system curve model.
5. **Confirm tower filter face area** from Phase 4 FreeCAD CAD model. This determines the actual face velocity at any given Q and whether the 593×593 mm filter format fits or requires adaptation.
6. **Select and obtain prefilter ΔP data** (G4/M5/F7 class). A prefilter protects the HEPA and adds 30–100 Pa. It is entirely unknown at this stage.
7. **Inquire with Systemair India** for local KVO 250 pricing and lead time.

Completed in Phase 6C (no longer action items):
- ~~Read G2E140-AE77-01 operating instructions~~ — Done. Thermal-limit claim corrected. No fan curve in this document.
- ~~Read Systemair KVO 250 datasheet~~ — Done. Evidence A. 2 confirmed curve points obtained.
- ~~Obtain at least one filter ΔP value~~ — Done (partial). Freudenberg H13 single-point data obtained.
- ~~Resolve R2E225-RA92-09 airflow discrepancy~~ — Done. 705 m³/h at 50 Hz confirmed.

Completed in Phase 6D (no longer action items):
- ~~Digitize 2+ additional KVO 250 fan curve points~~ — Done. 4 graph-digitized points added via PyMuPDF vector extraction. Curve now 6 points; CFD-ready. Shutoff head corrected from 850 Pa to 688 Pa.

Last updated: 2026-09-05 (Phase 6D).
