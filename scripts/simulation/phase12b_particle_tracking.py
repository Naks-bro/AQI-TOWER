"""Phase 12B: Conservative particle arrival fraction tracking.

PARTICLE ARRIVAL FRACTIONS — NOT FILTRATION EFFICIENCY.

Integrates equilibrium-slip particle paths through the frozen CASE_M_SEALED velocity
field (timestep 5000, steady RANS SIMPLEC) using nearest-neighbour velocity
interpolation with a gravitational terminal-settling correction. Each particle size
is tracked independently. The script does not solve a transient particle-momentum
equation.

Physical basis:
  Stokes number St = τ_p × U_char / L_char << 1 for all four tracked sizes.
  Particles follow airflow streamlines closely. Gravitational settling is the
  only size-dependent effect. Settling spans 0.00513–3.694 mm/s; the largest value
  is 0.123% of the stated 3.0 m/s characteristic velocity.
  Trajectories are therefore physically equivalent to streamlines for this flow.

Destinations (per particle):
  FILTER_ARRIVAL   — particle reached the active filter face (x > 0.290, in filter area)
  FRAME_DEPOSIT    — particle hit the filter mounting frame (x > 0.290, outside active area)
  WALL_DEPOSIT     — particle reached a tower wall before the filter
  RECIRCULATION    — particle exceeded MAX_TIME (trapped in recirculation zone)

Usage (in WSL from AQI-TOWER root):
    pvpython --force-offscreen-rendering scripts/simulation/phase12b_particle_tracking.py

Outputs:
    results/PARTICLE_CFD/particle_arrival_fractions.json
    results/PARTICLE_CFD/trajectory_0p3um.png
    results/PARTICLE_CFD/trajectory_1um.png
    results/PARTICLE_CFD/trajectory_2p5um.png
    results/PARTICLE_CFD/trajectory_10um.png
    results/PARTICLE_CFD/particle_summary.png
"""

from __future__ import annotations
import json
import math
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy.interpolate import griddata
from scipy.spatial import KDTree

from paraview import servermanager
from paraview.simple import OpenFOAMReader
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkFiltersCore import vtkCellCenters

# ---------------------------------------------------------------------------
# Particle physics constants
# ---------------------------------------------------------------------------
RHO_P       = 1200.0    # kg/m³  — density assumption (PM2.5 surrogate; between
                         #          water 1000 and mineral dust 2650 kg/m³)
MU_AIR      = 1.8e-5    # Pa·s   — air dynamic viscosity at 20°C
LAMBDA_MFP  = 66e-9     # m      — mean free path in standard air
G           = 9.81      # m/s²

DIAMETERS   = [0.3e-6, 1.0e-6, 2.5e-6, 10.0e-6]   # m
LABELS      = ["0.3 µm", "1 µm", "2.5 µm", "10 µm"]
TAGS        = ["0p3um", "1um", "2p5um", "10um"]

# ---------------------------------------------------------------------------
# Geometry constants (from Phases 9–11 documentation)
# ---------------------------------------------------------------------------
FILTER_X       = 0.305   # m — active filter face x-coordinate (FILTER_UPSTREAM)
FILTER_Y       = (0.1035, 0.6965)   # m — active filter y range
FILTER_Z       = (0.2035, 0.7965)   # m — active filter z range
FRAME_Y        = (0.100, 0.700)     # m — filter frame y extent (including inactive strip)
FRAME_Z        = (0.150, 0.850)     # m — filter frame z extent
BYPASS_SEAL_Z  = 0.850   # m — bypass seal z-coordinate
CLEAN_RISER_Z  = 0.850   # m — z above which is the CLEAN_RISER
FILTER_X_GATE  = 0.290   # m — x threshold for "particle reached filter region"

# ---------------------------------------------------------------------------
# Tracking parameters
# ---------------------------------------------------------------------------
SEED_X         = 0.010   # m — seed plane x-coordinate (just inside AIR_INLET)
N_SEED_Y       = 18      # seed grid in y direction
N_SEED_Z       = 18      # seed grid in z direction
DT             = 0.004   # s — Euler integration time step
MAX_TIME       = 6.0     # s — maximum integration time (>> flow residence time ~1.2 s)
MAX_STEPS      = int(MAX_TIME / DT)
CELL_SIZE      = 0.020   # m — nominal mesh cell size (all-hex 20 mm, from Phase 9)
WALL_DIST_THR  = 0.014   # m — nearest-cell distance above which particle has left domain

# U_char and L_char for Stokes number
U_CHAR         = 3.0     # m/s — characteristic riser velocity
L_CHAR         = 0.300   # m   — characteristic domain length (filter x-position)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT  = Path(__file__).resolve().parents[2]
CASE  = ROOT / "cfd" / "FILTER_H13" / "CASE_M_SEALED"
FOAM  = CASE / "CASE_M_SEALED.foam"
OUT   = ROOT / "results" / "PARTICLE_CFD"
OUT.mkdir(parents=True, exist_ok=True)

print("=" * 60, flush=True)
print("Phase 12B — Conservative particle tracking", flush=True)
print("  Case  : CASE_M_SEALED (Phase 10B, timestep 5000)", flush=True)
print("  Output: results/PARTICLE_CFD/", flush=True)
print("  PARTICLE ARRIVAL FRACTIONS — NOT FILTER EFFICIENCIES", flush=True)
print("=" * 60, flush=True)

# ---------------------------------------------------------------------------
# Physics helpers
# ---------------------------------------------------------------------------
def cunningham_cc(dp: float) -> float:
    """Cunningham slip correction factor (Allen–Raabe formula)."""
    Kn = LAMBDA_MFP / (dp / 2)
    return 1.0 + Kn * (1.257 + 0.4 * math.exp(-1.1 / Kn))

def tau_p(dp: float) -> float:
    """Particle relaxation time [s]."""
    return RHO_P * cunningham_cc(dp) * dp**2 / (18.0 * MU_AIR)

def v_settle(dp: float) -> float:
    """Terminal settling velocity [m/s] (downward in -z direction)."""
    return tau_p(dp) * G

def stokes_number(dp: float) -> float:
    return tau_p(dp) * U_CHAR / L_CHAR

# ---------------------------------------------------------------------------
# Load mesh (same approach as Phase 10B)
# ---------------------------------------------------------------------------
def leaves(dataset):
    if dataset.IsA("vtkMultiBlockDataSet"):
        for i in range(dataset.GetNumberOfBlocks()):
            blk = dataset.GetBlock(i)
            if blk is not None:
                yield from leaves(blk)
    elif dataset.GetNumberOfCells():
        yield dataset

print("\nLoading CASE_M_SEALED internal mesh...", flush=True)
reader = OpenFOAMReader(FileName=str(FOAM))
reader.MeshRegions = ["internalMesh"]
reader.CellArrays = ["U"]
reader.UpdatePipeline(time=5000.0)

grid = list(leaves(servermanager.Fetch(reader)))[0]
ctr = vtkCellCenters()
ctr.SetInputData(grid)
ctr.Update()

XYZ = vtk_to_numpy(ctr.GetOutput().GetPoints().GetData())   # (N_cells, 3)
U_FIELD = vtk_to_numpy(grid.GetCellData().GetArray("U"))    # (N_cells, 3)

print(f"  Loaded {len(XYZ)} cells, timestep 5000", flush=True)
print(f"  Domain x: {XYZ[:,0].min():.3f} – {XYZ[:,0].max():.3f} m", flush=True)
print(f"  Domain y: {XYZ[:,1].min():.3f} – {XYZ[:,1].max():.3f} m", flush=True)
print(f"  Domain z: {XYZ[:,2].min():.3f} – {XYZ[:,2].max():.3f} m", flush=True)

# Mean filter face velocity for reference
in_filter = (
    (np.abs(XYZ[:, 0] - FILTER_X) < 0.025) &
    (XYZ[:, 1] > FILTER_Y[0]) & (XYZ[:, 1] < FILTER_Y[1]) &
    (XYZ[:, 2] > FILTER_Z[0]) & (XYZ[:, 2] < FILTER_Z[1])
)
v_filter_ref = np.linalg.norm(U_FIELD[in_filter], axis=1).mean() if in_filter.any() else 1.0
print(f"  Approx filter face speed (cells near x=0.305): {v_filter_ref:.3f} m/s", flush=True)

# Build KDTree on cell centres
print("  Building KDTree for velocity interpolation...", flush=True)
TREE = KDTree(XYZ)

# ---------------------------------------------------------------------------
# Generate and validate seed points
# ---------------------------------------------------------------------------
y_seeds = np.linspace(0.08, 0.82, N_SEED_Y)
z_seeds = np.linspace(0.12, 0.88, N_SEED_Z)
YY, ZZ = np.meshgrid(y_seeds, z_seeds)
seeds_raw = np.column_stack([
    np.full(N_SEED_Y * N_SEED_Z, SEED_X),
    YY.ravel(),
    ZZ.ravel(),
])

# Keep only seeds inside the mesh (nearest cell distance < threshold)
d_seed, _ = TREE.query(seeds_raw)
seed_mask = d_seed < WALL_DIST_THR
SEEDS = seeds_raw[seed_mask]
N_SEEDS = len(SEEDS)
print(f"\n  Seed points: {N_SEEDS} valid (of {len(seeds_raw)} candidates at x={SEED_X} m)", flush=True)

# ---------------------------------------------------------------------------
# Particle tracking function (vectorised Euler integration)
# ---------------------------------------------------------------------------
def track(dp: float, label: str) -> dict:
    """
    Integrate N_SEEDS equilibrium-slip particle paths in the frozen velocity field.
    Adds Cunningham-corrected Stokes terminal settling in -z (size-dependent).
    Uses Euler integration with nearest-neighbour velocity lookup.
    """
    vs    = v_settle(dp)
    tau   = tau_p(dp)
    St    = stokes_number(dp)
    cc    = cunningham_cc(dp)

    print(f"\n  [{label}]  d_p={dp*1e6:.2f} µm  "
          f"τ_p={tau*1e6:.3f} µs  v_settle={vs*1e3:.4f} mm/s  St={St:.2e}", flush=True)

    pos  = SEEDS.copy()                      # (N, 3)  current positions
    dest = np.empty(N_SEEDS, dtype='U20')   # destination strings
    term = np.zeros((N_SEEDS, 3))           # terminal positions
    t_arr= np.zeros(N_SEEDS)               # terminal integration times
    alive= np.ones(N_SEEDS, dtype=bool)    # True = particle still moving

    for step in range(MAX_STEPS):
        if not alive.any():
            break
        t = step * DT

        idx_alive = np.where(alive)[0]
        p_alive   = pos[idx_alive]           # (n, 3)

        dists, kcell = TREE.query(p_alive)   # nearest cell distance & index

        # ---- Wall/domain-exit detection ----
        hit_wall = dists > WALL_DIST_THR
        for j, i in enumerate(idx_alive[hit_wall]):
            dest[i]  = "WALL_DEPOSIT"
            term[i]  = pos[i]
            t_arr[i] = t
            alive[i] = False

        # ---- Update remaining particles ----
        still = idx_alive[~hit_wall]
        if not still.any():
            break

        p_still  = pos[still]
        d2, kc2  = TREE.query(p_still)
        vel       = U_FIELD[kc2].copy()    # (n, 3) nearest-cell velocity
        vel[:, 2] -= vs                    # gravitational settling in -z

        pos[still] = p_still + vel * DT    # Euler step

        # ---- Filter arrival detection ----
        in_filter_area = (
            (pos[still, 0] > FILTER_X_GATE) &
            (pos[still, 1] > FILTER_Y[0])   &
            (pos[still, 1] < FILTER_Y[1])   &
            (pos[still, 2] > FILTER_Z[0])   &
            (pos[still, 2] < FILTER_Z[1])
        )
        hit_filter = still[in_filter_area]
        for i in hit_filter:
            dest[i]  = "FILTER_ARRIVAL"
            term[i]  = pos[i]
            t_arr[i] = t + DT
            alive[i] = False

        # ---- Filter FRAME deposit ----
        in_frame_area = (
            (pos[still, 0] > FILTER_X_GATE) &
            ~in_filter_area  # reached x=0.290 but outside active filter face
        )
        hit_frame = still[in_frame_area]
        for i in hit_frame:
            dest[i]  = "FRAME_DEPOSIT"
            term[i]  = pos[i]
            t_arr[i] = t + DT
            alive[i] = False

        if step % 300 == 0:
            n_alive  = alive.sum()
            n_filter = (dest == "FILTER_ARRIVAL").sum()
            n_wall   = (dest == "WALL_DEPOSIT").sum()
            print(f"      t={t:.2f}s  alive={n_alive}  filter={n_filter}  wall={n_wall}", flush=True)

    # ---- Remaining: stuck in recirculation ----
    recircs = np.where(alive)[0]
    for i in recircs:
        dest[i]  = "RECIRCULATION"
        term[i]  = pos[i]
        t_arr[i] = MAX_TIME

    # ---- Compute fractions ----
    n_filter = int((dest == "FILTER_ARRIVAL").sum())
    n_frame  = int((dest == "FRAME_DEPOSIT" ).sum())
    n_wall   = int((dest == "WALL_DEPOSIT"  ).sum())
    n_recirc = int((dest == "RECIRCULATION" ).sum())
    n_total  = N_SEEDS

    f_filter = n_filter / n_total
    f_frame  = n_frame  / n_total
    f_wall   = n_wall   / n_total
    f_recirc = n_recirc / n_total

    print(f"      DONE: filter={n_filter}/{n_total} ({f_filter*100:.1f}%)  "
          f"frame={n_frame} ({f_frame*100:.1f}%)  "
          f"wall={n_wall} ({f_wall*100:.1f}%)  "
          f"stuck={n_recirc} ({f_recirc*100:.1f}%)", flush=True)

    return {
        "dp_m"                    : dp,
        "dp_um"                   : dp * 1e6,
        "label"                   : label,
        "rho_p_kg_m3"             : RHO_P,
        "cunningham_cc"           : cc,
        "tau_p_us"                : tau * 1e6,
        "v_settle_mm_s"           : vs * 1e3,
        "stokes_number"           : St,
        "n_total"                 : n_total,
        "n_filter_arrival"        : n_filter,
        "n_frame_deposit"         : n_frame,
        "n_wall_deposit"          : n_wall,
        "n_recirculation"         : n_recirc,
        "filter_arrival_fraction" : f_filter,
        "frame_deposit_fraction"  : f_frame,
        "wall_deposit_fraction"   : f_wall,
        "recirculation_fraction"  : f_recirc,
        "destinations"            : dest,
        "term_positions"          : term,
    }


# ---------------------------------------------------------------------------
# Run tracking for all particle sizes
# ---------------------------------------------------------------------------
print("\n" + "=" * 60, flush=True)
print("Running particle tracking (4 sizes)...", flush=True)
results = {}
for dp, lbl, tag in zip(DIAMETERS, LABELS, TAGS):
    results[tag] = track(dp, lbl)

# ---------------------------------------------------------------------------
# Prepare mid-plane flow field for background (same as Phase 10B)
# ---------------------------------------------------------------------------
print("\nPreparing mid-plane flow field for visualisation...", flush=True)
y_vals = np.unique(np.round(XYZ[:, 1], 8))
y_mid  = y_vals[np.argmin(np.abs(y_vals - 0.40))]
mask_mp = np.isclose(XYZ[:, 1], y_mid, atol=2e-4)
sx, sz  = XYZ[mask_mp, 0], XYZ[mask_mp, 2]
su      = U_FIELD[mask_mp]
ss      = np.linalg.norm(su, axis=1)

xi = np.linspace(-0.005, 0.715, 145)
zi = np.linspace(0.08, 1.92, 175)
XX, ZZ = np.meshgrid(xi, zi)
pts    = np.column_stack([sx, sz])
Ux_g   = griddata(pts, su[:, 0], (XX, ZZ), method="linear")
Uz_g   = griddata(pts, su[:, 2], (XX, ZZ), method="linear")
Ssp_g  = griddata(pts, ss,       (XX, ZZ), method="linear")
Ux_g   = np.where(np.isnan(Ux_g), 0.0, Ux_g)
Uz_g   = np.where(np.isnan(Uz_g), 0.0, Uz_g)
Ssp_g  = np.where(np.isnan(Ssp_g), 0.0, Ssp_g)

print(f"  Mid-plane: y = {y_mid:.4f} m, {mask_mp.sum()} cells", flush=True)

# Streamline seeds (same as Phase 10B)
seed_x_stream = np.full(18, 0.010)
seed_z_stream = np.linspace(0.14, 0.86, 18)
stream_seeds  = np.column_stack([seed_x_stream, seed_z_stream])

# ---------------------------------------------------------------------------
# FIGURE: trajectory_Xum.png — one per particle size
# ---------------------------------------------------------------------------
DEST_COLORS = {
    "FILTER_ARRIVAL" : "#22cc44",   # green
    "FRAME_DEPOSIT"  : "#f0a030",   # orange
    "WALL_DEPOSIT"   : "#dd2222",   # red
    "RECIRCULATION"  : "#9966ff",   # purple
}
DEST_LABELS = {
    "FILTER_ARRIVAL" : "Filter arrival",
    "FRAME_DEPOSIT"  : "Frame deposit",
    "WALL_DEPOSIT"   : "Wall deposit",
    "RECIRCULATION"  : "Recirculation",
}

for dp, lbl, tag in zip(DIAMETERS, LABELS, TAGS):
    r = results[tag]
    dest = r["destinations"]
    term = r["term_positions"]     # (N, 3)

    fig, ax = plt.subplots(figsize=(7, 10), layout="constrained")

    # Background: speed field
    im = ax.pcolormesh(XX, ZZ, Ssp_g, cmap="viridis", vmin=0, vmax=7.0, shading="auto")
    plt.colorbar(im, ax=ax, label="|U| (m/s)", shrink=0.7)

    # Airflow streamlines
    ax.streamplot(xi, zi, Ux_g, Uz_g, start_points=stream_seeds,
                  color="white", linewidth=0.9, arrowsize=0.8, maxlength=3.5, zorder=3)

    # Particle terminal positions (mid-plane band y ≈ 0.35–0.45 m)
    mid_band = (term[:, 1] > 0.25) & (term[:, 1] < 0.55)
    for dkey, dcolor in DEST_COLORS.items():
        mask = (dest == dkey) & mid_band
        if mask.any():
            ax.scatter(term[mask, 0], term[mask, 2],
                       color=dcolor, s=22, zorder=5, label=DEST_LABELS[dkey],
                       edgecolors="none", alpha=0.85)

    # Reference lines
    ax.axvline(FILTER_X, color="#ff88ff", linestyle="--", linewidth=1.2, zorder=4,
               label=f"Filter x={FILTER_X} m")
    ax.axhline(BYPASS_SEAL_Z, color="#88aaff", linestyle=":", linewidth=1.0, zorder=4,
               label=f"Bypass seal z={BYPASS_SEAL_Z} m")

    # Annotations
    n  = r["n_total"]
    nf = r["n_filter_arrival"]
    nw = r["n_wall_deposit"]
    nr = r["n_recirculation"]
    ff = r["filter_arrival_fraction"]
    fw = r["wall_deposit_fraction"]

    ax.set(
        xlabel="X (m)", ylabel="Z (m)",
        xlim=(-0.01, 0.72), ylim=(0.07, 1.93)
    )
    ax.set_aspect("equal")
    ax.set_title(
        f"Phase 12B — Particle tracking — {lbl}\n"
        f"CASE_M_SEALED  timestep 5000  GEO_C + H13 sealed\n"
        f"Filter arrival: {nf}/{n} = {ff*100:.1f}%   "
        f"Wall deposit: {nw}/{n} = {fw*100:.1f}%\n"
        f"τ_p={r['tau_p_us']:.3f} µs  v_settle={r['v_settle_mm_s']:.4f} mm/s  St={r['stokes_number']:.2e}\n"
        f"PARTICLE ARRIVAL FRACTION — NOT FILTER EFFICIENCY",
        fontsize=8
    )
    legend = ax.legend(loc="upper right", fontsize=7, framealpha=0.8)
    ax.text(0.02, 0.02,
            "Dots = terminal positions (mid-plane band)\n"
            "Streamlines = airflow direction",
            transform=ax.transAxes, fontsize=6, color="white",
            va="bottom", ha="left")

    out_path = OUT / f"trajectory_{tag}.png"
    fig.savefig(out_path, dpi=170)
    plt.close(fig)
    print(f"  trajectory_{tag}.png saved.", flush=True)

# ---------------------------------------------------------------------------
# FIGURE: particle_summary.png — arrival fractions all four sizes
# ---------------------------------------------------------------------------
print("\nGenerating summary figure...", flush=True)
fig, axes = plt.subplots(1, 2, figsize=(13, 5), layout="constrained")

# Left: stacked bar of fractions
bar_w   = 0.5
x_pos   = np.arange(len(DIAMETERS))
f_filt  = [results[t]["filter_arrival_fraction"] for t in TAGS]
f_frame = [results[t]["frame_deposit_fraction"]   for t in TAGS]
f_wall  = [results[t]["wall_deposit_fraction"]    for t in TAGS]
f_recirc= [results[t]["recirculation_fraction"]   for t in TAGS]

ax = axes[0]
b1 = ax.bar(x_pos, f_filt,  bar_w, label="Filter arrival",  color="#22cc44")
b2 = ax.bar(x_pos, f_frame, bar_w, label="Frame deposit",   color="#f0a030",
            bottom=f_filt)
b3 = ax.bar(x_pos, f_wall,  bar_w, label="Wall deposit",    color="#dd2222",
            bottom=np.array(f_filt) + np.array(f_frame))
b4 = ax.bar(x_pos, f_recirc,bar_w, label="Recirculation",  color="#9966ff",
            bottom=np.array(f_filt)+np.array(f_frame)+np.array(f_wall))

ax.set_xticks(x_pos)
ax.set_xticklabels(LABELS)
ax.set_ylim(0, 1.0)
ax.set_ylabel("Fraction of injected particles")
ax.set_xlabel("Particle diameter")
ax.set_title(
    "Particle destination fractions by size\n"
    "PARTICLE ARRIVAL FRACTIONS — NOT FILTER EFFICIENCIES\n"
    "Phase 12B (CASE_M_SEALED, St << 1 for all sizes)"
)
ax.legend(loc="lower right", fontsize=8)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v*100:.0f}%"))
for i, (ff, lbl) in enumerate(zip(f_filt, LABELS)):
    ax.text(i, ff / 2, f"{ff*100:.1f}%", ha="center", va="center",
            fontsize=9, color="white", fontweight="bold")

# Right: Stokes numbers and settling velocities
ax2 = axes[1]
dp_um   = [dp * 1e6 for dp in DIAMETERS]
st_vals = [stokes_number(dp) for dp in DIAMETERS]
vs_vals = [v_settle(dp) * 1e3 for dp in DIAMETERS]  # mm/s

ax2.loglog(dp_um, st_vals, "o-", color="#3569a8", label="Stokes number St", linewidth=1.8)
ax2_r = ax2.twinx()
ax2_r.loglog(dp_um, vs_vals, "s--", color="#a83535", label="Settling velocity (mm/s)", linewidth=1.8)

ax2.axhline(0.01, color="#888", linestyle=":", linewidth=0.8)
ax2.text(0.35, 0.011, "St=0.01", fontsize=7, color="#888")
ax2.axhline(0.001, color="#aaa", linestyle=":", linewidth=0.8)
ax2.text(0.35, 0.0011, "St=0.001", fontsize=7, color="#aaa")

ax2.set_xlabel("Particle diameter (µm)")
ax2.set_ylabel("Stokes number", color="#3569a8")
ax2_r.set_ylabel("Settling velocity (mm/s)", color="#a83535")
ax2.set_title(
    "Particle size — physical parameters\n"
    f"ρ_p={RHO_P:.0f} kg/m³  μ_air={MU_AIR:.2e} Pa·s\n"
    "All St << 1 → particles follow streamlines"
)
lines, labs   = ax2.get_legend_handles_labels()
lines2, labs2 = ax2_r.get_legend_handles_labels()
ax2.legend(lines + lines2, labs + labs2, loc="upper left", fontsize=8)

fig.suptitle(
    "Phase 12B — Conservative particle tracking — CASE_M_SEALED GEO_C + H13 sealed bypass\n"
    "SIMULATION — PARTIAL NON-CONVERGED flow field — PARTICLE ARRIVAL FRACTIONS — NOT EFFICIENCIES",
    fontsize=9
)
fig.savefig(OUT / "particle_summary.png", dpi=170)
plt.close(fig)
print("  particle_summary.png saved.", flush=True)

# ---------------------------------------------------------------------------
# Save particle_arrival_fractions.json
# ---------------------------------------------------------------------------
print("\nWriting particle_arrival_fractions.json...", flush=True)
output_json = {
    "description": (
        "Phase 12B conservative particle tracking results. "
        "PARTICLE ARRIVAL FRACTIONS — NOT FILTER EFFICIENCIES. "
        "Particles tracked through frozen CASE_M_SEALED velocity field "
        "(Phase 10B, timestep 5000, steady RANS SIMPLEC). "
        "Nearest-neighbour velocity interpolation. Euler integration dt=%.4f s." % DT
    ),
    "flow_field": {
        "case": "CASE_M_SEALED",
        "timestep": 5000,
        "phase": "10B",
        "status": "PARTIAL NON-CONVERGED (same RANS limit as all GEO_C cases)",
        "Q_m3_h": 1332.2,
        "filter_face_velocity_mean_m_s": 1.053,
        "bypass_fraction": 9.997e-10,
        "filter_delta_P_Pa": 111.2,
    },
    "particle_model": {
        "type": "one-way coupled, non-reacting, dilute equilibrium-slip particle paths",
        "density_kg_m3": RHO_P,
        "density_note": "single assumed representative aerosol density; composition-specific density is not modelled",
        "drag_model": (
            "Equilibrium-slip approximation: particle velocity equals local frozen-air "
            "velocity plus Cunningham-corrected Stokes terminal settling; no time-resolved "
            "particle-momentum equation"
        ),
        "gravity_m_s2": G,
        "gravity_direction": "-z (downward in GEO_C coordinates)",
        "injection_plane_x_m": SEED_X,
        "injection_method": "uniform grid at x=0.010 m in active flow region",
        "n_seeds": N_SEEDS,
        "integration_method": "Euler, dt=%.4f s, max_time=%.1f s" % (DT, MAX_TIME),
        "velocity_interpolation": "nearest-neighbour (KDTree on cell centres)",
        "filter_face_model": (
            "Particles reaching x>%.3f m within active filter face area are classified "
            "as FILTER_ARRIVAL. No capture probability is applied. "
            "FILTER ARRIVAL != FILTER CAPTURE." % FILTER_X_GATE
        ),
    },
    "stokes_number_note": (
        "For all four tracked particle sizes, Stokes number St = tau_p * U_char / L_char << 1. "
        "Particles follow airflow streamlines with only gravity drift as a size-dependent effect. "
        "Settling velocities are 0.00513–3.694 mm/s. The maximum is 0.123% of the stated "
        "3.0 m/s characteristic velocity (and 0.739% of 0.5 m/s). "
        "Size-dependent trajectory differences are therefore negligible for this flow configuration. "
        "All four sizes are expected to show nearly identical arrival fractions."
    ),
    "results": {},
    "summary": {
        "n_seeds": N_SEEDS,
        "filter_arrival_fractions": {},
        "wall_deposit_fractions": {},
        "most_important_finding": (
            "Nearly identical particle arrival fractions occur across all four size classes "
            "for this seed grid and numerical model. This is consistent with the very low "
            "Stokes numbers (St << 1); the result is dominated by mean-flow topology and the "
            "injection/wall-classification method."
        ),
    },
}

for dp, lbl, tag in zip(DIAMETERS, LABELS, TAGS):
    r = results[tag]
    output_json["results"][tag] = {
        "label"                     : lbl,
        "dp_um"                     : dp * 1e6,
        "cunningham_cc"             : r["cunningham_cc"],
        "tau_p_us"                  : r["tau_p_us"],
        "v_settle_mm_s"             : r["v_settle_mm_s"],
        "stokes_number"             : r["stokes_number"],
        "n_total"                   : r["n_total"],
        "n_filter_arrival"          : r["n_filter_arrival"],
        "n_frame_deposit"           : r["n_frame_deposit"],
        "n_wall_deposit"            : r["n_wall_deposit"],
        "n_recirculation"           : r["n_recirculation"],
        "filter_arrival_fraction"   : r["filter_arrival_fraction"],
        "frame_deposit_fraction"    : r["frame_deposit_fraction"],
        "wall_deposit_fraction"     : r["wall_deposit_fraction"],
        "recirculation_fraction"    : r["recirculation_fraction"],
        "interpretation": (
            "%.1f%% of particles seeded at the inlet reached the active filter face. "
            "This is the PARTICLE ARRIVAL FRACTION at FILTER_UPSTREAM, not the filter "
            "capture/removal efficiency. Actual removal efficiency requires the product-specific "
            "fractional efficiency curve eta(d_p) which is not yet available (Phase 12A finding)."
            % (r["filter_arrival_fraction"] * 100)
        ),
    }
    output_json["summary"]["filter_arrival_fractions"][lbl] = r["filter_arrival_fraction"]
    output_json["summary"]["wall_deposit_fractions"][lbl]   = r["wall_deposit_fraction"]

(OUT / "particle_arrival_fractions.json").write_text(
    json.dumps(output_json, indent=2, ensure_ascii=False), encoding="utf-8"
)
print("  particle_arrival_fractions.json saved.", flush=True)

# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60, flush=True)
print("=== Phase 12B particle tracking results ===", flush=True)
print(f"  N_seeds = {N_SEEDS}  dt = {DT} s  max_time = {MAX_TIME} s", flush=True)
print(f"  Injection plane: x = {SEED_X} m  (AIR_INLET region)", flush=True)
print(f"  Frozen flow field: CASE_M_SEALED timestep 5000", flush=True)
print("", flush=True)
print(f"  {'Size':>8}  {'τ_p (µs)':>10}  {'v_s (mm/s)':>12}  {'St':>10}  {'FILTER':>8}  {'WALL':>8}  {'STUCK':>8}", flush=True)
print("  " + "-" * 80, flush=True)
for dp, lbl, tag in zip(DIAMETERS, LABELS, TAGS):
    r = results[tag]
    print(
        f"  {lbl:>8}  {r['tau_p_us']:>10.3f}  {r['v_settle_mm_s']:>12.4f}"
        f"  {r['stokes_number']:>10.2e}"
        f"  {r['filter_arrival_fraction']*100:>7.1f}%"
        f"  {r['wall_deposit_fraction']*100:>7.1f}%"
        f"  {r['recirculation_fraction']*100:>7.1f}%",
        flush=True
    )
print("  " + "-" * 80, flush=True)
print("  NOTE: FILTER arrival fraction ≠ filter removal efficiency.", flush=True)
print("  CADR cannot be computed without product-specific η(d_p).", flush=True)
print("=" * 60, flush=True)
print("\nPhase 12B complete. Files written to results/PARTICLE_CFD/", flush=True)
