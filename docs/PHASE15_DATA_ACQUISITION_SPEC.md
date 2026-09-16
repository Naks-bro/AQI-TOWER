# AQI Tower Phase 15 — Data Acquisition Specification

**PHASE 15 — SPECIFICATION DOCUMENT**
**STATUS: DESIGN ONLY — NO EXPERIMENT PERFORMED**
**Date: 2026-09-06**

---

## 1. Purpose

This document defines the synchronized data schema, logging architecture, and calibration requirements for the Phase 15 packed-bed test rig. It covers both clean-air pressure-drop tests and future HCHO breakthrough tests. The architecture is chosen to be simple, reproducible, and affordable within student-project constraints.

---

## 2. Architecture Choice and Justification

**Selected architecture: Raspberry Pi 4B + Python CSV logger**

| Option | Pros | Cons | Decision |
|---|---|---|---|
| Raspberry Pi + Python | Linux OS; direct I²C to SFA30; PWM/ADC for DP; portable; ~₹6,000–7,000; no per-run software cost; straightforward CSV output; widely supported in India | Requires basic Python coding; needs SD card; outdoor/wet environments need enclosure | **SELECTED** |
| Arduino + SD shield | Very low cost; simple; well-documented | No native floating-point RTC; I²C library for SFA30 requires more work; less flexible for future sensors | Reserve as backup / redundant logger |
| Commercial DAQ (NI USB-6008) | Professional; calibrated; LabVIEW ready | Very high cost; overkill for student project | Not recommended for initial setup |
| Spreadsheet via manual entry | Zero cost | Timing errors; human errors; not synchronized; unacceptable for breakthrough curve | Rejected for run data |

The Raspberry Pi approach:
- reads both SFA30 modules via I²C at 0.5–1 s intervals
- reads the DP sensor (via ADC or I²C, depending on sensor type)
- timestamps every row with an NTP-synchronized clock (or battery-backed RTC if no network)
- writes to CSV on the local SD card
- optionally streams to a USB-connected laptop or shared folder

---

## 3. Minimum Data Schema

Every measurement row must contain all of the following fields. Fields marked (REQUIRED) cannot be omitted; fields marked (RECOMMENDED) may be added if the instrument is available.

### 3.1 Mandatory fields — every row

| Field name | Units | Source | Notes |
|---|---|---|---|
| `timestamp_utc` | ISO 8601 string (YYYY-MM-DDTHH:MM:SS.sss) | Raspberry Pi RTC | UTC preferred; log local offset in header |
| `run_id` | String (e.g., RUN_20261015_001) | Operator entry at session start | Unique per replicate |
| `media_lot` | String | Operator entry at session start | From certificate; "OVC4x8_LOT_A" etc. |
| `media_name` | String | Operator entry | "OVC4x8" or "FORMASORB" or "EMPTY" |
| `bed_depth_mm` | mm (float) | Operator entry at session start | Measured settled depth |
| `media_mass_g` | g (float) | Operator entry at session start | Dry mass weighed before run |
| `column_id_mm` | mm (float) | Constant (75.0 for Phase 15 column) | Per rig design |
| `superficial_velocity_ms` | m/s (float) | Derived from measured flow | `Q_lpm / (60000 × A_m2)` |
| `flow_lpm` | L/min (float) | Read from calibrated flow instrument | Rotameter or MFC; actual measured value |
| `upstream_hcho_ppb` | ppb (float) | SFA30 #1 (upstream) | Raw sensor reading; do not apply correction here |
| `downstream_hcho_ppb` | ppb (float) | SFA30 #2 (downstream) | Raw sensor reading |
| `upstream_T_degC` | °C (float) | SFA30 #1 integrated SHT | |
| `upstream_RH_pct` | % RH (float) | SFA30 #1 integrated SHT | |
| `downstream_T_degC` | °C (float) | SFA30 #2 integrated SHT | |
| `downstream_RH_pct` | % RH (float) | SFA30 #2 integrated SHT | |
| `dp_sensor_Pa` | Pa (float) | Differential pressure sensor (upstream tap − downstream tap) | Positive = pressure drop across bed |
| `sfa30_upstream_status` | Integer (0 = OK, other = error code) | SFA30 #1 status register | Log raw status word |
| `sfa30_downstream_status` | Integer | SFA30 #2 status register | |
| `operator` | String | Operator entry at session start | |
| `notes` | String | Operator entry (inline or end-of-row) | Alarms, valve changes, sensor events |

### 3.2 Derived fields — computed in post-processing, not during logging

| Field name | Formula | When computed |
|---|---|---|
| `C_over_C0` | `downstream_hcho_ppb / upstream_hcho_ppb` | Post-processing only; requires transport-delay correction first |
| `downstream_hcho_ppb_corrected` | Shift downstream time series by `Δt_transport` | Post-processing |
| `delta_P_corrected_Pa` | `dp_sensor_Pa − fixture_dp_Pa_at_same_flow` | Post-processing (subtract empty-column baseline) |
| `EBCT_s` | `bed_depth_mm / (1000 × superficial_velocity_ms)` | Post-processing |
| `treated_bed_volumes` | `Q_lpm × elapsed_time_min / bed_volume_mL × 1000` | Post-processing |
| `dynamic_adsorbed_mass_mg_g` | `∫Q(C_in − C_out)dt / media_mass_g` | Post-processing, breakthrough runs only |

**Do not smooth, interpolate, or discard raw logged rows.** Post-processing should be done on a separate copy of the raw CSV.

### 3.3 Session header (written once per run, not per row)

The logger must write a header block at the start of each run file containing:

```
# AQI-TOWER BENCH TEST SESSION RECORD
# run_id: RUN_20261015_001
# date_start: 2026-10-15
# operator: [name]
# media_name: OVC4x8
# media_lot: [lot ID from certificate]
# media_dry_mass_g: [value]
# settled_bed_depth_mm: [value]
# column_id_mm: 75.0
# column_material: SS316
# target_superficial_velocity_ms: 0.26
# target_EBCT_s: 0.100
# test_type: PRESSURE_DROP / BREAKTHROUGH  (select one)
# HCHO_generation: NONE / CYLINDER_DILUTION  (select one)
# ambient_T_degC_at_start: [value]
# ambient_RH_pct_at_start: [value]
# ambient_pressure_kPa_at_start: [value]
# dp_sensor_model: [model and serial]
# dp_sensor_cal_date: [date]
# sfa30_upstream_serial: [serial if available]
# sfa30_downstream_serial: [serial if available]
# rotameter_model: [model]
# rotameter_cal_date: [date]
# transport_delay_s_at_this_flow: [Δt measured in setup]
# fixture_dp_Pa_at_this_flow: [empty-column ΔP at same U_s]
# notes: [any pre-run conditions]
```

---

## 4. Logging Software Architecture

### 4.1 Core loop

```python
# Pseudocode — not production code; implement and test before first run
import time, csv, datetime
from sensirion_i2c_sfa3x import Sfa3xI2cDevice  # Sensirion Python driver
import ads1115  # for analog DP sensor if needed

LOG_INTERVAL_S = 1.0  # target 1 s; sensor updates every 0.5 s

def read_sfa30(device):
    hcho, hum, temp = device.measure_raw_signals()
    # convert per Sensirion driver convention
    return hcho_ppb, temp_degC, hum_pct, status

def read_dp_sensor():
    # read 16-bit ADC value; convert to Pa using calibration factor
    return dp_Pa

with open(log_filename, 'w', newline='') as csvfile:
    write_header(csvfile)  # session header block
    writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
    writer.writeheader()
    while run_active:
        row = {
            'timestamp_utc': datetime.datetime.utcnow().isoformat(),
            'run_id': RUN_ID,
            # ... fill all mandatory fields ...
            'upstream_hcho_ppb': read_sfa30(upstream_device)[0],
            'downstream_hcho_ppb': read_sfa30(downstream_device)[0],
            'dp_sensor_Pa': read_dp_sensor(),
            # etc.
        }
        writer.writerow(row)
        csvfile.flush()
        time.sleep(LOG_INTERVAL_S)
```

### 4.2 Clock synchronization

- If network is available: use `systemd-timesyncd` or `ntpdate` to synchronize to NTP before each run; verify clock is within ±1 s of reference
- If no network: use a DS3231 battery-backed RTC module connected via I²C; set the RTC at the start of each run using a phone/internet reference; verify drift after long runs

### 4.3 File management

- One CSV file per run replicate; filename includes run_id and timestamp: `RUN_20261015_001_20261015T093045.csv`
- Copy CSV to at least one backup location (USB drive or shared network folder) immediately after each run
- Never overwrite or delete raw run CSVs; move to an archive folder after processing

### 4.4 Alarm logic (optional but recommended)

Log a warning row if:
- `upstream_hcho_ppb > 1000` (SFA30 range exceeded)
- `dp_sensor_Pa > 450` (approaching sensor limit)
- `sfa30_upstream_status != 0` or `sfa30_downstream_status != 0`

The logger must not automatically stop the experiment on alarm; it logs and alerts the operator who makes the stop decision.

---

## 5. DNPH Sample Record

DNPH samples are not logged by the DAQ system. Use a separate paper form for each cartridge:

```
DNPH CARTRIDGE RECORD
Cartridge ID:         [alphanumeric label on vial]
Position:             UPSTREAM / DOWNSTREAM / BLANK / FIELD_BLANK
Run ID:               [matching run_id from logger]
Sampling pump ID:     [pump serial]
Pump flow (L/min):    [calibrated value]
Start time (UTC):     [time when cartridge connected to port]
End time (UTC):       [time when cartridge sealed]
Total volume (L):     [pump flow × duration]
Storage condition:    Sealed amber vial; refrigerated at 4°C
Transport condition:  On ice; shipped within 7 days
Laboratory ID:        [external lab name and accreditation number]
Notes:
```

---

## 6. Calibration Requirements

### 6.1 Differential pressure sensor

| Task | Frequency | Method |
|---|---|---|
| Zero check | Before every test session | Block both taps; read should be ≤ ±1 Pa |
| Span check | Before every test session | Apply known pressure (≥ 50 Pa) using a water column or reference; compare reading |
| Full calibration | Annually or if check fails | Multi-point comparison against reference manometer; generate correction table |

### 6.2 SFA30 HCHO

| Task | Frequency | Method |
|---|---|---|
| Co-location | Before every campaign | Place both SFA30s in the same clean-air stream for ≥ 30 min; record offset |
| Zero check | Before every run | Both SFA30s should read ≤ 5 ppb in clean air; if higher, identify source |
| Span validation | Each campaign | DNPH sample during stabilized inlet; compare DNPH-HPLC result to SFA30 upstream reading |
| Position swap | Each campaign (one replicate) | Swap upstream and downstream modules; quantify position bias |

### 6.3 Airflow / rotameter

| Task | Frequency | Method |
|---|---|---|
| Calibration check | Before first use; after any repair | Compare rotameter reading against a calibrated reference (bubble flowmeter or certified MFC) at 3 flow points |
| Density correction | Each use | Correct reading for laboratory T and P if rotameter is calibrated for standard conditions |

---

## 7. C/C0 Calculation Procedure

This is a post-processing procedure; do not compute C/C0 in the logger.

**Step 1 — Load raw CSV.** Read all rows without modification.

**Step 2 — Apply transport-delay correction.** Shift downstream HCHO time series earlier by `Δt_transport` measured during the blank run at the same flow.

**Step 3 — Apply co-location offset.** If the co-location test showed a systematic offset between the two SFA30s (e.g., upstream reads 5 ppb higher on the same stream), subtract that offset from upstream readings before computing C/C0. Document and report the correction magnitude.

**Step 4 — Compute C/C0.** Only for periods where both sensors are above their measurement floor (> 20 ppb). Below 20 ppb, label as `< LOD; C/C0 indeterminate`.

`C_over_C0 = downstream_hcho_ppb_corrected / upstream_hcho_ppb_corrected`

**Step 5 — Compute t10.** Find the first timestamp where `C_over_C0 ≥ 0.10` is sustained across three consecutive evaluation windows, each ≥ 2 minutes. `t10` is the start of that first sustained window.

**Step 6 — DNPH cross-check.** For each DNPH pair (same interval, upstream + downstream), compute `(C/C0)_DNPH = C_downstream_DNPH / C_upstream_DNPH`. Compare to the SFA30-derived time-average over the same interval. Discrepancies > 25% must be investigated and reported.

**Step 7 — Compute treated bed volumes.** `BV = Q_lpm × elapsed_min / bed_volume_mL × 1000 / 60`. Report C/C0 against both time and BV axes.

---

## 8. Example Output Table (from a single run, illustrative format only)

```
timestamp                | C_in_ppb | C_out_ppb | C/C0  | ΔP_Pa | Q_lpm | T_up°C | RH_up%
-------------------------|----------|-----------|-------|-------|-------|--------|-------
2026-10-15T09:30:00.000  |  82.1    |   0.0     | <LOD  |  4.3  | 69.1  |  25.2  |  49.8
...
2026-10-15T11:15:00.000  |  81.8    |  12.4     | 0.152 |  4.3  | 69.0  |  25.3  |  50.1
```

All such tables are illustrative; no actual run has been performed in Phase 15.

---

## 9. Data Retention and Chain of Custody

| Record | Retention | Storage |
|---|---|---|
| Raw CSV logger files | Permanent | SD card + at least 2 independent backups |
| DNPH cartridge forms | Permanent | Physical binder + scanned copy |
| External lab report | Permanent | Digital + physical |
| Sensor calibration records | Permanent | Physical logbook |
| Session header sheets | Permanent | Physical binder |
| Photos (packing, column, setup) | Per campaign | Digital archive |

No logged data should be deleted to improve the appearance of results. Outlier rows should be flagged with the reason in the `notes` field and reported (not removed) in any publication.

---

*See also: `docs/PHASE15_TEST_RIG_ENGINEERING_SPEC.md` for rig architecture, `docs/PHASE15_BOM.md` for procurement, `docs/PHASE14_FORMALDEHYDE_TARGET.md` for Phase 14 requirements and breakthrough definitions.*
