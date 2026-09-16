# AQI Tower Phase 19 — Pre-filter Candidate Decision Matrix

**PHASE 19 STATUS: COMPLETE**
**Date: 2026-09-07**
**Research phase. No CFD run. No CAD modified. No experiment performed.**

This document scores five pre-filter candidates against eleven weighted criteria. For full engineering rationale, see `PHASE19_PREFILTER_SPECIFICATION.md`.

---

## Candidates

| ID | Candidate | Description |
|---|---|---|
| A | Freudenberg Viledon G4 — 592×592×48 mm | Synthetic G4 panel; existing India supplier relationship (Phase 12A); washable metal frame variant |
| B | Camfil G4 panel — 592×592×48 mm | Synthetic G4 panel; India manufacturing confirmed; standard HVAC pre-filter line |
| C | AAF G4 panel — 592×592×48 mm | Synthetic G4 panel; AAF India distribution; standard HVAC range |
| D | Mann+Hummel G4 panel — 592×592×48 mm | Synthetic G4 panel; India manufacturing (Noida); industrial filtration division |
| E | Generic Indian G4 washable — 592×592×48 mm | IndiaMART HVAC supplier; self-certified G4; lower cost; variable quality |

All candidates are specified at the same nominal size (592 × 592 × 48 mm) and the same filter class (G4), so the matrix distinguishes them on procurement, data quality, price, and risk — not on filtration physics (which is equivalent across G4 products).

---

## Criteria and Weights

Weights were fixed before scoring. Total: 100 points.

| # | Criterion | Weight | Rationale |
|---|---|---|---|
| 1 | Manufacturer data quality (datasheet with ΔP vs. v) | 20 | Pressure-drop budgeting requires actual numbers, not estimates |
| 2 | India availability and lead time | 18 | Prototype can only use parts that can actually be procured |
| 3 | Supplier relationship / procurement simplicity | 14 | Existing contacts reduce RFQ burden for a student team |
| 4 | Test certificate confidence (EN 779 or ISO 16890) | 12 | Filter class must be verifiable; self-certification is insufficient |
| 5 | Washability confirmation | 10 | Phase 18 requirement; saves recurring replacement cost |
| 6 | Approximate unit cost | 8 | Prototype budget sensitivity |
| 7 | Frame durability (washable vs disposable) | 8 | Reuse across multiple wash cycles |
| 8 | Dust holding capacity (service interval) | 5 | Fewer cleans = less maintenance burden in prototype phase |
| 9 | Upgrade path (G4 → M5 from same supplier) | 3 | Reduces effort if performance upgrade is needed later |
| 10 | Mechanical fit risk (standard 592×592 availability) | 1 | All 5 candidates nominally supply this size; low differentiator |
| 11 | Brand reputation for industrial HVAC | 1 | Minor; comfort factor for stakeholder presentations |
| **Total** | | **100** | |

---

## Scoring Scale

| Raw score | Meaning |
|---|---|
| 5 | Fully satisfies the criterion; best available |
| 4 | Good; minor gap |
| 3 | Adequate; meaningful limitation |
| 2 | Poor; significant shortcoming |
| 1 | Very poor |
| 0 | Fails criterion entirely |

Weighted score = raw score × weight / 5.

---

## Scores with Rationale

### Criterion 1 — Manufacturer data quality (Weight: 20)

Does the supplier publish actual ΔP vs face velocity data in a publicly available datasheet?

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 4 | Viledon product data available on request; EN 779 test certificates supplied with each batch; technical data requires contact/request but is routinely supplied. Not always on public web. |
| B — Camfil | 5 | Camfil publishes detailed technical datasheets including ΔP curves on their product portal; readily downloadable. Best data availability of the five candidates. |
| C — AAF | 4 | AAF technical data available via product portal; typically requires a login account but data is accessible. Good quality. |
| D — Mann+Hummel | 3 | Industrial filtration division data sometimes requires direct contact; less consistently published than Camfil or AAF. Adequate but requires effort. |
| E — Generic Indian | 1 | Most IndiaMART suppliers do not publish ΔP-velocity curves. Product is often listed by efficiency class only. Data gap is the primary risk with this option. |

**Weighted scores (× 20/5):** A: 16, B: 20, C: 16, D: 12, E: 4

---

### Criterion 2 — India availability and lead time (Weight: 18)

Can the product be delivered to an Indian address with reasonable lead time?

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 4 | India HQ confirmed in Pune (Phase 12A). Pre-filters are standard product line. Lead time likely 1–4 weeks from Pune. |
| B — Camfil | 5 | India manufacturing confirmed. Standard HVAC pre-filters are stocked locally. Lead time typically 1–2 weeks or ex-stock. |
| C — AAF | 3 | AAF India has distribution but specific lead time for non-standard orders (592×592 custom vs. 610×610 common Indian size) is uncertain. |
| D — Mann+Hummel | 3 | India manufacturing (Noida) confirmed for industrial filters; HVAC pre-filter line lead time unknown. |
| E — Generic Indian | 5 | Multiple IndiaMART suppliers offer same-day dispatch or < 1 week delivery; very wide local availability. |

**Weighted scores:** A: 14.4, B: 18, C: 10.8, D: 10.8, E: 18

---

### Criterion 3 — Supplier relationship / procurement simplicity (Weight: 14)

Does the project have an existing contact that simplifies the RFQ process?

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 5 | Phase 12A established direct India contact (info@freudenberg-filter.com, +91 20 67633600, Pune). Combined HEPA + pre-filter enquiry in a single email is possible. This is the only candidate with a project-established contact. |
| B — Camfil | 3 | No prior contact; new RFQ required to info.in@camfil.com. Easy to initiate, but starts from scratch. |
| C — AAF | 2 | No prior contact; RFQ via website form or regional distributor; process least established. |
| D — Mann+Hummel | 2 | No prior contact; RFQ via website; India industrial contacts exist but not HVAC-specific. |
| E — Generic Indian | 3 | IndiaMART direct messaging is fast; multiple simultaneous quotes easy to send. Less formal than OEM but simpler admin. |

**Weighted scores:** A: 14, B: 8.4, C: 5.6, D: 5.6, E: 8.4

---

### Criterion 4 — Test certificate confidence (Weight: 12)

Is there confidence that an EN 779:2012 or ISO 16890:2016 test certificate is available and traceable?

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 5 | Freudenberg is an established filtration manufacturer; test certificates accompany each production batch. Already confirmed for the H13 HEPA (Phase 12A). |
| B — Camfil | 5 | Camfil is a specialist filtration OEM; ISO/EN test certificates are standard deliverable. |
| C — AAF | 4 | AAF is an established OEM; certificates available but may need to be specifically requested for standard products. |
| D — Mann+Hummel | 4 | Industrial filtration OEM; test certificates available; HVAC-specific certification may require confirmation. |
| E — Generic Indian | 1 | Self-certification without independent test is common on IndiaMART. EN 779 or ISO 16890 accredited test certificates are not standard practice for budget suppliers. Must be verified case by case. |

**Weighted scores:** A: 12, B: 12, C: 9.6, D: 9.6, E: 2.4

---

### Criterion 5 — Washability confirmation (Weight: 10)

Is a washable (metal-frame) version confirmed for 592×592×48 mm in G4?

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 4 | Metal-frame washable variants confirmed in Viledon product range; specific 592×592 washable version requires confirmation with India office. |
| B — Camfil | 4 | Camfil offers both cardboard-frame (disposable, Cam30) and metal-frame (Cam-Flo G) variants; metal-frame washable option exists; 592×592 availability requires RFQ confirmation. |
| C — AAF | 3 | Washable metal-frame variants exist in AAF range but specific India availability for 592×592 requires confirmation. |
| D — Mann+Hummel | 3 | Metal-frame washable versions exist; India availability for this specific size requires confirmation. |
| E — Generic Indian | 4 | Washable metal-frame G4 panels are the dominant product category on IndiaMART HVAC section; very high availability. |

**Weighted scores:** A: 8, B: 8, C: 6, D: 6, E: 8

---

### Criterion 6 — Approximate unit cost (Weight: 8)

Lower cost = higher score for the same specification. All values are estimates pending RFQ.

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 3 | Estimated ₹700–1,800 per unit [EST]. Premium brand pricing. |
| B — Camfil | 3 | Estimated ₹800–2,000 per unit [EST]. Similar premium to Freudenberg. |
| C — AAF | 3 | Estimated ₹900–2,500 per unit [EST]. Similar range. |
| D — Mann+Hummel | 3 | Estimated ₹700–2,000 per unit [EST]. Similar range. |
| E — Generic Indian | 5 | Estimated ₹400–1,500 per unit [EST]. Significantly lower cost. |

Note: all five candidates score 3 except E (generic) which scores 5. The premium candidates are clustered in a similar price band; differentiation on cost alone does not justify choosing among A–D.

**Weighted scores:** A: 4.8, B: 4.8, C: 4.8, D: 4.8, E: 8

---

### Criterion 7 — Frame durability (Weight: 8)

Can the filter frame survive 12+ wash cycles without structural failure?

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 4 | Metal-frame Viledon variants are designed for repeated use; documented in product range. |
| B — Camfil | 4 | Cam-Flo G metal-frame variants designed for washability; documented wash specifications available. |
| C — AAF | 3 | Metal-frame available; wash cycle specification requires confirmation from AAF. |
| D — Mann+Hummel | 3 | Metal-frame available; durability specification requires confirmation. |
| E — Generic Indian | 2 | Quality of metal frame varies by supplier; some use thin galvanised sheet prone to corrosion after repeated washing. Without testing, durability is uncertain. |

**Weighted scores:** A: 6.4, B: 6.4, C: 4.8, D: 4.8, E: 3.2

---

### Criterion 8 — Dust holding capacity / service interval (Weight: 5)

Higher dust holding = less frequent washing = less maintenance. Scored on EN 779 dust holding data availability.

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 4 | Dust holding data available in Viledon product documentation. Typical G4: 150–300 g/m². |
| B — Camfil | 5 | Camfil publishes dust holding data in their technical datasheets. Best-documented of the five. |
| C — AAF | 3 | Data available but requires specific request; not always published for standard products. |
| D — Mann+Hummel | 3 | Data available from technical documentation on request. |
| E — Generic Indian | 1 | Dust holding capacity rarely published by IndiaMART suppliers. Cannot be verified. |

**Weighted scores:** A: 4, B: 5, C: 3, D: 3, E: 1

---

### Criterion 9 — Upgrade path to M5 (Weight: 3)

Can the same supplier provide an M5 version of the same size?

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 5 | Viledon makes M5/M6/F7 in same EU sizes. Easy upgrade. |
| B — Camfil | 5 | Camfil range includes M5 and F7 in same frame sizes. |
| C — AAF | 4 | M5/M6 available in same range; some size constraints. |
| D — Mann+Hummel | 4 | M5 available in the same industrial HVAC range. |
| E — Generic Indian | 3 | M5 products exist on IndiaMART but with the same data quality concerns. |

**Weighted scores:** A: 3, B: 3, C: 2.4, D: 2.4, E: 1.8

---

### Criterion 10 — Mechanical fit risk / 592×592 availability (Weight: 1)

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 4 | 592×592 is standard EU size; high probability of stock availability. |
| B — Camfil | 4 | Same. |
| C — AAF | 3 | Standard size but India stock for this specific size less certain. |
| D — Mann+Hummel | 3 | Standard size; India stock uncertain. |
| E — Generic Indian | 4 | 592×592 is commonly stocked by Indian HVAC suppliers. |

**Weighted scores:** A: 0.8, B: 0.8, C: 0.6, D: 0.6, E: 0.8

---

### Criterion 11 — Brand reputation (Weight: 1)

| Candidate | Score | Rationale |
|---|---|---|
| A — Freudenberg | 5 | Global industrial filtration OEM; strong reputation. |
| B — Camfil | 5 | Specialist filtration company; recognised globally. |
| C — AAF | 4 | Established brand; subsidiary of Daikin. |
| D — Mann+Hummel | 4 | Global filtration OEM; industrial reputation strong. |
| E — Generic Indian | 2 | Variable; not a differentiating brand. |

**Weighted scores:** A: 1, B: 1, C: 0.8, D: 0.8, E: 0.4

---

## Summary Score Table

| Criterion | Wt | A: Freudenberg | B: Camfil | C: AAF | D: Mann+Hummel | E: Generic |
|---|---|---|---|---|---|---|
| 1. Data quality | 20 | 16.0 | **20.0** | 16.0 | 12.0 | 4.0 |
| 2. India availability | 18 | 14.4 | **18.0** | 10.8 | 10.8 | **18.0** |
| 3. Procurement simplicity | 14 | **14.0** | 8.4 | 5.6 | 5.6 | 8.4 |
| 4. Test cert confidence | 12 | **12.0** | **12.0** | 9.6 | 9.6 | 2.4 |
| 5. Washability | 10 | 8.0 | 8.0 | 6.0 | 6.0 | 8.0 |
| 6. Unit cost | 8 | 4.8 | 4.8 | 4.8 | 4.8 | **8.0** |
| 7. Frame durability | 8 | 6.4 | 6.4 | 4.8 | 4.8 | 3.2 |
| 8. Dust holding | 5 | 4.0 | **5.0** | 3.0 | 3.0 | 1.0 |
| 9. Upgrade path | 3 | **3.0** | **3.0** | 2.4 | 2.4 | 1.8 |
| 10. Mechanical fit | 1 | 0.8 | 0.8 | 0.6 | 0.6 | 0.8 |
| 11. Brand reputation | 1 | **1.0** | **1.0** | 0.8 | 0.8 | 0.4 |
| **TOTAL** | **100** | **84.4** | **87.4** | **64.4** | **60.4** | **56.0** |
| **Rank** | | **2nd** | **1st** | **3rd** | **4th** | **5th** |

---

## Sensitivity Analysis

The gap between B (Camfil, 87.4) and A (Freudenberg, 84.4) is only 3 points. This gap is driven primarily by Camfil's better published data quality and local stock availability. However:

- If Freudenberg's existing India contact (Phase 12A) closes the enquiry faster than a cold RFQ to Camfil, the practical procurement advantage shifts to A.
- If Camfil's India 592×592 stock turns out to require special order, its availability advantage disappears.
- The gap is small enough that **both A and B should receive simultaneous RFQs**, and the order should go to whichever responds first with the required datasheet and acceptable price.

The gap between B (87.4) and E (generic, 56.0) is 31 points — sufficient to be unambiguous. The generic option is last primarily due to data quality and test certificate confidence. For a research prototype where traceable component specifications are important, the generic option is not the preferred choice.

---

## Decision

**Preferred product (simultaneous first choice): A — Freudenberg G4 and B — Camfil G4**

Send RFQ to both simultaneously. Order from whichever provides: (1) a datasheet with ΔP at ≥2 face velocities, (2) an EN 779 or ISO 16890 test certificate, (3) confirmed washable metal frame, (4) an acceptable price and lead time — whichever achieves all four criteria first.

**Backup: C — AAF G4** if Freudenberg and Camfil cannot supply 592×592 washable within a reasonable lead time.

**Generic Indian (E): Acceptable fallback only** if all OEM suppliers are blocked, provided the supplier can produce an EN 779 or ISO 16890 accredited test certificate from an independent laboratory.

---

## Evidence Quality Note

All scores in this matrix are engineering judgements based on published manufacturer product ranges, established India contacts, and general knowledge of the HVAC filtration industry. No specific products were tested or compared with measured data. Scores for criteria 1, 2, 5, 7, and 8 should be updated once RFQ responses are received and actual product datasheets are reviewed. The ranking is expected to remain stable among A and B; the gap to C, D, E is unlikely to close without a significant improvement in data quality from those suppliers.
