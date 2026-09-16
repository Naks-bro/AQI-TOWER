#!/usr/bin/env python3
"""
Phase 17A — Clean-Air Pressure-Drop Analysis
AQI-TOWER Project

Reads RAW_DATA.csv from the Phase 17A pressure-drop experiment, applies data
validity flags, computes fixture-corrected bed ΔP for each replicate, fits the
Darcy–Forchheimer model, and writes DARCY_FORCHHEIMER_FIT.json.  Generates
plots if matplotlib is available.

Usage:
    python phase17a_analysis.py \\
        --csv  results/PRESSURE_DROP_PHASE17A/RAW_DATA.csv \\
        --out  results/PRESSURE_DROP_PHASE17A/

Requirements:
    numpy  (mandatory for fitting)
    scipy  (mandatory for curve_fit and confidence intervals)
    matplotlib  (optional — skipped if not installed)

Install:
    pip install numpy scipy matplotlib
"""

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ── optional imports ──────────────────────────────────────────────────────────
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("WARNING: numpy not found. Fitting disabled.", file=sys.stderr)

try:
    from scipy.optimize import curve_fit
    from scipy.stats import t as t_dist
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("WARNING: scipy not found. Fitting disabled.", file=sys.stderr)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("INFO: matplotlib not found. Plots will be skipped.", file=sys.stderr)


# ── constants ─────────────────────────────────────────────────────────────────
COLUMN_ID_MM   = 75.0
COLUMN_AREA_M2 = math.pi * (COLUMN_ID_MM / 1000.0) ** 2 / 4.0   # 4.418e-3 m²

MU_AIR_25C  = 1.849e-5   # Pa·s  — dynamic viscosity of air at 25 °C
RHO_AIR_25C = 1.184      # kg/m³ — density of air at 25 °C, 1 atm

CV_MAX_WITHIN_RUN  = 0.05   # 5 % — ΔP CV within a 1-min recording window
CV_MAX_REPLICATES  = 0.15   # 15 % — ΔP/L CV across independent repacks
DP_SDP810_LIMIT_PA = 490.0  # Pa — SDP810 reading above this = flag
BED_DEPTH_TOL_MM   = 3.0    # mm — settled depth tolerance from target

TARGET_DEPTHS_MM = {"B": 26.0, "C": 52.0, "D": 104.0}
TARGET_VELOCITIES_MS = [0.13, 0.26, 0.52, 0.80, 1.05]

REQUIRED_FIELDS = [
    "timestamp_utc", "run_id", "stage", "replicate",
    "media_lot", "media_name", "bed_depth_mm", "media_mass_g",
    "column_id_mm", "flow_lpm", "superficial_velocity_ms",
    "temperature_C", "RH_pct",
    "dp_total_Pa", "dp_empty_Pa", "dp_bed_Pa", "dp_secondary_Pa",
    "dp_sdp810_status", "operator", "notes",
]


# ── data validity rules ───────────────────────────────────────────────────────
# Applied to each averaged point (not individual 1-s rows).
# Returns: "VALID" | "VALID_FLAGGED" | "INVALID", reason string

def assess_validity(row: dict) -> tuple[str, str]:
    reasons = []
    invalid = False

    try:
        dp_total  = float(row["dp_total_Pa"])
        dp_sec    = row["dp_secondary_Pa"]
        status    = int(float(row.get("dp_sdp810_status", 0)))
        depth     = float(row["bed_depth_mm"])
        stage     = row["stage"].strip().upper()
        notes     = row.get("notes", "").lower()
    except (ValueError, KeyError) as exc:
        return "INVALID", f"parse error: {exc}"

    # Sensor fault — automatic INVALID
    if status != 0:
        invalid = True
        reasons.append(f"SDP810 status={status} (fault)")

    # SDP810 saturation flag
    if dp_total >= DP_SDP810_LIMIT_PA:
        reasons.append(f"dp_total={dp_total:.1f} Pa >= {DP_SDP810_LIMIT_PA} Pa — SDP810 at limit; use secondary if available")

    # Secondary instrument disagreement
    if dp_sec and dp_sec.strip() not in ("", "NaN", "nan", "N/A"):
        try:
            dp_s = float(dp_sec)
            diff = abs(dp_total - dp_s)
            pct  = diff / max(abs(dp_total), 1.0) * 100.0
            if diff > 3.0 and pct > 5.0:
                reasons.append(f"Instrument disagreement: primary={dp_total:.1f} Pa, secondary={dp_s:.1f} Pa, diff={diff:.1f} Pa ({pct:.1f}%)")
                if pct > 25.0:
                    invalid = True
                    reasons[-1] += " — EXCEEDS 25 %; INVALID"
        except ValueError:
            pass

    # Bed depth tolerance check for packed stages
    if stage in TARGET_DEPTHS_MM:
        target = TARGET_DEPTHS_MM[stage]
        if abs(depth - target) > BED_DEPTH_TOL_MM:
            invalid = True
            reasons.append(
                f"Bed depth {depth:.1f} mm outside {target}±{BED_DEPTH_TOL_MM} mm tolerance"
            )

    # Keywords in notes that flag problems
    bad_keywords = ["leak", "hiss", "fines", "migrat", "fluidiz", "unstable", "fault"]
    for kw in bad_keywords:
        if kw in notes:
            reasons.append(f'Note contains "{kw}"')
            invalid = True

    if invalid:
        return "INVALID", "; ".join(reasons) if reasons else "see notes"
    if reasons:
        return "VALID_FLAGGED", "; ".join(reasons)
    return "VALID", ""


# ── Darcy–Forchheimer model ───────────────────────────────────────────────────

def darcy_forchheimer(U, a, b):
    """ΔP/L = a·U + b·U²"""
    return a * U + b * U ** 2


def fit_darcy_forchheimer(U_arr, dPL_arr, label=""):
    """
    Fit ΔP/L = a·U + b·U² with a ≥ 0, b ≥ 0.
    Returns dict with a, b, CI, R², residuals.
    """
    if not (HAS_NUMPY and HAS_SCIPY):
        return {"error": "numpy/scipy not available"}

    n = len(U_arr)
    if n < 3:
        return {"error": f"insufficient data ({n} points, need ≥ 3)"}

    try:
        popt, pcov = curve_fit(
            darcy_forchheimer,
            U_arr, dPL_arr,
            p0=[500.0, 2000.0],
            bounds=(0.0, np.inf),
            maxfev=10000,
        )
    except Exception as exc:
        return {"error": f"curve_fit failed: {exc}"}

    a, b = float(popt[0]), float(popt[1])
    perr = np.sqrt(np.diag(pcov))

    dof    = n - 2
    t_crit = float(t_dist.ppf(0.975, dof)) if dof > 0 else float("nan")
    a_ci   = float(perr[0] * t_crit)
    b_ci   = float(perr[1] * t_crit)

    fitted    = darcy_forchheimer(U_arr, a, b)
    residuals = dPL_arr - fitted
    ss_res    = float(np.sum(residuals ** 2))
    ss_tot    = float(np.sum((dPL_arr - np.mean(dPL_arr)) ** 2))
    r2        = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    residuals_pct = (residuals / np.maximum(np.abs(dPL_arr), 1.0) * 100.0).tolist()

    return {
        "label":              label,
        "n_observations":     n,
        "a_Pa_s_m2":          round(a, 2),
        "a_95CI_Pa_s_m2":     round(a_ci, 2),
        "b_Pa_s2_m3":         round(b, 2),
        "b_95CI_Pa_s2_m3":    round(b_ci, 2),
        "R2":                 round(r2, 6),
        "residuals_pct":      [round(r, 2) for r in residuals_pct],
        "velocity_range_ms":  [round(float(U_arr.min()), 3), round(float(U_arr.max()), 3)],
        "fit_valid":          r2 >= 0.99 and a > 0 and b > 0,
        "openfoam": {
            "d_m2":        round(a / MU_AIR_25C, 2),
            "f_m1":        round(b / RHO_AIR_25C, 4),
            "mu_air_Pa_s": MU_AIR_25C,
            "rho_air_kg_m3": RHO_AIR_25C,
            "note": (
                "ΔP/L = μ·d·U + ρ·f·U² in OpenFOAM DarcyForchheimer model. "
                "Valid only for this lot, this column, this packing protocol, and this velocity range."
            ),
        },
    }


# ── CSV loading ───────────────────────────────────────────────────────────────

def load_csv(path: Path) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                continue   # skip session header comment lines
            break          # first non-comment line is the CSV header
        # Re-open to use DictReader from the first non-comment line
    with open(path, newline="", encoding="utf-8") as fh:
        non_comment = (ln for ln in fh if not ln.startswith("#"))
        reader = csv.DictReader(non_comment)
        for row in reader:
            rows.append(row)
    return rows


def validate_fields(rows: list[dict]) -> list[str]:
    if not rows:
        return []
    missing = [f for f in REQUIRED_FIELDS if f not in rows[0]]
    return missing


# ── statistics helpers ────────────────────────────────────────────────────────

def mean_sd_cv(values: list[float]) -> tuple[float, float, float]:
    if not values:
        return float("nan"), float("nan"), float("nan")
    n  = len(values)
    mu = sum(values) / n
    if n == 1:
        return mu, 0.0, 0.0
    sd = math.sqrt(sum((x - mu) ** 2 for x in values) / (n - 1))
    cv = sd / mu if mu != 0 else float("nan")
    return mu, sd, cv


# ── main analysis ─────────────────────────────────────────────────────────────

def analyse(csv_path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = load_csv(csv_path)

    if not rows:
        print("No data rows found in CSV. Phase 17A is BLOCKED — no measurements yet.")
        return {"status": "BLOCKED", "reason": "CSV contains no data rows"}

    missing = validate_fields(rows)
    if missing:
        print(f"ERROR: CSV missing required fields: {missing}")
        return {"status": "ERROR", "missing_fields": missing}

    print(f"Loaded {len(rows)} rows from {csv_path}")

    # ── validity flags ──────────────────────────────────────────────────────
    for row in rows:
        v, reason = assess_validity(row)
        row["__validity"] = v
        row["__validity_reason"] = reason

    valid_rows   = [r for r in rows if r["__validity"] != "INVALID"]
    invalid_rows = [r for r in rows if r["__validity"] == "INVALID"]
    flagged_rows = [r for r in rows if r["__validity"] == "VALID_FLAGGED"]

    print(f"  VALID:         {len([r for r in rows if r['__validity'] == 'VALID'])}")
    print(f"  VALID_FLAGGED: {len(flagged_rows)}")
    print(f"  INVALID:       {len(invalid_rows)}")

    # ── Stage A fixture baseline ────────────────────────────────────────────
    stage_a = [r for r in valid_rows if r["stage"].strip().upper() == "A"]

    # Group by target velocity; average dp_total_Pa over each group
    fixture_by_velocity: dict[float, list[float]] = defaultdict(list)
    for r in stage_a:
        try:
            U   = float(r["superficial_velocity_ms"])
            dp  = float(r["dp_total_Pa"])
            fixture_by_velocity[round(U, 3)].append(dp)
        except ValueError:
            continue

    fixture_dp: dict[float, float] = {}
    for U, vals in fixture_by_velocity.items():
        mu, sd, cv = mean_sd_cv(vals)
        fixture_dp[U] = mu
        print(f"  Stage A  U={U:.2f} m/s: ΔP_fixture={mu:.2f} Pa  SD={sd:.2f}  CV={cv*100:.1f}%")

    # ── Stages B / C / D ───────────────────────────────────────────────────
    # Group: stage → replicate → target_velocity → list of dp_bed_Pa
    results: dict = {}   # stage → list of replicate summary dicts

    for stage_key in ("B", "C", "D"):
        stage_rows = [r for r in valid_rows if r["stage"].strip().upper() == stage_key]
        if not stage_rows:
            results[stage_key] = {"status": "NO_DATA"}
            continue

        # Sub-group by replicate
        rep_groups: dict[int, list] = defaultdict(list)
        for r in stage_rows:
            try:
                rep = int(float(r["replicate"]))
                rep_groups[rep].append(r)
            except ValueError:
                continue

        rep_summaries = []
        for rep_id in sorted(rep_groups.keys()):
            rep_rows = rep_groups[rep_id]

            # Group by velocity within replicate
            vel_groups: dict[float, list[float]] = defaultdict(list)
            for r in rep_rows:
                try:
                    U  = float(r["superficial_velocity_ms"])
                    dp = float(r["dp_bed_Pa"])
                    vel_groups[round(U, 3)].append(dp)
                except ValueError:
                    continue

            # Gather metadata from first row
            first = rep_rows[0]
            try:
                depth_mm = float(first["bed_depth_mm"])
                mass_g   = float(first["media_mass_g"])
                vol_mL   = COLUMN_AREA_M2 * (depth_mm / 1000.0) * 1e6  # mL
                bulk_density = (mass_g / vol_mL) * 1000.0              # kg/m³
            except (ValueError, ZeroDivisionError):
                depth_mm = float("nan")
                mass_g   = float("nan")
                vol_mL   = float("nan")
                bulk_density = float("nan")

            velocity_results = []
            for U in sorted(vel_groups.keys()):
                vals = vel_groups[U]
                mu_dp, sd_dp, cv_dp = mean_sd_cv(vals)
                dPL = mu_dp / (depth_mm / 1000.0) if depth_mm > 0 else float("nan")
                velocity_results.append({
                    "U_ms":     round(U, 3),
                    "n":        len(vals),
                    "dp_bed_mean_Pa": round(mu_dp, 2),
                    "dp_bed_sd_Pa":   round(sd_dp, 2),
                    "dp_bed_cv_pct":  round(cv_dp * 100.0, 2),
                    "dPL_Pa_m":       round(dPL, 2),
                    "qc_within_run":  "PASS" if cv_dp <= CV_MAX_WITHIN_RUN else "FAIL",
                })

            rep_summaries.append({
                "replicate":           rep_id,
                "bed_depth_mm":        round(depth_mm, 2),
                "media_mass_g":        round(mass_g, 2),
                "bed_volume_mL":       round(vol_mL, 2),
                "bulk_density_kg_m3":  round(bulk_density, 1),
                "media_lot":           first.get("media_lot", ""),
                "velocity_points":     velocity_results,
            })

        results[stage_key] = {"replicates": rep_summaries}

        # Cross-replicate scatter for each velocity
        print(f"\nStage {stage_key} — cross-replicate summary:")
        all_velocities = sorted(set(
            vp["U_ms"]
            for rs in rep_summaries
            for vp in rs["velocity_points"]
        ))
        for U in all_velocities:
            dPL_vals = [
                vp["dPL_Pa_m"]
                for rs in rep_summaries
                for vp in rs["velocity_points"]
                if vp["U_ms"] == U and not math.isnan(vp["dPL_Pa_m"])
            ]
            if not dPL_vals:
                continue
            mu, sd, cv = mean_sd_cv(dPL_vals)
            qc = "PASS" if cv <= CV_MAX_REPLICATES else "FAIL"
            print(f"  U={U:.2f} m/s: ΔP/L mean={mu:.1f} Pa/m  SD={sd:.1f}  CV={cv*100:.1f}%  [{qc}]")

    # ── Darcy–Forchheimer fitting ───────────────────────────────────────────
    fits: dict = {}
    if HAS_NUMPY and HAS_SCIPY:
        all_U_combined  = []
        all_dPL_combined = []

        for stage_key in ("B", "C", "D"):
            stage_result = results.get(stage_key, {})
            if "replicates" not in stage_result:
                fits[stage_key] = {"status": "NO_DATA"}
                continue

            rep_summaries = stage_result["replicates"]
            target_depth  = TARGET_DEPTHS_MM.get(stage_key, None)

            # Collect mean ΔP/L per velocity (over all replicates)
            vel_dPL: dict[float, list[float]] = defaultdict(list)
            for rs in rep_summaries:
                depth = rs["bed_depth_mm"]
                for vp in rs["velocity_points"]:
                    if not math.isnan(vp["dPL_Pa_m"]) and vp["qc_within_run"] == "PASS":
                        vel_dPL[vp["U_ms"]].append(vp["dPL_Pa_m"])

            if not vel_dPL:
                fits[stage_key] = {"status": "NO_VALID_DATA"}
                continue

            # Mean across replicates
            U_list   = sorted(vel_dPL.keys())
            dPL_list = [sum(vel_dPL[U]) / len(vel_dPL[U]) for U in U_list]

            U_arr   = np.array(U_list)
            dPL_arr = np.array(dPL_list)

            fit_result = fit_darcy_forchheimer(U_arr, dPL_arr, label=f"Stage {stage_key}")
            fits[stage_key] = fit_result

            all_U_combined.extend(U_list)
            all_dPL_combined.extend(dPL_list)

        # Combined fit across all depths (if justified)
        if all_U_combined:
            combined_fit = fit_darcy_forchheimer(
                np.array(all_U_combined),
                np.array(all_dPL_combined),
                label="Combined (all depths)",
            )
            fits["combined"] = combined_fit
        else:
            fits["combined"] = {"status": "NO_DATA"}
    else:
        fits = {"error": "numpy/scipy not available — fitting skipped"}

    # ── write JSON output ───────────────────────────────────────────────────
    output = {
        "metadata": {
            "analysis_date":    datetime.utcnow().isoformat(),
            "source_csv":       str(csv_path),
            "script":           "scripts/analysis/phase17a_analysis.py",
            "phase":            "17A",
            "column_id_mm":     COLUMN_ID_MM,
            "column_area_m2":   round(COLUMN_AREA_M2, 8),
            "mu_air_Pa_s":      MU_AIR_25C,
            "rho_air_kg_m3":    RHO_AIR_25C,
        },
        "row_counts": {
            "total":        len(rows),
            "valid":        len([r for r in rows if r["__validity"] == "VALID"]),
            "valid_flagged": len(flagged_rows),
            "invalid":      len(invalid_rows),
        },
        "stage_A_fixture": {
            "dp_fixture_by_velocity_Pa": {
                str(round(U, 3)): round(dp, 2)
                for U, dp in sorted(fixture_dp.items())
            },
        },
        "stage_results": {
            stage: {
                k: v for k, v in data.items() if k != "replicates"
            } if "replicates" not in data else {
                "replicates": data["replicates"]
            }
            for stage, data in results.items()
        },
        "darcy_forchheimer_fits": fits,
        "validity_summary": {
            "invalid_run_ids": [r.get("run_id", "") for r in invalid_rows],
            "flagged_run_ids": [r.get("run_id", "") for r in flagged_rows],
        },
    }

    json_path = out_dir / "DARCY_FORCHHEIMER_FIT.json"
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2)
    print(f"\nWrote {json_path}")

    # ── plots ───────────────────────────────────────────────────────────────
    if HAS_MATPLOTLIB and fixture_dp:
        _plot_fixture(fixture_dp, out_dir)
    if HAS_MATPLOTLIB:
        _plot_bed_pressure_drop(results, out_dir)
        _plot_darcy_forchheimer(results, fits, out_dir)

    return output


# ── plotting helpers ──────────────────────────────────────────────────────────

def _plot_fixture(fixture_dp: dict, out_dir: Path):
    U   = sorted(fixture_dp.keys())
    dP  = [fixture_dp[u] for u in U]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(U, dP, "ko-", linewidth=1.5, markersize=6)
    ax.set_xlabel("Superficial velocity U_s  (m/s)")
    ax.set_ylabel("ΔP_fixture  (Pa)")
    ax.set_title("Stage A — Empty-column fixture pressure loss")
    ax.grid(True, linewidth=0.4)
    fig.tight_layout()
    fig.savefig(out_dir / "stage_A_fixture_dp.png", dpi=150)
    plt.close(fig)
    print("  Plot: stage_A_fixture_dp.png")


def _plot_bed_pressure_drop(results: dict, out_dir: Path):
    fig, ax = plt.subplots(figsize=(8, 5))
    markers = {"B": "s", "C": "^", "D": "o"}
    colors  = {"B": "#1f77b4", "C": "#ff7f0e", "D": "#2ca02c"}
    labels  = {"B": "26 mm bed", "C": "52 mm bed", "D": "104 mm bed"}

    for stage_key in ("B", "C", "D"):
        if "replicates" not in results.get(stage_key, {}):
            continue
        for rs in results[stage_key]["replicates"]:
            U_vals  = [vp["U_ms"]         for vp in rs["velocity_points"]]
            dP_vals = [vp["dp_bed_mean_Pa"] for vp in rs["velocity_points"]]
            ax.plot(U_vals, dP_vals, marker=markers[stage_key],
                    color=colors[stage_key], alpha=0.6, linewidth=1.0,
                    label=labels[stage_key] if rs["replicate"] == 1 else "")

    handles, lbls = ax.get_legend_handles_labels()
    seen = set()
    unique = [(h, l) for h, l in zip(handles, lbls) if l not in seen and not seen.add(l)]
    ax.legend(*zip(*unique) if unique else ([], []))
    ax.set_xlabel("Superficial velocity U_s  (m/s)")
    ax.set_ylabel("ΔP_bed  (Pa)")
    ax.set_title("ΔP_bed vs U_s — all replicates (fixture-corrected)")
    ax.grid(True, linewidth=0.4)
    fig.tight_layout()
    fig.savefig(out_dir / "dp_bed_vs_velocity.png", dpi=150)
    plt.close(fig)
    print("  Plot: dp_bed_vs_velocity.png")


def _plot_darcy_forchheimer(results: dict, fits: dict, out_dir: Path):
    fig, ax = plt.subplots(figsize=(8, 5))
    colors  = {"B": "#1f77b4", "C": "#ff7f0e", "D": "#2ca02c"}
    labels  = {"B": "26 mm", "C": "52 mm", "D": "104 mm"}

    for stage_key in ("B", "C", "D"):
        if "replicates" not in results.get(stage_key, {}):
            continue
        depth_mm = TARGET_DEPTHS_MM.get(stage_key, 1.0)
        for rs in results[stage_key]["replicates"]:
            U_vals   = [vp["U_ms"]     for vp in rs["velocity_points"]]
            dPL_vals = [vp["dPL_Pa_m"] for vp in rs["velocity_points"]]
            ax.scatter(U_vals, dPL_vals, color=colors[stage_key], alpha=0.5, s=30,
                       label=labels[stage_key] if rs["replicate"] == 1 else "")

        # Overlay fitted curve
        fit = fits.get(stage_key, {})
        if "a_Pa_s_m2" in fit and HAS_NUMPY:
            U_line  = np.linspace(0.05, 1.15, 100)
            dPL_fit = fit["a_Pa_s_m2"] * U_line + fit["b_Pa_s2_m3"] * U_line ** 2
            ax.plot(U_line, dPL_fit, color=colors[stage_key], linewidth=2,
                    linestyle="--", label=f"{labels[stage_key]} fit (R²={fit['R2']:.4f})")

    handles, lbls = ax.get_legend_handles_labels()
    seen = set()
    unique = [(h, l) for h, l in zip(handles, lbls) if l not in seen and not seen.add(l)]
    if unique:
        ax.legend(*zip(*unique))
    ax.set_xlabel("Superficial velocity U_s  (m/s)")
    ax.set_ylabel("ΔP_bed / L  (Pa/m)")
    ax.set_title("Darcy–Forchheimer fit — ΔP/L vs U_s")
    ax.grid(True, linewidth=0.4)
    fig.tight_layout()
    fig.savefig(out_dir / "darcy_forchheimer_fit.png", dpi=150)
    plt.close(fig)
    print("  Plot: darcy_forchheimer_fit.png")


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Phase 17A pressure-drop analysis")
    parser.add_argument("--csv",  required=True, help="Path to RAW_DATA.csv")
    parser.add_argument("--out",  required=True, help="Output directory")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    out_dir  = Path(args.out)

    if not csv_path.exists():
        print(f"ERROR: CSV not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    result = analyse(csv_path, out_dir)

    if result.get("status") == "BLOCKED":
        print("\nPhase 17A is BLOCKED — no measurement data in CSV.")
        print("Populate RAW_DATA.csv with experimental readings and re-run this script.")
        sys.exit(0)

    fits = result.get("darcy_forchheimer_fits", {})
    combined = fits.get("combined", {})
    if "a_Pa_s_m2" in combined:
        print("\n── Combined Darcy–Forchheimer result ──────────────────────")
        print(f"  a = {combined['a_Pa_s_m2']:.2f} ± {combined['a_95CI_Pa_s_m2']:.2f} Pa·s/m²")
        print(f"  b = {combined['b_Pa_s2_m3']:.2f} ± {combined['b_95CI_Pa_s2_m3']:.2f} Pa·s²/m³")
        print(f"  R² = {combined['R2']:.6f}")
        ofc = combined.get("openfoam", {})
        if ofc.get("d_m2") is not None:
            print(f"  OpenFOAM d = {ofc['d_m2']:.2f} m⁻²")
            print(f"  OpenFOAM f = {ofc['f_m1']:.4f} m⁻¹")
    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
