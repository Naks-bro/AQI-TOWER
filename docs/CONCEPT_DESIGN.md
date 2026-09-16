# AQI Tower — Concept Design

## Phase 3 Scope

This document explores substantially different physical and airflow architectures before detailed CAD or CFD begins. It does not select final dimensions, fans, filters, materials, treatment order, or performance values.

### Engineering Traceability Labels

- **FACT** — known from the approved project requirements or a recorded source.
- **ENGINEERING JUDGMENT** — a reasoned conceptual recommendation that has not been validated.
- **UNKNOWN** — requires a requirement decision, source, simulation, or physical test.
- **ASSUMPTION** — a temporary modelling input that must be recorded and validated before use.

Unless a statement is explicitly labelled **FACT**, no architecture or feature in this document is a confirmed design requirement.

## Known Starting Conditions

- **FACT:** The intended product is a tower-type system that moves ambient air through treatment stages and discharges treated air.
- **FACT:** The application environment is not finalized; indoor, semi-enclosed, and localized outdoor use remain possibilities.
- **FACT:** No airflow, CADR, pressure-drop, particle-removal, size, power, water, noise, or reliability target has been approved.
- **FACT:** HEPA, biochar or biomass-derived media, and a water stage are candidate concepts, not a validated treatment train.
- **ASSUMPTION:** The current team concept starts from a vertical package.
- **ASSUMPTION:** Two intake plus two exhaust fans is only an initial idea and is not treated as optimal.
- **UNKNOWN:** Which architecture best serves the eventual application and pollutant target.

## Concept A — Vertical Cross-Flow

### Name

Vertical Cross-Flow with Separate Clean-Air Riser

### Basic Idea

**ENGINEERING JUDGMENT:** Use a predominantly straight, horizontal flow path through flat, replaceable treatment cassettes. After treatment, collect the air in an isolated clean-side plenum or vertical riser and discharge it away from the intake.

### Conceptual Diagram

```text
DIRTY AIR
    |
    v
+----------+   +-------------+   +----------------+   +--------------+
|  INLET   |-->| DIRTY-AIR   |-->| INTERCHANGEABLE|-->| CLEAN-AIR    |
|  REGION  |   | PLENUM      |   | STAGE REGIONS  |   | RISER/PLENUM |
+----------+   +-------------+   +----------------+   +------+-------+
                                                               |
                                                        [FAN REGION?]
                                                               |
                                                               v
                                                        CLEAN EXHAUST
```

The stage regions are placeholders. Their order and even their inclusion remain **UNKNOWN**.

### Airflow Path

1. Ambient air enters a side or lower-side inlet.
2. A dirty-air plenum spreads the flow over the available treatment face.
3. Air crosses one or more flat, removable treatment regions.
4. A clean-side collection plenum receives the treated stream.
5. The flow turns into an isolated riser or discharge passage.
6. Air exits through a top, rear, or otherwise separated exhaust.

### Fan Location

**ENGINEERING JUDGMENT:** A clean-side extraction fan region is a useful first arrangement because it creates one main flow path and keeps the fan downstream of major particle filtration. Push-only or push-pull placements remain alternatives. Fan count and fan type are **UNKNOWN**.

### Intake Location

**ENGINEERING JUDGMENT:** A broad side or lower-side intake could expose a large flat filter area and simplify the dirty plenum. Required height, face area, guards, and weather protection are **UNKNOWN**.

### Exhaust Location

**ENGINEERING JUDGMENT:** A top or high rear exhaust separated from the inlet may reduce immediate short-circuiting. The safe separation and direction depend on the final application and must be tested.

### Filter Location

Flat cassettes could sit between the dirty and clean plenums. A prefilter, HEPA region, and adsorption region can be represented as independent removable placeholders; no sequence is selected.

### Water Stage

**UNKNOWN:** If retained, a water subsystem could occupy a separate upstream cassette or lower chamber with drainage, droplet containment, and demisting. It must not expose a dry filter or electrical region to uncontrolled moisture. A dry configuration that omits the water stage must remain possible.

### Expected Advantages

- **ENGINEERING JUDGMENT:** Simple, visible airflow path.
- **ENGINEERING JUDGMENT:** Flat filter panels may be easier to source, seal, replace, and represent in CAD.
- **ENGINEERING JUDGMENT:** Separate dirty and clean plenums support pressure measurements and staged testing.
- **ENGINEERING JUDGMENT:** Rectangular volumes should be straightforward for a first CFD model.
- **ENGINEERING JUDGMENT:** Service doors can potentially access each stage from one face.

### Potential Problems

- **UNKNOWN:** Flow may concentrate near the fan or turn, leaving parts of a filter underused.
- **UNKNOWN:** The clean-air riser and outlet turn may add pressure loss.
- **UNKNOWN:** Poor seals could allow bypass around flat cassettes.
- **UNKNOWN:** A side intake may be vulnerable to rain, impact, or obstruction in some applications.
- **UNKNOWN:** A wet stage could make the otherwise simple linear arrangement difficult to drain and isolate.

### Maintenance and Manufacturing

**ENGINEERING JUDGMENT:** Folded sheet panels or a simple frame with removable flat cassettes could make this the least complex architecture to fabricate. Clear acrylic or polycarbonate may be useful only for non-structural prototype viewing panels. A wet compartment, if used, should be a separately removable corrosion- and water-compatible module. Filter replacement, fan access, sensor taps, drains, and an isolated electrical access panel must be reachable without dismantling the whole tower.

### What CFD Must Determine

- How uniform is velocity across each treatment face?
- Does the inlet plenum need a diffuser, straightener, or baffle?
- Where do separation, recirculation, and dead zones form?
- How much loss comes from the inlet, each placeholder stage, the riser turn, and the outlet?
- Does extraction, intake, or push-pull fan placement improve the usable operating point?
- Is dirty-air or clean-air bypass likely at cassette edges?
- Is inlet-to-exhaust short-circuiting likely in the external flow field?

## Concept B — Central Core

### Name

Annular Intake with Central Clean-Air Core

### Basic Idea

**ENGINEERING JUDGMENT:** Admit air around much of the tower perimeter and draw it radially inward through concentric or segmented treatment media into a central clean-air core. Move the collected clean air vertically to an exhaust.

### Conceptual Diagram

```text
TOP VIEW

          AMBIENT AIR FROM MULTIPLE SIDES
              v       v       v
        +---------------------------+
        |  OUTER INTAKE / PLENUM    |
        |   +-------------------+   |
    --> |   | TREATMENT RING(S) |   | <--
        |   |     +-------+     |   |
    --> |   | --> | CLEAN | <-- |   | <--
        |   |     | CORE  |     |   |
        |   +-----+---+---+-----+   |
        +-------------|-------------+
                      |
                      v
              CENTRAL FAN REGION?
                      |
                      v
                 CLEAN EXHAUST
```

### Airflow Path

1. Ambient air enters around an outer perforated or segmented intake region.
2. An annular dirty-air space distributes flow around the perimeter.
3. Air moves radially inward through concentric or faceted treatment regions.
4. Treated air enters a central vertical clean-air core.
5. One or more fan regions move air along the core.
6. Air leaves through a separated upper exhaust.

### Fan Location

**ENGINEERING JUDGMENT:** A central clean-side extraction fan or stacked fan regions could create a compact pressure source. Distributed perimeter fans remain possible but would add wiring and balance questions. The arrangement is **UNKNOWN**.

### Intake Location

Intakes could cover a full circumference or selected perimeter sectors. **UNKNOWN:** A full circumference may not be suitable near walls, pedestrians, rain, or service panels.

### Exhaust Location

A vertical top exhaust aligns naturally with the central core. A side discharge would require another turn and separation from active intake sectors.

### Filter Location

Treatment media could form concentric cylinders, polygonal rings, or removable perimeter segments around the core. A prefilter could occupy the outermost accessible region; HEPA and adsorption media could occupy separate inner or outer dry segments, with their order left open. Curved HEPA or adsorption elements must not be assumed available; faceted standard cassettes may be more practical.

### Water Stage

**ENGINEERING JUDGMENT:** A wet annular stage would require a continuous or segmented collection basin below it, strong droplet containment, and a demister before any moisture-sensitive stage. Uniform spraying around a circumference is an important **UNKNOWN**. Omitting the water stage must remain an option.

### Expected Advantages

- **ENGINEERING JUDGMENT:** Large perimeter intake area may allow broad use of the tower surface.
- **ENGINEERING JUDGMENT:** Radial collection may create a compact central discharge path.
- **ENGINEERING JUDGMENT:** A central pressure source could reduce the number of separate fan stations.
- **ENGINEERING JUDGMENT:** Circumferential modularity may support adding or disabling intake sectors.

### Potential Problems

- **UNKNOWN:** Nonuniform resistance, blocked sectors, or nearby walls may cause strong circumferential imbalance.
- **UNKNOWN:** Sealing concentric or segmented media may be difficult.
- **UNKNOWN:** The inner core and rear sides of media may be hard to access.
- **UNKNOWN:** Curved parts, rings, and circular drains increase fabrication complexity.
- **UNKNOWN:** Central fan access may require removal of other components.
- **UNKNOWN:** A radial wet stage may create difficult drainage and demisting problems.

### Maintenance and Manufacturing

**ENGINEERING JUDGMENT:** A faceted polygon made from flat sheet-metal or polymer panels is more manufacturable than a fully curved shell, but the segmented seals and central-core support remain more complex than Concept A. Service doors must reach every perimeter segment, the core fan, sensors, drains, and electrical areas. Media cannot be treated as replaceable if inner segments cannot be removed safely.

### What CFD Must Determine

- How evenly does air enter around the perimeter under different surrounding obstructions?
- Does the central core draw excessively from the nearest or least-resistant sectors?
- What core size is needed to prevent high velocity and excess loss?
- Where do circumferential recirculation and axial imbalance occur?
- Can segmented media receive acceptably uniform face velocity?
- How do central versus distributed fans change flow balance?
- Does the external exhaust re-enter nearby intake sectors?

## Concept C — Dual-Sided Intake / Central Exhaust

### Name

Mirrored Treatment Banks with Central Clean-Air Chimney

### Basic Idea

**ENGINEERING JUDGMENT:** Use two independent, mirrored intake and treatment banks on opposite sides of the tower. Each bank sends treated air into a shared central clean-air chimney that exhausts upward or rearward.

### Conceptual Diagram

```text
LEFT AMBIENT AIR                                      RIGHT AMBIENT AIR
        |                                                      |
        v                                                      v
+---------------+                                      +---------------+
| LEFT INTAKE   |                                      | RIGHT INTAKE  |
+-------+-------+                                      +-------+-------+
        |                                                      |
+-------v-------+       +----------------------+       +-------v-------+
| LEFT STAGE    |------>| CENTRAL CLEAN-AIR    |<------| RIGHT STAGE   |
| BANK          |       | CHIMNEY / PLENUM     |       | BANK          |
+---------------+       +----------+-----------+       +---------------+
                                  |
                           [FAN REGION?]
                                  |
                                  v
                            CLEAN EXHAUST
```

### Airflow Path

1. Ambient air enters two separated side intake regions.
2. Each side plenum distributes air across its own treatment bank.
3. The two streams pass independently through their treatment regions.
4. Treated streams merge only inside a central clean-air chimney or collection plenum.
5. A central or upper fan region moves the combined flow.
6. Air exits through a top or high rear exhaust separated from both intakes.

### Fan Location

Possible placements include one central extraction fan region, one fan per clean-side bank, distributed intake fans, or a controlled push-pull arrangement. **ENGINEERING JUDGMENT:** A single conceptual extraction region is the simplest comparison case; final count remains **UNKNOWN**.

### Intake Location

Opposing side intakes provide two clear dirty-air faces. The active faces, elevation, obstruction clearance, and weather protection depend on the application.

### Exhaust Location

A top exhaust can be centered on the shared chimney. A high rear exhaust is possible if it remains separated from both intake faces.

### Filter Location

Each side contains a replaceable treatment bank. A prefilter could sit nearest each intake, while HEPA and adsorption media occupy separate downstream or reorderable dry slots. The banks could use identical modules or intentionally different experimental modules, but any unequal resistance could unbalance the flow.

### Water Stage

**ENGINEERING JUDGMENT:** A water module could be tested in one or both banks upstream of a demister, allowing comparison with a dry bank only if cross-leakage and boundary conditions are controlled. Separate drains would be required. This is an experimental possibility, not a recommended treatment sequence.

### Expected Advantages

- **ENGINEERING JUDGMENT:** Two parallel banks can offer large treatment face area within a narrow tower.
- **ENGINEERING JUDGMENT:** Flat, mirrored modules may simplify fabrication and replacement.
- **ENGINEERING JUDGMENT:** Separate banks support controlled comparison or staged capacity.
- **ENGINEERING JUDGMENT:** Centralized clean-air sensing and exhaust may simplify monitoring.
- **ENGINEERING JUDGMENT:** The architecture can potentially scale by changing bank area or module count.

### Potential Problems

- **UNKNOWN:** One bank may dominate if resistances, seals, or surroundings differ.
- **UNKNOWN:** Flow can short-circuit near the shared chimney entrance.
- **UNKNOWN:** A central fan may produce poor vertical or left-right distribution.
- **UNKNOWN:** Twice as many doors, seals, drains, or sensor points may be needed.
- **UNKNOWN:** Opposing intakes may be unusable when installed close to a wall.
- **UNKNOWN:** Wet/dry bank comparisons may be misleading if flow is not balanced.

### Maintenance and Manufacturing

**ENGINEERING JUDGMENT:** Repeated flat cassettes, modular filter frames, and folded sheet or framed polymer panels could simplify manufacture. Each bank should open independently without exposing the clean chimney to dirty service air. Fan, sensor, drain, and electrical access should not require removal of both banks. Mirrored parts reduce variety but duplicate seals and service doors.

### What CFD Must Determine

- How evenly is total flow divided between the two banks?
- How sensitive is balance to unequal filter loading or external blockage?
- Does the central chimney create high-velocity jets or merge losses?
- Where should the fan region sit for stable flow through both banks?
- What plenum features are needed for uniform face velocity?
- Do the inlet and exhaust locations cause external recirculation?
- Can one-bank and two-bank operation be represented safely and predictably?

## Concept D — Radial / Multi-Plenum

### Name

Branched Multi-Plenum with Parallel Treatment Modules

### Basic Idea

**ENGINEERING JUDGMENT:** Use a common dirty-air distribution plenum that divides flow among several separated treatment branches arranged around or along the tower. A clean-air collection plenum recombines the branch flows before exhaust.

### Conceptual Diagram

```text
                         +--> [BRANCH 1: STAGE MODULES] --+
AMBIENT --> [INLET] -->  +--> [BRANCH 2: STAGE MODULES] --+--> [CLEAN
          [DIRTY PLENUM] +--> [BRANCH 3: STAGE MODULES] --+     PLENUM]
                         +--> [BRANCH 4: STAGE MODULES] --+        |
                                                                  v
                                                           [FAN REGION?]
                                                                  |
                                                                  v
                                                            CLEAN EXHAUST
```

The branch count is illustrative and is not an assumed fan or module count.

### Airflow Path

1. Ambient air enters one or more guarded inlet regions.
2. A primary dirty-air plenum distributes the stream to multiple branches.
3. Each branch passes through its own treatment module or sequence.
4. Branch flows enter a separate clean-air collection plenum.
5. One central or several coordinated fan regions maintain the flow.
6. The combined treated stream exits through a separated exhaust.

### Fan Location

Possible arrangements include one extraction fan after the clean plenum, one controlled fan per branch, or several fans distributed along the collection plenum. The balance, control, failure behavior, and electrical complexity are **UNKNOWN**.

### Intake Location

A common low, side, or circumferential inlet could feed the dirty plenum. Multiple inlets are possible if their paths remain separated from the clean exhaust and can be balanced.

### Exhaust Location

A single top or high-side exhaust could serve the clean plenum. Distributed exhausts are possible but increase recirculation and control questions.

### Filter Location

Each branch can hold removable flat treatment cassettes. A prefilter could sit at a branch entrance; HEPA and adsorption media could be placed in separate reorderable dry slots or assigned to different experimental branches. Branches might contain identical stages for capacity or different experimental stages for comparison, but unequal resistance must be measured and controlled.

### Water Stage

**ENGINEERING JUDGMENT:** A dedicated wet branch could isolate drainage, demisting, and cleaning from dry branches. However, its results would be useful only if its airflow and inlet challenge are measured independently. Integrating wet treatment into every branch would multiply drains, nozzles, pumps, and failure points.

### Expected Advantages

- **ENGINEERING JUDGMENT:** Parallel modules may support staged experiments, maintenance, or future scaling.
- **ENGINEERING JUDGMENT:** Branch-level pressure and sensing could reveal individual module behavior.
- **ENGINEERING JUDGMENT:** A wet subsystem can potentially be isolated from dry stages.
- **ENGINEERING JUDGMENT:** Flow-control elements could tune distribution if unequal branches are unavoidable.

### Potential Problems

- **UNKNOWN:** Air will favor the lowest-resistance branch unless the network is balanced.
- **UNKNOWN:** Many junctions, bends, seals, and transitions may create substantial loss.
- **UNKNOWN:** Distributed fans may interact or drive reverse flow through an inactive branch.
- **UNKNOWN:** Controls, wiring, sensing, and failure modes become more complex.
- **UNKNOWN:** Fabrication and leak testing may be difficult for a student prototype.
- **UNKNOWN:** Results from different treatment branches may not be comparable without controlled flow division.

### Maintenance and Manufacturing

**ENGINEERING JUDGMENT:** Rectangular branch modules can use sheet metal, aluminium framing, or compatible polymer panels, but the central distribution and collection manifolds require careful fabrication. Every branch needs access, sealing, isolation, and possibly its own drain or sensor ports. A concept that cannot provide safe access to the rear branches should be rejected even if its predicted flow is attractive.

### What CFD Must Determine

- How does flow divide among branches with equal and unequal resistance?
- What plenum size and shape reduce branch-to-branch imbalance?
- Are diffusers, baffles, or flow resistors required, and what penalty do they create?
- Can inactive or loaded branches produce reverse flow or bypass?
- Where do junction losses, separation, and stagnant volumes occur?
- Do central and distributed fan arrangements behave stably across expected operating states?
- Can a wet branch be aerodynamically isolated without invalidating comparisons?

## Fan Arrangement Analysis

All entries below are **ENGINEERING JUDGMENT** and require fan curves, a system resistance model, later CFD, and physical measurements. No arrangement is selected.

| Arrangement | Potential advantages | Potential disadvantages | Critical unknowns |
| --- | --- | --- | --- |
| 2 intake + 2 exhaust | Push-pull pressure capability may be shared; some redundancy may be possible | Fan interaction, imbalance, extra power/noise/wiring, and pressure-driven leakage may occur | Whether operating points remain stable and whether four fans add useful flow |
| All fans as extraction | One downstream pressure direction; dirty leakage through casing may tend inward; clean-side fan station can be centralized | Fans see treated air but the enclosure operates below ambient pressure; bypass air can enter through leaks | Required suction pressure, casing leakage, fan protection, and clean-side flow uniformity |
| All fans as intake | Fans can be placed at accessible inlets and may positively pressurize treatment stages | Untreated air may escape through dirty-side leaks; downstream distribution and casing pressure become important | Leak paths, fan exposure to dust/water, and uniformity at stage faces |
| Fewer larger fans | Fewer controls, openings, seals, and possible fan interactions | Reduced redundancy, larger service opening, concentrated suction/discharge, and single-point failure | Availability of a suitable fan curve, noise, controllability, and plenum needs |
| Multiple smaller fans | Modular packaging, possible redundancy, and potential distribution across a wide face | More wiring, guards, controls, interaction, noise sources, and failure cases | Matching, control method, backflow through stopped fans, and combined fan curve |
| Distributed fan arrangement | Local flow control may help large or branched filter areas | High electrical and control complexity; unequal operating points and maintenance burden | Sensor/control strategy, stability, fault behavior, and total efficiency |
| Central fan arrangement | Simple electrical architecture and one main operating point; compatible with a clean core or plenum | Concentrated flow can cause nonuniformity; central access and single-point failure may be difficult | Required plenum geometry, service access, noise path, and flow distribution |

## Filtration Architecture

The sequences below are conceptual configurations only. Their inclusion and order are **UNKNOWN** until the target pollutant, component data, moisture limits, and validation plan are established. More stages do not automatically mean better performance.

### Sequence 1 — Prefilter -> HEPA -> Biochar

- **Likely purpose — ENGINEERING JUDGMENT:** Remove larger particles first, use HEPA for defined particulate filtration, then expose relatively particle-clean air to adsorption media if a gas target justifies it.
- **Pressure-drop implication — UNKNOWN:** All three dry stages add resistance; actual values require rated component data at the intended flow and loading.
- **Contamination/loading:** The prefilter may reduce HEPA loading. HEPA upstream of biochar may reduce particle fouling of adsorption media, while biochar shedding would occur downstream unless contained.
- **Moisture:** No water stage is present, but ambient humidity limits remain source-dependent.
- **Maintenance:** Separate access is needed so the prefilter can be cleaned or changed without disturbing HEPA seals or adsorption media.
- **Validation required:** Particle removal, gas-specific adsorption if required, media shedding, sealing, loading behavior, combined pressure drop, and replacement criteria.

### Sequence 2 — Prefilter -> Water Stage -> HEPA -> Biochar

- **Likely purpose — ENGINEERING JUDGMENT:** Test whether wet contact removes a defined dust fraction before dry fine-particle and adsorption stages.
- **Pressure-drop implication — UNKNOWN:** The spray chamber, turns, droplet separator if added, and dry filters all add resistance.
- **Contamination/loading:** Captured material moves into water, drains, nozzles, and tank surfaces. Any carryover can contaminate downstream stages.
- **Moisture:** This sequence places HEPA immediately downstream of a wet concept; a demisting need and allowable humidity must be established before it can be considered credible.
- **Maintenance:** Requires water cleaning, nozzle access, drainage, leakage inspection, and dry-stage protection in addition to filter replacement.
- **Validation required:** Pollutant-specific wet capture, droplet distribution, water carryover, outlet humidity, microbial/scaling risk, water consumption, combined pressure drop, and performance against a dry control.

### Sequence 3 — Prefilter -> Biochar -> HEPA

- **Likely purpose — ENGINEERING JUDGMENT:** Place adsorption media before the final particle filter so any media dust can potentially be captured by HEPA.
- **Pressure-drop implication — UNKNOWN:** Media packing and containment geometry may dominate resistance and require sourced or measured data.
- **Contamination/loading:** Biochar may receive more residual particulate loading than in Sequence 1; HEPA may capture media fines but could load from them.
- **Moisture:** Ambient moisture may alter adsorption performance; no protection is assumed.
- **Maintenance:** Biochar access must avoid contaminating the downstream clean side or damaging the HEPA seal.
- **Validation required:** Target-gas capacity, breakthrough, effect of particle loading/humidity, media shedding, HEPA loading, combined pressure drop, and safe replacement.

### Sequence 4 — Prefilter -> Experimental Water Stage -> Demister -> HEPA -> Adsorption Stage

- **Likely purpose — ENGINEERING JUDGMENT:** Treat the water system as a defined wet subsystem and add explicit droplet separation before dry fine-particle and adsorption stages.
- **Pressure-drop implication — UNKNOWN:** This is the most component-rich listed sequence and may create several losses; no magnitude is claimed.
- **Contamination/loading:** Wet solids collect in the water circuit and demister, while remaining particles load HEPA. The adsorption stage receives relatively particle-filtered air.
- **Moisture:** A demister reduces neither humidity nor carryover to zero by assumption; both require measurement, and adsorption media limits require sources.
- **Maintenance:** Adds demister cleaning, tank/drain service, nozzle cleaning, water treatment/disposal, and wet/dry isolation.
- **Validation required:** Each wet component, demister effectiveness, humidity/carryover, particle and any gas performance, combined pressure drop, water/energy burden, hygiene, and comparison with simpler dry sequences.

## Flow Management Features

These are possible tools, not guaranteed improvements.

| Feature | Why it might help | Risk or question | Classification |
| --- | --- | --- | --- |
| Dirty-air plenum | Spreads inlet flow across a larger treatment face | Poor proportions may create stagnant corners or favor nearby regions | ENGINEERING JUDGMENT / UNKNOWN |
| Clean-air plenum | Collects flow and separates filters from the outlet or fan | Contraction and collection can create jets and added loss | ENGINEERING JUDGMENT / UNKNOWN |
| Diffuser | Reduces velocity and distributes flow after a compact inlet | Separation can occur if the transition is too abrupt | ENGINEERING JUDGMENT / UNKNOWN |
| Flow straightener | Reduces swirl or large lateral velocity components | Adds resistance and can foul | ENGINEERING JUDGMENT / UNKNOWN |
| Baffles | Redirect or balance flow within a plenum | Can create local jets, dead zones, and maintenance traps | ENGINEERING JUDGMENT / UNKNOWN |
| Turning vanes | Guide flow through necessary bends | Add fabrication, fouling surfaces, and pressure loss | ENGINEERING JUDGMENT / UNKNOWN |
| Gradual transition | Avoids abrupt area changes and may reduce separation | Consumes tower volume and may conflict with service access | ENGINEERING JUDGMENT / UNKNOWN |
| Separated inlet/outlet paths | Reduces the chance that discharged air immediately re-enters the system | Required distance and orientation are application-dependent | FACT requirement / UNKNOWN geometry |

## Maintenance Design Comparison

| Activity | Concept A | Concept B | Concept C | Concept D |
| --- | --- | --- | --- | --- |
| Filter replacement | Flat cassettes potentially accessible from one face | Segmented/ring access may be difficult at inner or rear locations | Two independent flat banks; duplicated doors and seals | Branch modules can be independent but rear branches may be obstructed |
| General cleaning | Simple dirty plenum and flat surfaces | Curved annular spaces and core are harder to reach | Two plenums increase surface area but remain separable | Junctions and multiple branches create cleaning traps |
| Water drainage | One isolated lower wet module is possible | Annular basin and level drainage are complex | Separate bank drains possible; duplication risk | Dedicated wet branch possible; manifold isolation needed |
| Biochar replacement | Single flat cassette possible | Segmented media handling and sealing are complex | One cassette per bank or shared bank; balance must be preserved | Branch-specific replacement may change network balance |
| Fan servicing | End/top fan region can be independently accessed | Central fan may be obstructed by media/core | Top or rear central fan access possible | Central fan is accessible; distributed fans multiply service points |
| Sensor access | Straightforward taps before/after stages | Multiple circumferential points may be needed | Bank-specific plus common clean-side access | Good branch-level sensing but high sensor count |
| Electrical access | One isolated dry panel appears feasible | Routing around annular/wet regions is difficult | Central dry spine or rear panel appears feasible | Wiring to distributed branches is complex |

**ENGINEERING JUDGMENT:** Concept performance cannot compensate for unsafe or impractical maintenance. Any architecture that prevents safe filter, drain, fan, sensor, or electrical access should fail the concept review.

## Manufacturing Considerations

- **FACT:** Final materials and suppliers have not been selected; availability, price, grade, and lead time in India require verification.
- **ENGINEERING JUDGMENT:** Sheet metal can suit rigid frames, plenums, and service panels where corrosion protection and safe edges are addressed.
- **ENGINEERING JUDGMENT:** Aluminium can reduce mass and corrosion concerns but may increase material/joining cost; grade and fabrication capability are **UNKNOWN**.
- **ENGINEERING JUDGMENT:** Acrylic or polycarbonate can provide prototype viewing sections, but structural duty, impact resistance, UV/weather exposure, sealing, and cleaning compatibility require review.
- **ENGINEERING JUDGMENT:** HDPE or PP may suit a removable wet module, tank, drain, or duct where chemical, temperature, structural, and joining requirements permit.
- **ENGINEERING JUDGMENT:** PVC should be considered only for a justified compatible duct or water function; fire, UV, temperature, joining, and environmental requirements must be checked.
- **ENGINEERING JUDGMENT:** Modular filter frames and common flat panel sizes could reduce custom fabrication and simplify replacement.

| Concept | Manufacturability view | Main fabrication risk |
| --- | --- | --- |
| A | Mostly flat panels, straight frames, and rectangular plenums | Sealing large cassettes and integrating a clean riser without bypass |
| B | Faceted construction is possible, but concentric supports and many seals are required | Curved/segmented fit-up, core access, and annular drainage |
| C | Repeated mirrored flat modules can reduce part variety | Maintaining left/right dimensional and leakage symmetry |
| D | Branch cassettes can be modular | Accurate multi-port plenums, many joints, access, and leak testing |

## Definition of the First CAD Model

The first CAD model should represent **Concept A as the baseline modelling geometry**, not as the final product. This is an **ENGINEERING JUDGMENT** based on its simple topology and model clarity. Concept B should remain available as the substantially different comparison geometry.

### Model Purpose

Create a simple, parametric assembly or volume model that can be changed quickly, reviewed by the student team, and later converted into clearly named airflow regions for CFD. Do not model performance or detailed components.

### Major Volumes and Regions

- Overall tower envelope placeholder
- External or approach-air volume placeholder, if required by the later CFD plan
- Dirty internal airflow volume
- Clean internal airflow volume
- Structural/service envelope placeholders that show access without detailed construction

### Inlet Region

- One parameterized inlet face or opening region
- Optional guard or weather-zone envelope represented only as a simple block
- Named interface to the dirty-air distribution plenum

### Outlet Region

- One parameterized outlet face or opening region
- Separated geometrically from the inlet
- Named interface from the clean-air riser or collection plenum

### Plenum Regions

- Dirty-air distribution plenum
- Clean-side collection plenum
- Simple vertical clean-air riser or outlet transition
- Optional diffuser, baffle, or straightener regions represented as suppressible placeholders rather than detailed parts

### Filter Regions

- Independent simple slab volumes for each possible treatment stage
- Parameterized thickness, spacing, face width, and face height
- Named interfaces before and after each stage
- Ability to suppress or reorder stage placeholders without rebuilding the entire model
- No pleats, fibres, pores, granules, droplets, or manufacturer geometry

### Fan Regions

- Simple disk or short-cylinder momentum/fan-zone placeholders
- Parameterized position, diameter, and count
- Ability to compare extraction, intake, and push-pull locations
- No blades, motors, guards, or selected commercial fan geometry

### Water-Stage Placeholder

- Optional suppressible chamber volume
- Separate drain/sump envelope and demister placeholder
- Clear wet/dry boundary
- No nozzles, droplets, pump, multiphase detail, or water simulation

### Parametric Controls

Use symbolic parameters for overall height, width, depth, inlet/outlet areas, plenum depths, stage thicknesses and spacing, fan-zone size/location, and wet-stage inclusion. All numerical values remain **ASSUMPTION** until supplied by requirements or sources and must be recorded in the assumptions register before modelling.

### CAD Acceptance for Handoff to CFD

- Geometry is simple and modifiable.
- Air volumes are watertight and non-overlapping.
- Inlet, outlet, walls, stage interfaces, plenums, and fan regions are separately named.
- Small manufacturing details are suppressed.
- No dimension is presented as an approved product dimension.
- The model can support a dry baseline before any experimental water subsystem is added.

## Requirements Traceability Summary

| Concept topic | Related requirement IDs | Current classification | Future evidence |
| --- | --- | --- | --- |
| Architecture alternatives | ARCH-001, APP-001, SIZE-001 | ENGINEERING JUDGMENT | Application decision and concept review |
| Airflow paths and plenums | AIR-001 to AIR-004 | UNKNOWN / SIMULATION | Requirements, CFD, and physical airflow measurements |
| Treatment regions | PART-001 to PART-003, GAS-001, FILTER-001 to FILTER-003 | UNKNOWN / SOURCE REQUIRED | Standards, scientific evidence, datasheets, and controlled tests |
| Fan arrangements | FAN-001, FAN-002 | ASSUMPTION / SOURCE REQUIRED | Fan curves, system model, CFD, and physical measurement |
| Water integration | WATER-001, WATER-002 | EXPERIMENTAL | Controlled subsystem comparison and hygiene/moisture evidence |
| Power and solar | POWER-001, SOLAR-001, BATTERY-001 | UNKNOWN | Load measurements and site-specific energy balance |
| Sensors | SENSOR-001 | PROPOSED | Approved measurement plan and sensor source data |
| Manufacture and service | CONSTRAINT-001 | ENGINEERING JUDGMENT / UNKNOWN | Local sourcing, fabrication, maintenance, safety, and stakeholder review |
| Validation | VALID-001 | UNKNOWN | Approved test plan and repeatable physical trials |
