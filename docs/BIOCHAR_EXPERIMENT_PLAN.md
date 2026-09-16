# AQI Tower Phase 13 — Future Biochar Experiment Plan

**PLAN ONLY — NO EXPERIMENT PERFORMED**  
**PHASE 14 UPDATE — TARGET GAS: FORMALDEHYDE (HCHO)**  
**Use an exact, traceable media grade and institutional laboratory safety controls**

> **Phase 14 controls this future plan.** The frozen points are 50/100/200 µg/m³ HCHO; baseline 100 µg/m³, 25 ± 2 °C, 50 ± 5% RH and 0.10 s EBCT. OVC 4×8 is the non-impregnated control and a traceable HCHO-specific impregnated carbon is the secondary comparison. The early breakthrough metric is `t10` at sustained, time-aligned `C/C0 ≥ 0.10`. Use synchronized continuous HCHO monitors with DNPH–HPLC reference validation. See [`PHASE14_FORMALDEHYDE_TARGET.md`](PHASE14_FORMALDEHYDE_TARGET.md). If this older plan conflicts with that specification, the Phase 14 document governs.

## Objective

Produce the missing pressure-loss, gas-adsorption, breakthrough, and humidity data needed to decide whether a carbon bed is useful in the AQI Tower. Test the primary research candidate first only after a physical sample, SDS, lot certificate, and target-gas requirement are available.

The experiment must not use PM2.5 or PM10 as the primary carbon-bed challenge. The particulate stage and carbon adsorption stage have different purposes.

## Required Before Testing

1. Apply the Phase 14 frozen formaldehyde target and 50/100/200 µg/m³ inlet matrix; do not substitute a generic VOC mixture.
2. Apply the normalized Phase 14 outlet states and primary `t10` breakthrough criterion.
3. Obtain the exact media grade, lot number, SDS, certificate/data sheet, and supplier packing instructions.
4. Complete an institutional chemical risk assessment, ventilation plan, gas-cylinder procedure, leak test, emergency response, and waste plan.
5. Select calibrated gas analysis suitable for the compound and concentration. A broad low-cost “VOC sensor” is not a substitute for compound-specific analysis.

## Common Test Records

For every run record:

- media name, lot, precursor, activation/impregnation, particle-size distribution;
- dry and as-tested mass, moisture, bulk density, packing method, and bed settling;
- column inside diameter, bed depth, bed volume, support screens, and seal arrangement;
- airflow at test temperature/pressure, superficial velocity, temperature, and RH;
- upstream/downstream concentration and analyzer calibration;
- pressure drop, elapsed time, and replicate identifier;
- blank-column result, leakage check, and mass balance where possible.

## A. Pressure Drop

### Question

What pressure loss does the exact packed medium create as a function of superficial velocity, bed thickness, and packing state?

### Apparatus

- Straight transparent or metal test column with an inside diameter large enough to reduce wall effects relative to the media particle diameter.
- Uniform air distributor, retaining screens, upstream/downstream static-pressure taps, differential-pressure instrument, temperature/RH sensor, and calibrated airflow measurement.
- Clean, dry air for the baseline; no target gas is required for the first hydraulic tests.

### Proposed matrix

- At least three bed thicknesses, selected to bracket plausible cassette depths; suggested planning levels are 25, 50, and 100 mm until requirements are approved.
- At least six superficial velocities spanning the intended operating range. Begin safely below the official OVC graph limit and increase only while the test rig and fan remain within ratings.
- Test both freshly poured/loose packing and a repeatable settled packing state.
- Minimum three independently repacked repeats per condition.
- Run an empty-column/support-screen baseline and subtract only the measured fixture loss.

### Outputs

- ΔP versus superficial velocity for each bed depth and packing state.
- ΔP per unit bed length where scaling is demonstrated.
- Repeatability, hysteresis after settling, and uncertainty.
- Measured bulk density and, if feasible, bed void fraction.
- A Darcy-only fit if the measured relation is linear; otherwise a Darcy–Forchheimer fit. Do not force either model.

The activated-carbon industry method measures packed-bed pressure drop at multiple gas velocities and reports it per bed length; its geometry and calibration principles should inform the rig ([industry pressure-drop method](https://www.activatedcarbon.org/wp-content/uploads/2025/02/Test_method_for_Activated_Carbon_86.pdf)).

## B. Adsorption

### Question

For the selected gas, how do inlet and outlet concentrations differ under a documented flow, bed, temperature, and humidity condition?

### Procedure

1. Condition the media using the supplier-approved procedure and record its mass/moisture.
2. Establish clean carrier-air flow, temperature, and RH through the sealed column.
3. Introduce a certified target-gas challenge at the approved concentration.
4. Measure concentration upstream and downstream continuously or at a justified interval.
5. Measure pressure drop throughout the run.
6. Continue through the pre-approved breakthrough endpoint or a safe maximum duration.
7. Repeat with a blank column and at least three media replicates.

### Outputs

- Time series of upstream and downstream concentration.
- Single-pass concentration ratio at each time, always tied to the test condition.
- Adsorbed mass per dry media mass from a documented inlet/outlet mass balance.
- Temperature rise across the bed and any visible channeling, settling, or dust release.

Do not translate a laboratory capacity into a guaranteed real-world removal percentage or service interval.

## C. Breakthrough

### Question

When does downstream concentration begin to rise as available adsorption capacity is consumed?

### Required analysis

- Plot normalized concentration `C_out/C_in` against elapsed time and treated gas volume.
- Predefine reporting points such as 5%, 10%, and 50% `C_out/C_in`; these are proposed experimental markers, not product guarantees.
- Report breakthrough capacity, saturation capacity if reached safely, and the mass-transfer-zone behavior.
- Repeat at more than one flow/empty-bed contact time and at more than one inlet concentration if the target application spans those conditions.
- Check whether a second guard bed is needed for safe experimental containment; this is a test-safety decision, not a tower design decision.

EPA distinguishes saturation, breakthrough, heel, and working capacities and emphasizes outlet concentration and regeneration conditions as performance indicators ([EPA carbon-adsorber guidance](https://www.epa.gov/air-emissions-monitoring-knowledge-base/monitoring-control-technique-activated-carbon-adsorber)).

## D. Humidity

### Question

How does water vapor change pressure loss, breakthrough time, and capacity for the exact target gas and medium?

### Proposed comparison

- Use at least three controlled RH levels representing dry, typical, and high-humidity service; exact setpoints must follow the selected application.
- Hold gas concentration, temperature, flow, bed mass, depth, and packing constant.
- Equilibrate the bed at each RH before introducing the target gas.
- Record water uptake where feasible and test for condensation.
- For impregnated media, follow manufacturer humidity limits because water can help or inhibit reaction chemistry.

Published rice-husk activated-carbon data show lower VOC adsorption coefficients at 90% RH than at about 55% RH, while a specialized hydrophobic bamboo-derived carbon retained different fractions for different VOCs. These results justify testing humidity but do not supply a correction factor for the selected product ([Li et al., 2016](https://doi.org/10.1016/j.seppur.2016.06.029); [Rong et al., 2023](https://doi.org/10.1016/j.cej.2023.141979)).

## Safety and Disposal

- Do not conduct student exposure tests or release challenge gas to a room.
- Use a ventilated enclosure/fume extraction and downstream guard treatment approved for the selected chemical.
- Treat spent media according to the adsorbate and SDS; it may become hazardous waste.
- Do not attempt thermal or chemical regeneration in a student laboratory without a separate reviewed process.
- Control dust and ignition sources. Wet activated carbon can deplete oxygen in confined spaces ([OVC safety statement](https://www.calgoncarbon.com/app/uploads/DS-OVC4x815-EIN-E2.pdf)).

## Acceptance Gate for CFD Data

Pressure data become CFD-ready only when:

1. the exact grade and packing state are documented;
2. the measured velocity range covers the intended tower operating range;
3. repeated ΔP measurements have acceptable uncertainty;
4. bed-thickness scaling is checked; and
5. the selected Darcy or Darcy–Forchheimer fit reproduces held-out measurements.

Adsorption transport modelling requires an additional validated breakthrough dataset. Pressure readiness alone does not establish adsorption performance.
