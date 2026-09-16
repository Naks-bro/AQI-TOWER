# AQI Tower — CAD V00

## Purpose

Provide the first simple parametric representation of the AQI Tower airflow architecture. The model is intended to support geometry review and become a clean foundation for later CFD preparation.

**This geometry has NOT been CFD validated.** It does not predict airflow, pressure drop, filtration, particle removal, fan performance, water behavior, or product performance.

## Concept Used

The model represents **Concept A — Vertical Cross-Flow with Separate Clean-Air Riser**, selected in Phase 3 as the best baseline for a first engineering model. This selection is an engineering judgement based on modelling simplicity, not a final product architecture decision.

Conceptual path:

```text
AIR_INLET
    -> DIRTY_PLENUM
    -> STAGE_01
    -> INTERSTAGE_01
    -> STAGE_02
    -> INTERSTAGE_02
    -> STAGE_03
    -> CLEAN_PLENUM
    -> CLEAN_RISER
    -> AIR_OUTLET
```

## Parameters

The FreeCAD document contains one spreadsheet named `Parameters`. All primary dimensions are defined there and referenced by native FreeCAD expressions. Changing a primary value and recomputing the document updates the dependent geometry.

Derived spreadsheet values center the airflow regions and calculate the stage positions, clean-plenum position, stage-top elevation, and riser dimensions. Dimensions are not repeated as independent constants across the model.

Every primary numerical entry is labelled:

**MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT**

## Placeholder Dimensions

| Parameter | V00 value | Meaning | Status |
| --- | ---: | --- | --- |
| `TowerHeight` | 2000 mm | Reference-envelope height | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `TowerWidth` | 800 mm | Reference-envelope width | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `TowerDepth` | 700 mm | Reference-envelope depth and airflow direction | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `InletHeight` | 700 mm | Inlet and lower airflow-path height | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `InletWidth` | 600 mm | Inlet and lower airflow-path width | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `InletBaseZ` | 150 mm | Inlet lower-edge position above the origin | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `OutletHeight` | 250 mm | Rear outlet-region height | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `OutletWidth` | 500 mm | Outlet and clean-riser width | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `OutletPosition` | 1600 mm | Outlet lower-edge elevation | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `DirtyAirPlenumDepth` | 140 mm | Dirty-air distribution-region depth | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `TreatmentRegionThickness` | 30 mm | Generic thickness of each stage placeholder | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `TreatmentRegionSpacing` | 40 mm | Air space between adjacent stage placeholders | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `CleanAirPlenumDepth` | 180 mm | Lower clean-air collection-region depth | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |
| `InterfaceThickness` | 10 mm | Visual thickness for inlet and outlet regions | MODELLING PLACEHOLDER — NOT A PRODUCT REQUIREMENT |

The values are also recorded as assumption `A-005` in `requirements/ASSUMPTIONS.md` so they cannot be mistaken for hidden design inputs.

## Geometry Structure

The document contains one central parameter sheet, grouped reference geometry, grouped airflow regions, and grouped treatment placeholders.

| FreeCAD object | Function |
| --- | --- |
| `Parameters` | Central editable parameters, status labels, descriptions, and derived values |
| `TowerEnvelope` | Wireframe reference boundary; not a fluid region or final enclosure |
| `Inlet` | Ambient-air inlet interface volume |
| `DirtyAirPlenum` | Dirty-air distribution volume |
| `TreatmentStage_01` | Generic treatment/resistance placeholder; function unassigned |
| `InterstageGap_01` | Air volume between stages 01 and 02 |
| `TreatmentStage_02` | Generic treatment/resistance placeholder; function unassigned |
| `InterstageGap_02` | Air volume between stages 02 and 03 |
| `TreatmentStage_03` | Generic treatment/resistance placeholder; function unassigned |
| `CleanAirPlenum` | Lower clean-air collection volume |
| `CleanAirRiser` | Upper clean-air riser and outlet-transition volume |
| `Outlet` | Clean-air outlet interface volume |

Treatment stages are intentionally named generically. V00 does not assume that they represent a prefilter, water stage, biochar, HEPA, or any particular sequence.

## CFD Interfaces

Each relevant FreeCAD object includes a `CFDRegion` metadata property.

| Required interface or region | FreeCAD object | Current representation |
| --- | --- | --- |
| `AIR_INLET` | `Inlet` | Short rectangular interface volume |
| `DIRTY_PLENUM` | `DirtyAirPlenum` | Rectangular distribution volume |
| `STAGE_01` | `TreatmentStage_01` | Simple rectangular resistance-region placeholder |
| `STAGE_02` | `TreatmentStage_02` | Simple rectangular resistance-region placeholder |
| `STAGE_03` | `TreatmentStage_03` | Simple rectangular resistance-region placeholder |
| `CLEAN_PLENUM` | `CleanAirPlenum` | Rectangular collection volume |
| `CLEAN_RISER` | `CleanAirRiser` | Rectangular vertical/transition volume |
| `AIR_OUTLET` | `Outlet` | Short rectangular interface volume |

`InterstageGap_01` and `InterstageGap_02` preserve continuous airflow space between the three generic treatment regions.

## What This Model Represents

- A simplified vertical cross-flow topology
- An inlet and dirty-air distribution region
- Three independently identifiable generic treatment regions
- Air gaps between treatment regions
- A clean-air collection region
- A clean-air riser and separated rear outlet
- Centralized, editable dimensional parameters
- Distinct named regions suitable for later boundary and region planning
- A technical color/transparency scheme and embedded FreeCAD thumbnail

## What This Model Does NOT Represent

- A final tower design or approved product dimensions
- A selected indoor, semi-enclosed, or outdoor application
- A selected airflow, CADR, pollutant target, or performance level
- Fan blades, motors, fan curves, or a validated fan count
- Filter pleats, fibres, pores, grades, media particles, or manufacturer products
- A confirmed treatment order
- Water, droplets, spray nozzles, demisting, drainage, or a pump
- Particles, gas chemistry, adsorption, filtration efficiency, or loading
- Screws, bolts, fillets, seals, structural joints, doors, or fabrication details
- Electrical, solar, battery, controller, communications, or sensor hardware

## Basic Validation

The generator created the file, closed it, reopened it, recomputed it, changed two central parameters, confirmed dependent geometry changed, restored the documented values, recomputed again, and saved the final state.

| Check | Result |
| --- | --- |
| File created and reopened with FreeCAD 1.1.3 | PASS |
| Required major regions present | PASS |
| Eleven geometry objects contain one valid solid each | PASS |
| Ten airflow/treatment regions have distinct bounds | PASS |
| Accidental duplicate region bounds | None detected |
| Unintended volumetric overlap between airflow/treatment regions | None detected |
| Nine consecutive interfaces are geometrically connected | PASS |
| `TowerHeight` regeneration test | PASS |
| `TreatmentRegionSpacing` regeneration test | PASS |
| Placeholder values restored after tests | PASS |
| Saved GUI colors, transparency, and thumbnail | PASS |

These checks establish basic CAD consistency only. They do not establish CFD suitability under a particular meshing workflow or engineering performance.

## Known Limitations

- All numerical dimensions are temporary placeholders.
- The reference envelope is not a designed enclosure or structural solid.
- Inlet and outlet are represented as short volumes rather than final boundary faces.
- The stage volumes have no assigned material, porosity, resistance, or efficiency.
- No fan region is included because fan count and placement remain unresolved.
- The riser/outlet arrangement is a simple baseline and has not been optimized.
- Clearances, service doors, seals, leakage paths, weather protection, and structural stability are absent.
- No external airflow domain is included.
- No mesh-quality study or CFD export has been performed.
- The geometry has not been compared with the Concept B alternative.

## Next Step

Phase 5 should prepare a controlled CFD plan and decide how the named regions will be represented in OpenFOAM. Before simulation, the team must define or explicitly register assumptions for inlet conditions, outlet conditions, stage resistance, wall treatment, external-domain need, convergence criteria, and comparison cases. OpenFOAM, ParaView, and CfdOF have not been installed, and no CFD work has begun.

