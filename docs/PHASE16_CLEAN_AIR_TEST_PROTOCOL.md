# AQI Tower Phase 16 — Clean-Air Pressure-Drop Test Protocol

**PHASE 16 — CLEAN-AIR PRESSURE-DROP RIG ONLY**
**STATUS: SPECIFICATION — NO EXPERIMENT PERFORMED, NO CFD RUN**
**Date: 2026-09-06**

---

## 1. Purpose and Scope

This protocol defines the complete procedure for measuring clean-air pressure drop across a packed bed of granular activated carbon (GAC) in the Phase 16 bench-scale rig. The output is a set of ΔP–U_s data pairs at three bed depths, fit to the Darcy–Forchheimer equation to yield empirical coefficients for future use in flow modelling and HCHO breakthrough test design.

**This protocol does not involve HCHO, any toxic gas, or any hazardous chemical.** Activated carbon is non-toxic in normal handling; standard dust precautions (gloves, dust mask) are required. Compressed air is the sole gas supply.

### 1.1 What this protocol produces

- Fixture (empty-rig) ΔP baseline as a function of flow (Stage A)
- Corrected bed ΔP = ΔP_total − ΔP_fixture for three bed depths (Stages B, C, D)
- Three independently repacked replicates per bed depth
- Fitted Darcy–Forchheimer coefficients a (Pa·s/m²) and b (Pa·s²/m³) from measurements only
- QC acceptance/rejection decisions for each replicate

### 1.2 Column and media reference

| Parameter | Value |
|---|---|
| Column ID | 75.0 mm |
| Column cross-sectional area A | 44.18 × 10⁻⁴ m² (4.418 × 10⁻³ m²) |
| Media | OVC 4×8 (Kuraray / Calgon Carbon), or equivalent GAC from same lot |
| Target bed depths | 26, 52, 104 mm |
| Target superficial velocities U_s | 0.13, 0.26, 0.52, 0.80, 1.05 m/s |
| Corresponding flows Q (75 mm col.) | 34.5, 68.9, 137.8, 212.1, 278.4 L/min |
| Ambient condition target | 25 ± 5°C, any RH (record measured value) |

---

## 2. Pre-Test Checklist

Complete before every test session (Stage A, B, C, or D).

| Item | Required state | Verified by |
|---|---|---|
| Media lot certificate | In hand with lot number, bulk density, particle size | Operator |
| Media dry mass | Confirmed ≤ 0.5% mass change between two consecutive 1-hour oven drying cycles at 105°C | Balance reading |
| Column assembly | End caps and O-rings seated; all bolts/clips tightened uniformly | Visual + bubble test |
| Bubble test | All joints at 200 Pa supply: ≤ 5 bubbles/minute at each joint | Soapy water |
| SDP810 zero | 0 ± 1 Pa with both taps open to atmosphere | DAQ reading |
| Testo 510 zero | 0 ± 1 Pa | Testo display |
| DAQ clock | NTP-synced (if network) or DS3231 RTC set from phone reference within 60 s | System time check |
| CSV header written | All mandatory header fields completed before logging starts | File inspection |
| Rotameter calibration check | Last calibration ≤ 3 months; correction factor noted in session header | Calibration record |
| Safety | Gloves worn for media handling; dust mask worn during packing and unpacking; no open flame near carbon | Operator |

---

## 3. Data Schema — Phase 16 Clean-Air

Every logged row must contain the following fields. No HCHO fields are included; they are defined in the Phase 15 Data Acquisition Specification for HCHO work.

| Field | Units | Source |
|---|---|---|
| `timestamp_utc` | ISO 8601 string | Raspberry Pi clock (NTP or RTC) |
| `run_id` | String (e.g., `RUN_P16_A_20261025_001`) | Operator |
| `stage` | String (`A`, `B`, `C`, or `D`) | Operator |
| `replicate` | Integer (1, 2, or 3) | Operator |
| `media_name` | String (`OVC4x8` or `EMPTY`) | Operator |
| `media_lot` | String | Operator (from certificate) |
| `media_dry_mass_g` | g (float) | Operator (weighed before run) |
| `settled_bed_depth_mm` | mm (float) | Operator (measured before sealing upper end cap) |
| `target_velocity_ms` | m/s (float) | Operator (from velocity sequence) |
| `flow_lpm` | L/min (float) | Rotameter reading (corrected if needed) |
| `dp_sdp810_Pa` | Pa (float) | SDP810 reading |
| `dp_testo510_Pa` | Pa (float or NaN) | Testo 510 reading (NaN if not connected at this moment) |
| `ambient_T_degC` | °C (float) | SHT40 at column inlet |
| `ambient_RH_pct` | % RH (float) | SHT40 at column inlet |
| `sdp810_status` | Integer (0 = OK) | SDP810 status register |
| `operator` | String | Operator |
| `notes` | String | Inline alarms, valve events, anomalies |

### 3.1 Session header

Written once per run file:

```
# AQI-TOWER PHASE 16 CLEAN-AIR TEST SESSION
# run_id: RUN_P16_B_20261025_001
# stage: B
# replicate: 1
# operator: [name]
# media_name: OVC4x8
# media_lot: [lot ID]
# media_dry_mass_g: [value]
# settled_bed_depth_mm: [measured value]
# column_id_mm: 75.0
# column_material: ACRYLIC
# target_velocities_ms: 0.13 0.26 0.52 0.80 1.05
# rotameter_model: [model]
# rotameter_cal_date: [date]
# rotameter_correction_factor: [value or 1.0 if within tolerance]
# sdp810_serial: [if labelled]
# sdp810_zero_check_Pa: [reading before run]
# testo510_zero_check_Pa: [reading before run or N/A]
# sht40_serial: [if labelled]
# fixture_dp_Pa_at_34.5lpm: [from Stage A]
# fixture_dp_Pa_at_68.9lpm: [from Stage A]
# fixture_dp_Pa_at_137.8lpm: [from Stage A]
# fixture_dp_Pa_at_212lpm: [from Stage A]
# fixture_dp_Pa_at_278lpm: [from Stage A or N/A if not yet run]
# ambient_T_start_degC: [value]
# ambient_RH_start_pct: [value]
# ambient_pressure_kPa: [value from phone/lab barometer]
# notes: [pre-run conditions, any deviations]
```

---

## 4. Stage A — Empty-Rig Baseline

### 4.1 Purpose

Measure the ΔP contribution of the empty column (fittings, screens, end caps, flow-path tubes) at each target flow. This is subtracted from Stage B, C, D totals to isolate the bed ΔP.

### 4.2 Assembly

- Install two mesh screens (one at each end) with no media between them.
- Seat end caps with O-rings. Tighten uniformly.
- Connect pressure taps to SDP810 and Testo 510.
- Confirm Stage A session header written.

### 4.3 Velocity sequence

Run velocity points in ascending order:

| Step | Target U_s (m/s) | Target Q (L/min) | Stabilization time |
|---:|---:|---:|---|
| A1 | 0.13 | 34.5 | 3 min |
| A2 | 0.26 | 68.9 | 3 min |
| A3 | 0.52 | 137.8 | 3 min |
| A4 | 0.80 | 212.1 | 3 min |
| A5 | 1.05 | 278.4 | 3 min |

At each step: adjust needle valve until rotameter reads the target flow ± 1 L/min. Log continuously for the full 3-minute stabilization window plus 1 additional minute of recording. Record the average of all 1-s readings during the recording minute as the `fixture_dp` for that flow. If the SDP810 reads above 480 Pa, stop and use Testo 510 reading only.

### 4.4 Stage A acceptance

- ΔP_fixture increases monotonically with Q.
- SDP810 and Testo 510 agree within ±3 Pa (or ±5%, whichever is larger) at all points.
- If sensors disagree: investigate pressure tube connections; repeat zero check; do not proceed until resolved.

### 4.5 Stage A outputs

A table of `fixture_dp_Pa_at_each_flow` that is entered in the header of every subsequent Stage B, C, D session file.

---

## 5. Stage B — 26 mm Bed

### 5.1 Target

Measure ΔP_total at five velocity points for a 26 mm settled bed of OVC 4×8. Three independently repacked replicates.

### 5.2 Media preparation (each replicate independently)

1. Dry OVC 4×8 in oven at 105°C for minimum 2 hours. Cool to room temperature in desiccator.
2. Weigh media to 0.01 g. Target mass for 26 mm bed: approximately 51 g (at estimated bulk density 450 kg/m³); actual value depends on lot measurement. Record exact weighed mass.
3. Load media into column from the upper end with lower end cap installed. Tamp column 20 times on a rubber mat.
4. Measure settled bed depth with digital caliper (depth gauge mode) from the upper face of the column bore to the top of the media surface. Record `settled_bed_depth_mm`.
5. If settled depth < 24 mm: add small additional mass (record), tamp again, remeasure. If settled depth > 28 mm: remove media, re-weigh, repack from scratch. Do not compress media to fit a target.
6. Install upper mesh screen. Install upper end cap. Tighten.

### 5.3 Velocity sequence (same for all packed stages)

Run in ascending order. Do not run descending to avoid bed compaction hysteresis.

| Step | Target U_s (m/s) | Target Q (L/min) | Stabilization | Stop criterion |
|---:|---:|---:|---|---|
| B1/C1/D1 | 0.13 | 34.5 | 3 min | — |
| B2/C2/D2 | 0.26 | 68.9 | 3 min | — |
| B3/C3/D3 | 0.52 | 137.8 | 3 min | See §7.1 |
| B4/C4/D4 | 0.80 | 212.1 | 3 min | See §7.1 |
| B5/C5/D5 | 1.05 | 278.4 | 3 min | See §7.1 |

At each step: stabilize flow, then log for 1 additional minute (60 data rows at 1 s interval). Compute mean and standard deviation of `dp_sdp810_Pa` over the recording window. Accept if SD/mean < 0.05 (coefficient of variation < 5%). If CV ≥ 5%, extend recording by 2 minutes and re-evaluate.

### 5.4 Replicate protocol

- Replicate 1: Fresh media from lot, freshly dried, independently weighed and packed.
- Replicate 2: **Discard media from Replicate 1** (do not re-use the same packed bed). Fresh portion of media from same lot, freshly dried, independently weighed and packed.
- Replicate 3: Same as Replicate 2, independently.

"Independent" means: each replicate uses a separate media portion that was dried, cooled, weighed, packed, tamped, and depth-measured without reference to prior replicate. The goal is to capture packing variability.

### 5.5 Between replicates

Disassemble column fully. Inspect screens for damage. Inspect O-rings for deformation. Record any media fines observed in the downstream screen (log in notes field).

---

## 6. Stages C and D — 52 mm and 104 mm Beds

Repeat the exact Stage B procedure (Section 5) for:

- **Stage C:** Settled bed depth 52 mm (target mass ~103 g at 450 kg/m³)
- **Stage D:** Settled bed depth 104 mm (target mass ~205 g at 450 kg/m³)

Three independently repacked replicates required at each depth.

### 6.1 Stage D special instructions (104 mm bed)

At Stage D, the Ergun-equation estimate predicts ΔP ~586 Pa at 1.05 m/s — potentially outside the SDP810-500Pa range.

**Stage D velocity sequence:**

1. Run D1 and D2 (U_s = 0.13 and 0.26 m/s) normally.
2. At D3 (U_s = 0.52 m/s): monitor SDP810 live. If reading > 450 Pa, stop D3 immediately and record "SENSOR LIMIT APPROACHED — use Testo 510 reading only."
3. At D4 (U_s = 0.80 m/s): begin with Testo 510 as primary. Record SDP810 reading for cross-check only if reading is < 480 Pa.
4. At D5 (U_s = 1.05 m/s): Use Testo 510 as primary. Record SDP810 only if below 480 Pa.
5. If the Testo 510 is not available, **do not run D4 or D5** until a wide-range DP instrument is confirmed operational.

---

## 7. Stop Criteria

### 7.1 Within-run stop criteria (apply at each velocity step)

| Condition | Action |
|---|---|
| SDP810 reading ≥ 490 Pa | Stop current velocity step. Record final reading. Use Testo 510 reading only for this and higher velocity steps. |
| SDP810 status ≠ 0 | Stop run. Investigate sensor fault. Do not accept data from faulted sensor. |
| Rotameter flow unstable (reading oscillates ± 5 L/min) | Wait 5 additional minutes. If oscillation continues, investigate air supply regulator. Do not record data until flow is stable. |
| Audible hiss from column fittings or pressure tap ports | Stop. Identify and repair leak. Repeat pre-test bubble test. Re-run the current replicate from the beginning. |
| Media audibly migrating or visible fines at downstream screen | Stop. Record observation. Disassemble and inspect. Do not re-run with compromised media packing. |

### 7.2 Replicate rejection criteria

Reject a replicate (and re-run) if:

- Settled bed depth outside ±3 mm of target (e.g., 26 ± 3 mm; if settled depth is < 23 mm or > 29 mm)
- CV of ΔP readings > 5% at any velocity point (after extended stabilization attempt)
- Sensor fault (SDP810 status ≠ 0) during any velocity step
- Leak detected at any point during the run

### 7.3 Stage termination criteria

Stop an entire stage (abandon all pending replicates) if:

- Three consecutive failed replicates with the same root cause — escalate to supervisor
- Media lot is confirmed exhausted without meeting minimum replicate requirement
- Equipment failure that cannot be repaired within one working day

---

## 8. Post-Processing and Darcy–Forchheimer Fitting

**All fitting is done post-test on the final confirmed dataset. No coefficients are invented or borrowed from literature for use as "expected" values.**

### 8.1 Step 1 — Load raw CSV files

For each replicate, load the raw CSV. Verify all mandatory fields are populated. Flag any rows with SDP810 status ≠ 0.

### 8.2 Step 2 — Compute corrected bed ΔP

For each velocity step in each packed-bed replicate:

```
ΔP_bed_Pa = mean(dp_sdp810_Pa over recording window) - fixture_dp_Pa_at_same_flow
```

or, where SDP810 was out of range:

```
ΔP_bed_Pa = mean(dp_testo510_Pa over recording window) - fixture_dp_Pa_at_same_flow
```

Use the `fixture_dp_Pa_at_each_flow` values from the Stage A run file header (not from any other source).

### 8.3 Step 3 — Compute ΔP/L

```
dP_over_L = ΔP_bed_Pa / (settled_bed_depth_mm / 1000)   [Pa/m]
```

### 8.4 Step 4 — Compute mean and spread across replicates

For each velocity and bed depth, compute:
- Arithmetic mean of ΔP_bed and ΔP_bed/L across three replicates
- Standard deviation
- Coefficient of variation (CV%) = 100 × SD / mean

**QC acceptance criterion (see Section 9):** CV% ≤ 15% for ΔP/L at every velocity point within a bed depth.

### 8.5 Step 5 — Darcy–Forchheimer regression

The Darcy–Forchheimer equation for a packed bed:

```
ΔP/L = a × U_s + b × U_s²
```

where:
- a [Pa·s/m²] is the viscous (Darcy) coefficient
- b [Pa·s²/m³] is the inertial (Forchheimer) coefficient
- U_s [m/s] is the superficial velocity

**Fitting procedure:**

1. Assemble the dataset: for each bed depth, list (U_s, ΔP/L_mean) for all five velocity points.
2. Fit the model ΔP/L = a·U + b·U² using ordinary least squares (Python `numpy.polyfit` with degree 2, no constant term; or `scipy.optimize.curve_fit`).
3. Constrain a > 0 and b > 0 (both physically required). If an unconstrained fit gives a negative coefficient, report the unconstrained result, flag it, and investigate.
4. Report 95% confidence intervals for a and b (from the covariance matrix of the fit).
5. Report R² of the fit to the mean ΔP/L data.
6. Compute fitted ΔP/L at each measured U_s and compare to measured mean. Report residuals as percentages of the measured value.

**Minimum acceptable fit:** R² ≥ 0.99 for ΔP/L vs U_s using the three-replicate mean values.

### 8.6 Step 6 — Cross-bed-depth consistency

Fit should ideally use all three bed depths simultaneously (assuming ΔP/L is independent of L — valid for uniform packing). Check: do fitted coefficients from 26 mm, 52 mm, and 104 mm data agree within ±20%? If yes, report the combined fit as the primary result. If there is a systematic trend (a or b increasing with L), report separately per depth and investigate end effects.

### 8.7 Step 7 — Report format

The Phase 16 results report must include:

| Bed depth | U_s | Rep 1 ΔP/L | Rep 2 ΔP/L | Rep 3 ΔP/L | Mean ΔP/L | CV% | Pass/Fail |
|---:|---:|---:|---:|---:|---:|---:|---|
| 26 mm | 0.13 | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... | ... |

Followed by fitted a, b, 95% CI, R², and residual table.

---

## 9. Quality Control Criteria

| QC Parameter | Threshold | Action if failed |
|---|---|---|
| SDP810/Testo 510 agreement | ≤ ±3 Pa or ±5% (whichever larger) at all points | Investigate connections; repeat zero check; do not proceed |
| ΔP/L CV across replicates | ≤ 15% at every velocity point | Re-run failed replicate; if third replicate also fails, escalate |
| SDP810 zero drift between runs | ≤ ±1 Pa | Re-zero before each run |
| Flow CV within recording window | ≤ 5% | Extend stabilization; if persists, fix air supply regulator |
| Darcy–Forchheimer R² | ≥ 0.99 | Investigate outlier replicates; report with flagged points |
| Residuals (fitted vs measured) | ≤ 15% at all U_s | Report as anomaly; compare with Ergun estimate for diagnostic |
| Settled bed depth tolerance | ±3 mm of target | Repack; do not accept out-of-tolerance beds |
| Media fines at downstream screen | None (zero) | Stop run; inspect; do not continue with compromised screen |

---

## 10. Data Retention

| Record | Minimum retention | Storage |
|---|---|---|
| Raw CSV run files | Permanent | SD card + ≥ 2 independent backups |
| Session header sheets (printed) | Permanent | Physical binder |
| Calibration records (rotameter, sensors) | Permanent | Physical logbook |
| Post-processing scripts (Python) | Permanent | Project repository or backup drive |
| Final Darcy–Forchheimer fit report | Permanent | Digital + physical |
| Photos of each packed bed (before sealing) | Per campaign | Digital archive |

No raw CSV row should be deleted. Outlier rows must be flagged in the `notes` field and reported, not removed.

---

## 11. Safety Summary

| Hazard | Control |
|---|---|
| GAC dust (carbon fines) | N95 or P100 dust mask during packing; nitrile gloves; avoid face contact |
| Compressed air release | Depressurise column before disassembly (vent needle valve; confirm ΔP = 0) |
| Column end cap ejection | Confirm all bolts/clips tightened uniformly; never exceed 5 kPa line pressure |
| Activated carbon skin/eye contact | Wash with water; no special first aid required; non-toxic |
| Electrical (Raspberry Pi, 240 V supply) | Standard lab electrical safety; no modifications to mains wiring |

No hazardous gas is used in Phase 16. If HCHO generation is ever needed, it must be performed under a separate approved Phase 17 protocol with full institutional safety review.

---

*See also: `docs/PHASE16_INSTRUMENT_SELECTION.md` for instrument specifications, `docs/PHASE16_PROCUREMENT_PLAN.md` for procurement decisions and build order, `docs/PHASE15_DATA_ACQUISITION_SPEC.md` for the full HCHO-era data schema.*
