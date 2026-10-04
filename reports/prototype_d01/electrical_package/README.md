# D01 electrical review E00 - 4 October 2026

**Current supplement, 5 October:** [four-page E01 power/wiring drawing](AQI_D01_POWER_AND_WIRING_SUPPLEMENT.pdf), [catalogue/conditional coordination calculation](POWER_COORDINATION.json) and [rated/reference parts](E01_RATED_PARTS.csv). Connector-level chain, official P14 Max pin functions, supply/controller/hub limits and protection coverage.20 assumed load scenarios and36 copper-drop examples; ten analytic/synthetic tests pass. No completed physical terminal schedule, fuse/wire selection or implemented protective restart. E00 PDF/ZIP preserved; E01 is included in the current50-page shareable technical handoff/ZIP.

Reproduce: `python scripts/analysis/d01_electrical_closure.py`, `python scripts/analysis/test_d01_electrical_closure.py`, `python scripts/reports/build_d01_power_closure.py` (ReportLab and pypdfium2 needed only for drawing/render). Current ARCTIC/Noctua primary source URLs and access date are in JSON. Only fan1 RPM is forwarded upstream; no four-fan protective feedback. Larger adapter alone cannot uprate the selected24W hub input. **Do not bridge unselected PR1 or energize this drawing.**

Later supplementary evidence: [protective-control candidate decision](PROTECTIVE_SELECTION_DECISION.md) and PROTECTIVE_CANDIDATE_SCREEN.json. Three OEM relays screened; none selected as a complete protective assembly. Eight reproducible checks pass. These supplements are not included in the original E00 PDF/ZIP.

Open **AQI_D01_ELECTRICAL_REVIEW.pdf**. This is the consolidated package 2 review for R03M, NOT released wiring or energization instructions.

Includes: OEM power-reference schematic; nominal and startup-sensitivity arithmetic; interface CSV; reference/unresolved BOM; enclosure/cable integration constraints; restart requirements with executable abstract tests; physical commissioning cases and three explicit electrical release blockers.

The protective module remains UNSELECTED. Hardware implementation, conductor/fuse ratings, terminal assignments, protective reliability and physical commissioning are not complete. Model PASS does not change this status. All physical tests NOT EXECUTED; prototypes 0.

The hub self-resetting protection and single upstream RPM channel prevent claiming this OEM chain is an independent four-fan protective system. Keep SATA unused and logger independent. No purchases, installations, supplier messages or publication performed.

Reproduce from repository root using Python with ReportLab:
`python scripts/analysis/d01_control_acceptance.py`
`python scripts/reports/build_d01_electrical_package.py`

Next meaningful work: finish rated protection/interface engineering and the actual filter/flow validation package, not another cosmetic CAD branch. Outdoor/public deployment remains unqualified.
