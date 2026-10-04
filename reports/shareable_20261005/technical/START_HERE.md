# AQI Tower technical bundle

Read AQI_TOWER_TECHNICAL_HANDOFF.pdf: 50 pages comprising the current five-page introduction, preserved 41-page IH02 engineering reference and four-page E01 power/wiring supplement. Room-model software and existing exploratory decay tool are included; read ROOM_MODEL_BASIS.md. Record actual decisions in TECHNICAL_REVIEW.xlsx. Not for fabrication, ordering or energization.

The last four pages provide the current power path, fan pin-function reference, catalogue-load and conditional wire-drop calculation, and exact remaining protection gaps. From engineering/ run python scripts/analysis/d01_electrical_closure.py and python scripts/analysis/test_d01_electrical_closure.py. Ten synthetic tests, not physical commissioning. PR1 protection, actual wires/fuses/enclosure and manual-restart implementation are still UNSELECTED; do not bridge this open design.

New separate E02 candidate: AQI_D01_OPTA_BENCH_REVIEW.pdf and engineering/firmware/d01_opta_review/. Implemented ordinary C++ START/STOP/RESET logic for proposed Opta Lite; all relay outputs disabled by default.1,041 host assertions,1,024 one-step cases. Run python scripts/analysis/test_d01_opta_host.py with existing g++ from engineering/. Not target-board compiled, not safety-rated, no hardware tested, no fan connection release. External enclosure and real fuse screens do not establish coordination. Firmware README names exact OEM sources and remaining protection gaps; existing project safety requirements unchanged.

Latest separate mechanical supplement: MASS_STABILITY_REVIEW.md. Corrected partial mass and directional static tipping arithmetic, NOT whole-device mass or safety approval. From engineering/ run python scripts/analysis/d01_mass_stability.py and python scripts/analysis/test_d01_mass_stability.py. Original mechanical PDFs and IH02 are preserved snapshots.

Authoritative assembly: engineering/reports/prototype_d01/mechanical_package/D01_R03M_ASSEMBLY.FCStd. STEP, exploded CAD, harness reservation derivative and 15 review DXFs accompany it. Blender and the offline viewer are tessellated presentation derivatives, not manufacturing models or CFD validation.

Run tools from engineering/ using TOOL_USAGE.md. The current pressure budget and blank filter curve are supplied. Supply actual measured data and calibration/source evidence; do not substitute animation dots for results.

Outstanding: exact filter resistance/tolerances, guard/structure/seal release, cable dimensions, hazard/protection/rated electrical enclosure, premises/targets, quotes, fabrication, commissioning and physical tests. OEM technical replies remain pending in reviewed records.

No lab assumed. No physical prototype built. Outdoor heat, rain, vandal resistance, site anchoring and measurable benefit remain separate future engineering.
