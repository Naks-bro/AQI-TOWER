"""T3 — Export CFD scalar planes for Three.js visualization.

Reads existing solved OpenFOAM fields (READ-ONLY) and exports sampled 2-D plane
data as browser-friendly JSON files.

Fields exported:
    U_MAGNITUDE  — |U| = sqrt(Ux²+Uy²+Uz²)  [m/s]
    P_STATIC     — p_kinematic × ρ             [Pa gauge, ρ=1.20 kg/m³]

Planes exported:
    longitudinal   — y = 0.400 m (centre of flow-domain depth)
    filter_xsec    — x = 0.305 m (STAGE_03 mid / CASE_M_SEALED filter baffle)

Cases:
    GEO_C          cfd/GEO_C          timestep 926   CONVERGED
    GEO_C_CONFIRM  cfd/GEO_C_CONFIRM  timestep 926   CONVERGED (deterministic confirm)
    CASE_M_SEALED  cfd/FILTER_H13/CASE_M_SEALED  timestep 5000  PARTIALLY_CONVERGED

Usage (WSL, from AQI-TOWER root):
    pvpython --force-offscreen-rendering threejs/tools/cfd/export_scalar_planes.py

Outputs:
    threejs/public/data/cfd/<CASE>_<FIELD>_<PLANE>.json
    threejs/public/data/cfd/cfd_index.json

READ-ONLY: does NOT modify any case file.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
from scipy.interpolate import griddata

from paraview import servermanager
from paraview.simple import OpenFOAMReader
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkFiltersCore import vtkCellCenters

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[3]   # AQI-TOWER root
OUT  = ROOT / "threejs" / "public" / "data" / "cfd"
OUT.mkdir(parents=True, exist_ok=True)

RHO = 1.20          # kg/m³ — reference density from physicalProperties

# Grid resolution — longitudinal plane (x-z): 100×130 ≈ 13 000 pts
NX_LONG, NZ_LONG = 100, 130
# Grid resolution — filter cross-section plane (y-z): 65×75 ≈ 4 875 pts
NY_XSEC, NZ_XSEC = 65, 75

# Plane definitions (CAD coordinate system: x=flow, y=depth, z=vertical)
LONG_Y        = 0.400   # m — longitudinal plane at y = 0.400
LONG_ATOL     = 1.5e-3  # m — ±1.5 mm slice tolerance

XSEC_X        = 0.305   # m — filter cross-section plane
XSEC_X_SLAB   = 0.020   # m — ±20 mm slab (catches cells in entire stage width)

# Domain extents for grid generation (CAD coords)
LONG_X_RANGE  = (0.000,  0.710)
LONG_Z_RANGE  = (0.140,  1.860)
XSEC_Y_RANGE  = (0.090,  0.710)
XSEC_Z_RANGE  = (0.140,  0.880)

CASE_REGISTRY = [
    {
        "case_id":   "GEO_C",
        "case_path": "cfd/GEO_C",
        "foam_file": "GEO_C.foam",
        "timestep":  926,
        "convergence_status": "CONVERGED",
        "criteria_met": "residuals, mass, flow_stability, fan_closure",
        "q_m3_h": 1496.0549912644801,
    },
    {
        "case_id":   "GEO_C_CONFIRM",
        "case_path": "cfd/GEO_C_CONFIRM",
        "foam_file": "GEO_C_CONFIRM.foam",
        "timestep":  926,
        "convergence_status": "CONVERGED",
        "criteria_met": "residuals, mass, flow_stability, fan_closure",
        "q_m3_h": 1496.0549912644801,
    },
    {
        "case_id":   "CASE_M_SEALED",
        "case_path": "cfd/FILTER_H13/CASE_M_SEALED",
        "foam_file": "CASE_M_SEALED.foam",
        "timestep":  5000,
        "convergence_status": "PARTIALLY_CONVERGED",
        "criteria_met": "mass, flow_stability — residuals reached plateau at iter ~2000",
        "q_m3_h": 1332.205242935976,
    },
]

# ---------------------------------------------------------------------------
# VTK helpers (identical pattern to phase10a/10b)
# ---------------------------------------------------------------------------
def leaves(dataset):
    if dataset.IsA("vtkMultiBlockDataSet"):
        for i in range(dataset.GetNumberOfBlocks()):
            blk = dataset.GetBlock(i)
            if blk is not None:
                yield from leaves(blk)
    elif dataset.GetNumberOfCells():
        yield dataset


def load_case(case_info: dict) -> dict:
    case_dir  = ROOT / case_info["case_path"]
    foam_file = case_dir / case_info["foam_file"]
    timestep  = case_info["timestep"]

    if not foam_file.exists():
        raise FileNotFoundError(f".foam file not found: {foam_file}")

    print(f"  Loading {case_info['case_id']} (timestep {timestep}) ...", flush=True)
    reader = OpenFOAMReader(FileName=str(foam_file))
    reader.MeshRegions = ["internalMesh"]
    reader.CellArrays  = ["U", "p"]
    reader.UpdatePipeline(time=float(timestep))
    grid = list(leaves(servermanager.Fetch(reader)))[0]

    # Cell centres
    ctr = vtkCellCenters()
    ctr.SetInputData(grid)
    ctr.Update()
    xyz = vtk_to_numpy(ctr.GetOutput().GetPoints().GetData())  # (N, 3) CAD coords

    # Velocity and speed
    u_vec   = vtk_to_numpy(grid.GetCellData().GetArray("U"))   # (N, 3) m/s
    speed   = np.linalg.norm(u_vec, axis=1)                    # (N,) m/s

    # Kinematic pressure → Pa
    p_kin   = vtk_to_numpy(grid.GetCellData().GetArray("p"))   # (N,) m²/s²
    p_pa    = p_kin * RHO                                       # (N,) Pa

    n_cells = len(xyz)
    print(f"    {n_cells} cells loaded. speed range: "
          f"{speed.min():.3f}–{speed.max():.3f} m/s | "
          f"p range: {p_pa.min():.2f}–{p_pa.max():.2f} Pa", flush=True)

    return {"xyz": xyz, "speed": speed, "p_pa": p_pa, "n_cells": n_cells}


# ---------------------------------------------------------------------------
# Plane samplers
# ---------------------------------------------------------------------------
def sample_longitudinal(data: dict) -> tuple[np.ndarray, np.ndarray, dict]:
    """Return (u_grid, p_grid) on NX_LONG×NZ_LONG grid, and grid_def dict."""
    xyz, speed, p_pa = data["xyz"], data["speed"], data["p_pa"]

    # Find nearest y-layer in actual cell centres
    y_unique = np.unique(np.round(xyz[:, 1], 6))
    y_layer  = float(y_unique[np.argmin(np.abs(y_unique - LONG_Y))])
    mask     = np.abs(xyz[:, 1] - y_layer) < LONG_ATOL

    pts_xz = xyz[mask][:, [0, 2]]
    vals_u = speed[mask]
    vals_p = p_pa[mask]

    n_slice = int(mask.sum())
    print(f"    longitudinal slice: y={y_layer:.4f} m, {n_slice} cells", flush=True)

    xi = np.linspace(*LONG_X_RANGE, NX_LONG)
    zi = np.linspace(*LONG_Z_RANGE, NZ_LONG)
    xi_grid, zi_grid = np.meshgrid(xi, zi, indexing="ij")  # (NX, NZ)

    u_grid = griddata(pts_xz, vals_u, (xi_grid, zi_grid), method="linear")
    p_grid = griddata(pts_xz, vals_p, (xi_grid, zi_grid), method="linear")

    grid_def = {
        "type":           "longitudinal",
        "normal":         "y",
        "position_cad_m": y_layer,
        "description":    f"Centre longitudinal plane y={y_layer:.4f} m (depth midplane)",
        "axis1":          "x",
        "axis2":          "z",
        "axis1_range":    list(LONG_X_RANGE),
        "axis2_range":    list(LONG_Z_RANGE),
        "n_axis1":        NX_LONG,
        "n_axis2":        NZ_LONG,
        "n_slice_cells":  n_slice,
        "interpolation":  "VISUAL INTERPOLATION ONLY — scipy.interpolate.griddata linear; not additional CFD cells",
    }
    return u_grid, p_grid, grid_def


def sample_filter_xsec(data: dict) -> tuple[np.ndarray, np.ndarray, dict]:
    """Return (u_grid, p_grid) on NY_XSEC×NZ_XSEC grid, and grid_def dict."""
    xyz, speed, p_pa = data["xyz"], data["speed"], data["p_pa"]

    mask = np.abs(xyz[:, 0] - XSEC_X) < XSEC_X_SLAB
    pts_yz = xyz[mask][:, [1, 2]]
    vals_u = speed[mask]
    vals_p = p_pa[mask]

    n_slice = int(mask.sum())
    print(f"    filter_xsec: x={XSEC_X:.3f}±{XSEC_X_SLAB:.3f} m, {n_slice} cells", flush=True)

    yi = np.linspace(*XSEC_Y_RANGE, NY_XSEC)
    zi = np.linspace(*XSEC_Z_RANGE, NZ_XSEC)
    yi_grid, zi_grid = np.meshgrid(yi, zi, indexing="ij")  # (NY, NZ)

    u_grid = griddata(pts_yz, vals_u, (yi_grid, zi_grid), method="linear")
    p_grid = griddata(pts_yz, vals_p, (yi_grid, zi_grid), method="linear")

    grid_def = {
        "type":           "filter_xsec",
        "normal":         "x",
        "position_cad_m": XSEC_X,
        "slab_half_width_m": XSEC_X_SLAB,
        "description":    f"Filter cross-section x={XSEC_X:.3f} m (STAGE_03 mid / filter baffle)",
        "axis1":          "y",
        "axis2":          "z",
        "axis1_range":    list(XSEC_Y_RANGE),
        "axis2_range":    list(XSEC_Z_RANGE),
        "n_axis1":        NY_XSEC,
        "n_axis2":        NZ_XSEC,
        "n_slice_cells":  n_slice,
        "interpolation":  "VISUAL INTERPOLATION ONLY — scipy.interpolate.griddata linear; not additional CFD cells",
    }
    return u_grid, p_grid, grid_def


# ---------------------------------------------------------------------------
# JSON serializer — NaN → null, compact floats
# ---------------------------------------------------------------------------
def _compact(v: float, decimals: int) -> object:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    return round(float(v), decimals)


def grid_to_list(arr: np.ndarray, decimals: int) -> list:
    """Flatten C-order (axis1, axis2) array; NaN → null."""
    flat = arr.ravel(order="C")
    return [_compact(x, decimals) for x in flat]


# ---------------------------------------------------------------------------
# Build export record
# ---------------------------------------------------------------------------
def build_record(case_info: dict, field_id: str, plane_id: str,
                 grid_def: dict, values_arr: np.ndarray,
                 units: str, field_desc: str, derivation: str,
                 decimals: int) -> dict:
    valid = values_arr[~np.isnan(values_arr)]
    data_min = float(valid.min()) if len(valid) else 0.0
    data_max = float(valid.max()) if len(valid) else 0.0

    return {
        "schema_version": 1,
        "case_id":        case_info["case_id"],
        "case_path":      case_info["case_path"],
        "source_timestep": str(case_info["timestep"]),
        "field":          field_id,
        "field_description": field_desc,
        "derivation":     derivation,
        "units":          units,
        "plane":          plane_id,
        "grid":           grid_def,
        "data_min":       round(data_min, decimals),
        "data_max":       round(data_max, decimals),
        "n_valid":        int(len(valid)),
        "n_total":        int(values_arr.size),
        "values":         grid_to_list(values_arr, decimals),
        "convergence_status":  case_info["convergence_status"],
        "validation_status":   "SIMULATION ONLY — NOT PHYSICALLY VALIDATED",
        "provenance": {
            "source_field":         "U" if "U" in field_id else "p",
            "solver":               "incompressibleFluid (RANS SIMPLEC, OpenFOAM 14)",
            "rho_kg_m3":            RHO,
            "pressure_note":        (
                "p is kinematic pressure [m²/s²] from incompressible RANS solver. "
                "Converted to Pa by P = p_kin × ρ (ρ=1.20 kg/m³ from physicalProperties). "
                "Values are gauge (relative to solver reference)."
            ) if "P" in field_id else "not applicable — velocity field",
            "export_script":        "threejs/tools/cfd/export_scalar_planes.py",
            "export_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        },
    }


# ---------------------------------------------------------------------------
# Main export loop
# ---------------------------------------------------------------------------
def main():
    print(f"T3 CFD export starting — output: {OUT}", flush=True)
    index_entries = []

    for case_info in CASE_REGISTRY:
        print(f"\n=== {case_info['case_id']} ===", flush=True)
        try:
            data = load_case(case_info)
        except Exception as exc:
            print(f"  ERROR loading {case_info['case_id']}: {exc}", flush=True)
            continue

        planes = [
            ("longitudinal",  sample_longitudinal),
            ("filter_xsec",   sample_filter_xsec),
        ]

        for plane_id, sampler in planes:
            print(f"  Sampling {plane_id} ...", flush=True)
            try:
                u_grid, p_grid, grid_def = sampler(data)
            except Exception as exc:
                print(f"  ERROR sampling {plane_id}: {exc}", flush=True)
                continue

            # Velocity magnitude
            u_rec = build_record(
                case_info, "U_MAGNITUDE", plane_id, grid_def, u_grid,
                units="m/s",
                field_desc="Velocity magnitude |U|",
                derivation="DERIVED FROM CFD VELOCITY FIELD: |U| = sqrt(Ux² + Uy² + Uz²)",
                decimals=3,
            )
            u_file = OUT / f"{case_info['case_id']}_U_MAGNITUDE_{plane_id}.json"
            u_file.write_text(json.dumps(u_rec, separators=(",", ":")), encoding="utf-8")
            size_kb = u_file.stat().st_size / 1024
            print(f"    → {u_file.name}  ({size_kb:.0f} kB)", flush=True)

            # Static pressure
            p_rec = build_record(
                case_info, "P_STATIC", plane_id, grid_def, p_grid,
                units="Pa (gauge)",
                field_desc="Static pressure P = p_kinematic × ρ",
                derivation="DERIVED FROM CFD PRESSURE FIELD: P_Pa = p_kin × 1.20 kg/m³",
                decimals=2,
            )
            p_file = OUT / f"{case_info['case_id']}_P_STATIC_{plane_id}.json"
            p_file.write_text(json.dumps(p_rec, separators=(",", ":")), encoding="utf-8")
            size_kb = p_file.stat().st_size / 1024
            print(f"    → {p_file.name}  ({size_kb:.0f} kB)", flush=True)

            for fid in ("U_MAGNITUDE", "P_STATIC"):
                index_entries.append({
                    "case_id":         case_info["case_id"],
                    "field":           fid,
                    "plane":           plane_id,
                    "convergence_status": case_info["convergence_status"],
                    "source_timestep": str(case_info["timestep"]),
                    "file":            f"{case_info['case_id']}_{fid}_{plane_id}.json",
                })

    # Write index
    idx_file = OUT / "cfd_index.json"
    idx_file.write_text(
        json.dumps({"schema_version": 1, "exports": index_entries}, indent=2),
        encoding="utf-8",
    )
    print(f"\ncfd_index.json written — {len(index_entries)} entries.", flush=True)
    print("T3 export complete.", flush=True)


if __name__ == "__main__":
    main()
