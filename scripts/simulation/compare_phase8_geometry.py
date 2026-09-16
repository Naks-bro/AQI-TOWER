"""Build the Phase 8 comparison dataset and static engineering figure."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/GEOMETRY_OPTIMIZATION"

v01 = json.loads((ROOT / "results/CFD_V01_FAN/metrics.json").read_text(encoding="utf-8"))
v01_diagnosis = json.loads((OUT / "v01_diagnosis.json").read_text(encoding="utf-8"))
records = []


def record(label, metrics, common_reverse):
    return {
        "case": label,
        "flow_m3_h": metrics["fan"]["Q_m3_h"],
        "fan_static_Pa": metrics["fan"]["measured_static_equivalent_Pa"],
        "tower_static_difference_Pa": metrics["pressure_Pa"]["tower_static_difference"],
        "tower_total_pressure_loss_Pa": metrics["pressure_Pa"]["tower_flux_weighted_total_loss"],
        "peak_speed_m_s": metrics["speed_m_s"]["cell_max"],
        "mean_speed_m_s": metrics["speed_m_s"]["volume_mean"],
        "riser_reverse_percent": metrics["regions"]["CLEAN_RISER"]["reverse_volume_fraction"] * 100,
        "common_riser_reverse_percent": common_reverse * 100,
        "clean_plenum_reverse_percent": metrics["regions"]["CLEAN_PLENUM"]["reverse_volume_fraction"] * 100,
        "low_speed_percent": metrics["slow_volume_fraction_below_0p1_m_s"] * 100,
        "riser_entry_CoV": metrics["sections"]["riser_entry_above_turn"]["normal_velocity_CoV"],
        "riser_entry_reverse_area_percent": metrics["sections"]["riser_entry_above_turn"]["reverse_area_fraction"] * 100,
        "stage03_CoV": metrics["sections"]["STAGE_03_mid"]["normal_velocity_CoV"],
        "mass_imbalance_percent": metrics["mass_imbalance_percent"],
        "final_residuals": {name: metrics["last_residuals"][name + "_initial"] for name in ["p", "Ux", "Uy", "Uz", "k", "epsilon"]},
        "criteria": metrics["criteria"],
        "cell_count": metrics["cell_count"],
        "final_iteration": metrics["final_iteration"],
    }


records.append(record("V01", v01, v01_diagnosis["field_findings"]["common_riser_z0p85_to_1p85_reverse_volume_fraction"]))
for case in ["GEO_A", "GEO_B", "GEO_C"]:
    metrics = json.loads((OUT / case / "metrics.json").read_text(encoding="utf-8"))
    records.append(record(case, metrics, metrics["common_riser_window"]["reverse_volume_fraction_Uz_below_minus_0p05"]))
confirm_path = OUT / "GEO_C_CONFIRM/metrics.json"
if confirm_path.exists():
    metrics = json.loads(confirm_path.read_text(encoding="utf-8"))
    records.append(record("GEO_C_CONFIRM", metrics, metrics["common_riser_window"]["reverse_volume_fraction_Uz_below_minus_0p05"]))

(OUT / "comparison_metrics.json").write_text(json.dumps({"records": records}, indent=2), encoding="utf-8")

labels = [row["case"] for row in records if not row["case"].endswith("CONFIRM")]
plot_rows = [row for row in records if not row["case"].endswith("CONFIRM")]
colors = ["#aeb4bc", "#8ab0d4", "#5689bd", "#285f96"]
hatches = ["", "///", "\\\\", "xx"]


def bars(ax, values, title, ylabel, fmt="{:.2f}", ylim=None):
    x = np.arange(len(values))
    artists = ax.bar(x, values, color=colors[:len(values)], edgecolor="#23384d", linewidth=0.7)
    for artist, hatch, value in zip(artists, hatches, values):
        artist.set_hatch(hatch)
        ax.text(artist.get_x() + artist.get_width() / 2, artist.get_height(), fmt.format(value), ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x, labels)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel(ylabel)
    if ylim:
        ax.set_ylim(*ylim)
    else:
        ax.set_ylim(0, max(values) * 1.18 if max(values) else 1)
    ax.grid(axis="y", alpha=0.18)


fig, axes = plt.subplots(2, 4, figsize=(17.0, 8.0), layout="constrained")
bars(axes[0, 0], [row["flow_m3_h"] for row in plot_rows], "Operating airflow", "m³/h", "{:.1f}")
bars(axes[0, 1], [row["tower_total_pressure_loss_Pa"] for row in plot_rows], "Tower total-pressure loss", "Pa", "{:.2f}")
bars(axes[0, 2], [row["tower_static_difference_Pa"] for row in plot_rows], "Inlet–outlet static difference", "Pa", "{:.2f}")
bars(axes[0, 3], [row["peak_speed_m_s"] for row in plot_rows], "Peak cell-centre speed", "m/s", "{:.2f}")

x = np.arange(len(plot_rows))
width = 0.36
full = [row["riser_reverse_percent"] for row in plot_rows]
common = [row["common_riser_reverse_percent"] for row in plot_rows]
axes[1, 0].bar(x - width / 2, full, width, color="#3569a8", edgecolor="#23384d", label="Full CLEAN_RISER")
axes[1, 0].bar(x + width / 2, common, width, color="#c9d9e8", edgecolor="#23384d", hatch="///", label="Common z=0.85–1.85 m")
for xpos, value in zip(x - width / 2, full):
    axes[1, 0].text(xpos, value, f"{value:.1f}", ha="center", va="bottom", fontsize=7)
for xpos, value in zip(x + width / 2, common):
    axes[1, 0].text(xpos, value, f"{value:.1f}", ha="center", va="bottom", fontsize=7)
axes[1, 0].set(xticks=x, xticklabels=labels, ylabel="Volume fraction (%)", title="Riser reverse-flow indicator")
axes[1, 0].set_ylim(0, max(full + common) * 1.23)
axes[1, 0].legend(fontsize=7)
axes[1, 0].grid(axis="y", alpha=0.18)

bars(axes[1, 1], [row["riser_entry_CoV"] for row in plot_rows], "Riser-entry non-uniformity", "Normal-velocity CoV", "{:.3f}")
bars(axes[1, 2], [row["stage03_CoV"] for row in plot_rows], "STAGE_03 non-uniformity", "Normal-velocity CoV", "{:.3f}")
bars(axes[1, 3], [row["low_speed_percent"] for row in plot_rows], "Low-speed fluid volume", "|U| < 0.1 m/s (%)", "{:.2f}")
fig.suptitle("AQI Tower Phase 8 geometry comparison\nActual KVO 250 empty-tower CFD; identical 20 mm maximum cell edge; convergence status reported separately", fontsize=13)
fig.savefig(OUT / "phase8_geometry_comparison.png", dpi=180)
plt.close(fig)

print(json.dumps({"records": records}, indent=2))
