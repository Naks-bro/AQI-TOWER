# V01 — Actual KVO 250 / empty Concept A tower

Status: RUN COMPLETED; PARTIAL / NON-CONVERGED, final fields at iteration 4000.

This case uses the supplied six-point Systemair KVO 250 curve, not the former fixed-300-Pa placeholder. The placeholder was never run and is preserved in archive_placeholder/.

The model predicts about 1476 m³/h, 17.33 Pa fan-static-equivalent head, and 32.46 Pa tower static-pressure difference. These are distinct pressure measures. Residual criteria are not fully met.

- Full setup: ../../docs/CFD_V01_FAN.md
- Results and limitations: ../../results/CFD_V01_FAN_RESULTS.md
- Figures and raw metrics: ../../results/CFD_V01_FAN/
- Exact input provenance: fan_implementation.json
- Mesh: copied byte-for-byte from V00; no CAD edits or new cells.
- Logs: logs/foamRun_kvo.log (initial solve, post-End cleanup crash) and logs/foamRun_kvo_continue.log (clean diagnostic continuation).
- Existing-run guards prevent automatic resets. See setup documentation before reproducing.
- The active controlDict describes continuation to iteration 4000 and preloads the locally compiled boundary library. Initial dictionaries are in logs/initial_kvo_setup/.

No filters, particles, water, solar, batteries, optimization or dashboard are included. No final fan or purification claim is made.
