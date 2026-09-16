"""Phase 10B: Generate before/after bypass-seal visualizations.

Compares CASE_M (bypass ~45%) with CASE_M_SEALED (bypass ~0%) using the
same methodology as Phase 10A (phase10a_visualize.py).

Generates:
  results/FILTER_H13/filter_face_bypass_CASE_M_SEALED.png
  results/FILTER_H13/bypass_streamlines_CASE_M_SEALED.png
  results/FILTER_H13/bypass_before_after_CASE_M.png

Usage (in WSL from AQI-TOWER root):
    pvpython --force-offscreen-rendering scripts/simulation/phase10b_visualize.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy.interpolate import griddata

from paraview import servermanager
from paraview.simple import OpenFOAMReader
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkFiltersCore import vtkCellCenters
from vtkmodules.vtkFiltersVerdict import vtkCellSizeFilter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "FILTER_H13"
OUT.mkdir(parents=True, exist_ok=True)

RHO = 1.20
FILTER_X = 0.305
FILTER_Y = (0.1035, 0.6965)
FILTER_Z = (0.2035, 0.7965)
FILTER_AREA = 0.3516

LOG_NAMES = [
    "foamRun_initial.log",
    "foamRun_tight.log",
    "foamRun_baffleRelax005.log",
    "foamRun_baffleRelax005_corrected.log",
    "foamRun_baffleRelax0005.log",
]

print("Phase 10B visualizer starting.", flush=True)

# ---------------------------------------------------------------------------
# Utilities (identical to phase10a)
# ---------------------------------------------------------------------------
def patch_values(path: Path, patch: str, components: int = 1, count: int | None = None) -> np.ndarray:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"\b" + re.escape(patch) + r"\s*\{", text, re.S)
    if not match:
        raise ValueError(f"Patch {patch!r} not found in {path}")
    start, depth, end = match.end(), 1, match.end()
    while depth:
        depth += (text[end] == "{") - (text[end] == "}")
        end += 1
    body = text[start:end - 1]
    values = re.search(r"\bvalue\s+nonuniform\s+List<\w+>\s+(\d+)\s*\((.*?)\)\s*;", body, re.S)
    if values:
        arr = np.fromstring(values[2].replace("(", " ").replace(")", " "), sep=" ")
        return arr.reshape(-1, components) if components > 1 else arr
    values = re.search(r"\bvalue\s+uniform\s+([^;]+);", body)
    if values and count is not None:
        arr = np.fromstring(values[1].replace("(", " ").replace(")", " "), sep=" ")
        return np.tile(arr, (count, 1)) if components > 1 else np.full(count, arr[0])
    raise ValueError(f"Could not parse patch values for {patch!r} in {path}")


def parse_residuals(case: Path) -> list[dict]:
    rows_by_iter: dict[float, dict] = {}
    for name in LOG_NAMES:
        path = case / "logs" / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for segment in re.split(r"\nTime = ", text)[1:]:
            m = re.match(r"[\d.eE+-]+", segment)
            if not m:
                continue
            row: dict = {"iteration": float(m.group())}
            for field, init, _ in re.findall(
                r"Solving for (\w+), Initial residual = ([\d.eE+-]+), Final residual = ([\d.eE+-]+)", segment
            ):
                row[field + "_initial"] = float(init)
            if "p_initial" in row:
                rows_by_iter[row["iteration"]] = row
    return [rows_by_iter[k] for k in sorted(rows_by_iter)]


def leaves(dataset):
    if dataset.IsA("vtkMultiBlockDataSet"):
        for i in range(dataset.GetNumberOfBlocks()):
            blk = dataset.GetBlock(i)
            if blk is not None:
                yield from leaves(blk)
    elif dataset.GetNumberOfCells():
        yield dataset


def load_case(case_name: str, foam_fname: str | None = None):
    case = ROOT / "cfd" / "FILTER_H13" / case_name
    if foam_fname is None:
        foam_fname = f"{case_name}.foam"
    foam_file = case / foam_fname
    times = sorted(
        (p for p in case.iterdir() if p.is_dir() and re.fullmatch(r"\d+", p.name) and int(p.name) > 0),
        key=lambda p: int(p.name),
    )
    final = times[-1]
    print(f"  {case_name}: loading timestep {final.name}", flush=True)

    reader = OpenFOAMReader(FileName=str(foam_file))
    reader.MeshRegions = ["internalMesh"]
    reader.CellArrays = ["U", "p"]
    reader.UpdatePipeline(time=float(final.name))
    grid = list(leaves(servermanager.Fetch(reader)))[0]

    ctr = vtkCellCenters()
    ctr.SetInputData(grid)
    ctr.Update()
    xyz = vtk_to_numpy(ctr.GetOutput().GetPoints().GetData())

    u = vtk_to_numpy(grid.GetCellData().GetArray("U"))
    p = vtk_to_numpy(grid.GetCellData().GetArray("p")) * RHO

    phi_path = final / "phi"
    p_path = final / "p"

    n_fu = 961
    n_fd = 961
    n_out = 325

    q_out = patch_values(phi_path, "AIR_OUTLET", count=n_out)
    q_filter = patch_values(phi_path, "FILTER_UPSTREAM", count=n_fu)
    pf_up_kin = patch_values(p_path, "FILTER_UPSTREAM", count=n_fu)
    pf_down_kin = patch_values(p_path, "FILTER_DOWNSTREAM", count=n_fd)

    return {
        "case": case_name,
        "final_iter": int(final.name),
        "xyz": xyz,
        "u": u,
        "p": p,
        "q_total": float(q_out.sum()),
        "q_filter": float(q_filter.sum()),
        "q_filter_per_face": q_filter,
        "pf_up_Pa": pf_up_kin * RHO,
        "pf_down_Pa": pf_down_kin * RHO,
    }


def load_patch_only(case_name: str):
    case = ROOT / "cfd" / "FILTER_H13" / case_name
    times = sorted(
        (p for p in case.iterdir() if p.is_dir() and re.fullmatch(r"\d+", p.name) and int(p.name) > 0),
        key=lambda p: int(p.name),
    )
    final = times[-1]
    phi_path = final / "phi"
    p_path = final / "p"
    n_fu = 961
    n_fd = 961
    n_out = 325
    q_out = patch_values(phi_path, "AIR_OUTLET", count=n_out)
    q_filter = patch_values(phi_path, "FILTER_UPSTREAM", count=n_fu)
    pf_up = patch_values(p_path, "FILTER_UPSTREAM", count=n_fu) * RHO
    pf_down = patch_values(p_path, "FILTER_DOWNSTREAM", count=n_fd) * RHO
    return {
        "case": case_name,
        "final_iter": int(final.name),
        "q_total": float(q_out.sum()),
        "q_filter": float(q_filter.sum()),
        "q_filter_per_face": q_filter,
        "pf_up_Pa": pf_up,
        "pf_down_Pa": pf_down,
    }


def filter_face_positions():
    ny, nz = 31, 31
    y_vals = np.linspace(FILTER_Y[0] + 0.01, FILTER_Y[1] - 0.01, ny)
    z_vals = np.linspace(FILTER_Z[0] + 0.01, FILTER_Z[1] - 0.01, nz)
    yy, zz = np.meshgrid(y_vals, z_vals)
    return yy.ravel(), zz.ravel()

FY, FZ = filter_face_positions()

# ---------------------------------------------------------------------------
# Load CASE_M_SEALED internal mesh (for spatial figures)
# ---------------------------------------------------------------------------
print("Loading CASE_M_SEALED VTK mesh...", flush=True)
cs = load_case("CASE_M_SEALED", foam_fname="CASE_M_SEALED.foam")
xyz_s, u_s, p_s = cs["xyz"], cs["u"], cs["p"]
speed_s = np.linalg.norm(u_s, axis=1)
print(f"  CASE_M_SEALED loaded: {len(xyz_s)} cells, iter {cs['final_iter']}", flush=True)

# ---------------------------------------------------------------------------
# FIGURE A: Filter face bypass map — CASE_M_SEALED
# ---------------------------------------------------------------------------
print("Generating filter face bypass map (SEALED)...", flush=True)
face_vel_s = cs["q_filter_per_face"] / (FILTER_AREA / 961)   # m/s per face
q_total_s  = abs(cs["q_total"])
q_filter_s = abs(cs["q_filter"])
bypass_s   = 1.0 - q_filter_s / q_total_s

fig, axes = plt.subplots(1, 2, figsize=(11, 5.5), layout="constrained")
vmax_fv = 2.0
sc0 = axes[0].scatter(FY, FZ, c=face_vel_s, cmap="plasma", s=16, marker="s",
                      linewidths=0, vmin=0, vmax=vmax_fv)
plt.colorbar(sc0, ax=axes[0], label="Normal velocity (m/s)")
axes[0].set(xlabel="Y (m)", ylabel="Z (m)", title=f"Filter face velocity\nCASE_M_SEALED iter {cs['final_iter']}")
axes[0].set_aspect("equal")

# Scatter: per-face flow colour by Q fraction (positive = into filter)
sc1 = axes[1].scatter(FY, FZ, c=face_vel_s, cmap="RdYlGn", s=16, marker="s",
                      linewidths=0, vmin=0, vmax=vmax_fv)
plt.colorbar(sc1, ax=axes[1], label="Normal velocity (m/s)")
axes[1].set(xlabel="Y (m)", ylabel="Z (m)",
            title=f"Filter face normal velocity (green = high)\n"
                  f"Q_total={q_total_s * 3600:.0f} m³/h  "
                  f"Q_filter={q_filter_s * 3600:.0f} m³/h  "
                  f"bypass={bypass_s * 100:.1f}%")
axes[1].set_aspect("equal")
fig.suptitle("Phase 10B — Bypass sealed — CASE_M_SEALED\n"
             "SIMULATION — PARTIAL NON-CONVERGED — GEO_C geometry")
fig.savefig(OUT / "filter_face_bypass_CASE_M_SEALED.png", dpi=170)
plt.close(fig)
print("  filter_face_bypass_CASE_M_SEALED.png saved.", flush=True)

# ---------------------------------------------------------------------------
# FIGURE B: Bypass streamlines — CASE_M_SEALED
# ---------------------------------------------------------------------------
print("Generating bypass streamlines (SEALED)...", flush=True)
y_vals_s = np.unique(np.round(xyz_s[:, 1], 8))
y_layer_s = y_vals_s[np.argmin(np.abs(y_vals_s - 0.4))]
mask_s = np.isclose(xyz_s[:, 1], y_layer_s, atol=2e-4)
sx_s, sz_s = xyz_s[mask_s, 0], xyz_s[mask_s, 2]
su_s = u_s[mask_s]
ss_s = speed_s[mask_s]

xi = np.linspace(-0.005, 0.710, 145)
zi = np.linspace(0.10, 1.90, 145)
XX, ZZ = np.meshgrid(xi, zi)
pts = np.column_stack([sx_s, sz_s])

Ux_g = griddata(pts, su_s[:, 0], (XX, ZZ), method="linear")
Uz_g = griddata(pts, su_s[:, 2], (XX, ZZ), method="linear")
Ux_g = np.where(np.isnan(Ux_g), 0.0, Ux_g)
Uz_g = np.where(np.isnan(Uz_g), 0.0, Uz_g)

seed_x = np.full(20, 0.01)
seed_z = np.linspace(0.16, 0.86, 20)
seed_pts = np.column_stack([seed_x, seed_z])

fig, ax = plt.subplots(figsize=(7, 9), layout="constrained")
Ssp = griddata(pts, ss_s, (XX, ZZ), method="linear")
Ssp = np.where(np.isnan(Ssp), 0.0, Ssp)
im = ax.pcolormesh(XX, ZZ, Ssp, cmap="viridis", vmin=0, vmax=7.0, shading="auto")
plt.colorbar(im, ax=ax, label="Speed |U| (m/s)")
ax.streamplot(xi, zi, Ux_g, Uz_g, start_points=seed_pts,
              color="white", linewidth=0.9, arrowsize=0.8, maxlength=3.0)
ax.axvline(FILTER_X, color="#f3e", linestyle="--", linewidth=1.2, label="Filter x=0.305")
ax.axhline(0.850, color="#aaf", linestyle=":", linewidth=1.0, label="z=0.850 m (sealed)")
ax.set(xlabel="X (m)", ylabel="Z (m)", xlim=(-0.01, 0.72), ylim=(0.10, 1.90))
ax.set_aspect("equal")
ax.set_title(f"CASE_M_SEALED — bypass streamlines\ny ≈ {y_layer_s:.3f} m mid-plane  iter {cs['final_iter']}\n"
             f"bypass={bypass_s * 100:.1f}%  Q_filter={q_filter_s * 3600:.0f} m³/h")
ax.legend(loc="upper right", fontsize=8)
fig.savefig(OUT / "bypass_streamlines_CASE_M_SEALED.png", dpi=170)
plt.close(fig)
print("  bypass_streamlines_CASE_M_SEALED.png saved.", flush=True)

# ---------------------------------------------------------------------------
# FIGURE C: Before / after comparison (CASE_M vs CASE_M_SEALED)
# ---------------------------------------------------------------------------
print("Generating before/after comparison figure...", flush=True)

# Load CASE_M patch data
print("  Loading CASE_M patch data...", flush=True)
cm_patch = load_patch_only("CASE_M")
q_total_m  = abs(cm_patch["q_total"])
q_filter_m = abs(cm_patch["q_filter"])
bypass_m   = 1.0 - q_filter_m / q_total_m
dp_m = float(np.mean(cm_patch["pf_up_Pa"]) - np.mean(cm_patch["pf_down_Pa"]))
face_vel_m = cm_patch["q_filter_per_face"] / (FILTER_AREA / 961)
dp_s = float(np.mean(cs["pf_up_Pa"]) - np.mean(cs["pf_down_Pa"]))

fig, axes = plt.subplots(2, 2, figsize=(12, 10), layout="constrained")
vmax_fv = max(face_vel_m.max(), face_vel_s.max()) * 1.05

# Top row: filter face velocity — before (left) and after (right)
sc_m = axes[0, 0].scatter(FY, FZ, c=face_vel_m, cmap="plasma", s=14, marker="s",
                           linewidths=0, vmin=0, vmax=vmax_fv)
plt.colorbar(sc_m, ax=axes[0, 0], label="v_face (m/s)")
axes[0, 0].set(xlabel="Y (m)", ylabel="Z (m)",
               title=f"CASE_M (unsealed)\n"
                     f"Q={q_total_m * 3600:.0f} m³/h  Q_filter={q_filter_m * 3600:.0f} m³/h\n"
                     f"bypass={bypass_m * 100:.1f}%  ΔP_filter={dp_m:.1f} Pa")
axes[0, 0].set_aspect("equal")

sc_s = axes[0, 1].scatter(FY, FZ, c=face_vel_s, cmap="plasma", s=14, marker="s",
                           linewidths=0, vmin=0, vmax=vmax_fv)
plt.colorbar(sc_s, ax=axes[0, 1], label="v_face (m/s)")
axes[0, 1].set(xlabel="Y (m)", ylabel="Z (m)",
               title=f"CASE_M_SEALED\n"
                     f"Q={q_total_s * 3600:.0f} m³/h  Q_filter={q_filter_s * 3600:.0f} m³/h\n"
                     f"bypass={bypass_s * 100:.1f}%  ΔP_filter={dp_s:.1f} Pa")
axes[0, 1].set_aspect("equal")

# Bottom row: residual histories
def plot_residuals(ax, case_path, label, color_base="#3569a8"):
    rows = parse_residuals(case_path)
    if not rows:
        ax.text(0.5, 0.5, "no log data", ha="center", va="center", transform=ax.transAxes)
        return
    for field, ls in [("p", "-"), ("Ux", "--"), ("Uy", ":"), ("Uz", "-.")]:
        key = field + "_initial"
        if key in rows[0]:
            iters = [r["iteration"] for r in rows]
            vals  = [r[key] for r in rows]
            ax.semilogy(iters, vals, linestyle=ls, label=field, linewidth=0.9)
    ax.axhline(1e-5, color="#888", linestyle="--", linewidth=0.7)
    ax.axhline(1e-6, color="#444", linestyle=":",  linewidth=0.7)
    ax.set(xlabel="Iteration", ylabel="Initial residual", title=label)
    ax.grid(alpha=0.2)
    ax.legend(ncol=4, fontsize=7)

plot_residuals(axes[1, 0], ROOT / "cfd" / "FILTER_H13" / "CASE_M",
               "CASE_M residual history")
plot_residuals(axes[1, 1], ROOT / "cfd" / "FILTER_H13" / "CASE_M_SEALED",
               "CASE_M_SEALED residual history")

fig.suptitle("Phase 10B — Bypass seal verification\n"
             "CASE_M (45% bypass) → CASE_M_SEALED\n"
             "SIMULATION — PARTIAL NON-CONVERGED — GEO_C + H13 filter + KVO 250",
             fontsize=11)
fig.savefig(OUT / "bypass_before_after_CASE_M.png", dpi=170)
plt.close(fig)
print("  bypass_before_after_CASE_M.png saved.", flush=True)

# ---------------------------------------------------------------------------
# Write sealed bypass_analysis supplement
# ---------------------------------------------------------------------------
print("Writing bypass_analysis_sealed.json...", flush=True)
sealed_data = {
    "CASE_M_SEALED": {
        "final_iteration": cs["final_iter"],
        "total_flow_m3_s": q_total_s,
        "total_flow_m3_h": q_total_s * 3600,
        "filter_flow_m3_s": q_filter_s,
        "filter_flow_m3_h": q_filter_s * 3600,
        "bypass_flow_m3_s": q_total_s - q_filter_s,
        "bypass_flow_m3_h": (q_total_s - q_filter_s) * 3600,
        "bypass_fraction": bypass_s,
        "effective_filtered_fraction": 1.0 - bypass_s,
        "filter_face_velocity_m_s": {
            "mean": float(np.mean(face_vel_s)),
            "min":  float(np.min(face_vel_s)),
            "max":  float(np.max(face_vel_s)),
            "p10":  float(np.percentile(face_vel_s, 10)),
            "p90":  float(np.percentile(face_vel_s, 90)),
            "CoV":  float(np.std(face_vel_s) / np.mean(face_vel_s)),
            "reverse_area_fraction": float(np.mean(face_vel_s < 0)),
        },
        "filter_delta_P_area_mean_Pa": dp_s,
        "resistance_multiplier": 1.0,
        "scenario_classification": "SINGLE-POINT CALIBRATED APPROXIMATION",
        "bypass_seal": "applied — bypassSeal plate baffle at z=0.850 m, x=0.260–0.305 m",
    },
    "comparison": {
        "CASE_M_bypass_fraction": bypass_m,
        "CASE_M_SEALED_bypass_fraction": bypass_s,
        "bypass_reduction_pct_points": (bypass_m - bypass_s) * 100,
        "CASE_M_Q_filter_m3_h": q_filter_m * 3600,
        "CASE_M_SEALED_Q_filter_m3_h": q_filter_s * 3600,
        "filter_flow_increase_fraction": (q_filter_s - q_filter_m) / q_filter_m,
        "CASE_M_delta_P_Pa": dp_m,
        "CASE_M_SEALED_delta_P_Pa": dp_s,
    },
    "method": "FILTER_UPSTREAM phi sum vs AIR_OUTLET phi sum",
    "note": (
        "bypass_fraction = 1 - Q_FILTER_UPSTREAM / Q_AIR_OUTLET. "
        "bypassSeal plate baffle added at z=0.850 m, x=0.260-0.305 m, y=0.150-0.650 m "
        "to block the open dirty-to-clean connection at the dirty-plenum/clean-riser junction."
    ),
}
(OUT / "bypass_analysis_sealed.json").write_text(
    json.dumps(sealed_data, indent=2, ensure_ascii=False), encoding="utf-8"
)
print("  bypass_analysis_sealed.json saved.", flush=True)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print(f"\n=== Phase 10B results ===", flush=True)
print(f"CASE_M       : bypass={bypass_m * 100:.1f}%  Q_filter={q_filter_m * 3600:.0f} m³/h  ΔP={dp_m:.1f} Pa", flush=True)
print(f"CASE_M_SEALED: bypass={bypass_s * 100:.1f}%  Q_filter={q_filter_s * 3600:.0f} m³/h  ΔP={dp_s:.1f} Pa", flush=True)
print(f"Bypass reduction: {(bypass_m - bypass_s) * 100:.1f} percentage points", flush=True)
print(f"Filter flow increase: {(q_filter_s - q_filter_m) / q_filter_m * 100:.0f}%", flush=True)
if bypass_s < 0.02:
    print("PASS: bypass < 2% target met.", flush=True)
else:
    print(f"WARNING: bypass {bypass_s * 100:.1f}% exceeds 2% target.", flush=True)
print("\nOutputs written to results/FILTER_H13/:", flush=True)
for f in ["filter_face_bypass_CASE_M_SEALED.png", "bypass_streamlines_CASE_M_SEALED.png",
          "bypass_before_after_CASE_M.png", "bypass_analysis_sealed.json"]:
    print(f"  {f}", flush=True)
