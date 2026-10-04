# Running the current tools

Extract the whole ZIP. Open a terminal in engineering/. Python3 is required; these analysis tools use the standard library. No extra engineering program is needed to run the checks. FreeCAD opens FCStd; STEP is supplied for other CAD tools. This is a review package.

```
python scripts/analysis/d01_validation.py
python scripts/analysis/d01_guard_bending.py
python scripts/analysis/d01_control_acceptance.py
python -m unittest discover -s scripts/analysis -p test_d01_current_filter_screen.py -v
```

To compare real OEM or reviewed physical filter data, create a new CSV from FILTER_CURVE_BLANK.csv. Use per-filter flow, not total tower flow. Rows must be sorted, finite and nonnegative. Do not extrapolate. Supply exact evidence and the condition definition:

```
python scripts/analysis/d01_current_filter_screen.py CURVE.csv --part "EXACT PART AND REVISION" --source "DOCUMENT OR TEST RECORD" --evidence OEM --condition CLEAN --condition-ref "SOURCE CLEAN CONDITION" --output NEW_SCREEN.json
```

For measured data use --evidence PHYSICAL; for a loaded curve use --condition LOADED and its actual loading reference. The tool does not verify the truth of labels or the authenticity of a source. Separate clean and loaded runs are needed.15 scenarios use the actual R03M guard open area with assumed loss coefficients. A positive margin does not release purchase or establish actual operating flow.

For accepted physical airflow rows:

```
python scripts/analysis/d01_validation.py --airflow-csv AIRFLOW.csv --plane-area-m2 AREA --output NEW_FLOW.json
```

Replace AREA with the independently established full measurement-plane area in m2. It is not automatically the guard hole area. Velocity-only error is not complete uncertainty. Preserve raw logs and use new output filenames. All bundled test fixtures are synthetic; there are no physical test results.
