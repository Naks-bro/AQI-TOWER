# Freudenberg Technical Data Request — AQI Tower Phase 12A

**PURPOSE:** Document what technical data has been found, what remains missing, and how to request it from the manufacturer.  
**Phase 12A — No CFD run or modified. No CAD changed.**

Last updated: 2026-09-06 (Phase 12A).

---

## 1. Product Identification (Exact)

| Field | Value |
|-------|-------|
| Manufacturer | Freudenberg Filtration Technologies |
| Article number | SF13-B-0593x0593x292/V12x25-N10N-J27-ACA |
| Series | SF13-B (HEPA High Volume Flow Filter) |
| Frame | Galvanized steel |
| Dimensions | 593 × 593 × 292 mm |
| Filter class | H13 (EN 1822), ISO 35 H (ISO 29463 equivalent) |
| Rated airflow | 3,600 m³/h |
| Rated face velocity | 2.84 m/s |
| Rated initial ΔP | 300 Pa (clean) |

This is the only confirmed data obtained to date (Phase 6C, from the manufacturer product page).

---

## 2. Data Available vs Data Required

| Data item | Needed for | Available | Source |
|-----------|-----------|-----------|--------|
| Filter class H13 (≥99.95% at MPPS) | CADR Level 1 estimate | YES | Freudenberg product page |
| Rated airflow and initial ΔP (single point) | CFD Darcy model | YES | Freudenberg product page |
| Fractional efficiency curve η(d_p) | CADR Level 2, particle CFD | **NO** | — |
| Actual MPPS particle diameter | CADR Level 2, particle CFD | **NO** | — |
| Efficiency at AQI Tower face velocity (1.053 m/s) | CADR Level 2 | **NO** | — |
| Multi-point ΔP vs face velocity | Accurate CFD model | **NO** | — |
| Terminal (loaded) ΔP | Service life estimate | **NO** | — |
| EN 1822 test certificate (product-specific) | Particle CFD with η | **NO** (but exists — see §4) | — |

---

## 3. Sources Searched in Phase 12A

The following sources were checked on 2026-09-06:

| Source | URL | Result |
|--------|-----|--------|
| Freudenberg product page (EU) — galvanized steel H13 | products.freudenberg-filter.com/en/detail/136582 | Nominal data only (300 Pa at 2.84 m/s, H13); no curve |
| Freudenberg product page (EU) — H13 high volume flow | products.freudenberg-filter.com/en/detail/8621 | 21 variants listed, all 300 Pa rated; no ΔP curve |
| Freudenberg product page (US) — H13 high volume flow | products.freudenberg-filter.com/en_US/detail/10893 | Same data; notes ISO 35 H equivalent; 250 Pa on some US variants |
| Freudenberg downloads centre | freudenberg-filter.com/en/downloads/ | Interface showed 0 results (JavaScript-rendered; download links not accessible) |
| Freudenberg product catalog PDF 2019/2020 | freudenberg-filter.com/media/.../Product_catalog_2019-2020_EN.pdf | Too large to retrieve (>10 MB); not fetched |
| Freudenberg filter classification page | freudenberg-filter.com/en/markets/industrial/standards-and-certifications/classification-of-air-filters/ | Classification frameworks only; no efficiency data |
| Freudenberg India contact page | in.freudenberg-filter.com/ | Address and phone confirmed; no data |
| Freudenberg global contacts | freudenberg-filter.com/en/markets/industrial/global-service-contacts/ | Addresses and phones confirmed; no data |
| Web search (fractional efficiency SF13-B) | — | No product-specific results found |
| Web search (technical data sheet SF13-B PDF) | — | No publicly accessible datasheet beyond product page |

---

## 4. Key Finding: Test Certificate Exists with Each Filter

The Freudenberg product page states:

> "Each filter element is tested for leakproofing in accordance with EN 1822, and delivered together with the corresponding test certificate."

This means that **an EN 1822 test certificate exists for every unit produced**, and it contains:
- The actual MPPS particle diameter measured for that unit
- The fractional efficiency at MPPS
- Individual local scan results (if EN 1822 Type Testing was conducted)

This test certificate is **not publicly available online** but would be physically supplied with a purchased filter. If a filter is purchased for the AQI Tower project, the test certificate should be retained and the efficiency data recorded.

---

## 5. Contact Routes for Data Request

### 5A. Freudenberg India (Recommended First Contact)

The project is India-based. Freudenberg Filtration Technologies India Pvt. Ltd. operates from Pune and serves industrial customers including HEPA filter users.

| Location | Address | Phone |
|----------|---------|-------|
| Pune HQ | 9th Floor, Fountainhead Tower 3B Wing, Phoenix Market City, Nagar Road, Viman Nagar, Pune 411014, Maharashtra | +91 20 67633600 |
| Production & Sales | Gat No. 837/2, Pune-Nagar Road, Village Sanaswadi, Taluka Shirur, Pune 412208, Maharashtra | +91 21 37615322 |

### 5B. Freudenberg International (Technical Data Requests)

| Contact | Detail |
|---------|--------|
| General email | info@freudenberg-filter.com |
| Global HQ phone | +49 6201 7107 264 |
| Address | Freudenberg Filtration Technologies GmbH & Co. KG, Höhnerweg 2-4, 69469 Weinheim, Germany |
| Contact form | Available at freudenberg-filter.com (footer link) |

---

## 6. Draft Data Request Message

The following is a draft inquiry that can be sent to Freudenberg India or international to request the missing technical data.

---

**Subject:** Technical data request — SF13-B-0593x0593x292/V12x25-N10N-J27-ACA HEPA H13 filter

Dear Freudenberg Filtration Technologies,

We are a student research team at [institution] developing a computational study of a tower-type air purification system (AQI Tower project). We have selected the Freudenberg SF13-B-0593x0593x292 H13 HEPA filter (article number: SF13-B-0593x0593x292/V12x25-N10N-J27-ACA) as the filtration element for our system.

We currently have the following confirmed data from your product page:
- Rated airflow: 3,600 m³/h
- Initial pressure drop: 300 Pa at 2.84 m/s face velocity
- Filter class: H13 (EN 1822)

To complete our CADR estimation and particle CFD study, we require the following additional technical data:

**Request 1 — Fractional efficiency curve**  
The efficiency η as a function of particle diameter, measured under EN 1822 test conditions. This is sometimes provided as a plot of efficiency vs. aerodynamic diameter from approximately 0.05 µm to 2 µm. Even three to five data points (e.g., at 0.1, 0.15, 0.2, 0.3, and 0.5 µm) would be sufficient for our purpose.

**Request 2 — MPPS particle diameter**  
The actual particle size at which filter efficiency is minimum for this product (the Most Penetrating Particle Size, as determined during EN 1822 testing).

**Request 3 — Multi-point pressure drop vs face velocity**  
Pressure drop data at two or more face velocities below the rated 2.84 m/s — particularly around 1.0–1.5 m/s — to characterize the filter resistance at AQI Tower operating conditions (1.053 m/s).

**Request 4 — EN 1822 test certificate**  
A copy of or excerpt from the EN 1822 test certificate for this product series showing fractional efficiency data.

Any data at a non-disclosure level that can be shared for academic research purposes would be greatly appreciated. We can provide a non-disclosure agreement if required.

Please let us know what documentation is available and under what conditions it can be shared.

Kind regards,  
[Name], [Institution]  
[Email], [Phone]

---

## 7. Alternative Data Acquisition Routes

If Freudenberg does not provide the fractional efficiency curve:

| Alternative | Approach | Evidence level | Notes |
|-------------|----------|----------------|-------|
| Physical purchase + test certificate | Buy one SF13-B-0593x0593x292 unit; read EN 1822 certificate supplied with it | Product-specific, manufacturer data | Highest quality for MPPS and integral efficiency; still only test velocity data |
| Laser particle counter upstream/downstream | Measure η at AQI Tower operating conditions in a controlled test rig | Direct measurement at operating velocity | Requires calibrated equipment; best for CFD validation |
| Conservtive η=1 particle tracking | Run Lagrangian CFD with all filter-face-arriving particles captured (η=1) | Conservative upper bound | No Freudenberg data needed; gives airflow delivery fraction only |
| Literature glass fibre HEPA curve | Apply published glass fibre HEPA efficiency models (e.g., Hinds, Brown, Payet) | Generic reference; NOT product-specific | Uncertainty is high; must be clearly labelled as a generic assumption |

---

## 8. Particle CFD Readiness Assessment

| CFD approach | Readiness | Blocking dependency |
|-------------|-----------|---------------------|
| Approach 3: Wall deposition + filter arrival fraction (η not needed) | **READY** | No external data needed; use CASE_M_SEALED airflow |
| Approach 2: η=1 at filter face (conservative capture) | **READY** | No external data needed |
| Approach 1: η(d_p) from Freudenberg data | **BLOCKED** | Awaiting Freudenberg fractional efficiency data |
| Level 2 CADR with η(d_p) | **BLOCKED** | Awaiting Freudenberg fractional efficiency data |

**Recommendation for Phase 12B:** Proceed with Approach 3 (conservative arrival fraction) and Approach 2 (η=1 upper bound). Dispatch the data request in §6 to Freudenberg India and international simultaneously. If test certificate is available, obtain it before any CADR estimate beyond Level 1.

---

## 9. Summary

| Question | Answer |
|----------|--------|
| Is fractional efficiency data publicly available? | **NO** — not found in any public source |
| Does the data exist? | **YES** — EN 1822 test certificate is issued with each filter |
| Can it be obtained? | **YES** — by purchasing a filter or contacting Freudenberg directly |
| Is particle CFD blocked entirely? | **NO** — conservative Approach 2/3 can proceed without η data |
| Is CADR Level 2 blocked? | **YES** — requires η(d_p) to compute meaningful CADR at specific particle sizes |
