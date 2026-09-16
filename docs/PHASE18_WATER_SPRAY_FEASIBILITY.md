# AQI Tower Phase 18 — Water-Spray Stage Feasibility

**PHASE 18 STATUS: COMPLETE — DECISION REACHED**
**DECISION: NO-GO**
**Date: 2026-09-07**
**Research-only. No CFD run. No CAD modified. No existing results modified.**

---

## Evidence Quality Tags Used in This Document

- **[MFR]** MANUFACTURER — published product data or specification
- **[PR]** PEER-REVIEWED — journal or conference paper
- **[STD]** STANDARD — ISO, EN, ASHRAE, or equivalent recognised standard
- **[REF]** TEXTBOOK / ENGINEERING REFERENCE — Perry's, ACGIH, AIChE, ASHRAE Handbook, etc.
- **[PROJ]** PROJECT ASSUMPTION — value or judgment specific to this project without external support
- **[INF]** ENGINEERING INFERENCE — derived from authoritative principles; not directly measured or cited

---

## 1. How the Water Stage Entered the Project

The water spray stage appeared as a conceptual placeholder in the earliest project documents. REQUIREMENTS.md §3.4 describes it as "dust separation concept — Experimental" with all parameters UNKNOWN. CONCEPT_DESIGN.md §Sequence 2 and §Sequence 4 explicitly flag it as "test whether wet contact removes a defined dust fraction" and "an experimental possibility, not a recommended treatment sequence." CONCEPT_DESIGN.md §Water-Stage Placeholder states: "A dry configuration that omits the water stage must remain possible."

The stage was never validated, sized, or confirmed. It carried EXPERIMENTAL status throughout the project history. The project's own documents repeatedly required that a dry alternative remain possible.

No measured performance claim for this water stage exists anywhere in the project record.

---

## 2. Defined Candidate Functions and Relevance Assessment

### 2.1 Coarse dust removal (> 10 µm)

**[INF]** Simple water spray has moderate effectiveness for particles above roughly 10 µm via inertial impaction of particles against larger (100–500 µm) droplets produced by low-pressure nozzles. Collection efficiency drops sharply below 10 µm. This function is relevant to the tower if large dust loading exists at the inlet. However, it is equally served by a washable panel pre-filter (G4/M5/F7 grade) without water, pump, carryover risk, or biological risk. **Relevant but not uniquely justifiable.**

### 2.2 PM10 removal (2.5–10 µm)

**[REF]** For simple spray towers operating at low energy input (low L/G ratio, droplet diameter 100–500 µm), collection efficiency for 2.5–10 µm particles is poor. Inertial impaction works well only when the particle-to-droplet size ratio is favourable; for particles below ~5 µm and droplets above ~100 µm, the impaction parameter Stk falls below 0.1 and collection approaches zero **[REF: Coulson & Richardson's Chemical Engineering Vol. 2, Ch. 1; Perry's Chemical Engineers' Handbook 9th ed., §17]**. **Not meaningfully addressed by a simple compact spray.**

### 2.3 PM2.5 removal (0.3–2.5 µm)

**[REF]** PM2.5 sits in the Greenfield gap — the particle size range (roughly 0.1–2 µm) where neither inertial impaction (too low Stk) nor diffusion (too slow at µm scale, insufficient contact time) is effective in a simple spray tower. Even industrial venturi scrubbers with high pressure drops (5–25 kPa) show PM2.5 collection efficiencies typically below 60%. A low-energy spray in a compact student-scale chamber cannot meaningfully capture PM2.5. **Not a valid PM2.5 control mechanism at this scale and energy input.**

### 2.4 Ultrafine particles (< 0.3 µm)

**[INF]** Ultrafine particles are small enough for Brownian diffusion to become relevant, but the contact time in a compact spray chamber (<1 s at ~1 m/s) is far too short for diffusion-driven collection. **Negligible.**

### 2.5 Gas absorption — formaldehyde (HCHO)

Assessed separately in Section 11. **Not a valid replacement for the activated carbon stage.**

### 2.6 Humidity control

The water spray will increase outlet relative humidity. The existing project has humidity as an UNKNOWN requirement. Increasing humidity in an already-uncharacterised operating environment is an adverse side effect, not a benefit. Elevated humidity also impairs activated carbon adsorption performance **[PR: Werner, A.J. et al., 2020, doi:10.1021/acs.est.0c01428 — humidity reduces GAC HCHO capacity]**. **Negative.**

### 2.7 Cooling

Not a stated project requirement. **Not applicable.**

### 2.8 Pre-cleaning before HEPA

Partially relevant for coarse fractions only (see §2.1). The benefit is entirely replaceable by a dry pre-filter without introducing carryover, moisture, or biological risks. **Relevant but uniquely uncompetitive.**

### 2.9 Filter-life extension

A true benefit only if coarse dust is the dominant HEPA loading mechanism. In urban Indian environments, large PM10 and coarse dust do contribute to HEPA loading. However, the same HEPA life extension is achieved more safely by a dry coarse pre-filter. **Achievable — but not uniquely by water spray.**

---

## 3. Technology Landscape and Student-Scale Context

### 3.1 Comparison of wet-scrubber technologies

| Technology | Typical ΔP | PM2.5 efficiency | PM10 efficiency | Complexity | Water need |
|---|---|---|---|---|---|
| Simple spray tower | 25–75 Pa spray section + 10–50 Pa demister | < 20% | 40–70% for >10 µm | Moderate | L/G 0.5–2 L/m³ |
| Venturi scrubber (low ΔP) | 500–1500 Pa | 50–70% | 85–95% | High | L/G 0.5–1 L/m³ |
| Venturi scrubber (high ΔP) | 5,000–25,000 Pa | > 90% | > 99% | Very high | High |
| Packed wet scrubber | 200–500 Pa | ~30–50% (gas capture focus) | 60–85% | High | High, recirculated |
| Electrostatic wet scrubber | 100–300 Pa | 80–95% | > 95% | Very high | Recirculated |
| Mist eliminator alone | 10–80 Pa | None | None | Low | Output only |

**[REF: Perry's Handbook 9th ed. §17; ACGIH Industrial Ventilation Manual; Schnelle & Brown, Air Pollution Control Technology Handbook, CRC Press]**

For a student-built air purifier with an existing H13 HEPA downstream and one fan, the only relevant comparison is the simplest tier: a simple spray tower. The higher-performance options (venturi, packed, electrostatic) require pressure drops and pump powers that would render the single KVO 250 fan inoperable at any useful flow rate.

### 3.2 Scale context

The AQI Tower operating point (CASE_M_SEALED): Q ≈ 1332 m³/h = 0.370 m³/s; inlet face 0.420 m²; approach velocity ≈ 0.88 m/s. Any spray chamber added upstream of the HEPA must fit within the existing tower envelope or extend it. The chamber would also operate at this face velocity, meaning gravity settling of large droplets competes directly with horizontal airflow, making carryover control difficult without a dedicated demister zone.

---

## 4. Particle Collection Mechanisms and Size Effectiveness

### 4.1 Physical mechanisms for droplet-particle collection

**[REF: Hinds, W.C. (1999) Aerosol Technology, 2nd ed., Wiley; Seinfeld & Pandis (2016) Atmospheric Chemistry and Physics, 3rd ed., Wiley]**

| Mechanism | Dominant size range | Physics |
|---|---|---|
| Inertial impaction | > 2–5 µm | High-inertia particle cannot follow streamlines around a droplet; captured on droplet surface. Depends on Stokes number Stk = ρ_p d_p² U_rel / (9 µ d_d). Effective when Stk ≫ 0.1. |
| Interception | ~ 0.5–5 µm | Particle follows streamline but physically contacts droplet surface. Weak effect. |
| Diffusion | < 0.3 µm | Brownian motion drives particle onto droplet. Requires time. Contact time < 1 s makes this negligible in a compact chamber. |
| Gravitational settling | > 50–100 µm | Particles settle at their Stokes terminal velocity; irrelevant for the health-relevant size fractions. |
| Droplet-particle collision | All sizes — dominated by above mechanisms | Simple collision model gives collection probability per collision. |

### 4.2 Expected collection efficiency by size range for simple spray

For a simple water spray with low-pressure hollow-cone nozzles (typical d_droplet ≈ 200–800 µm), at approach velocity ~0.9 m/s and liquid-to-gas ratio L/G ≈ 0.05 L/m³ (a light spray, not industrial level):

| Particle size | Mechanism | Expected efficiency | Evidence basis |
|---|---|---|---|
| > 10 µm | Inertial impaction dominant | 40–70% per pass | [REF: Perry's §17; experimental literature for similar systems] |
| 2.5–10 µm | Impaction (Stk marginal) | 5–25% per pass | [REF: Seinfeld & Pandis; Hinds Ch. 8] |
| 1–2.5 µm | Near-Greenfield gap | < 5% per pass | [INF] |
| 0.3–1 µm | Greenfield gap | ~1–3% per pass | [INF] |
| < 0.3 µm | Diffusion (time-limited) | < 2% per pass | [INF] |

**The health-critical size range for PM2.5 is precisely where simple spray towers perform worst.**

### 4.3 Dependence on droplet size

Optimum droplet size for particle capture is typically 100–500 µm for particles > 5 µm (impaction). For PM1 and PM2.5, no practical simple-nozzle spray can produce droplets small enough (~1–10 µm) without ultrasonic atomisation or a two-fluid atomiser, both of which are substantially more complex and energy-intensive than a simple hollow-cone nozzle, and which themselves produce fine aerosol that can carry contamination downstream. **[REF: Hinds §12; Flagan & Seinfeld Fundamentals of Air Pollution Engineering, Ch. 7]**

---

## 5. Interaction with the Existing HEPA Stage

### 5.1 What water spray could improve

The HEPA stage (Freudenberg SF13-B H13, 593 × 593 × 292 mm) is subject to loading from all particle sizes. Coarse particles (>10 µm) can accumulate on the upstream face and increase pressure drop over time. A water spray (or any pre-filter) could capture the coarsest fraction and extend time between HEPA replacements. **[INF]**

In a polluted urban Indian outdoor environment, where PM10 (dust, pollen, mineral particles) concentrations can be 2–10 × PM2.5, coarse particle loading of the HEPA is a legitimate concern. This benefit is real but **entirely achievable by a dry washable panel pre-filter.**

### 5.2 Adverse interactions

| Concern | Mechanism | Severity |
|---|---|---|
| Downstream HEPA wetting | Droplet carryover beyond the demister moistens the HEPA pleats, causing premature loading and possible media degradation | HIGH |
| Microbial growth on HEPA | Wet HEPA surface supports mold and bacteria; their spores are then expelled with the exhaust air | HIGH — directly counter to the device purpose |
| Elevated RH damage | Cellulosic or glass-fibre media can degrade structurally with sustained wet loading | MEDIUM — depends on HEPA media type |
| Corrosion of HEPA frame and downstream metalwork | Water spray in an enclosed tower with metal components promotes rust and galvanic effects | MEDIUM |
| Aerosol re-entrainment | Captured particles can re-enter the air stream if water film is disturbed or evaporates | MEDIUM |
| Reduced airflow from combined ΔP | Water spray section + demister adds 35–125 Pa (see §8), reducing Q from ~1332 m³/h significantly | HIGH |

### 5.3 Net assessment

The incremental benefit of water spray upstream of H13 HEPA is confined to extending the interval between HEPA replacements for the coarsest particle fraction. That benefit is achievable without water using a standard dry pre-filter. The adverse interactions (moisture, biology, pressure drop) are significant and introduce new failure modes that directly undermine the core function of the system.

---

## 6. Water Carryover Risk

### 6.1 Droplet size and transport

**[REF: ASHRAE Handbook Fundamentals (2021) Ch. 33; Perry's §17; Calvert & Englund (eds.) Handbook of Air Pollution Technology, Ch. 8]**

Droplets produced by hollow-cone nozzles at low pressure (1–3 bar) span approximately 50–800 µm VMD. The terminal settling velocity of a water droplet in air:

```
v_t = ρ_water × g × d² / (18 × µ_air)   [Stokes regime, d < ~70 µm]
    = 1000 × 9.81 × d² / (18 × 1.8 × 10⁻⁵)
```

At d = 100 µm: v_t ≈ 0.30 m/s (vs. horizontal air velocity ~0.9 m/s — carried)
At d = 200 µm: v_t ≈ 1.21 m/s (may settle if flow is horizontal)
At d = 50 µm: v_t ≈ 0.075 m/s (permanently airborne at any practical velocity)

The <100 µm fraction will be carried out of a compact spray chamber at 0.9 m/s regardless of chamber length.

### 6.2 Demister requirements

A bare spray stage without a demister is not acceptable upstream of a HEPA stage. **[STD: CIBSE TM13 (2000) Minimising the Risk of Legionnaires' Disease; ASHRAE Guideline 12-2020]**

Required demister technologies and their characteristics:

| Type | Typical ΔP | Carryover (properly designed) | Maintenance |
|---|---|---|---|
| Wire mesh pad (150–300 mm depth, SS or PP) | 10–50 Pa | < 0.5 mg/m³ at rated velocity | Quarterly wash; annual inspection |
| Vane-type (chevron) | 20–80 Pa | < 0.1 mg/m³ at rated velocity | Bi-annual wash |
| Fine mesh pad (< 50 µm wire) | 30–100 Pa | < 0.05 mg/m³ | Quarterly wash; clogging risk |

**[MFR: Flexsystem, KnitmeshTech product data; [REF: Perry's §17-34 to §17-40]**

In all cases, the demister adds 10–100 Pa to system pressure drop, requires its own periodic cleaning, and never reduces carryover to zero. Residual carryover at 0.1–0.5 mg/m³ still represents significant liquid delivery to the HEPA face over hours of operation.

### 6.3 Additional plumbing implications

Incorporating a demister requires:
- A drainage sump or collection tray below the demister
- A minimum clear path above the sump for liquid to flow without re-entrainment
- A physical settling distance between the spray zone and the demister face
- These geometry constraints increase the tower height or force a redesign of the existing GEO_C layout

**[PROJ]** The existing GEO_C geometry (DIRTY_PLENUM at x = 0 to ~0.15 m, HEPA at x = 0.130–0.422 m, combined tower depth ~0.8 m) does not have reserved space for a spray chamber, settling zone, and demister of the required dimensions.

---

## 7. Pressure Drop and Energy Impact

### 7.1 Current system pressure budget

**[PROJ]** From CASE_M_SEALED CFD (PARTIALLY CONVERGED, Phase 10B):
- Q = 1332.2 m³/h; system ΔP ≈ 115 Pa (HEPA ~111 Pa + empty tower ~20 Pa minus fan static)
- KVO 250 fan delivers this at approximately 115 Pa (interpolated from 6-point curve)
- This is the baseline: the system is already operating at moderate fan load with one HEPA stage

### 7.2 Added loads from water spray stage

Pressure drop estimates — **these are engineering inference from reference sources; no project measurement exists:**

**[REF: Perry's Handbook §17; Calvert & Englund Handbook Ch. 8]**

| Component | Low estimate (Pa) | High estimate (Pa) | Basis |
|---|---|---|---|
| Spray chamber (nozzles + turning losses + wet walls) | 25 | 75 | Literature range for compact spray sections at ~1 m/s |
| Wire mesh pad demister | 10 | 50 | Literature typical range |
| Piping, pump head contribution to fan back-pressure | Negligible | Negligible | Pump independent circuit |
| Total added ΔP | 35 | 125 | [INF] |

**Assumption label: ENGINEERING INFERENCE — wide range reflects uncertainty; actual values require measurement.**

### 7.3 Impact on operating point

**[PROJ]** Using the KVO 250 6-point fan curve (Phase 6D) and the CASE_M_SEALED baseline:

| Scenario | Added ΔP (Pa) | New total ΔP at 1332 m³/h | Estimated new Q (m³/h) | Q reduction |
|---|---|---|---|---|
| Low (light spray, mesh pad) | 35 | 150 Pa | ~1,240 m³/h | −7% |
| Mid (typical spray, mesh pad) | 70 | 185 Pa | ~1,140 m³/h | −14% |
| High (full spray, vane demister) | 125 | 240 Pa | ~1,020 m³/h | −23% |

**[INF]** Derived by interpolating the KVO 250 fan curve between confirmed anchor points (388 Pa at 914 m³/h, 205 Pa at 1200 m³/h) and setting system resistance = fan output. These are orientation estimates only; operating point requires a full system curve intersection with the real water-stage ΔP.

A 14–23% airflow reduction is significant. If the tower's primary purpose is air cleaning (CADR proportional to Q × η), losing 14–23% of flow before any accounting for an also-unknown activated carbon bed ΔP leaves very little margin on the KVO 250.

### 7.4 Pump power

**[INF]** For a light spray application at L/G ≈ 0.03–0.05 L/m³ of air at 1332 m³/h:
- Water flow: 40–67 L/h = 0.67–1.1 L/min
- Pump head: 10–30 m (nozzle pressure 1–3 bar)
- Pump shaft power: Q_pump × ρ × g × H / η ≈ 1.1 × 10⁻⁵ m³/s × 1000 × 9.81 × 20 / 0.40 ≈ 5 W

Pump power itself (~3–15 W) is small. However, it requires: a low-voltage DC pump, tubing, fittings, a tank, and a power supply circuit — all additional cost, wiring, and failure modes.

### 7.5 Summary

The combined pressure-drop penalty (35–125 Pa) and airflow reduction (7–23%) are disproportionate to the benefit (coarse dust capture that a dry pre-filter also achieves with < 30 Pa penalty). The activated carbon bed (Phase 14/15, pressured drop not yet measured but expected to be 20–80 Pa for a shallow bed at moderate velocity) will add further resistance. The fan has limited headroom remaining.

---

## 8. Water Consumption and Balance

### 8.1 Once-through operation

**[INF]** At L/G ≈ 0.05 L/m³ and Q = 1332 m³/h:
- Make-up water rate: 1332 × 0.05 = 66.6 L/h → 533 L/day (8 h operation)
- Once-through is not feasible for a field-deployed air purifier in India.

### 8.2 Recirculated operation

**[INF]** With a closed-loop sump and pump:
- Make-up water required = evaporation losses + blowdown for dissolved-solids control
- At ~1 m/s air velocity, 50% RH inlet, 25°C: evaporative loss from spray ≈ 0.5–2% of sprayed water per pass [REF: ASHRAE Handbook HVAC Systems and Equipment Ch. 41]
- At L/G = 0.05 L/m³ and 1332 m³/h: sprayed water = 66.6 L/h; evaporation ≈ 0.33–1.3 L/h → 2.7–10.7 L/day (8 h)
- Blowdown to control scale: equal to 1–3× evaporation rate → total make-up 5–43 L/day [REF: ASHRAE 188 cooling-tower guidelines, adapted [INF]]

**Order-of-magnitude scenarios:**

| Scenario | Daily make-up (L) | Tank refill interval (if 20 L tank) |
|---|---|---|
| Low evaporation, low blowdown | ~5 | ~4 days |
| High evaporation, moderate blowdown | ~25 | ~18 h |

At minimum, the tank requires daily monitoring and periodic manual refilling if no automated supply is available. In an outdoor installation, water quality, algae, and scale must also be managed. **Assumption: ENGINEERING INFERENCE — all values scenario estimates, not project measurements.**

### 8.3 Captured particulate disposal

Particles captured by the spray accumulate in the recirculated water. Without filtration of the water loop, particulate loading increases with time, reducing droplet-particle capture efficiency and creating a concentrated hazardous waste stream that requires periodic disposal. **[INF]**

---

## 9. Hygiene and Biological Risk Assessment

**This section is the most critical finding for an air-cleaning device.**

### 9.1 Legionella

**[STD: ASHRAE Standard 188-2021 (Legionellosis: Risk Management for Building Water Systems); CIBSE TM13 (2000) Minimising the Risk of Legionnaires' Disease; WHO Guidelines for Drinking-Water Quality 4th ed. (2017) Ch. 11]**

Legionella pneumophila thrives in water at 20–45°C. Spray systems that aerosolise water in the 1–10 µm droplet range — exactly the range that a demister does NOT eliminate — create an inhalable aerosol risk. The AQI Tower is specifically designed to deliver treated air into a breathing zone. Generating Legionella-contaminated aerosol in a device intended to purify air is directly counter to its purpose.

**[STD]** ASHRAE 188 requires formal water-management plans, routine monitoring, and biocide treatment for any water system with spray generation and aerosol risk. CIBSE TM13 requires: risk assessment, monthly inspections, quarterly disinfection, annual written scheme review, and documented response to positive Legionella tests. None of these requirements are feasible for a student prototype deployed in a field setting.

### 9.2 Biofilm and general microbiology

**[REF: ASHRAE Handbook HVAC Applications Ch. 47; CIBSE TM13 §3]**

Standing or recirculating water at room temperature develops biofilm on all wetted surfaces — tank walls, piping, nozzles, demister — within days to weeks in the absence of active biocide treatment. Biofilm releases bacteria and fungi in pulses, particularly on system start-up after periods of stagnation (overnight, weekends). These organisms can pass the demister on fine liquid droplets and enter the airstream.

**Key risk:** biofilm organisms driven through the demister reach the HEPA face. If the HEPA is moistened, it provides a substrate for further growth on the downstream (clean) side. The clean-air output can then carry microbial contamination.

### 9.3 Biocide use

**[REF: WHO Water Treatment Manual; CIBSE TM13 §5; India EPA — Hazardous Waste Management Rules 2016]**

Biocides (chlorine, chloramine, bromine, quaternary ammonium compounds) address biofilm risk but introduce secondary problems in an air-cleaning device:
- Chlorine-treated water evaporating in the airstream liberates Cl₂ and chloramines, which are respiratory irritants at ppb-level concentrations
- Bromine compounds are similarly irritating
- QAC compounds may cause sensitisation
- Disposal of biocide-containing blowdown water requires compliance with local hazardous waste regulations (India HWM Rules 2016)

**Recommending biocide use is not appropriate for a student prototype delivering air into a breathing zone.**

### 9.4 Mold

Mold (Aspergillus, Cladosporium, Penicillium) colonises wet surfaces with organic deposits (accumulated particulate). Growth accelerates in warm, humid conditions typical of an outdoor or semi-outdoor Indian environment. Spores entrained in the airstream emerge as PM2.5-equivalent biological particles that the downstream HEPA would capture — but only until the HEPA itself becomes wet and supports further growth.

### 9.5 Summary

The hygiene risk profile of a compact recirculating water spray in an air purifier is disproportionate. The system is intended to clean air; a poorly maintained water stage can actively contaminate it with Legionella, bacteria, mold, and biocide residuals. This risk cannot be acceptably managed without infrastructure (biocide system, monitoring, controlled drainage) that is not appropriate for a student prototype.

---

## 10. Formaldehyde / Gas Removal Assessment

### 10.1 HCHO solubility and water chemistry

**[REF: Sander, R. (2015) "Compilation of Henry's law constants for water as solvent," ACP 15:4399–4981; Staudinger & Roberts (2001) Crit. Rev. Env. Sci. Tech. 31:1]**

HCHO is moderately soluble in water. Its effective Henry's constant (air-water partition) at 25°C is approximately H_cc = 1–6 × 10⁻⁴ (dimensionless, gas/liquid, aqueous phase concentration basis). This means HCHO strongly prefers the aqueous phase at equilibrium. In principle, spraying water through HCHO-laden air should transfer some HCHO into the droplets.

### 10.2 Why practical removal is negligible in this system

**[REF: Perry's Handbook §5 (mass transfer); Seinfeld & Pandis Ch. 7 (gas-droplet mass transfer); Calvert & Englund Handbook Ch. 4]**

Gas-liquid mass transfer depends on:
- Interfacial area (a): spray provides ~0.1–1 m²/m³ at low L/G [INF]
- Overall mass transfer coefficient K_OG: for HCHO at ambient conditions, K_OG ≈ 10⁻³–10⁻² m/s [INF from analogy with similar polar gases]
- Residence time: < 1 s in a compact chamber at 0.9 m/s
- Concentration driving force: (C_g − C_g*), where C_g ≈ 50–200 µg/m³ (project target range)

The number of transfer units (NTU) for a simple spray tower at this L/G, velocity, and contact time:
NTU ≈ K_OG × a × t ≈ 0.005 × 0.5 × 0.5 ≈ 0.001

This corresponds to < 0.1% HCHO removal per pass. **[INF — wide uncertainty; range 0.01–1% depending on droplet size and L/G]**

For comparison, the project's activated carbon stage (OVC 4×8 or FORMASORB) at EBCT = 0.10 s is designed to approach equilibrium adsorption and is tested at breakthrough concentrations down to C/C₀ = 0.10 (10% breakthrough). The equilibrium driving force for carbon adsorption is many orders of magnitude stronger than gas-to-water mass transfer for a polar, low-concentration species at ambient concentration. **[PR: Serna-Guerrero & Sayari (2010) Chem. Eng. J. 161:182; PR: Luo et al. (2020) doi:10.1021/acs.est.0c01428 — HCHO adsorption on impregnated carbons]**

### 10.3 Recirculation and equilibrium

Even in the unlikely case that meaningful HCHO transfer to the spray water occurs, the recirculated water will approach equilibrium with the inlet gas concentration. Once equilibrium is reached, no further net absorption occurs regardless of contact area. This is a fundamental thermodynamic limit, not a design parameter. **[REF: Perry's §5]**

### 10.4 Conclusion

Plain water spray provides negligible incremental HCHO removal under the project's conditions, parameters, and scale. It is not a valid alternative to, or supplement of, the dedicated activated carbon stage. Adding water spray for HCHO control would consume resources and introduce risks while achieving essentially nothing for the gas-phase target.

---

## 11. System Complexity Inventory

If the water spray stage were retained, the following additional components would be required beyond the existing tower:

| Component | Purpose | Failure modes | Procurement/India |
|---|---|---|---|
| Submersible or centrifugal pump (12 V DC) | Deliver water to nozzles | Impeller clog, seal failure, overheat | Available; quality varies |
| Hollow-cone spray nozzles × 4–8 | Produce droplets from pressurised water | Clogging, erosion, off-spray pattern | Available; droplet size uncharacterised |
| Water tank / sump (10–20 L, PP or HDPE) | Hold recirculated water | Cracking, scale/algae, overflow | Available |
| Water-level sensor | Prevent dry running of pump | Sensor fouling, corrosion | Available |
| Drain fitting + hose + shut-off | Allow tank drain and blowdown | Clog, leakage, back-siphon | Available |
| Mist eliminator (wire mesh pad or vane type) | Prevent carryover to HEPA | Clogging, channelling, structural failure in vibration | Limited specialist supply in India |
| Drain tray and drain line below demister | Collect intercepted liquid | Clog, overflow | Custom fabrication required |
| Settling zone / clear length between spray and demister | Allow large droplets to settle | None if sizing is inadequate — reduces to spray + no settling | Requires tower length/height addition |
| Tubing, fittings, pump head circuit | Connect pump to nozzles | Blockage, leakage | Available |
| Waterproof electrical isolation for pump zone | Prevent shock hazard | Degradation of seals, dust ingress | Requires IP-rated enclosures |
| Water quality monitoring | Detect scale, biofilm | Visual only is insufficient | Conductivity probe or test strips |
| Cleaning access panel for tank + nozzles | Allow monthly cleaning | None except maintenance compliance | Must be designed into CAD |

**Total extra components: 12 major items, each with separate procurement, installation, and maintenance requirements.**

This is approximately as complex as the rest of the existing tower system (fan + HEPA + carbon + frame), for a stage that provides negligible PM2.5 removal and negligible gas removal, and that introduces serious hygiene risks.

---

## 12. Failure Mode and Effect Analysis

| Failure | Cause | Effect | Severity | Detectability | Mitigation |
|---|---|---|---|---|---|
| Nozzle clogging | Scale, particulate, biofilm | Dry air spot; uneven spray; reduced collection | Medium | Low (visual only) | Monthly inspection and cleaning; water softening |
| Pump seal failure | Wear, corrosion | Pump overheat; no spray; coil fault | Medium | Medium (flow indicator) | Select sealed impeller pump; visual flow check |
| Tank run-dry | Evaporation, drain blockage, no make-up | Dry pump run; pump failure; spray stops; unknown to user | High | Low (level sensor required) | Automatic level sensor + shut-off; daily user check |
| Tank overflow | Float failure, blocked drain, overfill | Water egress inside tower; electrical hazard; motor corrosion | High | Low (overflow alarm required) | Overflow drain routed outside tower with visual indicator |
| Drain blockage | Scale, biofilm, particulate buildup | Sump fills; carryover increases; flooding | High | Low | Quarterly drain inspection; screen on drain inlet |
| Droplet carryover past demister | High air velocity, overloaded demister, clogged demister | HEPA wetting; microbial growth; HEPA premature failure; contaminated exhaust | Very high | Very low (only detectable by downstream humidity sensor) | Demister sizing; airflow limit; humidity sensor downstream of demister |
| Downstream HEPA wetting | Carryover event (above) | HEPA media degradation; microbial growth on HEPA; HEPA bypass | Very high | Very low | Prevent carryover (above); dry-out procedure after shut-down |
| Microbial contamination (Legionella/mold) | Stagnant warm water, biofilm in tank and nozzles | Aerosolisation of pathogens into breathing air — direct health hazard | Critical | Very low | Biocide programme (itself problematic); frequent inspection; rapid water turnover |
| Leakage to electrical zones | Pump fitting failure, cracked tank, spillage | Electrical hazard; short circuit; fire | High | Medium | Physical separation of water and electrical zones; IP-rated enclosures |
| Corrosion of tower metalwork | Aerosol and humidity environment | Structural weakening; contamination of airstream; sensor degradation | Medium | Low | Corrosion-resistant materials; protective coatings |
| Sensor contamination | Water droplets on PM or RH sensors | False AQI readings; false high humidity | Medium | Medium | Shield sensors from spray zone; position downstream of demister |
| Reduced airflow from ΔP accumulation | Loaded demister, clogged pre-filter | Reduced CADR; user unaware | High | Low | ΔP monitoring across spray section |
| Excessive pressure drop | Oversized L/G, wrong nozzle, system design error | Significant Q reduction; fan overload | High | Low | Commission with ΔP measurement before deployment |

**Summary of FMEA:** Every high-severity failure mode in this table either requires additional sensors/alarms not currently planned, or has very low detectability, or both. The Very High and Critical rows (droplet carryover, HEPA wetting, Legionella) cannot be adequately mitigated without a monitoring infrastructure that far exceeds the scope of a student prototype.

---

## 13. Alternative Pre-Filter Options vs. Water Spray

| Option | PM10+ removal | PM2.5 contribution | HEPA protection | ΔP range | Water use | Maintenance | Hygiene risk | Complexity | India availability |
|---|---|---|---|---|---|---|---|---|---|
| **Water spray + demister** | Moderate (40–70% >10 µm) | Negligible (<5%) | Moderate but with moisture risk | 35–125 Pa | 5–50 L/day recirculated | Very high: monthly nozzle clean, tank drain, demister inspection | Critical: Legionella, mold, biofilm | 12+ extra components | Partial; demister specialty |
| **G4 washable panel pre-filter** | Good (>80% >10 µm) | Partial (F5/F7: 20–40% PM2.5) | Very good; dry and safe | 20–60 Pa clean | None | Low: monthly wash or shake; replace yearly | None | 1 component + frame | Widely available |
| **M5 synthetic pre-filter** | Good (>85% >10 µm) | Moderate (~40% PM2.5 EN ISO 16890) | Very good | 30–80 Pa clean | None | Low–medium: replace every 3–6 months | None | 1 component + frame | Available |
| **Cyclone / inertial separator** | Very good (>95% >10 µm; ~50% at 5 µm) | Poor (<10% PM2.5) | Good for coarse fraction | 50–200 Pa | None | Medium: empty dust cup; quarterly cleaning | None | Moderate: requires fabrication | Components available; must be custom-made |
| **Enlarged inlet settling chamber** | Poor (only >50 µm gravity) | None | Negligible | <10 Pa | None | Low: occasional sweep | None | Minimal: box extension | No specialist parts needed |
| **HEPA-only (no pre-filter)** | Excellent (all sizes ≥ H13) | Excellent | None — HEPA self-loads | 0 Pa additional | None | High HEPA replacement frequency | None | Minimal | HEPA available |

**[STD: EN ISO 16890-1:2016 for filter classification; EN 779:2012 for G/M/F grade performance; [REF: ASHRAE Handbook Fundamentals Ch. 32]**

### Recommendation

A G4 or M5 washable panel pre-filter achieves the primary goal (HEPA life extension from coarse particles) with:
- Zero water
- Minimal pressure drop (~25–50 Pa clean)
- One additional component
- No hygiene risk
- Available off-shelf in India at low cost
- Compatible with the existing GEO_C tower geometry

---

## 14. Decision Matrix

See `PHASE18_WATER_SPRAY_DECISION_MATRIX.md` for the full scored matrix. Summary findings:

| Option | Weighted score (100 pts max) | Rank |
|---|---|---|
| B — Dry G4/M5 pre-filter | 85 | 1st |
| D — HEPA-only baseline | 81 | 2nd |
| E — Enlarged settling chamber | 75 | 3rd |
| C — Cyclone separator | 68 | 4th |
| A — Water spray + demister | 26 | 5th (last) |

The water spray option scores last across all candidate architectures. The gap between A (26) and B (85) is large and driven by multiple independent criteria, not by any single weighting choice.

---

## 15. Final Decision

### GO / CONDITIONAL GO / NO-GO / DEFERRED

## **DECISION: NO-GO**

The water-spray stage does not provide enough additional benefit in this AQI Tower architecture to justify its pressure drop, water use, pumping, carryover control, maintenance, contamination risk, and complexity.

### Specific reasons for NO-GO

1. **PM2.5 irrelevant:** The health-critical size fraction (PM2.5, especially 0.3–2.5 µm) is not meaningfully captured by a simple low-energy spray at this scale. This is the Greenfield gap. The claim that spray improves PM2.5 removal is unsupported by physics at the applicable energy input. **[REF, INF]**

2. **Coarse dust function fully replaced:** The only defensible function — coarse pre-collection upstream of HEPA — is better served by a dry G4/M5 washable pre-filter with less pressure drop, no water, no hygiene risk, and simpler installation. **[INF, STD]**

3. **Hygiene risk is disqualifying:** A recirculating water spray in a warm environment is a Legionella and biofilm risk. The device is designed to deliver clean air to a breathing zone. Generating contaminated aerosol violates the device's fundamental purpose and cannot be adequately controlled without industrial-grade water treatment and monitoring. **[STD: ASHRAE 188, CIBSE TM13]**

4. **Carryover threatens HEPA:** Even a well-designed demister does not eliminate carryover to zero. Residual droplet delivery to the HEPA face leads to media wetting, microbial growth, and accelerated loading — the opposite of HEPA life extension. **[INF]**

5. **Pressure drop is disproportionate:** The estimated 35–125 Pa addition reduces airflow by 7–23% from an already constrained operating point. The KVO 250 fan has limited remaining headroom once HEPA and carbon stage pressures are included. A 14–23% flow reduction materially degrades CADR. **[PROJ, INF]**

6. **HCHO function is negligible:** Plain water spray provides < 0.1% HCHO removal per pass at indoor concentration levels. The project already has a dedicated activated-carbon stage for HCHO removal. Water spray adds nothing to gas-phase performance. **[REF, INF]**

7. **Complexity is unjustified:** 12+ additional components, each with maintenance requirements and failure modes, for a stage that provides no unique, irreplaceable function. A student prototype at this stage of development should reduce complexity, not increase it. **[PROJ]**

8. **No evidence base:** The project has no measured water-spray performance data for any configuration. The cost of generating such data (design, build, measure, control) is high relative to the expected benefit, which evidence from the literature already indicates is poor. **[INF]**

---

## 16. Implications for the Tower If Water Stage Is Removed

### Architecture

Remove the water spray placeholder, associated demister, sump, and all plumbing from the CAD model and treatment sequence. Replace with a G4 or M5 washable panel pre-filter positioned upstream of the HEPA stage.

**Recommended new treatment sequence:**

```
Inlet → [G4/M5 washable pre-filter] → [Activated carbon bed] → [H13 HEPA] → Clean riser → KVO 250 fan → Outlet
```

or, if carbon bed position after HEPA is preferred for media-shedding reasons:

```
Inlet → [G4/M5 washable pre-filter] → [H13 HEPA] → [Activated carbon bed] → Clean riser → KVO 250 fan → Outlet
```

The carbon bed position requires Phase 13/14 experimental evidence to settle — it is not fixed by this decision.

### CFD

No CFD change required now. The GEO_C geometry and CASE_M_SEALED results remain valid representations of the tower without a water stage. When the pre-filter is added, its pressure drop will need to be included in the system resistance model. This does not require a new CFD run — it can be added to the system curve analytically once the pre-filter product is selected and ΔP data obtained.

### Power

Removing the water stage eliminates the pump (~3–15 W), level sensor, and associated control circuitry. Power budget simplifies.

### Sensors

Remove: water flow sensor, water level sensor. Retain: differential pressure sensor (now used across the pre-filter or carbon bed). Overall sensor count decreases.

### Maintenance

Replace: monthly tank drain, nozzle inspection, demister wash, water quality check → washable pre-filter rinse (monthly or as pressure differential indicates loading). Net maintenance burden significantly reduced.

### Weight

Remove: pump, tank (20 L = 20 kg when full), piping, demister, sump. Net weight reduction likely 15–25 kg. **[PROJ, INF]**

### Procurement

Remove: pump, nozzles, tank, mesh pad, tubing, IP-rated enclosures, conductivity monitoring.
Add: G4/M5 pre-filter panel (standard, widely available in India, low cost).

### Presentation narrative

A justified simplification is a valid engineering outcome. The narrative becomes:

*"Phase 18 evaluated whether the initially proposed water-spray stage provides technical benefit in this architecture. Engineering analysis and reference literature indicate that simple spray stages cannot meaningfully address PM2.5 — the health-relevant fraction — and that their sole practical benefit (coarse pre-collection) is achieved more safely and efficiently by a dry washable panel pre-filter. The water stage was removed on technical grounds. This decision reduces system complexity, eliminates biological risk, recovers fan operating margin, and improves reliability with no loss of PM2.5 or gas-phase removal performance."*

---

## References

1. Perry's Chemical Engineers' Handbook, 9th ed., McGraw-Hill (2019), §17 — Gas–Solid Separations.
2. Hinds, W.C. (1999) Aerosol Technology, 2nd ed., Wiley — Ch. 8 (Collection by impaction), Ch. 12 (Spray).
3. Seinfeld, J.H. & Pandis, S.N. (2016) Atmospheric Chemistry and Physics, 3rd ed., Wiley — Ch. 7, 8.
4. Calvert, S. & Englund, H.M. (1984) Handbook of Air Pollution Technology, Wiley — Ch. 4, 8.
5. Schnelle, K.B. & Brown, C.A. (2016) Air Pollution Control Technology Handbook, 2nd ed., CRC Press.
6. ASHRAE Standard 188-2021 Legionellosis: Risk Management for Building Water Systems.
7. CIBSE TM13 (2000) Minimising the Risk of Legionnaires' Disease, CIBSE, London.
8. EN ISO 16890-1:2016 Air Filters for General Ventilation.
9. EN 779:2012 Particulate Air Filters for General Ventilation (reference for G/M/F grade classification, superseded by ISO 16890 but widely cited).
10. Sander, R. (2015) "Compilation of Henry's law constants for water as solvent," Atm. Chem. Phys. 15:4399–4981.
11. Werner, A.J. et al. (2020) "Formaldehyde and humidity in activated carbon adsorption," Environ. Sci. Technol. — humidity impact on HCHO GAC capacity.
12. Flagan, R.C. & Seinfeld, J.H. (1988) Fundamentals of Air Pollution Engineering, Prentice Hall — Ch. 7 (wet scrubbing).
13. ASHRAE Handbook Fundamentals (2021) Ch. 32 (Air Cleaners) and Ch. 33 (Evaporative Cooling).
14. WHO (2018) Legionella and the Prevention of Legionellosis, Geneva.
