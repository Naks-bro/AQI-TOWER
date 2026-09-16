# AQI Tower — Concept Comparison

## Assessment Boundary

**PRELIMINARY QUALITATIVE ASSESSMENT**

The scores in this document are engineering judgments used to organize the next modelling steps. They are not measurements, simulation results, predicted performance, or proof that any concept satisfies the requirements.

Scoring scale:

- **1 — Poor:** serious conceptual difficulty for this criterion.
- **2 — Weak:** important disadvantages or complexity.
- **3 — Moderate:** plausible, with meaningful unknowns.
- **4 — Good:** favorable conceptual characteristics, still unvalidated.
- **5 — Promising:** particularly useful or clear for this criterion, still unvalidated.

For **pressure-loss risk**, a higher score means lower anticipated risk or easier management; it does not predict a pressure-drop value. No total score is calculated because the project has not assigned criterion weights.

## Concepts Compared

- **Concept A — Vertical Cross-Flow:** one mainly straight path through flat treatment regions into a separate clean-air riser.
- **Concept B — Central Core:** perimeter intake and radial inward flow through annular or segmented treatment regions into a central clean-air core.
- **Concept C — Dual-Sided Intake / Central Exhaust:** two independent mirrored treatment banks feeding a shared central clean-air chimney.
- **Concept D — Radial / Multi-Plenum:** a common distribution plenum feeding multiple parallel treatment branches that recombine in a clean plenum.

## Qualitative Comparison Matrix

All scores are **ENGINEERING JUDGMENT**.

| Criterion | A: Vertical Cross-Flow | B: Central Core | C: Dual-Sided / Central Exhaust | D: Radial / Multi-Plenum |
| --- | ---: | ---: | ---: | ---: |
| Airflow simplicity | 5 | 3 | 4 | 2 |
| Expected flow-uniformity potential | 3 | 4 | 4 | 5 |
| Pressure-loss risk | 4 | 3 | 3 | 2 |
| Filtration integration | 5 | 3 | 5 | 4 |
| Maintenance | 5 | 2 | 4 | 3 |
| Manufacturability | 5 | 2 | 4 | 2 |
| Scalability | 4 | 4 | 5 | 4 |
| Electrical simplicity | 4 | 4 | 3 | 2 |
| Water-stage integration | 3 | 2 | 4 | 4 |
| Sensor integration | 4 | 3 | 5 | 5 |
| CFD suitability | 5 | 4 | 4 | 3 |
| Stakeholder explainability | 5 | 4 | 4 | 2 |

## Score Rationale

### Concept A — Vertical Cross-Flow

- **ENGINEERING JUDGMENT:** The single dominant path, flat treatment slabs, and rectangular plenums make it easiest to explain, parameterize, mesh, manufacture, and service.
- **UNKNOWN:** A compact inlet and downstream extraction region may still create poor face-velocity uniformity.
- **UNKNOWN:** The outlet turn and clean riser may add loss or recirculation.
- **UNKNOWN:** Integrating a wet stage without compromising dry media may reduce its simplicity.

### Concept B — Central Core

- **ENGINEERING JUDGMENT:** Radial inflow offers an interesting path toward broad perimeter intake and compact central extraction.
- **UNKNOWN:** Surrounding walls or obstructions may cause sector-to-sector imbalance.
- **ENGINEERING JUDGMENT:** Annular or segmented seals, drains, media supports, and core access are harder to manufacture and maintain than flat cassettes.
- **UNKNOWN:** Curved or faceted filter availability and replacement method require sourcing evidence.

### Concept C — Dual-Sided Intake / Central Exhaust

- **ENGINEERING JUDGMENT:** Mirrored flat banks combine good filtration access and scalability with a clear shared exhaust path.
- **UNKNOWN:** Unequal surroundings, loading, or sealing may produce left-right imbalance.
- **ENGINEERING JUDGMENT:** Two independent banks make instrumentation and controlled module comparisons easier, but duplicate doors, seals, and possible drains.
- **UNKNOWN:** The merge into a central chimney may cause jets, loss, or short-circuiting.

### Concept D — Radial / Multi-Plenum

- **ENGINEERING JUDGMENT:** Branch-level control and sensing make this concept attractive for modular experiments and treatment isolation.
- **UNKNOWN:** Passive flow division may be poor whenever branch resistances differ.
- **ENGINEERING JUDGMENT:** Multiple junctions, seals, controls, fans, and access paths create the highest integration burden.
- **UNKNOWN:** Balancing devices could improve distribution but also add pressure loss and maintenance.

## Criterion-by-Criterion Interpretation

| Criterion | Current interpretation | Evidence eventually required |
| --- | --- | --- |
| Airflow simplicity | A has the fewest junctions; D has the most branched topology | Flow schematic review, CFD, and physical airflow measurement |
| Flow-uniformity potential | B, C, and D offer distributed flow faces but depend on plenum and resistance balance | Face-velocity maps from CFD and experiments |
| Pressure-loss risk | A appears to require fewer bends and junctions; D has the most potential local losses | Component pressure data, system model, CFD, and pressure measurements |
| Filtration integration | Flat cassette concepts A and C appear easiest to reconfigure | Filter sourcing, seal design, stage pressure data, and service trials |
| Maintenance | A offers the clearest single-face access; B may hide inner/core parts | Mock service review and later maintenance trials |
| Manufacturability | A and C use more repeated flat parts; B and D need more complex fit-up | India-specific sourcing and fabrication review |
| Scalability | C can expand parallel banks; B can add sectors; D can add branches; A can change face area | Size, flow, transport, and cost requirements |
| Electrical simplicity | A or B can use one central fan region; D may require distributed control | Fan architecture, load budget, and fault review |
| Water-stage integration | C or D can isolate a wet bank/branch; B makes drainage most difficult | Wet-subsystem concept test and contamination review |
| Sensor integration | C and D expose bank/branch differences clearly, but need more channels | Measurement plan, sensor placement study, and calibration plan |
| CFD suitability | A is the simplest first domain; B provides the strongest topological contrast | Geometry quality and mesh-independence planning |
| Stakeholder explainability | A has the most direct airflow story; D needs the most explanation | Student/stakeholder design review |

## Candidate Selection

These selections assign modelling roles. They do not choose a final product.

### Best Baseline Concept

**Concept A — Vertical Cross-Flow**

- **ENGINEERING JUDGMENT:** It has the simplest airflow topology, flat stage regions, straightforward service access, and the clearest path to a low-detail parametric model.
- **ENGINEERING JUDGMENT:** It provides a useful reference against which later complexity can be justified.
- **UNKNOWN:** Its actual flow uniformity, pressure loss, bypass behavior, and recirculation remain unproven.

### Best Alternative

**Concept B — Central Core**

- **ENGINEERING JUDGMENT:** It is topologically different from the linear baseline because it uses perimeter intake and radial inward collection.
- **ENGINEERING JUDGMENT:** Comparing it with Concept A can reveal whether broad radial collection offers enough benefit to justify more difficult manufacture and maintenance.
- **UNKNOWN:** Sector balance, central-core loss, sealing, access, and external recirculation require simulation and testing.

### High-Risk / High-Interest Concept

**Concept D — Radial / Multi-Plenum**

- **ENGINEERING JUDGMENT:** Parallel branches could support modular treatment experiments, branch-level sensing, and isolation of an experimental wet subsystem.
- **ENGINEERING JUDGMENT:** It also has the greatest risk of flow imbalance, junction loss, controls complexity, leakage, difficult cleaning, and fabrication burden.
- **UNKNOWN:** Whether these risks can be managed without losing the modular benefit.

### Retained Comparison Concept

**Concept C — Dual-Sided Intake / Central Exhaust** remains a credible concept for later comparison. Its mirrored modular banks may be practical, but it is closer to Concept A than the radial core is, so it is not assigned the “best alternative” role for the first topology comparison.

## Major Engineering Risks Across All Concepts

1. **UNKNOWN:** The intended application and air volume are not defined, so no architecture can be sized or judged against useful airflow.
2. **UNKNOWN:** The primary pollutant and target removal performance are not defined.
3. **UNKNOWN:** Filter resistance, loading behavior, sealing, and bypass may dominate the fan operating point.
4. **UNKNOWN:** Proposed fan counts and locations may interact or operate away from a stable, efficient point.
5. **UNKNOWN:** Plenums and transitions may create uneven treatment-face velocity, recirculation, and dead zones.
6. **EXPERIMENTAL:** The water stage may add moisture carryover, biological or scaling risk, drainage burden, energy use, and maintenance without sufficient pollutant benefit.
7. **SOURCE REQUIRED:** Biochar or biomass-derived media may not treat the selected pollutant or may have inadequate capacity, pressure behavior, or durability.
8. **UNKNOWN:** Inlet/exhaust placement may cause external short-circuiting, particularly when installed near walls or outdoors.
9. **UNKNOWN:** Access, sealing, replacement, cleaning, and safe wet/electrical separation may make a concept impractical.
10. **UNKNOWN:** Size, weight, noise, weather, budget, local sourcing, power, solar contribution, and validation constraints remain open.

## CFD Questions Shared by the Candidates

1. What airflow distribution occurs through each treatment-region face?
2. Where do internal recirculation, separation, high-velocity jets, and dead zones form?
3. How much pressure loss is associated with each plenum, transition, turn, branch, and placeholder treatment region?
4. How do extraction, intake, central, distributed, and push-pull fan-zone placements alter the system flow?
5. How sensitive is flow to unequal stage resistance representing loading, manufacturing variation, or blockage?
6. Does air bypass treatment regions through gaps or unintended paths?
7. How effectively do plenums, diffusers, straighteners, baffles, and turning vanes distribute flow, and what loss do they add?
8. Do the inlet and outlet positions encourage external recirculation or short-circuiting?
9. For Concepts B–D, how evenly does flow divide among sectors, banks, or branches?
10. Which geometric parameters most strongly affect flow uniformity and pressure loss?

CFD cannot establish filter efficiency, adsorption effectiveness, water hygiene, maintenance feasibility, or real fan performance without appropriate source data and physical validation.

## Decision Gates Before a Final Architecture

- **FACT:** No concept can become a final design during Phase 3.
- **UNKNOWN:** Application, pollutant target, airflow/CADR, duty cycle, and constraint targets must be approved.
- **SOURCE REQUIRED:** Candidate fan curves and stage pressure-drop data must be obtained before a meaningful operating point can be assessed.
- **SIMULATION:** Baseline and alternative airflow domains must be compared using the same documented boundary assumptions.
- **EXPERIMENTAL:** Critical component behavior and integrated performance must be measured before performance claims.
- **ENGINEERING JUDGMENT:** A concept should advance only if its predicted airflow advantage is compatible with manufacture, safe service, and physical validation.

## First Modelling Recommendation

**ENGINEERING JUDGMENT:** Build a simple parametric airflow-region model of Concept A first, then a simplified Concept B comparison model. Use the same unknown stage-resistance placeholders and boundary-condition framework so the comparison tests topology rather than arbitrary inputs. Do not add detailed filters, fan blades, particles, water, or final dimensions at the first CAD stage.

