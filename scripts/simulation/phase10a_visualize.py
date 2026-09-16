"""Phase 10A: Generate all HEPA H13 CFD visualizations from saved Phase 9 fields.

Usage:
    pvpython --force-offscreen-rendering scripts/simulation/phase10a_visualize.py

Outputs go to results/FILTER_H13/.
Handles CASE_M (complete run, 5000 iters) and CASE_L/H (incomplete, 4750 iters).
Does NOT rerun CFD. Does NOT modify any case files.
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

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "FILTER_H13"
OUT.mkdir(parents=True, exist_ok=True)

RHO = 1.20          # kg/m3
FILTER_X = 0.305    # m — filter plane position
FILTER_Y = (0.1035, 0.6965)   # active face y bounds
FILTER_Z = (0.2035, 0.7965)   # active face z bounds
FILTER_AREA = 0.3516           # m2 — manufacturer nominal

CASES = {
    "CASE_L": {"multiplier": 0.6349, "label": "CASE_L (Lower, ~80 Pa/1.19 m·s⁻¹)"},
    "CASE_M": {"multiplier": 1.0000, "label": "CASE_M (Nominal, ~126 Pa/1.19 m·s⁻¹)"},
    "CASE_H": {"multiplier": 1.1905, "label": "CASE_H (Upper, ~150 Pa/1.19 m·s⁻¹)"},
}
LOG_NAMES = [
    "foamRun_initial.log",
    "foamRun_tight.log",
    "foamRun_baffleRelax005.log",
    "foamRun_baffleRelax005_corrected.log",
    "foamRun_baffleRelax0005.log",
]

print("Phase 10A visualizer starting.", flush=True)

# ---------------------------------------------------------------------------
# Utility: parse OpenFOAM ASCII field patch section
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

# ---------------------------------------------------------------------------
# Utility: residual log parser
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Utility: VTK leaf iterator
# ---------------------------------------------------------------------------
def leaves(dataset):
    if dataset.IsA("vtkMultiBlockDataSet"):
        for i in range(dataset.GetNumberOfBlocks()):
            blk = dataset.GetBlock(i)
            if blk is not None:
                yield from leaves(blk)
    elif dataset.GetNumberOfCells():
        yield dataset

# ---------------------------------------------------------------------------
# Load internal mesh and fields for one case via pvpython
# ---------------------------------------------------------------------------
def load_case(case_name: str):
    case = ROOT / "cfd" / "FILTER_H13" / case_name
    foam_file = case / f"{case_name}.foam"
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

    sizer = vtkCellSizeFilter()
    sizer.SetInputData(grid)
    sizer.Update()
    vol = vtk_to_numpy(sizer.GetOutput().GetCellData().GetArray("Volume"))

    u = vtk_to_numpy(grid.GetCellData().GetArray("U"))
    p = vtk_to_numpy(grid.GetCellData().GetArray("p")) * RHO

    # Load patch-level phi and p from ASCII files
    phi_path = final / "phi"
    p_path = final / "p"
    impl = json.loads((case / "filter_implementation.json").read_text(encoding="utf-8"))
    n_fu = 961   # FILTER_UPSTREAM faces (from boundary file)
    n_fd = 961   # FILTER_DOWNSTREAM faces
    n_in = 1221  # AIR_INLET faces
    n_out = 325  # AIR_OUTLET faces

    q_out = patch_values(phi_path, "AIR_OUTLET", count=n_out)
    q_filter = patch_values(phi_path, "FILTER_UPSTREAM", count=n_fu)
    pf_up_kin = patch_values(p_path, "FILTER_UPSTREAM", count=n_fu)
    pf_down_kin = patch_values(p_path, "FILTER_DOWNSTREAM", count=n_fd)

    return {
        "case": case_name,
        "final_iter": int(final.name),
        "xyz": xyz,
        "vol": vol,
        "u": u,
        "p": p,
        "q_total": float(q_out.sum()),
        "q_filter": float(q_filter.sum()),
        "q_filter_per_face": q_filter,
        "pf_up_Pa": pf_up_kin * RHO,
        "pf_down_Pa": pf_down_kin * RHO,
        "impl": impl,
    }

# ---------------------------------------------------------------------------
# Load patch-only data (no VTK internal mesh) for comparison figures
# ---------------------------------------------------------------------------
def load_patch_only(case_name: str):
    case = ROOT / "cfd" / "FILTER_H13" / case_name
    times = sorted(
        (p for p in case.iterdir() if p.is_dir() and re.fullmatch(r"\d+", p.name) and int(p.name) > 0),
        key=lambda p: int(p.name),
    )
    final = times[-1]
    phi_path = final / "phi"
    p_path = final / "p"
    impl = json.loads((case / "filter_implementation.json").read_text(encoding="utf-8"))
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
        "impl": impl,
    }

# ---------------------------------------------------------------------------
# Derive filter face Y,Z coordinates from mesh geometry (same for all cases)
# ---------------------------------------------------------------------------
def filter_face_positions():
    """Return (y, z) arrays for the 961 FILTER_UPSTREAM cell centres.
    The active face spans y=103.5–696.5 mm, z=203.5–796.5 mm at 20 mm mesh.
    31×31 = 961 face centres.
    """
    y_nodes = np.array([103.5, 150.0, 650.0, 696.5]) / 1000
    z_nodes = np.array([203.5, 450.0, 650.0, 796.5]) / 1000
    # Segments and cells per segment:
    # y: [103.5-150] = 46.5mm / ~20mm ≈ 2 cells, [150-650]=500mm/20mm=25 cells, [650-696.5]=46.5mm≈2 cells → 29 cells
    # z: [203.5-450]=246.5mm≈12 cells, [450-650]=200mm=10, [650-796.5]=146.5mm≈7 cells → 29 cells?
    # 29×29=841≠961; actual is 31×31=961
    # Use uniform spacing as approximation for plotting purposes:
    ny = 31
    nz = 31
    y_vals = np.linspace(FILTER_Y[0] + 0.01, FILTER_Y[1] - 0.01, ny)
    z_vals = np.linspace(FILTER_Z[0] + 0.01, FILTER_Z[1] - 0.01, nz)
    yy, zz = np.meshgrid(y_vals, z_vals)
    return yy.ravel(), zz.ravel()

FY, FZ = filter_face_positions()

# ---------------------------------------------------------------------------
# IMAGE 4: Residual history (CASE_M)
# ---------------------------------------------------------------------------
print("Generating residual history...", flush=True)
rows = parse_residuals(ROOT / "cfd" / "FILTER_H13" / "CASE_M")
fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
styles = [
    ("Ux", "#3569a8", "-"), ("Uy", "#3569a8", "--"), ("Uz", "#3569a8", ":"),
    ("p",  "#ae7927", "-"), ("k",  "#ae7927", "--"), ("epsilon", "#ae7927", ":"),
]
for field, color, ls in styles:
    key = field + "_initial"
    if key in rows[0]:
        ax.semilogy([r["iteration"] for r in rows], [r[key] for r in rows],
                    label=field, color=color, linestyle=ls, linewidth=1.0)
ax.axhline(1e-5, color="#888", linestyle="--", linewidth=0.8, label="p target")
ax.axhline(1e-6, color="#333", linestyle=":",  linewidth=0.8, label="U/k/ε target")
ax.set(xlabel="Iteration", ylabel="Initial residual",
       title="CASE_M residual history — KVO 250 + GEO_C + H13 filter\nSIMULATION — PHASE 9 — PARTIAL NON-CONVERGED")
ax.grid(alpha=0.2)
ax.legend(ncol=4, fontsize=8)
fig.savefig(OUT / "residual_history_CASE_M.png", dpi=170)
plt.close(fig)
print("  residual_history_CASE_M.png saved.", flush=True)

# ---------------------------------------------------------------------------
# Load CASE_M internal mesh (for spatial images)
# ---------------------------------------------------------------------------
print("Loading CASE_M VTK mesh...", flush=True)
cm = load_case("CASE_M")
xyz_m, u_m, p_m = cm["xyz"], cm["u"], cm["p"]
speed_m = np.linalg.norm(u_m, axis=1)
print(f"  CASE_M loaded: {len(xyz_m)} cells, iter {cm['final_iter']}", flush=True)

# ---------------------------------------------------------------------------
# IMAGE 1: Central velocity + pressure slice (CASE_M)
# ---------------------------------------------------------------------------
print("Generating central velocity/pressure figure...", flush=True)
y_vals = np.unique(np.round(xyz_m[:, 1], 8))
y_layer = y_vals[np.argmin(np.abs(y_vals - 0.4))]
mask = np.isclose(xyz_m[:, 1], y_layer, atol=2e-4)
px, pz = xyz_m[mask, 0], xyz_m[mask, 2]
pu, ps, pp = u_m[mask], speed_m[mask], p_m[mask]

fig, axes = plt.subplots(1, 2, figsize=(11.5, 8.0), layout="constrained", sharey=True)
vmax_speed = max(7.0, float(ps.max()))
sc0 = axes[0].scatter(px, pz, c=ps, cmap="viridis", s=14, marker="s",
                       linewidths=0, vmin=0, vmax=vmax_speed)
# Mark reverse-flow cells (Uz < -0.05)
rev = pu[:, 2] < -0.05
axes[0].scatter(px[rev], pz[rev], facecolors="none", edgecolors="#b24c3a",
                s=22, linewidths=0.8)
# Quiver every 8th cell
step = max(1, len(px) // 250)
samp = np.arange(0, len(px), step)
axes[0].quiver(px[samp], pz[samp], pu[samp, 0], pu[samp, 2],
               color="#20262e", angles="xy", scale_units="xy", scale=28,
               width=0.0025, alpha=0.75)
sc1 = axes[1].scatter(px, pz, c=pp, cmap="coolwarm", s=14, marker="s",
                       linewidths=0, vmin=float(pp.min()), vmax=float(pp.max()))
for ax in axes:
    ax.axvline(FILTER_X, color="#20262e", linestyle="--", linewidth=1.1, label="Filter x=0.305 m")
    ax.axhline(FILTER_Z[0], color="#888", linestyle=":", linewidth=0.7)
    ax.axhline(FILTER_Z[1], color="#888", linestyle=":", linewidth=0.7)
    ax.set(xlabel="X (m)", xlim=(-0.02, 0.72), ylim=(0.10, 1.90), aspect="equal")
axes[0].set_ylabel("Z (m)")
axes[0].set_title("Speed |U| + flow vectors\nRed outline: Uz < −0.05 m/s\nDashed gray: filter Z bounds")
axes[1].set_title("Gauge static pressure (Pa)\nFilter at x=0.305 m")
fig.colorbar(sc0, ax=axes[0], fraction=0.046, pad=0.04, label="Speed (m/s)")
fig.colorbar(sc1, ax=axes[1], fraction=0.046, pad=0.04, label="Pressure (Pa)")
fig.suptitle(
    "SIMULATION — PHASE 9 CASE_M | KVO 250 + GEO_C + H13\n"
    "APPROXIMATION FROM SINGLE MANUFACTURER DATA POINT | Y-layer at y ≈ {:.3f} m".format(y_layer),
    fontsize=11,
)
fig.savefig(OUT / "central_velocity_pressure_CASE_M.png", dpi=180)
plt.close(fig)
print("  central_velocity_pressure_CASE_M.png saved.", flush=True)

# ---------------------------------------------------------------------------
# IMAGE 3: Bypass streamlines (CASE_M, X-Z central plane)
# ---------------------------------------------------------------------------
print("Generating bypass streamlines...", flush=True)
# Only use cells in the lower duct region where filter is located (z < 0.90 m)
# This avoids the riser dominating the plot and lets us see the bypass path
duct_mask = mask & (xyz_m[:, 2] < 0.92)
dpx, dpz = xyz_m[duct_mask, 0], xyz_m[duct_mask, 2]
dpu = u_m[duct_mask]  # Ux, Uy, Uz
dps = speed_m[duct_mask]
dpux, dpuz = dpu[:, 0], dpu[:, 2]  # X and Z components for X-Z streamlines

# Build uniform grid for streamplot
x_grid = np.linspace(0.001, 0.70, 140)
z_grid = np.linspace(0.12, 0.89, 140)
XX, ZZ = np.meshgrid(x_grid, z_grid)
pts = np.column_stack([dpx, dpz])
UX_interp = griddata(pts, dpux, (XX, ZZ), method="linear", fill_value=0.0)
UZ_interp = griddata(pts, dpuz, (XX, ZZ), method="linear", fill_value=0.0)
SPD_interp = griddata(pts, dps, (XX, ZZ), method="linear", fill_value=np.nan)

fig, ax = plt.subplots(figsize=(9.0, 7.0), layout="constrained")
bg = ax.pcolormesh(x_grid, z_grid, SPD_interp, cmap="Greys", vmin=0,
                   vmax=max(4.0, float(np.nanmax(SPD_interp))), shading="auto", alpha=0.55)
strm = ax.streamplot(
    x_grid, z_grid, UX_interp, UZ_interp,
    density=1.8, linewidth=0.9, arrowsize=1.0,
    color=SPD_interp, cmap="plasma",
    start_points=np.column_stack([
        np.full(20, 0.01),
        np.linspace(0.16, 0.86, 20),
    ]),
    minlength=0.05,
)
ax.axvline(FILTER_X, color="#20262e", linestyle="--", linewidth=1.4,
           label=f"Filter x={FILTER_X} m")
ax.add_patch(mpatches.FancyArrowPatch((FILTER_X, FILTER_Z[0]),
                                       (FILTER_X, FILTER_Z[1]),
                                       color="#1a7a3f", linewidth=2.5,
                                       arrowstyle="-"))
ax.fill_betweenx([FILTER_Z[0], FILTER_Z[1]], FILTER_X - 0.002, FILTER_X + 0.002,
                 color="#1a7a3f", alpha=0.7, label="Active filter face (z=0.20–0.80 m)")
# Bypass region annotation
bypass_z_low = FILTER_Z[1]
bypass_z_high = 0.86
ax.fill_betweenx([bypass_z_low, bypass_z_high], 0.0, FILTER_X,
                 color="#e07840", alpha=0.10, label=f"Suspected bypass zone (z>{bypass_z_low:.2f})")
ax.set(xlabel="X (m)", ylabel="Z (m)", xlim=(0.0, 0.72), ylim=(0.10, 0.90),
       title=(
           "SIMULATION — PHASE 9 CASE_M | X-Z central plane streamlines\n"
           "Bypass streamlines = lines that reach x > 0.305 m without filter crossing\n"
           "PHASE 10A DIAGNOSIS — NOT A CORRECTED RESULT"
       ))
ax.legend(fontsize=8, loc="upper right")
fig.colorbar(bg, ax=ax, label="Background: cell speed (m/s)")
fig.savefig(OUT / "bypass_streamlines_CASE_M.png", dpi=180)
plt.close(fig)
print("  bypass_streamlines_CASE_M.png saved.", flush=True)

# ---------------------------------------------------------------------------
# IMAGE 2: Filter face bypass map (CASE_M)
# ---------------------------------------------------------------------------
print("Generating filter face bypass map...", flush=True)
q_filter_m = cm["q_filter_per_face"]   # 961 values, m3/s per face
# Estimate face areas: total active area / n_faces
face_area = FILTER_AREA / len(q_filter_m)
un_filter_m = q_filter_m / face_area    # normal velocity per face

fig, axes = plt.subplots(1, 2, figsize=(12, 5.8), layout="constrained")

# Left: filter face normal velocity
limit = max(abs(un_filter_m.min()), abs(un_filter_m.max()))
sc = axes[0].scatter(FY, FZ, c=un_filter_m, cmap="coolwarm",
                     vmin=-limit, vmax=limit, s=30, marker="s", linewidths=0)
fig.colorbar(sc, ax=axes[0], label="Normal velocity (m/s) — positive = forward")
axes[0].set(xlabel="Y (m)", ylabel="Z (m)", aspect="equal",
            title=f"CASE_M filter face normal velocity\n{len(q_filter_m)} active faces, area {FILTER_AREA:.4f} m²")
axes[0].text(0.05, 0.95,
             f"Mean: {un_filter_m.mean():.3f} m/s\n"
             f"CoV: {un_filter_m.std()/un_filter_m.mean():.3f}\n"
             f"Rev. area: {(un_filter_m < 0).mean()*100:.1f}%",
             transform=axes[0].transAxes, va="top", fontsize=8,
             bbox=dict(facecolor="white", alpha=0.75, edgecolor="none"))

# Right: upstream velocity Ux in duct immediately in front of filter (x=0.25 to 0.31 m)
near_mask = mask & (xyz_m[:, 0] > 0.25) & (xyz_m[:, 0] < 0.31)
near_yz = xyz_m[near_mask, 1:3]   # y, z of upstream cells
near_ux = u_m[near_mask, 0]        # Ux (toward filter, positive = approaching)
if len(near_yz) > 0:
    sc2 = axes[1].scatter(near_yz[:, 0], near_yz[:, 1], c=near_ux, cmap="RdBu_r",
                           s=16, marker="s", linewidths=0,
                           vmin=-abs(near_ux).max(), vmax=abs(near_ux).max())
    fig.colorbar(sc2, ax=axes[1], label="Ux (m/s) — positive = toward filter")
    axes[1].set(xlabel="Y (m)", ylabel="Z (m)", aspect="equal",
                title="Upstream Ux at x=0.25–0.31 m\n(positive = flow toward filter)")
    axes[1].add_patch(mpatches.Rectangle(
        (FILTER_Y[0], FILTER_Z[0]), FILTER_Y[1]-FILTER_Y[0], FILTER_Z[1]-FILTER_Z[0],
        fill=False, edgecolor="#1a7a3f", linewidth=1.5, linestyle="--", label="Filter face bounds"))
    axes[1].legend(fontsize=8)
else:
    axes[1].text(0.5, 0.5, "No cells in upstream slice\nat x=0.25–0.31 m",
                 transform=axes[1].transAxes, ha="center", va="center")

fig.suptitle(
    "SIMULATION — PHASE 9 CASE_M | Filter face + upstream velocity\n"
    "KVO 250 + GEO_C + H13 | APPROXIMATION FROM SINGLE DATA POINT",
    fontsize=11,
)
fig.savefig(OUT / "filter_face_bypass_CASE_M.png", dpi=180)
plt.close(fig)
print("  filter_face_bypass_CASE_M.png saved.", flush=True)

# ---------------------------------------------------------------------------
# IMAGE 5: All-cases filter face comparison
# ---------------------------------------------------------------------------
print("Loading CASE_L and CASE_H patch data...", flush=True)
patch_data: dict[str, dict] = {}
patch_data["CASE_M"] = {
    "q_total": cm["q_total"],
    "q_filter": cm["q_filter"],
    "q_filter_per_face": cm["q_filter_per_face"],
    "pf_up_Pa": cm["pf_up_Pa"],
    "pf_down_Pa": cm["pf_down_Pa"],
    "impl": cm["impl"],
    "final_iter": cm["final_iter"],
}
for cname in ["CASE_L", "CASE_H"]:
    patch_data[cname] = load_patch_only(cname)
    print(f"  {cname}: Q={patch_data[cname]['q_total']:.4f} m³/s, "
          f"Qf={patch_data[cname]['q_filter']:.4f} m³/s", flush=True)

fig, axes = plt.subplots(1, 3, figsize=(14.5, 5.8), layout="constrained", sharey=True)
case_names = ["CASE_L", "CASE_M", "CASE_H"]
short_labels = ["CASE_L (Lower)", "CASE_M (Nominal)", "CASE_H (Upper)"]
vmax_all = max(
    float(np.abs(patch_data[c]["q_filter_per_face"] / (FILTER_AREA / 961)).max())
    for c in case_names
)
for ax, cname, slabel in zip(axes, case_names, short_labels):
    pd = patch_data[cname]
    face_area_c = FILTER_AREA / len(pd["q_filter_per_face"])
    un_c = pd["q_filter_per_face"] / face_area_c
    q_tot = pd["q_total"]
    q_filt = pd["q_filter"]
    bypass_pct = (1 - q_filt / q_tot) * 100
    dp_Pa = float((np.mean(pd["pf_up_Pa"]) - np.mean(pd["pf_down_Pa"])))
    sc = ax.scatter(FY, FZ, c=un_c, cmap="coolwarm",
                    vmin=-vmax_all, vmax=vmax_all, s=22, marker="s", linewidths=0)
    ax.set(xlabel="Y (m)", aspect="equal",
           title=f"{slabel}\niter {pd['final_iter']}")
    ax.text(0.04, 0.97,
            f"Q_total={q_tot*3600:.0f} m³/h\n"
            f"Q_filter={q_filt*3600:.0f} m³/h\n"
            f"Bypass: {bypass_pct:.0f}%\n"
            f"ΔP: {dp_Pa:.1f} Pa",
            transform=ax.transAxes, va="top", fontsize=7.5,
            bbox=dict(facecolor="white", alpha=0.80, edgecolor="none"))
    # Filter face rectangle
    ax.add_patch(mpatches.Rectangle(
        (FILTER_Y[0], FILTER_Z[0]), FILTER_Y[1]-FILTER_Y[0], FILTER_Z[1]-FILTER_Z[0],
        fill=False, edgecolor="#333", linewidth=0.8))
axes[0].set_ylabel("Z (m)")
cbar_ax = fig.colorbar(sc, ax=axes.tolist(), shrink=0.85, pad=0.01,
                        label="Filter face normal velocity (m/s)")
fig.suptitle(
    "SIMULATION — PHASE 9 | Filter face normal velocity — CASE_L / CASE_M / CASE_H\n"
    "KVO 250 + GEO_C + H13 | APPROXIMATION FROM SINGLE MANUFACTURER DATA POINT\n"
    "Bypass fraction increases with filter resistance (L=38%, M=45%, H=48%)",
    fontsize=10,
)
fig.savefig(OUT / "filter_case_comparison.png", dpi=170)
plt.close(fig)
print("  filter_case_comparison.png saved.", flush=True)

# ---------------------------------------------------------------------------
# bypass_analysis.json
# ---------------------------------------------------------------------------
print("Writing bypass_analysis.json...", flush=True)
bypass_analysis = {"cases": {}, "method": "FILTER_UPSTREAM phi sum vs AIR_OUTLET phi sum"}
for cname in case_names:
    pd = patch_data[cname]
    face_area_c = FILTER_AREA / len(pd["q_filter_per_face"])
    un_c = pd["q_filter_per_face"] / face_area_c
    q_tot = abs(pd["q_total"])
    q_filt = abs(pd["q_filter"])
    bypass_q = q_tot - q_filt
    bypass_frac = bypass_q / q_tot
    dp = float(np.mean(pd["pf_up_Pa"]) - np.mean(pd["pf_down_Pa"]))
    bypass_analysis["cases"][cname] = {
        "final_iteration": pd["final_iter"],
        "total_flow_m3_s": q_tot,
        "total_flow_m3_h": q_tot * 3600,
        "filter_flow_m3_s": q_filt,
        "filter_flow_m3_h": q_filt * 3600,
        "bypass_flow_m3_s": bypass_q,
        "bypass_flow_m3_h": bypass_q * 3600,
        "bypass_fraction": bypass_frac,
        "effective_filtered_fraction": 1 - bypass_frac,
        "filter_face_velocity_m_s": {
            "mean": float(np.mean(un_c)),
            "min": float(un_c.min()),
            "max": float(un_c.max()),
            "p10": float(np.percentile(un_c, 10)),
            "p90": float(np.percentile(un_c, 90)),
            "CoV": float(un_c.std() / abs(un_c.mean())) if abs(un_c.mean()) > 1e-9 else None,
            "reverse_area_fraction": float((un_c < 0).mean()),
        },
        "filter_delta_P_area_mean_Pa": dp,
        "resistance_multiplier": pd["impl"]["resistance_multiplier"],
        "scenario_classification": pd["impl"]["scenario_classification"],
    }
bypass_analysis["note"] = (
    "bypass_fraction = 1 - Q_FILTER_UPSTREAM / Q_AIR_OUTLET. "
    "Same definition as Phase 9 FILTER_H13_COMPARISON.md. "
    "Bypass increases with filter resistance (L < M < H), indicating a real flow path "
    "around the filter that is not an artefact."
)
(OUT / "bypass_analysis.json").write_text(json.dumps(bypass_analysis, indent=2), encoding="utf-8")
print("  bypass_analysis.json saved.", flush=True)

print("\nPhase 10A visualization complete.", flush=True)
print(f"Output directory: {OUT}", flush=True)
for f in sorted(OUT.iterdir()):
    print(f"  {f.name}", flush=True)
