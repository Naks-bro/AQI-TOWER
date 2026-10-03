# Electrical review handout — assistant prepares, reviewer checks

3 October 2026. DRAFT REVIEW SCOPE — NOT A WIRING INSTRUCTION.

The user may give this package to an ENTC engineer to check accuracy. Their availability and competence for each review item are not yet confirmed. The assistant remains responsible for preparing the requested digital work. Do not delay all development waiting for this optional person, or interpret this handout as accepted sign-off.

## What to check

New preparation: [operating/fault sequence](CORE_CONTROL_SEQUENCE.md) and [functional visual](CORE_ELECTRICAL_FUNCTIONS.svg), with unreleased interfaces and unexecuted commissioning cases. Review the requirements; they are not installed safety functions or completed E01–E06 drawings.

| Review item | Current evidence | Required response |
|---|---|---|
| Exact fan motor/controller | Historical AC data and a different unselected EC candidate | Confirm the actual SKU/OEM diagram; do not mix AC and EC circuits |
| Supply and protection | Functional plan only | Confirm site supply/fault inputs; review ratings, isolation, protection and restart behavior with a qualified electrical professional |
| Bonding and segregation | Functions described, not a completed installation drawing | Review enclosure/panel bonding, cable routing, strain relief and separation |
| Sensor acquisition | Offline recorder exists; SPS30 USB kits and SDP8xx are candidates | Confirm delivered devices, voltage/interface compatibility, ports, duplicate addresses and driver/export format |
| Data correctness | Synthetic recorder/analysis tests | Reference-check real channels, clocks, units, signs, missing data and calibration records |
| Access/safety functions | Conceptual stop/isolation/interlock only | Review safe service/fan run-down behavior independently of laptop/software failures |

Read [electrical plan](ELECTRICAL_PLAN.md), [instrument kit](INDOOR_INSTRUMENT_KIT.md), [no-lab route](NO_LAB_BUILD_ROUTE.md), [recorder](MEASUREMENT_RECORDING.md) and [analysis limits](INDOOR_DECAY_ANALYSIS.md).

Return comments with document revision, issue/location, suggested correction, supporting OEM reference and review scope. State what you did NOT verify. The assistant can apply justified corrections and rerun digital checks. No vague 'looks correct' approval for a mains assembly.

## Deliverables still to prepare from verified inputs

E01 single-line; E02 actual power/control circuit; E03 terminals/cables; E04 enclosure/bonding; E05 rating/coordination calculations; E06 physical commissioning procedure and records. These depend on actual fan/controller and site facts. They are not complete merely because a functional block diagram exists.

An optional reviewer can take a qualified role only where competence/authorization is established. Otherwise hire the appropriate electrical reviewer/assembler. Final on-site checks and any required mechanical/test review remain independent requirements. Do not connect mains or energize the unfinished tower from this package.
