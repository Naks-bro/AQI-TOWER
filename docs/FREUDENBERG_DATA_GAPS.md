# Freudenberg Filter Data Gaps — AQI Tower Phase 12A

**PURPOSE:** Record what technical data remains unavailable for the Freudenberg SF13-B H13 HEPA filter after the Phase 12A search, and state the impact on each downstream task.

Last updated: 2026-09-06 (Phase 12A).

---

## 1. Product Confirmed

Filter: **Freudenberg SF13-B-0593x0593x292/V12x25-N10N-J27-ACA**  
Class: H13 (EN 1822) = ISO 35 H (ISO 29463)

---

## 2. Data Gaps Table

| Gap | Specific missing data | Impact on project | How to close |
|-----|----------------------|-------------------|--------------|
| **Fractional efficiency curve** | η(d_p) at particle sizes 0.05–2 µm; no product-specific curve found publicly | Particle CFD Approach 1 (Level 2 CADR) blocked; CADR claim stays at Level 1 (theoretical) | Request from Freudenberg; or read EN 1822 test certificate supplied with purchased filter |
| **Actual MPPS diameter** | Generic glass fibre range is 0.1–0.25 µm (CIBSE: 0.12–0.25 µm; Camfil: 0.1–0.2 µm); product-specific value not published | Cannot confirm which particle size is the worst-case for CADR claim | Request from Freudenberg; or read test certificate |
| **Efficiency at AQI Tower operating velocity** | AQI Tower face velocity = 1.053 m/s; EN 1822 tests at 2.84 m/s; η at 1.053 m/s not published | Reduces confidence in Level 1 CADR estimate; glass fibre physics suggests η improves at lower velocity but this is NOT confirmed for this product | Manufacturer measurement or experimental test rig |
| **Multi-point ΔP vs face velocity** | Only one data point: 300 Pa at 2.84 m/s (clean); no curve | CFD Darcy model uses linear single-point extrapolation (high uncertainty below ~1.5 m/s) | Request from Freudenberg; or measure directly |
| **Terminal (loaded) ΔP** | Not stated anywhere publicly; literature suggests 375–500 Pa typical | Cannot estimate filter service life or loaded operating point | Request from Freudenberg |
| **EN 1822 test face velocity** | Not published; manufacturer rated velocity used as proxy but EN 1822 may test at a different velocity | Small uncertainty in rated efficiency claim | Request from Freudenberg with test certificate |

---

## 3. What Was Found (New Data in Phase 12A)

The following data was confirmed or newly found in Phase 12A; the filter JSON has been updated:

| Item | Value | Source |
|------|-------|--------|
| ISO 29463 equivalent class | ISO 35 H | products.freudenberg-filter.com/en_US/detail/10893 |
| H13 local efficiency (EN 1822) | ≥ 99.75% (local scan minimum) | Mann+Hummel EN 1822 explainer |
| H13 integral efficiency (EN 1822) | ≥ 99.95% (already known) | EN 1822-1:2019 standard |
| MPPS range (generic glass fibre) | 0.1–0.2 µm (Camfil), 0.12–0.25 µm (CIBSE) — generic, not product-specific | Camfil/CIBSE published articles |
| Test certificate accompanies each unit | Yes — manufacturer product page states this | products.freudenberg-filter.com |
| Freudenberg India contact (HQ) | +91 20 67633600, Pune 411014 | in.freudenberg-filter.com |
| Freudenberg India contact (production) | +91 21 37615322, Pune 412208 | freudenberg-filter.com/en/company/locations/ |
| Freudenberg general email | info@freudenberg-filter.com | freudenberg-filter.com |
| Product datasheet | Downloadable from product page (confirmed available) but contains nominal rated data only | products.freudenberg-filter.com |

---

## 4. Impact on CADR Claim Levels

| CADR Level | Status | Blocked by |
|-----------|--------|-----------|
| Level 0 — Airflow CFD | Available — Q ≈ 1332 m³/h (Phase 10B) | — |
| Level 1 — Manufacturer η + CFD Q | Available — 1332 × 0.9995 ≈ 1331 m³/h THEORETICAL | Labelled as THEORETICAL/CONDITIONAL only |
| Level 2 — Particle CFD (conservative, arrival fraction) | **READY** — Approach 2/3 can run without η(d_p) | No blocking gap |
| Level 2 — Particle CFD (with η) | **BLOCKED** | Fractional efficiency curve not available |
| Level 3 — Physical particle test | **BLOCKED** | Requires physical hardware and test equipment |
| Level 4 — Certified CADR | **BLOCKED** | Requires full AHAM AC-1 or equivalent test |

---

## 5. Impact on Particle CFD (Phase 12B)

Phase 12B particle CFD (Lagrangian particle tracking in CASE_M_SEALED) can proceed with:

- **Approach 2:** Capture all particles reaching FILTER_UPSTREAM with η=1. Gives maximum possible filter arrival fraction (upper bound on CADR, ignores real filter penetration).
- **Approach 3:** Track wall deposition and filter arrival fraction without applying any capture efficiency. Gives the airflow delivery fraction — how much of the injected particle mass reaches the filter face vs deposits on walls or returns to outlet.

Both approaches do NOT require fractional efficiency data from Freudenberg.

**Approach 1** (applying the actual η(d_p) at filter face) remains blocked until the fractional efficiency data is received.

---

## 6. Recommended Actions (Priority Order)

1. **Send data request to Freudenberg India** (+91 20 67633600; info@freudenberg-filter.com) using the draft in `docs/FREUDENBERG_DATA_REQUEST.md §6`. Request: fractional efficiency curve, MPPS, multi-point ΔP.
2. **Proceed with Phase 12B particle CFD** using Approach 3 (conservative) and Approach 2 (η=1 upper bound). This does not require Freudenberg data.
3. **Obtain filter test certificate** when a physical filter is purchased. This certificate contains EN 1822 fractional efficiency data and will unblock Approach 1.
4. **Do NOT cite Level 2 CADR** until Freudenberg fractional efficiency data is in hand. The Level 1 theoretical estimate (~1331 m³/h at MPPS) remains the only available CADR figure.

---

## 7. What "NOT AVAILABLE" Means for Each Downstream Document

| Document | Impact of gaps |
|----------|---------------|
| `docs/CADR_METHODOLOGY.md` | Remains at Level 1 conditional estimate. No update needed from Phase 12A. |
| `data/filters/HEPA_EFFICIENCY_EVIDENCE.md` | Particle-size efficiency column remains "NOT AVAILABLE" for all sizes. ISO 29463 class added. |
| `docs/PARTICLE_CFD_PLAN.md` | Phase 12B can proceed (Approaches 2 and 3). Phase 12C (Approach 1) remains gated on Freudenberg data. |
| `data/filters/freudenberg_SF13B_593x593x292.json` | Updated with new ISO class, contacts, and evidence notes. Core ΔP and efficiency gaps unchanged. |
