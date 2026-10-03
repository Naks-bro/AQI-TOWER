# Indoor test analysis: off versus on

3 October 2026. EXPLORATORY SOFTWARE — NO PHYSICAL RESULTS.

## In simple words

Particles may settle or leave a room even when the tower is off. This tool compares that natural change with the change when the tower is on. It helps investigate an additional effect rather than crediting the tower for every reduction.

It uses the [measurement recorder's CSV](MEASUREMENT_RECORDING.md), one instrument/channel and **one explicitly selected off/on pair**. No readings exist yet; only synthetic mathematical fixtures were used to test the code. Multiple positions and repeated paired trials still need separate analysis and review.

## What the calculation assumes

Project method from [Build and test sequence](BUILD_AND_TEST.md): fit `ln(particle concentration)` against elapsed hours for each selected window. Decay rate is the negative fitted slope. A conditional clean-air-flow estimate is `room volume * (on decay rate - off decay rate)` in m3/h.

This simple model assumes reasonably well-mixed air, matched ventilation and stable sources with negligible continuing influx/background relative to the selected readings. These are **ASSUMPTIONS**, not facts the software can verify. A nonzero asymptote, changing outdoor pollution, humidity effects, instrument drift, unequal mixing or changing ventilation can bias the result. No background subtraction or asymptotic model is implemented.

The estimate is withheld unless all three assumption declarations in the plan are explicitly true. Declaring them is not scientific validation. A negative estimate remains negative; it is not silently changed to zero. Warnings identify absent calibration references and hypothetical room volumes. There is no automatic performance PASS, statistical significance decision or certification.

For context, [EPA's guide](https://www.epa.gov/indoor-air-quality-iaq/guide-air-cleaners-home) describes CADR as a particle-cleaning measure for indoor room sizing, not gas removal (reviewed 3 October 2026). This project script is our exploratory decay implementation, NOT the EPA method or an AHAM certification procedure. It produces no outdoor radius, network spacing, HEPA-integrity or health claim.

## Use after supervised data collection

Copy `data/monitoring/decay_plan_TEMPLATE.json` into the actual test folder and fill:

- Exact run/instrument identity and room particle channel.
- Room volume and whether measured or assumed; actual dimensions remain UNKNOWN today.
- A usable concentration floor with instrument/test evidence, not an invented detection limit. Physical data requires a positive floor and a reference. The importer cannot authenticate that reference.
- Offset-bearing start/end timestamps for separate off/on windows and the reason for selecting them. Document excluded settling/warm-up periods before examining a favorable outcome; do not cherry-pick windows.
- Honest model-assumption declarations. Leave false if not supported.

Run with actual files (example paths do not exist yet):

```powershell
python scripts/analysis/indoor_decay.py --input data/monitoring/YOUR_RUN/measurements.csv --plan data/monitoring/YOUR_RUN/decay_plan.json --output data/monitoring/YOUR_RUN/decay_exploratory.json
```

Standard library only. All rows must belong to one identified run and one evidence kind. Selected readings must use ug/m3, a matching instrument/channel, correct stage and strictly increasing timestamps. No merging different sensors into one fit. No overlapping off/on windows. A five-reading minimum per window is a software guard, **not an adequate experimental sample-size specification**.

Zero, negative, nonfinite or at/below-floor values stop the analysis; none are clipped, imputed or selectively removed. This may make a low-concentration trial unusable under the model. Output refuses an existing filename and includes input/plan SHA256 provenance, fitted rates, sample durations, R-squared and log residuals for review.

## What remains before a performance report

No confidence interval is implemented. Total uncertainty remains UNKNOWN; room-volume uncertainty, correlated samples, sensor errors, window selection, ventilation differences and trial-to-trial variability are not quantified. R-squared alone does not establish a suitable model. A positive point estimate is not proof of useful improvement.

The test mentor must assess controls, mixing, residuals, calibration/floor, sampling/duration, repeatability and uncertainty before interpreting results. The existing provisional plan calls for at least three paired trials and multiple room locations, not one favorable pair. No pooled multi-trial estimate is supplied here. No deliberate hazardous aerosol challenge or energized testing is authorized by this software.

Exact instruments, installation, mechanical/electrical release and actual data remain pending. Follow the [physical test gates](BUILD_AND_TEST.md). Next: adapt the recorder to confirmed instruments, collect supervised readings after commissioning, then add uncertainty/repeatability analysis using real trial structure.

## Verification

```powershell
python -m unittest discover -s scripts/analysis -p 'test_indoor_decay.py'
python scripts/analysis/indoor_decay.py --help
```

Eight tests use synthetic exponential/constant fixtures only; they cover arithmetic, assumption withholding, negative differences, invalid readings, times/windows, evidence/units, outdoor refusal and physical-floor requirements. Synthetic values are not saved as project measurement results.
