# AQI TOWER — ENGINEERING REQUIREMENTS

This document defines what the proposed AQI Tower must eventually achieve and what information is still missing. It does not select a final architecture, component, dimension, or performance target.

## Requirement Status System

| Status | Meaning |
| --- | --- |
| CONFIRMED | Requirement supplied by the project team. |
| PROPOSED | Reasonable initial proposal but not approved. |
| UNKNOWN | Information is currently missing. |
| ASSUMPTION | Temporary engineering assumption required for modelling. |
| SOURCE REQUIRED | Value must come from a datasheet, scientific source, standard, or experiment. |
| EXPERIMENTAL | Must be validated physically. |
| SIMULATION | Will be determined through modelling. |

Status describes the maturity of a requirement, not whether the current concept can satisfy it. Where no value has been supplied, the value is recorded as **UNKNOWN — REQUIRES REQUIREMENT**.

## 1. Product Objective

The intended product is a tower-type air treatment or purification system that moves ambient air through multiple treatment stages and discharges treated air.

The exact application environment is **NOT YET FINALIZED**. Possible applications include:

- Indoor spaces
- Semi-enclosed spaces
- Localized outdoor environments

These are possibilities, not confirmed requirements. The intended air volume, pollutant exposure, weather conditions, occupancy, placement, and operating pattern cannot be specified until the application is selected.

## 2. Current Concept

The team's current conceptual idea includes:

- A vertical tower form
- Air intake
- Air exhaust
- Multiple fans
- Electrical power
- Solar-assisted power
- HEPA filtration
- A biochar or biomass-derived adsorption or filtration stage
- An experimental water spray or dust-separation stage

**This is a conceptual starting point and is not yet an engineering-validated architecture.**

## 3. Requirement Categories

### 3.1 Airflow

| Parameter | Current value | Status | How it must be established |
| --- | --- | --- | --- |
| Target airflow | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Derive from the selected application, treated air volume, pollutant objective, and operating time. |
| Volumetric flow rate | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Specify a rated operating flow and a measurement condition. |
| Air changes / turnover | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Define only if the selected application has a meaningful enclosed or semi-enclosed air volume. |
| Inlet velocity | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Determine after airflow and inlet area are defined; verify by simulation and measurement. |
| Outlet velocity | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Determine after airflow and outlet area are defined; verify by simulation and measurement. |
| System pressure drop | UNKNOWN — REQUIRES REQUIREMENT | SOURCE REQUIRED | Combine sourced component pressure drops with later modelling and physical measurement. |
| Allowable pressure drop | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Set from required airflow and the usable fan operating range. |
| Flow uniformity | UNKNOWN — REQUIRES REQUIREMENT | SIMULATION | Define a measurable distribution criterion and verify it across critical treatment stages. |
| Recirculation | UNKNOWN — REQUIRES REQUIREMENT | SIMULATION | Identify where recirculation is acceptable or harmful and assess it in later modelling and tests. |
| Residence time | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Define only for treatment stages whose performance depends on contact time. |

Mass-flow consistency between intake and discharge must eventually be checked under steady operation, allowing for leakage and any deliberate side streams. Intake and exhaust separation must be evaluated to avoid immediate re-entrainment of treated air where that would reduce useful performance.

### 3.2 Particle Removal

| Target pollutant | Desired removal performance | Required evidence | Requirement status |
| --- | --- | --- | --- |
| PM2.5 | UNKNOWN — REQUIRES REQUIREMENT | Pollutant-specific upstream/downstream measurements under documented flow, loading, humidity, and test conditions | UNKNOWN |
| PM10 | UNKNOWN — REQUIRES REQUIREMENT | Pollutant-specific upstream/downstream measurements under documented flow, loading, humidity, and test conditions | UNKNOWN |
| Larger dust particles | UNKNOWN — REQUIRES REQUIREMENT | Defined particle-size range and repeatable capture or mass-removal measurements under documented conditions | UNKNOWN |

The primary particulate target has not been selected. Removal efficiency, clean-air delivery, loading capacity, and performance over time will require separate definitions and evidence.

### 3.3 Gas-Phase Pollutants

Possible pollutants for later consideration include VOCs, NOx, SOx, CO, and ozone. The exact target gases are **NOT YET DEFINED**.

**Pollutant-specific treatment performance must be established before any removal claim is made.**

| Candidate pollutant | Is treatment required? | Performance target | Evidence needed | Status |
| --- | --- | --- | --- | --- |
| VOCs | NOT YET DEFINED | UNKNOWN — REQUIRES REQUIREMENT | Compound-specific source review and controlled testing | UNKNOWN |
| NOx | NOT YET DEFINED | UNKNOWN — REQUIRES REQUIREMENT | Species-specific source review and controlled testing | UNKNOWN |
| SOx | NOT YET DEFINED | UNKNOWN — REQUIRES REQUIREMENT | Species-specific source review and controlled testing | UNKNOWN |
| CO | NOT YET DEFINED | UNKNOWN — REQUIRES REQUIREMENT | Source review establishing whether any proposed stage can affect CO, followed by suitable testing if required | UNKNOWN |
| Ozone | NOT YET DEFINED | UNKNOWN — REQUIRES REQUIREMENT | Source review and testing for both removal and unintended generation | UNKNOWN |

No proposed filter or treatment stage is assumed to remove any of these gases.

### 3.4 Filtration

| Stage | Intended Purpose | Material | Dimensions | Pressure Drop | Efficiency | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Prefilter | Unknown | Unknown | Unknown | Unknown | Unknown | TBD |
| Water stage | Dust separation concept | Unknown | Unknown | Unknown | Unknown | Experimental |
| Biochar stage | Adsorption concept | Unknown | Unknown | Unknown | Unknown | TBD |
| HEPA | Particle filtration | Unknown | Unknown | Unknown | Unknown | TBD |

Manufacturer specifications, standards, test conditions, media loading, sealing, bypass leakage, lifetime, service method, and compatibility between stages are all **SOURCE REQUIRED** or **UNKNOWN**. The biochar stage is not a proven solution; its material, target pollutant, mechanism, media geometry, pressure drop, capacity, and effectiveness require evidence.

### 3.5 Fans

Current conceptual arrangement: **2 intake fans + 2 exhaust fans — CONCEPT — NOT VALIDATED**.

Four fans are not a final requirement and must not be treated as optimal without system-level evidence.

| Parameter | Current information | Status | Evidence needed |
| --- | --- | --- | --- |
| Number of fans | Four considered: 2 intake + 2 exhaust | ASSUMPTION | Required airflow, system pressure drop, fan/system operating point, simulation, and physical test |
| Fan arrangement | Intake and exhaust positions not defined | UNKNOWN | Architecture study, recirculation assessment, serviceability, and safety review |
| Fan diameter | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Airflow, pressure, noise, and packaging requirements |
| Rated voltage | UNKNOWN — REQUIRES REQUIREMENT | SOURCE REQUIRED | Selected electrical architecture and manufacturer datasheet |
| Rated power | UNKNOWN — REQUIRES REQUIREMENT | SOURCE REQUIRED | Manufacturer datasheet and measured operating point |
| Maximum airflow | UNKNOWN — REQUIRES REQUIREMENT | SOURCE REQUIRED | Manufacturer fan curve at stated test conditions |
| Static pressure | UNKNOWN — REQUIRES REQUIREMENT | SOURCE REQUIRED | Manufacturer fan curve and later system resistance estimate |
| Fan curve | UNKNOWN — REQUIRES REQUIREMENT | SOURCE REQUIRED | Manufacturer data or controlled characterization |
| Noise | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Application-specific limit and measured sound level under stated conditions |
| Operating control | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Decide fixed, staged, or variable control after the duty range is known |

### 3.6 Physical Size

| Parameter | Value | Status | Basis required |
| --- | --- | --- | --- |
| Maximum height | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Application, transport, stability, airflow path, and service access |
| Maximum width | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Application, footprint, component packaging, and service access |
| Maximum depth | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Application, footprint, component packaging, and service access |
| Footprint | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Placement and clearance requirements |
| Weight | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Portability, structure, materials, water inventory, and components |
| Portability | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Intended deployment and handling method |
| Installation requirements | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Indoor, semi-enclosed, or outdoor application decision |

### 3.7 Power

**SOLAR-ASSISTED** means solar generation supplies only some of the required energy or operating power. **SOLAR-SUSTAINABLE** would require a demonstrated energy balance showing that solar generation and any storage can support the defined duty cycle under stated conditions. The current concept is solar-assisted; solar sufficiency is not assumed.

| Parameter | Value | Status | What must be specified or measured |
| --- | --- | --- | --- |
| Operating voltage | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Electrical architecture and load compatibility |
| Maximum electrical power | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Worst-case combined load at a defined operating condition |
| Average electrical power | UNKNOWN — REQUIRES REQUIREMENT | EXPERIMENTAL | Measured duty-cycle average after component selection |
| Fan power | UNKNOWN — REQUIRES REQUIREMENT | SOURCE REQUIRED | Selected fan data and physical measurement |
| Pump power | UNKNOWN — REQUIRES REQUIREMENT | SOURCE REQUIRED | Water-stage requirement and selected pump data |
| Sensor/controller power | UNKNOWN — REQUIRES REQUIREMENT | SOURCE REQUIRED | Selected sensing and control architecture |
| Battery requirement | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Decide whether storage is required, then define autonomy and allowable depth of discharge |
| Solar generation | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Required contribution, site conditions, panel rating, orientation, and losses |
| Expected daily operation | UNKNOWN — REQUIRES REQUIREMENT | UNKNOWN | Application and operating schedule |

Potential electrical loads are fans, a water pump, sensors, controller, communications equipment, and other supporting electronics. This list is preliminary and does not establish final power demand.

### 3.8 Water System

The proposed water stage is an **EXPERIMENTAL** concept involving water spray, dust separation, and possible particle capture. Its purpose and benefit relative to its pressure, energy, humidity, hygiene, and maintenance costs have not been established.

| Parameter | Value | Status | Validation need |
| --- | --- | --- | --- |
| Water consumption | TBD | UNKNOWN | Define operating mode and measure loss, collection, and reuse |
| Pump power | TBD | UNKNOWN | Define pressure and flow duty, source data, and measurement |
| Flow rate | TBD | UNKNOWN | Establish from a pollutant-specific capture mechanism and test plan |
| Nozzle type | TBD | UNKNOWN | Compare droplet production, clogging, pressure, and capture needs |
| Droplet size | TBD | SOURCE REQUIRED | Obtain characterized distribution and verify under operating conditions |
| Drainage | TBD | UNKNOWN | Define collection, overflow, leakage containment, and safe discharge |
| Treatment/reuse | TBD | UNKNOWN | Determine water-quality, contamination, and disposal requirements |
| Humidity effects | TBD | EXPERIMENTAL | Measure outlet humidity and effects on downstream media and sensors |
| Maintenance | TBD | EXPERIMENTAL | Establish from fouling, microbial, scaling, cleaning, and inspection evidence |

The future design must also investigate demisting and uncontrolled water carryover before the subsystem can be accepted.

### 3.9 Sensors

Sensor planning is **PRELIMINARY — NOT FINAL**. No commercial sensor has been selected.

| Potential measurement | Intended purpose | Status |
| --- | --- | --- |
| PM2.5 | Measure inlet, outlet, and/or ambient particle concentration for performance assessment | PROPOSED |
| PM10 | Measure inlet, outlet, and/or ambient coarse-particle concentration | PROPOSED |
| Temperature | Document test and operating conditions and support sensor compensation | PROPOSED |
| Humidity | Document test conditions and detect water-stage or condensation effects | PROPOSED |
| Pressure differential | Measure restriction across individual stages or the full treatment path | PROPOSED |
| Airflow | Establish delivered flow and support CADR or system performance calculations | PROPOSED |
| Power | Measure voltage, current, power, and energy consumption | PROPOSED |
| Water flow | Measure water-stage operating condition and consumption | PROPOSED |
| Solar/battery state | Quantify solar contribution, charging, storage, and available energy | PROPOSED |

Measurement range, accuracy, resolution, response time, calibration, placement, logging interval, environmental rating, and validation method are **SOURCE REQUIRED** for every selected sensor.

## 4. Engineering Constraints

No numerical constraint limits have been approved.

| Likely constraint | Requirement that must be defined | Status |
| --- | --- | --- |
| Budget | Total project, prototype, consumable, and operating-cost limits | UNKNOWN |
| Portability | Whether movement is required and acceptable handling method | UNKNOWN |
| Manufacturing complexity | Available student skills, tools, processes, and allowable fabrication difficulty | UNKNOWN |
| Material availability in India | Locally obtainable materials, components, lead times, substitutes, and documentation | SOURCE REQUIRED |
| Maintenance | Permitted skill level, access time, frequency, tools, and consumables | UNKNOWN |
| Filter replacement | Safe access, sealing, handling, sourcing, and disposal requirements | UNKNOWN |
| Water availability | Source, quality, permitted consumption, reuse, and drainage | UNKNOWN |
| Electrical safety | Voltage class, isolation, grounding, overcurrent protection, ingress protection, and applicable standards | SOURCE REQUIRED |
| Noise | Application-specific sound limit and measurement condition | UNKNOWN |
| Weather exposure | Rain, dust, sunlight, wind, temperature, humidity, and corrosion exposure if outdoor use is selected | UNKNOWN |
| Size | Placement, clearance, transport, and access envelope | UNKNOWN |
| Weight | Stability, floor loading, lifting, and movement limits | UNKNOWN |
| Serviceability | Safe access to filters, water components, fans, sensors, and electrical parts | UNKNOWN |

## 5. Success Metrics

These metrics describe how future designs can be compared. Their target values remain **UNKNOWN — REQUIRES REQUIREMENT**.

| Metric | Unit | What it tells us | Target status |
| --- | --- | --- | --- |
| Airflow | m³/h or another documented volumetric-flow unit | Amount of air delivered at the actual system operating point | UNKNOWN |
| Pressure drop | Pa | Resistance created by the full flow path and individual stages | UNKNOWN |
| Particle removal | Pollutant-specific efficiency, commonly expressed as % | Fraction of a defined particle challenge removed under stated test conditions | UNKNOWN |
| Clean Air Delivery Rate | m³/h where applicable | Effective clean-air delivery, combining airflow with pollutant removal performance | UNKNOWN |
| Power | W | Instantaneous electrical demand at a stated operating condition | UNKNOWN |
| Energy | Wh/day | Electrical energy used over the defined daily duty cycle | UNKNOWN |
| Water | L/h or L/day | Water demand, loss, and replenishment burden | UNKNOWN |
| Noise | dB with measurement method stated | Sound produced at a defined distance, operating condition, and environment | UNKNOWN |
| Reliability | Operating time and/or maintenance interval | Repeatability, uptime, failure behavior, and service burden | UNKNOWN |

Success will require documented test conditions, calibrated or verified measurements, repeatable trials, traceable calculations, and comparison against approved targets rather than isolated readings.

## 6. Open Engineering Questions

1. Is the primary application indoor, semi-enclosed, or localized outdoor treatment?
2. What air volume or local region must the system treat?
3. What operating airflow and CADR are required for that application?
4. Which pollutant is the primary performance target, and is PM2.5 the priority?
5. Are PM10 and larger-dust removal separate requirements?
6. Is treatment of any gas-phase pollutant actually required; if so, which compounds and concentrations?
7. What is the required operating schedule and duty cycle?
8. What maximum full-system and per-stage pressure drops are acceptable?
9. What level of flow uniformity is required through each treatment stage?
10. How will intake/exhaust separation, leakage, recirculation, and internal dead zones be assessed?
11. Is a prefilter required, and what particle-loading duty should it handle?
12. What HEPA grade, test standard, rated flow, size, sealing method, and replacement condition are required?
13. Is biochar intended for gas adsorption, particle filtration, or another function?
14. Which biochar or biomass-derived material has evidence for the selected pollutant and operating conditions?
15. What exact benefit must the experimental water stage provide?
16. Can the water stage demonstrate useful capture without unacceptable carryover, humidity, fouling, biological growth, energy use, or maintenance?
17. How much static pressure must the fan system provide at the required airflow?
18. Is the four-fan concept beneficial compared with fewer, larger, or differently arranged fans?
19. What fan control range and noise limit are required?
20. What height, footprint, weight, stability, portability, installation, and service-access limits apply?
21. What is the maximum acceptable power and daily energy consumption?
22. What portion of energy should solar supply, under what site and weather conditions?
23. Is a battery required; if so, what autonomy, chemistry constraints, and safety provisions apply?
24. Which measurements are required for control, safety, performance validation, and long-term monitoring?
25. What budget, local sourcing, maintenance, consumable, and disposal constraints apply in India?
26. Which electrical, particulate, environmental, and test standards apply?
27. How will pollutant reduction, airflow, pressure drop, energy, water use, noise, leakage, and reliability be physically validated?

