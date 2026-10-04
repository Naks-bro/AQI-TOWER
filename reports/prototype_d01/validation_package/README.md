# D01 validation V00

## Analyzer correction — 4 October 2026

Use the current repository script `scripts/analysis/d01_validation.py`, not the older copy embedded in this V00 folder/ZIP. The PDF/ZIP remain historical V00 snapshots and have NOT been regenerated. The current analyzer passes 23 synthetic/arithmetic checks and requires `--plane-area-m2 AREA` for physical CSV analysis. AREA is the independently established full measurement-plane area in square metres, not automatically the guard's open-hole area. Cell areas must sum to it within a numerical tolerance of 1e-6 relative (not a measurement uncertainty). A reviewer must still verify that cells do not overlap and cover the correct plane. Timezone-qualified ISO 8601 timestamps and one consistent calibration reference are required; the output records the source CSV SHA-256. No physical measurements were made.

Read AQI_D01_VALIDATION_PACKAGE.pdf. Five-page consolidated validation pack for mechanical R03M and electrical E00. NOT permission to energize. All physical records are blank / NOT EXECUTED.

R03M_PRESSURE_BUDGET uses actual proposed guard hole area, keeping loss coefficients explicitly assumed. It replaces the older 0.036 m2 guard-area screen for this revision only; no operating flow is established.

The CSV workbook consists of AIRFLOW_BLANK, RUN_LOG_BLANK and PARTICLE_TIMESERIES_BLANK. Copy templates into a new dated run folder; never replace raw observations. Cell count/layout must follow an approved measurement method. No automatic CADR/HEPA/outdoor claim.

From repository root:
`python scripts/analysis/d01_validation.py`
`python scripts/analysis/d01_validation.py --airflow-csv PATH --plane-area-m2 AREA --output NEW_PATH.json`
`python scripts/reports/build_d01_validation_package.py`

The analyzer validates arithmetic inputs, not their truth or calibration. Velocity-only error is not a full uncertainty budget. Physical review and commissioning remain required. Sources and input hashes accompany the pack.
