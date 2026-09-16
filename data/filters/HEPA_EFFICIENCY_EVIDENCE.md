# HEPA Filtration Efficiency Evidence — AQI Tower Phase 11

**EVIDENCE AUDIT ONLY — NO CFD CHANGES — NO CADR CALCULATION**  
**Separator from this file: confirmed manufacturer data / generic reference / assumption / unknown**

Last updated: 2026-09-06 (Phase 11).

---

## 1. Product Identification

| Field | Value | Source |
|-------|-------|--------|
| Manufacturer | Freudenberg Filtration Technologies | Manufacturer product page |
| Article number | SF13-B-0593x0593x292/V12x25-N10N-J27-ACA | Manufacturer product page |
| Series | SF13-B (HEPA High Volume Flow Filter) | Manufacturer product page |
| Frame material | Galvanized steel | Manufacturer product page |
| Media type | MiniPleat, V-shaped, glass fibre | Manufacturer product page |
| Dimensions | 593 × 593 × 292 mm | Manufacturer product page |
| Gross face area | 0.3516 m² | Derived: 0.593 × 0.593 |

---

## 2. Classification Evidence

| Parameter | Value | Unit | Condition | Source | Evidence class |
|-----------|------:|------|-----------|--------|----------------|
| Filter classification | H13 | — | EN 1822 | Manufacturer product page (Freudenberg, Phase 6C) | **CONFIRMED — MANUFACTURER** |
| Minimum efficiency at MPPS | ≥99.95% | % | EN 1822 test, integral filter, at MPPS | EN 1822-1:2019 class definition (H13 threshold) | **CONFIRMED — STANDARD DEFINITION** |
| Corresponding penetration at MPPS | ≤0.05% | % | EN 1822 test, integral filter, at MPPS | EN 1822-1:2019 class definition | **CONFIRMED — STANDARD DEFINITION** |

### What H13 / EN 1822 actually means

EN 1822-1 classifies HEPA and ULPA filters by their penetration at the **Most Penetrating Particle Size (MPPS)**. The MPPS is the particle size at which filter efficiency is at its minimum — the hardest size to capture. H13 requires that the filter efficiency at this worst-case size is ≥ 99.95%.

Penetration is lower (efficiency is higher) at all particle sizes other than MPPS. Particles larger than MPPS are caught by interception and impaction; particles smaller than MPPS are caught by Brownian diffusion. Only at MPPS do all three mechanisms contribute least efficiently.

**The H13 label therefore guarantees a lower bound on efficiency, but only at MPPS, and only under EN 1822 test conditions.** It does not directly state efficiency at PM2.5, PM10, or any real-world particle distribution.

---

## 3. Rated Operating Data (Manufacturer — Confirmed)

| Parameter | Value | Unit | Condition | Source | Evidence class |
|-----------|------:|------|-----------|--------|----------------|
| Rated airflow | 3600 | m³/h | Clean filter, manufacturer nominal | Freudenberg product page | **CONFIRMED — MANUFACTURER** |
| Rated face velocity | 2.84 | m/s | Derived: 3600/3600/0.3516 | Consistent with manufacturer stated value | **CONFIRMED** |
| Initial ΔP at rated conditions | 300 | Pa | Clean filter, manufacturer nominal | Freudenberg product page | **CONFIRMED — MANUFACTURER** |

---

## 4. Particle-Size Efficiency Data

| Particle size | Efficiency | Source | Evidence class |
|--------------|-----------|--------|----------------|
| MPPS (product-specific value not given) | ≥99.95% | Manufacturer H13 classification | **CONFIRMED — MINIMUM BOUND ONLY** |
| ~0.12–0.25 µm (generic glass fibre MPPS range) | ≥99.95% at MPPS | Generic glass fibre HEPA literature (not product-specific) | **GENERIC REFERENCE — NOT PRODUCT-SPECIFIC** |
| 0.1 µm | NOT AVAILABLE | No manufacturer data for this product | **NOT AVAILABLE** |
| 0.3 µm | NOT AVAILABLE | No manufacturer data for this product | **NOT AVAILABLE** |
| 0.5 µm | NOT AVAILABLE | No manufacturer data for this product | **NOT AVAILABLE** |
| 1.0 µm | NOT AVAILABLE | No manufacturer data for this product | **NOT AVAILABLE** |
| PM2.5 (0.1–2.5 µm integrated) | NOT AVAILABLE | No product-specific test data | **NOT AVAILABLE** |
| PM10 (0.1–10 µm integrated) | NOT AVAILABLE | No product-specific test data | **NOT AVAILABLE** |

**None of the particle-size-specific data has been obtained from Freudenberg for this product.**

---

## 5. Efficiency at AQI Tower Operating Conditions

The AQI Tower (CASE_M_SEALED, Phase 10B) operates at:
- Face velocity: **1.053 m/s** (vs manufacturer rated 2.84 m/s)
- This is 37% of the rated face velocity.

| Parameter | Value | Evidence class |
|-----------|-------|----------------|
| Efficiency at 1.053 m/s face velocity | NOT AVAILABLE | **NOT AVAILABLE — NO DATA** |
| How η changes with face velocity | NOT AVAILABLE | **NOT AVAILABLE — NO DATA** |
| Whether η increases or decreases at lower velocity | Physics predicts η generally increases at lower velocity (more diffusion time), but product-specific data is required to confirm | **GENERIC REFERENCE ONLY** |

At lower face velocity, glass fibre HEPA media typically shows equal or higher efficiency than at rated conditions because slower particles have more time for Brownian diffusion capture. However, this general statement from filter physics **cannot be cited as a confirmed property of this specific product without a test**.

---

## 6. What Is NOT Known

The following information is required for a rigorous CADR calculation or system-level efficiency claim, and is currently absent:

| Unknown | Why it matters | How to obtain |
|---------|---------------|---------------|
| Product-specific efficiency curve vs particle size | Cannot predict efficiency at real-world particle sizes | Request scan data or fractional efficiency curve from Freudenberg |
| Actual MPPS (exact particle size) | The MPPS for glass fibre HEPA media is typically 0.12–0.25 µm but is product- and test-condition-specific | Request from manufacturer or obtain from test report |
| Efficiency at AQI Tower face velocity (1.05 m/s) | Classification test was at 2.84 m/s; operating condition differs | Experimental measurement or manufacturer test at relevant velocity |
| Terminal (final loaded) ΔP | Required for service life and loaded operating point | Request from Freudenberg or conduct loading test |
| Multi-point ΔP curve | One data point (300 Pa at 2.84 m/s) currently; linear model is an approximation | Request from manufacturer or measure directly |
| Efficiency under humid conditions | Moisture affects glass fibre performance | Literature or experimental |
| Housing sealing and bypass (physical) | Even with CFD bypass sealed, physical installation may have leakage paths | Physical test with sealed housing |
| Particle charge / electrostatic effects | Not relevant for glass fibre HEPA, but confirm no electrostatic enhancement claimed | Manufacturer media specification |

---

## 7. Summary Assessment

| Claim | Status |
|-------|--------|
| Filter class is H13 per EN 1822 | **CONFIRMED** |
| Efficiency ≥ 99.95% at MPPS under EN 1822 test | **CONFIRMED** |
| Efficiency at PM2.5-relevant particle sizes | **NOT AVAILABLE** |
| Efficiency at AQI Tower operating face velocity | **NOT AVAILABLE** |
| CADR is established | **NOT ESTABLISHED** |

The H13 classification is confirmed. All other efficiency claims beyond the MPPS minimum bound require additional data.

---

## 8. Sources

| Source | Status | Date |
|--------|--------|------|
| Freudenberg product page (products.freudenberg-filter.com) | Retrieved Phase 6C | 2026-09-05 |
| EN 1822-1:2019 (classification standard) | Standard definition — publicly documented | — |
| `data/filters/freudenberg_SF13B_593x593x292.json` | Project data file | 2026-09-05 |
