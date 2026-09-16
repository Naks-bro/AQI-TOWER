# Phase 17A — Pressure-Drop Analysis Method

**STATUS: BLOCKED — HARDWARE NOT YET AVAILABLE**
**Date: 2026-09-07**

This document describes the analysis method that will be applied once experimental data exist in `RAW_DATA.csv`. It also defines data validity categories and the OpenFOAM translation procedure.

No ΔP values, fitted coefficients, or R² values appear here. All numerical results come from the analysis script after measurements are made.

---

## 1. Input File

`RAW_DATA.csv` — populated by the operator during and after each test run.

Required fields:

| Field | Type | Notes |
|---|---|---|
| `timestamp_utc` | ISO 8601 string | From RPi clock (NTP or RTC) |
| `run_id` | String | Unique per session; e.g., `RUN_P17A_A_001` |
| `stage` | String `A/B/C/D` | A = empty; B = 26 mm; C = 52 mm; D = 104 mm |
| `replicate` | Integer | 1, 2, or 3; each from independent repacking |
| `media_lot` | String | From lot certificate |
| `media_name` | String | `OVC4x8` or `EMPTY` |
| `bed_depth_mm` | float | Measured settled depth before sealing |
| `media_mass_g` | float | Dry mass weighed before packing |
| `column_id_mm` | float | 75.0 for this rig |
| `flow_lpm` | float | Rotameter reading, corrected for T and P |
| `superficial_velocity_ms` | float | Derived from `flow_lpm / (A × 60000)` |
| `temperature_C` | float | SHT40 at column inlet |
| `RH_pct` | float | SHT40 at column inlet |
| `dp_total_Pa` | float | Primary SDP810 reading (or Testo 510 if SDP810 saturated) |
| `dp_empty_Pa` | float | Fixture ΔP at same flow from Stage A (entered by operator) |
| `dp_bed_Pa` | float | `dp_total_Pa − dp_empty_Pa` (operator or post-processing) |
| `dp_secondary_Pa` | float or NaN | Testo 510 reading if available |
| `dp_sdp810_status` | integer | 0 = OK; any other = fault |
| `operator` | String | Name |
| `notes` | String | Alarms, anomalies, events |

---

## 2. Data Validity Categories

Each data point is classified before any averaging or fitting.

### VALID

All of the following are true:
- `dp_sdp810_status == 0`
- `dp_total_Pa < 490 Pa` (SDP810 not at limit) — or secondary instrument used and flagged
- If secondary is present: `|dp_total − dp_secondary| ≤ 3 Pa` or `≤ 5%` (whichever is larger)
- Settled bed depth within ±3 mm of stage target
- No leak, hiss, fines, migration, fluidization noted in `notes`
- Flow CV within 1-minute recording window ≤ 5%

### VALID WITH FLAG (VALID_FLAGGED)

One of the following:
- `dp_total_Pa ≥ 490 Pa` and secondary instrument provides a valid reading in range — use secondary; flag as "SDP810 at limit, Testo 510 used"
- Secondary instrument disagrees by > 3 Pa or > 5% but ≤ 25%: retain primary reading; flag and investigate
- Single note keyword present (e.g., minor vibration, one-off event) that does not indicate structural packing fault

### INVALID

Any of the following:
- `dp_sdp810_status ≠ 0` and secondary not available
- Leak detected during run
- `|dp_total − dp_secondary| > 25%` of primary — instrument fault or connection error
- Bed depth outside ±3 mm of stage target
- Media fines, migration, fluidization, or screen deformation observed
- Flow oscillation ≥ ±5 L/min persisting > 5 minutes after intervention

**Invalid rows are retained in RAW_DATA.csv with their flag. They are excluded from averaging and fitting but reported in the analysis output.**

---

## 3. Analysis Steps

### Step 1 — Stage A: empty-rig fixture baseline

For each velocity point in Stage A:
- Average `dp_total_Pa` over the 1-minute recording window (60 rows)
- Result: `ΔP_fixture(U_s)` table
- Enter `dp_empty_Pa` in session headers of all Stage B/C/D runs at the same flow

### Step 2 — Corrected bed ΔP

For each packed-bed row:

```
dp_bed_Pa = dp_total_Pa − dp_empty_Pa
```

`dp_empty_Pa` is the Stage A fixture value at the nearest target velocity. If the recorded flow differs by more than ±2 L/min from the Stage A flow, note the discrepancy and interpolate linearly.

### Step 3 — ΔP/L

```
dP_over_L = dp_bed_Pa / (bed_depth_mm / 1000)   [Pa/m]
```

### Step 4 — Replicate statistics (per velocity, per stage)

For each (stage, velocity) combination across all valid replicates:
- `mean_dPL` — arithmetic mean of `dP_over_L`
- `SD_dPL` — sample standard deviation
- `CV_dPL` — `SD / mean × 100 %`

QC criterion: CV ≤ 15%. If CV > 15% for any point, flag and investigate before fitting.

### Step 5 — Darcy–Forchheimer fit

Model: `ΔP/L = a·U_s + b·U_s²`

Fitting:
- Use `scipy.optimize.curve_fit` with non-negativity bounds `(0, ∞)` for both a and b
- Fit using replicate-mean `ΔP/L` values at each velocity
- Report 95% confidence intervals from the covariance matrix (t-distribution, n − 2 degrees of freedom)
- Evaluate R² (must be ≥ 0.99 for acceptance)
- Report residuals as percentage of measured value at each point
- Fit separately per bed depth (B, C, D) and attempt a combined fit across all depths

### Step 6 — Combined fit justification

The combined fit (all bed depths, all velocities) is valid if:
- Fitted `a` and `b` from individual depth fits agree within ±20%
- Combined R² ≥ 0.99
- Residuals do not show a systematic trend with bed depth

If the combined fit fails any of these, report per-depth fits as primary results and note that end-effects may be significant.

### Step 7 — Ergun comparison (conditional)

The Ergun comparison is **blocked** until the following inputs are measured or verified from a traceable lot certificate:
- Mean particle diameter `d_p` (mm) — from sieve analysis or lot certificate
- Bed void fraction `ε` — from measured bulk density and known particle density

If these are not available: write **ERGUN COMPARISON BLOCKED — REQUIRED INPUT NOT AVAILABLE**. Do not use literature estimates for `d_p` or `ε`.

If inputs exist, compute:

```
ΔP/L_Ergun = [150·μ·(1−ε)²·U / (ε³·d_p²)] + [1.75·ρ·(1−ε)·U² / (ε³·d_p)]
```

Report as a comparison only. The Darcy–Forchheimer fit from measurements is the primary engineering result.

---

## 4. OpenFOAM Translation

OpenFOAM's `DarcyForchheimer` porous zone model:

```
ΔP/L = μ·d·U + ρ·|U|·f·U
```

where d [m⁻²] and f [m⁻¹] are the zone coefficients.

Translation from measured coefficients:

```
d = a / μ_air    [m⁻²]
f = b / ρ_air    [m⁻¹]
```

| Symbol | Value | Source |
|---|---|---|
| `a` | TBD from measurements | Darcy–Forchheimer fit — this experiment |
| `b` | TBD from measurements | Darcy–Forchheimer fit — this experiment |
| μ_air | 1.849×10⁻⁵ Pa·s | Air at 25 °C |
| ρ_air | 1.184 kg/m³ | Air at 25 °C, 1 atm |
| `d` | `a / 1.849×10⁻⁵` | TBD |
| `f` | `b / 1.184` | TBD |

**Validity boundary:** these coefficients are valid only for:
- This media lot (OVC 4×8, lot number TBD)
- This packing protocol (tamped 20×, settled depth measured)
- This column (75 mm ID)
- This velocity range (0.13–1.05 m/s)
- This ambient condition (~25 °C, ~50 % RH)

Do not extrapolate beyond the tested velocity range. Do not apply these coefficients to a different column, different packing depth, or different GAC lot without re-measurement or explicit justification.

---

## 5. Running the Analysis Script

```
python scripts/analysis/phase17a_analysis.py \
    --csv results/PRESSURE_DROP_PHASE17A/RAW_DATA.csv \
    --out results/PRESSURE_DROP_PHASE17A/
```

The script:
1. Loads `RAW_DATA.csv` (skips `#` comment lines)
2. Validates all required fields
3. Applies validity flags per Section 2
4. Computes Stage A fixture baseline
5. Computes corrected ΔP_bed and ΔP/L per replicate and velocity
6. Fits Darcy–Forchheimer per depth and combined
7. Writes `DARCY_FORCHHEIMER_FIT.json`
8. Generates figures if matplotlib is installed

If the CSV contains no data rows, the script exits cleanly with message "BLOCKED — no measurement data."

---

*See `docs/PHASE17A_PRESSURE_DROP_RESULTS.md` for the full Phase 17A status, experiment checklist, and final decision table.*
