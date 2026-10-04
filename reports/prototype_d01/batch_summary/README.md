# Single-batch engineering result — 5 October 2026

Three parallel agents worked on mechanics, electrical design and handoff consistency. Root integrated their results and corrected the E05 pair-recording indentation bug. Original R03M geometry and historical IH02 evidence remain intact. **Review handoff, NOT construction or energization release. Physical prototypes: 0.**

## Concrete engineering findings

- Actual saved model: two 43 mm filter closing gaps, 36 mm sleeves, 7 mm stack offset. The new robust interval solver determines whether a fixed stop covers supplied filter/gasket/flatness intervals. In the clearly ASSUMED broad tolerance example, no fixed stop works; no seal PASS or machining setting is invented.
- Four actual eight-bolt cabinet groups now have in-plane force/moment demand calculations and equilibrium tests. Material/joint capacity, racking, withdrawal, perforated guards and full stability remain unverified.
- Electrical screen separates total source load from the fan path. Fans plus Opta yield a 1.3095× fan-current multiplier ceiling before auxiliaries, 1.2381× with an ASSUMED 0.10 A auxiliary load. These are data-acquisition thresholds, not measured inrush approval.
- An ASSUMED source-limited 2 A fault does not establish clearing of the screened 2 A fuse. No fuse/holder/PR1 selected. Hazard allocation distinguishes accessible motion and service isolation from performance interruption, preserving existing restart requirements.
- E05 assumed service volumes clear each other without reduction. Audit found the recorded service-pair list omitted a true pair and duplicated a stale self label; corrected generator now requires exactly three distinct non-self pairs. Actual intersection checks were already inside the original loop and passed.
- Current 28-line parts register replaces outdated procurement navigation, not historical evidence. Root-generated current pressure budget and freshly copied input files retain exact byte hashes. Package audit distinguishes line-ending-only equivalence from actual content differences; ZIP manifests are always strict byte checks.

## One command

From project root, using existing Python:

```
python scripts/maintenance/run_d01_release_batch.py
```

From the extracted technical bundle's `engineering/` folder:

```
python scripts/maintenance/run_d01_release_batch.py --calculations-only
```

This runs six calculation/synthetic-test programs; project-root mode also checks the complete handoff. It never installs, flashes, wires or energizes. The `--calculations-only` report is stored in BATCH_VERIFICATION.json; the independent package audit is in batch_review/HANDOFF_CONSISTENCY.json. Outcomes are digital evidence, never safety/physical approval.

Current deliverables: mechanical_package/batch_closure; electrical_package/batch_closure; batch_review/CURRENT_COMBINED_PARTS_REGISTER.csv; control_module/CURRENT_RELEASE_GATES.csv. The consolidated PDF begins with current build decisions and E05/E02 diagrams; the earlier evidence follows unchanged.

## Real blockers retained

Exact filter/frame/gasket and harness geometry; material/guard/joint/stability acceptance; actual protective function/circuit and fault coordination; real component retention, terminations/entries and thermal evaluation; agreed room/targets/instruments; authorized procurement, fabrication and qualified commissioning, followed by physical performance measurements. Numeric low-current contact suitability remains unverified because the current OEM wording is ambiguous. No prices, stock or completion dates invented.

Generated cache/backup duplicates are excluded from the delivery copy; original/local evidence and backups remain untouched. No new supplier contacts, purchases, software installations or physical results in this batch.
