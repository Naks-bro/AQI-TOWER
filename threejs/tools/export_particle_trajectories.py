"""
export_particle_trajectories.py — READ-ONLY trajectory export tool.

Re-runs the Phase 12B equilibrium-slip particle tracking while storing
intermediate path coordinates every STORE_INTERVAL steps.

OUTPUT:
    threejs/public/data/particleTrajectories.json

This script does NOT modify any existing project files.
It uses the same frozen CASE_M_SEALED velocity field and the same physics
constants as scripts/simulation/phase12b_particle_tracking.py.

USAGE (WSL, from AQI-TOWER root):
    pvpython --force-offscreen-rendering threejs/tools/export_particle_trajectories.py

REQUIREMENTS:
    - pvpython (ParaView Python)
    - scipy, numpy (available in the pvpython environment)
    - cfd/FILTER_H13/CASE_M_SEALED must be accessible (all timesteps present)

OUTPUT JSON STRUCTURE:
    {
      "metadata": {
        "source_case": "CASE_M_SEALED",
        "timestep": 5000,
        "phase": "12B",
        "n_seeds": 224,
        "dt_s": 0.004,
        "store_interval_steps": STORE_INTERVAL,
        "store_dt_s": STORE_INTERVAL * 0.004,
        "warning": "SIMULATION POST-PROCESSING ONLY ...",
        ...
      },
      "trajectories": [
        {
          "particle_id": 0,
          "diameter_um": 0.3,
          "tag": "0p3um",
          "seed": [x, y, z],            // CAD coordinates (m)
          "points": [[x,y,z], ...],     // CAD coordinates (m), stored every STORE_INTERVAL steps
          "final_status": "FILTER_ARRIVAL",
          "n_steps": 42
        },
        ...
      ]
    }

COORDINATE SYSTEM:
    All coordinates are in CAD system (x=flow, y=depth, z=vertical).
    Three.js viewer converts: THREE_x = x−0.350, THREE_y = z−0.925, THREE_z = y−0.400

FILTER ARRIVAL ≠ FILTER CAPTURE. No capture probability applied.
"""

from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import KDTree

from paraview import servermanager
from paraview.simple import OpenFOAMReader
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkFiltersCore import vtkCellCenters

# ── constants (identical to phase12b_particle_tracking.py) ──────────────────
RHO_P      = 1200.0
MU_AIR     = 1.8e-5
LAMBDA_MFP = 66e-9
G          = 9.81

DIAMETERS  = [0.3e-6, 1.0e-6, 2.5e-6, 10.0e-6]
LABELS     = ["0.3 µm", "1 µm", "2.5 µm", "10 µm"]
TAGS       = ["0p3um", "1um", "2p5um", "10um"]

FILTER_X       = 0.305
FILTER_Y       = (0.1035, 0.6965)
FILTER_Z       = (0.2035, 0.7965)
FRAME_Y        = (0.100, 0.700)
FRAME_Z        = (0.150, 0.850)
FILTER_X_GATE  = 0.290
SEED_X         = 0.010
N_SEED_Y       = 18
N_SEED_Z       = 18
DT             = 0.004
MAX_TIME       = 6.0
MAX_STEPS      = int(MAX_TIME / DT)
WALL_DIST_THR  = 0.014
U_CHAR         = 3.0
L_CHAR         = 0.300

# How often to store a path point (every STORE_INTERVAL Euler steps)
# 25 steps × 0.004 s = 0.1 s between stored points → max 60 points per trajectory
STORE_INTERVAL = 25

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "cfd" / "FILTER_H13" / "CASE_M_SEALED"
FOAM = CASE / "CASE_M_SEALED.foam"
OUT_DIR  = ROOT / "threejs" / "public" / "data"
OUT_FILE = OUT_DIR / "particleTrajectories.json"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── physics helpers ──────────────────────────────────────────────────────────
def cunningham_cc(dp):
    Kn = LAMBDA_MFP / (dp / 2)
    return 1.0 + Kn * (1.257 + 0.4 * math.exp(-1.1 / Kn))

def tau_p(dp):
    return RHO_P * cunningham_cc(dp) * dp**2 / (18.0 * MU_AIR)

def v_settle(dp):
    return tau_p(dp) * G

# ── load mesh ────────────────────────────────────────────────────────────────
print("Loading CASE_M_SEALED...", flush=True)

def leaves(dataset):
    if dataset.IsA("vtkMultiBlockDataSet"):
        for i in range(dataset.GetNumberOfBlocks()):
            blk = dataset.GetBlock(i)
            if blk is not None:
                yield from leaves(blk)
    elif dataset.GetNumberOfCells():
        yield dataset

reader = OpenFOAMReader(FileName=str(FOAM))
reader.MeshRegions = ["internalMesh"]
reader.CellArrays  = ["U"]
reader.UpdatePipeline(time=5000.0)

grid = list(leaves(servermanager.Fetch(reader)))[0]
ctr  = vtkCellCenters()
ctr.SetInputData(grid)
ctr.Update()

XYZ     = vtk_to_numpy(ctr.GetOutput().GetPoints().GetData())
U_FIELD = vtk_to_numpy(grid.GetCellData().GetArray("U"))
TREE    = KDTree(XYZ)

print(f"  {len(XYZ)} cells loaded, timestep 5000", flush=True)

# ── seed points ─────────────────────────────────────────────────────────────
y_seeds = np.linspace(0.08, 0.82, N_SEED_Y)
z_seeds = np.linspace(0.12, 0.88, N_SEED_Z)
YY, ZZ = np.meshgrid(y_seeds, z_seeds)
seeds_raw = np.column_stack([
    np.full(N_SEED_Y * N_SEED_Z, SEED_X),
    YY.ravel(), ZZ.ravel(),
])
d_seed, _ = TREE.query(seeds_raw)
seed_mask = d_seed < WALL_DIST_THR
SEEDS = seeds_raw[seed_mask]
print(f"  Seeds: {len(SEEDS)} valid of {len(seeds_raw)} candidates", flush=True)

# ── trajectory tracking ──────────────────────────────────────────────────────
all_trajectories = []

for dp, lbl, tag in zip(DIAMETERS, LABELS, TAGS):
    vs    = v_settle(dp)
    print(f"\n  [{lbl}]  v_settle={vs*1e3:.4f} mm/s", flush=True)

    n     = len(SEEDS)
    pos   = SEEDS.copy()
    dest  = np.empty(n, dtype='U20')
    alive = np.ones(n, dtype=bool)
    paths = [[list(SEEDS[i])] for i in range(n)]  # stored path per particle

    for step in range(MAX_STEPS):
        if not alive.any():
            break

        idx_alive = np.where(alive)[0]
        dists, kc = TREE.query(pos[idx_alive])

        # Wall exit
        hit_wall = dists > WALL_DIST_THR
        for j, i in enumerate(idx_alive[hit_wall]):
            dest[i]  = "WALL_DEPOSIT"
            alive[i] = False

        # Advance
        still = idx_alive[~hit_wall]
        if not still.any():
            break

        vel = U_FIELD[TREE.query(pos[still])[1]].copy()
        vel[:, 2] -= vs
        pos[still] = pos[still] + vel * DT

        # Filter arrival
        in_fa = (
            (pos[still, 0] > FILTER_X_GATE) &
            (pos[still, 1] > FILTER_Y[0]) & (pos[still, 1] < FILTER_Y[1]) &
            (pos[still, 2] > FILTER_Z[0]) & (pos[still, 2] < FILTER_Z[1])
        )
        for i in still[in_fa]:
            dest[i]  = "FILTER_ARRIVAL"
            alive[i] = False

        # Frame deposit
        in_fr = (pos[still, 0] > FILTER_X_GATE) & ~in_fa
        for i in still[in_fr]:
            dest[i]  = "FRAME_DEPOSIT"
            alive[i] = False

        # Store every STORE_INTERVAL steps
        if step % STORE_INTERVAL == 0:
            for i in np.where(alive)[0]:
                paths[i].append(list(pos[i]))

    # Append final positions for all particles
    for i in range(n):
        if alive[i]:
            dest[i] = "RECIRCULATION"
        paths[i].append(list(pos[i]))  # terminal

    for i in range(n):
        all_trajectories.append({
            "particle_id":   int(len(all_trajectories)),
            "diameter_um":   float(dp * 1e6),
            "tag":           tag,
            "seed":          list(SEEDS[i].astype(float)),
            "points":        [list(map(float, p)) for p in paths[i]],
            "final_status":  str(dest[i]),
            "n_steps_stored": len(paths[i]),
        })

    fa = int((dest == "FILTER_ARRIVAL").sum())
    print(f"    filter={fa}/{n}  wall={(dest=='WALL_DEPOSIT').sum()}  "
          f"frame={(dest=='FRAME_DEPOSIT').sum()}", flush=True)

# ── write output ─────────────────────────────────────────────────────────────
output = {
    "metadata": {
        "description": "Phase 12B trajectory export. FILTER ARRIVAL FRACTION — NOT FILTER CAPTURE EFFICIENCY.",
        "source_case":          "CASE_M_SEALED",
        "timestep":             5000,
        "phase":                "12B",
        "n_seeds":              int(len(SEEDS)),
        "n_candidates":         int(len(seeds_raw)),
        "dt_s":                 DT,
        "store_interval_steps": STORE_INTERVAL,
        "store_dt_s":           STORE_INTERVAL * DT,
        "max_time_s":           MAX_TIME,
        "rho_p_kg_m3":          RHO_P,
        "coordinate_system":    "CAD: x=flow, y=depth, z=vertical. THREE.js: x=x−0.350, y=z−0.925, z=y−0.400",
        "warning": (
            "SIMULATION POST-PROCESSING ONLY. FILTER ARRIVAL ≠ FILTER CAPTURE. "
            "Partial non-converged RANS velocity field. Equilibrium-slip approximation. "
            "No turbulent dispersion. Not validated on physical hardware."
        ),
        "script": "scripts/simulation/phase12b_particle_tracking.py",
        "export_script": "threejs/tools/export_particle_trajectories.py",
    },
    "n_trajectories": len(all_trajectories),
    "trajectories": all_trajectories,
}

OUT_FILE.write_text(json.dumps(output, separators=(',', ':')), encoding="utf-8")
print(f"\nWrote {len(all_trajectories)} trajectories → {OUT_FILE}", flush=True)
print("Total JSON size:", OUT_FILE.stat().st_size // 1024, "kB", flush=True)
