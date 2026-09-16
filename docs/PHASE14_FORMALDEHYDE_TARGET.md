# AQI Tower Phase 14 — Formaldehyde Target Specification

**PHASE 14 ONLY — REQUIREMENTS / RESEARCH / SPECIFICATION**  
**TARGET STATUS: FROZEN FOR THE NEXT CONTROLLED EXPERIMENTAL PHASE**  
**No CFD run, CAD change, experimental result, removal-efficiency claim, CADR claim, or final bed design**

## Evidence labels used in this document

- **MEASURED — PROJECT:** result already produced by an AQI-TOWER simulation or future physical measurement.
- **MEASURED — LITERATURE:** value measured in a cited peer-reviewed study.
- **MANUFACTURER SPECIFICATION:** value published for a named product; it is not a project measurement.
- **GUIDELINE / OCCUPATIONAL LIMIT:** value published by an authority; it is not an AQI-TOWER test target unless explicitly selected below.
- **DERIVED:** arithmetic based on identified inputs.
- **ENGINEERING ASSUMPTION:** provisional value used to plan an experiment; it must be checked.
- **PROPOSED PROJECT TARGET:** a Phase 14 requirement selected for future verification.
- **UNKNOWN / REQUIRED FROM EXPERIMENT:** no defensible value is presently available.

## 1. Executive Decision

**Formaldehyde (HCHO / CH₂O, CAS 50-00-0) is frozen as the single gas-phase target for AQI-TOWER.** It ranks first in the Phase 14 weighted matrix at **82.8/100 — DECISION-MATRIX RESULT**, ahead of benzene (72.4) and toluene (72.2). Its combination of health significance, common indoor sources, an authoritative indoor-air guideline, measured Indian-home evidence, compound-specific measurement options, and a clear reviewer-facing experiment outweighs its two important disadvantages: hazardous testing and the uncertain performance of ordinary activated carbon.

The material decision is **B**:

> **Calgon Carbon OVC 4×8 remains the non-impregnated baseline research control, and a traceable formaldehyde-specific impregnated carbon—initially Calgon Carbon FORMASORB if obtainable—must be the secondary comparison.**

This does **not** mean that OVC 4×8 is proven suitable for the final tower. The manufacturer supplies no formaldehyde breakthrough capacity for OVC 4×8, and the formaldehyde literature emphasizes surface chemistry, modification and humidity rather than treating all activated carbons as equivalent [15, 27]. No removal percentage, bed life, or gas-phase CADR is established.

The baseline future test is **100 µg/m³ HCHO at 25 ± 2 °C, 50 ± 5% RH, and 0.10 s nominal EBCT — PROPOSED PROJECT TARGETS**. The primary breakthrough metric is `t10`: elapsed time and treated bed volumes until a sustained, time-aligned `C/C0 ≥ 0.10`, confirmed by a reference method. These settings define a bench experiment; they do not define final tower geometry.

## 2. Why Gas Removal Exists in AQI-TOWER

The H13 HEPA stage and the proposed carbon stage solve different problems:

- HEPA classification concerns **particles**, not gaseous molecules.
- A gas adsorber transfers a named compound to a finite-capacity solid and eventually breaks through.
- Particle-filter efficiency, gas removal efficiency, adsorption capacity, breakthrough time, bed life, and CADR are different quantities and must not be interchanged.

The gas stage therefore exists to investigate whether the tower can reduce one explicitly named indoor gas under controlled conditions. Phase 14 supplies that missing requirement. It does not expand the claim to “all VOCs,” “AQI,” odors, PM2.5, or PM10.

## 3. Candidate Pollutant Comparison

| Candidate | Health and indoor relevance | Measurement and controlled testing | Carbon-stage fit | Phase 14 assessment |
|---|---|---|---|---|
| **Formaldehyde** | Human carcinogen and sensory irritant; WHO has a 30-minute indoor guideline; pressed-wood and other indoor sources are well documented [1–5] | Dedicated low-cost modules can trend ppb-level changes, while DNPH–HPLC provides a recognized reference method [7–10] | Small, polar, humidity-sensitive molecule; ordinary GAC is uncertain and formaldehyde-specific media exist [15, 19, 20] | **SELECT** — strongest complete engineering story, provided hazardous testing is institutional |
| **Benzene** | Human carcinogen; WHO states that no safe exposure level can be recommended [1] | Typical indoor concentrations are low, compound-selective real-time measurement is substantially harder, and deliberate generation adds severe toxicity and flammability concerns | Non-polar aromatic vapour is generally compatible with ordinary GAC | **Do not select first** — strong health case but poor student-scale measurement/safety balance |
| **Toluene** | Common solvent VOC with important neurological effects at higher exposure; lower priority than HCHO/benzene at typical indoor levels | PID/analytical methods are available but inexpensive broad VOC sensors are not compound-specific | Stronger ordinary-GAC adsorption than HCHO makes a clean breakthrough experiment plausible | **Reserve as a future method-development surrogate**, not the health-led project target |
| **Acetone** | Common indoors and in breath/products, but substantially weaker health rationale at normal indoor levels | Easy to create and detect only at concentrations much higher than the desired indoor HCHO range; broad sensors cross-respond | Polar and humidity-sensitive; compound is less compelling to reviewers | **Reject as primary target** |
| **Ethanol** | Common transient indoor vapour but weak project health rationale | Cheap sensors exist, yet selectivity is poor and deliberate vapour work adds flammability | Water competition and weak retention can complicate interpretation | **Reject as primary target** |
| **Generic VOC / TVOC** | Useful as a ventilation/source indicator, but a mixture total cannot identify which compound produces the risk [13, 14] | A broad sensor can trend a mixed response, not a defensible species concentration | No single isotherm, capacity, breakthrough curve, or CFD species represents “TVOC” | **Reject as the single engineering target**; it may remain a secondary context channel |

## 4. Weighted Decision Matrix

Scores use a five-point ordinal scale: `1 = very poor`, `2 = poor`, `3 = workable`, `4 = good`, `5 = strongest`. Weights sum to 100. The total is `Σ(weight × score) / 5`. The numerical rank is a transparent project decision aid, not a toxicological standard.

| Criterion | Weight | HCHO | Benzene | Toluene | Acetone | Ethanol | TVOC |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1. Health significance | 14 | 5 | 5 | 3 | 2 | 1 | 2 |
| 2. Indoor relevance | 12 | 5 | 4 | 4 | 3 | 3 | 5 |
| 3. India / realistic deployment relevance | 8 | 4 | 4 | 4 | 3 | 3 | 5 |
| 4. Useful real-world concentration range | 7 | 5 | 2 | 4 | 4 | 4 | 5 |
| 5. Activated-carbon compatibility | 9 | 3 | 5 | 5 | 3 | 2 | 2 |
| 6. Measurement feasibility | 10 | 4 | 2 | 3 | 3 | 4 | 4 |
| 7. Controlled-test safety | 9 | 2 | 1 | 2 | 3 | 2 | 3 |
| 8. Defensible breakthrough experiment | 7 | 4 | 3 | 4 | 3 | 3 | 1 |
| 9. Future CFD species model | 6 | 4 | 4 | 4 | 4 | 4 | 1 |
| 10. Authoritative data availability | 7 | 5 | 5 | 4 | 3 | 3 | 3 |
| 11. Humidity behaviour can be investigated | 5 | 3 | 4 | 4 | 3 | 2 | 2 |
| 12. Reviewer communication | 6 | 5 | 4 | 3 | 2 | 2 | 2 |
| **Weighted total / 100** | **100** | **82.8** | **72.4** | **72.2** | **58.6** | **53.2** | **60.8** |
| **Rank** | — | **1** | **2** | **3** | **5** | **6** | **4** |

The HCHO score is not artificially maximized: it loses points for ordinary-carbon compatibility and test safety. Benzene and toluene remain technically credible future targets, but neither has HCHO's combined low-concentration measurement path, indoor guideline, Indian-home dataset, and clear formaldehyde-specific comparison medium.

## 5. Selected Target Gas

| Field | Frozen value | Evidence class |
|---|---|---|
| Chemical | Formaldehyde | **PROPOSED PROJECT TARGET** |
| Formula | HCHO / CH₂O | **AUTHORITATIVE IDENTITY** [5] |
| CAS number | 50-00-0 | **AUTHORITATIVE IDENTITY** [5] |
| Molecular weight | 30.0 g/mol | **AUTHORITATIVE IDENTITY** [5] |
| Conversion at 25 °C and 1 atm | 1 ppm = 1.23 mg/m³ | **NIOSH REFERENCE CONVERSION** [5] |
| Project role | Single compound used to specify and validate the gas-adsorption stage | **PROPOSED PROJECT TARGET** |

HCHO was selected as a gas-phase target; it does not replace the particulate requirements. A result for HCHO must not be generalized to benzene, toluene, “VOC,” odors, or AQI.

## 6. Real-World Concentration Context

| Context | HCHO concentration | Evidence class and interpretation |
|---|---:|---|
| General non-industrial indoor environments | 0.01–0.10 mg/m³ = **10–100 µg/m³** | **WHO REVIEWED RANGE** [2] |
| Homes | Usually below 0.05 mg/m³; reported range 0.005–0.25 mg/m³ = **5–250 µg/m³** | **WHO REVIEWED RANGE**, not a safety boundary [2] |
| New/renovated and hot/humid buildings | Levels above 0.2 mg/m³ = **200 µg/m³** can occur | **WHO REVIEWED CONTEXT** [2] |
| Ahmedabad/Gandhinagar homes, May 2019 | Median **22.73 µg/m³**; maximum **211.82 µg/m³** | **MEASURED — PEER-REVIEWED INDIA PILOT**, 90-minute samples in 26 homes [4] |
| Same India pilot, January 2020 | Median **25.85 µg/m³** | **MEASURED — PEER-REVIEWED INDIA PILOT** [4] |
| WHO indoor-air guideline | **0.10 mg/m³ = 100 µg/m³**, 30-minute average, not to be exceeded in any 30-minute period | **GUIDELINE VALUE**, not a project measurement [1–3] |
| NIOSH REL | TWA **0.016 ppm**; ceiling **0.1 ppm for 15 min**; IDLH **20 ppm** | **OCCUPATIONAL LIMIT / SAFETY CONTEXT**, not a public indoor target [5] |
| OSHA PEL / STEL | **0.75 ppm over 8 h / 2 ppm over 15 min** | **OCCUPATIONAL LEGAL LIMIT**, not permission to expose students or a laboratory [6] |

No verified, publicly accessible Indian national indoor HCHO exposure limit was found in the reviewed BIS/CPWD/BEE sources. CPWD's 2024 HVAC specification includes a TVOC verification value and ISO 16000 methods, and BEE's 2024 code addresses low-emitting materials, but neither source is used here as an Indian HCHO limit [25, 26]. The **100 µg/m³ value is therefore identified as the WHO guideline**, not an Indian regulation.

These categories must remain separate:

- **Real-world exposure** describes concentrations observed in buildings.
- **Guideline value** is an authority's health-protective benchmark.
- **Engineering challenge concentration** is a controlled inlet used to characterize the bed.
- **Sensor range** describes an instrument, not health or safety.
- **Occupational limit** regulates workplace exposure and is not a design target or a declaration of safety.

## 7. Engineering Test Concentrations

The proposed points fall within the WHO-reviewed indoor range and bracket the WHO guideline and the high end measured in the Indian pilot.

| Test point | At 25 °C and 1 atm | Purpose | Evidence class |
|---:|---:|---|---|
| **50 µg/m³** | **0.0407 ppm = 40.7 ppb — DERIVED** from the NIOSH conversion | Lower occupied-space challenge; close to the upper range of many homes | **PROPOSED PROJECT TARGET** |
| **100 µg/m³** | **0.0813 ppm = 81.3 ppb — DERIVED** | Baseline; coincides numerically with the WHO 30-minute guideline but is used as an engineering inlet | **PROPOSED PROJECT TARGET** |
| **200 µg/m³** | **0.1626 ppm = 162.6 ppb — DERIVED** | Elevated but plausible building challenge; improves measurement margin without entering ppm-scale testing | **PROPOSED PROJECT TARGET** |

**Baseline laboratory inlet:** `100 µg/m³`.  
**Full initial concentration set:** `50 / 100 / 200 µg/m³`.

The **proposed minimum useful quantified concentration is ≤5 µg/m³**, so that `C/C0 = 0.10` at the 50 µg/m³ inlet can be resolved with useful margin. This is a **PROPOSED MEASUREMENT REQUIREMENT**, not a claim about the selected continuous sensor. ISO 16000-3 states an approximate method range from 1 µg/m³ to 1 mg/m³ for DNPH cartridge sampling followed by HPLC, subject to the actual sampling volume, blanks, laboratory method, and uncertainty [7].

The SFA30's standard range is 0–1000 ppb, but its manufacturer-specified limit of detection is below 20 ppb and its accuracy at 0–200 ppb is ±20 ppb or ±20% of reading, whichever is larger, under its stated reference conditions [9]. Therefore:

- it covers all three **inlet** points;
- it is useful for continuous trend and mid/late breakthrough;
- it cannot, by itself, substantiate 5 or 10 µg/m³ outlet concentrations or the early `C/C0 = 0.05–0.10` region.

## 8. Outlet / Breakthrough Definition

For each run, calculate the time-aligned penetration ratio

`P(t) = C_out(t) / C_in(t) = C/C0`

after blank/background correction and correction for the measured empty-rig transport delay. ASHRAE 145.1 uses downstream/upstream concentration as penetration and `1 − penetration` as removal efficiency [17]. The thresholds below are **PROPOSED PROJECT DEFINITIONS**, not regulatory limits:

| State | Frozen Phase 14 definition |
|---|---|
| **Successful removal window** | `C/C0 ≤ 0.10` for a predeclared time or number of treated bed volumes, with measurement uncertainty reported. This is a run-specific result, not a permanent product claim. |
| **Early penetration** | `C/C0 = 0.05`; report `t05` only if the reference method's quantification limit and uncertainty support it. |
| **Breakthrough — primary** | `t10`: first time `C/C0 ≥ 0.10` is sustained across three consecutive predeclared evaluation windows, each at least 2 minutes for the SFA30 architecture, and is confirmed over the relevant reference-sampling interval. If time-integrated DNPH samples only bracket the crossing, report `t10` as an interval rather than a falsely precise timestamp. |
| **Partial breakthrough region** | `0.10 < C/C0 < 0.50`. |
| **Midpoint** | `t50` at `C/C0 = 0.50`; a robust secondary comparison when early outlet concentrations challenge the continuous sensor. |
| **Operational exhaustion** | `t95` at sustained `C/C0 ≥ 0.95`, or an earlier preapproved safety/time/mass-balance stop, whichever occurs first. |

Every curve must report both elapsed time and **treated bed volumes**, `BV = Q t / V_bed`. Report initial single-pass removal separately from dynamic capacity. Dynamic adsorbed mass may be calculated from `∫Q(C_in − C_out)dt`; dividing by actual dry media mass yields a run-specific dynamic capacity. None of these is interchangeable with filter efficiency, CADR, or bed life in a real building.

## 9. Temperature and RH Envelope

| Condition | Temperature | Relative humidity | Purpose | Evidence class |
|---|---:|---:|---|---|
| **Baseline** | **25 ± 2 °C** | **50 ± 5% RH** | Reproducible indoor benchmark; matches the center of the SFA30 accuracy condition and is close to ISO gas-media benchmark conditions | **PROPOSED PROJECT TARGET** [9, 18] |
| **Humidity stress** | **25 ± 2 °C** | **70 ± 5% RH** | Isolates the influence of higher water loading | **PROPOSED PROJECT TARGET** |
| **Hot-humid stress** | **30 ± 2 °C** | **70 ± 5% RH** | Plausible warm/humid deployment stress after the baseline and humidity-only run | **PROPOSED PROJECT TARGET** |

An optional dry diagnostic at `25 ± 2 °C / 30 ± 5% RH` may be added after the core matrix; it is not part of the frozen minimum set.

Humidity can compete for activated-carbon sites, change HCHO transport, and alter the chemistry of impregnated media. EPA/ASHRAE sources warn that adsorption performance depends on humidity [15, 16]. A formaldehyde study found strong RH-dependent breakthrough and improved performance for a modified carbon, but its high challenge conditions cannot be transferred as a capacity for AQI-TOWER [21]. The direction and magnitude of the effect must therefore be measured for each exact product and lot; no generic humidity correction is allowed.

## 10. Flow / EBCT Design Basis

Empty-bed contact time is

`EBCT = V_bed / Q = (A_bed × L_bed) / Q = L_bed / U_s`

where `A_bed` is bed face area, `L_bed` is settled depth, `Q` is volumetric flow, and `U_s = Q/A_bed` is superficial face velocity. Bed area controls velocity; depth and velocity jointly control EBCT and pressure drop. Increasing depth at fixed area increases EBCT and pressure loss. Increasing area at fixed flow lowers velocity and generally lowers pressure loss while increasing required packaging area.

Current project context:

- `Q ≈ 1332.2 m³/h = 0.370 m³/s` — **MEASURED — PROJECT CFD RESULT**, Phase 10B `CASE_M_SEALED`, partial/non-converged.
- HEPA gross face area `0.593 × 0.593 = 0.3516 m²` — **DERIVED** from the manufacturer dimensions.
- `0.370 / 0.3516 = 1.053 m/s` — **DERIVED HEPA-FACE VELOCITY**.

That HEPA velocity is not automatically the carbon-bed velocity. OVC 4×8's manufacturer pressure graph ends near 0.56 m/s, so using 1.053 m/s would be an unsupported extrapolation [19]. At the current modelled flow, keeping `U_s ≤ 0.52 m/s` would require at least `0.370/0.52 = 0.712 m²` of total bed face area—**DERIVED SCREENING VALUE, NOT FINAL GEOMETRY**. Parallel beds or a different area may eventually be investigated, but no architecture is selected in Phase 14.

### Proposed bench EBCT matrix

ISO 10121-1's loose-media benchmark uses a 26 mm bed and 0.26 m/s, giving 0.10 s EBCT; an academic packed-GAC study also used approximately 0.10 s and identifies roughly 0.02–0.2 s as a relevant effective range [18, 24]. The Phase 14 matrix centers on that benchmark:

| Nominal bed depth | Superficial velocity | Nominal EBCT | Role |
|---:|---:|---:|---|
| 26 mm | 0.52 m/s | **0.05 s — DERIVED** | Short-contact stress |
| 26 mm | 0.26 m/s | **0.10 s — DERIVED** | Baseline |
| 26 mm | 0.13 m/s | **0.20 s — DERIVED** | Long-contact comparison |

Use a column diameter at least ten times the maximum granule dimension where practical; for the OVC 4×8 specification's 4.75 mm upper screen, about 50 mm internal diameter is the minimum **ENGINEERING ASSUMPTION** for wall-effect control [19]. Record the actual particle distribution and column dimensions.

To show why EBCT does not prescribe a bed automatically, if the current `0.370 m³/s` flow and `0.3516 m²` area were retained, 0.05/0.10/0.20 s would imply bed volumes of 0.0185/0.0370/0.0740 m³ and depths of about 52.6/105/211 mm—**DERIVED SCENARIOS ONLY, NOT A DESIGN OR MATERIAL QUANTITY**.

## 11. Measurement Strategy

### Method comparison

| Method | Detection/selectivity | Calibration and humidity | Approximate cost class | Continuous breakthrough use | Decision |
|---|---|---|---|---|---|
| **Dedicated SFA30 digital HCHO module** | 0–1000 ppb standard range; 1 ppb resolution; `<20 ppb` manufacturer LOD; stated low ethanol cross-response [9] | Condition and co-locate before use; stated accuracy applies at 25 ± 3 °C and 50 ± 5% RH; compensate/log T/RH | **Low thousands of INR per module**; one current RS India listing was about **₹6,714 including tax — DISTRIBUTOR LISTING, VOLATILE**, not a budget quote [11] | Yes, for inlet, trends, and mid/late breakthrough; not sufficient alone for early low-outlet validation | **SELECT as continuous project monitor** |
| **Other electrochemical HCHO cell/instrument** | Can be compound-oriented, but limits, cross-sensitivities, drift, and electronics are model-specific | Zero/span calibration and humidity/temperature characterization required | Moderate; quote required | Potentially, only with a traceable model and validation | Conditional alternative; no unspecified cell is accepted |
| **Colorimetric detector tube** | Dräger HCHO 0.2/a is nominally 0.2–5 ppm; an extension method reaches about 0.04–0.5 ppm with stated large uncertainty/interferences [12] | Pump-volume verification and interference review required | Low instrument cost; recurring per-test tubes; current India quote required | No; discrete checks only | Screening/safety check, not the primary 50–200 µg/m³ method |
| **DNPH cartridge + HPLC/UV** | Compound-separated reference method; ISO method approximately 1 µg/m³–1 mg/m³ depending on sampling [7, 8] | Field blanks, calibrated flow, cartridge handling, laboratory calibration, and uncertainty required | High per campaign if outsourced; best obtained through an institutional analytical lab | No; time-integrated samples | **SELECT as primary validation/reference method** |
| **High-grade online optical/laser analyzer** | Best real-time selectivity and time resolution when calibrated for HCHO | Traceable zero/span and manufacturer QA required | Very high; borrow or collaborate rather than purchase initially | Yes | Preferred reference upgrade if a partner laboratory already owns one |
| **MQ-series / broad TVOC sensor** | Cross-sensitive broad response; cannot establish HCHO concentration at the selected ppb range | Strong calibration and environmental dependence | Very low | Trend only, not HCHO breakthrough | **REJECT for performance validation** |

### Selected architecture

`conditioned challenge air → upstream sample point/SFA30 → packed bed → downstream sample point/SFA30 → exhausted capture system`

with paired DNPH–HPLC samples upstream and downstream at the baseline, early-breakthrough, midpoint, and blank/reference states.

Requirements:

1. Use one common logger and clock for both sensors, flow, differential pressure, temperature, and RH. Log at **1 s intervals — PROPOSED PROJECT TARGET**; the sensor's internal response remains slower than the log interval [9].
2. Measure the empty-rig step-response/transport delay and time-shift downstream data before calculating `C/C0`.
3. Co-locate the two SFA30 modules before every campaign; quantify offset, then swap upstream/downstream positions in a repeat run to expose channel bias.
4. Use blank cartridges and a laboratory calibration curve. Place paired DNPH samples at both ports during the same interval.
5. Treat the SFA30 as the continuous curve instrument and DNPH–HPLC as the concentration reference. Around `t10`, collect shorter sequential reference samples within the validated method capability.
6. If the two continuous modules disagree beyond predeclared uncertainty, do not compute a removal claim until the discrepancy is resolved.

## 12. Formaldehyde Test Safety

Formaldehyde is a hazardous carcinogenic and sensitizing chemical. The selected concentrations are engineering challenges, not a declaration that handling is safe. Intentional HCHO generation is permitted only in an institutionally managed laboratory after written approval by the responsible safety authority.

### Required controlled-laboratory approach

- Use a commercially controlled, calibrated **permeation/dynamic-dilution system** or other validated traceable generator inside exhausted containment. OSHA and NIST methods demonstrate permeation-tube challenge generation with controlled carrier/dilution flow and independent analytical confirmation [22, 23].
- Use zero/clean carrier air, calibrated mass-flow control, an RH-conditioning branch, static mixing, compatible low-adsorption tubing, and an enclosed test column.
- Exhaust the entire outlet to an approved capture/scrubber or facility exhaust—never into a room or occupied space.
- Complete a chemical risk assessment, SDS review, leak and containment test, exposure-monitoring plan, PPE selection, spill/emergency plan, waste plan, and shutdown checklist under trained supervision.
- Use an independent area/alarm instrument appropriate to the facility; research sensors do not serve as the sole safety monitor.
- Enforce preapproved concentration, flow, pressure, time, and detector-alarm stop limits. Occupational limits are safety context, not operating permissions.

### Explicitly prohibited for this student project

- No open hotplate, heated formalin, paraformaldehyde, improvised polymer off-gassing, MDF/furniture chamber, or room dosing.
- No testing in a classroom, hostel/home, ordinary workshop, or occupied space.
- No student-only hazardous-gas operation and no discharge to ambient indoor air.
- No ppm-scale acceleration merely to shorten the test unless a qualified laboratory writes and approves a separate protocol and justifies data transfer.

### Student prototype demonstration

Students may validate the logger, airflow, leak checks, pressure sensors, timing, dashboards, and transport-delay logic using clean air or a facility-approved nonhazardous signal. Such a demonstration is **not an HCHO-removal experiment** and cannot support a removal, capacity, breakthrough, or bed-life claim.

## 13. GAC Material Decision

**Decision B — OVC 4×8 remains baseline; a formaldehyde-specific impregnated carbon is the secondary comparison.**

| Material | Verified facts | Missing evidence | Phase 14 role |
|---|---|---|---|
| **Calgon Carbon OVC 4×8** | Non-impregnated, steam-activated coconut-shell GAC; 4×8 US mesh (2.36–4.75 mm screen range), minimum hardness 97, minimum CTC activity 60; official typical pressure graph [19] | HCHO capacity, HCHO breakthrough curve, bulk density/porosity in retrieved sheet, and pressure data above graph range | **BASELINE RESEARCH CONTROL**, not final media |
| **Calgon Carbon FORMASORB** | Impregnated coconut-shell activated carbon explicitly marketed for formaldehyde/aldehydes; typical 1150 m²/g and 600 kg/m³ bulk density; 4×8 or 6×12 mesh [20] | Quantitative HCHO breakthrough at 50–200 µg/m³, pressure curve, humidity response, India stock/price | **SECONDARY FORMALDEHYDE-SPECIFIC COMPARISON**, conditional on exact-grade procurement and SDS |

OVC is retained because it is traceable, mechanically robust, and supplies a pressure-loss reference. It is not retained because HCHO performance is proven. Formaldehyde is small, polar, and very volatile; the literature reports that surface-modified/impregnated carbon can improve affinity and that humidity can materially alter behaviour [15, 21, 27]. Only matched blank, pressure, and breakthrough tests can decide whether either medium is useful.

No unverified e-commerce charcoal, raw soil biochar, or unlabeled “activated charcoal” may substitute for a traceable air-treatment grade.

## 14. Required Pressure-Drop Experiment

This clean-air experiment must occur before any gas breakthrough work.

### Apparatus and controls

- Straight test column with uniform inlet distributor, media-retaining screens, downstream settling length, calibrated flow meter, static pressure taps, differential-pressure instrument, and T/RH measurement.
- Column diameter selected against the exact lot's largest granule; begin from the `ID ≥ 10 d_max` wall-effect criterion.
- Test the empty column plus supports first, then subtract that fixture loss from the packed result.
- Apply a documented fill, vibration/settling, surface-leveling, and weighing procedure. Record loose and settled depth, mass, bulk density, lot, and replicate.

### Frozen proposed matrix

| Variable | Levels | Evidence class |
|---|---|---|
| Settled bed depth | **26, 52, 104 mm** | **PROPOSED EXPERIMENTAL LEVELS** |
| Superficial velocity | **0.13, 0.26, 0.52, 0.80, 1.05 m/s** | **PROPOSED LEVELS** spanning EBCT work, the OVC graph limit, and current tower context |
| Packing replicate | **3 independently repacked beds per material/depth** | **PROPOSED REPEATABILITY REQUIREMENT** |
| Air state | **25 ± 2 °C; 50 ± 5% RH** | **PROPOSED BASELINE** |

Progress to the high-velocity points only while the rig, media screens, dust containment, fan, and pressure instruments remain within approved limits. Do not extrapolate through an unsafe or unmeasurable point.

### Required outputs

1. Fixture-corrected `ΔP` versus superficial velocity for each depth and packing replicate.
2. Mean, scatter, hysteresis check, settled bulk density, and inspection for channeling or media movement.
3. Fit `ΔP/L = aU_s + bU_s²` only after measurement; report coefficient uncertainty and valid velocity/depth range.
4. Compare with, but do not force-fit to, the manufacturer's OVC graph.
5. Do not assign OpenFOAM Darcy/Forchheimer coefficients until the sign, units, and solver convention are independently checked.

## 15. Required Breakthrough Experiment

### Objective

Measure matched HCHO breakthrough curves for OVC 4×8 and the selected formaldehyde-specific comparison medium. The experiment determines initial penetration, `t10`, `t50`, `t95`/stop point, treated bed volumes, pressure loss, and run-specific dynamic capacity. It does not directly establish full-tower bed life.

### Controlled system

| Element | Frozen requirement |
|---|---|
| Gas generation | Qualified-laboratory permeation/dynamic-dilution generator or equivalently validated traceable source; no improvised open generation |
| Carrier air | Clean/zero air with documented HCHO blank; dry and humidified branches mixed under calibrated flow control |
| Inlet concentration | 50, 100, 200 µg/m³; verify actual `C_in`, do not rely only on calculated generation |
| Flow | Calibrated and reported at test temperature/pressure; nominal EBCT 0.05, 0.10, 0.20 s via the Section 10 matrix |
| Column | Approximate 50 mm minimum ID for OVC screening, finalized from actual `d_max`; 26 mm baseline settled depth; sealed supports and distributors |
| Media record | Exact grade/lot, SDS, dry/as-tested mass, moisture, particle distribution, packing method, settled depth/volume, bulk density and, if measured, porosity |
| Pressure | Continuous differential pressure across the packed bed plus empty-fixture correction |
| Gas measurement | Synchronized upstream/downstream SFA30 trends plus paired DNPH–HPLC reference samples |
| Environment | Bed inlet and outlet temperature/RH, logged with common timebase |
| Data | Raw concentrations, blanks, calibrations, Q, ΔP, T, RH, alarms, time, media record, operator/run ID, and uncertainty retained without smoothing away the raw record |

### Minimum sequence

1. Complete safety approval, blank/zero test, leak test, media-off-gassing blank, instrument co-location, and empty-system transport-delay test.
2. Stabilize and verify `C_in` before directing the closed challenge through the test bed.
3. Run the **100 µg/m³, 25 °C, 50% RH, 0.10 s EBCT** baseline first.
4. Repeat with **three independently repacked beds — PROPOSED REQUIREMENT** for each material at the baseline condition.
5. Perform the 0.05/0.20 s EBCT comparisons, then 50/200 µg/m³ concentration comparisons.
6. Run the 25 °C/70% RH and 30 °C/70% RH stresses only after stable baseline repeatability.
7. End at sustained `C/C0 ≥ 0.95` or the earlier approved maximum time, cumulative dose, pressure, leak, alarm, or facility limit.
8. Continue clean carrier flow or follow the facility's approved shutdown/capture procedure; handle spent media as the SDS/risk assessment requires.

Plot `C_in`, `C_out`, `C/C0`, Q, ΔP, T, and RH against both time and treated bed volumes. Report all repeats, not only the best curve. Any dynamic capacity is **MEASURED FOR THAT MATERIAL, LOT, CONCENTRATION, EBCT, TEMPERATURE, RH, AND ENDPOINT ONLY**.

## 16. CFD Readiness

### AVAILABLE NOW

| Input | Status |
|---|---|
| Target species identity, formula, CAS, molecular weight | **AVAILABLE — authoritative** |
| Baseline/test concentration requirements | **AVAILABLE — proposed targets** |
| Baseline/stress temperature and RH requirements | **AVAILABLE — proposed targets** |
| Existing sealed-tower airflow operating context (`Q ≈ 0.370 m³/s`) | **AVAILABLE — project CFD, partial/non-converged** |
| OVC grade identity and 2.36–4.75 mm screen specification | **AVAILABLE — manufacturer** |
| OVC typical pressure graph over its published range | **AVAILABLE — manufacturer graph only; not digitized or tower-range validated** |
| FORMASORB identity, typical bulk density and surface area | **AVAILABLE — manufacturer; not performance data** |
| Future model hierarchy | **DEFINED BELOW** |

### REQUIRED FROM EXPERIMENT

| Missing input | Why required |
|---|---|
| Actual bed area, depth, volume, mass, packing state and placement | Defines velocity, EBCT and model region; no final geometry exists |
| Lot particle distribution, settled bulk density and preferably porosity | Required for reproducible packed-bed description and Ergun cross-check |
| Multi-point `ΔP–U_s–L` data | Required to fit Darcy/Forchheimer resistance without invention |
| Darcy and Forchheimer coefficients with units/convention | **UNKNOWN until fitted and solver-checked** |
| Time-resolved `C_in`, `C_out`, Q, T and RH | Required to validate species transport and breakthrough |
| Initial penetration, `t10`, `t50`, `t95`, dynamic capacity and replicate scatter | Required to describe finite adsorption capacity |
| Humidity and temperature dependence | Required before transfer to Indian hot/humid conditions |
| Mass-transfer/rate parameter | Required for a mechanistic finite-capacity source term |
| Equilibrium/isotherm parameters | Required only if a Langmuir-type model is later justified |
| Full-tower gas mixing/bypass validation | Required before converting bench-media data into a tower claim |

**Gas-phase adsorption CFD is BLOCKED until the pressure and breakthrough inputs are measured.** An airflow-only porous-zone sensitivity may eventually use measured pressure coefficients without making an adsorption claim.

### Simplest defensible future model

1. **Measured porous resistance:** represent the chosen finite bed as a porous zone using the experimentally fitted Darcy–Forchheimer relation.
2. **Passive scalar without adsorption:** first transport HCHO as a dilute scalar to test mixing, residence time, bypass, boundary conditions, and numerical conservation.
3. **Initial-removal screening:** a fitted first-order sink may describe only the verified clean-bed/early-time regime. It must not predict saturation or bed life.
4. **Breakthrough model:** when replicated curves exist, add the simplest one-state finite-capacity empirical or linear-driving-force source/sink that reproduces `C/C0(t)` and validate it against a held-out EBCT or RH condition.
5. Use a Langmuir-type equilibrium model only after equilibrium data justify it. Do not create kinetic or isotherm constants from unrelated media or literature.

## 17. Remaining Data Gaps

1. India stock, exact grade/lot, MOQ, cost, lead time, SDS, and disposal/reactivation route for OVC 4×8 and FORMASORB.
2. OVC bulk density, porosity, HCHO capacity, breakthrough, pressure curve above the datasheet range, and humidity response.
3. FORMASORB pressure curve and quantitative HCHO performance at 50–200 µg/m³.
4. Institutional gas-generation, exhaust/capture, reference-HPLC, and safety-review access.
5. Exact SFA30 procurement cost, calibration route, unit-to-unit bias, long-term drift, T/RH effects, and HCHO-mixture cross-sensitivity.
6. Validated blank levels and losses in tubing, seals, column materials, and media supports.
7. Repeatable packing procedure and actual bed physical properties.
8. Pressure-drop and breakthrough datasets with uncertainty and repeatability.
9. Full-tower adsorption-stage face area, depth, placement, seals, leakage, allowable pressure budget, maintenance interval, and safe service method.
10. Effect of mixed indoor pollutants and any upstream water-stage moisture carryover; neither is part of the first single-species test.

## 18. Acceptance Criteria

Status describes whether Phase 14 has defined the requirement, not whether the future experiment has been performed.

| Requirement | Status |
|---|---|
| Single gas target selected | **READY** |
| Target concentration defined | **READY** |
| Laboratory concentration defined | **READY** |
| Outlet criterion defined | **READY** |
| Breakthrough definition defined | **READY** |
| Temperature defined | **READY** |
| RH defined | **READY** |
| Measurement method defined | **PARTIALLY READY** |
| Safety approach defined | **PARTIALLY READY** |
| GAC baseline defined | **READY** |
| Pressure-drop experiment defined | **READY** |
| Breakthrough experiment defined | **PARTIALLY READY** |
| CFD input requirements defined | **READY** |

The three partial items have complete conceptual architectures but depend on external facts not yet secured: exact instruments/calibration and analytical laboratory, institutional safety approval/facility, and a validated controlled HCHO source. The actual experiments and adsorption CFD remain blocked until those dependencies and materials exist.

## 19. Evidence Quality / Uncertainty

| Evidence class | What is accepted | Main limitation |
|---|---|---|
| **A — authority/standard** | WHO concentration context and guideline; NIOSH/OSHA identity and occupational limits; ISO/EPA analytical methods | Guidelines and occupational limits do not prove media performance |
| **A — manufacturer** | SFA30 specifications; OVC/FORMASORB identities and listed properties | Product sheets do not provide matched AQI-TOWER breakthrough data |
| **B — peer reviewed** | Indian-home measurements; adsorption/humidity mechanisms; packed-bed method context | Different media, concentrations and rigs cannot supply project coefficients |
| **C — project-derived** | Weighted decision, conversions, EBCT scenarios and experimental matrix | These are transparent choices/scenarios, not measured results |
| **UNKNOWN** | Removal efficiency, dynamic capacity, bed life, Darcy/Forchheimer coefficients, full-tower gas CADR | Must be measured and validated |

Important corrections to the supplied background summary:

- A `593 × 593 × 592 mm` or `150 mm` carbon bed and a `1–2 kg` mass are **not** frozen project dimensions and have no measured basis.
- No porosity, particle diameter, Ergun coefficient, Darcy coefficient, or Forchheimer coefficient is assigned from nominal mesh size.
- `0.370 m³/s` through `0.3516 m²` is **1.053 m/s**, not 0.37 m/s.
- OVC 4×8 is not stated to “effectively” remove HCHO; it is a neutral baseline requiring a formaldehyde-specific comparison.
- The SFA30 has 1 ppb resolution, but that is not a 1 ppb detection limit or accuracy. Its low-outlet limitation requires a reference method.
- An open hotplate/formalin/polymer source is not accepted. HCHO challenge work requires closed, controlled, institutionally approved generation and exhaust.

## 20. References

1. World Health Organization, *WHO Guidelines for Indoor Air Quality: Selected Pollutants* (2010), formaldehyde and benzene chapters: <https://www.afro.who.int/sites/default/files/2017-06/e94535.pdf>
2. WHO / NCBI Bookshelf, *Formaldehyde — WHO Guidelines for Indoor Air Quality: Selected Pollutants*: <https://www.ncbi.nlm.nih.gov/books/NBK138711/>
3. WHO, *Types of pollutants*: <https://www.who.int/teams/environment-climate-change-and-health/air-quality-and-health/health-impacts/types-of-pollutants>
4. *A Pilot Study to Quantify Volatile Organic Compounds and Their Sources Inside and Outside Homes in Urban India in Summer and Winter during Normal Daily Activities* (2022), DOI 10.3390/environments9070075: <https://doi.org/10.3390/environments9070075>
5. NIOSH Pocket Guide to Chemical Hazards, *Formaldehyde*: <https://www.cdc.gov/niosh/npg/npgd0293.html>
6. OSHA, *Hospitals eTool — Formaldehyde*: <https://www.osha.gov/etools/hospitals/laboratory/formaldehyde>
7. ISO 16000-3:2022, *Indoor air — Determination of formaldehyde and other carbonyl compounds*: <https://www.iso.org/standard/81864.html>
8. US EPA, *Compendium Method TO-11A — Determination of Formaldehyde in Ambient Air Using DNPH*: <https://www.epa.gov/sites/default/files/2019-11/documents/to-11ar.pdf>
9. Sensirion, *SFA30 product page and datasheet*: <https://sensirion.com/products/catalog/SFA30> and <https://sensirion.com/media/documents/DEB1C6D6/63D92360/Sensirion_formaldehyde_sensors_datasheet_SFA30.pdf>
10. Sensirion, *SFA30 Laboratory Testing Guide*: <https://sensirion.com/media/documents/BA78378E/65F015E2/GAS_AN_SFA30_Laboratory_Testing_Guide_D1.pdf>
11. RS India, *Sensirion SFA30 distributor listing* (price/stock are time-dependent): <https://in.rsdelivers.com/product/sensirion/3000422/sensirion-environment-sensor-digital-output-mount/2121796>
12. Dräger, *Detector Tube/CMS Handbook*, formaldehyde methods: <https://www.draeger.ie/admin/resources/pdf/17th-edition-tube-handbook2.pdf>
13. German Environment Agency, *German Committee on Indoor Air Guide Values* (TVOC interpretation): <https://www.umweltbundesamt.de/en/topics/health/commissions-working-groups/german-committee-on-indoor-air-guide-values>
14. Health Canada, *Guidance for indoor air quality professionals* (TVOC limitation): <https://www.canada.ca/en/health-canada/services/publications/healthy-living/guidance-indoor-air-quality-professionals.html>
15. US EPA, *EPA Air Pollution Control Cost Manual, Chapter 1: Carbon Adsorbers*: <https://www.epa.gov/sites/default/files/2018-10/documents/final_carbonadsorberschapter_7thedition.pdf>
16. ASHRAE Handbook, *Chapter 47 — Air Cleaners for Gaseous Contaminants*: <https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch47/a23_ch47_si.aspx>
17. ASHRAE, *Standard 145.1-2024 — Laboratory Test Method for Assessing the Performance of Gas-Phase Air-Cleaning Systems: Loose Granular Media* (current scope) and the public 2015 addendum containing the cited terminology: <https://www.ashrae.org/technical-resources/standards-and-guidelines/titles-purposes-and-scopes> and <https://www.ashrae.org/file%20library/technical%20resources/standards%20and%20guidelines/standards%20addenda/145_1_2015_a_20230228.pdf>
18. ISO, *ISO 10121-1:2014 — Gas-phase air-cleaning media* (current published edition, revision in progress), plus an accessible catalog rendering used for benchmark details: <https://www.iso.org/standard/51372.html> and <https://standards.iteh.ai/catalog/standards/iso/beb61744-b460-4b88-b0a8-09bccbf182ea/iso-10121-1-2014>
19. Calgon Carbon, *OVC 4×8 Product Bulletin*: <https://www.calgoncarbon.com/app/uploads/DS-OVC4x815-EIN-E2.pdf>
20. Calgon Carbon, *FORMASORB Product Bulletin*: <https://www.calgoncarbon.com/app/uploads/FORMASORB.pdf>
21. *Removal of gaseous formaldehyde by activated carbon: effect of humidity and modification of the adsorbent*, Chinese Journal of Chemical Engineering 17(4), 2009: <https://www.sciencedirect.com/science/article/pii/S1004954109600082>
22. OSHA Method 52, *Acrolein and Formaldehyde*—controlled permeation generation and analytical confirmation: <https://www.osha.gov/sites/default/files/methods/osha-52.pdf>
23. NIST, *Quantitative FT-IR Spectroscopy of Toxic Industrial Chemical Test Gases*—permeation-oven challenge generation: <https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917602>
24. Ali Khazraei Vizhemehr, *Predicting performance of activated carbon filters for indoor VOC removal* (Concordia University, 2014): <https://spectrum.library.concordia.ca/979033/>
25. Central Public Works Department, India, *General Specifications for Heating, Ventilation and Air-Conditioning Works 2024*: <https://www.cpwd.gov.in/Publication/HVAC_Specification_2024.pdf>
26. Bureau of Energy Efficiency, India, *Eco Niwas Samhita / ECSBC 2024*: <https://beeindia.gov.in/sites/default/files/publications/files/BEE%20ECSBC%202024.pdf>
27. Kang et al., *A Brief Review of Formaldehyde Removal through Activated Carbon Adsorption* (2022), DOI 10.3390/app12105025: <https://doi.org/10.3390/app12105025>

---

**TARGET GAS: FORMALDEHYDE (HCHO / CH₂O, CAS 50-00-0)**

**BASELINE MEDIA: CALGON CARBON OVC 4×8 AS THE NON-IMPREGNATED RESEARCH CONTROL; FORMASORB OR AN EQUIVALENT DOCUMENTED HCHO-SPECIFIC IMPREGNATED CARBON AS THE SECONDARY COMPARISON**

**BASELINE TEST CONCENTRATION: 100 µg/m³ (≈81.3 ppb at 25 °C and 1 atm)**

**BASELINE RH: 50 ± 5% RH**

**BASELINE TEMPERATURE: 25 ± 2 °C**

**PRIMARY BREAKTHROUGH METRIC: t10 — ELAPSED TIME AND TREATED BED VOLUMES TO SUSTAINED, TIME-ALIGNED C/C0 ≥ 0.10, REFERENCE-METHOD CONFIRMED**

**NEXT PHASE: CONTROLLED BENCH-TEST PREPARATION, TRACEABLE MATERIAL/INSTRUMENT PROCUREMENT, AND INSTITUTIONAL CHEMICAL-SAFETY APPROVAL — NOT STARTED IN PHASE 14**
