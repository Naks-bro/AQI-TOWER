# AQI Tower — Assumptions Register

Working assumptions are recorded separately from confirmed requirements and validated design decisions. A-005 contains Phase 4 dimensional placeholders; A-006 records the Phase 7 simplified fan connection.

## A-001

### Statement

A vertical tower form is the initial packaging concept.

### Why It Is Needed

The project is framed as an AQI Tower, so the tower form provides a common starting point for requirements discussion.

### Risk

The form may conflict with airflow performance, stability, component access, transport, or the eventual application environment.

### How It Will Be Validated

Compare it with alternative concept arrangements in Phase 3 against approved footprint, height, stability, serviceability, airflow-path, and application requirements.

## A-002

### Statement

Four fans are initially considered: two intake fans and two exhaust fans.

### Why It Is Needed

This is the fan arrangement explicitly identified in the team's current conceptual idea.

### Risk

Four fans may be unnecessary, mismatched, inefficient, noisy, or unable to operate at the airflow and static pressure required by the treatment stages.

### How It Will Be Validated

Establish the airflow and pressure requirements, compare candidate fan arrangements using sourced fan curves and a system resistance model, then use later CFD and physical airflow measurements.

## A-003

### Statement

HEPA, biochar or biomass-derived media, and an experimental water stage are considered as candidate treatment stages.

### Why It Is Needed

These stages are explicitly part of the team's current concept and therefore need separate requirements and evidence checks.

### Risk

One or more stages may not address the selected pollutant, may create excessive pressure drop, or may introduce unacceptable energy, moisture, hygiene, cost, or maintenance burdens.

### How It Will Be Validated

Define the target pollutant first, review standards, scientific evidence, and manufacturer data, then test each justified stage independently before considering an integrated treatment train.

## A-004

### Statement

The system is expected to use electrical power with possible solar assistance.

### Why It Is Needed

Electrical and solar-assisted power are explicitly included in the current concept.

### Risk

Available solar energy may be insufficient or intermittent, and the loads, storage need, installation conditions, cost, and safety requirements are unknown.

### How It Will Be Validated

Create a measured load and duty-cycle budget after component selection, define the required solar contribution and site conditions, and compare predicted generation with physical measurements. Solar-sustainable operation must not be claimed without a demonstrated energy balance.

## A-005

### Statement

The first Concept A CAD model uses temporary numerical dimensions solely to generate and test a parametric geometry: tower 2000 mm high, 800 mm wide, and 700 mm deep; inlet 700 mm high by 600 mm wide at a 150 mm base elevation; outlet 250 mm high by 500 mm wide at a 1600 mm base elevation; dirty-air plenum depth 140 mm; treatment-region thickness 30 mm; treatment-region spacing 40 mm; clean-air plenum depth 180 mm; and inlet/outlet interface-region thickness 10 mm.

Every listed value is classified as **MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT**.

### Why It Is Needed

FreeCAD requires internally consistent numerical values to generate, display, save, reopen, and regeneration-test the first parametric model before approved product dimensions exist.

### Risk

Placeholder dimensions could be mistaken for optimized or approved design values, or could influence later work without a requirement, source, or comparison.

### How It Will Be Validated

Replace the placeholders only after application, airflow, component, service, safety, and size requirements are approved. Recompute the CAD model after every change, then assess the resulting geometry through later CFD and physical validation. Do not cite the V00 values as product specifications.

## A-006 — Phase 7 ideal terminal fan connection

### Statement

For the KVO 250 empty-tower simulation only, a loss-free adapter connects the 0.125 m² tower outlet to the fan suction; the fan discharges at zero-gauge static pressure. A uniform static suction patch is mapped to the supplied fan-static curve through its flux-weighted total pressure. No blade wake, swirl, mechanical adapter, leakage or installation effect is modelled. Reference air density remains 1.20 kg/m³.

### Why It Is Needed

It permits the real fan characteristic to drive the unchanged V00 domain without redesigning CAD or equating the 250 mm circular fan area to the rectangular tower outlet.

### Risk

Real adapter loss and inlet distortion can shift the operating point. The simplified, partially converged result cannot establish final fan suitability, purifier flow or CADR.

### How It Will Be Validated

Review the actual connection and manufacturer installation conditions, quantify losses, improve numerical validation and compare with a physical airflow/pressure test before final selection. See `docs/CFD_V01_FAN.md`.

## A-007 — Phase 8 geometry experiment dimensions

### Statement

GEO_A uses two outer turning-chamber steps at X=500–590 mm / Z=450–850 mm and X=590–690 mm / Z=650–850 mm. GEO_B moves the riser inner wall from X=320 to 260 mm. GEO_C combines both changes and ends the riser at Z=1850 mm instead of 2000 mm.

Every value is a **DESIGN EXPERIMENT PARAMETER — NOT PRODUCT REQUIREMENT**.

### Why It Is Needed

These controlled alternatives test the V01 field diagnosis: restricted riser entry, abrupt turn/expansion, and blind cap above the side outlet.

### Risk

The steps can create cleaning ledges, the enlarged riser can conflict with future treatment cassettes, and cap removal reduces packaging space. A CFD improvement does not establish fabrication, maintenance, structural, acoustic, or product suitability.

### How It Will Be Validated

Compare the empty-tower KVO 250 fields under common mesh/solver rules, then retain the best empty case as a control for any source-backed filter-resistance study. Later mesh, transient, physical airflow, maintenance, and fabrication checks remain required.
