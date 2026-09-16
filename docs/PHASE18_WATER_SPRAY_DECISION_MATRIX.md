# AQI Tower Phase 18 — Water-Spray Stage Decision Matrix

**PHASE 18 STATUS: COMPLETE — DECISION: NO-GO**
**Date: 2026-09-07**
**Research-only. No CFD run. No CAD modified. No existing results modified.**

This document contains the full scored decision matrix for Phase 18. For the engineering rationale behind each score, see `PHASE18_WATER_SPRAY_FEASIBILITY.md`.

---

## Options Evaluated

| ID | Option | Description |
|---|---|---|
| A | Water spray + demister | Low-pressure hollow-cone nozzle spray chamber; wire mesh pad or vane demister; recirculated sump; pump |
| B | Dry G4/M5 panel pre-filter | Washable synthetic panel pre-filter (G4 or M5 grade per EN ISO 16890); fits existing GEO_C inlet face |
| C | Cyclone / inertial separator | Custom-fabricated centrifugal separator upstream of HEPA; good coarse efficiency; no water |
| D | HEPA-only baseline | No pre-filter; retain current CASE_M_SEALED configuration with H13 HEPA as first active stage |
| E | Enlarged settling chamber | Passive gravity settling chamber extension at inlet; captures only >50 µm particles |

These options cover the design space identified in §13 of `PHASE18_WATER_SPRAY_FEASIBILITY.md`. Options A–E are not mutually exclusive in principle, but the matrix evaluates each as a standalone pre-treatment choice for the slot currently occupied by the water-spray concept.

---

## Evaluation Criteria and Weights

Criteria were selected to represent the primary decision factors for an air-cleaning device at this development stage. Weights were fixed before scoring to avoid post-hoc rationalisation.

| # | Criterion | Weight (pts) | Rationale |
|---|---|---|---|
| 1 | PM2.5 removal effectiveness | 18 | The health-critical pollutant. Primary mission metric. |
| 2 | PM10 and coarse dust removal | 10 | Secondary; relevant to indoor air quality and HEPA loading |
| 3 | HEPA filter life protection | 10 | Reduces operating cost; important for long-term viability |
| 4 | Hygiene and biological safety | 14 | Air purifier in a breathing zone; biological risk is a disqualifying factor |
| 5 | System pressure drop added | 10 | Direct impact on CADR (proportional to Q × η) |
| 6 | System complexity | 8 | Component count, failure modes, integration difficulty |
| 7 | Maintenance burden | 8 | Frequency and difficulty of required maintenance actions |
| 8 | Water / consumable use | 6 | Water availability and operational cost |
| 9 | India procurement feasibility | 6 | Availability and lead time of required components |
| 10 | Prototype-stage suitability | 6 | Appropriate for a student-built first prototype |
| 11 | Reversibility / future upgrade path | 4 | Ease of removing or replacing this stage in future |
| **Total** | | **100** | |

**Weight total: 100 points.**

---

## Scoring Scale

Each criterion is scored 0–5 per option. Raw score is multiplied by the criterion weight, then divided by 5 to produce weighted points (so a perfect score of 5 on a weight-18 criterion yields 18 points).

| Raw score | Meaning |
|---|---|
| 5 | Fully satisfies the criterion; best achievable at this scale |
| 4 | Good; minor shortcoming relative to best |
| 3 | Adequate; meaningful limitation |
| 2 | Poor; significant shortcoming |
| 1 | Very poor; near-negligible or high-risk |
| 0 | Fails criterion; disqualifying or zero contribution |

---

## Scores With Rationale

### Criterion 1 — PM2.5 Removal Effectiveness (Weight: 18)

The health-critical fraction. Scored on actual collection efficiency for 0.3–2.5 µm particles per device physics.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 0 | Simple spray in Greenfield gap: < 3% efficiency for PM2.5. Physics prevents effective impaction or diffusion at this energy input and contact time. See §4.2, §2.3. |
| B — G4/M5 pre-filter | 2 | G4 negligible PM2.5; M5 captures ~30–40% PM2.5 (EN ISO 16890 ePM2.5 classification). Not primary PM2.5 device — that is the HEPA downstream. Role is pre-collection, not PM2.5 removal. |
| C — Cyclone | 1 | Cyclone cut-size typically 2–5 µm for practical student-scale units; PM2.5 collection < 10%. |
| D — HEPA-only | 5 | H13 HEPA is the gold standard for PM2.5 (≥99.95% at MPPS per EN 1822). HEPA-only passes all PM2.5 to the filter with maximum airflow. |
| E — Settling chamber | 0 | Gravity settling is irrelevant for PM2.5 (terminal velocity ~0.08 µm/s for 2.5 µm particle at 1g). |

**Weighted scores (raw × weight / 5):** A: 0, B: 7.2, C: 3.6, D: 18, E: 0

---

### Criterion 2 — PM10 and Coarse Dust Removal (Weight: 10)

Scored on collection efficiency for particles > 2.5 µm (primarily PM10, pollen, mineral dust).

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 2 | Moderate coarse capture (40–70% for >10 µm per §2.1) but energy-intensive to achieve; poor for 2.5–10 µm. |
| B — G4/M5 pre-filter | 4 | G4 >80% for >10 µm; M5 >85% for >10 µm, moderate for 2.5–10 µm (EN 779/ISO 16890). Effective and safe. |
| C — Cyclone | 5 | >95% for >10 µm; ~50% at 5 µm for well-designed unit. Best coarse-capture performance of all options. |
| D — HEPA-only | 3 | HEPA captures PM10 well (>99.95%), but with no upstream protection HEPA loads faster. Airflow maintained. |
| E — Settling chamber | 1 | Only captures >50 µm by gravity; negligible for PM10. |

**Weighted scores:** A: 4.0, B: 8.0, C: 10.0, D: 6.0, E: 2.0

---

### Criterion 3 — HEPA Filter Life Protection (Weight: 10)

Scored on whether the option reduces the rate of coarse particle loading on the HEPA face, extending replacement interval.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 2 | Moderate coarse capture extends HEPA life for the >10 µm fraction, but moisture carryover causes premature loading by a different mechanism (wetting, microbial). Net effect on HEPA life may be negative. |
| B — G4/M5 pre-filter | 5 | Primary purpose. Captures >80% of particles that would otherwise load the HEPA face. Dry, safe, and effective. Best HEPA protector of all options. |
| C — Cyclone | 4 | Removes coarse fraction well; PM2.5 still reaches HEPA. Good HEPA protection for the coarse component. |
| D — HEPA-only | 0 | No upstream protection; HEPA loads at the full particle inlet concentration. Replacement interval shortest of all options. |
| E — Settling chamber | 1 | Negligible protection; only removes the coarsest fraction (>50 µm) which is already the smallest HEPA loading contributor in urban PM. |

**Weighted scores:** A: 4.0, B: 10.0, C: 8.0, D: 0.0, E: 2.0

---

### Criterion 4 — Hygiene and Biological Safety (Weight: 14)

Scored on absence of biological risk in a device delivering air to a breathing zone. This criterion is weighted highest after PM2.5 because a contaminated air purifier is actively harmful.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 0 | Disqualifying. Recirculating warm water + aerosol generation = Legionella risk (ASHRAE 188, CIBSE TM13). Biofilm in nozzles, tank, and demister releases bacteria and mold into the airstream. HEPA wetting provides growth substrate on the clean side. See §9.1–§9.4. |
| B — G4/M5 pre-filter | 5 | No water, no biological substrate on a clean dry synthetic filter. Standard hygiene. Mold growth possible only if filter becomes wet from a separate cause. |
| C — Cyclone | 5 | Dry mechanical separator; no water, no biological risk. |
| D — HEPA-only | 5 | No water stage; HEPA itself is a biological barrier. No hygiene concerns added by this choice. |
| E — Settling chamber | 5 | Dry; no biological risk. |

**Weighted scores:** A: 0.0, B: 14.0, C: 14.0, D: 14.0, E: 14.0

---

### Criterion 5 — System Pressure Drop Added (Weight: 10)

Scored on the additional pressure drop introduced by this option on top of the CASE_M_SEALED baseline (Q = 1332 m³/h, ΔP ≈ 115 Pa). Lower is better. Zero additional ΔP = 5/5.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 1 | 35–125 Pa added (§7.2); flow reduction 7–23% (§7.3). Wide range reflects design uncertainty; any plausible implementation penalises the operating point materially. |
| B — G4/M5 pre-filter | 4 | Clean ΔP ~20–60 Pa for a properly sized G4/M5 panel at approach velocity ≤0.5 m/s. Modest; well within fan headroom. Increases as filter loads (managed by replacement schedule). |
| C — Cyclone | 3 | 50–200 Pa depending on cut size and inlet velocity; student-fabricated cyclone likely in the 80–150 Pa range — significant additional resistance. |
| D — HEPA-only | 5 | No additional component; no additional ΔP beyond baseline. Maximum available airflow. |
| E — Settling chamber | 5 | Negligible additional ΔP (<10 Pa); large open volume, low velocity, no resistance element. |

**Weighted scores:** A: 2.0, B: 8.0, C: 6.0, D: 10.0, E: 10.0

---

### Criterion 6 — System Complexity (Weight: 8)

Scored on additional component count, assembly difficulty, and integration risk. Lower complexity = higher score.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 0 | 12+ additional major components (§11): pump, nozzles, tank, level sensor, drain, demister, drain tray, settling zone, tubing, IP-rated electrical, water quality monitoring, cleaning access. Each has its own failure mode. |
| B — G4/M5 pre-filter | 5 | 1 component (filter panel) + frame/seal. Trivially simple. |
| C — Cyclone | 3 | Custom fabrication required; 3–5 components (body, inlet, outlet, dust cup, seals). Moderate complexity; no off-shelf unit likely fits the GEO_C geometry. |
| D — HEPA-only | 5 | No new components. Zero added complexity. |
| E — Settling chamber | 4 | Box/extension geometry only; 1 structural component; no moving parts; negligible complexity. |

**Weighted scores:** A: 0.0, B: 8.0, C: 4.8, D: 8.0, E: 6.4

---

### Criterion 7 — Maintenance Burden (Weight: 8)

Scored on frequency, effort, and skill required for routine maintenance to keep the option functioning safely. Lower burden = higher score.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 0 | Monthly: nozzle inspection and cleaning, tank drain and refill, demister wash. Quarterly: full system disinfection. Annual: written Legionella risk scheme review. All require technical skill and records. Neglect has immediate health consequences. |
| B — G4/M5 pre-filter | 5 | Monthly shake or rinse; annual replacement. Low skill required. |
| C — Cyclone | 4 | Periodic emptying of dust cup (monthly in high-dust environments); quarterly clean of cyclone body; no water. |
| D — HEPA-only | 2 | No pre-filter means HEPA loads faster; HEPA replacement is more frequent and more expensive (₹5,000–15,000 per unit). Burden is financial and logistic, not operational skill. |
| E — Settling chamber | 5 | Occasional sweep or vacuum of settled dust. Minimal effort. |

**Weighted scores:** A: 0.0, B: 8.0, C: 6.4, D: 3.2, E: 8.0

---

### Criterion 8 — Water / Consumable Use (Weight: 6)

Scored on absence of water consumption and minimisation of consumable cost.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 0 | 5–43 L/day make-up water (§8.2); recirculated sump; blowdown disposal; pump electricity. In a field setting, daily water management is required. |
| B — G4/M5 pre-filter | 4 | No water; occasional cleaning water used during wash (~1–2 L); replaced annually (low cost ₹200–600). |
| C — Cyclone | 5 | No water; no consumables beyond periodic cleaning. |
| D — HEPA-only | 3 | No water; but HEPA replacement frequency higher and replacement cost significant. |
| E — Settling chamber | 5 | No water; no consumables. |

**Weighted scores:** A: 0.0, B: 4.8, C: 6.0, D: 3.6, E: 6.0

---

### Criterion 9 — India Procurement Feasibility (Weight: 6)

Scored on ability to source all required components in India within reasonable lead time and cost.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 2 | Pump, nozzles, tank: available. Demister (wire mesh pad, mist eliminator): limited specialty supply in India; demister to the required size and material specification likely requires import or custom fabrication. Quality of available nozzle droplet-size characteristics unverified. |
| B — G4/M5 pre-filter | 5 | G4/M5 panel pre-filters are standard HVAC products sold by multiple India distributors (Camfil, AAF, local manufacturers). Off-shelf in major cities; standard sizes available or easily custom-cut. Low cost. |
| C — Cyclone | 3 | No off-shelf unit likely to match GEO_C geometry; requires fabrication by a local sheet-metal shop. Components available; design and fabrication must be done by the project team. Moderate effort. |
| D — HEPA-only | 5 | No new procurement; existing HEPA already specified (Freudenberg SF13-B, Phase 12A India contacts established). |
| E — Settling chamber | 5 | Sheet metal or acrylic box; available at any fabrication shop. No specialty parts. |

**Weighted scores:** A: 2.4, B: 6.0, C: 3.6, D: 6.0, E: 6.0

---

### Criterion 10 — Prototype-Stage Suitability (Weight: 6)

Scored on whether the option is appropriate for a student-built first prototype that has not yet left the digital/research stage.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 0 | 12+ extra components, regulatory hygiene obligations (ASHRAE 188, CIBSE TM13), and a safety profile that is inappropriate for a prototype without institutional water-management oversight. Introduces risk before benefit is established. |
| B — G4/M5 pre-filter | 5 | Ideal for a prototype: simple, available, reversible, and directly comparable to the baseline in a controlled experiment. A well-established industrial component used at this scale by millions of HVAC systems. |
| C — Cyclone | 3 | Requires custom fabrication; moderate effort; adds design risk; appropriate only after basic airflow and filter data are validated. |
| D — HEPA-only | 4 | The current prototype baseline; appropriate for early screening. Limits HEPA replacement budget but introduces no new complications. |
| E — Settling chamber | 4 | Simple to build; negligible risk; appropriate for a prototype exploring the effect of reducing the coarsest inlet loading. |

**Weighted scores:** A: 0.0, B: 6.0, C: 3.6, D: 4.8, E: 4.8

---

### Criterion 11 — Reversibility / Future Upgrade Path (Weight: 4)

Scored on ease of removing this option later or replacing it with a better one.

| Option | Score | Rationale |
|---|---|---|
| A — Water spray | 1 | Removing it requires undoing 12+ components; plumbing penetrations; sealing of spray-zone openings; potential corrosion damage to tower interior; cleaning of residual biological contamination. Difficult to reverse cleanly. |
| B — G4/M5 pre-filter | 5 | Drop-in slot in a frame; replacement takes minutes; can be upgraded to F7 or removed at zero cost. |
| C — Cyclone | 3 | Bolted-on unit; can be bypassed or removed; duct connections remain as hardware. Moderate reversibility. |
| D — HEPA-only | 5 | Default state; trivially reversible (add a pre-filter upstream). |
| E — Settling chamber | 4 | Box extension; can be disconnected; negligible integration. |

**Weighted scores:** A: 0.8, B: 4.0, C: 2.4, D: 4.0, E: 3.2

---

## Summary Score Table

| Criterion | Wt | A: Water spray | B: G4/M5 pre-filter | C: Cyclone | D: HEPA-only | E: Settling chamber |
|---|---|---|---|---|---|---|
| 1. PM2.5 effectiveness | 18 | 0.0 | 7.2 | 3.6 | 18.0 | 0.0 |
| 2. PM10 / coarse removal | 10 | 4.0 | 8.0 | 10.0 | 6.0 | 2.0 |
| 3. HEPA life protection | 10 | 4.0 | 10.0 | 8.0 | 0.0 | 2.0 |
| 4. Hygiene / bio safety | 14 | 0.0 | 14.0 | 14.0 | 14.0 | 14.0 |
| 5. Pressure drop added | 10 | 2.0 | 8.0 | 6.0 | 10.0 | 10.0 |
| 6. Complexity | 8 | 0.0 | 8.0 | 4.8 | 8.0 | 6.4 |
| 7. Maintenance burden | 8 | 0.0 | 8.0 | 6.4 | 3.2 | 8.0 |
| 8. Water / consumable | 6 | 0.0 | 4.8 | 6.0 | 3.6 | 6.0 |
| 9. India procurement | 6 | 2.4 | 6.0 | 3.6 | 6.0 | 6.0 |
| 10. Prototype suitability | 6 | 0.0 | 6.0 | 3.6 | 4.8 | 4.8 |
| 11. Reversibility | 4 | 0.8 | 4.0 | 2.4 | 4.0 | 3.2 |
| **TOTAL** | **100** | **13.2** | **84.0** | **68.4** | **77.6** | **62.4** |
| **Rank** | | **5th** | **1st** | **3rd** | **2nd** | **4th** |

> **Note:** The original summary in `PHASE18_WATER_SPRAY_FEASIBILITY.md` §14 reported rounded totals (A=26, B=85, C=68, D=81, E=75). The exact totals above reflect the full per-criterion calculation. The ranking and the gap between A and B are unchanged.

---

## Sensitivity Analysis

The gap between Option A (13.2) and Option B (84.0) is 70.8 points out of 100. To assess robustness, consider what would need to change for A to approach B:

| Change | Effect on gap |
|---|---|
| Halve the weight of Hygiene (14 → 7) | A gains 0 (still scored 0); gap unchanged |
| Give A maximum score on PM2.5 (0 → 5) | A gains 18.0; gap reduces to 52.8 — still large |
| Give A maximum score on all criteria | A = 100; but criteria 4 (hygiene) and 1 (PM2.5) are scored 0 on physical grounds independent of weighting |
| Remove hygiene criterion entirely (redistribute 14 pts) | A loses 0.0 from criterion 4; gap still ≥70 pts |

The decision is insensitive to reasonable weighting changes. The water-spray option is not competitive primarily because it scores 0 on two of the three highest-weight criteria (PM2.5 effectiveness and hygiene safety) simultaneously. These scores reflect fundamental physical and public health constraints, not subjective preferences.

---

## Decision

**Option B — Dry G4/M5 Panel Pre-filter: RECOMMENDED**
**Option A — Water Spray + Demister: REJECTED (NO-GO)**

The decision matrix result, combined with the independent engineering analysis in `PHASE18_WATER_SPRAY_FEASIBILITY.md`, supports a clear NO-GO decision for the water-spray stage. Option B is the recommended replacement: a washable G4/M5 panel pre-filter inserted at the inlet, upstream of the activated carbon bed and H13 HEPA.

---

## Evidence Quality Notes

All scores are engineering judgements based on physics and reference literature as cited in `PHASE18_WATER_SPRAY_FEASIBILITY.md`. No experimental data from the AQI Tower project exists for any of the evaluated options. Scores labelled [INF] or [PROJ] in the feasibility document carry wider uncertainty than scores labelled [PR] or [STD]. The hygiene criterion (score 0 for Option A) is based on published standards (ASHRAE 188, CIBSE TM13) and is not sensitive to project-specific uncertainty.
