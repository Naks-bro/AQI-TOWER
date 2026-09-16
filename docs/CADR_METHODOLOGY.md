# CADR Methodology — AQI Tower Phase 11

**METHODOLOGY AND FRAMEWORK ONLY — FINAL CADR IS NOT ESTABLISHED**  
**No CFD was run or modified in this phase.**

Last updated: 2026-09-06 (Phase 11).

---

## 1. What CADR Means

**Clean Air Delivery Rate (CADR)** is a measure of how quickly an air purifier delivers clean air to a space, for a defined pollutant. It combines two things:

### 1.1 Airflow (Q)

How much air the machine moves through the treatment stages per unit time. This is a mechanical property — it is determined by the fan curve, system resistance, and geometry. In SI units: m³/s or m³/h.

*AQI Tower Phase 10B result:* Q ≈ 1332 m³/h (CFD model, PARTIAL NON-CONVERGED).

### 1.2 Removal efficiency (η)

The fraction of a defined pollutant or particle population that is removed during a single pass through the treatment system. This depends on:
- The specific pollutant / particle size distribution
- The filter media, loading state, and face velocity
- Housing seal quality (leakage paths)
- Upstream and downstream mixing conditions
- The specific test protocol (chamber, particle generator, sensor)

*AQI Tower Phase 11:* η is **NOT ESTABLISHED** for any particle size.

### 1.3 CADR (single-pass, ideal mixing approximation)

For a simple single-pass system with ideal upstream and downstream mixing, CADR can be approximated as:

```
CADR ≈ Q × η
```

where Q is volumetric airflow (m³/h) and η is the fractional removal efficiency for the specific pollutant under the relevant test condition.

This relationship is an approximation that becomes exact only in an ideal test chamber with perfect mixing and steady-state particle concentration. In real installations, departure from ideal mixing, recirculation, particle settling, and sensor uncertainty all affect the measured CADR.

---

## 2. Formal CADR Standard (AHAM AC-1)

The most widely cited CADR standard for residential air purifiers is **AHAM AC-1-2015** (Association of Home Appliance Manufacturers), which defines:

- Test chamber: approximately 30 m³ room, 8 × 10 × 12 ft (≈ 27 m³)
- Three standard pollutants: tobacco smoke, dust (Arizona test dust), pollen
- Particle sizes measured: 0.09–1.0 µm (smoke), 0.5–3.0 µm (dust), 5.0–11.0 µm (pollen)
- Test protocol: constant-speed purifier, measure particle decay rate
- Result: CADR [ft³/min or m³/h] for each of the three pollutants

**AHAM CADR is a standardized test result, not a calculated value.** It cannot be predicted from airflow and filter classification alone without conducting the specified test or a validated equivalent.

Indian standards (IS/BIS) and ISO are developing or have separate air purifier test methods. The appropriate target standard depends on the intended market and application.

---

## 3. The Three Quantities and Why They Must Be Kept Separate

| Quantity | How obtained | Current AQI Tower status |
|----------|-------------|--------------------------|
| Airflow Q | Fan curve + CFD or physical measurement | CFD: Q ≈ 1332 m³/h (Phase 10B). Not physically measured. |
| Removal efficiency η | Filter test at relevant face velocity, particle size, loading | NOT AVAILABLE — only H13 ≥ 99.95% at MPPS under EN 1822 |
| CADR | Formal test protocol or Q × η with confirmed η | NOT ESTABLISHED |

Combining an unconfirmed η with a modelled Q does not produce a confirmed CADR. Any number produced from these inputs is a conditional estimate, not a product rating.

---

## 4. CADR Claim Hierarchy

The following levels define what can and cannot be claimed at each stage of evidence:

### LEVEL 0 — Airflow simulation only

**What it provides:** Modelled total volumetric flow rate Q.  
**Current AQI Tower position:** Phase 10B CFD gives Q ≈ 1332 m³/h (sealed geometry, PARTIAL NON-CONVERGED).  
**What can be claimed:** "The CFD model predicts ≈ 1332 m³/h total airflow through the sealed system at the modelled operating point."  
**What cannot be claimed:** Any filtration performance or CADR.

---

### LEVEL 1 — Manufacturer filter efficiency + CFD airflow

**What it provides:** An estimate of CADR using manufacturer classification efficiency and modelled airflow. No measurement of the assembled system.  
**Inputs available:**
- Q = 1332 m³/h (CFD, Phase 10B)
- η ≥ 99.95% at MPPS (H13 classification, EN 1822)

**Conditional estimate (THEORETICAL — NOT MEASURED CADR):**

```
CADR_MPPS [theoretical] ≈ Q × η_MPPS
                        ≈ 1332 m³/h × 0.9995
                        ≈ 1331 m³/h
```

**Explicit label for this number:** THEORETICAL / CONDITIONAL — NOT MEASURED CADR  
**What this number means:** If the filter actually achieves its H13 classification minimum (≥99.95%) at MPPS, and if all modelled airflow passes through the filter, and if there is no housing leakage, and if the operating face velocity does not reduce efficiency below the rated value — then the CADR at MPPS would be approximately 1331 m³/h.  
**What this number does not mean:**
- It is not a measured CADR.
- It does not apply to PM2.5, PM10, or any specific real-world particle size distribution.
- 99.95% at MPPS does not imply 99.95% for PM2.5 as a whole (PM2.5 spans multiple particle sizes, only some of which are near MPPS).
- The 1332 m³/h airflow is a CFD result, not a physical measurement.
- Housing leakage is not accounted for.

**What can be claimed at Level 1:** "Under the modelled airflow and the H13 classification minimum, a theoretical single-pass removal rate of ≥99.95% at MPPS is applicable. This gives a conditional theoretical CADR at MPPS of approximately 1331 m³/h. This is not a measured CADR."

---

### LEVEL 2 — System CFD particle model

**What it provides:** Numerical particle trajectories, deposition, filter interception fraction, and filter face approach conditions for defined particle sizes.  
**Current status:** Not yet planned in detail; methodology defined in `docs/PARTICLE_CFD_PLAN.md`.  
**Limitations:** CFD particle models also require validated boundary conditions, measured particle-size efficiency for the filter media, and do not substitute for a physical test.  
**What can be claimed:** Modelled particle removal fraction for defined sizes under CFD assumptions.

---

### LEVEL 3 — Controlled physical particle-removal test

**What it provides:** Measured upstream and downstream particle concentration under documented airflow, particle size, loading, and test conditions.  
**Requirements:** See §6 (Future Physical Test).  
**What can be claimed:** Measured single-pass efficiency for defined particle sizes at the tested conditions. Still not a formal CADR certification.

---

### LEVEL 4 — Repeatable validated CADR measurement

**What it provides:** CADR for defined pollutants under a recognized test standard (e.g., AHAM AC-1).  
**Requirements:** Compliance with the full test protocol, calibrated instrumentation, multiple repeats, and uncertainty quantification.  
**What can be claimed:** CADR for specified pollutants under the stated test standard.

---

## 5. System-Level Factors Preventing Direct Conversion from H13 to CADR

The following factors prevent directly converting the H13 filter classification into a product CADR, even with a known airflow:

| Factor | Description | AQI Tower status |
|--------|-------------|-----------------|
| Particle-size dependence | H13 specifies efficiency only at MPPS. Real pollutants span wide size ranges. Efficiency at each size is different. | No product-specific data across sizes. |
| Face velocity effect | EN 1822 tests at manufacturer rated conditions (2.84 m/s for this filter). AQI Tower operates at 1.05 m/s. The efficiency may differ (generally better at lower velocity for glass fibre media, but product-specifically unconfirmed). | Not measured. |
| Filter loading | HEPA ΔP and efficiency change as the filter accumulates particles. EN 1822 classifies a clean filter. Performance over time is uncharacterized. | Not modelled or measured. |
| Housing leakage | The CFD model (Phase 10B) sealed the bypass path numerically. A physical housing may have gaps at the filter frame, around cable penetrations, or at joints. Any leakage path bypasses the filter. | Not assessed physically. |
| Upstream/downstream mixing | CADR assumes adequate mixing in the test chamber. In real installations, short-circuit flows (clean air re-entering the inlet) can reduce effective CADR below the single-pass product. | Not assessed. |
| Particle settling | Heavier particles (> ~1 µm) may settle before reaching the filter. This could increase or decrease measured CADR depending on test configuration and sensor placement. | Not assessed. |
| Sensor uncertainty | Low-cost PM2.5 sensors (OPC-based, nephelometer) have large particle-size uncertainties. They cannot measure filter efficiency at the H13 level. Calibrated particle counters are required for efficiency measurement. | Not assessed. |
| Test chamber size | CADR depends on the test chamber volume and ventilation. A result measured in one chamber is not directly transferable to another space without applying the dilution model. | Not defined. |
| Particle charge | Some aerosols carry electrostatic charge that affects capture efficiency. Glass fibre HEPA does not rely on electrostatic charge (unlike electrostatically enhanced filters), so this is less sensitive — but test aerosol charge state matters for repeatability. | Not assessed. |

---

## 6. Current Conclusion

We currently have:

- A modelled airflow: Q ≈ 1332 m³/h (CFD, Phase 10B, PARTIAL NON-CONVERGED)
- A modelled HEPA pressure loss: ΔP ≈ 111 Pa (CFD, one-point Darcy model)
- Manufacturer H13 efficiency classification: ≥99.95% at MPPS (EN 1822)

We do NOT have:

- Measured system-level particle removal efficiency
- Measured CADR for any pollutant
- Product-specific efficiency curve vs particle size
- Efficiency at the AQI Tower operating face velocity (1.05 m/s)
- Physical validation of CFD airflow
- Housing leakage characterization

**FINAL CADR = NOT ESTABLISHED**

The conditional theoretical estimate (Level 1) of ~1331 m³/h at MPPS may be cited only if clearly labelled as THEORETICAL / CONDITIONAL — NOT MEASURED CADR.
