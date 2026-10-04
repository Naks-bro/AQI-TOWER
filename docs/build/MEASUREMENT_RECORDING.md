# First indoor trial: measurement recording

3 October 2026. SOFTWARE PREPARATION ONLY — no physical readings collected.

## What now works

`scripts/monitoring/record_measurements.py` imports readings from a JSON Lines file and writes a new CSV. It uses Python's standard library: no new installation. It accepts manual transcription or instrument exports converted to the input format. It is NOT a live sensor driver or fan controller.

The importer labels every reading as physical measurement or synthetic test, records instrument identity and units, converts offset-bearing timestamps to UTC, and preserves calibration references (UNKNOWN where absent). It rejects missing/nonfinite numbers, unit mismatches, unknown instruments, duplicate instrument/timestamp entries and backwards per-instrument timestamps. It refuses empty inputs and existing output filenames. Missing samples are omitted, not replaced with zeros or carried forward.

These checks establish file consistency, not accuracy/calibration or safe operation. A person can still enter incorrect data; preserve original exports and metadata alongside the derived CSV. No performance claim is generated.

## Channels and research stages

| Channel | Meaning | Input unit |
|---|---|---|
| pm25_room_a / pm25_room_b | Particle trend at two recorded positions | ug/m3 |
| dp_prefilter / dp_hepa | Signed filter differential pressure; document high/low tap orientation | Pa |
| airflow | Complete measured device flow with method recorded | m3/h |
| power | Measured electrical input from appropriate instrument | W |
| temperature | Temperature at recorded location | degC |
| humidity | Relative humidity | percent |
| noise | Sound measurement with method/location recorded | dBA |

Stages: `colocation`, `baseline_off`, `tower_on`, `postcheck`. These labels record research conditions, not switching commands. Instrument channels may have different sampling intervals; the software does not invent synchronized readings. Flow/power/noise measurements may be manual spot readings. Instrument ranges, response times and uncertainty still require selection/review.

## Use when real readings exist

1. Copy `data/monitoring/run_metadata_TEMPLATE.json` into a new test-run folder. Set run identity, location, room/ventilation conditions and approved test reference; register actual instruments, positions/methods, calibration/range/uncertainty. Template is intentionally not runnable until identities are filled.
2. Keep each instrument's raw export unchanged. Prepare `readings.jsonl` with one actual reading per line; no comments. Use exactly these fields: `timestamp`, `stage`, `channel`, `value`, `unit`, `instrument_id`, `notes`. Timestamp is ISO 8601 with UTC offset, e.g. `+05:30` for India. Register a unique instrument ID per measurement channel, even for a multi-channel device.
3. Put a numeric value in `value` only when measured. Record transcription/conversion steps and anomalies in notes. Do not relabel CFD or test fixtures as physical data. Set metadata `evidence_kind` to `synthetic_test` for development inputs.
4. Run, replacing paths with the actual new run folder:

```powershell
python scripts/monitoring/record_measurements.py --metadata data/monitoring/YOUR_RUN/metadata.json --input data/monitoring/YOUR_RUN/readings.jsonl --output data/monitoring/YOUR_RUN/measurements.csv
```

The example paths do not yet exist. No fabricated sample measurement file is supplied. All input is validated before output creation; an error identifies the input line. Output parent folder must already exist. Import is offline/batch, not continuous acquisition; raw files/metadata remain the provenance record.

## Before any physical trial

Follow [build and test gates](BUILD_AND_TEST.md) and [electrical review](ELECTRICAL_PLAN.md). Instruments and their safe installation must be reviewed. No unguarded energized testing, hazardous challenge or improvised mains measurement is authorized here. This software cannot isolate the fan, implement a safety interlock, verify HEPA integrity or prove an outdoor bubble. UNKNOWN calibration and acceptance limits remain visible, not silently certified.

Next software step: add an adapter for the actual chosen instrument/export format and validate against known reference readings. Do not select a sensor protocol or wire pins without its exact OEM documentation. Live acquisition is not implemented. A separate [exploratory single-pair decay tool](INDOOR_DECAY_ANALYSIS.md) now exists; it has no physical input or validated performance result.

## Verification

Eight tests use temporary synthetic fixtures only:

```powershell
python -m unittest discover -s scripts/analysis -p 'test_measurement_recording.py'
python scripts/monitoring/record_measurements.py --help
```

No test output is stored as project measurement evidence. Physical prototype/tests remain zero in the reviewed records.
