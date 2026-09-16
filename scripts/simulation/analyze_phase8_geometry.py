"""Extract actual Phase 8 CFD metrics using the V01 definitions.

Usage: pvpython --force-offscreen-rendering analyze_phase8_geometry.py GEO_A
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from paraview import servermanager
from paraview.simple import OpenFOAMReader
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkCellCenters, vtkCutter
from vtkmodules.vtkFiltersVerdict import vtkCellSizeFilter


ROOT = Path(__file__).resolve().parents[2]
CASE_NAME = sys.argv[1] if len(sys.argv) > 1 else "GEO_A"
CASE = ROOT / "cfd" / CASE_NAME
OUT = ROOT / "results" / "GEOMETRY_OPTIMIZATION" / CASE_NAME
OUT.mkdir(parents=True, exist_ok=True)
RHO = 1.20


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def patch_values(path, patch, components=1, count=None):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"\b" + re.escape(patch) + r"\s*\{", text, re.S)
    if not match:
        raise ValueError(f"Missing patch {patch} in {path}")
    start, depth, end = match.end(), 1, match.end()
    while depth:
        depth += (text[end] == "{") - (text[end] == "}")
        end += 1
    body = text[start:end - 1]
    values = re.search(r"\bvalue\s+nonuniform\s+List<\w+>\s+(\d+)\s*\((.*?)\)\s*;", body, re.S)
    if values:
        array = np.fromstring(values[2].replace("(", " ").replace(")", " "), sep=" ")
        if array.size != int(values[1]) * components:
            raise RuntimeError(f"Unexpected value count for {patch} in {path}")
        return array.reshape(-1, components) if components > 1 else array
    values = re.search(r"\bvalue\s+uniform\s+([^;]+);", body)
    if values and count is not None:
        array = np.fromstring(values[1].replace("(", " ").replace(")", " "), sep=" ")
        if array.size != components:
            raise RuntimeError(f"Unexpected uniform value for {patch} in {path}")
        return np.tile(array, (count, 1)) if components > 1 else np.full(count, array[0])
    raise ValueError(f"Missing explicit patch values for {patch} in {path}")


def leaves(dataset):
    if dataset.IsA("vtkMultiBlockDataSet"):
        for index in range(dataset.GetNumberOfBlocks()):
            block = dataset.GetBlock(index)
            if block is not None:
                yield from leaves(block)
    elif dataset.GetNumberOfCells():
        yield dataset


def sizes(dataset, array):
    algorithm = vtkCellSizeFilter()
    algorithm.SetInputData(dataset)
    algorithm.Update()
    return vtk_to_numpy(algorithm.GetOutput().GetCellData().GetArray(array))


logs = []
for name in ["foamRun_initial.log", "foamRun_tight.log"]:
    path = CASE / "logs" / name
    if path.exists():
        logs.append(path.read_text(encoding="utf-8", errors="replace"))
log = "\n".join(logs)
if not logs or not re.search(r"\nEnd\s*$", logs[-1]):
    raise RuntimeError(f"{CASE_NAME}: final solver log did not end cleanly")

rows = []
for segment in re.split(r"\nTime = ", log)[1:]:
    time_match = re.match(r"[\d.eE+-]+", segment)
    if not time_match:
        continue
    row = {"iteration": float(time_match.group())}
    for field, initial, linear_final in re.findall(
        r"Solving for (\w+), Initial residual = ([\d.eE+-]+), Final residual = ([\d.eE+-]+)", segment
    ):
        row[field + "_initial"] = float(initial)
        row[field + "_linear_final"] = float(linear_final)
    continuity = re.search(
        r"continuity errors : sum local = ([\d.eE+-]+), global = ([\d.eE+-]+), cumulative = ([\d.eE+-]+)", segment
    )
    if continuity:
        row.update(dict(zip(["continuity_local", "continuity_global", "continuity_cumulative"], map(float, continuity.groups()))))
    if "p_initial" in row:
        rows.append(row)
if not rows:
    raise RuntimeError(f"{CASE_NAME}: no solved iterations found")
columns = list(rows[0])
with (OUT / "residuals.csv").open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

times = sorted(
    (path for path in CASE.iterdir() if path.is_dir() and re.fullmatch(r"\d+(?:\.\d+)?", path.name) and float(path.name) > 0),
    key=lambda path: float(path.name),
)
final = times[-1]
foam_file = CASE / f"{CASE_NAME}.foam"
reader = OpenFOAMReader(FileName=str(foam_file))
reader.MeshRegions = ["internalMesh"]
reader.CellArrays = ["U", "p", "k", "epsilon", "nut"]
reader.UpdatePipeline(time=float(final.name))
grid = list(leaves(servermanager.Fetch(reader)))[0]
vol = sizes(grid, "Volume")
u = vtk_to_numpy(grid.GetCellData().GetArray("U"))
p_pa = vtk_to_numpy(grid.GetCellData().GetArray("p")) * RHO
speed = np.linalg.norm(u, axis=1)
centres = vtkCellCenters()
centres.SetInputData(grid)
centres.Update()
xyz = vtk_to_numpy(centres.GetOutput().GetPoints().GetData())
audit = json.loads((CASE / "geometry_audit.json").read_text(encoding="utf-8"))
if abs(vol.sum() - audit["fluid_volume_m3"]) > 1e-7 or len(vol) != audit["total_cells"]:
    raise RuntimeError(f"{CASE_NAME}: VTK mesh does not match audit")

patch_reader = OpenFOAMReader(FileName=str(foam_file))
available = list(patch_reader.MeshRegions.Available)
patch_data = {}
for patch in ["AIR_INLET", "AIR_OUTLET", "WALLS"]:
    mesh_name = next(name for name in available if name.split("/")[-1] == patch)
    patch_reader.MeshRegions = [mesh_name]
    patch_reader.UpdatePipeline(time=float(final.name))
    patch_grid = list(leaves(servermanager.Fetch(patch_reader)))[0]
    patch_data[patch] = sizes(patch_grid, "Area")

q_in = patch_values(final / "phi", "AIR_INLET", count=len(patch_data["AIR_INLET"]))
q_out = patch_values(final / "phi", "AIR_OUTLET", count=len(patch_data["AIR_OUTLET"]))
q_wall = patch_values(final / "phi", "WALLS", count=len(patch_data["WALLS"]))
pin = patch_values(final / "p", "AIR_INLET", count=len(q_in)) * RHO
pout = patch_values(final / "p", "AIR_OUTLET", count=len(q_out)) * RHO
uin = patch_values(final / "U", "AIR_INLET", 3, len(q_in))
uout = patch_values(final / "U", "AIR_OUTLET", 3, len(q_out))
yp = patch_values(final / "yPlus", "WALLS", count=len(patch_data["WALLS"]))

metrics = {
    "label": f"SIMULATION — PHASE 8 {CASE_NAME} | KVO 250 | EMPTY TOWER | PARTIAL STATUS UNTIL CRITERIA CHECKED",
    "case": CASE_NAME,
    "final_iteration": float(final.name),
    "solved_iterations": len(rows),
    "solver_reported_converged": bool(re.search(r"converged in \d+ iterations", log)),
    "last_residuals": rows[-1],
    "fluid_volume_m3": float(vol.sum()),
    "cell_count": len(vol),
    "flow_m3_s": {
        "inlet_outward_signed": float(q_in.sum()),
        "outlet_outward_signed": float(q_out.sum()),
        "wall_signed": float(q_wall.sum()),
        "outlet_backflow": float(-q_out[q_out < 0].sum()),
    },
    "mass_imbalance_percent": float(abs(q_in.sum() + q_out.sum() + q_wall.sum()) / -q_in.sum() * 100),
    "mass_in_kg_s": float(-q_in.sum() * RHO),
    "mass_out_kg_s": float(q_out.sum() * RHO),
    "pressure_Pa": {
        "cell_min": float(p_pa.min()),
        "cell_max": float(p_pa.max()),
        "volume_mean": float(np.average(p_pa, weights=vol)),
        "inlet_area_mean": float(np.average(pin, weights=patch_data["AIR_INLET"])),
        "outlet_area_mean": float(np.average(pout, weights=patch_data["AIR_OUTLET"])),
        "inlet_flux_weighted_total": float(np.average(pin + 0.5 * RHO * np.sum(uin ** 2, axis=1), weights=-q_in)),
        "outlet_flux_weighted_total": float(np.average(pout + 0.5 * RHO * np.sum(uout ** 2, axis=1), weights=q_out)),
    },
    "speed_m_s": {
        "cell_min": float(speed.min()),
        "cell_max": float(speed.max()),
        "volume_mean": float(np.average(speed, weights=vol)),
        "wall_boundary": 0,
        "max_cell_center_m": xyz[int(np.argmax(speed))].tolist(),
    },
    "slow_volume_fraction_below_0p1_m_s": float(vol[speed < 0.1].sum() / vol.sum()),
    "wall_yplus": {
        "min": float(yp.min()),
        "max": float(yp.max()),
        "face_mean": float(yp.mean()),
        "face_fraction_below_30": float(np.mean(yp < 30)),
        "face_fraction_above_300": float(np.mean(yp > 300)),
    },
    "regions": {},
    "sections": {},
    "source_cad_sha256": audit["source_sha256"],
    "log_sha256": hashlib.sha256(log.encode()).hexdigest(),
}

coverage = np.zeros(len(vol), dtype=int)
for name, item in audit["regions"].items():
    bounds = np.array(item["bounds_mm"]) / 1000
    mask = np.all((xyz > bounds[::2]) & (xyz < bounds[1::2]), axis=1)
    coverage += mask
    if int(mask.sum()) != audit["cell_counts"][name]:
        raise RuntimeError(f"{CASE_NAME}: cell-zone mismatch for {name}")
    axis = 2 if name == "CLEAN_RISER" else 0
    metrics["regions"][name] = {
        "cells": int(mask.sum()),
        "volume_m3": float(vol[mask].sum()),
        "speed_volume_mean_m_s": float(np.average(speed[mask], weights=vol[mask])),
        "reverse_volume_fraction": float(vol[mask & (u[:, axis] < -0.05)].sum() / vol[mask].sum()),
        "reverse_definition": f"U{'xyz'[axis]} < -0.05 m/s; V01 indicator",
    }
if not (coverage == 1).all():
    raise RuntimeError(f"{CASE_NAME}: CFD regions do not cover internal mesh exactly once")

riser_bounds = np.array(audit["regions"]["CLEAN_RISER"]["bounds_mm"]) / 1000
common_riser = (
    (xyz[:, 0] > riser_bounds[0]) & (xyz[:, 0] < riser_bounds[1])
    & (xyz[:, 1] > riser_bounds[2]) & (xyz[:, 1] < riser_bounds[3])
    & (xyz[:, 2] > 0.850) & (xyz[:, 2] < 1.850)
)
metrics["common_riser_window"] = {
    "bounds_z_m": [0.850, 1.850],
    "reverse_volume_fraction_Uz_below_minus_0p05": float(vol[common_riser & (u[:, 2] < -0.05)].sum() / vol[common_riser].sum()),
    "speed_volume_mean_m_s": float(np.average(speed[common_riser], weights=vol[common_riser])),
}

section_specs = [
    ("STAGE_01_mid", [0.165, 0.4, 0.5], [1, 0, 0], [None, None, 0.100, 0.700, 0.150, 0.850]),
    ("STAGE_02_mid", [0.235, 0.4, 0.5], [1, 0, 0], [None, None, 0.100, 0.700, 0.150, 0.850]),
    ("STAGE_03_mid", [0.305, 0.4, 0.5], [1, 0, 0], [None, None, 0.100, 0.700, 0.150, 0.850]),
    ("riser_entry_above_turn", [0.4, 0.4, 0.86], [0, 0, 1], [riser_bounds[0], riser_bounds[1], 0.150, 0.650, None, None]),
    ("riser_mid", [0.4, 0.4, 1.2], [0, 0, 1], [riser_bounds[0], riser_bounds[1], 0.150, 0.650, None, None]),
    ("outlet_mid", [0.695, 0.4, 1.7], [1, 0, 0], [None, None, 0.150, 0.650, 1.600, 1.850]),
]
for name, origin, normal, bounds in section_specs:
    plane = vtkPlane()
    plane.SetOrigin(origin)
    plane.SetNormal(normal)
    cut = vtkCutter()
    cut.SetCutFunction(plane)
    cut.SetInputData(grid)
    cut.Update()
    section = cut.GetOutput()
    area = sizes(section, "Area")
    section_u = vtk_to_numpy(section.GetCellData().GetArray("U"))
    section_p = vtk_to_numpy(section.GetCellData().GetArray("p")) * RHO
    section_centres = vtkCellCenters()
    section_centres.SetInputData(section)
    section_centres.Update()
    section_xyz = vtk_to_numpy(section_centres.GetOutput().GetPoints().GetData())
    keep = np.ones(len(area), dtype=bool)
    for dimension in range(3):
        lo, hi = bounds[2 * dimension], bounds[2 * dimension + 1]
        if lo is not None:
            keep &= section_xyz[:, dimension] > lo - 1e-7
        if hi is not None:
            keep &= section_xyz[:, dimension] < hi + 1e-7
    area, section_u, section_p = area[keep], section_u[keep], section_p[keep]
    if not len(area):
        raise RuntimeError(f"{CASE_NAME}: empty intended section {name}")
    normal_velocity = section_u @ np.array(normal)
    mean = float(np.average(normal_velocity, weights=area))
    metrics["sections"][name] = {
        "origin_m": origin,
        "normal": normal,
        "area_m2": float(area.sum()),
        "speed_area_mean_m_s": float(np.average(np.linalg.norm(section_u, axis=1), weights=area)),
        "normal_velocity_area_mean_m_s": mean,
        "normal_velocity_min_m_s": float(normal_velocity.min()),
        "normal_velocity_max_m_s": float(normal_velocity.max()),
        "normal_velocity_CoV": float(np.sqrt(np.average((normal_velocity - mean) ** 2, weights=area)) / abs(mean)),
        "pressure_area_mean_Pa": float(np.average(section_p, weights=area)),
        "reverse_area_fraction": float(area[normal_velocity < 0].sum() / area.sum()),
        "sampled_volume_flow_m3_s": float(np.sum(normal_velocity * area)),
        "method": "Piecewise cell values on VTK cut; not conservative face phi",
        "selection_bounds_m": bounds,
    }

fan = json.loads((ROOT / "data/fans/systemair_KVO_250.json").read_text(encoding="utf-8"))
curve_q = np.array([point["Q_m3s"] for point in fan["fan_curve_points"]])
curve_p = np.array([point["delta_P_static_Pa"] for point in fan["fan_curve_points"]])
q = float(q_out.sum())
fan_head = float(np.interp(q, curve_q, curve_p))
total_suction = metrics["pressure_Pa"]["outlet_flux_weighted_total"]
metrics["fan"] = {
    "Q_m3_s": q,
    "Q_m3_h": q * 3600,
    "curve_static_Pa": fan_head,
    "measured_static_equivalent_Pa": -total_suction,
    "curve_closure_error_Pa": -total_suction - fan_head,
    "inside_source_curve": bool(curve_q[0] < q < curve_q[-1]),
    "source_json_sha256": sha256(ROOT / "data/fans/systemair_KVO_250.json"),
}
metrics["pressure_Pa"]["tower_static_difference"] = metrics["pressure_Pa"]["inlet_area_mean"] - metrics["pressure_Pa"]["outlet_area_mean"]
metrics["pressure_Pa"]["tower_flux_weighted_total_loss"] = metrics["pressure_Pa"]["inlet_flux_weighted_total"] - total_suction

for monitor, factor in [("inletPressure", RHO), ("outletFlow", 1.0)]:
    paths = list((CASE / "postProcessing" / monitor).glob("*/*.dat"))
    history = np.vstack([np.atleast_2d(np.loadtxt(path)) for path in paths])
    history = history[np.argsort(history[:, 0])]
    late = history[(history[:, 0] >= float(final.name) - 100) & (history[:, 0] <= float(final.name))]
    metrics[monitor + "_late100"] = {
        "min": float(late[:, -1].min() * factor),
        "max": float(late[:, -1].max() * factor),
        "range_percent_of_mean": float(np.ptp(late[:, -1]) / abs(late[:, -1].mean()) * 100),
    }
metrics["criteria"] = {
    "residuals": all(rows[-1][field + "_initial"] < (1e-5 if field == "p" else 1e-6) for field in ["p", "Ux", "Uy", "Uz", "k", "epsilon"]),
    "mass": metrics["mass_imbalance_percent"] < 0.1,
    "flow_stability": metrics["outletFlow_late100"]["range_percent_of_mean"] < 0.1,
    "fan_closure": abs(metrics["fan"]["curve_closure_error_Pa"]) < 0.1,
}
metrics["classification_boundary"] = "No automatic design classification; compare all cases and limitations together."
(OUT / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
styles = [("Ux", "#3569a8", "-"), ("Uy", "#3569a8", "--"), ("Uz", "#3569a8", ":"), ("p", "#ae7927", "-"), ("k", "#ae7927", "--"), ("epsilon", "#ae7927", ":")]
for field, color, style in styles:
    ax.semilogy([row["iteration"] for row in rows], [row[field + "_initial"] for row in rows], label=field, color=color, linestyle=style, linewidth=1.0)
ax.axhline(1e-5, color="#777777", linestyle="--", linewidth=0.8, label="p criterion")
ax.axhline(1e-6, color="#20262e", linestyle=":", linewidth=0.8, label="U/k/epsilon criterion")
ax.set(xlabel="Steady iteration (not physical time)", ylabel="Initial equation residual", title=f"{CASE_NAME} residual history\nKVO 250 / empty tower; same Phase 8 solver protocol")
ax.grid(alpha=0.2)
ax.legend(ncol=4, fontsize=8)
fig.savefig(OUT / "residual_history.png", dpi=170)
plt.close(fig)

y_values = np.unique(np.round(xyz[:, 1], 8))
y_layer = y_values[np.argmin(np.abs(y_values - 0.4))]
plane_mask = np.isclose(xyz[:, 1], y_layer, atol=1e-7)
px, pz = xyz[plane_mask, 0], xyz[plane_mask, 2]
pu, ps, pp = u[plane_mask], speed[plane_mask], p_pa[plane_mask]
order = np.lexsort((px, pz))
px, pz, pu, ps, pp = px[order], pz[order], pu[order], ps[order], pp[order]
fig, axes = plt.subplots(1, 2, figsize=(11.5, 8.0), layout="constrained", sharey=True)
velocity = axes[0].scatter(px, pz, c=ps, cmap="viridis", s=14, marker="s", linewidths=0, vmin=0, vmax=max(7, float(speed.max())))
reverse = pu[:, 2] < -0.05
axes[0].scatter(px[reverse], pz[reverse], facecolors="none", edgecolors="#b24c3a", s=20, linewidths=0.7)
sample = np.arange(0, len(px), 10)
axes[0].quiver(px[sample], pz[sample], pu[sample, 0], pu[sample, 2], color="#20262e", angles="xy", scale_units="xy", scale=32, width=0.0023, alpha=0.80)
pressure = axes[1].scatter(px, pz, c=pp, cmap="coolwarm", s=14, marker="s", linewidths=0, vmin=float(p_pa.min()), vmax=float(p_pa.max()))
for axis in axes:
    axis.set(xlabel="X (m)", xlim=(-0.02, 0.72), ylim=(0.10, 2.03), aspect="equal")
    axis.axhline(0.850, color="#555555", linestyle="--", linewidth=0.8)
axes[0].set_ylabel("Z (m)")
axes[0].set_title("Speed + velocity vectors\nred outline: Uz < -0.05 m/s")
axes[1].set_title("Gauge static pressure")
fig.colorbar(velocity, ax=axes[0], fraction=0.046, pad=0.04, label="Cell-centre speed (m/s)")
fig.colorbar(pressure, ax=axes[1], fraction=0.046, pad=0.04, label="Gauge pressure (Pa)")
fig.suptitle(f"SIMULATION — PHASE 8 {CASE_NAME} | KVO 250 | EMPTY TOWER\nCentral cell layer Y={y_layer:.3f} m; saved iteration {final.name}; convergence classified separately", fontsize=12)
fig.savefig(OUT / "central_velocity_pressure.png", dpi=180)
plt.close(fig)

print(json.dumps(metrics, indent=2))
