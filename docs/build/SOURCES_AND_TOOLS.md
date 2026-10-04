# Sources and tools

Reviewed 2 October 2026. Public sources inform planning; they do not approve our design.

## External references

- [US EPA: air cleaners and filters](https://www.epa.gov/indoor-air-quality-iaq/air-cleaners-and-air-filters-home): filtration supplements source control/ventilation; does not remove every pollutant. Residential advice is not outdoor-tower validation.
- [EPA consumer guide](https://www.epa.gov/sites/default/files/2018-07/documents/guide_to_air_cleaners_in_the_home_2nd_edition.pdf): clean-air delivery should match the room. Our room sizing and outdoor flow comparison are explicitly our own screening assumptions, not EPA ratings.
- [IEC 60335-2-65:2023 public scope](https://webstore.iec.ch/en/publication/70378): appliance safety reference for expert review with Part 1. Full standard not acquired; requirements/compliance not inferred from a web summary.
- [Systemair fan instruction catalogue result](https://shop.systemair.com/upload/assets/202341_FANS_INSTRUCTIONS_CE__A016_.PDF): OEM instructions must be matched to the exact purchased fan; this link alone does not resolve historical KVO 250/L identity.
- [QElectroTech official site](https://qelectrotech.org/index.php) and [downloads](https://qelectrotech.org/download): free electrical drawing software. Drawing software is not an electrical-safety checker.

## Local evidence

`docs/CAD_V00.md`, `cad/parametric/v00.json`, `cad/parametric/PHASE8_GEOMETRY_AUDIT.json`, `docs/FILTER_BYPASS_FIX.md`, `results/FILTER_H13/bypass_analysis_sealed.json`, `data/fans/systemair_KVO_250.json`, `data/filters/freudenberg_SF13B_593x593x292.json`, `docs/PRESSURE_DROP_BUDGET.md`, Phase 15–19 documents. Historical supplier prices/contact details are not refreshed quotations.

## Tool decision

DETECTED in this review: FreeCAD executable at `D:\Applications\FreeCAD 1.1.3\bin\FreeCADCmd.exe`; WSL Ubuntu has `/opt/openfoam14` and `/usr/bin/pvpython`; Python, Git and Node executables are present. This presence check is not a complete functional verification of each installation.

Use existing FreeCAD for physical assembly and drawings; Python for transparent calculations; existing OpenFOAM/ParaView when the physical air path is frozen enough to simulate meaningfully; Git for revisions. Three.js is optional presentation, not build validation. No new MCP server is required to prepare this package.

RECOMMENDATION: QElectroTech later, when producing the detailed electrical sheets with the reviewer. Its installation status is UNKNOWN in this audit, and it was not installed. KiCad/custom PCB work is unnecessary for the first off-the-shelf logger. No paid CAD or extra simulation tool is currently justified.

## Skills

The skill-creator guide was used to write a small local `aqi-build-review` skill based on the specific project gaps and source checks. It is an agent workflow, not engineering certification. No third-party engineering skill was installed: an attractive GitHub checklist is not evidence that a mains-powered outdoor tower is safe. Prefer OEM manuals and accountable qualified reviews over indiscriminate downloads. Latest delivery basis is paid services where needed, not an assumed college lab or faculty reviewer.
